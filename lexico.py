import re
import ply.lex as lex  # Si se usa PLY

class Lexer:
    def __init__(self):
        """Inicializa el analizador léxico."""
        self.lexer = None  # Aquí se definirá el lexer

    def tokenize(self, expression):
        """Convierte una expresión matemática en una lista de tokens."""
        pass  # Implementación futura

    def manejar_errores(self):
        """Manejo de errores léxicos (caracteres no reconocidos, etc.)."""
        pass
