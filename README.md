
# Include C Replacer

Include C Replacer is a Python program designed to scan through a specified folder, locate `.c` and `.h` files, read the `#include` paths within these files, and replace these paths with relative paths within the folder. This ensures that all `#include` paths are correctly set up according to your project's directory structure.

## Features

- **File Scanning:** Scans for `.c` and `.h` files in a specified folder.
- **Path Reading:** Reads `#include` paths from the files.
- **Path Replacement:** Replaces `#include` paths with relative paths within the folder.
- **Progress Bar:** Displays a progress bar for reading and replacing paths for better user experience.

## Prerequisites

- **Python 3.x**
- **tqdm library** for progress bars

You can install the `tqdm` library using pip:

```sh
pip install tqdm
```

## Usage

1. **Clone or Download:**
   Clone this repository or download the script to your local machine.
   
2. **Install Dependencies:**
   Ensure you have Python 3.x installed and install the `tqdm` library.

3. **Run the Script:**
   Run the script from the command line, providing the folder path as an argument. If no argument is provided, the script will prompt you to enter the folder path.

### Running the Script

To run the script, navigate to the directory where the script is located and run the following command:

```sh
python include_c_replacer.py [options] <folder_path>
```

Replace `<folder_path>` with the path to the folder you want to process.

### Options

- `-h, --help`: Show the help message and exit.
- `-v, --version`: Show version information and exit.
- `-only <subfolders>`: Only process `#include` paths in the specified subfolders.

If no subfolders are specified with `-only`, all files in the folder will be processed.

If no arguments are provided, the script will prompt you to enter the folder path and optionally specify subfolders.

### Example

Suppose you have a project structure like this:

```
/project
    main.c
    utils/
        utils.c
        utils.h
    includes/
        config.h
```

And the `main.c` file contains:

```c
#include "utils.h"
#include "config.h"
```

If you run the script with `/project` as the folder path:

```sh
python include_c_replacer.py /path/to/project
```

It will update the `main.c` file to:

```c
#include "utils/utils.h"
#include "includes/config.h"
```

The script ensures that all `#include` paths are relative to the project folder.

If you only want to process specific subfolders, such as `utils` and `includes`:

```sh
python include_c_replacer.py /path/to/project -only utils includes
```

Alternatively, if no arguments are provided, the script will prompt you for the folder path and subfolders:

```sh
python include_c_replacer.py
```

```
Enter the folder path: /path/to/project
Specify subfolders (comma separated) or leave blank for all: utils,includes
```

## Code Explanation

### find_files(folder, extensions, subfolders=None)

Finds all files with the given extensions in the specified folder (and optionally subfolders) and returns their paths.

### read_include_paths(file_path)

Reads `#include` paths from a file.

### find_include_files(folder, include_paths)

Finds the files specified in `#include` paths within the folder.

### replace_include_paths(file_path, include_files)

Replaces `#include` paths in the file with relative paths in the folder.

### process_folder(folder, subfolders=None)

Processes the folder: finds files, reads `#include` paths, and replaces them with relative paths.

## Contributing

Contributions are welcome! If you would like to contribute to this project, please feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License.

---
