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
