import os
import sys
import re

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token( Type: {self.type}, {self.value}, Line: {self.line}, Column: {self.column})"

# Definição dos tokens e palavras-chave
keywords = {
    'def': 'DEF',
    'int': 'INT',
    'return': 'RETURN',
    'if': 'IF',
    'else': 'ELSE',
    'print': 'PRINT'
}

token_specification = [
    ('NUM',      r'\d+'),       # Inteiros
    ('ID',       r'[A-Za-z_]\w*'),  # Identificadores
    ('PLUS',     r'\+'),        # Operador +
    ('MINUS',    r'-'),         # Operador -
    ('TIMES',    r'\*'),        # Operador *
    ('DIVIDE',   r'/'),         # Operador /
    ('ASSIGN',   r'='),         # Operador =
    ('LT',       r'<'),         # Operador <
    ('GT',       r'>'),         # Operador >
    ('EQ',       r'=='),        # Operador ==
    ('LPAREN',   r'\('),        # Parênteses esquerdo
    ('RPAREN',   r'\)'),        # Parênteses direito
    ('LBRACE',   r'\{'),        # Chave esquerda
    ('RBRACE',   r'\}'),        # Chave direita
    ('COMMA',    r','),         # Vírgula
    ('SEMICOLON', r';'),        # Ponto e vírgula
    ('NEWLINE',  r'\n'),        # Nova linha
    ('SKIP',     r'[ \t]'),     # Espaços e tabulações
    ('MISMATCH', r'.'),         # Qualquer outro caractere
]

token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)

def lexer(code):
    line_num = 1
    line_start = 0
    tokens = []
    errors = []

    for mo in re.finditer(token_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if kind == 'NUM':
            value = int(value)
        elif kind == 'ID':
            kind = keywords.get(value, 'ID')
        elif kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            continue
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            errors.append(f'!!!!! Erro léxico na linha {line_num} coluna {column} : {value!r} !!!!!')
            continue
        tokens.append(Token(kind, value, line_num, column))
    
    if errors:
        for error in errors:
            print(error)
    return tokens

# Função para testar o lexer com um exemplo de código
def main():
    if len(sys.argv) <= 1:
        print("Insira o nome do arquivo a ser analisado. \nExemplo: python lexer.py caminho/para/seu/arquivo.lsi")
        return

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"Arquivo não encontrado: {filepath}")
        return

    with open(filepath, 'r') as file:
        code = file.read()
        
    tokens = lexer(code)
    for token in tokens:
        print(token)

if __name__ == '__main__':
    main()
