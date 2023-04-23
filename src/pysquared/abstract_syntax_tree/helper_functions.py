"""Helper functions to parse and build the AST."""
from pysquared import Token, TokenTypes

def get_token_type(tokens: list[Token], index: int) -> TokenTypes | None:
    """
    Get the token type at the given list index.
    If no token is found at the index, return None.
    """
    if index >= len(tokens):
        return None
    return tokens[index].token_type
