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
