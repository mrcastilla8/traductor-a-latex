import subprocess
import os

class PDFGenerator:
    def __init__(self, latex_content, output_pdf="output.pdf", author="Desconocido", timestamp=""):
        """
        Inicializa el generador de PDF con el contenido LaTeX, el nombre del archivo de salida,
        el autor y la fecha/hora de generación.
        
        :param latex_content: Contenido LaTeX generado por LatexGenerator (solo el contenido, sin preámbulo).
        :param output_pdf: Nombre del archivo PDF de salida (por defecto: "output.pdf").
        :param author: Nombre del autor del documento (por defecto: "Desconocido").
        :param timestamp: Fecha y hora en que se generó el documento.
        """
        self.latex_content = latex_content
        self.output_pdf = output_pdf
        self.author = author
        self.timestamp = timestamp
        self.title = os.path.splitext(output_pdf)[0]  # Usa el nombre del archivo sin la extensión como título

    def generate_pdf(self):
        """
        Genera un archivo PDF a partir del contenido LaTeX.
        """
        # Código LaTeX con título, autor y fecha/hora
        latex_code = (
            r"\documentclass{article}"
            "\n"
            r"\usepackage{amsmath}"  # Paquete para mejorar la representación matemática
            "\n"
            r"\usepackage{geometry}"  # Ajustar márgenes
            "\n"
            r"\geometry{a4paper, margin=1in}"  # Márgenes más amplios
            "\n"
            r"\begin{document}"
            "\n"
            r"\centering"  # Centrar contenido
            "\n"
            r"\LARGE\textbf{" + self.title + "}"  # Título en negrita
            "\n\n"
            r"\vspace{0.5cm}" "\n"
            r"\large Autor: " + self.author + "\n\n"
            r"\vspace{0.5cm}" "\n"
            r"\small Fecha: " + self.timestamp + "\n\n"
            r"\Huge"  # Hace la ecuación grande
            "\n"
            f"{self.latex_content}"  # Expresión matemática centrada
            "\n"
            r"\end{document}"
        )

        # Escribe el código LaTeX en un archivo temporal
        with open("temp.tex", "w", encoding="utf-8") as f:
            f.write(latex_code)
        print("Archivo LaTeX creado: temp.tex")
        
        try:
            # Compila el archivo LaTeX a PDF usando pdflatex
            print("Compilando con pdflatex...")
            subprocess.run(["pdflatex", "-interaction=nonstopmode", "temp.tex"], check=True)
            
            # Verifica si el PDF se generó correctamente
            if os.path.exists("temp.pdf"):
                print(f"PDF generado correctamente: temp.pdf")
                # Renombra el archivo PDF generado
                if os.path.exists(self.output_pdf):
                    os.remove(self.output_pdf)
                os.rename("temp.pdf", self.output_pdf)
                print(f"PDF renombrado a: {self.output_pdf}")
            else:
                print("Error: No se pudo generar el PDF.")
        
        except subprocess.CalledProcessError as e:
            print(f"Error al compilar el archivo LaTeX: {e}")
            # Si hay un error, muestra el archivo de log
            if os.path.exists("temp.log"):
                with open("temp.log", "r", encoding="utf-8") as log_file:
                    print("Detalles del error:")
                    print(log_file.read())
        
        finally:
            # Limpia los archivos temporales (opcional)
            print("Limpiando archivos temporales...")
            for ext in [".aux", ".log", ".tex"]:
                if os.path.exists(f"temp{ext}"):
                    os.remove(f"temp{ext}")
                    print(f"Archivo eliminado: temp{ext}")