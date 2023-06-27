# Project 06
#
# Yves Yang
#
# Helper Function translate to convert each assembly line to binary code.
import re


def translate(lines, table):
    '''
    Take in cleaned & labels removed assembly code in a list
    Take in reference table of Table type.
    Return a list of translated binary codes
    '''
    result = []
    for line in lines:
        if "@" in line:
            # Implementation for A-instruction.
            symbol = line[1:]
            if re.match(r'^[0-9]+$', symbol):
                # Scenario 1: @number
                result.append(number_to_16bits(int(symbol)))
            elif symbol in table.symbol_table:
                # Scenario 2: @predefined-symbols or @in_table_variables.
                value = table.symbol_table[symbol]
                result.append(number_to_16bits(value))
            else:
                # Scenario 3: @variables ----- first occurence, add in table.
                table.symbol_table[symbol] = table.next_available_value
                result.append(number_to_16bits(table.next_available_value))
                table.next_available_value += 1
        else:
            # Implementation for C-instruction: dest=comp;jump
            if "=" not in line:
                # Add dest part to get standard format.
                line = "null=" + line
            if ";" not in line:
                # Add jump part to get standard format.
                line = line + ";null"
            # Use regular expression to match each part.
            match = re.match(r"^(.*)=(.*);(.*)$", line)
            dest = match.group(1)
            comp = match.group(2)
            jump = match.group(3)
            # Find the matching binary codes from reference table.
            dest_code = table.dest_table[dest]
            comp_code = table.comp_table[comp]
            jump_code = table.jump_table[jump]
            result.append("111" + comp_code + dest_code + jump_code)
    return result


def number_to_16bits(number):
    ''' Convert number to a string of 16-bit binary code. '''
    binary_value = bin(number)[2:]
    left_zeros = 16 - len(binary_value)
    # Fill zeros at left to get 16-bit complete binary code
    result = "0" * left_zeros + binary_value
    return result
