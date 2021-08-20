# blackbox

A blackbox fuzzy tester to be used for testing various applications.

## Setup

`blackbox` can easily be installed by running the following commands:

```
pip3 install -r requirements.txt
pip3 install -e .
```

After this blackbox is setup and ready to go!

## Documentation

The following project is documented using mkdocs. Navigate to the `/docs` directory, and enter the following command to build the docs: `mkdocs build`.

## Usage

`blackbox` runs via the following command line arguments. When entering required arguments or optional arguments that include a `-`, you must write this as a `_` instead.

| argument  | description                                           |
|-----------| ------------------------------------------------------|
| -t        | test type (for now only can use 1)                    |
| -n        | total test runs to use                                |
| -p        | program name that will be tested using blackbox       |
| --a       | arguments that will be used with tested program       |
| --o       | optional arguments that can be included to be tester  |

An example usage of this program would be the following, using [maestrowf](https://github.com/LLNL/maestrowf):

`blackbox -t 1 -n 1000 -p maestro --a run --o _o`

By running the above code, blackbox will run 1000 tests of test 1, which in this case is [RandomValues](/source/fuzzytests/randomvalues/). 

This test will use random values for the provided arguments. The different types of values that can be used are:

- int
- float
- string
- binary
- file

By running blackbox as listed above, the following command will be run 1000 times with various inputs, and randomly selecting when to include optional arguments as well.

`maestro run [random value] -o [random value]`

Wherever `blackbox` is run, an output log in the form of a `.csv` file will be output for a user to inspect the results.

## Future Work

This tool is designed to have a collection of various tests to run with. For now, only one test is available which is RandomValues. In time different tests could easily be added which behave in a smatter manner. 


These tests could be looking for security vulnerabilities, and use specific assertions to find these. Another type of test that could be added is much more complex, but one that uses working sample inputs, and using machine learning to get more coverage of the program to find more issues and vulnerabilities.