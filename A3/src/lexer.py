#!/usr/bin/python3
# ------------------------------------------------------------------
#  Lexer for generating tokens in C#  language
# ------------------------------------------------------------------
import ply.lex as lex
import sys

# THE LIST OF RESERVED KEYWORDS IN C# 
reserved = {
	'abstract' : 'ABSTRACT',
	'break' : 'BREAK',
	'char' : 'CHAR',
	'continue' : 'CONTINUE',
	'do' : 'DO',
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
	'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET', 'COMMA', 'STMT_TERMINATOR', 'COLON',
	# Others: \n // ...
	'NEWLINE', 'COMMENT', 'PREPROCESSOR'

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
t_STMT_TERMINATOR  = r';'
t_COLON            = r':'

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