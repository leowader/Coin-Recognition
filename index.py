import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
import numpy as np

X = np.array([[0, 0],
              [0, 1],
              [1, 0],
              [1, 1]])

y = np.array([[0],
              [1],
              [1],
              [0]])

# Configuracion de la red
model = tf.keras.Sequential([
    tf.keras.layers.Dense(40, input_dim=2, activation='sigmoid'),  # Capa oculta con 40 neuronas y función de activación sigmoide
    tf.keras.layers.Dense(30, activation='sigmoid'),  # Capa oculta adicional con 30 neuronas y función de activación sigmoide
    tf.keras.layers.Dense(1, activation='sigmoid')  # Capa de salida con 1 neurona y función de activación sigmoide
])

model.compile(tf.keras.optimizers.Adam(0.1), loss='mean_squared_error')

# Entrenar el modelo
model.fit(X, y, epochs=1000, verbose=0)

# datos de prueba
X2 = np.array([[0.1, 0.1],
              [0, 0.9],
              [0.9, 0],
              [0.9, 0.9]])
predictions = model.predict(X2)
rounded_predictions = np.round(predictions)
print("Salida de la red neuronal después del entrenamiento:")
rounded_numbers = [[round(num[0], 1)] for num in predictions]
print(rounded_numbers)