import sys
import joblib
import pandas as pd
from datetime import date
# from collections import OrderedDict
from PyQt5.QtWidgets import QSpacerItem, QFrame, QDialog, QMessageBox, QApplication, QWidget, QStackedWidget, QVBoxLayout, QLabel, QComboBox, QDesktopWidget, QPushButton, QGridLayout,  QSizePolicy
from PyQt5.QtGui import QPixmap, QResizeEvent, QIcon
from PyQt5.QtCore import Qt, QSize, QEventLoop
from src.AppDrivers import Drivers
from src.AppConstructors import Constructors
from src.AppCircuits import Circuits
from src.AppResults import Results
from src.AppCoder import Coder
from apQtDialogGrid import WaitingDialog

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.waiting_dialog = None
        self.event_loop = None
        self.grid_pos = []

    # def waitUntilButtonClicked(self, driver):
    #     self.waiting_dialog = WaitingDialog(driver)
    #     self.event_loop = QEventLoop()
    #     self.waiting_dialog.exec_()
    #     self.event_loop.exec_()

    # def continueExecution(self):
    #     if self.waiting_dialog is not None:
    #         self.waiting_dialog.accept()
    #     if self.event_loop is not None:
    #         self.event_loop.exit()

    def initUI(self):
        # Configurar la ventana principal
        self.setWindowTitle('F1 Predictor App')
        # self.width = 400
        # self.height = 300
        # self.setGeometry(100, 100, self.width, self.height)
        self.setStyleSheet('background-color: white;')

        self.modelo_race_pos = joblib.load('trained_model_race_pos.pkl')
        self.modelo_winner = joblib.load('trained_model_winner.pkl')
        self.modelo_pole = joblib.load('trained_model_pole.pkl')

        self.results_class = Results()
        self.coder_class = Coder()

        self.season = 2023
        self.driver_season = pd.read_csv('app_drivers.csv')
        self.circuit_season = pd.read_csv('app_circuits.csv')
        self.constructor_season = pd.read_csv('app_constructor_season.csv')

        self.rounds = {
            'albert_park' : 3,
            'americas' : 19,
            'bahrain' : 1,
            'baku' : 4,
            'catalunya' : 8,
            'hungaroring' : 12,
            'imola' : 6,
            'interlagos' : 21,
            'jeddah' : 2,
            'losail' : 18,
            'marina_bay' : 16,
            'miami' : 5,
            'monaco' : 7,
            'monza' : 15,
            'red_bull_ring' : 10,
            'rodriguez' : 20,
            'silverstone' : 11,
            'spa' : 13,
            'suzuka' : 17,
            'vegas' : 22,
            'villeneuve' : 9,
            'yas_marina' : 23,
            'zandvoort' : 14
        }
        
        self.circuit_season['race_round'] = self.circuit_season['circuit_id'].map(self.rounds)
        self.circuit = None
        self.weather = None

        # Crear el layout principal
        layout = QVBoxLayout()

        # Crear el widget de navegación
        self.stacked_widget = QStackedWidget()

        # Crear las pantallas
        screen1 = QWidget()
        screen2 = QWidget()
        screen3 = QWidget()
        screen4 = QWidget()

        screen1.setLayout(self.screen1())
        screen2.setLayout(self.screen2())
        screen3.setLayout(self.screen3())
        screen4.setLayout(self.screen4())
        

        # Agregar las pantallas al widget de navegación
        self.stacked_widget.addWidget(screen1)
        self.stacked_widget.addWidget(screen2)
        self.stacked_widget.addWidget(screen3)
        self.stacked_widget.addWidget(screen4)

        # Agregar el widget de navegación al layout principal
        layout.addWidget(self.stacked_widget)

        # Establecer la pantalla inicial
        self.stacked_widget.setCurrentIndex(0)

        # Agregar el layout a la ventana
        self.setLayout(layout)

        # Mostrar la ventana
        self.show()

    def screen1(self):
        # Agregar contenido a las pantallas
        screen_layout = QVBoxLayout()

        # self.background_label = QLabel(self)
        # self.background_label.setGeometry(0, 0, self.width, self.height)
        # self.set_background_image('data/wallpaper.jpeg')


        size = QSize(1300,900)
        
        button1 = self.create_button('data/wallpaper.jpeg', size, self.go_to_screen2)
        # button1 = self.create_button('temp22.png', size, self.go_to_screen2)
        # button2 = self.create_button('temp23.png', size, self.go_to_screen2)

        # Agregar el botón al layout
        # screen_layout.addWidget(self.background_label)
        screen_layout.addWidget(button1)
        # screen_layout.addWidget(button2)

        return screen_layout

    def screen3(self):
        # Agregar contenido a las pantallas
        # Crear el contenedor para los layouts
        container = QWidget(self)

        # Crear el layout principal y el layout secundario
        screen_layout = QVBoxLayout(container)
        label_layout = QVBoxLayout()
        frames_layout = QVBoxLayout()
        # buttons_layout = QGridLayout()

        # Crear un marco para la pantalla en tiempo de ejecución
        self.frame = QFrame(self)
        # self.frame.setStyleSheet('background-color: white; border: 1px solid black;')

        # Establecer un diseño en el marco
        frame_layout = QGridLayout(self.frame)
        
        size = QSize(500, 560)
        button1 = self.create_button('data/weather/dry.png', size, self.go_to_screen4, 'clima-dry')
        button2 = self.create_button('data/weather/wet.png', size, self.go_to_screen4, 'clima-wet')
        # Agregar el botón al layout
        frame_layout.addWidget(button1, 0, 0)
        frame_layout.addWidget(button2, 0, 1)
        self.frame.setLayout(frame_layout)

        # Mostrar la ventana con el botón y el marco
        # Agregar el botón al layout
        frames_layout.addWidget(self.frame)

        label = QLabel()
        pixmap = QPixmap('data/selectweather.png')
        scaled_pixmap = pixmap.scaled(QSize(600,70))
        label.setPixmap(scaled_pixmap)
        label_layout.addWidget(label) 

        screen_layout.addLayout(label_layout)
        screen_layout.addLayout(frames_layout)

        return(screen_layout)
    
    def screen2(self):

        screen_layout = QGridLayout()
        size = QSize(500,70)
        # Crear el botón con la imagen
        button = QPushButton()
        pixmap = QPixmap('data/selectcircuit.png')
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
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # label = QLabel()
        # pixmap = QPixmap('data/selectcircuit.png')
        # scaled_pixmap = pixmap.scaled(QSize(1000,75))
        # label.setPixmap(scaled_pixmap)
        # img_layout.addWidget(button) #, 0, 0
        screen_layout.addWidget(button, 0, 0)
        
        
        fila = 1
        columna = 0
        for circuit in self.circuit_season.sort_values('race_round')['circuit_id']:
            
            button = self.create_button(f'data/circuits/{circuit}.png', size,self.go_to_screen3, f'id-{circuit}')
            # print(f'circuits/temp23/{i}.png')

            # Agregar el botón al layout
            screen_layout.addWidget(button, fila, columna)
            
            columna += 1
            if columna == 2:
                fila += 1
                columna = 0


        # main_layout.addLayout(img_layout)
        # main_layout.addLayout(screen_layout)

        return(screen_layout)
    
    def screen4(self):
        # Agregar contenido a las pantallas
        # Crear el contenedor para los layouts
        container = QWidget(self)

        # Crear el layout principal y el layout secundario
        screen_layout = QVBoxLayout(container)
        # screen_layout = QWidget()
        frames_layout = QVBoxLayout()
        buttons_layout = QGridLayout()
            
        # Crear los botones
        size = QSize(300,55)
        button_pos = self.create_button(f'data/pred_pos.png', size, self.OnButtonClick_pred_pos)
        # button_pos = QPushButton('Predecir posiciones')
        # button_pos.clicked.connect(self.OnButtonClick_pred_pos)

        # Crear los botones
        button_winner = self.create_button(f'data/pred_winner.png', size, self.OnButtonClick_pred_winner)
        # button_winner = QPushButton('Predecir ganador')
        # button_winner.clicked.connect(self.OnButtonClick_pred_winner)

        # Crear los botones
        button_poleman = self.create_button(f'data/pred_poleman.png', size, self.OnButtonClick_pred_poleman)
        # button_poleman = QPushButton('Predecir poleman')
        # button_poleman.clicked.connect(self.OnButtonClick_pred_poleman)

        # Crear los botones
        size = QSize(200,55)
        button_back = self.create_button(f'data/home.png', size, self.go_to_screen1)
        # button_back = QPushButton('Inicio')
        # button_back.clicked.connect(self.go_to_screen1)
        # print(f'circuits/temp23/{i}.png')

        # Crear un marco para la pantalla en tiempo de ejecución
        self.frame = QFrame(self)
        # self.frame.setStyleSheet('background-color: white; border: 1px solid black;')

        # Establecer un diseño en el marco
        frame_layout = QGridLayout(self.frame)
        self.frame.setLayout(frame_layout)

        # Mostrar la ventana con el botón y el marco
        # Agregar el botón al layout
        buttons_layout.addWidget(button_pos, 0, 0)
        buttons_layout.addWidget(button_winner, 0, 1)
        buttons_layout.addWidget(button_poleman, 0, 2)
        buttons_layout.addWidget(button_back, 0, 3)
        frames_layout.addWidget(self.frame)

        screen_layout.addLayout(buttons_layout)
        screen_layout.addLayout(frames_layout)
            

        return(screen_layout) # 
    
    def screen5(self, predicciones):
        # Agregar contenido a las pantallas
        # screen_layout = QVBoxLayout()
        # screen_layout = QGridLayout()
        # Limpiar el contenido anterior del marco
        frame_layout = self.frame.layout()
        if frame_layout is not None:
            while frame_layout.count():
                item = frame_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)

        # Agregar el contenido al marco
        # frame_layout.addWidget(label)
        size_driver = QSize(350, 30)
        size_pos = QSize(100, 30)
        fila = 0
        columna = 1
        dict_final = {}
        for i, driver in enumerate(self.driver_season['driver_id']):
            dict_final[driver] = predicciones[i]
        diccionario_ordenado = dict(sorted(dict_final.items(), key=lambda x: x[1]))

        print(diccionario_ordenado)
        print(dict_final)
        for pos, driver in enumerate(diccionario_ordenado):

            button = self.create_button(f'data/drivers/{driver}.png', size_driver, self.go_to_screen1)
            button_pos = self.create_button(f'data/pos/p{pos+1}.png', size_pos, self.go_to_screen1)
            # print(f'circuits/temp23/{i}.png')

            # Agregar el botón al layout
            # screen_layout.addWidget(button, fila, columna)
            # screen_layout.addWidget(button_pos, fila, columna-1)
            frame_layout.addWidget(button, fila, columna)
            frame_layout.addWidget(button_pos, fila, columna-1)
            
            columna += 2
            fila += 1
            if columna == 5:
                fila += 1
                columna = 1

        return(frame_layout) # 
    
    def screen6(self, predicciones):
        # Agregar contenido a las pantallas
        # screen_layout = QVBoxLayout()
        # screen_layout = QGridLayout()
        # Limpiar el contenido anterior del marco
        frame_layout = self.frame.layout()
        if frame_layout is not None:
            while frame_layout.count():
                item = frame_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)

        # Agregar el contenido al marco
        # frame_layout.addWidget(label)
        size_driver = QSize(450, 50)
        size_pos = QSize(140, 50)
        dict_final = {}
        for i, driver in enumerate(self.driver_season['driver_id']):
            dict_final[driver] = predicciones[i]
        diccionario_ordenado = dict(sorted(dict_final.items(), key=lambda x: x[1]))

        print(diccionario_ordenado)
        print(dict_final)
        for pos, driver in enumerate(diccionario_ordenado):

            button = self.create_button(f'data/drivers/{driver}.png', size_driver, self.go_to_screen1)
            button_pos = self.create_button(f'data/pos/p{pos+1}.png', size_pos, self.go_to_screen1)
            frame_layout.addWidget(button, 0, 1)
            frame_layout.addWidget(button_pos, 0, 0)
            break


        return(frame_layout) #  
    
    def screen7(self, predicciones):
        # Agregar contenido a las pantallas
        frame_layout = self.frame.layout()
        if frame_layout is not None:
            while frame_layout.count():
                item = frame_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)

        # Agregar el contenido al marco
        size_driver = QSize(450, 50)
        size_pos = QSize(140, 50)
        dict_final = {}
        for i, driver in enumerate(self.driver_season['driver_id']):
            dict_final[driver] = predicciones[i]
        diccionario_ordenado = dict(sorted(dict_final.items(), key=lambda x: x[1], reverse=True))

        print(diccionario_ordenado)
        print(dict_final)
        for pos, driver in enumerate(diccionario_ordenado):
            if diccionario_ordenado[driver] == 0:
                driver = 'max_verstappen'
            button = self.create_button(f'data/drivers/{driver}.png', size_driver, self.go_to_screen1)
            button_pos = self.create_button(f'data/pos/p1.png', size_pos, self.go_to_screen1)
            frame_layout.addWidget(button, 0, 1)
            frame_layout.addWidget(button_pos, 0, 0)
            break

        return(frame_layout) # 

    def create_button(self, image_path, size, go_to_screen, property = None):
        try:
            # Crear el botón con la imagen
            button = QPushButton(clicked=go_to_screen)
            if property != None:
                id = property.split("-")[0]
                valor = property.split("-")[1]
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
            button.clicked.connect(self.buttonClicked)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        except:
            print(image_path)

        return button
    
    def go_to_screen1(self):
        # Limpiar el contenido anterior del marco
        frame_layout = self.frame.layout()
        if frame_layout is not None:
            while frame_layout.count():
                item = frame_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
        self.circuit = None
        self.weather = None
        self.grid_pos = []
        self.stacked_widget.setCurrentIndex(0)

    def go_to_screen2(self):
        self.stacked_widget.setCurrentIndex(1)

    def go_to_screen3(self):
        self.stacked_widget.setCurrentIndex(2)

    def go_to_screen4(self):
        self.stacked_widget.setCurrentIndex(3)

    def buttonClicked(self):
        sender = self.sender()
        if sender.property('id'):
            self.circuit = sender.property('id')
        if sender.property('clima'):
            self.weather = sender.property('clima')
        print('¡Botón presionado!')
        
    def OnButtonClick_pred_pos(self,):
        try:
            data = self.data_coder(True)
            # self.textctrl.SetValue(self.textctrl.GetValue() + f'Iniciando predicción...\n')
            # Lista de columnas a mantener
            columnas_mantener = self.modelo_race_pos.feature_names_in_

            # Obtener la intersección entre las columnas del DataFrame y la lista de columnas a mantener
            columnas_interseccion = list(set(data.columns) & set(columnas_mantener))

            # Seleccionar solo las columnas de la intersección
            data = data.loc[:, columnas_interseccion]
            data = data.reindex(columns=columnas_mantener)

            print(data)

            # Realizar la predicción
            prediccion_codificada = self.modelo_race_pos.predict(data)
            self.screen5(prediccion_codificada)

        except Exception as e:
            # Captura del error y print del mensaje de error
            print("Error:", str(e))
            # self.textctrl.SetValue("")
            return
        return
    
    def OnButtonClick_pred_winner(self,):
        try:
            data = self.data_coder(True)
            # Lista de columnas a mantener
            columnas_mantener = self.modelo_race_pos.feature_names_in_

            # Obtener la intersección entre las columnas del DataFrame y la lista de columnas a mantener
            columnas_interseccion = list(set(data.columns) & set(columnas_mantener))

            # Seleccionar solo las columnas de la intersección
            data = data.loc[:, columnas_interseccion]
            data = data.reindex(columns=columnas_mantener)

            print(data)

            # Realizar la predicción
            prediccion_codificada = self.modelo_race_pos.predict(data)
            self.screen6(prediccion_codificada)
        except Exception as e:
            # Captura del error y print del mensaje de error
            print("Error:", str(e))
            # self.textctrl.SetValue("")
            return
        return
    
    def OnButtonClick_pred_poleman(self,):
        try:
            data = self.data_coder(False)
            # Lista de columnas a mantener
            columnas_mantener = self.modelo_pole.feature_names_in_

            # Obtener la intersección entre las columnas del DataFrame y la lista de columnas a mantener
            columnas_interseccion = list(set(data.columns) & set(columnas_mantener))

            # Seleccionar solo las columnas de la intersección
            data = data.loc[:, columnas_interseccion]
            data = data.reindex(columns=columnas_mantener)

            print(data)

            # Realizar la predicción
            prediccion_codificada = self.modelo_pole.predict(data)
            self.screen7(prediccion_codificada)
        except Exception as e:
            # Captura del error y print del mensaje de error
            print("Error:", str(e))
            # self.textctrl.SetValue("")
            return
        return
    
    def data_coder(self, get_result):
        if self.weather == None or self.circuit == None:
            # Mostrar un mensaje de aviso
            QMessageBox.warning(self, 'Aviso', 'Debe haberse seleccionado circuito y clima.')
            return []
        data = []
        try:
            if get_result:
                print("1")
                driver_season_pos = self.driver_season.copy()
                circuit_season_pos = self.circuit_season.copy()
                print("2")
                result_circuit = self.results_class.get_f1_race_results(self.season, self.circuit)

                print("3")
                if result_circuit.empty:
                    print("3.1")
                    if self.grid_pos.__len__() == 0:
                        print("3.2")
                        for i in driver_season_pos['driver_id'].values:
                            # self.waitUntilButtonClicked(i)
                            dialog = WaitingDialog(i, self.grid_pos)
                            dialog.exec_()
                            selected_option = dialog.selected_option
                            self.grid_pos.append(selected_option)
                    result_circuit = pd.DataFrame({'driver_id': driver_season_pos['driver_id'].values, 'race_grid_position': self.grid_pos})
                    print(self.grid_pos)
                    result_circuit['race_date'] = date.today()
                    result_circuit['circuit_id'] = self.circuit
                    result_circuit['year'] = self.season
                    result_circuit['race_status'] = 'Finished'
                    
                    print("3.2")
                else:
                    driver_season_pos = driver_season_pos.drop('constructor_id', axis=1)
                    circuit_season_pos = circuit_season_pos.drop('race_round', axis=1)
                    print("4")
                result_circuit['race_weather'] = self.weather
                    
                   
                
                
                print("5")
                data = self.coder_class.encode_result(
                    result_circuit, 
                    driver_season_pos,
                    circuit_season_pos,
                    self.constructor_season
                )
                
                print("5")
            else:
                circuit_season_pole = self.circuit_season.copy()
                circuit_season_pole['race_weather'] = self.weather
                driver_pole = self.driver_season.copy()
                driver_pole = self.driver_season.copy()
                driver_pole['circuit_id'] = self.circuit
                driver_pole['year'] = self.season
                data = self.coder_class.encode( 
                    driver_pole,
                    circuit_season_pole,
                    self.constructor_season
                )
            return data
        except Exception as e:
            # Captura del error y print del mensaje de error
            print("Error:", str(e))
            QMessageBox.warning(self, "Advertencia", "La clasificación debe haberse realizado para poder predecir el dato.")
            raise e

if __name__ == '__main__':
    app = QApplication([])
    ex = MyApp()
    app.exec_()
