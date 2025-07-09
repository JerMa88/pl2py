def write_to_file(output_file_dir:str, text:str, mode:str='a'):
    """Writes text to a specified file.

    Args:
        output_file_dir (str): The path to the output file where the text will be written.
        text (str): The text to write to the file.
        mode (str, optional): The mode in which to open the file. Defaults to 'a'.
            'a' for append, 'w' for write (overwriting existing content), 'x' for exclusive creation.
            'a' is the default mode, which appends to the file if it exists or creates a new file if it does not exist.
            'w' will overwrite the file if it exists, and create a new file if it does not exist.
            'x' will raise an error if the file already exists, ensuring that you do not accidentally overwrite an existing file.
            'r' is not used here as it is for reading only and does not allow writing.
        Raises:
            ValueError: If the mode is not one of 'a', 'w', or 'x'.
        """
    
    with open(output_file_dir, mode) as file:
        """Open the file in the specified mode and write the text to it."""
        if mode not in ['a', 'w', 'x']:
            raise ValueError("Mode must be 'a', 'w', or 'x'.")
        file.write(text)

def __main__():
    """Main function to demonstrate writing to a file.
    parses the command line arguments to get the output file name and text to write.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Write text to a file.")
    parser.add_argument('-o', '--output', type=str, required=True, help='Output file path')
    parser.add_argument('-t', '--text', type=str, required=True, help='Text to write to the file')
    parser.add_argument('--mode', type=str, default='a', choices=['a', 'w', 'x'], help="File mode: 'a' for append, 'w' for write (overwrite), 'x' for exclusive creation")
    args = parser.parse_args()

    # Write to the file
    write_to_file(args.text, args.text, mode=args.mode)