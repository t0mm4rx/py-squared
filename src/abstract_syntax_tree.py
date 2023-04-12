"""Handle everything related to the abstract syntax tree."""
from __future__ import annotations
from typing import Tuple
from enum import Enum, auto
from .tokenization import Token, TokenTypes

class NodeTypes(Enum):
    """All different node types."""
    ENTRYPOINT           = auto() # root of the program, every children will be sequentially called
    FUNCTION_CALL        = auto() # print() method
    INT_EXPR             = auto() # Plain int, ex: "42"
    VARIABLE_DECLARATION = auto() # Declaration of int variable, ex: "a: int = 42"
    VARIABLE_REFERENCE   = auto() # Reference of a variable, ex: "a"

class Node:
    """AST node."""

    def __init__(
            self,
            parent_node: Node | None,
            node_type: Node,
            value: str | None,
            variable_type: str | None = None,
        ) -> None:
        self.node_type: NodeTypes       = node_type
        self.parent_node: Node          = parent_node
        self.children: list[Node]       = []
        self.value: str | None          = value
        self.variable_type: str | None  = variable_type

class InvalidStatement(Exception):
    """The current statement/expression is not recognized."""

def match_pattern(
        parent_node: Node,
        tokens: list[Token],
    ) -> Tuple[Node | None, int]:
    """Match the statement pattern from given tokens."""
    token_types = [ token.token_type for token in tokens ]

    match token_types:

        # skip whitespaces
        case [
            TokenTypes.BREAK_LINE,
            *_,
        ]:
            return None, 1

        # function call
        case [
            TokenTypes.STR_LITERAL,
            TokenTypes.OPEN_PARENTHESIS,
            argument,
            TokenTypes.CLOSE_PARENTHESIS,
            *_,
            ]:
            new_node = Node(
                parent_node=parent_node,
                node_type=NodeTypes.FUNCTION_CALL,
                value=tokens[0].value,
            )
            tokens_to_ast(tokens[2:3], new_node)
            return new_node, 4

        # int expr
        case [
            TokenTypes.INT_LITERAL,
            *_,
            ]:
            return Node(
                parent_node=parent_node,
                node_type=NodeTypes.INT_EXPR,
                value=tokens[0].value,
            ), 1

        # variable declaration
        case [
            TokenTypes.STR_LITERAL,
            TokenTypes.COLON,
            TokenTypes.STR_LITERAL,
            TokenTypes.EQUAL,
            TokenTypes.INT_LITERAL,
            TokenTypes.BREAK_LINE,
            *_,
            ]:
            # return NodeTypes.VARIABLE_DECLARATION, tokens[4:5], 6, tokens[0].value
            new_node = Node(
                parent_node=parent_node,
                node_type=NodeTypes.VARIABLE_DECLARATION,
                value=tokens[0].value,
                variable_type=tokens[2].value,
            )
            tokens_to_ast(tokens[4:5], new_node)
            return new_node, 6

        case [TokenTypes.STR_LITERAL, *_]:
            return Node(
                parent_node=parent_node,
                node_type=NodeTypes.VARIABLE_REFERENCE,
                value=tokens[0].value,
            ), 1

        case _:
            raise InvalidStatement()

def tokens_to_ast(tokens: list[Token], parent_node: Node | None = None) -> Node:
    """Transform a list of tokens into an AST."""
    cursor = 0

    if parent_node is None:
        parent_node = Node(None, NodeTypes.ENTRYPOINT, None)

    while cursor < len(tokens):
        print(cursor, tokens[cursor])
        new_node, to_skip = match_pattern(parent_node, tokens[cursor:])
        if new_node is not None:
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
