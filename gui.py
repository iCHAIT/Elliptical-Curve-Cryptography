from Crypto.Cipher import AES
from hashlib import md5
import hashlib
import base64
import os, sys 
from PyQt4 import QtGui, QtCore 
import collections
from eclib import EC
from eclib import DiffieHellman


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

        # CURVE FOR ELGAMAL
        button_enc.clicked.connect(self.elgamal_code)
        button_dec.clicked.connect(self.elgamal_dec)
        global label_key
        label_ans = QtGui.QLabel("The decrypted value is: ")
        label_key = QtGui.QLabel()
        label_key.hide()
        label_a = QtGui.QLabel("Enter value of a:")
        label_b = QtGui.QLabel("Enter value of b:")
        label_c = QtGui.QLabel("Enter value of n (private key):")

        # ECDH
        
        #ELGAMAL
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
       
        # TAB FOR CURVE / ELGAMAL
        p1_vertical.addWidget(label_a)
        p1_vertical.addWidget(self.val_a)
        p1_vertical.addWidget(label_b)
        p1_vertical.addWidget(self.val_b)
        p1_vertical.addWidget(label_c)
        p1_vertical.addWidget(self.val_c) 
        p1_vertical.addStretch(1)
        p1_vertical.addWidget(self.go_ahead)
        p1_vertical.addWidget(button)

        # TAB FOR ELGAMAL
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
    

#ECDH CODE--------------------------------------------------------------------------------------------
        # ECDH GUI DECLARATIONS
        labele1 = QtGui.QLabel("DIFFIE HELMAN EQUATION")
        labele2 = QtGui.QLabel("y3 = x2 + ax + b( mod q )")
        labele1.setStyleSheet('font-size: 13pt')
        labele2.setStyleSheet('font-size: 12pt')
        labela = QtGui.QLabel("Enter value of a:")
        labelb = QtGui.QLabel("Enter value of b:")
        labelc = QtGui.QLabel("Enter value of q (prime):")
        label_PrivA = QtGui.QLabel("Enter Private Key of A:")
        label_PrivB = QtGui.QLabel("Enter Private Key of B:")
        label_result = QtGui.QLabel("ENCODED/DECODED TEXT")
        label_result.setStyleSheet('font-size: 12pt')
        textEdit = QtGui.QTextEdit()
        button_file = QtGui.QPushButton("Import File") 
        button_encrypt = QtGui.QPushButton("Encrypt") 
        button_decrypt = QtGui.QPushButton("Decrypt") 
        button_file.clicked.connect(self.importfile)        
        button_encrypt.clicked.connect(self.ecdhencrypt)        
        button_decrypt.clicked.connect(self.ecdhdecrypt)        
        self.vala = QtGui.QTextEdit()
        self.valb = QtGui.QTextEdit()
        self.valc = QtGui.QTextEdit()  
        self.apriv = QtGui.QTextEdit()  
        self.bpriv = QtGui.QTextEdit()  
        self.textEdit = QtGui.QTextEdit()  
        self.vala.setMaximumHeight(labela.sizeHint().height()*2)
        self.valb.setMaximumHeight(labelb.sizeHint().height()*2)
        self.valc.setMaximumHeight(labelc.sizeHint().height()*2)        
        self.apriv.setMaximumHeight(label_c.sizeHint().height()*2)
        self.bpriv.setMaximumHeight(label_c.sizeHint().height()*2)
        hbox = QtGui.QHBoxLayout()
        hbox1 = QtGui.QHBoxLayout()
        vbox1 = QtGui.QHBoxLayout()
        vbox2 = QtGui.QHBoxLayout()

        # GUI LAYOUT
        p3_vertical.addWidget(labele1)
        p3_vertical.addWidget(labele2)
        vbox1.addWidget(labela)
        vbox1.addWidget(self.vala)
        vbox2.addWidget(labelb)
        vbox2.addWidget(self.valb)
        hbox1.addLayout(vbox1)
        hbox1.addLayout(vbox2)
        p3_vertical.addLayout(hbox1)
        p3_vertical.addWidget(labelc)
        p3_vertical.addWidget(self.valc) 
        p3_vertical.addWidget(label_PrivA)
        p3_vertical.addWidget(self.apriv)
        p3_vertical.addWidget(label_PrivB)
        p3_vertical.addWidget(self.bpriv)
        p3_vertical.addWidget(button_file)
        p3_vertical.addWidget(label_result)
        p3_vertical.addWidget(self.textEdit)
        hbox.addWidget(button_encrypt)
        hbox.addWidget(button_decrypt)
        p3_vertical.addStretch(1)
        p3_vertical.addLayout(hbox)

        vbox = QtGui.QVBoxLayout() 
        vbox.addWidget(self.tab_widget) 
        self.setLayout(vbox) 
    
    #GUI Functionality
    def ecdhencrypt(self):
        global A,B,C,PrivA,PrivB
        A = int(self.vala.toPlainText())
        B = int(self.valb.toPlainText())
        C = int(self.valc.toPlainText())
        PrivA = int(self.apriv.toPlainText())
        PrivB = int(self.bpriv.toPlainText())
        txt = data
        ec = EC(A,B,C)
        g, _ = ec.at(7)
        assert ec.order(g) <= ec.q
        dh = DiffieHellman(ec, g)
        apub = dh.gen(PrivA)
        bpub = dh.gen(PrivB)
        assert dh.secret(PrivA, bpub) == dh.secret(PrivB, apub)
        # a=(dh.secret(PrivB,apub))
        BLOCK_SIZE = 64
        PADDING = '{'
        pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
        EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
        # DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
        x,y = dh.secret(PrivA,apub)
        secret=x+y
        # print"using x+y cordinate= " ,secret
        secret = hashlib.md5('secret').hexdigest()
        cipher = AES.new(secret)
        encoded = EncodeAES(cipher, txt)
        self.textEdit.setText(encoded)
        # print 'Encrypted string:', encoded

    def ecdhdecrypt(self):
        global A,B,C,PrivA,PrivB
        A = int(self.vala.toPlainText())
        B = int(self.valb.toPlainText())
        C = int(self.valc.toPlainText())
        PrivA = int(self.apriv.toPlainText())
        PrivB = int(self.bpriv.toPlainText())
        txt = data
        ec = EC(A,B,C)
        g, _ = ec.at(7)
        assert ec.order(g) <= ec.q
        dh = DiffieHellman(ec, g)
        apub = dh.gen(PrivA)
        bpub = dh.gen(PrivB)
        assert dh.secret(PrivA, bpub) == dh.secret(PrivB, apub)
        BLOCK_SIZE = 64
        PADDING = '{'
        pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
        DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
        x,y = dh.secret(PrivA,apub)
        secret=x+y
        secret = hashlib.md5('secret').hexdigest()
        cipher = AES.new(secret)
        decoded = DecodeAES(cipher, txt)
        self.textEdit.setText(decoded)
    
    def importfile(self):
        global data
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/home')        
        f = open(fname, 'r')        
        with f:        
            data = f.read()
# ________________________________________________________________________________________________________
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