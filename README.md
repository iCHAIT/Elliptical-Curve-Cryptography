## Elliptical Curve Cryptography


Elliptic Curve Cryptography (ECC) is a **public key cryptography**. 

![ScreenShot](/images/publickey.png)

In public key cryptography each user or the device taking part in the communication generally have a pair of keys, a **public key** and a **private key**, and a set of operations associated with the keys to do the cryptographic operations. Only the particular user knows the private key whereas the public key is distributed to all users taking part in the communication.

The public key is a point on the curve and the private key is a random number. The public key is obtained by multiplying the private key with a generator point G in the curve.

The mathematical operations of ECC is defined over the elliptic curve **y^2 = x^3 + ax + b**, where **4a^3 + 27b^2 ≠ 0**. Each value of the ‘a’ and ‘b’ gives a different elliptic curve.

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



## ECDSA(Elliptic Curve Digital Signature Algorithm)

Signature algorithm is used for authenticating a device or a message sent by the device. For example consider two devices A and B. To authenticate a message sent by A, the device A **signs the message using its private key**. The device A sends the message and the signature to the device B. This signature can be **verified only by using the public key** of device A. Since the device B knows A’s public key, it can verify whether the message is indeed send by A or not.

ECDSA is a variant of the **Digital Signature Algorithm (DSA)** that operates on elliptic curve groups. For sending a signed message from A to B, both have to agree up on **Elliptic Curve domain parameters**. Sender ‘A’ have a key pair consisting of a private key dA (a randomly selected integer less than n, where n is the order of the curve, an elliptic curve domain parameter) and a public key QA = dA * G (G is the generator point, an elliptic curve domain parameter). An overview of ECDSA process is defined below.

ECDSA has three phases -
* **key generation**
* **signature generation**
* **signature verification**


### ECDSA Key Generation

An entity A’s key pair is associated with a particular set of EC domain parameters D= (q, FR, a, b, G, n, h). E is an elliptic curve defined over Fq , and P is a point of prime order n in E(Fq), q is a prime. Each entity A does the following -

1. Select a random integer d in the interval [1, n- 1]. 
2. Compute Q = dP.
3. A’s public key is Q, A’s private key is d.


### ECDSA Signature Generation

To sign a message m, an entity A with domain parameters D= (q,
FR, a, b, G, n, h) does the following -

1. Select a random or pseudorandom integer k in the interval [1, n-1].
2. Compute kP =x1, y1 and r= x1 mod(n) (where x1 is regarded as an integer between 0 and q-1). If r= 0 then go back to step 1.
3. Compute k^(-1) mod(n).
4. Compute s= k^(-1) {h(m)+ dr} mod(n), where h is the Secure Hash Algorithm (SHA-1). If s = 0, then go back to step 1.
5. The signature for the message m is the pair of integers (r, s).



![ScreenShot](/images/siggen.png)



### ECDSA Signature Verification

To verify A’s signature (r, s) on m, B obtains an authenticated copy of A’s domain parameters D = (q, FR, a, b, G, n, h) and public key Q and do the following -

1. Verify that r and s are integers in the interval [1, n-1].
2. Compute w = s^(-1)mod(n) and h(m)
3. Compute u1 =h(m)w mod(n) and u2 =rw mod(n).
4. Compute u1P + u2Q =(x0, y0) and v= x0 mod(n).
5. Accept the signature if and only if v = r



![ScreenShot](/images/sigver.png)



## ECDH(Elliptic curve Diffie–Hellman)

Elliptic curve Diffie–Hellman (ECDH) is an anonymous **key agreement protocol**that allows two parties, each having an elliptic curve **public–private key pair**, to establish a **shared secret** over an insecure channel.
This shared secret may be directly used as a key, or to derive another key which can then be used to encrypt subsequent communications using a symmetric key cipher.

Both parties exchange some public information to each other. Using this public data and their own private data these parties calculates the shared secret. Any third party, who doesn’t have access to the private details of each device, will not be able to calculate the shared secret from the available public information.

An overview of ECDH process is defined below -

For generating a shared secret between A and B using ECDH, both have to agree up on Elliptic Curve domain parameters. Both end have a key pair consisting of a **private key d** (a randomly selected integer less than n, where n is the order of the curve, an elliptic curve domain parameter) and a **public key Q = d * G** (G is the generator point, an elliptic curve domain parameter). Let **(dA, QA)** be the private key - public key pair of A and **(dB, QB)** be the private key - public key pair of B.

1. The end A computes K = (xK,yK) = dA *QB
2. The end B computes L = (xL,yL) = dB *QA
3. Since dA*QB = dA*dB*G = dB*dA*G = dB*QA. Therefore K = L and hence xK = xL
4. Hence the shared secret is xK

Since it is practically impossible to find the private key dA or dB from the public key K or L, its not possible to obtain the shared secret for a third party.



![ScreenShot](/images/ecdh.png)