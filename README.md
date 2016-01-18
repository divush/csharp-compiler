# IMPLEMENTING C SHARP IN PYTHON #
Here is a summary of what we have done :
1) The tool used for creating the lexer was PLY. It stands for Python Lex-Yacc. This tool enables us to define tokens and their matching RE's and also analyzes the input text and breaks input text into tokens.

2) The data structures used are as follows :-
	a) tokentype : A dictionary. Key is type of token. Value is number of times that token is seen.
	b) lexeme : Dictionary. Key is again type of token. Value is a list of ALL lexemes matching that token's RE.