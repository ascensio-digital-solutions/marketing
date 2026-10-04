"""Category 01 · Global chrome: one function per module, `fn(theme) -> card rows`. See build_bank.py."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".claude/skills/shopify-email-html/scripts"))
from v6_html import *  # noqa: F401,F403
from bank_registry import module


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


# The Figma nav modules "Logo Center Light", "Logo Centered Above Horizontal" and "Inverted Ink Theme" are drawn
# identically (centred logo, links row below). The bank keeps all three ids and gives each a distinct, rule-based
# layout (alignment and structure are free variables in the composition guide); see each adaptations list.

@module("Pre-Header", "Preheader · Message and browser link", "Preheader bar",
        ["New textures and lengths now available", "View in browser"],
        ["Meta role (JetBrains Mono 11, tracked) on the v6 preheader surface; v6 default is the White version",
         "'View in browser' is a slot: Shopify Messaging has no view-in-browser variable (see PROJECT.md), leave it out or link your own page"])
def preheader(th):
    row = ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>'
           f'<td align="left" valign="middle" style="padding-right:16px;">{meta("[Preheader text]", th)}</td>'
           f'<td align="right" valign="middle" style="white-space:nowrap;">'
           f'<a href="{SITE}" target="_blank" style="font-family:{MONO};font-size:11px;line-height:17px;font-weight:500;'
           f'letter-spacing:0.9px;text-transform:uppercase;color:{th["muted"]};text-decoration:underline;">[View in browser]</a></td></tr></table>')
    return card(row, th, pad="10px 24px", cls="pad-sm")


@module("Navigation · Logo Center Light", "Navigation · Centred logo and links", "Navigation",
        ["Shop systems", "System guide", "Care", "Support"],
        ["Logo is the approved v5 wordmark on Shopify Files (ink on light, bone on Ink)",
         "Links in the v6 eyebrow face, centred, wrapping on mobile; the Figma name said 'light' but it is now a real three-theme module"])
def nav_centred(th):
    return card(logo(th, 128) + gap(20) + nav_links(th), th, pad="32px 40px")


@module("Navigation · Logo Left / Links Right", "Navigation · Logo left, links right", "Navigation",
        ["Shop systems", "System guide", "Care", "Support"],
        ["Logo (112px, as the v6 header) and links stay side by side on mobile; the links wrap to two lines",
         "Approved v5 wordmark, v6 eyebrow face for the links"])
def nav_logo_left(th):
    row = ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>'
           f'<td align="left" valign="middle" width="112" style="width:112px;">{logo(th, 112, center=False)}</td>'
           f'<td align="right" valign="middle">{nav_links(th, align="right", gap_px=16)}</td></tr></table>')
    return card(row, th, pad="28px 40px")


@module("Navigation · Logo Centered Above Horizontal", "Navigation · Logo above a justified link bar", "Navigation",
        ["Shop systems", "System guide", "Care", "Support"],
        ["Figma drew this identically to the centred nav; here the four links are equal-width cells in a full-width bar under a hairline",
         "Link cells stay four across on mobile (they shrink and wrap)"])
def nav_justified(th):
    cells = "".join(f'<td align="center" width="25%" style="width:25%;padding:14px 4px 0 4px;"><a href="{SITE}" target="_blank" '
                    f'style="font-family:{DISPLAY};font-size:12px;line-height:18px;font-weight:600;letter-spacing:1.2px;'
                    f'text-transform:uppercase;color:{th["text"]};text-decoration:none;">[Link {i}]</a></td>' for i in range(1, 5))
    bar = (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" '
           f'style="border-top:1px solid {th["rule"]};"><tr>{cells}</tr></table>')
    return card(logo(th, 128) + gap(22) + bar, th, pad="32px 24px", cls="pad-sm")


@module("Navigation · Centered Brand Splash with Social", "Navigation · Centred logo, links and social", "Navigation",
        ["Shop systems", "System guide", "Care", "Support", "Instagram   Facebook   LinkedIn"],
        ["Social names are slots in the v6 meta role (add real channels once confirmed)",
         "Approved v5 wordmark; links in the v6 eyebrow face"])
def nav_splash_social(th):
    social = meta("[Social 1] &nbsp;&middot;&nbsp; [Social 2] &nbsp;&middot;&nbsp; [Social 3]", th, "center")
    return card(logo(th, 128) + gap(20) + nav_links(th) + gap(18) + social, th, pad="36px 40px")


@module("Navigation · Centered Logo Only", "Navigation · Centred logo", "Navigation",
        [],
        ["Logo at 128px (v6 header size), centred, 30px padding: the v6 Frame · Header"])
def nav_logo_only(th):
    return card(logo(th, 128), th, pad="30px 40px")


@module("Navigation · Centered Logo with Underline", "Navigation · Centred logo, links and rule", "Navigation",
        ["Shop systems", "System guide", "Care", "Support"],
        ["The underline is a v6 hairline (the surface's rule colour), full content width, under the links",
         "Approved v5 wordmark; links in the v6 eyebrow face"])
def nav_underline(th):
    return card(logo(th, 128) + gap(20) + nav_links(th) + gap(22) + hairline(th), th, pad="32px 40px 28px 40px")


@module("Navigation · Inverted Ink Theme", "Navigation · Compact centred logo and links", "Navigation",
        ["Shop systems", "System guide", "Care", "Support"],
        ["Figma drew an 'inverted ink' nav identical to the centred one; it is now a compact variant (96px logo, tighter padding) so the three themes are real",
         "Named for the layout, not the colour: Bone, Ink and White all exist"])
def nav_compact(th):
    return card(logo(th, 96) + gap(14) + nav_links(th, gap_px=20, size=11), th, pad="22px 24px", cls="pad-sm")


@module("Footer", "Footer · Logo, links and legal", "Footer",
        ["Shop Systems", "Our Story", "Guides", "Contact", "In · YouTube · Instagram · X", "© 2026 Hair Solutions Co. · Unsubscribe · Manage preferences"],
        ["Links are slots in the v6 body-small face; the legal line is the v6 meta role with the registered address from the v6 emails",
         "Shopify Messaging adds its own unsubscribe footer after sections; keep this card for brand, links and address only"])
def footer_links(th):
    links = nav_links(th, gap_px=20, size=13).replace("text-transform:uppercase;", "text-transform:none;").replace("letter-spacing:1.5px;", "letter-spacing:0;")
    return card(logo(th, 112) + gap(20) + links + gap(14) +
                meta("[Social 1] &nbsp;&middot;&nbsp; [Social 2] &nbsp;&middot;&nbsp; [Social 3]", th, "center") + gap(14) +
                meta(ADDRESS, th, "center"), th, pad="36px 24px", cls="pad-sm")


@module("Brand logo", "Brand · Logo panel", "Logo",
        ["hair solutions co."],
        ["Figma set the name as live text in a display italic; the bank uses the approved v5 wordmark image (never retyped), larger, as a standalone brand panel"])
def brand_logo(th):
    return card(logo(th, 176), th, pad="48px 40px")


@module("Email footer", "Footer · Brand line", "Footer",
        ["Hair Solutions Co."],
        ["Brand name in the v6 subtitle role, centred; for emails that need only a name line"])
def footer_brand_line(th):
    return card(subtitle("Hair Solutions Co.", th, "center", mb=0), th, pad="28px 40px")
