from PyQt5 import QtCore, QtGui, QtWidgets
import serial, time, sys, threading


class Temperatura(QtWidgets.QWidget):
    puerto = "COM5"
    baudrate = 9600
    arduino = serial.Serial(port=puerto, baudrate=baudrate, timeout=1)

    def __init__(self):
        super(Temperatura, self).__init__()
        self.setupUi(self)
        self.init_ui()
        
    def init_ui(self):
        self.pushUp.clicked.connect(self.aumentar)
        self.pushDown.clicked.connect(self.disminuir)
        self.pushDesconectar.clicked.connect(self.cambiar)
        self.tempset = 30.0
        self.lcdControl.display(self.tempset)
        self.lcdReal.display(0)
        self.iniciar()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(650, 400)
        Form.setMinimumSize(QtCore.QSize(650, 400))
        Form.setMaximumSize(QtCore.QSize(650, 400))
        Form.setAcceptDrops(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("App y Registros/ucm.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setStyleSheet("QPushButton#pushDesconectar, #pushRegistro{\n"
"background-color: rgba(191, 45, 14, 255);\n"
"color: rgba(255, 255, 255, 255);\n"
"border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton#pushDesconectar:hover, #pushRegistro:hover{\n"
"background-color: rgba(191, 45, 14, 175);\n"
"}\n"
"\n"
"QPushButton#pushDesconectar:pressed, #pushRegistro:pressed{\n"
"padding-left: 5px;\n"
"padding-top: 5px;\n"
"background-color: rgba(191, 45, 14, 100);\n"
"background-position: calc(100% - 10px)center;\n"
"}\n"
"\n"
"\n"
"")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(0, 0, 650, 400))
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(0, 0, 650, 400))
        self.label.setStyleSheet("background-color: rgba(23, 21, 25, 240)")
        self.label.setText("")
        self.label.setObjectName("label")
        self.widget_2 = QtWidgets.QWidget(self.widget)
        self.widget_2.setGeometry(QtCore.QRect(0, 0, 650, 400))
        self.widget_2.setObjectName("widget_2")
        self.lcdControl = QtWidgets.QLCDNumber(self.widget_2)
        self.lcdControl.setGeometry(QtCore.QRect(25, 80, 200, 71))
        self.lcdControl.setObjectName("lcdControl")
        self.label_2 = QtWidgets.QLabel(self.widget_2)
        self.label_2.setGeometry(QtCore.QRect(20, 50, 221, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255)")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.widget_2)
        self.label_3.setGeometry(QtCore.QRect(50, 220, 171, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255)")
        self.label_3.setObjectName("label_3")
        self.lcdReal = QtWidgets.QLCDNumber(self.widget_2)
        self.lcdReal.setGeometry(QtCore.QRect(30, 250, 200, 71))
        self.lcdReal.setObjectName("lcdReal")
        self.pushUp = QtWidgets.QPushButton(self.widget_2)
        self.pushUp.setGeometry(QtCore.QRect(235, 80, 30, 30))
        font = QtGui.QFont()
        font.setFamily("dripicons-v2")
        font.setPointSize(14)
        self.pushUp.setFont(font)
        self.pushUp.setObjectName("pushUp")
        self.pushDown = QtWidgets.QPushButton(self.widget_2)
        self.pushDown.setGeometry(QtCore.QRect(235, 120, 30, 31))
        font = QtGui.QFont()
        font.setFamily("dripicons-v2")
        font.setPointSize(14)
        self.pushDown.setFont(font)
        self.pushDown.setObjectName("pushDown")
        self.lcdPeso = QtWidgets.QLCDNumber(self.widget_2)
        self.lcdPeso.setGeometry(QtCore.QRect(415, 250, 200, 71))
        self.lcdPeso.setObjectName("lcdPeso")
        self.lcdBebe = QtWidgets.QLCDNumber(self.widget_2)
        self.lcdBebe.setGeometry(QtCore.QRect(410, 80, 200, 71))
        self.lcdBebe.setObjectName("lcdBebe")
        self.label_4 = QtWidgets.QLabel(self.widget_2)
        self.label_4.setGeometry(QtCore.QRect(440, 220, 151, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(255, 255, 255)")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.widget_2)
        self.label_5.setGeometry(QtCore.QRect(410, 50, 211, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(255, 255, 255)")
        self.label_5.setObjectName("label_5")
        self.pushDesconectar = QtWidgets.QPushButton(self.widget_2)
        self.pushDesconectar.setGeometry(QtCore.QRect(270, 340, 111, 28))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.pushDesconectar.setFont(font)
        self.pushDesconectar.setCheckable(True)
        self.pushDesconectar.setObjectName("pushDesconectar")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Temperatura"))
        self.label_2.setText(_translate("Form", "Temperatura de Control (ºC)"))
        self.label_3.setText(_translate("Form", "Temperatura Real (ºC)"))
        self.pushUp.setText(_translate("Form", "o"))
        self.pushDown.setText(_translate("Form", "h"))
        self.label_4.setText(_translate("Form", "Peso del bebé (kg)"))
        self.label_5.setText(_translate("Form", "Temperatura del bebé (ºC)"))
        self.pushDesconectar.setText(_translate("Form", "Desconectar"))

    def aumentar(self):
        self.tempset = self.tempset + 0.5
        self.lcdControl.display(float(self.tempset))
        self.lcdControl.repaint()
        message = f"NEW {self.tempset}\n" #probar eliminar este msg
        self.arduino.write(message.encode())
        print(f"{message}")
        
    def disminuir(self):
        self.tempset = self.tempset - 0.5
        self.lcdControl.display(float(self.tempset))
        self.lcdControl.repaint()
        message = f"NEW {self.tempset}\n" #probar eliminar este msg
        self.arduino.write(message.encode())
        print(f"{message}")

    def escribirarduino(self):
        try:
            while self.arthrrun1:
                message = f"SET: {self.tempset}\n"
                self.arduino.write(message.encode())

                if self.tempset:
                    self.lcdControl.display(self.tempset)
                time.sleep(1)

        except Exception as e:
            print(f"Error en el hilo: {e}")
        finally:
            self.arduino.close()

    def leerarduino(self):
        try:
            while self.arthrrun2:
                #tempreal = self.arduino.readline().decode().rstrip()
                #tempreal = ''.join(filter(lambda x: x.isdigit() or x == '.', tempreal))
                #tempreal = float(tempreal) if '.' in tempreal else 0.0
                
                tempreal = self.convardtopy("Ambiente", tempreal)
                pesobebe = self.convardtopy("Peso", pesobebe)
                tempbebe = self.convardtopy("Guagua", tempbebe)
                
                self.lcdReal.display(tempreal)
                self.lcdPeso.display(pesobebe)
                self.lcdBebe.display(tempbebe)
                time.sleep(0.5)   

        except Exception as e:
            print(f"Error en el hilo: {e}")
        finally:
            self.arduino.close()

    def terminar(self):
        self.arthrrun1 = False
        self.arthrrun2 = False
        self.leerthread.join()
        self.escribirthread.join()
        print("Comunicación serial cerrada manualmente")
        self.lcdReal.display("Off")
        self.lcdReal.repaint()

    def iniciar(self):
        self.arthrrun1 = True
        self.arthrrun2 = True
        self.leerthread.start()
        self.leerthread = threading.Thread(target=self.leerarduino)
        self.escribirthread.start()
        self.escribirthread = threading.Thread(target=self.escribirarduino)

    def cambiar(self):
        if self.pushDesconectar.isChecked():
            self.terminar()
            self.pushDesconectar.setText("Conectar")
        else:
            self.iniciar()
            self.pushDesconectar.setText("Desconectar")

    def convardtopy(self, arg, variable):
        variable = self.arduino.readline().decode().rstrip()
        if variable.startswith(f"{arg}"):
            variable = ''.join(filter(lambda x: x.isdigit() or x == '.', variable))
            variable = float(variable) if '.' in variable else 0.0


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = Temperatura()
    widget.show()
    sys.exit(app.exec_())
