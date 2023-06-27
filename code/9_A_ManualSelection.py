import pandas as pd

# Leemmos los archivos CSV y creamos los DataFrames
df_manual_selecction = pd.read_csv('data/all_data.csv') 

# Hacemos la selección manual de características
df_manual_selecction = df_manual_selecction.drop('race_round', axis=1)
df_manual_selecction = df_manual_selecction.drop('race_date', axis=1)
df_manual_selecction = df_manual_selecction.drop('driver_date_of_birth', axis=1)
df_manual_selecction = df_manual_selecction.drop('circuit_lat', axis=1)
df_manual_selecction = df_manual_selecction.drop('circuit_lon', axis=1)
df_manual_selecction = df_manual_selecction.drop('race_points_won', axis=1)
df_manual_selecction = df_manual_selecction.drop('race_laps_finished', axis=1)
df_manual_selecction = df_manual_selecction.drop('race_status', axis=1)

# Alamcenaje de los datos
df_manual_selecction.to_csv('data/data_manual_selection.csv', index=False)