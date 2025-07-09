import re
import argparse
from typing import Any, List, Dict, Callable

def _append_typing(sigil: str) -> str:
    """return a string of python type hints based on Perl sigils.

    Args:
        line (str): The sigil.

    Returns:
        str: Python type hints.
    """
    sigil_to_type = {
        '$': "Any",
        '@': "List[Any]",
        '%': "Dict[Any, Any]",
        '&': "Callable[..., Any]",
        '*': "Any"
    }
    if sigil in sigil_to_type:
        return sigil_to_type[sigil]
    else:
        raise ValueError(f"Unsupported sigil: {sigil}")

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

    # Handle full subroutine declaration `sub name`
    sub_match = re.match(r'sub\s+(\w+)\s', line)
    if sub_match:
        func_name, body = sub_match.groups()
        body = body.strip().rstrip('};')
        processed_body = remove_sigils(body) if body else ""
        line = f"def {func_name}(*args): {processed_body}"

    # Handle `my $var = shift;`
    shift_match = re.match(r'my\s+\$(\w+)\s*=\s*shift\s*;?', line)
    if shift_match:
        var_name = shift_match.group(1)
        line = f"{var_name}: Any = args.pop(0);"

    # Handle array initialization `my @array = (1, 2, 3);`
    array_match = re.match(r'(my|our)\s+@(\w+)\s*=\s*\((.*)\)\s*;?', line)
    if array_match:
        scope, var_name, content = array_match.groups()
        var_name = var_name.upper() if scope == 'our' else var_name
        line = f"{var_name}: List[Any] = [{content}]"

    # Handle hash initialization `my %hash = ('key' => 'value');`
    hash_match = re.match(r'(my|our)\s+%(\w+)\s*=\s*\((.*)\)\s*;?', line)
    if hash_match:
        scope, var_name, content = hash_match.groups()
        var_name = var_name.upper() if scope == 'our' else var_name
        py_content = content.replace('=>', ':')
        line = f"{var_name}: Dict[Any, Any] = {{{py_content}}}"
    
    # Handle hash value access `$hash{'key'}` -> `hash['key']`
    # This regex finds a variable with a $ sigil followed by braces {}
    # and converts the braces to brackets []. It's placed before the general
    # sigil removal to correctly handle the brace-to-bracket conversion.
    line = re.sub(r'\$(\w+)\{(.*?)\}', r'\1[\2]', line)

    # simple declarations and general sigil removal
    pattern = r'(\$|\@|\%|\&|\*)(\w+)'
    matches = re.findall(pattern, line)
    if not matches:
        return line

    # Handle declarations (e.g., `my $scalar;`) that weren't matched above
    if line.startswith(("my ", "our ")):
        sigil, var_name = matches[0]
        type_hint = _append_typing(sigil)
        
        if line.startswith("my "):
            line = re.sub(rf'my\s+{re.escape(sigil)}{var_name}', f'{var_name}: {type_hint}', line, count=1)
        elif line.startswith("our "):
            line = re.sub(rf'our\s+{re.escape(sigil)}{var_name}', f'{var_name.upper()}: {type_hint}', line, count=1)

    # Final cleanup: remove any remaining sigils
    line = re.sub(pattern, r'\2', line)
    return line

def __main__():
    parser = argparse.ArgumentParser(description="Remove sigils from Perl variable names in a string.")
    parser.add_argument('-l', '--line', type=str, required=False, default="$value = $hash{'key'};", help='Input line containing Perl code')
    args = parser.parse_args()

    result = remove_sigils(args.line)
    print(f"Original Perl: {args.line}")
    print(f"Converted Python: {result}")

if __name__ == "__main__":
    __main__()