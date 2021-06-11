from ply import lex


class Lexer:

    def __init__(self):
        self.errors = []

    
    reserved = {
    'if' : 'IF',
    'elif' : 'ELIF',
    'else' : 'ELSE',
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

    literals = ['=', '+', '-', '*', '/', '^',
                ">", "<", '(', ')', '{', '}', ';']

    tokens = [
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
    ] + list(reserved.values())

    t_ADD = r'\+'
    t_SUBSTRACT = r'\-'
    t_MULTIPLY = r'\*'
    t_DIVIDE = r'/'
    t_EXP = r'\^'
    t_EQUAL = r'=='
    t_NOT_EQUAL = r'!='
    t_GREATER = r'\>'
    t_LESS = r'\<'
    t_GREATER_EQUAL = r'>='
    t_LESS_EQUAL = r'<='
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_LBRACE  = r'\{'
    t_RBRACE  = r'\}'
    t_SEMICOLON = r'\;'
    t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    t_NUMBER = r'[0-9]+'

    t_ignore = ' \t'
    t_ignore_COMMENT = r'\/\/.*'

    def t_id(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = reserved.get(t.value, 'ID')
        return t

    def t_int(self, t):
        r'[0-9]+'
        t.value = int(t.value)
        return t

    def t_float(self, t):
        r'[0-9]*\.[0-9]+'
        t.value = float(t.value)
        return t

    def t_string(self, t):
        r'".*"'
        return t

    def t_newline(self, t):
        r'\n+|\r+|(\r\n)+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print("Error: %s \n" % t.value[0])
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer

'''
def t_eof(t):
    more = input('Add more input? If so: \n')
    if more:
        lexer.input(more)
        return lexer.token()
    
    return None
'''

'''lexer.num_count = 0
lexer.input(data)'''

'''while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)'''