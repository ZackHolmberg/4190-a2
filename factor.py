

class Factor:
    def __init__(self, variables, relation):
        self.data = {}
        self.variables = variables
        self.relation = relation

    def generate_keys(self, probabilities=None):
        n = len(self.variables)
        for i in range(2 ** n):
            key = ''

            for j in range(n):
                variable = self.variables[j]
                is_plus = bool((i >> (n - j - 1)) & 1)

                if is_plus:
                    key += f'+{variable}'
                else:
                    key += f'-{variable}'

            if probabilities:
                self.data[key] = probabilities[i]
            else:
                self.data[key] = 0
