import os, sys 
from PyQt4 import QtGui, QtCore 
import collections

def inv(n, q):
    """div on PN modulo a/b mod q as a * inv(b, q) mod q
    >>> assert n * inv(n, q) % q == 1
    """
    for i in range(q):
        if (n * i) % q == 1:
            return i
        pass
    assert False, "unreached"
    pass
 
 
def sqrt(n, q):
    """sqrt on PN modulo: returns two numbers or exception if not exist
    >>> assert (sqrt(n, q)[0] ** 2) % q == n
    >>> assert (sqrt(n, q)[1] ** 2) % q == n
    """
    assert n < q
    for i in range(1, q):
        if i * i % q == n:
            return (i, q - i)
        pass
    raise Exception("not found")
 
 
Coord = collections.namedtuple("Coord", ["x", "y"])
 
 
class EC(object):
    """System of Elliptic Curve"""
    def __init__(self, a, b, q):
        """elliptic curve as: (y**2 = x**3 + a * x + b) mod q
        - a, b: params of curve formula
        - q: prime number
        """
        assert 0 < a and a < q and 0 < b and b < q and q > 2
        assert (4 * (a ** 3) + 27 * (b ** 2))  % q != 0
        self.a = a
        self.b = b
        self.q = q
        # just as unique ZERO value representation for "add": (not on curve)
        self.zero = Coord(0, 0)
        pass
 
    def is_valid(self, p):
        if p == self.zero: return True
        l = (p.y ** 2) % self.q
        r = ((p.x ** 3) + self.a * p.x + self.b) % self.q
        return l == r
 
    def at(self, x):
        """find points on curve at x
        - x: int < q
        - returns: ((x, y), (x,-y)) or not found exception
        >>> a, ma = ec.at(x)
        >>> assert a.x == ma.x and a.x == x
        >>> assert a.x == ma.x and a.x == x
        >>> assert ec.neg(a) == ma
        >>> assert ec.is_valid(a) and ec.is_valid(ma)
        """
        assert x < self.q
        ysq = (x ** 3 + self.a * x + self.b) % self.q
        y, my = sqrt(ysq, self.q)
        return Coord(x, y), Coord(x, my)
 
    def neg(self, p):
        """negate p
        >>> assert ec.is_valid(ec.neg(p))
        """
        return Coord(p.x, -p.y % self.q)
 
    def add(self, p1, p2):
        """<add> of elliptic curve: negate of 3rd cross point of (p1,p2) line
        >>> d = ec.add(a, b)
        >>> assert ec.is_valid(d)
        >>> assert ec.add(d, ec.neg(b)) == a
        >>> assert ec.add(a, ec.neg(a)) == ec.zero
        >>> assert ec.add(a, b) == ec.add(b, a)
        >>> assert ec.add(a, ec.add(b, c)) == ec.add(ec.add(a, b), c)
        """
        if p1 == self.zero: return p2
        if p2 == self.zero: return p1
        if p1.x == p2.x and (p1.y != p2.y or p1.y == 0):
            # p1 + -p1 == 0
            return self.zero
        if p1.x == p2.x:
            # p1 + p1: use tangent line of p1 as (p1,p1) line
            l = (3 * p1.x * p1.x + self.a) * inv(2 * p1.y, self.q) % self.q
            pass
        else:
            l = (p2.y - p1.y) * inv(p2.x - p1.x, self.q) % self.q
            pass
        x = (l * l - p1.x - p2.x) % self.q
        y = (l * (p1.x - x) - p1.y) % self.q
        return Coord(x, y)
 
    def mul(self, p, n):
        """n times <mul> of elliptic curve
        >>> m = ec.mul(p, n)
        >>> assert ec.is_valid(m)
        >>> assert ec.mul(p, 0) == ec.zero
        """
        r = self.zero
        m2 = p
        # O(log2(n)) add
        while 0 < n:
            if n & 1 == 1:
                r = self.add(r, m2)
                pass
            n, m2 = n >> 1, self.add(m2, m2)
            pass
        # [ref] O(n) add
        #for i in range(n):
        #    r = self.add(r, p)
        #    pass
        return r
 
    def order(self, g):
        """order of point g
        >>> o = ec.order(g)
        >>> assert ec.is_valid(a) and ec.mul(a, o) == ec.zero
        >>> assert o <= ec.q
        """
        assert self.is_valid(g) and g != self.zero
        for i in range(1, self.q + 1):
            if self.mul(g, i) == self.zero:
                return i
            pass
        raise Exception("Invalid order")
    pass
 
 
class ElGamal(object):
    """ElGamal Encryption
    pub key encryption as replacing (mulmod, powmod) to (ec.add, ec.mul)
    - ec: elliptic curve
    - g: (random) a point on ec
    """
    def __init__(self, ec, g):
        assert ec.is_valid(g)
        self.ec = ec
        self.g = g
        self.n = ec.order(g)
        pass
 
    def gen(self, priv):
        """generate pub key
        - priv: priv key as (random) int < ec.q
        - returns: pub key as points on ec
        """
        return self.ec.mul(g, priv)
 
    def enc(self, plain, pub, r):
        """encrypt
        - plain: data as a point on ec
        - pub: pub key as points on ec
        - r: randam int < ec.q
        - returns: (cipher1, ciper2) as points on ec
        """
        assert self.ec.is_valid(plain)
        assert self.ec.is_valid(pub)
        return (self.ec.mul(g, r), self.ec.add(plain, self.ec.mul(pub, r)))
 
    def dec(self, cipher, priv):
        """decrypt
        - chiper: (chiper1, chiper2) as points on ec
        - priv: private key as int < ec.q
        - returns: plain as a point on ec
        """
        c1, c2 = cipher
        assert self.ec.is_valid(c1) and ec.is_valid(c2)
        return self.ec.add(c2, self.ec.neg(self.ec.mul(c1, priv)))
    pass
 
class DiffieHellman(object):
    """Elliptic Curve Diffie Hellman (Key Agreement)
    - ec: elliptic curve
    - g: a point on ec
    """
    def __init__(self, ec, g):
        self.ec = ec
        self.g = g
        self.n = ec.order(g)
        pass
 
    def gen(self, priv):
        """generate pub key"""
        assert 0 < priv and priv < self.n
        return self.ec.mul(self.g, priv)
 
    def secret(self, priv, pub):
        """calc shared secret key for the pair
        - priv: my private key as int
        - pub: partner pub key as a point on ec
        - returns: shared secret as a point on ec
        """
        assert self.ec.is_valid(pub)
        assert self.ec.mul(pub, self.n) == self.ec.zero
        return self.ec.mul(pub, priv)
    pass
 
class DSA(object):
    """ECDSA
    - ec: elliptic curve
    - g: a point on ec
    """
    def __init__(self, ec, g):
        self.ec = ec
        self.g = g
        self.n = ec.order(g)
        pass
 
    def gen(self, priv):
        """generate pub key"""
        assert 0 < priv and priv < self.n
        return self.ec.mul(self.g, priv)
 
    def sign(self, hashval, priv, r):
        """generate signature
        - hashval: hash value of message as int
        - priv: priv key as int
        - r: random int 
        - returns: signature as (int, int)
        """
        assert 0 < r and r < self.n
        m = self.ec.mul(self.g, r)
        return (m.x, inv(r, self.n) * (hashval + m.x * priv) % self.n)
 
    def validate(self, hashval, sig, pub):
        """validate signature
        - hashval: hash value of message as int
        - sig: signature as (int, int)
        - pub: pub key as a point on ec
        """
        assert self.ec.is_valid(pub)
        assert self.ec.mul(pub, self.n) == self.ec.zero
        w = inv(sig[1], self.n)
        u1, u2 = hashval * w % self.n, sig[0] * w % self.n
        p = self.ec.add(self.ec.mul(self.g, u1), self.ec.mul(pub, u2))
        return p.x % self.n == sig[0]
    pass

class MainWindow(QtGui.QWidget): 
    def __init__(self): 
        QtGui.QWidget.__init__(self) 
        global to_enc
        global dec1
        global dec2
        global label_ans
         
        self.setGeometry(0,0, 500,650) 
        self.setWindowTitle("Elliptic Curve Cryptography") 
        self.setWindowIcon(QtGui.QIcon("icon.png")) 
        self.resize(500,650) 
        self.setMinimumSize(500,650) 
        self.center() 
         
        self.tab_widget = QtGui.QTabWidget() 
        tab1 = QtGui.QWidget() 
        tab2 = QtGui.QWidget() 
        tab3 = QtGui.QWidget()
        tab4 = QtGui.QWidget()
         
        p1_vertical = QtGui.QVBoxLayout(tab1) 
        p2_vertical = QtGui.QVBoxLayout(tab2)
        p3_vertical = QtGui.QVBoxLayout(tab3)
        p4_vertical = QtGui.QVBoxLayout(tab4) 
         
        self.tab_widget.addTab(tab1, "ECC Curve") 
        self.tab_widget.addTab(tab2, "ElGamal")
        self.tab_widget.addTab(tab3, "ECDH")
        self.tab_widget.addTab(tab4, "ECDSA")

        key_enc_label = QtGui.QLabel("Enter the key to encrypt:")
        key_dec1_label = QtGui.QLabel("Enter the key(x) to decrypt:")
        key_dec2_label = QtGui.QLabel("Enter the key(y) to decrypt:")
        elgamal_pub_key = QtGui.QLabel("The ElGamal public key is:")
        button_enc = QtGui.QPushButton("Encrypt")
        button_dec = QtGui.QPushButton("Decrypt")
        self.elg_key = QtGui.QTextEdit()
        to_enc = QtGui.QTextEdit()
        dec1 = QtGui.QTextEdit()
        dec2 = QtGui.QTextEdit()
        self.tab_widget.currentChanged.connect(self.loadValues)
        self.elg_key.setMaximumHeight(key_enc_label.sizeHint().height()*2)
        to_enc.setMaximumHeight(key_enc_label.sizeHint().height()*2)
        dec1.setMaximumHeight(key_enc_label.sizeHint().height()*2)
        dec2.setMaximumHeight(key_enc_label.sizeHint().height()*2)

        button_enc.clicked.connect(self.elgamal_code)
        button_dec.clicked.connect(self.elgamal_dec)
        global label_key
        label_ans = QtGui.QLabel("The decrypted value is: ")
        label_key = QtGui.QLabel()
        label_key.hide()
        label_a = QtGui.QLabel("Enter value of a:")
        label_b = QtGui.QLabel("Enter value of b:")
        label_c = QtGui.QLabel("Enter value of n (private key):")    
        self.val_a = QtGui.QTextEdit()
        self.val_b = QtGui.QTextEdit()
        self.val_c = QtGui.QTextEdit()   
        button = QtGui.QPushButton("Generate curve") 
        self.go_ahead = QtGui.QLabel("Curve defined. Please select a tab based on your need.")
        self.go_ahead.hide()
        button.clicked.connect(self.generateprime)

        self.val_a.setMaximumHeight(label_a.sizeHint().height()*2)
        self.val_b.setMaximumHeight(label_b.sizeHint().height()*2)
        self.val_c.setMaximumHeight(label_c.sizeHint().height()*2)

        p1_vertical.addWidget(label_a)
        p1_vertical.addWidget(self.val_a)
        p1_vertical.addWidget(label_b)
        p1_vertical.addWidget(self.val_b)
        p1_vertical.addWidget(label_c)
        p1_vertical.addWidget(self.val_c) 
        p1_vertical.addStretch(1)
        p1_vertical.addWidget(self.go_ahead)
        p1_vertical.addWidget(button)

        p2_vertical.addWidget(elgamal_pub_key)
        p2_vertical.addWidget(self.elg_key)
        p2_vertical.addWidget(key_enc_label)
        p2_vertical.addWidget(to_enc)
        p2_vertical.addWidget(button_enc)
        p2_vertical.addWidget(label_key)
        p2_vertical.addStretch(1)
        p2_vertical.addWidget(key_dec1_label)
        p2_vertical.addWidget(dec1 )
        p2_vertical.addWidget(key_dec2_label)
        p2_vertical.addWidget(dec2 )
        p2_vertical.addWidget(label_ans)
        p2_vertical.addWidget(button_dec)

        vbox = QtGui.QVBoxLayout() 
        vbox.addWidget(self.tab_widget) 
         
        self.setLayout(vbox) 
     
    def generateprime(self):
        global a
        global b
        global priv
        global q
        a = int(self.val_a.toPlainText())
        b = int(self.val_b.toPlainText())
        priv = int(self.val_c.toPlainText())
        q = max(a,b) + 1

        #generate prime q
        while(1):
            if self.isPrime(q):
                break
            q = q + 1

        self.go_ahead.show()

    def isPrime(self, num):
        if num == 2:
            return True
        if num < 2 or num % 2 == 0:
            return False
        for n in xrange(3, int(num**0.5)+2, 2):
            if num % n == 0:
                return False
        return True  
     
    def center(self): 
        screen = QtGui.QDesktopWidget().screenGeometry() 
        size = self.geometry() 
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2) 

    def loadValues(self):
        global ec
        global eg
        idx = self.tab_widget.currentIndex()
        if idx == 1:
            global g
            global pub
            ec = EC(a, b, q)
            g, _ = ec.at(7)
            eg = ElGamal(ec, g)
            pub = eg.gen(priv)
            print_pub = str(pub[0]) + "," + str(pub[1])
            self.elg_key.insertPlainText(print_pub)
        
    def elgamal_code(self):
        global mapping
        mapping = [ec.mul(g, i) for i in range(eg.n)]
        key_to_encrypt = int(to_enc.toPlainText())
        plain = mapping[key_to_encrypt]
        #print plain
        #cipher = eg.enc(plain, pub, 15)
        keyval = "The encrypted code is: " + str(plain)
        label_key.setText(keyval)
        label_key.show()

    def elgamal_dec(self):
        x_co = int(dec1.toPlainText())
        y_co = int(dec2.toPlainText())
        check = Coord(x_co,y_co)
        if mapping.index(check) != -1:
            label_ans.setText("The decrypted value is: " + str(mapping.index(check)))

app = QtGui.QApplication(sys.argv) 
frame = MainWindow() 
frame.show() 
sys.exit(app.exec_())

'''

        cipher = eg.enc(plain, pub, 15)
        decoded = eg.dec(cipher, priv)
        assert decoded == plain
        assert cipher != pub
        
        
        # ECDH usage
        dh = DiffieHellman(ec, g)
        
        apriv = 11
        apub = dh.gen(apriv)
        
        bpriv = 3
        bpub = dh.gen(bpriv)
        
        cpriv = 7
        cpub = dh.gen(cpriv)
        # same secret on each pair
        assert dh.secret(apriv, bpub) == dh.secret(bpriv, apub)
        assert dh.secret(apriv, cpub) == dh.secret(cpriv, apub)
        assert dh.secret(bpriv, cpub) == dh.secret(cpriv, bpub)
        
        # not same secret on other pair
        assert dh.secret(apriv, cpub) != dh.secret(apriv, bpub)
        assert dh.secret(bpriv, apub) != dh.secret(bpriv, cpub)
        assert dh.secret(cpriv, bpub) != dh.secret(cpriv, apub)
        
        
        # ECDSA usage
        dsa = DSA(ec, g)
        
        priv = 11
        pub = eg.gen(priv)
        hashval = 128
        r = 7
        
        sig = dsa.sign(hashval, priv, r)
        assert dsa.validate(hashval, sig, pub)
        pass
    '''
