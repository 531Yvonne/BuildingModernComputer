# Project 8: VM Translator Part 2
#
# Yves Yang
#
# Store reference table data and methods to translate code accordingly


class Table:
    def __init__(self, filename):
        # PART 1 TABLES
        self.filename = filename
        self.table1 = {"add": "+", "sub": "-", "and": "&", "or": "|"}
        self.table2 = {"neg": "-", "not": "!"}
        self.table3 = {"eq": "JEQ", "gt": "JGT", "lt": "JLT"}
        self.arithmetic_commands = list(self.table1.keys()) +\
            list(self.table2.keys()) +\
            list(self.table3.keys())
        self.memory_access_action = ["push", "pop"]
        self.segments = {"local": "LCL",
                         "argument": "ARG",
                         "this": "THIS",
                         "that": "THAT"}
        self.pointer_table = {"0": "THIS", "1": "THAT"}

        # PART 2 TABLES
        self.branching_commands = ["label", "goto", "if-goto"]

        # Initialization: Set initial SP to 256 and call Sys.init
        self.initial_code = self.get_initial_code()

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

    def translate_memory_command(self, line):
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
                script = ["@" + self.filename + "." + value,
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
                          "@" + self.filename + "." + value,
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

    def translate_branching_command(self, line):
        '''
        Input:
        Take a line of VM language branching command code in a string.
        Output:
        Translated Assembly code script in a list.
        '''
        action, label_name = line.split()[0], line.split()[1].upper()
        if action == "label":
            script = ["(" + label_name + ")"]
        elif action == "goto":
            script = ["@" + label_name, "0;JMP"]
        else:
            # if-goto.
            script = ["@SP",
                      "AM=M-1",
                      "D=M",
                      "@" + label_name,
                      "D;JNE"
                      ]
        return script

    def translate_function_command(self, line, return_label_id):
        '''
        Input:
        Take a line of VM language function command code in a string.
        Take an int counting return address label.
        Output:
        Translated Assembly code script in a list.
        '''
        if line == "return":
            # CASE 1: return command
            # FRAME = LCL
            script = ["@LCL", "D=M", "@FRAME", "M=D"]
            # Get return address: RET = *(FRAME - 5)
            script += ["@5", "A=D-A", "D=M", "@RET", "M=D"]
            # Reposition return result value to where currently ARG points to.
            script += ["@SP", "AM=M-1", "D=M", "@ARG", "A=M", "M=D"]
            # Restore caller's SP to *ARG + 1
            script += ["@ARG", "D=M+1", "@SP", "M=D"]
            # Restore caller's THAT, THIS, ARG, LCL (in reverse order)
            script += ["@FRAME", "AM=M-1", "D=M", "@THAT", "M=D"] + \
                ["@FRAME", "AM=M-1", "D=M", "@THIS", "M=D"] + \
                ["@FRAME", "AM=M-1", "D=M", "@ARG", "M=D"] + \
                ["@FRAME", "AM=M-1", "D=M", "@LCL", "M=D"]
            # goto return address (caller's return label)
            script += ["@RET", "A=M", "0;JMP"]
            return script, return_label_id

        action, func_name, n = line.split()
        if action == "call":
            # CASE 2: Call func_name nArgs
            return_label_id += 1
            # Push return address
            write_d_to_sp = ["@SP",
                             "AM=M+1",
                             "A=A-1",
                             "M=D"]
            script = ["@" + self.filename + "$ret" + str(return_label_id),
                      "D=A"] + write_d_to_sp
            # Push LCL, ARG, THIS, THAT
            script += ["@LCL", "D=M"] + write_d_to_sp + \
                ["@ARG", "D=M"] + write_d_to_sp + \
                ["@THIS", "D=M"] + write_d_to_sp + \
                ["@THAT", "D=M"] + write_d_to_sp
            # Update ARG = SP - n - 5
            script += ["@SP",
                       "D=M",
                       "@" + str(5+int(n)),
                       "D=D-A",
                       "@ARG",
                       "M=D"]
            # Update LCL = SP
            script += ["@SP",
                       "D=M",
                       "@LCL",
                       "M=D"]
            # goto func and show return label
            script += ["@" + func_name,
                       "0;JMP",
                       "(" + self.filename + "$ret" + str(return_label_id) + ")"]
            return script, return_label_id

        else:
            # CASE 3: function func_name nVars
            script = ["(" + func_name + ")"]
            if int(n) < 5:
                # Variables below 5, use simple duplicate to save cycles.
                script += ["@SP",
                           "AM=M+1",
                           "A=A-1",
                           "M=0",
                           ] * int(n)
            else:
                # Variables n >= 5, use LOOP instead to save cycles.
                script += ["@" + n,
                           "D=A",
                           "@R13",
                           "M=D",
                           "(CREATE_VAR_LOOP)",
                           "@R13",
                           "D=M",
                           "@END_VAR_LOOP",
                           "D;JLE",
                           "@SP",
                           "AM=M+1",
                           "A=A-1",
                           "M=0",
                           "@R13",
                           "M=M-1",
                           "@CREATE_VAR_LOOP",
                           "0;JMP",
                           "(END_VAR_LOOP)"
                           ]
            return script, return_label_id

    def get_initial_code(self):
        '''
        Set initial SP to 256
        call Sys.init 0 (treat as a 0 argument function call)
        '''
        script = ["@256",
                  "D=A",
                  "@SP",
                  "M=D"]
        script += self.translate_function_command("call Sys.init 0", 0)[0]

        return script
