import numpy as np
import py5

# Cocharacter of some matrix group
# This should take as input a complex number and return a matrix
def cochar(z):
    return np.matrix([[z.real, -z.imag], [z.imag, z.real]])

# Complex-valued function on matrices to be iterated for fractal
def mat_fun(zmat, cmat):
    return zmat**2 + cmat



def setup():
    py5.size(500, 500)

def draw():
