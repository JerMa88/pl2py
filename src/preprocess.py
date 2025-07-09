#!/usr/bin/env python3

"""
preprocesses the file to be translated into python.

run ./preprocess -i <INPUT_FILE_DIRECTORY> in order to

    1. extract perldoc documentation of the input perl script
    2. parse PERL 

"""

__all__ = []
__author__ = "Zerui Ma <jerma88@icloud.com>"
__date__ = "7/7/2025"
__version__ = "0.0.0"
__credits__ = """
Peng Tao, for the TAO package and tasking me to translate the package from PERL into Python.
Larry Wall, for the first postmodern computer language.
Guido van Rossum, for an excellent programming language.
"""


def _parse_argument():
    import argparse
    parser = argparse.ArgumentParser(description='Preprocess the entire PERL script by converting the neccessary argument into python template',
                                    epilog='I think, therefore I am.'
                                    )
    parser.add_argument('-i','--input','-input', type=str, required=True, help='input file directory')
    return parser.parse_args()



def assign_var(line:str) -> str:
    """Translates a Perl line like 'my $foo = shift;' into equivalent Python code with type hinting.
    Assumes that 'shift' operates on a function argument list named 'args'.

    Args:
        line (str): _description_

    Raises:
        ValueError: _description_
        ValueError: _description_

    Returns:
        str: _description_
    """
    import re
    from typing import List, Dict, Any

    # Match pattern like: my $var = shift;
    match = re.match(r'my\s+([\$\@\%])(\w+)\s*=\s*shift\s*;', line.strip())
    if not match:
        raise ValueError("Input line is not in expected Perl format.")

    sigil, var_name = match.groups()

    # Determine Python type hint based on Perl sigil
    if sigil == '$':
        py_type = "Any"  # Scalar could be anything; leave it generic
    elif sigil == '@':
        py_type = "List[Any]"
    elif sigil == '%':
        py_type = "Dict[Any, Any]"
    else:
        raise ValueError(f"Unsupported sigil: {sigil}")

    # Python line using 'args' list as input (like Perl's @_)
    py_line = f"{var_name}: {py_type} = args.pop(0)"
    return py_line


from typing import List
import re
def convert_arrow_dereference(lines: List[str]) -> List[str]:
    """Converts Perl-style ->{key} dereferencing to Python ["key"].
    Example: $obj->{DEBUG}  =>  obj["DEBUG"]
    Assumes variable sigils are removed before this step.

    Args:
        lines (List[str]): _description_

    Returns:
        List[str]: _description_
    """
    converted = []
    pattern = re.compile(r'->\{(\w+)\}')

    for line in lines:
        new_line = pattern.sub(r'["\1"]', line)
        converted.append(new_line)

    return converted

def cli():
    import subprocess
    import re
    import datetime
    
    args = _parse_argument()

    perl_file_dir = args.input

    perldoc=subprocess.run(["perldoc", perl_file_dir], capture_output=True).stdout.decode('utf-8')

    _write_to_file(perl_file_dir+'.txt', perldoc, 'w')
    
    first_lines_text=f'''#!/usr/bin/env python3

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
    python_file_dir = re.sub(r'\.[^.]*$', '.py',perl_file_dir)
    print(python_file_dir)
    _write_to_file(python_file_dir, first_lines_text, 'w')
    
    debug = True
    indent_level = 0
    with open(args.input, 'r') as file:
        for line in file:
            line = line.strip()
            if debug: print(f'line: {line}')
            if line == '': 
                _write_to_file(python_file_dir, '\n')
                continue
            if line[0] == '=': continue
            if line.find('{'): 
                indent_level += 1
                line = line.replace('{', ':')
            if line.find('}'): 
                indent_level -= 1
                line = line.replace('}', '')
            if line[0:4] == 'use ':
                module_name = line.split()[1]
                if module_name == 'strict':
                    _write_to_file(python_file_dir, "    "*indent_level+'import sys\n    sys.tracebacklimit = 0\n')
                elif module_name == 'warnings':
                    _write_to_file(python_file_dir, "    "*indent_level+'import warnings\n    warnings.filterwarnings("ignore")\n')
                else:
                    _write_to_file(python_file_dir, "    "*indent_level+f'import {module_name}\n')
            elif line[0:12] == 'our $VERSION': 
                print ('I found VERSION!')
                continue
            elif line[0] == '#': _write_to_file(python_file_dir, "    "*indent_level+line)
            elif line[0:6] == 'print ':
                if line.find('print STDERR'):
                    _write_to_file(python_file_dir, "    "*indent_level+'import sys\n')
                    _write_to_file(python_file_dir, "    "*indent_level+'print(sys.stderr, end="")\n')
                    continue
                if line.find('print STDOUT'):
                    _write_to_file(python_file_dir, "    "*indent_level+'import sys\n')
                    _write_to_file(python_file_dir, "    "*indent_level+'print(sys.stdout, end="")\n')
                    continue
                if re.match(r'print\s+(.+?)\s+if\s+\$(\w+)->\{(DEBUG)\}\s*(==|!=|>=|<=|>|<)\s*(\d+);', line):
                    # Handle Perl-style conditional print statements
                    match = re.match(r'print\s+(.+?)\s+if\s+\$(\w+)->\{(DEBUG)\}\s*(==|!=|>=|<=|>|<)\s*(\d+);', line)
                    print_parts, obj, key, operator, threshold = match.groups()
                    parts = [p.strip() for p in print_parts.split(',') if p.strip()]
                    converted_parts = []
                    for part in parts:
                        if re.match(r'^".*"$', part) or re.match(r"^'.*'$", part):
                            converted_parts.append(part.strip('"').strip("'"))
                        elif re.match(r'^\$\w+$', part):
                            converted_parts.append(f"{{{part[1:]}}}")
                        else:
                            converted_parts.append(part)
                    fstring = " ".join(converted_parts).replace("\\n", "\n")

                    _write_to_file(python_file_dir, "    "*indent_level+f'if {obj}["{key}"] {operator} {threshold}: print(f"{fstring}")')
                    continue
                message = re.match(r'print\s+"(.*?)\\n";', line).group(1) # Replace Perl-style variables inside string with Python f-string
                fstring = re.sub(r'\$(\w+)', r'{\1}', message)
                _write_to_file(python_file_dir, "    "*indent_level+f'print(f"{fstring}")\n')
            elif line[0:2] == 'my': 
                line = assign_var(line)
                _write_to_file(python_file_dir, "    "*indent_level+line)
            elif line[0:3] == 'sub': _write_to_file(python_file_dir, "    "*indent_level+line.replace('sub ', 'def ').replace(': method', '(*args_input)'))
            else:
                line = line.replace(r'/[@$%]/g', "")
                _write_to_file(python_file_dir, "    "*indent_level+line+'___LINE_WAS_NOT_PROCESSED___\n')
            # _write_to_file(python_file_dir, '\n')
    

if __name__ == '__main__':
    cli()