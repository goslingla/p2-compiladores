# Analisador Léxico e Sintático para LSI-2024-1

## Gramática LSI-2024 Fatorada à Esquerda

```plaintext
MAIN → STMT | FLIST | ε
FLIST → FDEF FLIST | FDEF
FDEF → def id(PARLIST) { STMTLIST }
PARLIST → int id PARLIST'
PARLIST' → , int id PARLIST' | ε
STMT → int id; | ATRIBSTMT; | PRINTSTMT; | RETURNSTMT; | IFSTMT; | { STMTLIST } | ;
ATRIBSTMT → id = EXPR | id = FCALL
FCALL → id(PARLISTCALL)
PARLISTCALL → id PARLISTCALL'
PARLISTCALL' → , id PARLISTCALL' | ε
PRINTSTMT → print EXPR
RETURNSTMT → return
IFSTMT → if(EXPR) STMT IFSTMT'
IFSTMT' → else STMT | ε
STMTLIST → STMT STMTLIST'
STMTLIST' → STMT STMTLIST' | ε
EXPR → NUMEXPR EXPR'
EXPR' → < NUMEXPR | > NUMEXPR | == NUMEXPR | ε
NUMEXPR → TERM NUMEXPR'
NUMEXPR' → + TERM NUMEXPR' | - TERM NUMEXPR' | ε
TERM → FACTOR TERM'
TERM' → * FACTOR TERM' | ε
FACTOR → num | (NUMEXPR) | id
```

## Gramática Transformada em LL(1)

```plaintext
MAIN → STMT | FLIST | ε
FLIST → FDEF FLIST'
FLIST' → FDEF FLIST' | ε
FDEF → def id(PARLIST) { STMTLIST }
PARLIST → int id PARLIST'
PARLIST' → , int id PARLIST' | ε
STMT → int id; | ATRIBSTMT; | PRINTSTMT; | RETURNSTMT; | IFSTMT; | { STMTLIST } | ;
ATRIBSTMT → id = EXPR | id = FCALL
FCALL → id(PARLISTCALL)
PARLISTCALL → id PARLISTCALL'
PARLISTCALL' → , id PARLISTCALL' | ε
PRINTSTMT → print EXPR
RETURNSTMT → return
IFSTMT → if(EXPR) STMT IFSTMT'
IFSTMT' → else STMT | ε
STMTLIST → STMT STMTLIST'
STMTLIST' → STMT STMTLIST' | ε
EXPR → NUMEXPR EXPR'
EXPR' → < NUMEXPR | > NUMEXPR | == NUMEXPR | ε
NUMEXPR → TERM NUMEXPR'
NUMEXPR' → + TERM NUMEXPR' | - TERM NUMEXPR' | ε
TERM → FACTOR TERM'
TERM' → * FACTOR TERM' | ε
FACTOR → num | (NUMEXPR) | id

```

## Conjunto FIRST

```plaintext
FIRST(MAIN) = { def, int, {, if, print, return, ;, ε }
FIRST(FLIST) = { def }
FIRST(FLIST') = { def, ε }
FIRST(FDEF) = { def }
FIRST(PARLIST) = { int, ε }
FIRST(PARLIST') = { ,, ε }
FIRST(STMT) = { int, id, print, return, if, {, ; }
FIRST(ATRIBSTMT) = { id }
FIRST(FCALL) = { id }
FIRST(PARLISTCALL) = { id, ε }
FIRST(PARLISTCALL') = { ,, ε }
FIRST(PRINTSTMT) = { print }
FIRST(RETURNSTMT) = { return }
FIRST(IFSTMT) = { if }
FIRST(IFSTMT') = { else, ε }
FIRST(STMTLIST) = { int, id, print, return, if, {, ; }
FIRST(STMTLIST') = { int, id, print, return, if, {, ;, ε }
FIRST(EXPR) = { num, (, id }
FIRST(EXPR') = { <, >, ==, ε }
FIRST(NUMEXPR) = { num, (, id }
FIRST(NUMEXPR') = { +, -, ε }
FIRST(TERM) = { num, (, id }
FIRST(TERM') = { *, ε }
FIRST(FACTOR) = { num, (, id }
```

## Conjunto FOLLOW

```plaintext
FOLLOW(MAIN) = { $ }
FOLLOW(FLIST) = { $ }
FOLLOW(FLIST') = { $ }
FOLLOW(FDEF) = { def, $ }
FOLLOW(PARLIST) = { ) }
FOLLOW(PARLIST') = { ) }
FOLLOW(STMT) = { int, id, print, return, if, {, ;, def, }, $ }
FOLLOW(ATRIBSTMT) = { ; }
FOLLOW(FCALL) = { ; }
FOLLOW(PARLISTCALL) = { ) }
FOLLOW(PARLISTCALL') = { ) }
FOLLOW(PRINTSTMT) = { ; }
FOLLOW(RETURNSTMT) = { ; }
FOLLOW(IFSTMT) = { int, id, print, return, if, {, ;, def, }, $ }
FOLLOW(IFSTMT') = { int, id, print, return, if, {, ;, def, }, $ }
FOLLOW(STMTLIST) = { } }
FOLLOW(STMTLIST') = { } }
FOLLOW(EXPR) = { ;, ), int, id, print, return, if, {, ;, def, }, $ }
FOLLOW(EXPR') = { ;, ), int, id, print, return, if, {, ;, def, }, $ }
FOLLOW(NUMEXPR) = { <, >, ==, ;, ), int, id, print, return, if, {, ;, def, }, $ }
FOLLOW(NUMEXPR') = { <, >, ==, ;, ), int, id, print, return, if, {, ;, def, }, $ }
FOLLOW(TERM) = { +, -, <, >, ==, ;, ), int, id, print, return, if, {, ;, def, }, $ }
FOLLOW(TERM') = { +, -, <, >, ==, ;, ), int, id, print, return, if, {, ;, def, }, $ }
FOLLOW(FACTOR) = { \*, +, -, <, >, ==, ;, ), int, id, print, return, if, {, ;, def, }, $ }
```

### Tabela LL(1)

### Legenda

- `M[A, a]`: Produção a ser utilizada se `A` é o não-terminal e `a` é o terminal de entrada.

### Tabela LL(1)

## Legenda

- `MAIN`, `FLIST`, `FDEF`, `PARLIST`, `STMT`, etc. são não-terminais.
- `def`, `int`, `id`, `print`, `return`, `if`, `{`, `}`, `;`, `,`, `num`, `(`, `)`, `<`, `>`, `==`, `+`, `-`, `*`, são terminais.
- `ε` representa a produção vazia.

## Instruções de Uso

1. Clone o repositório.
2. Certifique-se de que você tenha a versão 3.12.3 do Python instalada.
3. Execute o analisador sintático:
   ```sh
   python parser.py caminho/para/seu/arquivo.lsi
   ```
