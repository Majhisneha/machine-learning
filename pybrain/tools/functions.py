__author__ = 'Tom Schaul, tom@idsia.ch'

from scipy import array, exp, tanh, clip, log, dot, sqrt, power, pi, tan, diag, rand, real_if_close
from scipy.linalg import inv, det, svd, logm, expm

import warnings
warnings.filterwarnings("ignore") # suppress warnings for deprecated functions

# Data structures to keep track of branch coverage
branch_coverage_semilinear = {1: False, 2: False, 3: False, 4: False}
branch_coverage_explnPrime = {1: False, 2: False, 3: False, 4: False}

def printBranchCoverageSemilinear():
    print("Branch coverage for semilinear: ", branch_coverage_semilinear)
    print("Coverage is ", sum(branch_coverage_semilinear.values()) / len(branch_coverage_semilinear) * 100, "%")

def printBranchCoverageExplnPrime():
    print("Branch coverage for explnPrime: ", branch_coverage_semilinear)
    print("Coverage is ", sum(branch_coverage_explnPrime.values()) / len(branch_coverage_explnPrime) * 100, "%")

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


def semilinearPrime(x):
    """ This function is the first derivative of the semilinear function (above).
        It is needed for the backward pass of the module. """
    try:
        # assume x is a numpy array
        shape = x.shape
        x.flatten()
        x = x.tolist()
    except AttributeError:
        # no, it wasn't: build shape from length of list
        shape = (1, len(x))
    def f(val):
        if val < 0:
            # exponential function for x<0
            return safeExp(val)
        else:
            # linear function for x>=0
            return 1.0
    return array(list(map(f, x))).reshape(shape)


def safeExp(x):
    """ Bounded range for the exponential function (won't produce inf or NaN). """
    return exp(clip(x, -500, 500))


def sigmoid(x):
    """ Logistic sigmoid function. """
    return 1. / (1. + safeExp(-x))


def sigmoidPrime(x):
    """ Derivative of logistic sigmoid. """
    tmp = sigmoid(x)
    return tmp * (1 - tmp)


def tanhPrime(x):
    """ Derivative of tanh. """
    tmp = tanh(x)
    return 1 - tmp * tmp


def ranking(R):
    """ Produces a linear ranking of the values in R. """
    l = sorted(list(enumerate(R)), cmp=lambda a, b: cmp(a[1], b[1]))
    l = sorted(list(enumerate(l)), cmp=lambda a, b: cmp(a[1], b[1]))
    return array([kv[0] for kv in l])


def expln(x):
    """ This continuous function ensures that the values of the array are always positive.
        It is ln(x+1)+1 for x >= 0 and exp(x) for x < 0. """
    def f(val):
        if val < 0:
            # exponential function for x < 0
            return exp(val)
        else:
            # natural log function for x >= 0
            return log(val + 1.0) + 1
    try:
        result = array(list(map(f, x)))
    except TypeError:
        result = array(f(x))

    return result


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


def multivariateNormalPdf(z, x, sigma):
    """ The pdf of a multivariate normal distribution (not in scipy).
    The sample z and the mean x should be 1-dim-arrays, and sigma a square 2-dim-array. """
    assert len(z.shape) == 1 and len(x.shape) == 1 and len(x) == len(z) and sigma.shape == (len(x), len(z))
    tmp = -0.5 * dot(dot((z - x), inv(sigma)), (z - x))
    res = (1. / power(2.0 * pi, len(z) / 2.)) * (1. / sqrt(det(sigma))) * exp(tmp)
    return res


def simpleMultivariateNormalPdf(z, detFactorSigma):
    """ Assuming z has been transformed to a mean of zero and an identity matrix of covariances.
    Needs to provide the determinant of the factorized (real) covariance matrix. """
    dim = len(z)
    return exp(-0.5 * dot(z, z)) / (power(2.0 * pi, dim / 2.) * detFactorSigma)


def multivariateCauchy(mu, sigma, onlyDiagonal=True):
    """ Generates a sample according to a given multivariate Cauchy distribution. """
    if not onlyDiagonal:
        u, s, d = svd(sigma)
        coeffs = sqrt(s)
    else:
        coeffs = diag(sigma)
    r = rand(len(mu))
    res = coeffs * tan(pi * (r - 0.5))
    if not onlyDiagonal:
        res = dot(d, dot(res, u))
    return res + mu


def approxChiFunction(dim):
    """ Returns Chi (expectation of the length of a normal random vector)
    approximation according to: Ostermeier 1997. """
    dim = float(dim)
    return sqrt(dim) * (1 - 1 / (4 * dim) + 1 / (21 * dim ** 2))


def sqrtm(M):
    """ Returns the symmetric semi-definite positive square root of a matrix. """
    r = real_if_close(expm(0.5 * logm(M)), 1e-8)
    return (r + r.T) / 2

