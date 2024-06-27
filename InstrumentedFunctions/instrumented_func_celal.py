__author__ = 'Tom Schaul, tom@idsia.ch'

import warnings
warnings.filterwarnings("ignore") # suppress warnings for deprecated functions

from scipy import array, exp, clip

def safeExp(x):
    """ Bounded range for the exponential function (won't produce inf or NaN). """
    return exp(clip(x, -500, 500))

def printBranchCoverage(branch_coverage, function_name):
    print("Branch coverage for ", function_name, " ", branch_coverage)
    print("Coverage is ", sum(branch_coverage.values()) / len(branch_coverage) * 100, "%")

# Data structures to keep track of branch coverage
branch_coverage_semilinear = {1: False, 2: False, 3: False, 4: False}
branch_coverage_explnPrime = {1: False, 2: False, 3: False, 4: False}

def semilinear(x):
    """ This function ensures that the values of the array are always positive. It is
        x+1 for x=>0 and exp(x) for x<0. """    
    # Branch 1
    try:
        branch_coverage_semilinear[1] = True
        # assume x is a numpy array
        shape = x.shape
        x.flatten()
        x = x.tolist()
    # Branch 2
    except AttributeError:
        branch_coverage_semilinear[2] = True
        # no, it wasn't: build shape from length of list
        shape = (1, len(x))
    def f(val):
        # Branch 3
        if val < 0:
            branch_coverage_semilinear[3] = True
            # exponential function for x<0
            return safeExp(val)
        # Branch 4
        else:
            branch_coverage_semilinear[4] = True
            # linear function for x>=0
            return val + 1.0
        
    return array(list(map(f, x))).reshape(shape)


def explnPrime(x):
    """ This function is the first derivative of the expln function (above).
        It is needed for the backward pass of the module. """
    def f(val):
        # Branch 1
        if val < 0:
            branch_coverage_explnPrime[1] = True
            # exponential function for x<0
            return exp(val)
        # Branch 2
        else:
            branch_coverage_explnPrime[2] = True
            # linear function for x>=0
            return 1.0 / (val + 1.0)
    # Branch 3
    try:
        branch_coverage_explnPrime[3] = True
        result = array(list(map(f, x)))
    # Branch 4
    except TypeError:
        branch_coverage_explnPrime[4] = True
        result = array(f(x))

    return result

print("Branch coverage for semilinear before calling the function: ")
printBranchCoverage(branch_coverage_semilinear, "semilinear")

semilinear(array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
print("Branch coverage for semilinear after Test 1: ")
printBranchCoverage(branch_coverage_semilinear, "semilinear")

semilinear(array([-1, -2, -3, -4, -5, -6, -7, -8, -9, -10]))
print("Branch coverage for semilinear after Test 2: ")
printBranchCoverage(branch_coverage_semilinear, "semilinear")

semilinear((1,1))
print("Branch coverage for semilinear after Test 3: ")
printBranchCoverage(branch_coverage_semilinear, "semilinear")

print("Full branch coverage for semilinear achieved")

print("Branch coverage for explnPrime before calling the function: ")
printBranchCoverage(branch_coverage_explnPrime, "explnPrime")

explnPrime(array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
print("Branch coverage for explnPrime after Test 1: ")
printBranchCoverage(branch_coverage_explnPrime, "explnPrime")

explnPrime(array([-1, -2, -3, -4, -5, -6, -7, -8, -9, -10]))
print("Branch coverage for explnPrime after Test 2: ")
printBranchCoverage(branch_coverage_explnPrime, "explnPrime")

explnPrime(404)
print("Branch coverage for explnPrime after Test 3: ")
printBranchCoverage(branch_coverage_explnPrime, "explnPrime")

print("Full branch coverage for explnPrime achieved")
