import hashlib
import base64
import os, sys 
from Crypto.Cipher import AES
from hashlib import md5
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
        tab = QtGui.QWidget()
        tab2 = QtGui.QWidget() 
        p3_vertical = QtGui.QVBoxLayout(tab)
         
        self.tab_widget.addTab(tab, "EC Diffie Hellman")

        # ECDH GUI DECLARATIONS
        labele1 = QtGui.QLabel(" Elliptical Curve EQUATION ")
        labele2 = QtGui.QLabel("y^3 = x^2 + ax + b( mod q )")
        labele1.setStyleSheet('font-size: 13pt')
        labele2.setStyleSheet('font-size: 12pt')
        labele1.setAlignment(QtCore.Qt.AlignCenter)
        labele2.setAlignment(QtCore.Qt.AlignCenter)
        labela = QtGui.QLabel("Enter value of a:")
        labelb = QtGui.QLabel("Enter value of b:")
        labelc = QtGui.QLabel("Enter value of q (prime):")
        label_PrivA = QtGui.QLabel("Enter Private Key of A:")
        label_PrivB = QtGui.QLabel("Enter Private Key of B:")
        label_result = QtGui.QLabel("ENCODED / DECODED TEXT")
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
        self.vala.setMaximumHeight(labela.sizeHint().height()*1.5)
        self.valb.setMaximumHeight(labelb.sizeHint().height()*1.5)
        self.valc.setMaximumHeight(labelc.sizeHint().height()*1.5)        
        self.apriv.setMaximumHeight(label_PrivA.sizeHint().height()*1.5)
        self.bpriv.setMaximumHeight(label_PrivB.sizeHint().height()*1.5)
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
        BLOCK_SIZE = 64
        PADDING = '{'
        pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
        EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
        x,y = dh.secret(PrivA,apub)
        secret=x+y
        secret = hashlib.md5('secret').hexdigest()
        cipher = AES.new(secret)
        encoded = EncodeAES(cipher, txt)
        self.textEdit.setText(encoded)
        fileName = open('Encrypted.txt','w')
        fileName.write(encoded)
        fileName.close()
        
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
        fileName = open('Decrypted.txt','w')
        fileName.write(decoded)
        fileName.close()

        
    def importfile(self):
        global data
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/home')        
        f = open(fname, 'r')        
        with f:        
            data = f.read()

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
        
app = QtGui.QApplication(sys.argv) 
frame = MainWindow() 
frame.show() 
sys.exit(app.exec_())