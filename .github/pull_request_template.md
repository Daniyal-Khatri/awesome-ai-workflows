## Purpose

<!-- What does this PR add or fix, in one or two lines? -->

## What changed

<!-- One tool or one workflow stack per PR. Name the tool/stack and its category. -->

## Validation

I ran these locally from the repo root and they pass:

- [ ] `python3 scripts/generate.py` — regenerated `data/tools.csv` and the README tables, committed together with my `tools.json` change
- [ ] `python3 scripts/validate.py`
- [ ] `python3 scripts/check_links.py`

## Checklist

- [ ] I read CONTRIBUTING.md and edited **only** `data/tools.json` for tool data (README tables and the CSV are generated, not hand-edited)
- [ ] The tool is **free or freemium**, and its free plan works **without a credit card** — I set `pricing_url` and `pricing_checked` (today's date) in my entry
- [ ] The link is the official website — no affiliate links, no tracking parameters
- [ ] The tool is not already on the list, and the description is short (max 100 characters), honest and neutral
- [ ] If this is my own tool or project, I have said so here: <!-- delete if not yours -->
