# Shopify email surfaces

Verified against Hair Solutions Co. (`admin.shopify.com/store/oneheadhair`, Files prefix
`cdn.shopify.com/s/files/1/0276/9115/5508/files/`) on 2026-10-03.

## 1. Notification templates (transactional)

- Path: Settings → Notifications → Customer notifications → *template* → **Edit code**.
  Direct URL: `/store/<store>/email_templates/order_confirmation/edit` (`/preview` for read-only).
- Fields: **Email subject** (Liquid allowed) and **Email body (HTML)** — a CodeMirror 6 editor in
  the main admin document (same origin, so JS injection works).
- Saving = live. There is no draft. Always back up first.
- Shopify does not wrap the body: your `<html>`, `<head>` and `<style>` are used as written.
- No Admin API mutation edits notification templates; the browser is the only route.
- Useful order variables: `order_name`, `order_status_url`, `created_at`, `customer.first_name`,
  `billing_address.first_name`, `line_items`, `subtotal_line_items`, `line.product.title`,
  `line.product.handle`, `line.quantity`, `shop.name`, `shop.email`.
- Date maths: `{% assign placed_s = created_at | date: '%s' | plus: 0 %}` then
  `{{ placed_s | plus: 1814400 | date: '%B %-d, %Y' }}`.
- Branching on product type: loop `line_items` and test `li.product.handle contains 'custom'`
  (or a tag/type) to switch copy and lead times.

## 2. Shopify Messaging (marketing email)

Opened from Apps → Messaging, or from a Flow "Send marketing email" step (custom configuration
page). The editor is a **cross-origin iframe** (`email.shopifyapps.com`): page JS cannot read or
write it; drive it with clicks and typing only.

### 2a. Section emails (visual editor)

- Template picker → any template, or edit an existing email.
- **Add section** → *Custom* → **Custom Liquid**: one HTML+Liquid code box per section.
- Shopify adds: a **Header** section (logo) — can only be *hidden* (eye icon), and a black legal
  **footer** (social icons, address, unsubscribe) — cannot be removed.
- "Email colors" panel (click empty canvas): Content background and Border. The picker has no
  alpha slider, but typing `transparent` in the hex field is accepted and stored as
  `RGBA(0,0,0,0)` — set Content background to that (no page background behind the cards).
- `<style>` and `<link>` inside a section are kept in the preview; put them in the first section.
- Do not add `{{ open_tracking_block }}` in sections (Shopify tracks opens itself).

### 2b. "Code your own" (only when Vincent asks; marketing emails are built as sections)

- Template picker → left rail → **Code your own**. One code box for the whole document.
- Required tags (the starter comment says so): `{{ unsubscribe_link }}` and
  `{{ open_tracking_block }}`. `unsubscribe_link` renders a complete `<a>Unsubscribe</a>`; style it
  through a wrapper class (`.unsub a { color:… !important; }`).
- No Shopify header/footer, no sections, no drag-and-drop.
- The upload icon at the top of the code box imports an HTML file (needs a file chooser — not
  usable from the automated browser).

### Messaging variables (abandoned checkout context, verified by probe)

| Need | Liquid |
|---|---|
| Recovery link | `{{ abandoned_checkout.url }}` |
| First name | `{{ customer.first_name }}` |
| Line items | `{% for line_item in abandoned_checkout.line_items %}` |
| Item title / variant / qty | `line_item.product_title`, `line_item.variant_title`, `line_item.quantity` |
| Items beyond the loop limit | `abandoned_checkout.remaining_products_count` |
| Unsubscribe URL only | `{{ unsubscribe_url }}` (renders, but Code your own still requires `unsubscribe_link`) |

- Single-variant products return `variant_title` = `"Default Title"`; guard with
  `!= blank and != 'Default Title'`.
- Auto-applied discount link: append `discount=CODE` to `abandoned_checkout.url` (check for an
  existing `?`). Confirm the code exists: `codeDiscountNodeByCode(code: "CODE")`.

## 3. Shopify Flow

- Workflow list: Apps → Flow. A workflow created from a Messaging automation template opens in the
  Flow editor; each "Send marketing email" step owns one Messaging email.
- Workflow states: Draft/Inactive vs Active (**Turn on workflow**). Email states: Draft vs Active.
  Editing an active email reverts it to Draft ("Customers won't receive this email while in a draft
  state").
- See `flow-recipes.md` for the abandoned-checkout graph.

### Messaging variables outside abandoned checkout (campaigns and non-checkout Flows, verified by probe 2026-10-03)

Probed in a "Code your own" campaign draft preview (sample customer "Bob").

| Need | Liquid | Result |
|---|---|---|
| First name / email / id | `{{ customer.first_name }}`, `{{ customer.email }}`, `{{ customer.id }}` | works |
| Last order | `{{ customer.last_order.name }}`, `{{ customer.last_order.created_at \| date: "%B %-d, %Y" }}` | works |
| Send date | `{{ "now" \| date: "%B %-d, %Y" }}` | works (date at render time) |
| Shop | `{{ shop.name }}`, `{{ shop.url }}`, `{{ shop.email }}`, `{{ shop.permanent_domain }}`, `{{ shop.currency }}` | works |
| Live product price | `{{ all_products['<handle>'].price \| money }}` (`$279.00`), `\| money_without_currency` (`289.00`; price is in cents) | works |
| Product title / path | `{{ all_products['<handle>'].title }}`, `.url` (relative, `/products/<handle>`) | works |
| Customer metafields | `{{ customer.metafields.custom.<key> }}` | renders (empty object for the sample customer); **not verifiable in the preview** |
| View in browser | `view_in_browser_url`, `web_version_url`, `view_online_url`, `view_in_browser_link`, `email_url`, `campaign.url`, `browser_url`, `message.url` | **none render**; leave the link out |
| `shop.products[...]`, `customer.tags`, `customer.orders_count` | | empty |

`{{ unsubscribe_url }}` renders a bare URL, so a cream/light footer can use `<a href="{{ unsubscribe_url }}">` with its
own colour; `{{ unsubscribe_link }}` is still required in Code your own (the shared head forces pale grey on
`.unsub a`, which is unreadable on light cards). Verify that a comment-wrapped `<!-- {{ unsubscribe_link }} -->` satisfies Shopify's check.
