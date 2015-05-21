import sys
import random
from fractions import gcd
import sympy

a = raw_input("Enter a large prime no P:")

b = raw_input("Enter another large prime no Q:")

p = int(a)

if not sympy.isprime(p):
    print "ERROR p is not prime"
    sys.exit()

q = int(b)

if not sympy.isprime(q):
    print "ERROR q is not prime"
    sys.exit()

f = (p-1)*(q-1)

n = p*q

while 1:
    # Choosing a random no. e such that 1<e<f and e is coprime to f
    e = random.randint(1, f)
    if gcd(e, f) == 1:   # Condition for coprime
        break

for i in range(1, n-1):
    if ((i * e) % f) == 1:
        d = i         # d is private key.
        break

print "Public Key is:", e, n

print "Private Key is:", d, n

msg = raw_input("Enter the message:")

cipher_enc = []

for c in msg:
    cipher_enc.append(pow(ord(c), e, n))
print "Encrypted message:", cipher_enc

cipher_dec = []

for c in cipher_enc:
    cipher_dec.append(chr(pow(c, d, n)))
print "Decrypted message:", cipher_dec
