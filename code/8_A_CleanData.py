import pandas as pd

# Lee el archivo CSV y crea un DataFrame
df_merge_results = pd.read_csv('data/merged_data.csv')

# Comprobar valores nulos o vacíos en cada columna
valores_nulos = df_merge_results.isnull().sum()

print("Valores nulos:")
print(valores_nulos)

df_merge_results = df_merge_results.drop('race_time_millis', axis=1)
df_merge_results = df_merge_results.drop('race_fastest_lap', axis=1)
df_merge_results = df_merge_results.drop('race_average_speed', axis=1)
df_merge_results = df_merge_results.drop('driver_permanent_number', axis=1)
df_merge_results = df_merge_results.drop('driver_code', axis=1)

#  Eliminamos las columnas que no aportan ninguna información
df_merge_results = df_merge_results.drop('race_url', axis=1)
df_merge_results = df_merge_results.drop('driver_url', axis=1)
df_merge_results = df_merge_results.drop('circuit_url', axis=1)
df_merge_results = df_merge_results.drop('driver_first_name', axis=1)
df_merge_results = df_merge_results.drop('driver_last_name', axis=1)
df_merge_results = df_merge_results.drop('constructor_name', axis=1)
df_merge_results = df_merge_results.drop('constructor_url', axis=1)
df_merge_results = df_merge_results.drop('circuit_locality', axis=1)
df_merge_results = df_merge_results.drop('circuit_name', axis=1)
df_merge_results = df_merge_results.drop('driver_nationality', axis=1)
df_merge_results = df_merge_results.drop('constructor_nationality', axis=1)


valores_nulos = df_merge_results.isnull().sum()

print("Valores nulos:")
print(valores_nulos)

df_merge_results.to_csv('data/all_data.csv', index=False)

