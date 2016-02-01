# IMPLEMENTING C SHARP IN PYTHON
# Machine Code Generation Module
###################################################################################################

import sys

###################################################################################################

# Function definitions ----------------------------------------------------------------------------

# getreg: returns a register which is currently empty
def getreg():
	# Check the current instruction to see if a register is going to be freed

	# Otherwise return an empty register (if available)

	# Otherwise free a register by splitting live range (heuristic algorithm) of a variable

	# Otherwise return None so that memory is allocated instead of a register
	return None



#--------------------------------------------------------------------------------------------------

# Get the intermediate code file name
if len(sys.argv) == 2:
	filename = str(sys.argv[1])
else:
	print "usage: python codegen.py irfile"
	exit()

# Define the list of registers
reglist = ['rax','rbx','rcx','rdx','rbp','rsp','rsi','rdi','r8','r9','r10','r11','r12','r13','r14','r15']

# Construct the register descriptor table
registers = {}
regdict = registers.fromkeys(reglist)

# Load the intermediate representation of the program from a file
irfile = open(filename, 'r')
ircode = irfile.read()
ircode = ircode.strip('\n')

# Construct the basic blocks from ircode
