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

t_ignore = ' \t'  # Ignorar espaços e tabulações

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Erro Léxico: Caractere inválido '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

# Construção do analisador léxico
lexer = lex.lex()

# Variável global para erros sintáticos
syntax_error = False

# Definição da gramática
def p_program(p):
    """program : statement_list"""
    global syntax_error
    if not syntax_error:
        print("A expressão foi aceita na análise sintática.")

def p_statement_list(p):
    """statement_list : statement
                      | statement statement_list"""
    pass  # Permite múltiplas instruções em sequência

def p_statement_declaration(p):
    """statement : RESERVED IDENTIFIER OPERATOR NUMBER SEPARATOR"""
    pass

def p_statement_assignment(p):
    """statement : IDENTIFIER OPERATOR IDENTIFIER OPERATOR NUMBER SEPARATOR
                 | IDENTIFIER OPERATOR IDENTIFIER OPERATOR IDENTIFIER SEPARATOR
                 | IDENTIFIER OPERATOR NUMBER SEPARATOR"""
    pass

# Estruturas condicionais if-else
def p_statement_condition(p):
    """statement : RESERVED SEPARATOR expression SEPARATOR block
                 | RESERVED SEPARATOR expression SEPARATOR block RESERVED block
                 | RESERVED SEPARATOR expression SEPARATOR block RESERVED statement"""
    pass  # Agora aceita if-else corretamente


# Blocos entre chaves {}
def p_block(p):
    """block : SEPARATOR statement_list SEPARATOR
             | SEPARATOR SEPARATOR"""
    pass  # Blocos vazios {} são permitidos

def p_expression_comparison(p):
    """expression : IDENTIFIER comparison_operator IDENTIFIER
                  | IDENTIFIER comparison_operator NUMBER"""
    pass

def p_comparison_operator(p):
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

# Construção do analisador sintático
parser = yacc.yacc()

# Teste
def analyze(code):
    global syntax_error
    syntax_error = False  # Resetando variável de erro

    lexer.input(code)
    print("== Análise Léxica ==")
    for tok in lexer:
        print((tok.type, tok.value))
    print("\n== Análise Sintática ==")
    parser.parse(code)

# Exemplo de entrada
code = "z = y * -1;"
analyze(code)
