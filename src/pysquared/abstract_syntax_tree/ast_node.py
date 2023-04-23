"""A single node of the AST."""
from __future__ import annotations
from pysquared import Token

class NotImplementedInNodeSubclass(Exception):
    """Raised when a node implementaion lacks called method."""

class ASTNode:
    """A single node of the AST."""

    def __init__(self, parent_node: ASTNode | None = None) -> None:
        self.children: list[ASTNode] = []
        self.parent_node: ASTNode | None = parent_node

    @staticmethod
    def match(tokens: list[Token], parent_node: ASTNode | None) -> tuple[ASTNode, int] | None:
        """
        Returns a new instance of the node and the number of tokens to skip, if it
        matches the tokens.

        Examples:
        INTExprNode.match([Token(TokenTypes.INT_LITERAL)]) -> INTExprNode(tokens)
        INTExprNode.match([Token(TokenTypes.OPEN_PARENTHESIS), ...]) -> None
        """
        raise NotImplementedInNodeSubclass()

    def compile(self) -> str:
        """Returns a C source code string generated from the node."""
        raise NotImplementedInNodeSubclass()

    def print_tree(self, depth: int = 0):
        """Print the current node and children."""
        print("   " * depth, end="")
        print(self.__class__.__name__)
        for child in self.children:
            child.print_tree(depth=depth + 1)
