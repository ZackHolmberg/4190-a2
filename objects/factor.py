"""
Course: COMP 4190
Instructor: Cuneyt Akcora

Assignment 2

Submission by:
Yaroslav Mikhaylik, 7853156
Zack Holmberg, 7777823

File purpose: A class that represents a probabilistic Factor, used in Bayes Nets

"""

from typing import List
from .key_iterator import KeyIterator
from .relation import Relation
from .helpers import get_key_values


class Factor:
    def __init__(self, relation: str, known_values: List[str] = []):
        """
        Function aim: Factor class constructor
        Parameters: A string representing the factor's relation and a list of strings representing its known values (evidence)
        Return: N/A
        """
        self.data = {}
        self.relation = Relation(relation, known_values)
        self.kit = KeyIterator(self.relation)

    def init(self, probabilities: List[float]):
        count = 0
        for key in self.kit:
            self.data[key] = probabilities[count]
            count += 1

    def find_fuzzy_keys(self, key: str) -> List[str]:
        """
        Function aim: Matches keys fuzzily to a given key. Sort of like filtering.
        Example: key='+r-t'
        Will return ['+r-t-l', '+r-t+l', ... other keys that have '+r-t' in them]
        Parameters: A string representing the substring of keys that we want to find
        Return: List of strings representing corresponding keys
        """
        keys = []
        key_values = get_key_values(key)

        # Can't do fancy bit-matching cuz values might be in different order and/or at
        #   different positions
        for key in self.kit:
            match = True
            for value in key_values:
                if value not in key:
                    match = False
                    break

            if match:
                keys.append(key)

        return keys

    def __str__(self) -> str:
        """
        Function aim: Converts the class instance to a string representation
        Parameters: N/A
        Return: string
        """
        result = f'Table for {self.relation}:\n'

        for key in self.kit:
            result += '  {}  {:.8f}\n'.format(key, self.data[key])

        return result
