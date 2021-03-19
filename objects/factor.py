from typing import List
from .key_iterator import KeyIterator
from .relation import Relation
from .helpers import get_key_values


class Factor:
    def __init__(self, relation: str, known_values: List[str] = []):
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
        Matches keys fuzzily to a given key. Sort of like filtering.
        Example: key='+r-t'
        Will return ['+r-t-l', '+r-t+l', ... other keys tha thave '+r-t' in them]
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
        result = f'Table for {self.relation}:\n'

        for key in self.kit:
            result += '  {}  {:.8f}\n'.format(key, self.data[key])

        return result
