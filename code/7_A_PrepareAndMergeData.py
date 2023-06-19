import pandas as pd

# Leemmos los archivos CSV y creamos los DataFrames
df_results = pd.read_csv('data/final_results.csv')
df_driver = pd.read_csv('data/drivers.csv')
df_circuits = pd.read_csv('data/circuits.csv')
df_constructors = pd.read_csv('data/constructors.csv')

"""
Añadimos estado final de carrera más simple en función
de el estado fional de carrera
"""
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

df_results['race_finish'] = df_results['race_status'].apply(classify_status_finish)


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

df_results['constructor_id'] = df_results['constructor_id'].map(constructors_history).fillna(df_results['constructor_id'])

"""
Modificamos las nacionalidades para tener únicamente países para
que el país del circuito y la nacionalidad del piloto o equipo coincidan
"""

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

df_driver['driver_nationality_country'] = df_driver['driver_nationality'].map(nationality_to_country).fillna(df_driver['driver_nationality'])
df_constructors['constructor_nationality_country'] = df_constructors['constructor_nationality'].map(nationality_to_country).fillna(df_constructors['constructor_nationality'])

# Combinamos los DataFrames utilizando el id de cada uno como clave de combinación
df_merged = df_results.merge(df_driver, on='driver_id', how='left')
df_merged = df_merged.merge(df_circuits, on='circuit_id', how='left')
df_merged = df_merged.merge(df_constructors, on='constructor_id', how='left')


"""
Añadimos la edad del piloto durante la carrera
"""
# Convertimos las columnas de fecha al formato datetime
df_merged['driver_date_of_birth'] = pd.to_datetime(df_merged['driver_date_of_birth'])
df_merged['race_date'] = pd.to_datetime(df_merged['race_date'])

# Calculamos la edad en base a la fecha de nacimiento y la fecha de la carrera
df_merged['driver_age'] = (df_merged['race_date'] - df_merged['driver_date_of_birth']).dt.days // 365


"""
Rellenamos los datos del clima de carrera con clima seco
ya que es lo más probable que salga
"""
print(df_merged['race_weather'].value_counts())
df_merged['race_weather'] = df_merged['race_weather'] .fillna("dry")

"""
Añadimos los datos del piloto ganador de la carrera y del poleman
"""
df_merged['race_winner'] = df_merged['race_final_position'].apply(lambda x: 1 if x == 1 else 0)
df_merged['qualy_pole'] = df_merged['race_grid_position'].apply(lambda x: 1 if x == 1 else 0)

# Alamcenaje de los datos
df_merged.to_csv('data/merged_data.csv', index=False)


