"""
Writes the documentation of a package to a Markdown file and an HTML file.

This script uses the `pydoc` module to generate documentation for a specified package.
It supports rendering the documentation in Markdown format with custom styling.
It also provides an option to write the documentation in HTML format.
Usage:
    python write_pydoc.py <package_name>
where `<package_name>` is the name of the package you want to document.
It will create two files: `<package_name>.md` for Markdown documentation and
`<package_name>.html` for HTML documentation.
"""

from pydoc import render_doc, TextDoc, writedoc

class MDDoc(TextDoc):
    """
    Custom Markdown documentation renderer.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def bold(self, text: str) -> str:
        """
        Render text in bold Markdown format.
        """
        return f"**{text}**"
    
def write_pydoc_text(package_name: str) -> None:
    """
    Write the documentation of a package to a Markdown file.

    Args:
        package_name (str): The name of the package to document.
    """
    doc = render_doc(package_name, renderer=MDDoc())
    with open(f"{package_name}.md", "w") as f:
        f.write(doc)
    print(f"Documentation for {package_name} written to {package_name}.md")

def write_pydoc_HTML(package_name: str) -> None:
    """
    Write the documentation of a package to an HTML file.

    Args:
        package_name (str): The name of the package to document.
    """
    writedoc(package_name)

def __main__() -> None:
    """
    Main function to generate documentation for a package, called upon cli.
    """
    import sys
    if len(sys.argv) != 2:
        print("Usage: write_pydoc.py <package_name>")
        sys.exit(1)

    package_name = sys.argv[1]
    write_pydoc_text(package_name)
    write_pydoc_HTML(package_name)

if __name__ == "__main__":
    __main__()