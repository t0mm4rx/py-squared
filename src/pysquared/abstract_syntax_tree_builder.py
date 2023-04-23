"""Handle everything related to the abstract syntax tree."""
from __future__ import annotations
from typing import Tuple
from pysquared import Token, TokenTypes
from .abstract_syntax_tree import ASTNode, ALL_NODE_TYPES, Entrypoint
from .abstract_syntax_tree import get_token_type

class InvalidStatement(Exception):
    """The current statement/expression is not recognized."""

def match_node(
        parent_node: ASTNode,
        tokens: list[Token],
    ) -> Tuple[ASTNode | None, int]:
    """Match the statement pattern from given tokens."""
    if get_token_type(tokens, 0) == TokenTypes.BREAK_LINE:
        return None, 1

    for node_type in ALL_NODE_TYPES:
        result = node_type.match(tokens, parent_node)
        if result:
            return result
    raise InvalidStatement()

def tokens_to_ast(tokens: list[Token], parent_node: ASTNode | None = None) -> ASTNode:
    """Transform a list of tokens into an AST."""
    cursor = 0

    if parent_node is None:
        parent_node = Entrypoint()

    while cursor < len(tokens):
        print(cursor, tokens[cursor])
        new_node, to_skip = match_node(parent_node, tokens[cursor:])
        if new_node is not None:
            parent_node.children.append(new_node)
        cursor += to_skip

    return parent_node
