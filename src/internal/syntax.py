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
    line = re.sub(r' \b=~\b ', ' re.match(', line)
    line = re.sub(r' \b!~\b ', ' re.search(', line)

    # Convert Perl's ' x ', ' . ' to Python's ' * ', ' + '
    line = re.sub(r' \bx\b ', ' * ', line)
    line = re.sub(r' \b\.\b ', ' + ', line)
    # Convert Perl's ' && ', ' || ', ' ! ', to Python's ' and ', ' or ', ' not '
    line = re.sub(r' \b&&\b ', ' and ', line)
    line = re.sub(r' \b\|\|\b ', ' or ', line)
    line = re.sub(r' \b!\b ', ' not ', line)
    # Convert Perl's ' ||= ', ' &&= ', ' .= ' to Python's ' |= ', ' &= ', ' += '
    line = re.sub(r' \|\|= ', ' |= ', line)
    line = re.sub(r' &&= ', ' &= ', line)
    line = re.sub(r' \.\+= ', ' += ', line)

    # Convert Perl's 'last', 'next', 'redo' to Python's 'break', 'continue', 'pass'
    line = re.sub(r'\blast\b', 'break', line)
    line = re.sub(r'\bnext\b', 'continue', line)
    line = re.sub(r'\bredo\b', 'pass', line)

    # Convert Perl's 'open' to Python's 'open'
    line = re.sub(r'\bopen\s*\(\s*([\'"])(.*?)\1\s*,\s*([\'"])(.*?)([\'"])\s*\)', r'open(\2, \3\4)', line)
    # Convert Perl's 'close' to Python's 'close'
    line = re.sub(r'\bclose\s*\(\s*([\'"])(.*?)\1\s*\)', r'\2.close()', line)
    
    return line

def _convert_print(line: str) -> str:
    """Convert Perl's print statements to Python's print function."""
    # Convert Perl's print statements to Python's print function
    if line.startswith('print '):
        line = line.replace('print ', 'print(f').rstrip(';') + ')'
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
    else:
        raise ValueError("Input does not match expected 'statement if condition;' pattern.")

def __main__():
    