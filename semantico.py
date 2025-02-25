from sintactico import NumberNode, VariableNode, ConstantNode, BinOpNode, FunctionNode
import math

class SemanticAnalyzer:
    """
    Analizador semántico que valida el AST y detecta errores semánticos.
    Realiza una evaluación parcial de la expresión para detectar errores como división por 0 y exponentes inválidos.
    """

    MATH_FUNCTIONS = {
        'sqrt': 1, 'sin': 1, 'cos': 1, 'tan': 1,
        'log': 1, 'exp': 1, 'abs': 1
    }
    CONSTANTS = {'pi', 'π'}

    def __init__(self):
        self.variables = {}

    def evaluate_static(self, node):
        """
        Intenta evaluar el nodo si es estático (número o constante).
        Devuelve el valor numérico o None si no es evaluable.
        """
        if isinstance(node, NumberNode):
            return node.value
        elif isinstance(node, ConstantNode):
            if node.value in self.CONSTANTS:
                return math.pi
        return None

    def validate(self, node):
        """
        Valida el nodo, realizando una evaluación parcial cuando es posible.
        """
        if isinstance(node, NumberNode) or isinstance(node, ConstantNode):
            value = self.evaluate_static(node)
            if value is None:
                raise ValueError(f"Error semántico: Constante desconocida '{node.value}'.")
            return value

        elif isinstance(node, VariableNode):
            # Se consideran válidas sin evaluar
            return None

        elif isinstance(node, BinOpNode):
            left_val = self.validate(node.left)
            right_val = self.validate(node.right)

            if node.operator not in {'+', '-', '*', '/', '^'}:
                raise ValueError(f"Error semántico: Operador desconocido '{node.operator}'.")

            if node.operator == '/':
                # Si ambos operandos son evaluables, comprobar división entre 0
                if right_val is not None and right_val == 0:
                    raise ZeroDivisionError("Error semántico: División entre 0 detectada.")
                # Si no se evaluó completamente, intentar evaluar el denominador de forma estática
                elif right_val is None:
                    static_right = self.evaluate_static(node.right)
                    if static_right == 0:
                        raise ZeroDivisionError("Error semántico: División entre 0 detectada.")

            if node.operator == '^':
                if left_val is not None and right_val is not None:
                    if left_val == 0 and right_val < 0:
                        raise ValueError("Error semántico: No se puede elevar 0 a un exponente negativo.")
                else:
                    static_left = self.evaluate_static(node.left)
                    static_right = self.evaluate_static(node.right)
                    if static_left == 0 and static_right is not None and static_right < 0:
                        raise ValueError("Error semántico: No se puede elevar 0 a un exponente negativo.")

            # Si ambos operandos se evaluaron, se puede calcular el resultado parcial (opcional)
            if left_val is not None and right_val is not None:
                if node.operator == '+':
                    return left_val + right_val
                elif node.operator == '-':
                    return left_val - right_val
                elif node.operator == '*':
                    return left_val * right_val
                elif node.operator == '/':
                    return left_val / right_val
                elif node.operator == '^':
                    return left_val ** right_val

            return None

        elif isinstance(node, FunctionNode):
            if node.name not in self.MATH_FUNCTIONS:
                raise ValueError(f"Error semántico: Función desconocida '{node.name}'.")

            expected_args = self.MATH_FUNCTIONS[node.name]
            if not node.arguments or len(node.arguments) == 0:
                raise ValueError(f"Error semántico: La función '{node.name}' requiere {expected_args} argumento(s), pero recibió 0.")
            if len(node.arguments) != expected_args:
                raise ValueError(f"Error semántico: La función '{node.name}' esperaba {expected_args} argumento(s), pero recibió {len(node.arguments)}.")

            # Evaluar el primer argumento (en nuestro caso, sqrt espera 1 argumento)
            arg_value = self.validate(node.arguments[0])
            
            # Verificar específicamente para sqrt
            if node.name == 'sqrt' and arg_value is not None and arg_value < 0:
                raise ValueError("Error semántico: No se puede calcular la raíz cuadrada de un número negativo en los números reales.")

            # Luego se validan todos los argumentos recursivamente
            for arg in node.arguments:
                self.validate(arg)

            return None

        else:
            raise ValueError("Error semántico: Nodo inválido en la expresión.")

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

            ast = parser.parse(entrada, lexer=lexer)
            if parser.error:
                print("No se puede validar el AST debido a errores sintácticos.")
            else:
                semantic_analyzer.validate(ast)
                print("El AST es válido y no tiene errores semánticos.")

        except ZeroDivisionError as e:
            print("\n", str(e))
        except ValueError as e:
            print("\n", str(e))
        except Exception as e:
            print("\nError inesperado:", str(e))