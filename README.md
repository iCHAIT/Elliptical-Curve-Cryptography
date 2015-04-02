## Elliptical Curve Cryptography


* **ECC**

Elliptic Curve Cryptography (ECC) is a **public key cryptography**. 

![ScreenShot](/images/publickey.png)

In public key cryptography each user or the device taking part in the communication generally have a pair of keys, a **public key** and a **private key**, and a set of operations associated with the keys to do the cryptographic operations. Only the particular user knows the private key whereas the public key is distributed to all users taking part in the communication.

The mathematical operations of ECC is defined over the elliptic curve **y2 = x3 + ax + b**, where **4a3 + 27b2 ≠ 0**. Each value of the ‘a’ and ‘b’ gives a different elliptic curve.

One main **advantage** of ECC is its **small key size**. A 160-bit key in ECC is considered to be as secured as 1024-bit key in RSA.


* **Point Multiplication**

In point multiplication a point P on the elliptic curve is multiplied with a **scalar k** using elliptic curve equation to obtain another point Q on the same elliptic curve.

i.e. **kP=Q**

Point multiplication is achieved by two basic elliptic curve operations
    * **Point addition**, adding two points J and K to obtain another point L, i.e  **(L = J + K)**
    * **Point doubling**, adding a point J to itself to obtain another point L, i.e **(L = 2J)**


* **Point Addition**

Point addition is the addition of two points J and K on an elliptic curve to obtain another point L on the same elliptic curve.

![ScreenShot](/images/pointadd.png)

Consider two points J and K on an elliptic curve as shown in the above figure. If K ≠ -J then a line drawn through the points J and K will intersect the elliptic curve at exactly one more point –L. The reflection of the point –L with respect to x-axis gives the point L, which is the result of addition of points J and K.

Thus on an **elliptic curve L = J + K**.


* **Point Doubling**

Point doubling is the addition of a point J on the elliptic curve to itself to obtain another point L on the same elliptic curve.

![ScreenShot](/images/pointmult.png)

To double a point J to get L, i.e. to find L = 2J, consider a point J on an elliptic curve as shown in the above figure. If y coordinate of the point J is not zero then the tangent line at J will intersect the elliptic curve at exactly one more point –L. The reflection of the point –L with respect to x-axis gives the point L, which is the result of doubling the point J.

Thus **L = 2J**.


## TODO

* **Elgamal**

* **ECDSA**

* **ECDH**
