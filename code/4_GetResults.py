import requests
import pandas as pd
import time

def get_f1_race_results(start_year, end_year):
    """
    Obtiene los datos de todas las carreras de la Fórmula 1 que hay en la base de datos de Ergast
        de todos los años entre las dos fechas indicadas.
    Retorna un dataframe con la lista de todos las carreras.
    """
    total_results = []
    for year in range(start_year, end_year+1):
        page = 1
        limit = 1000
        while True:
            url = f'http://ergast.com/api/f1/{year}/results.json?page={page}&limit={limit}'
            response = requests.get(url)
            response_json = response.json()
            data_races = response_json['MRData']['RaceTable']['Races']
            
            for race_data in data_races:
                for race_result in race_data['Results']:
                    driver_race_result = {}
                    driver_race_result['year'] = year
                    driver_race_result['race_date'] = race_data['date']
                    driver_race_result['race_round'] = race_data['round']
                    driver_race_result['race_url'] = race_data['url']
                    driver_race_result['circuit_id'] = race_data['Circuit']['circuitId']
                    driver_race_result['driver_id'] = race_result['Driver']['driverId']
                    driver_race_result['constructor_id'] = race_result['Constructor']['constructorId']
                    driver_race_result['race_grid_position'] = int(race_result['grid'])
                    driver_race_result['race_final_position'] = int(race_result['position'])
                    driver_race_result['race_laps_finished'] = int(race_result['laps'])
                    driver_race_result['race_status'] = race_result['status']
                    if 'Time' in race_result:
                        driver_race_result['race_time_millis'] = race_result['Time']['millis']
                    else:
                        driver_race_result['race_time_millis'] = None
                    if 'FastestLap' in race_result:
                        driver_race_result['race_fastest_lap'] = race_result['FastestLap']['Time']['time']
                        driver_race_result['race_average_speed'] = race_result['FastestLap']['AverageSpeed']['speed']
                    else:
                        driver_race_result['race_fastest_lap'] = None
                        driver_race_result['race_average_speed'] = None
                    driver_race_result['race_points_won'] = get_points(driver_race_result['race_final_position'])
                    total_results.append(driver_race_result)
            if page < limit:
                break
            page += 1
    return pd.DataFrame(total_results)

# Puntos por posición
puntos = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}

def get_points(posicion):
    """
    Obtiene los puntos que gana un piloto en función de la posición final en carrera.
    """
    if posicion in puntos:
        return puntos[posicion]  # Se devuelven los puntos correspondientes a la posición
    else:
        return 0  # No ha ganado puntos

inicio = time.time()  # Tiempo de inicio

# Obtención de datos
df = get_f1_race_results(1950,2022)

# Alamcenaje de los datos
df.to_csv('data/results.csv', index=False)

fin = time.time()  # Tiempo de fin

tiempo_ejecucion = fin - inicio  # Diferencia de tiempo
print("Tiempo de ejecución:", tiempo_ejecucion, "segundos")

# Mostramos el resultado
print (df)