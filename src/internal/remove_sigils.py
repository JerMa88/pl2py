import re
import argparse

def _append_typing(sigil: str) -> str:
    """return a string of python type hints based on Perl sigils.

    Args:
        line (str): The sigil.

    Returns:
        str: Python type hints.
    """
    sigil_to_type = {
        '$': "Any",                 # scalar
        '@': "List[Any]",           # array
        '%': "Dict[Any, Any]",      # hashe
        '&': "Callable[..., Any]",  # subroutine
        '*': "Any"                  # typeblob, used to refer to a variable's symbol table entry
    }
    if sigil in sigil_to_type:
        return sigil_to_type[sigil]
    else:
        raise ValueError(f"Unsupported sigil: {sigil}")

def _convert_shift(line: str) -> str:
    # Handle `my $var = shift;`
    line = re.sub(r'shift', 'args.pop(0)', line)
    return line
    
def _convert_declarations(line: str) -> str:
    # Handle declarations (e.g., `my $scalar;`) that weren't matched above
    if line.find("my ") == -1 and line.find("our ") == -1 and line.find("sub ") == -1 : return line # verbose: the string does not have "my", does not find "our", and does not find "sub"
    matches = re.findall(r'(\$|\@|\%|\&|\*)(\w+)', line)
    if not matches: raise SyntaxError(f"Given Perl code does not have sigils upon initilization of variables or subroutine!\nIssue occured at: {line}")
    for sigil, var_name in matches:
        type_hint = _append_typing(sigil)
            
        # local variable declaration
        line = re.sub(rf'my\s+{re.escape(sigil)}{var_name}', f'{var_name}: {type_hint}', line, count=1)
        # global variable declaration
        line = re.sub(rf'our\s+{re.escape(sigil)}{var_name}', f'{var_name.upper()}: {type_hint}', line, count=1)
        #function declaration
        func_name = var_name
        line = re.sub(rf'sub\s+{re.escape(sigil)}{func_name}', f'def {func_name}(**args): Callable[..., Any]', line, count=1)
        # print(line)
    return line

def _remove_final_sigils(line: str) -> str:
    """remove the rest of the sigils, not previously matched with any patterns, from a line.
    YOU SHOULD ONLY CALL THIS FUNCTION AT THE END OF THE SYNTAX CONVERSION PROCESS! 
    Many other functions that deals with syntax parsing such as _convert_declarations depend on the sigils to match and find certain text patterns.

    Args:
        line (str): The input string, a line of Perl code that may contain sigils though already attemped to be removed from more complicated logic.

    Returns:
        str: The modified string with sigils replaced by Python syntax and type hints entirely.
    """
    pattern = r'(\$|\@|\%|\&|\*)(\w+)'
    
    # Final cleanup: remove any remaining sigils
    line = re.sub(pattern, r'\2', line)
    return line

def _array_hash_init(line:str) -> str:
    # Handle array initialization `my @array = (1, 2, 3);`
    array_match = re.match(r'(my|our)\s+@(\w+)\s*=\s*\((.*)\)\s*;?', line)
    if array_match:
        scope, var_name, content = array_match.groups()
        var_name = var_name.upper() if scope == 'our' else var_name
        line = f"{var_name}: List[Any] = [{content}];"

    # Handle hash initialization `my %hash = ('key' => 'value');`
    hash_match = re.match(r'(my|our)\s+%(\w+)\s*=\s*\((.*)\)\s*;?', line)
    if hash_match:
        scope, var_name, content = hash_match.groups()
        var_name = var_name.upper() if scope == 'our' else var_name
        py_content = content.replace('=>', ':')
        line = f"{var_name}: Dict[Any, Any] = {{{py_content}}};"
    
    # Handle hash value access `$hash{'key'}` -> `hash['key']`
    # This regex finds a variable with a $ sigil followed by braces {}
    # and converts the braces to brackets []. It's placed before the general
    # sigil removal to correctly handle the brace-to-bracket conversion.
    line = re.sub(r'\$(\w+)\{(.*?)\}', r'\1[\2]', line)
    return line

def remove_sigils(line: str) -> str:
    """Process sigils in a Perl line and return Python type hints.

    This function is updated to handle specific Perl initialization patterns for
    arrays, hashes, and subroutines, converting them to their Python equivalents.
    It prioritizes these specific patterns before falling back to general sigil removal.

    Args:
        line (str): The input string, a line of Perl code.

    Returns:
        str: The modified string with sigils replaced by Python syntax and type hints.
    """
    line = line.strip()

    line = _array_hash_init(line)
    line = _convert_declarations(line)
    line = _convert_shift(line)
    
    return _remove_final_sigils(line)

def __main__():
    parser = argparse.ArgumentParser(description="Remove sigils from Perl variable names in a string.")
    parser.add_argument('-l', '--line', type=str, required=False, default="$value = $hash{'key'};", help='Input line containing Perl code')
    parser.add_argument('-f', '--file', type=str, required=False, help='Input file containing Perl code to process line by line')
    parser.add_argument('-o', '--output', type=str, required=False, help='Output file to save the processed Python code')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    args = parser.parse_args()

    if args.file:
        with open(args.file, 'r') as infile, open(args.output, 'w') if args.output else open('./translated.py', 'w') as outfile:
            for line in infile:
                result = remove_sigils(line)
                if args.verbose:
                    print(f"Original: {line.strip()} -> Converted: {result}")
                if outfile:
                    outfile.write(result + '\n')
                
    else:
        # Process a single line input
        if not args.line:
            raise ValueError("No input line provided. Use -l or --line to specify a line of Perl code.")
        if args.verbose:
            print(f"Processing line: {args.line}")
        if args.output:
            with open(args.output, 'w') as outfile:
                result = remove_sigils(args.line)
                outfile.write(result + '\n')
        else:
            # Print the result to console if no output file is specified
            if args.verbose:
                print(f"Converted line: {args.line} -> {remove_sigils(args.line)}")
            else:
                print(remove_sigils(args.line)) 

if __name__ == "__main__":
    __main__()