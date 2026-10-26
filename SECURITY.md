# Security Policy

## What "security" means for this repository

Awesome AI Workflows is a curated list: Markdown documents, a JSON/CSV
dataset, and small Python helper scripts. It ships no server, no user
accounts, and no code that runs for visitors. The realistic risks are:

- A listed link that has been taken over and now points at a harmful site.
- Bad data merged by mistake (wrong URL, misleading pricing claim).
- A problem in the helper scripts under `scripts/`.

## Reporting a vulnerability or a harmful link

Please **do not** open a public issue with exploit details.

Preferred route: use GitHub's private vulnerability reporting — open the
repository's **Security** tab and choose **Report a vulnerability**. That
keeps the report private until it has been looked at.

If that option is not available to you, open a minimal public issue that
only says you need a private contact channel for a security report (no
technical details), and one will be arranged.

## What to expect

This is a small, volunteer-maintained project, so expectations are modest
and honest:

- Reports are read and acknowledged as soon as reasonably possible —
  usually within a week, but there is no guaranteed response time.
- Confirmed harmful or hijacked links are removed or marked in the list
  as quickly as possible after confirmation.
- There is no bug bounty.

## Scope notes

- Pricing and free-tier claims are editorial data, verified by hand on
  the date recorded in `pricing_checked` in `data/tools.json`. A tool
  changing its pricing is a data issue, not a vulnerability — a normal
  issue or pull request is the right route for those.
