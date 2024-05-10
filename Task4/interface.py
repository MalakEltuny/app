from PyQt5 import QtWidgets
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton,QRadioButton,QTextEdit,QLCDNumber
import functions


def initConnectors(self):
    
    # Vital Sign Value LCD
    vitalNumber=self.findChild(QLCDNumber,"lcdNumber")

    #Send Btn connection
    sendBtn=self.findChild(QPushButton,"send_button")
    sendBtn.clicked.connect(lambda: functions.testConnection(self,vitalNumber))

    #Vital Sign  Radio btn
    bodyTemp=self.findChild(QRadioButton,"bodytemp_radioButton")
    respiratoryRadio=self.findChild(QRadioButton,"respiratory_radioButton")
    heartRate=self.findChild(QRadioButton,"heartrate_radioButton")

    bodyTemp.clicked.connect(lambda: functions.handleRadioBtn(self,"temperature"))
    respiratoryRadio.clicked.connect(lambda: functions.handleRadioBtn(self,"respiratory"))
    heartRate.clicked.connect(lambda: functions.handleRadioBtn(self,"heart"))

    # Name and ID connection
    patientName=self.findChild(QTextEdit,"name_textbox")
    patientName.textChanged.connect(lambda: functions.handleTextChanged(self,patientName.toPlainText(),'name'))

    patientId=self.findChild(QTextEdit,"id_textbox")
    patientId.textChanged.connect(lambda: functions.handleTextChanged(self,patientId.toPlainText(),'id'))