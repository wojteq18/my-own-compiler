import ply.yacc as yacc
from lexer import tokens
from compiler_utils import get_addr, symbols_table, free_memory_address, get_array_addr, procedures_table
import sys
from register_manager import reg_manager
from abstract_syntax_tree import AssignmentNode, CallNode, NumberNode, BinaryOperationNode, ProcedureNode, ReadNode, VariableNode, WhileNode, WriteNode, ArrayElementNode, IfNode, ConditionNode, ForNodeTo, ForNodeDownTo, RepeatNode
from code_buffer import CodeBuffer

current_scope = "main"

precedence = (
    ('left', 'ADD', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE', 'MODULO'),
)

def p_program_all(p):
    'program : procedures main'
    buffer = CodeBuffer()
    buffer.add_instr("JUMP LABEL_MAIN")
    for proc_node in p[1]:
        proc_node.generate(buffer)
    buffer.set_label("MAIN")
    for cmd in p[2]:
        cmd.generate(buffer)
    buffer.add_instr("HALT")
    p[0] = buffer.finalize()

def p_procedures_multiple(p):
    '''procedures : procedures PROCEDURE proc_head IS declarations IN commands END
                  | procedures PROCEDURE proc_head IS IN commands END'''
    name, params = p[3]
    commands = p[7] if len(p) == 9 else p[6]
    node = ProcedureNode(name, params, commands)
    global current_scope
    current_scope = "main"
    p[0] = p[1] + [node]

def p_procedures_empty(p):
    'procedures : '
    p[0] = []    

def p_proc_head(p):
    'proc_head : ID LPAREN args_decl RPAREN'
    name, params = p[1], p[3]
    if name in procedures_table:
        sys.exit(f"Error: Procedure {name} already defined") 
    global current_scope
    current_scope = name
    param_addrs = []
    for i, (p_name, p_type) in enumerate(params):
        full_name = f"{current_scope}_{p_name}"
        addr = get_addr(full_name)
        symbols_table[full_name]['is_param'] = True
        symbols_table[full_name]['param_type'] = p_type
        param_addrs.append(addr)
    procedures_table[name] = {'args_count': len(params), 'params': params, 'param_addrs': param_addrs}
    p[0] = (name, params)  

def p_args_decl_multi(p):
    'args_decl : args_decl COMMA arg_type ID'
    p[0] = p[1] + [(p[4], p[3])] 

def p_args_decl_single(p):
    'args_decl : arg_type ID'
    p[0] = [(p[2], p[1])]     

def p_arg_type(p):
    '''arg_type : T I O
                | T I
                | T O
                | T
                | I
                | O
                | empty'''
    p[0] = "".join([str(x) for x in p[1:] if x is not None]) 

def p_main_node(p):
    '''main : PROGRAM IS declarations IN commands END
            | PROGRAM IS IN commands END'''
    p[0] = p[5] if len(p) == 7 else p[4]   

def p_proc_call(p):
    'command : ID LPAREN args RPAREN SEMICOLON'
    name, args = p[1], p[3]
    if name not in procedures_table:
        sys.exit(f"Błąd: Nieznana procedura {name}") 
    if len(args) != procedures_table[name]['args_count']:
        sys.exit(f"Błąd: Zła liczba argumentów w {name}")
    p[0] = CallNode(name, args)    

def p_args_multi(p):
    'args : args COMMA ID'
    p[0] = p[1] + [VariableNode(f"{current_scope}_{p[3]}")]    

def p_args_single(p):
    'args : ID'
    p[0] = [VariableNode(f"{current_scope}_{p[1]}")]    

def p_empty(p):
    'empty :'
    p[0] = None             

def p_commands_multiple(p):
    'commands : commands command'
    p[0] = p[1] + [p[2]]

def p_commands_single(p):
    'commands : command'
    p[0] = [p[1]]   

def p_command_read(p):
    'command : READ identifier SEMICOLON'
    p[0] = ReadNode(p[2])

def p_command_write(p):
    'command : WRITE value SEMICOLON'
    p[0] = WriteNode(p[2])

def p_value_num(p):
    'value : NUMBER'
    p[0] = NumberNode(p[1])

def p_value_id(p): 
    'value : identifier'
    p[0] = p[1]       

def p_variable_declaration_single(p):
    'declarations : ID'
    get_addr(f"{current_scope}_{p[1]}")

def p_assign_command(p):
    'command : identifier ASSIGN expression SEMICOLON'
    p[0] = AssignmentNode(p[1], p[3])

def p_expression_value(p):
    'expression : value'
    p[0] = p[1]

def p_variable_declaration_multiple(p):
    'declarations : declarations COMMA ID'
    get_addr(f"{current_scope}_{p[3]}")

def p_expression_addition(p):
    'expression : expression ADD expression'
    p[0] = BinaryOperationNode(p[1], 'ADD', p[3])

def p_expression_minus(p):
    'expression : expression MINUS expression'
    p[0] = BinaryOperationNode(p[1], 'MINUS', p[3])

def p_expression_multiply(p):
    'expression : expression MULTIPLY expression'
    p[0] = BinaryOperationNode(p[1], 'MULTIPLY', p[3]) 

def p_expression_if(p):
    'command : IF condition THEN commands ELSE commands ENDIF'
    p[0] = IfNode(p[2], p[4], p[6])

def p_expression_if_no_else(p):
    'command : IF condition THEN commands ENDIF'
    p[0] = IfNode(p[2], p[4]) 

def p_expression_while(p):
    'command : WHILE condition DO commands ENDWHILE'
    p[0] = WhileNode(p[2], p[4])  

def p_command_forto(p):
    'command : for_iterator FROM value TO value DO commands ENDFOR' 
    p[0] = ForNodeTo(p[1], p[3], p[5], p[7]) 

def p_command_repeatuntil(p):
    'command : REPEAT commands UNTIL condition SEMICOLON'
    p[0] = RepeatNode(p[2], p[4])

def p_for_iterator(p):
    'for_iterator : FOR ID'
    full_name = f"{current_scope}_{p[2]}"
    if full_name not in symbols_table:
        get_addr(full_name)
    p[0] = full_name        

def p_command_fordownto(p):
    'command : for_iterator FROM value DOWNTO value DO commands ENDFOR' 
    p[0] = ForNodeDownTo(p[1], p[3], p[5], p[7])    

def p_condition_less(p):
    'condition : expression LESS expression'
    p[0] = ConditionNode(p[1], '<', p[3])

def p_condition_greater(p):
    'condition : expression GREATER expression'
    p[0] = ConditionNode(p[1], '>', p[3])

def p_condition_equalsto(p):
    'condition : expression EQUALSTO expression'
    p[0] = ConditionNode(p[1], '=', p[3])

def p_condition_notequal(p):
    'condition : expression NOTEQUAL expression'
    p[0] = ConditionNode(p[1], '!=', p[3])    

def p_condition_biggerorequals(p):
    'condition : expression BIGGEROREQUALS expression'
    p[0] = ConditionNode(p[1], '>=', p[3])   

def p_condition_LESSOREQULAS(p):
    'condition : expression LESSOREQULAS expression'
    p[0] = ConditionNode(p[1], '<=', p[3])         

def p_expression_divide(p):
    'expression : expression DIVIDE expression'
    p[0] = BinaryOperationNode(p[1], 'DIVIDE', p[3])

def p_expression_modulo(p):
    'expression : expression MODULO expression'
    p[0] = BinaryOperationNode(p[1], 'MODULO', p[3])           
   
def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_variable_declaration_array(p):
    '''declarations : ID LBRACKET NUMBER COLON NUMBER RBRACKET
                    | declarations COMMA ID LBRACKET NUMBER COLON NUMBER RBRACKET'''
    if len(p) == 7:
        get_array_addr(f"{current_scope}_{p[1]}", p[3], p[5]) 
    else: 
        get_array_addr(f"{current_scope}_{p[3]}", p[5], p[7]) 

def p_identifier_simple(p):
    'identifier : ID'
    full_name = f"{current_scope}_{p[1]}"
    if full_name not in symbols_table:
        sys.exit(f"Error: Variable '{p[1]}' not declared in scope {current_scope}") 
    p[0] = VariableNode(full_name)

def p_identifier_array_var(p):
    'identifier : ID LBRACKET ID RBRACKET'
    full_name_arr = f"{current_scope}_{p[1]}"
    full_name_idx = f"{current_scope}_{p[3]}"
    if full_name_arr not in symbols_table:
        sys.exit(f"Error: Array '{p[1]}' not declared") 
    if full_name_idx not in symbols_table:
        sys.exit(f"Error: Index variable '{p[3]}' not declared") 
    p[0] = ArrayElementNode(full_name_arr, VariableNode(full_name_idx))

def p_identifier_array_num(p):
    'identifier : ID LBRACKET NUMBER RBRACKET'
    full_name_arr = f"{current_scope}_{p[1]}"
    if full_name_arr not in symbols_table:
        sys.exit(f"Error: Array '{p[1]}' not declared") 
    p[0] = ArrayElementNode(full_name_arr, NumberNode(p[3]))        

def p_error(p):
    if p:
        print(f"Error in syntax in line {p.lineno} at token {p.value}")      
    else:
        print("Error in syntax at EOF")

parser = yacc.yacc()