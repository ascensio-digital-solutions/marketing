# Project status

## 2026-10-03 — Claude Code

Made this repository the only source of truth for email marketing and added the email library.

- `templates/email-blocks/`: 34 sections (HTML, properties, 1200px previews).
- `templates/emails/`: 5 templates (CR-1 to CR-4, PP-1) as ordered section recipes, with generated install files and previews.
- `.claude/skills/shopify-email-html/`: the skill plus the scripts (`build_library.py`, `assemble_email.py`, lint, preview, install helpers).
- Verification: rebuilt templates have the same text as the v6 originals, and their previews are pixel-identical to the v6 renders.
- Shopify state: PP-1 is live. The abandoned-checkout Flow is inactive and CR-1 to CR-4 are drafts.
  The CR-2 to CR-4 Shopify drafts still have the old 2px gaps and need re-syncing from `template.html`.
  CR-2's testimonial is still a placeholder.
- Design source linked: `vincent-laroche/brand-design-system` → `email/`.

## 2026-08-19 — Codex

Initialized the repository and pushed `main` at `53b7617`.

- Created strategy, automation, campaign, template, analytics, and implementation-documentation structure.
- Notion holds the corresponding masterplan, automation blueprints, lifecycle map, campaign briefs, asset library, and KPI records.
- Next: add implementation only from approved Notion records; do not enable any flow from this repository alone.
