import requests
import pandas as pd

class Drivers:
    def __init__(self):
        return

    def get_season_drivers_from_Ergast(self, season):
        """
        Obtiene los datos de todos los pilotos de la Fórmula 1.
        Retorna un dataframe con la lista de todos los pilotos.
        """
        drivers = []
        page = 1
        limit = 1000
        while True:
            url = f'http://ergast.com/api/f1/{season}/drivers.json?page={page}&limit={limit}'
            response = requests.get(url)
            response_json = response.json()
            drivers_data = response_json['MRData']['DriverTable']['Drivers']
            drivers += drivers_data
            if len(drivers_data) < limit:
                break
            page += 1
        return self.create_dataframe(drivers)


    def create_dataframe(sef, drivers):
        """
        Crea un DataFrame a partir de los datos de los circuitos.
        Además, renombra las columnas para su posterior tratamiento.
        Retorna el DataFrame resultante.
        """
        df_drivers = pd.DataFrame(drivers)
        df_drivers = df_drivers.rename(columns={'driverId': 'driver_id'})
        df_drivers = df_drivers.rename(columns={'code': 'driver_code'})
        df_drivers = df_drivers.rename(columns={'givenName': 'driver_first_name'})
        df_drivers = df_drivers.rename(columns={'familyName': 'driver_last_name'})
        df_drivers = df_drivers.rename(columns={'dateOfBirth': 'driver_date_of_birth'})
        df_drivers = df_drivers.rename(columns={'nationality': 'driver_nationality'})
        df_drivers = df_drivers.rename(columns={'url': 'driver_url'})
        df_drivers = df_drivers.rename(columns={'permanentNumber': 'driver_permanent_number'})
        return df_drivers