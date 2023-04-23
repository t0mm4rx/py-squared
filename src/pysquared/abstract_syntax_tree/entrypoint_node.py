"""Entrypoint AST node."""
from pysquared import Token
from .ast_node import ASTNode

class Entrypoint(ASTNode):
    """
    Entrypoint node. It's just a container for other nodes.
    This is the program's root.
    """

    def __init__(self) -> None:
        super().__init__(None)

    @staticmethod
    def match(tokens: list[Token], parent_node: ASTNode | None) -> ASTNode | None:
        return None

    def compile(self) -> str:
        source_code: str = ""
        for child in self.children:
            source_code += child.compile()
        return source_code
