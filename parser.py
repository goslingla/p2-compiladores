import os
import sys
from lexer import lexer, Token

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]
        self.symbol_table = set()  # Tabela de símbolos para rastrear declarações de variáveis
        self.function_table = set()  # Tabela de símbolos para rastrear declarações de funções
    
    def advance(self):
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = None

    def parse(self):
        try:
            self.main()
            print("Análise sintática concluída com sucesso!")
        except Exception as e:
            print(f"Erro sintático: {e}")

    def main(self):
        if self.current_token.type == 'DEF':
            self.flist()
        elif self.current_token.type == 'INT':
            self.stmt()
        elif self.current_token.type == 'EOF':
            pass
        else:
            raise Exception(f"Erro: token inesperado {self.current_token.type} na linha {self.current_token.line}, coluna {self.current_token.column}")

    def flist(self):
        self.fdef()
        while self.current_token and self.current_token.type == 'DEF':
            self.fdef()

    def fdef(self):
        self.match('DEF')
        function_name = self.current_token.value
        self.match('ID')
        self.function_table.add(function_name)  # Adiciona a função definida à tabela de funções
        self.match('LPAREN')
        self.parlist()
        self.match('RPAREN')
        self.match('LBRACE')
        self.stmtlist()
        self.match('RBRACE')

    def parlist(self):
        if self.current_token.type == 'INT':
            self.match('INT')
            id_token = self.current_token
            self.match('ID')
            self.symbol_table.add(id_token.value)
            while self.current_token and self.current_token.type == 'COMMA':
                self.match('COMMA')
                self.match('INT')
                id_token = self.current_token
                self.match('ID')
                self.symbol_table.add(id_token.value)
        else:
            pass  # Produção vazia

    def stmtlist(self):
        while self.current_token and self.current_token.type in ['INT', 'ID', 'PRINT', 'RETURN', 'IF', 'LBRACE', 'SEMICOLON']:
            self.stmt()

    def stmt(self):
        if self.current_token.type == 'INT':
            self.match('INT')
            id_token = self.current_token
            self.match('ID')
            self.symbol_table.add(id_token.value)
            if self.current_token.type == 'SEMICOLON':
                self.match('SEMICOLON')
            elif self.current_token.type == 'ASSIGN':
                self.match('ASSIGN')
                self.expr()
                self.match('SEMICOLON')
            else:
                raise Exception(f"Erro: esperava SEMICOLON ou ASSIGN, mas encontrou {self.current_token.type} na linha {self.current_token.line}, coluna {self.current_token.column}")
        elif self.current_token.type == 'ID':
            if self.current_token.value not in self.symbol_table:
                raise Exception(f"Erro: variável não declarada {self.current_token.value} na linha {self.current_token.line}, coluna {self.current_token.column}")
            self.atribstmt()
            self.match('SEMICOLON')
        elif self.current_token.type == 'PRINT':
            self.printstmt()
            self.match('SEMICOLON')
        elif self.current_token.type == 'RETURN':
            self.returnstmt()
            self.match('SEMICOLON')
        elif self.current_token.type == 'IF':
            self.ifstmt()
        elif self.current_token.type == 'LBRACE':
            self.match('LBRACE')
            self.stmtlist()
            self.match('RBRACE')
        elif self.current_token.type == 'SEMICOLON':
            self.match('SEMICOLON')
        else:
            raise Exception(f"Erro: token inesperado {self.current_token.type} na linha {self.current_token.line}, coluna {self.current_token.column}")

    def atribstmt(self):
        id_token = self.current_token
        self.match('ID')
        self.match('ASSIGN')
        if self.current_token.type == 'ID' and self.lookahead() and self.lookahead().type == 'LPAREN':
            self.fcall()  # Trata chamadas de função corretamente
        else:
            self.expr()
        # Adiciona a variável atribuída à tabela de símbolos se ainda não estiver presente
        if id_token.value not in self.symbol_table:
            self.symbol_table.add(id_token.value)

    def fcall(self):
        function_name = self.current_token.value
        if function_name not in self.function_table:
            raise Exception(f"Erro: função não declarada {function_name} na linha {self.current_token.line}, coluna {self.current_token.column}")
        self.match('ID')
        self.match('LPAREN')
        self.parlistcall()
        self.match('RPAREN')

    def parlistcall(self):
        if self.current_token.type == 'ID':
            if self.current_token.value not in self.symbol_table:
                raise Exception(f"Erro: variável não declarada {self.current_token.value} na linha {self.current_token.line}, coluna {self.current_token.column}")
            self.match('ID')
            while self.current_token and self.current_token.type == 'COMMA':
                self.match('COMMA')
                if self.current_token.value not in self.symbol_table:
                    raise Exception(f"Erro: variável não declarada {self.current_token.value} na linha {self.current_token.line}, coluna {self.current_token.column}")
                self.match('ID')
        else:
            pass  # Produção vazia

    def lookahead(self):
        if self.current_token_index + 1 < len(self.tokens):
            return self.tokens[self.current_token_index + 1]
        return None

    def printstmt(self):
        self.match('PRINT')
        self.expr()

    def returnstmt(self):
        self.match('RETURN')

    def ifstmt(self):
        self.match('IF')
        self.match('LPAREN')
        self.expr()
        self.match('RPAREN')
        self.stmt()
        if self.current_token and self.current_token.type == 'ELSE':
            self.match('ELSE')
            self.stmt()

    def expr(self):
        self.numexpr()
        while self.current_token and self.current_token.type in ['LT', 'GT', 'EQ']:
            self.match(self.current_token.type)
            self.numexpr()

    def numexpr(self):
        self.term()
        while self.current_token and self.current_token.type in ['PLUS', 'MINUS']:
            self.match(self.current_token.type)
            self.term()

    def term(self):
        self.factor()
        while self.current_token and self.current_token.type in ['TIMES', 'DIVIDE']:
            self.match(self.current_token.type)
            self.factor()

    def factor(self):
        if self.current_token.type == 'NUM':
            self.match('NUM')
        elif self.current_token.type == 'LPAREN':
            self.match('LPAREN')
            self.numexpr()
            self.match('RPAREN')
        elif self.current_token.type == 'ID':
            if self.current_token.value not in self.symbol_table:
                raise Exception(f"Erro: variável não declarada {self.current_token.value} na linha {self.current_token.line}, coluna {self.current_token.column}")
            self.match('ID')
        else:
            raise Exception(f"Erro: token inesperado {self.current_token.type} na linha {self.current_token.line}, coluna {self.current_token.column}")

    def match(self, token_type):
        if self.current_token and self.current_token.type == token_type:
            self.advance()
        else:
            raise Exception(f"Erro: esperava {token_type}, mas encontrou {self.current_token.type} na linha {self.current_token.line}, coluna {self.current_token.column}")

# Função para testar o parser com um exemplo de código
def main():
    if len(sys.argv) <= 1:
        print("Insira o nome do arquivo a ser analisado. \nExemplo: python parser.py caminho/para/seu/arquivo.lsi")
        return

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"Arquivo não encontrado: {filepath}")
        return

    with open(filepath, 'r') as file:
        code = file.read()

    tokens = lexer(code)
    
    parser = Parser(tokens)
    parser.parse()

if __name__ == '__main__':
    main()
