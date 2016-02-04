#!/usr/bin/python3
# Assembly code generator: TAC to x86 (AT&T) Assembly
###################################################################################################

import sys 

###################################################################################################

# Get the intermediate code file name
if len(sys.argv) == 2:
	filename = str(sys.argv[1])
else:
	print("usage: python codegen.py irfile")
	exit()

# Define the list of registers
reglist = ['%eax', '%ebx', '%ecx', '%edx']
# Construct the register descriptor table
registers = {}
registers = registers.fromkeys(reglist)

# Mathematical Operators
mathops = ['+', '-', '*', '/']

# Variable 
varlist = []
addressDescriptor = {}

assembly = ""

# Three address code keywords
tackeywords = ['ifgoto', 'goto', 'return', 'call', 'print', 'label', '<=', '>=', '==', '>', '<', '!=', '=', 'function', 'exit'] + mathops

###################################################################################################

# Sets the register descriptor entry as per the arguments
def setregister(register, content):
	registers[register] = content

# getreg function... return register for the variable. spilling implemented here.
def getReg(variable, instrno):
	#instrno is the line number!
	if variable in registers.values():
		for x in registers.keys():
			if registers[x] == variable:
				return x
	for x in registers.keys():
		if registers[x] == None:
			return x
	instrvardict = nextuseTable[instrno - 1]
	farthestnextuse = max(instrvardict.keys())
	for var in instrvardict:
		if instrvardict[var] == farthestnextuse:
			break;
	#var is variable to be spilled!
	for regspill in registers.keys():
		if registers[regspill] == var:
			break;
	#regspill contais register to be spilled!!
	assembly = assembly + "movl " + regspill + ", " + var + "\n"
	return regspill

# Returns the location of the variable from the addrss descriptor table
def getlocation(variable):
	return addressDescriptor[variable]

# Sets the location entry in the adrdrss decriptor for a variable 
def setlocation(variable, location):
	addressDescriptor[variable] = location

# Returns the nextuse of the variable
def nextuse(variable, line):
	return nextuseTable[line-1][variable]

# The function to translate a single line tac to x86 assembly
def translate(instruction):
	assembly = ""
	line = int(instruction[0])
	operator = instruction[1]
	# Generating assembly code if the tac is a mathematical operation
	if operator in mathops:
		result = instruction[2]
		operand1 = instruction[3]
		operand2 = instruction[4]
		# Addition
		if operator == '+':
			if not operand1.isdigit() and not operand2.isdigit():
				# Get the register to store the result
				regdest = getReg(result, line)
				# Get the locations of the operands
				loc1 = getlocation(operand1)
				loc2 = getlocation(operand2)
				# Move the value of the first operand to the destination register
				if loc1 != regdest:
					assembly = assembly + "movl " + loc1 + ", " + regdest + "\n"
				# Perform the addition, the result will be stored in the register regdest
				assembly = assembly + "addl " + loc2 + ", " + regdest + "\n"
				# Update the register descriptor entry for regdest to say that it contains the result
				setregister(regdest, result)
				# Update the address descriptor entry for result variable to say where it is stored now
				setlocation(result, regdest)
				# If operand1 and operand2 have no further use, then free their registers
				if nextuse(operand1, line) == -1:
					if loc1 != "mem":
						setregister(loc1, None)
						assembly = assembly + "movl " + regdest + ", " + operand1 + "\n"
						setlocation(operand1, "mem")
				if nextuse(operand2, line) == -1:
					if loc2 != "mem":
						setregister(loc2, None)
						assembly = assembly + "movl " + regdest + ", " + operand2 + "\n"
						setlocation(operand2, "mem")
			elif operand1.isdigit() and not operand2.isdigit():
				# Get the register to store the result
				regdest = getReg(result, line)
				loc2 = getlocation(operand2)
				# Move the first operand to the destination register
				assembly = assembly + "movl $" + operand1 + ", " + regdest + "\n"
				# Add the other operand to the register content
				assembly = assembly + "addl " + loc2 + ", " + regdest + "\n"
				setregister(regdest, result)
				setlocation(result, regdest)
				if nextuse(operand2, line) == -1:
					if loc2 != "mem":
						setregister(loc2, None)
						assembly = assembly + "movl " + regdest + ", " + operand2 + "\n"
						setlocation(operand2, "mem")
			elif not operand1.isdigit() and operand2.isdigit():
				# Get the register to store the result
				regdest = getReg(result, line)
				loc1 = getlocation(operand2)
				# Move the first operand to the destination register
				assembly = assembly + "movl $" + operand2 + ", " + regdest + "\n"
				# Add the other operand to the register content
				assembly = assembly + "addl " + loc1 + ", " + regdest + "\n"
				setregister(regdest, result)
				setlocation(result, regdest)
				if nextuse(operand1, line) == -1:
					if loc1 != "mem":
						setregister(loc1, None)
						assembly = assembly + "movl " + regdest + ", " + operand1 + "\n"
						setlocation(operand1, "mem")
			elif operand1.isdigit() and operand2.isdigit():
				# Get the register to store the result
				regdest = getReg(result, line)
				assembly = assembly + "movl $" + str(int(operand1)+int(operand2)) + ", " + regdest + "\n"
				# Update the address descriptor entry for result variable to say where it is stored no
				setregister(regdest, result)
				setlocation(result, regdest)	
		# Subtraction
		elif operator == '-':
			pass
		# Multiplication
		elif operator == '*':
			pass
		# Division
		elif operator == '/':
			pass

	# Generating assembly code if the tac is a functin call
	elif operator == "call":
		label = instruction[2]
		assembly = assembly + "call " + label + "\n"

	# Generating assembly code if the tac is a label for a new leader
	elif operator == "label":
		label = instruction[2]
		assembly = assembly + label + ": \n"

	# Generating assembly code if the tac is an ifgoto statement
	elif operator == "ifgoto":
		operator = instruction[2]
		operand1 = instruction[3]
		operand2 = instruction[4]
		# Translation for diffrent conditional operators
		if operator == "<=":
			pass
		elif operator == ">=":
			pass
		elif operator == "==":
			pass
		elif operator == "<":
			pass
		elif operator == ">":
			pass
		elif operator == "!=":
			pass


	# Generating assembly code if the tac is a goto statement
	elif operator == "goto":
		label = instruction[2]
		if label.isdigit():
			assembly = assembly + "jmp L" + label + "\n"
		else:
			assembly = assembly + "jmp " + label + "\n" 

	# Generating assembly code if the tac is a return statement
	elif operator == "exit":
		assembly = assembly + "call exit\n"

	# Generating assembly code if the tac is a print
	elif operator == "print":
		operand = instruction[2]
		if not operand.isdigit():
			loc = getlocation(operand)
			if not loc == "mem":
				assembly = assembly + "pushl " + loc + "\n"
				assembly = assembly + "pushl $str\n"
				assembly = assembly + "call printf\n"
			else:
				assembly = assembly + "pushl " + operand + "\n"
				assembly = assembly + "pushl $str\n"
				assembly = assembly + "call printf\n"
		else:
			assembly = assembly + "pushl $" + operand + "\n"
			assembly = assembly + "pushl $str\n"
			assembly = assembly + "call printf\n"			

	# Generating code for assignment operations
	elif operator == '=':
		destination = instruction[2]
		source = instruction[3]
		loc1 = getlocation(destination)
		# If the source is a literal then we can just move it to the destination
		if source.isdigit():
			assembly = assembly + "movl $" + source + ", " + loc1
		# If both the source and the destination reside in the memory
		elif loc1 == "mem":
			loc2 = getlocation(source)
			regdest = getReg(destination)
			assembly = assembly + "movl " + source + ", " + regdest
			# Update the address descriptor entry for result variable to say where it is stored no
			setregister(regdest, destination)
			setlocation(destination, regdest)			
		# If one of the locations is a register	
		else:
			assembly = assembly + "movl " + loc2 + ", " + loc1 

	# Generating the prelude for a function definition
	elif operator == "function":
		function_name = instruction[2]
		assembly = assembly + ".globl " + function_name + "\n"
		assembly = assembly + ".type "  + function_name + ", @function\n"
		assembly = assembly + function_name + ":\n"
		assembly = assembly + "pushl %ebp\n"
		assembly = assembly + "movl %esp, %ebp\n"
		
	# Generating the conclude of the function
	elif operator == "return":
		assembly = assembly + "movl %ebp, %esp\n"
		assembly = assembly + "popl %ebp\n"
		assembly = assembly + "ret\n"

	# Return the assembly code
	return assembly

###################################################################################################

# Load the intermediate representation of the program from a file
irfile = open(filename, 'r')
ircode = irfile.read()
ircode = ircode.strip('\n')

# Consruct the instruction list
instrlist = []
instrlist = ircode.split('\n')

nextuseTable = [None for i in range(len(instrlist))]

# Construct the variable list and the address discriptor table
for instr in instrlist:
	templist = instr.split(', ')
	if templist[1] not in ['label', 'call', 'function']:
		varlist = varlist + templist 
varlist = list(set(varlist))
varlist = [x for x in varlist if not (x.isdigit() or (x[0] == '-' and x[1:].isdigit()))]
for word in tackeywords:
	if word in varlist:
		varlist.remove(word)
addressDescriptor = addressDescriptor.fromkeys(varlist, "mem")
symbolTable = addressDescriptor.fromkeys(varlist, ["live", None])

# Get the leaders
leaders = [1,]
for i in range(len(instrlist)):
	instrlist[i] = instrlist[i].split(', ')
	if 'ifgoto' in instrlist[i]:
		leaders.append(int(instrlist[i][-1]))
		leaders.append(int(instrlist[i][0])+1)
	elif 'goto' in instrlist[i]:
		leaders.append(int(instrlist[i][-1]))
		leaders.append(int(instrlist[i][0])+1)
	elif 'function' in instrlist[i]:
		leaders.append(int(instrlist[i][0]))
	elif 'label' in instrlist[i]:
		leaders.append(int(instrlist[i][0]))
leaders = list(set(leaders))
leaders.sort()

# Constructing the Basic Blocks as nodes
nodes = []
i = 0
while i < len(leaders)-1:
	nodes.append(list(range(leaders[i],leaders[i+1])))
	i = i + 1
nodes.append(list(range(leaders[i],len(instrlist)+1)))

# Constructing the next use table
for node in nodes:
	revlist=node.copy()
	revlist.reverse()
	for instrnumber in revlist:
		# Get the current instruction and the operator and the operands
		instr = instrlist[instrnumber - 1]
		operator = instr[1]
		# Get the variable names in the current istruction
		variables = [x for x in instr if x in varlist]
		# Set the next use values here
		nextuseTable[instrnumber-1] = {var:symbolTable[var] for var in variables}
		# Rule for mathematical operations
		if operator in mathops:
			z = instr[2]
			x = instr[3]
			y = instr[4]
			if z in variables:
				symbolTable[z] = ["dead", None]
			if x in variables:
				symbolTable[x] = ["live", instrnumber]
			if y in variables:
				symbolTable[y] = ["live", instrnumber]
		elif operator == "ifgoto":
			x = instr[3]
			y = instr[4]
			if x in variables:
				symbolTable[x] = ["live", instrnumber]
			if y in variables:
				symbolTable[y] = ["live", instrnumber]
		elif operator == "print":
			x = instr[2]
			if x in variables:
				symbolTable[x] = ["live", instrnumber]			
		elif operator == "=":
			x = instr[2]
			y = instr[3]
			if x in variables:
				symbolTable[x] = ["dead", None]
			if y in variables:
				symbolTable[y] = ["live", instrnumber]					

		i = i - 1

# Generating the x86 Assembly code
#--------------------------------------------------------------------------------------------------
data_section = ".section .data\n"
for var in varlist:
	data_section = data_section + var + ":\n" + ".int 0\n"
data_section = data_section + "str:\n.ascii \"%d\\n\\0\"\n"

bss_section = ".section .bss\n"
text_section = ".section .text\n" + ".globl main\n" + "main:\n"

for node in nodes:
	for n in node:
		text_section = text_section + "L" + str(n) + ":\n"
		text_section = text_section + translate(instrlist[n-1])

#--------------------------------------------------------------------------------------------------

print("\n")
# Priniting the final output
print("Assembly Code (x86) for: [" + filename + "]")
print("--------------------------------------------------------------------")
x86c = data_section + bss_section + text_section
print(x86c) 
print("--------------------------------------------------------------------")

# Save the x86 code in a file here as output.s

###################################################################################################
