
"""
function that restricts a variable to some value in agiven factor.
"""


def observe(factor, variable, value):
    # TODO: Implement
    print()


"""
 function that multiplies two factors.
"""


def multiply(factor1, factor2):
    # TODO: Implement
    print()


"""
function that sums out a variable in a given factor.
"""


def sumout(factor, variable):
    # TODO: Implement
    print()


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
