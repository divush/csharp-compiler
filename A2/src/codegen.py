import sys
#list of registers. Saves work later
reglist=['rax', ' rbx', ' rcx', ' rdx', ' rbp', ' rsp', ' rsi', ' rdi', ' r8', ' r9', ' r10', ' r11', ' r12', ' r13', ' r14', ' r15']
registers.fromkeys(reglist)			#dictionary storing register values.
#symbol table starts out empty.
symboltable=[]