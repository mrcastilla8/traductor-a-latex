import ply.yacc as yacc
from lexico import Lexer  # Importa el Lexer actualizado

class NumberNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Number({self.value})"

class VariableNode:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Variable({self.name})"

class ConstantNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Constant({self.value})"

class BinOpNode:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"BinOp({self.left}, {self.operator}, {self.right})"

class FunctionNode:
    def __init__(self, name, argument):
        self.name = name
        self.argument = argument

    def __repr__(self):
        return f"Function({self.name}, {self.argument})"

class Parser:
    tokens = Lexer.tokens  # Tokens definidos en lexico.py

    precedence = (
        ('right', 'POWER'),     # Exponente
        ('left', 'TIMES', 'DIVIDE'),   # Multiplicación y división
        ('left', 'PLUS', 'MINUS'),     # Suma y resta
    )

    def __init__(self):
        self.parser = yacc.yacc(module=self)

    def parse(self, data, lexer):
        return self.parser.parse(data, lexer=lexer)

    # --- Reglas gramaticales ---
    def p_expression_plus(self, p):
        'expression : expression PLUS term'
        p[0] = BinOpNode(p[1], '+', p[3])

    def p_expression_minus(self, p):
        'expression : expression MINUS term'
        p[0] = BinOpNode(p[1], '-', p[3])

    def p_expression_term(self, p):
        'expression : term'
        p[0] = p[1]

    def p_term_times(self, p):
        'term : term TIMES expression'
        p[0] = BinOpNode(p[1], '*', p[3])

    def p_term_divide(self, p):
        'term : term DIVIDE expression'
        p[0] = BinOpNode(p[1], '/', p[3])

    def p_term_power(self, p):
        'term : term POWER factor'
        p[0] = BinOpNode(p[1], '^', p[3])

    def p_term_factor(self, p):
        'term : factor'
        p[0] = p[1]

    def p_factor_number(self, p):
        'factor : NUMBER'
        p[0] = NumberNode(p[1])

    def p_factor_variable(self, p):
        'factor : VARIABLE'
        p[0] = VariableNode(p[1])

    def p_factor_constant(self, p):
        'factor : CONSTANT'
        p[0] = ConstantNode(p[1])

    def p_factor_function(self, p):
        'factor : FUNCTION PAREN_OPEN expression PAREN_CLOSE'
        p[0] = FunctionNode(p[1], p[3])

    def p_factor_paren(self, p):
        'factor : PAREN_OPEN expression PAREN_CLOSE'
        p[0] = p[2]

    def p_error(self, p):
        if p:
            print(f"\nError de sintaxis: Token '{p.value}' no esperado en posición {p.lexpos}")
        else:
            print("\nError de sintaxis: Final inesperado de la entrada")

# --- Función principal ---
if __name__ == "__main__":
    lexer = Lexer().lexer  # Crea el lexer
    parser = Parser()      # Crea el parser

    while True:
        try:
            entrada = input("\nIngresa una expresión matemática (o escribe 'salir' para terminar): ")
            if entrada.lower() == "salir":
                break
            resultado = parser.parse(entrada, lexer=lexer)
            print("AST generado:", resultado)
        except Exception as e:
            print("\nError durante el análisis:", str(e))