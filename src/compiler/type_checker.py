import compiler.ast as ast
from compiler.types import Bool, Int, SymTab, Type, Unit

def typecheck(node: ast.Expression, symbol_table = SymTab()) -> Type:
    match node:
        case ast.Literal():
            if isinstance(node.value, int):
                return Int()
            elif isinstance(node.value, bool):
                return Bool()
            elif node.value is None:
                return Unit()
            else:
                raise ValueError(f"unknown literal type at {node.location}")
        case ast.Identifier():
            return symbol_table.lookup(node.name)
        
        case ast.BinaryOp():
            if node.op in ['+', '-', '*', '/', '%']:
                t1 = typecheck(node.left, symbol_table)
                t2 = typecheck(node.right, symbol_table)
                if t1 != Int() or t2 != Int():
                    raise ValueError(f"operands of binary operator '{node.op}' must be of type Int at {node.location}")
                return Int()
            elif node.op in ['==', '!=']:
                t1 = typecheck(node.left, symbol_table)
                t2 = typecheck(node.right, symbol_table)
                if t1 != t2:
                    raise ValueError(f"type mismatch in comparison for operator '{node.op}' at {node.location}")
                return Bool()
            elif node.op in ['==', '!=', '<', '<=', '>', '>=']:
                t1 = typecheck(node.left, symbol_table)
                t2 = typecheck(node.right, symbol_table)
                if t1 != t2:
                    raise ValueError(f"type mismatch in comparison for operator '{node.op}' at {node.location}")
                return Bool()
            else:
                raise ValueError(f"unknown binary operator '{node.op}' at {node.location}")

        case Type():
            if node == Int():
                return Int()
            elif node == Bool():
                return Bool()
            elif node == Unit():
                return Unit()

        case ast.Variable():
            if node.type is not None:
                # Check the type if present
                initializer_type = typecheck(node.type, symbol_table)
                if initializer_type != node.type:
                    raise ValueError(f"type mismatch in types {initializer_type} and {node.type}")
                node.type = initializer_type
                symbol_table.define(node.name.name, node.type)
            value_type = typecheck(node.value, symbol_table)
            symbol_table.define(node.name.name, value_type)
            return value_type
        
        case ast.Assignment():
            variable_type = symbol_table.lookup(node.name.name)
            value_type = typecheck(node.value, symbol_table)
            if variable_type != value_type:
                raise ValueError(f"type mismatch in assignment for variable '{node.name.name}' at {node.location}")
            return variable_type
        
        case ast.ControlFlow():
            t1 = typecheck(node.if_exp)
            if t1 is not Bool:
                raise ...
            t2 = typecheck(node.then_exp)
            t3 = typecheck(node.else_exp)
            if t2 != t3:
                raise ValueError("mismatch in types at {node.location}")
            return t2
        
        case ast.UnaryOp():
            if node.op == '-':
                operand_type = typecheck(node.operand, symbol_table)
                if operand_type != Int():
                    raise ValueError(f"operand of unary '-' must be of type Int at {node.location}")
                return Int()
            else:
                raise ValueError(f"unknown unary operator '{node.op}' at {node.location}")

        case ast.Function():
            func_signature = symbol_table.lookup(node.identifier.name)

            if len(node.args) != len(func_signature.param_types):
                raise ValueError(f"incorrect number of arguments for function '{node.identifier}' at {node.location}")

            for arg, param_type in zip(node.args, func_signature.param_types):
                arg_type = typecheck(arg, symbol_table)
                if arg_type != param_type:
                    raise ValueError(f"type mismatch in argument for function '{node.identifier}' at {node.location}")
            return func_signature.return_type

        case ast.Block():
            block_symbol_table = SymTab(parent=symbol_table)

            for expr in node.expressions:
                typecheck(expr)
            if node.expressions:
                return typecheck(node.expressions[-1], block_symbol_table)
            else:
                return Unit()

        case ast.ControlFlow():
            t1 = typecheck(node.if_exp, symbol_table)
            if t1 != Bool():
                raise ValueError(f"condition expression must be of type Bool at {node.location}")
            t2 = typecheck(node.then_exp, symbol_table)
            t3 = typecheck(node.else_exp, symbol_table)
            if t2 != t3:
                raise ValueError(f"mismatch in types of 'then' and 'else' expressions at {node.location}")
            return t2

        case ast.WhileLoop():
            t1 = typecheck(node.while_expr, symbol_table)
            if t1 != Bool():
                raise ValueError(f"condition expression must be of type Bool at {node.location}")
            typecheck(node.do_expr, symbol_table)
            return Unit()     