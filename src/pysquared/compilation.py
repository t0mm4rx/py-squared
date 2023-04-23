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

def compile_c_output(c_source: str, binary_name: str, fsanitize: bool = False):
    """Compile the given C source code into a binary."""
    os.system("mkdir -p build")
    c_file_name = binary_name + ".c"
    with open(c_file_name, "w+", encoding="utf-8") as file:
        file.write(c_source)
    print((f"gcc {c_file_name} -o {binary_name}"
           " -Wall -Werror -Wextra "
           f"{'-g3 -fsanitize=address' if fsanitize else ''}"
        ))
    os.system(f"gcc {c_file_name} -o {binary_name} {'-g3 -fsanitize=address' if fsanitize else ''}")
