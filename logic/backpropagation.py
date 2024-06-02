import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
import pandas as pd
import numpy as np

datos = pd.read_excel("logic/data/data.xlsx")

x = datos.filter(like='X') 
y = datos.filter(like='Y')

datosx = np.array(x, dtype=int)
datosy = np.array(y, dtype=int)

# Configuración de la red
model = tf.keras.Sequential([
    tf.keras.Input(shape=(3,)),# numero de entradas
    tf.keras.layers.Dense(40,  activation='sigmoid'),  # Capa oculta con 40 neuronas y función de activación sigmoide
    tf.keras.layers.Dense(30, activation='sigmoid'),  # Capa oculta adicional con 30 neuronas y función de activación sigmoide
    tf.keras.layers.Dense(3, activation=tf.nn.sigmoid)  # Capa de salida con 3 neurona y función de activación sigmoide
])
# tf.keras.layers.Dense(40, input_dim=3, activation='sigmoid'), #primera capa con el numero de entradas

model.compile(optimizer=tf.keras.optimizers.Adam(0.1), loss='mean_squared_error')

# Entrenar el modelo
model.fit(datosx, datosy, epochs=500, verbose=0)

# Datos de prueba
X2 = np.array([[0, 0, 0],
               [1, 0, 1],
               [1, 1, 0],
               [1, 1, 1]], dtype=int)

# Hacer predicciones
predictions = model.predict(X2)

rounded_predictions = np.round(predictions).astype(int)

print("Salida de la red neuronal")
print(rounded_predictions)

print("Salida deseada:")
print(datosy)