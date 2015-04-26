# Basics of Elliptic Curve Cryptography implementation on Python
from Crypto.Cipher import AES
from hashlib import md5
import hashlib
import base64
import os
import collections
import eclib

if __name__ == "__main__":
    print("\nFILE CONTENT\n")
    
    file='./context.txt'

    txt = (open(file,'r')).read()
    print txt

    # shared elliptic curve system of examples
    print "ENTER DOMAIN PARAMETERS : "
    print "Enter value of a : "
    a=int(raw_input())#1
    print "Enter value of b : "
    b=int(raw_input())#18
    print "Enter value of q : "
    q=int(raw_input())#19
    ec = eclib.EC(a,b,q)
    g, _ = ec.at(7)
    assert ec.order(g) <= ec.q

    # ECDH usage
    dh = eclib.DiffieHellman(ec, g)
    
    
    print("Enter private key for A")
    apriv = int(raw_input()) #11   
    apub = dh.gen(apriv)
    print "Public key is",apub

