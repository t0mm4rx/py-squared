"""
Tokenization related methods.

Tokenization is the process of converting raw source code into a list of tokens.
"""
from enum import Enum, auto
from dataclasses import dataclass

class TokenTypes(Enum):
    """All different token types."""
    OPEN_PARENTHESIS    = auto()
    CLOSE_PARENTHESIS   = auto()
    STR_LITERAL         = auto()
    INT_LITERAL         = auto()

@dataclass
class Token:
    """Token data structure."""
    token_type:    TokenTypes
    value:         str | None
    line_position: int
    row_position:  int

text_to_tokens: dict[str, TokenTypes] = {
    "(": TokenTypes.OPEN_PARENTHESIS,
    ")": TokenTypes.CLOSE_PARENTHESIS,
}

def starts_with_token(code: str) -> TokenTypes | None:
    """
    Return the token type the given code is starting with.

    Examples:
        - starts_with_token("print(42)") -> None
        - starts_with_token("(42)") -> TokenTypes.OPEN_PARENTHESIS
        - starts_with_token(")") -> TokenTypes.CLOSE_PARENTHESIS
    """
    for value, token_type in text_to_tokens.items():
        if code.startswith(value):
            return token_type
    return None

def get_literal_token_type(literal: str) -> TokenTypes:
    """Get the TokenTypes corresponding to the given literal."""
    if literal.isnumeric():
        return TokenTypes.INT_LITERAL
    return TokenTypes.STR_LITERAL

def tokenize(source_code: str) -> list[Token]:
    """Convert the given source code into an array of tokens."""
    tokens: list[Token] = []
    lines = source_code.split("\n")
    for liner_number, line in enumerate(lines):
        literal_buffer  = ""
        cursor          = 0

        while cursor < len(line):

            token_type = starts_with_token(line[cursor:])

            if token_type:
                if len(literal_buffer) > 0:
                    tokens.append(Token(
                        token_type=get_literal_token_type(literal_buffer),
                        value=literal_buffer,
                        line_position=liner_number,
                        row_position=cursor,
                    ))
                    literal_buffer = ""
                tokens.append(Token(
                    token_type=token_type,
                    value=None,
                    line_position=liner_number,
                    row_position=cursor,
                ))
            else:
                literal_buffer += line[cursor]

            cursor += 1

        if len(literal_buffer) > 0:
            tokens.append(Token(
                token_type=get_literal_token_type(literal_buffer),
                value=literal_buffer,
                line_position=liner_number,
                row_position=cursor,
            ))

    return tokens
