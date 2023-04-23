"""
Entrypoint of the package.
Run `python3 -m pysquared` to execute this code.
"""
from argparse import ArgumentParser
from pysquared.tokenization import tokenize
from pysquared.abstract_syntax_tree_builder import tokens_to_ast
from pysquared.compilation import compile_ast, compile_c_output

parser = ArgumentParser(prog="Pysquared compiler")
subparsers = parser.add_subparsers(title="commands", dest="command")

# Compile command
compile_parser = subparsers.add_parser(
    "compile",
    help="Compile the given Pysquared sript into a binary"
)
compile_parser.add_argument(
    "filename", help="The path of the .py file to compile",
)
compile_parser.add_argument(
    "--memory-leak-check",
    help="Do we compile with fsanitize?",
    action='store_true',
    default=False,
)
compile_parser.add_argument(
    "--output", help="The name of the output binary",
)

def main():
    """Run the compilation."""
    args = parser.parse_args()
    print(args)
    with open(args.filename, "r", encoding="utf-8") as file:
        tokens = tokenize(file.read())
        ast = tokens_to_ast(tokens)
        ast.print_tree()
        output_file = args.filename.replace(".py", "")
        if args.output:
            output_file = args.output
        compile_c_output(compile_ast(ast), output_file, args.memory_leak_check)

if __name__ == "__main__":
    main()
