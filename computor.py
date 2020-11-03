#!/bin/python3

from src.utils import MAX_DEGRES, print_results, DEFAULT_INDEFINITE
from src.parser import Parser
from src.resolver import Resolver
import argparse
import sys


def parse_line(args, eq, idx=-1):
    parser = Parser(eq, indefinite=args.define_indefinite)
    obj = {'idx': idx, 'have_error': False}
    if parser.is_valid():
        data = parser.validated_data
        obj['resolve'] = Resolver(data, verbose=args.verbose)
    else:
        obj['parser'] = parser
        obj['have_error'] = True
    return obj


def validate_indefinite(value):
    if not value.isalpha() or len(value) != 1:
        raise ValueError(f"you can only set one char, not {value}")
    return value


def from_stdin(args):
    results = []
    try:
        line = input()
    except KeyboardInterrupt:
        print("exit program ...")
        exit(-1)
    results.append(parse_line(args, line))
    print_results(results)


def from_args(args):
    results = []
    for idx, eq in enumerate(args.equations):
        results.append(parse_line(args, eq, idx=idx))
    print_results(results)


def main():
    _argparse = argparse.ArgumentParser(
        "computor",
        "computor v1: [falgs] equations...",
        f"solves a polynomial equation of lower or equal degree {MAX_DEGRES}"
    )
    _argparse.add_argument(
        "-v", "--verbose", action="store_true", default=False)
    _argparse.add_argument(
        "-d",
        "--define-indefinite",
        type=validate_indefinite,
        action="store",
        default=DEFAULT_INDEFINITE
    )
    _argparse.add_argument('equations', nargs='*')
    args = _argparse.parse_args(sys.argv[1:])  # remove name programe

    # check have one equation in args
    if not len(args.equations):
        from_stdin(args)
    else:
        from_args(args)


if __name__ == "__main__":
    main()
