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
	print("usage: python codegen.py irfile")
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
instrlist=[]
instrlist=ircode.split('\n')

#Get instr list
leaders=[]
for instr in instrlist:
	if 'ifgoto' in instr:
		temp=instr.split(',')
		print("In instr : "+ instr)
		leaders.append(temp[-1])
		print("Appended "+temp[-1])
		leaders.append(str(int(temp[0])+1))
		print("Appended "+str(int(temp[0])+1))
	if 'goto' in instr and 'ifgoto' not in instr:
		temp=instr.split(',')
		print("In instr : "+ instr)
		leaders.append(temp[-1])
		print("Appended "+temp[-1])
		leaders.append(str(int(temp[0])+1))
		print("Appended "+str(int(temp[0])+1))

flag=0
if str(len(instrlist)) not in leaders:
	flag=1
	leaders.append(str(len(instrlist)))
#converting to integer.
for x in range(0, len(leaders)):
	leaders[x]=int(leaders[x])	

leaders = list(set(leaders))
leaders.sort()
print("leaders = "+ str(leaders))

#nodes of the control flow graph
preleader=1
nodes=[]
for l in leaders:
	newlist=list(range(preleader, l))
	print(str(preleader))
	nodes.append(newlist)
	preleader=l

if flag==1:
	nodes[-1].append(len(instrlist))
else:
	nodes.append([len(instrlist)])

print(nodes)
validleaders=list(range(1,len(instrlist)+1))
#adding edges in CFG. Adjacency list form..
adjlist=[]
for x in nodes:
	newlist=[]
	newlist.append(x)
	adjlist.append(newlist)