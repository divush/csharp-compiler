#!/usr/bin/python3
# Interediate Code Generator

# Authors: Divyanshu Shende, Pranshu Gupta, Prashant Kumar, Rahul Tudu
# Compiler Design: CS335A, Group 25, Indian Institute of Technology, Kanpur
###################################################################################################

from lexer import *

###################################################################################################

# Implement the symbol table and all the IR methods here

sym_tab = [dict()]

def push_scope():
	sym_tab.append({})

def pop_scope():
	sym_tab.pop()

def insert(varname, vartype, varval, size, modifiers, category):
	if varname in sym_tab[-1]:
		print("Error: ", varname, "declared before in this scope.")
		exit()
	else:
		sym_tab[-1][varname] = {'type':vartype, 'size':size, 'val':varval, 'modifiers':modifiers, 'category':category}

def lookup(varname):
	i = len(sym_tab) - 1
	while i >= 0:
		if varname in sym_tab[i]:
			typ = sym_tab[i][varname]['type']
			size = sym_tab[i][varname]['size'] 
			val = sym_tab[i][varname]['val']
			return [i, typ, size, val]
		i = i - 1
	return None


class array_type:
	def __init__(typ, length):
		self.sub_typ = typ
		self.length = length
		self.size = typ.size * length

class pointer:
	def __init__(typ):
		self.sub_typ = typ
		self.size = 4
count = 0
TAC=[]
def emit(lineir):
	TAC.append(lineir)

def create_array_from_basic(typ, dims, init):
	pass

def create_array_from_array(typ, init):
	return 


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

def create_new_object(typ, parameters):
	pass

def typof_expr(typ):
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
	count = count + 1
	#Check for operand1 and operand2 in symtab
	#vartype = operand1
	op1_l = lookup(operand1)
	op2_l = lookup(operand2)
	if op1_l is None:
		print("Error: Variable "+ op1[0] + " not delared!")
		exit()
	if op2_l is None:
		print("Error: Variable "+ op2[0] + " not delared!")
		exit()
	tvar = "t"+str(count)
	tvar_type = op1_l[1]
	tvar_size = max(op1_l[3], op2_l[3])
	insert(varname=tvar, vartype=tvar_type, varval=None, size=tvar_size, modifiers=None, category="temp")
	temp = str(operator)+", " + tvar +", " + str(operand1)+", " + str(operand2)
	emit(temp)
	return tvar

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
	e1 = lookup(expr1)
	e2 = lookup(expr2)
	if e1 is None:
		print("Error: Variable "+ e1[0] + " not delared!")
		exit()
	if e2 is None:
		print("Error: Variable "+ e2[0] + " not delared!")
		exit()
	e1[2] = e2[2]
	temp = str(op) + ", " + str(expr1) + ", " + str(expr2)

def create_labeled_statement(label, stmt):
	pass

def declare_variables(modifiers, typ, declarators):
	for decl in declarators:
		varname, varval = decl[0], None
		width = typ.size
		if len(decl) == 2:
			varval = decl[1]
		insert(varname, vartype, varval, size, modifiers, 'variable')


def declare_constants(modifiers, typ, declarators):
	for decl in declarators:
		varname, varval = decl[0], None
		width = typ.size
		if len(decl) == 2:
			varval = decl[1]
		insert(varname, vartype, varval, size, modifiers, 'constant')

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
	using_directives, member_decls = body[0], body[1]
	


def create_identifier_alias(identifier, qual_identifier):
	pass

def create_using_namespace_directive(name):
	pass

def create_class(modifiers, identifier, base, body):
	pass

def create_method(header, body):
	pass

def create_operator_declaration(modifiers, declarator, body):
	pass

def create_constructor(modifiers, declarator, body):
	pass

def create_destructor(modifiers, identifier, body):
	pass

def create_struct(modifiers, identifier, body):
	pass

def create_enum(modifiers, identifier, base, body):
	pass