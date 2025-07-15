#!/usr/bin/env python3

__all__ = []
__author__ = "Zerui Ma <jerma88@icloud.com>"
__date__ = "7/8/2025"
__version__ = "0.0.0"
__credits__ = """
Peng Tao, for the TAO package and tasking me to translate the package from PERL into Python.
Larry Wall, for the first postmodern computer language.
Guido van Rossum, for an excellent programming language.
"""

import re

from internal.write_to_file import write_to_file
from internal.write_pydoc import write_pydoc
from internal.syntax import convert_syntax
from internal.remove_sigils import remove_sigils
from preprocess import preprocess

def process_each_line(line:str) -> str:
    """
    The periodic looping logic for each line of Perl code to convert. 
    This function processes a single line of Perl code, converting it to Python syntax.

    Args:
        line (str): Perl code line to process.

    Returns:
        str: Converted Python code line.
    """
    line = convert_syntax(line)
    line = remove_sigils(line)
    line = re.sub(r'(\w+)->\{(\w+)\}', r'\1.\2', line)
    return line

def pl2py(input_file_dir:str, 
          output_file_dir:str = None, 
          pydoc_dir:str = "", 
          verbose:bool = False,
          shebang:str = '#!/usr/bin/python3',
          author:str = "Zerui Ma",
          credits:str = "\n"
          ) -> None:

    output_file_dir = output_file_dir if output_file_dir else re.sub(r'\.[^.]*$', '.py', input_file_dir)
    
    if verbose: print(f"Preprocessing file: {input_file_dir}")
    preprocessed_file_dir = re.sub(r'\.[^.]*$', '.pl2py', output_file_dir)
    preprocess(input_file_dir, preprocessed_file_dir, shebang = shebang)
    if verbose: print(f"File preprocessed. pl2py file created: {preprocessed_file_dir}")

    # Flags for tracking if file has reached the pydoc section
    doc_content = True
    # Open the preprocessed file and convert each line
    with open(preprocessed_file_dir, 'r') as infile, \
        open(output_file_dir, 'w') as outfile:
        if verbose: print(f"Converting file: {preprocessed_file_dir} to {output_file_dir}")
        for line in infile:
            # Copy the pydocs at the beginning of the file
            # write all lines before line with '=====Start Converting Now====='
            if doc_content:
                if ('=====Start Converting Now=====' in line): doc_content = False; continue
                outfile.write(line)
                continue
            
            line = line.strip()
            if verbose: print(f'Processing line: {line}')
            if line == '' or line.startswith('#'): # Skip empty lines and comments
                outfile.write(line+'\n')
                continue

            # Process the line and write to the output file
            outfile.write(process_each_line(line) + '\n')
    
    if verbose: print(f"File converted and written to: {output_file_dir}")
    # if pydoc_dir:
    #     write_pydoc(output_file_dir, output_dir=pydoc_dir)
    #     if verbose: print(f"Documentation written for {output_file_dir}")

def __main__() -> None:

    import sys
    if len(sys.argv) < 2:
        print("Usage: pl2py.py <input_file> [output_file] [pydoc_dir] [verbose]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    pydoc_dir = sys.argv[3] if len(sys.argv) > 3 else ""
    verbose = bool(sys.argv[4]) if len(sys.argv) > 4 else False

    pl2py(input_file, output_file, pydoc_dir, verbose)

if __name__ == "__main__":
    __main__()