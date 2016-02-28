#!/usr/bin/python3
# Parser for C# in Python
###################################################################################################

import sys
import ply.yacc as yacc
from lexer import lexer

###################################################################################################

if len(sys.argv) == 2:
	filename = sys.argv[1]
else:
	print("Usage: ./parser file.cs")
	exit(0)

# Read the input program
inputfile = open(filename, 'r')
data = inputfile.read()
lexer.input(data)
# Now we can access the tokens in the program as lexer.token()

###################################################################################################

def create_opt_rules(rulename):
	optname = rulename + '_opt'
	def optrule(self, p):
	    p[0] = p[1]
	optrule.__doc__ = '%s : empty\n| %s' % (optname, rulename)
	optrule.__name__ = 'p_%s' % optname
	setattr(self.__class__, optrule.__name__, optrule)


###################################################################################################


# Precedence and associativity of operators
precedence = (
	('left', 'COR'),
	('left', 'CAND'),
	('left', 'OR'),
	('left', 'XOR'),
	('left', 'AND'),
	('left', 'EQ', 'NE'),
	('left', 'GT', 'GE', 'LT', 'LE'),
	('left', 'RSHIFT', 'LSHIFT'),
	('left', 'PLUS', 'MINUS'),
	('left', 'TIMES', 'DIVIDE', 'MOD')
)

opt_rules = [
	''
]

for rule in opt_rules:
	create_opt_rule(rule)

# Grammar Productions for C#
def p_compilation_unit(p):
	"""
	"""