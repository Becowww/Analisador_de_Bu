import ply.lex as lex
import ply.yacc as yacc

# Lista de tokens
tokens = ('IDENTIFIER', 'NUMBER', 'OPERATOR', 'RESERVED', 'SEPARATOR')

# Palavras reservadas
reserved = {
    'int': 'RESERVED',
    'float': 'RESERVED',
    'if': 'RESERVED',
    'else': 'RESERVED'
}

# Caracteres literais (operadores e separadores)
literals = ['+', '-', '*', '/', '=', ';', '(', ')', '{', '}']

# Expressões regulares para tokens simples
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')  # Verifica se é palavra reservada
    return t

def t_NUMBER(t):
    r'-?\d+(\.\d+)?'
    return t

def t_OPERATOR(t):
    r'[+\-*/=<>!]=?|=='
    return t

def t_SEPARATOR(t):
    r'[;{}()]'
    return t

t_ignore = ' \t'  

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Erro Léxico: Caractere inválido '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)


lexer = lex.lex()

# Variável global para erros sintáticos
syntax_error = False

# Definição da gramática
def p_program(p):
    """program : statement_list"""
    global syntax_error
    if syntax_error == False:
        print("A expressão foi aceita na análise sintática.")

def p_statement_list(p):
    """statement_list : statement
                      | statement statement_list"""
    pass  # Permite múltiplas instruções em sequência

def p_statement_declaration(p):#declaração
    """statement : RESERVED IDENTIFIER OPERATOR expression SEPARATOR"""
    
    # Verifica se o operador usado na declaração é '='
    if p[3] != '=' or p[5] != ';':
        global syntax_error
        syntax_error = True

def p_statement_assignment(p): #atribuição
    """statement : IDENTIFIER OPERATOR term OPERATOR term SEPARATOR
                 | IDENTIFIER OPERATOR term SEPARATOR"""
    pass


def p_statement_condition(p): # Estruturas condicionais if-else
    """statement : RESERVED SEPARATOR expression SEPARATOR block
                 | RESERVED SEPARATOR expression SEPARATOR block RESERVED block
                 | RESERVED SEPARATOR expression SEPARATOR block RESERVED statement""" 
    pass


def p_block(p):
    """block : SEPARATOR statement_list SEPARATOR
             | SEPARATOR SEPARATOR"""
    pass  

def p_expression_comparison(p): #expressão de uma comparação
    """expression : term
                  | term comparison_operator term"""
    pass

def p_term(p): #Permite ler numeros e variáveis negativas
    """term : IDENTIFIER
            | NUMBER
            | OPERATOR IDENTIFIER
            | OPERATOR NUMBER"""
    if len(p) == 3 and p[1] == '-':
        pass  

def p_comparison_operator(p): #Verificando se os operadores de comparação estão corretos
    """comparison_operator : OPERATOR"""
    if p[1] not in ['==', '>', '<', '>=', '<=', '!=']:
        global syntax_error
        if syntax_error == False:
            syntax_error = True
            print("Erro de sintaxe encontrado. Fim inesperado do código.")
            

def p_error(p):
    global syntax_error
    if syntax_error == False:
            syntax_error = True
            print("Erro de sintaxe encontrado. Fim inesperado do código.")
            


parser = yacc.yacc()


def analyze(code):
    global syntax_error
    syntax_error = False  

    lexer.input(code)
    print("== Análise Léxica ==")
    for tok in lexer:
        print((tok.type, tok.value))
    print("\n== Análise Sintática ==")
    parser.parse(code)

# Entradas:
code = "y = y * 3.5;"
analyze(code)
