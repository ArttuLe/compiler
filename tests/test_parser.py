import pytest

from compiler import tokenizer
from compiler.ast import BinaryOp, Literal
from compiler.parser import parse


def test_parser_simple() -> None:
    tokens = [tokenizer.Token(type="int_literal", text=1, location=(1, 1)),
              tokenizer.Token(type="identifier", text="+", location=(1, 1)),
              tokenizer.Token(type="int_literal", text=2, location=(1, 1))]
    parsed = parse(tokens)

    assert(parsed == BinaryOp(left=Literal(value=1), op='+', right=Literal(value=2)))

def test_empty_input() -> None:
    tokens = []

    with pytest.raises(ValueError, match="Empty Token"):
        parse(tokens)

def test_broken_tokens() -> None:
    tokens = [tokenizer.Token(type="identifier", text="a", location=(1, 1)),
              tokenizer.Token(type="identifier", text="+", location=(1, 1)),
              tokenizer.Token(type="identifier", text="b", location=(1, 1)),
              tokenizer.Token(type="identifier", text="c", location=(1,1))]
    with pytest.raises(ValueError, match="Couldn't parse the whole expression"):
        parse(tokens)

def test_with_clauses() -> None:
    tokens = [tokenizer.Token(type="Punctuation", text="(", location=(1, 1)),
              tokenizer.Token(type="identifier", text="a", location=(1, 1)),
              tokenizer.Token(type="identifier", text="+", location=(1, 1)),
              tokenizer.Token(type="identifier", text="b", location=(1,1)),
              tokenizer.Token(type="Punctuation", text=")", location=(1,1)),
              tokenizer.Token(type="identifier", text="*", location=(1, 1)),
              tokenizer.Token(type="identifier", text="c", location=(1,1))]
    
