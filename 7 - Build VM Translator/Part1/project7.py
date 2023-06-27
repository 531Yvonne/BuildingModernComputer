# Project 7: VM Translator Part 1
#
# Yves Yang
#
# This source code contains a VM Translator (Translate VM Language to Assembly)
import sys
import os
from cleaner import clean_text
from translator import translate


def main(path):
    '''
    Main function calls data cleaner and translator
    in order to convert .vm input to assembly language at .asm file to the same
    directory as the input file.
    '''
    with open(path, "r") as file:
        # Clean the .vm input file using cleaner function.
        # (clean_text function inherited from project0 code).
        lines = clean_text(file)

        # filename obtained for static symbol naming during translation
        filename = os.path.basename(path)[:-3]
        # Translate cleaned VM Language lines.
        result = translate(lines, filename)

        # Create output path based on input path.
        newpath = path[:-2] + "asm"

        # Write assembly code to .asm file.
        with open(newpath, "w") as newfile:
            for line in result[:-1]:
                newfile.write(line + "\n")
            # Write last line without \n
            newfile.write(result[-1])


# This enables direct excution of the assembler at Command Line
if __name__ == "__main__":
    path = sys.argv[1]
    main(path)
