# Project status

## 2026-10-03 (later) — Claude Code

- Re-synced CR-2, CR-3 and CR-4 in Shopify Messaging from `template.html`: no gaps, 12px corners,
  Outlook wrapper. The typed character counts matched the repository exactly.
- CR-4's Subject was empty in Shopify; set it to "Last note about your cart".
- CR-2 testimonial: the placeholder was replaced with a published Judge.me review (Scott S., Dura
  Skin, word for word, chosen by Vincent) and the Dura Skin hairline photo
  (`hsc-email-review-dura-skin-hairline.jpg` on Shopify Files). Judge.me marks all store reviews
  as not from a verified buyer.
- Accidentally dragged one Condition step on the Flow canvas; its position was restored and the
  wiring never changed.
- Local setup: `~/01_hair_solutions_co/marketing/email-marketing` is now a clean clone of this
  repo. The old Resend/Customer.io worker moved to
  `~/01_hair_solutions_co/marketing/resend-customerio-archive` (no remote).
- Added `HANDOFF.md` (prompt for parallel agents) and updated AGENTS, README, CLAUDE and the skill's
  editor notes.
- Next: agents build the remaining journeys from Figma (see `HANDOFF.md`). The Flow stays inactive
  until Vincent approves.

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
