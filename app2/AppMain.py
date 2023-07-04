import wx
import joblib
import threading
import time
import pandas as pd
from AppDrivers import Drivers
from AppConstructors import Constructors
from AppCircuits import Circuits
from AppResults import Results
from AppCoder import Coder

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, title='Aplicación con Desplegables')
        self.SetTopWindow(frame)
        frame.Show()
        return True

class MyCustomPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        super(MyCustomPanel, self).__init__(parent, *args, **kwargs)

        self.modelo_race_pos = joblib.load('trained_model_race_pos.pkl')
        self.modelo_winner = joblib.load('trained_model_winner.pkl')
        self.modelo_pole = joblib.load('trained_model_pole.pkl')

        api_key = 'AIzaSyAjdhmdwEMtm91-dv-eb5FJ6Zoq0j_xepM'
        self.drivers_class = Drivers()
        self.constructors_class = Constructors()
        self.circuits_class = Circuits(api_key)
        self.results_class = Results()
        self.coder_class = Coder()

        self.Bind(wx.EVT_PAINT, self.OnPaint)

        # self.background_image = wx.Bitmap("imagen.jpg", wx.BITMAP_TYPE_ANY)
        display_size = wx.DisplaySize()
        half_width = display_size[0] // 2
        half_height = display_size[1] // 2
        # self.background_image = wx.Bitmap("wallpaper.jpg", wx.BITMAP_TYPE_ANY)
        wallpaper = wx.Image("wallpaper.jpg", wx.BITMAP_TYPE_ANY)
        wallpaper = wallpaper.Scale(half_width, half_height, wx.IMAGE_QUALITY_HIGH)
        self.background_image = wx.Bitmap(wallpaper)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        vbox.Add(hbox, flag=wx.EXPAND)

        # Desplegables en horizontal (igual que en el ejemplo anterior)
        label1 = wx.StaticText(self, label="Año:")
        hbox.Add(label1,  proportion=1, flag=wx.ALL, border=10)

        label2 = wx.StaticText(self, label="Piloto:")
        hbox.Add(label2,  proportion=1, flag=wx.ALL, border=10)

        label3 = wx.StaticText(self, label="Circuito")
        hbox.Add(label3,  proportion=1, flag=wx.ALL, border=10)

        label4 = wx.StaticText(self, label="Clima")
        hbox.Add(label4,  proportion=1, flag=wx.ALL, border=10)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox.Add(hbox, flag=wx.EXPAND)

        # Desplegables en horizontal (igual que en el ejemplo anterior)
        # self.constructor_season['constructor_id'].unique()
        seasons = [str(2022), str(2023)]
        self.combobox1 = wx.ComboBox(self, choices=seasons, style=wx.CB_DROPDOWN)
        hbox.Add(self.combobox1, proportion=1, flag=wx.ALL, border=10)

        choices = []
        self.combobox2 = wx.ComboBox(self, choices=choices, style=wx.CB_DROPDOWN)
        hbox.Add(self.combobox2, proportion=1, flag=wx.ALL, border=10)

        self.combobox3 = wx.ComboBox(self, choices=choices, style=wx.CB_DROPDOWN)
        hbox.Add(self.combobox3, proportion=1, flag=wx.ALL, border=10)

        weather_choices = ['dry', 'wet']
        self.combobox4 = wx.ComboBox(self, choices=weather_choices, style=wx.CB_DROPDOWN)
        hbox.Add(self.combobox4, proportion=1, flag=wx.ALL, border=10)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        vbox.Add(hbox2, flag=wx.EXPAND)

        button1 = wx.Button(self, label='Predecir resultado carrera')
        hbox2.Add(button1, proportion=1, flag=wx.ALL, border=10)

        button2 = wx.Button(self, label='Predecir si es ganador')
        hbox2.Add(button2, proportion=1, flag=wx.ALL, border=10)

        button3 = wx.Button(self, label='Predecir si es poleman')
        hbox2.Add(button3, proportion=1, flag=wx.ALL, border=10)

        self.textctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        vbox.Add(self.textctrl, proportion=1, flag=wx.ALL|wx.EXPAND, border=30)

        # hbox.Add(vbox, flag=wx.EXPAND)

        # self.textctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        # vbox.Add(self.textctrl, proportion=1, flag=wx.ALL|wx.EXPAND, border=10)

        self.SetSizer(vbox)
        button1.Bind(wx.EVT_BUTTON, self.OnButtonClick_pred_pos)
        button2.Bind(wx.EVT_BUTTON, self.OnButtonClick_pred_winner)
        button3.Bind(wx.EVT_BUTTON, self.OnButtonClick_pred_pole)
        self.combobox1.Bind(wx.EVT_COMBOBOX, self.OnComboboxChange)

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.background_image, 0, 0)

    def OnComboboxChange(self, event):
        # Iniciar hilo para obtener los datos de la API
        self.textctrl.SetValue("")
        self.season = int(self.combobox1.GetValue())
        self.textctrl.SetValue(self.textctrl.GetValue() + f'Obtenindo valores de la temporada: {self.season}...\n')
        thread = threading.Thread(target=self.GetDataThread)
        # Mostrar diálogo de progreso
        self.dialog = wx.ProgressDialog("Cargando", "Obteniendo datos...", maximum=10, parent=self, style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE)
        thread.start()

    def GetDataThread(self):
        self.dialog.Update(1)
        self.driver_season = self.drivers_class.get_season_drivers_from_Ergast(self.season)
        self.constructor_driver_season = self.drivers_class.get_constructor_driver_from_Ergast(self.season)
        self.dialog.Update(3)
        self.constructor_season = self.constructors_class.get_all_constructors_from_Ergast(self.season)
        self.dialog.Update(6)
        self.circuit_season = self.circuits_class.get_circuits_from_Ergast(self.season)
        self.dialog.Update(9)
        self.combobox2.Set(self.driver_season['driver_id'].unique())
        self.combobox3.Set(self.circuit_season['circuit_id'].unique())
        self.dialog.Update(10)
        # Cerrar diálogo de progreso
        self.dialog.Destroy()
        self.textctrl.SetValue(self.textctrl.GetValue() + f'Valores obtenidos.\n')

    def data_coder(self, get_result):
        if self.combobox1.GetSelection() == -1 or self.combobox2.GetSelection() == -1 or self.combobox3.GetSelection() == -1 or self.combobox4.GetSelection() == -1:
            wx.MessageBox("Debe rellenar todos los datos.", "Advertencia", wx.OK | wx.ICON_WARNING)
            return
        else:
            driver = []
            res = []
            self.data = []
        try:
            driver = pd.DataFrame(self.driver_season[self.driver_season['driver_id']  == self.combobox2.GetValue().replace('\'', '')])
            self.textctrl.SetValue(self.textctrl.GetValue() + f'Codificando datos...\n')
            if get_result:
                result_circuit = self.results_class.get_f1_race_results(self.season, self.combobox3.GetValue().replace('\'', ''))
                result_circuit['race_weather'] = self.combobox4.GetValue()
                res = result_circuit[result_circuit['driver_id']  == self.combobox2.GetValue().replace('\'', '')]
                self.data = self.coder_class.encode_result(
                    res, 
                    driver,
                    self.circuit_season,
                    self.constructor_season
                )
            else:
                self.circuit_season['race_weather'] = self.combobox4.GetValue()
                driver.loc[:, 'circuit_id'] = self.combobox3.GetValue()
                driver.loc[:, 'constructor_id'] = self.constructor_driver_season[self.combobox2.GetValue()]
                print(driver)
                self.data = self.coder_class.encode( 
                    driver,
                    self.circuit_season,
                    self.constructor_season
                )
        
            # print(result_circuit['race_weather'])
            
            # driver.to_csv('prueba0.csv', index=False)
            # res.to_csv('prueba0.csv', index=False)
            # print(driver)
            # print(res)
            
            self.textctrl.SetValue(self.textctrl.GetValue() + f'Datos codificados\n')
        except Exception as e:
            # Captura del error y print del mensaje de error
            print("Error:", str(e))
            wx.MessageBox("La clasificación debe haberse realizado para poder predecir el dato.", "Advertencia", wx.OK | wx.ICON_WARNING)
            raise e

    def OnButtonClick_pred_pos(self, event):
        self.textctrl.SetValue("")
        try:
            self.data_coder(True)
            self.textctrl.SetValue(self.textctrl.GetValue() + f'Iniciando predicción...\n')
            # Lista de columnas a mantener
            columnas_mantener = self.modelo_race_pos.feature_names_in_

            # Obtener la intersección entre las columnas del DataFrame y la lista de columnas a mantener
            columnas_interseccion = list(set(self.data.columns) & set(columnas_mantener))

            # Seleccionar solo las columnas de la intersección
            self.data = self.data.loc[:, columnas_interseccion]
            self.data = self.data.reindex(columns=columnas_mantener)

            # Realizar la predicción
            prediccion_codificada = self.modelo_race_pos.predict(self.data)
            self.textctrl.SetValue(self.textctrl.GetValue() + f'Predicción completada.\n')
            self.textctrl.SetValue(self.textctrl.GetValue() + f'Posición final = {int(prediccion_codificada[0])}.\n')
            message = f'La posición del piloto será: {int(prediccion_codificada[0])}'
            style = wx.OK | wx.ICON_INFORMATION

            dlg = wx.MessageBox(message, "Aviso", style)
        except Exception as e:
            # Captura del error y print del mensaje de error
            print("Error:", str(e))
            self.textctrl.SetValue("")
            return
        return
    
    def OnButtonClick_pred_pole(self, event):
        try:
            self.textctrl.SetValue("")
            self.data_coder(False)
            self.textctrl.SetValue(self.textctrl.GetValue() + f'Iniciando predicción...\n')
            # Lista de columnas a mantener
            columnas_mantener = self.modelo_pole.feature_names_in_

            # Obtener la intersección entre las columnas del DataFrame y la lista de columnas a mantener
            columnas_interseccion = list(set(self.data.columns) & set(columnas_mantener))

            # Seleccionar solo las columnas de la intersección
            self.data = self.data.loc[:, columnas_interseccion]
            self.data = self.data.reindex(columns=columnas_mantener)

            # Realizar la predicción
            prediccion_codificada = self.modelo_pole.predict(self.data)
            self.textctrl.SetValue(self.textctrl.GetValue() + f'Predicción completada.\n')

            if (bool(prediccion_codificada[0])):
                message = f'El piloto hará la pole!'
            else:
                message = f'El piloto no hará la pole'

            self.textctrl.SetValue(self.textctrl.GetValue() + f'{message}.\n')
            style = wx.OK | wx.ICON_INFORMATION
            dlg = wx.MessageBox(message, "Aviso", style)
        except Exception as e:
            # Captura del error y print del mensaje de error
            print("Error:", str(e))
            self.textctrl.SetValue("")
            return
        return
    
    def OnButtonClick_pred_winner(self, event):
        try:
            self.textctrl.SetValue("")
            self.data_coder(True)
            self.textctrl.SetValue(self.textctrl.GetValue() + f'Iniciando predicción...\n')
            # Lista de columnas a mantener
            columnas_mantener = self.modelo_winner.feature_names_in_

            # Obtener la intersección entre las columnas del DataFrame y la lista de columnas a mantener
            columnas_interseccion = list(set(self.data.columns) & set(columnas_mantener))

            # Seleccionar solo las columnas de la intersección
            self.data = self.data.loc[:, columnas_interseccion]
            self.data = self.data.reindex(columns=columnas_mantener)

            # Realizar la predicción
            prediccion_codificada = self.modelo_winner.predict(self.data)
            self.textctrl.SetValue(self.textctrl.GetValue() + f'Predicción completada.\n')
            
            if (bool(prediccion_codificada[0])):
                message = f'El piloto ganará la carrera!'
            else:
                message = f'El piloto no ganará la carrera'

            self.textctrl.SetValue(self.textctrl.GetValue() + f'{message}.\n')
            style = wx.OK | wx.ICON_INFORMATION
            dlg = wx.MessageBox(message, "Aviso", style)
        except Exception as e:
            # Captura del error y print del mensaje de error
            print("Error:", str(e))
            self.textctrl.SetValue("")
            return
        return
    
class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title)
        self.SetSize(self.GetHalfScreenSize())  # Establecer tamaño de ventana

        panel = MyCustomPanel(self)

    def GetHalfScreenSize(self):
        display_size = wx.DisplaySize()
        half_width = display_size[0] // 2
        half_height = display_size[1] // 2
        # Desactivar opción de redimensionamiento
        self.SetWindowStyle(self.GetWindowStyle() & ~wx.RESIZE_BORDER)

        return wx.Size(half_width, half_height)

if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()
