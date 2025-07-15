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
    
def write_pydoc_text(package_name: str, output_dir: str = None) -> None:
    """
    Write the documentation of a package to a Markdown file.

    Args:
        package_name (str): The name of the package to document.
    """
    doc = render_doc(package_name, renderer=MDDoc())
    if output_dir is None: output_dir = f"{package_name}.md"
    with open(output_dir, "w") as f:
        f.write(doc)
    print(f"Documentation for {package_name} written to {package_name}.md")

def write_pydoc_HTML(package_name: str, output_dir: str = None) -> None:
    """
    Write the documentation of a package to an HTML file.

    Args:
        package_name (str): The name of the package to document.
    """
    writedoc(package_name)
    # if user wants to specify output directory, move the file into it
    if output_dir is not None:
        import os
        html_file = f"{package_name}.html"
        if os.path.exists(html_file):
            os.rename(html_file, os.path.join(output_dir, html_file))
            print(f"Documentation for {package_name} written to {os.path.join(output_dir, html_file)}")
        else:
            print(f"Documentation file {html_file} does not exist.")

def write_pydoc(package_name: str, output_dir: str = None) -> None:
    """
    Write the documentation of a package in both Markdown and HTML formats.

    Args:
        package_name (str): The name of the package to document.
        output_dir (str, optional): Directory to save the documentation files.
    """
    write_pydoc_text(package_name, output_dir)
    write_pydoc_HTML(package_name, output_dir)
    print(f"Documentation for {package_name} written in both Markdown and HTML formats.")

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