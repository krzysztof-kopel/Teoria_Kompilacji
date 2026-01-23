import numpy as np

def better_mul(a, b):
    if type(a) == str and type(b) == int:
        return a * b
    else:
        return np.dot(a, b)
