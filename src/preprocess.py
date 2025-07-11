import re
import argparse
import subprocess
import datetime

from internal.write_to_file import _write_to_file

def preprocess(input_file_dir: str, output_file_dir:str = None, shebang:str = '#!/usr/bin/python3') -> str:
    
    output_file_dir = output_file_dir if output_file_dir else re.sub(r'\.[^.]*$', '.pl2py', input_file_dir)

    content = ""

    # open the file
    with open(input_file_dir, 'r') as file:
        file_content = file.readlines()
        print(f"Processing {len(file_content)} lines from {input_file_dir}...")
        print(f"file content: {file_content}, type: {type(file_content)}")

        if '#!/usr/bin/perl' in file_content[0]:
            content += shebang + '\n'

        # add pydoc to the file based on the perldoc of the input file
        perldoc=subprocess.run(["perldoc", input_file_dir], capture_output=True).stdout.decode('utf-8')
        content += f'''
"""{perldoc}"""
__all__ = []
__author__ = "Zerui Ma <jerryma@smu.edu>"
__date__ = "{datetime.datetime.now().strftime('%m-%d-%Y')}"
__version__ = "2.0.0"

__credits__ = """
Peng Tao, for the TAO package and tasking me to translate the package from PERL into Python.
Larry Wall, for the first postmodern computer language.
Guido van Rossum, for an excellent programming language.
"""'''
        _write_to_file(output_file_dir, content, 'w')

        # remove use strict as python does not need it
        file_content = [line for line in file_content if not line.startswith('use strict;')]
        # replace use warnings with python's warning module
        file_content = [line.replace('use warnings;', 'import warnings') for line in file_content]
        # replace use File::Basename with python's os.path
        file_content = [line.replace('use File::Basename;', 'import os') for line in file_content]
        # remove perldoc "=...=cut" lines and every lines in between
        perldoc_flag = False
        for line in file_content:
            if line.startswith('=cut'):
                perldoc_flag = False
                continue
            if line.startswith('=') and not line.startswith('=cut'):
                perldoc_flag = True
                continue
            if perldoc_flag:
                continue
            else: # add the line to content
                _write_to_file(output_file_dir, line, 'a')
    
def __main__():
    parser = argparse.ArgumentParser(description="Preprocess a Perl file to Python.")
    parser.add_argument('-i', '--input', type=str, required=True, help='Input Perl file to preprocess')
    parser.add_argument('-o', '--output', type=str, required=False, help='Output Python file (default: input file name with .pl2py extension)')
    args = parser.parse_args()
    preprocess(args.input, args.output)

if __name__ == "__main__":
    __main__()