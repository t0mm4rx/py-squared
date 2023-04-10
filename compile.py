"""Compile the given file with given options."""
from argparse import ArgumentParser
from src.tokenization import tokenize
from src.ast import tokens_to_ast, print_ast
from src.compilation import compile_ast, compile_c_output

parser = ArgumentParser(prog="Py-squared compiler")
parser.add_argument("filename")

def main():
    """Run the compilation."""
    args = parser.parse_args()
    with open(args.filename, "r", encoding="utf-8") as file:
        tokens = tokenize(file.read())
        ast = tokens_to_ast(tokens)
        print_ast(ast)

        compile_c_output(compile_ast(ast), "print")

if __name__ == "__main__":
    main()
