# IMPLEMENTING C SHARP IN PYTHON
# Machine Code Generation Module
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
reglist = ['%eax', '%ebx', '%ecx', '%edx', '%ebp', '%esp', '%esi', '%edi']
# Construct the register descriptor table
registers = {}
registers = registers.fromkeys(reglist)

# Mathematical Operators
mathops = ['+', '-', '*', '/']

# The function to translate a single line tac to x8 assembly
def translate(instruction):
	assembly = ""
	line = instruction[0]
	operator = instruction[1]
	if operator in mathops:
		result = instruction[2]
		operand1 = instruction[3]
		operand2 = instruction[4]
		if operator == '+':
			# Get the register to store the result
			regdest = getReg(result)
			# Get the locations of the operands
			loc1 = location(operand1)
			loc2 = location(operand2)
			# Move the value of the first operand to the destination register
			if loc1 != regdest:
				assembly = assembly + "movl " + loc1 + ", " + regdest + "\n"
			# Perform the addition, the result ill be stored in the register regdest
			assembly = assembly + "addl " + loc2 + ", " + regdest + "\n"
			# Update the register descriptor entry for destreg to say that it contains the result
			registers[destreg] = result
			# Updae the address descriptor entry for result variable to say where it is stored now
			location(result) = destreg
			# If operand1 and operand2 have no further use, then free their respective locations
			if nextuse(operand1) == -1:
				loc = location(operand1)
				if loc != "mem":
					registers[loc] = None
			if nextuse(operand2) == -1:
				loc = location(operand2)
				if loc != "mem":
					registers[loc] = None


# Load the intermediate representation of the program from a file
irfile = open(filename, 'r')
ircode = irfile.read()
ircode = ircode.strip('\n')

# Consruct the instruction list
instrlist = []
instrlist = ircode.split('\n')

# Construct the variable list and the address discriptor table
varlist = []
addressDescriptor = {}
tackeywords = ['ifgoto', 'goto', 'ret', 'call', 'print', 'label', 'leq', 'geq', '='] + mathops
for instr in instrlist:
	templist = instr.split(', ')
	if templist[1] not in ['label', 'call']:
		varlist = varlist + templist 
varlist = list(set(varlist))
varlist = [x for x in varlist if not (x.isdigit() or (x[0] == '-' and x[1:].isdigit()))]
for word in tackeywords:
	if word in varlist:
		varlist.remove(word)
addressDescriptor = addressDescriptor.fromkeys(varlist, "mem")

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

# Generating the x86 Assembly code
#--------------------------------------------------------------------------------------------------
data_section = ".section .data\n"
for var in varlist:
	data_section = data_section + var + ":\n" + ".int 0"

bss_section = ".section .bss\n"
text_section = ".section .text\n" + ".globl _main\n" + "_main:\n"

for node in nodes:
	for n in node:
		text_section = text_section + translate(instrlist[n-1])

exit = "movl $1, %eax\n" + "movl $0, %ebx\n" + "int 0x80"

#--------------------------------------------------------------------------------------------------

print("\n")
# Priniting the final output
print("Assembly Code (x86) for: [" + filename + "]")
print("--------------------------------------------------------------------")
x86c = data_section + bss_section + text_section + exit
print(x86c) 
print("--------------------------------------------------------------------")

# Save the x86 code in a file here as output.s

###################################################################################################
