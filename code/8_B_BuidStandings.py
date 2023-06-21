import pandas as pd

# Leemos el archivo CSV y creamos un DataFrame
df_results = pd.read_csv('data/all_data.csv')

df_standings = df_results.groupby(['year', 'driver_id']).agg({'race_points_won': 'sum'}).reset_index()
print(df_standings) # .sort_values(ascending=False)
df_standings.to_csv('data/driver_standings.csv', index=False)

df_standings = df_results.groupby(['year', 'constructor_id']).agg({'race_points_won': 'sum'}).reset_index()
print(df_standings) # .sort_values(ascending=False)
df_standings.to_csv('data/constructor_standings.csv', index=False)


