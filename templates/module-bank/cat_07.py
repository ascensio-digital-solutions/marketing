"""Category 07 · Transactional lifecycle: one function per module, `fn(theme) -> card rows`. See build_bank.py."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".claude/skills/shopify-email-html/scripts"))
from v6_html import *  # noqa: F401,F403
from bank_registry import module


@module("SHIPPING TRACKER", "Order · Shipping tracker", "Transactional",
        ["On its way to you", "Processed / Shipped / In transit / Delivered", "Carrier: UPS Ground", "Tracking number: 1Z999AA10123456784",
         "Estimated arrival: Aug 9", "Track package"],
        ["Progress uses the text colour for finished steps, not coral (coral budget: one button plus at most two marks)",
         "Inactive steps use the v6 strong line; step labels in the v6 small role",
         "Detail rows use the v6 label/value hairline rows",
         "All values are slots (carrier, tracking number, arrival); wire them to the shipping variables in the template"])
def shipping_tracker(th):
    done = [True, True, False, False]
    labels = ["[Step 1]", "[Step 2]", "[Step 3]", "[Step 4]"]

    def dot(on):
        c = th["text"] if on else LINE_STRONG
        return (f'<div style="width:12px;height:12px;line-height:12px;font-size:0;border-radius:999px;'
                f'background-color:{c};">&nbsp;</div>')

    def rule(on):
        c = th["text"] if on else LINE_STRONG
        return f'<div style="height:2px;line-height:2px;font-size:0;background-color:{c};">&nbsp;</div>'

    cells = []
    for i in range(4):
        if i < 3:
            inner = ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>'
                     f'<td width="12" valign="middle" style="width:12px;">{dot(done[i])}</td>'
                     f'<td valign="middle" style="padding:0 6px 0 6px;">{rule(done[i] and done[i + 1])}</td></tr></table>')
        else:
            inner = f'<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td width="12" style="width:12px;">{dot(done[i])}</td></tr></table>'
        cells.append(f'<td width="25%" valign="middle" style="width:25%;">{inner}</td>')
    progress = f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>{"".join(cells)}</tr></table>'
    lab = ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>' +
           "".join(f'<td width="25%" valign="top" style="width:25%;padding-top:8px;">{small(l, th)}</td>' for l in labels) +
           '</tr></table>')
    rows = kv_rows([("Carrier", "[Carrier]"), ("Tracking number", "[Tracking number]"), ("Estimated arrival", "[Estimated arrival]")], th)
    return card(subtitle("[Status line]", th, mb=18) + progress + lab + gap(18) + rows + gap(24) +
                button("[Button label]", th), th, pad="40px")
