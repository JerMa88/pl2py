import os
import pytest
from src.internal.write_to_file import _write_to_file

@pytest.fixture
def temp_file(tmp_path):
    """Fixture to create a temporary file for testing."""
    temp_file = tmp_path / "test_file.txt"
    yield temp_file
    if temp_file.exists():
        temp_file.unlink()

def test_write_to_file_append_mode(temp_file):
    """Test writing to a file in append mode."""
    _write_to_file(str(temp_file), "Hello, world!", mode='a')
    _write_to_file(str(temp_file), " Appending text.", mode='a')
    with open(temp_file, 'r') as file:
        content = file.read()
    assert content == "Hello, world! Appending text."

def test_write_to_file_write_mode(temp_file):
    """Test writing to a file in write mode (overwrite)."""
    _write_to_file(str(temp_file), "Initial text.", mode='w')
    _write_to_file(str(temp_file), "Overwritten text.", mode='w')
    with open(temp_file, 'r') as file:
        content = file.read()
    assert content == "Overwritten text."

def test_write_to_file_exclusive_mode(temp_file):
    """Test writing to a file in exclusive creation mode."""
    _write_to_file(str(temp_file), "Exclusive text.", mode='x')
    with open(temp_file, 'r') as file:
        content = file.read()
    assert content == "Exclusive text."
    with pytest.raises(FileExistsError):
        _write_to_file(str(temp_file), "This should fail.", mode='x')

def test_write_to_file_invalid_mode(temp_file):
    """Test providing an invalid mode."""
    _write_to_file(str(temp_file), "Create this file so no FileNotFoundError.", mode='w')
    with pytest.raises(ValueError):
        _write_to_file(str(temp_file), "Invalid mode test.", mode='r')

def test_write_to_nonexistent_directory():
    """Test writing to a file in a nonexistent directory."""
    with pytest.raises(FileNotFoundError):
        _write_to_file("/nonexistent_dir/test_file.txt", "This should fail.", mode='w')