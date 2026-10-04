"""Category 05 · Services & proof: one function per module, `fn(theme) -> card rows`. See build_bank.py."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".claude/skills/shopify-email-html/scripts"))
from v6_html import *  # noqa: F401,F403
from bank_registry import module


@module("SERVICE · STATS BAND DARK", "Service · Stats band", "Stats",
        ["By the numbers", "10K+ Customers", "97% Satisfaction", "15+ Years", "40+ Salons"],
        ["Figma named it 'dark' but drew bone text on a bone card: rebuilt as a real three-theme module",
         "Numerals: Inter Tight 800 with a serif-italic suffix; the suffix is coral only on Ink, ink on light",
         "Eyebrow in the v6 eyebrow role (coral dash, label ink on light, coral on Ink)",
         "Eyebrow, numerals and labels are centred, so the 2x2 grid is balanced in the card",
         "Two across on mobile (no stacking)"])
def stats_band(th):
    def stat(i):
        value = (f'<p style="margin:0 0 6px 0;font-family:{DISPLAY};font-size:56px;line-height:60px;font-weight:800;'
                 f'letter-spacing:-2px;text-align:center;color:{th["text"]};">[00]{em("+", th)}</p>')
        return value + meta(f"[Label {i}]", th, "center")
    grid = pair_row([stat(1), stat(2)], th, 24) + gap(28) + pair_row([stat(3), stat(4)], th, 24)
    return card(eyebrow("[Eyebrow]", th, center=True, mb=28) + grid, th, pad="48px 40px")
