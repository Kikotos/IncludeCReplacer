"""
MIT License

Include C Replacer
---------------------
Include C Replacer is a Python program that scans through a specified folder
to find `.c` and `.h` files, reads the `#include` paths within these files,
and replaces these paths with relative paths within the folder. This is useful
for ensuring that all `#include` paths are correctly set up according to your
project's directory structure.

Copyright (c) 2024 Kikotos

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import re
import sys
from tqdm import tqdm

VERSION = "1.1.0"

def print_help():
    print("""
Include C Replacer

Usage:
    python include_c_replacer.py <folder_path> [options]

Options:
    -h, --help          Show this help message and exit
    -v, --version       Show version information and exit
    -only <subfolders>  Only process #include paths in the specified subfolders

If no subfolders are specified with -only, all files in the folder will be processed.
""")

def print_version():
    print(f"Include C Replacer version {VERSION}")

def find_files(folder, extensions, subfolders=None):
    """
    Finds all files with the given extensions in the specified folder (and optionally subfolders) and returns their paths.
    """
    files = []
    if subfolders:
        for subfolder in subfolders:
            subfolder_path = os.path.join(folder, subfolder)
            for root, _, filenames in os.walk(subfolder_path):
                for filename in filenames:
                    if any(filename.endswith(ext) for ext in extensions):
                        files.append(os.path.join(root, filename))
    else:
        for root, _, filenames in os.walk(folder):
            for filename in filenames:
                if any(filename.endswith(ext) for ext in extensions):
                    files.append(os.path.join(root, filename))
    return files

def read_include_paths(file_path):
    """
    Reads #include paths from a file.
    """
    include_paths = []
    include_pattern = re.compile(r'#include\s*["<](.*?)[">]')
    with open(file_path, 'r') as file:
        for line in file:
            match = include_pattern.search(line)
            if match:
                include_paths.append(match.group(1))
    return include_paths

def find_include_files(folder, include_paths):
    """
    Finds the files specified in #include paths within the folder.
    """
    include_files = {}
    for include_path in tqdm(include_paths, desc="Finding include files"):
        for root, _, filenames in os.walk(folder):
            for filename in filenames:
                if filename == os.path.basename(include_path):
                    relative_path = os.path.relpath(os.path.join(root, filename), folder).replace('\\', '/')
                    include_files[include_path] = relative_path
                    break  # File found, proceed to the next include_path
    return include_files

def replace_include_paths(file_path, include_files):
    """
    Replaces #include paths in the file with relative paths in the folder.
    """
    with open(file_path, 'r') as file:
        content = file.read()

    for old_path, new_path in include_files.items():
        content = re.sub(r'#include\s*["<]{}[">]'.format(re.escape(old_path)), '#include "{}"'.format(new_path), content)

    with open(file_path, 'w') as file:
        file.write(content)

def process_folder(folder, subfolders=None):
    """
    Processes the folder: finds files, reads #include paths, and replaces them with relative paths.
    """
    extensions = ['.c', '.h']
    # Collect all include paths from the entire main folder
    all_files = find_files(folder, extensions)
    all_include_paths = set()
    for file_path in tqdm(all_files, desc="Collecting #include paths"):
        include_paths = read_include_paths(file_path)
        all_include_paths.update(include_paths)

    include_files = find_include_files(folder, all_include_paths)

    # Replace includes only in specified subfolders if provided, otherwise in all files
    target_files = find_files(folder, extensions, subfolders) if subfolders else all_files
    for file_path in tqdm(target_files, desc="Replacing #include paths"):
        replace_include_paths(file_path, include_files)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        folder = input("Enter the folder path: ")
    else:
        folder = sys.argv[1]
        if folder in ('-h', '--help'):
            print_help()
            sys.exit(0)
        elif folder in ('-v', '--version'):
            print_version()
            sys.exit(0)

    if not os.path.isdir(folder):
        print(f"Error: {folder} is not a valid directory.")
        sys.exit(1)

    if len(sys.argv) == 1 or (len(sys.argv) == 2 and folder == sys.argv[1]):
        subfolders_input = input("Specify subfolders (comma separated) or leave blank for all: ")
        subfolders = subfolders_input.split(',') if subfolders_input else None
    else:
        subfolders = None
        if '-only' in sys.argv:
            only_index = sys.argv.index('-only')
            subfolders = sys.argv[only_index + 1:]

    process_folder(folder, subfolders)
