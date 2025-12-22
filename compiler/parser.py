import ply.yacc as yacc
from lexer import tokens

def p_statement_expr(p):
    'statement : expression'
    p[0] = p[1]

def p_statement_empty(p):
    'statement : '
    p[0] = None

def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = p[1] + p[3]

def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = p[1] - p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_number(p):
    'term : NUMBER'
    p[0] = p[1]    

def p_error(p):
    print("Error in syntax!")        

parser = yacc.yacc()
