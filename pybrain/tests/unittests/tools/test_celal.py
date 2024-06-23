import numpy as np
from pybrain.tools.functions import semilinear, explnPrime
from pybrain.tests import runModuleTestSuite


def test_semilinear(self):
    x = np.array([0, 1, 2, 3])
    expected = np.array([1, 2, 3, 4])
    np.testing.assert_array_equal(semilinear(x), expected)
    
    x = np.array([-1, -2, -3])
    expected = np.exp(x)
    np.testing.assert_array_equal(semilinear(x), expected)
    
    x = np.array([-1, 0, 1])
    expected = np.array([np.exp(-1), 1, 2])
    np.testing.assert_array_equal(semilinear(x), expected)

def test_explnPrime(self):
    x = np.array([0, 1, 2, 3])
    expected = np.array([1, 0.5, 1/3, 0.25])
    np.testing.assert_array_equal(explnPrime(x), expected)
    
    x = np.array([-1, -2, -3])
    expected = np.exp(x)
    np.testing.assert_array_equal(explnPrime(x), expected)
    
    x = np.array([-1, 0, 1])
    expected = np.array([np.exp(-1), 1, 0.5])
    np.testing.assert_array_equal(explnPrime(x), expected)

if __name__ == "__main__":
    runModuleTestSuite(__import__('__main__'))
