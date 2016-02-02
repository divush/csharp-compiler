# IMPLEMENTING C SHARP IN PYTHON
# Machine Code Generation Module
###################################################################################################

import sys

###################################################################################################

# Initialization of Data Structures----------------------------------------------------------------

# Get the intermediate code file name
if len(sys.argv) == 2:
	filename = str(sys.argv[1])
else:
	print("usage: python codegen.py irfile")
	exit()

# Define the list of registers
reglist = ['rax', 'rbx', 'rcx', 'rdx', 'rbp', 'rsp', 'rsi', 'rdi', 'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r14', 'r15']

# Construct the register descriptor table
registers = {}
regdict = registers.fromkeys(reglist)

# Opcodes
mathops = ['+', '-', '*', '/']

# Function definitions ----------------------------------------------------------------------------

# getreg: returns a register which is currently empty
def getreg():
	# Check the current instruction to see if a register is going to be freed

	# Otherwise return an empty register (if available)

	# Otherwise free a register by splitting live range (heuristic algorithm) of a variable

	# Otherwise return None so that memory is allocated instead of a register
	return None

# translate: returns the x86 assembly code for a three address code
def translate(tac):
	# tac is the string containing the one line three address code
	x86c = None
	line = tac[0]
	operator = tac[1]
	
	if operator in mathops:
		result = tac[2]
		operand1 = tac[3]
		operand2 = tac[4]
		# Construct the x86 code here


	elif operator == '=':
		pass
	elif operator == 'ifgoto':
		pass
	elif operator == 'goto':
		pass

	return x86c

###################################################################################################

# Load the intermediate representation of the program from a file
irfile = open(filename, 'r')
ircode = irfile.read()
ircode = ircode.strip('\n')

# Consruct the instruction list
instrlist = []
instrlist = ircode.split('\n')

# Get the leaders
leaders = [1,]
for instr in instrlist:
	temp = instr.split(', ')
	if 'ifgoto' in instr:
		# print("In instr : "+ instr)
		leaders.append(int(temp[-1]))
		# print("Appended "+temp[-1])
		leaders.append(int(temp[0])+1)
		# print("Appended "+str(int(temp[0])+1))
	elif 'goto' in instr:
		# print("In instr : "+ instr)
		leaders.append(int(temp[-1]))
		# print("Appended "+temp[-1])
		leaders.append(int(temp[0])+1)
		# print("Appended "+str(int(temp[0])+1))
leaders = list(set(leaders))
leaders.sort()
# print("leaders = "+ str(leaders))

# Constructing the Basic Blocks as nodes
nodes = []
i = 0
while i < len(leaders)-1:
	nodes.append(list(range(leaders[i],leaders[i+1])))
	i = i + 1
nodes.append(list(range(leaders[i],len(instrlist)+1)))

# X86 ASEMBLY CODE GENERATION BEGINS HERE
#--------------------------------------------------------------------------------------------------
# Generate the data section (if required) of the assembly program
print(".section .data\n")

# Generate the bss section (if required) of the assembly program
print(".section .bss\n")

# Generate the text section (if required) of the assembly program
print(".section .text\n")
for node in nodes:
	for n in node:
		print(translate(instrlist[n-1].split(', ')))

# Generate the assembly code to cleanly exit the program
print("movl $1, %eax")
print("movl $0, %ebx")
print("int 0x80")

#--------------------------------------------------------------------------------------------------