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
    Function that multiplies two factors. The function tries to automatically figure out
    on what variable to perform the join.
    """
    joint_factor = f1 if f1.relation.is_joint else f2
    conditional_factor = f1 if f1.relation.is_conditional else f2

    assert(joint_factor.relation.is_joint)
    assert(conditional_factor.relation.is_conditional)

    # Automatic detection of variable to join on. Works with in-class examples, but may
    #   misbehave pretty badly with any other factors
    joint_rel = joint_factor.relation
    cond_rel = conditional_factor.relation
    joining_var = list(set(joint_rel.variables).intersection(set(cond_rel.variables)))[0]

    new_relation = ','.join(joint_rel.variables + [var for var in cond_rel.variables if var != joining_var])
    new_f = Factor(new_relation, joint_rel.values + cond_rel.values)

    for key in new_f.kit:
        joint_key = new_key_from_existing(key, joint_rel.variables)
        cond_key = new_key_from_existing(key, cond_rel.variables)

        new_f.data[key] = conditional_factor.data[cond_key] * joint_factor.data[joint_key]

    return new_f


def sumout(f: Factor, v: str) -> Factor:
    """
    Function that sums out a variable in a given factor.
    """
    assert(not f.relation.is_conditional)
    assert(v in f.relation.variables)
    assert(len(f.relation.variables) > 1)

    remaining_vars = [var for var in f.relation.variables if var != v]
    new_f = Factor(','.join(remaining_vars), f.relation.values)

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
