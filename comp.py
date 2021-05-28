from ply import lex
import ply.yacc as yacc

tokens = (
    'ADD',
    'SUBSTRACT',
    'MULTIPLY',
    'DIVIDE',
    'EXP',
    'EQUAL',
    'NOT_EQUAL',
    'GREATER',
    'LESS',
    'GREATER_EQUAL',
    'LESS_EQUAL',
    'AND',
    'OR',
    'NUMBER',
    'LPAREN',
    'RPAREN',
    'LBRACES',
    'RBRACES',
)

precedence = (
    ('left', 'ADD', 'SUBSTRACT'),
    ('left', 'MULTIPLY', 'DIVIDE'),
    ('left', 'EXP')
)

reserved = {
   'if' : 'IF',
   'then' : 'THEN',
   'else' : 'ELSE',
   'while' : 'WHILE',
   
}

t_ADD = r'\+'
t_SUBSTRACT = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_EXP = r'\*\*'
t_EQUAL = r'\=\='
t_NOT_EQUAL = r'\!\='
t_GREATER = r'\>'
t_LESS = r'\<'
t_GREATER_EQUAL = r'\>\='
t_LESS_EQUAL = r'\<\='
t_AND = r'\&\&'
t_OR = r'\|\|'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACES  = r'\{'
t_RBRACES  = r'\}'

t_ignore = ' \t'

def t_number( op ):
    r'[0-9]+'
    op.lexer.num_count += 1
    op.value = int(op.value)
    return op

def t_add( op ) :
    'expr : expr ADD expr'
    op[0] = op[1] + op[3]

def t_substract( op ) :
    'expr : expr SUBSTRACT expr'
    op[0] = op[1] - op[3]

def t_mult_div( op ) :
    '''expr : expr TIMES expr
            | expr DIV expr'''

    if op[2] == '*' :
        op[0] = op[1] * op[3]
    else :
        if op[3] == 0 :
            print("Can't divide by 0")
            raise ZeroDivisionError('integer division by 0')
        op[0] = op[1] / op[3]

def t_exp( op ):
    'expr : expr EXP expr'
    op[0] = op[1] ** op[3]

def t_parens( op ):
    'expr: LPAREN expr RPAREN'
    op[0] = op[2]

def t_expt_to_number( op ) :
    'expr : NUMBER'
    op[0] = op[1]

def t_error( op ):
    print("Error: \n", op.value[0], "\n")
    op.lexer.skip(1)

data = '''
3 + 4 * 10
'''

lexer = lex.lex()
lexer.num_count = 0
lexer.input(data)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)

parser = yacc.yacc()

res = parser.parse(data)
print(res)