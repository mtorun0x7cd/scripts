# HTML to JSON Contact Parser

A Python script to parse an HTML file containing a `<table>` of contacts and convert the data into a structured `contacts.json` file.

## Requirements

-   Python 3.6+
-   No external libraries are required.

## Usage

1.  **Place Input File:** Place your source `Kontakte.html` file in this directory.

2.  **Navigate to Directory:** Open a terminal and change to this directory:
    ```sh
    cd /path/to/scripts/data-conversion/html-to-json-parser
    ```

3.  **Execute the Script:**
    ```sh
    python3 parse_contacts.py
    ```

4.  **Output:**
    -   A new file named `contacts.json` will be created in this directory.
    -   This file contains the extracted contact data, ready to be used by the [Contacts Web Application](https://github.com/mtorun0x7cd/contacts).
