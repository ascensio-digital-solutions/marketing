# Handoff: building Shopify email templates and Flows

Paste the prompt below into a new agent session (Claude Code, desktop app, working directory
`~/01_hair_solutions_co/marketing/email-marketing`). Replace `<ASSIGNMENT>` with the journey or emails
that agent owns, for example "Welcome series W-1 to W-5" or "Post-purchase PP-2 to PP-7b".
Give every agent a different assignment.

---

## Prompt

You are building Hair Solutions Co. marketing and transactional emails in Shopify. Your
assignment: **<ASSIGNMENT>**.

### 1. Read these first, in this order

1. `AGENTS.md` (repo root): the rules. This repository, `vincent-laroche/email-marketing`, is the
   **only source of truth for email marketing**. Ignore marketing-os, MailerLite, HubSpot, Resend
   and the folder `~/01_hair_solutions_co/marketing/resend-customerio-archive`.
2. `.claude/skills/shopify-email-html/SKILL.md`: the skill. It covers the whole procedure
   (surfaces, approval gates, HTML contract, install, verify, record). It is also installed
   globally as `shopify-email-html`. Then read the references it points to:
   - `references/email-library.md`: the sections and templates databases (how to reuse and add);
   - `references/html-contract.md`: the HTML rules;
   - `references/surfaces.md`: the Shopify surfaces and their Liquid variables;
   - `references/editor-automation.md`: what works in the Shopify editors, and the pitfalls;
   - `references/flow-recipes.md`: how the abandoned-checkout Flow was wired.
3. `templates/email-blocks/README.md` and `templates/emails/README.md`: galleries of every existing
   section and template. Reuse sections before creating new ones.
4. Look at the finished examples:
   - `templates/emails/cr-2-three-questions-answered/` for Messaging · Code your own;
   - `templates/emails/cr-1-your-carts-still-here/` for Messaging · Custom Liquid sections;
   - `templates/emails/pp-1-order-confirmation/` for a notification template.

### 2. Design and content sources

- **Design: Figma "Email Design System"**:
  https://www.figma.com/design/9Il504CQE8jLaUTBVzphqc/Email-Design-System?node-id=557-7295
  This is the page the CR and PP emails were built from (page "v6 · Reference"). Find the frames for
  your assignment there and match them. Use the Figma MCP tools (`get_metadata`, `get_screenshot`,
  `get_design_context`) to read frames.
- **Tokens and components:** `vincent-laroche/brand-design-system`, folder `email/`
  (local clone: `~/01_hair_solutions_co/design/brand/brand-design-system/email`). Never invent
  colours, fonts or components.
- **Copy:** use the copy in the Figma frame word for word. If an email has no frame or no copy, stop
  and ask Vincent. Never write marketing copy yourself.
- **Notion** (read-only references; the repo wins if they disagree):
  - "Shopify Email Marketing Masterplan": strategy, lifecycle map, automation blueprints and timing;
  - "Shopify Email Sections" and "Shopify Email Templates" databases (01 Hair Solutions Co. ›
    Company Home › Projects › Email Marketing): an older mirror of this library.
- **Facts:** every commercial fact (lead times, prices, discount codes, testimonials) must be
  confirmed. Known facts:
  - lead times: stock orders dispatch in 2 days and arrive in 7; custom orders take 56 and 63 days;
  - discount `FREESHIP` exists and is active;
  - testimonials may only be published Judge.me reviews, quoted word for word. Ask Vincent which one.

### 3. Non-negotiable design rules

These are enforced by `lint_email.py` and by the GitHub check.

1. Rounded corners on every component: cards 12px, insets 8px, buttons and pills 999px.
2. No gap between blocks: card rows are `<tr><td style="padding:0;">`, with no spacers.
3. Transparent background behind the modules: body, the outer wrapper, and Shopify Messaging's
   **Email colors → Content background** set to `transparent`.
4. No placeholders anywhere: every name, quote and photo is a real value or a Liquid variable.

### 4. How to build (in the repo)

1. Work on your own branch: `git checkout -b <journey>-emails` (for example `welcome-emails`).
2. New sections go in `templates/email-blocks/<id>/` with `section.html` and `section.json`.
   Name new folders `<code>-<slug>` (for example `w-1-hero`), not with a number prefix, so that
   parallel agents do not collide.
   - Reuse the shared sections: `00-email-head-fonts-styles`, `02-logo-header`,
     `04-cart-contents`, `06-preferences-footer` (marketing), `11-trust-strip`, and the PP-1 footer
     for notifications.
3. New templates go in `templates/emails/<code-slug>/template.json`. The `sections` list (in
   order) is the recipe; `surface` is `messaging-code-your-own`, `messaging-sections` or
   `notification`.
4. Images go on Shopify Files through the Admin API (`stagedUploadsCreate` → curl → `fileCreate`),
   named `hsc-email-<what>.jpg`. Reference them at
   `https://cdn.shopify.com/s/files/1/0276/9115/5508/files/<name>`.
5. Build and preview. Screenshots need Chrome and Pillow in a venv:
   `python3 .claude/skills/shopify-email-html/scripts/build_library.py --screenshots <ids>`.
   Then run `build_library.py --check` and look at every `preview.png` yourself.
6. Commit and open a pull request. The "Email library" check must pass. Merging is not activation.

### 5. How to install (in Shopify, in the browser pane so Vincent can watch)

- **Store:** `admin.shopify.com/store/oneheadhair`.
- **Marketing emails:** each email is a "Send marketing email" step inside a Shopify **Flow**
  workflow, built from **Custom Liquid sections** assembled one at a time in the Messaging editor
  (Vincent's rule, 2026-10-04; not Code your own unless he asks).
  - Create your own workflow; do not edit "Recover abandoned checkout" (CR-1 to CR-4), which is done.
  - Type the generated `template.html` with the `type` action in two halves of about 10–12 KB.
    Check that each reported character count matches what you computed locally.
  - Set **Subject** and **Preview text** from `template.json` (scroll the preview to the top
    first).
  - Exit with **Leave**, so the email stays a draft.
- **Transactional emails** go in Settings → Notifications. Back up the live code first. Saving
  makes the email live, so get Vincent's approval before saving.
- **Waits** in Flow are entered in seconds, because the unit dropdown does not work under
  automation. Pan the canvas only from empty space: dragging a step moves it.

### 6. Never without Vincent's explicit approval

- Turning on a workflow, or clicking "Turn on" on an email.
- Saving a notification template.
- Sending a test or real email, or creating discount codes.
- Deleting a Flow step or an existing email.

### 7. When you finish

- Set `shopify_status`, `shopify_matches_repo` and `blockers` in each `template.json` to what Shopify
  actually shows, rebuild, and commit.
- Add a dated entry to `PROJECT.md`: what you built, what is in Shopify (draft or live), and the
  open blockers.
- Report to Vincent for each email: the surface, its state, what you verified, and its blockers.
