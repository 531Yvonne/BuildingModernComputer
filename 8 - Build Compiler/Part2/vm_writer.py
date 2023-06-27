# Project 11: Compiler Part 2
#
# Yves Yang
#
# VM Writer


class VMWriter:
    '''
    Represent a writer tool which writes vm codes based on jack code
    '''
    arithmetic_table = {"+": "add", "-": "sub", "&": "and", "|": "or",
                        ">": "gt", "<": "lt", "=": "eq", "~": "not",
                        "*": "call Math.multiply 2",
                        "/": "call Math.divide 2"}

    def __init__(self):
        self.vm_codes = []

    def writePush(self, segment, index):
        '''Write a VM push command line to current list of VM codes'''
        self.vm_codes.append(f"push {segment} {str(index)}")

    def writePop(self, segment, index):
        '''Write a VM pop command line to current list of VM codes'''
        self.vm_codes.append(f"pop {segment} {str(index)}")

    def writeArithmetic(self, command):
        '''Write a VM arithmetic/logical command line to list of VM codes'''
        self.vm_codes.append(command)

    def writeLabel(self, label):
        '''Write a VM label command'''
        self.vm_codes.append(f"label {label}")

    def writeGoto(self, label):
        '''Write a VM goto command'''
        self.vm_codes.append(f"goto {label}")

    def writeIfgoto(self, label):
        '''Write a VM if-goto command'''
        self.vm_codes.append(f"if-goto {label}")

    def writeCall(self, name, n_args):
        '''Write a VM call command'''
        self.vm_codes.append(f"call {name} {str(n_args)}")

    def writeFunction(self, name, n_vars):
        '''Write a VM function command'''
        self.vm_codes.append(f"function {name} {str(n_vars)}")

    def writeReturn(self):
        '''Write a VM self.vm_codes.append(command'''
        self.vm_codes.append("return")
