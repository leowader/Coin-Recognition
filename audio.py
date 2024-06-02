import pyaudio
import numpy as np
import threading
from scipy import signal

# Variables para verificar si el micrófono está activo y para almacenar los datos de audio
mic_active = False
audio_data = []

def calculate_frequency(audio_data, sample_rate):
    """
    Calcula la frecuencia dominante en el audio utilizando la transformada de Fourier.
    """
    # Aplica la transformada de Fourier
    fft_data = np.fft.fft(audio_data)
    # Calcula la magnitud de las frecuencias
    magnitude = np.abs(fft_data)
    # Encuentra el índice de la frecuencia dominante
    dominant_index = np.argmax(magnitude)
    # Calcula la frecuencia correspondiente al índice
    frequency = dominant_index * sample_rate / len(audio_data)
    return frequency

def record_audio():
    """
    Función para grabar audio desde el micrófono.
    """
    global mic_active, audio_data
    # Configura los parámetros de grabación
    duration = 10  # Duración de la grabación en segundos
    sample_rate = 44100  # Tasa de muestreo en Hz
    chunk = 1024  # Tamaño del búfer de audio
    # Coeficientes del filtro de preénfasis y post-enfasis
    preemphasis_coeff = 0.97
    postemphasis_coeff = 1.0 / preemphasis_coeff
    preemphasis_filter = [1, -preemphasis_coeff]
    postemphasis_filter = [1, -postemphasis_coeff]
    # Inicia la grabación
    audio_data = []
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=sample_rate, input=True, output=True, frames_per_buffer=chunk)
    mic_active = True
    print("Grabando audio... (Presiona '2' para detener)")
    for _ in range(int(sample_rate / chunk * duration)):
        data = stream.read(chunk)
        # Aplica el filtro de preénfasis
        data = signal.lfilter(preemphasis_filter, 1, np.frombuffer(data, dtype=np.float32))
        audio_data.append(data)
        if not mic_active:
            break
    stream.stop_stream()
    stream.close()
    p.terminate()
    mic_active = False
    print("Grabación finalizada.")
    # Concatena los fragmentos de audio en un solo array
    audio_data = np.concatenate(audio_data)
    print("audi",audio_data)
    # Aplica el filtro de post-enfasis
    audio_data = signal.lfilter(postemphasis_filter, 1, audio_data)
    # Calcula la frecuencia del audio grabado
    frequency = calculate_frequency(audio_data, sample_rate)
    print("Frecuencia del audio: {:.2f} Hz".format(frequency))

def main():
    """
    Función principal que controla la grabación del micrófono.
    """
    global mic_active
    print("Presiona '1' para iniciar la grabación del micrófono.")
    while True:
        key = input()
        if key == '1' and not mic_active:
            # Inicia la grabación en un hilo separado
            threading.Thread(target=record_audio).start()
        elif key == '2' and mic_active:
            # Detiene la grabación si está activa
            mic_active = False

if __name__ == "__main__":
    main()
