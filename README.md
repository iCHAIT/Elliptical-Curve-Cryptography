## Elliptical Curve Cryptography


Elliptic Curve Cryptography (ECC) is a **public key cryptography**. 

![ScreenShot](/images/publickey.png)

In public key cryptography each user or the device taking part in the communication generally have a pair of keys, a **public key** and a **private key**, and a set of operations associated with the keys to do the cryptographic operations. Only the particular user knows the private key whereas the public key is distributed to all users taking part in the communication.

The mathematical operations of ECC is defined over the elliptic curve **y2 = x3 + ax + b**, where **4a3 + 27b2 ≠ 0**. Each value of the ‘a’ and ‘b’ gives a different elliptic curve.

One main **advantage** of ECC is its **small key size**. A 160-bit key in ECC is considered to be as secured as 1024-bit key in RSA.


## Point Multiplication

In point multiplication a point P on the elliptic curve is multiplied with a **scalar k** using elliptic curve equation to obtain another point Q on the same elliptic curve.

i.e. **kP=Q**

Point multiplication is achieved by two basic elliptic curve operations
*  **Point addition**, adding two points J and K to obtain another point L, i.e  **(L = J + K)**
* **Point doubling**, adding a point J to itself to obtain another point L, i.e **(L = 2J)**


### Point Addition

Point addition is the addition of two points J and K on an elliptic curve to obtain another point L on the same elliptic curve.

![ScreenShot](/images/pointadd.png)

Consider two points J and K on an elliptic curve as shown in the above figure. If K ≠ -J then a line drawn through the points J and K will intersect the elliptic curve at exactly one more point –L. The reflection of the point –L with respect to x-axis gives the point L, which is the result of addition of points J and K.

Thus on an **elliptic curve L = J + K**.


### Point Doubling

Point doubling is the addition of a point J on the elliptic curve to itself to obtain another point L on the same elliptic curve.

![ScreenShot](/images/pointmult.png)

To double a point J to get L, i.e. to find L = 2J, consider a point J on an elliptic curve as shown in the above figure. If y coordinate of the point J is not zero then the tangent line at J will intersect the elliptic curve at exactly one more point –L. The reflection of the point –L with respect to x-axis gives the point L, which is the result of doubling the point J.

Thus **L = 2J**.


## ElGamal Encryption

In cryptography, the ElGamal encryption system is an **asymmetric key encryption** algorithm for **public-key** cryptography which is based on the **Diffie–Hellman key exchange**. It was described by Taher Elgamal in 1985.

ElGamal has the **disadvantage** that the ciphertext is twice as long as the plaintext.

It has the **advantage** the same plaintext gives a different ciphertext (with near certainty) each time it is encrypted

ElGamal encryption consists of three components -

* **The key generator**
* **The encryption algorithm**
* **The decryption algorithm**


### Key Generation

The key generator works as follows -

* Alice generates an efficient description of a cyclic group G, of order q with generator g.
* Alice chooses a random x, from {1,.........., q-1}.
* Alice computes h = g^x.
* Alice publishes h, along with the description of G, q, g as her public key. Alice retains x as her private key which must be kept secret.


### Encryption

The encryption algorithm works as follows - to encrypt a message m, to Alice under her public key (G,q,g,h)

* Bob chooses a random y, from {1,............, q-1}, then calculates c1=g^y.
* Bob calculates the shared secret s=h^y.
* Bob converts his secret message m, into an element m' of G.
* Bob calculates c2=m'*s.
* Bob sends the ciphertext (c1,c2)=(g^y, m'*h^y)=(g^y, m'*(g^x)^y), to Alice.

Note that one can easily find h^y, if one knows m'.
Therefore, a new y, is generated for every message to improve security. For this reason, y, is also called an **ephemeral key**.


### Decryption

The decryption algorithm works as follows: to decrypt a ciphertext (c1,c2) with her private key x,

* Alice calculates the shared secret s=c1^x,
* and then computes m'=c2*(s^(-1)), which she then converts back into the plaintext message m, where s^(-1) is the inverse of s in the group G.
The decryption algorithm produces the intended message, since

**c2*(s^(-1)) = m'*h^y*(g^{xy})^(-1) = m'*g^{xy}*g^{-xy} = m'.**


### Security

The security of the ElGamal scheme depends on the properties of the underlying group G as well as any padding scheme used on the messages.

If the **computational Diffie–Hellman assumption (CDH)** holds in the underlying cyclic group G, then the encryption function is **one-way**.

If the **decisional Diffie–Hellman assumption (DDH)** holds in G, then ElGamal achieves **semantic security**.

ElGamal encryption is unconditionally malleable, and therefore is not secure under chosen ciphertext attack. For example, given an encryption (c1, c2) of some (possibly unknown) message m, one can easily construct a valid encryption (c1, 2c2) of the message 2m.

To achieve chosen-ciphertext security, the scheme must be further modified, or an appropriate padding scheme must be used.


![ScreenShot](/images/elgamal.png)



## TODO

* **ECDSA**

* **ECDH**
