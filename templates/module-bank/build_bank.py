#!/usr/bin/env python3
"""Generate the HSC email module bank: every module in three real themes (Bone, Ink, White).

Source of the module list: Figma file 9Il504CQE8jLaUTBVzphqc, page "Modules Library + Hubspot Source",
frame "Email module library — organized by function" (489:7305). `modules.tsv` holds the 94 definitions
with the Figma module node of each theme cell. Each implemented module is one function below,
`fn(theme) -> card rows`, rebuilt to the v6 email design system (see v6_html.py).

Output: templates/email-blocks/mb-<NN>-<slug>-<theme>/{section.html, section.json}. These folders are
generated: change the module function here, never the files. The gallery, READMEs and previews are
produced afterwards by .claude/skills/shopify-email-html/scripts/build_library.py.

Usage:
    python3 templates/module-bank/build_bank.py            # write the folders
    python3 templates/module-bank/build_bank.py --check    # fail if any generated file is stale or a module lacks a theme
    python3 templates/module-bank/build_bank.py --status   # coverage report (implemented / total per category)
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude/skills/shopify-email-html/scripts"))
from v6_html import *  # noqa: E402,F401,F403
import v6_html as V  # noqa: E402

BLOCKS = ROOT / "templates/email-blocks"
THEME_ORDER = ["bone", "ink", "white"]
CATEGORIES = {"01": "Global chrome", "02": "Heroes", "03": "Titles & editorial", "04": "Products & commerce",
              "05": "Services & proof", "06": "CTAs & promotions", "07": "Transactional lifecycle", "08": "Utility"}
FIGMA_FILE = "https://www.figma.com/design/9Il504CQE8jLaUTBVzphqc/Email-Design-System?node-id="


def slugify(s):
    s = s.lower().replace("·", " ").replace("&", " and ").replace("+", " plus ")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def load_index():
    rows = []
    for line in (Path(__file__).parent / "modules.tsv").read_text(encoding="utf-8").splitlines():
        cat, src, ids = line.split("|")
        rows.append({"cat": cat, "source": src, "figma": dict(zip(THEME_ORDER, ids.split(",")))})
    return rows


# ---------------------------------------------------------------- the module registry
MODULES = {}


def module(source, name, type_, copy, adaptations, notes=""):
    """Register a module function. `source` is the Figma row name, `name` the bank name (renamed when the
    Figma name described a colour). `copy` is the Figma sample copy, kept for reference only."""
    def deco(fn):
        MODULES[source] = dict(fn=fn, name=name, type=type_, copy=copy, adaptations=adaptations, notes=notes)
        return fn
    return deco


# ---------------- 01 · Global chrome
@module("Navigation · Full Brand Utility Bar", "Navigation · Utility bar with links", "Navigation",
        ["Journal", "Cart (0)", "Shop systems", "System guide", "Care", "Support"],
        ["Coral 'Cart' label → muted (coral text fails contrast on light surfaces)",
         "Logo is the approved v5 wordmark on Shopify Files (ink on light, bone on ink), not the storefront logo image",
         "Links in the v6 eyebrow face (Inter Tight 600, tracked) and the card on the v6 12px radius",
         "Logo and links stay side by side on mobile; the links wrap to two lines"])
def nav_utility(th):
    util = ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>'
            f'<td align="left" width="50%" style="width:50%;">{meta("[Utility link]", th)}</td>'
            f'<td align="right" width="50%" style="width:50%;">{meta("[Cart]", th, "right")}</td></tr></table>')
    links = "".join(f'<a href="{SITE}" target="_blank" style="font-family:{DISPLAY};font-size:12px;line-height:20px;'
                    f'font-weight:600;letter-spacing:1.5px;text-transform:uppercase;color:{th["text"]};'
                    f'text-decoration:none;padding-left:16px;white-space:nowrap;display:inline-block;">[Link {i}]</a>'
                    for i in range(1, 5))
    brand = ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>'
             f'<td align="left" valign="middle" width="112" style="width:112px;">{logo(th, 112, center=False)}</td>'
             f'<td align="right" valign="middle">{links}</td></tr></table>')
    return card(util + gap(16) + brand, th, pad="24px 40px", cls="pad")


# ---------------- 02 · Heroes
@module("Hero · Image background with overlaid", "Hero · Image with text below", "Hero",
        ["Atelier invitation", "Bespoke Hair Systems",
         "Hand-crafted, custom matched, and completely natural. Book your signature consultation today.",
         "Schedule Appointment"],
        ["Text no longer sits on the photo (v6: never put text on a photo): the image is a full-bleed top, the copy sits on the card surface below",
         "Headline in sentence case, 48/50 Inter Tight 800", "Button is the v6 primary pill (coral, ink label, arrow)"])
def hero_image_text_below(th):
    text = (eyebrow("[Eyebrow]", th, center=True) + headline("[Headline]", th, "center") +
            body("[Body: one or two lines]", th, "center", mb=26) + button("[Button label]", th, center=True))
    return card_flush(photo_bleed("[Photo · hero image]", th, 280) +
                      f'<tr><td class="pad" style="padding:40px;">{text}</td></tr>', th)


# ---------------- 03 · Titles & editorial
@module("Title · Coral accent line", "Title · Centred with short rule", "Title",
        ["pH-Balanced Botanic Formulas", "Sulfate-free citrus extracts engineered to cleanse custom Swiss lace bases safely."],
        ["The 60x3 coral bar becomes the v6 edge rule (short, centred, 32px, 24px to the heading)",
         "Title in the v6 title role (Inter Tight 700, 28/31), body in the v6 body role"])
def title_short_rule(th):
    rule = ('<table role="presentation" align="center" cellpadding="0" cellspacing="0" border="0" style="margin:0 auto 24px auto;">'
            f'<tr><td width="32" style="width:32px;"><div style="height:2px;line-height:2px;font-size:0;background-color:{CORAL};">&nbsp;</div></td></tr></table>')
    return card(rule + title("[Title]", th, "center", mb=14) + body("[Body: one or two lines]", th, "center", mb=0),
                th, pad="48px 40px")


# ---------------- 04 · Products & commerce
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


# ---------------- 05 · Services & proof
@module("SERVICE · STATS BAND DARK", "Service · Stats band", "Stats",
        ["By the numbers", "10K+ Customers", "97% Satisfaction", "15+ Years", "40+ Salons"],
        ["Figma named it 'dark' but drew bone text on a bone card: rebuilt as a real three-theme module",
         "Numerals: Inter Tight 800 with a serif-italic suffix; the suffix is coral only on Ink, ink on light",
         "Eyebrow in the v6 eyebrow role (coral dash, label ink on light, coral on Ink)",
         "Eyebrow, numerals and labels are centred, so the 2x2 grid is balanced in the card",
         "Two across on mobile (no stacking)"])
def stats_band(th):
    def stat(i):
        value = (f'<p style="margin:0 0 6px 0;font-family:{DISPLAY};font-size:56px;line-height:60px;font-weight:800;'
                 f'letter-spacing:-2px;text-align:center;color:{th["text"]};">[00]{em("+", th)}</p>')
        return value + meta(f"[Label {i}]", th, "center")
    grid = pair_row([stat(1), stat(2)], th, 24) + gap(28) + pair_row([stat(3), stat(4)], th, 24)
    return card(eyebrow("[Eyebrow]", th, center=True, mb=28) + grid, th, pad="48px 40px")


# ---------------- 06 · CTAs & promotions
@module("CTA · CORAL ACCENT PANEL", "CTA · Centred panel with rule", "CTA",
        ["Exclusive Member Offer", "Sign up today and receive a complimentary botanical adhesive release elixir with your first order.", "Claim Offer"],
        ["Figma drew a full coral surface; in v6 coral is a surface only for the ask panel (Action · Main ask on Coral), so the three themes use a short coral edge rule and the coral button",
         "Sentence case title in the v6 title role, v6 primary pill button"],
        notes="The real v6 coral panel is a fourth, coral-only surface; it is not part of the Bone / Ink / White bank.")
def cta_panel_rule(th):
    rule = ('<table role="presentation" align="center" cellpadding="0" cellspacing="0" border="0" style="margin:0 auto 24px auto;">'
            f'<tr><td width="32" style="width:32px;"><div style="height:2px;line-height:2px;font-size:0;background-color:{CORAL};">&nbsp;</div></td></tr></table>')
    return card(rule + title("[Title]", th, "center", mb=14) + body("[Body: one or two lines]", th, "center", mb=26) +
                button("[Button label]", th, center=True), th, pad="56px 40px")


# ---------------- 07 · Transactional lifecycle
@module("SHIPPING TRACKER", "Order · Shipping tracker", "Transactional",
        ["On its way to you", "Processed / Shipped / In transit / Delivered", "Carrier: UPS Ground", "Tracking number: 1Z999AA10123456784",
         "Estimated arrival: Aug 9", "Track package"],
        ["Progress uses the text colour for finished steps, not coral (coral budget: one button plus at most two marks)",
         "Inactive steps use the v6 strong line; step labels in the v6 small role",
         "Detail rows use the v6 label/value hairline rows",
         "All values are slots (carrier, tracking number, arrival); wire them to the shipping variables in the template"])
def shipping_tracker(th):
    done = [True, True, False, False]
    labels = ["[Step 1]", "[Step 2]", "[Step 3]", "[Step 4]"]

    def dot(on):
        c = th["text"] if on else LINE_STRONG
        return (f'<div style="width:12px;height:12px;line-height:12px;font-size:0;border-radius:999px;'
                f'background-color:{c};">&nbsp;</div>')

    def rule(on):
        c = th["text"] if on else LINE_STRONG
        return f'<div style="height:2px;line-height:2px;font-size:0;background-color:{c};">&nbsp;</div>'

    cells = []
    for i in range(4):
        if i < 3:
            inner = ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>'
                     f'<td width="12" valign="middle" style="width:12px;">{dot(done[i])}</td>'
                     f'<td valign="middle" style="padding:0 6px 0 6px;">{rule(done[i] and done[i + 1])}</td></tr></table>')
        else:
            inner = f'<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td width="12" style="width:12px;">{dot(done[i])}</td></tr></table>'
        cells.append(f'<td width="25%" valign="middle" style="width:25%;">{inner}</td>')
    progress = f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>{"".join(cells)}</tr></table>'
    lab = ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>' +
           "".join(f'<td width="25%" valign="top" style="width:25%;padding-top:8px;">{small(l, th)}</td>' for l in labels) +
           '</tr></table>')
    rows = kv_rows([("Carrier", "[Carrier]"), ("Tracking number", "[Tracking number]"), ("Estimated arrival", "[Estimated arrival]")], th)
    return card(subtitle("[Status line]", th, mb=18) + progress + lab + gap(18) + rows + gap(24) +
                button("[Button label]", th), th, pad="40px")


# ---------------- 08 · Utility
@module("Regard / sign-off", "Utility · Sign-off", "Sign-off",
        ["Warmly,", "Hair Solutions Co.", "A new look should still feel unmistakably like you."],
        ["Closing in the v6 body role, name in the v6 subtitle role, tagline in the v6 note role (serif italic)",
         "Never a handwritten-signature image"])
def signoff(th):
    return card(body("[Closing],", th, mb=10) + subtitle("[Name]", th, mb=10) + note("[Tagline: one short line]", th, mb=0),
                th, pad="36px 40px")


# ---------------------------------------------------------------- generation
def generate():
    """Return {relative path: text} for every implemented module in every theme."""
    files, index = {}, load_index()
    seen = set()
    for row in index:
        spec = MODULES.get(row["source"])
        if not spec:
            continue
        seen.add(row["source"])
        slug = slugify(spec["name"])
        for t in THEME_ORDER:
            th = V.THEMES[t]
            sid = f"mb-{row['cat']}-{slug}-{t}"
            html = section(spec["fn"](th))
            meta_ = {
                "name": f"{spec['name']} · {th['label']}",
                "type": spec["type"],
                "context": "any",
                "surfaces": ["messaging-code-your-own", "messaging-section"],
                "liquid_variables": [],
                "placeholders": True,
                "notes": ("Module bank. All copy is a labelled slot: replace it before use. " + spec["notes"]).strip(),
                "bank": {
                    "category": f"{row['cat']} · {CATEGORIES[row['cat']]}",
                    "module": spec["name"],
                    "theme": t,
                    "figma_source": row["source"],
                    "figma_node": FIGMA_FILE + row["figma"][t].replace(":", "-"),
                    "sample_copy": spec["copy"],
                    "adaptations": spec["adaptations"],
                },
            }
            files[f"templates/email-blocks/{sid}/section.html"] = html
            files[f"templates/email-blocks/{sid}/section.json"] = json.dumps(meta_, indent=2, ensure_ascii=False) + "\n"
    unknown = set(MODULES) - seen
    if unknown:
        raise SystemExit(f"modules without a row in modules.tsv: {sorted(unknown)}")
    return files


def status():
    index = load_index()
    by_cat = {}
    for r in index:
        c = by_cat.setdefault(r["cat"], [0, 0])
        c[1] += 1
        c[0] += r["source"] in MODULES
    for cat, (done, total) in sorted(by_cat.items()):
        print(f"{cat} · {CATEGORIES[cat]:<26} {done:>2}/{total:<2}")
    done = sum(v[0] for v in by_cat.values())
    total = sum(v[1] for v in by_cat.values())
    print(f"{'total':<31} {done:>2}/{total:<2}  ({done * 3} of {total * 3} sections)")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "--status":
        return status()
    files = generate()
    if mode == "--check":
        stale = []
        for rel, text in files.items():
            p = ROOT / rel
            if not p.exists() or p.read_text(encoding="utf-8") != text:
                stale.append(rel)
        existing = {str(p.relative_to(ROOT)) for d in BLOCKS.glob("mb-*") for p in d.iterdir()
                    if p.name in ("section.html", "section.json")}
        orphans = sorted(existing - set(files))
        if stale or orphans:
            print("STALE:", *stale, *["ORPHAN: " + o for o in orphans], sep="\n  ")
            raise SystemExit(1)
        print(f"ok: {len(files) // 2} bank sections up to date")
        return
    for rel, text in files.items():
        p = ROOT / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    print(f"wrote {len(files) // 2} sections")
    status()


if __name__ == "__main__":
    main()
