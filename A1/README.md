# LEXER FOR C SHARP IN PYTHON #

### Some information about PLY ###
* tok = lex.token() returns a token. The returned token has the following fields :
> tok.type - gives the type of token (prints from the TOKEN LIST)
> tok.value - contains the lexeme
> tok.lexpos, tok.line - position and line number respectively.

* Sample example (printing type, value and lexpos):
> 3 + 4 * 10 + -20 *2
> NUMBER 3 0
> PLUS + 2
> NUMBER 4 4
> TIMES * 6
> NUMBER 10 8
> PLUS + 11
> MINUS - 13
> NUMBER 20 14
> TIMES * 17
> NUMBER 2 18
