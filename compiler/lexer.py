import ply.lex as lex

tokens = (
    'PROGRAM',
    'IS',
    'IN',
    'READ',
    'END',
    'ID',
    'SEMICOLON',
    'WRITE',
    'COMMA',
)

reserved = {
    'PROGRAM': 'PROGRAM',
    'IS': 'IS',
    'IN': 'IN',
    'READ': 'READ',
    'END': 'END',
    'WRITE': 'WRITE',
}

t_ignore = ' \t'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value.upper(), 'ID')  # Sprawdź czy to słowo kluczowe
    return t

def t_SEMICOLON(t):
    r';'
    return t

def t_COMMA(t):
    r','
    return t

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