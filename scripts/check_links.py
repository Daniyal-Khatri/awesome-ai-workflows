#!/usr/bin/env python3
"""Internal-link check for the Markdown docs, with exact GitHub anchors.

Rules enforced (any violation is an ERROR, exit code 1):
- Relative links that point at files (e.g. data/tools.json) must exist.
- In-page anchors (#...) must exactly match the anchor GitHub generates
  for some heading in the same document. The slug algorithm below matches
  GitHub's observed behavior for plain-text headings: lowercase, remove
  punctuation, turn every space into a hyphen ("Blogger / Creator Stack"
  -> "blogger--creator-stack").
- A heading must NOT start with an emoji or symbol. GitHub strips a
  leading emoji but leaves an invisible character or a leading hyphen in
  the anchor ("-short-form-video-stack", or worse, anchors containing
  zero-width characters), which silently breaks normal links. Keep emojis
  in body text, not at the start of headings.
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
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$", re.M)


def github_slug(heading):
    """GitHub anchor for a plain-text heading (ASCII text)."""
    s = heading.strip().lower()
    s = "".join(c for c in s if c.isalnum() or c in " -_")
    return s.replace(" ", "-")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))),
        help="repository root (default: parent of this script's directory)")
    args = parser.parse_args()
    root = args.root

    docs = ["README.md", "CONTRIBUTING.md", "SECURITY.md"]
    errors = []
    for doc in docs:
        path = os.path.join(root, doc)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            text = f.read()

        # Collect heading slugs (GitHub suffixes duplicates with -1, -2...).
        slugs, seen = set(), {}
        for hashes, h in HEADING_RE.findall(text):
            if len(hashes) >= 2 and h and ord(h[0]) > 127:
                errors.append(
                    f"{doc}: heading '{h}' starts with an emoji/symbol — "
                    "GitHub generates a broken anchor for it. Move the "
                    "emoji out of the heading.")
            base = github_slug(h)
            if base in seen:
                seen[base] += 1
                slugs.add(f"{base}-{seen[base]}")
            else:
                seen[base] = 0
                slugs.add(base)

        for target in LINK_RE.findall(text):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            if target.startswith("#"):
                if target[1:] not in slugs:
                    errors.append(f"{doc}: anchor '{target}' matches no "
                                  "heading in this document")
                continue
            file_part = target.split("#", 1)[0]
            if file_part and not os.path.exists(
                    os.path.normpath(os.path.join(root, file_part))):
                errors.append(f"{doc}: linked file '{file_part}' "
                              "does not exist")

    for e in errors:
        print(f"ERROR: {e}")
    if errors:
        print(f"\nLink check FAILED with {len(errors)} error(s).")
        return 1
    print("Link check OK: every anchor matches a heading, every linked "
          "file exists, no emoji-led headings.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
