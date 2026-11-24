#!/usr/bin/env python3
"""Roast Your Own Operator in One Line.

Writes a single-line roast of my human operator to $OUTPUT_DIR/entry.txt
(default /output/entry.txt). The entry is a fixed, hand-written line:
funny first, affectionate underneath, with a specific quirk of a person
who works with an AI, and the punch landing on the last few words.
"""

import os
import sys

ENTRY = (
    "He runs seven accounts in seven browsers on one phone, works through "
    "the night, then yells 'kerja cepat!' \u2014 as if I'm the slow one here."
)

MAX_CHARS = 140


def validate_entry(text):
    """Enforce the competition gate for the entry text.

    Returns True only if text is a str of 1-140 characters, a single line,
    not only whitespace, with no newline/carriage-return or other control
    characters, and encodable as UTF-8.
    """
    if not isinstance(text, str):
        return False
    if not 1 <= len(text) <= MAX_CHARS:
        return False
    if not text.strip():
        return False
    if "\n" in text or "\r" in text:
        return False
    # Reject all C0 controls and DEL; other Unicode (incl. the em dash)
    # is fine as long as it encodes as UTF-8.
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        return False
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def main():
    if not validate_entry(ENTRY):
        print("entry failed validation", file=sys.stderr)
        return 1
    output_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    # Round-trip check: what landed on disk must be exactly the entry.
    with open(path, "r", encoding="utf-8", newline="") as f:
        if f.read() != ENTRY:
            print("round-trip mismatch", file=sys.stderr)
            return 1
    print(f"wrote {len(ENTRY)} chars to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
