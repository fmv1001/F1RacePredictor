from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtWidgets import QSpacerItem, QFrame, QDialog, QMessageBox, QApplication, QWidget, QStackedWidget, QVBoxLayout, QLabel, QComboBox, QDesktopWidget, QPushButton, QGridLayout,  QSizePolicy
from PyQt5.QtGui import QPixmap, QResizeEvent, QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtCore import pyqtSignal

class WaitingDialog(QDialog):
    optionSelected = pyqtSignal(int)  # Señal personalizada para enviar la opción seleccionada

    def __init__(self, piloto, postions):
        super().__init__()
        self.piloto = piloto
        self.positions = postions
        self.selected_option = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Grid positions')
        # self.width = 400
        # self.height = 300
        self.setGeometry(100, 100, 500, 760)
        # self.setStyleSheet('background-color: white;')
        container = QWidget(self)

        # Crear el layout principal y el layout secundario
        screen_layout = QVBoxLayout(container)
        # screen_layout = QWidget()
        label_layout = QVBoxLayout()
        buttons_layout = QGridLayout()
        
        size_driver = QSize(450, 50)
        size_pos = QSize(140, 50)

        label = QLabel()
        pixmap = QPixmap(f'data/selectgrid1.png')
        scaled_pixmap = pixmap.scaled(size_driver)
        label.setPixmap(scaled_pixmap)
        label1 = QLabel()
        pixmap1 = QPixmap(f'data/selectgrid2.png')
        scaled_pixmap1 = pixmap1.scaled(size_driver)
        label1.setPixmap(scaled_pixmap1)
        label2 = QLabel()
        pixmap2 = QPixmap(f'data/drivers/{self.piloto}.png')
        scaled_pixmap2 = pixmap2.scaled(size_driver)
        label2.setPixmap(scaled_pixmap2)

        label_layout.addWidget(label)
        label_layout.addWidget(label1)
        label_layout.addWidget(label2)

        fila = 1
        columna = 0
        rango = list(range(1,21))
        actualy_pos = [x for x in rango if x not in self.positions]
        for i in actualy_pos:
            button = self.create_button(f'data/pos/p{i}.png', size_pos, self.onOption1Clicked, f'race_position-{i}')
            buttons_layout.addWidget(button, fila, columna) 
            columna += 1
            if columna == 2:
                fila += 1
                columna = 0
        
        screen_layout.addLayout(label_layout)
        screen_layout.addLayout(buttons_layout)

    def onOption1Clicked(self):
        sender = self.sender()
        # self.optionSelected.emit(sender.property('pos'))  # Emitir la señal con la opción seleccionada
        self.selected_option = sender.property('race_position')
        # self.close()  # Cerrar la ventana
        self.accept()
    
    def create_button(self, image_path, size, onclick, property = None):
        try:
            # Crear el botón con la imagen
            button = QPushButton()
            if property != None:
                id = property.split("-")[0]
                valor = int(property.split("-")[1])
                button.setProperty(id, valor)
            pixmap = QPixmap(image_path)
            # print(image_path)
            pixmap = pixmap.scaled(size)

            # Obtener las dimensiones de la imagen
            width = pixmap.width()
            height = pixmap.height()

            # Establecer el tamaño del botón según las dimensiones de la imagen
            button.setFixedSize(width, height)

            # Establecer la imagen como icono del botón
            button.setIcon(QIcon(pixmap))
            button.setIconSize(button.size())
            button.clicked.connect(onclick)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        except:
            print(image_path)

        return button
