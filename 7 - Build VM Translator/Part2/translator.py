# Project 08 VM Translator Part 2
#
# Yves Yang
#
# Helper Function translate to convert each VM Language line to Assembly.
from reference_table import Table


def translate(lines, vm_filename):
    '''
    Take in VM codes in a list and filename(without extension) in a string.
    Return a list of translated Assembly codes
    '''
    table = Table(vm_filename)
    result = []
    continue_counter = 0    # Unique id at the end of "CONTINUE" label
    return_label_id = 0    # Unique id for ret-address label when call func

    for line in lines:
        words = line.split()
        if words[0] in table.arithmetic_commands:
            # Translate Arithmetic-Logical Commands
            script, continue_counter = table.translate_arithmetic_command(
                line, continue_counter)
        elif words[0] in table.memory_access_action:
            # Translate Memory Access Code
            script = table.translate_memory_command(line)
        elif words[0] in table.branching_commands:
            # Translate Branching Commands
            script = table.translate_branching_command(line)
        else:
            # Translate Function Commands
            script, return_label_id = table.translate_function_command(
                line, return_label_id)

        # Add script for current line to the result list.
        result += script
    return result
