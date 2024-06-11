from PyQt5 import QtCore, QtGui, QtWidgets
import serial, time, sys, threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Temperatura(QtWidgets.QWidget):
    puerto = "COM3"
    baudrate = 9600
    arduino = serial.Serial(port=puerto, baudrate=baudrate, timeout=1)

    def __init__(self):
        super(Temperatura, self).__init__()
        self.setupUi(self)
        self.init_ui()
        
    def init_ui(self):
        self.lcdReal.display(0)
        self.lcdBebe.display(0)
        self.lcdPeso.display(0)
        self.paused = False
        self.arthrrun1 = True
        self.arthrrun2 = True
        self.leerthread = threading.Thread(target=self.leerarduino)
        self.leerthread.start()

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
        self.lcdPeso = QtWidgets.QLCDNumber(self.widget_2)
        self.lcdPeso.setGeometry(QtCore.QRect(415, 250, 200, 71))
        self.lcdPeso.setObjectName("lcdPeso")
        self.lcdBebe = QtWidgets.QLCDNumber(self.widget_2)
        self.lcdBebe.setGeometry(QtCore.QRect(205, 80, 200, 71))
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
        self.label_5.setGeometry(QtCore.QRect(250, 50, 211, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(255, 255, 255)")
        self.label_5.setObjectName("label_5")


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Temperatura"))
        self.label_3.setText(_translate("Form", "Volumen (L)"))
        self.label_4.setText(_translate("Form", "Flujo (L/s)"))
        self.label_5.setText(_translate("Form", "Diferencial (kPa)"))

    def pausar(self):
        self.paused = True
    
    def reanudar(self):
        self.paused = False

    def leerarduino(self):

        self.tempreal = 0
        self.pesobebe = 0
        self.tempbebe = 0

        try:
            while not self.paused:

                variable = self.arduino.readline().decode('latin-1').rstrip()

                if variable.startswith("Volumen"):
                    variable = ''.join(filter(lambda x: x.isdigit() or x == '.', variable))
                    self.tempreal = float(variable) if '.' in variable else 0.0

                    fig, ax = plt.subplots()
                    x = []
                    n = 50

                    # Función para actualizar el gráfico
                    def update(frame):
                        x.append(self.tempreal)
                        ax.clear()
                        ax.plot(x, color="r")
                        if frame < n // 2:
                            ax.set_xlim(0, n)
                        else:
                            ax.set_xlim(frame - n // 2, frame + n // 2)
                        ax.set_ylim(0, 100)  # Ajustar el límite del eje y si es necesario

                    # Crear una animación
                    ani = animation.FuncAnimation(fig, update, frames=range(n), repeat=False)

                    plt.show()
  

                if variable.startswith("Diferencial"):      #guagua
                    variable = ''.join(filter(lambda x: x.isdigit() or x == '.', variable))
                    self.tempbebe = float(variable) if '.' in variable else 0.0
                elif variable.startswith("CALIBRANDO..."):
                    self.tempbebe = "..."

                if variable.startswith("Flujo"):    #peso
                    variable = ''.join(filter(lambda x: x.isdigit() or x == '.', variable))
                    self.pesobebe = float(variable) if '.' in variable else 0.0
                
                self.lcdReal.display(self.tempreal)
                self.lcdPeso.display(self.pesobebe)
                self.lcdBebe.display(self.tempbebe)

        except Exception as e:
            print(f"Error en el hilo: {e}")
        finally:
            self.arduino.close()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = Temperatura()
    widget.show()
    sys.exit(app.exec_())
