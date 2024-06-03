from cProfile import label #Para mostrar los mensajes en la interfaz
import tkinter as tk #Para la interfaz grafica
from PIL import Image, ImageTk #Para manejar imagenes
import sounddevice as sd
import numpy as np #Para manejar los datos de audio
from scipy.io.wavfile import write #Para manejar los datos de audio
from pydub import AudioSegment
import threading #Para manejar la grabación de audio en un hilo separado.
import os #Para manejar el guardado de archivo en los directorios

# Variables globales para la grabación de audio
is_recording = False
recording_thread = None
filename_wav = "output.wav"
filename_mp3 = "output.mp3"
directory = "./audio/"  # Cambia esto al directorio deseado

def toggle_recording():
    global is_recording, recording_thread

    if is_recording:
        is_recording = False
        status_label.config(text="Audio grabado")
        save_audio()
    else:
        is_recording = True
        status_label.config(text="Grabando audio")
        recording_thread = threading.Thread(target=record_audio)
        recording_thread.start()

def record_audio():
    global is_recording, filename_wav
    fs = 44100  # Frecuencia de muestreo
    duration = 10  # Duración máxima (segundos)

    # Grabar audio
    print("Grabando...")
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='int16')
    sd.wait()  # Esperar hasta que se complete la grabación
    write(filename_wav, fs, audio_data)
    print("Grabación completada")

def save_audio():
    global filename_wav, filename_mp3, directory
    # Convertir el archivo WAV a MP3
    audio = AudioSegment.from_wav(filename_wav)
    audio.export(os.path.join(directory, filename_mp3), format="mp3")
    print(f"Audio guardado como {filename_mp3} en {directory}")

# Crear la ventana principal
root = tk.Tk()
root.title("Reconocimiento de moneda")

# Ajustar el tamaño de la ventana (ancho x alto)
root.geometry("400x400")

# Cargar la imagen del micrófono
try:
    mic_image = Image.open("./img/microred.png")
    mic_image = mic_image.resize((100, 100), Image.Resampling.LANCZOS)
    mic_photo = ImageTk.PhotoImage(mic_image)
except FileNotFoundError:
    print("No se encontró la imagen del micrófono.")
    root.destroy()

# Crear un lienzo para el botón circular
canvas = tk.Canvas(root, width=100, height=100)
canvas.pack(expand=True)  # Permite que el lienzo se expanda

# Crear un botón con la imagen del micrófono y ajustar el tamaño del botón con padding
button = tk.Button(root, image=mic_photo, borderwidth=0, padx=20, pady=20, command=toggle_recording)
button_window = canvas.create_window(50, 50, window=button)

# Centrar el lienzo en la ventana principal
canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Crear una etiqueta para mostrar el estado del audio
label = tk.Label(root, text="")
label.pack(pady=20)

# Crear una etiqueta para mostrar el estado del audio
status_label = tk.Label(root, text="")
status_label.pack(pady=20)

# Ejecutar el bucle principal de la aplicación
root.mainloop()