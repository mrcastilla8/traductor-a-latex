import ply.yacc as yacc

# --- Abstract Syntax Tree (AST) Node Classes ---
class Node:
    pass

class BinOpNode(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinOp({self.left}, {self.op}, {self.right})"

class NumberNode(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Number({self.value})"

class VariableNode(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Variable({self.value})"

class FunctionNode(Node):
    def __init__(self, name, argument):
        self.name = name
        self.argument = argument

    def __repr__(self):
        return f"Function({self.name}, {self.argument})"

# --- Mock Lexer for Manual Token Input ---
class MockLexer:
    def __init__(self, tokens_json):
        import json
        self.tokens = []
        for token_dict in json.loads(tokens_json):
            token_dict['lineno'] = 1
            token_dict['lexpos'] = 1
            self.tokens.append(token_dict)
        self.index = 0

    def input(self, data):
        pass  # Ignore the input data

    def token(self):
        if self.index >= len(self.tokens):
            return None
        token_info = self.tokens[self.index]
        token_obj = type('Token', (object,), {})()
        for key, value in token_info.items():
            setattr(token_obj, key, value)
        self.index += 1
        return token_obj

# --- Parser Class ---
class Parser:
    tokens = [
        'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
        'VARIABLE', 'PAREN_OPEN', 'PAREN_CLOSE', 'FUNCTION'
    ]

    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('right', 'UMINUS'),
    )

    def __init__(self):
        self.parser = yacc.yacc(module=self, write_tables=False, debug=True)

    def parse_manual(self, tokens_json):
        mock_lexer = MockLexer(tokens_json)
        return self.parser.parse(input='', lexer=mock_lexer)  # Fixed keyword

    def test_ast(self):
        tokens_json = '''
        [
          {"type": "NUMBER", "value": "2"},
          {"type": "TIMES", "value": "*"},
          {"type": "PAREN_OPEN", "value": "("},
          {"type": "VARIABLE", "value": "x"},
          {"type": "PLUS", "value": "+"},
          {"type": "NUMBER", "value": "3"},
          {"type": "PAREN_CLOSE", "value": ")"},
          {"type": "DIVIDE", "value": "/"},
          {"type": "NUMBER", "value": "5"}
        ]
        '''
        ast = self.parse_manual(tokens_json)
        print("Generated AST:", ast)

    # Grammar Rules
    def p_expression_binop(self, p):
        '''expression : expression PLUS term
                      | expression MINUS term'''
        p[0] = BinOpNode(p[1], p[2], p[3])

    def p_expression_term(self, p):
        'expression : term'
        p[0] = p[1]

    def p_term_factor(self, p):
        'term : factor'
        p[0] = p[1]

    def p_term_times_divide(self, p):
        '''term : term TIMES factor
                | term DIVIDE factor'''
        p[0] = BinOpNode(p[1], p[2], p[3])

    def p_factor_num(self, p):
        'factor : NUMBER'
        p[0] = NumberNode(p[1])

    def p_factor_var(self, p):
        'factor : VARIABLE'
        p[0] = VariableNode(p[1])

    def p_factor_paren(self, p):
        'factor : PAREN_OPEN expression PAREN_CLOSE'
        p[0] = p[2]

    def p_factor_unary_minus(self, p):
        'factor : MINUS factor %prec UMINUS'
        p[0] = BinOpNode(NumberNode(0), '-', p[2])

    def p_function_call(self, p):
        'factor : FUNCTION PAREN_OPEN expression PAREN_CLOSE'
        p[0] = FunctionNode(p[1], p[3])

    # Error Handling
    def p_error(self, p):
        if p:
            print(f"Sintaxis incorrecta: Token '{p.value}' en posición {p.lexpos}")
        else:
            print("Sintaxis incorrecta: Final del archivo")

parser = Parser()
parser.test_ast()