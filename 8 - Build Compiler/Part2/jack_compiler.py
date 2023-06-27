# Project 11: Compiler Part 2
#
# Yves Yang
#
# This source code contains the Compiler for code written in jack language.
import sys
from path_processer import Path
from cleaner import clean_text
from jack_tokenizer import Tokenizer
from compile_engine import CompileEngine


def main(path):
    '''
    Main function calls path processor, data cleaner, tokenizer and parser
    in order to convert Xxx.jack file(s) to XxxT.xml and Xxx.xml file(s) to the
    same directory as the input file.
    '''
    source = Path(path)

    for jack_filepath in source.filepaths:
        with open(jack_filepath, "r") as file:

            # Clean the .jack input file using cleaner function.
            # (clean_text function carried over from previous project).
            lines = clean_text(file)

            # Tokenize cleaned jack Language lines and get tokens in a list.
            tokens = Tokenizer(lines).tokens

            # Parse the tokens and get final result in a list.
            result = CompileEngine(tokens).vm_writer.vm_codes

        # Write final Parsed Result to Xxx.vm file.
        output_path = jack_filepath[:-4] + "vm"  # Based on jack_filepath.
        with open(output_path, "w") as destination:
            for line in result[:-1]:
                destination.write(line + "\n")
            # Write last line without \n
            destination.write(result[-1])


# This enables direct excution of the Analyzer at Command Line
if __name__ == "__main__":
    path = sys.argv[1]
    main(path)
