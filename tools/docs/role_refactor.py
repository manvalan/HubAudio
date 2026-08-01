#!/usr/bin/env python3
"""
HubAudio Documentation Role Refactor

Replaces hardware implementation names with architectural role names.

Example:

    python role_refactor.py docs --dry-run
    python role_refactor.py docs --write
"""

from pathlib import Path
import argparse
import re
import sys


# ----------------------------------------------------------------------
# Mapping
# ----------------------------------------------------------------------

ROLE_MAP = {
    "ADAU1467": "Audio Processor",
    "ESP32-S3": "System Controller",
    "Si4684": "Radio Receiver",
    "BT1026": "Bluetooth Receiver",
    "BT1035": "Bluetooth Transmitter",
    "PCS2P2309NZ": "Clock Buffer",
    "BQ24074": "Battery Charger",
    "BQ27441": "Fuel Gauge",
    "TPS65217": "Power Manager",
    "25AA1024": "Audio EEPROM",
}


# ----------------------------------------------------------------------
# Ignore folders
# ----------------------------------------------------------------------

IGNORE = {
    "datasheets",
    "hardware",
    "firmware",
    ".git",
    "__pycache__",
}


# ----------------------------------------------------------------------
# Replace inside one file
# ----------------------------------------------------------------------

def process_file(path: Path, write: bool):

    text = path.read_text(encoding="utf-8")

    original = text

    replacements = []

    for implementation, role in ROLE_MAP.items():

        pattern = r"\b" + re.escape(implementation) + r"\b"

        matches = len(re.findall(pattern, text))

        if matches:

            text = re.sub(pattern, role, text)

            replacements.append((implementation, role, matches))

    if not replacements:
        return False, []

    print(f"\n{path}")

    total = 0

    for old, new, count in replacements:

        total += count

        print(f"  {old:18} -> {new:24} ({count})")

    print(f"  Total replacements: {total}")

    if write:
        path.write_text(text, encoding="utf-8")

    return True, replacements


# ----------------------------------------------------------------------
# Scan tree
# ----------------------------------------------------------------------

def scan(root: Path, write: bool):

    modified = 0

    files = 0

    for file in root.rglob("*.md"):

        if any(part in IGNORE for part in file.parts):
            continue

        changed, _ = process_file(file, write)

        if changed:
            modified += 1

        files += 1

    print("\n----------------------------------------")

    print(f"Markdown scanned : {files}")
    print(f"Files modified   : {modified}")

    if write:
        print("\nChanges written to disk.")
    else:
        print("\nDry run completed.")


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "path",
        help="Root documentation directory"
    )

    parser.add_argument(
        "--write",
        action="store_true",
        help="Write modifications"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only show modifications"
    )

    args = parser.parse_args()

    if args.write and args.dry_run:
        print("Choose either --write or --dry-run")
        sys.exit(1)

    root = Path(args.path)

    if not root.exists():
        print("Directory not found.")
        sys.exit(1)

    scan(root, write=args.write)


if __name__ == "__main__":
    main()