import sys
import os
import joblib
import pandas as pd
from datetime import date
# from collections import OrderedDict
from PyQt5.QtWidgets import QSpacerItem, QFrame, QDialog, QMessageBox, QApplication, QWidget, QStackedWidget, QVBoxLayout, QLabel, QComboBox, QDesktopWidget, QPushButton, QGridLayout,  QSizePolicy
from PyQt5.QtGui import QPixmap, QResizeEvent, QIcon
from PyQt5.QtCore import Qt, QSize, QEventLoop
from AppDialog import GridDialog

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from logic.AppDrivers import Drivers
from logic.AppConstructors import Constructors
from logic.AppCircuits import Circuits
from logic.AppResults import Results
from logic.AppCoder import Coder


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.waiting_dialog = None
        self.event_loop = None
        self.grid_pos = []

    def initUI(self):
        # Configuramos la ventana principal y cargamos los datos
        self.setWindowTitle('F1 Predictor App')
        self.setStyleSheet('background-color: white;')

        self.modelo_race_pos = joblib.load('data/models/trained_model_race_pos.pkl')
        self.modelo_winner = joblib.load('data/models/trained_model_winner.pkl')
        self.modelo_pole = joblib.load('data/models/trained_model_pole.pkl')

        self.results_class = Results()
        self.coder_class = Coder()

        self.season = 2023
        self.driver_season = pd.read_csv('data/datacsv/app_drivers.csv')
        self.circuit_season = pd.read_csv('data/datacsv/app_circuits.csv')
        self.constructor_season = pd.read_csv('data/datacsv/app_constructor_season.csv')

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

        # Creamos el layout principal
        layout = QVBoxLayout()

        # Creamos el widget de navegación
        self.stacked_widget = QStackedWidget()

        # Creamos las diferentes pantallas de la aplicación
        screen1 = QWidget()
        screen2 = QWidget()
        screen3 = QWidget()
        screen4 = QWidget()

        # Se las asignamos al layout
        screen1.setLayout(self.screen1())
        screen2.setLayout(self.screen2())
        screen3.setLayout(self.screen3())
        screen4.setLayout(self.screen4())
        

        # Agregamos las pantallas al widget de navegación
        self.stacked_widget.addWidget(screen1)
        self.stacked_widget.addWidget(screen2)
        self.stacked_widget.addWidget(screen3)
        self.stacked_widget.addWidget(screen4)

        # Agregamos el widget de navegación al layout principal
        layout.addWidget(self.stacked_widget)

        # Establecemos la pantalla inicial
        self.stacked_widget.setCurrentIndex(0)

        # Agregamos el layout a la ventana
        self.setLayout(layout)

        # Mostramos la ventana
        self.show()

    def screen1(self):
        # Agregamos contenido a la pantalla home
        screen_layout = QVBoxLayout()
        size = QSize(1300,900)
        button1 = self.create_button('data/img/wallpaper.jpeg', size, self.go_to_screen2)
        screen_layout.addWidget(button1)

        return screen_layout  
  
    def screen2(self):
        # Layout con configuración inicial
        screen_layout = QGridLayout()
        size = QSize(500,70)
        button = QPushButton()
        pixmap = QPixmap('data/img/selectcircuit.png')
        pixmap = pixmap.scaled(size)

        # Obtenemos las dimensiones de la imagen
        width = pixmap.width()
        height = pixmap.height()

        # Establecemos el tamaño del botón según las dimensiones de la imagen
        button.setFixedSize(width, height)

        # Establecemos la imagen como icono del botón
        button.setIcon(QIcon(pixmap))
        button.setIconSize(button.size())
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        screen_layout.addWidget(button, 0, 0)
        
        # Ordenamos los circuitos en base a su fecha de realización
        fila = 1
        columna = 0
        for circuit in self.circuit_season.sort_values('race_round')['circuit_id']:
            # Creamos el botón
            button = self.create_button(f'data/circuits/{circuit}.png', size,self.go_to_screen3, f'id-{circuit}')
            # Agregamos el botón al layout
            screen_layout.addWidget(button, fila, columna)
            
            columna += 1
            if columna == 2:
                fila += 1
                columna = 0

        return(screen_layout)

    def screen3(self):
        # Agregamos el contenido a la pantalla y creamos el contenedor para los layouts
        container = QWidget(self)

        # Creamos el layout principal y el layout secundario
        screen_layout = QVBoxLayout(container)
        label_layout = QVBoxLayout()
        frames_layout = QVBoxLayout()

        # Creamos un marco para la pantalla en tiempo de ejecución
        self.frame = QFrame(self)

        # Establecemos un diseño en el marco
        frame_layout = QGridLayout(self.frame)
        
        size = QSize(500, 560)
        button1 = self.create_button('data/weather/dry.png', size, self.go_to_screen4, 'clima-dry')
        button2 = self.create_button('data/weather/wet.png', size, self.go_to_screen4, 'clima-wet')
        
        # Agregamos los botones al layout
        frame_layout.addWidget(button1, 0, 0)
        frame_layout.addWidget(button2, 0, 1)
        self.frame.setLayout(frame_layout)
        frames_layout.addWidget(self.frame)

        # Agregamos el texto
        label = QLabel()
        pixmap = QPixmap('data/img/selectweather.png')
        scaled_pixmap = pixmap.scaled(QSize(600,70))
        label.setPixmap(scaled_pixmap)
        label_layout.addWidget(label) 

        # Añadimos todo a la pantalla principal
        screen_layout.addLayout(label_layout)
        screen_layout.addLayout(frames_layout)

        return(screen_layout)
   
    def screen4(self):
        # Agregamos el contenido a la pantalla y creamos el contenedor para los layouts
        container = QWidget(self)
        screen_layout = QVBoxLayout(container)

        # Creamos el layout principal y el layout secundario
        frames_layout = QVBoxLayout()
        buttons_layout = QGridLayout()
            
        # Creamos los botones
        size = QSize(300,55)
        button_pos = self.create_button(f'data/img/pred_pos.png', size, self.OnButtonClick_pred_pos)
        button_winner = self.create_button(f'data/img/pred_winner.png', size, self.OnButtonClick_pred_winner)
        button_poleman = self.create_button(f'data/img/pred_poleman.png', size, self.OnButtonClick_pred_poleman)
        size = QSize(200,55)
        button_back = self.create_button(f'data/img/home.png', size, self.go_to_screen1)

        # Creamos un marco para la pantalla 
        self.frame = QFrame(self)

        # Establecemos el marco en un layout
        frame_layout = QGridLayout(self.frame)
        self.frame.setLayout(frame_layout)

        # Agregamos los componentes a su layout y al principal
        buttons_layout.addWidget(button_pos, 0, 0)
        buttons_layout.addWidget(button_winner, 0, 1)
        buttons_layout.addWidget(button_poleman, 0, 2)
        buttons_layout.addWidget(button_back, 0, 3)
        frames_layout.addWidget(self.frame)
        screen_layout.addLayout(buttons_layout)
        screen_layout.addLayout(frames_layout)

        return(screen_layout)
    
    def screen5(self, predicciones):
        # Limpiamos el contenido anterior del marco
        frame_layout = self.clean_frame()
        
        # Generamos los componentes de la predicción
        size_driver = QSize(350, 30)
        size_pos = QSize(100, 30)
        fila = 0
        columna = 1
        dict_final = {}
        for i, driver in enumerate(self.driver_season['driver_id']):
            dict_final[driver] = predicciones[i]
        diccionario_ordenado = dict(sorted(dict_final.items(), key=lambda x: x[1]))

        for pos, driver in enumerate(diccionario_ordenado):
            # Creamos los botones
            button = self.create_button(f'data/drivers/{driver}.png', size_driver, self.go_to_screen1)
            button_pos = self.create_button(f'data/pos/p{pos+1}.png', size_pos, self.go_to_screen1)
            # Agregamos los botones al layout
            frame_layout.addWidget(button, fila, columna)
            frame_layout.addWidget(button_pos, fila, columna-1)
            
            columna += 2
            fila += 1
            if columna == 5:
                fila += 1
                columna = 1

        return(frame_layout) 
    
    def screen6(self, predicciones):
        # Limpiamos el contenido anterior del marco
        frame_layout = self.clean_frame()

        # Generamos los componentes de la predicción
        size_driver = QSize(450, 50)
        size_pos = QSize(140, 50)
        dict_final = {}
        for i, driver in enumerate(self.driver_season['driver_id']):
            dict_final[driver] = predicciones[i]
        diccionario_ordenado = dict(sorted(dict_final.items(), key=lambda x: x[1]))

        for pos, driver in enumerate(diccionario_ordenado):
            # Creamos los botones
            button = self.create_button(f'data/drivers/{driver}.png', size_driver, self.go_to_screen1)
            button_pos = self.create_button(f'data/pos/p{pos+1}.png', size_pos, self.go_to_screen1)
            # Agregamos los botones al layout
            frame_layout.addWidget(button, 0, 1)
            frame_layout.addWidget(button_pos, 0, 0)
            break

        return(frame_layout) #  
    
    def screen7(self, predicciones):
        # Limpiamos el contenido anterior del marco
        frame_layout = self.clean_frame()

        # Generamos los componentes de la predicción
        size_driver = QSize(450, 50)
        size_pos = QSize(140, 50)
        dict_final = {}
        for i, driver in enumerate(self.driver_season['driver_id']):
            dict_final[driver] = predicciones[i]
        diccionario_ordenado = dict(sorted(dict_final.items(), key=lambda x: x[1], reverse=True))

        for pos, driver in enumerate(diccionario_ordenado):
            if diccionario_ordenado[driver] == 0:
                driver = 'max_verstappen'
            # Creamos los botones
            button = self.create_button(f'data/drivers/{driver}.png', size_driver, self.go_to_screen1)
            button_pos = self.create_button(f'data/pos/p1.png', size_pos, self.go_to_screen1)
            # Agregamos los botones al layout
            frame_layout.addWidget(button, 0, 1)
            frame_layout.addWidget(button_pos, 0, 0)
            break

        return(frame_layout)

    def create_button(self, image_path, size, go_to_screen, property = None):
        try:
            # Creamos el botón con la imagen
            button = QPushButton(clicked=go_to_screen)
            if property != None:
                id = property.split("-")[0]
                valor = property.split("-")[1]
                button.setProperty(id, valor)
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(size)

            # Obtenemos las dimensiones de la imagen
            width = pixmap.width()
            height = pixmap.height()

            # Establecemos el tamaño del botón según las dimensiones de la imagen
            button.setFixedSize(width, height)

            # Establecemos la imagen como icono del botón
            button.setIcon(QIcon(pixmap))
            button.setIconSize(button.size()) 
            button.clicked.connect(self.buttonClicked)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        except:
            print("Error on image: " + image_path)

        return button
    
    def clean_frame(self):
        # Limpiamos el contenido del marco
        frame_layout = self.frame.layout()
        if frame_layout is not None:
            while frame_layout.count():
                item = frame_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
        return frame_layout
    
    def go_to_screen1(self):
        # Limpiamos el contenido anterior del marco
        self.clean_frame()

        # Establecemos los valores por defecto
        self.circuit = None
        self.weather = None
        self.grid_pos = []
        # Vamos a pantalla de inicio
        self.stacked_widget.setCurrentIndex(0)

    def go_to_screen2(self):
        # Vamos a pantalla 1
        self.stacked_widget.setCurrentIndex(1)

    def go_to_screen3(self):
        # Vamos a pantalla 2
        self.stacked_widget.setCurrentIndex(2)

    def go_to_screen4(self):
        # Vamos a pantalla 3
        self.stacked_widget.setCurrentIndex(3)

    def buttonClicked(self):
        # Establecemos las propiedades escogidas
        sender = self.sender()
        if sender.property('id'):
            self.circuit = sender.property('id')
        if sender.property('clima'):
            self.weather = sender.property('clima')
        
    def OnButtonClick_pred_pos(self,):
        try:
            # Codificación de los datos
            data = self.data_coder(True)

            # Lista de columnas de entrenamiento
            columnas_mantener = self.modelo_race_pos.feature_names_in_

            # Obtenemos la intersección entre las columnas del DataFrame y la lista de columnas del entrenamiento
            columnas_interseccion = list(set(data.columns) & set(columnas_mantener))

            # Seleccionamos solo las columnas de la intersección
            data = data.loc[:, columnas_interseccion]
            data = data.reindex(columns=columnas_mantener)

            # Realizamos y mostramos la predicción
            prediccion_codificada = self.modelo_race_pos.predict(data)
            self.screen5(prediccion_codificada)

        except Exception as e:
            print("Error: ", str(e))
            return
        return
    
    def OnButtonClick_pred_winner(self,):
        try:
            # Codificación de los datos
            data = self.data_coder(True)

            # Lista de columnas de entrenamiento
            columnas_mantener = self.modelo_race_pos.feature_names_in_

            # Obtenemos la intersección entre las columnas del DataFrame y la lista de columnas del entrenamiento
            columnas_interseccion = list(set(data.columns) & set(columnas_mantener))

            # Seleccionamos solo las columnas de la intersección
            data = data.loc[:, columnas_interseccion]
            data = data.reindex(columns=columnas_mantener)

            # Realizamos y mostramos la predicción
            prediccion_codificada = self.modelo_race_pos.predict(data)
            self.screen6(prediccion_codificada)
        except Exception as e:
            print("Error:", str(e))
            return
        return
    
    def OnButtonClick_pred_poleman(self,):
        try:
            # Codificación de los datos
            data = self.data_coder(False)
            
            # Lista de columnas de entrenamiento
            columnas_mantener = self.modelo_pole.feature_names_in_

            # Obtenemos la intersección entre las columnas del DataFrame y la lista de columnas del entrenamiento
            columnas_interseccion = list(set(data.columns) & set(columnas_mantener))

            # Seleccionamos solo las columnas de la intersección
            data = data.loc[:, columnas_interseccion]
            data = data.reindex(columns=columnas_mantener)

            # Realizamos y mostramos la predicción
            prediccion_codificada = self.modelo_pole.predict(data)
            self.screen7(prediccion_codificada)
        except Exception as e:
            print("Error:", str(e))
            return
        return
    
    def data_coder(self, get_result):
        if self.weather == None or self.circuit == None:
            # Mostramos un mensaje de aviso porqeu debe haber datos seleccionados
            QMessageBox.warning(self, 'Aviso', 'Debe haberse seleccionado circuito y clima.')
            return []
        data = []
        try:
            if get_result:
                driver_season_pos = self.driver_season.copy()
                circuit_season_pos = self.circuit_season.copy()
                result_circuit = self.results_class.get_f1_race_results(self.season, self.circuit)
                if result_circuit.empty:
                    if self.grid_pos.__len__() == 0:
                        for i in driver_season_pos['driver_id'].values:
                            dialog = GridDialog(i, self.grid_pos)
                            dialog.exec_()
                            selected_option = dialog.selected_option
                            self.grid_pos.append(selected_option)
                    result_circuit = pd.DataFrame({'driver_id': driver_season_pos['driver_id'].values, 'race_grid_position': self.grid_pos})
                    result_circuit['race_date'] = date.today()
                    result_circuit['circuit_id'] = self.circuit
                    result_circuit['year'] = self.season
                    result_circuit['race_status'] = 'Finished'
                else:
                    driver_season_pos = driver_season_pos.drop('constructor_id', axis=1)
                    circuit_season_pos = circuit_season_pos.drop('race_round', axis=1)
                result_circuit['race_weather'] = self.weather
                    
                data = self.coder_class.encode_result(
                    result_circuit, 
                    driver_season_pos,
                    circuit_season_pos,
                    self.constructor_season
                )
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
