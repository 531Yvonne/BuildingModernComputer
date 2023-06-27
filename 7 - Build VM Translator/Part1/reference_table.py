# Project 7: VM Translator Part 1
#
# Yves Yang
#
# Store reference table data and methods to translate code accordingly


class Table:
    def __init__(self):
        self.table1 = {"add": "+", "sub": "-", "and": "&", "or": "|"}
        self.table2 = {"neg": "-", "not": "!"}
        self.table3 = {"eq": "JEQ", "gt": "JGT", "lt": "JLT"}
        self.arithmetic_commands = list(self.table1.keys()) +\
            list(self.table2.keys()) +\
            list(self.table3.keys())
        self.segments = {"local": "LCL",
                         "argument": "ARG",
                         "this": "THIS",
                         "that": "THAT"
                         }
        self.pointer_table = {"0": "THIS", "1": "THAT"}

    def translate_arithmetic_command(self, keyword, continue_counter):
        '''
        Input:
        a string of arithmetic command; an int counting CONTINUE Label.
        Output:
        translated Assembly code in a list; an int for updated counter.
        '''

        if keyword in self.table1:
            # keyword is add, sub, and, or
            script = ["@SP",
                      "AM=M-1",
                      "D=M",
                      "A=A-1",
                      "M=M" + self.table1[keyword] + "D",
                      ]
        elif keyword in self.table2:
            # keyword is neg, not
            script = ["@SP",
                      "A=M-1",
                      "M=" + self.table2[keyword] + "M",
                      ]
        else:
            # keyword is gt, eq, lt
            # Add counter number to the end of "CONTINUE" label as Unique ID
            continue_counter += 1
            coutinue_label = "CONTINUE" + str(continue_counter)
            script = ["@SP",
                      "AM=M-1",
                      "D=M",
                      "A=A-1",
                      "D=M-D",
                      "M=-1",
                      "@" + coutinue_label,
                      "D;" + self.table3[keyword],
                      "@SP",
                      "A=M-1",
                      "M=0",
                      "(" + coutinue_label + ")"
                      ]
        return script, continue_counter

    def translate_memory_command(self, line, filename):
        '''
        Input:
        Take a line of VM language code in a string.
        Take in filename for static symbol naming
        Output:
        Translated Assembly code script in a list.
        '''
        # Decompose Memory Access Code
        action, segment, value = line.split()

        if segment == "constant":
            # Case 1: push constant value
            script = ["@" + value,
                      "D=A",
                      "@SP",
                      "AM=M+1",
                      "A=A-1",
                      "M=D"
                      ]

        elif segment == "static":
            # Case 2: static involved
            if action == "push":
                # push static value
                script = ["@" + filename + "." + value,
                          "D=M",
                          "@SP",
                          "AM=M+1",
                          "A=A-1",
                          "M=D"
                          ]
            else:
                # pop static value
                script = ["@SP",
                          "AM=M-1",
                          "D=M",
                          "@" + filename + "." + value,
                          "M=D"
                          ]

        elif segment == "temp":
            # Case 3: temp involved
            index = int(value) + 5
            if action == "push":
                # push temp value
                script = ["@" + str(index),
                          "D=M",
                          "@SP",
                          "AM=M+1",
                          "A=A-1",
                          "M=D"
                          ]
            else:
                # pop temp value
                script = ["@SP",
                          "AM=M-1",
                          "D=M",
                          "@" + str(index),
                          "M=D"
                          ]

        elif segment == "pointer":
            # Case 4: pointer involved
            if action == "push":
                # push pointer 0/1
                script = ["@" + self.pointer_table[value],
                          "D=M",
                          "@SP",
                          "AM=M+1",
                          "A=A-1",
                          "M=D"
                          ]
            else:
                # pop pointer 0/1
                script = ["@SP",
                          "AM=M-1",
                          "D=M",
                          "@" + self.pointer_table[value],
                          "M=D"
                          ]

        else:
            # Case 5: local, argument, this, that
            if action == "push":
                # push local/argument/this/that value
                script = ["@" + value,
                          "D=A",
                          "@" + self.segments[segment],
                          "A=M+D",
                          "D=M",
                          "@SP",
                          "AM=M+1",
                          "A=A-1",
                          "M=D"
                          ]
            else:
                # pop local/argument/this/that value
                script = ["@" + value,
                          "D=A",
                          "@" + self.segments[segment],
                          "D=M+D",
                          "@R13",  # store target address at 3rd place
                          "M=D",
                          "@SP",
                          "AM=M-1",
                          "D=M",
                          "@R13",
                          "A=M",
                          "M=D"
                          ]
        return script
