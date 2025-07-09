from src.internal.write_pydoc import MDDoc, write_pydoc_text, write_pydoc_HTML
import os, subprocess

package_name = "pydoc"

def test_mddoc_bold():
    renderer = MDDoc()
    result = renderer.bold("test")
    assert result == "**test**"

def test_write_pydoc_text():
    """Test the write_pydoc_text function."""
    assert write_pydoc_text(package_name) is None
    assert os.path.exists(f"{package_name}.md")

def test_write_pydoc_HTML():
    """Test the write_pydoc_HTML function."""
    assert write_pydoc_HTML(package_name) is None
    assert os.path.exists(f"{package_name}.html")

def test_main_function_creates_files():
    """Test the main function generates both .md and .html files."""
    assert subprocess.run(["python3", "src/internal/write_pydoc.py", package_name], check=True).returncode == 0
    assert os.path.exists(f"{package_name}.md")
    assert os.path.exists(f"{package_name}.html")

def test_invalid_package_name():
    """Test the main function with an invalid package name."""
    invalid_package_name = "non_existent_package"
    result = subprocess.run(["python3", "src/internal/write_pydoc.py", invalid_package_name], capture_output=True, text=True)
    assert result.returncode != 0
    assert "non_existent_package" in result.stderr
    assert not os.path.exists(f"{invalid_package_name}.md")
    assert not os.path.exists(f"{invalid_package_name}.html")