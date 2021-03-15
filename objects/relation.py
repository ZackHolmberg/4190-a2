from .helpers import value_to_variable
from typing import List, Union

class Relation:
    def __init__(self, relation: str, values: List[str]=[]):
        self.relation = relation
        self.is_conditional = '|' in relation
        self.is_joint = not self.is_conditional
        self.values = values

        if self.is_conditional:
            chunks = self.relation.split('|')
            assert(len(chunks) == 2)
            self.query_variables = chunks[0].split(',')
            self.evidence_variables = chunks[1].split(',')
            self.variables = self.evidence_variables + self.query_variables

            assert(len(self.query_variables) == 1 and len(self.evidence_variables) >= 1)
        else:
            self.variables = relation.split(',')
            
            assert(len(self.variables) > 0)


    def get_value_by_variable(self, variable: str) -> Union[str, None]:
        """
        Looks for assigned value that matches a variable.
        Example: values=['+r', '-t'], variable='R', returns='+r'
        """
        for value in self.values:
            v = value_to_variable(value)
            if v == variable:
                return value

        return None


    def __str__(self) -> str:
        return f'P({self.relation}), values={self.values}'
