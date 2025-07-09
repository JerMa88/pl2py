Python Library Documentation: module remove_sigil

**NAME**
    remove_sigil

**FUNCTIONS**
    **__main__**()

    **remove_sigils**(line: str) -> str
        Process sigils in a Perl line and return Python type hints.

        This function is updated to handle specific Perl initialization patterns for
        arrays, hashes, and subroutines, converting them to their Python equivalents.
        It prioritizes these specific patterns before falling back to general sigil removal.

        Args:
            line (str): The input string, a line of Perl code.

        Returns:
            str: The modified string with sigils replaced by Python syntax and type hints.

**DATA**
    **Callable** = typing.Callable
        Deprecated alias to collections.abc.Callable.

        Callable[[int], str] signifies a function that takes a single
        parameter of type int and returns a str.

        The subscription syntax must always be used with exactly two
        values: the argument list and the return type.
        The argument list must be a list of types, a ParamSpec,
        Concatenate or ellipsis. The return type must be a single type.

        There is no syntax to indicate optional or keyword arguments;
        such function types are rarely used as callback types.

    **Dict** = typing.Dict
        A generic version of dict.

    **List** = typing.List
        A generic version of list.

**FILE**
    /home/zma/Documents/programs/pl2py/src/internal/remove_sigil.py

