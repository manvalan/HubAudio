#!/usr/bin/env python3
"""
HubAudio Architecture Linter

Checks that architecture documentation uses architectural roles
instead of hardware implementation names.

Usage

    python architecture_linter.py docs --check

    python architecture_linter.py docs --fix

    python architecture_linter.py docs --report report.md
"""

from __future__ import annotations

import argparse
import re
import sys

from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List

import yaml


# ==========================================================
# Configuration
# ==========================================================

TARGET_DIRS = {
    "adr",
    "architecture",
    "engineering",
}

SKIP_FILE_PATTERNS = (
    "-Hardware-Architecture.md",
    "-Hardware.md",
    "-Datasheet.md",
)

CODE_BLOCK = re.compile(
    r"```.*?```",
    flags=re.DOTALL
)

INLINE_CODE = re.compile(
    r"`[^`]+`"
)

ASCII_DIAGRAM = re.compile(
    r"^[\s\|\+\-\>\<]+$"
)


# ==========================================================
# Data model
# ==========================================================

@dataclass
class Role:

    role: str

    implementation: str

    aliases: List[str]


@dataclass
class Finding:

    line: int

    implementation: str

    role: str


# ==========================================================
# Role database
# ==========================================================

class RoleDatabase:

    def __init__(self, filename: Path):

        self.roles: List[Role] = []

        self.load(filename)

    def load(self, filename: Path):

        if not filename.exists():
            raise FileNotFoundError(filename)

        data = yaml.safe_load(
            filename.read_text(encoding="utf8")
        )

        for role_name, cfg in data["roles"].items():

            self.roles.append(
                Role(
                    role=role_name,
                    implementation=cfg["implementation"],
                    # aliases=cfg.get("aliases", [])
                    aliases=list(
                            set(cfg.get("aliases", []))
                            -
                            {cfg["implementation"]}
                        )
                )
            )


# ==========================================================
# Markdown parser
# ==========================================================

class MarkdownCleaner:

    """
    Temporarily removes code blocks before scanning.
    """

    def __init__(self):

        self.blocks = []

    def protect(self, text: str):

        def repl(match):

            token = f"@@BLOCK{len(self.blocks)}@@"

            self.blocks.append(match.group(0))

            return token

        text = CODE_BLOCK.sub(repl, text)

        text = INLINE_CODE.sub(repl, text)

        return text

    def restore(self, text: str):

        for i, block in enumerate(self.blocks):

            text = text.replace(
                f"@@BLOCK{i}@@",
                block
            )

        return text


# ==========================================================
# Linter
# ==========================================================

class ArchitectureLinter:

    def __init__(
        self,
        docs_root: Path,
        roles: RoleDatabase
    ):

        self.root = docs_root

        self.roles = roles

        self.findings: Dict[Path, List[Finding]] = {}

        self.checked = 0

        self.modified = 0

    # ------------------------------------------------------

    def iter_files(self):

        for md in self.root.rglob("*.md"):

            rel = md.relative_to(self.root)

            if len(rel.parts) == 0:
                continue

            first = rel.parts[0]

            if first not in TARGET_DIRS:
                continue

            skip = False

            for pattern in SKIP_FILE_PATTERNS:

                if md.name.endswith(pattern):
                    skip = True
                    break

            if skip:
                continue

            yield md

    # ------------------------------------------------------

    def analyse_file(
        self,
        filename: Path
    ):

        cleaner = MarkdownCleaner()

        original = filename.read_text(
            encoding="utf8"
        )

        text = cleaner.protect(original)

        findings = []

        lines = text.splitlines()

        for lineno, line in enumerate(lines, start=1):

            #
            # Ignore implementation section
            #
            if ASCII_DIAGRAM.match(line):
                continue

            if "Current implementation" in line:
                continue
            if line.lstrip().startswith("#"):
                continue
            #
            # Ignore titles like
            #
            # ADAU1467 Hardware Architecture
            #

            if line.startswith("#") and "Hardware" in line:
                continue

            for role in self.roles.roles:

                names = [
                    role.implementation,
                    *role.aliases
                ]

                for implementation in names:

                    pattern = (
                        r"\b"
                        + re.escape(implementation)
                        + r"\b"
                    )

                    if re.search(pattern, line):

                        findings.append(
                            Finding(
                                line=lineno,
                                implementation=implementation,
                                role=role.role
                            )
                        )

        self.findings[filename] = findings

        self.checked += 1
            # ------------------------------------------------------

    def check(self):

        for file in self.iter_files():

            self.analyse_file(file)

    # ------------------------------------------------------

    def fix(self):

        for filename in self.iter_files():

            cleaner = MarkdownCleaner()

            original = filename.read_text(
                encoding="utf8"
            )

            protected = cleaner.protect(original)

            text = protected

            changed = False

            #
            # sostituzioni
            #

            for role in self.roles.roles:

                names = [
                    role.implementation,
                    *role.aliases
                ]

                for implementation in names:

                    pattern = (
                        r"\b"
                        + re.escape(implementation)
                        + r"\b"
                    )

                    new_text = re.sub(
                        pattern,
                        role.role,
                        text
                    )

                    if new_text != text:

                        changed = True
                        text = new_text

            text = cleaner.restore(text)

            if changed:

                filename.write_text(
                    text,
                    encoding="utf8"
                )

                self.modified += 1

    # ------------------------------------------------------

    def print_report(self):

        issues = 0

        print()

        print("=" * 70)
        print("HubAudio Architecture Linter")
        print("=" * 70)

        for filename in sorted(self.findings):

            findings = self.findings[filename]

            if not findings:
                continue

            issues += len(findings)

            rel = filename.relative_to(self.root)

            print()
            print(rel)
            print("-" * len(str(rel)))

            for f in findings:

                print(
                    f"line {f.line:4d} : "
                    f"{f.implementation}"
                    f"  ->  "
                    f"{f.role}"
                )

        print()
        print("=" * 70)
        print(f"Files checked : {self.checked}")
        print(f"Issues found  : {issues}")
        print(f"Files changed : {self.modified}")
        print("=" * 70)

    # ------------------------------------------------------

    def save_report(
        self,
        filename: Path
    ):

        issues = 0

        with filename.open(
            "w",
            encoding="utf8"
        ) as fp:

            fp.write("# HubAudio Architecture Report\n\n")

            for md in sorted(self.findings):

                findings = self.findings[md]

                if not findings:
                    continue

                rel = md.relative_to(self.root)

                fp.write(f"## {rel}\n\n")

                for f in findings:

                    issues += 1

                    fp.write(
                        f"- Line {f.line}: "
                        f"`{f.implementation}` "
                        f"→ "
                        f"`{f.role}`\n"
                    )

                fp.write("\n")

            fp.write("---\n\n")
            fp.write(f"Files checked: {self.checked}\n\n")
            fp.write(f"Issues found: {issues}\n")


# ==========================================================
# CLI
# ==========================================================

def main():

    parser = argparse.ArgumentParser(
        description="HubAudio Architecture Linter"
    )

    parser.add_argument(
        "docs",
        help="Documentation root"
    )

    parser.add_argument(
        "--roles",
        default="tools/docs/roles.yml",
        help="roles.yml"
    )

    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "--check",
        action="store_true"
    )

    parser.add_argument(
        "--report",
        help="Write markdown report"
    )

    parser.add_argument(
        "--fix",
        action="store_true",
        help="Apply architecture naming fixes"
    )   

    args = parser.parse_args()

    docs = Path(args.docs)

    if not docs.exists():

        print("Documentation directory not found.")
        sys.exit(1)

    role_db = RoleDatabase(
        Path(args.roles)
    )

    linter = ArchitectureLinter(
        docs,
        role_db
    )

    linter.check()

    if args.fix:

        print()
        print("=" * 70)
        print("Applying architecture fixes")
        print("=" * 70)

        linter.fix()

        #
        # Ricontrolla dopo la correzione
        #

        linter.findings.clear()
        linter.checked = 0

        linter.check()

    linter.print_report()

    if args.report:

        linter.save_report(
            Path(args.report)
        )

        print()
        print("Report written to")
        print(args.report)
    

if __name__ == "__main__":

    main()