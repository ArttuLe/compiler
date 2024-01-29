
from compiler import tokenizer
from compiler.ast import BinaryOp, Literal
from compiler.parser import parse

def test_parser_simple() -> None:
    tokens = [tokenizer.Token(type="int_literal", text=1, location=(1, 1)),
              tokenizer.Token(type="identifier", text="+", location=(1, 1)),
              tokenizer.Token(type="int_literal", text=2, location=(1, 1))]
    parsed = parse(tokens)

    assert(parsed == BinaryOp(left=Literal(value=1), op='+', right=Literal(value=2)))