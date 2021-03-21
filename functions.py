"""
Course: COMP 4190
Instructor: Cuneyt Akcora

Assignment 2

Submission by:
Yaroslav Mikhaylik, 7853156
Zack Holmberg, 7777823

File purpose: Contains the functions required by Q1

"""

from objects.factor import Factor
from objects.helpers import new_key_from_existing, value_to_variable
from typing import List


def observe(f: Factor, var: str, val: str) -> Factor:
    """
    Function aim: Restricts a variable to some value in a given factor.
    Parameters: Factor object reporesent factor to oberserve, and two strings var and val representing the variable and value to observe, respectively
    Return: Returns a Factor object
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
    Function aim: Function that multiplies two factors. The join is pretty much a pointwise product of entries
    of both tables, as explained in the course notes.
    Parameters: Two Factor objects to multiply together
    Return: Returns a Factor object
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
    Function aim: Function that sums out a variable in a given factor.
    Parameters: A Factor object and a string representing which variable to sum out
    Return: Returns a Factor object
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
    Function aim: Normalizes a factor by dividing each entry by the sum of all the entries.
    This is useful when the factor is a distribution (i.e. sum of the probabilities must be 1).
    Parameters: A Factor object to normalize
    Return: Returns a Factor object
    """
    the_sum = sum(f.data.values())
    for key in f.kit:
        f.data[key] = f.data[key]/the_sum
    assert(sum(f.data.values()) > 0.999999 and sum(f.data.values()) < 1.000001)
    return f


"""
function that 
Finally, the answer can be normalized if a probability distribution that sums up to 1 is desired.
"""


def inference(factor_list, query_variables, ordered_hidden_variables, evidence_list) -> Factor:
    """
    Function aim: Computes Pr(queryVariables|evidenceList) by variable elimination.
    This function restricts the factors in factorList according to the evidence in evidenceList.
    Next, it sums out the hidden variables from the product of the factors in factorList.
    The variables are summed out in the order given in orderedListOfHiddenVariables.
    Parameters: A List of Factor objects, a list of strings reporesenting Query variables, a list 
    of strings representing the ordered hidden variables and finally a list of strings representing evidence
    Return: Returns a Factor object representing the desired probability
    """
    new_factor_list = []
    real_hidden_vars = set()

    for factor in factor_list:
        # Extract all variables across all factors
        for variable in factor.relation.variables:
            real_hidden_vars.add(variable)

    # Observe the evidence values in each factor, and remove evidence variables from real_hidden_vars
    for factor in factor_list:
        for evidence in evidence_list:
            var = value_to_variable(evidence)
            val = evidence[0]
            factor = observe(factor, var, val)
            real_hidden_vars.discard(var)

        new_factor_list.append(factor)

    # Remove query variables from real_hidden_vars
    for var in query_variables:
        real_hidden_vars.discard(var)

    print('>: Leftover hidden variables to sum out:', real_hidden_vars)
    print('>: Elimination order:', ordered_hidden_variables)

    # Sum out remaining hidden variables according to the order, and join the factors together
    for hidden_var in ordered_hidden_variables:
        if hidden_var not in real_hidden_vars:
            continue

        print('>: Eliminating:', hidden_var)

        to_join = []

        # Join all factors mentioning hidden_var
        for factor in new_factor_list:
            if hidden_var in factor.relation.variables:
                to_join.append(factor)

        print(f'>: Joining and summing out {len(to_join)} factors:', [
              str(f.relation) for f in to_join])
        temp_factor = to_join[0]
        new_factor_list.remove(temp_factor)

        for i in range(1, len(to_join)):
            print(
                f'>: Joining {temp_factor.relation} with {to_join[i].relation}')

            new_factor_list.remove(to_join[i])
            temp_factor = multiply(temp_factor, to_join[i])

            print(temp_factor)

        print(f'>: Done joining {len(to_join)} factors')

        # We additionally handle edge case when attempting to sum out X in P(X|Y), if this factor is not used at all
        #   In such cases we just avoid saving the unused factors
        if (temp_factor.relation.is_conditional and len(temp_factor.relation.query_variables) == 1 and temp_factor.relation.query_variables[0] == hidden_var) or \
                (temp_factor.relation.is_joint and len(temp_factor.relation.variables) == 1 and temp_factor.relation.variables[0] == hidden_var):
            print('>: Omitting this unused factor:', temp_factor.relation)
        else:
            temp_factor = sumout(temp_factor, hidden_var)
            print('>: After summing out', hidden_var)
            print(temp_factor)
            new_factor_list.append(temp_factor)

    # One more join across all factors to get a joint probability
    temp_factor = new_factor_list[0]
    for i in range(1, len(new_factor_list)):
        temp_factor = multiply(temp_factor, new_factor_list[i])

    print('>: Final join of remaining factor')
    print(temp_factor)

    # Construct the final table of probabilities via normalization
    temp_factor = normalize(temp_factor)

    print('>: Normalized factor')
    print(temp_factor)

    conditional_vars = [
        v for v in temp_factor.relation.variables if v not in query_variables]

    if conditional_vars:
        new_relation = ','.join(query_variables) + '|' + \
            ','.join(conditional_vars)
    else:
        new_relation = ','.join(query_variables)

    new_f = Factor(new_relation, list(set(temp_factor.relation.values)))
    for key in new_f.kit:
        keys = temp_factor.find_fuzzy_keys(key)
        assert(len(keys) == 1)

        new_f.data[key] = temp_factor.data[keys[0]]

    return new_f
