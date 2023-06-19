import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import time

fallos = 0
def get_f1_race_weather_results_from_Wikipedia():
    """
    Obtiene los datos de climatología de todas las carreras proporcionadas
        buscando la información el la web de la Wikipedia.
    Retorna el dataframe con la columna de los datos climatológicos añadida.
    """
    df_results = pd.read_csv('data/results.csv')

    urls_unicas = df_results['race_url'].unique()

    # Aplicamos la función que obtiene el clima a las url y creamos un diccionario con los resultados
    resultados = {elemento: get_race_weather(elemento) for elemento in urls_unicas}

    # Mapeamos los resultados en una nueva columna
    df_results['race_weather'] = df_results['race_url'].map(resultados)
    return df_results

palabras_clima = {
    "dry": "dry",
    "sunny": "dry",
    "clear": "dry",
    "cloudy": "dry",
    "overcast": "dry",
    "rainy": "wet",
    "showers": "wet",
    "drizzle": "wet",
    "stormy": "wet",
    "thunderstorms": "wet",
    "snowy": "wet",
    "blizzard": "dry",
    "foggy": "wet",
    "misty": "wet",
    "hazy": "dry",
    "windy": "dry",
    "breezy": "dry",
    "calm": "dry",
    "hot": "dry",
    "cold": "dry",
    "rain": "wet",
    "cool": "dry",
    "hail": "wet"
}

lluvia_dict = {
    "dry": False,
    "wet": True
}

def get_race_weather(url):
    """
    Obtiene los datos da la url proporcionada y extrae la información mediante webscrapping
        en base a determinadas palabras que indican el clima.
    Retorna "wet" si llovió durante el gran premio o "dry" si no.
    """
    # Obtenemos toda la informaciónde la url
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Obtenemos el elemento donde se encuentra el dato del clima
    tabla = soup.find('table', class_='infobox vevent')
    fila_weather = None

    if tabla:
        # Dentro de la tabla buscamos la sección del clima
        fila_weather = tabla.select_one('tr:has(th:-soup-contains("Weather"))')

        if fila_weather:
            # Eliminamos datos innecesarios
            sup_elements = fila_weather.find_all('sup')
            for sup_element in sup_elements:
                sup_element.decompose()

            # Separamos en lineas la información
            lineas = fila_weather.text.splitlines()

            if len(lineas) > 1:
                # Accedemos a la segunda línea, donde está lo que realmente importa, el clima
                segunda_fila = lineas[1]
                # Eliminamos cartacteres cómo símbolos u otros
                texto_limpio = re.sub(r"[^a-zA-Z\s]", "", segunda_fila)
                # Recibimos si ha llovido o no
                lluvia = comprobar_lluvia(texto_limpio)
                return lluvia
            else:
                print("No hay suficientes líneas en el texto.")
                fallos += 1
            return None


def comprobar_lluvia(texto):
    """
    Comprueba del texto enviado si alguna palabra indica lluvia
    Retorna "wet" hay alguna plabara que lo indique o "dry" si no.
    """
    palabras = texto.split()
    lluvia = False
    for palabra in palabras:
        palabra = palabra.lower()
        if palabra in palabras_clima:
            lluvia = lluvia_dict[palabras_clima[palabra]]
        if lluvia:
            break
    if lluvia:
        return "wet"
    else:
        return "dry"

inicio = time.time()  # Guardar el tiempo de inicio

df = get_f1_race_weather_results_from_Wikipedia()

df.to_csv('data/final_results.csv', index=False)

fin = time.time()  # Guardar el tiempo de fin

tiempo_ejecucion = fin - inicio  # Calcular la diferencia de tiempo

print("Tiempo de ejecución:", tiempo_ejecucion, "segundos")
print("Se ha encontrado el clima de " + str((df['race_url'].unique().__len__() - fallos)) + " del total de " + str(df['race_url'].unique().__len__()) + " carreras.")

print (df)