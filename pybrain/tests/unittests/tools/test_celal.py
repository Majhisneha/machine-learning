from pybrain.tools.functions import printBranchCoverageSemilinear, printBranchCoverageExplnPrime, semilinear, explnPrime
from scipy import array

print("Branch coverage for semilinear before calling the function: ")
printBranchCoverageSemilinear()

semilinear(array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
print("Branch coverage for semilinear after Test 1: ")
printBranchCoverageSemilinear()

semilinear(array([-1, -2, -3, -4, -5, -6, -7, -8, -9, -10]))
print("Branch coverage for semilinear after Test 2: ")
printBranchCoverageSemilinear()

semilinear((1,1)) 
print("Branch coverage for semilinear after Test 3: ")
printBranchCoverageSemilinear()

print("Full branch coverage for semilinear achieved")

print("Branch coverage for explnPrime before calling the function: ")
printBranchCoverageExplnPrime()

explnPrime(array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
print("Branch coverage for explnPrime after Test 1: ")
printBranchCoverageExplnPrime()

explnPrime(array([-1, -2, -3, -4, -5, -6, -7, -8, -9, -10]))
print("Branch coverage for explnPrime after Test 2: ")
printBranchCoverageExplnPrime()

explnPrime(404)
print("Branch coverage for explnPrime after Test 3: ")
printBranchCoverageExplnPrime()

print("Full branch coverage for explnPrime achieved")
