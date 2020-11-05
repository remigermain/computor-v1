#!/usr/bin/python3

from src.utils import MAX_DEGRES, DEFAULT_INDEFINITE
from src.parser import Parser
from src.resolver import Resolver
import argparse
import sys
import string


def parse_line(args, eq):
    parser = Parser(eq, indefinite=args.define_indefinite)
    obj = {
        'have_error': False
    }
    if parser.is_valid():
        data = parser.validated_data
        resolver = Resolver(
            data,
            verbose=args.verbose,
            no_print=args.minimal,
            indefinite=args.define_indefinite
        )
        if resolver.is_valid():
            obj['resolve'] = resolver
        else:
            obj['errors'] = resolver.get_errors()
            obj['have_error'] = True
    else:
        obj['errors'] = parser.get_errors()
        obj['have_error'] = True
    return obj


def validate_indefinite(value):
    if not value.isalpha() or len(value) != 1:
        raise argparse.ArgumentTypeError(
            f"you can only set one char, not \"{value}\"."
        )
    return value


def print_results(args, results):
    new_line = False
    for r in results:
        if new_line:
            print("\n")
        if r['have_error']:
            r['errors'].print_error()
        else:
            resolver = r['resolve']
            result = resolver.resolve()
            if args.minimal:
                result = result if isinstance(result, list) else [result]
                for r in result:
                    print(r)
        new_line = True


def from_stdin(args):
    new_line = False
    while True:
        if new_line:
            print("")
        try:
            line = input("enter your equation (or tape \"exit\" to quit):  ")
            if line.lower().strip() == "exit":
                exit(1)
        except (KeyboardInterrupt, EOFError, UnboundLocalError):
            print("exit program ...")
            exit(-1)
        print_results(args, [parse_line(args, line)])
        new_line = True


def from_args(args):
    results = [parse_line(args, eq) for eq in args.equations]
    print_results(args, results)


def main():

    _argparse = argparse.ArgumentParser(
        description=f"solves a polynomial equation of lower or equal degree {MAX_DEGRES}."
    )
    _argparse.add_argument(
        "-v",
        "--verbose",
        help="display more information during parsing and resolve.",
        action="store_true",
        default=False
    )
    _argparse.add_argument(
        "-m",
        "--minimal",
        help="display only result (disabled verboser flag).",
        action="store_true",
        default=False
    )
    _argparse.add_argument(
        "-d",
        "--define-indefinite",
        help=f"change the indefinite letter, default \"{DEFAULT_INDEFINITE}\" (insensitive case).",
        type=str,
        choices=list(string.ascii_lowercase),
        default=DEFAULT_INDEFINITE
    )
    _argparse.add_argument('equations', nargs='*')
    args = _argparse.parse_args(sys.argv[1:])

    # check have one equation in args
    if not len(args.equations):
        from_stdin(args)
    else:
        from_args(args)


if __name__ == "__main__":
    main()
