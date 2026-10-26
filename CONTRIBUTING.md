# Contributing to Awesome AI Workflows

Thanks for helping grow this list. Contributions are welcome — one tool or one workflow stack per pull request.

## The data source of truth

`data/tools.json` is the **canonical source** for the tool list. Everything
else is generated from it:

- `data/tools.csv` — generated, never edit by hand.
- The "Tools by Category" tables in `README.md` — generated (see the
  `generated:tools-tables` markers), never edit by hand.

Contributors edit **only** `data/tools.json`, then regenerate. Everything
else in `README.md` (prose, workflow stacks, recipes) is edited normally.

## Add a tool

1. Fork this repository.
2. Add one entry to `data/tools.json`, in the position you want it to
   appear (entries are shown in file order, grouped by category).
3. Use this format for every entry:
   - **name** — the tool's real name
   - **category** — Writing, Research, Image, Video, Code, Audio, Productivity, Presentations, Websites, Marketing, Automation, Meetings, Design or Chatbots
   - **url** — the official website only (no affiliate or referral links, no tracking parameters)
   - **pricing** — Free or Freemium only. Paid-only tools are not accepted, and the free plan must work without a credit card.
   - **description** — one short line on what it does
   - **use** — one short line on who should use it
   - **pricing_url** — link to the official pricing page you checked (may be left empty if you verified through another official page)
   - **pricing_checked** — the date you verified the free tier, as `YYYY-MM-DD` (leave empty only if you could not verify — unverified tools may be held or rejected)
4. Regenerate and validate (see below), then open a pull request with a
   clear title, e.g. `Add <Tool Name> to Image`.

## Before you open a pull request

Run these from the repository root (Python 3, no extra packages needed):

```bash
python3 scripts/generate.py   # rebuilds data/tools.csv and the README tables from tools.json
python3 scripts/validate.py   # must pass: fields, categories, pricing, duplicates, URLs
python3 scripts/check_links.py
```

Commit the regenerated `data/tools.csv` and `README.md` together with your
`tools.json` change. CI runs the same checks on every pull request and
fails if the generated files do not match `tools.json`, so a red build
usually means "run `generate.py` and commit the result".

## Add a workflow stack

Stacks are the heart of this repo. A good stack:

- Solves one real job end to end (for example: podcast, online course, product launch)
- Chains 2–5 tools in order, with one line on what each step does
- Uses tools that are already listed, or adds them in the same PR

## Rules

- Official links only. No affiliate links, no tracking parameters.
- No duplicate tools.
- Keep descriptions short, honest and neutral — no marketing hype.
- Tools must be live and publicly available.
- Free or freemium only — no paid-only tools, and no free plan that needs a credit card to start.
- If a listed tool dies or goes paid-only, mark it ❌ dead or 💲 went paid in the tables instead of deleting it quietly, and note it in the changelog.

Maintained by [SaaSListy](https://saaslisty.com).
