import ply.yacc as yacc
from lexer import tokens
from compiler_utils import get_addr, symbols_table, free_memory_address, generate_number
import sys
from register_manager import reg_manager
from abstract_syntax_tree import AssignmentNode, NumberNode, BinaryOperationNode, ReadNode, VariableNode, WhileNode, WriteNode, IfNode, ConditionNode
from code_buffer import CodeBuffer

precedence = (
    ('left', 'ADD', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE', 'MODULO'),
)

def p_program(p):
    'program : PROGRAM IS declarations IN commands END'
    buffer = CodeBuffer()
    for cmd in p[5]:
        cmd.generate(buffer)

    buffer.add_instr("HALT")
    p[0] = buffer.finalize()    

def p_commands_multiple(p):
    'commands : commands command'
    p[0] = p[1] + [p[2]]

def p_commands_single(p):
    'commands : command'
    p[0] = [p[1]]   

def p_command_read(p):
    'command : READ ID SEMICOLON'
    if p[2] not in symbols_table:
        sys.exit(f"Error: Variable '{p[2]}' not declared")
    p[0] = ReadNode(p[2])

def p_command_write(p):
    'command : WRITE value SEMICOLON'
    p[0] = WriteNode(p[2])

def p_value_num(p):
    'value : NUMBER'
    p[0] = NumberNode(p[1])

def p_value_id(p): 
    'value : ID'
    if p[1] not in symbols_table:
        sys.exit(f"Error: Variable '{p[1]}' not declared")
    p[0] = VariableNode(p[1])       


def p_variable_declaration_single(p):
    'declarations : ID'
    var_name = p[1]
    addr = get_addr(var_name)
    print(f"Zmienna {p[1]} zarejestrowana pod adresem {addr}") 

def p_assign_command(p):
    'command : ID ASSIGN expression SEMICOLON'
    if p[1] not in symbols_table:
        sys.exit(f"Error: Variable '{p[1]}' not declared")
    p[0] = AssignmentNode(p[1], p[3])


def p_expression_number(p):
    'expression : NUMBER'
    p[0] = NumberNode(p[1]) 

def p_expression_variable(p):
    'expression : ID'
    p[0] = VariableNode(p[1])   


def p_variable_declaration_multiple(p):
    'declarations : declarations COMMA ID'
    var_name = p[3]
    addr = get_addr(var_name)
    print(f"Zmienna {p[3]} zarejestrowana pod adresem {addr}") 

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

def p_expression_divide(p):
    'expression : expression DIVIDE expression'
    p[0] = BinaryOperationNode(p[1], 'DIVIDE', p[3])

def p_expression_modulo(p):
    'expression : expression MODULO expression'
    p[0] = BinaryOperationNode(p[1], 'MODULO', p[3])           
   
def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_error(p):
    print(f"Error in syntax in line {p.lineno}")      
             
parser = yacc.yacc()
