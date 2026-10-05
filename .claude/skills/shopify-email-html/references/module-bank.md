# Module bank

The bank is Vincent's favourite email modules, rebuilt to the v6 email design system in three real themes
(**Bone, Ink, White**), each one a paste-ready Shopify Messaging **Custom Liquid section**. Gallery:
`templates/email-blocks/BANK.md` (sortable table: `bank.tsv`). Source of the module list: Figma page "Modules Library + Hubspot Source", frame "Email module library — organized
by function" (`489:7305`). That page was removed from the working file on 2026-10-05 and now exists only in the
snapshot file `a01FHSyLdgi6ppzaThHl2B` (09 Archive); the Figma links in `section.json` and `modules.tsv` still carry
the working file key `9Il504CQE8jLaUTBVzphqc`, so swap the key to `a01FHSyLdgi6ppzaThHl2B` to open a source cell; `templates/module-bank/modules.tsv` keeps the Figma node of every module and theme.

## Using a module

1. Pick it in `BANK.md` (the three themes sit side by side) or by id: `mb-<category>-<slug>-<theme>`.
2. List the ids in a template's `sections` (surface `messaging-sections`) like any other section, or paste
   `section.html` into a Custom Liquid section. Every bank section is **one card**, so any bank section
   stacks with any other, flush, with a transparent outside.
3. Replace every slot. Copy is a bracketed label (`[Headline]`, `[Body: one or two lines]`, `[Button label]`);
   a bank section is `placeholders: true` and must not ship as is. Image slots are labelled `[Photo · …]`
   until an approved image replaces them (no stock or generated imagery).
4. Choose surfaces by the composition guide, not by taste: no two Paper blocks or two White blocks touching,
   at most two Ink in a row, one coral button, at most two coral marks. Run
   `design-team/skills/email-block-composition/scripts/check_sequence.py` on the sequence.

## The three themes

| | Bone | Ink | White |
|---|---|---|---|
| card / edge | `#f7f1de` / `#e5dfcd` | `#15140f` / `#35332c` | `#ffffff` / `#ececec` |
| text / muted | `#15140f` / `#5a5448` | `#f7f1de` / `#b8b3a4` | `#15140f` / `#5a5448` |
| eyebrow label, serif emphasis | ink | coral | ink |
| inset | `#ffffff` | `#2a2620` | `#f7f1de` |
| logo | ink wordmark | bone wordmark | ink wordmark |

The coral dash, the coral button (ink label) and the pill radius are the same on all three. **Coral text is Ink-only**
(it fails contrast on Bone and White); the build rejects it.

## What changed from the Figma modules

Each section's `section.json` has a `bank.adaptations` list. The common ones:
- text no longer sits on a photo (the photo is a full-bleed top, the copy sits on the card below);
- coral eyebrow or coral text on a light surface becomes ink with the coral dash;
- Title Case headlines become sentence case;
- radii 20 → 12 (cards), 8 (insets), 999 (buttons); storefront tokens → v6 tokens; storefront logo → the v5 wordmark;
- modules named for a colour ("dark ink theme") are renamed for their layout and rebuilt in all three themes;
- coral surfaces are reserved for the coral ask panel (`Action · Main ask` on Coral), not part of the bank;
- design notes inside the Figma frames ("× 20 · infinite scroll") are dropped.

## Generating and changing

Bank sections are **generated**. Edit the module function in `templates/module-bank/cat_NN.py` (one file per category; `build_bank.py` is the generator, `modules.tsv` the Figma index), then:

```bash
python3 templates/module-bank/build_bank.py                 # write section.html + section.json
python3 .claude/skills/shopify-email-html/scripts/build_library.py --screenshots <ids>   # READMEs, BANK.md, previews
python3 templates/module-bank/mobile_preview.py OUT.png <ids>   # 375px render (iframe, so the email head's media queries fire)
python3 templates/module-bank/build_bank.py --check         # stale files or orphans fail
python3 .claude/skills/shopify-email-html/scripts/build_library.py --check
python3 templates/module-bank/build_bank.py --status        # coverage per category
```

Building blocks live in `.claude/skills/shopify-email-html/scripts/v6_html.py` (themes, type roles from `hx.css`,
button, eyebrow, columns, image slot, card). Mobile uses only the classes the shared email head defines
(`.pad .pad-sm .pad-copy .stack .stack-gap .fluid .hero-h .btn`); `templates/module-bank/mobile_preview.py`
renders sections at 375px. `build_library.py` rejects a bank section with more than one card, a colour outside the
v6 palette, a font outside the four v6 families, coral text on Bone or White, or a module missing a theme.

## Figma review page

Figma file "HSC Email - Modules & Emails" (`9Il504CQE8jLaUTBVzphqc`, formerly "Email Design System"), page **Module bank V6** (`779:1067`): all 282 sections as
600px frames, grouped by the 8 categories, one row per module with Bone | Ink | White side by side. Every frame is named
with its section id (`mb-04-product-two-by-two-grid-bone`). It is an imported picture of the generated HTML (plain layers),
not a component library: the repo stays the source, Figma is where the bank is reviewed.

To rebuild after the bank changes: `python3 templates/module-bank/figma_export.py OUT_DIR` writes 24 self-contained
HTML documents (logos inlined, 12 modules each); each is sent through the Figma `html_to_figma` tool with
`cssSelector=.mod` under the page, then the frames are matched to ids by theme, height and text fingerprint and laid out.
Large documents time out at the gateway but still finish on the server; send them one or two at a time.
