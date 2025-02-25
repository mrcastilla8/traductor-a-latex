import datetime
from lexico import Lexer
from sintactico import Parser
from semantico import SemanticAnalyzer
from generador_latex import LatexGenerator
from generador_pdf import PDFGenerator

def generate_latex_for_expressions(expressions):
    """
    Generates LaTeX content for a list of expressions.
    """
    latex_content = ""
    for idx, expr in enumerate(expressions, start=1):
        latex_content += f"\\subsection*{{Expression {idx}:}}\n"
        latex_content += f"\\[{expr}\\]\n\n"
    return latex_content

def main():
    # Inicializar componentes
    lexer = Lexer().lexer
    parser = Parser()
    semantic_analyzer = SemanticAnalyzer()

    print("Bienvenido al generador de PDFs matemáticos.")
    print("Ingresa una expresión matemática y se generará un PDF con las expresiones renderizadas.")
    print("Escribe 'salir' para terminar el programa y generar el PDF.\n")

    expressions = []  # Lista para almacenar todas las expresiones válidas

    while True:
        try:
            # Solicitar la expresión matemática
            entrada = input("\nIngresa una expresión matemática (o 'salir' para terminar): ")
            if entrada.lower() == "salir":
                break

            # Analizar la expresión y generar el AST
            ast = parser.parse(entrada, lexer=lexer)
            if parser.error:
                print("Error: No se puede generar el AST debido a errores sintácticos.")
                continue

            # Validar el AST semánticamente
            semantic_analyzer.validate(ast)
            print("El AST es válido y no tiene errores semánticos.")
            print("AST generado:", ast)

            # Generar código LaTeX a partir del AST
            generator = LatexGenerator(ast)
            latex_content = generator.generate()
            print("Código LaTeX generado:", latex_content)

            # Agregar la expresión LaTeX a la lista de expresiones
            expressions.append(latex_content)

        except ZeroDivisionError as e:
            print("\nError semántico:", str(e))
        except ValueError as e:
            print("\nError semántico:", str(e))
        except Exception as e:
            print("\nError inesperado:", str(e))

    if expressions:
        # Solicitar el nombre del archivo PDF
        pdf_name = input("Ingresa el nombre del archivo PDF (sin extensión): ").strip()
        if not pdf_name:
            pdf_name = "output"  # Nombre por defecto
        pdf_name += ".pdf"  # Añadir extensión .pdf

        # Solicitar el nombre del autor
        author = input("Ingresa el nombre del autor: ").strip()
        if not author:
            author = "Desconocido"  # Autor por defecto

        # Obtener la fecha y hora actual (formato dd/mm/yyyy HH:MM)
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

        # Generar el contenido LaTeX para todas las expresiones
        latex_content = generate_latex_for_expressions(expressions)

        # Generar el PDF a partir del código LaTeX
        pdf_generator = PDFGenerator(latex_content, pdf_name, author, timestamp)
        pdf_generator.generate_pdf()
    else:
        print("No se ingresaron expresiones válidas. No se generará ningún PDF.")

if __name__ == "__main__":
    main()