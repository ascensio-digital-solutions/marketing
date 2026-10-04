"""Category 05 · Services & proof: one function per module, `fn(theme) -> card rows`. See build_bank.py."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".claude/skills/shopify-email-html/scripts"))
from v6_html import *  # noqa: F401,F403
from bank_registry import module


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


def _chip(th, size=36):
    """A neutral icon slot: round inset chip with a plus. Swap for an approved icon; emails use no icon components."""
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:separate;">'
            f'<tr><td align="center" valign="middle" width="{size}" height="{size}" style="width:{size}px;height:{size}px;'
            f'border-radius:999px;background-color:{th["inset"]};font-family:{DISPLAY};'
            f'font-size:16px;line-height:{size - 2}px;font-weight:700;color:{th["text"]};text-align:center;">+</td></tr></table>')


def _chip_c(th, size=36):
    return f'<div style="margin:0 auto;width:{size}px;">{_chip(th, size)}</div>'


def _num(text, th, w=48):
    return (f'<p style="margin:0;font-family:{DISPLAY};font-size:32px;line-height:36px;font-weight:800;letter-spacing:-1px;'
            f'color:{th["text"]};width:{w}px;">{text}</p>')


@module("Service", "Service · Three feature columns", "Service",
        ["Considered construction", "Specification guidance", "Long-term care", "Clear guidance for every decision."],
        ["Three centred feature columns; they stack on mobile",
         "Icon glyphs (★ + →) replaced by one neutral icon chip: swap for an approved icon",
         "Title in the v6 subtitle role, body in the v6 small role (sentence case)"])
def service_three_columns(th):
    def col(i):
        return _chip_c(th) + gap(14) + subtitle(f"[Feature {i}]", th, "center", mb=6) + small("[Body: one short line]", th, "center")
    return card(cols([col(1), col(2), col(3)], 20), th, pad="40px 32px", cls="pad-sm")


@module("SERVICE · ARTISANAL VENTILATING METHOD", "Service · Centred method with button", "Service",
        ["Artisanal Ventilating Method", "Every strand of premium natural hair is individually…", "Learn our method →"],
        ["Heading in the v6 title role, body in the v6 body role, both centred",
         "Icon glyph replaced by the neutral icon chip; button is the v6 coral pill (46px)"])
def service_centred_method(th):
    return card(_chip_c(th, 40) + gap(18) + title("[Heading]", th, "center", mb=14) +
                body("[Body: three or four lines]", th, "center", mb=22) +
                button("[Button label]", th, center=True, size=13, height=46, padx=24), th, pad="48px 40px")


@module("SERVICE · CONSTRUCTION & SIZING", "Service · Two feature columns", "Service",
        ["Lace Construction", "Custom Sizing"],
        ["Two columns of icon, title and copy; they stack on mobile",
         "Icon glyphs replaced by the neutral icon chip; title in the v6 subtitle role, body in the v6 body role"])
def service_two_columns(th):
    def col(i):
        return _chip(th) + gap(14) + subtitle(f"[Feature {i}]", th, mb=8) + body("[Body: two or three lines]", th, mb=0)
    return card(cols([col(1), col(2)], 24), th, pad="40px")


@module("SERVICE · KEY BENEFITS", "Service · Three key benefits", "Service",
        ["Premium Hair", "Perfect Match", "Secure Fit"],
        ["Compact three-benefit row (icon, short title, one line); stays three across on mobile",
         "Icon glyphs replaced by the neutral icon chip; title in the v6 name role, description in the v6 small role"])
def service_key_benefits(th):
    def col(i):
        return _chip_c(th, 32) + gap(10) + name(f"[Benefit {i}]", th, "center", mb=4) + small("[One line]", th, "center")
    return card(pair_row([col(1), col(2), col(3)], th, 16), th, pad="32px 24px", cls="pad-sm")


@module("SERVICE · ARTISAN BIO-BASE", "Service · Image and base standard", "Service",
        ["THE BASE STANDARD", "Artisan Bio-Base", "Designed to completely mimic natural follicle…"],
        ["Square image left with eyebrow, heading and body right; stacks on mobile with the image first",
         "Eyebrow in the v6 eyebrow role (the Figma pill label dropped); heading in the v6 title role",
         "Image is a labelled slot: use an approved render"])
def service_image_and_standard(th):
    text = eyebrow("[Eyebrow]", th, mb=12) + title("[Heading]", th, mb=10) + body("[Body: three lines]", th, mb=0)
    return card(cols([photo_slot("[Photo]", th, 160), text], 24, valign="middle", weights=[34, 66]), th, pad="32px", cls="pad-sm")


@module("SERVICE · BESPOKE PROCESS", "Service · Numbered steps with rules", "Service",
        ["01 Bespoke Fitting Consultation", "02 Hand-Woven Fabrication"],
        ["Two numbered steps separated by a hairline; numbers in Inter Tight 800 on the v6 type scale",
         "Step title in the v6 subtitle role, description in the v6 body role"])
def service_numbered_steps(th):
    def step(n, last=False):
        row = ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>'
               f'<td width="64" valign="top" style="width:64px;padding:0;">{_num(f"0{n}", th)}</td>'
               f'<td valign="top" style="padding:0;">{subtitle(f"[Step {n} title]", th, mb=6)}{body("[Body: two lines]", th, mb=0)}</td></tr></table>')
        return row
    return card(step(1) + hairline(th, mb=24, mt=24) + step(2), th, pad="40px")


@module("SERVICE · PURCHASE ASSURANCE", "Service · Assurance icon row", "Service",
        ["First Purchase Assurance", "30-day Money-back", "Free Shipping", "Secure Payment"],
        ["Four assurance points in one row; stays four across on mobile, shrinking",
         "Round icon chips (storefront feather icons replaced by the neutral chip), titles in the v6 meta role"])
def service_assurance_row(th):
    def col(i):
        return _chip_c(th, 40) + gap(10) + meta(f"[Point {i}]", th, "center")
    return card(pair_row([col(1), col(2), col(3), col(4)], th, 12), th, pad="32px 24px", cls="pad-sm")


@module("SERVICE · CUSTOMER SATISFACTION", "Service · Big stat with copy", "Stats",
        ["98%", "Verified Customer Satisfaction", "Our clients report an immediate confidence uplift…"],
        ["One big numeral left, title and copy right; stacks on mobile",
         "Numeral: Inter Tight 800 at 64px, suffix in the serif italic (coral on Ink only); title in the v6 subtitle role"])
def service_big_stat(th):
    stat = (f'<p style="margin:0;font-family:{DISPLAY};font-size:64px;line-height:64px;font-weight:800;letter-spacing:-2.5px;'
            f'color:{th["text"]};">[00]{em("%", th)}</p>')
    text = subtitle("[Stat title]", th, mb=8) + body("[Body: three lines]", th, mb=0)
    return card(cols([stat, text], 28, valign="middle", weights=[34, 66]), th, pad="40px", cls="pad-sm")


@module("SERVICE · THREE-STEP JOURNEY", "Service · Three-step journey", "Service",
        ["01 · INTAKE Consultation", "02 · ARTISAN Creation", "03 · ATELIER Delivery"],
        ["Three steps with a mono step label, title and one line; stack on mobile",
         "The connector lines between steps are dropped (they have no place when columns stack)",
         "Step label in the v6 meta role, title in the v6 name role, description in the v6 small role"])
def service_three_step_journey(th):
    def col(i):
        return meta(f"[0{i} · Step]", th, mb=8) + name(f"[Step {i} title]", th, mb=4) + small("[One line]", th)
    return card(cols([col(1), col(2), col(3)], 20), th, pad="32px")


@module("SERVICE · HOW IT WORKS", "Service · How it works, four steps", "Service",
        ["How it works", "From first call to first look.", "01 · Consult … 04 · Care"],
        ["Eyebrow plus a four-step list of inset cards (step label, title, one line)",
         "Section title in the v6 title role; Figma's 673px-wide frame trimmed to the 600px shell",
         "Step cards are the v6 inset (8px)"])
def service_how_it_works(th):
    def step(i):
        inner = meta(f"[0{i} · Step]", th, mb=8) + subtitle(f"[Step {i} title]", th, mb=4) + small("[One line]", th)
        return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" '
                f'style="border-collapse:separate;background-color:{th["inset"]};border:1px solid {th["inset_edge"]};'
                f'border-radius:8px;"><tr><td style="padding:20px 24px;">{inner}</td></tr></table>')
    steps = step(1) + gap(10) + step(2) + gap(10) + step(3) + gap(10) + step(4)
    return card(eyebrow("[Eyebrow]", th, mb=14) + title("[Section title]", th, mb=22) + steps, th, pad="40px")


@module("SERVICE · STATS BAND LIGHT", "Service · Stats band without heading", "Stats",
        ["10K+ Customers", "97% Satisfaction", "15+ Years", "40+ Salons"],
        ["The same 2x2 stats grid as the heading version, with no eyebrow; two across on mobile",
         "Numerals: Inter Tight 800 with a serif-italic suffix (coral on Ink only); labels in the v6 meta role"])
def service_stats_plain(th):
    def stat(i):
        value = (f'<p style="margin:0 0 6px 0;font-family:{DISPLAY};font-size:56px;line-height:60px;font-weight:800;'
                 f'letter-spacing:-2px;text-align:center;color:{th["text"]};">[00]{em("+", th)}</p>')
        return value + meta(f"[Label {i}]", th, "center")
    grid = pair_row([stat(1), stat(2)], th, 24) + gap(28) + pair_row([stat(3), stat(4)], th, 24)
    return card(grid, th, pad="48px 40px")


@module("PERSONAL CONSULTATION LETTER", "Service · Personal letter", "Content",
        ["Hey Marcus,", "I noticed you started your consultation a few days ago…", "– David, Founder, Hair Solutions Co."],
        ["Plain personal letter: greeting, two paragraphs, signature; no logo, no hero image, no button",
         "Body in the v6 body role; signature in the serif-italic note role with the role line in the v6 meta role",
         "The Figma intent note ('no logo · no hero image · no button styling') is dropped: it is a design note, not email content"])
def service_personal_letter(th):
    sig = note("[Name]", th, mb=4) + meta("[Role]", th)
    return card(body("Hi [First name],", th, mb=16, color=th["text"]) + body("[Body: three lines]", th, mb=16) +
                body("[Body: two lines]", th, mb=22) + sig, th, pad="40px")
