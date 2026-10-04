#!/usr/bin/env python3
"""Build the Hair Solutions Co. v6 emails (Figma "v6 · Reference") as Shopify-ready Liquid HTML.

Outputs (out/):
  pp-1_order-confirmation.shopify-notification.liquid.html  -> Settings > Notifications > Order confirmation
  cr-1 .. cr-4 *.shopify-messaging.liquid.html               -> Messaging > Automations > Recover abandoned checkout

Stdlib only. Re-run after editing; every file is regenerated from the blocks below.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent

# ---------------------------------------------------------------- tokens: brand-design-system tokens/tokens.css + email/src/styles/hx.css
INK = "#15140f"          # ink surface + primary text
INK_SOFT = "#2a2620"     # raised card on ink
BONE = "#f7f1de"         # bone card surface / text on ink
WHITE = "#ffffff"
CORAL = "#ff5757"        # action + section signal
MUTED = "#5a5448"        # secondary text on light
ON_INK_MUTED = "#b8b3a4" # secondary text on ink
RULE_BONE = "#e5dfcd"    # --az-bone-line
RULE_WHITE = "#ececec"   # --az-email-white-line
EDGE_WHITE = "#ececec"   # --az-email-white-line
EDGE_BONE = "#e5dfcd"    # --az-bone-line
EDGE_INK = "#35332c"     # --az-ink-line
PORTRAIT = "#e5dfcd"     # --az-email-portrait-fill on bone
LINE_STRONG = "#c9c1ae"  # --az-line-strong

SANS = "'Inter',Arial,Helvetica,sans-serif"
DISPLAY = "'Inter Tight',Arial,Helvetica,sans-serif"
SERIF = "'Playfair Display',Georgia,'Times New Roman',serif"
MONO = "'JetBrains Mono','Courier New',monospace"

# ---------------------------------------------------------------- hosted assets
# Upload the four files in out/images/ to Shopify > Content > Files with EXACTLY these names.
# Shopify serves Files at a stable URL built from the file name, so no edit is needed afterwards.
FILES = "https://cdn.shopify.com/s/files/1/0276/9115/5508/files/"
IMG_LOGO_INK_MARK = FILES + "hsc-email-logo-ink.png"    # v5 wordmark, ink (for light surfaces)
IMG_LOGO_BONE_MARK = FILES + "hsc-email-logo-bone.png"  # v5 wordmark, bone (for ink surfaces)
IMG_HAIRLINE = FILES + "hsc-email-hairline-profile.jpg"
IMG_WORKSHOP = FILES + "hsc-email-workshop-hands.jpg"

SITE = "https://hairsolutions.co"
PREFS = SITE + "/pages/edit-notifications"
PRIVACY = SITE + "/policies/privacy-policy"
CONTACT = SITE + "/pages/contact-us?utm_source=shopify_email&amp;utm_medium=email&amp;utm_campaign=cr-3"
ADDRESS = "Hair Solutions Co. &middot; Ehitajate tee 110, Tallinn, Harjumaa 13517, Estonia"
ARROW = "&rarr;"


# ---------------------------------------------------------------- primitives
def card(inner, bg, edge, pad="40px", cls="pad", extra=""):
    return f"""
<tr><td style="padding:0;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:separate;background-color:{bg};border:1px solid {edge};border-radius:12px;{extra}">
<tr><td class="{cls}" style="padding:{pad};">{inner}</td></tr>
</table>
</td></tr>"""


def p(text, color=INK, size=16, lh=26, mb=16, weight=400, family=SANS, align="left", extra="", cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<p{c} style="margin:0 0 {mb}px 0;font-family:{family};font-size:{size}px;line-height:{lh}px;'
            f'font-weight:{weight};color:{color};text-align:{align};{extra}">{text}</p>')


def mono(text, color=MUTED, size=11, lh=16, ls=0.8, align="left", mb=0, extra=""):
    return (f'<p style="margin:0 0 {mb}px 0;font-family:{MONO};font-size:{size}px;line-height:{lh}px;'
            f'font-weight:500;letter-spacing:{ls}px;text-transform:uppercase;color:{color};text-align:{align};{extra}">{text}</p>')


def eyebrow(text, color=INK, center=False, mb=16):
    align = 'align="center" ' if center else ""
    return f"""<table role="presentation" {align}cellpadding="0" cellspacing="0" border="0" style="margin:0 {'auto' if center else '0'} {mb}px {'auto' if center else '0'};">
<tr><td width="20" style="width:20px;vertical-align:middle;"><div style="height:2px;line-height:2px;font-size:0;background-color:{CORAL};">&nbsp;</div></td>
<td style="padding-left:12px;font-family:{DISPLAY};font-size:12px;line-height:16px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:{color};white-space:nowrap;">{text}</td></tr>
</table>"""


def button(label, href, fill=CORAL, text=INK, border=None, size=15, height=58, padx=34, center=False):
    b = f"border:1px solid {border};" if border else ""
    align = 'align="center" ' if center else ""
    # The outline sits on the <a> (which carries the pill radius) and the table is border-collapse:separate:
    # Shopify Messaging collapses table borders, which squares off a bordered <td>.
    return f"""<table role="presentation" {align}class="btn" cellpadding="0" cellspacing="0" border="0" style="border-collapse:separate;margin:{'0 auto' if center else '0'};">
<tr><td style="border-radius:999px;background-color:{fill};">
<a href="{href}" target="_blank" style="display:inline-block;{b}padding:0 {padx}px;line-height:{height - (2 if border else 0)}px;font-family:{DISPLAY};font-size:{size}px;font-weight:600;letter-spacing:0.3px;color:{text};text-decoration:none;border-radius:999px;white-space:nowrap;">{label}<span style="padding-left:12px;font-family:{SANS};font-size:16px;">{ARROW}</span></a>
</td></tr></table>"""


def kv_rows(rows, rule=RULE_BONE):
    """rows: list of (label, value_html, optional liquid wrapper open, close)."""
    out = []
    for r in rows:
        label, value = r[0], r[1]
        pre, post = (r[2], r[3]) if len(r) > 2 else ("", "")
        out.append(f"""{pre}<tr>
<td style="border-top:1px solid {rule};padding:12px 0;font-family:{MONO};font-size:11px;line-height:16px;letter-spacing:0.8px;text-transform:uppercase;color:{MUTED};vertical-align:middle;">{label}</td>
<td align="right" style="border-top:1px solid {rule};padding:12px 0 12px 16px;font-family:{DISPLAY};font-size:15px;line-height:20px;font-weight:700;color:{INK};text-align:right;vertical-align:middle;">{value}</td>
</tr>{post}""")
    return out


def table(rows_html, extra=""):
    return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;{extra}">{"".join(rows_html)}</table>'


# ---------------------------------------------------------------- shared blocks
def preheader_bar(text, link, two_line=False):
    pad = "10px 24px" if two_line else "9px 24px"
    return card(f"""<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
<td style="font-family:{MONO};font-size:11px;line-height:17px;letter-spacing:0.8px;text-transform:uppercase;color:{MUTED};vertical-align:middle;">{text}</td>
<td align="right" style="padding-left:16px;vertical-align:middle;white-space:nowrap;"><a href="{link}" target="_blank" style="font-family:{MONO};font-size:11px;line-height:17px;letter-spacing:0.8px;text-transform:uppercase;color:{MUTED};text-decoration:underline;">View in browser</a></td>
</tr></table>""", WHITE, EDGE_WHITE, pad=pad, cls="pad-sm")


def logo_header():
    return card(f'<img src="{IMG_LOGO_INK_MARK}" width="128" height="38" alt="Hair Solutions Co." '
                f'style="display:block;margin:0 auto;border:0;width:128px;height:38px;">',
                BONE, EDGE_BONE, pad="30px 40px")


def hidden_preview(text):
    return (f'<div style="display:none;max-height:0;max-width:0;overflow:hidden;opacity:0;mso-hide:all;'
            f'font-size:1px;line-height:1px;color:{WHITE};">{text}{"&zwnj;&nbsp;" * 40}</div>')


def photo_card(src, alt, caption, w, h, caption_on_ink=False):
    if caption_on_ink:
        cap = f'<tr><td class="pad-sm" style="background-color:{INK};padding:11px 24px;">{mono(caption, ON_INK_MUTED)}</td></tr>'
        bg, edge = INK, EDGE_INK
    else:
        cap = f'<tr><td class="pad-sm" style="background-color:{WHITE};padding:11px 24px;">{mono(caption, MUTED)}</td></tr>'
        bg, edge = WHITE, EDGE_WHITE
    return f"""
<tr><td style="padding:0;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:separate;background-color:{bg};border:1px solid {edge};border-radius:12px;overflow:hidden;">
<tr><td style="padding:0;font-size:0;line-height:0;"><img src="{src}" width="598" height="{h}" alt="{alt}" class="fluid" style="display:block;width:100%;max-width:598px;height:auto;border:0;border-radius:12px 12px 0 0;"></td></tr>
{cap}
</table>
</td></tr>"""


def trust_strip():
    dot = f'<span style="color:{LINE_STRONG};">&nbsp;&middot;&nbsp;</span>'
    return card(mono(f"Handcrafted to your spec&nbsp;{dot}&nbsp;14-day inspection window&nbsp;{dot}<br>Direct line to the founder",
                     INK, lh=26, align="center"), WHITE, EDGE_WHITE, pad="8px 24px", cls="pad-sm")


MESSAGING_UNSUB = "{{ unsubscribe_link }}"


def footer(unsub_href):
    link = f"color:{ON_INK_MUTED};text-decoration:underline;"
    # Shopify Messaging "Code your own" requires its own {{ unsubscribe_link }} tag (it renders a full <a>).
    unsub = ('<span class="unsub">{{ unsubscribe_link }}</span>' if unsub_href == MESSAGING_UNSUB
             else f'<a href="{unsub_href}" target="_blank" style="{link}">Unsubscribe entirely</a>')
    inner = f"""<img src="{IMG_LOGO_BONE_MARK}" width="114" height="34" alt="Hair Solutions Co." style="display:block;margin:0 auto 10px auto;border:0;width:114px;height:34px;">
{p("Your preferences", BONE, 20, 28, 10, 700, DISPLAY, "center", "letter-spacing:-0.3px;")}
{p("You can hear from us less often, or not at all. Either is completely fine and it will not affect your order or your support.", ON_INK_MUTED, 13, 21, 20, align="center", extra="padding:0 70px;", cls="pad-copy")}
{button("Send me less often", PREFS, fill=INK, text=BONE, border=BONE, size=14, height=44, padx=34, center=True)}
{p(f'<a href="{PREFS}" target="_blank" style="{link}">Update my preferences</a> &middot; {unsub}', ON_INK_MUTED, 14, 21, 16, align="center", extra="padding-top:12px;")}
{mono(ADDRESS, ON_INK_MUTED, lh=17, align="center", mb=12, extra="padding:0 24px;")}
{p(f'<a href="{PREFS}" target="_blank" style="{link}">Manage preferences</a> &middot; <a href="{PRIVACY}" target="_blank" style="{link}">Privacy</a>', ON_INK_MUTED, 14, 21, 0, align="center")}"""
    return card(inner, INK, EDGE_INK, pad="36px 24px 36px 24px", cls="pad-sm")


def founder_text(paras, sign_mt=8):
    body = "".join(p(x) for x in paras)
    return body


def signature(title=True, mb=0):
    s = p("Vincent", INK, 24, 30, 6 if title else mb, 400, SERIF, extra="font-style:italic;")
    if title:
        s += mono("Founder, Hair Solutions Co.", MUTED, mb=mb)
    return s


# ---------------------------------------------------------------- Messaging (abandoned checkout) helpers
FNAME_MSG = '{{ customer.first_name | default: "there" }}'

# Return-to-checkout link. abandoned_checkout.url is the documented Shopify Messaging variable.
CHECKOUT_URL = "{{ abandoned_checkout.url }}"


def cart_summary(title="Still in your cart"):
    rows = f"""{{% for line_item in abandoned_checkout.line_items limit:5 %}}
{{% unless forloop.first %}}<tr><td colspan="2" style="height:10px;line-height:10px;font-size:0;">&nbsp;</td></tr>{{% endunless %}}
{"".join(kv_rows([
        ("Item", "{{ line_item.product_title }}"),
        ("Variant", "{{ line_item.variant_title }}", "{% if line_item.variant_title != blank and line_item.variant_title != 'Default Title' %}", "{% endif %}"),
        ("Qty", "{{ line_item.quantity }}"),
    ]))}
{{% endfor %}}"""
    more = (f'{{% if abandoned_checkout.remaining_products_count > 0 %}}'
            f'<tr><td colspan="2" style="border-top:1px solid {RULE_BONE};padding:16px 0 0 0;font-family:{MONO};font-size:11px;line-height:16px;letter-spacing:0.8px;text-transform:uppercase;color:{MUTED};">'
            f'+ {{{{ abandoned_checkout.remaining_products_count }}}} more item{{% if abandoned_checkout.remaining_products_count != 1 %}}s{{% endif %}}</td></tr>'
            f'{{% else %}}<tr><td colspan="2" style="border-top:1px solid {RULE_BONE};font-size:0;line-height:0;">&nbsp;</td></tr>{{% endif %}}')
    return card(eyebrow(title, INK) + table([rows, more]), BONE, EDGE_BONE)


def page(title, preview, rows, open_tracking=False, lang="en"):
    tracking = "{{ open_tracking_block }}" if open_tracking else ""
    return f"""<!DOCTYPE html>
<html lang="{lang}" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="x-apple-disable-message-reformatting">
<meta name="color-scheme" content="light">
<meta name="supported-color-schemes" content="light">
<title>{title}</title>
<!--[if mso]><noscript><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml></noscript><![endif]-->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&amp;family=Inter+Tight:wght@600;700;800&amp;family=JetBrains+Mono:wght@500;700&amp;family=Playfair+Display:ital,wght@1,400;1,500&amp;display=swap" rel="stylesheet">
<style>
  body {{ margin:0 !important; padding:0 !important; background-color:transparent; -webkit-text-size-adjust:100%; -ms-text-size-adjust:100%; }}
  table, td {{ mso-table-lspace:0pt; mso-table-rspace:0pt; }}
  img {{ -ms-interpolation-mode:bicubic; }}
  a {{ text-decoration-skip-ink:auto; }}
  .unsub a {{ color:#b8b3a4 !important; text-decoration:underline !important; }}
  @media only screen and (max-width:480px) {{
    .shell {{ width:100% !important; }}
    .pad {{ padding:32px 22px !important; }}
    .pad-sm {{ padding-left:16px !important; padding-right:16px !important; }}
    .hero-h {{ font-size:36px !important; line-height:37px !important; letter-spacing:-1.2px !important; }}
    .btn {{ width:100% !important; }} .btn a {{ display:block !important; text-align:center !important; }}
    .stack {{ display:block !important; width:100% !important; padding:0 !important; }}
    .stack-gap {{ padding-top:20px !important; }}
    .fluid {{ width:100% !important; height:auto !important; }}
    .pad-copy {{ padding:0 4px !important; }}
  }}
</style>
</head>
<body style="margin:0;padding:0;background-color:transparent;">
{hidden_preview(preview)}
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:transparent;">
<tr><td align="center" style="padding:0;">
<!--[if mso]><table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0"><tr><td><![endif]-->
<table role="presentation" class="shell" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;">
{"".join(rows)}
</table>
<!--[if mso]></td></tr></table><![endif]-->
</td></tr>
</table>
{tracking}
</body>
</html>
"""


# ---------------------------------------------------------------- CR-2 (Figma: 02_J2_CR-2_Three-Questions-Answered)
def q_card(q, a, last=False):
    return f"""<tr><td style="padding:0 0 {0 if last else 16}px 0;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:separate;background-color:{INK_SOFT};border-radius:8px;">
<tr><td class="pad-q" style="padding:20px 24px 22px 24px;">
{p(q, BONE, 22, 28, 8, 500, SERIF, extra="font-style:italic;letter-spacing:-0.2px;")}
{p(a, ON_INK_MUTED, 16, 26, 0)}
</td></tr></table></td></tr>"""


def proof_bank():
    # Figma placeholder slots. Replace the three assigns with a published-review quote before activating.
    liquid = """{% assign proof_quote = "[Proof Bank: a first-order quote that answers the &ldquo;will it look real&rdquo; doubt]" %}{% assign proof_name = "[Name, initial]" %}{% assign proof_meta = "[System worn] &middot; Permission = yes" %}{% assign proof_portrait = "" %}"""
    portrait = f"""{{% if proof_portrait != blank %}}<img src="{{{{ proof_portrait }}}}" width="200" height="250" alt="" style="display:block;width:200px;height:250px;border:0;border-radius:8px;object-fit:cover;">{{% else %}}
<table role="presentation" width="200" cellpadding="0" cellspacing="0" border="0" style="border-collapse:separate;width:200px;height:250px;background-color:{PORTRAIT};border:1px solid {LINE_STRONG};border-radius:8px;">
<tr><td valign="bottom" style="height:250px;padding:0 12px 12px 12px;vertical-align:bottom;">{mono("Consented portrait &middot; 4:5", MUTED, 10, 15, 1.4)}</td></tr></table>{{% endif %}}"""
    inner = f"""{liquid}<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
<td class="stack" width="200" valign="top" style="width:200px;vertical-align:top;">{portrait}</td>
<td class="stack stack-gap" valign="top" style="padding-left:24px;vertical-align:top;padding-top:8px;">
{eyebrow("In their words", INK, mb=14)}
{p("{{ proof_quote }}", INK, 22, 33, 20, 400, SERIF, extra="font-style:italic;letter-spacing:-0.2px;")}
{p("{{ proof_name }}", INK, 15, 20, 4, 700, DISPLAY, extra="letter-spacing:-0.2px;")}
{mono("{{ proof_meta }}", MUTED, 10, 15, 1.4)}
</td></tr></table>"""
    return card(inner, BONE, EDGE_BONE, pad="24px")


def build_cr2():
    rows = [
        preheader_bar("Will it look real, will it hold, and what if it&rsquo;s wrong.", CHECKOUT_URL),
        logo_header(),
        card(p(f"Hi {FNAME_MSG},") + p("Most people who hesitate at checkout are stuck on one of three things. Here they are, answered straight.", mb=0),
             WHITE, EDGE_WHITE, pad="38px 40px 40px 40px"),
        card(eyebrow("Three questions, answered", CORAL, mb=16) + table([
            q_card("&ldquo;Will it actually look real?&rdquo;", "At conversation distance, a well-fitted lace front is not detectable. The giveaway is never the hair &mdash; it&rsquo;s a hairline set too low, or a density too high for your age. We set both conservatively for exactly that reason."),
            q_card("&ldquo;Will it hold?&rdquo;", "With clean prep and the right adhesive, a bond holds 7 to 14 days through showering, sweating and sleeping. Prep is the variable, not the product, and we walk you through it."),
            q_card("&ldquo;What if it&rsquo;s not right when it arrives?&rdquo;", "Then you email me and we fix it. Colour off, density wrong, base size out &mdash; those are on us to resolve, and we do.", last=True),
        ]), INK, EDGE_INK, pad="40px"),
        photo_card(IMG_HAIRLINE, "A lace front hair system at the hairline, in profile", "A lace front at the hairline, in profile.", 598, 394),
        cart_summary(),
        trust_strip(),
        proof_bank(),
        card(p("Vincent", INK, 24, 30, 24, 400, SERIF, extra="font-style:italic;") + button("Finish your order", CHECKOUT_URL),
             WHITE, EDGE_WHITE, pad="64px 40px 40px 40px"),
        footer(MESSAGING_UNSUB),
    ]
    return page("The three things people ask before ordering", "Will it look real, will it hold, and what if it&rsquo;s wrong.", rows, open_tracking=True)


# ---------------------------------------------------------------- CR-1 / CR-3 / CR-4 (no Figma frame; copy verbatim from the Email Reference File decks)
def founder_card(paras, signoff=True, title=True, pad="38px 40px 40px 40px"):
    inner = p(f"Hi {FNAME_MSG},") + "".join(p(x) for x in paras)
    if signoff:
        inner += signature(title=title)
    return card(inner, WHITE, EDGE_WHITE, pad=pad)


def cta_card(label, href, note=None):
    inner = button(label, href)
    if note:
        inner += p(note, MUTED, 14, 21, 0, extra="padding-top:20px;")
    return card(inner, WHITE, EDGE_WHITE, pad="40px")


def build_cr1():
    rows = [
        preheader_bar("No pressure &mdash; just making sure nothing broke on our end.", CHECKOUT_URL),
        logo_header(),
        card(p(f"Hi {FNAME_MSG},") + p("You were partway through an order and stopped. That&rsquo;s completely fine &mdash; but occasionally it&rsquo;s because something on our side didn&rsquo;t work, and I&rsquo;d want to know.", mb=0),
             WHITE, EDGE_WHITE, pad="38px 40px 40px 40px"),
        cart_summary(),
        card(p("If it was a payment error, a shipping surprise, or the page just froze, reply and tell me. I&rsquo;ll sort it out.")
             + p("If you&rsquo;re still deciding, no rush at all. Your cart&rsquo;s saved.", mb=24)
             + p("Vincent", INK, 24, 30, 24, 400, SERIF, extra="font-style:italic;")
             + button("Finish your order", CHECKOUT_URL), WHITE, EDGE_WHITE, pad="40px"),
        footer(MESSAGING_UNSUB),
    ]
    return page("Your cart's still here", "No pressure &mdash; just making sure nothing broke on our end.", rows, open_tracking=True)


def build_cr3():
    reply_list = "".join(
        f'<tr><td width="28" valign="top" style="width:28px;padding:10px 0;border-top:1px solid {RULE_BONE};font-family:{MONO};font-size:11px;line-height:24px;color:{MUTED};">0{i}</td>'
        f'<td style="padding:10px 0;border-top:1px solid {RULE_BONE};font-family:{DISPLAY};font-size:15px;line-height:24px;font-weight:700;color:{INK};">{t}</td></tr>'
        for i, t in enumerate(["how you currently wear your hair", "whether you want daily removal or a longer bond", "your rough age bracket"], 1))
    rows = [
        preheader_bar("Tell me your situation and I&rsquo;ll tell you what I&rsquo;d choose.", CONTACT),
        logo_header(),
        card(p(f"Hi {FNAME_MSG},")
             + p("There&rsquo;s one reason for stalling I haven&rsquo;t covered, and it&rsquo;s the most common: you&rsquo;re not certain you chose the right system.")
             + p("That&rsquo;s reasonable. Base type, density, hairline, colour &mdash; it&rsquo;s a lot of decisions to make from product photos.", mb=0),
             WHITE, EDGE_WHITE, pad="38px 40px 40px 40px"),
        card(p("So here&rsquo;s an easier route. Reply to this email with:", mb=16)
             + table([reply_list], f"border-bottom:1px solid {RULE_BONE};"), BONE, EDGE_BONE),
        card(p("That&rsquo;s enough for me to tell you which base and density I&rsquo;d actually recommend, and whether what&rsquo;s in your cart is right. If it isn&rsquo;t, I&rsquo;ll say so, even if the answer is a cheaper unit.")
             + p("Or if you&rsquo;d rather talk it through properly, book fifteen minutes with me.", mb=24)
             + p("Vincent", INK, 24, 30, 24, 400, SERIF, extra="font-style:italic;")
             + button("Book 15 minutes", CONTACT), WHITE, EDGE_WHITE, pad="40px"),
        card(p("The two-minute version while you&rsquo;re deciding: lace is the most natural at the hairline and the least durable. Poly is the toughest and the easiest to clean and reattach. Hybrid takes the front from one and the back from the other &mdash; which is why most people end up there. Density should sit slightly under what feels safe; it&rsquo;s the difference between natural and obviously new.", ON_INK_MUTED, 15, 25, 0),
             INK, EDGE_INK),
        card(table(kv_rows([("What you were looking at", '{{ abandoned_checkout.line_items.first.product_title | default: "Your selected system" }}')]))
             + p("Nothing expires here. Your cart stays saved, and a spec question before you order costs you nothing &mdash; it&rsquo;s what I&rsquo;m here for.", MUTED, 14, 21, 0, extra=f"border-top:1px solid {RULE_BONE};padding-top:16px;"),
             BONE, EDGE_BONE),
        trust_strip(),
        footer(MESSAGING_UNSUB),
    ]
    return page("Not sure you picked the right one?", "Tell me your situation and I&rsquo;ll tell you what I&rsquo;d choose.", rows, open_tracking=True)


DISCOUNT_CODE = "FREESHIP"
# Same pattern Shopify documents for abandoned-checkout links: append ?discount= / &discount= to the checkout URL.
CHECKOUT_URL_DISCOUNT = ("{% if abandoned_checkout.url contains '?' %}{{ abandoned_checkout.url | append: '&discount=" + DISCOUNT_CODE +
                         "' }}{% else %}{{ abandoned_checkout.url | append: '?discount=" + DISCOUNT_CODE + "' }}{% endif %}")


def code_card():
    inner = f"""{p("If cost is the sticking point, here&rsquo;s free shipping on the order:", BONE, 16, 26, 20)}
<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:separate;"><tr>
<td style="border:1px dashed {ON_INK_MUTED};border-radius:8px;padding:12px 20px;font-family:{MONO};font-size:18px;line-height:24px;font-weight:700;letter-spacing:3px;color:{BONE};">{DISCOUNT_CODE}</td>
</tr></table>"""
    return card(inner, INK, EDGE_INK)


def build_cr4():
    rows = [
        preheader_bar("Free shipping if it helps. Either way, this is the last one.", CHECKOUT_URL_DISCOUNT, two_line=True),
        logo_header(),
        card(p(f"Hi {FNAME_MSG},") + p("Last email about this &mdash; I won&rsquo;t keep bringing it up.", mb=0),
             WHITE, EDGE_WHITE, pad="38px 40px 40px 40px"),
        code_card(),
        cart_summary(),
        card(p("And if the timing just isn&rsquo;t right, that&rsquo;s genuinely fine. Your cart stays saved, the code will be honoured whenever you come back, and I&rsquo;ll stop emailing you about it.", mb=24)
             + signature(title=True, mb=24)
             + button("Complete your order", CHECKOUT_URL_DISCOUNT), WHITE, EDGE_WHITE, pad="40px"),
        footer(MESSAGING_UNSUB),
    ]
    return page("Last note about your cart", "Free shipping if it helps. Either way, this is the last one.", rows, open_tracking=True)


# ---------------------------------------------------------------- PP-1 (Figma: 01_J1_PP-1_Order-Confirmation) -> Shopify native notification
PP1_LIQUID_HEAD = """{%- comment -%}
  PP-1 · Order Confirmation — Shopify > Settings > Notifications > Customer notifications > Order confirmation > Edit code
  Subject line field:  Your order is confirmed{% if customer.first_name != blank %}, {{ customer.first_name }}{% endif %}.
  Lead times below drive "Estimated dispatch", the delivery line and the copy branch.
  Custom orders (any line whose product handle contains "custom") use the custom lead times; everything else ships from stock.
{%- endcomment -%}
{%- assign is_custom = false -%}
{%- for li in line_items -%}{%- if li.product.handle contains 'custom' -%}{%- assign is_custom = true -%}{%- endif -%}{%- endfor -%}
{%- if is_custom -%}
{%- assign dispatch_days = 56 -%}
{%- assign delivery_days = 63 -%}
{%- else -%}
{%- assign dispatch_days = 2 -%}
{%- assign delivery_days = 7 -%}
{%- endif -%}
{%- assign fname = customer.first_name | default: billing_address.first_name -%}
{%- assign placed_s = created_at | date: '%s' | plus: 0 -%}
{%- assign dispatch_s = dispatch_days | times: 86400 | plus: placed_s -%}
{%- assign delivery_s = delivery_days | times: 86400 | plus: placed_s -%}
{%- assign summary_line = subtotal_line_items | first -%}
{%- if summary_line == nil -%}{%- assign summary_line = line_items | first -%}{%- endif -%}
{%- assign item_count = subtotal_line_items.size | default: line_items.size -%}
{%- capture product_summary -%}{{ summary_line.product.title | default: summary_line.title }}{% if summary_line.quantity > 1 %} &times; {{ summary_line.quantity }}{% endif %}{% if item_count > 1 %} + {{ item_count | minus: 1 }} more{% endif %}{%- endcapture -%}
"""


def build_pp1():
    hero = f"""{eyebrow("Order confirmed", CORAL, center=True, mb=10)}
<h1 class="hero-h" style="margin:0;font-family:{DISPLAY};font-size:48px;line-height:50px;font-weight:800;letter-spacing:-1.8px;color:{BONE};text-align:center;">Your order is confirmed{{% if fname != blank %}},<br>{{{{ fname }}}}{{% endif %}}.</h1>"""
    order = eyebrow("Your order", INK) + table(kv_rows([
        ("Order number", "{{ order_name }}"),
        ("What you ordered", "{{ product_summary }}"),
        ("Estimated dispatch", "{{ dispatch_s | date: '%B %-d, %Y' }}"),
    ]), f"border-bottom:1px solid {RULE_BONE};") + p(
        f'<a href="{{{{ order_status_url }}}}" target="_blank" style="color:{INK};text-decoration:underline;text-underline-offset:3px;">View your order {ARROW}</a>',
        INK, 15, 20, 0, 600, DISPLAY, extra="padding-top:16px;")

    steps = [("01", "Production starts", "The base is cut and the hair is hand-tied to your spec."),
             ("02", "I email you when it goes into production", None),
             ("03", "I email you when it ships, with tracking", None),
             ("04", "It should be at your door around {{ delivery_s | date: '%B %-d' }}", None)]
    stock_steps = [("01", "We check and pack it", "Your system is in stock, so it&rsquo;s inspected by hand and packed now."),
                   ("02", "I email you when it ships, with tracking", None),
                   ("03", "It should be at your door around {{ delivery_s | date: '%B %-d' }}", None)]
    step_rows = ["{% if is_custom %}"]
    for i, (n, t, d) in enumerate(steps + [("", "{% else %}", None)] + stock_steps):
        if t == "{% else %}":
            step_rows.append("{% else %}")
            continue
        desc = p(d, MUTED, 14, 21, 0, extra="padding-top:4px;") if d else ""
        step_rows.append(f"""<tr>
<td width="48" valign="top" style="width:48px;border-top:1px solid {RULE_WHITE};padding:12px 0;font-family:{MONO};font-size:11px;line-height:22px;color:{MUTED};vertical-align:top;">{n}</td>
<td valign="top" style="border-top:1px solid {RULE_WHITE};padding:11px 0 12px 0;vertical-align:top;">{p(t, INK, 15, 22, 0, 700, DISPLAY, extra="letter-spacing:-0.2px;")}{desc}</td></tr>""")
    step_rows.append("{% endif %}")
    nxt = eyebrow("What happens next", INK) + table(step_rows, f"border-bottom:1px solid {RULE_WHITE};") + p(
        "No filler emails in between &mdash; only the real steps.", MUTED, 14, 21, 0, extra="padding-top:18px;")

    rows = [
        preheader_bar("Here&rsquo;s exactly what happens between now and the day it arrives.", "{{ order_status_url }}", two_line=True),
        logo_header(),
        card(hero, INK, EDGE_INK, pad="74px 32px 74px 32px"),
        card(p("Hi {% if fname != blank %}{{ fname }}{% else %}there{% endif %},") + p("Your order is in. Thank you &mdash; genuinely.")
             + p("{% if is_custom %}Here&rsquo;s what happens now. Your system isn&rsquo;t sitting on a shelf waiting to be boxed; it gets made for you. That takes time, and I&rsquo;d rather tell you that up front than have you wondering where it is.{% else %}Here&rsquo;s what happens now. Your system is in stock, so it gets checked by hand and packed straight away &mdash; no long wait.{% endif %}", mb=0),
             WHITE, EDGE_WHITE, pad="38px 40px 40px 40px"),
        card(order, BONE, EDGE_BONE),
        photo_card(IMG_WORKSHOP, "Hands fitting a hair system by hand in the workshop", "Every system is fitted and finished by hand before it ships.", 598, 396, caption_on_ink=True),
        card(nxt, WHITE, EDGE_WHITE),
        card(p("If anything about your order looks wrong, reply to this email today and I&rsquo;ll fix it before {% if is_custom %}production starts{% else %}it ships{% endif %}.", mb=24) + signature(),
             BONE, EDGE_BONE, pad="38px 40px 40px 40px"),
        card(button("View your order", "{{ order_status_url }}")
             + p("Questions about your order? Reply to this email &mdash; it comes straight to me.", MUTED, 14, 21, 0, extra="padding-top:24px;"),
             WHITE, EDGE_WHITE, pad="54px 40px 40px 40px"),
        footer(PREFS),
    ]
    return PP1_LIQUID_HEAD + page("Your order is confirmed", "Here&rsquo;s exactly what happens between now and the day it arrives.", rows)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    files = {
        "pp-1_order-confirmation.shopify-notification.liquid.html": build_pp1(),
        "cr-1_your-carts-still-here.shopify-messaging.liquid.html": build_cr1(),
        "cr-2_three-questions-answered.shopify-messaging.liquid.html": build_cr2(),
        "cr-3_not-sure-you-picked-right.shopify-messaging.liquid.html": build_cr3(),
        "cr-4_last-note-free-shipping.shopify-messaging.liquid.html": build_cr4(),
    }
    for name, html in files.items():
        (OUT / name).write_text(html, encoding="utf-8")
        print(f"{name}: {len(html.encode()) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
