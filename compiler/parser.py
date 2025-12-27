import ply.yacc as yacc
from lexer import tokens
from compiler_utils import get_addr, symbols_table, free_memory_address, generate_number
import sys
from register_manager import RegisterManager, reg_manager

precedence = (
    ('left', 'ADD', 'MINUS'),
)

def p_program(p):
    'program : PROGRAM IS declarations IN commands END'
    final_code = p[5] + "HALT"
    p[0] = final_code
    print("Generated Code:")
    print(final_code)

def p_commands_multiple(p):
    'commands : commands command'
    p[0] = p[1] + p[2]

def p_commands_single(p):
    'commands : command'
    p[0] = p[1]   

def p_commandd_read(p):
    'command : READ ID SEMICOLON'
    variable_name = p[2]
    if variable_name not in symbols_table:
        sys.exit(f"Error: Variable '{variable_name}' not declared in line {p.lineno(2)}")
        p[0] = ""
        return
    else:
        addr = symbols_table[variable_name]
    p[0] = f"READ\nSTORE {addr}\n"

def p_commands_write(p):
    'command : WRITE ID SEMICOLON'
    variable_anme = p[2]
    if variable_anme not in symbols_table:
        sys.exit(f"Error: Variable '{variable_anme}' not declared in line {p.lineno(2)}")
        p[0] = ""
        return
    else:
        addr = symbols_table[variable_anme]
    p[0] = f"LOAD {addr}\nWRITE\n"


def p_variable_declaration_single(p):
    'declarations : ID'
    var_name = p[1]
    addr = get_addr(var_name)
    print(f"Zmienna {p[1]} zarejestrowana pod adresem {addr}") 

def p_assign_command(p):
    'command : ID ASSIGN expression SEMICOLON'
    variable_name = p[1]
    if variable_name not in symbols_table:
        sys.exit(f"Error: Variable '{variable_name}' not declared in line {p.lineno(1)}")
        p[0] = ""
        return
    else:
        addr = symbols_table[variable_name]
    p[0] = f"{p[3]}STORE {addr}\n"  

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = generate_number(p[1])  

def p_expression_variable(p):
    'expression : ID'
    variable_name = p[1]
    if variable_name not in symbols_table:
        sys.exit(f"Error: Variable '{variable_name}' not declared in line {p.lineno(1)}")
        p[0] = ""
        return
    else:
        addr = symbols_table[variable_name]
    p[0] = f"LOAD {addr}\n"  # Ładuje wartość zmiennej na stos    


def p_variable_declaration_multiple(p):
    'declarations : declarations COMMA ID'
    var_name = p[3]
    addr = get_addr(var_name)
    print(f"Zmienna {p[3]} zarejestrowana pod adresem {addr}") 

def p_expression_addition(p):
    'expression : expression ADD expression'
    register = reg_manager.get_register()

    code = p[1]
    code += f"SWP {register}\n"       
    code += p[3]
    code += f"ADD {register}\n"
    p[0] = code

def p_expression_minus(p):
    'expression : expression MINUS expression'
    register = reg_manager.get_register()

    code = p[1]
    code += f"SWP {register}\n"       
    code += p[3]
    code += f"SWP {register}\n"
    code += f"SUB {register}\n"
    p[0] = code    

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_error(p):
    print(f"Error in syntax in line {p.lineno}")   
             
parser = yacc.yacc()
