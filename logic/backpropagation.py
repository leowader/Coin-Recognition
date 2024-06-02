import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
import pandas as pd
import numpy as np

datos = pd.read_excel("logic/data/500.xlsx")
x = datos.filter(like='Hz') 
y = datos.filter(like='Moneda')

datosx = np.array(x, dtype=float)
datosy = np.array(y, dtype=float)

# normalizando
maximo = max(datosx)
print("maximo",maximo)
# Divide cada número por el máximo
resultados = [numero / maximo for numero in datosx]
xNormalizado=np.array(resultados)
print("resultados nomalizados",xNormalizado)

# Configuración de la red
model = tf.keras.Sequential([
    tf.keras.Input(shape=(1,)),# numero de entradas
    tf.keras.layers.Dense(80,  activation='relu'), 
    tf.keras.layers.Dense(90, activation='relu'),  
    tf.keras.layers.Dense(1, activation='linear')  
])

model.compile(optimizer=tf.keras.optimizers.Adam(0.01), loss='mean_squared_error')

# Entrenar el modelo
model.fit(xNormalizado, datosy, epochs=1000, verbose=0)

# Datos de prueba
X2 = np.array([[6004]], dtype=float)
x2Normalizado=[num / maximo for num in X2]

predictions = model.predict(x2Normalizado)
rounded_predictions = np.round(predictions).astype(int)

print("Salida de la red neuronal")
print(predictions)
print("Salida deseada:")
print(datosy[4])
# model.summary()
# model.save("logic/data/prueba.keras")#guardar modelo una vez entrenado 
# mimodelo=tf.keras.models.load_model("logic/data/prueba.keras")# importar modelo guardado
# mimodelo.summary()