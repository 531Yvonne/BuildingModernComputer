# Project 06
#
# Yves Yang
#
# Helper Function read cleaned lines and add declared label to reference table
from reference_table import Table


def process_label(lines):
    '''
    Take in a list of cleaned assembly code lines
    Return a list of assembly code without label declaration lines
    Return a Table type reference_table
    '''
    table = Table()
    result = []
    label_counter = 0
    for line_number, line in enumerate(lines):
        if line[0] == "(" and line[-1] == ")":
            # Label declaration line identified
            label = line[1:-1]
            table.symbol_table[label] = line_number - label_counter
            label_counter += 1
        else:
            # Not a label declaration line ---- append to new list
            result.append(line)
    return result, table
