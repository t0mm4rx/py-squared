"""Function call node."""
from pysquared import Token, TokenTypes
import pysquared.abstract_syntax_tree_builder as ast_builder
from .ast_node import ASTNode
from .helper_functions import get_token_type

class FunctionCall(ASTNode):
    """
    Function call node.

    Function calls have a function name, and children representing arguments.
    """

    def __init__(self, function_name: str, parent_node: ASTNode | None = None) -> None:
        self.function_name: str = function_name
        super().__init__(parent_node)

    @staticmethod
    def match(tokens: list[Token], parent_node: ASTNode | None) -> ASTNode | None:
        if get_token_type(tokens, 0) != TokenTypes.STR_LITERAL:
            return None
        if get_token_type(tokens, 1) != TokenTypes.OPEN_PARENTHESIS:
            return None
        cursor = 2
        children: list[Token] = []
        while get_token_type(tokens, cursor) != TokenTypes.CLOSE_PARENTHESIS:
            if cursor > len(tokens):
                return None
            children.append(tokens[cursor])
            cursor += 1
        new_node = FunctionCall(
            function_name=tokens[0].value,
            parent_node=parent_node,
        )
        ast_builder.tokens_to_ast(children, new_node)
        return (new_node, cursor + 1)

    def compile(self) -> str:
        return f"{self.function_name}({','.join([child.compile() for child in self.children])});"
