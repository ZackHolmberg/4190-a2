from objects.factor import Factor
from objects.helpers import new_key_from_existing, value_to_variable
from typing import List


def observe(f: Factor, var: str, val: str) -> Factor:
    """
    function that restricts a variable to some value in a given factor.
    """
    assert(len(f.relation.variables) > 0)
    assert(val == '+' or val == '-')

    new_f = Factor(f.relation.relation,
                   [val + var.lower()]+f.relation.values)

    for key in new_f.kit:
        new_f.data[key] = f.data[key]

    return new_f


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
            variables_on_the_left = variables_on_the_left.union(
                set(f.relation.query_variables))
        else:
            variables_on_the_left = variables_on_the_left.union(
                set(f.relation.variables))

        variables_all = variables_all.union(set(f.relation.variables))
    variables_on_the_right = list(
        variables_all.difference(variables_on_the_left))
    variables_on_the_left = list(variables_on_the_left)

    # If there are no variables on the right of '|', then the new factor is a joint factor,
    #   otherwise it is a conditional factor
    if len(variables_on_the_right) == 0:
        new_relation = ','.join(variables_on_the_left)
    else:
        new_relation = ','.join(variables_on_the_left) + \
            '|' + ','.join(variables_on_the_right)

    new_f = Factor(new_relation, list(
        set(f1.relation.values + f2.relation.values)))

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
        variables_on_the_left = variables_on_the_left.union(
            set(f.relation.query_variables))
    else:
        variables_on_the_left = variables_on_the_left.union(
            set(f.relation.variables))

    variables_on_the_left.discard(v)
    variables_all.discard(v)

    variables_on_the_right = list(
        variables_all.difference(variables_on_the_left))
    variables_on_the_left = list(variables_on_the_left)

    # If there are no variables on the right of '|', then the new factor is a joint factor,
    #   otherwise it is a conditional factor
    if len(variables_on_the_right) == 0:
        new_relation = ','.join(variables_on_the_left)
    else:
        new_relation = ','.join(variables_on_the_left) + \
            '|' + ','.join(variables_on_the_right)

    new_f = Factor(new_relation, list(set(f.relation.values)))

    for key in new_f.kit:
        keys = f.find_fuzzy_keys(key)

        s = 0
        for k in keys:
            s += f.data[k]

        new_f.data[key] = s

    return new_f


def normalize(f: Factor) -> Factor:
    """
    function that normalizes a factor by dividing each entry by the sum of all the entries.
    This is useful when the factor is a distribution (i.e. sum of the probabilities must be1).
    """
    the_sum = sum(f.data.values())
    for key in f.kit:
        f.data[key] = f.data[key]/the_sum
    assert(sum(f.data.values()) == 1.0)
    return f


"""
function that computes Pr(queryVariables|evidenceList) by variable elimination.
This function shouldrestrict the factors in factorListaccording to the evidence in evidenceList.
Next, it should sum-out thehidden variables from the product of the factors in factorList.
The variables should be summed out inthe order given in orderedListOfHiddenVariables.
Finally, the answer can be normalized if a probabilitydistribution that sums up to 1 is desired
"""


def inference(factor_list, query_variables, ordered_hidden_variables, evidence_list):
    # 1. Observe variables in factorList according to the evidence in evidenceList
    new_factor_list = []
    for factor in factor_list:
        for evidence in evidence_list:
            var = value_to_variable(evidence)
            val = evidence[0]
            factor = observe(factor, var, val)
        new_factor_list.append(factor)

    for hidden_var in ordered_hidden_variables:
        to_join = []
        # Join all factors mentioning hidden_var
        for factor in new_factor_list:
            if hidden_var in factor.relation.variables:
                to_join.append(factor)
        temp_factor = to_join[0]
        new_factor_list.remove(temp_factor)
        for i in range(1, len(to_join)):
            new_factor_list.remove(to_join[i])
            temp_factor = multiply(temp_factor, to_join[i])
        temp_factor = sumout(temp_factor, hidden_var)
        new_factor_list.append(temp_factor)

    temp_factor = new_factor_list[0]
    for i in range(1, len(new_factor_list)):
        temp_factor = multiply(temp_factor, new_factor_list[i])

    for var in query_variables:
        temp_factor = sumout(temp_factor, var)

    to_return = normalize(temp_factor)
    return to_return
