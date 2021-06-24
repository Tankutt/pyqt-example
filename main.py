import sys
import serial
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QMainWindow, QPushButton, QTextEdit
from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtGui import QIntValidator


class serialThreadClass(QtCore.QThread):  

    message = QtCore.pyqtSignal(str)
    def __init__(self,parent = None):
        super(serialThreadClass,self).__init__(parent)
        self.serialPort = serial.Serial()
        self.stopflag = False

    def stop(self):
        self.stopflag = True

    def run(self):
        while True:
            if (self.stopflag):
                self.stopflag = False
                break
            elif(self.serialPort.isOpen()): 
                try:                        
                    self.data = self.serialPort.readline()
                except:
                    print("HATA\n")
                self.message.emit(str(self.data.decode()))

class MainWindow(QtWidgets.QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
        self.show()

    def initUI(self):
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
        #self.textEdit=QTextEdit("",self)
        self.lineEditSendData=QLineEdit("",self)
        self.lineEditSendData.setValidator(QIntValidator(0,10000,self))
        
        #self.textEdit.setGeometry(100,80,200,30)
        self.buttonStart.setGeometry(400,80,100,30)
        self.buttonOn.setGeometry(100,300,100,30)
        self.buttonOff.setGeometry(400,300,100,30)
        self.labelLed.setGeometry(100,220,100,100)
        self.labelLedStatus.setGeometry(100,330,100,100)
        self.labelLedStatusResult.setGeometry(400,330,100,100)
        self.labelTime.setGeometry(100,30,50,50)
        self.labelMessage.setGeometry(100,100,100,100)
        self.lineEditSendData.setGeometry(100,80,200,30)
        
        self.mySerialPort = serialThreadClass()
        self.mySerialPort.message.connect(self.messageTextEdit)  
        self.mySerialPort.start()

        self.connectSerialPort() 
        self.buttonStart.clicked.connect(self.dataReceived)
        self.buttonOn.clicked.connect(self.ledOn)
        self.buttonOff.clicked.connect(self.ledOff)
        
    def connectSerialPort(self):
        self.portName="COM5"
        self.mySerialPort.serialPort.port=self.portName
        self.mySerialPort.serialPort.baudrate = int(9600)
        if not self.mySerialPort.serialPort.isOpen():
            self.mySerialPort.serialPort.open()

    def ledOn(self):
        self.mySerialPort.serialPort.write("L,1".encode())
        self.buttonOn.setEnabled(False)
        self.buttonOff.setEnabled(True)
        

    def ledOff(self):
        self.mySerialPort.serialPort.write("L,0".encode())
        self.buttonOn.setEnabled(True)
        self.buttonOff.setEnabled(False)


    def dataReceived(self):
        self.buttonStart.setEnabled(False)
        self.labelMessage.setText("Message Send.")
        self.test=self.lineEditSendData
        self.mySerialPort.serialPort.write("T".encode()) #going to update
        self.incomingMessage = str(self.mySerialPort.data.decode())    
        self.labelLedStatusResult.setText(self.incomingMessage)
        if self.lineEditSendData == "feedback":
            self.buttonStart.setEnabled(True)
            self.labelMessage.setText("Message Received...")
        
       
    def messageTextEdit(self):
        if self.lineEditSendData != "feedback":
            self.incomingMessage = str(self.mySerialPort.data.decode())    
            self.labelLedStatusResult.setText(self.incomingMessage)
        
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())

