import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
import pandas as pd
import numpy as np

def createModel():
    # Configuración de la red
    model = tf.keras.Sequential([
        tf.keras.Input(shape=(1,)),# numero de entradas
        tf.keras.layers.Dense(256,  activation='relu'), 
        tf.keras.layers.Dense(128, activation='relu'),  
        tf.keras.layers.Dense(1, activation='linear')  
    ])
    model.compile(optimizer=tf.keras.optimizers.Adam(0.01), loss='mean_squared_error')
    return model

def normalize(inputs):
    maxNumber = max(inputs)
    results = [number / maxNumber for number in inputs]
    return np.array(results)

def training():
    datos = pd.read_excel("logic/data/500.xlsx")
    x = datos.filter(like='Hz') 
    y = datos.filter(like='Moneda')
    datosx = np.array(x, dtype=float)
    datosy = np.array(y, dtype=float)
    inputsNormalize = normalize(datosx)
    model=createModel()
    model.fit(inputsNormalize, datosy, epochs=1000, verbose=0)
    # Datos de prueba
    X2 = np.array([[6286.05]], dtype=float)
    x2Normalizado=[num / max(datosx) for num in X2]

    predictions = model.predict(x2Normalizado)
    model.summary()
    model.save("logic/models/prueba2.keras")#guardar modelo
    print("resultado red",predictions)
    return predictions

def simulation():
    model= tf.keras.models.load_model("logic/models/prueba2.keras")#importar modelo entrenado
    print("Simulacion")
    model.summary()
    x = pd.read_excel("logic/data/500.xlsx").filter(like="Hz")
    X2 = np.array([[7440.11]], dtype=float)#pasar por parametro esto
    x2Normalizado=[num / max(np.array(x,dtype=float)) for num in X2]
    predictions=model.predict(x2Normalizado)
    print("prediction",predictions)
    return predictions