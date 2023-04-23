"""Function declaration node."""
from pysquared import Token, PRIMITIVE_TYPES, TokenTypes
import pysquared.abstract_syntax_tree_builder as ast_builder
from pysquared.memory import register_variable
from .helper_functions import get_token_type
from .ast_node import ASTNode

class TypeUnknown(Exception):
    """Raised when the given type is not known."""

class VariableDeclaration(ASTNode):
    """
    Variable declaration node.

    Example:
    - "a: int64 = 42"
    - "xyz: abc = abc(...)"
    - "abc: int64 = 42 * squared(4)"
    """

    def __init__(
            self,
            variable_name: str,
            variable_type: str,
            parent_node: ASTNode | None = None) -> None:
        self.variable_name = variable_name
        self.variable_type = variable_type
        super().__init__(parent_node)

    @staticmethod
    def match(tokens: list[Token], parent_node: ASTNode | None) -> tuple[ASTNode, int] | None:
        if get_token_type(tokens, 0) != TokenTypes.STR_LITERAL:
            return None
        if get_token_type(tokens, 1) != TokenTypes.COLON:
            return None
        if get_token_type(tokens, 2) != TokenTypes.STR_LITERAL:
            return None
        if get_token_type(tokens, 3) != TokenTypes.EQUAL:
            return None
        children: list[Token] = []
        cursor = 4
        while get_token_type(tokens, cursor) != TokenTypes.BREAK_LINE:
            if cursor >= len(tokens):
                return None
            children.append(tokens[cursor])
            cursor += 1
        new_node = VariableDeclaration(
            variable_name=tokens[0].value,
            variable_type=tokens[2].value,
            parent_node=parent_node,
        )
        ast_builder.tokens_to_ast(children, new_node)
        return new_node, cursor

    def compile(self) -> str:
        if self.variable_type in PRIMITIVE_TYPES:
            c_type = PRIMITIVE_TYPES[self.variable_type]
            new_index = register_variable(self.variable_name, c_type.type_c_name)
            return f"""
            reserve_slot({new_index}, {c_type.type_size});
            *(({c_type.type_c_name}*)memory_slots[{new_index}]) = {self.children[0].compile()};
            """
        raise TypeUnknown()
