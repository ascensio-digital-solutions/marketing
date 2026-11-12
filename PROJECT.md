# Project status

## 2026-10-04 — Claude Code (v6 reference emails: W-1, WB-2, RO-3, C-0, NL-01)

Scope (Vincent): the first email of each series on the Figma "v6 · Reference" page. PP-1 and CR-1 to CR-4 already existed.

- Library: 45 new sections and 5 new templates (`w-1-welcome`, `wb-2-whats-changed`, `ro-3-replacement-window`, `c-0-consultation-recap`, `nl-01-no-best-base`), all Messaging · Code your own. Copy is transcribed from the Figma captures (the page holds flat PNG captures, not editable text); subjects and preview text come from the Figma "Inbox" blocks.
- Build: templates can set `"context": "customer"`; new fixture `fixture-customer.json`; `mini_liquid.py` supports `"now" | date`, `money_without_currency` and `remove`.
- Verified Messaging variables (probe in a campaign preview): see `references/surfaces.md`. No "view in browser" variable exists, so that link is left out of every email.
- Shopify: **NL-01 is a draft campaign** (Messaging, no segment, not scheduled; photo label synced 2026-10-04). WB-1 is attached to the WB Flow draft; W-1, WB-2 and RO-3 are not installed; C-0 is not created on purpose.
- Flow (nothing turned on, all inactive drafts): (1) "WB win-back: 90 days without an order": Order created, Wait 7 776 000 s, Get customer data (Advanced query: this customer, orders on or after the day after the trigger order), Condition (at least one customer found whose id equals the order's customer id; the False branch, no newer order, sends WB-1 as a draft email). (2) "RO reorder: 60 days after last purchase": same graph with Wait 5 184 000 s and no email step (RO-1 has no design; RO-3 would be a later step). Untested: the `order_date` filter and the customer id extraction need one test run before activation. Stray drafts to delete (need Vincent's approval): "New Workflow" (Order fulfilled, Wait 7 776 000 s) and an earlier "New Workflow" (Order created, Wait, orphaned Condition). W-1 (trigger: newsletter sign-up or first order, whichever comes first) has no workflow yet.
- W-1 welcome workflows (2026-10-04, drafted by Shopify Sidekick, inactive, tag "sidekick"): "Welcome email on email marketing subscribe" (Customer subscribed to email marketing → Condition tags = welcome-email-sent → Add customer tag welcome-email-sent → Send marketing email) and "Welcome email on first order" (Order created → Condition customer orders = 1 → Wait 2 minutes → same tag check → add tag → Send). W-1 is installed as a **sections** email (8 Custom Liquid sections, subject and preview text set, Header hidden, Content background transparent) in the subscribe workflow only. The first-order workflow's Send step still holds a Code your own draft (the email type cannot change; replacing the step needs Vincent's approval). The "What you'll get / never get" section lost its white cards at Vincent's request. A trigger-only stray "New Workflow" (Customer subscribed to email marketing) and an orphaned Code your own "Untitled Activity" draft email also exist.
- Build rule added (Vincent, 2026-10-04): every email is built from Custom Liquid sections one at a time in the Shopify editor (see `AGENTS.md`).
- Series triggers (Vincent, 2026-10-04): WB starts after 90 days without any order; RO starts 60 days after the last purchase. Lead times: stock 5-7 days, custom 8-10 weeks (RO-3 and C-0 now print 8-10 weeks).
- WB-1 (checking in) added: copy from the older Figma frame; subject "Checking in — Vincent here", preview text and sign-off from the Notion emails master. RO-1 has no design.
- Review photos are product shots; captions now say "Product photo".
- Images: 15 images uploaded to Shopify Files (`hsc-email-*`), cropped from the Figma captures.
- Testimonials: real reviews only (Notion Reviews export, the 5 rows created 2025-11-15): Thomas L. (NL-01), Robert M. (WB-2), Michael T. (RO-3). The angles only partly match the designs.
- All buttons go to the homepage for now. Open items are in GitHub issues #3 (button links), #4 (RO-3 customer metafields) and #5 (copy, facts and testimonials to confirm).
- Notion: records added to "Shopify Email Sections" and "Shopify Email Templates".

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
- `.claude/skills/shopify-email-html/scripts/` and `assets/`: the build and install tooling (`build_library.py`, `assemble_email.py`, lint, preview, install helpers). The skill text itself moved out of the repo on 2026-11-12: it ships from `~/03_agents` (hsc-email).
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
