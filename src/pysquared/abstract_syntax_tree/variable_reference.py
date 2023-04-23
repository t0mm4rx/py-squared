"""Variable reference."""
from pysquared import Token, TokenTypes
from pysquared.memory import get_variable
from .ast_node import ASTNode
from .helper_functions import get_token_type

class VariableReference(ASTNode):
    """
    Variable reference.

    Examples: "a".
    """

    def __init__(self, variable_name: str, parent_node: ASTNode | None = None) -> None:
        self.variable_name = variable_name
        super().__init__(parent_node)

    @staticmethod
    def match(tokens: list[Token], parent_node: ASTNode | None) -> tuple[ASTNode, int] | None:
        if get_token_type(tokens, 0) == TokenTypes.STR_LITERAL:
            return VariableReference(
                variable_name=tokens[0].value,
                parent_node=parent_node,
            ), 1
        return None

    def compile(self) -> str:
        variable = get_variable(name=self.variable_name)
        return f"*(({variable.type}*)memory_slots[{variable.index}])"
