#!/usr/bin/python3
# Parser for C# in Python
###################################################################################################

import sys
import ply.yacc as yacc
from lexer import *

###################################################################################################

if len(sys.argv) == 2:
	filename = sys.argv[1]
else:
	print("Usage: ./parser file.cs")
	exit(0)

# Read the input program
inputfile = open(filename, 'r')
data = inputfile.read()
# lexer.input(data)
# Now we can access the tokens in the program as lexer.token()

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


#--------------------------------------------------------------------------------------------------
# Grammar Productions for C#

#defining a rule for empty productions
def p_empty(p):
	'empty :'
	pass

#opt rules goes here
def p_implicit_anonymous_function_parameter_list_opt(p): 
	"""implicit_anonymous_function_parameter_list_opt : empty 
			| implicit_anonymous_function_parameter_list""" 

def p_generic_dimension_specifier_opt(p): 
	"""generic_dimension_specifier_opt : empty 
			| generic_dimension_specifier""" 

def p_method_modifiers_opt(p): 
	"""method_modifiers_opt : empty 
			| method_modifiers""" 

def p_variant_type_parameter_list_opt(p): 
	"""variant_type_parameter_list_opt : empty 
			| variant_type_parameter_list""" 

def p_formal_parameter_list_opt(p): 
	"""formal_parameter_list_opt : empty 
			| formal_parameter_list""" 

def p_get_accessor_declaration_opt(p): 
	"""get_accessor_declaration_opt : empty 
			| get_accessor_declaration""" 

def p_indexer_modifiers_opt(p): 
	"""indexer_modifiers_opt : empty 
			| indexer_modifiers""" 

def p_rank_specifiers_opt(p): 
	"""rank_specifiers_opt : empty 
			| rank_specifiers""" 

def p_smt_terminator_opt(p): 
	"""smt_terminator_opt : empty 
			| STMT_TERMINATOR""" 

def p_enum_member_declarations_opt(p): 
	"""enum_member_declarations_opt : empty 
			| enum_member_declarations""" 

def p_for_initializer_opt(p): 
	"""for_initializer_opt : empty 
			| for_initializer""" 

def p_constant_modifiers_opt(p): 
	"""constant_modifiers_opt : empty 
			| constant_modifiers""" 

def p_set_accessor_declaration_opt(p): 
	"""set_accessor_declaration_opt : empty 
			| set_accessor_declaration""" 

def p_enum_modifiers_opt(p): 
	"""enum_modifiers_opt : empty 
			| enum_modifiers""" 

def p_enum_base_opt(p): 
	"""enum_base_opt : empty 
			| enum_base""" 

def p_default_argument_opt(p): 
	"""default_argument_opt : empty 
			| default_argument""" 

def p_array_initializer_opt(p): 
	"""array_initializer_opt : empty 
			| array_initializer""" 

def p_struct_modifiers_opt(p): 
	"""struct_modifiers_opt : empty 
			| struct_modifiers""" 

def p_accessor_modifier_opt(p): 
	"""accessor_modifier_opt : empty 
			| accessor_modifier""" 

def p_switch_sections_opt(p): 
	"""switch_sections_opt : empty 
			| switch_sections""" 

def p_namespace_member_declarations_opt(p): 
	"""namespace_member_declarations_opt : empty 
			| namespace_member_declarations""" 

def p_explicit_anonymous_function_signature_opt(p): 
	"""explicit_anonymous_function_signature_opt : empty 
			| explicit_anonymous_function_signature""" 

def p_property_modifiers_opt(p): 
	"""property_modifiers_opt : empty 
			| property_modifiers""" 

def p_parameter_modifier_opt(p): 
	"""parameter_modifier_opt : empty 
			| parameter_modifier""" 

def p_field_modifiers_opt(p): 
	"""field_modifiers_opt : empty 
			| field_modifiers""" 

def p_variable_initializer_list_opt(p): 
	"""variable_initializer_list_opt : empty 
			| variable_initializer_list""" 

def p_member_declarator_list_opt(p): 
	"""member_declarator_list_opt : empty 
			| member_declarator_list""" 

def p_partial_opt(p): 
	"""partial_opt : empty 
			| PARTIAL""" 

def p_class_base_opt(p): 
	"""class_base_opt : empty 
			| class_base""" 

def p_explicit_anonymous_function_parameter_list_opt(p): 
	"""explicit_anonymous_function_parameter_list_opt : empty 
			| explicit_anonymous_function_parameter_list""" 

def p_argument_name_opt(p): 
	"""argument_name_opt : empty 
			| argument_name""" 

def p_type_parameter_constraints_clauses_opt(p): 
	"""type_parameter_constraints_clauses_opt : empty 
			| type_parameter_constraints_clauses""" 

def p_statement_list_opt(p): 
	"""statement_list_opt : empty 
			| statement_list""" 

def p_for_condition_opt(p): 
	"""for_condition_opt : empty 
			| for_condition""" 

def p_struct_member_declarations_opt(p): 
	"""struct_member_declarations_opt : empty 
			| struct_member_declarations""" 

def p_class_modifiers_opt(p): 
	"""class_modifiers_opt : empty 
			| class_modifiers""" 

def p_expression_opt(p): 
	"""expression_opt : empty 
			| expression""" 

def p_delegate_modifiers_opt(p): 
	"""delegate_modifiers_opt : empty 
			| delegate_modifiers""" 

def p_for_iterator_opt(p): 
	"""for_iterator_opt : empty 
			| for_iterator""" 

def p_object_or_collection_initializer_opt(p): 
	"""object_or_collection_initializer_opt : empty 
			| object_or_collection_initializer""" 

def p_event_modifiers_opt(p): 
	"""event_modifiers_opt : empty 
			| event_modifiers""" 

def p_dim_separators_opt(p): 
	"""dim_separators_opt : empty 
			| dim_separators""" 

def p_constructor_initializer_opt(p): 
	"""constructor_initializer_opt : empty 
			| constructor_initializer""" 

def p_member_initializer_list_opt(p): 
	"""member_initializer_list_opt : empty 
			| member_initializer_list""" 

def p_using_directives_opt(p): 
	"""using_directives_opt : empty 
			| using_directives""" 

def p_commas_opt(p): 
	"""commas_opt : empty 
			| commas""" 

def p_class_member_declarations_opt(p): 
	"""class_member_declarations_opt : empty 
			| class_member_declarations""" 

def p_constructor_modifiers_opt(p): 
	"""constructor_modifiers_opt : empty 
			| constructor_modifiers""" 

def p_extern_opt(p): 
	"""extern_opt : empty 
			| EXTERN""" 

def p_argument_list_opt(p): 
	"""argument_list_opt : empty 
			| argument_list""" 


###################################################################################################

# Compilation unit marks the beginning of the program
def p_compilation_unit(p):
	"""compilation_unit : using_directives_opt
				| namespace_member_declarations_opt
	"""

# Using directives
def p_using_directives(p):
	"""using_directives : using_directive
				| using_directives using_directive
	"""
def p_using_directive(p):
	"""using_directive : using_namespace_directive
	"""

# Variable Names, may be a simple type variable or namespace member
def p_namespace_or_type_name(p):
	"""namespace_or_type_name : IDENTIFIER
				| namespace_or_type_name MEMBERACCESS IDENTIFIER
	"""

# Data Types
def p_type(p):
	"""type : value_type
				| reference_type
	"""
def p_value_type(p):
	"""value_type : struct_type
	"""
def p_struct_type(p):
	"""struct_type : type_name
				| simple_type
	"""
def p_type_name(p):
	"""type_name : namespace_or_type_name
	"""
def p_simple_type(p):
	"""simple_type : numeric_type
				| BOOL
	"""
def p_numeric_type(p):
	"""numeric_type : integral_type
				| floating_point_type
				| DECIMAL
	"""
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
def p_floating_point_type(p):
	"""floating_point_type : FLOAT
				| DOUBLE
	"""
def p_reference_type(p):
	"""reference_type : class_type
				| array_type
				| delegate_type
	"""
def p_class_type(p):
	"""class_type : type_name
				| OBJECT
				| DYNAMIC
				| STRING
	"""
def p_array_type(p):
	"""array_type : non_array_type rank_specifiers
	"""
def p_non_array_type(p):
	"""non_array_type : type
	"""
def p_rank_specifiers(p):
	"""rank_specifiers : rank_specifier
				| rank_specifiers rank_specifier
	"""
def p_rank_specifier(p):
	"""rank_specifier : LBRACKET dim_separators_opt RBRACKET
	"""

# Separators like ','	
def p_dim_separators(p):
	"""dim_separators : COMMA
				| dim_separators COMMA
	"""

# Delegate Type
def p_delegate_type(p):
	"""delegate_type : type_name
	"""

# Using namespace e.g., using System;
def p_using_namespace_directive(p):
	"""using_namespace_directive : USING namespace_name STMT_TERMINATOR
	"""
# Namespace
def p_namespace_name(p):
	"""namespace_name : namespace_or_type_name
	"""

# Arguments
def p_argument_name(p):
	"""argument_name : IDENTIFIER COLON
	"""

# Expressions 
def p_expression(p):
	"""expression : non_assignment_expression
				| assignment
	"""
def p_non_assignment_expression(p):
	"""non_assignment_expression : conditional_expression
				| lambda_expression
	"""
def p_conditional_expression(p):
	"""conditional_expression : null_coalescing_expression
				| null_coalescing_expression CONDOP expression COLON expression
	"""
def p_null_coalescing_expression(p):
	"""null_coalescing_expression : conditional_or_expression
				| conditional_or_expression "??" null_coalescing_expression
	"""
def p_conditional_or_expression(p):
	"""conditional_or_expression : conditional_and_expression
				| conditional_or_expression COR conditional_and_expression
	"""
def p_conditional_and_expression(p):
	"""conditional_and_expression : inclusive_or_expression
				| conditional_and_expression CAND inclusive_or_expression
	"""
def p_inclusive_or_expression(p):
	"""inclusive_or_expression : exclusive_or_expression
				| inclusive_or_expression OR exclusive_or_expression
	"""
def p_exclusive_or_expression(p):
	"""exclusive_or_expression : and_expression
				| exclusive_or_expression XOR and_expression
	"""
def p_and_expression(p):
	"""and_expression : equality_expression
				| and_expression AND equality_expression
	"""
def p_equality_expression(p):
	"""equality_expression : relational_expression
				| equality_expression EQ relational_expression
				| equality_expression NE relational_expression
	"""
def p_relational_expression(p):
	"""relational_expression : shift_expression
				| relational_expression LT shift_expression
				| relational_expression GT shift_expression
				| relational_expression LE shift_expression
				| relational_expression GE shift_expression
				| relational_expression IS type
				| relational_expression AS type
	"""
def p_shift_expression(p):
	"""shift_expression : additive_expression
				| shift_expression LSHIFT additive_expression
				| shift_expression RSHIFT additive_expression
	"""
def p_additive_expression(p):
	"""additive_expression : multiplicative_expression
				| additive_expression PLUS multiplicative_expression
				| additive_expression MINUS multiplicative_expression
	"""
def p_multiplicative_expression(p):
	"""multiplicative_expression : unary_expression
				| multiplicative_expression TIMES unary_expression
				| multiplicative_expression DIVIDE unary_expression
				| multiplicative_expression MOD unary_expression
	"""
def p_unary_expression(p):
	"""unary_expression : primary_expression
				| PLUS unary_expression
				| MINUS unary_expression
				| LNOT unary_expression
				| NOT unary_expression
				| pre_increment_expression
				| pre_decrement_expression
				| cast_expression
	"""
def p_primary_expression(p):
	"""primary_expression : primary_no_array_creation_expression
				| array_creation_expression
	"""
def p_primary_no_array_creation_expression(p):
	"""primary_no_array_creation_expression : literal
				| simple_name
				| parenthesized_expression
				| member_access
				| invocation_expression
				| element_access
				| this_access
				| base_access
				| post_increment_expression
				| post_decrement_expression
				| object_creation_expression
				| delegate_creation_expression
				| anonymous_object_creation_expression
				| typeof_expression
				| default_value_expression
				| anonymous_method_expression
	"""

# Simple Variables	
def p_simple_name(p):
	"""simple_name : IDENTIFIER
	"""

# Expression in paranthesis
def p_parenthesized_expression(p):
	"""parenthesized_expression : LPAREN expression RPAREN
	"""

# Member of an expression
def p_member_access(p):
	"""member_access : primary_expression MEMBERACCESS IDENTIFIER
				| predefined_type MEMBERACCESS IDENTIFIER
				| qualified_alias_member MEMBERACCESS IDENTIFIER
	"""

# Types
def p_predefined_type(p):
	"""predefined_type : BOOL
				| BYTE
				| CHAR
				| DECIMAL
				| DOUBLE
				| FLOAT
				| INT
				| LONG
				| OBJECT
				| SBYTE
				| SHORT
				| STRING
				| UINT
				| ULONG
				| USHORT
	"""

def p_invocation_expression(p):
	"""invocation_expression : primary_expression LPAREN argument_list_opt RPAREN
	"""

# Arguments related
def p_argument_list(p):
	"""argument_list : argument
				| argument_list COMMA argument
	"""
def p_argument(p):
	"""argument : argument_name_opt argument_value
	"""
def p_argument_value(p):
	"""argument_value : expression
	"""


def p_variable_reference(p):
	"""variable_reference : expression
	"""

def p_element_access(p):
	"""element_access : primary_no_array_creation_expression LBRACKET argument_list RBRACKET
	"""

def p_this_access(p):
	"""this_access : THIS
	"""

def p_base_access(p):
	"""base_access : BASE MEMBERACCESS IDENTIFIER
				| BASE LBRACKET argument_list RBRACKET
	"""

def p_post_increment_expression(p):
	"""post_increment_expression : primary_expression INCREMENT
	"""

def p_post_decrement_expression(p):
	"""post_decrement_expression : primary_expression DECREMENT
	"""

def p_object_creation_expression(p):
	"""object_creation_expression : NEW type LPAREN argument_list_opt RPAREN object_or_collection_initializer_opt
				| NEW type object_or_collection_initializer
	"""

def p_object_or_collection_initializer(p):
	"""object_or_collection_initializer : object_initializer
				| collection_initializer
	"""

def p_object_initializer(p):
	"""object_initializer : LBRACE member_initializer_list_opt RBRACE
				| LBRACE member_initializer_list COMMA RBRACE
	"""

def p_member_initializer_list(p):
	"""member_initializer_list : member_initializer
				| member_initializer_list COMMA member_initializer
	"""

def p_member_initializer(p):
	"""member_initializer : IDENTIFIER EQUALS initializer_value
	"""

def p_initializer_value(p):
	"""initializer_value : expression
				| object_or_collection_initializer
	"""

def p_collection_initializer(p):
	"""collection_initializer : LBRACE element_initializer_list RBRACE
				| LBRACE element_initializer_list COMMA RBRACE
	"""

def p_element_initializer_list(p):
	"""element_initializer_list : element_initializer
				| element_initializer_list COMMA element_initializer
	"""

def p_element_initializer(p):
	"""element_initializer : non_assignment_expression
				| LBRACE expression_list RBRACE
	"""

def p_expression_list(p):
	"""expression_list : expression
				| expression_list COMMA expression
	"""

def p_delegate_creation_expression(p):
	"""delegate_creation_expression : NEW delegate_type LPAREN expression RPAREN
	"""

def p_anonymous_object_creation_expression(p):
	"""anonymous_object_creation_expression : NEW anonymous_object_initializer
	"""

def p_anonymous_object_initializer(p):
	"""anonymous_object_initializer : LBRACE member_declarator_list_opt RBRACE
				| LBRACE member_declarator_list COMMA RBRACE
	"""

def p_member_declarator_list(p):
	"""member_declarator_list : member_declarator
				| member_declarator_list COMMA member_declarator
	"""

def p_member_declarator(p):
	"""member_declarator : simple_name
				| member_access
				| IDENTIFIER EQUALS expression
	"""

def p_typeof_expression(p):
	"""typeof_expression : TYPEOF LPAREN type RPAREN
				| TYPEOF LPAREN unbound_type_name RPAREN
				| TYPEOF LPAREN VOID RPAREN
	"""

def p_unbound_type_name(p):
	"""unbound_type_name : IDENTIFIER generic_dimension_specifier_opt
				| IDENTIFIER "::" IDENTIFIER generic_dimension_specifier_opt
				| unbound_type_name MEMBERACCESS IDENTIFIER generic_dimension_specifier_opt
	"""

def p_generic_dimension_specifier(p):
	"""generic_dimension_specifier : "<" commas_opt ">"
	"""

def p_commas(p):
	"""commas : COMMA
				| commas COMMA
	"""

def p_default_value_expression(p):
	"""default_value_expression : DEFAULT LPAREN type RPAREN
	"""

# Anonymous methods
def p_anonymous_method_expression(p):
	"""anonymous_method_expression : DELEGATE explicit_anonymous_function_signature_opt block
	"""
def p_explicit_anonymous_function_signature(p):
	"""explicit_anonymous_function_signature : LPAREN explicit_anonymous_function_parameter_list_opt RPAREN
	"""
def p_explicit_anonymous_function_parameter_list(p):
	"""explicit_anonymous_function_parameter_list : explicit_anonymous_function_parameter
				| explicit_anonymous_function_parameter_list COMMA explicit_anonymous_function_parameter
	"""
def p_explicit_anonymous_function_parameter(p):
	"""explicit_anonymous_function_parameter : type IDENTIFIER
	"""

# Statements
def p_block(p):
	"""block : LBRACE statement_list_opt RBRACE
	"""
def p_statement_list(p):
	"""statement_list : statement
				| statement_list statement
	"""
def p_statement(p):
	"""statement : declaration_statement
				| embedded_statement
	"""
def p_declaration_statement(p):
	"""declaration_statement : local_variable_declaration STMT_TERMINATOR
				| local_constant_declaration STMT_TERMINATOR
	"""

# Local Variables Related
def p_local_variable_declaration(p):
	"""local_variable_declaration : local_variable_type local_variable_declarators
	"""
def p_local_variable_type(p):
	"""local_variable_type : type
				| VAR
	"""
def p_local_variable_declarators(p):
	"""local_variable_declarators : local_variable_declarator
				| local_variable_declarators COMMA local_variable_declarator
	"""
def p_local_variable_declarator(p):
	"""local_variable_declarator : IDENTIFIER
				| IDENTIFIER EQUALS local_variable_initializer
	"""
def p_local_variable_initializer(p):
	"""local_variable_initializer : expression
				| array_initializer
	"""
def p_array_initializer(p):
	"""array_initializer : LBRACE variable_initializer_list_opt RBRACE
				| LBRACE variable_initializer_list COMMA RBRACE
	"""
def p_variable_initializer_list(p):
	"""variable_initializer_list : variable_initializer
				| variable_initializer_list COMMA variable_initializer
	"""
def p_variable_initializer(p):
	"""variable_initializer : expression
				| array_initializer
	"""

# Loacl Constants Related
def p_local_constant_declaration(p):
	"""local_constant_declaration : CONST type constant_declarators
	"""
def p_constant_declarators(p):
	"""constant_declarators : constant_declarator
				| constant_declarators COMMA constant_declarator
	"""
def p_constant_declarator(p):
	"""constant_declarator : IDENTIFIER EQUALS constant_expression
	"""
def p_constant_expression(p):
	"""constant_expression : expression
	"""

# Embedded Staements
def p_embedded_statement(p):
	"""embedded_statement : block
				| empty_statement
				| expression_statement
				| selection_statement
				| iteration_statement
				| jump_statement
	"""

def p_empty_statement(p):
	"""empty_statement : STMT_TERMINATOR
	"""

def p_expression_statement(p):
	"""expression_statement : statement_expression STMT_TERMINATOR
	"""

def p_statement_expression(p):
	"""statement_expression : invocation_expression
				| object_creation_expression
				| assignment
				| post_increment_expression
				| post_decrement_expression
				| pre_increment_expression
				| pre_decrement_expression
	"""

def p_assignment(p):
	"""assignment : unary_expression assignment_operator expression
	"""

def p_assignment_operator(p):
	"""assignment_operator : EQUALS
				| PLUSEQUAL
				| MINUSEQUAL
				| TIMESEQUAL
				| DIVEQUAL
				| MODEQUAL
				| ANDEQUAL
				| OREQUAL
				| XOREQUAL
				| LAMBDADEC
				| RSHIFTEQUAL
	"""

# Increment Decrement
def p_pre_increment_expression(p):
	"""pre_increment_expression : INCREMENT unary_expression
	"""
def p_pre_decrement_expression(p):
	"""pre_decrement_expression : DECREMENT unary_expression
	"""

def p_selection_statement(p):
	"""selection_statement : if_statement
				| switch_statement
	"""

# Branching Statements
def p_if_statement(p):
	"""if_statement : IF LPAREN boolean_expression RPAREN embedded_statement
				| IF LPAREN boolean_expression RPAREN embedded_statement ELSE embedded_statement
	"""
def p_boolean_expression(p):
	"""boolean_expression : expression
	"""

# Switch Case Related
def p_switch_statement(p):
	"""switch_statement : SWITCH LPAREN expression RPAREN switch_block
	"""
def p_switch_block(p):
	"""switch_block : LBRACE switch_sections_opt RBRACE
	"""
def p_switch_sections(p):
	"""switch_sections : switch_section
				| switch_sections switch_section
	"""
def p_switch_section(p):
	"""switch_section : switch_labels statement_list
	"""
def p_switch_labels(p):
	"""switch_labels : switch_label
				| switch_labels switch_label
	"""
def p_switch_label(p):
	"""switch_label : CASE constant_expression COLON
				| DEFAULT COLON
	"""

# Iteration related
def p_iteration_statement(p):
	"""iteration_statement : while_statement
				| do_statement
				| for_statement
	"""
def p_while_statement(p):
	"""while_statement : WHILE LPAREN boolean_expression RPAREN embedded_statement
	"""
def p_do_statement(p):
	"""do_statement : DO embedded_statement WHILE LPAREN boolean_expression RPAREN STMT_TERMINATOR
	"""
def p_for_statement(p):
	"""for_statement : FOR LPAREN for_initializer_opt STMT_TERMINATOR for_condition_opt STMT_TERMINATOR for_iterator_opt RPAREN embedded_statement
	"""
def p_for_initializer(p):
	"""for_initializer : local_variable_declaration
				| statement_expression_list
	"""

def p_statement_expression_list(p):
	"""statement_expression_list : statement_expression
				| statement_expression_list COMMA statement_expression
	"""

def p_for_condition(p):
	"""for_condition : boolean_expression
	"""

def p_for_iterator(p):
	"""for_iterator : statement_expression_list
	"""

def p_jump_statement(p):
	"""jump_statement : break_statement
				| continue_statement
				| goto_statement
				| return_statement
	"""

def p_break_statement(p):
	"""break_statement : BREAK STMT_TERMINATOR
	"""

def p_continue_statement(p):
	"""continue_statement : CONTINUE STMT_TERMINATOR
	"""

def p_goto_statement(p):
	"""goto_statement : GOTO IDENTIFIER STMT_TERMINATOR
				| GOTO CASE constant_expression STMT_TERMINATOR
				| GOTO DEFAULT STMT_TERMINATOR
	"""

def p_return_statement(p):
	"""return_statement : RETURN expression_opt STMT_TERMINATOR
	"""

def p_array_creation_expression(p):
	"""array_creation_expression : NEW non_array_type LBRACKET expression_list RBRACKET rank_specifiers_opt array_initializer_opt
				| NEW array_type array_initializer
				| NEW rank_specifier array_initializer
	"""

def p_cast_expression(p):
	"""cast_expression : LPAREN type RPAREN unary_expression
	"""

def p_lambda_expression(p):
	"""lambda_expression : anonymous_function_signature LAMBDADEC anonymous_function_body
	"""

def p_anonymous_function_signature(p):
	"""anonymous_function_signature : explicit_anonymous_function_signature
				| implicit_anonymous_function_signature
	"""

def p_implicit_anonymous_function_signature(p):
	"""implicit_anonymous_function_signature : LPAREN implicit_anonymous_function_parameter_list_opt RPAREN
				| implicit_anonymous_function_parameter
	"""

def p_implicit_anonymous_function_parameter_list(p):
	"""implicit_anonymous_function_parameter_list : implicit_anonymous_function_parameter
				| implicit_anonymous_function_parameter_list COMMA implicit_anonymous_function_parameter
	"""

def p_implicit_anonymous_function_parameter(p):
	"""implicit_anonymous_function_parameter : IDENTIFIER
	"""

def p_anonymous_function_body(p):
	"""anonymous_function_body : expression
				| block
	"""

def p_namespace_member_declarations(p):
	"""namespace_member_declarations : namespace_member_declaration
				| namespace_member_declarations namespace_member_declaration
	"""

def p_namespace_member_declaration(p):
	"""namespace_member_declaration : namespace_declaration
				| type_declaration
	"""

def p_namespace_declaration(p):
	"""namespace_declaration : "namespace" qualified_IDENTIFIER namespace_body smt_terminator_opt
	"""

def p_qualified_IDENTIFIER(p):
	"""qualified_IDENTIFIER : IDENTIFIER
				| qualified_IDENTIFIER MEMBERACCESS IDENTIFIER
	"""

def p_namespace_body(p):
	"""namespace_body : LBRACE using_directives_opt namespace_member_declarations_opt RBRACE
	"""

def p_type_declaration(p):
	"""type_declaration : class_declaration
				| struct_declaration
				| enum_declaration
				| delegate_declaration
	"""

def p_class_declaration(p):
	"""class_declaration : class_modifiers_opt partial_opt CLASS IDENTIFIER
				| class_base_opt class_body smt_terminator_opt
	"""

def p_class_modifiers(p):
	"""class_modifiers : class_modifier
				| class_modifiers class_modifier
	"""

def p_class_modifier(p):
	"""class_modifier : NEW
				| PUBLIC
				| PROTECTED
				| INTERNAL
				| PRIVATE
				| ABSTRACT
				| SEALED
				| STATIC
	"""

def p_class_base(p):
	"""class_base:
				| COLON class_type
	"""

def p_class_body(p):
	"""class_body : LBRACE class_member_declarations_opt RBRACE
	"""

def p_class_member_declarations(p):
	"""class_member_declarations : class_member_declaration
				| class_member_declarations class_member_declaration
	"""

def p_class_member_declaration(p):
	"""class_member_declaration : constant_declaration
				| field_declaration
				| method_declaration
				| property_declaration
				| event_declaration
				| indexer_declaration
				| operator_declaration
				| constructor_declaration
				| destructor_declaration
				| static_constructor_declaration
				| type_declaration
	"""

def p_constant_declaration(p):
	"""constant_declaration :  constant_modifiers_opt CONST type constant_declarators STMT_TERMINATOR
	"""

def p_constant_modifiers(p):
	"""constant_modifiers : constant_modifier
				| constant_modifiers constant_modifier
	"""

def p_constant_modifier(p):
	"""constant_modifier : NEW
				| PUBLIC
				| PROTECTED
				| INTERNAL
				| PRIVATE
	"""

def p_field_declaration(p):
	"""field_declaration :  field_modifiers_opt type variable_declarators STMT_TERMINATOR
	"""

def p_field_modifiers(p):
	"""field_modifiers : field_modifier
				| field_modifiers field_modifier
	"""

def p_field_modifier(p):
	"""field_modifier : NEW
				| PUBLIC
				| PROTECTED
				| INTERNAL
				| PRIVATE
				| STATIC
				| READONLY
				| VOLATILE
	"""

def p_variable_declarators(p):
	"""variable_declarators : variable_declarator
				| variable_declarators COMMA variable_declarator
	"""

def p_variable_declarator(p):
	"""variable_declarator : IDENTIFIER
				| IDENTIFIER EQUALS variable_initializer
	"""

def p_method_declaration(p):
	"""method_declaration : method_header method_body
	"""

def p_method_header(p):
	"""method_header :  method_modifiers_opt partial_opt return_type member_name
				| LPAREN formal_parameter_list_opt RPAREN
	"""

def p_method_modifiers(p):
	"""method_modifiers : method_modifier
				| method_modifiers method_modifier
	"""

def p_method_modifier(p):
	"""method_modifier : NEW
				| PUBLIC
				| PROTECTED
				| INTERNAL
				| PRIVATE
				| STATIC
				| VIRTUAL
				| SEALED
				| OVERRIDE
				| ABSTRACT
				| EXTERN
	"""

def p_return_type(p):
	"""return_type : type
				| VOID
	"""

def p_member_name(p):
	"""member_name : IDENTIFIER
	"""

def p_formal_parameter_list(p):
	"""formal_parameter_list : fixed_parameters
				| fixed_parameters COMMA parameter_array
				| parameter_array
	"""

def p_fixed_parameters(p):
	"""fixed_parameters : fixed_parameter
				| fixed_parameters COMMA fixed_parameter
	"""

def p_fixed_parameter(p):
	"""fixed_parameter :  parameter_modifier_opt type IDENTIFIER default_argument_opt
	"""

def p_parameter_modifier(p):
	"""parameter_modifier : THIS
	"""

def p_default_argument(p):

	"""default_argument : EQUALS expression
	"""

def p_parameter_array(p):
	"""parameter_array :  "params" array_type IDENTIFIER
	"""

def p_method_body(p):
	"""method_body : block
				| STMT_TERMINATOR
	"""

def p_property_declaration(p):
	"""property_declaration :  property_modifiers_opt type member_name LBRACE accessor_declarations RBRACE
	"""

def p_property_modifiers(p):
	"""property_modifiers : property_modifier
				| property_modifiers property_modifier
	"""

def p_property_modifier(p):
	"""property_modifier : NEW
				| PUBLIC
				| PROTECTED
				| INTERNAL
				| PRIVATE
				| STATIC
				| VIRTUAL
				| SEALED
				| OVERRIDE
				| ABSTRACT
				| EXTERN
	"""

def p_accessor_declarations(p):
	"""accessor_declarations : get_accessor_declaration set_accessor_declaration_opt
				| set_accessor_declaration get_accessor_declaration_opt
	"""

def p_get_accessor_declaration(p):
	"""get_accessor_declaration :  accessor_modifier_opt "get" accessor_body
	"""

def p_accessor_modifier(p):
	"""accessor_modifier : PROTECTED
				| INTERNAL
				| PRIVATE
				| PROTECTED INTERNAL
				| INTERNAL PROTECTED
	"""

def p_accessor_body(p):
	"""accessor_body : block
				| STMT_TERMINATOR
	"""

def p_set_accessor_declaration(p):
	"""set_accessor_declaration :  accessor_modifier_opt "set" accessor_body
	"""

def p_event_declaration(p):
	"""event_declaration :  event_modifiers_opt "event" type variable_declarators STMT_TERMINATOR
				|  event_modifiers_opt "event" type member_name LBRACE event_accessor_declarations RBRACE
	"""

def p_event_modifiers(p):
	"""event_modifiers : event_modifier
				| event_modifiers event_modifier
	"""

def p_event_modifier(p):
	"""event_modifier : NEW
				| PUBLIC
				| PROTECTED
				| INTERNAL
				| PRIVATE
				| STATIC
				| VIRTUAL
				| SEALED
				| OVERRIDE
				| ABSTRACT
				| EXTERN
	"""

def p_event_accessor_declarations(p):
	"""event_accessor_declarations : add_accessor_declaration remove_accessor_declaration
				| remove_accessor_declaration add_accessor_declaration
	"""

def p_add_accessor_declaration(p):
	"""add_accessor_declaration :  ADD block
	"""

def p_remove_accessor_declaration(p):
	"""remove_accessor_declaration :  REMOVE block
	"""

def p_indexer_declaration(p):
	"""indexer_declaration :  indexer_modifiers_opt indexer_declarator LBRACE accessor_declarations RBRACE
	"""

def p_indexer_modifiers(p):
	"""indexer_modifiers : indexer_modifier
				| indexer_modifiers indexer_modifier
	"""

def p_indexer_modifier(p):
	"""indexer_modifier : NEW
				| PUBLIC
				| PROTECTED
				| INTERNAL
				| PRIVATE
				| VIRTUAL
				| SEALED
				| OVERRIDE
				| ABSTRACT
				| EXTERN
	"""

def p_indexer_declarator(p):
	"""indexer_declarator : type THIS LBRACKET formal_parameter_list RBRACKET
	"""

def p_operator_declaration(p):
	"""operator_declaration :  operator_modifiers operator_declarator operator_body
	"""

def p_operator_modifiers(p):
	"""operator_modifiers : operator_modifier
				| operator_modifiers operator_modifier
	"""

def p_operator_modifier(p):
	"""operator_modifier : PUBLIC
				| STATIC
				| EXTERN
	"""

def p_operator_declarator(p):
	"""operator_declarator : unary_operator_declarator
				| binary_operator_declarator
				| conversion_operator_declarator
	"""

def p_unary_operator_declarator(p):
	"""unary_operator_declarator : type OPERATOR overloadable_unary_operator LPAREN type IDENTIFIER RPAREN
	"""

def p_overloadable_unary_operator(p):
	"""overloadable_unary_operator : PLUS
				| MINUS
				| LNOT
				| NOT
				| INCREMENT
				| DECREMENT
				| TRUE
				| FALSE
	"""

def p_binary_operator_declarator(p):
	"""binary_operator_declarator : type OPERATOR overloadable_binary_operator LPAREN type IDENTIFIER COMMA type IDENTIFIER RPAREN
	"""

def p_overloadable_binary_operator(p):
	"""overloadable_binary_operator : PLUS
				| MINUS
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

def p_conversion_operator_declarator(p):
	"""conversion_operator_declarator : "implicit" OPERATOR type LPAREN type IDENTIFIER RPAREN
				| "explicit" OPERATOR type LPAREN type IDENTIFIER RPAREN
	"""

def p_operator_body(p):
	"""operator_body : block
				| STMT_TERMINATOR
	"""

def p_constructor_declaration(p):
	"""constructor_declaration :  constructor_modifiers_opt constructor_declarator constructor_body
	"""

def p_constructor_modifiers(p):
	"""constructor_modifiers : constructor_modifier
				| constructor_modifiers constructor_modifier
	"""

def p_constructor_modifier(p):
	"""constructor_modifier : PUBLIC
				| PROTECTED
				| INTERNAL
				| PRIVATE
				| EXTERN
	"""

def p_constructor_declarator(p):
	"""constructor_declarator : IDENTIFIER LPAREN formal_parameter_list_opt RPAREN constructor_initializer_opt
	"""

def p_constructor_initializer(p):
	"""constructor_initializer: COLON BASE LPAREN argument_list_opt RPAREN
				| COLON THIS LPAREN argument_list_opt RPAREN
	"""


def p_constructor_body(p):
	"""constructor_body : block
				| STMT_TERMINATOR
	"""

def p_destructor_declaration(p):
	"""destructor_declaration :  extern_opt NOT IDENTIFIER LPAREN RPAREN destructor_body
	"""

def p_destructor_body(p):
	"""destructor_body : block
				| STMT_TERMINATOR
	"""

def p_static_constructor_declaration(p):
	"""static_constructor_declaration :  static_constructor_modifiers IDENTIFIER LPAREN RPAREN static_constructor_body
	"""

def p_static_constructor_modifiers(p):
	"""static_constructor_modifiers : extern_opt STATIC
				| STATIC extern_opt
	"""

def p_static_constructor_body(p):
	"""static_constructor_body : block
				| STMT_TERMINATOR
	"""

def p_struct_declaration(p):
	"""struct_declaration :  struct_modifiers_opt partial_opt STRUCT IDENTIFIER
				| struct_body smt_terminator_opt
	"""

def p_struct_modifiers(p):
	"""struct_modifiers : struct_modifier
				| struct_modifiers struct_modifier
	"""

def p_struct_modifier(p):
	"""struct_modifier : NEW
				| PUBLIC
				| PROTECTED
				| INTERNAL
				| PRIVATE
	"""


def p_struct_body(p):
	"""struct_body : LBRACE struct_member_declarations_opt RBRACE
	"""

def p_struct_member_declarations(p):
	"""struct_member_declarations : struct_member_declaration
				| struct_member_declarations struct_member_declaration
	"""

def p_struct_member_declaration(p):
	"""struct_member_declaration : constant_declaration
				| field_declaration
				| method_declaration
				| property_declaration
				| event_declaration
				| indexer_declaration
				| operator_declaration
				| constructor_declaration
				| static_constructor_declaration
				| type_declaration
	"""

def p_enum_declaration(p):
	"""enum_declaration :  enum_modifiers_opt "enum" IDENTIFIER enum_base_opt enum_body smt_terminator_opt
	"""

def p_enum_modifiers(p):
	"""enum_modifiers : enum_modifier
				| enum_modifiers enum_modifier
	"""

def p_enum_modifier(p):
	"""enum_modifier : NEW
				| PUBLIC
				| PROTECTED
				| INTERNAL
				| PRIVATE
	"""


def p_enum_base(p):
	"""enum_base : COLON integral_type
	"""


def p_enum_body(p):
	"""enum_body : LBRACE enum_member_declarations_opt RBRACE
				| LBRACE enum_member_declarations COMMA RBRACE
	"""

def p_enum_member_declarations(p):
	"""enum_member_declarations : enum_member_declaration
				| enum_member_declarations COMMA enum_member_declaration
	"""

def p_enum_member_declaration(p):
	"""enum_member_declaration :  IDENTIFIER
				|  IDENTIFIER EQUALS constant_expression
	"""

def p_delegate_declaration(p):
	"""delegate_declaration :  delegate_modifiers_opt DELEGATE return_type
				| IDENTIFIER variant_type_parameter_list_opt
				| LPAREN formal_parameter_list_opt RPAREN type_parameter_constraints_clauses_opt STMT_TERMINATOR
	"""

def p_delegate_modifiers(p):
	"""delegate_modifiers : delegate_modifier
				| delegate_modifiers delegate_modifier
	"""

def p_delegate_modifier(p):
	"""delegate_modifier : NEW
				| PUBLIC
				| PROTECTED
				| INTERNAL
				| PRIVATE
	"""
