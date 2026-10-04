---
name: shopify-email-html
description: Builds and installs custom HTML emails in Shopify — notification templates (Settings → Notifications, e.g. Order confirmation), Shopify Messaging emails as Custom Liquid sections or full custom-code documents, and the Shopify Flow steps that send them. Enforces the house design rules (rounded corners, no gap between blocks, transparent background), covers Shopify Liquid variables, required tags, admin editor automation, image hosting on Shopify Files and safe draft/live handling, and maintains the email library in the email-marketing repository (sections and templates databases, recipes, previews, assembler). Use when asked to put, build, split, fix or update an HTML email or section in Shopify, Shopify Messaging or a Flow email step, or to find, reuse, add or change email sections and templates in the email library. Don't use for MailerLite, Customer.io, HubSpot or Resend emails, theme code, Flow action extension apps, or designing new components (brand-design-system repository, email folder).
---

# Shopify email HTML

Ship hand-built HTML emails into the three Shopify surfaces without breaking the design or sending
anything by accident. This skill lives in `vincent-laroche/email-marketing`, the only source of
truth for email marketing. Visual design (tokens, components, Figma library) comes from
`vincent-laroche/brand-design-system` → `email/`; this skill is the build-and-install layer.

## Design rules (non-negotiable)

These were set by Vincent and are checked by `scripts/lint_email.py`. Breaking any of them is a
regression, even if the email "looks fine" in one client.

1. **Rounded corners on every component**, matching Figma: cards 12px, insets (quote boxes, code
   chips, portraits, photos inside cards) 8px, buttons and pills 999px, a full-bleed top photo
   `12px 12px 0 0`. Never leave a square card, and never put a border on a button `<td>` (it squares
   off in Messaging; the border goes on the `<a>`).
2. **No gap between blocks.** Cards stack flush: each card row is `<tr><td style="padding:0;">`.
   No spacer rows, no `padding:0 0 2px 0`, no margins between sections, no blank Custom Liquid
   section. In Messaging the cards must still touch across section boundaries.
3. **Transparent background behind the modules.** `<body>`, the outer wrapper table and the shell
   are `background-color:transparent`; colour lives only on cards and insets. In Shopify
   Messaging also set **Email colors → Content background** to `transparent` (and Border to
   transparent if a line shows). No page colour, not even the brand cream.
4. Fixed 600px column, table layout, inline styles; one Email head (fonts + `<style>`) per email.
5. Unconfirmed facts (lead times, discounts, testimonials) are placeholders and blockers, never
   defaults.

Full details: `references/html-contract.md`.

## Procedure

### Step 1: Identify the surface and the risk

1. Read the repository's `AGENTS.md` and follow it where it is stricter. Merging a pull request
   or installing a draft is never activation.
2. Read `references/email-library.md` and look in the library first:
   `templates/email-blocks/README.md` (sections gallery) and `templates/emails/README.md`
   (templates gallery). Reuse existing sections and recipes; build only what is missing.
3. Classify every email in the request, then read `references/surfaces.md`:
   - **Notification template** — transactional, Settings → Notifications (Order confirmation,
     Shipping confirmation …). **Saving makes it live for every real customer immediately.**
   - **Messaging Custom Liquid sections** — marketing email built from sections in the visual
     editor; Shopify keeps its own header (hideable) and legal footer (not removable).
   - **Messaging "Code your own"** — marketing email as one full HTML document; no sections,
     no Shopify footer, must contain `{{ unsubscribe_link }}` and `{{ open_tracking_block }}`.
4. **House rule (Vincent, 2026-10-04): build every marketing email from Messaging Custom Liquid
   sections**, created and assembled one at a time in the Shopify email editor (each becomes a
   reusable section), with recipe surface `messaging-sections`. Choose Code your own only when
   Vincent asks for it. The choice is fixed once the email exists (see Error Handling): a Flow
   step that already holds a Code your own draft needs a new Send step.
5. Approval gates — stop and ask in chat before:
   - saving a notification template (live immediately);
   - turning on any Flow workflow or Messaging automation, or clicking "Turn on" on an email;
   - deleting a Flow step or an existing Messaging email;
   - creating discount codes or any Admin data beyond uploading the email's own images.
   Uploading images to Shopify Files and editing draft emails need no extra approval once the user
   asked for the templates to be installed.
6. Find out every commercial fact the template prints (lead times, dispatch dates, discount codes,
   testimonials). Ask the user for missing values; never ship defaults like "21 days" unconfirmed.

### Step 2: Make the HTML Shopify-ready locally

1. Read `references/html-contract.md` and apply every rule to the source. Library emails are
   edited as sections (`templates/email-blocks/<id>/section.html`) plus recipes
   (`templates/emails/<id>/template.json`), never in the generated template files.
2. Swap provider-specific Liquid for the target surface using the variable tables in
   `references/surfaces.md` (e.g. `abandoned_checkout.url`, `customer.first_name`,
   `{{ unsubscribe_link }}`).
3. Build the install files: `python3 .claude/skills/shopify-email-html/scripts/build_library.py`
   (from the repo root). It validates every recipe, lints every section and writes
   `template.html` (Code your own), `template.liquid.html` (notification) or
   `custom-liquid/NN.html` (sections). For one-off assembly outside the library use
   `scripts/assemble_email.py --mode code-your-own|notification|sections <head> [<liquid header>] <blocks…> -o <out>`;
   to cut an external full email into sections use `scripts/split_cards.py <email.html> <out-dir>`.
4. Lint every file you will install:
   `python3 scripts/lint_email.py <file> --mode notification|section|code-your-own`.
   Fix every ERROR; read every WARN.
5. Check image URLs return 200 (`curl -s -o /dev/null -w '%{http_code}' <url>`). Missing images:
   upload them first (Step 3).

### Step 3: Host images on Shopify Files

1. Confirm the store's Files CDN prefix by curling a known file
   (`https://cdn.shopify.com/s/files/1/<shop-path>/files/<name>`).
2. Upload missing images with the Admin API: `stagedUploadsCreate` (resource `IMAGE`, method POST)
   → `curl -F` each file to the returned target with every returned parameter → `fileCreate`
   with `originalSource` = `resourceUrl`, exact `filename`, alt text, `duplicateResolutionMode:
   RAISE_ERROR`. The browser cannot upload local files (no file chooser access, loopback fetches
   are blocked), so do this via API even when the user wants to "see it in the browser"; then show
   the Files page.
3. If no Admin API tool with `write_files` is available, stop and ask the user to drag the files
   into Content → Files with the exact filenames; continue once the CDN URLs return 200.
4. Re-curl the CDN URLs until they return 200.

### Step 4: Install

Read `references/editor-automation.md` before touching any editor; it lists which inputs work.

1. **Notification template**
   1. Open `admin.shopify.com/store/<store>/email_templates/<template>/edit`.
   2. Back up the current code first: read it with
      `document.querySelector('.cm-content').cmView.view.state.doc.toString()` and save the
      returned text to `templates/hsc-v6-emails/backups/<template>.live-before-<change>.<date>.liquid.html` (write it from
      the tool result; for long templates extract it from the session transcript JSONL with a
      script rather than retyping). Compare the backup's length with the editor's
      `state.doc.length` before continuing.
   3. Inject the new code: `python3 scripts/pack_for_injection.py <file>` prints a JavaScript
      snippet; run it in the page. It must report `match: true` and the expected hash prefix.
   4. Set the Email subject field (click, select all, type).
   5. Click Preview, read the rendered text from the preview iframe, fix Liquid errors.
   6. Get approval (Step 1.5), then Save; confirm the "Notification template saved" toast.
2. **Messaging email from a Flow step** (Flow → workflow → Edit)
   1. New step: add Action → search "Send marketing email" → **Select template → Blank** (the
      sections editor), then rebuild it with Custom Liquid sections. Code your own only if Vincent
      asks. A step that already holds the other type needs a new Send step.
   2. Existing step: open it → Edit email → confirm "revert to draft".
   3. Type into code boxes with the `type` action (the editor is a cross-origin iframe; JS injection
      and paste do not reach it). Strip leading indentation first and check each reported character
      count against the file. (Code your own only: clear first with cmd+a, Delete.)
   4. Sections: **Add section** (bottom-left) → search or scroll to **Custom Liquid** → click the code
      box → type fragment 01 (it carries the fonts and `<style>`); repeat Add section → Custom
      Liquid for each next fragment (new sections append above the Shopify footer). To fix one
      section, select it by clicking its padding (not its text), cmd+a, Delete and retype.
      Hide the stock Header (select it, eye icon at its right edge). Click empty canvas → Email
      colors → Content background swatch → type `transparent` in the hex field, Enter.
   5. Fill Subject and Preview text (scroll the preview to the top first); the email name follows
      the subject.
   6. Exit → **Leave** (keeps it a draft). Never press Turn on without approval.
3. **Flow wiring** — read `references/flow-recipes.md` for the step graphs, the conditions and the
   wait-unit workaround. Prefer asking Shopify **Sidekick** to build the workflow (Flow page →
   Sidekick or the "Tell me what you want to create" box): click **Preview** on each workflow it
   offers, then **Add to store** (top right). Stay on the page until both are added. Never click
   "Turn on workflow".

### Step 5: Verify

1. Notification: preview text shows real fixture values, no raw `{{` / `{%`, correct branch copy.
2. Messaging: the editor preview renders every card with the fixture customer ("Bob"/"John"),
   images load, buttons are pills, corners are round, no white strips between cards, no white
   behind the cards (Content background transparent), no "Default Title" rows.
3. Flow: every Send step shows only the expected "email is in draft state" note; workflow status
   stays **Inactive** unless the user approved activation.
4. Re-hash any injected file and compare with the local file.
5. Update `PROJECT.md` and the `AGENTS.md` state table with what is live, what is draft, and the
   open blockers.

### Step 6: Record in the email library

Follow `references/email-library.md` → "Workflows":

1. Set `shopify_status`, `shopify_matches_repo` and `blockers` in each `template.json` from what
   Shopify actually shows, never from intent.
2. Refresh previews for every new or changed section and template:
   `build_library.py --screenshots <id> …` (Chrome + Pillow; every preview is 1200px wide).
3. Run `build_library.py --check`, then commit sources, generated files and previews on a branch
   and open a pull request.
4. Update Notion (Vincent wants it current): the Sections and Templates records, and the "Messaging
   Journeys" row for each workflow (name, ID, trigger, steps, delays, metrics, blockers). Tick the
   email off in GitHub issue #7.

### Step 7: Report

Report per email: surface, state (live / draft / inactive), what was verified, the library
files and pull request, and blockers such as placeholder testimonials, unconfirmed facts, or the Shopify footer
on sectioned emails. Tell the
user if the page wrote to their clipboard during automation.

## Error Handling

- Typed text landed in the document instead of the search panel: retype the whole section/email
  from the local file; do not try to patch around stray text.
- Search/replace inside an editor code box: one replacement per open of the panel; re-open with
  cmd+f, cmd+a in the search field, triple-click the replace field before typing (see
  `references/editor-automation.md`).
- A Flow step's email cannot be switched between sections and Code your own; the only route is a
  new Send step. Deleting a mid-chain step is not exposed reliably — ask before attempting it.
- A native `<select>` inside Flow (wait unit) will not open in the automated browser: enter the
  wait in seconds (hours × 3600) and tell the user.
- Preview shows the stock template after editing: you are in View-only mode; click Edit and
  confirm the draft dialog.
- `{{ open_tracking }}` / `{{ unsubscribe_url }}` from other platforms: replace with Messaging's
  `{{ open_tracking_block }}` / `{{ unsubscribe_link }}` (Code your own requires both).
- `build_library.py` reports "reads order data, but a messaging-… email only has
  abandoned-checkout": the recipe mixes sections from different contexts. Use or create a section
  with the right context.
- `build_library.py --check` reports STALE files: someone edited a generated file or forgot to
  rebuild. Rebuild; if the hand edit was intended, move it into `section.html` first.
- `screenshot_block.py` says "Liquid render failed (x)": the fixture lacks `x` or the block needs
  another context (Order block with the cart fixture, or a PP-1 block without `--prefix`).
- The editor redraws about a second after each click, so a screenshot taken straight away can show
  the previous selection: wait 2-3 seconds, then look again.
- Unsure whether a variable exists: type a one-line probe (`<p>X={{ var }}</p>`) into a Custom
  Liquid section or Code your own draft and read the preview, then remove it.
