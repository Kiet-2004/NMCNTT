#Importing necessary module for the tool
import os, sys
from PIL import Image
import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets    
from PyQt5 import uic
import spacy
from string import punctuation
from googlesearch import search
from paddleocr import PaddleOCR,draw_ocr

#This is for paddleocr
ocr = PaddleOCR(use_angle_cls = True, lang = 'en')
    
#This is for the font size
font_list = []
font = 2

for font in range(110):
    font += 2
    font_list.append(str(font))

#App setup
class OCR_APP(QtWidgets.QMainWindow):
    #Setup for app feature
    def __init__(self):
        #Open the main.ui file
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi('main.ui',self)
        self.image = None
		
        #Select image button
        self.ui.pushButton.clicked.connect(self.select_image)
        self.rubberBand = QRubberBand(QRubberBand.Rectangle,self)
        self.ui.label_2.setAlignment(PyQt5.QtCore.Qt.AlignTop)

        #Default size
        self.font_size = '20'
        self.text = ''
        self.text_2 = ''
        self.comboBox_2.addItems(font_list)
        self.comboBox_2.currentIndexChanged['QString'].connect(self.update_font_size)
        self.comboBox_2.setCurrentIndex(font_list.index(self.font_size))
		
        #Set font size for text box
        self.ui.textEdit.setFontPointSize(int(self.font_size))
        self.ui.textEdit_2.setFontPointSize(int(self.font_size))
        self.setAcceptDrops(True)
        
    #Updating the font size
    def update_font_size(self, value):
        self.font_size = value
        self.ui.textEdit.setFontPointSize(int(self.font_size))
        self.ui.textEdit.setText(str(self.text))
        self.ui.textEdit_2.setFontPointSize(int(self.font_size))
        self.ui.textEdit_2.setText(str(self.text_2))
        
    #Selecting image from the computer
    def select_image(self):
        filename = QFileDialog.getOpenFileName(self,'Select File')
        self.ui.label_2.setPixmap(QtGui.QPixmap(filename[0]))
        self.text = ""
        self.text_2 = ""    
    
        #Scanning text
        result = ocr.ocr(filename[0], cls = True)
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                self.text = self.text + " " + line[1][0]
        self.ui.textEdit_2.setText(str(self.text))
        
        #Keyword extracting and google searching
        for i in self.get_keywords(self.text):
            self.text_2 = self.text_2 + i + '\n'
        self.ui.textEdit.setText(str(self.text_2))
    
    #Extracting keyword  
    def get_keywords(self, text):
        nlp = spacy.load("en_core_web_sm")
        result = []
        pos_tag = ['PROPN','ADJ','NOUN'] 
        doc = nlp(text.lower()) 
        for token in doc:
            if(token.text in nlp.Defaults.stop_words or token.text in punctuation or token.text in result):
                continue
            if(token.pos_ in pos_tag):
                result.append(token.text)
        print("Keyword search: ")
        keyword = ""
		
		#Searching
        search_result = []
        for i in result:
            keyword = keyword + i + " "
        for j in search(keyword, tld="co.in", num=10, stop=10, pause=2):
            print(j)
            search_result.append(j)
        return search_result

#Running the app
app = QtWidgets.QApplication(sys.argv)
mainWindow = OCR_APP()
mainWindow.show()
sys.exit(app.exec_())