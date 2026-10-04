# Email HTML contract for Shopify

Rules learned shipping the HSC v6 emails. Apply them in the generator, then lint.

## Structure

1. Table layout only. Outer table `width="100%"` with a transparent background → centred shell
   table `class="shell"`, `width:600px;max-width:600px` (full document) or
   `width:100%;max-width:600px` (Messaging section; the column is already ~600px).
2. One card = one row: `<tr><td style="padding:0;">` + card table. **No spacer padding between
   cards** (`padding:0 0 2px 0` shows as white strips; the design system stacks blocks with
   `gap: 0`).
3. Card table: `border-collapse:separate;background-color:<surface>;border:1px solid <line>;
   border-radius:12px;` (`--hsc-radius-option`). Insets (quote boxes, code chips, portraits)
   use 8px (`--hsc-radius-inset`). Buttons 999px.
4. Body/outer background stays `transparent`: no page colour behind the modules, not even the
   brand cream. In Shopify Messaging also set Email colors → **Content background** to
   `transparent` (type it in the hex field) or Shopify paints white behind every section. The
   client's canvas shows through the corner wedges of rounded cards; that cannot be removed
   without square corners — say so if asked.
5. Full-bleed photo at the top of a card: image `border-radius:12px 12px 0 0` and the card
   `overflow:hidden`.

## Buttons

- `<table class="btn" style="border-collapse:separate;…">` → `<td style="border-radius:999px;
  background-color:<fill>;">` → `<a style="display:inline-block;…;border-radius:999px;">`.
- Put an outline **on the `<a>`**, never on the `<td>`: Shopify Messaging collapses table borders,
  which squares off a bordered cell. Reduce the link's `line-height` by 2px to keep the height.

## Head

- Keep `<meta name="x-apple-disable-message-reformatting">`, colour-scheme metas, MSO
  `PixelsPerInch` block, Google Fonts `<link>` and one `<style>` block with the mobile media
  query (`.shell`, `.pad`, `.btn`, `.stack`, `.fluid` overrides).
- Hidden preheader `<div style="display:none…">`: keep it for notification templates; drop it
  for Messaging (use the Preview text field — both together duplicate the inbox snippet).

## Liquid

- Default every personalisation: `{{ customer.first_name | default: "there" }}`.
- Guard `variant_title` against `"Default Title"`.
- Balance every `{% if %}/{% endif %}`, `{% for %}/{% endfor %}`, `{% unless %}`; the linter
  counts them.
- Never hard-code commercial facts the user has not confirmed (lead times, prices, discount codes,
  testimonials). Leave clearly marked placeholders and report them as blockers.

## Images

- Host on Shopify Files; reference `https://cdn.shopify.com/s/files/1/<shop-path>/files/<name>`.
- Give every image explicit `width`/`height`, `display:block`, `border:0`, real alt text.

## Footer

- Notification templates: service-email wording; no marketing unsubscribe needed.
- Messaging section emails: your footer card plus Shopify's mandatory footer (two legal blocks).
  Acceptable; mention it.
- Messaging Code your own: your footer must contain `{{ unsubscribe_link }}` and the physical
  address; add `{{ open_tracking_block }}` just before `</body>`.
