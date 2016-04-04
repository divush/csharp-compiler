#!/usr/bin/python3
# Parser for C# in Python

# Grammar Specification Reference
# https://msdn.microsoft.com/en-in/library/aa664812(v=vs.71).aspx
# With some modifications to resolve conflicts

# Authors: Divyanshu Shende, Pranshu Gupta, Prashant Kumar, Rahul Tudu
# Compiler Design: CS335A, Group 25, Indian Institute of Technology, Kanpur
###################################################################################################

from lexer import *

###################################################################################################

# Implement the symbol table and all the IR methods here

def pointer(type):
	pass

def create_array_type(type, length):
	pass

def get_member_value(expr, identifier):
	pass

def function_call(expr, parameters):
	pass

def get_array_element(array, index):
	pass

def post_increment_expression(expr):
	pass

def post_decrement_expression(expr):
	pass

def create_new_object(type, parameters):
	pass

def create_array_from_basic(type, dims, init):
	pass

def create_array_from_array(type, init):
	pass

def typeof_expr(type):
	pass

def get_member_value_via_pointer(object_ptr, member):
	pass

def address_of(expr):
	pass

def logical_not_of(expr):
	pass

def not_of(expr):
	pass

def pre_increment_expression(expr):
	pass

def pre_decrement_expression(expr):
	pass

def expression(operand1, operator, operand2):
	pass

def create_and_expression(and_expr, clause):
	pass

def create_xor_expression(xor_expr, clause):
	pass

def create_or_expression(or_expr, clause):
	pass

def create_cand_expression(cand_expr, clause):
	pass

def create_cor_expression(cor_expr, clause):
	pass

def condop_expression(cond, expr1, expr2):
	pass

def assignment(expr1, op, expr2):
	pass

def create_labeled_statement(label, stmt):
	pass

def declare_variables(modifiers, type, declarators):
	pass

def declare_constants(modifiers, type, declarators):
	pass

def create_if_statement(cond, expr):
	pass

def create_if_else_statement(cond, expr1, expr2):
	pass

def create_switch_statement(expr, block):
	pass

def create_switch_section(label, stmts):
	pass

def create_while_statement(cond, block):
	pass

def create_for_statement(init, cond, iter, stmts):
	pass

def create_return_statement(expr):
	pass

def create_lambda_expression(params, stmts):
	pass

def create_namespace(name, body):
	pass

def create_identifier_alias(identifier, qual_identifier):
	pass

def create_using_namespace_directive(name):
	pass

def create_class(modifiers, identifier, base, body):
	pass

def create_method(header, body):
	pass