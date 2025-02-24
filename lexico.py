import ply.lex as lex

class Lexer:
    """
    Analizador léxico que tokeniza expresiones matemáticas.
    Soporta números, variables, operadores, funciones y constantes matemáticas.
    """
    # Definición de los tokens
    tokens = (
        'NUMBER', 'VARIABLE', 'CONSTANT',
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER',
        'PAREN_OPEN', 'PAREN_CLOSE', 'FUNCTION', 'COMMA'
    )

    # Lista de funciones matemáticas soportadas
    MATH_FUNCTIONS = {'sqrt', 'sin', 'cos', 'tan', 'log', 'exp', 'abs'}
    

    # Reglas para reconocer tokens con expresiones regulares
    t_COMMA = r','
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_POWER = r'\^'
    t_PAREN_OPEN = r'\('
    t_PAREN_CLOSE = r'\)'
    t_ignore = ' \t'

    def t_NUMBER(self, t):
        r'\d+\.?\d*'
        t.value = float(t.value) if '.' in t.value else int(t.value)
        return t

    def t_VARIABLE(self, t):
        r'[a-zA-Z_]+'
        if t.value in self.MATH_FUNCTIONS:
            t.type = 'FUNCTION'
        elif t.value.lower() in {'pi', 'π'}:
            t.type = 'CONSTANT'
        return t

    def t_error(self, t):
        print(f"Error léxico: Carácter no reconocido '{t.value[0]}' en posición {t.lexpos}")
        t.lexer.skip(1)

    def __init__(self):
        self.lexer = lex.lex(module=self)

    def tokenize(self, expr):
        self.lexer.input(expr)
        return [{"type": tok.type, "value": tok.value} for tok in self.lexer]

# Ejemplo de uso
if __name__ == "__main__":
    lexer = Lexer()
    user_expression = input("Introduce una expresión matemática: ")
    tokens = lexer.tokenize(user_expression)
    print(tokens)