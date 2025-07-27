#
# File:      data-conversion/html-to-json-parser/parse_contacts.py
# Purpose:   Parses an HTML file to extract contact data and convert it to JSON.
# Author:    MTORUN0X7CD
# Version:   3.1
# Last Modified: 2025-07-27
#
# ===================================================================

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Sequence

from bs4 import BeautifulSoup, Tag


def parse_arguments(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Parse an HTML file containing a table of contacts into a structured JSON file."
    )
    parser.add_argument(
        "input_file",
        type=Path,
        help="Path to the source HTML file (e.g., 'Kontakte.html').",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("contacts.json"),
        help="Path to the destination JSON file (default: 'contacts.json').",
    )
    return parser.parse_args(argv)


def extract_contacts_from_html(html_content: str) -> List[Dict[str, str]]:
    """
    Extracts contact data from an HTML string using a robust, scoped search.

    This improved version first finds the primary '<table>' element and only
    then searches for rows within it, preventing data contamination from
    other tables in the document.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    contacts: List[Dict[str, str]] = []

    # Step 1: Isolate the main data table. Assumes the first table is the correct one.
    contact_table = soup.find("table")
    if not isinstance(contact_table, Tag):
        # This handles the case where no table is found in the document.
        return []

    # Step 2: Iterate through all rows '<tr>' within the isolated table.
    for row in contact_table.find_all("tr"):
        # Find all data cells '<td>' within the current row.
        # This is more specific than searching the whole document.
        cells = row.find_all("td")

        # Ensure the row has the expected number of columns (3).
        if len(cells) == 3:
            # .get_text(strip=True) cleanly extracts and strips whitespace from data.
            alias = cells[0].get_text(strip=True)
            name = cells[1].get_text(strip=True)
            phone = cells[2].get_text(strip=True)

            # Add the contact only if all key fields contain data.
            if alias and name and phone:
                contacts.append({"alias": alias, "name": name, "phone": phone})

    return contacts


def main(argv: Sequence[str] | None = None) -> int:
    """
    Main function to orchestrate reading, parsing, and writing.
    Returns an exit code (0 for success, 1 for failure).
    """
    args = parse_arguments(argv)

    if not args.input_file.exists():
        print(f"Error: Input file '{args.input_file}' not found.", file=sys.stderr)
        return 1

    print(f"-> Reading input file: '{args.input_file}'")
    try:
        html_content = args.input_file.read_text(encoding="utf-8")
    except (IOError, PermissionError) as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        return 1

    print("-> Parsing HTML content with scoped search...")
    contacts_data = extract_contacts_from_html(html_content)

    if not contacts_data:
        print(
            "Warning: No contacts found or table could not be parsed.", file=sys.stderr
        )
        return 1

    num_contacts = len(contacts_data)
    print(f"-> Found {num_contacts} contact{'s' if num_contacts != 1 else ''}.")
    print(f"-> Writing to output file: '{args.output}'")

    try:
        # Ensure the output directory exists before writing.
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8") as f:
            json.dump(contacts_data, f, indent=2, ensure_ascii=False)
        print(f"\nSuccess: '{args.output}' has been created successfully.")
    except (IOError, PermissionError) as e:
        print(f"Error writing JSON file: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    # Pass command-line arguments (excluding the script name) to main.
    # This makes the script's logic testable.
    sys.exit(main(sys.argv[1:]))
