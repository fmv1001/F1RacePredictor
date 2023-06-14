import requests
import pandas as pd
import time

fallos = 0
def get_circuits_from_Ergast():
    """
    Obtiene los datos de todos los circuitos de la Fórmula 1.
    Retorna un dataframe con la lista de todos los circuitos.
    """
    url = "http://ergast.com/api/f1/circuits.json?limit=1000"
    response = requests.get(url)
    data = response.json()
    circuits_data = data['MRData']['CircuitTable']['Circuits']
    return create_dataframe(circuits_data)

def create_dataframe(circuits):
    """
    Crea un DataFrame a partir de los datos de los circuitos.
    Además, renombra las columnas para su posterior tratamiento
        y obtiene la altitud en metros sobre el nivel del mar donde se encuentra.
    Retorna el DataFrame resultante.
    """
    df_data = {
        'circuit_id': [c['circuitId'] for c in circuits],
        'circuit_url': [c['url'] for c in circuits],
        'circuit_name': [c['circuitName'] for c in circuits],
        'circuit_country': [c['Location']['country'] for c in circuits],
        'circuit_locality': [c['Location']['locality'] for c in circuits],
        'circuit_lat': [c['Location']['lat'] for c in circuits],
        'circuit_lon': [c['Location']['long'] for c in circuits],
        'circuit_alt': [google_api_get_elevation(c['Location']['lat'],c['Location']['long']) for c in circuits]
    }
    return pd.DataFrame(df_data)

def google_api_get_elevation(latitud, longitud):
    """
    Obtiene los datos de altitud de un circuito a apartir de su latitud y longitud
        de la API Google Elevation. Necesario poseer el Api Key de acceso a la API.
    """
    api_key = "" # Your API_KEY
    url = f"https://maps.googleapis.com/maps/api/elevation/json?locations={latitud}%2C{longitud}&key={api_key}"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    elevation_data = response.json()
    
    if elevation_data["status"] == "OK":
        altitud = elevation_data["results"][0]["elevation"]
        return altitud
    else:
        fallos += 1
        return None

inicio = time.time()  # Tiempo de inicio

# Obtención de datos
df = get_circuits_from_Ergast()

# Alamcenaje de los datos
df.to_csv('data/circuits.csv', index=False)

fin = time.time()  # Tiempo de fin

tiempo_ejecucion = fin - inicio  # Diferencia de tiempo
print("Tiempo de ejecución:", tiempo_ejecucion, "segundos")
print("Se han encontrado las altitudes de " + str((df.__len__() - fallos)) + " del total de " + str(df.__len__()) + " circuitos.")

# Mostramos el resultado
print (df)