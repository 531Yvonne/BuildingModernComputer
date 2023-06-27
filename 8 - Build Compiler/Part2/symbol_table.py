# Project 11: Compiler Part 2
#
# Yves Yang
#
# SymbolTable for jack compiler


class SymbolTable:
    def __init__(self, classname=None):
        '''Initialize an empty symbol table'''
        self.table = {}
        self.classname = classname
        self.subroutine_type = None     # constructor | function | method
        self.return_void = None         # whether subroutine returns void
        self.fullname = None            # Classname.subroutineName

    def reset(self):
        '''Reset and get an empty symbol table'''
        self.table = {}
        self.subroutine_type = None
        self.return_void = None
        self.fullname = None

    def add(self, name, type, kind):
        '''
        add new variable to table
        key: name
        value: (type, kind, index)
        '''
        self.table[name] = (type, kind, self.count(kind))

    def count(self, kind):
        '''Get index for current variable by counting records in this kind'''
        count = 0
        for value in self.table.values():
            if value[1] == kind:
                count += 1
        return count

    def type_of(self, name):
        '''Return the type of given name variable'''
        return self.table[name][0]

    def kind_of(self, name):
        '''Return the kind of given name variable'''
        return self.table[name][1]

    def index_of(self, name):
        '''Return the index of given name variable'''
        return self.table[name][2]
