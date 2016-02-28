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
	'class-member-declarations',
	'struct-member-declarations',
	'verbatim-string-literal-characters',
	'interface-base',
	'new',
	'expression',
	'identifier-part-characters',
	'integer-type-suffix',
	'enum-modifiers',
	'interface-member-declarations',
	'statement-list',
	'argument-list',
	'dim-separators',
	'array-initializer',
	'hex-digit',
	'constant-modifiers',
	'pp-else-section',
	'formal-parameter-list',
	'variable-initializer-list',
	'exponent-part',
	'delegate-modifiers',
	'attribute-target-specifier',
	'regular-string-literal-characters',
	'general-catch-clause',
	'identifier',
	'parameter-modifier',
	'enum-base',
	'namespace-member-declarations',
	'method-modifiers',
	'conditional-section',
	'specific-catch-clauses',
	'constructor-initializer',
	'skipped-characters',
	'struct-modifiers',
	'constructor-modifiers',
	'positional-argument-list',
	'switch-sections',
	'pp-elif-sections',
	'for-condition',
	'using-directives',
	'rank-specifiers',
	'attribute-arguments',
	'interface-modifiers',
	'unsafe',
	'input-characters',
	'class-base',
	'indexer-modifiers',
	'enum-member-declarations',
	'property-modifiers',
	'class-modifiers',
	'set-accessor-declaration',
	'input-section',
	'extern',
	'field-modifiers',
	'whitespace',
	'get-accessor-declaration',
	'real-type-suffix',
	'global-attributes',
	';',
	'struct-interfaces',
	'sign',
	'single-line-comment',
	'event-modifiers',
	'for-iterator',
	'for-initializer',
	'delimited-comment-characters',
	'input-elements'
]

for rule in opt_rules:
	create_opt_rule(rule)

# Grammar Productions for C#
def p_compilation_unit(p):
	"""compilation_unit 	: extern_alias_directives_opt
							| using_directives_opt
							| global_attributes_opt
							| namespace_member_declaration_opt
	"""
	pass

def p_extern_alias_directives(p):
	"""extern_alias_directives 	: extern_alias_directive
								| extern_alias_directives extern_alias_directive
	"""
	pass

def p_extern_alias_directive(p):
	"""extern_alias_directive 	: EXTERN 