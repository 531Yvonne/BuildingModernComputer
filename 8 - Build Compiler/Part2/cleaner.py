# Project 11: Compiler Part 2
#
# Yves Yang
#
# Helper Function to get clean jack file code
import re


def clean_text(file):
    '''
    This clean raw text function is carried over and modified from project0

    Clean comments in format 1:
        begin with the sequence "//" and end at the line return
    Clean comments in format 2:
        begin with the sequence /* and end at the sequence */
        the comment can be in one line or cross multiple lines
    Clean blank lines and leading white space:
        spaces and tabs before the first character that isn't a space or tab

    Input: an open file

    Output: a list of each line of the cleaned string
    '''

    # Delete Comments begin with the sequence "//" and end at the line return.
    lines = file.readlines()
    full_text_1 = ""
    for line in lines:
        if line[0:2] == "//":
            # Whole line is comment, ignore whole line.
            continue
        elif "//" in line:
            # Comment starts from middle
            index = line.find("//")
            valid_part = line[:index]
            # With comment, keep non-comment part.
            full_text_1 += valid_part + "\n"
        else:
            # No comment, keep the whole line.
            full_text_1 += line

    # Delete comments begin with the sequence /* and end at the sequence */
    # in one line.
    full_text_2 = ""
    # Drop comments in such format by split().
    for i in re.split(r"/\*.*\*/", full_text_1):
        full_text_2 += i

    # Delete comments begin with the sequence /* and end at the sequence */ and
    # cross multiple lines
    full_text_3 = ""
    # Drop comments in such format by split().
    for i in re.split(r"/\*(.|\n)*?\*/", full_text_2):
        full_text_3 += i

    # Clean blank lines and leading white space
    result = ""
    for line in full_text_3.strip().split("\n"):
        line = line.strip("\t").strip()
        if len(line) != 0:
            result += line + "\n"

    # Delete the final blank line and return the result as a list of each line
    result = result.strip().split("\n")
    return result