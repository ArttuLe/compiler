import unittest

from compiler.tokenizer import Tokenizer, Token



def test_tokenize_simple() -> None:
    values = Tokenizer.tokenize("if 3\nwhile")
    assert get_tokenlist(values) == ['if', '3', 'while']

def test_operators() -> None:
    values = Tokenizer.tokenize("if 3 < 10\n")
    assert get_tokenlist(values) == ['if', '3', '<', '10']

def test_with_punctuation() -> None:
    values = Tokenizer.tokenize("if 3 < 10;")
    assert get_tokenlist(values) == ['if', '3', '<', '10', ';']

def test_with_comments() -> None:
    values = Tokenizer.tokenize("if 3 < while\n# aaaa\n//      asd")
    assert get_tokenlist(values) == ['if', '3', '<', 'while']

def get_tokenlist(obj_list):
       return [token.text for token in obj_list]