from lex import Lexer
from yacc import Yaccer

def run(sample):
    le = Lexer()
    ya = Yaccer()

    try:
        parser = ya.build()
        result = parser.parse(sample)
        print(result)
    except:
        print("Error in execution")

data = '''
3 + 4 * 10
'''

run(data)