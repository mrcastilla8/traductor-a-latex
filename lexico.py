# pylint: disable=C0103,C0116
"""
Este módulo implementa un analizador léxico utilizando PLY.
"""

import ply.lex as lex

class Lexer:
    """
    Analizador léxico que tokeniza expresiones matemáticas.
    Soporta números, variables, operadores, funciones y constantes matemáticas.
    """
    # ANALISIS LEXICOGRAFICO: Especificacion de componentes lexicos
    tokens = (
        'NUMBER', 'VARIABLE', 'OPERATOR',
        'PAREN_OPEN', 'PAREN_CLOSE', 'CONSTANT', 'FUNCTION'
    )

    # Lista de funciones matemáticas soportadas
    MATH_FUNCTIONS = {'sqrt', 'sin', 'cos', 'tan', 'log', 'exp', 'abs'}

    # EXPRESIONES REGULARES Y AUTOMATAS FINITOS: Expresiopnes regularees
    t_OPERATOR = r'\+|\-|\*|\/|\^'
    t_PAREN_OPEN = r'\('
    t_PAREN_CLOSE = r'\)'
    t_ignore = ' \t'

    # EXPRESIONES REGULARES Y AUTOMATAS FINITOS: Uso de automatas finitos deterministas
    def t_NUMBER(self, t):
        r'\d+\.?\d*'
        t.value = float(t.value) if '.' in t.value else int(t.value)
        return t

    def t_VARIABLE(self, t):
        r'[a-zA-Z_]+'
        if t.value in self.MATH_FUNCTIONS:
            t.type = 'FUNCTION'
        elif t.value in {'pi', 'π'}:
            t.type = 'CONSTANT'
        return t

    def t_error(self, t):
        print(f"Error léxico: carácter no reconocido '{t.value[0]}' en posición {t.lexpos}")
        t.lexer.skip(1)

    def __init__(self):
        self.lexer = lex.lex(module=self)

    # ANALISIS LEXICOGRAFICO: Construccion de analizador lexicos
    def tokenize(self, expr):
        """Convierte una expresión en una lista de tokens."""
        self.lexer.input(expr)
        return [{"type": tok.type, "value": tok.value} for tok in self.lexer]

if __name__ == "__main__":
    lexer = Lexer()
    user_expression = input("Introduce una expresión matemática: ")
    tokens = lexer.tokenize(user_expression)
    print(tokens)
