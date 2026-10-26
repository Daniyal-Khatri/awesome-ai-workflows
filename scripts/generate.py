#!/usr/bin/env python3
"""Regenerate derived files from the canonical data source.

Source of truth: data/tools.json
Generated outputs:
  - data/tools.csv            (full export of the JSON)
  - README.md                 (only the "Tools by Category" tables region,
                               delimited by the generated:tools-tables markers)

Everything else in README.md (prose, workflow stacks, recipes, navigation)
is left untouched. Run scripts/validate.py afterwards to confirm consistency.

Usage: python3 scripts/generate.py [--root DIR]
Stdlib only.
"""

import argparse
import csv
import io
import json
import os
import sys

FIELDS = ["name", "category", "url", "pricing", "description", "use",
          "pricing_url", "pricing_checked"]

START_MARKER = "<!-- generated:tools-tables:start -->"
END_MARKER = "<!-- generated:tools-tables:end -->"
TABLES_HEADING = "## 🧰 Tools by Category"

# Display headings used in the README for some canonical category names.
DISPLAY_NAME = {
    "Writing": "Writing & Chat",
    "Websites": "Website Builders",
    "Meetings": "Meetings & Notes",
    "Chatbots": "Voice & Chatbots",
}
PRICING_LABEL = {"Free": "🆓 Free", "Freemium": "🔓 Freemium"}


def load_tools(root):
    with open(os.path.join(root, "data", "tools.json"), encoding="utf-8") as f:
        return json.load(f)


def csv_text(tools):
    buf = io.StringIO(newline="")
    writer = csv.DictWriter(buf, fieldnames=FIELDS)
    writer.writeheader()
    for tool in tools:
        writer.writerow({k: tool.get(k, "") for k in FIELDS})
    return buf.getvalue()


def tables_text(tools):
    """Markdown for all category tables, in JSON first-appearance order."""
    categories = []
    for tool in tools:
        if tool["category"] not in categories:
            categories.append(tool["category"])
    sections = []
    for category in categories:
        lines = [f"### {DISPLAY_NAME.get(category, category)}", "",
                 "| Tool | What it does | Pricing | Best for |",
                 "| --- | --- | --- | --- |"]
        for tool in tools:
            if tool["category"] != category:
                continue
            desc = tool["description"].replace("|", "\\|")
            use = tool["use"].replace("|", "\\|")
            lines.append(
                f"| [{tool['name']}]({tool['url']}) | {desc} "
                f"| {PRICING_LABEL[tool['pricing']]} | {use} |")
        sections.append("\n".join(lines))
    return "\n\n".join(sections)


def regenerate_readme(root, tools):
    path = os.path.join(root, "README.md")
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    try:
        heading = next(i for i, l in enumerate(lines)
                       if l.strip() == TABLES_HEADING)
    except StopIteration:
        sys.exit(f"error: '{TABLES_HEADING}' heading not found in README.md")
    # The generated region runs from just after the heading to just before
    # the next level-2 heading.
    end = next(i for i in range(heading + 1, len(lines))
               if lines[i].startswith("## "))
    block = ["", START_MARKER, "", tables_text(tools), "", END_MARKER, ""]
    lines[heading + 1:end] = block
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))),
        help="repository root (default: parent of this script's directory)")
    args = parser.parse_args()

    tools = load_tools(args.root)
    with open(os.path.join(args.root, "data", "tools.csv"), "w",
              encoding="utf-8", newline="") as f:
        f.write(csv_text(tools))
    regenerate_readme(args.root, tools)
    print(f"Generated data/tools.csv and README.md tool tables "
          f"from data/tools.json ({len(tools)} tools).")


if __name__ == "__main__":
    main()
