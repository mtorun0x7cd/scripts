#
# File:      data-conversion/html-to-json-parser/parse_contacts.py
# Purpose:   Parses an HTML file to extract contact data and convert it to JSON.
# Author:    MTORUN0X7CD
# Version:   2.0
# Last Modified: 2025-07-26
#
# ===================================================================

import json
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Dict, List

# --- Configuration ---
INPUT_HTML_FILE: Path = Path("Kontakte.html")
OUTPUT_JSON_FILE: Path = Path("contacts.json")


class ContactParser(HTMLParser):
    """
    A custom HTML parser to extract contact data from table rows.
    It specifically looks for <tr> tags and captures the data within
    the subsequent three <td> tags.
    """

    def __init__(self) -> None:
        super().__init__()
        self.contacts: List[Dict[str, str]] = []
        self._in_tr: bool = False
        self._in_td: bool = False
        self._current_contact_data: List[str] = []
        self._td_count: int = 0

    def handle_starttag(self, tag: str, attrs: Any) -> None:
        if tag == "tr":
            self._in_tr = True
            self._current_contact_data = []
            self._td_count = 0
        elif self._in_tr and tag == "td":
            self._in_td = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "tr":
            self._in_tr = False
            if len(self._current_contact_data) == 3:
                contact_dict = {
                    "alias": self._current_contact_data[0],
                    "name": self._current_contact_data[1],
                    "phone": self._current_contact_data[2],
                }
                self.contacts.append(contact_dict)
        elif tag == "td":
            self._in_td = False
            self._td_count += 1

    def handle_data(self, data: str) -> None:
        if self._in_td and self._td_count < 3:
            clean_data = data.strip()
            if clean_data:
                self._current_contact_data.append(clean_data)


def main() -> None:
    """
    Main function to read the HTML, parse it, and write the JSON output.
    """
    print(f"-> Reading input file: '{INPUT_HTML_FILE}'")
    if not INPUT_HTML_FILE.exists():
        print(f"\nError: Input file '{INPUT_HTML_FILE}' not found.")
        print("Please place it in the same directory as this script.")
        return

    try:
        html_content = INPUT_HTML_FILE.read_text(encoding="utf-8")
    except Exception as e:
        print(f"\nError reading file: {e}")
        return

    print("-> Parsing HTML content...")
    parser = ContactParser()
    parser.feed(html_content)
    contacts_data = parser.contacts

    if not contacts_data:
        print("\nWarning: No contact data was found in the HTML file.")
        return

    print(f"-> Found {len(contacts_data)} contacts.")
    print(f"-> Writing to output file: '{OUTPUT_JSON_FILE}'")
    try:
        with OUTPUT_JSON_FILE.open("w", encoding="utf-8") as f:
            json.dump(contacts_data, f, indent=2, ensure_ascii=False)
        print(f"\nSuccess: '{OUTPUT_JSON_FILE}' has been created successfully.")
    except Exception as e:
        print(f"\nError writing JSON file: {e}")


if __name__ == "__main__":
    main()
