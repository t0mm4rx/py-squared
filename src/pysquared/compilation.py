"""Functions to compile the AST into C code."""
import os
from pysquared.abstract_syntax_tree import ASTNode
# from .memory import register_variable, get_variable

class NoCompilerImplemented(Exception):
    """Raised when no compile is defined yet."""

def compile_ast(node: ASTNode) -> str:
    """Compile the AST into a C file."""
    with open("./lib_c/main.c", "r", encoding="utf-8") as file:
        main = file.read()
        main = main.replace("// %%main", node.compile())
        return main

def compile_c_output(c_source: str, binary_name: str):
    """Compile the given C source code into a binary."""
    os.system("mkdir -p build")
    with open("./build/output.c", "w+", encoding="utf-8") as file:
        file.write(c_source)
    os.system(f"gcc ./build/output.c -o ./build/{binary_name} -g3 -fsanitize=address")

# def compile_variable_declaration(node: Node) -> str:
#     """Compile NodeTypes.VARIABLE_DECLARATION."""
#     if node.variable_type == "int":
#         new_index = register_variable(node.value, node.variable_type)
#         return f"""
#         reserve_slot({new_index}, 8);
#         *((int*)memory_slots[{new_index}]) = {compile_node(node.children[0])};
#         """
#     raise NoCompilerImplemented()

# def compile_variable_reference(node: Node) -> str:
#     """Compile NodeTypes.VARIABLE_REFERENCE."""
#     variable = get_variable(name=node.value)
#     return f"*(({variable.type}*)memory_slots[{variable.index}])"
