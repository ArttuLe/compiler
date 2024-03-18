import re

from dataclasses import dataclass

@dataclass
class Token():
    type: str
    text: str
    location: tuple[str]


    def __eq__(self, location: object) -> bool:
        return self.location == location

class Tokenizer():
    """
    Class implementing the tokenizer functionalities
    Includes main logic and hepler functions 
    """

    @staticmethod
    def tokenize(source_code: str) -> list[Token]:
        tokens: list[str] = []

        keywords = {'if', 'else', 'while', 'print', 'then'}
        token_specification = [
            ('identifier',       r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
            ('int_literal', r'\b\d+\b'),
            ('NEWLINE',  r'\\n'),           
            ('SKIP',     r'[ \t]+'),
            ('Comment', r'#\s?.*|//.*'),
            ('Operator', r'==|!=|<=|>=|\+|-|\*|/|=|<|>|%'),
            ('Punctuation', r'[(),:,{};]'),
            ('MISMATCH', r'.'),            
        ]
        token_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        line_num = 1
        line_start = 0
        for match_obj in re.finditer(token_regex, source_code):
            kind = match_obj.lastgroup
            value = match_obj.group()
            column = match_obj.start() - line_start
            if kind == 'identifier' and value in keywords:
                kind = value
            elif kind == 'NEWLINE':
                line_start = match_obj.end()
                line_num += 1
                continue
            elif kind == 'SKIP' or kind == 'Comment':
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f'{value!r} unexpected on line {line_num}')
            tokens.append(Token(type=kind, text=value, location=(line_num, column)))
        
        return tokens


if __name__ == "__main__":
    Tokenizer.tokenize("if 3 < while\n# aaaa\n// asd")