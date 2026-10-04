# v6 build (history)

This folder is how the first five Shopify emails (CR-1 to CR-4, PP-1) were produced on
2026-10-03, built from the Figma file `9Il504CQE8jLaUTBVzphqc` and the brand tokens in
`vincent-laroche/brand-design-system` → `email/`. It was the seed of the email library.

**Do not edit emails here.** The canonical sections and templates are now:

- [`../email-blocks/`](../email-blocks/) — sections database
- [`../emails/`](../emails/) — templates database (recipes, install files, previews)

What is still useful here:

| Path | Purpose |
|---|---|
| `images/` | Source files of the images hosted on Shopify Files (`cdn.shopify.com/s/files/1/0276/9115/5508/files/<name>`). |
| `backups/order-confirmation.live-before-v6.2026-10-03.liquid.html` | Exact copy of the Order confirmation that was live before PP-1. Paste it back to roll back. |
| `build_emails.py` | The original generator; `python3 build_emails.py` rewrites the five `*.liquid.html` files in this folder. |
| `*.liquid.html` | The five full emails as first generated. |

Live state on 2026-10-03: PP-1 is live as the Order confirmation notification. The "Recover
abandoned checkout" Flow workflow is inactive and CR-1 to CR-4 are drafts. Current state is
tracked in each `../emails/*/template.json`.
