# Project 8: VM Translator Part 2
#
# Yves Yang
#
# This source code contains a VM Translator (Translate VM Language to Assembly)
import sys
from path_processer import Path
from reference_table import Table
from translator import translate
from cleaner import clean_text


def main(path):
    '''
    Main function calls path processor, data cleaner and translator
    in order to convert .vm file(s) to assembly language at .asm file to the
    same directory as the input file.
    '''
    source = Path(path)
    result = []
    contains_bootstrap_code = False

    for vm_filename, vm_filepath in source.vm_files:
        with open(vm_filepath, "r") as file:

            # if not contains_bootstrap_code:
            #     # Initialize the result by adding initial bootstrap code
            #     result += Table(vm_filename).initial_code
            #     contains_bootstrap_code = True

            # Clean the .vm input file using cleaner function.
            # (clean_text function carried over from project7 code).
            lines = clean_text(file)

            # Translate cleaned VM Language lines.
            assembly_code = translate(lines, vm_filename)
            result += assembly_code

    # Write the list of all assembly codes to .asm file.
    with open(source.output_path, "w") as destination:
        for line in result[:-1]:
            destination.write(line + "\n")
        # Write last line without \n
        destination.write(result[-1])


# This enables direct excution of the assembler at Command Line
if __name__ == "__main__":
    path = sys.argv[1]
    main(path)
