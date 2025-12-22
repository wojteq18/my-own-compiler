import ply.yacc as yacc
from lexer import tokens

free_memory_address = 0
symbols_table = {}

def get_addr(variable_name): #Przyporządkowuje unikalny adres w pamięci dla zmiennej
    global free_memory_address
    if variable_name not in symbols_table:
        symbols_table[variable_name] = free_memory_address
        free_memory_address += 1
    return symbols_table[variable_name]

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
    addr = get_addr(variable_name)
    p[0] = f"READ\nSTORE {addr}\n"

def p_commands_write(p):
    'command : WRITE ID SEMICOLON'
    variable_anme = p[2]
    if variable_anme not in symbols_table:
        print(f"Error: Variable '{variable_anme}' not declared.")
        p[0] = ""
        return
    else:
        addr = symbols_table[variable_anme]
    p[0] = f"LOAD {addr}\nWRITE\n"


def p_variable_declaration(p):
    'declarations : ID'
    var_name = p[1]
    addr = get_addr(var_name)
    print(f"Zmienna {p[1]} zarejestrowana pod adresem {addr}") 

def p_error(p):
    print("Error in syntax!")   
             
parser = yacc.yacc()
