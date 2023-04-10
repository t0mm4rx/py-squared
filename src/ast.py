"""Handle everything related to the abstract syntax tree."""
from __future__ import annotations
from typing import Tuple
from enum import Enum, auto
from .tokenization import Token, TokenTypes

class NodeTypes(Enum):
    """All different node types."""
    ENTRYPOINT      = auto() # root of the program, every children will be sequentially called
    FUNCTION_CALL   = auto() # print() method
    INT_EXPR        = auto() # Plain int, ex: "42"

class Node:
    """AST node."""

    def __init__(
            self,
            parent_node: Node | None,
            node_type: Node,
            value: str | None,
        ) -> None:
        self.node_type: NodeTypes   = node_type
        self.parent_node: Node      = parent_node
        self.children: list[Node]   = []
        self.value: str | None      = value

class InvalidStatement(Exception):
    """The current statement/expression is not recognized."""

def match_pattern(
        tokens: list[Token],
    ) -> Tuple[
        NodeTypes,    # Node type
        list[Token],  # Children
        int,          # Number of tokens used by the node
        str | None,   # Value of the node, may be None
    ]:
    """Match the statement pattern from given tokens."""
    token_types = [ token.token_type for token in tokens ]
    match token_types:


        # function call
        case [
            TokenTypes.STR_LITERAL,
            TokenTypes.OPEN_PARENTHESIS,
            argument,
            TokenTypes.CLOSE_PARENTHESIS,
            *_,
            ]:
            return NodeTypes.FUNCTION_CALL, tokens[2:3], 4, tokens[0].value

        # int expr
        case [
            TokenTypes.INT_LITERAL,
            *_,
            ]:
            return NodeTypes.INT_EXPR, [], 1, tokens[0].value

        case _:
            raise InvalidStatement()

def tokens_to_ast(tokens: list[Token], parent_node: Node | None = None) -> Node:
    """Transform a list of tokens into an AST."""
    cursor = 0

    if parent_node is None:
        parent_node = Node(None, NodeTypes.ENTRYPOINT, None)

    while cursor < len(tokens):

        node_type, children, to_skip, value = match_pattern(tokens[cursor:])

        new_node = Node(
            parent_node=parent_node,
            node_type=node_type,
            value=value,
        )
        tokens_to_ast(children, parent_node=new_node)

        parent_node.children.append(new_node)

        cursor += to_skip

    return parent_node

def print_ast(node: Node, level: int = 0) -> None:
    """Recurcively print the AST."""
    print("   " * level, end="")
    print(node.node_type, end=" ")
    if node.value is not None:
        print(f"({node.value})", end="")
    print()
    for child in node.children:
        print_ast(child, level=level + 1)
