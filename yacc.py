import ply.yacc as yacc
from lex import Lexer

class Symbol:

    def __init__(self, name, type, declaration_pos, value=None, init_pos=None):
        self.name = name
        self.type = type.upper()
        self.declaration_pos = declaration_pos
        self.value = value
        self.init_pos = init_pos

    def initialized(self):
        return self.init_pos is not None


class Yaccer:

    tokens = Lexer.tokens
    start = 'prog'
    precedence = (
        ('left', 'ADD', 'SUBSTRACT'),
        ('left', 'MULTIPLY', 'DIVIDE'),
        ('left', 'EXP'),
    )

    def __init__(self):
        self.errors = []
        self.lexer = Lexer()
        self.lexer = self.lexer.build()
        self.symbol_table = {}

    def p_prog(self, p):
        ''' prog : prog expression
                 | expression '''
        if len(p) == 3 and p[2][0] is not None:
            p[0] = p[1] + (p[2],)
        else:
            p[0] = (p[1],)

    def p_type(self, p):
        ''' type : INTEGER
                 | FLOAT
                 | STRING
                 | BOOLEAN '''
        p[0] = p[1]

    def p_expression(self, p):
        '''expression : closing
                      | conditional
                      | iteration '''
        p[0] = p[1]

    def p_expression_binop(self, p):
        '''operation : operation ADD operation
                     | operation SUBSTRACT operation
                     | operation MULTIPLY operation
                     | operation DIVIDE operation
                     | operation EXP operation 
                     | boolean_operation'''

        if   p[2] == '+' : p[0] = p[1] + p[3]
        elif p[2] == '-' : p[0] = p[1] - p[3]
        elif p[2] == '*' : p[0] = p[1] * p[3]
        elif p[2] == '/' : p[0] = p[1] / p[3]
        elif p[2] == '^' : p[0] = p[1] ** p[3]

    def p_boolean_op(self, p):
        '''boolean_operation : operation EQUAL operation
                             | operation NOT_EQUAL operation
                             | operation GREATER operation
                             | operation LESS operation 
                             | operation GREATER_EQUAL operation
                             | operation LESS_EQUAL operation'''
        
        if   p[2] == '==': p[0] = p[1] == p[3]
        elif p[2] == '!=': p[0] = p[1] != p[3]
        elif p[2] == '>' : p[0] = p[1] > p[3]
        elif p[2] == '<' : p[0] = p[1] < p[3]
        elif p[2] == '>=': p[0] = p[1] >= p[3]
        elif p[2] == '<=': p[0] = p[1] <= p[3]

    def p_declaration(self, p):
        ''' declaration : type ID
                        | type ID EQUAL num
                        | type ID EQUAL bool
                        | type ID EQUAL operation'''
    '''if p[2] in self.symbol_table:'''

    def p_parens(self, p):
        '''parens : LPAREN boolean_operation RPAREN
                  | LPAREN boolean_operation OR boolean_operation RPAREN
                  | LPAREN boolean_operation AND boolean_operation RPAREN
                  | LPAREN parens OR parens RPAREN
                  | LPAREN parens AND parens RPAREN'''
        p[0] = p[2]

    def p_braces(self, p):
        'braces : LBRACE statement RBRACE'
        p[0] = p[2]

    def p_special_statement(self, p):
            ''' special_statement : parens braces'''
            p[0] = (p[1], p[2])

    def p_number(self, p) :
        'num : NUMBER'
        p[0] = p[1]
        return p[0]

    def p_boolean(self, p):
        '''bool : TRUE 
                | FALSE'''

    def p_conditional(self, p):
        '''conditional : IF special_statement
                        | IF special_statement ELSE braces
                        | IF special_statement elif ELSE braces'''
        
        if len(p) == 3:
            p[0] = (p[1], p[2], None, None)
        elif len(p) == 5:
            p[0] = (p[1], p[2], None, (p[3], p[4]))
        else:
            p[0] = (p[1], p[2], p[3], (p[4], p[5]))

    def p_elif(self, p):
        '''elif : ELIF special_statement
                | elif ELIF special_statement '''
        
        if p[1] == 'elif':
            p[0] = ((p[1], p[2][0], p[2][1]),)
        else:
            p[0] = p[1] + ((p[2], p[3][0], p[3][1]),)

    def p_iteration(self, p):
        ''' iteration : WHILE parens 
                      | DO braces WHILE parens
                      | FOR LPAREN for_declaration for_operation RPAREN braces
                      | FOR LPAREN for_declaration for_operation operation RPAREN braces'''
        
        if p[1] == "while":
            p[0] = (p[1], p[2])
        elif p[1] == "do":
            p[0] = (p[1], p[2], p[4])
        elif p[1] == "for" and p[5] == ')':
            p[0] = (p[1], p[3], p[4], None, p[6])
        elif p[1] == "for":
            p[0] = (p[1], p[3], p[4], p[5], p[7])

    def p_for_decl(self, p):
        '''for_declaration : SEMICOLON
                            | declaration SEMICOLON'''

        if p[1] != ";":
            p[0] = p[1]

    def p_for_op(self, p):
        '''for_operation : SEMICOLON
                        | operation SEMICOLON'''

        if p[1] != ";":
            p[0] = p[1]

    def p_closing_statement(self, p):
        ''' closing : SEMICOLON
                    | statement SEMICOLON '''
        if p[1] != ";":
            p[0] = p[1]

    def p_statement(self, p):
        ''' statement : operation
                      | declaration 
                      | conditional'''
        p[0] = p[1]

    def p_error(self, p):
        if p:
            self.errors.append(
                "Syntax error: Symbol {}; line {}".format(p.value, p.lineno))
        else:
            self.errors.append(
                "Unexpected EOF")

    
    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)
        return self.parser