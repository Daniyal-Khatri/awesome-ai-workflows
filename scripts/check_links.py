#!/usr/bin/env python3
"""Lightweight internal-link check for the Markdown docs.

- Relative links that point at files (e.g. data/tools.json, CONTRIBUTING.md)
  must exist. A missing file is an ERROR (exit code 1).
- In-page anchors (#...) are checked approximately against heading slugs
  (GitHub's slugification is more subtle than this approximation), so a
  non-matching anchor is only a WARNING and never fails the build.
- External links (http/https/mailto) are not fetched: a successful HTTP
  response would not prove anything about a tool anyway.

Usage: python3 scripts/check_links.py [--root DIR]
Stdlib only.
"""

import argparse
import os
import re
import sys

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
HEADING_RE = re.compile(r"^#{1,6}\s+(.*)$", re.M)


def slugify(heading):
    """Approximate GitHub heading slugs. Two variants are produced because
    GitHub's handling of punctuation (e.g. '&', '—') is not fully
    predictable: one that collapses runs of spaces, one that maps every
    space to a hyphen. An anchor matching either variant counts as found."""
    s = heading.strip().lower()
    s = "".join(c for c in s if c.isalnum() or c in " -_")
    collapsed = "-".join(s.split())
    literal = s.replace(" ", "-")
    return {collapsed, literal}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))),
        help="repository root (default: parent of this script's directory)")
    args = parser.parse_args()
    root = args.root

    docs = ["README.md", "CONTRIBUTING.md", "SECURITY.md"]
    errors, warnings = [], []
    for doc in docs:
        path = os.path.join(root, doc)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            text = f.read()
        slugs = set()
        for h in HEADING_RE.findall(text):
            slugs |= slugify(h)
        # GitHub prefixes a hyphen for headings that start with an emoji.
        slugs |= {"-" + s for s in list(slugs)}
        for target in LINK_RE.findall(text):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            if target.startswith("#"):
                if target[1:] not in slugs:
                    warnings.append(f"{doc}: anchor '{target}' has no "
                                    f"matching heading (approximate check)")
                continue
            file_part = target.split("#", 1)[0]
            if file_part and not os.path.exists(
                    os.path.normpath(os.path.join(root, file_part))):
                errors.append(f"{doc}: linked file '{file_part}' "
                              f"does not exist")

    for w in warnings:
        print(f"WARNING: {w}")
    for e in errors:
        print(f"ERROR: {e}")
    if errors:
        print(f"\nLink check FAILED with {len(errors)} error(s).")
        return 1
    print(f"Link check OK ({len(warnings)} anchor warning(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
