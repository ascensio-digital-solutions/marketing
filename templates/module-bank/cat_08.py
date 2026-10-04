"""Category 08 · Utility: one function per module, `fn(theme) -> card rows`. See build_bank.py."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".claude/skills/shopify-email-html/scripts"))
from v6_html import *  # noqa: F401,F403
from bank_registry import module


@module("Regard / sign-off", "Utility · Sign-off", "Sign-off",
        ["Warmly,", "Hair Solutions Co.", "A new look should still feel unmistakably like you."],
        ["Closing in the v6 body role, name in the v6 subtitle role, tagline in the v6 note role (serif italic)",
         "Never a handwritten-signature image"])
def signoff(th):
    return card(body("[Closing],", th, mb=10) + subtitle("[Name]", th, mb=10) + note("[Tagline: one short line]", th, mb=0),
                th, pad="36px 40px")


def _link_rows(th, labels):
    rows = "".join(f'<tr><td style="border-top:1px solid {th["rule"]};padding:12px 0;">{textlink(l, th)}</td></tr>' for l in labels)
    return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;">{rows}</table>'


@module("Divider", "Divider · Short rule", "Divider",
        ["SECTION BREAK · 48PX RHYTHM"],
        ["Figma's divider was a rule plus a usage note ('48px rhythm'): the note is dropped; the divider is a v6 card holding the short coral rule, so it keeps the flush stack",
         "Use it where two blocks share a surface and need a break; where the surface can change instead, change the surface (the composition guide's seam rule)"])
def divider_short_rule(th):
    return card(short_rule(mb=0), th, pad="28px 40px")


@module("Divider · Thin solid rule", "Divider · Thin rule", "Divider",
        ["Thin solid line"],
        ["Full-width hairline in the theme's rule colour inside a v6 card (the Figma divider was a free-floating 600px frame)",
         "Use sparingly: a hairline between two text blocks of the same surface"])
def divider_thin_rule(th):
    return card(hairline(th), th, pad="24px 40px")


@module("SUPPORT CONTACT BAR", "Utility · Support contact bar", "Footer",
        ["Questions? Reply to this email or reach us at support@hairsolutions.co"],
        ["One centred line in the v6 small role with the address as an underlined link",
         "The address is a slot: use the approved support address of the store"])
def utility_support_bar(th):
    line = (f'<p style="margin:0;font-family:{SANS};font-size:13px;line-height:21px;color:{th["muted"]};text-align:center;">'
            f'[Prompt: one short line] <a href="{SITE}" target="_blank" style="color:{th["text"]};font-weight:600;'
            f'text-decoration:underline;">[Support address]</a></p>')
    return card(line, th, pad="24px 40px")


@module("EMAIL PREFERENCE SAVE", "Utility · Frequency save", "Utility",
        ["Before you go –", "Would fewer emails work better for you?", "Once a month →", "Unsubscribe instead"],
        ["Offers a lower frequency before the unsubscribe, the retention pattern of the v6 emails; the offer button is the one coral pill",
         "The unsubscribe stays a plain underlined link (never hidden or de-emphasised below legal requirements)"])
def utility_frequency_save(th):
    actions = cols([button("[Button label]", th, size=13, height=46, padx=24), textlink("[Unsubscribe link]", th).replace(f" {ARROW}", "")],
                   16, valign="middle", weights=[44, 56])
    return card(subtitle("[Title]", th, mb=8) + small("[Description: one or two lines]", th, mb=20) + actions,
                th, pad="32px 40px", cls="pad-sm")


@module("Preference centre", "Utility · Preference centre", "Utility",
        ["YOUR PREFERENCES", "Not the right frequency?…", "Send me less often →", "Update my preferences →", "Unsubscribe entirely →"],
        ["Eyebrow, a short note and three link rows on hairlines; every link is a slot wired to the subscription pages"])
def utility_preference_centre(th):
    return card(eyebrow("[Eyebrow]", th, mb=14) + body("[Body: two lines]", th, mb=16) +
                _link_rows(th, ["[Link 1]", "[Link 2]", "[Link 3]"]), th, pad="40px")


@module("Base type guidance", "Utility · Base type guidance", "Utility",
        ["Still weighing up base types?", "Lace — most natural… Poly — most durable… Hybrid — balanced…", "Compare base types →"],
        ["Title in the v6 title role (sentence case), three guidance lines in the v6 body role, v6 coral pill",
         "Guidance lines are slots: keep one line per option"])
def utility_base_guidance(th):
    return card(title("[Title]", th, mb=14) + body("[Option 1: one line]", th, mb=8) + body("[Option 2: one line]", th, mb=8) +
                body("[Option 3: one line]", th, mb=22) + button("[Button label]", th), th, pad="40px")
