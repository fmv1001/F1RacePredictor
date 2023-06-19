import pandas as pd

# Leemmos los archivos CSV y creamos los DataFrames
data = pd.read_csv('data/merged_data.csv')

# Creamos un diccionario con la consistencia del piloto
driver_awareness_dict = (1 - (data['race_finish'] == 'driver mistake').groupby(data['driver_id']).mean()).to_dict()
# También creamos un diccionario con la fiabilidad de los equipos
constructor_relaiblity_dict = (1 - ((data['race_finish'] == 'mechanical failure') | (data['race_finish'] == 'engine failure')).groupby(data['constructor_id']).mean()).to_dict()

# Aplicamos los diccionarios a los datos
data['driver_awareness'] = data['driver_id'].apply(lambda x:driver_awareness_dict[x])
data['constructor_car_relaiblity'] = data['constructor_id'].apply(lambda x:constructor_relaiblity_dict[x])

# Alamcenaje de los datos
data.to_csv('data/merged_data.csv', index=False)