# Handoff: building Shopify email templates and Flows

Paste the prompt below into a new agent session (Claude Code, desktop app, working directory
`~/01_hair_solutions_co/marketing/email-marketing`). Replace `<ASSIGNMENT>` with the journey or emails
that agent owns, for example "NL-02 to NL-05 newsletters" or "Shipping confirmation, Shipping update and
Delivered notifications". Give every agent a different assignment. What is still missing is listed
in GitHub issue #7 ("Emails in Figma that are not in Shopify yet"); pick from it.

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
   - `references/flow-recipes.md`: how the Flow workflows (cart recovery, welcome, win-back, reorder)
     are wired, and how to have Shopify Sidekick build one.
3. `templates/email-blocks/README.md` and `templates/emails/README.md`: galleries of every existing
   section and template. Reuse sections before creating new ones.
4. Look at the finished examples:
   - `templates/emails/w-1-welcome/` and `cr-1-your-carts-still-here/` for Messaging · Custom Liquid
     sections (the way every marketing email is built now);
   - `templates/emails/pp-1-order-confirmation/` for a notification template;
   - `templates/emails/cr-2-three-questions-answered/` for Code your own (older emails only; do not
     copy that approach).

### 2. Design and content sources

- **Design: Figma "Email Design System"**:
  https://www.figma.com/design/9Il504CQE8jLaUTBVzphqc/Email-Design-System?node-id=557-7295
  This is the current design (page "v6 · Reference": PP-1, CR-2, WB-2, RO-3, C-0, W-1 and NL-01 to
  NL-05). The same file has an older page, "Email Templates" (node 62:830), with PP-1 to PP-7, WB-1 to
  WB-4, lifecycle examples and layout explorations: use it only for copy and structure, restyled to v6.
  Find the frames for your assignment and match them. Use the Figma MCP tools (`get_metadata`, `get_screenshot`,
  `get_design_context`) to read frames.
- **Tokens and components:** `vincent-laroche/brand-design-system`, folder `email/`
  (local clone: `~/01_hair_solutions_co/design/brand/brand-design-system/email`). Never invent
  colours, fonts or components.
- **Copy:** use the copy in the Figma frame word for word. If an email has no frame or no copy, stop
  and ask Vincent. Never write marketing copy yourself.
- **Notion** (01 Hair Solutions Co. › Company Home › Projects › Email Marketing). The repo wins if they
  disagree, but Vincent wants Notion kept current as you build:
  - "Shopify Email Marketing Masterplan": strategy, lifecycle map, automation blueprints and timing
    (read-only);
  - "Shopify Email Sections" and "Shopify Email Templates" databases: a record for every section and
    template (status, location, blockers);
  - "Messaging Journeys" database
    (https://app.notion.com/p/d3802cf29293450cad97d24a04e64b49): one row per journey or workflow, with
    the Shopify workflow name and ID, trigger, entry and exit rules, steps, email sequence, delays
    between emails, metrics and blockers.
- **Facts:** every commercial fact (lead times, prices, discount codes, testimonials) must be
  confirmed. Known facts:
  - lead times (Vincent, 2026-10-04): stock hair systems 5-7 days; custom hair systems 8-10 weeks.
    (The live PP-1 still prints the older 2 and 7 days: do not copy it.);
  - system cost wording: "Between $199 and $399 on average.";
  - series timing: WB starts after 90 days without any order; RO starts 60 days after the last
    purchase; W-1 goes out when someone signs up for the newsletter OR places their first order,
    whichever comes first;
  - discount `FREESHIP` exists and is active;
  - testimonials: real reviews only (the 5 real rows in the Notion Reviews export), quoted word for
    word and clearly marked; photos are product shots and are captioned "· Product photo". Ask Vincent
    which review;
  - every button goes to the homepage `https://hairsolutions.co` for now (issue #3);
  - post-consultation emails (C-0 and the C series) are never created in Shopify.

### 3. Non-negotiable design rules

These are enforced by `lint_email.py` and by the GitHub check.

1. Rounded corners on every component: cards 12px, insets 8px, buttons and pills 999px.
2. No gap between blocks: card rows are `<tr><td style="padding:0;">`, with no spacers.
3. Transparent background behind the modules: body, the outer wrapper, and Shopify Messaging's
   **Email colors → Content background** set to `transparent`.
4. No placeholders anywhere: every name, quote and photo is a real value or a Liquid variable.

### 4. How to build (in the repo)

1. Work on your own branch: `git checkout -b <journey>-emails` (for example `welcome-emails`).
2. New sections go in `templates/email-blocks/<id>/` with `section.html` and `section.json`. Reach for the module bank first (`templates/email-blocks/BANK.md`, 282 sections in Bone, Ink and White; see `.claude/skills/shopify-email-html/references/module-bank.md`). Bank folders (`mb-*`) are generated: change `templates/module-bank/cat_*.py`, never the files.
   Name new folders `<code>-<slug>` (for example `w-1-hero`), not with a number prefix, so that
   parallel agents do not collide.
   - Reuse the shared sections: `00-email-head-fonts-styles`, `02-logo-header`,
     `04-cart-contents`, `06-preferences-footer` (marketing), `11-trust-strip`, and the PP-1 footer
     for notifications.
3. New templates go in `templates/emails/<code-slug>/template.json`. The `sections` list (in
   order) is the recipe; `surface` is `messaging-sections` for every marketing email (Vincent's
   build rule), `notification` for transactional emails, and `messaging-code-your-own` only if he asks.
4. Images go on Shopify Files through the Admin API (`stagedUploadsCreate` → curl → `fileCreate`),
   named `hsc-email-<what>.jpg`. Reference them at
   `https://cdn.shopify.com/s/files/1/0276/9115/5508/files/<name>`.
5. Build and preview. Screenshots need Chrome and Pillow in a venv:
   `python3 .claude/skills/shopify-email-html/scripts/build_library.py --screenshots <ids>`.
   Then run `build_library.py --check` and look at every `preview.png` yourself.
6. Commit and open a pull request. The "Email library" check must pass. Merging is not activation.

### 5. How to install (in Shopify, in the browser pane so Vincent can watch)

- **Store:** `admin.shopify.com/store/oneheadhair`. Vincent logs in himself.
- **Build rule (Vincent, 2026-10-04):** every marketing email is built by creating and assembling
  Custom Liquid sections one at a time in the Shopify Messaging editor, never as one Code your own
  document. The skill's Step 4.2 has the exact clicks.
  - Flow step → **Select template → Blank**, then **Add section → Custom Liquid** once per generated
    fragment `templates/emails/<id>/custom-liquid/NN.html`; type each with the `type` action (indentation
    stripped; check each reported character count against the file). Fragment 01 carries the fonts and
    `<style>`.
  - Hide the stock Header (select it, eye icon), set **Email colors → Content background** to
    `transparent`, fill **Subject** and **Preview text** from `template.json`, then **Exit → Leave** so
    the email stays a draft.
  - A step's email type cannot change later: a step that holds a Code your own draft needs a new
    Send step (ask before deleting the old one).
- **Flow workflows:** ask Shopify **Sidekick** to design and build the workflow (it is much faster than
  the canvas): stay on the Flow page, click **Preview** on each workflow it offers, then **Add to store**
  (top right). They are saved inactive with a "sidekick" tag. Review the result: Flow allows one trigger
  per workflow, so "A or B" means two workflows with a shared guard. Never edit another agent's
  workflow, and never click **Turn on workflow**.
- **Transactional emails** go in Settings → Notifications. Back up the live code first. Saving
  makes the email live, so get Vincent's approval before saving.
- **Waits** in Flow are entered in seconds, because the unit dropdown does not work under
  automation. Pan the canvas only from empty space: dragging a step moves it. The editor redraws a
  moment after each click: wait 2-3 seconds before taking the next screenshot.

### 6. Never without Vincent's explicit approval

- Turning on a workflow, or clicking "Turn on" on an email.
- Saving a notification template.
- Sending a test or real email, or creating discount codes.
- Deleting a Flow step, a workflow or an existing email (leftover drafts: list them for Vincent).

### 7. When you finish

- Set `shopify_status`, `shopify_matches_repo` and `blockers` in each `template.json` to what Shopify
  actually shows, rebuild, and commit.
- Add a dated entry to `PROJECT.md`: what you built, what is in Shopify (draft or live), and the
  open blockers. Update the `AGENTS.md` current-state table.
- Update Notion: the Sections and Templates records for what you built, and the "Messaging Journeys"
  row for each workflow (name, ID, trigger, steps, delays, metrics, blockers).
- Tick off what you finished in GitHub issue #7.
- Report to Vincent for each email: the surface, its state, what you verified, and its blockers.
