from cProfile import label
import tkinter as tk
from PIL import Image, ImageTk

# Función para cambiar el texto cuando se presiona el botón
def toggle_text():
    if label.cget("text") == "Grabando audio":
        label.config(text="Audio grabado")
    else:
        label.config(text="Grabando audio")

# Crear la ventana principal
root = tk.Tk()
root.title("Reconocimiento de moneda")

# Ajustar el tamaño de la ventana (ancho x alto)
root.geometry("400x400")

# Cargar la imagen del micrófono
mic_image = Image.open("./img/microred.png")  # Asegúrate de tener el archivo "microphone.png" en el mismo directorio
mic_image = mic_image.resize((100, 100), Image.Resampling.LANCZOS)  # Ajustar el tamaño de la imagen
mic_photo = ImageTk.PhotoImage(mic_image)

# Crear un lienzo para el botón circular
canvas = tk.Canvas(root, width=100, height=100)
canvas.pack(expand=True)  # Permite que el lienzo se expanda

# Dibujar un círculo en el lienzo
# canvas.create_oval(10, 10, 90, 90, fill="blue")

# Crear un botón con la imagen del micrófono y ajustar el tamaño del botón con padding
button = tk.Button(root, image=mic_photo, borderwidth=0, padx=20, pady=20, command=toggle_text)  # Agregar comando para el botón
button_window = canvas.create_window(50, 50, window=button)

# Centrar el lienzo en la ventana principal
canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Crear una etiqueta para mostrar el estado del audio
label = tk.Label(root, text="")
label.pack(pady=20)

# Ejecutar el bucle principal de la aplicación
root.mainloop()