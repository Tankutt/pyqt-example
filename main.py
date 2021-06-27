from os import read
import re
import sys, serial, serial.tools.list_ports, warnings, time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel, QTextEdit, QPushButton, QLineEdit
from PyQt5.QtGui import *
from PyQt5.QtCore import *

mySerial = serial.Serial("COM5",9600)

class Worker(QObject):
    finished = pyqtSignal()
    readData = pyqtSignal(str)

    @pyqtSlot()
    def __init__(self):
        super(Worker, self).__init__()
        self.working = True

    def work(self):
        while self.working:
            line = mySerial.readline().decode('utf-8')
            print(line)
            time.sleep(0.1)
            self.readData.emit(line)
        self.finished.emit()

class MainWindow(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.thread = None
        self.worker = None
        self.initUI()
        self.show()
    
    def initUI(self):

        self.worker = Worker()  
        self.thread = QThread() 
        
        self.worker.moveToThread(self.thread)  
        self.thread.started.connect(self.worker.work)
        self.worker.readData.connect(self.LedStatusResult)
        self.thread.start()

        self.setGeometry(600,300,600,500)
        self.setWindowTitle("QtPy_Proje")
        self.labelLed=QLabel("Led ",self)
        self.labelLedStatus=QLabel("Led Status: ",self)
        self.labelLedStatusResult=QLabel("OFF ",self)
        self.labelTime=QLabel("Time",self)
        self.labelMessage=QLabel("",self)
        self.buttonStart=QPushButton("Start",self)
        self.buttonOn=QPushButton("On",self)
        self.buttonOff=QPushButton("Off",self)
        self.buttonOff.setEnabled(False)
        self.lineEditSendData=QLineEdit("",self)
        self.lineEditSendData.setValidator(QIntValidator(0,1000000000,self))
        
        self.buttonStart.setGeometry(400,80,100,30)
        self.buttonOn.setGeometry(100,300,100,30)
        self.buttonOff.setGeometry(400,300,100,30)
        self.labelLed.setGeometry(100,220,100,100)
        self.labelLedStatus.setGeometry(100,330,100,100)
        self.labelLedStatusResult.setGeometry(400,330,100,100)
        self.labelTime.setGeometry(100,30,50,50)
        self.labelMessage.setGeometry(100,100,100,100)
        self.lineEditSendData.setGeometry(100,80,200,30)
        
        mySerial.reset_output_buffer
        
        self.buttonStart.clicked.connect(self.start)
        self.buttonOn.clicked.connect(self.ledOn)
        self.buttonOff.clicked.connect(self.ledOff)

    def ledOn(self):
        self.buttonOn.setEnabled(False)
        self.buttonOff.setEnabled(True)
        mySerial.write("L,1".encode())

    def ledOff(self):
        mySerial.write("L,0".encode())
        self.buttonOn.setEnabled(True)
        self.buttonOff.setEnabled(False)
    
    def LedStatusResult(self, i):
        self.labelLedStatusResult.setText("{}".format(i))
        print(i)
    
    def start(self):
        self.buttonStart.setEnabled(False)
        self.labelMessage.setText("Message Send.")
        self.lineEditSendData.setReadOnly(True)
        self.message="T"+","+self.lineEditSendData.text()
        mySerial.write(self.message.encode())
        if (mySerial.in_waiting>0):
            self.dataReceived()
        
    def dataReceived(self):
        self.buttonStart.setEnabled(True)
        self.labelMessage.setText("Message Received..")
        self.lineEditSendData.setReadOnly(False)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
