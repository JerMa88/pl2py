Python Library Documentation: module write_pydoc

**NAME**
    write_pydoc - Writes the documentation of a package to a Markdown file and an HTML file.

**DESCRIPTION**
    This script uses the `pydoc` module to generate documentation for a specified package.
    It supports rendering the documentation in Markdown format with custom styling.
    It also provides an option to write the documentation in HTML format.
    Usage:
        python write_pydoc.py <package_name>
    where `<package_name>` is the name of the package you want to document.
    It will create two files: `<package_name>.md` for Markdown documentation and
    `<package_name>.html` for HTML documentation.

**CLASSES**
    pydoc.TextDoc(pydoc.Doc)
        MDDoc

    class **MDDoc**(pydoc.TextDoc)
     |  MDDoc(*args, **kwargs)
     |
     |  Custom Markdown documentation renderer.
     |
     |  Method resolution order:
     |      MDDoc
     |      pydoc.TextDoc
     |      pydoc.Doc
     |      builtins.object
     |
     |  Methods defined here:
     |
     |  **__init__**(self, *args, **kwargs)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |
     |  **bold**(self, text: str) -> str
     |      Render text in bold Markdown format.
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from pydoc.TextDoc:
     |
     |  **docclass**(self, object, name=None, mod=None, *ignored)
     |      Produce text documentation for a given class object.
     |
     |  **docdata**(self, object, name=None, mod=None, cl=None, *ignored)
     |      Produce text documentation for a data descriptor.
     |
     |  **docmodule**(self, object, name=None, mod=None, *ignored)
     |      Produce text documentation for a given module object.
     |
     |  **docother**(self, object, name=None, mod=None, parent=None, *ignored, maxlen=None, doc=None)
     |      Produce text documentation for a data object.
     |
     |  **docproperty** = docdata(self, object, name=None, mod=None, cl=None, *ignored)
     |
     |  **docroutine**(self, object, name=None, mod=None, cl=None, homecls=None)
     |      Produce text documentation for a function or method object.
     |
     |  **formattree**(self, tree, modname, parent=None, prefix='')
     |      Render in text a class tree as returned by inspect.getclasstree().
     |
     |  **formatvalue**(self, object)
     |      Format an argument default value as text.
     |
     |  **indent**(self, text, prefix='    ')
     |      Indent text by prepending a given prefix to each line.
     |
     |  **section**(self, title, contents)
     |      Format a section with a given heading.
     |
     |  ----------------------------------------------------------------------
     |  Static methods inherited from pydoc.TextDoc:
     |
     |  **repr**(x) method of pydoc.TextRepr instance
     |
     |  ----------------------------------------------------------------------
     |  Methods inherited from pydoc.Doc:
     |
     |  **document**(self, object, name=None, *args)
     |      Generate documentation for an object.
     |
     |  **fail**(self, object, name=None, *args)
     |      Raise an exception for unimplemented types.
     |
     |  **getdocloc**(self, object, basedir='/home/zma/anaconda3/lib/python3.12')
     |      Return the location of module docs or None
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from pydoc.Doc:
     |
     |  **__dict__**
     |      dictionary for instance variables
     |
     |  **__weakref__**
     |      list of weak references to the object
     |
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from pydoc.Doc:
     |
     |  **PYTHONDOCS** = 'https://docs.python.org/3.12/library'

**FUNCTIONS**
    **__main__**() -> None
        Main function to generate documentation for a package, called upon cli.

    **write_pydoc_HTML**(package_name: str) -> None
        Write the documentation of a package to an HTML file.

        Args:
            package_name (str): The name of the package to document.

    **write_pydoc_text**(package_name: str) -> None
        Write the documentation of a package to a Markdown file.

        Args:
            package_name (str): The name of the package to document.

**FILE**
    /home/zma/Documents/programs/pl2py/src/internal/write_pydoc.py

