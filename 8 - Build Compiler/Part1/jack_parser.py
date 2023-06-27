# Project 10: Compiler Part 1
#
# Yves Yang
#
# This source code contains a Parser for jack code syntax analysis
class Parser:
    op = ["+", "-", "*", "/", "&", "|", "<", ">", "="]

    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 1  # Ignore tokens[0]: "<tokens>", start from tokens[1]
        self.parsed_result = self.compileClass()

    def compileClass(self):
        '''
        Compile a complete class
        Structure: class className { classVarDec* subroutineDec* }
        '''
        result = ["<class>"]
        # Include 3 lines of token: class className {
        result += self.tokens[self.index:self.index+3]
        self.index += 3     # Move pointer to next pending token line
        while ("<keyword> static" in self.tokens[self.index] or
                "<keyword> field" in self.tokens[self.index]):
            # Compile classVarDec zero or more times
            result += self.compileClassVarDec()
        while ("<keyword> constructor" in self.tokens[self.index] or
                "<keyword> function" in self.tokens[self.index] or
                "<keyword> method" in self.tokens[self.index]):
            # Compile subroutineDec zero or more times
            result += self.compileSubroutineDec()
        result.append(self.tokens[self.index])      # Append } token line
        self.index += 1     # Move pointer
        result.append("</class>")
        return result

    def compileClassVarDec(self):
        '''
        Compile a static or field declaration
        Structure: (static | field) type varName (, varName)* ;
        '''
        result = ["<classVarDec>"]
        # Include 3 lines of token: (static | field) type varName
        result += self.tokens[self.index:self.index+3]
        self.index += 3     # Move pointer
        while ";" not in self.tokens[self.index]:
            # Declaration not end, contains extra (, varName)
            result += self.tokens[self.index:self.index+2]
            self.index += 2     # Move pointer down one line
        result.append(self.tokens[self.index])      # Append ; token line
        self.index += 1     # Move pointer
        result.append("</classVarDec>")
        return result

    def compileSubroutineDec(self):
        '''
        Compile a complete method, function or constructor
        Structure: (constructor | function | method) (void | type)
                    subroutineName ( parameterList ) subroutineBody
        '''
        result = ["<subroutineDec>"]
        # Include 4 lines of token: (constructor | function | method),
        # (void | type), subroutineName and (
        result += self.tokens[self.index:self.index+4]
        self.index += 4     # Move pointer
        result += self.compileParameterList()
        result.append(self.tokens[self.index])      # Append ) token line
        self.index += 1     # Move pointer
        result += self.compileSubroutineBody()
        result.append("</subroutineDec>")
        return result

    def compileParameterList(self):
        '''
        Compile a parameter list
        Structure: ((type varName) (, type varName)*)?
        '''
        result = ["<parameterList>"]
        if ("int" in self.tokens[self.index] or
            "char" in self.tokens[self.index] or
            "boolean" in self.tokens[self.index] or
                "<identifier>" in self.tokens[self.index]):
            # at least 1 parameter exist, add 2 tokens: type varName to result.
            result += self.tokens[self.index:self.index+2]
            self.index += 2     # Move pointer
            while "<symbol> )" not in self.tokens[self.index]:
                # parameters list not done, add 3 extra tokens: , type varName
                result += self.tokens[self.index:self.index+3]
                self.index += 3     # Move pointer
        result.append("</parameterList>")
        return result

    def compileSubroutineBody(self):
        ''' Compile a subroutine's body, Structure: { varDec* statements }'''
        result = ["<subroutineBody>"]
        result.append(self.tokens[self.index])      # Add { token line
        self.index += 1     # Move pointer
        while "<keyword> var" in self.tokens[self.index]:
            # Compile varDec zero or more times
            result += self.compileVarDec()
        result += self.compileStatements()
        result.append(self.tokens[self.index])      # Append ) token line
        self.index += 1     # Move pointer
        result.append("</subroutineBody>")
        return result

    def compileVarDec(self):
        '''
        Compile a var declaration
        Structure: var type varName (, type varName)* ;
        '''
        result = ["<varDec>"]
        # Add 3 token lines: var type varName
        result += self.tokens[self.index:self.index+3]
        self.index += 3     # Move pointer to next pending token
        while "<symbol> ;" not in self.tokens[self.index]:
            # Declaration not finished, process extra variables
            result += self.tokens[self.index:self.index+2]
            self.index += 2     # Move pointer
        result.append(self.tokens[self.index])      # Append ; token line
        self.index += 1     # Move pointer
        result.append("</varDec>")
        return result

    def compileStatements(self):
        ''' Compile a sequence of statements '''
        result = ["<statements>"]
        while (self.tokens[self.index] == "<keyword> let </keyword>" or
                self.tokens[self.index] == "<keyword> if </keyword>" or
                self.tokens[self.index] == "<keyword> while </keyword>" or
                self.tokens[self.index] == "<keyword> do </keyword>" or
                self.tokens[self.index] == "<keyword> return </keyword>"):
            if self.tokens[self.index] == "<keyword> let </keyword>":
                result += self.compileLet()
            elif self.tokens[self.index] == "<keyword> if </keyword>":
                result += self.compileIf()
            elif self.tokens[self.index] == "<keyword> while </keyword>":
                result += self.compileWhile()
            elif self.tokens[self.index] == "<keyword> do </keyword>":
                result += self.compileDo()
            elif self.tokens[self.index] == "<keyword> return </keyword>":
                result += self.compileReturn()
        result.append("</statements>")
        return result

    def compileLet(self):
        '''
        Compile a let statement
        Structure: let varName ([ expression ])? = expression ;
        '''
        result = ["<letStatement>"]
        # Add 2 token lines: let varName
        result += self.tokens[self.index:self.index+2]
        self.index += 2     # Move pointer to next pending token
        if "<symbol> [" in self.tokens[self.index]:
            # [ expression ] exists
            result.append(self.tokens[self.index])   # Append [ token line
            self.index += 1     # Move pointer
            result += self.compileExpression()
            result.append(self.tokens[self.index])   # Append ] token line
            self.index += 1     # Move pointer
        result.append(self.tokens[self.index])      # Append = token line
        self.index += 1     # Move pointer
        result += self.compileExpression()
        result.append(self.tokens[self.index])      # Append ; token line
        self.index += 1     # Move pointer
        result.append("</letStatement>")
        return result

    def compileIf(self):
        '''
        Compile an if statement
        Structure: if ( expression ) { statements } (else { statements })?
        '''
        result = ["<ifStatement>"]
        # Add 2 token lines: if (
        result += self.tokens[self.index:self.index+2]
        self.index += 2     # Move pointer to next pending token
        result += self.compileExpression()
        result += self.tokens[self.index:self.index+2]  # Append ) { token line
        self.index += 2     # Move pointer
        result += self.compileStatements()
        result.append(self.tokens[self.index])      # Append } token line
        self.index += 1     # Move pointer
        if "<keyword> else" in self.tokens[self.index]:
            # else statement exists
            # Append 2 tokens: else {
            result += self.tokens[self.index:self.index+2]
            self.index += 2     # Move pointer
            result += self.compileStatements()
            result.append(self.tokens[self.index])      # Append } token line
            self.index += 1     # Move pointer
        result.append("</ifStatement>")
        return result

    def compileWhile(self):
        '''
        Compile a while statement
        Structure: while ( expression ) { statements }
        '''
        result = ["<whileStatement>"]
        # Add 2 token lines: while (
        result += self.tokens[self.index:self.index+2]
        self.index += 2     # Move pointer to next pending token
        result += self.compileExpression()
        result += self.tokens[self.index:self.index+2]  # Append ) { token line
        self.index += 2     # Move pointer
        result += self.compileStatements()
        result.append(self.tokens[self.index])      # Append } token line
        self.index += 1     # Move pointer
        result.append("</whileStatement>")
        return result

    def compileDo(self):
        '''
        Compile a do statement
        Structure: do subroutineCall ;
        '''
        result = ["<doStatement>"]
        result.append(self.tokens[self.index])      # Append do token line
        self.index += 1     # Move pointer
        result += self.compileSubroutineCall()
        result.append(self.tokens[self.index])      # Append ; token line
        self.index += 1     # Move pointer
        result.append("</doStatement>")
        return result

    def compileReturn(self):
        ''' Compile a return statement, Structure: return expression? ;'''
        result = ["<returnStatement>"]
        result.append(self.tokens[self.index])      # Append return token line
        self.index += 1     # Move pointer
        if self.tokens[self.index] != "<symbol> ; </symbol>":
            result += self.compileExpression()
        result.append(self.tokens[self.index])      # Append ; token line
        self.index += 1     # Move pointer
        result.append("</returnStatement>")
        return result

    def compileExpression(self):
        ''' Compile an expression. Structure: term (op term)* '''
        result = ["<expression>"]
        result += self.compileTerm()
        while ("<symbol>" in self.tokens[self.index] and
               self.tokens[self.index][9] in self.op):
            # Check whether next token is <symbol> x </symbol>
            result.append(self.tokens[self.index])      # Append op token line
            self.index += 1     # Move pointer
            result += self.compileTerm()
        result.append("</expression>")
        return result

    def compileTerm(self):
        ''' Compile a term '''
        result = ["<term>"]
        if ("<integerConstant>" in self.tokens[self.index] or
                "<stringConstant>" in self.tokens[self.index]):
            result.append(self.tokens[self.index])      # Append token line
            self.index += 1     # Move pointer
        elif "<keyword>" in self.tokens[self.index]:
            if (self.tokens[self.index][10:14] in ["true", "null", "this"]
                    or self.tokens[self.index][10:15] == "false"):
                # term is keywordConstant
                result.append(self.tokens[self.index])   # Append keyword line
                self.index += 1     # Move pointer
        elif ("<symbol> -" in self.tokens[self.index]
              or "<symbol> ~" in self.tokens[self.index]):
            # term is unaryOp term
            result.append(self.tokens[self.index])      # Append unaryOp line
            self.index += 1     # Move pointer
            result += self.compileTerm()
        elif "<symbol> (" in self.tokens[self.index]:
            # term is ( expression )
            result.append(self.tokens[self.index])      # Append ( line
            self.index += 1     # Move pointer
            result += self.compileExpression()
            result.append(self.tokens[self.index])      # Append ) line
            self.index += 1     # Move pointer
        elif "<identifier>" in self.tokens[self.index]:
            # Term can be varName | varName[expression] | subroutineCall
            if (self.tokens[self.index+1] != "<symbol> ( </symbol>"
                    and self.tokens[self.index+1] != "<symbol> . </symbol>"):
                # Term can be varName | varName[expression]
                if self.tokens[self.index+1] == "<symbol> [ </symbol>":
                    # Term is varName[expression]
                    # Append 2 token lines: varName [
                    result += self.tokens[self.index:self.index+2]
                    self.index += 2     # Move pointer
                    result += self.compileExpression()
                    result.append(self.tokens[self.index])      # Append ] line
                    self.index += 1     # Move pointer
                else:
                    # Term is varName, Append one token line: varName
                    result.append(self.tokens[self.index])
                    self.index += 1     # Move pointer
            else:
                # Term is subroutineCall
                result += self.compileSubroutineCall()
        result.append("</term>")
        return result

    def compileSubroutineCall(self):
        ''' Compile a subroutine call '''
        result = []
        if self.tokens[self.index+1] == "<symbol> ( </symbol>":
            # Structure: subroutineName ( expressionList )
            # Append 2 token lines: subroutineName (
            result += self.tokens[self.index:self.index+2]
            self.index += 2     # Move pointer
            result += self.compileExpressionList()
            result.append(self.tokens[self.index])      # Append ) line
            self.index += 1     # Move pointer
        else:
            # Structure: className|varName . subroutineName ( expressionList )
            # Append 4 token lines: className|varName . subroutineName (
            result += self.tokens[self.index:self.index+4]
            self.index += 4     # Move pointer
            result += self.compileExpressionList()
            result.append(self.tokens[self.index])      # Append ) line
            self.index += 1     # Move pointer
        return result

    def compileExpressionList(self):
        '''
        Compile list of expressions
        Structure: (expression (, expression)*)?'''
        result = ["<expressionList>"]
        if self.tokens[self.index] != "<symbol> ) </symbol>":
            # Expression list not empty
            result += self.compileExpression()
            while self.tokens[self.index] == "<symbol> , </symbol>":
                # Expression list not finished, add next expression
                result.append(self.tokens[self.index])      # Append , line
                self.index += 1     # Move pointer
                result += self.compileExpression()
        result.append("</expressionList>")
        return result
