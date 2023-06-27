import pandas as pd
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
"""
Preparación de los datos para los algoritmos
"""
# Leemmos los archivos CSV y creamos los DataFrames
df_codification = pd.read_csv('data/data_manual_selection.csv') 

# Creamos los codificadores
le = LabelEncoder()
oh = OneHotEncoder()

# Codificación ordinal 
df_codification['driver_id'] = le.fit_transform(df_codification['driver_id'])
df_codification['circuit_id'] = le.fit_transform(df_codification['circuit_id'])
df_codification['constructor_id'] = le.fit_transform(df_codification['constructor_id'])
df_codification['race_finish'] = le.fit_transform(df_codification['race_finish'])

# Codificación One-Hot 
def cod_oh(df, columna):
    encoded_column = oh.fit_transform(df[[columna]])
    df_encoded = pd.DataFrame(encoded_column.toarray(), columns=columna+ "_" + oh.categories_[0])
    df_final = pd.concat([df, df_encoded], axis=1)
    return df_final

df_codification = cod_oh(df_codification,'race_weather')
df_codification = cod_oh(df_codification,'driver_nationality_country')
df_codification = cod_oh(df_codification,'constructor_nationality_country')
df_codification = cod_oh(df_codification,'circuit_country')

# Eliminación de las columnas que ya no son necesarias por existir ya codificadas
columnas_eliminar = ['race_weather', 'driver_nationality_country', 'constructor_nationality_country', 'circuit_country'] 
df_codification = df_codification.drop(columnas_eliminar, axis=1)

# Save data
df_codification.to_csv('data/coded_manual_data.csv', index=False)