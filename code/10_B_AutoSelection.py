import pandas as pd
import time
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.feature_selection import RFE
# from sklearn.datasets import make_regression
def encontrar_peso_minimo(row):
    # pesos = row
    # del pesos['feature']
    peso_final = (row['ranking_LinearRegression']*0.5) + (row['ranking_DecisionTreeRegressor']*0.5) #+ (row['ranking_DecisionTreeClassifier']*0.33)
    return peso_final

# Leemmos el archivo CSV y creamos el DataFrame
data = pd.read_csv("data/coded_auto_selection_data.csv")

# Diccionario de modelos
model_estimator_dict = {
    'LinearRegression': [LinearRegression(), pd.DataFrame()],
    'DecisionTreeRegressor': [DecisionTreeRegressor(), pd.DataFrame()]
}

# Asignamos el número de características qeu queremos
n_features = 109

variables_objetivo = ['race_final_position','race_winner','qualy_pole']
for variable_obj in variables_objetivo:
    for estimator_name in model_estimator_dict:
        # Inicializamos los modelos
        model_estimator_dict[estimator_name] = [model_estimator_dict[estimator_name][0],pd.DataFrame()]

        # Separamos los datos en características (X) y variable objetivo (y)
        X = data.drop(variable_obj, axis=1)
        y = data[variable_obj]

        # Creamos el estimador del modelo
        estimator = model_estimator_dict[estimator_name][0]

        # Inicializamos el algoritmo RFE (Recursive Feature Elimination) 
        #   y especificamos el número de características a seleccionar
        rfe = RFE(estimator, n_features_to_select=n_features)

        # Realizar la selección de características
        inicio = time.time()
        print(f"Iniciando Backward Elimination {estimator_name}, target:{variable_obj}...")
        X_selected = rfe.fit_transform(X, y)
        print("Backward Elimination completada.")
        fin = time.time()
        tiempo_ejecucion = fin - inicio 
        print("Tiempo de ejecución:", tiempo_ejecucion, "segundos")

        # Obtenemos el ranking de las características y creamos el DataFrame
        feature_ranking = rfe.ranking_
        rankings_df = pd.DataFrame({'feature': X.columns, f'ranking_{estimator_name}': feature_ranking})

        # Ordenamos el DataFrame según el ranking
        rankings_df = rankings_df.sort_values(by=f'ranking_{estimator_name}')

        # Guardamos el ranking para posteriormente combinarlo
        model_estimator_dict[estimator_name] = [model_estimator_dict[estimator_name][0],pd.DataFrame(rankings_df)]

    df_combinado = pd.DataFrame()
    # Combinamos los rankings por partes iguales
    for i in model_estimator_dict:
        if(df_combinado.empty):
            df_combinado = model_estimator_dict[i][1]
        else:
            df_combinado = df_combinado.merge(model_estimator_dict[i][1], on='feature')

    # Aplicamos la combinación
    df_combinado['final_ranking'] = df_combinado.apply(encontrar_peso_minimo, axis=1)

    # Eliminamos las caracteristicas que contienen los datos del equipo piloto o circuito
    df_filtered = df_combinado[~df_combinado['feature'].str.contains('_id')]

    # Ordenamos el ranking 
    df_sorted = df_filtered.sort_values('final_ranking')

    # Cargamos todos los datos codificados
    df_final = pd.read_csv('data/coded_auto_selection_data.csv')
    
    # Eliminamos las características descartadas
    columnas_a_eliminar = df_sorted['feature'].values[n_features-df_final.shape[1]:]
    print(columnas_a_eliminar)
    df_data = df_final.drop(columnas_a_eliminar, axis=1)

    # Save data
    df_data.to_csv(f'data/coded_auto_selection_data_{variable_obj}.csv', index=False)
