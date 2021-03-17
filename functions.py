from objects.factor import Factor
from objects.helpers import new_key_from_existing
from typing import List


"""
function that restricts a variable to some value in agiven factor.
"""


def observe(factor, variable, value):
    # TODO: Implement
    print()


def multiply(f1: Factor, f2: Factor) -> Factor:
    """
    Function that multiplies two factors. The join is pretty much a pointwise product of entries
    of both tables, as explained in the course notes.
    """
    # For the new factor we extract what variables should be on the left of '|' and what variables
    #   should be on the right of '|'
    variables_on_the_left = set()
    variables_all = set()
    for f in [f1, f2]:
        if f.relation.is_conditional:
            variables_on_the_left = variables_on_the_left.union(set(f.relation.query_variables))
        else:
            variables_on_the_left = variables_on_the_left.union(set(f.relation.variables))

        variables_all = variables_all.union(set(f.relation.variables))
    variables_on_the_right = list(variables_all.difference(variables_on_the_left))
    variables_on_the_left = list(variables_on_the_left)

    # If there are no variables on the right of '|', then the new factor is a joint factor,
    #   otherwise it is a conditional factor
    if len(variables_on_the_right) == 0:
        new_relation = ','.join(variables_on_the_left)
    else:
        new_relation = ','.join(variables_on_the_left) + '|' + ','.join(variables_on_the_right)

    new_f = Factor(new_relation, list(set(f1.relation.values + f2.relation.values)))

    for key in new_f.kit:
        f1_key = new_key_from_existing(key, f1.relation.variables)
        f2_key = new_key_from_existing(key, f2.relation.variables)

        new_f.data[key] = f1.data[f1_key] * f2.data[f2_key]

    return new_f


def sumout(f: Factor, v: str) -> Factor:
    """
    Function that sums out a variable in a given factor.
    """
    assert(v in f.relation.variables)
    assert(len(f.relation.variables) > 1)


    variables_on_the_left = set()
    variables_all = set(f.relation.variables)
    if f.relation.is_conditional:
        variables_on_the_left = variables_on_the_left.union(set(f.relation.query_variables))
    else:
        variables_on_the_left = variables_on_the_left.union(set(f.relation.variables))

    variables_on_the_left.discard(v)
    variables_all.discard(v)

    variables_on_the_right = list(variables_all.difference(variables_on_the_left))
    variables_on_the_left = list(variables_on_the_left)

    # If there are no variables on the right of '|', then the new factor is a joint factor,
    #   otherwise it is a conditional factor
    if len(variables_on_the_right) == 0:
        new_relation = ','.join(variables_on_the_left)
    else:
        new_relation = ','.join(variables_on_the_left) + '|' + ','.join(variables_on_the_right)

    new_f = Factor(new_relation, list(set(f.relation.values)))

    for key in new_f.kit:
        keys = f.find_fuzzy_keys(key)

        s = 0
        for k in keys:
            s += f.data[k]

        new_f.data[key] = s

    return new_f


"""
function that normalizes a factor by dividing each entry by thesum of all the entries. 
This is useful when the factor is a distribution (i.e. sum of the probabilities must be1).
"""


def normalize(factor):
    # TODO: Implement
    print()


"""
function that computes Pr(queryVariables|evidenceList) by variable elimination. 
This function shouldrestrict the factors in factorListaccording to the evidence in evidenceList. 
Next, it should sum-out thehidden variables from the product of the factors in factorList. 
The variables should be summed out inthe order given in orderedListOfHiddenVariables. 
Finally, the answer can be normalized if a probabilitydistribution that sums up to 1 is desired
"""


def inference(factorList, queryVariables, orderedListOfHiddenVariables, evidenceList):
    # TODO: Implement
    print()
