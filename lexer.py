import os  # Importa o módulo os para interagir com o sistema operacional
import sys  # Importa o módulo sys para manipular argumentos da linha de comando
import re  # Importa o módulo re para usar expressões regulares

class Token:
    def __init__(self, type, value, line, column):
        self.type = type  # Tipo do token
        self.value = value  # Valor do token
        self.line = line  # Linha do token no código fonte
        self.column = column  # Coluna do token no código fonte

    def __repr__(self):
        return f"Token(Type: {self.type}, Value: {self.value}, Line: {self.line}, Column: {self.column})"
        # Representação em string do objeto Token para fácil visualização

# Definição dos tokens e palavras-chave
keywords = {
    'def': 'DEF',
    'int': 'INT',
    'return': 'RETURN',
    'if': 'IF',
    'else': 'ELSE',
    'print': 'PRINT'
    # Palavras reservadas da linguagem associadas aos seus tipos de token
}

# Especificação dos tokens usando expressões regulares
token_specification = [
    ('EQ',       r'=='),        # Operador ==
    ('ASSIGN',   r'='),         # Operador de atribuição =
    ('NUM',      r'\d+'),       # Números inteiros
    ('ID',       r'[A-Za-z_]\w*'),  # Identificadores (variáveis, funções)
    ('PLUS',     r'\+'),        # Operador +
    ('MINUS',    r'-'),         # Operador -
    ('TIMES',    r'\*'),        # Operador *
    ('DIVIDE',   r'/'),         # Operador /
    ('LT',       r'<'),         # Operador <
    ('GT',       r'>'),         # Operador >
    ('LPAREN',   r'\('),        # Parêntese esquerdo
    ('RPAREN',   r'\)'),        # Parêntese direito
    ('LBRACE',   r'\{'),        # Chave esquerda
    ('RBRACE',   r'\}'),        # Chave direita
    ('COMMA',    r','),         # Vírgula
    ('SEMICOLON', r';'),        # Ponto e vírgula
    ('NEWLINE',  r'\n'),        # Nova linha
    ('SKIP',     r'[ \t]'),     # Espaços e tabulações
    ('MISMATCH', r'.'),         # Qualquer outro caractere
]

# Compilar as expressões regulares em uma única expressão
token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)

def lexer(code):
    line_num = 1  # Número da linha atual
    line_start = 0  # Posição de início da linha atual
    tokens = []  # Lista de tokens identificados
    errors = []  # Lista de erros léxicos

    previous_token = None  # Último token processado

    for mo in re.finditer(token_regex, code):
        kind = mo.lastgroup  # Tipo do token identificado
        value = mo.group()  # Valor do token identificado
        column = mo.start() - line_start  # Coluna do token identificado

        if kind == 'NUM':
            value = int(value)  # Converte números para inteiros
        elif kind == 'ID':
            kind = keywords.get(value, 'ID')  # Verifica se é uma palavra-chave
        elif kind == 'NEWLINE':
            line_start = mo.end()  # Atualiza a posição de início da linha
            line_num += 1  # Incrementa o número da linha
            continue
        elif kind == 'SKIP':
            continue  # Ignora espaços e tabulações
        elif kind == 'MISMATCH':
            errors.append(f'!!!!! Erro léxico na linha {line_num} coluna {column} : {value!r} !!!!!')
            # Adiciona mensagem de erro léxico à lista de erros
            continue

        # Verificar múltiplos operadores consecutivos
        if previous_token and previous_token.type in {'PLUS', 'MINUS', 'TIMES', 'DIVIDE'} and kind in {'PLUS', 'MINUS', 'TIMES', 'DIVIDE'}:
            errors.append(f'!!!!! Erro léxico na linha {line_num} coluna {column} : múltiplos operadores {previous_token.value}{value} !!!!!')
            # Adiciona mensagem de erro léxico para múltiplos operadores consecutivos
            continue

        previous_token = Token(kind, value, line_num, column)  # Cria um novo token
        tokens.append(previous_token)  # Adiciona o token à lista de tokens
    
    if errors:
        for error in errors:
            print(error)  # Imprime todos os erros léxicos
    return tokens  # Retorna a lista de tokens

# Função para testar o lexer com um exemplo de código
def main():
    if len(sys.argv) <= 1:
        print("Insira o nome do arquivo a ser analisado. \nExemplo: python lexer.py caminho/para/seu/arquivo.lsi")
        return  # Verifica se o nome do arquivo foi passado como argumento

    filepath = sys.argv[1]  # Obtém o caminho do arquivo a partir dos argumentos da linha de comando
    if not os.path.exists(filepath):
        print(f"Arquivo não encontrado: {filepath}")
        return  # Verifica se o arquivo existe

    with open(filepath, 'r') as file:
        code = file.read()  # Lê o conteúdo do arquivo
        
    tokens = lexer(code)  # Chama a função lexer para analisar o código
    for token in tokens:
        print(token)  # Imprime todos os tokens gerados

if __name__ == '__main__':
    main()  # Executa a função main se o script for executado diretamente
