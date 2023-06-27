import pandas as pd
from sklearn.preprocessing import StandardScaler,LabelEncoder,OneHotEncoder
import joblib
"""
Preparación de los datos para los algoritmos
"""
# Leemmos los archivos CSV y creamos los DataFrames
df_codification = pd.read_csv('data/all_data.csv')

"""
 Date columns to be coded
"""
# Convertimos primero a fecha
df_codification['race_date'] = pd.to_datetime(df_codification['race_date'])
df_codification['driver_date_of_birth'] = pd.to_datetime(df_codification['driver_date_of_birth'])

# Utilizaremos el día de nacimiento más antigua como fecha de referencia para la conversión
reference_race_date = df_codification['race_date'].min()
reference_driver_date_of_birth = df_codification['driver_date_of_birth'].min()

# Creamos las nuevas columnas
df_codification['race_date_numeric'] = (df_codification['race_date'] - reference_race_date).dt.total_seconds()
df_codification['driver_date_of_birth_numeric'] = (df_codification['driver_date_of_birth'] - reference_driver_date_of_birth).dt.total_seconds()

# Eliminamos las viejas
df_codification = df_codification.drop('race_date', axis=1)
df_codification = df_codification.drop('driver_date_of_birth', axis=1)

dict_coders = {}

"""
 Preprocessing coders
"""
le = LabelEncoder()
le_driver_id = LabelEncoder()
le_circuit_id = LabelEncoder()
le_constructor_id = LabelEncoder()

# Codificación ordinal
df_codification['driver_id'] = le_driver_id.fit_transform(df_codification['driver_id'])
dict_coders['driver_id'] = le_driver_id

df_codification['circuit_id'] = le_circuit_id.fit_transform(df_codification['circuit_id'])
dict_coders['circuit_id'] = le_circuit_id

df_codification['constructor_id'] = le_constructor_id.fit_transform(df_codification['constructor_id'])
dict_coders['constructor_id'] = le_constructor_id

df_codification['race_finish'] = le.fit_transform(df_codification['race_finish'])
df_codification['race_status'] = le.fit_transform(df_codification['race_status'])

# Codificación One-Hot 
def cod_oh(df, columna):
    oh = OneHotEncoder()
    encoded_column = oh.fit_transform(df[[columna]])
    dict_coders[columna] = oh
    df_encoded = pd.DataFrame(encoded_column.toarray(), columns=columna+ "_" + oh.categories_[0])
    df_final = pd.concat([df, df_encoded], axis=1)
    return df_final

df_codification = cod_oh(df_codification,'race_weather')
df_codification = cod_oh(df_codification,'driver_nationality_country')
df_codification = cod_oh(df_codification,'constructor_nationality_country')
df_codification = cod_oh(df_codification,'circuit_country')

# Eliminación de las columnas que ya no son necesarias por existir ya codificadas
columnas_eliminar = ['race_weather','driver_nationality_country', 'constructor_nationality_country', 'circuit_country']
df_codification = df_codification.drop(columnas_eliminar, axis=1)

# Guardamos el diccionario de los codificadores utilizados
joblib.dump(dict_coders, 'coders/codificadores.pkl')

# Save Data
df_codification.to_csv('data/coded_auto_selection_data.csv', index=False)