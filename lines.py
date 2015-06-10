import os
import sys
import argparse

"""A program that documents function and class names.

This program parses all python source files in the current directory.
It will output into a file called lines.txt that include the filenames, 
the class and function names, and the line numbers of that file.
It also has a verbose mode that includes information about the classes
and functions such as what the extend and what their arguments are 
respectivly along with the numbers.

Example:
  The program is normally run like so:
 
    $python lines.py

  This formats the data so that the output is only the name of the
  class or function and the line number.
  It can also be used like so:
  
    $python lines.py -v | --version
 
  This will include the parameters the function takes in the output and
  includes what class the class extends. 

Attributes:
  data (list of lists of strs): A list of lists which contain two
    strings.  This data is in the form 
    [[function/class name, line_num],[function/class name, line_num],...]
  
"""

def find_functions(filename, data):
  """Search a file for function and class names.
  
  Args: 
    filename (str): The name of the file that will be parsed.
    data (list of lists): The data list that new funciton/class names
      will be added to.

  Attributes:
    line_num (int): The number of the current line read from filename.
      This is the second half of data units the will be added to data.
  """
  line_num = 1
  fin = open(filename, 'r')
  for line in fin:
    # The final check for ':' stops comments and whatnot that contain
    # the word default.
    if ('def ' in line or 'class' in line) and ':' in line:
      line = line[:-1]
      if 'def' in line:
        line = format_function(line)
      if 'class' in line:
        line = format_class(line)
      pack_data(data, line, str(line_num))
    line_num = line_num + 1

def format_function(function_name):
  """Format data that is a function name.

  This formats the output for a function name in the following ways.

    "function name"

  of like so when -v or --verbose is set.
  
    "function name(args, ...)"

  In either case the ':' is removed.

  Args:
    function_name (str): The data that is the name of a function.

  """
  function = ''
  parts = function_name.split(' ')
  if opts.verbose:
    for i in parts:
      if i != '' and i != 'def':
        function += i + " "
    function = function[:function.find(':')]
  else:
    for i in parts:
      if i != '' and i != 'def':
        name = i.split('(')
        function = name[0]
        break
  return function

def format_class(class_name):
  """Format the data that is a class name.

  This formats the output for a class name in the following ways.

    "class name"
  
  or like so when -v or --verbose is set.
  
    "class name(extends)"

  In either case the ':' is removed.

  Args:
    class_name (str): The name of a class in the python source code.

  """
  function = ''
  if not opts.verbose:
    name = class_name.split('(')
    function = name[0]
  else:
    function = class_name[:-1]
  return function

def pack_data(data, entry1, entry2):
  """A function that adds formatted data to the list.
  
  Args:
    data (list of lists): The list to add the current data to.
    entry1 (str): The first piece of data.
    entry2 (str): The second piece of data.

  Attributes:
    entry (list of str): The list that will be added to data.
      entry is a list of entry1 and entry 2 [entry1, entry2].
 
  """
  entry = []
  entry.append(entry1)
  entry.append(entry2)
  data.append(entry)

def write_output(data):
  """Writes the data to an output file.

  Note: 
    If ran with the verbose option the padding is less so that there is
    less of a chance that a piece of data will span multiple lines.

  Args:
    data (list of lists): The list of data that will be output.

  Attributes:
    padding (int): The padding that is the distance between the first
      column of data and the second.
    fout (FILE): The file that data will be output to.
    col_width (int): The length of the longest piece of data in the 
      list plus padding.  This is used to format the output.
  
  """
  if opts.verbose:
    padding = 2
  else:
    padding = 10
  fout = open('lines.txt', 'w')
  col_width = max(len(word) for row in data for word in row) + padding
  for row in data:
    output = "".join(word.ljust(col_width) for word in row)
    output = output.strip()
    fout.write(output)
    fout.write('\n')
  fout.close()

if __name__ == '__main__':
  """The part that is run when the script is ran.
 
  All the files in the current working directiory are looked at and if
  it is a python source file (extension '.py') it will parse the file.
  This file does not parse itself.

  Attributes:
    data (list of lists): The data structure that will hold the
      filenames and line numbers.
    parser (object): The object to parse the command line arguments.
      It detects -v or --verbose and sets it to true if one of those 
      flags are present. 
    opts (namespace): The namespace object that holds if verbose was
      set or not.

  """
  data = []
  parser = argparse.ArgumentParser()
  parser.add_argument('-v', '--verbose', dest='verbose', action='store_true')
  opts = parser.parse_args()
  for i in os.listdir(os.getcwd()):
    if i.endswith('.py'):
      if i == sys.argv[0]:
        continue
      filename = i
      pack_data(data, '####' + filename + '####', '')
      find_functions(filename, data)
      pack_data(data, '', '')
  if len(data) == 0:
    print "No files to parse"
    exit()
  write_output(data)
