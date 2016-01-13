#------------------------------------------------------------------
# Lexer for generating tokens in C# language
#------------------------------------------------------------------
import ply.lex as lex

#List of reserved keywords in C#
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

#List of token names
tokens = [
   'INTCONST',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
   'NEWLINE',
   'IDENTIFIER',
   'COMMENTS',
   'BLOCKBEGIN',
   'BLOCKEND',
   'STMT_TERMINATOR'
] + list(reserved.values())

#Regex rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_BLOCKBEGIN = r'{'
t_BLOCKEND = r'}'
t_STMT_TERMINATOR = r';'

#Regex rule for identifiers
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

#Regex rule for integers
def t_INTCONST(t):
    r'\d+'
    t.value = int(t.value)
    return t

#Define a rule so we can track line numbers
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

#Ignored characters (spaces and tabs)
t_ignore  = ' \t'

#Comments
def t_COMMENT(t):
    r'//'
    pass
    # No return value. Token discarded

#Error handling rule
def t_ERROR(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()