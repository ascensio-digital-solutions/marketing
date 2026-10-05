#!/usr/bin/env python3
"""Theme-aware v6 email HTML kit for the module bank.

Every function returns an HTML fragment (a string). Nothing here invents a colour, a type role or a
radius: the numbers come from brand-design-system `tokens/tokens.css` and `email/src/styles/hx.css`
(type roles .hx-headline … .hx-meta, surfaces Bone / White / Ink, radii 12 / 8 / 999) and match the
existing sections in templates/email-blocks (for example w-1-hero).

The mobile behaviour only uses classes the shared email head (00-email-head-fonts-styles) defines:
.pad .pad-sm .pad-copy .stack .stack-gap .fluid .hero-h .btn

Usage:
    th = THEMES["ink"]
    html = section(card(eyebrow("[Eyebrow]", th) + headline("[Headline]", th), th))
"""

# ---------------------------------------------------------------- tokens
INK = "#15140f"
INK_SOFT = "#2a2620"
BONE = "#f7f1de"
WHITE = "#ffffff"
CORAL = "#ff5757"
MUTED = "#5a5448"
ON_INK_MUTED = "#b8b3a4"
LINE_STRONG = "#c9c1ae"

SANS = "'Inter',Arial,Helvetica,sans-serif"
DISPLAY = "'Inter Tight',Arial,Helvetica,sans-serif"
SERIF = "'Playfair Display',Georgia,'Times New Roman',serif"
MONO = "'JetBrains Mono','Courier New',monospace"

FILES = "https://cdn.shopify.com/s/files/1/0276/9115/5508/files/"
LOGO_INK = FILES + "hsc-email-logo-ink.png"     # v5 wordmark for light surfaces (128 x 38)
LOGO_BONE = FILES + "hsc-email-logo-bone.png"   # v5 wordmark for ink surfaces
SITE = "https://hairsolutions.co"
ADDRESS = "Hair Solutions Co. &middot; Ehitajate tee 110, Tallinn, Harjumaa 13517, Estonia"
ARROW = "&rarr;"

# The only hex values a bank section may contain (the build checks this).
PALETTE = {INK, INK_SOFT, BONE, WHITE, CORAL, MUTED, ON_INK_MUTED, LINE_STRONG,
           "#e5dfcd", "#ececec", "#35332c"}

# One row per surface: the role tokens of hx.css surface modes.
THEMES = {
    "bone": dict(name="bone", label="Bone", bg=BONE, edge="#e5dfcd", text=INK, muted=MUTED, inset=WHITE,
                 inset_edge="#e5dfcd", rule="#e5dfcd", strong=LINE_STRONG, label_color=INK, em=INK,
                 logo=LOGO_INK, btn_solid=INK, btn_solid_text=BONE, btn_outline=INK),
    "ink": dict(name="ink", label="Ink", bg=INK, edge="#35332c", text=BONE, muted=ON_INK_MUTED, inset=INK_SOFT,
                inset_edge="#35332c", rule="#35332c", strong="#35332c", label_color=CORAL, em=CORAL,
                logo=LOGO_BONE, btn_solid=BONE, btn_solid_text=INK, btn_outline=BONE),
    "white": dict(name="white", label="White", bg=WHITE, edge="#ececec", text=INK, muted=MUTED, inset=BONE,
                  inset_edge="#e5dfcd", rule="#ececec", strong=LINE_STRONG, label_color=INK, em=INK,
                  logo=LOGO_INK, btn_solid=INK, btn_solid_text=BONE, btn_outline=INK),
}


# ---------------------------------------------------------------- structure
def section(rows):
    """Wrap one or more card rows (each a `<tr><td style="padding:0;">…</td></tr>`) as a Messaging section."""
    return ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" '
            'style="background-color:transparent;"><tr><td align="center" style="padding:0;">\n'
            '<table role="presentation" class="shell" width="100%" cellpadding="0" cellspacing="0" border="0" '
            'style="width:100%;max-width:600px;">\n' + rows + '\n</table>\n</td></tr></table>\n')


def card(inner, th, pad="40px", cls="pad", clip=False):
    """One card row: 12px corners, 1px inside stroke, flush (row padding 0)."""
    over = "overflow:hidden;" if clip else ""
    return (f'<tr><td style="padding:0;">\n'
            f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" '
            f'style="border-collapse:separate;background-color:{th["bg"]};border:1px solid {th["edge"]};'
            f'border-radius:12px;{over}">\n'
            f'<tr><td class="{cls}" style="padding:{pad};">{inner}</td></tr>\n</table>\n</td></tr>')


def card_flush(inner, th):
    """A card whose first child bleeds to the edges (full-bleed image); the card clips it."""
    return (f'<tr><td style="padding:0;">\n'
            f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" '
            f'style="border-collapse:separate;background-color:{th["bg"]};border:1px solid {th["edge"]};'
            f'border-radius:12px;overflow:hidden;">\n{inner}\n</table>\n</td></tr>')


def gap(px):
    return f'<div style="height:{px}px;line-height:{px}px;font-size:0;">&nbsp;</div>'


def cols(cells, gap_px=24, valign="top", weights=None):
    """Columns that stack on mobile. `cells` are HTML strings; `weights` are percentages (default equal)."""
    n = len(cells)
    weights = weights or [round(100 / n, 2)] * n
    tds = []
    for i, c in enumerate(cells):
        cls = "stack" if i == 0 else "stack stack-gap"
        pl = 0 if i == 0 else gap_px
        tds.append(f'<td class="{cls}" width="{weights[i]}%" valign="{valign}" '
                   f'style="width:{weights[i]}%;padding:0 0 0 {pl}px;vertical-align:{valign};">{c}</td>')
    return ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">'
            f'<tr>{"".join(tds)}</tr></table>')


# ---------------------------------------------------------------- type roles (hx.css)
def _p(text, th, family, size, lh, weight=400, color=None, align="left", mb=0, ls=None, extra="", tag="p", cls=""):
    c = f' class="{cls}"' if cls else ""
    l = f"letter-spacing:{ls}px;" if ls is not None else ""
    return (f'<{tag}{c} style="margin:0 0 {mb}px 0;font-family:{family};font-size:{size}px;line-height:{lh}px;'
            f'font-weight:{weight};{l}color:{color or th["text"]};text-align:{align};{extra}">{text}</{tag}>')


def em(text, th):
    """The serif emphasis phrase. Coral only on Ink; ink on light surfaces (coral text fails contrast there)."""
    return (f'<span style="font-family:{SERIF};font-style:italic;font-weight:400;color:{th["em"]};'
            f'letter-spacing:-0.5px;">{text}</span>')


def headline(text, th, align="left", mb=18, size=48, lh=50, ls=-1.8):
    return _p(text, th, DISPLAY, size, lh, 800, align=align, mb=mb, ls=ls, tag="h1", cls="hero-h")


def title(text, th, align="left", mb=14):
    return _p(text, th, DISPLAY, 28, 31, 700, align=align, mb=mb, ls=-0.6, tag="h2")


def subtitle(text, th, align="left", mb=8):
    return _p(text, th, DISPLAY, 19, 24, 700, align=align, mb=mb, tag="h3")


def name(text, th, align="left", mb=4, color=None):
    return _p(text, th, DISPLAY, 15, 20, 700, align=align, mb=mb, color=color)


def lead(text, th, align="left", mb=22):
    return _p(text, th, SANS, 19, 30, 400, color=th["muted"], align=align, mb=mb)


def body(text, th, align="left", mb=16, color=None):
    return _p(text, th, SANS, 16, 26, 400, color=color or th["muted"], align=align, mb=mb)


def small(text, th, align="left", mb=0):
    return _p(text, th, SANS, 13, 21, 400, color=th["muted"], align=align, mb=mb)


def meta(text, th, align="left", mb=0, color=None):
    return _p(text, th, MONO, 11, 17, 500, color=color or th["muted"], align=align, mb=mb, ls=0.9,
              extra="text-transform:uppercase;")


def note(text, th, align="left", mb=16):
    return _p(text, th, SERIF, 22, 33, 500, align=align, mb=mb, extra="font-style:italic;")


def price(text, th, align="left", mb=0, small_=False):
    size, lh = (16, 20) if small_ else (26, 26)
    return _p(text, th, SERIF, size, lh, 500, align=align, mb=mb, extra="font-style:italic;white-space:nowrap;")


def eyebrow(text, th, center=False, mb=16):
    """Coral dash + label. The label is coral on Ink and ink on light surfaces."""
    al = 'align="center" ' if center else ""
    side = "auto" if center else "0"
    return (f'<table role="presentation" {al}cellpadding="0" cellspacing="0" border="0" '
            f'style="margin:0 {side} {mb}px {side};">\n'
            f'<tr><td width="20" style="width:20px;vertical-align:middle;"><div style="height:2px;line-height:2px;'
            f'font-size:0;background-color:{CORAL};">&nbsp;</div></td>\n'
            f'<td style="padding-left:12px;font-family:{DISPLAY};font-size:12px;line-height:16px;font-weight:600;'
            f'letter-spacing:2px;text-transform:uppercase;color:{th["label_color"]};white-space:nowrap;">{text}</td></tr>\n'
            '</table>')


def textlink(text, th, href=SITE):
    return (f'<a href="{href}" target="_blank" style="font-family:{DISPLAY};font-size:15px;font-weight:600;'
            f'color:{th["text"]};text-decoration:underline;">{text} {ARROW}</a>')


def button(label, th, kind="primary", href=SITE, center=False, size=15, height=58, padx=34):
    """kind: primary (coral, ink label), solid (contrast fill) or outline. Pill (999px); the outline is on the <a>."""
    if kind == "primary":
        fill, txt, border = CORAL, INK, None
    elif kind == "solid":
        fill, txt, border = th["btn_solid"], th["btn_solid_text"], None
    else:
        fill, txt, border = th["bg"], th["btn_outline"], th["btn_outline"]
    b = f"border:1px solid {border};" if border else ""
    al = 'align="center" ' if center else ""
    return (f'<table role="presentation" {al}class="btn" cellpadding="0" cellspacing="0" border="0" '
            f'style="border-collapse:separate;margin:{"0 auto" if center else "0"};">\n'
            f'<tr><td style="border-radius:999px;background-color:{fill};">\n'
            f'<a href="{href}" target="_blank" style="display:inline-block;{b}padding:0 {padx}px;'
            f'line-height:{height - (2 if border else 0)}px;font-family:{DISPLAY};font-size:{size}px;font-weight:600;'
            f'letter-spacing:0.3px;color:{txt};text-decoration:none;border-radius:999px;white-space:nowrap;">{label}'
            f'<span style="padding-left:12px;font-family:{SANS};font-size:16px;">{ARROW}</span></a>\n'
            f'</td></tr></table>')


def hairline(th, mb=0, mt=0):
    return (f'<div style="margin:{mt}px 0 {mb}px 0;height:1px;line-height:1px;font-size:0;'
            f'background-color:{th["rule"]};">&nbsp;</div>')


def badge(text, th):
    return (f'<span style="display:inline-block;font-family:{MONO};font-size:11px;line-height:16px;font-weight:500;'
            f'letter-spacing:0.9px;text-transform:uppercase;padding:5px 12px;border-radius:999px;'
            f'border:1px solid {th["strong"] if th["name"] != "ink" else "#35332c"};background-color:{th["inset"]};'
            f'color:{th["muted"]};">{text}</span>')


def code_chip(text, th):
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:separate;">'
            f'<tr><td style="border:1px dashed {th["text"]};border-radius:8px;padding:9px 16px;font-family:{MONO};'
            f'font-size:15px;line-height:20px;font-weight:500;letter-spacing:1.8px;color:{th["text"]};'
            f'white-space:nowrap;">{text}</td></tr></table>')


# ---------------------------------------------------------------- images
def logo(th, w=128, center=True):
    h = round(w * 38 / 128)
    m = "0 auto" if center else "0"
    return (f'<img src="{th["logo"]}" width="{w}" height="{h}" alt="Hair Solutions Co." '
            f'style="display:block;margin:{m};border:0;width:{w}px;height:{h}px;">')


def image(src, w, h, alt, th=None, radius=8, fluid=True):
    """A hosted image with explicit size. `radius` 8 for insets, 0 when the card clips it."""
    cls = ' class="fluid"' if fluid else ""
    return (f'<img src="{src}" width="{w}" height="{h}" alt="{alt}"{cls} style="display:block;width:100%;'
            f'max-width:{w}px;height:auto;border:0;border-radius:{radius}px;">')


def photo_slot(label, th, h=240, radius=8):
    """A labelled image slot (no stock imagery): inset fill, mono label, explicit height."""
    return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" '
            f'style="border-collapse:separate;background-color:{th["inset"]};border:1px solid {th["inset_edge"]};'
            f'border-radius:{radius}px;"><tr><td align="center" valign="middle" height="{h}" '
            f'style="height:{h}px;padding:0 16px;">{meta(label, th, "center")}</td></tr></table>')


def square_slot(label, th, radius=8):
    """A labelled 1:1 image slot: the shape of a square product render at any column width (desktop and mobile).
    The slot is a placeholder that is replaced by a square <img class="fluid"> (width:100%, height:auto); the
    aspect-ratio keeps the preview square where the slot is still in place."""
    return (f'<div style="width:100%;box-sizing:border-box;aspect-ratio:1/1;display:flex;align-items:center;'
            f'justify-content:center;background-color:{th["inset"]};border:1px solid {th["inset_edge"]};'
            f'border-radius:{radius}px;padding:0 8px;">{meta(label, th, "center")}</div>')


def kv_rows(rows, th):
    """Label / value pairs separated by hairlines. rows: [(label, value_html)]."""
    out = []
    for lab, val in rows:
        out.append(f'<tr><td style="border-top:1px solid {th["rule"]};padding:12px 0;font-family:{MONO};font-size:11px;'
                   f'line-height:16px;letter-spacing:0.9px;text-transform:uppercase;color:{th["muted"]};'
                   f'vertical-align:middle;">{lab}</td>'
                   f'<td align="right" style="border-top:1px solid {th["rule"]};padding:12px 0 12px 16px;'
                   f'font-family:{DISPLAY};font-size:15px;line-height:20px;font-weight:700;color:{th["text"]};'
                   f'text-align:right;vertical-align:middle;">{val}</td></tr>')
    return ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" '
            f'style="border-collapse:collapse;">{"".join(out)}</table>')


def photo_bleed(label, th, h=260):
    """Full-bleed image slot for the top of a clipped card (see card_flush): a single cell, so the card's
    12px clip supplies the top corners."""
    return (f'<tr><td align="center" valign="middle" height="{h}" style="height:{h}px;padding:0 16px;'
            f'background-color:{th["inset"]};font-size:11px;line-height:17px;">{meta(label, th, "center")}</td></tr>')


def pair_row(cells, th=None, gap_px=24, valign="top"):
    """Equal columns that stay side by side on mobile (a 2-up grid reflows by shrinking, never stacks).
    Use for product tiles and stats; use cols() for text columns that should stack."""
    n = len(cells)
    w = round(100 / n, 2)
    tds = []
    for i, c in enumerate(cells):
        pl = 0 if i == 0 else gap_px // 2
        pr = 0 if i == n - 1 else gap_px // 2
        tds.append(f'<td width="{w}%" valign="{valign}" style="width:{w}%;padding:0 {pr}px 0 {pl}px;vertical-align:{valign};">{c}</td>')
    return ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">'
            f'<tr>{"".join(tds)}</tr></table>')


def short_rule(mb=24):
    """The v6 edge rule for centred blocks: 32px wide, 2px, coral, centred."""
    return ('<table role="presentation" align="center" cellpadding="0" cellspacing="0" border="0" '
            f'style="margin:0 auto {mb}px auto;"><tr><td width="32" style="width:32px;">'
            f'<div style="height:2px;line-height:2px;font-size:0;background-color:{CORAL};">&nbsp;</div></td></tr></table>')


def nav_links(th, n=4, align="center", gap_px=24, size=12):
    """A row of nav link slots in the v6 eyebrow face. Links wrap on narrow screens."""
    pad = f"padding:0 {gap_px // 2}px;" if align == "center" else (f"padding-left:{gap_px}px;" if align == "right" else f"padding-right:{gap_px}px;")
    links = "".join(f'<a href="{SITE}" target="_blank" style="font-family:{DISPLAY};font-size:{size}px;line-height:24px;'
                    f'font-weight:600;letter-spacing:1.5px;text-transform:uppercase;color:{th["text"]};'
                    f'text-decoration:none;{pad}white-space:nowrap;display:inline-block;">[Link {i}]</a>' for i in range(1, n + 1))
    return f'<p style="margin:0;text-align:{align};font-size:0;line-height:0;">{links}</p>'
