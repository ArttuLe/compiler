from dataclasses import dataclass, field

from compiler.types import Type, Unit

@dataclass
class Expression:
    """Base class for AST nodes representing expressions."""
    location: tuple[str]
    type: Type = field(kw_only=True,default_factory=lambda: Unit())

@dataclass
class Literal(Expression):
    value: int | bool | None
    # (value=None is used when parsing the keyword `unit`)

@dataclass
class Identifier(Expression):
    name: str

@dataclass
class ControlFlow(Expression):
    if_exp: Expression
    else_exp: str
    then_exp: Expression | None

@dataclass
class Function(Expression):
    identifier: Identifier
    args: list

@dataclass
class BinaryOp(Expression):
    left: Expression
    op: str
    right: Expression

@dataclass
class Assignment(Expression):
    name: str
    op_token: str
    value: int | str

@dataclass
class WhileLoop(Expression):
    while_expr: Expression
    do_expr: Expression

@dataclass
class UnaryOp(Expression):
    operator: str
    operand: Expression

@dataclass
class Block(Expression):
    expressions: list

@dataclass
class Variable(Expression):
    name: Identifier
    value: str
