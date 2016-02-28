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

inputfile = open(filename, 'r')
data = inputfile.read()
lexer.input(data)

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

# Grammar Productions for C#
