# Project 6: Assembler
#
# Yves Yang
#
# This source code contains an Assembler for the Hack computer.
import sys
from cleaner import clean_text
from translator import translate
from label_processer import process_label


def main(path):
    '''
    Main function calls data cleaner, label processor and translator
    in order to convert .asm input to binary code at a .hack file to the same
    directory as the input file.
    '''
    with open(path, "r") as file:
        # Clean the .asm input file using cleaner function.
        # (clean_text function modified from project0 code).
        lines = clean_text(file)

        # Identify labels and get updated codes and updated reference table
        new_lines, reference_table = process_label(lines)

        # Translate new lines based on a Table type reference_table
        result = translate(new_lines, reference_table)

        # Create output path based on input path.
        newpath = path[:-3] + "hack"

        # Write binary code to .hack file.
        with open(newpath, "w") as newfile:
            for line in result[:-1]:
                newfile.write(line + "\n")
            # Write last line without \n
            newfile.write(result[-1])


# This enables direct excution of the assembler at Command Line
if __name__ == "__main__":
    path = sys.argv[1]
    main(path)
