"""Category 02 · Heroes: one function per module, `fn(theme) -> card rows`. See build_bank.py."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".claude/skills/shopify-email-html/scripts"))
from v6_html import *  # noqa: F401,F403
from bank_registry import module


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


# Several Figma heroes differ only in their sample copy (Solid dark ink vs Minimal essay; Text only contact vs
# category landing). The bank keeps every id and differentiates by alignment and type role, which the composition
# guide treats as free variables; each adaptations list says so.

def _hl(th, size=48):
    """Headline slot with the serif emphasis phrase on the second half."""
    lh, ls = {48: (50, -1.8), 38: (40, -1.4), 36: (38, -1.2)}[size]
    return headline(f'[Headline] {em("[emphasis]", th)}', th, size=size, lh=lh, ls=ls)


def _btn_small(label, th, kind="primary"):
    return button(label, th, kind, size=13, height=46, padx=24)


@module("Hero", "Hero · Image beside copy", "Hero",
        ["A considered change", "Your next look does not have to be more of the same",
         "Explore options that adjust texture, density, or length without losing the confidence of a well-chosen system.", "Explore new looks"],
        ["Image left, copy right; on mobile the columns stack (image first)",
         "Headline sentence case at the v6 mobile size (36/38) because it sits in a narrow column",
         "Button is the v6 primary pill; the Figma button was a square-ish storefront style"])
def hero_beside(th):
    copy = (eyebrow("[Eyebrow]", th) + headline("[Headline]", th, size=36, lh=38, ls=-1.2, mb=14) +
            body("[Body: two or three lines]", th, mb=22) + button("[Button label]", th))
    return card(cols([photo_slot("[Photo · product]", th, 220), copy], 28, "middle", [38, 62]), th, pad="40px")


@module("Hero · Asymmetric image-text split", "Hero · Asymmetric image and text split", "Hero",
        ["The Atelier metric", "Uncompromising Hair Restoration", "Experience the security of custom-tailored medical-grade bases.", "Discover Atelier"],
        ["Tall image left (about 40%), copy right; stacks on mobile",
         "Eyebrow in the v6 eyebrow role (label ink on light, coral on Ink); title in the v6 title role; small v6 pill button"])
def hero_asym_split(th):
    copy = (eyebrow("[Eyebrow]", th) + title("[Title]", th, mb=14) + body("[Body: two or three lines]", th, mb=22) +
            _btn_small("[Button label]", th))
    return card(cols([photo_slot("[Photo · portrait]", th, 320), copy], 24, "middle", [42, 58]), th, pad="24px", cls="pad-sm")


@module("Hero · Minimal text essay layout", "Hero · Text essay, centred", "Hero",
        ["Our design philosophy", "Designed around real life", "We believe hair restoration shouldn't feel like a compromise.", "Book consultation"],
        ["Lead paragraph in the v6 lead role (19/30), headline 48/50 sentence case, centred, generous 64px padding"])
def hero_essay(th):
    return card(eyebrow("[Eyebrow]", th, center=True, mb=24) + headline("[Headline]", th, "center", mb=22) +
                lead("[Lead: two lines]", th, "center", mb=28) + button("[Button label]", th, center=True), th, pad="64px 48px")


@module("Hero · Stacked asymmetric image", "Hero · Inset image with two buttons", "Hero",
        ["The botanical maintenance routine", "Protect and prolong the vitality of your base and natural hair.", "Shop elixirs", "Read care guides"],
        ["Image is an inset inside the card (8px corners), copy and buttons below it",
         "Two buttons: the v6 primary pill and an outline pill (never two coral buttons)"])
def hero_inset_two_buttons(th):
    inner = (photo_slot("[Photo · hero image]", th, 300) + gap(28) + headline("[Headline]", th, mb=14) +
             body("[Body: one or two lines]", th, mb=24) +
             cols([button("[Button label]", th), button("[Second button]", th, "outline")], 12, "middle", [40, 60]))
    return card(inner, th, pad="24px 24px 40px 24px", cls="pad-sm")


@module("Hero · Solid dark ink theme", "Hero · Centred statement", "Hero",
        ["Strictly confidential", "The absolute standard in premium care", "Every system is customized entirely to your hair colour, density requirements, and scalp contour.", "Request private booking"],
        ["Figma named it 'solid dark ink' and drew all three cells dark (the Ink cell's headline was invisible): rebuilt as a real Bone / Ink / White module",
         "Differs from the text-essay hero by body role (16/26, not lead) and 72px padding"])
def hero_statement(th):
    return card(eyebrow("[Eyebrow]", th, center=True, mb=22) + headline("[Headline]", th, "center", mb=18) +
                body("[Body: two lines]", th, "center", mb=28) + button("[Button label]", th, center=True), th, pad="72px 40px")


@module("Hero · New product reveal block", "Hero · Product reveal with price", "Hero",
        ["New arrival", "The Swiss Lace Atelier System", "Introductory rate $580", "Configure your system"],
        ["Badge in the v6 badge role; image is a labelled slot; price in the v6 price role (serif italic)",
         "Price and its label are slots: no price is stated until confirmed"])
def hero_product_reveal(th):
    price_row = (f'<table role="presentation" align="center" cellpadding="0" cellspacing="0" border="0" style="margin:0 auto 26px auto;">'
                 f'<tr><td valign="bottom" style="padding-right:10px;">{meta("[Price label]", th)}</td>'
                 f'<td valign="bottom">{price("[Price]", th)}</td></tr></table>')
    inner = (f'<p style="margin:0 0 18px 0;text-align:center;">{badge("[Badge]", th)}</p>' + headline("[Headline]", th, "center", mb=22) +
             photo_slot("[Photo · product reveal]", th, 300) + gap(22) + price_row + button("[Button label]", th, center=True))
    return card(inner, th, pad="40px 24px", cls="pad-sm")


@module("Hero · Seasonal campaign card", "Hero · Campaign card", "Hero",
        ["The suite review", "Spring restoration: seamless density refresh", "Is your system due for seasonal servicing?", "Claim refresh booking"],
        ["Inset image on top, left-aligned copy below; title in the v6 title role"])
def hero_campaign_card(th):
    inner = (photo_slot("[Photo · campaign]", th, 260) + gap(24) + eyebrow("[Eyebrow]", th) + title("[Title]", th, mb=12) +
             body("[Body: two or three lines]", th, mb=24) + button("[Button label]", th))
    return card(inner, th, pad="40px")


@module("Hero · Editorial minimal caption", "Hero · Editorial caption with rule", "Hero",
        ["The precision method", "Crafted in small batches by master hair ventilating artisans"],
        ["Centred eyebrow, title and a hairline; no button (an editorial opener)"])
def hero_editorial_caption(th):
    return card(eyebrow("[Eyebrow]", th, center=True, mb=16) + title("[Title]", th, "center", mb=24) + hairline(th),
                th, pad="56px 40px 40px 40px")


@module("Hero · Full image dark background", "Hero · Full-bleed image, headline and two buttons", "Hero",
        ["Non-surgical hair replacement", "Confidence starts at the top.", "Premium men's hair systems, handmade from 100% human hair.", "Shop hair systems", "Book a free consultation"],
        ["Text no longer sits on the image: full-bleed image on top, copy below, left-aligned (unlike 'Image with text below', which is centred)",
         "Serif emphasis phrase in the headline (coral on Ink, ink on light); two stacked buttons: primary and outline"])
def hero_full_image_two(th):
    text = (eyebrow("[Eyebrow]", th) + _hl(th, 36).replace("margin:0 0 18px 0", "margin:0 0 14px 0") +
            body("[Body: one or two lines]", th, mb=26) + button("[Button label]", th) + gap(12) + button("[Second button]", th, "outline"))
    return card_flush(photo_bleed("[Photo · full-bleed hero]", th, 300) + f'<tr><td class="pad" style="padding:36px 40px 40px 40px;">{text}</td></tr>', th)


@module("Hero · Collection banner dark", "Hero · Collection banner", "Hero",
        ["The collection", "Men's hair systems.", "Design your system"],
        ["Full-bleed image top, left-aligned eyebrow, short headline with serif emphasis and one button below",
         "Named for the layout, not the colour: Bone, Ink and White all exist"])
def hero_collection(th):
    text = eyebrow("[Eyebrow]", th) + _hl(th, 38) + button("[Button label]", th)
    return card_flush(photo_bleed("[Photo · collection]", th, 260) + f'<tr><td class="pad" style="padding:32px 40px 40px 40px;">{text}</td></tr>', th)


@module("Hero · Text only contact", "Hero · Text only, left-aligned", "Hero",
        ["Contact", "Talk to someone who builds these.", "Tell us what you are working with and what you want it to do."],
        ["Left-aligned eyebrow, headline with serif emphasis and body; no button or image"])
def hero_text_left(th):
    return card(eyebrow("[Eyebrow]", th) + _hl(th, 38) + body("[Body: one or two lines]", th, mb=0), th, pad="56px 40px")


@module("Hero · Text only category landing", "Hero · Text only, centred", "Hero",
        ["All hair systems", "Start with the base. Choose for your routine.", "Browse every system by construction, wear pattern, and maintenance."],
        ["Figma drew this like the contact hero; here it is centred (alignment is a free variable) so the two ids are distinct"])
def hero_text_centred(th):
    lh, ls = 40, -1.4
    h = headline(f'[Headline] {em("[emphasis]", th)}', th, "center", size=38, lh=lh, ls=ls)
    return card(eyebrow("[Eyebrow]", th, center=True) + h + body("[Body: one or two lines]", th, "center", mb=0), th, pad="64px 40px")
