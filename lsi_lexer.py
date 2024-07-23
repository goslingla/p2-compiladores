import os
import sys
from sly import Lexer

class LSILexer(Lexer):
    tokens = { DEF, ID, PLUS, MINUS, TIMES, DIVIDE, ASSIGN, LPAREN, RPAREN, LBRACE, 
               RBRACE, INT, RETURN, IF, ELSE, PRINT, SEMICOLON, COMMA, NUM,
               LT, GT, EQ }

    ignore = ' \t'

    # Palavras-chave
    DEF = r'\bdef\b'
    INT = r'\bint\b'
    RETURN = r'\breturn\b'
    IF = r'\bif\b'
    ELSE = r'\belse\b'
    PRINT = r'\bprint\b'

    # Símbolos
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACE = r'\{'
    RBRACE = r'\}'
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    ASSIGN = r'='
    SEMICOLON = r';'
    COMMA = r','
    LT = r'<'
    GT = r'>'
    EQ = r'=='

    # Identificadores e números
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUM = r'\d+'
    
    # Ignorar comentários
    ignore_comment = r'\#.*'

    # Contagem de novas linhas
    @_(r'\n+')
    def newline(self, t):
        self.lineno += len(t.value)

    # Converte números para inteiros
    @_(r'\d+')
    def NUM(self, t):
        t.value = int(t.value)
        return t

    # Tratamento de erros léxicos
    def error(self, t):
        print(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Erro léxico na linha {self.lineno}, coluna {self.index}: {t.value[0]} !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        self.index += 1
        return t

def main():
    if len(sys.argv) <= 1:
        print("Insira o nome do arquivo a ser analisado. \nExemplo: python lsi_lexer.py caminho/para/seu/arquivo.lsi")
        return

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"Arquivo não encontrado: {filepath}")
        return

    with open(filepath, 'r') as file:
        code = file.read()

    lexer = LSILexer()
    for token in lexer.tokenize(code):
        print(token)

if __name__ == '__main__':
    main()
