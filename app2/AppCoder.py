import pandas as pd
from sklearn.preprocessing import StandardScaler,LabelEncoder,OneHotEncoder
import joblib

class Coder:
    def __init__(self):
        self.coders = joblib.load('codificadores.pkl')
        self.all_data = pd.read_csv('all_data.csv')
        return

    def encode_result(self, data_result, data_driver, data_circuit, data_constructor):
        # print('Paso 1')
        # Combinamos los DataFrames utilizando el id de cada uno como clave de combinación
        # print(data['race_weather'])
        data = data_driver.merge(data_result, on='driver_id', how='left')
        # print('Paso 1')
        # print(data)
        data = data.merge(data_circuit, on='circuit_id', how='left')
        # print('Paso 1')
        # print(data)
        data = data.merge(data_constructor, on='constructor_id', how='left')
        # print('Paso 1')
        # print(data)
        # print('Paso 1.1')
        # data.to_csv('prueba0.csv', index=False)
        data = self.prepare_data_with_results(data)
        data.to_csv('prueba1.csv', index=False)
        # print(data)
        # print(data['race_weather'])

        # print('Paso 2')

        # Convertimos primero a fecha
        data['race_date'] = pd.to_datetime(data['race_date'])
        data['driver_date_of_birth'] = pd.to_datetime(data['driver_date_of_birth'])
        self.all_data['race_date'] = pd.to_datetime(self.all_data['race_date'])
        self.all_data['driver_date_of_birth'] = pd.to_datetime(self.all_data['driver_date_of_birth'])

        # Utilizaremos el día de nacimiento más antigua como fecha de referencia para la conversión
        reference_race_date = self.all_data['race_date'].min()
        reference_driver_date_of_birth = self.all_data['driver_date_of_birth'].min()

        # Creamos las nuevas columnas
        data['race_date_numeric'] = (data['race_date'] - reference_race_date).dt.total_seconds()
        data['driver_date_of_birth_numeric'] = (data['driver_date_of_birth'] - reference_driver_date_of_birth).dt.total_seconds()
        
        # print('Paso 3')

        # Codificación ordinal
        data['driver_id'] = self.coders['driver_id'].transform(data['driver_id'])

        data['circuit_id'] = self.coders['circuit_id'].transform(data['circuit_id'])

        data['constructor_id'] = self.coders['constructor_id'].transform(data['constructor_id'])

        data = self.cod_oh(data,'race_weather')
        data = self.cod_oh(data,'driver_nationality_country')
        data = self.cod_oh(data,'constructor_nationality_country')
        data = self.cod_oh(data,'circuit_country')

        # Eliminamos las columnas viejas
        data = data.drop('race_date', axis=1)
        data = data.drop('driver_date_of_birth', axis=1)

        # print('Paso 4')

        # Eliminación de las columnas que ya no son necesarias por existir ya codificadas
        columnas_eliminar = ['race_weather','driver_nationality_country', 'constructor_nationality_country', 'circuit_country']
        data = data.drop(columnas_eliminar, axis=1)
        return data
    
    def encode(self, data_driver, data_circuit, data_constructor):
        # print('Paso 1')
        # Combinamos los DataFrames utilizando el id de cada uno como clave de combinación
        # print(data['race_weather'])
        # print('Paso 1')
        # print(data)
        data = data_driver.merge(data_circuit, on='circuit_id', how='left')
        # print('Paso 1')
        # print(data)
        data = data.merge(data_constructor, on='constructor_id', how='left')
        data['race_date'] = pd.Timestamp.today()
        # print('Paso 1')
        # print(data)
        # print('Paso 1.1')
        # data.to_csv('prueba0.csv', index=False)
        data = self.prepare_data(data)
        data.to_csv('prueba1.csv', index=False)
        # print(data)
        # print(data['race_weather'])

        # print('Paso 2')

        # Convertimos primero a fecha
        data['driver_date_of_birth'] = pd.to_datetime(data['driver_date_of_birth'])
        self.all_data['race_date'] = pd.to_datetime(self.all_data['race_date'])
        self.all_data['driver_date_of_birth'] = pd.to_datetime(self.all_data['driver_date_of_birth'])

        # Utilizaremos el día de nacimiento más antigua como fecha de referencia para la conversión
        reference_race_date = self.all_data['race_date'].min()
        reference_driver_date_of_birth = self.all_data['driver_date_of_birth'].min()

        # Creamos las nuevas columnas
        data['race_date_numeric'] = (data['race_date'] - reference_race_date).dt.total_seconds()
        data['driver_date_of_birth_numeric'] = (data['driver_date_of_birth'] - reference_driver_date_of_birth).dt.total_seconds()
        
        # print('Paso 3')

        # Codificación ordinal
        data['driver_id'] = self.coders['driver_id'].transform(data['driver_id'])

        data['circuit_id'] = self.coders['circuit_id'].transform(data['circuit_id'])

        data['constructor_id'] = self.coders['constructor_id'].transform(data['constructor_id'])

        data = self.cod_oh(data,'race_weather')
        data = self.cod_oh(data,'driver_nationality_country')
        data = self.cod_oh(data,'constructor_nationality_country')
        data = self.cod_oh(data,'circuit_country')

        # Eliminamos las columnas viejas
        data = data.drop('race_date', axis=1)
        data = data.drop('driver_date_of_birth', axis=1)

        # print('Paso 4')

        # Eliminación de las columnas que ya no son necesarias por existir ya codificadas
        columnas_eliminar = ['race_weather','driver_nationality_country', 'constructor_nationality_country', 'circuit_country']
        data = data.drop(columnas_eliminar, axis=1)
        return data
    
    def decode(self, data):
        
        return
    
    # Codificación One-Hot 
    def cod_oh(self, df, columna):
        # print(df[columna])
        # print(self.coders[columna])
        # print(self.coders[columna].categories_[0])
        encoded_column = self.coders[columna].transform(df[[columna]])
        df_encoded = pd.DataFrame(encoded_column.toarray(), columns=columna+ "_" + self.coders[columna].categories_[0])
        df_final = pd.concat([df, df_encoded], axis=1)
        return df_final
    

    def prepare_data(self, data):

        """
        Modificamos algunos nombres de equipos porque han cambiado de nombre
        por patrocionios pero realmente son el mismo
        """
        constructors_history = {
            'bmw_sauber' : 'alfa',
            'sauber' : 'alfa',
            'stewart' : 'red_bull',
            'Jaguar' : 'red_bull',
            'jordan' : 'aston_martin',
            'force_india' : 'aston_martin',
            'benetton' : 'renault',
            'toleman' : 'renault',
            'lotus_f1' : 'renault',
            'alpine' : 'renault',
            'minardi' : 'alphatauri',
            'toro_rosso' : 'alphatauri',
            'fondmetal' : 'ags',
            'honda' : 'mercedes',
            'brawn' : 'mercedes',
            'tyrrell' : 'mercedes',
            'bar' : 'mercedes',
            'team_lotus' : 'caterham',
            'footwork' : 'arrows',
            'marussia' : 'manor',
            'virgin' : 'manor',
            'lotus-brm' : 'lotus-borgward',
            'lotus-climax' : 'lotus-borgward',
            'lotus-ford' : 'lotus-borgward',
            'lotus-maserati' : 'lotus-borgward',
            'lotus-pw' : 'lotus-borgward',
            'brabham-alfa_romeo' : 'brabham',
            'brabham-brm' : 'brabham',
            'brabham-climax' : 'brabham',
            'brabham-ford' : 'brabham',
            'brabham-repco' : 'brabham',
            'brm-ford' : 'brm',
            'de_tomaso-alfa_romeo' : 'tomaso',
            'de_tomaso-ferrari' : 'tomaso',
            'de_tomaso-osca' : 'tomaso',
            'cooper-alfa_romeo' : 'cooper',
            'cooper-ats' : 'cooper',
            'cooper-borgward' : 'cooper',
            'cooper-brm' : 'cooper',
            'cooper-castellotti' : 'cooper',
            'cooper-climax' : 'cooper',
            'cooper-ferrari' : 'cooper',
            'cooper-ford' : 'cooper',
            'cooper-maserati' : 'cooper',
            'cooper-osca' : 'cooper',
            'march-alfa_romeo' : 'march',
            'march-ford' : 'march'
        }

        data['constructor_id'] = data['constructor_id'].map(constructors_history).fillna(data['constructor_id'])
        # print('prep 2')

        """
        Modificamos las nacionalidades para tener únicamente países para
        que el país del circuito y la nacionalidad del piloto o equipo coincidan
        """
        # print(data['driver_nationality'])
        nationality_to_country = {
            'Italian': 'Italy',
            'British': 'UK',
            'French': 'France',
            'Belgian': 'Belgium',
            'Argentine': 'Argentina',
            'Irish': 'Ireland',
            'Thai': 'Thailand',
            'Swiss': 'Switzerland',
            'Monegasque': 'Monaco',
            'American': 'USA',
            'Spanish': 'Spain',
            'Australian': 'Australia',
            'Brazilian': 'Brazil',
            'Uruguayan': 'Uruguay',
            'German': 'Germany',
            'Swedish': 'Sweden',
            'Dutch': 'Netherlands',
            'New Zealander': 'New Zealand',
            'South African': 'South Africa',
            'Mexican': 'Mexico',
            'Austrian': 'Austria',
            'Liechtensteiner': 'Liechtenstein',
            'Japanese': 'Japan',
            'Finnish': 'Finland',
            'Canadian': 'Canada',
            'Chilean': 'Chile',
            'Colombian': 'Colombia',
            'Venezuelan': 'Venezuela',
            'Portuguese': 'Portugal',
            'Danish': 'Denmark',
            'Hungarian': 'Hungary',
            'Indian': 'India',
            'Polish': 'Poland',
            'Russian': 'Russia',
            'Indonesian': 'Indonesia',
            'Malaysian': 'Malaysia',
            'American-Italian': 'USA',
            'Rhodesian': 'Zimbabwe',
            'Czech': 'Czech Republic',
            'East German': 'Germany',
            'Argentine-Italian': 'Argentina'
        }

        data['driver_nationality_country'] = data['driver_nationality'].map(nationality_to_country).fillna(data['driver_nationality'])
        data['constructor_nationality_country'] = data['constructor_nationality'].map(nationality_to_country).fillna(data['constructor_nationality'])

        """
        Añadimos la edad del piloto durante la carrera
        """
        # Convertimos las columnas de fecha al formato datetime
        data['driver_date_of_birth'] = pd.to_datetime(data['driver_date_of_birth'])
        data['race_date'] = pd.to_datetime(data['race_date'])

        # Calculamos la edad en base a la fecha de nacimiento y la fecha de la carrera
        data['driver_age'] = (data['race_date'] - data['driver_date_of_birth']).dt.days // 365
        

        
        # Obtener los valores únicos de las columnas 'A' y 'B'
        columnas_seleccionadas_ccr = ['constructor_id', 'constructor_car_relaiblity']
        columnas_seleccionadas_da = ['driver_id', 'driver_awareness']
        valores_unicos_ccr = self.all_data.drop_duplicates(subset=columnas_seleccionadas_ccr)
        valores_unicos_da = self.all_data.drop_duplicates(subset=columnas_seleccionadas_da)

        dict_ccr = dict(valores_unicos_ccr[columnas_seleccionadas_ccr].values)
        dict_da = dict(valores_unicos_da[columnas_seleccionadas_da].values)

        data['constructor_car_relaiblity'] = data['constructor_id'].map(dict_ccr)
        data['driver_awareness'] = data['driver_id'].map(dict_da)

        return data

    def prepare_data_with_results(self, data):
        """
        Añadimos estado final de carrera más simple en función
        de el estado fional de carrera
        """
        # print('prep 1')
        diccionario_clasificacion = {
            'Finished': 'finished',
            '+1 Lap': 'finished',
            '+2 Laps': 'finished',
            '+3 Laps': 'finished',
            '+4 Laps': 'finished',
            '+5 Laps': 'finished',
            '+6 Laps': 'finished',
            '+7 Laps': 'finished',
            '+8 Laps': 'finished',
            '+9 Laps': 'finished',
            '+10 Laps': 'finished',
            '+11 Laps': 'finished',
            '+12 Laps': 'finished',
            '+13 Laps': 'finished',
            '+14 Laps': 'finished',
            '+15 Laps': 'finished',
            '+16 Laps': 'finished',
            '+17 Laps': 'finished',
            '+18 Laps': 'finished',
            '+19 Laps': 'finished',
            '+20 Laps': 'finished',
            '+21 Laps': 'finished',
            '+22 Laps': 'finished',
            '+23 Laps': 'finished',
            '+24 Laps': 'finished',
            '+25 Laps': 'finished',
            '+26 Laps': 'finished',
            '+29 Laps': 'finished',
            '+30 Laps': 'finished',
            '+42 Laps': 'finished',
            '+44 Laps': 'finished',
            'Oil leak': 'engine failure',
            'Not classified': 'mechanical failure',
            'Out of fuel': 'mechanical failure',
            'Engine': 'engine failure',
            'Transmission': 'mechanical failure',
            'Clutch': 'mechanical failure',
            'Oil pressure': 'mechanical failure',
            'Gearbox': 'mechanical failure',
            'Supercharger': 'mechanical failure',
            'Axle': 'mechanical failure',
            'Accident': 'driver mistake',
            'Collision': 'driver mistake',
            'Spun off': 'driver mistake',
            'Oil line': 'mechanical failure',
            'Wheel bearing': 'mechanical failure',
            'Stalled': 'driver mistake',
            'Suspension': 'mechanical failure',
            'Oil pump': 'mechanical failure',
            'Oil pipe': 'mechanical failure',
            'Overheating': 'mechanical failure',
            'Fuel pump': 'mechanical failure',
            'Radiator': 'mechanical failure',
            'Retired': 'driver mistake',
            'Brakes': 'mechanical failure',
            'Water pipe': 'mechanical failure',
            'Withdrew': 'driver mistake',
            'Magneto': 'mechanical failure',
            'Ignition': 'engine failure',
            'Fuel system': 'mechanical failure',
            'Heat shield fire': 'mechanical failure',
            'Fuel leak': 'mechanical failure',
            'Wheel': 'mechanical failure',
            'Halfshaft': 'mechanical failure',
            'Steering': 'mechanical failure',
            'Differential': 'mechanical failure',
            'Turbo': 'engine failure',
            'Exhaust': 'mechanical failure',
            'Disqualified': 'driver mistake',
            'Electrical': 'engine failure',
            'Did not qualify': 'driver mistake',
            'Throttle': 'mechanical failure',
            'Physical': 'driver mistake',
            '+46 Laps': 'finished',
            'Injection': 'engine failure',
            'Fuel pressure': 'mechanical failure',
            'Tyre': 'mechanical failure',
            'Chassis': 'mechanical failure',
            'Water leak': 'mechanical failure',
            'Water pump': 'mechanical failure',
            'Distributor': 'mechanical failure',
            'Handling': 'mechanical failure',
            'Vibrations': 'mechanical failure',
            'Puncture': 'mechanical failure',
            'Battery': 'mechanical failure',
            'Driver unwell': 'driver mistake',
            'Did not prequalify': 'driver mistake',
            'Alternator': 'engine failure',
            'Injury': 'driver mistake',
            'Broken wing': 'driver mistake',
            'Fuel pipe': 'mechanical failure',
            'Fatal accident': 'driver mistake',
            'Eye injury': 'driver mistake',
            'Injured': 'driver mistake',
            'Mechanical': 'mechanical failure',
            'Spark plugs': 'engine failure',
            'CV joint': 'mechanical failure',
            'Excluded': 'driver mistake',
            'Driveshaft': 'mechanical failure',
            'Hydraulics': 'mechanical failure',
            'Fire': 'engine failure',
            'Safety belt': 'mechanical failure',
            '107% Rule': 'mechanical failure',
            'Fuel': 'mechanical failure',
            'Underweight': 'mechanical failure',
            'Rear wing': 'mechanical failure',
            'Safety concerns': 'mechanical failure',
            'Not restarted': 'mechanical failure',
            'Crankshaft': 'engine failure',
            'Fuel rig': 'mechanical failure',
            'Wheel rim': 'mechanical failure',
            'Power loss': 'engine failure',
            'Safety': 'mechanical failure',
            'Electronics': 'engine failure',
            'Drivetrain': 'mechanical failure',
            'Launch control': 'mechanical failure',
            'Pneumatics': 'mechanical failure',
            'Engine fire': 'engine failure',
            'Tyre puncture': 'mechanical failure',
            'Wheel nut': 'mechanical failure',
            'Technical': 'mechanical failure',
            'Track rod': 'mechanical failure',
            'Front wing': 'mechanical failure',
            'Water pressure': 'mechanical failure',
            'Refuelling': 'mechanical failure',
            'Driver Seat': 'mechanical failure',
            'Engine misfire': 'engine failure',
            'Collision damage': 'driver mistake',
            'ERS': 'engine failure',
            'Power Unit': 'engine failure',
            'Brake duct': 'mechanical failure',
            'Undertray': 'driver mistake',
            'Cooling system': 'mechanical failure',
            'Illness': 'driver mistake',
            'Debris': 'driver mistake',
            'Damage': 'mechanical failure',
            'Seat': 'mechanical failure'
        }

        def classify_status_finish(key):
            return diccionario_clasificacion[key]

        data['race_finish'] = data['race_status'].apply(classify_status_finish)

        """
        Modificamos algunos nombres de equipos porque han cambiado de nombre
        por patrocionios pero realmente son el mismo
        """
        constructors_history = {
            'bmw_sauber' : 'alfa',
            'sauber' : 'alfa',
            'stewart' : 'red_bull',
            'Jaguar' : 'red_bull',
            'jordan' : 'aston_martin',
            'force_india' : 'aston_martin',
            'benetton' : 'renault',
            'toleman' : 'renault',
            'lotus_f1' : 'renault',
            'alpine' : 'renault',
            'minardi' : 'alphatauri',
            'toro_rosso' : 'alphatauri',
            'fondmetal' : 'ags',
            'honda' : 'mercedes',
            'brawn' : 'mercedes',
            'tyrrell' : 'mercedes',
            'bar' : 'mercedes',
            'team_lotus' : 'caterham',
            'footwork' : 'arrows',
            'marussia' : 'manor',
            'virgin' : 'manor',
            'lotus-brm' : 'lotus-borgward',
            'lotus-climax' : 'lotus-borgward',
            'lotus-ford' : 'lotus-borgward',
            'lotus-maserati' : 'lotus-borgward',
            'lotus-pw' : 'lotus-borgward',
            'brabham-alfa_romeo' : 'brabham',
            'brabham-brm' : 'brabham',
            'brabham-climax' : 'brabham',
            'brabham-ford' : 'brabham',
            'brabham-repco' : 'brabham',
            'brm-ford' : 'brm',
            'de_tomaso-alfa_romeo' : 'tomaso',
            'de_tomaso-ferrari' : 'tomaso',
            'de_tomaso-osca' : 'tomaso',
            'cooper-alfa_romeo' : 'cooper',
            'cooper-ats' : 'cooper',
            'cooper-borgward' : 'cooper',
            'cooper-brm' : 'cooper',
            'cooper-castellotti' : 'cooper',
            'cooper-climax' : 'cooper',
            'cooper-ferrari' : 'cooper',
            'cooper-ford' : 'cooper',
            'cooper-maserati' : 'cooper',
            'cooper-osca' : 'cooper',
            'march-alfa_romeo' : 'march',
            'march-ford' : 'march'
        }

        data['constructor_id'] = data['constructor_id'].map(constructors_history).fillna(data['constructor_id'])
        # print('prep 2')

        """
        Modificamos las nacionalidades para tener únicamente países para
        que el país del circuito y la nacionalidad del piloto o equipo coincidan
        """
        # print(data['driver_nationality'])
        nationality_to_country = {
            'Italian': 'Italy',
            'British': 'UK',
            'French': 'France',
            'Belgian': 'Belgium',
            'Argentine': 'Argentina',
            'Irish': 'Ireland',
            'Thai': 'Thailand',
            'Swiss': 'Switzerland',
            'Monegasque': 'Monaco',
            'American': 'USA',
            'Spanish': 'Spain',
            'Australian': 'Australia',
            'Brazilian': 'Brazil',
            'Uruguayan': 'Uruguay',
            'German': 'Germany',
            'Swedish': 'Sweden',
            'Dutch': 'Netherlands',
            'New Zealander': 'New Zealand',
            'South African': 'South Africa',
            'Mexican': 'Mexico',
            'Austrian': 'Austria',
            'Liechtensteiner': 'Liechtenstein',
            'Japanese': 'Japan',
            'Finnish': 'Finland',
            'Canadian': 'Canada',
            'Chilean': 'Chile',
            'Colombian': 'Colombia',
            'Venezuelan': 'Venezuela',
            'Portuguese': 'Portugal',
            'Danish': 'Denmark',
            'Hungarian': 'Hungary',
            'Indian': 'India',
            'Polish': 'Poland',
            'Russian': 'Russia',
            'Indonesian': 'Indonesia',
            'Malaysian': 'Malaysia',
            'American-Italian': 'USA',
            'Rhodesian': 'Zimbabwe',
            'Czech': 'Czech Republic',
            'East German': 'Germany',
            'Argentine-Italian': 'Argentina'
        }

        data['driver_nationality_country'] = data['driver_nationality'].map(nationality_to_country).fillna(data['driver_nationality'])
        data['constructor_nationality_country'] = data['constructor_nationality'].map(nationality_to_country).fillna(data['constructor_nationality'])

        """
        Añadimos la edad del piloto durante la carrera
        """
        # Convertimos las columnas de fecha al formato datetime
        data['driver_date_of_birth'] = pd.to_datetime(data['driver_date_of_birth'])
        data['race_date'] = pd.to_datetime(data['race_date'])

        # Calculamos la edad en base a la fecha de nacimiento y la fecha de la carrera
        data['driver_age'] = (data['race_date'] - data['driver_date_of_birth']).dt.days // 365
        
        # print('prep 3')
        
        data.to_csv('prueba.csv', index=False)
        """
        Añadimos los datos del piloto ganador de la carrera y del poleman
        """
        # data['race_winner'] = data['race_final_position'].apply(lambda x: 1 if x == 1 else 0)
        data['qualy_pole'] = data['race_grid_position'].apply(lambda x: 1 if x == 1 else 0)

        
        # Obtener los valores únicos de las columnas 'A' y 'B'
        columnas_seleccionadas_ccr = ['constructor_id', 'constructor_car_relaiblity']
        columnas_seleccionadas_da = ['driver_id', 'driver_awareness']
        valores_unicos_ccr = self.all_data.drop_duplicates(subset=columnas_seleccionadas_ccr)
        valores_unicos_da = self.all_data.drop_duplicates(subset=columnas_seleccionadas_da)

        dict_ccr = dict(valores_unicos_ccr[columnas_seleccionadas_ccr].values)
        dict_da = dict(valores_unicos_da[columnas_seleccionadas_da].values)

        data['constructor_car_relaiblity'] = data['constructor_id'].map(dict_ccr)
        data['driver_awareness'] = data['driver_id'].map(dict_da)


        return data
    

