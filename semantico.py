from sintactico import NumberNode, VariableNode, ConstantNode, BinOpNode, FunctionNode

import math

class SemanticAnalyzer:
    """
    Analizador semántico que valida el AST y detecta errores semánticos.
    También evalúa parcialmente la expresión para detectar errores como división por 0.
    """

    MATH_FUNCTIONS = {
        'sqrt': 1, 'sin': 1, 'cos': 1, 'tan': 1,
        'log': 1, 'exp': 1, 'abs': 1
    }  # Funciones y la cantidad de argumentos esperados

    CONSTANTS = {'pi', 'π'}

    def __init__(self):
        self.variables = {}  # Diccionario de variables con sus valores

    def validate(self, node):
        """
        Recorre el AST y valida que la estructura sea correcta.
        Además, evalúa parcialmente la expresión para detectar errores.
        :param node: Nodo raíz del AST.
        """
        if isinstance(node, NumberNode):
            return node.value  # Devolver el valor numérico

        elif isinstance(node, ConstantNode):
            if node.value in self.CONSTANTS:
                return math.pi  # Usamos el valor de pi como ejemplo
            else:
                raise ValueError(f"Constante desconocida: {node.value}")

        elif isinstance(node, VariableNode):
            if node.name not in self.variables:
                raise ValueError(f"Variable no definida: {node.name}")
            return self.variables[node.name]  # Retornar el valor de la variable

        elif isinstance(node, BinOpNode):
            left_val = self.validate(node.left)  # Validar y obtener el valor izquierdo
            right_val = self.validate(node.right)  # Validar y obtener el valor derecho

            if node.operator not in {'+', '-', '*', '/', '^'}:
                raise ValueError(f"Operador desconocido: {node.operator}")

            if node.operator == '/':
                if right_val == 0:
                    raise ZeroDivisionError("Error semántico: División entre 0 detectada.")

            if node.operator == '^':
                if left_val == 0 and right_val < 0:
                    raise ValueError("Error semántico: No se puede elevar 0 a un exponente negativo.")

            return 0  # Solo estamos validando, no calculamos el resultado final

        elif isinstance(node, FunctionNode):
            if node.name not in self.MATH_FUNCTIONS:
                raise ValueError(f"Función desconocida: {node.name}")

            expected_args = self.MATH_FUNCTIONS[node.name]
            if len(node.arguments) != expected_args:
                raise ValueError(f"La función '{node.name}' esperaba {expected_args} argumento(s), pero recibió {len(node.arguments)}.")

            for arg in node.arguments:
                self.validate(arg)  # Validamos cada argumento

            return 0  # No calculamos el resultado, solo validamos

        else:
            raise ValueError("Error semántico: Nodo inválido en la expresión")

if __name__ == "__main__":
    from lexico import Lexer
    from sintactico import Parser

    lexer = Lexer().lexer
    parser = Parser()
    semantic_analyzer = SemanticAnalyzer()

    while True:
        try:
            entrada = input("\nIngresa una expresión matemática (o 'salir' para terminar): ")
            if entrada.lower() == "salir":
                break

            ast = parser.parse(entrada, lexer=lexer)  # Obtener el AST generado
            if parser.error:
                print("No se puede validar el AST debido a errores sintácticos.")
            else:
                semantic_analyzer.validate(ast)  # Validamos y evaluamos semánticamente
                print("El AST es válido y no tiene errores semánticos.")

        except ZeroDivisionError as e:
            print("\nError semántico:", str(e))
        except ValueError as e:
            print("\nError semántico:", str(e))
        except Exception as e:
            print("\nError inesperado:", str(e))