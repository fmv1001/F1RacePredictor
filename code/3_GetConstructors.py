import requests
import pandas as pd

def get_all_constructors_from_Ergast():
    """
    Obtiene los datos de todos los constructores o equipos de la Fórmula 1.
    Retorna un dataframe con la lista de todos los equipos.
    """
    total_constructors = []
    page = 1
    limit = 1000
    while True:
        url = f'http://ergast.com/api/f1/constructors.json?page={page}&limit={limit}'
        response = requests.get(url)
        response_json = response.json()
        constructors_data = response_json['MRData']['ConstructorTable']['Constructors']
        total_constructors += constructors_data
        if len(constructors_data) < limit:
            break
        page += 1
    return create_dataframe(total_constructors)


def create_dataframe(constructors):
    """
    Crea un DataFrame a partir de los datos de los pilotos.
    Además, renombra las columnas para su posterior tratamiento.
    Retorna el DataFrame resultante.
    """
    df_constructors = pd.DataFrame(constructors)
    df_constructors = df_constructors.rename(columns={'constructorId': 'constructor_id'})
    df_constructors = df_constructors.rename(columns={'url': 'constructor_url'})
    df_constructors = df_constructors.rename(columns={'name': 'constructor_name'})
    df_constructors = df_constructors.rename(columns={'nationality': 'constructor_nationality'})
    return df_constructors

# Obtención de datos
df = get_all_constructors_from_Ergast()

# Alamcenaje de los datos
df.to_csv('data/constructors.csv', index=False)

# Mostramos el resultado
print (df)