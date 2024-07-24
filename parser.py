import os  # Importa o módulo os para interagir com o sistema operacional
import sys  # Importa o módulo sys para manipular argumentos da linha de comando
from lexer import lexer, Token  # Importa o lexer e a classe Token

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens  # Lista de tokens fornecida pelo analisador léxico
        self.current_token_index = 0  # Índice do token atual
        self.current_token = self.tokens[self.current_token_index]  # Token atual
        self.symbol_table = set()  # Tabela de símbolos para rastrear declarações de variáveis
        self.function_table = set()  # Tabela de símbolos para rastrear declarações de funções
    
    def advance(self):
        # Avança para o próximo token na lista de tokens
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]  # Atualiza o token atual
        else:
            self.current_token = None  # Define como None se não houver mais tokens

    def parse(self):
        # Inicia a análise sintática a partir do símbolo inicial (MAIN)
        try:
            self.main()  # Chama a função main para iniciar a análise
            print("Análise sintática concluída com sucesso!")
        except Exception as e:
            # Exibe uma mensagem de erro sintático caso ocorra uma exceção
            print(f"Erro sintático: {e}")

    def main(self):
        # Verifica o token inicial e decide qual produção seguir
        if self.current_token.type == 'DEF':
            self.flist()
        elif self.current_token.type == 'INT':
            self.stmt()
        elif self.current_token.type == 'EOF':
            pass  # Produção vazia (epsilon)
        else:
            raise Exception(f"Erro: token inesperado {self.current_token.type} na linha {self.current_token.line}, coluna {self.current_token.column}")

    def flist(self):
        # Processa uma lista de definições de funções (FLIST)
        self.fdef()  # Processa a primeira definição de função
        while self.current_token and self.current_token.type == 'DEF':
            self.fdef()  # Processa definições de função adicionais

    def fdef(self):
        # Processa a definição de uma função (FDEF)
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
        # Processa a lista de parâmetros de uma função (PARLIST)
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
            pass  # Produção vazia (epsilon)

    def stmtlist(self):
        # Processa uma lista de declarações (STMTLIST)
        while self.current_token and self.current_token.type in ['INT', 'ID', 'PRINT', 'RETURN', 'IF', 'LBRACE', 'SEMICOLON']:
            self.stmt()

    def stmt(self):
        # Processa uma declaração (STMT)
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
        # Processa uma atribuição (ATRIBSTMT)
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
        # Processa uma chamada de função (FCALL)
        function_name = self.current_token.value
        if function_name not in self.function_table:
            raise Exception(f"Erro: função não declarada {function_name} na linha {self.current_token.line}, coluna {self.current_token.column}")
        self.match('ID')
        self.match('LPAREN')
        self.parlistcall()
        self.match('RPAREN')

    def parlistcall(self):
        # Processa a lista de parâmetros em uma chamada de função (PARLISTCALL)
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
            pass  # Produção vazia (epsilon)

    def lookahead(self):
        # Retorna o próximo token sem avançar no índice de tokens
        if self.current_token_index + 1 < len(self.tokens):
            return self.tokens[self.current_token_index + 1]
        return None

    def printstmt(self):
        # Processa uma declaração de impressão (PRINTSTMT)
        self.match('PRINT')
        self.expr()

    def returnstmt(self):
        # Processa uma declaração de retorno (RETURNSTMT)
        self.match('RETURN')

    def ifstmt(self):
        # Processa uma declaração if (IFSTMT)
        self.match('IF')
        self.match('LPAREN')
        self.expr()
        self.match('RPAREN')
        self.stmt()
        if self.current_token and self.current_token.type == 'ELSE':
            self.match('ELSE')
            self.stmt()

    def expr(self):
        # Processa uma expressão (EXPR)
        self.numexpr()
        while self.current_token and self.current_token.type in ['LT', 'GT', 'EQ']:
            self.match(self.current_token.type)
            self.numexpr()

    def numexpr(self):
        # Processa uma expressão numérica (NUMEXPR)
        self.term()
        while self.current_token and self.current_token.type in ['PLUS', 'MINUS']:
            self.match(self.current_token.type)
            self.term()

    def term(self):
        # Processa um termo (TERM)
        self.factor()
        while self.current_token and self.current_token.type in ['TIMES', 'DIVIDE']:
            self.match(self.current_token.type)
            self.factor()

    def factor(self):
        # Processa um fator (FACTOR)
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
        # Verifica se o token atual corresponde ao tipo esperado e avança para o próximo token
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

    tokens = lexer(code)  # Chama a função lexer para analisar o código e gerar os tokens
    
    parser = Parser(tokens)  # Cria uma instância do parser com a lista de tokens
    parser.parse()  # Inicia a análise sintática

if __name__ == '__main__':
    main()  # Executa a função main se o script for executado diretamente
