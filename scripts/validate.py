#!/usr/bin/env python3
"""Validate the canonical tool data and its generated outputs.

Checks data/tools.json (the source of truth):
  - valid JSON, top-level list of objects with exactly the expected fields
  - required fields (name, category, url, pricing, description, use) non-empty
  - category is one of the canonical categories (the set in the audited data;
    adding a category means updating this list deliberately)
  - pricing is "Free" or "Freemium"
  - no duplicate names (case-insensitive) and no duplicate URLs (normalized)
  - url (and pricing_url when present) is a well-formed https URL with a host
  - pricing_checked, when present, is a real YYYY-MM-DD date

Consistency hooks (generated files must match the JSON):
  - data/tools.csv rows equal the JSON rows
  - the README "Tools by Category" tables equal the JSON data and sit
    between the generated:tools-tables markers

Exit code: 0 = pass, 1 = one or more errors (all errors are printed).
Usage: python3 scripts/validate.py [--root DIR]
Stdlib only.
"""

import argparse
import csv
import io
import json
import os
import re
import sys
from datetime import datetime
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate import FIELDS, DISPLAY_NAME, PRICING_LABEL, START_MARKER, \
    END_MARKER, TABLES_HEADING, tables_text  # noqa: E402

REQUIRED_NONEMPTY = ["name", "category", "url", "pricing", "description", "use"]
ALLOWED_PRICING = {"Free", "Freemium"}
# Canonical categories, as audited on 2026-10-26. A new category is a
# deliberate change: add it here in the same PR that adds the tool.
CANONICAL_CATEGORIES = [
    "Writing", "Research", "Image", "Video", "Code", "Audio", "Productivity",
    "Presentations", "Websites", "Marketing", "Automation", "Meetings",
    "Design", "Chatbots",
]


def normalize_url(url):
    p = urlparse(url.strip())
    host = p.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    return f"{host}{p.path.rstrip('/')}"


def url_ok(url):
    if not url or any(c.isspace() for c in url):
        return False
    p = urlparse(url)
    return p.scheme == "https" and bool(p.netloc) and "." in p.netloc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))),
        help="repository root (default: parent of this script's directory)")
    args = parser.parse_args()
    root = args.root
    errors = []

    # ---- data/tools.json -------------------------------------------------
    json_path = os.path.join(root, "data", "tools.json")
    try:
        with open(json_path, encoding="utf-8") as f:
            tools = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: data/tools.json is not valid JSON: {exc}")
        return 1
    if not isinstance(tools, list):
        print("ERROR: data/tools.json must be a list of tool objects")
        return 1

    seen_names = {}
    seen_urls = {}
    for i, tool in enumerate(tools):
        where = f"tools.json entry #{i + 1}"
        if not isinstance(tool, dict):
            errors.append(f"{where}: not an object")
            continue
        name = tool.get("name", "?")
        where = f"tools.json '{name}'"
        missing = [k for k in FIELDS if k not in tool]
        extra = [k for k in tool if k not in FIELDS]
        if missing:
            errors.append(f"{where}: missing field(s): {', '.join(missing)}")
        if extra:
            errors.append(f"{where}: unexpected field(s): {', '.join(extra)}")
        for field in REQUIRED_NONEMPTY:
            if not str(tool.get(field, "")).strip():
                errors.append(f"{where}: field '{field}' is empty")
        if tool.get("category") not in CANONICAL_CATEGORIES:
            errors.append(
                f"{where}: category '{tool.get('category')}' is not one of "
                f"the canonical categories")
        if tool.get("pricing") not in ALLOWED_PRICING:
            errors.append(
                f"{where}: pricing '{tool.get('pricing')}' must be Free "
                f"or Freemium")
        desc = str(tool.get("description", ""))
        if len(desc) > 100:
            errors.append(
                f"{where}: description is {len(desc)} characters "
                f"(max 100) — shorten it, do not truncate mid-sentence")
        if not url_ok(str(tool.get("url", ""))):
            errors.append(f"{where}: malformed url '{tool.get('url')}'")
        purl = str(tool.get("pricing_url", ""))
        if purl and not url_ok(purl):
            errors.append(f"{where}: malformed pricing_url '{purl}'")
        pdate = str(tool.get("pricing_checked", ""))
        if pdate:
            try:
                datetime.strptime(pdate, "%Y-%m-%d")
            except ValueError:
                errors.append(
                    f"{where}: pricing_checked '{pdate}' is not a "
                    f"YYYY-MM-DD date")
        key = str(tool.get("name", "")).strip().lower()
        if key in seen_names:
            errors.append(f"{where}: duplicate tool name (also entry "
                          f"#{seen_names[key] + 1})")
        else:
            seen_names[key] = i
        ukey = normalize_url(str(tool.get("url", "")))
        if ukey in seen_urls:
            errors.append(f"{where}: duplicate URL '{tool.get('url')}' "
                          f"(also used by '{seen_urls[ukey]}')")
        else:
            seen_urls[ukey] = name

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        print(f"\nValidation FAILED with {len(errors)} error(s).")
        return 1

    # ---- data/tools.csv consistency --------------------------------------
    csv_path = os.path.join(root, "data", "tools.csv")
    try:
        with open(csv_path, encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
    except OSError:
        print("ERROR: data/tools.csv is missing — run scripts/generate.py")
        return 1
    expected = [{k: tool.get(k, "") for k in FIELDS} for tool in tools]
    if rows != expected:
        print("ERROR: data/tools.csv does not match data/tools.json — "
              "run scripts/generate.py")
        return 1

    # ---- README tables consistency ---------------------------------------
    readme_path = os.path.join(root, "README.md")
    with open(readme_path, encoding="utf-8") as f:
        readme = f.read()
    if START_MARKER not in readme or END_MARKER not in readme:
        print("ERROR: README.md is missing the generated:tools-tables "
              "markers — run scripts/generate.py")
        return 1
    region = readme.split(START_MARKER, 1)[1].split(END_MARKER, 1)[0].strip()
    if region != tables_text(tools).strip():
        print("ERROR: README.md tool tables do not match data/tools.json — "
              "run scripts/generate.py")
        return 1
    if TABLES_HEADING not in readme:
        print(f"ERROR: README.md is missing the '{TABLES_HEADING}' heading")
        return 1

    cats = {t["category"] for t in tools}
    print(f"OK: {len(tools)} tools, {len(cats)} categories — tools.json is "
          f"valid and tools.csv + README tables match it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
