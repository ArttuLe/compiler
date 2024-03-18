from compiler.tokenizer import Token
import compiler.ast as ast
from compiler.types import Bool, Int, Unit


def parse(tokens: list[Token]) -> ast.Expression:
    pos = 0
    
    def peek() -> Token:
        if len(tokens) == 0:
            raise ValueError("Empty Token")
        if pos < len(tokens):
            return tokens[pos]
        else:
            return Token(
                location=tokens[-1].location,
                type="end",
                text="",
            )

    def consume(expected: str | list[str] | None = None) -> Token:
        nonlocal pos
        token = peek()
        if isinstance(expected, str) and token.text != expected:
            raise Exception(f'{token.location}: expected "{expected}"')
        if isinstance(expected, list) and token.text not in expected:
            comma_separated = ", ".join([f'"{e}"' for e in expected])
            raise Exception(f'{token.location}: expected one of: {comma_separated}')
        pos += 1
        return token

    def parse_int_literal() -> ast.Literal:
        if peek().type != 'int_literal':
            raise Exception(f'{peek().location}: expected an integer literal')
        token = consume()
        return ast.Literal(value=int(token.text), location=token.location)
    
    def parse_identifier() -> ast.Identifier:
        if peek().type != 'identifier':
            raise Exception(f'{peek().location}: expected an identifier')
        token = consume()
        return ast.Identifier(name=token.text, location=token.location)
    
    def parse_arg_list() -> ast.Function:
        args = []
        consume('(')
        if peek().text != ')':
            args.append(parse_expression())
            while peek().text == ',':
                consume(',')
                args.append(parse_expression())
        consume(')')
        return args

    def parse_controlflow() -> ast.ControlFlow:
        if peek().type not in ["if", "else", "while", "then", "do"]:
            raise Exception(f'{peek().location}: expected an conditional expression')
        consume('if')
        if_expr = parse_expression()
        consume('then')
        then_expr = parse_expression()
        if peek().type == "else":
            consume('else')
            else_expr = parse_expression()
            return ast.ControlFlow(peek().location, if_expr, then_expr, else_expr)
        else:
            return ast.ControlFlow(peek().location, if_expr, then_expr, None)

        
    def parse_term() -> ast.Expression:
        left = parse_factor()
        while peek().text in ['*', '/', '%']:
            operator_token = consume()
            operator = operator_token.text
            right = parse_factor()
            left = ast.BinaryOp(
                peek().location,
                left,
                operator,
                right,
            )
        return left
    
    def parse_factor() -> ast.Expression:
        if peek().text == '(':
            return parse_parenthesized()
        elif peek().type == 'int_literal':
            return parse_int_literal()
        elif peek().text in ['-', 'not']:
            operator_token = consume()
            operator = operator_token.text
            operand = parse_factor()
            return ast.UnaryOp(peek().location, operator, operand)
        elif peek().type == 'identifier':
            identifier = parse_identifier()
            if peek().text == '(':
                args = parse_arg_list()
                return ast.Function(peek().location, identifier, args)
            return identifier
        elif peek().type in ["if", "else", "then"]:
            return parse_controlflow()
        else:
            raise Exception(f'{peek().location}: expected "(", an integer literal or an identifier')

    def parse_parenthesized() -> ast.Expression:
        consume('(')
        expr = parse_expression()
        consume(')')
        return expr
    
    def parse_while_loops() -> ast.WhileLoop:
        consume('while')
        condition = parse_expression()
        consume('do')
        block = parse_blocks()
        return ast.WhileLoop(peek().location, condition, block)
    
    def parse_arith_expression() -> ast.Expression:
        left = parse_term()

        while peek().text in ['+', '-']:
            operator_token = consume()
            operator = operator_token.text
            right = parse_term()
            left = ast.BinaryOp(peek().location, left, operator, right)

        return left

    def parse_comparison_expression() -> ast.Expression:
        left = parse_arith_expression()

        while peek().text in ['==', '!=', '<', '<=', '>', '>=']:
            operator_token = consume()
            operator = operator_token.text
            right = parse_arith_expression()
            left = ast.BinaryOp(peek().location, left, operator, right)

        return left

    def parse_logical_and_expression() -> ast.Expression:
        left = parse_comparison_expression()

        while peek().text == 'and':
            consume('and')
            right = parse_comparison_expression()
            left = ast.BinaryOp(peek().location, left, 'and', right)

        return left

    def parse_logical_or_expression() -> ast.Expression:
        left = parse_logical_and_expression()

        while peek().text == 'or':
            consume('or')
            right = parse_logical_and_expression()
            left = ast.BinaryOp(peek().location, left, 'or', right)

        return left
    
    def parse_statement() -> ast.Variable | ast.Expression:
        if peek().text == 'var':
            return parse_variable_declaration()
        elif peek().text == "while":
            return parse_while_loops()
        else:
            return parse_expression()
        
    def parse_type():
        token = consume()
        if token.text == 'Int':
            return Int()
        elif token.text == 'Bool':
            return Bool()
        elif token.text == 'Unit':
            return Unit()
        else:
            raise SyntaxError(f"Unexpected token {token.text} at position {token.location}")

    def parse_variable_declaration() -> ast.Variable:
        consume('var')
        identifier = parse_identifier()
        if peek().text == ":":
            consume(":")
            type = parse_type()
            consume('=')
            value = parse_expression()
            return ast.Variable(location=peek().location, name=identifier, value=value, type=type)
        else:
            consume("=")
            value = parse_expression()
            return ast.Variable(location=peek().location, name=identifier, value=value)
        
    def parse_expression() -> ast.Expression:
        if peek().text == '{':
            return parse_blocks()
        else:
            left = parse_logical_or_expression()
            if peek().text == '=':
                operator_token = consume('=')
                right = parse_expression()
                left = ast.Assignment(peek().location, left, operator_token, right)

        return left

    def parse_blocks() -> ast.Block:
        expressions = []
        consume('{')

        while peek().text != '}':
            statement = parse_statement()
            expressions.append(statement)

            if peek().text == ';':
                consume(';')


        consume('}')
        if peek().text == ';':
            expressions.append(ast.Literal(peek().location, value=None))

        return ast.Block(peek().location, expressions)
    
    return parse_expression()