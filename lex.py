# Compilation Command
# python -m PyInstaller --distpath DEV/dist --workpath DEV/build --specpath DEV/ --noconfirm --hidden-import llama-cpp-python --hidden-import pyttsx3 --hidden-import comtypes.client --windowed --hidden-import comtypes.gen --onedir --add-data "C:\Users\ignac\Desktop\Proyectos\Assistant\env\Lib\site-packages\comtypes;comtypes" --add-data "C:\Users\ignac\Desktop\Proyectos\Assistant\env\Lib\site-packages\customtkinter;customtkinter/" --clean --icon "C:\Users\ignac\Desktop\Proyectos\Assistant\assets\lex_1.ico" --add-data "C:\Users\ignac\Desktop\Proyectos\Assistant\env\Lib\site-packages\pyttsx3;pyttsx3" --add-data "C:\Users\ignac\Desktop\Proyectos\Assistant\env\Lib\site-packages\llama_cpp;llama_cpp" --add-data "C:\Users\ignac\Desktop\Proyectos\Assistant\assets;assets/" --add-data "C:\Users\ignac\Desktop\Proyectos\Assistant\models\;models/" "C:\Users\ignac\Desktop\Proyectos\Assistant\lex.py"
# CORREGIR DIMENSIONES DE LA VENTANA DE CONVERSACION EN COMPARACION CON LA VENTANA DEL SOFTWARE
# Añadir TTS
# Añadir lectura de archivos
# Añadir Transcripción de audio
# Añadir varios chats según los archivos JSON que haya 
import customtkinter as ctk
import threading
from llama_cpp import Llama
import json
import pyttsx3
import os
from tkinter import filedialog
from datetime import datetime

class ChatApp(ctk.CTk):
    global history
    global engine
    global llm
    history = []
    version = "Release 2.2"

    engine = pyttsx3.init()
    for voice in engine.getProperty('voices'):
        if 'spanish' in voice.languages and 'male' in voice.id:
            engine.setProperty('voice', voice.id)
            break
    actual_speed = engine.getProperty('rate')
    engine.setProperty('rate', int(actual_speed * 1.2))


    llm = Llama(
        model_path = "models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf",
        #model_path="_internal/models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf",
        n_gpu_layers=30,
        n_batch=4096,
        n_ctx=21504,
        n_threads=8,
        chat_format="llama-3"
    )

    def __init__(self):
        super().__init__()

        self.title("Lexicon")
        self.geometry("700x800")

        # Cuadro de texto para mostrar los mensajes
        self.text_area = ctk.CTkTextbox(self, state='disabled')
        self.text_area.pack(padx=10, pady=10, fill="both", expand=True)

        # Iconos
        self.iconbitmap('assets/lex_1.ico')
        #self.iconbitmap('_internal/assets/lex_1.ico')
        self.after(201, lambda: self.iconbitmap('assets/lex_1.ico'))
        #self.after(201, lambda: self.iconbitmap('_internal/assets/lex_1.ico'))

        # Frame para la entrada de texto y los botones
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        # Campo de entrada de texto
        self.input_text = ctk.CTkEntry(input_frame)
        self.input_text.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # Botón de enviar
        self.send_button = ctk.CTkButton(input_frame, text="Enviar", command=self.send_message)
        self.send_button.pack(side="right")

        # Botón para guardar la conversación en JSON
        self.save_button = ctk.CTkButton(self, text="Save JSON", command=self.save_to_json)
        self.save_button.pack(side="left", padx=10, pady=10)

        # Botón para cargar una conversación desde JSON
        self.load_button = ctk.CTkButton(self, text="Load JSON", command=self.load_from_json)
        self.load_button.pack(side="left", padx=10, pady=10)

        # Switch para activar/desactivar TTS
        self.tts_switch = ctk.CTkSwitch(self, text="TTS", command=self.on_switch_toggle)
        self.tts_switch.pack(side="right", padx=0, pady=0)

        self.tts_enabled = False

        # Mensaje de carga
        self.loading_label = ctk.CTkLabel(self, text="", fg_color="transparent")
        self.loading_label.pack(padx=0, pady=0)

        # Versión de la aplicación
        self.version_label = ctk.CTkLabel(self, text=self.version, fg_color="transparent")
        self.version_label.pack(side="bottom", anchor="se", padx=0, pady=0)

        # Bind de la tecla Enter
        self.input_text.bind("<Return>", lambda event: self.send_message())

    def on_switch_toggle(self):
        self.tts_enabled = self.tts_switch.get()

    def text_to_speech(self, ai_message):
        if self.tts_enabled:
            engine.say(ai_message)
            engine.runAndWait()

    def send_message(self):
        user_message = self.input_text.get()
        if user_message.strip() == "":
            return  # No enviar mensajes vacíos
        
        history.append({"role": "user", "content": user_message})
        now = datetime.now()
        date_time = now.strftime("%d/%m/%Y %H:%M:%S")
        history.append({"role": "system", "content": f"{date_time}"})

        self.display_message(f"\nTú: {user_message}\n")
        self.save_to_json()

        # Limpiar el campo de entrada
        self.input_text.delete(0, 'end')

        # Mostrar mensaje de carga y deshabilitar el botón de enviar
        self.loading_label.configure(text="Cargando Respuesta...")
        self.send_button.configure(state='disabled')
        self.input_text.unbind("<Return>")

        # Ejecutar la llamada a la IA en un hilo separado
        threading.Thread(target=self.get_ai_response).start()

    def get_ai_response(self):
        # Llamar a la IA
        completion = llm.create_chat_completion(
            model="local-model",
            messages=history,
            temperature=0.8,
        )

        ai_message = completion['choices'][0]['message']['content']

        # Mostrar la respuesta en el hilo principal
        self.after(0, lambda: self.display_ai_message(ai_message))
        self.text_to_speech(ai_message)
        self.save_to_json()

    def display_ai_message(self, ai_message):
        history.append({"role": "assistant", "content": ai_message})
        self.loading_label.configure(text="")  # Borrar mensaje de carga
        self.display_message(f"\nIA: {ai_message}\n")

        # Volver a habilitar el botón de enviar
        self.send_button.configure(state='normal')
        self.input_text.bind("<Return>", lambda event: self.send_message())

    def display_message(self, message):
        self.text_area.configure(state='normal')  # Habilitar el cuadro de texto
        self.text_area.insert('end', message)  # Añadir el mensaje
        self.text_area.configure(state='disabled')  # Volver a deshabilitar el cuadro de texto
        self.text_area.yview('end')  # Desplazar hacia abajo

    def save_to_json(self):
        self.loading_label.configure(text="Guardando archivo JSON...")
        folder = "chats/"
        #folder = "_internal/chats/"
        if not os.path.isdir(folder):
            os.makedirs(folder)
        # Generar un nombre de archivo basado en la fecha y hora si el archivo ya existe
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{folder}chat_{timestamp}.json"

        # Guardar la conversación en formato JSON
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(history, file, ensure_ascii=False, indent=4)

        # Mostrar mensaje de guardado
        self.loading_label.configure(text="Archivo JSON guardado.")
        self.after(2000, lambda: self.loading_label.configure(text=""))  # El mensaje desaparece después de 2 segundos
        #print(f"Conversación guardada en {filename}")

    def load_from_json(self):
        # Mostrar mensaje de carga
        self.loading_label.configure(text="Cargando archivo JSON...")

        # Abrir una ventana de diálogo para seleccionar el archivo JSON
        filepath = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filepath:
            # Vaciar la lista de historia actual
            history.clear()

            # Cargar el archivo JSON seleccionado
            with open(filepath, 'r', encoding='utf-8') as file:
                loaded_history = json.load(file)
                history.extend(loaded_history)

            # Mostrar los mensajes cargados en la ventana de chat
            self.text_area.configure(state='normal')
            self.text_area.delete(1.0, 'end')  # Limpiar el área de texto
            for message in history:
                if message["role"] == "user":
                    self.display_message(f"\nTú: {message['content']}\n")
                elif message["role"] == "assistant":
                    self.display_message(f"\nIA: {message['content']}\n")
            self.text_area.configure(state='disabled')
        
        self.loading_label.configure(text="Archivo JSON cargado")
        self.after(2000, lambda: self.loading_label.configure(text=""))  # El mensaje desaparece después de 2 segundos

if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()
