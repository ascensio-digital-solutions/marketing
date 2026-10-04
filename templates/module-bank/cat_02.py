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
