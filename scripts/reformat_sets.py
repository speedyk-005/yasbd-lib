"""Reformat set literals in rule files."""

from __future__ import annotations

import re
from pathlib import Path

RULES_DIR = Path("src/yasbd/rules")

MAX_LINE = 65
ITEM_INDENT = " " * 8

SET_START_RE = re.compile(
    r"""
    ^(
        [ ]{4}                      # Class attribute indentation.
        ([A-Z_]+)                   # Attribute name.
        \s*=\s*
        (?:\w+Rules\.\w+\s*\|\s*)?   # Optional inherited set.
        \{
    )\s*$
    """,
    re.VERBOSE,
)


def pack_items(items: list[str]) -> list[str]:
    """Pack items into lines no longer than MAX_LINE."""
    lines: list[str] = []
    current = ITEM_INDENT

    # Sort only when a rewrite is required.
    # This keeps normal runs from creating unnecessary diffs.
    for item in sorted(set(items), key=str.lower):
        piece = f"{item}, "

        if len(current + piece) <= MAX_LINE:
            current += piece
        else:
            lines.append(current.rstrip())
            current = ITEM_INDENT + piece

    if current.strip():
        lines.append(current.rstrip())

    return lines


def flush_items(
    out: list[str],
    items: list[str],
    original_lines: list[str],
) -> None:
    """Write buffered items, preserving already valid formatting."""
    if not items:
        return

    # Avoid touching sets that are already within the line limit.
    # This prevents pointless sorting and formatting churn.
    if all(len(line.rstrip()) <= MAX_LINE for line in original_lines):
        out.extend(original_lines)
    else:
        out.extend(f"{line}\n" for line in pack_items(items))

    items.clear()
    original_lines.clear()


def reformat_set_block(text: str) -> str:
    """Reformat class-level set literals."""
    lines = text.splitlines(keepends=True)

    out: list[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Only process class attributes that look like set definitions.
        if not SET_START_RE.match(line):
            out.append(line)
            i += 1
            continue

        out.append(line)
        i += 1

        items: list[str] = []
        original_lines: list[str] = []

        while i < len(lines):
            current = lines[i]
            stripped = current.strip()

            # Closing brace ends the current set block.
            if stripped == "}":
                flush_items(out, items, original_lines)
                out.append(current)
                i += 1
                break

            # Keep comments and blank lines attached to their section.
            # Flush pending items before preserving them.
            if not stripped or stripped.startswith("#"):
                flush_items(out, items, original_lines)
                out.append(current)
                i += 1
                continue

            original_lines.append(current)
            items.extend(re.findall(r'"[^"]*"', stripped))
            i += 1

    return "".join(out)


def main() -> None:
    """Reformat all rule files."""
    # Skip files that are templates or package initializers.
    files = [
        path
        for path in sorted(RULES_DIR.glob("*.py"))
        if path.name not in {"_template.py", "__init__.py"}
    ]

    for path in files:
        original = path.read_text()
        reformatted = reformat_set_block(original)

        if original == reformatted:
            continue

        changes = sum(
            before != after
            for before, after in zip(
                original.splitlines(),
                reformatted.splitlines(),
                strict=False,
            )
        )

        print(f"{path.name}: {changes} line(s) changed")
        path.write_text(reformatted)


if __name__ == "__main__":
    main()
