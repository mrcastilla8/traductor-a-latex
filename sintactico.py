import ply.yacc as yacc
from lexico import Lexer

class Parser:
    def __init__(self):
        """Inicializa el analizador sintáctico."""
        self.tokens = None  # Se obtendrán desde Lexer
        self.parser = None  # Aquí se definirá el parser

    def parse(self, tokens):
        """Convierte una lista de tokens en un AST."""
        pass  # Implementación futura

    def manejar_errores(self):
        """Manejo de errores sintácticos (operadores mal colocados, etc.)."""
        pass
