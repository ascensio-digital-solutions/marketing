# Shopify Email Marketing

Hair Solutions Co.'s email marketing: the single source of truth for strategy, the email
library, campaigns, automations and reporting.

## Start here

- **New agent or contributor:** read [`HANDOFF.md`](HANDOFF.md). It has the full prompt for building
  Shopify emails and Flows from the Figma design, then [`AGENTS.md`](AGENTS.md) for the rules and
  current state.
- **Shopify today:** PP-1 Order confirmation is live. CR-1 to CR-4 (abandoned checkout) are drafts
  in an inactive Flow and match this repository.

## Email library

| Database | What it holds |
|---|---|
| [**Email sections**](templates/email-blocks/) | Every reusable section (block) of a Shopify email: exact HTML, properties and a preview. |
| [**Email templates**](templates/emails/) | Every assembled email: the ordered list of sections it is built from, the code to paste into Shopify, and a preview. |

Both have a gallery (`README.md`) and a sortable table (`index.tsv`). To build a new email, list the
sections you want in a `template.json` and run:

```bash
python3 .claude/skills/shopify-email-html/scripts/build_library.py
```

Tools (in [`.claude/skills/shopify-email-html/scripts/`](.claude/skills/shopify-email-html/scripts/)):

- `build_library.py` — validates and builds every template, writes the galleries; `--check`, `--screenshots`.
- `assemble_email.py` — assembles one email from any list of section files.
- `lint_email.py` — checks an email against the Shopify and design rules.
- `screenshot_block.py`, `mini_liquid.py` — preview renders with fictional data.
- `split_cards.py`, `pack_for_injection.py` — splitting and installing helpers.

The how-to for agents and people is the skill: [`.claude/skills/shopify-email-html/SKILL.md`](.claude/skills/shopify-email-html/SKILL.md).

## Design system

Brand and email design live in
[`vincent-laroche/brand-design-system` → `email/`](https://github.com/vincent-laroche/brand-design-system/tree/main/email):
email components, tokens and the Figma library "HSC Email Design System". Every section in this
repository is built to that system: rounded corners (cards 12px), no gap between sections, and a
transparent background behind the modules.

## Structure

- `templates/email-blocks/` — sections database.
- `templates/emails/` — templates database.
- `templates/hsc-v6-emails/` — the original v6 build (history, image sources, rollback backup).
- `strategy/` — masterplan, lifecycle map, and segmentation policy.
- `automations/` — approved automation implementation and QA evidence.
- `campaigns/` — calendar exports and campaign briefs.
- `analytics/` — KPI definitions and reporting notes.
- `docs/` — platform implementation and release checks.

## Working rule

Respect consent, purchase exits, suppression rules, and the customer lifecycle state in every
implementation. Nothing is sent, scheduled or turned on without Vincent's explicit approval.
