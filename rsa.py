import os
import numpy
import random
from fractions import gcd
import math
# from sympy import *

a = raw_input("Enter a large prime no P:")

b = raw_input("Enter another large prime no Q:")

p = int(a)
q = int(b)

i = 2

# print sympy.prime(p)


for i in range(2, p/2):
	if p % i == 0:
	    print "ERROR: P is not prime"
	    break


for i in range(2, q/2):
	if q % i == 0:
	    print "ERROR: Q is not prime"
	    break

