import ply.yacc as yacc
from sintactico import Parser
from lexico import Lexer
from sintactico import BinOpNode,ConstantNode, FunctionNode, NumberNode, VariableNode
from semantico import SemanticAnalyzer

class LatexGenerator:
    def __init__(self, ast):
        """Inicializa el generador con un Árbol de Sintaxis Abstracta (AST)."""
        self.ast = ast

    def generate(self):
        """Genera código LaTeX a partir del AST."""
        return self._generate_latex(self.ast)

    def _generate_latex(self, node):
        """Método recursivo para convertir nodos del AST en LaTeX."""
        if isinstance(node, NumberNode):
            return str(node.value)
        elif isinstance(node, ConstantNode):
            if node.value == "pi":
                return f"\\pi"
        elif isinstance(node, VariableNode):
            return node.name
        elif isinstance(node, BinOpNode):
            left = self._generate_latex(node.left)
            right = self._generate_latex(node.right)
            if node.operator == "+":
                return f"{left} + {right}"
            elif node.operator == '-':
                return f"{left} - {right}"
            elif node.operator == '*':
                # Asegurar que la multiplicación se pareterice si es necesario
                left = self._add_parentheses_if_needed(node.left, node.operator)
                right = self._add_parentheses_if_needed(node.right, node.operator)
                return f"{left} \\cdot {right}"
            elif node.operator == '/':
                return f"\\frac{{{left}}}{{{right}}}"
            elif node.operator == '^':
                # Asegurar que la base se pareterice si es necesario
                left = self._add_parentheses_if_needed(node.left, node.operator)
                return f"{left}^{{{right}}}"
        elif isinstance(node, FunctionNode):
            # Procesar cada argumento y convertirlo a LaTeX
            args_latex = [self._generate_latex(arg) for arg in node.arguments]

            # Generar el LaTeX para la función
            if node.name == "sqrt":
                return f"\\sqrt{{{args_latex[0]}}}"
            elif node.name == "exp":
                return f"e^{{{args_latex[0]}}}"
            elif node.name in {"sin", "cos", "tan", "log", "abs"}:
                return f"\\{node.name}({{{args_latex[0]}}})"
            else:
                raise ValueError(f"Error semántico: Función '{node.name}' no soportada en LaTeX.")
        return ""

    def _add_parentheses_if_needed(self, node, parent_op):
        """Añade paréntesis si es necesario para mantener la precedencia."""
        latex = self._generate_latex(node)
        # No añadir paréntesis si el nodo es una función (ya tienen sus propios paréntesis)
        if isinstance(node, FunctionNode):
            return latex
        if isinstance(node, BinOpNode):
            if self._precedence(node.operator) < self._precedence(parent_op):
                return f"({latex})"
        return latex

    def _precedence(self, op):
        """Devuelve la precedencia de un operador."""
        if op in {'+', '-'}:
            return 1
        elif op in {'*', '/'}:
            return 2
        elif op == '^':
            return 3
        return 0


if __name__ == "__main__":

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
                print("AST generado:", ast)
                generator = LatexGenerator(ast)
                latex_code = generator.generate()
                print(latex_code)

        except ZeroDivisionError as e:
            print("\nError semántico:", str(e))
        except ValueError as e:
            print("\nError semántico:", str(e))
        except Exception as e:
            print("\nError inesperado:", str(e))