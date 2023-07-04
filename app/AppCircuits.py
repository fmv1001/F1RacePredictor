import requests
import pandas as pd
import time

class Circuits:
    def __init__(self, api_key):
        self.google_api_elevation_errors = 0
        self.api_key =  api_key # Your API_KEY
        return

    
    def get_circuits_from_Ergast(self, season):
        """
        Obtiene los datos de todos los circuitos de la Fórmula 1.
        Retorna un dataframe con la lista de todos los circuitos.
        """
        url = f'http://ergast.com/api/f1/{season}/circuits.json?limit=1000'
        response = requests.get(url)
        data = response.json()
        circuits_data = data['MRData']['CircuitTable']['Circuits']
        return self.create_dataframe(circuits_data)

    def create_dataframe(self, circuits):
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
            'circuit_alt': [self.google_api_get_elevation(c['Location']['lat'],c['Location']['long']) for c in circuits]
        }
        return pd.DataFrame(df_data)

    def google_api_get_elevation(self, latitud, longitud):
        """
        Obtiene los datos de altitud de un circuito a apartir de su latitud y longitud
            de la API Google Elevation. Necesario poseer el Api Key de acceso a la API.
        """
        
        url = f"https://maps.googleapis.com/maps/api/elevation/json?locations={latitud}%2C{longitud}&key={self.api_key}"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        elevation_data = response.json()
        
        if elevation_data["status"] == "OK":
            altitud = elevation_data["results"][0]["elevation"]
            return altitud
        else:
            self.google_api_elevation_errors += 1
            return None