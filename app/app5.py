import tkinter as tk
from tkinter import ttk
import joblib

# Función para cargar el modelo de predicción
def load_model():
    # Ruta al archivo que contiene el modelo entrenado
    model_path = 'trained_model.pkl'

    # Cargar el modelo desde el archivo
    model = joblib.load(model_path)

    # Retornar el modelo cargado
    return model

# Función para realizar una predicción utilizando el modelo cargado
def predict(model, inputs):
    # Realizar la predicción utilizando el modelo y los inputs
    prediction = model.predict(inputs)

    # Retornar el resultado de la predicción
    return prediction

# Función para manejar el evento del botón de predicción
def predict_button_click():
    # Obtener los valores de entrada del usuario
    input1 = input1_entry.get()
    input2 = input2_entry.get()

    # Convertir los valores de entrada a un formato adecuado para la predicción
    inputs = [[float(input1), float(input2)]]

    # Realizar la predicción utilizando el modelo cargado
    prediction = predict(model, inputs)

    # Mostrar el resultado de la predicción en el cuadro de texto de salida
    output_text.delete('1.0', tk.END)
    output_text.insert(tk.END, f"La predicción es: {prediction}")

# Crear la ventana principal
root = tk.Tk()

# Cargar el modelo de predicción
model = load_model()

# Crear los elementos de la interfaz de usuario
input1_label = ttk.Label(root, text="Valor 1:")
input1_entry = ttk.Entry(root)
input2_label = ttk.Label(root, text="Valor 2:")
input2_entry = ttk.Entry(root)
predict_button = ttk.Button(root, text="Predecir", command=predict_button_click)
output_text = tk.Text(root, height=5, width=40)

# Posicionar los elementos en la ventana
input1_label.grid(row=0, column=0, padx=10, pady=10)
input1_entry.grid(row=0, column=1, padx=10, pady=10)
input2_label.grid(row=1, column=0, padx=10, pady=10)
input2_entry.grid(row=1, column=1, padx=10, pady=10)
predict_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
output_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Ejecutar el bucle principal de la aplicación
root.mainloop()