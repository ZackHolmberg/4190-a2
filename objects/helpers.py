from typing import List


def value_to_variable(value: str) -> str:
    """
    Converts keys to their values, ie:
    '+a' -> 'A'
    '-abc' -> 'ABC'
    """
    if value[0] != '-' and value[0] != '+':
        # If already a variable, then return it
        return value.upper()

    return value[1:].upper()


def get_key_values(key: str) -> List[str]:
    """
    Returns a list of key values from a key
    Example: key='+r,-t,+l', returns=['+r', '-t', '+l']
    """
    return key.split(',')


def new_key_from_existing(key: str, variables: List[str]) -> str:
    """
    Generates a new key from existing. How exciting!
    Example: key='+r,-t,+l', variables=['R', 'L'], returns='+r,+l'
    """
    key_values = get_key_values(key)
    key_variables = [ value_to_variable(v) for v in key_values ]

    matched_key_values = []
    for variable in variables:
        try:
            index = key_variables.index(variable)
            matched_key_values.append(key_values[index])
        except:
            pass

    return ','.join(matched_key_values)
