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
