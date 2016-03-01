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

#--------------------------------------------------------------------------------------------------

opt_rules = [
	'class_member_declarations',
	'struct_member_declarations',
	'verbatim_string_literal_characters',
	'interface_base',
	'new',
	'expression',
	'IDENTIFIER_part_characters',
	'integer_type_suffix',
	'enum_modifiers',
	'interface_member_declarations',
	'statement_list',
	'argument_list',
	'dim_separators',
	'array_initializer',
	'hex_digit',
	'constant_modifiers',
	'pp_else_section',
	'formal_parameter_list',
	'variable_initializer_list',
	'exponent_part',
	'delegate_modifiers',
	'regular_string_literal_characters',
	'IDENTIFIER',
	'parameter_modifier',
	'enum_base',
	'namespace_member_declarations',
	'method_modifiers',
	'conditional_section',
	'constructor_initializer',
	'skipped_characters',
	'struct_modifiers',
	'constructor_modifiers',
	'positional_argument_list',
	'switch_sections',
	'pp_elif_sections',
	'for_condition',
	'using_directives',
	'rank_specifiers',
	'interface_modifiers',
	'unsafe',
	'input_characters',
	'class_base',
	'indexer_modifiers',
	'enum_member_declarations',
	'property_modifiers',
	'class_modifiers',
	'set_accessor_declaration',
	'input_section',
	'extern',
	'field_modifiers',
	'whitespace',
	'get_accessor_declaration',
	'real_type_suffix',
	';',
	'struct_interfaces',
	'sign',
	'single_line_comment',
	'event_modifiers',
	'for_iterator',
	'for_initializer',
	'delimited_comment_characters',
	'input_elements'
]

for rule in opt_rules:
	create_opt_rule(rule)

#--------------------------------------------------------------------------------------------------
# Grammar Productions for C#


def p_compilation_unit(p):
	"""compilation_unit : using_directives_opt global_
				| namespace_member_declarations_opt
	"""

# def p_extern_alias_directives(p):
# 	"""extern_alias_directives : extern_alias_directive
# 				| extern_alias_directives extern_alias_directive
# 	"""


# def p_extern_alias_directive(p):
# 	"""extern_alias_directive : EXTERN "alias" IDENTIFIER STMT_TERMINATOR
# 	"""


def p_using_directives(p):
	"""using_directives : using_directive
				| using_directives using_directive
	"""


def p_using_directive(p):
	"""using_directive : using_alias_directive
				| using_namespace_directive
	"""


def p_using_alias_directive(p):
	"""using_alias_directive : USING IDENTIFIER EQUALS namespace_or_type_name STMT_TERMINATOR
	"""


def p_namespace_or_type_name(p):
	"""namespace_or_type_name : IDENTIFIER type_argument_list_opt
				| namespace_or_type_name MEMBERACCESS IDENTIFIER type_argument_list_opt
				| qualified_alias_member
	"""


def p_type_argument_list(p):
	"""type_argument_list : "<" type_arguments ">"
	"""


def p_type_arguments(p):
	"""type_arguments : type_argument
				| type_arguments COMMA type_argument
	"""


def p_type_argument(p):
	"""type_argument : type
	"""


def p_type(p):
	"""type : value_type
				| reference_type
				| type_parameter
	"""


def p_value_type(p):
	"""value_type : struct_type
				| enum_type
	"""


def p_struct_type(p):
	"""struct_type : type_name
				| simple_type
				| nullable_type
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


def p_nullable_type(p):
	"""nullable_type : non_nullable_value_type CONDOP
	"""


def p_non_nullable_value_type(p):
	"""non_nullable_value_type : type
	"""


def p_enum_type(p):
	"""enum_type : type_name
	"""


def p_reference_type(p):
	"""reference_type : class_type
				| interface_type
				| array_type
				| delegate_type
	"""


def p_class_type(p):
	"""class_type : type_name
				| OBJECT
				| DYNAMIC
				| STRING
	"""


def p_interface_type(p):
	"""interface_type : type_name
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


def p_dim_separators(p):
	"""dim_separators : COMMA
				| dim_separators COMMA
	"""


def p_delegate_type(p):
	"""delegate_type : type_name
	"""


def p_type_parameter(p):
	"""type_parameter : IDENTIFIER
	"""


def p_qualified_alias_member(p):
	"""qualified_alias_member : IDENTIFIER "::" IDENTIFIER type_argument_list_opt
	"""


def p_using_namespace_directive(p):
	"""using_namespace_directive : USING namespace_name STMT_TERMINATOR
	"""


def p_namespace_name(p):
	"""namespace_name : namespace_or_type_name
	"""


# def p_global_attributes(p):
# 	"""global_attributes : global_attribute_sections
# 	"""

# def p_global_attribute_sections(p):
# 	"""global_attribute_sections : global_attribute_section
# 				| global_attribute_sections global_attribute_section
# 	"""

# def p_global_attribute_section(p):
# 	"""global_attribute_section : LBRACKET global_attribute_target_specifier attribute_list RBRACKET
# 				| LBRACKET global_attribute_target_specifier attribute_list COMMA RBRACKET
# 	"""

# def p_global_attribute_target_specifier(p):
# 	"""global_attribute_target_specifier : global_attribute_target COLON
# 	"""


# def p_global_attribute_target(p):
# 	"""global_attribute_target : "assembly"
# 				| "module"
# 	"""

# def p_attribute_list(p):
# 	"""attribute_list : attribute
# 				| attribute_list COMMA attribute
# 	"""

# def p_attribute(p):
# 	"""attribute : attribute_name attribute_arguments_opt
# 	"""

# def p_attribute_name(p):
# 	"""attribute_name : type_name
# 	"""

# def p_attribute_arguments(p):
# 	"""attribute_arguments : LPAREN positional_argument_list_opt RPAREN
# 				| LPAREN positional_argument_list COMMA named_argument_list RPAREN
# 				| LPAREN named_argument_list RPAREN
# 	"""

# def p_positional_argument_list(p):
# 	"""positional_argument_list : positional_argument
# 				| positional_argument_list COMMA positional_argument
# 	"""

# def p_positional_argument(p):
# 	"""positional_argument : argument_name_opt attribute_argument_expression
# 	"""


def p_argument_name(p):
	"""argument_name : IDENTIFIER COLON
	"""


# def p_attribute_argument_expression(p):
# 	"""attribute_argument_expression : expression
# 	"""

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

def p_simple_name(p):
	"""simple_name : IDENTIFIER type_argument_list_opt
	"""

def p_parenthesized_expression(p):
	"""parenthesized_expression : LPAREN expression RPAREN
	"""

def p_member_access(p):
	"""member_access : primary_expression MEMBERACCESS IDENTIFIER type_argument_list_opt

				| predefined_type MEMBERACCESS IDENTIFIER type_argument_list_opt
				| qualified_alias_member MEMBERACCESS IDENTIFIER
	"""

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

def p_argument_list(p):
	"""argument_list : argument
				| argument_list COMMA argument
	"""

def p_argument(p):
	"""argument : argument_name_opt argument_value
	"""

def p_argument_value(p):
	"""argument_value : expression
				| REF variable_reference
				| OUT variable_reference
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

# def p_checked_expression(p):
# 	"""checked_expression : "checked" LPAREN expression RPAREN
# 	"""

# def p_unchecked_expression(p):
# 	"""unchecked_expression : "unchecked" LPAREN expression RPAREN
# 	"""

def p_default_value_expression(p):
	"""default_value_expression : DEFAULT LPAREN type RPAREN
	"""

def p_anonymous_method_expression(p):
	"""anonymous_method_expression : DELEGATE" explicit_anonymous_function_signature_opt block
	"""

def p_explicit_anonymous_function_signature(p):
	"""explicit_anonymous_function_signature : LPAREN explicit_anonymous_function_parameter_list_opt RPAREN
	"""

def p_explicit_anonymous_function_parameter_list(p):
	"""explicit_anonymous_function_parameter_list : explicit_anonymous_function_parameter
				| explicit_anonymous_function_parameter_list COMMA explicit_anonymous_function_parameter
	"""

def p_explicit_anonymous_function_parameter(p):
	"""explicit_anonymous_function_parameter : anonymous_function_parameter_modifier_opt type IDENTIFIER
	"""

def p_anonymous_function_parameter_modifier(p):
	"""anonymous_function_parameter_modifier : REF
				| OUT
	"""

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

# def p_labeled_statement(p):
# 	"""labeled_statement: IDENTIFIER COLON statement
# 	"""

def p_declaration_statement(p):
	"""declaration_statement : local_variable_declaration STMT_TERMINATOR
				| local_constant_declaration STMT_TERMINATOR
	"""

def p_local_variable_declaration(p):
	"""local_variable_declaration : local_variable_type local_variable_declarators
	"""

def p_local_variable_type(p):
	"""local_variable_type : type
				| "var"
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

# def p_right_shift_assignment(p):
# 	"""right_shift_assignment : RSHIFTEQUAL
# 	"""

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

def p_if_statement(p):
	"""if_statement : IF LPAREN boolean_expression RPAREN embedded_statement
				| IF LPAREN boolean_expression RPAREN embedded_statement ELSE embedded_statement
	"""

def p_boolean_expression(p):
	"""boolean_expression : expression
	"""

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

# def p_foreach_statement(p):
# 	"""foreach_statement : "foreach" LPAREN local_variable_type IDENTIFIER IN expression RPAREN embedded_statement
# 	"""

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

# def p_throw_statement(p):
# 	"""throw_statement : "throw" expression_opt STMT_TERMINATOR
# 	"""

# def p_try_statement(p):
# 	"""try_statement : "try" block catch_clauses
# 				| "try" block finally_clause
# 				| "try" block catch_clauses finally_clause
# 	"""

# def p_catch_clauses(p):
# 	"""catch_clauses : specific_catch_clauses general_catch_clause_opt
# 				| specific_catch_clauses_opt general_catch_clause
# 	"""

# def p_specific_catch_clauses(p):
# 	"""specific_catch_clauses : specific_catch_clause
# 				| specific_catch_clauses specific_catch_clause
# 	"""

# def p_specific_catch_clause(p):
# 	"""specific_catch_clause : "catch" LPAREN class_type IDENTIFIER_opt RPAREN block
# 	"""

# def p_general_catch_clause(p):
# 	"""general_catch_clause : "catch" block
# 	"""

# def p_finally_clause(p):
# 	"""finally_clause : "finally" block
# 	"""

# def p_checked_statement(p):
# 	"""checked_statement : "checked" block
# 	"""

# def p_unchecked_statement(p):
# 	"""unchecked_statement : "unchecked" block
# 	"""

# def p_lock_statement(p):
# 	"""lock_statement : "lock" LPAREN expression RPAREN embedded_statement
# 	"""

# def p_using_statement(p):
# 	"""using_statement : USING LPAREN resource_acquisition RPAREN embedded_statement
# 	"""

# def p_resource_acquisition(p):
# 	"""resource_acquisition : local_variable_declaration
# 				| expression
# 	"""

# def p_yield_statement(p):
# 	"""yield_statement : "yield" RETURN expression STMT_TERMINATOR
# 				| "yield" BREAK STMT_TERMINATOR
# 	"""

def p_array_creation_expression(p):
	"""array_creation_expression : NEW non_array_type LBRACKET expression_list RBRACKET rank_specifiers_opt array_initializer_opt
				| NEW array_type array_initializer
				| NEW rank_specifier array_initializer
	"""

def p_cast_expression(p):
	"""cast_expression : LPAREN type RPAREN unary_expression
	"""

# def p_right_shift(p):
# 	"""right_shift : RSHIFT
# 	"""

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

# def p_query_expression(p):
# 	"""query_expression : from_clause query_body
# 	"""

# def p_from_clause(p):
# 	"""from_clause : "from" type_opt IDENTIFIER IN expression
# 	"""

# def p_query_body(p):
# 	"""query_body : query_body_clauses_opt select_or_group_clause query_continuation_opt
# 	"""

# def p_query_body_clauses(p):
# 	"""query_body_clauses : query_body_clause
# 				| query_body_clauses query_body_clause
# 	"""

# def p_query_body_clause(p):
# 	"""query_body_clause : from_clause
# 				| let_clause
# 				| where_clause
# 				| join_clause
# 				| join_into_clause
# 				| orderby_clause
# 	"""

# def p_let_clause(p):
# 	"""let_clause : "let" IDENTIFIER EQUALS expression
# 	"""

# def p_where_clause(p):
# 	"""where_clause : "where" boolean_expression
# 	"""

# def p_join_clause(p):
# 	"""join_clause : "join" type_opt IDENTIFIER IN expression "on" expression "equals" expression
# 	"""

# def p_join_into_clause(p):
# 	"""join_into_clause : "join" type_opt IDENTIFIER IN expression "on" expression "equals" expression "into" IDENTIFIER
# 	"""

# def p_orderby_clause(p):
# 	"""orderby_clause : "orderby" orderings
# 	"""

# def p_orderings(p):
# 	"""orderings : ordering
# 				| orderings COMMA ordering
# 	"""

# def p_ordering(p):
# 	"""ordering : expression ordering_direction_opt
# 	"""

# def p_ordering_direction(p):
# 	"""ordering_direction : "ascending"
# 				| "descending"
# 	"""

# def p_select_or_group_clause(p):
# 	"""select_or_group_clause : select_clause
# 				| group_clause
# 	"""

# def p_select_clause(p):
# 	"""select_clause : "select" expression
# 	"""

# def p_group_clause(p):
# 	"""group_clause : "group" expression "by" expression
# 	"""

# def p_query_continuation(p):
# 	"""query_continuation : "into" IDENTIFIER query_body
# 	"""

# def p_named_argument_list(p):
# 	"""named_argument_list : named_argument
# 				| named_argument_list COMMA named_argument
# 	"""

# def p_named_argument(p):
# 	"""named_argument : IDENTIFIER EQUALS attribute_argument_expression
# 	"""

def p_namespace_member_declarations(p):
	"""namespace_member_declarations : namespace_member_declaration
				| namespace_member_declarations namespace_member_declaration
	"""

def p_namespace_member_declaration(p):
	"""namespace_member_declaration : namespace_declaration
				| type_declaration
	"""

def p_namespace_declaration(p):
	"""namespace_declaration : "namespace" qualified_IDENTIFIER namespace_body STMT_TERMINATOR_opt
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
				| interface_declaration
				| enum_declaration
				| delegate_declaration
	"""

def p_class_declaration(p):
	"""class_declaration : class_modifiers_opt "partial"_opt CLASS IDENTIFIER type_parameter_list_opt
				| class_base_opt type_parameter_constraints_clauses_opt class_body STMT_TERMINATOR_opt
	"""

# def p_attributes(p):
# 	"""attributes : attribute_sections
# 	"""

# def p_attribute_sections(p):
# 	"""attribute_sections : attribute_section
# 				| attribute_sections attribute_section
# 	"""

# def p_attribute_section(p):
# 	"""attribute_section : LBRACKET attribute_target_specifier_opt attribute_list RBRACKET
# 				| LBRACKET attribute_target_specifier_opt attribute_list COMMA RBRACKET
# 	"""

# def p_attribute_target_specifier(p):
# 	"""attribute_target_specifier:
# 				| attribute_target COLON
# 	"""


# def p_attribute_target(p):
# 	"""attribute_target : "field"
# 				| "event"
# 				| "method"
# 				| "param"
# 				| "property"
# 				| RETURN
# 				| type
# 	"""

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

def p_type_parameter_list(p):
	"""type_parameter_list : "<" type_parameters ">"
	"""

def p_type_parameters(p):
	"""type_parameters :  type_parameter
				| type_parameters COMMA  type_parameter
	"""

def p_class_base(p):
	"""class_base:
				| COLON class_type
				| COLON interface_type_list
				| COLON class_type COMMA interface_type_list
	"""


def p_interface_type_list(p):
	"""interface_type_list : interface_type
				| interface_type_list COMMA interface_type
	"""

def p_type_parameter_constraints_clauses(p):
	"""type_parameter_constraints_clauses : type_parameter_constraints_clause
				| type_parameter_constraints_clauses type_parameter_constraints_clause
	"""

def p_type_parameter_constraints_clause(p):
	"""type_parameter_constraints_clause: "where" type_parameter COLON type_parameter_constraints
	"""


def p_type_parameter_constraints(p):
	"""type_parameter_constraints : primary_constraint
				| secondary_constraints
				| constructor_constraint
				| primary_constraint COMMA secondary_constraints
				| primary_constraint COMMA constructor_constraint
				| secondary_constraints COMMA constructor_constraint
				| primary_constraint COMMA secondary_constraints COMMA constructor_constraint
	"""

def p_primary_constraint(p):
	"""primary_constraint : class_type
				| CLASS
				| STRUCT
	"""

def p_secondary_constraints(p):
	"""secondary_constraints : interface_type
				| type_parameter
				| secondary_constraints COMMA interface_type
				| secondary_constraints COMMA type_parameter
	"""

def p_constructor_constraint(p):
	"""constructor_constraint : NEW LPAREN RPAREN
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
	"""method_header :  method_modifiers_opt "partial"_opt return_type member_name type_parameter_list_opt
				| LPAREN formal_parameter_list_opt RPAREN type_parameter_constraints_clauses_opt
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
				| interface_type MEMBERACCESS IDENTIFIER
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
	"""parameter_modifier : REF
				| OUT
				| THIS
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
				| type interface_type MEMBERACCESS THIS LBRACKET formal_parameter_list RBRACKET
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
	"""destructor_declaration :  EXTERN_opt NOT IDENTIFIER LPAREN RPAREN destructor_body
	"""

def p_destructor_body(p):
	"""destructor_body : block
				| STMT_TERMINATOR
	"""

def p_static_constructor_declaration(p):
	"""static_constructor_declaration :  static_constructor_modifiers IDENTIFIER LPAREN RPAREN static_constructor_body
	"""

def p_static_constructor_modifiers(p):
	"""static_constructor_modifiers : EXTERN_opt STATIC
				| STATIC EXTERN_opt
	"""

def p_static_constructor_body(p):
	"""static_constructor_body : block
				| STMT_TERMINATOR
	"""

def p_struct_declaration(p):
	"""struct_declaration :  struct_modifiers_opt "partial"_opt STRUCT IDENTIFIER type_parameter_list_opt
				| struct_interfaces_opt type_parameter_constraints_clauses_opt struct_body STMT_TERMINATOR_opt
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

def p_struct_interfaces(p):
	"""struct_interfaces: COLON interface_type_list
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

def p_interface_declaration(p):
	"""interface_declaration :  interface_modifiers_opt "partial"_opt "interface"
				| IDENTIFIER variant_type_parameter_list_opt interface_base_opt
				| type_parameter_constraints_clauses_opt interface_body STMT_TERMINATOR_opt
	"""

def p_interface_modifiers(p):
	"""interface_modifiers : interface_modifier
				| interface_modifiers interface_modifier
	"""

def p_interface_modifier(p):
	"""interface_modifier : NEW
				| PUBLIC
				| PROTECTED
				| INTERNAL
				| PRIVATE
	"""

def p_variant_type_parameter_list(p):
	"""variant_type_parameter_list : "<" variant_type_parameters ">"
	"""

def p_variant_type_parameters(p):
	"""variant_type_parameters :  variance_annotation_opt type_parameter
				| variant_type_parameters COMMA  variance_annotation_opt type_parameter
	"""

def p_variance_annotation(p):
	"""variance_annotation : IN
				| OUT
	"""

def p_interface_base(p):
	"""interface_base : COLON interface_type_list
	"""


def p_interface_body(p):
	"""interface_body : LBRACE interface_member_declarations_opt RBRACE
	"""

def p_interface_member_declarations(p):
	"""interface_member_declarations : interface_member_declaration
				| interface_member_declarations interface_member_declaration
	"""

def p_interface_member_declaration(p):
	"""interface_member_declaration : interface_method_declaration
				| interface_property_declaration
				| interface_event_declaration
				| interface_indexer_declaration
	"""

def p_interface_method_declaration(p):
	"""interface_method_declaration :  NEW_opt return_type IDENTIFIER type_parameter_list
				| LPAREN formal_parameter_list_opt RPAREN type_parameter_constraints_clauses_opt STMT_TERMINATOR
	"""

def p_interface_property_declaration(p):
	"""interface_property_declaration :  NEW_opt type IDENTIFIER LBRACE interface_accessors RBRACE
	"""

def p_interface_accessors(p):
	"""interface_accessors :  "get" STMT_TERMINATOR
				|  "set" STMT_TERMINATOR
				|  "get" STMT_TERMINATOR  "set" STMT_TERMINATOR
				|  "set" STMT_TERMINATOR  "get" STMT_TERMINATOR
	"""

def p_interface_event_declaration(p):
	"""interface_event_declaration :  NEW_opt "event" type IDENTIFIER STMT_TERMINATOR
	"""

def p_interface_indexer_declaration(p):
	"""interface_indexer_declaration :  NEW_opt type THIS LBRACKET formal_parameter_list RBRACKET LBRACE interface_accessors RBRACE
	"""

def p_enum_declaration(p):
	"""enum_declaration :  enum_modifiers_opt "enum" IDENTIFIER enum_base_opt enum_body STMT_TERMINATOR_opt
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