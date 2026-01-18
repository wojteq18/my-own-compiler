import ply.lex as lex
import sys

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
    'NUMBER',
    'DIVIDE',
    'MODULO',
    'MULTIPLY',
    'ASSIGN',
    'ADD',
    'MINUS',
    'LPAREN',
    'RPAREN',
    'IF',
    'ELSE',
    'THEN',
    'ENDIF',
    'GREATER',
    'LESS',
    'EQUALSTO',
    'NOTEQUAL',
    'WHILE',
    'DO',
    'ENDWHILE',
    'BIGGEROREQUALS',
    'LESSOREQULAS',
    'FOR',
    'TO',
    'ENDFOR',
    'FROM',
    'DOWNTO',
    'REPEAT',
    'UNTIL',
    'LBRACKET',
    'RBRACKET',
    'COLON',
    'PROCEDURE',
    'T',
    'I',
    'O',

)

reserved = {
    'PROGRAM': 'PROGRAM',
    'IS': 'IS',
    'IN': 'IN',
    'READ': 'READ',
    'END': 'END',
    'WRITE': 'WRITE',
    'IF': 'IF',
    'THEN': 'THEN',
    'ELSE': 'ELSE',
    'ENDIF': 'ENDIF',
    'WHILE': 'WHILE',
    'DO': 'DO',
    'ENDWHILE': 'ENDWHILE',
    'FOR': 'FOR',
    'TO': 'TO',
    'ENDFOR': 'ENDFOR',
    'DOWNTO': 'DOWNTO',
    'FROM': 'FROM',
    'REPEAT': 'REPEAT',
    'UNTIL': 'UNTIL',
    'PROCEDURE': 'PROCEDURE',
    'T' : 'T',
    'I' : 'I',
    'O' : 'O',
}

t_ignore = ' \t'

def t_ID(t):
    r'[a-z_][a-z0-9_]*' 
    t.type = reserved.get(t.value, 'ID') 
    return t

def t_RESERVED(t):
    r'[A-Z]+'
    t.type = reserved.get(t.value, 'ID')
    if t.type == 'ID':
        sys.exit(f"Error: Unknown keyword or invalid identifier '{t.value}' at line {t.lineno}")
    return t

def t_SEMICOLON(t):
    r';'
    return t

def t_LBRACKET(t):
    r'\['
    return t

def t_RBRACKET(t):
    r'\]'
    return t

def t_ASSIGN(t):
    r':='
    return t

def t_COLON(t):
    r':'
    return t

def t_MULTIPLY(t):
    r'\*'
    return t


def t_DIVIDE(t):
    r'/'
    return t

def t_MINUS(t):
    r'-'
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

def t_BIGGEROREQUALS(t):
    r'>='
    return t

def t_LESSOREQULAS(t):
    r'<='
    return t


def t_ADD(t):
    r'\+'
    return t

def t_LESS(t):
    r'<'
    return t

def t_GREATER(t):
    r'>'
    return t

def t_EQUALSTO(t):
    r'='
    return t    

def t_NOTEQUAL(t):
    r'!='
    return t

def t_MODULO(t):
    r'%'
    return t

def t_LPAREN(t):
    r'\('
    return t

def t_RPAREN(t):
    r'\)'
    return t

def t_PROCEDURE(t):
    r'PROCEDURE'
    return t

def t_T(t):
    r'T'
    return t

def t_I(t):
    r'I'
    return t

def t_O(t):
    r'O'
    return t

def t_error(t):
    sys.exit(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)   

lexer = lex.lex()