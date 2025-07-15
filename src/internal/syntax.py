import re
import argparse

def _convert_operators(line: str) -> str:
    """Convert Perl operators to Python equivalents."""
    # Convert Perl's ' eq ', ' ne ', ' lt ', ' gt ', ' le ', ' ge ' to Python's ' == ', ' != ', ' < ', ' > ', ' <= ', ' >= '
    line = re.sub(r' \beq\b ', ' == ', line)
    line = re.sub(r' \bne\b ', ' != ', line)
    line = re.sub(r' \blt\b ', ' < ', line)
    line = re.sub(r' \bgt\b ', ' > ', line)
    line = re.sub(r' \ble\b ', ' <= ', line)
    line = re.sub(r' \bge\b ', ' >= ', line)

    # Convert Perl's ' =~ ', ' !~ ' to Python's ' re.match(), ' re.search()'
    line = re.sub(r'(\$\w+)\s*=~\s*/(.+?)/', r'\1 = re.match(r"\2", \1)', line)
    line = re.sub(r'(\$\w+)\s*!~\s*/(.+?)/', r'\1 = re.search(r"\2", \1)', line)

    # Convert Perl's ' x ', ' . ' to Python's ' * ', ' + '
    line = re.sub(r' x ', ' * ', line)
    line = re.sub(r' \. ', ' + ', line)
    # Convert Perl's ' && ', ' || ', ' ! ', to Python's ' and ', ' or ', ' not '
    line = re.sub(r' && ', 'and', line)
    line = re.sub(r' \|\| ', 'or', line)
    line = re.sub(r' ! ', ' not ', line)
    # Convert Perl's ' ||= ', ' &&= ', ' .= ' to Python's ' |= ', ' &= ', ' += '
    line = re.sub(r' \|\|= ', ' |= ', line)
    line = re.sub(r' &&= ', ' &= ', line)
    line = re.sub(r' \.\+= ', ' += ', line)

    # Convert Perl's 'last', 'next', 'redo' to Python's 'break', 'continue', 'pass'
    line = re.sub(r'\blast\b', 'break', line)
    line = re.sub(r'\bnext\b', 'continue', line)
    line = re.sub(r'\bredo\b', 'pass', line)

    # Convert Perl's 'open' to Python's 'open'
    line = re.sub(r'\bopen\s*\(\s*([\'"])(.*?)\1\s*,\s*([\'"])(.*?)([\'"])\s*\)', r'open(\2, \3\4")', line)
    # Convert Perl's 'close' to Python's 'close'
    line = re.sub(r'\bclose\s*\(\s*([\'"])(.*?)\1\s*\)', r'\2.close()', line)

    # Convert Perl's 'die' to Python's 'raise Exception'
    line = re.sub(r'\bdie\s*"\s*(.*?)\s*"\s*;', r'raise Exception("\1")', line)
    line = re.sub(r'\bdie\s*"\s*(.*?)\s*"', r'raise Exception("\1")', line)
    # Convert Perl's 'warn' to Python's 'warnings.warn'
    line = re.sub(r'\bwarn\s*"\s*(.*?)\s*"\s*;', r'warnings.warn("\1")', line)
    line = re.sub(r'\bwarn\s*"\s*(.*?)\s*"', r'warnings.warn("\1")', line)

    #Convert Perl's 'system' to Python's 'os.system'
    line = re.sub(r'\bsystem\s*\(\s*([\'"])(.*?)\1\s*\)', r'os.system("\2")', line)
    
    return line

def _convert_print(line: str) -> str:
    """Convert Perl's print statements to Python's print function."""
    # Convert Perl's print statements to Python's print function
    if line.startswith('print '):
        line = line.replace('print ', 'print(f').rstrip(';') + ');'
    return line

def _convert_oneline_if(line: str) -> str:
    """
    Converts Perl-style postfix '... if condition;' to Python-style 'if condition: ...;'
    """
    pattern = r'^(.*?)\s+if\s+(.*?);?\s*$'
    match = re.match(pattern, line)
    if match:
        statement = match.group(1).strip()
        condition = match.group(2).strip()
        return f"if {condition}: {statement};"
    return line

def _delete_semicolon(line: str) -> str:
    """
    Remove semicolon from the end of a line if it exists.
    If there are semicolons in the middle of the line, push the line content after the semicolon to a new line and then remove the semicolon.
    """
    if line.endswith(';'):
        line = line[:-1].strip()
    if ';' in line:
        parts = line.split(';')
        line = parts[0].strip() + '\n' + ' '.join(part.strip() for part in parts[1:])
    return line
    
def convert_syntax(line: str) -> str:
    """
    Convert a line of Perl syntax to Python syntax.
    This function applies operator conversion, print conversion, and one-line if conversion.
    """
    line = _convert_operators(line)
    line = _convert_print(line)
    line = _convert_oneline_if(line)
    line = _delete_semicolon(line)
    return line

def __main__():
    parser = argparse.ArgumentParser(description="convert Perl syntax to Python syntax")
    parser.add_argument('-l', '--line', type=str, required=False, help='Input line to convert')
    parser.add_argument('-f', '--file', type=str, required=False, help='Input file to convert')
    parser.add_argument('-o', '--output', type=str, required=False, default='output.py', help='Output file to write converted code')
    args = parser.parse_args()

    if args.line:
        # Convert a single line
        line = args.line.strip()
        print(convert_syntax(line))
    elif args.file:
        # Convert a file
        with open(args.file, 'r') as infile, open(args.output, 'w') as outfile:
            for line in infile:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                line = convert_syntax(line)
                outfile.write(line + '\n')
    else:
        print("Please provide either a line with -l or a file with -f to convert.")

if __name__ == "__main__":
    __main__()