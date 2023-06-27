# Project 07 VM Translator Part 1
#
# Yves Yang
#
# Helper Function translate to convert each VM Language line to Assembly.
from reference_table import Table


def translate(lines, filename):
    '''
    Take in VM codes in a list and filename(without extension) in a string.
    Return a list of translated Assembly codes
    '''
    table = Table()
    result = []
    continue_counter = 0

    for line in lines:
        if line in table.arithmetic_commands:
            # Translate Arithmetic-Logical Commands
            script, continue_counter = table.translate_arithmetic_command(
                line, continue_counter)
        else:
            # Translate Memory Access Code
            # script = ["PLACEHOLDER"]
            script = table.translate_memory_command(line, filename)
        # Add script for current line to the result list.
        result += script
    return result
