import requests
import pandas as pd
import time

def get_f1_qualifying_results_from_Ergast(start_year, end_year):
    """
    Obtiene los datos de todas las clasificaciones de la Fórmula 1 que hay en la base de datos de Ergast
        de todos los años entre las dos fechas indicadas.
    Retorna un dataframe con la lista de todos las clasificaciones.
    """
    results = []
    for year in range(start_year, end_year+1):
        page = 1
        limit = 1000
        while True:
            url = f'http://ergast.com/api/f1/{year}/qualifying.json?page={page}&limit={limit}'
            response = requests.get(url)
            response_json = response.json()
            qualys = response_json['MRData']['RaceTable']['Races']
            
            for qualy in qualys:
                for qualy_result in qualy["QualifyingResults"]:
                    new_result = {}
                    new_result["year"] = year
                    new_result["qualy_round"] = qualy["round"]
                    new_result["qualy_url"] = qualy["url"]
                    new_result["qualy_date"] = qualy["date"]
                    new_result["circuit_id"] = qualy["Circuit"]["circuitId"]
                    new_result["driver_id"] = qualy_result["Driver"]["driverId"]
                    new_result["constructor_id"] = qualy_result["Constructor"]["constructorId"]
                    new_result["qualy_pos"] = int(qualy_result["position"])
                    new_result["qualy_q1_time"] = qualy_result.get("Q1", None)
                    new_result["qualy_q2_time"] = qualy_result.get("Q2", None)
                    new_result["qualy_q3_time"] = qualy_result.get("Q3", None)
                    results.append(new_result)
            if page < limit:
                break
            page += 1
    return pd.DataFrame(results)

inicio = time.time()  # Tiempo de inicio

# Obtención de datos
df = get_f1_qualifying_results_from_Ergast(1950,2018)

# Alamcenaje de los datos
df.to_csv('data/qualifying_ergast.csv', index=False)

fin = time.time()  # Tiempo de fin

tiempo_ejecucion = fin - inicio  # Diferencia de tiempo
print("Tiempo de ejecución:", tiempo_ejecucion, "segundos")

# Mostramos el resultado
print (df)