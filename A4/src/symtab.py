#!/usr/bin/python3
# Symbol Table Implementation

from copy import deepcopy


base_table = None

# Types
class type:
	def __init__(self, name, isbasic, isarray, ispointer, width, elem_type, length):
		self.name = name
		self.isbasic = isbasic
		self.isarray = isarray
		self.ispointer = ispointer
		self.width = width
		self.elem_type = elem_type
		self.length = length
	
	def type_name(self):
		if self.isbasic:
			return self.name
		elif self.isarray:
			return "array of " + self.elem_type.type_name() + ", length " + str(self.length)

class table:
	def __init__(self, prev = None):
		self.hash = {}
		self.width = 0
		self.parent = prev
		self.children = []

	def insert_variable(self, var_type, identifier):
		self.hash[identifier] = {}
		self.hash[identifier]['type'] = var_type
		self.hash[identifier]['category'] = 'variable'

	def insert_temp(self, var_type, identifier):
		if identifier not in self.hash:		
			self.hash[identifier] = {}
			self.hash[identifier]['type'] = var_type
			self.hash[identifier]['category'] = 'temporary'
			return True	
		else:
			return False

	def insert_array(self, var_type, identifier):
		self.hash[identifier] = {}
		self.hash[identifier]['type'] = var_type
		self.hash[identifier]['category'] = 'array'


	# def lookup(self, identifier, table):
	# 	if table == None:
	# 		return None
	# 	v = table.lookup_in_this(identifier)
	# 	if v == None:
	# 		lookup(self, identifier, table.parent)

		

	def insert_function(self, method_name, return_type, param_types, param_num):
		if method_name not in self.hash:
			self.hash[method_name] = {}
			self.hash[method_name]['type'] = return_type
			self.hash[method_name]['category'] = 'function'
			self.hash[method_name]['arg_num'] = param_num
			self.hash[method_name]['arg_types'] = param_types
		

	def lookup_in_this(self, identifier):
		if identifier in self.hash:
			return self.hash[identifier]
		else:
			return None

	def print_symbol_table(self):
		print("")
		for key in self.hash:
			print("NAME: ", key)
			for k in self.hash[key]:
				if k == 'type' and not isinstance(self.hash[key][k], str):
					print(k, ': ', self.hash[key][k].type_name())
				elif k == 'arg_types':
					types = []
					for t in self.hash[key][k]:
						if not isinstance(t, str):
							types.append(t.type_name())
						else:
							types.append(t)
					print(k, ': ', types)
				else:
					print(k, ': ', self.hash[key][k])
			print("")


# A wrapper around the table class to maintain different scopes
class environ:
	def __init__(self):
		self.curr_table = table(None)
		# global temp_count
		# global label_count
		global base_table
		base_table = self.curr_table
		self.label_count = 0
		self.temp_count = 0

	def maketemp(self, temp_type, table):
		success = False
		while not success:
			name = "t"+str(self.temp_count)
			self.temp_count += 1
			success = table.insert_temp(temp_type, name)
		return name


	# Labels
	def newlabel(self):
		label = "L"+str(self.label_count)
		self.label_count += 1
		return label

	def begin_scope(self):
		new_table = table(self.curr_table)
		self.curr_table.children.append(new_table)
		self.curr_table = new_table
		return self.curr_table

	def end_scope(self):
		self.curr_table = self.curr_table.parent

	def insert_variable(self, var_type, identifier):
		self.curr_table.insert_variable(var_type, identifier)

	def insert_temp(self, var_type, identifier):
		self.curr_table.insert_temp(var_type, identifier)

	def insert_array(self, var_type, identifier):
		self.curr_table.insert_array(var_type, identifier)

	def lookup(self, identifier, table):
		if table != None:
			v = table.lookup_in_this(identifier)
			if v == None:
				return self.lookup(identifier, table.parent)
			return v
		else:
			return None

		
	def insert_function(self, method_name, return_type, param_types, param_num):
		self.curr_table.insert_function(method_name, return_type, param_types, param_num)
		
	def lookup_in_this(self, identifier):
		self.curr_table.lookup_in_this(identifier)

	def print_symbol_table(self, t):
		t.print_symbol_table()
		print("----------------")
		for c in t.children:
			self.print_symbol_table(c)
		 





