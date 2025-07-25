Python Library Documentation: module pydoc

**NAME**
    pydoc - Generate Python documentation in HTML or text for interactive use.

**MODULE REFERENCE**
    https://docs.python.org/3.12/library/pydoc.html

    The following documentation is automatically generated from the Python
    source files.  It may be incomplete, incorrect or include features that
    are considered implementation detail and may vary between Python
    implementations.  When in doubt, consult the module reference at the
    location listed above.

**DESCRIPTION**
    At the Python interactive prompt, calling help(thing) on a Python object
    documents the object, and calling help() starts up an interactive
    help session.

    Or, at the shell command line outside of Python:

    Run "pydoc <name>" to show documentation on something.  <name> may be
    the name of a function, module, package, or a dotted reference to a
    class or function within a module or module in a package.  If the
    argument contains a path segment delimiter (e.g. slash on Unix,
    backslash on Windows) it is treated as the path to a Python source file.

    Run "pydoc -k <keyword>" to search for a keyword in the synopsis lines
    of all available modules.

    Run "pydoc -n <hostname>" to start an HTTP server with the given
    hostname (default: localhost) on the local machine.

    Run "pydoc -p <port>" to start an HTTP server on the given port on the
    local machine.  Port number 0 can be used to get an arbitrary unused port.

    Run "pydoc -b" to start an HTTP server on an arbitrary unused port and
    open a web browser to interactively browse documentation.  Combine with
    the -n and -p options to control the hostname and port used.

    Run "pydoc -w <name>" to write out the HTML documentation for a module
    to a file named "<name>.html".

    Module docs for core modules are assumed to be in

        https://docs.python.org/X.Y/library/

    This can be overridden by setting the PYTHONDOCS environment variable
    to a different URL or to a local directory containing the Library
    Reference Manual pages.

**DATA**
    **__all__** = ['help']
    **help** = <pydoc.Helper instance>

**DATE**
    26 February 2001

**AUTHOR**
    Ka-Ping Yee <ping@lfw.org>

**CREDITS**
    Guido van Rossum, for an excellent programming language.
    Tommy Burnette, the original creator of manpy.
    Paul Prescod, for all his work on onlinehelp.
    Richard Chamberlain, for the first implementation of textdoc.

**FILE**
    /usr/lib/python3.12/pydoc.py

