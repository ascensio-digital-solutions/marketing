"""Category 06 · CTAs & promotions: one function per module, `fn(theme) -> card rows`. See build_bank.py."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".claude/skills/shopify-email-html/scripts"))
from v6_html import *  # noqa: F401,F403
from bank_registry import module


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


def _centre(html):
    return f'<table role="presentation" align="center" cellpadding="0" cellspacing="0" border="0" style="margin:0 auto;"><tr><td>{html}</td></tr></table>'


@module("Call-To-Action", "CTA · Headline with button", "CTA",
        ["Planning a Change?", "Keep what works and adjust only what needs to change.", "Build Your Next System →"],
        ["Headline in the v6 headline role (48/50, 800), left-aligned, with the body under it; the Figma body was centred under a left headline, aligned left here",
         "Button is the v6 coral pill"])
def cta_headline_button(th):
    return card(headline("[Headline]", th, mb=16) + body("[Body: one line]", th, mb=26) + button("[Button label]", th), th, pad="48px 40px")


@module("CTA · CENTERED HEADING + BODY + CORAL", "CTA · Centred heading, body and button", "CTA",
        ["Secure Your Priority Slot Today", "Each master artisan can only ventilate 4 systems per month…", "Schedule Appointment →"],
        ["Figma's 'coral' in the name meant the coral button: kept as the one v6 coral pill; no coral surface",
         "Title in the v6 title role, centred; body in the v6 body role"])
def cta_centred_heading(th):
    return card(title("[Heading]", th, "center", mb=14) + body("[Body: two lines]", th, "center", mb=26) +
                button("[Button label]", th, center=True), th, pad="48px 40px")


@module("CTA · TWO BUTTONS", "CTA · Two buttons", "CTA",
        ["Explore Our Base Systems", "Compare transparent Swiss lace, durable poly skin…", "Shop All Systems", "Read base guide →"],
        ["One coral primary pill and one outline pill; they sit side by side on desktop and stack on mobile",
         "Only the primary is coral (one coral button per email); the outline uses the theme's text colour"])
def cta_two_buttons(th):
    return card(title("[Heading]", th, "center", mb=14) + body("[Body: two lines]", th, "center", mb=26) +
                cols([button("[Primary label]", th, center=True), button("[Secondary label]", th, "outline", center=True)], 12, valign="middle"),
                th, pad="48px 40px")


@module("CTA · DARK INK THEME PANEL", "CTA · Large centred panel", "CTA",
        ["Private Stylist Sessions", "Our master stylists offer virtual mappings…", "Book Private Consultation →"],
        ["Figma named it 'dark ink theme' (and drew it dark in every theme cell): rebuilt as a real three-theme module and renamed for its layout",
         "Larger vertical padding and a 30px title (title role) set it apart from the standard centred CTA"])
def cta_large_panel(th):
    t = title("[Heading]", th, "center", mb=14).replace("font-size:28px;line-height:31px", "font-size:30px;line-height:36px")
    return card(t + body("[Body: two lines]", th, "center", mb=28) + button("[Button label]", th, center=True), th, pad="64px 40px")


@module("CTA · APP REFERRALS BLOCK", "CTA · App store badges", "CTA",
        ["Manage Orders On The Go", "Track your custom ventilation steps, order supplies…", "App Store · Google Play"],
        ["Two store badges side by side under the centred text; badges are labelled slots (use the official store badge images)",
         "Title in the v6 title role, body in the v6 body role"])
def cta_app_badges(th):
    def badge_slot(label):
        return photo_slot(label, th, 39).replace("padding:0 16px", "padding:0 8px")
    badges = (f'<table role="presentation" align="center" cellpadding="0" cellspacing="0" border="0" style="margin:0 auto;"><tr>'
              f'<td width="130" style="width:130px;padding:0 6px 0 0;">{badge_slot("[App Store]")}</td>'
              f'<td width="130" style="width:130px;padding:0 0 0 6px;">{badge_slot("[Google Play]")}</td></tr></table>')
    return card(title("[Heading]", th, "center", mb=14) + body("[Body: two lines]", th, "center", mb=26) + badges, th, pad="48px 40px")


@module("CTA · MINIMAL ARROW LINK", "CTA · Minimal arrow link", "CTA",
        ["Explore the Atelier standard →"],
        ["A single text link with an arrow, no button; underline link in the v6 link style",
         "Sentence case; link centred"])
def cta_arrow_link(th):
    return card('<p style="margin:0;text-align:center;">' + textlink("[Link text]", th) + '</p>', th, pad="40px")


@module("CTA · DISCOUNT CODE PROMOTION", "CTA · Discount code", "Promo",
        ["Welcome To Hair Solutions Co.", "Start your journey with a virtual mapping…", "CODE: FIRSTATELIER", "Get 15% Off Consultation →"],
        ["Code in the v6 dashed code chip (mono 15, 8px radius), centred; title in the v6 title role",
         "Button is the v6 coral pill; the code stays a slot (never a real code)"])
def cta_discount_code(th):
    return card(title("[Heading]", th, "center", mb=12) + body("[Body: two lines]", th, "center", mb=24) +
                _centre(code_chip("[CODE]", th)) + gap(24) + button("[Button label]", th, center=True), th, pad="48px 40px")


@module("CTA · BONE RAISED CARD", "CTA · Raised card", "CTA",
        ["Need A Customized Quote?", "Answer a few questions about your coverage goals…", "Start Customizer Quiz →"],
        ["Figma's 'bone raised card' is a lighter card sitting on the page: rebuilt as a v6 inset (8px radius) inside the card, so it stays one card in three themes",
         "Title in the v6 title role, body in the v6 body role, v6 coral pill"])
def cta_raised_card(th):
    inner = title("[Heading]", th, "center", mb=12) + body("[Body: two lines]", th, "center", mb=24) + button("[Button label]", th, center=True)
    raised = (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" '
              f'style="border-collapse:separate;background-color:{th["inset"]};border:1px solid {th["inset_edge"]};'
              f'border-radius:8px;"><tr><td class="pad" style="padding:40px;">{inner}</td></tr></table>')
    return card(raised, th, pad="32px", cls="pad-sm")


@module("Promotional code", "Promo · Code block", "Promo",
        ["YOUR CODE", "WELCOMEBACK20", "Valid 14 days · applied at checkout"],
        ["Eyebrow in the v6 eyebrow role, the code as the title role (slot, never a real code), terms in the v6 body role",
         "The Figma 'paper' name dropped: the module now exists in three themes"])
def promo_code_block(th):
    return card(eyebrow("[Eyebrow]", th, mb=14) + title("[CODE]", th, mb=14) +
                body("[Terms: valid for, where it applies]", th, mb=10) + body("[Condition: one line]", th, mb=0), th, pad="40px")
