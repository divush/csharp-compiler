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
	'identifier_part_characters',
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
	'attribute_target_specifier',
	'regular_string_literal_characters',
	'general_catch_clause',
	'identifier',
	'parameter_modifier',
	'enum_base',
	'namespace_member_declarations',
	'method_modifiers',
	'conditional_section',
	'specific_catch_clauses',
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
	'attribute_arguments',
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
	'global_attributes',
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
	"""compilation_unit : extern_alias_directives_opt using_directives_opt global_attributes_opt
				| namespace_member_declarations_opt
	"""
def p_extern_alias_directives(p):
	"""extern_alias_directives : extern_alias_directive
				| extern_alias_directives extern_alias_directive
	"""
def p_extern_alias_directive(p):
	"""extern_alias_directive : "extern" "alias" identifier ";"
	"""
def p_using_directives(p):
	"""using_directives : using_directive
				| using_directives using_directive
	"""
def p_using_directive(p):
	"""using_directive : using_alias_directive
				| using_namespace_directive
	"""
def p_using_alias_directive(p):
	"""using_alias_directive : "using" identifier "=" namespace_or_type_name ";"
	"""
def p_namespace_or_type_name(p):
	"""namespace_or_type_name : identifier type_argument_list_opt
				| namespace_or_type_name "." identifier type_argument_list_opt
				| qualified_alias_member
	"""
def p_type_argument_list(p):
	"""type_argument_list : "<" type_arguments ">"
	"""
def p_type_arguments(p):
	"""type_arguments : type_argument
				| type_arguments "," type_argument
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
				| "bool"
	"""
def p_numeric_type(p):
	"""numeric_type : integral_type
				| floating_point_type
				| "decimal"
	"""
def p_integral_type(p):
	"""integral_type : "sbyte"
				| "byte"
				| "short"
				| "ushort"
				| "int"
				| "uint"
				| "long"
				| "ulong"
				| "char"
	"""
def p_floating_point_type(p):
	"""floating_point_type : "float"
				| "double"
	"""
def p_nullable_type(p):
	"""nullable_type : non_nullable_value_type "?"
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
				| "object"
				| "dynamic"
				| "string"
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
	"""rank_specifier : "[" dim_separators_opt "]"
	"""
def p_dim_separators(p):
	"""dim_separators : ","
				| dim_separators ","
	"""
def p_delegate_type(p):
	"""delegate_type : type_name
	"""
def p_type_parameter(p):
	"""type_parameter : identifier
	"""
def p_qualified_alias_member(p):
	"""qualified_alias_member : identifier "::" identifier type_argument_list_opt
	"""
def p_using_namespace_directive(p):
	"""using_namespace_directive : "using" namespace_name ";"
	"""
def p_namespace_name(p):
	"""namespace_name : namespace_or_type_name
	"""
def p_global_attributes(p):
	"""global_attributes : global_attribute_sections
	"""
def p_global_attribute_sections(p):
	"""global_attribute_sections : global_attribute_section
				| global_attribute_sections global_attribute_section
	"""
def p_global_attribute_section(p):
	"""global_attribute_section : "[" global_attribute_target_specifier attribute_list "]"
				| "[" global_attribute_target_specifier attribute_list "," "]"
	"""
def p_global_attribute_target_specifier(p):
	"""global_attribute_target_specifier : global_attribute_target ":"
	"""

def p_global_attribute_target(p):
	"""global_attribute_target : "assembly"
				| "module"
	"""
def p_attribute_list(p):
	"""attribute_list : attribute
				| attribute_list "," attribute
	"""
def p_attribute(p):
	"""attribute : attribute_name attribute_arguments_opt
	"""
def p_attribute_name(p):
	"""attribute_name : type_name
	"""
def p_attribute_arguments(p):
	"""attribute_arguments : "(" positional_argument_list_opt ")"
				| "(" positional_argument_list "," named_argument_list ")"
				| "(" named_argument_list ")"
	"""
def p_positional_argument_list(p):
	"""positional_argument_list : positional_argument
				| positional_argument_list "," positional_argument
	"""
def p_positional_argument(p):
	"""positional_argument : argument_name_opt attribute_argument_expression
	"""

def p_argument_name(p):
	"""argument_name : identifier ":"
	"""

def p_attribute_argument_expression(p):
	"""attribute_argument_expression : expression
	"""
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
				| null_coalescing_expression "?" expression ":" expression
	"""

def p_null_coalescing_expression(p):
	"""null_coalescing_expression : conditional_or_expression
				| conditional_or_expression "??" null_coalescing_expression
	"""
def p_conditional_or_expression(p):
	"""conditional_or_expression : conditional_and_expression
				| conditional_or_expression "||" conditional_and_expression
	"""
def p_conditional_and_expression(p):
	"""conditional_and_expression : inclusive_or_expression
				| conditional_and_expression "&&" inclusive_or_expression
	"""
def p_inclusive_or_expression(p):
	"""inclusive_or_expression : exclusive_or_expression
				| inclusive_or_expression "|" exclusive_or_expression
	"""
def p_exclusive_or_expression(p):
	"""exclusive_or_expression : and_expression
				| exclusive_or_expression "^" and_expression
	"""
def p_and_expression(p):
	"""and_expression : equality_expression
				| and_expression "&" equality_expression
	"""
def p_equality_expression(p):
	"""equality_expression : relational_expression
				| equality_expression "==" relational_expression
				| equality_expression "!=" relational_expression
	"""
def p_relational_expression(p):
	"""relational_expression : shift_expression
				| relational_expression "<" shift_expression
				| relational_expression ">" shift_expression
				| relational_expression "<=" shift_expression
				| relational_expression ">=" shift_expression
				| relational_expression "is" type
				| relational_expression "as" type
	"""
def p_shift_expression(p):
	"""shift_expression : additive_expression
				| shift_expression "<<" additive_expression
				| shift_expression right_shift additive_expression
	"""
def p_additive_expression(p):
	"""additive_expression : multiplicative_expression
				| additive_expression "+" multiplicative_expression
				| additive_expression "-" multiplicative_expression
	"""
def p_multiplicative_expression(p):
	"""multiplicative_expression : unary_expression
				| multiplicative_expression "*" unary_expression
				| multiplicative_expression "/" unary_expression
				| multiplicative_expression "%" unary_expression
	"""
def p_unary_expression(p):
	"""unary_expression : primary_expression
				| "+" unary_expression
				| "-" unary_expression
				| "!" unary_expression
				| "~" unary_expression
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
				| checked_expression
				| unchecked_expression
				| default_value_expression
				| anonymous_method_expression
	"""
def p_simple_name(p):
	"""simple_name : identifier type_argument_list_opt
	"""
def p_parenthesized_expression(p):
	"""parenthesized_expression : "(" expression ")"
	"""
def p_member_access(p):
	"""member_access : primary_expression "." identifier type_argument_list_opt
				| predefined_type "." identifier type_argument_list_opt
				| qualified_alias_member "." identifier
	"""
def p_predefined_type(p):
	"""predefined_type : "bool"
				| "byte"
				| "char"
				| "decimal"
				| "double"
				| "float"
				| "int"
				| "long"
				| "object"
				| "sbyte"
				| "short"
				| "string"
				| "uint"
				| "ulong"
				| "ushort"
	"""
def p_invocation_expression(p):
	"""invocation_expression : primary_expression "(" argument_list_opt ")"
	"""
def p_argument_list(p):
	"""argument_list : argument
				| argument_list "," argument
	"""
def p_argument(p):
	"""argument : argument_name_opt argument_value
	"""
def p_argument_value(p):
	"""argument_value : expression
				| "ref" variable_reference
				| "out" variable_reference
	"""
def p_variable_reference(p):
	"""variable_reference : expression
	"""
def p_element_access(p):
	"""element_access : primary_no_array_creation_expression "[" argument_list "]"
	"""
def p_this_access(p):
	"""this_access : "this"
	"""
def p_base_access(p):
	"""base_access : "base" "." identifier
				| "base" "[" argument_list "]"
	"""
def p_post_increment_expression(p):
	"""post_increment_expression : primary_expression "++"
	"""
def p_post_decrement_expression(p):
	"""post_decrement_expression : primary_expression "--"
	"""
def p_object_creation_expression(p):
	"""object_creation_expression : "new" type "(" argument_list_opt ")" object_or_collection_initializer_opt
				| "new" type object_or_collection_initializer
	"""
def p_object_or_collection_initializer(p):
	"""object_or_collection_initializer : object_initializer
				| collection_initializer
	"""
def p_object_initializer(p):
	"""object_initializer : "{" member_initializer_list_opt "}"
				| "{" member_initializer_list "," "}"
	"""
def p_member_initializer_list(p):
	"""member_initializer_list : member_initializer
				| member_initializer_list "," member_initializer
	"""
def p_member_initializer(p):
	"""member_initializer : identifier "=" initializer_value
	"""
def p_initializer_value(p):
	"""initializer_value : expression
				| object_or_collection_initializer
	"""
def p_collection_initializer(p):
	"""collection_initializer : "{" element_initializer_list "}"
				| "{" element_initializer_list "," "}"
	"""
def p_element_initializer_list(p):
	"""element_initializer_list : element_initializer
				| element_initializer_list "," element_initializer
	"""
def p_element_initializer(p):
	"""element_initializer : non_assignment_expression
				| "{" expression_list "}"
	"""
def p_expression_list(p):
	"""expression_list : expression
				| expression_list "," expression
	"""
def p_delegate_creation_expression(p):
	"""delegate_creation_expression : "new" delegate_type "(" expression ")"
	"""
def p_anonymous_object_creation_expression(p):
	"""anonymous_object_creation_expression : "new" anonymous_object_initializer
	"""
def p_anonymous_object_initializer(p):
	"""anonymous_object_initializer : "{" member_declarator_list_opt "}"
				| "{" member_declarator_list "," "}"
	"""
def p_member_declarator_list(p):
	"""member_declarator_list : member_declarator
				| member_declarator_list "," member_declarator
	"""
def p_member_declarator(p):
	"""member_declarator : simple_name
				| member_access
				| identifier "=" expression
	"""
def p_typeof_expression(p):
	"""typeof_expression : "typeof" "(" type ")"
				| "typeof" "(" unbound_type_name ")"
				| "typeof" "(" "void" ")"
	"""
def p_unbound_type_name(p):
	"""unbound_type_name : identifier generic_dimension_specifier_opt
				| identifier "::" identifier generic_dimension_specifier_opt
				| unbound_type_name "." identifier generic_dimension_specifier_opt
	"""
def p_generic_dimension_specifier(p):
	"""generic_dimension_specifier : "<" commas_opt ">"
	"""
def p_commas(p):
	"""commas : ","
				| commas ","
	"""
def p_checked_expression(p):
	"""checked_expression : "checked" "(" expression ")"
	"""
def p_unchecked_expression(p):
	"""unchecked_expression : "unchecked" "(" expression ")"
	"""
def p_default_value_expression(p):
	"""default_value_expression : "default" "(" type ")"
	"""
def p_anonymous_method_expression(p):
	"""anonymous_method_expression : "delegate" explicit_anonymous_function_signature_opt block
	"""
def p_explicit_anonymous_function_signature(p):
	"""explicit_anonymous_function_signature : "(" explicit_anonymous_function_parameter_list_opt ")"
	"""
def p_explicit_anonymous_function_parameter_list(p):
	"""explicit_anonymous_function_parameter_list : explicit_anonymous_function_parameter
				| explicit_anonymous_function_parameter_list "," explicit_anonymous_function_parameter
	"""
def p_explicit_anonymous_function_parameter(p):
	"""explicit_anonymous_function_parameter : anonymous_function_parameter_modifier_opt type identifier
	"""
def p_anonymous_function_parameter_modifier(p):
	"""anonymous_function_parameter_modifier : "ref"
				| "out"
	"""
def p_block(p):
	"""block : "{" statement_list_opt "}"
	"""
def p_statement_list(p):
	"""statement_list : statement
				| statement_list statement
	"""
def p_statement(p):
	"""statement : labeled_statement
				| declaration_statement
				| embedded_statement
	"""

def p_labeled_statement(p):
	"""labeled_statement: identifier ":" statement
	"""

def p_declaration_statement(p):
	"""declaration_statement : local_variable_declaration ";"
				| local_constant_declaration ";"
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
				| local_variable_declarators "," local_variable_declarator
	"""
def p_local_variable_declarator(p):
	"""local_variable_declarator : identifier
				| identifier "=" local_variable_initializer
	"""
def p_local_variable_initializer(p):
	"""local_variable_initializer : expression
				| array_initializer
	"""
def p_array_initializer(p):
	"""array_initializer : "{" variable_initializer_list_opt "}"
				| "{" variable_initializer_list "," "}"
	"""
def p_variable_initializer_list(p):
	"""variable_initializer_list : variable_initializer
				| variable_initializer_list "," variable_initializer
	"""
def p_variable_initializer(p):
	"""variable_initializer : expression
				| array_initializer
	"""
def p_local_constant_declaration(p):
	"""local_constant_declaration : "const" type constant_declarators
	"""
def p_constant_declarators(p):
	"""constant_declarators : constant_declarator
				| constant_declarators "," constant_declarator
	"""
def p_constant_declarator(p):
	"""constant_declarator : identifier "=" constant_expression
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
				| try_statement
				| checked_statement
				| unchecked_statement
				| lock_statement
				| using_statement
				| yield_statement
	"""
def p_empty_statement(p):
	"""empty_statement : ";"
	"""
def p_expression_statement(p):
	"""expression_statement : statement_expression ";"
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
	"""assignment_operator : "="
				| "+="
				| "-="
				| "*="
				| "/="
				| "%="
				| "&="
				| "|="
				| "^="
				| "<<="
				| right_shift_assignment
	"""
def p_right_shift_assignment(p):
	"""right_shift_assignment : ">>="
	"""
def p_pre_increment_expression(p):
	"""pre_increment_expression : "++" unary_expression
	"""
def p_pre_decrement_expression(p):
	"""pre_decrement_expression : "--" unary_expression
	"""
def p_selection_statement(p):
	"""selection_statement : if_statement
				| switch_statement
	"""
def p_if_statement(p):
	"""if_statement : "if" "(" boolean_expression ")" embedded_statement
				| "if" "(" boolean_expression ")" embedded_statement "else" embedded_statement
	"""
def p_boolean_expression(p):
	"""boolean_expression : expression
	"""
def p_switch_statement(p):
	"""switch_statement : "switch" "(" expression ")" switch_block
	"""
def p_switch_block(p):
	"""switch_block : "{" switch_sections_opt "}"
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
	"""switch_label : "case" constant_expression ":"
				| "default" ":"
	"""

def p_iteration_statement(p):
	"""iteration_statement : while_statement
				| do_statement
				| for_statement
				| foreach_statement
	"""
def p_while_statement(p):
	"""while_statement : "while" "(" boolean_expression ")" embedded_statement
	"""
def p_do_statement(p):
	"""do_statement : "do" embedded_statement "while" "(" boolean_expression ")" ";"
	"""
def p_for_statement(p):
	"""for_statement : "for" "(" for_initializer_opt ";" for_condition_opt ";" for_iterator_opt ")" embedded_statement
	"""
def p_for_initializer(p):
	"""for_initializer : local_variable_declaration
				| statement_expression_list
	"""
def p_statement_expression_list(p):
	"""statement_expression_list : statement_expression
				| statement_expression_list "," statement_expression
	"""
def p_for_condition(p):
	"""for_condition : boolean_expression
	"""
def p_for_iterator(p):
	"""for_iterator : statement_expression_list
	"""
def p_foreach_statement(p):
	"""foreach_statement : "foreach" "(" local_variable_type identifier "in" expression ")" embedded_statement
	"""
def p_jump_statement(p):
	"""jump_statement : break_statement
				| continue_statement
				| goto_statement
				| return_statement
				| throw_statement
	"""
def p_break_statement(p):
	"""break_statement : "break" ";"
	"""
def p_continue_statement(p):
	"""continue_statement : "continue" ";"
	"""
def p_goto_statement(p):
	"""goto_statement : "goto" identifier ";"
				| "goto" "case" constant_expression ";"
				| "goto" "default" ";"
	"""
def p_return_statement(p):
	"""return_statement : "return" expression_opt ";"
	"""
def p_throw_statement(p):
	"""throw_statement : "throw" expression_opt ";"
	"""
def p_try_statement(p):
	"""try_statement : "try" block catch_clauses
				| "try" block finally_clause
				| "try" block catch_clauses finally_clause
	"""
def p_catch_clauses(p):
	"""catch_clauses : specific_catch_clauses general_catch_clause_opt
				| specific_catch_clauses_opt general_catch_clause
	"""
def p_specific_catch_clauses(p):
	"""specific_catch_clauses : specific_catch_clause
				| specific_catch_clauses specific_catch_clause
	"""
def p_specific_catch_clause(p):
	"""specific_catch_clause : "catch" "(" class_type identifier_opt ")" block
	"""
def p_general_catch_clause(p):
	"""general_catch_clause : "catch" block
	"""
def p_finally_clause(p):
	"""finally_clause : "finally" block
	"""
def p_checked_statement(p):
	"""checked_statement : "checked" block
	"""
def p_unchecked_statement(p):
	"""unchecked_statement : "unchecked" block
	"""
def p_lock_statement(p):
	"""lock_statement : "lock" "(" expression ")" embedded_statement
	"""
def p_using_statement(p):
	"""using_statement : "using" "(" resource_acquisition ")" embedded_statement
	"""
def p_resource_acquisition(p):
	"""resource_acquisition : local_variable_declaration
				| expression
	"""
def p_yield_statement(p):
	"""yield_statement : "yield" "return" expression ";"
				| "yield" "break" ";"
	"""
def p_array_creation_expression(p):
	"""array_creation_expression : "new" non_array_type "[" expression_list "]" rank_specifiers_opt array_initializer_opt
				| "new" array_type array_initializer
				| "new" rank_specifier array_initializer
	"""
def p_cast_expression(p):
	"""cast_expression : "(" type ")" unary_expression
	"""
def p_right_shift(p):
	"""right_shift : ">>"
	"""
def p_lambda_expression(p):
	"""lambda_expression : anonymous_function_signature "=>" anonymous_function_body
	"""
def p_anonymous_function_signature(p):
	"""anonymous_function_signature : explicit_anonymous_function_signature
				| implicit_anonymous_function_signature
	"""
def p_implicit_anonymous_function_signature(p):
	"""implicit_anonymous_function_signature : "(" implicit_anonymous_function_parameter_list_opt ")"
				| implicit_anonymous_function_parameter
	"""
def p_implicit_anonymous_function_parameter_list(p):
	"""implicit_anonymous_function_parameter_list : implicit_anonymous_function_parameter
				| implicit_anonymous_function_parameter_list "," implicit_anonymous_function_parameter
	"""
def p_implicit_anonymous_function_parameter(p):
	"""implicit_anonymous_function_parameter : identifier
	"""
def p_anonymous_function_body(p):
	"""anonymous_function_body : expression
				| block
	"""
# def p_query_expression(p):
# 	"""query_expression : from_clause query_body
# 	"""
# def p_from_clause(p):
# 	"""from_clause : "from" type_opt identifier "in" expression
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
# 	"""let_clause : "let" identifier "=" expression
# 	"""
# def p_where_clause(p):
# 	"""where_clause : "where" boolean_expression
# 	"""
# def p_join_clause(p):
# 	"""join_clause : "join" type_opt identifier "in" expression "on" expression "equals" expression
# 	"""
# def p_join_into_clause(p):
# 	"""join_into_clause : "join" type_opt identifier "in" expression "on" expression "equals" expression "into" identifier
# 	"""
# def p_orderby_clause(p):
# 	"""orderby_clause : "orderby" orderings
# 	"""
# def p_orderings(p):
# 	"""orderings : ordering
# 				| orderings "," ordering
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
# 	"""query_continuation : "into" identifier query_body
# 	"""
def p_named_argument_list(p):
	"""named_argument_list : named_argument
				| named_argument_list "," named_argument
	"""
def p_named_argument(p):
	"""named_argument : identifier "=" attribute_argument_expression
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
	"""namespace_declaration : "namespace" qualified_identifier namespace_body ";"_opt
	"""
def p_qualified_identifier(p):
	"""qualified_identifier : identifier
				| qualified_identifier "." identifier
	"""
def p_namespace_body(p):
	"""namespace_body : "{" extern_alias_directives_opt using_directives_opt namespace_member_declarations_opt "}"
	"""
def p_type_declaration(p):
	"""type_declaration : class_declaration
				| struct_declaration
				| interface_declaration
				| enum_declaration
				| delegate_declaration
	"""
def p_class_declaration(p):
	"""class_declaration : attributes_opt class_modifiers_opt "partial"_opt "class" identifier type_parameter_list_opt
				| class_base_opt type_parameter_constraints_clauses_opt class_body ";"_opt
	"""
def p_attributes(p):
	"""attributes : attribute_sections
	"""
def p_attribute_sections(p):
	"""attribute_sections : attribute_section
				| attribute_sections attribute_section
	"""
def p_attribute_section(p):
	"""attribute_section : "[" attribute_target_specifier_opt attribute_list "]"
				| "[" attribute_target_specifier_opt attribute_list "," "]"
	"""
def p_attribute_target_specifier(p):
	"""attribute_target_specifier:
				| attribute_target ":"
	"""

def p_attribute_target(p):
	"""attribute_target : "field"
				| "event"
				| "method"
				| "param"
				| "property"
				| "return"
				| type
	"""
def p_class_modifiers(p):
	"""class_modifiers : class_modifier
				| class_modifiers class_modifier
	"""
def p_class_modifier(p):
	"""class_modifier : "new"
				| "public"
				| "protected"
				| "internal"
				| "private"
				| "abstract"
				| "sealed"
				| "static"
	"""
def p_type_parameter_list(p):
	"""type_parameter_list : "<" type_parameters ">"
	"""
def p_type_parameters(p):
	"""type_parameters : attributes_opt type_parameter
				| type_parameters "," attributes_opt type_parameter
	"""
def p_class_base(p):
	"""class_base:
				| ":" class_type
				| ":" interface_type_list
				| ":" class_type "," interface_type_list
	"""

def p_interface_type_list(p):
	"""interface_type_list : interface_type
				| interface_type_list "," interface_type
	"""
def p_type_parameter_constraints_clauses(p):
	"""type_parameter_constraints_clauses : type_parameter_constraints_clause
				| type_parameter_constraints_clauses type_parameter_constraints_clause
	"""
def p_type_parameter_constraints_clause(p):
	"""type_parameter_constraints_clause: "where" type_parameter ":" type_parameter_constraints
	"""

def p_type_parameter_constraints(p):
	"""type_parameter_constraints : primary_constraint
				| secondary_constraints
				| constructor_constraint
				| primary_constraint "," secondary_constraints
				| primary_constraint "," constructor_constraint
				| secondary_constraints "," constructor_constraint
				| primary_constraint "," secondary_constraints "," constructor_constraint
	"""
def p_primary_constraint(p):
	"""primary_constraint : class_type
				| "class"
				| "struct"
	"""
def p_secondary_constraints(p):
	"""secondary_constraints : interface_type
				| type_parameter
				| secondary_constraints "," interface_type
				| secondary_constraints "," type_parameter
	"""
def p_constructor_constraint(p):
	"""constructor_constraint : "new" "(" ")"
	"""
def p_class_body(p):
	"""class_body : "{" class_member_declarations_opt "}"
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
	"""constant_declaration : attributes_opt constant_modifiers_opt "const" type constant_declarators ";"
	"""
def p_constant_modifiers(p):
	"""constant_modifiers : constant_modifier
				| constant_modifiers constant_modifier
	"""
def p_constant_modifier(p):
	"""constant_modifier : "new"
				| "public"
				| "protected"
				| "internal"
				| "private"
	"""
def p_field_declaration(p):
	"""field_declaration : attributes_opt field_modifiers_opt type variable_declarators ";"
	"""
def p_field_modifiers(p):
	"""field_modifiers : field_modifier
				| field_modifiers field_modifier
	"""
def p_field_modifier(p):
	"""field_modifier : "new"
				| "public"
				| "protected"
				| "internal"
				| "private"
				| "static"
				| "readonly"
				| "volatile"
	"""
def p_variable_declarators(p):
	"""variable_declarators : variable_declarator
				| variable_declarators "," variable_declarator
	"""
def p_variable_declarator(p):
	"""variable_declarator : identifier
				| identifier "=" variable_initializer
	"""
def p_method_declaration(p):
	"""method_declaration : method_header method_body
	"""
def p_method_header(p):
	"""method_header : attributes_opt method_modifiers_opt "partial"_opt return_type member_name type_parameter_list_opt
				| "(" formal_parameter_list_opt ")" type_parameter_constraints_clauses_opt
	"""
def p_method_modifiers(p):
	"""method_modifiers : method_modifier
				| method_modifiers method_modifier
	"""
def p_method_modifier(p):
	"""method_modifier : "new"
				| "public"
				| "protected"
				| "internal"
				| "private"
				| "static"
				| "virtual"
				| "sealed"
				| "override"
				| "abstract"
				| "extern"
	"""
def p_return_type(p):
	"""return_type : type
				| "void"
	"""
def p_member_name(p):
	"""member_name : identifier
				| interface_type "." identifier
	"""
def p_formal_parameter_list(p):
	"""formal_parameter_list : fixed_parameters
				| fixed_parameters "," parameter_array
				| parameter_array
	"""
def p_fixed_parameters(p):
	"""fixed_parameters : fixed_parameter
				| fixed_parameters "," fixed_parameter
	"""
def p_fixed_parameter(p):
	"""fixed_parameter : attributes_opt parameter_modifier_opt type identifier default_argument_opt
	"""
def p_parameter_modifier(p):
	"""parameter_modifier : "ref"
				| "out"
				| "this"
	"""
def p_default_argument(p):
	"""default_argument : "=" expression
	"""
def p_parameter_array(p):
	"""parameter_array : attributes_opt "params" array_type identifier
	"""
def p_method_body(p):
	"""method_body : block
				| ";"
	"""
def p_property_declaration(p):
	"""property_declaration : attributes_opt property_modifiers_opt type member_name "{" accessor_declarations "}"
	"""
def p_property_modifiers(p):
	"""property_modifiers : property_modifier
				| property_modifiers property_modifier
	"""
def p_property_modifier(p):
	"""property_modifier : "new"
				| "public"
				| "protected"
				| "internal"
				| "private"
				| "static"
				| "virtual"
				| "sealed"
				| "override"
				| "abstract"
				| "extern"
	"""
def p_accessor_declarations(p):
	"""accessor_declarations : get_accessor_declaration set_accessor_declaration_opt
				| set_accessor_declaration get_accessor_declaration_opt
	"""
def p_get_accessor_declaration(p):
	"""get_accessor_declaration : attributes_opt accessor_modifier_opt "get" accessor_body
	"""
def p_accessor_modifier(p):
	"""accessor_modifier : "protected"
				| "internal"
				| "private"
				| "protected" "internal"
				| "internal" "protected"
	"""
def p_accessor_body(p):
	"""accessor_body : block
				| ";"
	"""
def p_set_accessor_declaration(p):
	"""set_accessor_declaration : attributes_opt accessor_modifier_opt "set" accessor_body
	"""
def p_event_declaration(p):
	"""event_declaration : attributes_opt event_modifiers_opt "event" type variable_declarators ";"
				| attributes_opt event_modifiers_opt "event" type member_name "{" event_accessor_declarations "}"
	"""
def p_event_modifiers(p):
	"""event_modifiers : event_modifier
				| event_modifiers event_modifier
	"""
def p_event_modifier(p):
	"""event_modifier : "new"
				| "public"
				| "protected"
				| "internal"
				| "private"
				| "static"
				| "virtual"
				| "sealed"
				| "override"
				| "abstract"
				| "extern"
	"""
def p_event_accessor_declarations(p):
	"""event_accessor_declarations : add_accessor_declaration remove_accessor_declaration
				| remove_accessor_declaration add_accessor_declaration
	"""
def p_add_accessor_declaration(p):
	"""add_accessor_declaration : attributes_opt "add" block
	"""
def p_remove_accessor_declaration(p):
	"""remove_accessor_declaration : attributes_opt "remove" block
	"""
def p_indexer_declaration(p):
	"""indexer_declaration : attributes_opt indexer_modifiers_opt indexer_declarator "{" accessor_declarations "}"
	"""
def p_indexer_modifiers(p):
	"""indexer_modifiers : indexer_modifier
				| indexer_modifiers indexer_modifier
	"""
def p_indexer_modifier(p):
	"""indexer_modifier : "new"
				| "public"
				| "protected"
				| "internal"
				| "private"
				| "virtual"
				| "sealed"
				| "override"
				| "abstract"
				| "extern"
	"""
def p_indexer_declarator(p):
	"""indexer_declarator : type "this" "[" formal_parameter_list "]"
				| type interface_type "." "this" "[" formal_parameter_list "]"
	"""
def p_operator_declaration(p):
	"""operator_declaration : attributes_opt operator_modifiers operator_declarator operator_body
	"""
def p_operator_modifiers(p):
	"""operator_modifiers : operator_modifier
				| operator_modifiers operator_modifier
	"""
def p_operator_modifier(p):
	"""operator_modifier : "public"
				| "static"
				| "extern"
	"""
def p_operator_declarator(p):
	"""operator_declarator : unary_operator_declarator
				| binary_operator_declarator
				| conversion_operator_declarator
	"""
def p_unary_operator_declarator(p):
	"""unary_operator_declarator : type "operator" overloadable_unary_operator "(" type identifier ")"
	"""
def p_overloadable_unary_operator(p):
	"""overloadable_unary_operator : "+"
				| "-"
				| "!"
				| "~"
				| "++"
				| "--"
				| "true"
				| "false"
	"""
def p_binary_operator_declarator(p):
	"""binary_operator_declarator : type "operator" overloadable_binary_operator "(" type identifier "," type identifier ")"
	"""
def p_overloadable_binary_operator(p):
	"""overloadable_binary_operator : "+"
				| "-"
				| "*"
				| "/"
				| "%"
				| "&"
				| "|"
				| "^"
				| "<<"
				| right_shift
				| "=="
				| "!="
				| ">"
				| "<"
				| ">="
				| "<="
	"""
def p_conversion_operator_declarator(p):
	"""conversion_operator_declarator : "implicit" "operator" type "(" type identifier ")"
				| "explicit" "operator" type "(" type identifier ")"
	"""
def p_operator_body(p):
	"""operator_body : block
				| ";"
	"""
def p_constructor_declaration(p):
	"""constructor_declaration : attributes_opt constructor_modifiers_opt constructor_declarator constructor_body
	"""
def p_constructor_modifiers(p):
	"""constructor_modifiers : constructor_modifier
				| constructor_modifiers constructor_modifier
	"""
def p_constructor_modifier(p):
	"""constructor_modifier : "public"
				| "protected"
				| "internal"
				| "private"
				| "extern"
	"""
def p_constructor_declarator(p):
	"""constructor_declarator : identifier "(" formal_parameter_list_opt ")" constructor_initializer_opt
	"""
def p_constructor_initializer(p):
	"""constructor_initializer: ":" "base" "(" argument_list_opt ")"
				| ":" "this" "(" argument_list_opt ")"
	"""

def p_constructor_body(p):
	"""constructor_body : block
				| ";"
	"""
def p_destructor_declaration(p):
	"""destructor_declaration : attributes_opt "extern"_opt "~" identifier "(" ")" destructor_body
	"""
def p_destructor_body(p):
	"""destructor_body : block
				| ";"
	"""
def p_static_constructor_declaration(p):
	"""static_constructor_declaration : attributes_opt static_constructor_modifiers identifier "(" ")" static_constructor_body
	"""
def p_static_constructor_modifiers(p):
	"""static_constructor_modifiers : "extern"_opt "static"
				| "static" "extern"_opt
	"""
def p_static_constructor_body(p):
	"""static_constructor_body : block
				| ";"
	"""
def p_struct_declaration(p):
	"""struct_declaration : attributes_opt struct_modifiers_opt "partial"_opt "struct" identifier type_parameter_list_opt
				| struct_interfaces_opt type_parameter_constraints_clauses_opt struct_body ";"_opt
	"""
def p_struct_modifiers(p):
	"""struct_modifiers : struct_modifier
				| struct_modifiers struct_modifier
	"""
def p_struct_modifier(p):
	"""struct_modifier : "new"
				| "public"
				| "protected"
				| "internal"
				| "private"
	"""
def p_struct_interfaces(p):
	"""struct_interfaces: ":" interface_type_list
	"""

def p_struct_body(p):
	"""struct_body : "{" struct_member_declarations_opt "}"
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
	"""interface_declaration : attributes_opt interface_modifiers_opt "partial"_opt "interface"
				| identifier variant_type_parameter_list_opt interface_base_opt
				| type_parameter_constraints_clauses_opt interface_body ";"_opt
	"""
def p_interface_modifiers(p):
	"""interface_modifiers : interface_modifier
				| interface_modifiers interface_modifier
	"""
def p_interface_modifier(p):
	"""interface_modifier : "new"
				| "public"
				| "protected"
				| "internal"
				| "private"
	"""
def p_variant_type_parameter_list(p):
	"""variant_type_parameter_list : "<" variant_type_parameters ">"
	"""
def p_variant_type_parameters(p):
	"""variant_type_parameters : attributes_opt variance_annotation_opt type_parameter
				| variant_type_parameters "," attributes_opt variance_annotation_opt type_parameter
	"""
def p_variance_annotation(p):
	"""variance_annotation : "in"
				| "out"
	"""
def p_interface_base(p):
	"""interface_base : ":" interface_type_list
	"""

def p_interface_body(p):
	"""interface_body : "{" interface_member_declarations_opt "}"
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
	"""interface_method_declaration : attributes_opt "new"_opt return_type identifier type_parameter_list
				| "(" formal_parameter_list_opt ")" type_parameter_constraints_clauses_opt ";"
	"""
def p_interface_property_declaration(p):
	"""interface_property_declaration : attributes_opt "new"_opt type identifier "{" interface_accessors "}"
	"""
def p_interface_accessors(p):
	"""interface_accessors : attributes_opt "get" ";"
				| attributes_opt "set" ";"
				| attributes_opt "get" ";" attributes_opt "set" ";"
				| attributes_opt "set" ";" attributes_opt "get" ";"
	"""
def p_interface_event_declaration(p):
	"""interface_event_declaration : attributes_opt "new"_opt "event" type identifier ";"
	"""
def p_interface_indexer_declaration(p):
	"""interface_indexer_declaration : attributes_opt "new"_opt type "this" "[" formal_parameter_list "]" "{" interface_accessors "}"
	"""
def p_enum_declaration(p):
	"""enum_declaration : attributes_opt enum_modifiers_opt "enum" identifier enum_base_opt enum_body ";"_opt
	"""
def p_enum_modifiers(p):
	"""enum_modifiers : enum_modifier
				| enum_modifiers enum_modifier
	"""
def p_enum_modifier(p):
	"""enum_modifier : "new"
				| "public"
				| "protected"
				| "internal"
				| "private"
	"""

def p_enum_base(p):
	"""enum_base : ":" integral_type
	"""

def p_enum_body(p):
	"""enum_body : "{" enum_member_declarations_opt "}"
				| "{" enum_member_declarations "," "}"
	"""
def p_enum_member_declarations(p):
	"""enum_member_declarations : enum_member_declaration
				| enum_member_declarations "," enum_member_declaration
	"""
def p_enum_member_declaration(p):
	"""enum_member_declaration : attributes_opt identifier
				| attributes_opt identifier "=" constant_expression
	"""
def p_delegate_declaration(p):
	"""delegate_declaration : attributes_opt delegate_modifiers_opt "delegate" return_type
				| identifier variant_type_parameter_list_opt
				| "(" formal_parameter_list_opt ")" type_parameter_constraints_clauses_opt ";"
	"""
def p_delegate_modifiers(p):
	"""delegate_modifiers : delegate_modifier
				| delegate_modifiers delegate_modifier
	"""
def p_delegate_modifier(p):
	"""delegate_modifier : "new"
				| "public"
				| "protected"
				| "internal"
				| "private"
	"""