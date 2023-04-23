"""int expression node."""
from pysquared import Token, TokenTypes
from .ast_node import ASTNode
from .helper_functions import get_token_type

class INTExpr(ASTNode):
    """
    int expression.

    Examples: "42", "12", "0"...
    """

    def __init__(self, value: str, parent_node: ASTNode | None = None) -> None:
        self.value = value
        super().__init__(parent_node)

    @staticmethod
    def match(tokens: list[Token], parent_node: ASTNode | None) -> ASTNode | None:
        if get_token_type(tokens, 0) == TokenTypes.INT_LITERAL:
            return (INTExpr(
                value=tokens[0].value,
                parent_node=parent_node
            ), 1)
        return None

    def compile(self) -> str:
        return self.value
