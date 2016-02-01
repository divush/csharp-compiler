#!/usr/bin/python3
# ------------------------------------------------------------------
#  Lexer for generating tokens in C#  language
# ------------------------------------------------------------------
import ply.lex as lex
import sys
# import itertools

# THE LIST OF RESERVED KEYWORDS IN C# 
reserved = {
	'abstract' : 'ABSTRACT',
	'break' : 'BREAK',
	'char' : 'CHAR',
	'continue' : 'CONTINUE',
	'do' : 'DO',
	'event' : 'EVENT',
	'finally' : 'FINALLY',
	'foreach' : 'FOREACH',
	'in' : 'IN',
	'internal' : 'INTERNAL',
	'namespace' : 'NAMESPACE',
	'operator' : 'OPERATOR',
	'params' : 'PARAMS',
	'readonly' : 'READONLY',
	'sealed' : 'SEALED',
	'static' : 'STATIC',
	'this' : 'THIS',
	'typeof' : 'TYPEOF',
	'unsafe' : 'UNSAFE',
	'void' : 'VOID',
	'as' : 'AS',
	'byte' : 'BYTE',
	'checked' : 'CHECKED',
	'decimal' : 'DECIMAL',
	'double' : 'DOUBLE',
	'explicit' : 'EXPLICIT',
	'fixed' : 'FIXED',
	'goto' : 'GOTO',
	'in' : 'IN',
	'is' : 'IS',
	'new' : 'NEW',
	'out' : 'OUT',
	'private' : 'PRIVATE',
	'ref' : 'REF',
	'short' : 'SHORT',
	'string' : 'STRING',
	'throw' : 'THROW',
	'uint' : 'UINT',
	'ushort' : 'USHORT',
	'volatile' : 'VOLATILE',
	'base' : 'BASE',
	'case' : 'CASE',
	'class' : 'CLASS',
	'default' : 'DEFAULT',
	'else' : 'ELSE',
	'extern' : 'EXTERN',
	'float' : 'FLOAT',
	'if' : 'IF',
	'int' : 'INT',
	'lock' : 'LOCK',
	'null' : 'NULL',
	'out' : 'OUT',
	'protected' : 'PROTECTED',
	'return' : 'RETURN',
	'sizeof' : 'SIZEOF',
	'struct' : 'STRUCT',
	'TRUE' : 'TRUE',
	'ulong' : 'ULONG',
	'using' : 'USING',
	'while' : 'WHILE',
	'bool' : 'BOOL',
	'catch' : 'CATCH',
	'const' : 'CONST',
	'delegate' : 'DELEGATE',
	'enum' : 'ENUM',
	'FALSE' : 'FALSE',
	'for' : 'FOR',
	'implicit' : 'IMPLICIT',
	'interface' : 'INTERFACE',
	'long' : 'LONG',
	'object' : 'OBJECT',
	'override' : 'OVERRIDE',
	'public' : 'PUBLIC',
	'sbyte' : 'SBYTE',
	'stackalloc' : 'STACKALLOC',
	'switch' : 'SWITCH',
	'try' : 'TRY',
	'unchecked' : 'UNCHECKED',
	'virtual' : 'VIRTUAL'
}

# THE LIST OF TOKENS
tokens = [
	# Literals: Identifiers, Int-Constants, Char-Constant, String-Constant 
	'IDENTIFIER', 'INTCONST', 'CHCONST', 'STRCONST',

	# Primary Operators: . ?. ++ -- ->
	'MEMBERACCESS', 'CONDMEMBACCESS', 'INCREMENT', 'DECREMENT', 'ARROW',
	# Unary Operators: ~ ! 
	'NOT', 'LNOT',
	# Multiplicative Operators: * / %
	'TIMES', 'DIVIDE', 'MOD',
	# Additive Operators + -
	'PLUS', 'MINUS',
	# Shift Operators: << >>
	'LSHIFT', 'RSHIFT',
	# Relational Operators: < > <= >=
	'LT', 'GT', 'LE', 'GE',
	# Equality Operators == !=
	'EQ', 'NE',
	# Logical Operators: & ^ | && ||
	'AND', 'XOR', 'OR', 'CAND', 'COR',
	# Conditional Operator: ?
	'CONDOP',
	# Assignment and Lambda Operators: = += -= *= /= %= &= |= ^= <<= >>= =>
	'EQUALS', 'PLUSEQUAL', 'MINUSEQUAL', 'TIMESEQUAL', 'DIVEQUAL', 'MODEQUAL',
	'ANDEQUAL', 'OREQUAL', 'XOREQUAL', 'LSHIFTEQUAL', 'RSHIFTEQUAL',
	'LAMBDADEC',

	# Delimiters: ( ) { } [ ] , . ; :
	'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET', 'COMMA', 'PERIOD', 'STMT_TERMINATOR', 'COLON',
	# Others: \n // ...
	'NEWLINE', 'COMMENT', 'ELLIPSIS', 'PREPROCESSOR'

] + list(reserved.values())

# Completely ignored characters
t_ignore = ' \t\x0c'

# Define a rule so we can track line numbers
def t_NEWLINE(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

# Operators
t_MEMBERACCESS		= r'\.'
t_CONDMEMBACCESS	= r'\?\.'
t_INCREMENT			= r'\+\+'
t_DECREMENT			= r'--'
t_ARROW				= r'->'
t_NOT 				= r'~'
t_LNOT				= r'!'
t_TIMES				= r'\*'
t_DIVIDE 			= r'/'
t_MOD   			= r'%'
t_PLUS  			= r'\+'
t_MINUS 			= r'-'
t_LSHIFT 			= r'<<'
t_RSHIFT 			= r'>>'
t_LT				= r'<'
t_GT				= r'>'
t_LE 				= r'<='
t_GE  				= r'>='
t_EQ   				= r'=='
t_NE   				= r'!='
t_AND  				= r'&'
t_XOR   			= r'\^'
t_OR     			= r'\|'
t_CAND  			= r'&&'
t_COR    			= r'\|\|'
t_CONDOP  			= r'\?'
t_EQUALS     		= r'='
t_PLUSEQUAL   		= r'\+='
t_MINUSEQUAL  		= r'-='
t_TIMESEQUAL 		= r'\*='
t_DIVEQUAL  		= r'/='
t_MODEQUAL 			= r'%='
t_ANDEQUAL   		= r'&='
t_OREQUAL    		= r'\|='
t_XOREQUAL    		= r'\^='
t_LSHIFTEQUAL  		= r'<<='
t_RSHIFTEQUAL  		= r'>>='
t_LAMBDADEC  		= r'=>'

# Delimiters
t_LPAREN           = r'\('
t_RPAREN           = r'\)'
t_LBRACKET         = r'\['
t_RBRACKET         = r'\]'
t_LBRACE           = r'\{'
t_RBRACE           = r'\}'
t_COMMA            = r','
t_PERIOD           = r'\.'
t_STMT_TERMINATOR  = r';'
t_COLON            = r':'
t_ELLIPSIS         = r'\.\.\.'

# Identifiers and Keywords
def t_IDENTIFIER(t):
	r'[a-zA-Z_@][a-zA-Z_0-9]*'
	t.type = reserved.get(t.value,'IDENTIFIER')    #  Check for reserved words
	return t

# Integer literal
t_INTCONST = r'\d+([uU]|[lL]|[uU][lL]|[lL][uU])?'

# String literal
t_STRCONST = r'\"([^\\\n]|(\\.))*?\"'

# Character constant 'c' or L'c'
t_CHCONST = r'(L)?\'([^\\\n]|(\\.))*?\''

# Comments (Only delimited comments for now)
def t_COMMENT(t):
	r' /\*(.|\n)*?\*/'
	t.lineno += t.value.count('\n')

# Preprocessor directive (ignored)
def t_PREPROCESSOR(t):
	r'\#(.)*?\n'
	t.lineno += 1

# Error handling rule
def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)


#  Build the lexer
lexer = lex.lex()

# File I/O
# Input filename from terminal
strinputfile = sys.argv[1]
inputfile = open(strinputfile, 'r')

#data = "using System; namespace HelloWorld"
#Convert file to string as lexer takes only string inputs.
data = inputfile.read()

#Giving file (in string form) as input to our lexer
lexer.input(data)

#Data Structures for various counts.
#Stores {token_type : token_count} pairs for each token
tokentype = {}

#The key here is the token_type(like IDENTIFIER, INT, etc.). Value is a LIST of lexemes that match the token.
lexeme = {}			

#This stores those token types which are not be recounted of they occur more than once. For example, a variable name.
non_recountable = ['IDENTIFIER']
#Tokenize input!
while True:
	tok = lexer.token() #Get token
	if not tok:			#No token?
		break      # No more input
	tokname = tok.value 		#store the lexeme
	toktype = tok.type 			#stores the token_type
	if toktype not in tokentype:		
		tokentype[toktype] = 1			#initianlize count of token to 1
		lexeme[toktype]=[]				#initialize the list in the lexeme dictionary
		lexeme[toktype].append(tokname)	#append lexeme to the lexeme dictionary
		# print(tokname+"\t"+toktype+"NOT here previously")
	else:
		if tokname not in lexeme[toktype]:	
			lexeme[toktype].append(tokname)		#if not present add. above check avoids repetitions
			tokentype[toktype] += 1			#add another token seen of that type
		else:
			if toktype not in non_recountable:			#if this token type is not to be recounted
				tokentype[toktype] +=1			#add token seen.

# print(tokentype)
# print(lexeme)

#printing the tokens
for types in tokentype:
	print("----------------------------------------")
	print("{0:<20s} {1:>5s}".format(types, (str)(tokentype[types])))
	for lexlist in lexeme[types]:
		print("{0:>40s}".format(lexlist))
print("----------------------------------------")
