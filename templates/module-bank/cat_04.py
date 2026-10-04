"""Category 04 · Products & commerce: one function per module, `fn(theme) -> card rows`. See build_bank.py."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".claude/skills/shopify-email-html/scripts"))
from v6_html import *  # noqa: F401,F403
from bank_registry import module


@module("Product · Two by two product grid", "Product · Two by two grid", "Product",
        ["Lace Edge 360+ $289 · ★ 4.8", "SkinLife Ultra $319 · ★ 4.9", "MonoCrown $259 · ★ 4.7", "Hybrid Lace-Skin $339 · ★ 4.8"],
        ["Tiles stay two across on mobile (they shrink; they never stack to one column)",
         "Grid is centred in the card and each tile's name and price line are centred under its image (the Figma grid sat left, leaving the right third empty)",
         "Product name in the v6 name role, price/rating line in the v6 meta role",
         "Image tiles are labelled slots: use the approved product renders (square, on the card inset)",
         "Removed the 'x20 · infinite scroll + load more' annotation (a design note, not email content)"])
def product_grid_2x2(th):
    def tile(i):
        return (photo_slot(f"[Photo · product {i}]", th, 200) + gap(10) + name(f"[Product {i}]", th, "center", mb=2) +
                meta("[Price] · [Rating]", th, "center"))
    rows = pair_row([tile(1), tile(2)], th, 24) + gap(28) + pair_row([tile(3), tile(4)], th, 24)
    return card(rows, th, pad="40px 30px", cls="pad-sm")


def _mini(label, th, h):
    """A photo slot for narrow tiles: the label gets less side padding so it fits in a 70px column."""
    return photo_slot(label, th, h).replace("padding:0 16px", "padding:0 4px")


def _line(left, right):
    """Two cells on one line, the second right-aligned and never wrapping (name and price)."""
    return ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>'
            f'<td valign="baseline" style="width:100%;padding:0 16px 0 0;">{left}</td>'
            f'<td valign="baseline" align="right" style="padding:0;white-space:nowrap;">{right}</td></tr></table>')


@module("Product", "Product · Three card row", "Product",
        ["Refined Density · From $420", "Natural Movement · From $420", "Longer Lengths · From $420"],
        ["Three product cards in a row; on mobile they stack one per line (a 169px card does not fit three across)",
         "Card fill and 20px radius dropped: tiles sit directly on the card, image on the v6 inset (8px)",
         "Title in the v6 subtitle role (sentence case), price in the v6 serif-italic price role",
         "Image tiles are labelled slots: use approved product renders"])
def product_three_cards(th):
    def tile(i):
        return photo_slot("[Photo]", th, 120) + gap(12) + subtitle(f"[Product {i}]", th, mb=4) + price("[From $00]", th)
    return card(cols([tile(1), tile(2), tile(3)], 16), th, pad="32px", cls="pad-sm")


@module("Product · Single product feature", "Product · Single feature with button", "Product",
        ["Swiss Lace Atelier System", "$580", "Featuring single-knot hair ventilation…", "Configure Your Fit →"],
        ["One large product image with the name, price, one line of copy and a button below it",
         "Name in the v6 title role, price in the v6 serif-italic price role (was two 22px sans lines)",
         "Button is the v6 coral pill (58px high, ink label, arrow)",
         "Image is a labelled slot: use the approved product render"])
def product_single_feature(th):
    return card(photo_slot("[Photo · product]", th, 300) + gap(22) +
                _line(title("[Product name]", th, mb=0), price("[$00]", th)) + gap(12) +
                body("[Body: one or two lines about the product]", th, mb=22) + button("[Button label]", th),
                th, pad="32px", cls="pad-sm")


@module("Product · Two-column product grid", "Product · Two column grid", "Product",
        ["Poly Skin Perimeter $490", "Atelier Silk Top $620"],
        ["Two product tiles side by side; they stay two across on mobile (shrinking, never stacking)",
         "Tile fill and 16px padding dropped; image on the v6 inset, text under it in the v6 name and price roles",
         "Image tiles are labelled slots: use approved product renders"])
def product_two_column_grid(th):
    def tile(i):
        return photo_slot(f"[Photo · product {i}]", th, 180) + gap(14) + name(f"[Product {i}]", th, mb=2) + price("[$00]", th, small_=True)
    return card(pair_row([tile(1), tile(2)], th, 20), th, pad="32px 28px", cls="pad-sm")


@module("Product · Asymmetric image-details split", "Product · Image and details split", "Product",
        ["French Lace Active · $520", "A highly durable, breathable lace mesh base…", "Shop French Lace →"],
        ["Narrow image left, details right; the columns stack on mobile with the image first",
         "Product name in the v6 title role, price in the v6 serif-italic role; button is the v6 coral pill at 46px",
         "Image is a labelled slot: use the approved product render"])
def product_image_details_split(th):
    details = (title("[Product name]", th, mb=6) + price("[$00]", th, small_=True, mb=14) +
               body("[Body: two or three lines]", th, mb=18) + button("[Button label]", th, size=13, height=46, padx=24))
    return card(cols([photo_slot("[Photo · product]", th, 250), details], 24, valign="middle", weights=[37, 63]),
                th, pad="32px", cls="pad-sm")


@module("Product · Three-column product row", "Product · Three column row", "Product",
        ["Citrus Cleanser $28", "pH Shampoo $24", "Lace Sealer $32"],
        ["Three compact tiles (care products); they stay three across on mobile, shrinking",
         "Tile fill dropped; image on the v6 inset, name in the v6 small role, price in the serif-italic price role",
         "Image tiles are labelled slots: use approved product renders"])
def product_three_column_row(th):
    def tile(i):
        return (_mini("[Photo]", th, 110) + gap(10) + name(f"[Product {i}]", th, "center", mb=2) +
                price("[$00]", th, "center", small_=True))
    return card(pair_row([tile(1), tile(2), tile(3)], th, 16), th, pad="28px 24px", cls="pad-sm")


@module("Product · Featured system banner", "Product · Featured banner with badge", "Product",
        ["LIMITED RELEASE", "The Masterpiece Swiss Lace $520 (was $580)", "Secure an introductory rate…", "Order Featured System →"],
        ["The 'Limited release' badge sat on the photo: moved onto the copy, above the title (no text on photos)",
         "Image is a labelled slot above the copy; the title uses the v6 title role, the sale price the serif-italic price role with the old price struck through in muted",
         "Button is the v6 coral pill"])
def product_featured_banner(th):
    row = ('<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>'
           f'<td style="padding:0 10px 0 0;">{price("[$00]", th)}</td>'
           f'<td style="padding:0;"><span style="font-family:{SANS};font-size:16px;line-height:20px;text-decoration:line-through;'
           f'color:{th["muted"]};">[$00]</span></td></tr></table>')
    return card(photo_slot("[Photo · featured system]", th, 260) + gap(22) + badge("[Badge]", th) + gap(14) +
                title("[Product name]", th, mb=10) + row + gap(10) +
                body("[Body: one or two lines]", th, mb=22) + button("[Button label]", th), th, pad="32px", cls="pad-sm")


@module("Product · Recommended products thumbnail", "Product · Recommended thumbnails", "Product",
        ["You may also like", "Citrus Release Elixir", "Scalp Protector Spray", "Waterproof Bond Adhesive", "COMPANION CARE"],
        ["Three small cards (thumbnail left, text right); on mobile they stack one per line",
         "Heading in the v6 eyebrow role (sentence case sample copy, label uppercase by role)",
         "Card fill dropped: each tile is the v6 inset (8px) with the thumbnail on the card colour",
         "Thumbnails are labelled slots: use approved product renders"])
def product_recommended_thumbs(th):
    def tile(i):
        inner = ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>'
                 f'<td width="48" valign="middle" style="width:48px;padding:0;">{_mini("", th, 48)}</td>'
                 f'<td valign="middle" style="padding:0 0 0 10px;">{name(f"[Product {i}]", th, mb=2)}{meta("[Tag]", th)}</td></tr></table>')
        return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" '
                f'style="border-collapse:separate;background-color:{th["inset"]};border:1px solid {th["inset_edge"]};'
                f'border-radius:8px;"><tr><td style="padding:10px;">{inner}</td></tr></table>')
    return card(eyebrow("[Heading]", th, mb=18) + cols([tile(1), tile(2), tile(3)], 12), th, pad="32px", cls="pad-sm")


@module("RECENTLY VIEWED PRODUCT", "Product · Recently viewed", "Product",
        ["YOU LOOKED AT THIS", "System 01 - Lace, Base 06", "$329.00"],
        ["Thumbnail left, text right; stays side by side on mobile",
         "Eyebrow in the v6 eyebrow role (coral dash, ink on light); title in the v6 name role; price in the serif-italic price role"])
def product_recently_viewed(th):
    row = ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>'
           f'<td width="100" valign="middle" style="width:100px;padding:0;">{photo_slot("[Photo]", th, 100)}</td>'
           f'<td valign="middle" style="padding:0 0 0 20px;">{eyebrow("[Eyebrow]", th, mb=8)}{name("[Product name]", th, mb=6)}'
           f'{price("[$00.00]", th)}</td></tr></table>')
    return card(row, th, pad="28px 32px", cls="pad-sm")


@module("SHOP BY COLLECTION", "Product · Shop by collection", "Product",
        ["Shop by collection", "Lace", "Poly", "Skin", "Care"],
        ["Four collection thumbnails with centred names; they stay four across on mobile",
         "Heading in the v6 title role (was a 17px label); names in the v6 name role",
         "Thumbnails are labelled slots: use approved collection images"])
def product_shop_by_collection(th):
    def tile(i):
        return _mini("[Photo]", th, 90) + gap(8) + name(f"[Name {i}]", th, "center", mb=0)
    return card(subtitle("[Heading]", th, mb=16) + pair_row([tile(1), tile(2), tile(3), tile(4)], th, 12),
                th, pad="32px 28px", cls="pad-sm")


def _cell(text_html, th, align="center", top=True, w=None):
    b = f"border-top:1px solid {th['rule']};" if top else ""
    wd = f"width:{w}%;" if w else ""
    return f'<td align="{align}" valign="middle" style="{wd}{b}padding:12px 4px;text-align:{align};">{text_html}</td>'


@module("LACE VS. POLY COMPARISON", "Product · Comparison table", "Product",
        ["Lace vs. Poly", "Breathability: Excellent / Good", "Durability: Moderate / Excellent", "Best for: Active styling / Daily wear"],
        ["Three-column table (attribute plus two values) with hairline rows",
         "Attribute labels in the v6 mono meta role, column headers and values in the v6 name role (was 12px sans)",
         "Table title in the v6 title role",
         "Column headers are slots ([Option A], [Option B]), not a fixed lace/poly pair"])
def product_comparison_table(th):
    head = ('<tr>' + _cell("", th, top=False, w=30) + _cell(name("[Option A]", th, "center", mb=0), th, top=False, w=35) +
            _cell(name("[Option B]", th, "center", mb=0), th, top=False, w=35) + '</tr>')
    rows = "".join('<tr>' + _cell(meta(f"[Attribute {i}]", th, "left"), th, "left") +
                   _cell(small("[Value]", th, "center"), th) + _cell(small("[Value]", th, "center"), th) + '</tr>'
                   for i in (1, 2, 3))
    table = ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" '
             f'style="border-collapse:collapse;">{head}{rows}</table>')
    return card(title("[Table title]", th, mb=14) + table, th, pad="40px", cls="pad-sm")


@module("Recommended specification", "Product · Recommended specification", "Product",
        ["YOUR SPECIFICATION", "What we recommended", "Base: French lace · Density: Medium · Colour: #4 — Dark Brown · Base size: 8\" × 6\" · Quoted price: $580.00",
         "Reply and tell me what you'd change…", "Confirm this specification →"],
        ["Label/value rows between hairlines, the same pattern as the v6 order details (labels mono uppercase, values bold, right-aligned)",
         "Title in the v6 title role (sentence case); eyebrow in the v6 eyebrow role; body in the v6 body role; button is the v6 coral pill",
         "Row labels and values are slots; the row count (five) is kept"])
def product_recommended_spec(th):
    rows = kv_rows([(f"[Label {i}]", "[Value]") for i in range(1, 6)], th)
    return card(eyebrow("[Eyebrow]", th, mb=14) + title("[Title]", th, mb=18) + rows + gap(22) +
                body("[Body: two lines]", th, mb=22) + button("[Button label]", th), th, pad="40px")


@module("Base comparison", "Product · Base comparison", "Product",
        ["COMPARE", "Lace: Most natural, shortest life", "Poly: Most durable, easy to clean", "Hybrid: Balanced — most people end up here"],
        ["Three label/value rows between hairlines (same pattern as the recommended specification)",
         "Eyebrow in the v6 eyebrow role; the Figma 'paper' name dropped (the module now exists in three themes)"])
def product_base_comparison(th):
    rows = kv_rows([(f"[Option {i}]", "[Value: one short line]") for i in (1, 2, 3)], th)
    return card(eyebrow("[Eyebrow]", th, mb=14) + rows, th, pad="40px")
