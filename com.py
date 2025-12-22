import ply.lex as lex
import ply.yacc as yacc

# --- CZĘŚĆ 1: LEXER (Analiza leksykalna) ---
# Tokeny to najmniejsze "słowa", które rozumie nasz język.

# Lista nazw tokenów - jest wymagana przez PLY
tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
)

# Reguły (wyrażenia regularne) dla prostych tokenów
t_PLUS  = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'

# Reguła dla liczb (z konwersją na int)
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignorowanie spacji i tabulacji
t_ignore = ' \t'

# Obsługa błędów leksykalnych (nieznane znaki)
def t_error(t):
    print(f"Nielegalny znak: {t.value[0]}")
    t.lexer.skip(1)

# Budujemy lexer
lexer = lex.lex()

# --- CZĘŚĆ 2: PARSER (Analiza składniowa) ---
# Tutaj definiujemy gramatykę, czyli jak tokeny mogą się łączyć.

def p_expression_plus(p):
    'expression : expression PLUS term'
    # p[0] to wynik, p[1] to pierwszy element, p[2] to operator, p[3] to drugi element
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

# Obsługa błędów składniowych
def p_error(p):
    print("Błąd składniowy w tekście!")

# Budujemy parser
parser = yacc.yacc()

# --- CZĘŚĆ 3: URUCHOMIENIE ---

if __name__ == "__main__":
    print("Prosty kalkulator PLY (wpisz np. 10 + 5 - 2). Wpisz 'exit' by wyjść.")
    while True:
        try:
            s = input('kalkulator > ')
        except EOFError:
            break
        if s.lower() == 'exit':
            break
        if not s:
            continue
        result = parser.parse(s)
        print(f"Wynik: {result}")