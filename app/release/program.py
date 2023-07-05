import sys
import os
import joblib
import pandas as pd
from datetime import date

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from logic.AppDrivers import Drivers
from logic.AppConstructors import Constructors
from logic.AppCircuits import Circuits
from logic.AppResults import Results
from logic.AppCoder import Coder

def data_coder(get_result):
        if eleccion_cilma == None or eleccion_cir == None:
            # Mostramos un mensaje de aviso porqeu debe haber datos seleccionados
            print('Debe haberse seleccionado circuito y clima.')
            return None
        data = []
        try:
            if get_result:
                driver_season_pos = driver_season.copy()
                circuit_season_pos = circuit_season.copy()
                result_circuit = results_class.get_f1_race_results(season, eleccion_cir)
                if result_circuit.empty:
                    if grid_pos.__len__() == 0:
                        for i in driver_season_pos['driver_id'].values:
                            print(f'Escoge la posicion de {i}\n')
                            rango = list(range(1,21))
                            actualy_pos = [x for x in rango if x not in grid_pos]
                            print(f'Psiciones disponibles: \n')
                            print(actualy_pos)
                            eleccion_pos = input("Por favor, elige la posición: ")
                            eleccion_pos = int(eleccion_pos)
                            if eleccion_pos in actualy_pos:
                                grid_pos.append(eleccion_pos)
                            else:
                                return pd.DataFrame()
                    result_circuit = pd.DataFrame({'driver_id': driver_season_pos['driver_id'].values, 'race_grid_position': grid_pos})
                    result_circuit['race_date'] = date.today()
                    result_circuit['circuit_id'] = eleccion_cir
                    result_circuit['year'] = season
                    result_circuit['race_status'] = 'Finished'
                else:
                    driver_season_pos = driver_season_pos.drop('constructor_id', axis=1)
                    circuit_season_pos = circuit_season_pos.drop('race_round', axis=1)
                result_circuit['race_weather'] = eleccion_cilma
                    
                data = coder_class.encode_result(
                    result_circuit, 
                    driver_season_pos,
                    circuit_season_pos,
                    constructor_season
                )
            else:
                circuit_season_pole = circuit_season.copy()
                circuit_season_pole['race_weather'] = eleccion_cilma
                driver_pole = driver_season.copy()
                driver_pole = driver_season.copy()
                driver_pole['circuit_id'] = eleccion_cir
                driver_pole['year'] = season
                data = coder_class.encode( 
                    driver_pole,
                    circuit_season_pole,
                    constructor_season
                )
            return data
        except Exception as e:
            # Captura del error y print del mensaje de error
            print("Error:", str(e))
            raise e

modelo_race_pos = joblib.load('data/models/trained_model_race_pos.pkl')
modelo_winner = joblib.load('data/models/trained_model_winner.pkl')
modelo_pole = joblib.load('data/models/trained_model_pole.pkl')

results_class = Results()
coder_class = Coder()

season = 2023
driver_season = pd.read_csv('data/datacsv/app_drivers.csv')
circuit_season = pd.read_csv('data/datacsv/app_circuits.csv')
constructor_season = pd.read_csv('data/datacsv/app_constructor_season.csv')

grid_pos = []


rounds = {
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

circuit_season['race_round'] = circuit_season['circuit_id'].map(rounds)

input("Por favor, pulse enter para continuar\n")
election = {}
for num, circuit in enumerate(circuit_season.sort_values('race_round')['circuit_id']):
    election[num] = circuit
    print(f'{num}: {circuit}\n')

eleccion_cir = input("Por favor, elige el circuito: ")
eleccion_cir = int(eleccion_cir)
if eleccion_cir in election.keys():
    eleccion_cir = election[eleccion_cir]
    election = {}
    election[1] = "dry"
    election[2] = "wet"

    print('1: dry\n')
    print('2: wet\n')
    eleccion_cilma = input("Por favor, elige el clima: ")
    eleccion_cilma = int(eleccion_cilma)
    if eleccion_cilma in election.keys():
        eleccion_cilma = election[eleccion_cilma]
        election = {}
        election[1] = modelo_race_pos
        election[2] = modelo_winner
        election[3] = modelo_pole
        print('1: Predicción resultados\n')
        print('2: Predicción ganador\n')
        print('3: Predicción poleman\n')
        eleccion_pred = input("Por favor, elige la predicción deseada: ")
        eleccion_pred = int(eleccion_pred)
        get_results = True
        if eleccion_pred == 3:
            get_results = False
        if eleccion_pred in election.keys():
            model = election[eleccion_pred]
            try:
                # Codificación de los datos
                data = data_coder(get_results)

                if data.empty:
                    print("Elije una opcion de las mostradas.")  
                else:

                    # Lista de columnas de entrenamiento
                    columnas_mantener = model.feature_names_in_

                    # Obtenemos la intersección entre las columnas del DataFrame y la lista de columnas del entrenamiento
                    columnas_interseccion = list(set(data.columns) & set(columnas_mantener))

                    # Seleccionamos solo las columnas de la intersección
                    data = data.loc[:, columnas_interseccion]
                    data = data.reindex(columns=columnas_mantener)

                    # Realizamos y mostramos la predicción
                    prediccion_codificada = model.predict(data)

                    print('Predicción:')

                    dict_final = {}
                    for i, driver in enumerate(driver_season['driver_id']):
                        dict_final[driver] = prediccion_codificada[i]
                    diccionario_ordenado = dict(sorted(dict_final.items(), key=lambda x: x[1]))

                    for pos, driver in enumerate(diccionario_ordenado):
                        print(f'{pos+1}: {driver}')
                        if eleccion_pred != 1:
                            break

            except Exception as e:
                print("Error: ", str(e))
        else:
            print("Elije una opcion de las mostradas.")   
    else:
        print("Elije una opcion de las mostradas.")    
else:
    print("Elije una opcion de las mostradas.")
