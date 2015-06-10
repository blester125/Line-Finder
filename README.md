## Lines ##

**Lines.py** is a program that will parse a directory of 
python files to find all of the class definitions and 
function definitions in the files and save them to an output file *lines.txt* along with the line numbers.

### Dependencies 

This requires the [argparse](https://pypi.python.org/pypi/argparse) module.  It can also be installed with `pip install argparse` on many systems.

### Usage

This program can be run two ways.

`python lines.py`

This will display the output that is only the names of the classes and functions and the line numbers.

`python lines.py -v`

or

`python lines.py --verbose`

This will display the entire signature of the functions and classes (the arguments of the function and what the classes extend).
