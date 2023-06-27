# Project 11: Compiler Part 2
#
# Yves Yang
#
# This source code contains the Engine to write vm codes based on tokens.
from symbol_table import SymbolTable
from vm_writer import VMWriter


class CompileEngine:
    op = ["+", "-", "*", "/", "&", "|", "<", ">", "="]

    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 1  # Ignore tokens[0]: "<tokens>", start from tokens[1].
        self.vm_writer = VMWriter()
        # Get classname from 2nd line <identifier> xxx </identifier>.
        self.classname = self.tokens[self.index+1][13:-14]
        # Below properties used to track label occurrences for unique label id.
        self.label_count = 0
        # Initiate the Compiling process from compileClass().
        self.compileClass()

    def compileClass(self):
        '''
        Compile a complete class
        Structure: class className { classVarDec* subroutineDec* }
        '''
        # Initialize symbol table for identifiers.
        class_table = SymbolTable()
        subroutine_table = SymbolTable()

        self.index += 3     # Jump 3 lines of token: class className {
        while ("<keyword> static" in self.tokens[self.index] or
                "<keyword> field" in self.tokens[self.index]):
            # Compile classVarDec zero or more times
            self.compileClassVarDec(class_table)

        while ("<keyword> constructor" in self.tokens[self.index] or
                "<keyword> function" in self.tokens[self.index] or
                "<keyword> method" in self.tokens[self.index]):
            # Compile subroutineDec zero or more times
            self.compileSubroutineDec(class_table,
                                      subroutine_table)
        return

    def compileClassVarDec(self, class_table):
        '''
        Compile a static or field declaration
        Structure: (static | field) type varName (, varName)* ;
        '''
        # Get kind for symbol table.
        if "<keyword> static" in self.tokens[self.index]:
            kind = "static"
        else:
            kind = "this"
        # Get type for symbol table.
        if "<keyword>" in self.tokens[self.index+1]:
            # Get type from <keyword> xxx </keyword>.
            type = self.tokens[self.index+1][10:-11]
        else:
            # Get type from <identifier> xxx </identifier>.
            type = self.tokens[self.index+1][13:-14]

        # Get name for symbol table from <identifier> xxx </identifier>.
        name = self.tokens[self.index+2][13:-14]
        # Add name, type, kind record to symbol table.
        class_table.add(name, type, kind)

        # Jump 3 lines of token: (static | field) type varName
        self.index += 3     # Move pointer
        while ";" not in self.tokens[self.index]:
            # Declaration not end, contains extra (, varName)
            # Get name for symbol table from <identifier> xxx </identifier>.
            name = self.tokens[self.index+1][13:-14]
            # Add name, type, kind record to symbol table.
            class_table.add(name, type, kind)
            # Jump 2 token lines: , varName
            self.index += 2
        self.index += 1     # Jump ; token line
        return

    def compileSubroutineDec(self, class_table, subroutine_table):
        '''
        Compile a complete method, function or constructor
        Structure: (constructor | function | method) (void | type)
                    subroutineName ( parameterList ) subroutineBody
        '''
        # Reset symbol table for each Subroutine.
        subroutine_table.reset()

        # Get subroutine type: constructor | function | method
        # from <keyword> xxx </keyword>.
        subroutine_table.subroutine_type = self.tokens[self.index][10:-11]

        # Get whether return type is void or other type
        if self.tokens[self.index+1] == "<keyword> void </keyword>":
            subroutine_table.return_void = True
        else:
            subroutine_table.return_void = False

        # Get subroutine name from <identifier> subroutineName </identifier>.
        subroutine_name = self.tokens[self.index+2][13:-14]
        subroutine_table.fullname = f"{self.classname}.{subroutine_name}"

        # Add "this" as argument 0 when it's a method.
        if subroutine_table.subroutine_type == "method":
            subroutine_table.add("this", self.classname, "argument")

        # Jump 4 lines of token: (constructor | function | method),
        # (void | type), subroutineName and (
        self.index += 4
        self.compileParameterList(class_table, subroutine_table)
        self.index += 1     # Jump ) token line
        self.compileSubroutineBody(class_table, subroutine_table)
        return

    def compileParameterList(self, class_table, subroutine_table):
        '''
        Compile a parameter list
        Structure: ((type varName) (, type varName)*)?
        '''
        if ("int" in self.tokens[self.index] or
            "char" in self.tokens[self.index] or
            "boolean" in self.tokens[self.index] or
                "<identifier>" in self.tokens[self.index]):
            # at least 1 parameter exist.

            # Get type for symbol table.
            if "<keyword>" in self.tokens[self.index]:
                # Get type from <keyword> xxx </keyword>.
                type = self.tokens[self.index][10:-11]
            else:
                # Get type from <identifier> xxx </identifier>.
                type = self.tokens[self.index][13:-14]
            # Get name for symbol table from <identifier> xxx </identifier>.
            name = self.tokens[self.index+1][13:-14]
            # Add name, type, kind record to symbol table.
            subroutine_table.add(name, type, "argument")

            # Jump 2 token lines: type varName.
            self.index += 2
            while "<symbol> )" not in self.tokens[self.index]:
                # parameters list not done: next 3 tokens: , type varName
                # Get type for symbol table.
                if "<keyword>" in self.tokens[self.index+1]:
                    # Get type from <keyword> xxx </keyword>.
                    type = self.tokens[self.index+1][10:-11]
                else:
                    # Get type from <identifier> xxx </identifier>.
                    type = self.tokens[self.index+1][13:-14]
                # Get name for symbol table from <identifier> xxx </identifier>
                name = self.tokens[self.index+2][13:-14]
                # Add name, type, kind record to symbol table.
                subroutine_table.add(name, type, "argument")
                # Jump 3 tokens: , type varName
                self.index += 3
        return

    def compileSubroutineBody(self, class_table, subroutine_table):
        ''' Compile a subroutine's body, Structure: { varDec* statements }'''
        self.index += 1     # Jump { token line
        while "<keyword> var" in self.tokens[self.index]:
            # Compile varDec zero or more times
            self.compileVarDec(subroutine_table)

        self.vm_writer.writeFunction(subroutine_table.fullname,
                                     subroutine_table.count("local"))
        if subroutine_table.subroutine_type == "constructor":
            self.vm_writer.writePush("constant",
                                     class_table.count("this"))
            self.vm_writer.writeCall("Memory.alloc", 1)
            self.vm_writer.writePop("pointer", 0)
        elif subroutine_table.subroutine_type == "method":
            self.vm_writer.writePush("argument", 0)
            self.vm_writer.writePop("pointer", 0)

        self.compileStatements(class_table, subroutine_table)
        self.index += 1     # Jump } token line
        return

    def compileVarDec(self, subroutine_table):
        '''
        Compile a var declaration
        Structure: var type varName (, type varName)* ;
        '''
        # Get type for symbol table.
        if "<keyword>" in self.tokens[self.index+1]:
            # Get type from <keyword> xxx </keyword>.
            type = self.tokens[self.index+1][10:-11]
        else:
            # Get type from <identifier> xxx </identifier>.
            type = self.tokens[self.index+1][13:-14]
        # Get name for symbol table from <identifier> xxx </identifier>.
        name = self.tokens[self.index+2][13:-14]
        # Add name, type, kind record to symbol table.
        subroutine_table.add(name, type, "local")

        self.index += 3     # Jump 3 token lines: var type varName
        while "<symbol> ;" not in self.tokens[self.index]:
            # Declaration not finished, has extra variables: , varName
            # Get name for symbol table from <identifier> xxx </identifier>.
            name = self.tokens[self.index+1][13:-14]
            # Add name, type, kind record to symbol table.
            subroutine_table.add(name, type, "local")
            self.index += 2     # Jump 2 token lines: , varName
        self.index += 1     # Jump ; token line
        return

    def compileStatements(self, class_table, subroutine_table):
        ''' Compile a sequence of statements '''
        while (self.tokens[self.index] == "<keyword> let </keyword>" or
                self.tokens[self.index] == "<keyword> if </keyword>" or
                self.tokens[self.index] == "<keyword> while </keyword>" or
                self.tokens[self.index] == "<keyword> do </keyword>" or
                self.tokens[self.index] == "<keyword> return </keyword>"):
            if self.tokens[self.index] == "<keyword> let </keyword>":
                self.compileLet(class_table, subroutine_table)
            elif self.tokens[self.index] == "<keyword> if </keyword>":
                self.compileIf(class_table, subroutine_table)
            elif self.tokens[self.index] == "<keyword> while </keyword>":
                self.compileWhile(class_table, subroutine_table)
            elif self.tokens[self.index] == "<keyword> do </keyword>":
                self.compileDo(class_table, subroutine_table)
            elif self.tokens[self.index] == "<keyword> return </keyword>":
                self.compileReturn(class_table, subroutine_table)
        return

    def compileLet(self, class_table, subroutine_table):
        '''
        Compile a let statement
        Structure: let varName ([ expression ])? = expression ;
        '''
        # Get varName from <identifier> xxx </identifier>.
        varName = self.tokens[self.index+1][13:-14]
        var_in_sub_table = False
        if varName in subroutine_table.table:
            var_in_sub_table = True
        self.index += 2     # Jump 2 token lines: let varName
        array_handling = False
        if "<symbol> [" in self.tokens[self.index]:
            array_handling = True
            # [ expression ] exists
            if var_in_sub_table:
                self.vm_writer.writePush(subroutine_table.kind_of(varName),
                                         subroutine_table.index_of(varName))
            else:
                self.vm_writer.writePush(class_table.kind_of(varName),
                                         class_table.index_of(varName))
            self.index += 1     # Jump [ token line
            self.compileExpression(class_table, subroutine_table)
            self.vm_writer.writeArithmetic("add")
            self.index += 1     # Jump ] token line
        self.index += 1     # Jump = token line
        self.compileExpression(class_table, subroutine_table)
        if array_handling:
            self.vm_writer.writePop("temp", 0)
            self.vm_writer.writePop("pointer", 1)
            self.vm_writer.writePush("temp", 0)
            self.vm_writer.writePop("that", 0)
        else:
            # No array involved ---- line is: let varName = expression;
            if var_in_sub_table:
                self.vm_writer.writePop(subroutine_table.kind_of(varName),
                                        subroutine_table.index_of(varName))
            else:
                self.vm_writer.writePop(class_table.kind_of(varName),
                                        class_table.index_of(varName))
        self.index += 1     # Jump ; token line
        return

    def compileIf(self, class_table, subroutine_table):
        '''
        Compile an if statement
        Structure: if ( expression ) { statements } (else { statements })?
        '''
        self.index += 2     # Jump 2 token lines: if (
        self.compileExpression(class_table, subroutine_table)
        self.vm_writer.writeArithmetic("not")
        if_true_label = "L" + str(self.label_count)
        if_false_label = "L" + str(self.label_count+1)
        self.label_count += 2
        self.vm_writer.writeIfgoto(if_false_label)
        self.index += 2     # Jump ) { token line
        self.compileStatements(class_table, subroutine_table)
        self.vm_writer.writeGoto(if_true_label)
        self.vm_writer.writeLabel(if_false_label)
        self.index += 1     # Jump } token line
        if "<keyword> else" in self.tokens[self.index]:
            # else statement exists
            self.index += 2     # Jump 2 token lines: else {
            self.compileStatements(class_table, subroutine_table)
            self.index += 1     # Jump 1 token line: ;
        self.vm_writer.writeLabel(if_true_label)
        return

    def compileWhile(self, class_table, subroutine_table):
        '''
        Compile a while statement
        Structure: while ( expression ) { statements }
        '''
        exp_label = "L" + str(self.label_count)
        end_label = "L" + str(self.label_count+1)
        self.label_count += 2
        self.vm_writer.writeLabel(exp_label)
        self.index += 2     # Jump while ( tokens
        self.compileExpression(class_table, subroutine_table)
        self.vm_writer.writeArithmetic("not")
        self.vm_writer.writeIfgoto(end_label)
        self.index += 2     # Jump ) { token line
        self.compileStatements(class_table, subroutine_table)
        self.vm_writer.writeGoto(exp_label)
        self.index += 1     # Jump } token line
        self.vm_writer.writeLabel(end_label)
        return

    def compileDo(self, class_table, subroutine_table):
        '''
        Compile a do statement
        Structure: do subroutineCall ;
        '''
        self.index += 1     # Jump 1 token line: do
        self.compileSubroutineCall(class_table, subroutine_table)
        self.index += 1     # Jump 1 token line: ;
        # After return from the subroutine, VM should have pop temp 0.
        self.vm_writer.writePop("temp", 0)
        return

    def compileReturn(self, class_table, subroutine_table):
        ''' Compile a return statement, Structure: return expression? ;'''
        self.index += 1     # Jump 1 token line: return
        if self.tokens[self.index] != "<symbol> ; </symbol>":
            self.compileExpression(class_table, subroutine_table)
        else:
            # return statement contains only return;
            self.vm_writer.writePush("constant", 0)
        self.vm_writer.writeReturn()
        self.index += 1     # Jump 1 token line: ;
        return

    def compileExpression(self, class_table, subroutine_table):
        ''' Compile an expression. Structure: term (op term)* '''
        self.compileTerm(class_table, subroutine_table)
        while ("<symbol>" in self.tokens[self.index] and
               self.tokens[self.index][9] in self.op):
            # Check whether next token is <symbol> op </symbol>
            op = self.tokens[self.index][9]
            command = self.vm_writer.arithmetic_table[op]
            self.index += 1     # Jump op token line
            self.compileTerm(class_table, subroutine_table)
            self.vm_writer.writeArithmetic(command)
        return

    def compileTerm(self, class_table, subroutine_table):
        ''' Compile a term '''
        if "<integerConstant>" in self.tokens[self.index]:
            # term is an intergerConstant
            number = int(self.tokens[self.index][18:-19])
            self.vm_writer.writePush("constant", number)
            self.index += 1     # Jump term token
        elif "<stringConstant>" in self.tokens[self.index]:
            # term is a stringConstant
            text = self.tokens[self.index][17:-18]
            self.vm_writer.writePush("constant", len(text))
            self.vm_writer.writeCall("String.new", 1)
            for i in range(len(text)):
                self.vm_writer.writePush("constant", ord(text[i]))
                self.vm_writer.writeCall("String.appendChar", 2)
            self.index += 1     # Move pointer
        elif "<keyword>" in self.tokens[self.index]:
            # term is keywordConstant
            if self.tokens[self.index][10:14] == "true":
                self.vm_writer.writePush("constant", 0)
                self.vm_writer.writeArithmetic("not")
            elif self.tokens[self.index][10:14] == "this":
                self.vm_writer.writePush("pointer", 0)
            elif (self.tokens[self.index][10:15] == "false" or
                  self.tokens[self.index][10:14] == "null"):
                self.vm_writer.writePush("constant", 0)
            self.index += 1     # Move pointer
        elif ("<symbol> -" in self.tokens[self.index]
              or "<symbol> ~" in self.tokens[self.index]):
            # line is unaryOp term
            unaryOp = self.tokens[self.index][9]
            self.index += 1     # Jump unaryOp line
            self.compileTerm(class_table, subroutine_table)
            if unaryOp == "-":
                self.vm_writer.writeArithmetic("neg")
            elif unaryOp == "~":
                self.vm_writer.writeArithmetic("not")
        elif "<symbol> (" in self.tokens[self.index]:
            # term is ( expression )
            self.index += 1     # Jump ( token line
            self.compileExpression(class_table, subroutine_table)
            self.index += 1     # Jump ) token line
        elif "<identifier>" in self.tokens[self.index]:
            # Term can be varName | varName[expression] | subroutineCall
            if (self.tokens[self.index+1] != "<symbol> ( </symbol>"
                    and self.tokens[self.index+1] != "<symbol> . </symbol>"):
                # Term can be varName | varName[expression]
                # Get varName from <identifier> xxx </identifier>.
                varName = self.tokens[self.index][13:-14]
                var_in_sub_table = False
                if varName in subroutine_table.table:
                    var_in_sub_table = True
                if self.tokens[self.index+1] == "<symbol> [ </symbol>":
                    # Term is varName[expression]
                    if var_in_sub_table:
                        self.vm_writer.writePush(subroutine_table.kind_of(varName),
                                                 subroutine_table.index_of(varName))
                    else:
                        self.vm_writer.writePush(class_table.kind_of(varName),
                                                 class_table.index_of(varName))
                    self.index += 2     # Jump 2 token lines: varName [
                    self.compileExpression(class_table, subroutine_table)
                    self.vm_writer.writeArithmetic("add")
                    self.vm_writer.writePop("pointer", 1)
                    self.vm_writer.writePush("that", 0)
                    self.index += 1     # Jump ] token line

                else:
                    # Term is varName
                    if var_in_sub_table:
                        self.vm_writer.writePush(subroutine_table.kind_of(varName),
                                                 subroutine_table.index_of(varName))
                    else:
                        self.vm_writer.writePush(class_table.kind_of(varName),
                                                 class_table.index_of(varName))
                    self.index += 1     # Jump varName line
            else:
                # Term is subroutineCall
                self.compileSubroutineCall(class_table, subroutine_table)
        return

    def compileSubroutineCall(self, class_table, subroutine_table):
        ''' Compile a subroutine call '''
        if self.tokens[self.index+1] == "<symbol> ( </symbol>":
            # Structure: subroutineName ( expressionList )
            # Get subroutineName from <identifier> xxx </identifier>.
            subroutineName = self.tokens[self.index][13:-14]
            self.vm_writer.writePush("pointer", 0)
            self.index += 2     # Jump 2 token lines: subroutineName (
            nArgs = self.compileExpressionList(class_table, subroutine_table) + 1
            self.index += 1     # Jump ) token line
            self.vm_writer.writeCall(self.classname + "." + subroutineName,
                                     nArgs)
        else:
            # Structure: className|varName . subroutineName ( expressionList )
            # Get className|varName from <identifier> xxx </identifier>.
            class_or_varName = self.tokens[self.index][13:-14]
            nArgs = 0
            is_varname = False
            var_in_sub_table = False
            if class_or_varName in subroutine_table.table:
                is_varname = True
                var_in_sub_table = True
            elif class_or_varName in class_table.table:
                is_varname = True
            # Get subroutineName from <identifier> xxx </identifier>.
            subroutineName = self.tokens[self.index+2][13:-14]
            if is_varname:
                # Line is varName.subroutineName(expression list)
                nArgs += 1
                if var_in_sub_table:
                    self.vm_writer.writePush(subroutine_table.kind_of(class_or_varName),
                                             subroutine_table.index_of(class_or_varName))
                    fullname = subroutine_table.type_of(class_or_varName) + "." + subroutineName
                else:
                    self.vm_writer.writePush(class_table.kind_of(class_or_varName),
                                             class_table.index_of(class_or_varName))
                    fullname = class_table.type_of(class_or_varName) + "." + subroutineName
            else:
                # Line is className.subroutineName(expression list)
                fullname = class_or_varName + "." + subroutineName
            # Jump 4 token lines: className|varName . subroutineName (
            self.index += 4
            nArgs += self.compileExpressionList(class_table, subroutine_table)
            self.index += 1    # Jump ) token line
            self.vm_writer.writeCall(fullname, nArgs)
        return

    def compileExpressionList(self, class_table, subroutine_table):
        '''
        Compile list of expressions
        Structure: (expression (, expression)*)?'''
        counter = 0
        if self.tokens[self.index] != "<symbol> ) </symbol>":
            # Expression list not empty
            self.compileExpression(class_table, subroutine_table)
            counter += 1
            while self.tokens[self.index] == "<symbol> , </symbol>":
                # Expression list not finished
                self.index += 1     # Jump , token line
                self.compileExpression(class_table, subroutine_table)
                counter += 1
        return counter
