#Remove first and last \n's :
f=open('filename', 'r')
inputstr=f.read()
inputstr=inputstr.strip('\n')

#GET INSTR LIST:
for instr in instrlist:
	if 'ifgoto' in instr:
        labels.append(instr[-1])
		labels.append(str(int(instr[0])+1))



#Make nodes in  control flow graph:
prelabel=1
for l in labels:
	newlist=list(range(prelabel, l))
     	nodes.append(newlist)
     	prelabel=l
nodes=nodes[1:]


tackeywords = ['ifgoto', 'goto', 'ret', 'call', 'print', 'label', 'leq', 'geq', '='] + mathops
newinstr = Instruction(instrlist[i])
#Sample class declaration
class Instruction:
	"""Instruction class"""
	def __init__(self, instr):
		components = instr.split(',')
		number = components[0]
		for keyword in tackeywords:
			if keyword in components:
				mytype = keyword
				break;
