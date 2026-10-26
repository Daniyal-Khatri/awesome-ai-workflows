# Production Audit Report — awesome-ai-workflows

**Date:** October 26, 2026
**Scope:** Local copy of the repository (README.md, CONTRIBUTING.md, data/tools.json,
data/tools.csv, build_readme_v4.py, LEARNINGS.md, devto-launch-article.md).
GitHub itself was not touched; CI is delivered as a workflow file that has been
syntax-checked locally but **not executed on GitHub**.
**Method:** every file read in full; counts and cross-source comparisons done by
script (see "Reproduction commands"); pricing evidence taken only from
`~/workspace/research_notes/free-freemium-ai-tools-research-20261026-1009/report.md`.

---

## 1. Verified state of the data (what was already correct)

A scripted field-for-field comparison of all three data sources found **no
data drift**:

| Check | Result |
| --- | --- |
| Tool count — tools.json / tools.csv / README tables | 65 / 65 / 65 |
| Categories | 14 in all three sources |
| Per-category counts | Identical in all three sources for all 14 categories (Writing 11, Research 6, Image 8, Video 10, Code 6, Audio 8, Productivity 1, Presentations 2, Websites 2, Marketing 2, Automation 2, Meetings 3, Design 2, Chatbots 2) |
| Per-entry fields (name, category, URL, pricing, description, best-for) | Identical across JSON, CSV and README — 0 mismatches |
| Duplicate names (case-insensitive) | None |
| Duplicate URLs (normalized: case, `www.`, trailing slash) | None |
| Malformed URLs | None — all 65 are `https` with a host |
| Pricing values outside {Free, Freemium} | None (64 Freemium, 1 Free — Google AI Studio) |
| Workflow stacks in README | 17 headings; every stack references only tools present in the data; every stack has a free-plan catch line and a recipe card (full read) |
| "First Week: 10 Tools" shelf | Exactly 10 rows |
| "Just the 5 Best" box | Exactly 5 rows |
| Goal table rows | 17 — matches the 17 stacks |
| Free-plan numbers quoted in stacks (spot-check vs the research report) | Matched: Gamma 400 one-time credits; Zapier 100 tasks/month; Make 1,000 ops/month; Otter.ai 300 min/month, 30 min/meeting; Fliki 3 credits/month; Chatbase 20 messages/month; Durable 300 credits total; Krea 100 units/day; Buffer 3 channels × 10 posts; SciSpace 100 credits/month; Uizard 3 AI generations/month |

README prose counts — "65 tools", "14 categories", "17 stacks" — are all
accurate against the data.

---

## 2. Findings

### F1 — HIGH (process) — Three hand-synced copies of the same data, no validation, no CI
- **Evidence:** Pre-audit, the same tool list existed in `data/tools.json`,
  `data/tools.csv`, and the README tables, and `CONTRIBUTING.md` instructed
  contributors to "Add the tool in **all three places**" by hand. There was no
  `.github/` directory (verified: none existed) and no validation script, so
  any future edit could silently desynchronise the three copies.
- **Affected files:** `data/tools.json`, `data/tools.csv`, `README.md`, `CONTRIBUTING.md`.
- **Fix applied:** `tools.json` is now the canonical source; `scripts/generate.py`
  regenerates the CSV and the README tables; `scripts/validate.py` enforces the
  schema and the JSON↔CSV↔README consistency; `.github/workflows/validate.yml`
  runs both on push and pull requests; `CONTRIBUTING.md` now documents the
  JSON-only workflow.
- **Verification:** `validate.py` passes on the fixed data; generation is
  idempotent (§4); negative tests (§4) fail as designed.

### F2 — MEDIUM — `build_readme_v4.py` is a stale full-README generator that conflicts with the current README
- **Evidence:** The script rebuilds the entire README from hard-coded content
  that predates the current README: it has no recipe cards, no Beginner
  Roadmap, no cost legend, no badge section, and an outdated "What's new"
  line. It also reads the pre-audit JSON keys (`website`, `best_for`), so
  after this audit's field rename it fails loudly with a `KeyError` instead of
  silently overwriting — but before the rename, running it would have
  destroyed current content.
- **Affected file:** `build_readme_v4.py`.
- **Fix applied:** None (left in place; it is superseded by
  `scripts/generate.py`). **Recommendation:** delete it or move it to an
  `archive/` folder in a follow-up commit so nobody runs it by accident.
- **Verification:** file read in full during the audit; not executed.

### F3 — MEDIUM — No LICENSE file in the local copy
- **Evidence:** A full file listing of the local copy contains no LICENSE
  file, although the project presents itself as MIT-licensed.
- **Affected file:** `LICENSE` (absent).
- **Fix applied:** None — licensing must not be added or changed without the
  owner's explicit approval.
- **Manual action required:** owner to confirm the LICENSE exists on GitHub,
  or add the MIT license text via GitHub's UI if it is genuinely missing.

### F4 — MEDIUM — Pricing verification covers only 37 of 65 tools; the README's "Last checked" line implies more
- **Evidence:** The 2026-10-26 research report verifies free tiers for the 37
  tools it added. The other 28 tools (the original list: ChatGPT, Claude,
  Perplexity, Cursor, ElevenLabs, etc.) have no verification record in the
  repository or the research report, yet the README header says
  "Last checked: October 26, 2026" for the list as a whole.
- **Affected files:** `README.md` (claim), `data/tools.json` (missing provenance).
- **Fix applied (partial, evidence-only):** every entry now carries
  `pricing_url` and `pricing_checked`. The 37 research-verified tools got
  `pricing_checked: "2026-10-26"` (the report states each free tier was
  checked on that date); 23 of them also got a `pricing_url`, but **only**
  where the report actually names a pricing page. The 28 unverified tools got
  empty strings — no dates or URLs were invented. The README claim itself was
  left unchanged; it is flagged here as broader than the recorded evidence.
- **Verification:** field population counts printed during the transform
  (65 tools, 23 with `pricing_url`, 37 with `pricing_checked`); spot-checked
  entries against the report's Sources section.

### F5 — LOW — README table headings differ from the canonical category names for 4 categories
- **Evidence:** Data uses `Writing`, `Websites`, `Meetings`, `Chatbots`;
  README headings read "Writing & Chat", "Website Builders",
  "Meetings & Notes", "Voice & Chatbots". Consistent everywhere, but the
  mapping existed nowhere in writing.
- **Fix applied:** the mapping is now encoded in `scripts/generate.py`
  (`DISPLAY_NAME`) and the canonical category list is written down in
  `scripts/validate.py` and `CONTRIBUTING.md`.
- **Verification:** regenerated README tables are byte-identical to the
  pre-audit tables (diff shows only the added marker lines).

### F6 — LOW — Three listed tools have been renamed by their vendors
- **Evidence:** `Windsurf` → Devin Desktop (June 2026), `Mistral Le Chat` →
  Mistral Vibe, `NotebookLM` → Gemini Notebook (July 2026), per the research
  report; the JSON descriptions already carry "(now …)" notes. The `name`
  fields and the old domains are still what the vendors' sites use.
- **Fix applied:** None — kept the JSON values (per audit safety rules) and
  flagged here. A rename pass is a content decision for the owner.
- **Verification:** research report "Watch-outs" section and tool entries.

### F7 — LOW — Unpublished draft in the repo root contains a wrong recipe attribution
- **Evidence:** `devto-launch-article.md` presents a ChatGPT script prompt as
  the "Short-Form Video Stack — the ChatGPT step". The actual Short-Form
  Video stack is Suno AI → Kling AI → ElevenLabs; the quoted ChatGPT recipe
  belongs to the YouTube Creator Stack.
- **Fix applied:** None (draft, not published documentation). Fix before
  publishing the article.

### F8 — LOW (housekeeping) — Working files live in the public repo root
- **Evidence:** `LEARNINGS.md` (internal promotion notes), the article draft
  above, and `social-preview.png` sit alongside the project's public files.
- **Fix applied:** None. Optional tidy-up for the owner.

### F9 — INFORMATIONAL — Historical selection claims are arithmetically consistent but not re-verifiable
- **Evidence:** README/dev.to draft claim "checked 77, kept 65, threw out 12 —
  2 paid-only, 10 fake-free/trial-only/dead". Arithmetic holds (65 + 12 = 77;
  2 + 10 = 12) and the research report independently lists exactly 10 tools
  that failed its filter. The original checking process itself is historical
  and cannot be re-run from repository data.
- **Disposition:** left unchanged, recorded here as historical/unverified
  rather than silently "fixed".

---

## 3. Files changed

| File | Change |
| --- | --- |
| `data/tools.json` | Normalized schema: `website` → `url`, `best_for` → `use`; added `pricing_url` + `pricing_checked` to every entry, populated only from research-report evidence (23 URLs, 37 dates). No tool data values were altered. |
| `data/tools.csv` | Regenerated from the JSON (new header `name,category,url,pricing,description,use,pricing_url,pricing_checked`; same CRLF convention as before). |
| `README.md` | Only: `generated:tools-tables` markers around the category tables (table content byte-identical), one changelog entry for this audit, and two lines in "The Data" explaining the source of truth. All prose, stacks, and recipes untouched. |
| `scripts/validate.py` | **New.** Stdlib-only validator: JSON syntax, required/non-empty fields, category set, pricing ∈ {Free, Freemium}, duplicate names/URLs, URL format, date format, plus CSV and README-tables consistency with the JSON. Exit 0/1 with readable errors. |
| `scripts/generate.py` | **New.** Stdlib-only generator: rebuilds `data/tools.csv` and the README category tables from `tools.json`. Idempotent (verified). |
| `scripts/check_links.py` | **New.** Stdlib-only internal-link check: relative file links must exist (error); in-page anchors checked approximately (warning only, never fails). |
| `.github/workflows/validate.yml` | **New.** On push + pull_request, `ubuntu-latest`, `permissions: contents: read`, `actions/checkout@v4`, `actions/setup-python@v5` (Python 3.x). Steps: `validate.py`; `generate.py` + `git diff --exit-code`; `check_links.py`. No secrets, no paid services. |
| `SECURITY.md` | **New.** Responsible-disclosure process via GitHub's private vulnerability reporting (Security tab → "Report a vulnerability"), minimal-issue fallback, honest response expectations, no invented contact email. |
| `CONTRIBUTING.md` | Added: canonical-source explanation, JSON-only editing, the new field list (incl. `pricing_url`/`pricing_checked`), and the local generate/validate/link-check commands to run before a PR. Existing rules (free/freemium only, no credit card, official links only, one tool per PR, ❌/💲 dead/went-paid marking) preserved verbatim. |
| `AUDIT-REPORT.md` | This report. |

**Compatibility impact:** dataset consumers must use the renamed keys
(`url`, `use`). The v1.0.0 release assets on GitHub still use the old keys;
the rename is announced in the README changelog entry.

---

## 4. Tests actually executed (real outputs)

All commands run from the repository root unless noted.

1. **Validator on the fixed data — PASS**
   ```
   $ python3 scripts/validate.py
   OK: 65 tools, 14 categories — tools.json is valid and tools.csv + README tables match it.
   (exit 0)
   ```

2. **Generator fidelity** — first `generate.py` run: `diff` of the README
   against the pre-audit original showed **only** the two marker lines added;
   table content byte-identical.

3. **Generator idempotence — PASS**
   ```
   $ python3 scripts/generate.py   # twice; diff after the second run
   IDEMPOTENT: second generate produced no changes
   ```
   A final run after all Phase-4 edits also produced no changes.

4. **Link check — PASS**
   ```
   $ python3 scripts/check_links.py
   Link check OK (0 anchor warning(s)).
   (exit 0)
   ```

5. **Negative tests** (each on a separate copy of the repo under `/tmp`, real
   files never touched) — all failed with clear errors, exit 1:
   - (a) duplicate name appended →
     `ERROR: tools.json 'ChatGPT': duplicate tool name (also entry #1)`
   - (b) pricing set to `Paid` →
     `ERROR: tools.json 'ChatGPT': pricing 'Paid' must be Free or Freemium`
   - (c) URL `chatgpt.com` (no scheme) →
     `ERROR: tools.json 'ChatGPT': malformed url 'chatgpt.com'`
   - (d) `description` field deleted →
     `ERROR: tools.json 'ChatGPT': missing field(s): description` (+ empty-field error)
   - (e) hand-edited generated CSV → validator:
     `ERROR: data/tools.csv does not match data/tools.json — run scripts/generate.py`;
     and regenerating produced a file differing from the hand-edited one
     (`cmp` mismatch), which is what CI's `git diff --exit-code` step catches.

6. **CI workflow syntax** — parsed locally with PyYAML: structure confirmed
   (triggers `push` + `pull_request`, `permissions: contents: read`, runner
   `ubuntu-latest`, 5 steps, actions `actions/checkout@v4` and
   `actions/setup-python@v5`). Note: PyYAML (YAML 1.1) reads the `on:` key as
   boolean `True`; GitHub's parser handles `on:` correctly. **The workflow
   itself has not run** — it only executes once pushed to GitHub.

7. **Script syntax** — `python3 -m py_compile` on all three scripts: OK.

---

## 5. Remaining problems and unverified claims

- **F2, F3, F6, F7, F8 above are open** (stale generator script, missing
  LICENSE in the local copy, vendor renames, draft inaccuracy, root
  housekeeping).
- **28 tools have no recorded pricing verification** (`pricing_checked` is
  empty). Their Free/Freemium status is asserted by the list but was not
  re-verified in this audit — no web checks were in scope, and an HTTP 200
  would not prove a free tier anyway. The README's list-wide "Last checked:
  October 26, 2026" should be read with that caveat.
- **Free-plan limits quoted in workflow stacks** were spot-checked only for
  the research-covered tools (§1). Limits attached to the original 28 tools
  (e.g. "Runway and Kling free credits go fast") are qualitative and were not
  independently verified.
- **Historical claims** ("checked 77 / threw out 12") are consistent but
  historical — see F9.
- **Contents-index anchors** for the `&` headings (e.g. `#writing-chat`)
  could not be verified against GitHub's exact slugification locally; the
  link checker therefore treats anchors as warnings only, by design.
- **The CI workflow is untested end-to-end** until it is pushed to GitHub.

## 6. Reproduction commands

```bash
cd awesome-ai-workflows
python3 scripts/validate.py        # data + generated-file consistency
python3 scripts/generate.py        # regenerate CSV + README tables from tools.json
python3 scripts/generate.py && git diff --exit-code   # staleness check (CI equivalent)
python3 scripts/check_links.py     # internal file links (errors) + anchors (warnings)
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/validate.yml'))"  # CI syntax
```

## 7. Manual actions still required (owner)

1. Commit and push all changes so CI runs for the first time on GitHub;
   confirm the "Validate data" workflow goes green.
2. Confirm the LICENSE situation on GitHub (F3) and add the MIT text via
   GitHub's UI if it is missing — not done here, by design.
3. Decide on `build_readme_v4.py` (F2): delete or archive it.
4. Optionally: fix the recipe attribution in `devto-launch-article.md` (F7)
   before publishing, and consider the vendor-rename pass (F6).
5. When re-checking any tool's pricing, update its `pricing_url` /
   `pricing_checked` in `data/tools.json` and re-run `generate.py` +
   `validate.py`.
