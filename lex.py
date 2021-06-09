from ply import lex

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
    'LBRACE',
    'RBRACE',
    'SEMICOLON',
    'ID',
)

reserved = {
   'if' : 'IF',
   'elif' : 'ELIF',
   'else' : 'ELSE',
   'then' : 'THEN',
   'while' : 'WHILE',
   'do' : 'DO',
   'for' : 'FOR',
   'and' : 'AND',
   'or' : 'OR',
   'true' : 'TRUE',
   'false' : 'FALSE',
   'int' : 'INTEGER',
   'float' : 'FLOAT',
   'boolean' : 'BOOLEAN',
   'string' : 'STRING',
}

t_ADD = r'\+'
t_SUBSTRACT = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_EXP = r'\^'
t_EQUAL = r'\=\='
t_NOT_EQUAL = r'\!\='
t_GREATER = r'\>'
t_LESS = r'\<'
t_GREATER_EQUAL = r'\>\='
t_LESS_EQUAL = r'\<\='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_SEMICOLON = r'\;'
t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_NUMBER = r'\d+'

t_ignore = '\t'

def t_id( t ):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_number( t ):
    r'\d+'
    try:
        t.lexer.num_count += 1
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_error( t ):
    print("Error: %s \n" % t.value[0])
    t.lexer.skip(1)

'''
def t_eof(t):
    more = input('Add more input? If so: \n')
    if more:
        lexer.input(more)
        return lexer.token()
    
    return None
'''

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