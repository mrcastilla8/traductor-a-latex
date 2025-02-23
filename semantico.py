from sintactico import Parser

class SemanticAnalyzer:
    def __init__(self):
        """Inicializa el analizador semántico."""
        self.ast = None  # Se recibirá un AST para analizar

    def validar_ast(self, ast):
        """Valida el AST generado por el parser."""
        pass  # Implementación futura

    def manejar_errores(self):
        """Manejo de errores semánticos (paréntesis desbalanceados, etc.)."""
        pass
