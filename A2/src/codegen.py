# IMPLEMENTING C SHARP IN PYTHON
# Machine Code Generation Module
###################################################################################################

import sys

###################################################################################################

if len(sys.argv) == 2:
	filename = str(sys.argv[1])
else:
	print "usage: python codegen.py irfile"
	exit()

# List of registers
reglist = ['rax','rbx','rcx','rdx','rbp','rsp','rsi','rdi','r8','r9','r10','r11','r12','r13','r14','r15']

# Dictionary that stores the current values in the register
registers = {}
regdict = registers.fromkeys(reglist)

# Load the intermediate representation of the program from a file
irfile = open(filename, 'r')
ircode = irfile.read()
ircode = ircode.strip('\n')

# Construct the basic blocks from ircode
