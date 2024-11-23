import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import time
from docx import Document
import PyPDF2
import os
from transformers import pipeline

# Inicializar el modelo preentrenado de Hugging Face para análisis de sentimientos (Sistemas Inteligentes)
analizador_sentimientos = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# Listas de palabras críticas
palabras_criticas = {"matar", "quitar", "suicidar", "agredir", "cortar"}

# Función de un autómata de pila para detectar palabras críticas (Teoria de la computacion)
def automata_palabras_criticas(texto):
    stack = []
    for palabra in texto.split():
        if palabra.lower() in palabras_criticas:
            stack.append(palabra.lower())  # Empujar palabra crítica en la pila
    return len(stack) > 0  # Si hay palabras en la pila, existe una palabra crítica

# Función para cargar un archivo
def cargar_documento():
    ruta_archivo = filedialog.askopenfilename(
        title="Selecciona un archivo",
        filetypes=(("Archivos de texto y documentos", ".txt;.docx;*.pdf"),)
    )

    if ruta_archivo:
        extension = os.path.splitext(ruta_archivo)[1].lower()
        try:
            if extension == ".txt":
                with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                    texto = archivo.read()
            elif extension == ".docx":
                doc = Document(ruta_archivo)
                texto = '\n'.join([para.text for para in doc.paragraphs])
            elif extension == ".pdf":
                with open(ruta_archivo, 'rb') as archivo_pdf:
                    lector_pdf = PyPDF2.PdfReader(archivo_pdf)
                    texto = ''
                    for pagina in lector_pdf.pages:
                        texto += pagina.extract_text()
            else:
                messagebox.showerror("Error", "Formato de archivo no compatible.")
                return

            entrada_texto.delete(1.0, tk.END)
            entrada_texto.insert(tk.END, texto)
            eliminar_placeholder()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")

# Función de análisis de sentimientos usando el modelo preentrenado (Sistemas inteligentes)
def analizar_texto():
    texto = entrada_texto.get(1.0, tk.END).strip()
    if not texto:
        messagebox.showerror("Error", "Debe ingresar o cargar un texto para analizar.")
        return
    
    # Cambiar a la ventana de análisis
    cambiar_ventana(ventana_analizando)
    ventana_analizando.update()
    time.sleep(2)  # Simular análisis durante 2 segundos

    # Verificar palabras críticas usando el autómata de pila (Teoria de la computacion)
    necesita_ayuda = automata_palabras_criticas(texto)
    
    # Analizar el sentimiento usando el modelo (Sistemas Inteligentes)
    if necesita_ayuda:
        estado_emocional = "negativo con necesidad de ayuda urgente"
    else:
        resultado = analizador_sentimientos(texto[:512])  # Límite de tokens(palabras) para el analisis a traves del modelo 
        sentimiento = resultado[0]['label']
        
        # Mapear la respuesta del modelo a un estado emocional (Sistemas Inteligentes)
        if "1" in sentimiento or "2" in sentimiento:
            estado_emocional = "negativo"
        elif "4" in sentimiento or "5" in sentimiento:
            estado_emocional = "positivo"
        else:
            estado_emocional = "neutral"

    # Cambiar a la ventana de resultados y mostrar el estado emocional
    cambiar_ventana(ventana_resultado)
    texto_resultado.config(state=tk.NORMAL)
    texto_resultado.delete(1.0, tk.END)
    texto_resultado.insert(tk.END, f"Resultado del análisis: El texto tiene un sentimiento {estado_emocional}.\n")
    texto_resultado.config(state=tk.DISABLED)

# Función para cambiar entre ventanas
def cambiar_ventana(ventana):
    for v in [ventana_presentacion, ventana_inicio, ventana_analizando, ventana_resultado]:
        v.place_forget()
    ventana.place(x=0, y=0, relwidth=1, relheight=1)

# Función para eliminar el texto de marcador de posición
def eliminar_placeholder(event=None):
    if entrada_texto.get(1.0, tk.END).strip() == "Ingresa o pega el texto aquí...":
        entrada_texto.delete(1.0, tk.END)

# Función para restablecer el cuadro de texto con el placeholder
def restablecer_texto_inicio():
    entrada_texto.delete(1.0, tk.END)  # Limpiar el campo de texto
    entrada_texto.insert(tk.END, "Ingresa o pega el texto aquí...")  # Insertar el placeholder

# Función para redimensionar la imagen de fondo según el tamaño de la ventana
def ajustar_imagen(event, label_fondo):
    nuevo_ancho = event.width
    nuevo_alto = event.height
    imagen_redimensionada = imagen_comun.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
    fondo_comun_resized = ImageTk.PhotoImage(imagen_redimensionada)
    label_fondo.config(image=fondo_comun_resized)
    label_fondo.image = fondo_comun_resized  # Evitar que la imagen sea recolectada por el garbage collector

# Inicialización de la ventana principal y la GUI(Interfaz grafica de usuario)
root = tk.Tk()
root.title("Analizador de Textos")
root.geometry("600x500")
root.resizable(False, False)
root.configure(bg="#2E6EC2")

# Deshabilitar redimensionamiento y eliminar el botón de maximizar
root.resizable(False, False)
# Cambiar el color de fondo a #2E6EC2
root.configure(bg="#2E6EC2")

# Estilo de los botones
boton_style = {
    "font": ("Arial", 14),
    "bg": "#0056b3",
    "fg": "white",
    "activebackground": "#004090",
    "activeforeground": "white",
    "bd": 0,
    "relief": tk.FLAT
}

imagen_comun = Image.open("fondo.png")  # Imagen de fondo sobre un fondo azul

# Ventana de presentación
ventana_presentacion = tk.Frame(root, bg="#2E6EC2")
ventana_presentacion.place(x=0, y=0, relwidth=1, relheight=1)

label_titulo_presentacion = tk.Label(ventana_presentacion, text="Bienvenido al Analizador de Sentimientos", bg="#2E6EC2", fg="white", font=("Arial", 18))
label_titulo_presentacion.pack(pady=20)

# Cargar y mostrar imagen de presentación
imagen_presentacion = Image.open("Escudo.png")  # Ruta de la imagen de presentación
imagen_presentacion = imagen_presentacion.resize((200, 200), Image.Resampling.LANCZOS)
img_presentacion = ImageTk.PhotoImage(imagen_presentacion)
label_imagen_presentacion = tk.Label(ventana_presentacion, image=img_presentacion, bg="#2E6EC2")
label_imagen_presentacion.pack(pady=10)

label_autores = tk.Label(ventana_presentacion, text=" José Jimenez \n Edinson Palacio \n Julio Peñaloza", bg="#2E6EC2", fg="white", font=("Arial", 14))
label_autores.pack(pady=10)

# Botón para comenzar
boton_comenzar = tk.Button(ventana_presentacion, text="Comenzar", command=lambda: cambiar_ventana(ventana_inicio))
boton_comenzar.pack(pady=20)

# Ventana de inicio
ventana_inicio = tk.Frame(root, bg="#2E6EC2")
ventana_inicio.place(x=0, y=0, relwidth=1, relheight=1)

# Imagen de fondo sobre el fondo azul
label_fondo_inicio = tk.Label(ventana_inicio, bg="#2E6EC2")
label_fondo_inicio.place(x=0, y=0, relwidth=1, relheight=1)

# Llamar a la función para redimensionar la imagen cuando la ventana cambia de tamaño
ventana_inicio.bind("<Configure>", lambda event: ajustar_imagen(event, label_fondo_inicio))

label_bienvenida = tk.Label(ventana_inicio, text="Analizar Sentimientos", bg="#2E6EC2", fg="white", font=("Arial", 16))
label_bienvenida.pack(pady=20)

# Cuadro de texto con placeholder
entrada_texto = tk.Text(ventana_inicio, height=10, width=50, wrap=tk.WORD)
entrada_texto.pack(pady=10)
entrada_texto.insert(tk.END, "Ingresa o pega el texto aquí...")
entrada_texto.bind("<FocusIn>", eliminar_placeholder)

# Crear un frame para alinear los botones horizontalmente
frame_botones = tk.Frame(ventana_inicio, bg="#2E6EC2")
frame_botones.pack(pady=10)

# Redimensionar el icono de carga
imagen_icono = Image.open("cargar.png")  # Cargar la imagen del icono
imagen_icono = imagen_icono.resize((60,60), Image.Resampling.LANCZOS)
icono_cargar = ImageTk.PhotoImage(imagen_icono)

# Botón para analizar
boton_analizar = tk.Button(frame_botones, text="Analizar", command=analizar_texto, **boton_style)
boton_analizar.grid(row=0, column=0, padx=5)

# Icono de carga 
boton_cargar = tk.Button(frame_botones, image=icono_cargar, command=cargar_documento, bg="white", bd=0)
boton_cargar.grid(row=0, column=1, padx=5)

# Ventana de análisis
ventana_analizando = tk.Frame(root, bg="#2E6EC2")
ventana_analizando.place(x=0, y=0, relwidth=1, relheight=1)

label_fondo_analizando = tk.Label(ventana_analizando, bg="#2E6EC2")
label_fondo_analizando.place(x=0, y=0, relwidth=1, relheight=1)

# Llamar a la función para redimensionar la imagen cuando la ventana cambia de tamaño
ventana_analizando.bind("<Configure>", lambda event: ajustar_imagen(event, label_fondo_analizando))

label_analizando = tk.Label(ventana_analizando, text="Analizando...", bg="#2E6EC2", fg="white", font=("Arial", 18))
label_analizando.pack(pady=20)

# Ventana de resultados
ventana_resultado = tk.Frame(root, bg="#2E6EC2")
ventana_resultado.place(x=0, y=0, relwidth=1, relheight=1)

label_fondo_resultado = tk.Label(ventana_resultado, bg="#2E6EC2")
label_fondo_resultado.place(x=0, y=0, relwidth=1, relheight=1)

# Llamar a la función para redimensionar la imagen cuando la ventana cambia de tamaño
ventana_resultado.bind("<Configure>", lambda event: ajustar_imagen(event, label_fondo_resultado))

label_resultado = tk.Label(ventana_resultado, text="Resultado del Análisis", bg="#2E6EC2", fg="white", font=("Arial", 16))
label_resultado.pack(pady=20)

texto_resultado = tk.Text(ventana_resultado, height=10, width=50, wrap=tk.WORD, state=tk.DISABLED)
texto_resultado.pack(pady=10)

boton_inicio = tk.Button(ventana_resultado, text="Volver ", command=lambda: [cambiar_ventana(ventana_inicio), restablecer_texto_inicio()], **boton_style)
boton_inicio.pack(pady=20)

# Comenzar con la ventana de presentación
cambiar_ventana(ventana_presentacion)

# Ejecutar la aplicación
root.mainloop()