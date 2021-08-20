"""A class module used to provide the randomvalues fuzzy testing."""
from collections import defaultdict
import string
import random
import os
import tempfile
import shutil


class RandomValues:
    """A fuzzytest class used for random inputs fuzzy testing."""

    name = "RandomValues"
    types = ["int", "float", "string", "binary"]
    final_outputs = [1, 2, 3, 4, 5, 6, 7, 8, 9, "file"]
    file_exts = ["yaml", "txt", "csv", "jpg", "sh"]
    max_length = 5000

    def __init__(self, prog, args, optionals):
        """
        Used to initialize RandomValues Test.

        Arguments:
            prog: program name to be testing
            args: required arguments for `prog` to be run
            optionals: optional arguments to run with `prog`

        Returns:
            None: Initializes class object
        """
        self.prog = prog
        self.args = args
        self.optionals = optionals
        self.arg_dict = defaultdict(lambda: None)


    def generate_test_command(self):
        """
        Used to generate a given test.
        
        Returns:
            str: command line string to be executed for test
        """
        arguments_str = self.generate_random_args(self.args)
        optionals_str = self.generate_optional_args(self.optionals)
        command = "{} {} {}".format(self.prog, arguments_str, optionals_str)
        command = command.split()
        return command, dict(self.arg_dict)


    def generate_optional_args(self, optionals):
        """
        Used to select and generate which optional arguments are used

        Arguments:
            optionals: list of optional arguments

        Returns:
            str: optional command arguments and their values
        """
        if optionals:
            num_optional_params = random.randrange(len(optionals))
            optional_params = random.sample(optionals, num_optional_params)
            optional_str = self.generate_random_args(optional_params)
            return optional_str
        else:
            return ""

    def generate_random_args(self, arguments):
        """
        Used to generate arguments for `progs`.

        Arguments:
            arguments: arguments for prog. (can be self.args, or self.optionals)

        Returns:
            str: command line string of arguments to run
        """
        all_argument_str = ""
        for arg in arguments:
            # decide what type of data this arg will have
            data_type = random.choice(self.types)
            final_output = random.choice(self.final_outputs) # .2 percent chance will use a file
            argument_dict = {"type": data_type, "file": False}

            # generate data based on the random data type
            if data_type == "int":
                # select between smallest int, and max int
                value = random.randrange(-2147483648, 2147483647)
            elif data_type == "float":
                # select between smallest float and max float
                value = random.uniform(2.2250738585072014e-308, 1.7976931348623157e+308)
            elif data_type == "string":
                # get random size of string, and generate random string characters
                size = random.randrange(0, self.max_length)
                value = ''.join(random.choices(string.ascii_uppercase + string.digits, k=size))
            elif data_type == "binary":
                # convert this integer to bytes
                size = random.randrange(0, 1000)
                value = bytes(size)
            
            # 10% chance of writing to file
            if final_output == "file":
                argument_dict["file"] = True
                # get file extension and file name
                file_ext = random.choice(self.file_exts)
                basename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                basename = "{}.{}".format(basename, file_ext)
                tempdir = tempfile.mkdtemp()
                file_path = os.path.join(tempdir, basename)

                # write value to file 
                with open(file_path, "w") as f:
                    f.write(str(value))

                value = file_path
                argument_dict["path"] = value
                
                
            self.arg_dict[arg] = argument_dict
            arg_value_str = '{} {}'.format(arg, value)
            all_argument_str = "{} {}".format(all_argument_str, arg_value_str)

        return all_argument_str


    def cleanup(self):
        """
        Used to clean up test.
        
        Returns:
            None: removes temporary files and directories that were created for test
        """
        # if a file was generated, delete it.
        for args, arg_dict in self.arg_dict.items():
            if "path" in arg_dict:
                path = os.path.dirname(arg_dict["path"])
                shutil.rmtree(os.path.dirname(path), ignore_errors=True)
            
                




