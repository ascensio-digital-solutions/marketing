"""Category 03 · Titles & editorial: one function per module, `fn(theme) -> card rows`. See build_bank.py."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".claude/skills/shopify-email-html/scripts"))
from v6_html import *  # noqa: F401,F403
from bank_registry import module


@module("Title · Coral accent line", "Title · Centred with short rule", "Title",
        ["pH-Balanced Botanic Formulas", "Sulfate-free citrus extracts engineered to cleanse custom Swiss lace bases safely."],
        ["The 60x3 coral bar becomes the v6 edge rule (short, centred, 32px, 24px to the heading)",
         "Title in the v6 title role (Inter Tight 700, 28/31), body in the v6 body role"])
def title_short_rule(th):
    rule = ('<table role="presentation" align="center" cellpadding="0" cellspacing="0" border="0" style="margin:0 auto 24px auto;">'
            f'<tr><td width="32" style="width:32px;"><div style="height:2px;line-height:2px;font-size:0;background-color:{CORAL};">&nbsp;</div></td></tr></table>')
    return card(rule + title("[Title]", th, "center", mb=14) + body("[Body: one or two lines]", th, "center", mb=0),
                th, pad="48px 40px")


def _inset_card(inner, th, pad="16px"):
    return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" '
            f'style="border-collapse:separate;background-color:{th["inset"]};border:1px solid {th["inset_edge"]};'
            f'border-radius:8px;"><tr><td style="padding:{pad};">{inner}</td></tr></table>')


@module("Title", "Title · Eyebrow, headline and lead, centred", "Title",
        ["Change with intention", "Small adjustments can create a completely different result", "A subtle shift in density, wave pattern, hair length, or colour."],
        ["Headline in the v6 headline role (48/50, sentence case) with the lead role below; the eyebrow is centred over the centred headline (Figma left-aligned it)"])
def title_headline_lead(th):
    return card(eyebrow("[Eyebrow]", th, center=True, mb=18) + headline("[Headline]", th, "center", mb=18) +
                lead("[Lead: two lines]", th, "center", mb=0), th, pad="48px 40px")


@module("Content", "Content · Title and body", "Content",
        ["Lace: lightweight and breathable", "Lace systems are selected for their light feel, airflow, and a barely-there hairline."],
        ["Title in the v6 title role (28/31), body in the v6 body role, left-aligned"])
def content_title_body(th):
    return card(title("[Title]", th, mb=14) + body("[Body: three or four lines]", th, mb=0), th, pad="40px")


@module("Blog", "Content · Article feature, image left", "Content",
        ["Care library · 5 min read", "Five questions to ask before choosing a base", "Climate, activity, maintenance, and attachment all shape the right choice.", "Read the full guide →"],
        ["Image left, copy right; stacks on mobile. Meta line in the v6 meta role; the read link is a v6 text link (ink, underlined)"])
def content_article_feature(th):
    copy = meta("[Category · read time]", th, mb=10) + title("[Title]", th, mb=10) + body("[Body: two lines]", th, mb=16) + textlink("[Link label]", th)
    return card(cols([photo_slot("[Photo · article]", th, 150), copy], 24, "top", [38, 62]), th, pad="32px 40px")


@module("Title · Simple centered heading", "Title · Simple centred heading", "Title",
        ["Artisan ventilation technique", "Every single strand of our virgin human hair is hand-tied."],
        ["Title in the v6 title role, body role below, centred; no eyebrow and no rule"])
def title_simple(th):
    return card(title("[Title]", th, "center", mb=14) + body("[Body: two lines]", th, "center", mb=0), th, pad="48px 40px")


@module("Title · Dark ink background theme", "Title · Eyebrow, title and body, centred", "Title",
        ["Exclusive access", "The absolute standard", "Your custom blueprint remains completely private on our servers."],
        ["Figma named it 'dark ink background' (only the Ink cell was dark): now a real Bone / Ink / White module",
         "Eyebrow with the coral dash (label ink on light, coral on Ink), title in the v6 title role"])
def title_eyebrow_title(th):
    return card(eyebrow("[Eyebrow]", th, center=True, mb=16) + title("[Title]", th, "center", mb=14) +
                body("[Body: two lines]", th, "center", mb=0), th, pad="56px 40px")


@module("Title · Overline label + large centered", "Title · Overline label and large title", "Title",
        ["The Atelier collection", "Bespoke hair systems", "Custom-matched to your exact scalp contour, density needs, and colour."],
        ["The overline is a plain mono label (v6 meta role) rather than the dash eyebrow, so this differs from the other centred titles",
         "Title at the large headline size on mobile (36/38)"])
def title_overline_large(th):
    h = headline("[Large title]", th, "center", size=36, lh=38, ls=-1.2, mb=14)
    return card(meta("[Overline label]", th, "center", mb=14, color=th["text"]) + h + body("[Body: two lines]", th, "center", mb=0),
                th, pad="48px 40px")


@module("Title · Left-aligned heading with rule", "Title · Left-aligned with top rule", "Title",
        ["The Swiss lace difference", "Experience unparalleled breathability and an invisible hairline."],
        ["The rule is a v6 hairline (the surface's rule colour), full content width, above a left-aligned title"])
def title_left_rule(th):
    return card(hairline(th, mb=22) + title("[Title]", th, mb=12) + body("[Body: two lines]", th, mb=0), th, pad="40px")


@module("Content · Full-width body paragraph", "Content · Full-width body", "Content",
        ["Uncompromising quality standards", "Each strand of virgin remy human hair undergoes rigorous inspection."],
        ["Subtitle role (19/24) heading over a long body paragraph at full content width"])
def content_full_body(th):
    return card(subtitle("[Heading]", th, mb=14) + body("[Body: a full paragraph, five or six lines]", th, mb=0), th, pad="48px 40px")


@module("Content · Two-column image + text", "Content · Two-column image and text", "Content",
        ["Bespoke fitting", "We design your template based on your head shape."],
        ["Square image left, heading and small body right; stacks on mobile; body in the v6 small role"])
def content_two_col(th):
    copy = subtitle("[Heading]", th, mb=10) + small("[Body: three lines]", th)
    return card(cols([photo_slot("[Photo]", th, 200), copy], 24, "middle", [40, 60]), th, pad="24px", cls="pad-sm")


@module("Content · Three-column feature grid", "Content · Three-column feature grid", "Content",
        ["Breathable: Allows full heat dissipation.", "Hand-knotted: Artisan single ventilation.", "Seamless: Disappears against the scalp."],
        ["Three inset cards (8px corners) with a glyph, a name-role heading and small body; they stack on mobile (three narrow columns do not fit a phone)",
         "Glyphs are plain characters (no icon images)"])
def content_three_col(th):
    def feat(glyph, i):
        g = f'<p style="margin:0 0 12px 0;font-family:{DISPLAY};font-size:20px;line-height:24px;color:{th["text"]};">{glyph}</p>'
        return _inset_card(g + name(f"[Feature {i}]", th, mb=4) + small("[One short line]", th), th)
    return card(cols([feat("&#9776;", 1), feat("+", 2), feat("&#9733;", 3)], 14, "top"), th, pad="32px")


@module("Content · Founder quote block", "Content · Founder quote", "Content",
        ["From the founder", "The best compliment we get is silence.", "Vincent · Founder"],
        ["Quote in the v6 note role (serif italic 22/33), centred, with an eyebrow and a meta attribution line"])
def content_founder_quote(th):
    return card(eyebrow("[Eyebrow]", th, center=True, mb=22) + note("&ldquo;[Quote: two or three lines]&rdquo;", th, "center", mb=20) +
                meta("[Name] &middot; [Role]", th, "center"), th, pad="64px 40px")


@module("WORKSHOP FOUNDER NOTE", "Content · Founder note with portrait", "Content",
        ["A note from the workshop", "We build every system the same way, whether it's your first or your fifth.", "Vincent, Founder"],
        ["Portrait is a labelled 96px slot (consented portrait only; never a stock avatar); quote in the v6 note role",
         "Portrait and note stay side by side on mobile"])
def content_founder_portrait(th):
    por = ('<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:separate;'
           f'background-color:{th["inset"]};border:1px solid {th["inset_edge"]};border-radius:8px;"><tr>'
           f'<td align="center" valign="middle" width="96" height="96" style="width:96px;height:96px;">{meta("[Portrait]", th, "center")}</td></tr></table>')
    copy = (meta("[Eyebrow]", th, mb=8) + _p_note(th) + meta("&ndash; [Name], [Role]", th))
    row = ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>'
           f'<td valign="top" width="96" style="width:96px;padding-right:20px;">{por}</td><td valign="top">{copy}</td></tr></table>')
    return card(row, th, pad="32px 40px")


def _p_note(th):
    return note("&ldquo;[Note: two or three lines]&rdquo;", th, mb=10).replace("font-size:22px;line-height:33px", "font-size:20px;line-height:30px")


@module("FEATURE STORY CARD", "Content · Feature story card", "Content",
        ["How it's made", "Every system starts as a hand-drawn base pattern before ventilation begins."],
        ["Full-bleed photo on top, caption block below (subtitle role and small body)"])
def content_feature_story(th):
    cap = subtitle("[Heading]", th, mb=8) + small("[Body: two or three lines]", th)
    return card_flush(photo_bleed("[Photo · feature story]", th, 280) + f'<tr><td class="pad" style="padding:28px 40px 32px 40px;">{cap}</td></tr>', th)


@module("Founder note", "Content · Greeting line", "Content",
        ["Hi {{ firstname }},"],
        ["A single greeting line in the v6 title role; the first name is a slot (wire it to the customer first-name variable in the template)"])
def content_greeting(th):
    return card(title("Hi [First name],", th, mb=0), th, pad="32px 40px")


@module("Image and copy", "Content · Image strip", "Content",
        [],
        ["The Figma frame held only an image area: kept as a full-width image strip (8px inset corners) inside the card"])
def content_image_strip(th):
    return card(photo_slot("[Photo · wide strip]", th, 150), th, pad="24px 40px")
