#!/usr/bin/python3
# Parser for C# in Python

# Grammar Specification Reference
# https://msdn.microsoft.com/en-in/library/aa664812(v=vs.71).aspx

# Authors: Divyanshu Shende, Pranshu Gupta, Prashant Kumar, Rahul Tudu
# Compiler Design: CS335A, Group 25, Indian Institute of Technology, Kanpur
###################################################################################################

import sys
import ply.yacc as yacc
from lexer import *
from copy import deepcopy
import symtab
import tac

symbol_table = symtab.environ()
###################################################################################################

if len(sys.argv) == 2:
	filename = sys.argv[1]
else:
	print("Usage: ./parser file.cs")
	exit(0)

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
	('left', 'TIMES', 'DIVIDE', 'MOD'),
	('right', 'NOT', 'LNOT'),
)

# C.2 Syntactic grammar 

# C.2.2 Types 
# (self, name, isbasic, isarray, ispointer, width, elem_type, length)
def p_type(p):
	"""type : non_array_type
		| array_type
	"""
	p[0] = deepcopy(p[1])

def p_non_array_type(p):
	"""non_array_type : simple_type
	"""
	p[0] = deepcopy(p[1])
def p_simple_type(p):
	"""simple_type : primitive_type
	"""
	p[0] = deepcopy(p[1])
def p_primitive_type(p):
	"""primitive_type : numeric_type
	"""
	p[0] = deepcopy(p[1])
def p_numeric_type(p):
	"""numeric_type : integral_type
		| floating_point_type
	"""
	p[0] = deepcopy(p[1])
def p_integral_type(p):
	"""integral_type : INT 
					| CHAR
	"""
	if p[1] == 'int':
		p[0] = symtab.type('int', True, False, False, 4, None, None)
	elif p[1] == 'char':
		p[0] = symtab.type('char', True, False, False, 1, None, None)

def p_floating_point_type(p):
	"""floating_point_type : FLOAT 
	"""
	p[0] = symtab.type('float', True, False, False, 8, None, None)

#(self, name, isbasic, isarray, ispointer, width, elem_type, length)
def p_array_type(p):
	"""array_type : simple_type LBRACKET RBRACKET
	"""
	p[0] = symtab.type(None, False, True, False, None, p[1], None)

# C.2.4 Expressions 
def p_argument_list(p):
	"""argument_list : argument
		| argument_list COMMA argument
	"""
	if len(p) == 2:
		p[0] = [deepcopy(p[1])]
	else:
		p[0] = deepcopy(p[1]) + [deepcopy(p[3])]	
def p_argument(p):
	"""argument : expression
	"""
	p[0] = deepcopy(p[1])
def p_primary_expression(p):
	"""primary_expression : parenthesized_expression
		| primary_expression_no_parenthesis
	"""
	p[0] = deepcopy(p[1])
def p_primary_expression_no_parenthesis_1(p):
	"""primary_expression_no_parenthesis : literal
		| invocation_expression
		| element_access
	"""
	p[0] = deepcopy(p[1])

def p_primary_expression_no_parenthesis_2(p):
	"""primary_expression_no_parenthesis : IDENTIFIER
	"""
	p[0] = {'code':[], 'value':p[1]}

def p_literal(p):
	"""literal : INTCONST
				| STRCONST
				| CHCONST
	"""
	p[0] = {}
	p[0]['code'] = [""]
	p[0]['value'] = p[1]

def p_parenthesized_expression(p):
	"""parenthesized_expression : LPAREN expression RPAREN
	"""
	p[0] = deepcopy(p[2])


def p_invocation_expression(p):
	"""invocation_expression : IDENTIFIER LPAREN argument_list_opt RPAREN
	"""
	p[0] = {'code':[], 'value':None}
	name = symbol_table.lookup(p[1], symbol_table.curr_table)
	if name != None:
		if name['category'] == 'function':
			arg_cnt = 0
			if p[3] != None:
				arg_cnt = len(p[3])
			if name['arg_num'] == arg_cnt:
				if arg_cnt > 0:
					for arg in p[3]:
						p[0]['code'] += arg['code']
					for arg in p[3]:
						p[0]['code'] += ['param, ' + arg['value']]
				if name['type'] != 'void':
					t = symbol_table.maketemp(name['type'], symbol_table.curr_table)
					p[0]['value'] = t
					p[0]['code'] += ['call, ' + p[1] + ', ' + str(arg_cnt) + ', ' + t]
				else:
					p[0]['code'] += ['call, ' + p[1] + ', ' + str(arg_cnt)]
			else:
				print("ERROR L", p.lineno(1), "Function", p[1], "needs exactly", name['arg_num'], "parameters, given", len(p[3]))
				print("Compilation Terminated")
				exit()
		else:
			print("ERROR L", p.lineno(1), "Function", p[1], "not defined as a function")
			print("Compilation Terminated")
			exit()			
	else:
		print("ERROR L", p.lineno(1), "Function", p[1], "not defined")
		print("Compilation Terminated")
		exit()


def p_argument_list_opt(p):
	"""argument_list_opt : empty 
		| argument_list
	"""
	p[0] = deepcopy(p[1])


def p_element_access(p):
	"""element_access : IDENTIFIER LBRACKET expression RBRACKET
	"""
	# Element Access for a 1D array
	p[0] = {'code':[], 'value':None}
	arr = symbol_table.lookup(p[1], symbol_table.curr_table)
	if arr != None:
		if arr['category'] == 'array':
			p[0]['code'] += p[3]['code']
			t1 = symbol_table.maketemp('int', symbol_table.curr_table)
			t2 = symbol_table.maketemp('int', symbol_table.curr_table)
			t = symbol_table.maketemp(arr['type'].elem_type, symbol_table.curr_table)
			p[0]['code'] += ['=, ' + t1 + ', ' + p[3]['value']]
			p[0]['code'] += ['*, ' + t2 + ', ' + t1 + ', ' + str(arr['type'].elem_type.width)]
			p[0]['code'] += ['member, ' + t + ', ' + p[1] + ', ' + t2]
			p[0]['value'] = t
		else:
			print("ERROR L", p.lineno(1), "Function", p[1], "not defined as an array")
			print("Compilation Terminated")
			exit()
	else:
		print("ERROR L", p.lineno(1), ": symbol", p[0], "used without declaration")
		print("Compilation Terminated")
		exit()

def p_postfix_expression(p):
	"""postfix_expression : primary_expression
	"""
	p[0] = deepcopy(p[1])

def p_unary_expression_not_plusminus(p):
	"""unary_expression_not_plusminus : postfix_expression
		| LNOT unary_expression
		| NOT unary_expression
	"""
	if len(p) == 2:
		p[0] = deepcopy(p[1])
	else:
		p[0] = deepcopy(p[2])
		if p[1] == '!':
			p[0]['code'] += ["!, " + p[0]['value']]
		elif p[1] == '~':
			# bitwise not ~ is available in x86
			p[0]['code'] += ["~, " + p[0]['value']]

def p_pre_increment_expression(p):
	"""pre_increment_expression : INCREMENT unary_expression
	"""
	t = symbol_table.maketemp('int', symbol_table.curr_table)
	p[0] = deepcopy(p[2])
	p[0]['code'] += ["+, " + t + ", 1, " + p[0]['value']]
	p[0]['code'] += ["=, " + p[0]['value'] + ", " + t]

def p_pre_decrement_expression(p):
	"""pre_decrement_expression : DECREMENT unary_expression
	"""
	t = symbol_table.maketemp('int', symbol_table.curr_table)
	p[0] = deepcopy(p[2])
	p[0]['code'] += ["-, " + t + ", 1, " + p[0]['value']]
	p[0]['code'] += ["=, " + p[0]['value'] + ", " + t]

def p_unary_expression(p):
	"""unary_expression : unary_expression_not_plusminus
		| PLUS unary_expression
		| MINUS unary_expression
		| pre_increment_expression
		| pre_decrement_expression
	"""
	p[0] = {}
	if len(p) == 2:
		p[0] = deepcopy(p[1])
	else:
		if p[1] == '+':
			p[0] = deepcopy(p[2])
		elif p[1] == '-':
			t = symbol_table.maketemp('int', symbol_table.curr_table)
			p[0]['value'] = t
			p[0]['code'] = deepcopy(p[2]['code'])
			p[0]['code'] += ["-, " + p[0]['value'] + ", " + p[2]['value'] + ", 0"]

def p_multiplicative_expression(p):
	"""multiplicative_expression : unary_expression
		| multiplicative_expression TIMES unary_expression	
		| multiplicative_expression DIVIDE unary_expression
		| multiplicative_expression MOD unary_expression
	"""
	if len(p) == 2:
		p[0] = deepcopy(p[1])
	else:
		p[0] = {}
		t = symbol_table.maketemp('int', symbol_table.curr_table)
		if p[2] == '*':		
			p[0]['value'] = t
			p[0]['code'] = p[1]['code'] + p[3]['code']
			p[0]['code'] += ["*, " + t + ", " + p[1]['value'] + ", " + p[3]['value']]
		elif p[2] == '/':		
			p[0]['value'] = t
			p[0]['code'] = p[1]['code'] + p[3]['code']
			p[0]['code'] += ["/, " + t + ", " + p[1]['value'] + ", " + p[3]['value']]
		elif p[2] == '%':
			p[0]['value'] = t
			p[0]['code'] = p[1]['code'] + p[3]['code']
			p[0]['code'] += ["%, " + t + ", " + p[1]['value'] + ", " + p[3]['value']]			

def p_additive_expression(p):
	"""additive_expression : multiplicative_expression
		| additive_expression PLUS multiplicative_expression
		| additive_expression MINUS multiplicative_expression
	"""
	if len(p) == 2:
		p[0] = deepcopy(p[1])
	else:
		p[0] = {}
		t = symbol_table.maketemp('int', symbol_table.curr_table)
		p[0]['value'] = t
		#print(p[1], p[2], p[3])
		p[0]['code'] = p[1]['code'] + p[3]['code']
		if p[2] == '+':
			p[0]['code'] += ["+, " + t + ", " + p[1]['value'] + ", " + p[3]['value']]
		elif p[2] == '-':
			p[0]['code'] += ["-, " + t + ", " + p[3]['value'] + ", " + p[1]['value']]


def p_shift_expression(p):
	"""shift_expression : additive_expression 
		| shift_expression LSHIFT additive_expression
		| shift_expression RSHIFT additive_expression
	"""
	if len(p) == 2:
		p[0] = deepcopy(p[1])
	else:
		p[0] = {}
		t = symbol_table.maketemp('int', symbol_table.curr_table)
		p[0]['value'] = t
		p[0]['code'] = p[1]['code'] + p[3]['code']
		if p[2] == '<<':
			p[0]['code'] += ["<<, " + t + ", " + p[1]['value'] + ", " + p[3]['value']]
		elif p[2] == '>>':
			p[0]['code'] += [">>, " + t + ", " + p[1]['value'] + ", " + p[3]['value']]


def p_relational_expression(p):
	"""relational_expression : shift_expression
		| relational_expression LT shift_expression
		| relational_expression GT shift_expression
	"""
	if len(p) == 2:
		p[0] = deepcopy(p[1])
	else:
		p[0] = {}
		t = symbol_table.maketemp('int', symbol_table.curr_table)
		p[0]['value'] = t
		p[0]['code'] = p[1]['code'] + p[3]['code']
		if p[2] == '<':
			p[0]['code'] += ["<, " + t + ", " + p[1]['value'] + ", " + p[3]['value']]
		elif p[2] == '>':
			p[0]['code'] += [">, " + t + ", " + p[1]['value'] + ", " + p[3]['value']]

def p_equality_expression(p):
	"""equality_expression : relational_expression
		| equality_expression EQ relational_expression
		| equality_expression NE relational_expression
	"""
	if len(p) == 2:
		p[0] = deepcopy(p[1])
	else:
		p[0] = {}
		t = symbol_table.maketemp('int', symbol_table.curr_table)
		p[0]['value'] = t
		p[0]['code'] = p[1]['code'] + p[3]['code']
		if p[2] == '==':
			p[0]['code'] += ["==, " + t + ", " + p[1]['value'] + ", " + p[3]['value']]
		elif p[2] == '!=':
			p[0]['code'] += ["!=, " + t + ", " + p[1]['value'] + ", " + p[3]['value']]

def p_and_expression(p):
	"""and_expression : equality_expression
	"""
	p[0] = deepcopy(p[1])

def p_exclusive_or_expression(p):
	"""exclusive_or_expression : and_expression
	"""
	p[0] = deepcopy(p[1])

def p_inclusive_or_expression(p):
	"""inclusive_or_expression : exclusive_or_expression
	"""
	p[0] = deepcopy(p[1])

def p_conditional_and_expression(p):
	"""conditional_and_expression : inclusive_or_expression
		| conditional_and_expression CAND inclusive_or_expression
	"""
	if len(p) == 2:
		p[0] = deepcopy(p[1])
	else:
		p[0] = {}
		t = symbol_table.maketemp('int', symbol_table.curr_table)
		p[0]['value'] = t
		p[0]['code'] = p[1]['code'] + p[3]['code']
		p[0]['code'] += ["&&, " + t + ", " + p[1]['value'] + ", " + p[3]['value']]	

def p_conditional_or_expression(p):
	"""conditional_or_expression : conditional_and_expression
		| conditional_or_expression COR conditional_and_expression
	"""
	if len(p) == 2:
		p[0] = deepcopy(p[1])
	else:
		p[0] = {}
		t = symbol_table.maketemp('int', symbol_table.curr_table)
		p[0]['value'] = t
		p[0]['code'] = p[1]['code'] + p[3]['code']
		p[0]['code'] += ["||, " + t + ", " + p[1]['value'] + ", " + p[3]['value']]

def p_conditional_expression(p):
	"""conditional_expression : conditional_or_expression
	"""
	p[0] = deepcopy(p[1])

def p_assignment(p):
	"""assignment : unary_expression assignment_operator expression
	"""
	var = symbol_table.lookup(p[1]['value'], symbol_table.curr_table)
	if var != None:
		p[0] = {}
		p[0]['value'] = p[1]['value']
		p[0]['code'] = p[3]['code']
		p[0]['code'] += p[1]['code']
		p[0]['code'] += ['=, ' + p[1]['value'] + ", " + p[3]['value']]
	else:
		print("ERROR: symbol", p[1]['value'], " used without declaration")
		print("Compilation Terminated")
		exit()

def p_assignment_operator(p):
	"""assignment_operator : EQUALS 
	"""
	p[0] = p[1]
def p_expression(p):
	"""expression : conditional_expression
		| assignment
	"""
	p[0] = deepcopy(p[1])
# def p_constant_expression(p):
# 	"""constant_expression : expression
# 	"""
# 	p[0] = deepcopy(p[1])
def p_boolean_expression(p):
	"""boolean_expression : expression
	"""
	p[0] = deepcopy(p[1])
# C.2.5 Statements 
def p_statement(p):
	"""statement : declaration_statement
		| embedded_statement
	"""
	p[0] = deepcopy(p[1])
def p_embedded_statement(p):
	"""embedded_statement : block
		| expression_statement
		| selection_statement
		| iteration_statement
		| jump_statement
	"""
	p[0] = deepcopy(p[1])
def p_block(p):
	"""block : LBRACE begin_scope statement_list_opt RBRACE
	"""
	p[0] = deepcopy(p[3])
	symbol_table.end_scope()
	
def p_statement_list_opt(p):
	"""statement_list_opt : empty 
		| statement_list
	"""
	p[0] = deepcopy(p[1])

def p_statement_list(p):
	"""statement_list : statement
		| statement_list statement
	"""
	p[0] = deepcopy(p[1])
	if len(p) == 3:
		p[0]['code'] += p[2]['code']
		p[0]['value'] = None

def p_declaration_statement(p):
	"""declaration_statement : local_variable_declaration STMT_TERMINATOR
	"""
	p[0] = deepcopy(p[1])


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# VARIABLE DECLARATION
def p_local_variable_declaration(p):
	"""local_variable_declaration : type variable_declarators
	"""
	# print(p[1], p[2])
	p[0] = {'code':[], 'value':None}
	# Implement variable declaration here
	var_type = p[1]
	for decl in p[2]:
		identifier, initializer, line = decl[0], decl[1], decl[2]
		if symbol_table.lookup_in_this(identifier) == None:
			# Generate the IR Code
			if initializer == None:
				# Not an array type
				if var_type.isbasic:
					symbol_table.insert_variable(var_type, identifier)
					p[0]['code'] += [var_type.name + ", " + identifier]
				elif var_type.isarray and var_type.elem_type.isbasic:
					symbol_table.insert_array(var_type, identifier)
					p[0]['code'] += ["array, " + var_type.elem_type + ", " + var_type.length + ", " + identifier]
			else:
				if var_type.isbasic:
					symbol_table.insert_variable(var_type, identifier)
					p[0]['code'] += initializer['code']
					p[0]['code'] += ["=, " + identifier + ", " + initializer['value']]
				elif var_type.isarray and var_type.elem_type.isbasic:
					# Update the length and width attributes of this array_type instance
					var_type.length = len(initializer)
					var_type.width = len(initializer)*var_type.elem_type.width
					symbol_table.insert_array(var_type, identifier)
					p[0]['code'] += ["array, " + var_type.elem_type.type_name() + ", " + str(len(initializer)) + ", " + identifier]
					# Initialize the values in the array
					for i in range(len(initializer)):
						p[0]['code'] += initializer[i]['code']
						p[0]['code'] += ['=, ' + identifier + ", " + str(i) + ", " + initializer[i]['value']]
		else:
			print("ERROR L", line, ": ", identifier, " has been declared before in this scope")
			print("Compilation Terminated")
			exit()


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------

def p_variable_declarators(p):
	"""variable_declarators : variable_declarator
		| variable_declarators COMMA variable_declarator
	"""
	if len(p) == 2:
		p[0] = [deepcopy(p[1])]
	else:
		p[0] = deepcopy(p[1])
		p[0].append(deepcopy(p[3]))
def p_variable_declarator(p):
	"""variable_declarator : IDENTIFIER
		| IDENTIFIER EQUALS variable_initializer 
	"""
	if len(p) == 2:
		p[0] = [p[1], None, p.lineno(1)]
	else:
		p[0] = [p[1], deepcopy(p[3]), p.lineno(1)]
def p_variable_initializer(p):
	"""variable_initializer : expression
		| array_initializer
	"""
	p[0] = deepcopy(p[1])

def p_array_initializer(p):
	"""array_initializer : LBRACE variable_initializer_list RBRACE
	"""
	p[0] = deepcopy(p[2])

def p_variable_initializer_list(p):
	"""variable_initializer_list : variable_initializer
		| variable_initializer_list COMMA variable_initializer
	"""
	if len(p) == 2:
		p[0] = [deepcopy(p[1])]
	else:
		p[0] = deepcopy(p[1]) + [deepcopy(p[3])]



def p_expression_statement(p):
	"""expression_statement : statement_expression STMT_TERMINATOR
	"""
	p[0] = deepcopy(p[1])
def p_statement_expression(p):
	"""statement_expression : invocation_expression
		| assignment
		| pre_increment_expression
		| pre_decrement_expression
	"""
	p[0] = deepcopy(p[1])
def p_selection_statement(p):
	"""selection_statement : if_statement
	"""
	p[0] = deepcopy(p[1])

def p_if_statement(p):
	"""if_statement : IF LPAREN boolean_expression RPAREN embedded_statement
		| IF LPAREN boolean_expression RPAREN embedded_statement ELSE embedded_statement
	"""
	p[0] = {'code':[], 'value':None}
	if len(p) == 6:
		p[3]['True'] = symbol_table.newlabel()
		p[3]['False'] = symbol_table.newlabel()
		p[0]['code'] += p[3]['code']
		p[0]['code'] += ['ifgoto, ==, 1, ' + p[3]['value'] + ", " + p[3]['True']]
		p[0]['code'] += ['goto, ' + p[3]['False']]
		p[0]['code'] += ['label, ' + p[3]['True']]
		p[0]['code'] += p[5]['code']
		p[0]['code'] += ['label, ' + p[3]['False']]
	else:
		p[3]['True'] = symbol_table.newlabel()
		p[0]['next'] = symbol_table.newlabel()
		p[0]['code'] += p[3]['code']
		p[0]['code'] += ['ifgoto, ==, 1, ' + p[3]['value'] + ", " + p[3]['True']]
		p[0]['code'] += p[7]['code']
		p[0]['code'] += ['goto, ' + p[0]['next']]
		p[0]['code'] += ['label, ' + p[3]['True']]
		p[0]['code'] += p[5]['code']
		p[0]['code'] += ['label, ' + p[0]['next']]			
	

def p_iteration_statement(p):
	"""iteration_statement : while_statement
		| for_statement
	"""
	p[0] = p[1]
def p_while_statement(p):
	"""while_statement : WHILE LPAREN boolean_expression RPAREN embedded_statement
	"""
	p[0] = {'code':[], 'value':None}
	p[0]['begin'] = symbol_table.newlabel()
	p[0]['next'] = symbol_table.newlabel()
	p[3]['True'] = symbol_table.newlabel()
	p[0]['code'] += ['label, ' + p[0]['begin']]
	p[0]['code'] += p[3]['code']
	p[0]['code'] += ['ifgoto, ==, 1, ' + p[3]['value'] + ", " + p[3]['True']]
	p[0]['code'] += ['goto, ' + p[0]['next']]
	p[0]['code'] += ['label, ' + p[3]['True']]
	p[0]['code'] += p[5]['code']
	p[0]['code'] += ['goto, ' + p[0]['begin']]
	p[0]['code'] += ['label, ' + p[0]['next']]

def p_for_statement(p):
	"""for_statement : FOR LPAREN for_initializer STMT_TERMINATOR for_condition STMT_TERMINATOR for_iterator RPAREN embedded_statement
	"""
	p[0] = {'code':[], 'value':None}
	p[0]['begin'] = symbol_table.newlabel()
	p[0]['next'] = symbol_table.newlabel()
	p[5]['True'] = symbol_table.newlabel()
	p[0]['code'] += p[3]['code']
	p[0]['code'] += ['label, ' + p[0]['begin']]
	p[0]['code'] += p[5]['code']
	p[0]['code'] += ['ifgoto, ==, 1, ' + p[5]['value'] + ", " + p[5]['True']]
	p[0]['code'] += ['goto, ' + p[0]['next']]
	p[0]['code'] += ['label, ' + p[5]['True']]
	p[0]['code'] += p[9]['code']
	p[0]['code'] += p[7]['code']
	p[0]['code'] += ['goto, ' + p[0]['begin']]
	p[0]['code'] += ['label, ' + p[0]['next']]

def p_for_initializer(p):
	"""for_initializer : local_variable_declaration
		| statement_expression_list
	"""
	p[0] = deepcopy(p[1])
def p_for_condition(p):
	"""for_condition : boolean_expression
	"""
	p[0] = deepcopy(p[1])
def p_for_iterator(p):
	"""for_iterator : statement_expression_list
	"""
	p[0] = deepcopy(p[1])
def p_statement_expression_list(p):
	"""statement_expression_list : statement_expression
		| statement_expression_list COMMA statement_expression
	"""
	if len(p) == 2:
		p[0] = deepcopy(p[1])
	else:
		p[0] = {}
		p[0]['code'] = p[1]['code']
		p[0]['code'] += p[3]['code']
		p[0]['value'] = None

def p_jump_statement(p):
	"""jump_statement : return_statement
	"""
	p[0] = deepcopy(p[1])
def p_return_statement(p):
	"""return_statement : RETURN expression_opt STMT_TERMINATOR
	"""
	p[0] = {'code':[], 'value':None}
	p[0]['code'] += p[2]['code']
	p[0]['code'] += ['return, ' + p[2]['value']]

def p_expression_opt(p):
	"""expression_opt : empty 
		| expression
	"""
	p[0] = p[1]

# Compilation Unit
def p_compilation_unit(p):
	"""compilation_unit : namespace_declaration
	"""
	p[0] = p[1]
	# print("PARSING DONE !!!")
	# # symbol_table.print_symbol_table()
	# # tac.generate_ircode(p[0]['code'])
	# print("----------------------------------------------------------------------")
	# print("SYMBOL TABLE")
	# print("----------------------------------------------------------------------")
	# symbol_table.print_symbol_table(symtab.base_table)
	# print("")
	# print("----------------------------------------------------------------------")
	# print("THREE ADDRESS CODE")
	# print("----------------------------------------------------------------------")
	tac.print_tac(p[0])
	print("")

def p_namespace_member_declarations_opt(p):
	"""namespace_member_declarations_opt : empty 
		| namespace_member_declarations
	"""
	p[0] = deepcopy(p[1])
def p_namespace_declaration(p):
	"""namespace_declaration :  NAMESPACE IDENTIFIER namespace_body
	"""
	p[0] = p[3]

def p_namespace_body(p):
	"""namespace_body : LBRACE namespace_member_declarations_opt RBRACE
	"""
	p[0] = p[2]
def p_namespace_member_declarations(p):
	"""namespace_member_declarations : namespace_member_declaration
	"""
	p[0] = p[1]

def p_namespace_member_declaration(p):
	"""namespace_member_declaration : type_declaration
	"""
	p[0] = p[1]
def p_type_declaration(p):
	"""type_declaration : class_declaration
	"""
	p[0] = p[1]


# C.2.6 Classes 
def p_class_declaration(p):
	"""class_declaration :  CLASS IDENTIFIER class_body
	"""
	p[0] = p[3]


def p_class_body(p):
	"""class_body : LBRACE class_member_declarations_opt RBRACE
	"""
	p[0] = deepcopy(p[2])
def p_class_member_declarations_opt(p):
	"""class_member_declarations_opt : empty 
		| class_member_declarations
	"""
	p[0] = p[1]
def p_class_member_declarations(p):
	"""class_member_declarations : class_member_declaration
		| class_member_declarations class_member_declaration
	"""
	if len(p) == 2:
		p[0] = [deepcopy(p[1])]
	else:
		p[0] = deepcopy(p[1]) + [deepcopy(p[2])]
def p_class_member_declaration(p):
	"""class_member_declaration : field_declaration
		| method_declaration
	"""
	p[0] = deepcopy(p[1])

def p_field_declaration(p):
	"""field_declaration :  type variable_declarators STMT_TERMINATOR
	"""
	# print(p[1], p[2])
	p[0] = {'code':[], 'value':None}
	# Implement variable declaration here
	var_type = p[1]
	for decl in p[2]:
		identifier, initializer, line = decl[0], decl[1], decl[2]
		if symbol_table.lookup_in_this(identifier) == None:
			# Generate the IR Code
			if initializer == None:
				# Not an array type
				if var_type.isbasic:
					symbol_table.insert_variable(var_type, identifier)
					p[0]['code'] += [var_type.name + ", " + identifier]
				elif var_type.isarray and var_type.elem_type.isbasic:
					symbol_table.insert_array(var_type, identifier)
					p[0]['code'] += ["array, " + var_type.elem_type + ", " + var_type.length + ", " + identifier]
			else:
				if var_type.isbasic:
					symbol_table.insert_variable(var_type, identifier)
					p[0]['code'] += initializer['code']
					p[0]['code'] += ["=, " + identifier + ", " + initializer['value']]
				elif var_type.isarray and var_type.elem_type.isbasic:
					# Update the length and width attributes of this array_type instance
					var_type.length = len(initializer)
					var_type.width = len(initializer)*var_type.elem_type.width
					symbol_table.insert_array(var_type, identifier)
					p[0]['code'] += ["array, " + var_type.elem_type.type_name() + ", " + str(len(initializer)) + ", " + identifier]
					# Initialize the values in the array
					for i in range(len(initializer)):
						p[0]['code'] += initializer[i]['code']
						p[0]['code'] += ['=, ' + identifier + ", " + str(i) + ", " + initializer[i]['value']]
		else:
			print("ERROR L", line, ": ", identifier, " has been declared before in this scope")
			print("Compilation Terminated")
			exit()
		
def p_method_declaration(p):
	"""method_declaration : method_header method_body
	"""
	return_type = p[1][0]
	method_name = p[1][1]
	method_params = p[1][2]
	method_body = p[2]
	p[0] = {'code':[], 'value':None}
	p[0]['code'] += ['function, ' + method_name]
	if method_params != None:
		for param in method_params:
			# parameters would have been pushed to the stack, so we just pop them off
			p[0]['code'] += ['pop, ' + param[1]]
	p[0]['code'] += p[2]['code']
	# type, category, arg_num are the parameters needed in the symbol table entry against the function name
	

def p_method_header(p):
	"""method_header :  type IDENTIFIER LPAREN formal_parameter_list_opt RPAREN
	"""
	p[0] = [p[1], p[2], p[4]]
	method_params = p[4]
	param_types = []
	param_num = 0
	if method_params != None:
		param_types = [param[0] for param in method_params]
		param_num = len(method_params)
	symbol_table.insert_function(p[2], p[1], param_types, param_num)


def p_formal_parameter_list_opt(p):
	"""formal_parameter_list_opt : empty 
		| formal_parameter_list
	"""
	p[0] = p[1]

def p_method_body(p):
	"""method_body : block
	"""
	p[0] = deepcopy(p[1])

def p_formal_parameter_list(p):
	"""formal_parameter_list : formal_parameter
		| formal_parameter_list COMMA formal_parameter
	"""
	if len(p) == 2:
		p[0] = [deepcopy(p[1])]
	else:
		p[0] = deepcopy(p[1]) + [deepcopy(p[3])]

def p_formal_parameter(p):
	"""formal_parameter : type IDENTIFIER
	"""
	p[0] = [p[1],p[2]]


def p_begin_scope(p):
	"""begin_scope : empty
	"""
	p[0] = p[1]
	symbol_table.begin_scope()
	#print("returned from begin_scope")

def p_empty(p):
	"""empty :"""
	p[0] = None

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!", p)

###################################################################################################
# Build the parser now
parser = yacc.yacc(start='compilation_unit', debug=True, optimize=False)

# Read the input program
inputfile = open(filename, 'r')
data = inputfile.read()
result = parser.parse(data, debug=0)