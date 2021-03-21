"""
Course: COMP 4190
Instructor: Cuneyt Akcora

Assignment 2

Submission by:
Yaroslav Mikhaylik, 7853156
Zack Holmberg, 7777823

File purpose: A class that generates keys to index into a factors' dictionary, which contains the probabilistic values. 
            Keys represent rows in a CPT, so one key may equal "+T,-R,+F" which will index into the dictionary to get the 
            corresponding probabilistic value for that combination. 

"""

from .relation import Relation


class KeyIterator:
    def __init__(self, relation: Relation):
        """
        Function aim: KeyIterator class constructor
        Parameters: A Relation object representing the relation that the keys correspond to
        Return: N/A
        """
        self.relation = relation
        self.n = len(self.relation.variables)
        self.it = 0

    def __iter__(self):
        return self

    def __next__(self) -> str:
        """
        Function aim: Overrides a python iterator method for iterating over the Factor's keys
        Parameters: N/A
        Return: string
        """
        while True:
            # Iterated through every possible permutation of values, now we stop
            if self.it >= 2 ** self.n:
                self.reset()
                raise StopIteration()

            skip = False
            key_values = []

            for j in range(self.n):
                variable = self.relation.variables[j].lower()

                is_true = bool((self.it >> (self.n - j - 1)) & 1)

                # If we are generating a key value whose variable corresponds to a variable of some assigned
                #   value AND if the key part does not equal that assigned value, then we ignore this key
                #   as it is invalid -> won't be included in the table (ie: not generating entries for '+r' rows
                #   if we already have evidence '-r')
                matching_value = self.relation.get_value_by_variable(
                    variable.upper())
                if matching_value:
                    if (matching_value[0] == '+' and not is_true) or (matching_value[0] == '-' and is_true):
                        self.it += 1
                        skip = True

                key_values.append(
                    f'+{variable}' if is_true else f'-{variable}')

            if not skip:
                break

        self.it += 1

        return ','.join(key_values)

    def reset(self) -> None:
        self.it = 0

    def __str__(self) -> str:
        """
        Function aim: Converts the class instance to a string representation
        Parameters: N/A
        Return: string
        """
        old_it = self.it
        self.it = 0

        result = str(self.relation) + '\n'
        for key in self:
            result += f'  {key}\n'

        self.it = old_it
        return result
