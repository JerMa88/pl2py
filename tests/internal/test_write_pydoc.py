import os
import pytest
from unittest.mock import patch, mock_open
from src.internal.write_pydoc import write_pydoc_text, write_pydoc_HTML

@pytest.fixture
def cleanup_files():
    """Fixture to clean up generated files after tests."""
    yield
    for ext in ['.md', '.html']:
        for file in os.listdir():
            if file.endswith(ext):
                os.remove(file)

def test_write_pydoc_text_creates_md_file(cleanup_files):
    """Test that _write_pydoc_text creates a .md file."""
    package_name = "test_package"
    with patch("builtins.open", mock_open()) as mocked_file, patch("pydoc.render_doc", return_value="Mocked Documentation"):
        write_pydoc_text(package_name)
        mocked_file.assert_called_once_with(f"{package_name}.md", "w")
        mocked_file().write.assert_called_once_with("Mocked Documentation")

def test_write_pydoc_HTML_creates_html_file(cleanup_files):
    """Test that _write_pydoc_HTML creates a .html file."""
    package_name = "test_package"
    with patch("pydoc.writedoc") as mocked_writedoc:
        write_pydoc_HTML(package_name)
        mocked_writedoc.assert_called_once_with(package_name)

def test_main_function_creates_files(cleanup_files):
    """Test the main function generates both .md and .html files."""
    package_name = "test_package"
    with patch("sys.argv", ["write_pydoc.py", package_name]), \
         patch("pydoc.render_doc", return_value="Mocked Documentation"), \
         patch("pydoc.writedoc") as mocked_writedoc, \
         patch("builtins.open", mock_open()) as mocked_file:
        from src.internal.write_pydoc import __main__  # Importing __main__ to simulate script execution
        mocked_file.assert_called_once_with(f"{package_name}.md", "w")
        mocked_file().write.assert_called_once_with("Mocked Documentation")
        mocked_writedoc.assert_called_once_with(package_name)

def test_write_pydoc_text_raises_error_on_invalid_package():
    """Test that _write_pydoc_text raises an error for an invalid package."""
    invalid_package_name = "non_existent_package"
    with pytest.raises(ImportError):
        write_pydoc_text(invalid_package_name)

def test_write_pydoc_HTML_raises_error_on_invalid_package():
    """Test that _write_pydoc_HTML raises an error for an invalid package."""
    invalid_package_name = "non_existent_package"
    with pytest.raises(ImportError):
        write_pydoc_HTML(invalid_package_name)