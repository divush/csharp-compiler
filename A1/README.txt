Please follow the instructions in order to build and run the implementation of lexer by group 25.
Source language :- C#
Implementation language :- Python3
Target language :- x86

1) cd asgn1
2) make
3) To run test1.cs
	bin/lexer test/test1.cs
   For the rest of the test files ( tes2.cs, test3.cs, test4.cs and test5.cs)
   just give the proper file name.


Explanations :-
Here is a summary of what we have done :
1) The tool used for creating the lexer was PLY. It stands for Python Lex-Yacc. This tool enables us to define tokens and their matching RE's and also analyzes the input text and breaks input text into tokens.

2) The data structures used are as follows :-
	a) tokentype : A dictionary. Key is type of token. Value is number of times that token is seen.
	b) lexeme : Dictionary. Key is again type of token. Value is a list of ALL lexemes matching that token's RE.

3) Test file test4.cs contains invalid declaration.