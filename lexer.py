#-------------------------------------------
# Lexer for generating tokens in C# language
#-------------------------------------------
import ply.lex as lex1

#-------------------------------------------
# Specifying the list of tokens.
# Begin with keywords. Do not use RE
# for keywords.
#-------------------------------------------
KEYWORDS={
	'abstract':'ABSTRACT',
	'as':'AS',

	# Note to team : Fill this keyword section!

}