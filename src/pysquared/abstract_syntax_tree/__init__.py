"""
AST module.

The AST is an abstract data structure of our code.
It's made of ASTNodes.
Each ASTNode can have children, in a recursive manner.
"""
from .ast_node import ASTNode
from .entrypoint_node import Entrypoint
from .function_call import FunctionCall
from .int_expr import INTExpr
from .variable_declaration import VariableDeclaration
from .variable_reference import VariableReference
from .helper_functions import *

ALL_NODE_TYPES: list[ASTNode] = [
    Entrypoint,
    FunctionCall,
    INTExpr,
    VariableDeclaration,
    VariableReference,
]
