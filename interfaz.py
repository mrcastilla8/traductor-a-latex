import customtkinter as ctk
from PIL import Image
import pyperclip
from pygame import mixer
import datetime
from lexico import Lexer
from sintactico import Parser
from semantico import SemanticAnalyzer
from generador_latex import LatexGenerator
from generador_pdf import PDFGenerator


# Inicializar pygame mixer para reproducir sonidos
mixer.init()

class ChatLatexApp:
    def __init__(self):
        self.app = ctk.CTk()
        self.chat_created = False
        self.window = None
        self.notification_sound = mixer.Sound("notification.wav")



        # Configuración de la aplicación
        self.app.title("ChatLatex")
        chat_width = 1000
        chat_height = 700
        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()
        pos_x = int((screen_width / 2) - (chat_width / 2))
        pos_y = int((screen_height / 2) - (chat_height / 2))
        self.app.geometry(f"{chat_width}x{chat_height}+{pos_x}+{pos_y}")
        self.app.configure(fg_color="#081c29")  # Fondo principal

        # Cargar imágenes
        self.user_img = ctk.CTkImage(light_image=Image.open("user.png"), size=(40, 40))
        self.bot_img = ctk.CTkImage(light_image=Image.open("bot.png"), size=(40, 40))
        self.copy_img = ctk.CTkImage(light_image=Image.open("copy.png"), size=(20, 20))
        self.download_img = ctk.CTkImage(light_image=Image.open("download.png"), size=(20, 20))

        


    def start(self):
        self.start_window()

    def start_window(self):
        self.window = ctk.CTk()
        self.window.title("ChatLatex - Inicio")
        self.window_width = 800
        self.window_height = 400
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        pos_x = int((screen_width / 2) - (self.window_width / 2))
        pos_y = int((screen_height / 2) - (self.window_height / 2))
        self.window.geometry(f"{self.window_width}x{self.window_height}+{pos_x}+{pos_y}")
        self.window.configure(fg_color="#081c29")  # Fondo principal

        title_label = ctk.CTkLabel(self.window, text="Bienvenido a ChatLatex", font=("Poppins", 26, "bold"), text_color="#4d4e4f",
                                   fg_color="#93d0f8", corner_radius=8, padx=10, pady=10)
        title_label.pack(fill="x", padx=20, pady=10)

        start_button = ctk.CTkButton(self.window, text="Empezar a traducir", command=self.open_chat, font=("Poppins", 16, "bold"), width=250, height=100)
        start_button.pack(pady=20)


        self.window.mainloop()



    def open_chat(self):
        if not self.chat_created:
            self.chat_window()
            self.chat_created = True
        self.window.withdraw()  # Oculta la ventana de inicio
        self.app.deiconify()    # Muestra la ventana de chat

    def go_back(self):
        self.app.withdraw()  # Oculta la ventana de chat
        self.window.deiconify()  # Muestra la ventana de inicio
    def generate_latex_for_expressions(self,expressions):
        """
        Generates LaTeX content for a list of expressions.
        """
        latex_content = ""
        for idx, expr in enumerate(expressions, start=1):
            latex_content += f"\\subsection*{{Expression {idx}:}}\n"
            latex_content += f"\\[{expr}\\]\n\n"
        return latex_content


    def chat_window(self):
        back_frame = ctk.CTkFrame(self.app, fg_color="#081c29", corner_radius=8)
        back_frame.pack(fill="x", padx=20, pady=10)

        back_button = ctk.CTkButton(back_frame, text="Regresar", command=self.go_back, font=("Poppins", 16, "bold"))
        back_button.pack(side="left", padx=10)
        # Botón de reiniciar chat
        restart_button = ctk.CTkButton(back_frame, text="Reiniciar Chat", command=self.restart_chat, font=("Poppins", 16, "bold"))
        restart_button.pack(side="left", padx=10)
        self.title_label = ctk.CTkLabel(self.app, text="Traductor a Latex", font=("Poppins", 26, "bold"), text_color="#4d4e4f",
                               fg_color="#93d0f8", corner_radius=8, padx=10, pady=10)
        self.title_label.pack(fill="x", padx=20, pady=10)

        self.chat_frame = ctk.CTkScrollableFrame(self.app, fg_color="#0a2536", corner_radius=12)
        self.chat_frame.pack(fill="both", expand=True, padx=20, pady=10)
        # Inicializar componentes
        self.lexer = Lexer().lexer
        self.parser = Parser()
        self.semantic_analyzer = SemanticAnalyzer()
        self.expression_number=1
        # Lista para almacenar las expresiones
        self.expresiones = []

        # Estado para seguimiento de las interacciones
        self.state = "waiting_for_message"
        self.pdf_name = ""
        self.author = ""

        # Enviar mensaje de bienvenida automáticamente
        self.add_message("Bienvenido al generador de PDFs matemáticos.\n"
                     "Ingresa una expresión matemática y se generará un PDF con las expresiones renderizadas.\n"
                     "Escribe 'salir' para terminar el programa y generar el PDF.\n", 
                     self.chat_frame, sender="bot")

        entry_frame = ctk.CTkFrame(self.app, fg_color="#0a2536", corner_radius=12)
        entry_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        def on_textbox_click(event):
            if textbox.get("1.0", "end-1c") == "Type your message here...":
                textbox.configure(state="normal")
                textbox.delete("1.0", "end")

        textbox = ctk.CTkTextbox(entry_frame, height=80, wrap="word", fg_color="#252525", text_color="#FFFFFF", corner_radius=12, border_width=0, padx=10, pady=10, font=("Roboto", 14))
        textbox.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Configurar el texto de marcador de posición
        textbox.insert("0.0", "Type your message here...")
        textbox.configure(state="disabled")

        textbox.bind("<Button-1>", on_textbox_click)

        submit_button = ctk.CTkButton(entry_frame, text="Enviar", fg_color="#2196F3", text_color="white", corner_radius=12, command=lambda: self.send_message(textbox, self.chat_frame))
        submit_button.pack(side="right", padx=10, pady=10)
        if self.state == "finished":
            textbox.configure(state="disabled")
            submit_button.configure(state="disable")


    def send_message(self, textbox, chat_frame):
        user_message = textbox.get("1.0", "end-1c").strip()
        mensaje_bot = ""

        try:
            if self.state == "finished":
                # Si el estado es "finished", no permitir más mensajes
                self.add_message("El chat ha terminado. Debes reiniciar el chat para continuar.", chat_frame, sender="bot")
                return  # Salir de la función para evitar que se procese el mensaje
            if user_message.lower() == "salir":
                # Detener la ejecución del código cuando el usuario escribe "salir"
                self.state = "waiting_for_pdf_name"
                self.add_message("salir", chat_frame, sender="user")
                self.add_message("Por favor, ingresa el nombre del archivo PDF (sin extensión):", chat_frame, sender="bot")
            elif self.state == "waiting_for_pdf_name":
                self.pdf_name = user_message
                self.state = "waiting_for_author"
                self.add_message(user_message, chat_frame, sender="user")
                self.add_message(f"Nombre del PDF: {self.pdf_name}\nAhora, por favor, ingresa el autor del PDF:", chat_frame, sender="bot")
            elif self.state == "waiting_for_author":
                                
                self.author = user_message
                self.state = "finished"
                self.add_message(user_message, chat_frame, sender="user")
                self.add_message(f"Autor: {self.author}\nPDF generado con el nombre: {self.pdf_name} y autor: {self.author}. Puedes descargarlo", chat_frame, sender="bot")
                # Aquí podemos hacer la lógica para generar el PDF
            else:
                # Solo procesar las expresiones si no se está en el estado de "waiting_for_pdf_name"
                self.add_message(user_message, chat_frame, sender="user")
                ast = self.parser.parse(user_message, lexer=self.lexer)
                if self.parser.error:
                    mensaje_bot += "\nError: No se puede generar el AST debido a errores sintácticos."
                    self.add_message(mensaje_bot, chat_frame, sender="bot")
                else:
                    mensaje_bot += f"Expresion {self.expression_number}"
                    # Validar el AST semánticamente
                    self.semantic_analyzer.validate(ast)
                    mensaje_bot += f"\nEl AST es válido y no tiene errores semánticos.\nAST generado:{ast}"
                    # Generar código LaTeX a partir del AST
                    generator = LatexGenerator(ast)
                    latex_content = generator.generate()
                    mensaje_bot += f"\nCódigo LaTeX generado: {latex_content}"

                    self.add_message(mensaje_bot, chat_frame, sender="bot")
                    self.expresiones.append(latex_content)

                    # Mostrar la expresión con el número correspondiente
                    self.expression_number += 1

            # Limpiar el cuadro de texto
            textbox.delete("1.0", "end")
            textbox.configure(state="normal")
        except ZeroDivisionError as e:
            mensaje_bot += f"\nError semántico: {str(e)}"
            self.add_message(mensaje_bot, chat_frame, sender="bot")
        except ValueError as e:
            mensaje_bot += f"\nError semántico: {str(e)}"
            self.add_message(mensaje_bot, chat_frame, sender="bot")
        except Exception as e:
            mensaje_bot += f"\nError semántico: {str(e)}"
            self.add_message(mensaje_bot, chat_frame, sender="bot")


    def add_message(self, text, chat_frame, sender="user"):
        frame = ctk.CTkFrame(chat_frame, fg_color="transparent")
        frame.pack(fill="x", padx=10, pady=5, anchor="e" if sender == "user" else "w")

        if sender == "user":
            img_label = ctk.CTkLabel(frame, image=self.user_img, text="") 
            img_label.pack(side="right", padx=5)
            text_label = ctk.CTkLabel(frame, text=text, fg_color="#3B5998", text_color="white", corner_radius=12, padx=10, pady=5, wraplength=400, font=("Poppins", 14))
            text_label.pack(side="right")
        else:
            img_label = ctk.CTkLabel(frame, image=self.bot_img, text="") 
            img_label.pack(side="left", padx=5)

            text_frame = ctk.CTkFrame(frame, fg_color="transparent")
            text_frame.pack(side="left", fill="x")

            text_label = ctk.CTkLabel(text_frame, text=text, fg_color="#616161", text_color="white", corner_radius=12, padx=10, pady=5, wraplength=400, font=("Open Sans", 14))
            text_label.pack()

            button_frame = ctk.CTkFrame(text_frame, fg_color="transparent")
            button_frame.pack(pady=2)

            copy_button = ctk.CTkButton(button_frame, image=self.copy_img, text="", fg_color="#f6f9fb", corner_radius=8, width=40, height=40, command=lambda: pyperclip.copy(text))
            copy_button.pack(side="left", padx=5)
            if self.state!="finished":
                download_button = ctk.CTkButton(button_frame, image=self.download_img, text="", fg_color="#f6f9fb", corner_radius=8, width=40, height=40,  state="disabled")
                download_button.pack(side="left", padx=5)
            else: 
                download_button = ctk.CTkButton(button_frame, image=self.download_img, text="", fg_color="#f6f9fb", corner_radius=8, width=40, height=40, command=lambda: self.download_latex(self.pdf_name,self.author), state="normal")
                download_button.pack(side="left", padx=5)

        if sender == "bot":
            self.notify_message()
    
    def download_latex(self, nombre_pdf, autor_pdf):
            if self.expresiones:
            # Solicitar el nombre del archivo PDF
                if not nombre_pdf:
                    nombre_pdf = "output"  # Nombre por defecto
                nombre_pdf += ".pdf"  # Añadir extensión .pdf

                # Solicitar el nombre del autor
                if not autor_pdf:
                    author_pdf= "Desconocido"  # Autor por defecto

                # Obtener la fecha y hora actual (formato dd/mm/yyyy HH:MM)
                timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

                # Generar el contenido LaTeX para todas las expresiones
                latex_content = self.generate_latex_for_expressions(self.expresiones)

                # Generar el PDF a partir del código LaTeX
                pdf_generator = PDFGenerator(latex_content, nombre_pdf,autor_pdf, timestamp)
                pdf_generator.generate_pdf()

                # Mostrar mensaje de confirmación
                self.show_confirmation_message("El PDF se ha generado correctamente", "Éxito")

            else:
                self.add_message("No se ingresaron expresiones válidas. No se generará ningún PDF.", self.ch)
    def show_confirmation_message(self, message, title):
        # Crear la ventana emergente de confirmación
        ventana_confirmacion = ctk.CTkToplevel(self.app)
        ventana_confirmacion.title(title)
        ventana_confirmacion.geometry("300x150")
         # Obtener las dimensiones de la pantalla
        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()
    
        # Obtener las dimensiones de la ventana emergente
        window_width = 300  # Ancho de la ventana
        window_height = 150  # Alto de la ventana
    
        # Calcular la posición para centrar la ventana
        position_top = int((screen_height / 2) - (window_height / 2))
        position_left = int((screen_width / 2) - (window_width / 2))
    
        # Establecer la geometría de la ventana emergente en función de la posición calculada
        ventana_confirmacion.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")
    
        ventana_confirmacion.lift()
        # Etiqueta con el mensaje
        mensaje = ctk.CTkLabel(ventana_confirmacion, text=message, anchor="center", font=("Poppins", 14, "bold"))
        mensaje.pack(pady=20)
    
        # Botón para cerrar la ventana
        boton_cerrar = ctk.CTkButton(ventana_confirmacion, text="Cerrar", command=ventana_confirmacion.destroy)
        boton_cerrar.pack(pady=10)
        # Mantener la ventana emergente al frente si el usuario hace clic fuera de ella
        ventana_confirmacion.grab_set()  # Esto bloquea la interacción con la ventana principal hasta que se cierre la emergente
    def notify_message(self):
        self.notification_sound.play()  # Reproduce el sonido cuando el bot responde
    def restart_chat(self):
        # Limpiar las expresiones
        self.expresiones = []
    
        # Restablecer el número de expresión
        self.expression_number = 1
    
        # Restablecer el estado del chat
        self.state = "waiting_for_message"
        self.pdf_name = ""
        self.author = ""
        
        # Limpiar el marco de mensajes
        for widget in self.app.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and widget not in [self.window, self.chat_frame]:  # Evitar destruir la ventana principal y el chat_frame
                widget.destroy()
        # Volver a crear la ventana de chat con todos los componentes necesarios
        self.title_label.destroy()
        self.chat_window()

    


# Ejecutar la aplicación
if __name__ == "__main__":
    app = ChatLatexApp()
    app.start()