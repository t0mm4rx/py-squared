"""Functions to compile the AST into C code."""
import os
from .ast import NodeTypes, Node

def compile_ast(node: Node) -> str:
    """Compile the AST into a C file."""
    with open("./lib_c/main.c", "r", encoding="utf-8") as file:
        main = file.read()
        injection = ""
        for child in node.children:
            injection += compile_node(child)
        main = main.replace("// %%main", injection)
        return main

def compile_c_output(c_source: str, binary_name: str):
    """Compile the given C source code into a binary."""
    os.system("mkdir -p build")
    with open("./build/output.c", "w+", encoding="utf-8") as file:
        file.write(c_source)
    os.system(f"gcc ./build/output.c -o ./build/{binary_name}")

def compile_node(node: Node) -> str:
    """Compile the given node."""
    if node.node_type == NodeTypes.ENTRYPOINT:
        return ""
    return node_compilers[node.node_type](node)

def compile_function_call(node: Node) -> str:
    """Compile NodeTypes.FUNCTION_CALL."""
    return f"{node.value}({','.join([compile_node(child) for child in node.children])});"

def compile_int_expr(node: Node) -> str:
    """Compile NodeTypes.INT_EXPR."""
    return node.value

node_compilers: dict[str, NodeTypes] = {
    NodeTypes.FUNCTION_CALL:    compile_function_call,
    NodeTypes.INT_EXPR:         compile_int_expr,
}
