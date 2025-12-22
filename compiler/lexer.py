import ply.lex as lex

tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
)

t_PLUS   = r'\+'
t_MINUS  = r'\-'
t_ignore = ' \t'

def t_COMMENT(t):
    r'\#.*'
    pass  # Ignoruj komentarze

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t 

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)   

lexer = lex.lex()