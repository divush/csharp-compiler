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

# C.2 Syntactic grammar 

# C.2.1 Basic concepts 
def p_namespace_name(p):
	"""namespace_name : qualified_identifier
	"""
def p_type_name(p):
	"""type_name : qualified_identifier
	"""
# C.2.2 Types 
def p_type(p):
	"""type : non_array_type
		| array_type
	"""
def p_non_array_type(p):
	"""non_array_type : simple_type
		| type_name
	"""
def p_simple_type(p):
	"""simple_type : primitive_type
		| class_type
		| pointer_type
	"""
def p_primitive_type(p):
	"""primitive_type : numeric_type
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
def p_class_type(p):
	"""class_type : OBJECT 
					| STRING
	"""
def p_pointer_type(p):
	"""pointer_type : type dereferencer
		| VOID dereferencer
	"""

def p_dereferencer(p):
	"""dereferencer : TIMES
	"""

def p_array_type(p):
	"""array_type : array_type rank_specifier
		| simple_type rank_specifier
		| qualified_identifier rank_specifier
	"""
def p_rank_specifier(p):
	"""rank_specifier : LBRACKET dim_separators_opt RBRACKET
	"""
def p_dim_separators_opt(p): 
	"""dim_separators_opt : empty 
			| dim_separators""" 
def p_dim_separators(p):
	"""dim_separators : COMMA
				| dim_separators COMMA
	"""

# C.2.3 Variables 
def p_variable_reference(p):
	"""variable_reference : expression
	"""
# C.2.4 Expressions 
def p_argument_list(p):
	"""argument_list : argument
		| argument_list COMMA argument
	"""
def p_argument(p):
	"""argument : expression
		| REF variable_reference
		| OUT variable_reference
	"""
def p_primary_expression(p):
	"""primary_expression : parenthesized_expression
		| primary_expression_no_parenthesis
		| anonymous_method_expression
	"""
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
# Literal
def p_literal(p):
	"""literal : INTCONST
				| STRCONST
				| CHCONST
	"""
def p_parenthesized_expression(p):
	"""parenthesized_expression : LPAREN expression RPAREN
	"""
def p_member_access(p):
	"""member_access : primary_expression MEMBERACCESS IDENTIFIER
		| primitive_type MEMBERACCESS IDENTIFIER
		| class_type MEMBERACCESS IDENTIFIER
	"""
def p_invocation_expression(p):
	"""invocation_expression : primary_expression_no_parenthesis LPAREN argument_list_opt RPAREN
		| qualified_identifier LPAREN argument_list_opt RPAREN
	"""
def p_argument_list_opt(p):
	"""argument_list_opt : empty 
		| argument_list
	"""
def p_element_access(p):
	"""element_access : primary_expression LBRACKET expression_list RBRACKET
		| qualified_identifier LBRACKET expression_list RBRACKET
	"""
def p_expression_list(p):
	"""expression_list : expression
		| expression_list COMMA expression
	"""
def p_this_access(p):
	"""this_access : THIS
	"""
def p_base_access(p):
	"""base_access : BASE MEMBERACCESS IDENTIFIER
		| BASE LBRACKET expression_list RBRACKET
	"""
def p_post_increment_expression(p):
	"""post_increment_expression : postfix_expression INCREMENT
	"""
def p_post_decrement_expression(p):
	"""post_decrement_expression : postfix_expression DECREMENT
	"""
def p_new_expression(p):
	"""new_expression : object_creation_expression
	"""
def p_object_creation_expression(p):
	"""object_creation_expression : NEW type LPAREN argument_list_opt RPAREN
	"""
def p_array_creation_expression(p):
	"""array_creation_expression : NEW non_array_type LBRACKET expression_list RBRACKET array_initializer_opt
		| NEW array_type array_initializer
	"""
def p_array_initializer_opt(p):
	"""array_initializer_opt : empty 
		| array_initializer
	"""
def p_typeof_expression(p):
	"""typeof_expression : TYPEOF LPAREN type RPAREN
		| TYPEOF LPAREN VOID RPAREN
	"""
def p_checked_expression(p):
	"""checked_expression : CHECKED LPAREN expression RPAREN
	"""
def p_unchecked_expression(p):
	"""unchecked_expression : UNCHECKED LPAREN expression RPAREN
	"""
def p_pointer_member_access(p):
	"""pointer_member_access : postfix_expression ARROW IDENTIFIER
	"""
def p_addressof_expression(p):
	"""addressof_expression : AND unary_expression
	"""
def p_sizeof_expression(p):
	"""sizeof_expression : SIZEOF LPAREN type RPAREN
	"""
def p_postfix_expression(p):
	"""postfix_expression : primary_expression
		| qualified_identifier
		| post_increment_expression
		| post_decrement_expression
		| pointer_member_access
	"""
def p_unary_expression_not_plusminus(p):
	"""unary_expression_not_plusminus : postfix_expression
		| LNOT unary_expression
		| NOT unary_expression
		| cast_expression
	"""
def p_pre_increment_expression(p):
	"""pre_increment_expression : INCREMENT unary_expression
	"""
def p_pre_decrement_expression(p):
	"""pre_decrement_expression : DECREMENT unary_expression
	"""
def p_unary_expression(p):
	"""unary_expression : unary_expression_not_plusminus
		| PLUS unary_expression
		| MINUS unary_expression
		| TIMES unary_expression
		| pre_increment_expression
		| pre_decrement_expression
		| addressof_expression
	"""

def p_cast_expression(p):
	"""cast_expression : LPAREN expression RPAREN unary_expression_not_plusminus
		| LPAREN multiplicative_expression TIMES RPAREN unary_expression 
		| LPAREN qualified_identifier rank_specifier type_quals_opt RPAREN unary_expression	
		| LPAREN primitive_type type_quals_opt RPAREN unary_expression
		| LPAREN class_type type_quals_opt RPAREN unary_expression
		| LPAREN VOID type_quals_opt RPAREN unary_expression
	"""
def p_type_quals_opt(p):
	"""type_quals_opt : empty 
		| type_quals
	"""
def p_type_quals(p):
	"""type_quals : type_qual
		| type_quals type_qual
	"""
def p_type_qual (p):
	"""type_qual  : rank_specifier 
		| dereferencer
	"""
def p_multiplicative_expression(p):
	"""multiplicative_expression : unary_expression
		| multiplicative_expression TIMES unary_expression	
		| multiplicative_expression DIVIDE unary_expression
		| multiplicative_expression MOD unary_expression
	"""
def p_additive_expression(p):
	"""additive_expression : multiplicative_expression
		| additive_expression PLUS multiplicative_expression
		| additive_expression MINUS multiplicative_expression
	"""
def p_shift_expression(p):
	"""shift_expression : additive_expression 
		| shift_expression LSHIFT additive_expression
		| shift_expression RSHIFT additive_expression
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
def p_equality_expression(p):
	"""equality_expression : relational_expression
		| equality_expression EQ relational_expression
		| equality_expression NE relational_expression
	"""
def p_and_expression(p):
	"""and_expression : equality_expression
		| and_expression AND equality_expression
	"""
def p_exclusive_or_expression(p):
	"""exclusive_or_expression : and_expression
		| exclusive_or_expression XOR and_expression
	"""
def p_inclusive_or_expression(p):
	"""inclusive_or_expression : exclusive_or_expression
		| inclusive_or_expression OR exclusive_or_expression
	"""
def p_conditional_and_expression(p):
	"""conditional_and_expression : inclusive_or_expression
		| conditional_and_expression CAND inclusive_or_expression
	"""
def p_conditional_or_expression(p):
	"""conditional_or_expression : conditional_and_expression
		| conditional_or_expression COR conditional_and_expression
	"""
def p_conditional_expression(p):
	"""conditional_expression : conditional_or_expression
		| conditional_or_expression CONDOP expression COLON expression
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
							| XOREQUAL
							| ANDEQUAL
							| OREQUAL
							| RSHIFTEQUAL
							| LSHIFTEQUAL
	"""
def p_expression(p):
	"""expression : conditional_expression
		| lambda_expression
		| assignment
	"""
def p_constant_expression(p):
	"""constant_expression : expression
	"""
def p_boolean_expression(p):
	"""boolean_expression : expression
	"""
# C.2.5 Statements 
def p_statement(p):
	"""statement : labeled_statement
		| declaration_statement
		| embedded_statement
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
		| unsafe_statement
		| fixed_statement
	"""
def p_block(p):
	"""block : LBRACE statement_list_opt RBRACE
	"""
def p_statement_list_opt(p):
	"""statement_list_opt : empty 
		| statement_list
	"""

def p_statement_list(p):
	"""statement_list : statement
		| statement_list statement
	"""
def p_empty_statement(p):
	"""empty_statement : STMT_TERMINATOR
	"""
def p_labeled_statement(p):
	"""labeled_statement : IDENTIFIER COLON statement
	"""
def p_declaration_statement(p):
	"""declaration_statement : local_variable_declaration STMT_TERMINATOR
		| local_constant_declaration STMT_TERMINATOR
	"""
def p_local_variable_declaration(p):
	"""local_variable_declaration : type variable_declarators
	"""
def p_variable_declarators(p):
	"""variable_declarators : variable_declarator
		| variable_declarators COMMA variable_declarator
	"""
def p_variable_declarator(p):
	"""variable_declarator : IDENTIFIER
		| IDENTIFIER EQUALS variable_initializer
	"""
def p_variable_initializer(p):
	"""variable_initializer : expression
		| array_initializer
		| stackalloc_initializer
	"""
def p_stackalloc_initializer(p):
	"""stackalloc_initializer : STACKALLOC type LBRACKET expression RBRACKET
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
def p_selection_statement(p):
	"""selection_statement : if_statement
		| switch_statement
	"""
def p_if_statement(p):
	"""if_statement : IF LPAREN boolean_expression RPAREN embedded_statement
		| IF LPAREN boolean_expression RPAREN embedded_statement ELSE embedded_statement
	"""
def p_switch_statement(p):
	"""switch_statement : SWITCH LPAREN expression RPAREN switch_block
	"""
def p_switch_block(p):
	"""switch_block : LBRACE switch_sections_opt RBRACE
	"""
def p_switch_sections_opt(p):
	"""switch_sections_opt : empty 
		| switch_sections
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
		| foreach_statement
	"""
def p_unsafe_statement(p):
	"""unsafe_statement : UNSAFE block
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
def p_for_initializer_opt(p):
	"""for_initializer_opt : empty 
		| for_initializer
	"""
def p_for_condition_opt(p):
	"""for_condition_opt : empty 
		| for_condition
	"""
def p_for_iterator_opt(p):
	"""for_iterator_opt : empty 
		| for_iterator
	"""
def p_for_initializer(p):
	"""for_initializer : local_variable_declaration
		| statement_expression_list
	"""
def p_for_condition(p):
	"""for_condition : boolean_expression
	"""
def p_for_iterator(p):
	"""for_iterator : statement_expression_list
	"""
def p_statement_expression_list(p):
	"""statement_expression_list : statement_expression
		| statement_expression_list COMMA statement_expression
	"""
def p_foreach_statement(p):
	"""foreach_statement : FOREACH LPAREN type IDENTIFIER IN expression RPAREN embedded_statement
	"""
def p_jump_statement(p):
	"""jump_statement : break_statement
		| continue_statement
		| goto_statement
		| return_statement
		| throw_statement
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
def p_expression_opt(p):
	"""expression_opt : empty 
		| expression
	"""
def p_throw_statement(p):
	"""throw_statement : THROW expression_opt STMT_TERMINATOR
	"""
def p_try_statement(p):
	"""try_statement : TRY block catch_clauses
		| TRY block finally_clause
		| TRY block catch_clauses finally_clause
	"""
def p_catch_clauses(p):
	"""catch_clauses : catch_clause
		| catch_clauses catch_clause
	"""
def p_catch_clause(p):
	"""catch_clause : CATCH LPAREN class_type identifier_opt RPAREN block
		| CATCH LPAREN type_name identifier_opt RPAREN block
		| CATCH block
	"""
def p_identifier_opt(p):
	"""identifier_opt : empty 
		| IDENTIFIER
	"""
def p_finally_clause(p):
	"""finally_clause : FINALLY block
	"""
def p_checked_statement(p):
	"""checked_statement : CHECKED block
	"""
def p_unchecked_statement(p):
	"""unchecked_statement : UNCHECKED block
	"""
def p_lock_statement(p):
	"""lock_statement : LOCK LPAREN expression RPAREN embedded_statement
	"""
def p_using_statement(p):
	"""using_statement : USING LPAREN resource_acquisition RPAREN embedded_statement
	"""
def p_resource_acquisition(p):
	"""resource_acquisition : local_variable_declaration
		| expression
	"""
def p_fixed_statement(p):
	"""fixed_statement : FIXED LPAREN	type fixed_pointer_declarators RPAREN embedded_statement
	"""
def p_fixed_pointer_declarators(p):
	"""fixed_pointer_declarators : fixed_pointer_declarator
		| fixed_pointer_declarators COMMA fixed_pointer_declarator
	"""
def p_fixed_pointer_declarator(p):
	"""fixed_pointer_declarator : IDENTIFIER EQUALS expression
	"""

# Lambda Expressions
def p_lambda_expression(p):
	"""lambda_expression : explicit_anonymous_function_signature LAMBDADEC block
						| explicit_anonymous_function_signature LAMBDADEC expression
	"""

# Anonymous Method Expression
def p_anonymous_method_expression(p):
	"""anonymous_method_expression : DELEGATE explicit_anonymous_function_signature_opt block
	"""
def p_explicit_anonymous_function_signature_opt(p):
	"""explicit_anonymous_function_signature_opt : explicit_anonymous_function_signature
												| empty
	"""
def p_explicit_anonymous_function_signature(p):
	"""explicit_anonymous_function_signature : LPAREN explicit_anonymous_function_parameter_list_opt RPAREN
	"""
def p_explicit_anonymous_function_parameter_list_opt(p):
	"""explicit_anonymous_function_parameter_list_opt : explicit_anonymous_function_parameter_list
														| empty
	"""
def p_explicit_anonymous_function_parameter_list(p):
	"""explicit_anonymous_function_parameter_list : explicit_anonymous_function_parameter
													| explicit_anonymous_function_parameter_list COMMA explicit_anonymous_function_parameter
	"""
def p_explicit_anonymous_function_parameter(p):
	"""explicit_anonymous_function_parameter : type IDENTIFIER
	"""	

# Compilation Unit
def p_compilation_unit(p):
	"""compilation_unit : using_directives_opt
		| using_directives_opt namespace_member_declarations
	"""
def p_using_directives_opt(p):
	"""using_directives_opt : empty 
		| using_directives
	"""
def p_namespace_member_declarations_opt(p):
	"""namespace_member_declarations_opt : empty 
		| namespace_member_declarations
	"""
def p_namespace_declaration(p):
	"""namespace_declaration :  NAMESPACE qualified_identifier namespace_body comma_opt
	"""
def p_comma_opt(p):
	"""comma_opt : empty 
		| STMT_TERMINATOR
	"""

def p_qualified_identifier(p):
	"""qualified_identifier : IDENTIFIER
		| qualifier IDENTIFIER
	"""

def p_qualifier(p):
	"""qualifier : IDENTIFIER MEMBERACCESS 
		| qualifier IDENTIFIER MEMBERACCESS 
	"""
def p_namespace_body(p):
	"""namespace_body : LBRACE using_directives_opt namespace_member_declarations_opt RBRACE
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
	"""using_alias_directive : USING IDENTIFIER EQUALS qualified_identifier STMT_TERMINATOR
	"""
def p_using_namespace_directive(p):
	"""using_namespace_directive : USING namespace_name STMT_TERMINATOR
	"""
def p_namespace_member_declarations(p):
	"""namespace_member_declarations : namespace_member_declaration
		| namespace_member_declarations namespace_member_declaration
	"""
def p_namespace_member_declaration(p):
	"""namespace_member_declaration : namespace_declaration
		| type_declaration
	"""
def p_type_declaration(p):
	"""type_declaration : class_declaration
		| struct_declaration
		| enum_declaration
		| delegate_declaration
	"""

# Modifiers
 
def p_modifiers_opt(p):
	"""modifiers_opt : empty 
		| modifiers
	"""
def p_modifiers(p):
	"""modifiers : modifier
		| modifiers modifier
	"""
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

# C.2.6 Classes 
def p_class_declaration(p):
	"""class_declaration :  modifiers_opt CLASS IDENTIFIER class_base_opt class_body comma_opt
	"""
def p_class_base_opt(p):
	"""class_base_opt : empty 
		| class_base
	"""
def p_class_base(p):
	"""class_base : COLON class_type
	"""
def p_class_body(p):
	"""class_body : LBRACE class_member_declarations_opt RBRACE
	"""
def p_class_member_declarations_opt(p):
	"""class_member_declarations_opt : empty 
		| class_member_declarations
	"""
def p_class_member_declarations(p):
	"""class_member_declarations : class_member_declaration
		| class_member_declarations class_member_declaration
	"""
def p_class_member_declaration(p):
	"""class_member_declaration : constant_declaration
		| field_declaration
		| method_declaration
		| operator_declaration
		| constructor_declaration
		| destructor_declaration 
		| type_declaration
	"""
def p_constant_declaration(p):
	"""constant_declaration :  modifiers_opt CONST type constant_declarators STMT_TERMINATOR
	"""
def p_field_declaration(p):
	"""field_declaration :  modifiers_opt type variable_declarators STMT_TERMINATOR
	"""
def p_method_declaration(p):
	"""method_declaration : method_header method_body
	"""

def p_method_header(p):
	"""method_header :  modifiers_opt type qualified_identifier LPAREN formal_parameter_list_opt RPAREN
		|  modifiers_opt VOID qualified_identifier LPAREN formal_parameter_list_opt RPAREN
	"""
def p_formal_parameter_list_opt(p):
	"""formal_parameter_list_opt : empty 
		| formal_parameter_list
	"""
def p_return_type(p):
	"""return_type : type
		| VOID
	"""
def p_method_body(p):
	"""method_body : block
		| STMT_TERMINATOR
	"""
def p_formal_parameter_list(p):
	"""formal_parameter_list : formal_parameter
		| formal_parameter_list COMMA formal_parameter
	"""
def p_formal_parameter(p):
	"""formal_parameter : fixed_parameter
		| parameter_array
	"""
def p_fixed_parameter(p):
	"""fixed_parameter :  parameter_modifier_opt type IDENTIFIER
	"""
def p_parameter_modifier_opt(p):
	"""parameter_modifier_opt : empty 
		| REF
		| OUT
	"""
def p_parameter_array(p):
	"""parameter_array :  PARAMS type IDENTIFIER
	"""

 
def p_operator_declaration(p):
	"""operator_declaration :  modifiers_opt operator_declarator operator_body
	"""
def p_operator_declarator(p):
	"""operator_declarator : overloadable_operator_declarator
		| conversion_operator_declarator
	"""
def p_overloadable_operator_declarator(p):
	"""overloadable_operator_declarator : type OPERATOR overloadable_operator LPAREN type IDENTIFIER RPAREN
		| type OPERATOR overloadable_operator LPAREN type IDENTIFIER COMMA type IDENTIFIER RPAREN
	"""
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
def p_conversion_operator_declarator(p):
	"""conversion_operator_declarator : IMPLICIT OPERATOR type LPAREN type IDENTIFIER RPAREN
		| EXPLICIT OPERATOR type LPAREN type IDENTIFIER RPAREN
	"""
def p_constructor_declaration(p):
	"""constructor_declaration :  modifiers_opt constructor_declarator constructor_body
	"""
def p_constructor_declarator(p):
	"""constructor_declarator : IDENTIFIER LPAREN formal_parameter_list_opt RPAREN constructor_initializer_opt
	"""
def p_constructor_initializer_opt(p):
	"""constructor_initializer_opt : empty 
		| constructor_initializer
	"""
def p_constructor_initializer(p):
	"""constructor_initializer : COLON BASE LPAREN argument_list_opt RPAREN
		| COLON THIS LPAREN argument_list_opt RPAREN
	"""

def p_destructor_declaration(p):
	"""destructor_declaration :  modifiers_opt NOT IDENTIFIER LPAREN RPAREN block
	"""
def p_operator_body(p):
	"""operator_body : block
		| STMT_TERMINATOR
	"""
def p_constructor_body(p):
	"""constructor_body : block
		| STMT_TERMINATOR
	"""

# C.2.7 Structs 
def p_struct_declaration(p):
	"""struct_declaration :  modifiers_opt STRUCT IDENTIFIER struct_body comma_opt
	"""
def p_struct_body(p):
	"""struct_body : LBRACE struct_member_declarations_opt RBRACE
	"""
def p_struct_member_declarations_opt(p):
	"""struct_member_declarations_opt : empty 
		| struct_member_declarations
	"""
def p_struct_member_declarations(p):
	"""struct_member_declarations : struct_member_declaration
		| struct_member_declarations struct_member_declaration
	"""
def p_struct_member_declaration(p):
	"""struct_member_declaration : constant_declaration
		| field_declaration
		| method_declaration
		| operator_declaration
		| constructor_declaration
		| type_declaration
	"""

# C.2.8 Arrays 
def p_array_initializer(p):
	"""array_initializer : LBRACE variable_initializer_list_opt RBRACE
		| LBRACE variable_initializer_list COMMA RBRACE
	"""
def p_variable_initializer_list_opt(p):
	"""variable_initializer_list_opt : empty 
		| variable_initializer_list
	"""
def p_variable_initializer_list(p):
	"""variable_initializer_list : variable_initializer
		| variable_initializer_list COMMA variable_initializer
	"""

# C.2.10 Enums 
def p_enum_declaration(p):
	"""enum_declaration :  modifiers_opt ENUM IDENTIFIER enum_base_opt enum_body comma_opt
	"""
def p_enum_base_opt(p):
	"""enum_base_opt : empty 
		| enum_base
	"""
def p_enum_base(p):
	"""enum_base : COLON integral_type
	"""
def p_enum_body(p):
	"""enum_body : LBRACE enum_member_declarations_opt RBRACE
		| LBRACE enum_member_declarations COMMA RBRACE
	"""
def p_enum_member_declarations_opt(p):
	"""enum_member_declarations_opt : empty 
		| enum_member_declarations
	"""
def p_enum_member_declarations(p):
	"""enum_member_declarations : enum_member_declaration
		| enum_member_declarations COMMA enum_member_declaration
	"""
def p_enum_member_declaration(p):
	"""enum_member_declaration :  IDENTIFIER
		|  IDENTIFIER EQUALS constant_expression
	"""

# C.2.11 Delegates 
def p_delegate_declaration(p):
	"""delegate_declaration :  modifiers_opt DELEGATE return_type IDENTIFIER LPAREN formal_parameter_list_opt RPAREN STMT_TERMINATOR
	"""

# Anonymous Functions


def p_empty(p):
	"""empty :"""
	pass

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