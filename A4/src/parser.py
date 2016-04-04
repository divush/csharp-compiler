#!/usr/bin/python3
# Parser for C# in Python

# Grammar Specification Reference
# https://msdn.microsoft.com/en-in/library/aa664812(v=vs.71).aspx
# With some modifications to resolve conflicts

# Authors: Divyanshu Shende, Pranshu Gupta, Prashant Kumar, Rahul Tudu
# Compiler Design: CS335A, Group 25, Indian Institute of Technology, Kanpur
###################################################################################################

import sys
import ply.yacc as yacc
from lexer import *
from irgen import *

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
	('left', 'MEMBERACCESS')
)
#The Symbol Table and its interface. symbol_table.table is the symbol table. 
#It contains identifier:scope pairs.
#symbol_table.Insert(identifier, scope) ---> add ident:scope pair to the table.
#symbol_table.Insert(identifier) ---> look for ident entry in table. if found, return lexeme, else return None.
# class symbol_table:
# 	self.table={}
# 	def __init__(self, reserved):
# 		self.table.fromkeys(list(reserved.keys()))

# 	def Insert(ident, vartype, scope):
# 		self.table[ident] = [vartype, scope]
# 		pass

# 	def Lookup(ident):
# 		if ident in self.table.keys:
# 			return ident
# 		else:
# 			return None

# symtab = symbol_table() 

# C.2.1 Basic concepts 
def p_namespace_name(p):
	"""namespace_name : qualified_identifier
	"""
	p[0] = p[1]
def p_type_name(p):
	"""type_name : qualified_identifier
	"""
	p[0] = p[1]
# C.2.2 Types 
def p_type(p):
	"""type : non_array_type
		| array_type
	"""
	p[0] = p[1]
def p_non_array_type(p):
	"""non_array_type : simple_type
		| type_name
	"""
	p[0] = p[1]
def p_simple_type(p):
	"""simple_type : primitive_type
		| class_type
		| pointer_type
	"""
	p[0] = p[1]
def p_primitive_type(p):
	"""primitive_type : numeric_type
		| BOOL
	"""
	p[0] = p[1]
def p_numeric_type(p):
	"""numeric_type : integral_type
		| floating_point_type
		| DECIMAL
	"""
	p[0] = p[1]
def p_integral_type(p):
	"""integral_type : SBYTE 
					| BYTE 
					| SHORT 
					| USHORT 
					| INT 
					| UINT 
					| LONG 
					| ULONG 
					| CHAR
	"""
	p[0] = p[1]
def p_floating_point_type(p):
	"""floating_point_type : FLOAT 
						| DOUBLE
	"""
	p[0] = p[1]
def p_class_type(p):
	"""class_type : OBJECT 
					| STRING
	"""
	p[0] = p[1]
def p_pointer_type(p):
	"""pointer_type : type dereferencer
		| VOID dereferencer
	"""
	p[0] = pointer(p[1])
def p_dereferencer(p):
	"""dereferencer : TIMES
	"""
	p[0] = p[1]
# This constructs a new 'array data type'
def p_array_type(p):
	"""array_type : array_type rank_specifier
		| simple_type rank_specifier
		| qualified_identifier rank_specifier
	"""
	# p[1] is the type of array elements and p[2] gives the length of the array type
	p[0] = create_array_type(p[1], p[2])
def p_rank_specifier(p):
	"""rank_specifier : LBRACKET dim_separators_opt RBRACKET
	"""
	p[0] = p[2]
def p_dim_separators_opt(p): 
	"""dim_separators_opt : empty 
			| dim_separators"""
	p[0] = p[1] 
def p_dim_separators(p):
	"""dim_separators : COMMA
				| dim_separators COMMA
	"""
	if len(p) == 2:
		p[0] = 1
	else:
		p[0] = p[1] + 1

# C.2.3 Variables 
def p_variable_reference(p):
	"""variable_reference : expression
	"""
	p[0] = p[1]
# C.2.4 Expressions 
def p_argument_list(p):
	"""argument_list : argument
		| argument_list COMMA argument
	"""
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = p[1] + [p[3]]
def p_argument(p):
	"""argument : expression
		| REF variable_reference
		| OUT variable_reference
	"""
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = p[2]
def p_primary_expression(p):
	"""primary_expression : parenthesized_expression
		| primary_expression_no_parenthesis
		| anonymous_method_expression
	"""
	p[0] = p[1]
def p_primary_expression_no_parenthesis(p):
	"""primary_expression_no_parenthesis : literal
		| array_creation_expression
		| member_access
		| invocation_expression
		| element_access
		| this_access
		| base_access
		| new_expression
		| typeof_expression
		| sizeof_expression
		| checked_expression
		| unchecked_expression
	"""
	p[0] = p[1]
# Literal
def p_literal(p):
	"""literal : INTCONST
				| STRCONST
				| CHCONST
	"""
	p[0] = p[1]
def p_parenthesized_expression(p):
	"""parenthesized_expression : LPAREN expression RPAREN
	"""
	p[0] = p[2]
def p_member_access(p):
	"""member_access : primary_expression MEMBERACCESS IDENTIFIER
		| primitive_type MEMBERACCESS IDENTIFIER
		| class_type MEMBERACCESS IDENTIFIER
	"""
	p[0] = get_member_value(p[1], p[3])

def p_invocation_expression(p):
	"""invocation_expression : primary_expression_no_parenthesis LPAREN argument_list_opt RPAREN
		| qualified_identifier LPAREN argument_list_opt RPAREN
	"""
	p[0] = function_call(p[1], p[3])  
def p_argument_list_opt(p):
	"""argument_list_opt : empty 
		| argument_list
	"""
	p[0] = p[1]
# This is for accessing an element of an array with a given index
def p_element_access(p):
	"""element_access : primary_expression LBRACKET expression_list RBRACKET
		| qualified_identifier LBRACKET expression_list RBRACKET
	"""
	array, index = p[1], p[2]
	p[0] = get_array_element(array, index)
def p_expression_list(p):
	"""expression_list : expression
		| expression_list COMMA expression
	"""
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = p[1] + [p[3]]
def p_this_access(p):
	"""this_access : THIS
	"""
	p[0] = p[1]
def p_base_access(p):
	"""base_access : BASE MEMBERACCESS IDENTIFIER
		| BASE LBRACKET expression_list RBRACKET
	"""

def p_post_increment_expression(p):
	"""post_increment_expression : postfix_expression INCREMENT
	"""
	p[0] = post_increment_expression(p[1])
def p_post_decrement_expression(p):
	"""post_decrement_expression : postfix_expression DECREMENT
	"""
	p[0] = post_decrement_expression(p[1])
def p_new_expression(p):
	"""new_expression : object_creation_expression
	"""
	p[0] = p[1]
def p_object_creation_expression(p):
	"""object_creation_expression : NEW type LPAREN argument_list_opt RPAREN
	"""
	p[0] = create_new_object(p[2], p[4])
def p_array_creation_expression(p):
	"""array_creation_expression : NEW non_array_type LBRACKET expression_list RBRACKET array_initializer_opt
		| NEW array_type array_initializer
	"""
	if len(p) == 7:
		# Array creation of the form e.g., new int[5] {1, 2, 3, 4, 5}
		p[0] = create_array_from_basic(p[2], p[4], p[5])
	else:
		p[0] = create_array_from_array(p[2], p[3])

def p_array_initializer_opt(p):
	"""array_initializer_opt : empty 
		| array_initializer
	"""
	p[0] = p[1]
def p_typeof_expression(p):
	"""typeof_expression : TYPEOF LPAREN type RPAREN
		| TYPEOF LPAREN VOID RPAREN
	"""
	p[0] = typeof_expr([3])
def p_checked_expression(p):
	"""checked_expression : CHECKED LPAREN expression RPAREN
	"""
	p[0] = p[3]
def p_unchecked_expression(p):
	"""unchecked_expression : UNCHECKED LPAREN expression RPAREN
	"""
	p[0] = p[3]
def p_pointer_member_access(p):
	"""pointer_member_access : postfix_expression ARROW IDENTIFIER
	"""
	p[0] = get_member_value_via_pointer(p[1], p[3])
def p_addressof_expression(p):
	"""addressof_expression : AND unary_expression
	"""
	p[0] = address_of(p[2])
def p_sizeof_expression(p):
	"""sizeof_expression : SIZEOF LPAREN type RPAREN
	"""
	p[0] = sizeof(p[3])
def p_postfix_expression(p):
	"""postfix_expression : primary_expression
		| qualified_identifier
		| post_increment_expression
		| post_decrement_expression
		| pointer_member_access
	"""
	p[0] = p[1]
def p_unary_expression_not_plusminus(p):
	"""unary_expression_not_plusminus : postfix_expression
		| LNOT unary_expression
		| NOT unary_expression
	"""
	if len(p) == 2:
		p[0] = p[1]
	elif len(p) == 3:
		if p[1] == 'LNOT':
			p[0] = logical_not_of(p[2])
		elif p[1] == 'NOT':
			p[0] = not_of(p[2])
def p_pre_increment_expression(p):
	"""pre_increment_expression : INCREMENT unary_expression
	"""
	p[0] = pre_increment_expression(p[2])
def p_pre_decrement_expression(p):
	"""pre_decrement_expression : DECREMENT unary_expression
	"""
	p[0] = pre_decrement_expression(p[2])
def p_unary_expression(p):
	"""unary_expression : unary_expression_not_plusminus
		| PLUS unary_expression
		| MINUS unary_expression
		| TIMES unary_expression
		| pre_increment_expression
		| pre_decrement_expression
		| addressof_expression
	"""
	p[0] = p[1]

def p_type_quals_opt(p):
	"""type_quals_opt : empty 
		| type_quals
	"""
	p[0] = p[1]
def p_type_quals(p):
	"""type_quals : type_qual
		| type_quals type_qual
	"""
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = p[1] + [p[2]]
def p_type_qual (p):
	"""type_qual  : rank_specifier 
		| dereferencer
	"""
	p[0] = p[1]
def p_multiplicative_expression(p):
	"""multiplicative_expression : unary_expression
		| multiplicative_expression TIMES unary_expression	
		| multiplicative_expression DIVIDE unary_expression
		| multiplicative_expression MOD unary_expression
	"""
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = expression(p[1], p[2], p[3])

def p_additive_expression(p):
	"""additive_expression : multiplicative_expression
		| additive_expression PLUS multiplicative_expression
		| additive_expression MINUS multiplicative_expression
	"""
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = expression(p[1], p[2], p[3])

def p_shift_expression(p):
	"""shift_expression : additive_expression 
		| shift_expression LSHIFT additive_expression
		| shift_expression RSHIFT additive_expression
	"""
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = expression(p[1], p[2], p[3])

def p_relational_expression(p):
	"""relational_expression : shift_expression
		| relational_expression LT shift_expression
		| relational_expression GT shift_expression
		| relational_expression LE shift_expression
		| relational_expression GE shift_expression
	"""
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = expression(p[1], p[2], p[3])
def p_equality_expression(p):
	"""equality_expression : relational_expression
		| equality_expression EQ relational_expression
		| equality_expression NE relational_expression
	"""
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = expression(p[1], p[2], p[3])
def p_and_expression(p):
	"""and_expression : equality_expression
		| and_expression AND equality_expression
	"""
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = create_and_expression(p[1], p[3])
def p_exclusive_or_expression(p):
	"""exclusive_or_expression : and_expression
		| exclusive_or_expression XOR and_expression
	"""
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = create_xor_expression(p[1], p[3])	
def p_inclusive_or_expression(p):
	"""inclusive_or_expression : exclusive_or_expression
		| inclusive_or_expression OR exclusive_or_expression
	"""
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = create_or_expression(p[1], p[3])
def p_conditional_and_expression(p):
	"""conditional_and_expression : inclusive_or_expression
		| conditional_and_expression CAND inclusive_or_expression
	"""
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = create_cand_expression(p[1], p[3])
def p_conditional_or_expression(p):
	"""conditional_or_expression : conditional_and_expression
		| conditional_or_expression COR conditional_and_expression
	"""
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = create_cor_expression(p[1], p[3])
def p_conditional_expression(p):
	"""conditional_expression : conditional_or_expression
		| conditional_or_expression CONDOP expression COLON expression
	"""
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = condop_expression(p[1], p[3], p[5])
def p_assignment(p):
	"""assignment : unary_expression assignment_operator expression
	"""
	p[0] = assignment(p[1], p[2], p[3])
def p_assignment_operator(p):
	"""assignment_operator : EQUALS 
							| PLUSEQUAL
							| MINUSEQUAL 
							| TIMESEQUAL 
							| DIVEQUAL 
							| MODEQUAL
							| XOREQUAL
							| ANDEQUAL
							| OREQUAL
							| RSHIFTEQUAL
							| LSHIFTEQUAL
	"""
	p[0] = p[1]
def p_expression(p):
	"""expression : conditional_expression
		| lambda_expression
		| assignment
	"""
	p[0] = p[1]
def p_constant_expression(p):
	"""constant_expression : expression
	"""
	p[0] = p[1]
def p_boolean_expression(p):
	"""boolean_expression : expression
	"""
	p[0] = p[1]
# C.2.5 Statements 
def p_statement(p):
	"""statement : labeled_statement
		| declaration_statement
		| embedded_statement
	"""
	p[0] = p[1]
def p_embedded_statement(p):
	"""embedded_statement : block
		| empty_statement
		| expression_statement
		| selection_statement
		| iteration_statement
		| jump_statement
		| checked_statement
		| unchecked_statement
		| unsafe_statement
	"""
	p[0] = p[1]
def p_block(p):
	"""block : LBRACE statement_list_opt RBRACE
	"""
	p[0] = p[2]
def p_statement_list_opt(p):
	"""statement_list_opt : empty 
		| statement_list
	"""
	p[0] = p[1]
def p_statement_list(p):
	"""statement_list : statement
		| statement_list statement
	"""
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = p[1] + [p[2]]
def p_empty_statement(p):
	"""empty_statement : STMT_TERMINATOR
	"""
	p[0] = p[1]

def p_labeled_statement(p):
	"""labeled_statement : IDENTIFIER COLON statement
	"""
	p[0] = create_labeled_statement(p[1], p[3])

# Declaration Statements
def p_declaration_statement(p):
	"""declaration_statement : local_variable_declaration STMT_TERMINATOR
		| local_constant_declaration STMT_TERMINATOR
	"""
	p[0] = p[1]
def p_local_variable_declaration(p):
	"""local_variable_declaration : type variable_declarators
	"""
	p[0] = declare_variables([], p[1], p[2])
def p_variable_declarators(p):
	"""variable_declarators : variable_declarator
		| variable_declarators COMMA variable_declarator
	"""

def p_variable_declarator(p):
	"""variable_declarator : IDENTIFIER
		| IDENTIFIER EQUALS variable_initializer
	"""
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = [p[1], p[2]]
def p_variable_initializer(p):
	"""variable_initializer : expression
		| array_initializer
	"""
	p[0] = p[1]

def p_local_constant_declaration(p):
	"""local_constant_declaration : CONST type constant_declarators
	"""
	p[0] = declare_constants([], p[2],p[3])
def p_constant_declarators(p):
	"""constant_declarators : constant_declarator
		| constant_declarators COMMA constant_declarator
	"""
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = p[1] + [p[2]]
def p_constant_declarator(p):
	"""constant_declarator : IDENTIFIER EQUALS constant_expression
	"""
	p[0] = [p[1],p[3]]
def p_expression_statement(p):
	"""expression_statement : statement_expression STMT_TERMINATOR
	"""
	p[0] = p[1]
def p_statement_expression(p):
	"""statement_expression : invocation_expression
		| object_creation_expression
		| assignment
		| post_increment_expression
		| post_decrement_expression
		| pre_increment_expression
		| pre_decrement_expression
	"""
	p[0] = p[1]
def p_selection_statement(p):
	"""selection_statement : if_statement
		| switch_statement
	"""
	p[0] = p[1]
def p_if_statement(p):
	"""if_statement : IF LPAREN boolean_expression RPAREN embedded_statement
		| IF LPAREN boolean_expression RPAREN embedded_statement ELSE embedded_statement
	"""
	if len(p) == 6:
		p[0] = create_if_statement(p[3], p[5])
	else:
		p[0] = create_if_else_statement(p[3], p[5], p[7])
def p_switch_statement(p):
	"""switch_statement : SWITCH LPAREN expression RPAREN switch_block
	"""
	p[0] = create_switch_statement(p[3], p[5])
def p_switch_block(p):
	"""switch_block : LBRACE switch_sections_opt RBRACE
	"""
	p[0] = p[2]
def p_switch_sections_opt(p):
	"""switch_sections_opt : empty 
		| switch_sections
	"""
	p[0] = p[1]
def p_switch_sections(p):
	"""switch_sections : switch_section
		| switch_sections switch_section
	"""
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = p[1] + [p[2]]
def p_switch_section(p):
	"""switch_section : switch_labels statement_list
	"""
	p[0] = create_switch_section(p[1], p[2])
def p_switch_labels(p):
	"""switch_labels : switch_label
		| switch_labels switch_label
	"""
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = p[1] + [p[2]]
def p_switch_label(p):
	"""switch_label : CASE constant_expression COLON
		| DEFAULT COLON
	"""
	if len(p) == 4:
		p[0] = p[2]
	else:
		p[0] = p[1]
def p_iteration_statement(p):
	"""iteration_statement : while_statement
		| for_statement
	"""
	p[0] = p[1]
def p_unsafe_statement(p):
	"""unsafe_statement : UNSAFE block
	"""
	p[0] = p[1]
def p_while_statement(p):
	"""while_statement : WHILE LPAREN boolean_expression RPAREN embedded_statement
	"""
	p[0] = create_while_statement(p[3], p[5])
def p_for_statement(p):
	"""for_statement : FOR LPAREN for_initializer_opt STMT_TERMINATOR for_condition_opt STMT_TERMINATOR for_iterator_opt RPAREN embedded_statement
	"""
	p[0] = create_for_statement(p[3], p[5], p[7], p[9])
def p_for_initializer_opt(p):
	"""for_initializer_opt : empty 
		| for_initializer
	"""
	p[0] = p[1]
def p_for_condition_opt(p):
	"""for_condition_opt : empty 
		| for_condition
	"""
	p[0] = p[1]
def p_for_iterator_opt(p):
	"""for_iterator_opt : empty 
		| for_iterator
	"""
	p[0] = p[1]
def p_for_initializer(p):
	"""for_initializer : local_variable_declaration
		| statement_expression_list
	"""
	p[0] = p[1]
def p_for_condition(p):
	"""for_condition : boolean_expression
	"""
	p[0] = p[1]
def p_for_iterator(p):
	"""for_iterator : statement_expression_list
	"""
	p[0] = p[1]
def p_statement_expression_list(p):
	"""statement_expression_list : statement_expression
		| statement_expression_list COMMA statement_expression
	"""
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = p[1] + [p[3]]

def p_jump_statement(p):
	"""jump_statement : break_statement
		| continue_statement
		| return_statement
	"""
	p[0] = p[1]
def p_break_statement(p):
	"""break_statement : BREAK STMT_TERMINATOR
	"""
	p[0] = p[1]
def p_continue_statement(p):
	"""continue_statement : CONTINUE STMT_TERMINATOR
	"""
	p[0] = p[1]

def p_return_statement(p):
	"""return_statement : RETURN expression_opt STMT_TERMINATOR
	"""
	p[0] = create_return_statement(p[2])
def p_expression_opt(p):
	"""expression_opt : empty 
		| expression
	"""
	p[0] = p[1]

# def p_throw_statement(p):
# 	"""throw_statement : THROW expression_opt STMT_TERMINATOR
# 	"""
# 	p[0] = create_throw_statement()
# def p_try_statement(p):
# 	"""try_statement : TRY block catch_clauses
# 		| TRY block finally_clause
# 		| TRY block catch_clauses finally_clause
# 	"""
# def p_catch_clauses(p):
# 	"""catch_clauses : catch_clause
# 		| catch_clauses catch_clause
# 	"""
# 	if len(p) == 2:
# 		p[0] = [p[1]]
# 	else:
# 		p[0] = p[1].append(p[2])
# def p_catch_clause(p):
# 	"""catch_clause : CATCH LPAREN class_type identifier_opt RPAREN block
# 		| CATCH LPAREN type_name identifier_opt RPAREN block
# 		| CATCH block
# 	"""

def p_identifier_opt(p):
	"""identifier_opt : empty 
		| IDENTIFIER
	"""
	p[0] = p[1]

# def p_finally_clause(p):
# 	"""finally_clause : FINALLY block
# 	"""
def p_checked_statement(p):
	"""checked_statement : CHECKED block
	"""
	p[0] = p[2]
def p_unchecked_statement(p):
	"""unchecked_statement : UNCHECKED block
	"""
	p[0] = p[2]

# def p_lock_statement(p):
# 	"""lock_statement : LOCK LPAREN expression RPAREN embedded_statement
# 	"""
# def p_using_statement(p):
# 	"""using_statement : USING LPAREN resource_acquisition RPAREN embedded_statement
# 	"""
# def p_resource_acquisition(p):
# 	"""resource_acquisition : local_variable_declaration
# 		| expression
# 	"""
# def p_fixed_statement(p):
# 	"""fixed_statement : FIXED LPAREN	type fixed_pointer_declarators RPAREN embedded_statement
# 	"""
# def p_fixed_pointer_declarators(p):
# 	"""fixed_pointer_declarators : fixed_pointer_declarator
# 		| fixed_pointer_declarators COMMA fixed_pointer_declarator
# 	"""
# def p_fixed_pointer_declarator(p):
# 	"""fixed_pointer_declarator : IDENTIFIER EQUALS expression
# 	"""

# Lambda Expressions
def p_lambda_expression(p):
	"""lambda_expression : explicit_anonymous_function_signature LAMBDADEC block
						| explicit_anonymous_function_signature LAMBDADEC expression
	"""
	p[0] = create_lambda_expression(p[1], p[3])

# # Anonymous Method Expression
# def p_anonymous_method_expression(p):
# 	"""anonymous_method_expression : DELEGATE explicit_anonymous_function_signature_opt block
# 	"""	
# def p_explicit_anonymous_function_signature_opt(p):
# 	"""explicit_anonymous_function_signature_opt : explicit_anonymous_function_signature
# 												| empty
# 	"""
# 	p[0] = p[1]

def p_explicit_anonymous_function_signature(p):
	"""explicit_anonymous_function_signature : LPAREN explicit_anonymous_function_parameter_list_opt RPAREN
	"""
	p[0] = p[2]
def p_explicit_anonymous_function_parameter_list_opt(p):
	"""explicit_anonymous_function_parameter_list_opt : explicit_anonymous_function_parameter_list
														| empty
	"""
	p[0] = p[1]
def p_explicit_anonymous_function_parameter_list(p):
	"""explicit_anonymous_function_parameter_list : explicit_anonymous_function_parameter
													| explicit_anonymous_function_parameter_list COMMA explicit_anonymous_function_parameter
	"""
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = p[1] + [p[2]]
def p_explicit_anonymous_function_parameter(p):
	"""explicit_anonymous_function_parameter : type IDENTIFIER
	"""	
	p[0] = [p[1],p[2]]

# Compilation Unit
def p_compilation_unit(p):
	"""compilation_unit : using_directives_opt
		| using_directives_opt namespace_member_declarations
	"""
	p[0] = [p[1]]
	if len(p) == 3:
		p[0].append(p[1])

def p_using_directives_opt(p):
	"""using_directives_opt : empty 
		| using_directives
	"""
	p[0] = p[1]
def p_namespace_member_declarations_opt(p):
	"""namespace_member_declarations_opt : empty 
		| namespace_member_declarations
	"""
	p[0] = p[1]
def p_namespace_declaration(p):
	"""namespace_declaration :  NAMESPACE qualified_identifier namespace_body stmt_term_opt
	"""
	p[0] = create_namespace(p[2],p[3])
def p_stmt_term_opt(p):
	"""stmt_term_opt : empty 
		| STMT_TERMINATOR
	"""
	p[0] = p[1]
def p_qualified_identifier(p):
	"""qualified_identifier : IDENTIFIER
		| qualifier IDENTIFIER
	"""
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = p[1] + [p[2]]
def p_qualifier(p):
	"""qualifier : IDENTIFIER MEMBERACCESS 
		| qualifier IDENTIFIER MEMBERACCESS 
	"""
	if len(p) == 3:
		p[0] = [p[1]]
	else:
		p[0] = p[1] + [p[2]]
def p_namespace_body(p):
	"""namespace_body : LBRACE using_directives_opt namespace_member_declarations_opt RBRACE
	"""
	p[0] = [p[2],p[3]]
def p_using_directives(p):
	"""using_directives : using_directive
		| using_directives using_directive
	"""
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = p[1] + [p[2]]
def p_using_directive(p):
	"""using_directive : using_alias_directive
		| using_namespace_directive
	"""
	p[0] = p[1]
def p_using_alias_directive(p):
	"""using_alias_directive : USING IDENTIFIER EQUALS qualified_identifier STMT_TERMINATOR
	"""
	p[0] = create_identifier_alias(p[2], p[4])
def p_using_namespace_directive(p):
	"""using_namespace_directive : USING namespace_name STMT_TERMINATOR
	"""
	p[0] = create_using_namespace_directive(p[2])
def p_namespace_member_declarations(p):
	"""namespace_member_declarations : namespace_member_declaration
		| namespace_member_declarations namespace_member_declaration
	"""
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = p[1] + [p[2]]
def p_namespace_member_declaration(p):
	"""namespace_member_declaration : namespace_declaration
		| type_declaration
	"""
	p[0] = p[1]
def p_type_declaration(p):
	"""type_declaration : class_declaration
		| struct_declaration
		| enum_declaration
		| delegate_declaration
	"""
	p[0] = p[1]
# Modifiers
 
def p_modifiers_opt(p):
	"""modifiers_opt : empty 
		| modifiers
	"""
	p[0] = p[1]
def p_modifiers(p):
	"""modifiers : modifier
		| modifiers modifier
	"""
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = p[1] + [p[2]]
def p_modifier(p):
	"""modifier : ABSTRACT
		| EXTERN
		| INTERNAL
		| NEW
		| OVERRIDE
		| PRIVATE
		| PROTECTED
		| PUBLIC
		| READONLY
		| SEALED
		| STATIC
		| UNSAFE
		| VIRTUAL
		| VOLATILE
	"""
	p[0] = p[1]
# C.2.6 Classes 
def p_class_declaration(p):
	"""class_declaration :  modifiers_opt CLASS IDENTIFIER class_base_opt class_body stmt_term_opt
	"""
	# create_class(modifiers, identifier, base, body)
	p[0] = create_class(p[1], p[3], p[4], p[5])
def p_class_base_opt(p):
	"""class_base_opt : empty 
		| class_base
	"""
	p[0] = p[1]
def p_class_base(p):
	"""class_base : COLON class_type
	"""
	p[0] = p[2]
def p_class_body(p):
	"""class_body : LBRACE class_member_declarations_opt RBRACE
	"""
	p[0] = p[2]
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
		p[0] = [p[1]]
	else:
		p[0] = p[1] + [p[2]]
def p_class_member_declaration(p):
	"""class_member_declaration : constant_declaration
		| field_declaration
		| method_declaration
		| operator_declaration
		| constructor_declaration
		| destructor_declaration 
		| type_declaration
	"""
	p[0] = p[1]
def p_constant_declaration(p):
	"""constant_declaration :  modifiers_opt CONST type constant_declarators STMT_TERMINATOR
	"""
	p[0] = declare_constants(p[1],p[3],p[4])
def p_field_declaration(p):
	"""field_declaration :  modifiers_opt type variable_declarators STMT_TERMINATOR
	"""
	p[0] = declare_variables(p[1],p[2],p[3])
def p_method_declaration(p):
	"""method_declaration : method_header method_body
	"""
	p[0] = create_method(p[1],p[2])
def p_method_header(p):
	"""method_header :  modifiers_opt type qualified_identifier LPAREN formal_parameter_list_opt RPAREN
					 |  modifiers_opt VOID qualified_identifier LPAREN formal_parameter_list_opt RPAREN
	"""
	p[0] = [p[1], p[2], p[3], p[5]]
def p_formal_parameter_list_opt(p):
	"""formal_parameter_list_opt : empty 
		| formal_parameter_list
	"""
	p[0] = p[1]
def p_return_type(p):
	"""return_type : type
		| VOID
	"""
	p[0] = p[1]
def p_method_body(p):
	"""method_body : block
		| STMT_TERMINATOR
	"""
	p[0] = p[1]
def p_formal_parameter_list(p):
	"""formal_parameter_list : formal_parameter
		| formal_parameter_list COMMA formal_parameter
	"""
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = p[1] + [p[2]]
def p_formal_parameter(p):
	"""formal_parameter : parameter_array
	"""
	p[0] = p[1]

# def p_fixed_parameter(p):
# 	"""fixed_parameter :  parameter_modifier_opt type IDENTIFIER
# 	"""
# def p_parameter_modifier_opt(p):
# 	"""parameter_modifier_opt : empty 
# 		| REF
# 		| OUT
# 	"""

	p[0] = p[1]
def p_parameter_array(p):
	"""parameter_array :  PARAMS type IDENTIFIER
	"""
	p[0] = [p[2],p[3]]
 
def p_operator_declaration(p):
	"""operator_declaration :  modifiers_opt operator_declarator operator_body
	"""
	p[0] = create_operator_declaration(p[1], p[2], p[3])
def p_operator_declarator(p):
	"""operator_declarator : overloadable_operator_declarator
	"""
	p[0] = p[1]
def p_overloadable_operator_declarator(p):
	"""overloadable_operator_declarator : type OPERATOR overloadable_operator LPAREN type IDENTIFIER RPAREN
										| type OPERATOR overloadable_operator LPAREN type IDENTIFIER COMMA type IDENTIFIER RPAREN
	"""
	if len(p) == 8:
		p[0] = create_overloadable_unary_operator_declarator(p[1], p[3], p[5], p[6])
	else:
		p[0] = create_overloadable_binary_operator_declarator(p[1], p[3], p[5], p[6], p[8], p[9])
def p_overloadable_operator(p):
	"""overloadable_operator : PLUS 
							| MINUS 
							| LNOT 
							| NOT 
							| INCREMENT 
							| DECREMENT 
							| TRUE 
							| FALSE
							| TIMES 
							| DIVIDE 
							| MOD 
							| AND 
							| OR 
							| XOR 
							| LSHIFT 
							| RSHIFT 
							| EQ
							| NE
							| GT 
							| LT 
							| GE
							| LE
	"""
	p[0] = p[1]
# def p_conversion_operator_declarator(p):
# 	"""conversion_operator_declarator : IMPLICIT OPERATOR type LPAREN type IDENTIFIER RPAREN
# 		| EXPLICIT OPERATOR type LPAREN type IDENTIFIER RPAREN
# 	"""
def p_constructor_declaration(p):
	"""constructor_declaration :  modifiers_opt constructor_declarator constructor_body
	"""
	p[0] = create_constructor(p[1], p[2], p[3])
def p_constructor_declarator(p):
	"""constructor_declarator : IDENTIFIER LPAREN formal_parameter_list_opt RPAREN constructor_initializer_opt
	"""
	p[0] = create_constructor_declarator(p[1], p[3], p[5])
def p_constructor_initializer_opt(p):
	"""constructor_initializer_opt : empty 
		| constructor_initializer
	"""
	p[0] = p[1]
def p_constructor_initializer(p):
	"""constructor_initializer : COLON BASE LPAREN argument_list_opt RPAREN
							   | COLON THIS LPAREN argument_list_opt RPAREN
	"""
	p[0] = create_constructor_initializer(p[2], p[4])
def p_destructor_declaration(p):
	"""destructor_declaration :  modifiers_opt NOT IDENTIFIER LPAREN RPAREN block
	"""
	p[0] = create_destructor(p[1], p[3], p[6])
def p_operator_body(p):
	"""operator_body : block
		| STMT_TERMINATOR
	"""
	p[0] = p[1]
def p_constructor_body(p):
	"""constructor_body : block
		| STMT_TERMINATOR
	"""
	p[0] = p[1]
# C.2.7 Structs 
def p_struct_declaration(p):
	"""struct_declaration :  modifiers_opt STRUCT IDENTIFIER struct_body stmt_term_opt
	"""
	p[0] = create_struct(p[1], p[3], p[4])
def p_struct_body(p):
	"""struct_body : LBRACE struct_member_declarations_opt RBRACE
	"""
	p[0] = p[2]
def p_struct_member_declarations_opt(p):
	"""struct_member_declarations_opt : empty 
		| struct_member_declarations
	"""
	p[0] = p[1]
def p_struct_member_declarations(p):
	"""struct_member_declarations : struct_member_declaration
		| struct_member_declarations struct_member_declaration
	"""
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = p[1] + [p[2]]
def p_struct_member_declaration(p):
	"""struct_member_declaration : constant_declaration
		| field_declaration
		| method_declaration
		| operator_declaration
		| constructor_declaration
		| type_declaration
	"""
	p[0] = p[1]
# C.2.8 Arrays 
def p_array_initializer(p):
	"""array_initializer : LBRACE variable_initializer_list_opt RBRACE
						 | LBRACE variable_initializer_list COMMA RBRACE
	"""
	p[0] = p[2]
def p_variable_initializer_list_opt(p):
	"""variable_initializer_list_opt : empty 
		| variable_initializer_list
	"""
	p[0] = p[1]
def p_variable_initializer_list(p):
	"""variable_initializer_list : variable_initializer
		| variable_initializer_list COMMA variable_initializer
	"""
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = p[1] + [p[2]]
# C.2.10 Enums 
def p_enum_declaration(p):
	"""enum_declaration :  modifiers_opt ENUM IDENTIFIER enum_base_opt enum_body stmt_term_opt
	"""
	p[0] = create_enum(p[1], p[3], p[4], p[5])
def p_enum_base_opt(p):
	"""enum_base_opt : empty 
		| enum_base
	"""
	p[0] = p[1]
def p_enum_base(p):
	"""enum_base : COLON integral_type
	"""
	p[0] = p[2]
def p_enum_body(p):
	"""enum_body : LBRACE enum_member_declarations_opt RBRACE
				 | LBRACE enum_member_declarations COMMA RBRACE
	"""
	p[0] = p[2]
def p_enum_member_declarations_opt(p):
	"""enum_member_declarations_opt : empty 
		| enum_member_declarations
	"""
	p[0] = p[1]
def p_enum_member_declarations(p):
	"""enum_member_declarations : enum_member_declaration
		| enum_member_declarations COMMA enum_member_declaration
	"""
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = p[1] + [p[2]]
def p_enum_member_declaration(p):
	"""enum_member_declaration :  IDENTIFIER
		|  IDENTIFIER EQUALS constant_expression
	"""
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = [p[1], p[3]]

# C.2.11 Delegates 
def p_delegate_declaration(p):
	"""delegate_declaration :  modifiers_opt DELEGATE return_type IDENTIFIER LPAREN formal_parameter_list_opt RPAREN STMT_TERMINATOR
	"""
	p[0] = create_delegate(p[1], p[3], p[4], p[6])


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
result = parser.parse(data, debug=2)