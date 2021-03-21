"""
Course: COMP 4190
Instructor: Cuneyt Akcora

Assignment 2

Submission by:
Yaroslav Mikhaylik, 7853156
Zack Holmberg, 7777823

File purpose: Contains various helper methods used in the program

"""

from typing import List


def value_to_variable(value: str) -> str:
    """
    Function aim: Converts keys to their values, ie:
    '+a' -> 'A'
    '-abc' -> 'ABC'
    Parameters: One string representing the value to turn into a variable
    Return: string
    """
    if value[0] != '-' and value[0] != '+':
        # If already a variable, then return it
        return value.upper()

    return value[1:].upper()


def get_key_values(key: str) -> List[str]:
    """
    Function aim: Returns a list of key values from a key
    Example: key='+r,-t,+l', returns=['+r', '-t', '+l']
    Parameters: One string representing the key to split into individual values
    Return: List of strings representing all values in a key
    """
    return key.split(',')


def new_key_from_existing(key: str, variables: List[str]) -> str:
    """
    Function aim: Generates a new key from existing. How exciting!
    Example: key='+r,-t,+l', variables=['R', 'L'], returns='+r,+l'
    Parameters: One string representing a key and a list of strings representing the variables
    Return: String representing the new key
    """
    key_values = get_key_values(key)
    key_variables = [value_to_variable(v) for v in key_values]

    matched_key_values = []
    for variable in variables:
        try:
            index = key_variables.index(variable)
            matched_key_values.append(key_values[index])
        except:
            pass

    return ','.join(matched_key_values)
