"""Manager for running tests."""
import os
import subprocess
import time
import csv
import concurrent.futures
from blackbox.fuzzytests.randomvalues import RandomValues

class TestRunner:
    """A class used to manage running tests."""

    status_fields = ["args", "return_code", "stderr", "stdout"]

    def __init__(self, args):
        """
        Used to initiate test runner object
        
        Arguments:
            args: provided command line arguments

        Returns:
            None: Initiates class variables 
        """
        # based on user option, 
        self.test = args.test
        self.count = args.count
        self.prog = args.prog
        self.arguments = args.a
        self.optionals = args.o
        self.status_file = "blackboxtest-{}.csv".format(time.strftime("%Y%m%d-%H%M%S"))


    def write_to_status(self, line):
        """
        Used to write to the status file

        Arguments:
            line: array of csv data to write
        
        Returns:
            None: writes to file
        """
        
        with open(self.status_file, 'a+', newline='') as status:
            csv_file = csv.writer(status)
            csv_file.writerow(line)

    def run_single_test(self):
        """
        Used to run a single test.

        Returns:
            str: csv line to be written
        """
        test_class = None

        # get test type
        if self.test == "1":
            test_class = RandomValues(
                prog=self.prog,
                args=self.arguments,
                optionals=self.optionals
            )

        # generate test command
        command, arg_dict = test_class.generate_test_command()

        # create process to run command
        dut = subprocess.run(
            command,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        # log output
        args_string = " ".join(dut.args)
        csv_line = [args_string, dut.returncode, dut.stderr, dut.stdout]
        self.write_to_status(csv_line)

        # clean up test
        test_class.cleanup()

    def run(self):
        """
        Used to run tests in parallel via multithreading.

        Returns:
            file: status file containing results of run
        """
        start = time.time()
        self.write_to_status(self.status_fields)
        count = range(self.count)

        #for test_runs in range(self.count): -> 130 sec
        #    self.run_single_test()
        
        # parallelize using multithreading
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_runs = {executor.submit(self.run_single_test): num for num in count}
            for future in concurrent.futures.as_completed(future_runs):
                pass

    
        end = time.time()
        print("completed in {}.".format(end - start))
    
