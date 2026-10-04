# Email library (sections + templates databases)

The GitHub repository `vincent-laroche/email-marketing` is the only source of truth for email
marketing. Its email library has two linked "databases", stored as plain folders. Check them
**before** building anything: most new emails are a new order of existing sections plus one or
two new ones.

Design authority for every section: `vincent-laroche/brand-design-system`, folder `email/`
(React email blocks, tokens, Figma library "HSC Email Design System" `hpen3ExIfmyI7xBEqC6i2h`).
Read its `email/guides/01-assembling-an-email.md` before designing a new section; never invent
colours, type roles or components that are not there.

## Layout

```
templates/
  email-blocks/                  Sections database
    README.md                    gallery (generated)
    index.tsv                    sortable table, GitHub renders it (generated)
    <NN-slug>/
      section.html               the exact HTML/Liquid of the block (edit by hand)
      section.json               its properties (edit by hand)
      preview.png                1200px-wide render (generated with --screenshots)
      README.md                  page: properties, preview, code (generated)
  emails/                        Templates database
    README.md, index.tsv         (generated)
    <code-slug>/
      template.json              properties + "sections": the ordered recipe (edit by hand)
      template.html              Messaging · Code your own (generated)
      template.liquid.html       Notification template (generated)
      custom-liquid/NN.html      Messaging · Custom Liquid sections, one file per section (generated)
      preview.png, README.md     (generated)
  hsc-v6-emails/                 the original v6 build: generator, images, backups (history)
```

Everything marked "generated" comes from
`.claude/skills/shopify-email-html/scripts/build_library.py`. Never edit those files by hand;
`build_library.py --check` fails when they are stale.

## section.json

| Key | Values |
|---|---|
| `name` | Human name, e.g. "Cart contents". |
| `type` | Email head, Liquid header, Preheader bar, Logo header, Hero, Text, Cart contents, FAQ, Photo + caption, Trust strip, Testimonial, Sign-off + CTA, CTA, Discount code, Checklist, Ink note, Product reminder, Order summary, Timeline, Signature, Preferences footer (add new types as needed). |
| `context` | `any` (no data), `abandoned-checkout` (`abandoned_checkout.*`, Messaging), `customer` (customer, shop and `all_products` data; fixture `fixture-customer.json`), `order` (notification variables + the PP-1 Liquid header). The build rejects a section whose context does not match the template's context. |
| `surfaces` | Where it may be used: `messaging-section`, `messaging-code-your-own`, `notification`. |
| `liquid_variables` | Variables it reads. |
| `placeholders` | `true` when it holds unconfirmed copy; never ship it like that. |
| `notes` | Placement rules or warnings. |

Status (live / draft / unused) is derived from the templates that use the section.

Special sections:
- **Email head** (`00-email-head-fonts-styles`): fonts `<link>` + the single `<style>` block. First
  in every recipe; the assembler puts it in `<head>` or in the first Custom Liquid section.
- **Liquid header** (`24-pp-1-liquid-header-…`): PP-1's Liquid assigns (`is_custom`, `dispatch_s`,
  `delivery_s`, `fname`, `product_summary`). Notification templates only; it lands above
  `<!DOCTYPE>`.

## template.json

| Key | Values |
|---|---|
| `code`, `name` | e.g. `CR-1`, "Your cart's still here". |
| `journey` | e.g. `cart-recovery`, `post-purchase`. |
| `surface` | `notification`, `messaging-code-your-own` or `messaging-sections`; decides the output file. |
| `context` | Optional. The data the email can read: `order` (notification), `abandoned-checkout` (CR Flow) or `customer` (welcome, win-back, reorder, newsletters: `customer.*`, `shop.*`, `all_products`). Defaults from `surface`. A section whose `context` is not `any` or the template's context is rejected. |
| `shopify_location` | Where it lives in Shopify admin. |
| `subject`, `preview_text`, `timing` | As configured in Shopify. Notifications get `preview_text` as a hidden preheader. |
| `html_title` | Optional `<title>`; defaults to the subject (or name when the subject has Liquid). |
| `shopify_status` | `live`, `draft` or `not-installed`: what Shopify shows **now**, never what is intended. |
| `shopify_matches_repo` | `false` while Shopify still runs older code than the generated file. |
| `blockers` | Open issues to report. |
| `sections` | **The recipe**: section ids in assembly order. |

## Workflows

**Build a new template from existing sections**
1. Copy a similar template folder, keep only `template.json`, and edit it: code, name, subject,
   surface, and the `sections` list in the order the cards should stack.
2. Run `python3 .claude/skills/shopify-email-html/scripts/build_library.py --screenshots <new-id>`.
3. Open the template's `README.md` preview, then install the generated file in Shopify (SKILL.md
   Step 4).

**Add or change a section**
1. Create `templates/email-blocks/<NN-slug>/section.html` (next free number) following
   `html-contract.md`, and its `section.json`.
2. Run `build_library.py --screenshots <section-id> <each template that uses it>`. The build lints
   every section with `lint_email.py` and refuses gaps, backgrounds or square cards.
3. Changing a section used by a live template changes that template's generated file; it goes live
   only when installed in Shopify (approval gate). Set `shopify_matches_repo: false` until then.

**After installing in Shopify**: set `shopify_status` and `shopify_matches_repo` in
`template.json`, rebuild, commit.

Screenshots need Google Chrome and Pillow (use a venv: `python3 -m venv .venv && .venv/bin/pip
install pillow`, then run the build with `.venv/bin/python`). Fixtures are fictional
(`assets/fixture-*.json`); never render with real customer data.

## Committing

Work on a branch and open a pull request. Run `build_library.py --check` before committing; the
generated files and `preview.png` must be committed with their sources.

## Notion mirror (secondary)

Notion holds an older mirror of this library (01 Hair Solutions Co. › Company Home › Projects ›
Email Marketing › "Shopify Email Sections" and "Shopify Email Templates"). The repository wins
when they disagree. Update Notion only when the user asks.
