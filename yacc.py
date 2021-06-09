import ply.yacc as yacc
from lex import tokens, reserved

precedence = (
    ('right', '='),
    ('left', 'AND', 'OR'),
    ('left', 'EQUALS'),
    ('nonassoc', '<', '>', 'GREAT_EQUAL', 'LESS_EQUAL'),
    ('left', 'ADD', 'SUBSTRACT'),
    ('left', 'MULTIPLY', 'DIVIDE'),
    ('left', 'EXP'),
)

def p_expression_binop( p ):
    '''expr : expr ADD expr
            | expr SUBSTRACT expr
            | expr MULTIPLY expr
            | expr DIVIDE expr
            | expr EXP expr'''
    if p[2] == '+'  : p[0] = p[1] + p[3]
    elif p[2] == '-': p[0] = p[1] - p[3]
    elif p[2] == '*': p[0] = p[1] * p[3]
    elif p[2] == '/': p[0] = p[1] / p[3]
    elif p[2] == '^': p[0] = p[1] ** p[3]

def p_parens( p ):
    'parens : LPAREN condition RPAREN'
    p[0] = p[2]

def p_braces( p ):
    'braces : LBRACE statement RBRACE'
    p[0] = p[2]
    return p[0]

def p_special_statement( p ):
        ''' special_statement : parens braces'''
        p[0] = (p[1], p[2])

def p_expression_to_number( p ) :
    'num : NUMBER'
    p[0] = p[1]
    return p[0]

def p_conditional( p ):
    '''expr : IF special_statement
            | IF special_statement ELSE braces
            | IF special_statement elif ELSE braces'''
    
    if len(p) == 3:
        p[0] = (p[1], p[2], None, None)
    elif len(p) == 5:
        p[0] = (p[1], p[2], None, (p[3], p[4]))
    else:
        p[0] = (p[1], p[2], p[3], (p[4], p[5]))

def p_elif( p ):
    '''elif : ELIF special_statement
            | elif ELIF special_statement '''
    
    if p[1] == 'elif':
        p[0] = ((p[1], p[2][0], p[2][1]),)
    else:
        p[0] = p[1] + ((p[2], p[3][0], p[3][1]),)

def p_iteration( p ):
    ''' iter : WHILE parens '''

def p_error( p ):
    print("Syntax error at '%s'" % p.value)

data = '''
3 + 4 * 10
'''

parser = yacc.yacc()

res = parser.parse(data)
print(res)