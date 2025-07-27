# HTML to JSON Contact Parser

A robust Python script to parse an HTML file containing a `<table>` of contacts and convert the data into a structured `contacts.json` file. This script uses BeautifulSoup for reliable parsing and accepts command-line arguments for flexibility.

## Requirements

-   Python 3.8+
-   Dependencies can be installed via pip:
    ```sh
    pip3 install -r requirements.txt
    ```

## Usage

The script is a command-line tool that takes the input HTML file as a required argument and an optional output path.

### Basic Usage

This will read `Kontakte.html` and create `contacts.json` in the current directory.

```sh
python3 parse_contacts.py Kontakte.html
```

### Specifying an Output File

This will read `some-other-file.html` and create the output in a specific location with a different name. The script will automatically create the `output/` directory if it does not exist.

```sh
python3 parse_contacts.py some-other-file.html -o output/my-contacts.json
```

### Help

For a full list of options, use the `--help` flag.

```sh
python3 parse_contacts.py --help
```

### Output

-   A JSON file will be created at the specified output path.
-   This file contains the extracted contact data, ready to be used by the [Contacts Web Application](https://github.com/mtorun0x7cd/contacts).
