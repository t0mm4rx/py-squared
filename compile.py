"""Compile the given file with given options."""
from argparse import ArgumentParser
# from pysquared. import tokenize, tokens_to_ast, compile_ast, compile_c_output
from pysquared.tokenization import tokenize
from pysquared.abstract_syntax_tree_builder import tokens_to_ast
from pysquared.compilation import compile_ast, compile_c_output

parser = ArgumentParser(prog="Py-squared compiler")
parser.add_argument("filename")

def main():
    """Run the compilation."""
    args = parser.parse_args()
    with open(args.filename, "r", encoding="utf-8") as file:
        tokens = tokenize(file.read())
        ast = tokens_to_ast(tokens)
        ast.print_tree()

        compile_c_output(compile_ast(ast), "print")

if __name__ == "__main__":
    main()
