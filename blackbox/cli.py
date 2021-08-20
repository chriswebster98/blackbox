"""A CLI interface for blackbox."""
from argparse import ArgumentParser
import sys
import shutil

from blackbox.fuzzytests.randomvalues import RandomValues
from blackbox.manager import TestRunner


def run_test(args):
    """
    Execute Using TestRunner
    """
    # correct arguments and optionals
    args.a = correct_args(args.a)
    args.o = correct_args(args.o)
    
    test_runner = TestRunner(args)
    test_runner.run()

    
def correct_args(arguments):
    """
    Used to correct arguments and replace hyphens.

    Arguments:
        arguments: list of arguments from CLI

    Returns:
        list: correct arguments from _ to -
    """
    if arguments:
        return [x.replace("_", "-") for x in arguments]
    else:
        return None

class CLI:
    """
    Command Line Interface used to parse arguments.
    """
    def __init__(self):
        """
        Runs the setup for CLI arguments, and executes CLI commands.

        Returns:
            csv: Results of used arguments
        """
        parser = self.setup()
        args = parser.parse_args()
        

        # execute arguments
        rc = args.func(args)
        sys.exit(rc)


    def setup(self):
        """
        Setup the argument parser and its commands.

        Returns:
            parser: Argument Parser for user CLI commands.
        """
        parser = ArgumentParser(
            prog="blackbox",
            description="A tool to test different inputs for any given program."
        )
        parser.add_argument("-t", "--test", action="store", type=str)
        parser.add_argument("-n", "--count", type=int, default=100)
        parser.add_argument("-p", "--prog", action="store", type=str)
        parser.add_argument("--a", "--arguments", action="append")
        parser.add_argument("--o", "--optionals", action="append")
        parser.set_defaults(func=run_test)

        return parser
