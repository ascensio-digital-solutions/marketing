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
