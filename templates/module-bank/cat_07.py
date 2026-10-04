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


def _thumb(th, size=56):
    return photo_slot("", th, size).replace("padding:0 16px", "padding:0")


def _line_item(th, qty=True):
    """Thumbnail, name and detail line, price on the right (stays on one line on mobile)."""
    return ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>'
            f'<td width="56" valign="middle" style="width:56px;padding:0;">{_thumb(th)}</td>'
            f'<td valign="middle" style="padding:0 14px;">{name("[Product name]", th, mb=2)}{small("[Variant details] &middot; [Qty]", th)}</td>'
            f'<td valign="middle" align="right" style="padding:0;white-space:nowrap;">{price("[$00.00]", th, "right", small_=True)}</td></tr></table>')


@module("ORDER PRODUCTION STATUS", "Order · Production status", "Transactional",
        ["Order #HS-10482", "IN PRODUCTION", "System 01 - Lace, Base 06 · Density: Medium · Qty 1 · $329.00",
         "Estimated ship date: 4-6 weeks from today"],
        ["Order number with a status pill, one line item, and the ship estimate",
         "Status pill is the v6 badge (mono 11, 999px); product thumbnail is a labelled slot",
         "Order number, status, item and estimate are slots wired to the order variables in the template"])
def order_production_status(th):
    head = ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>'
            f'<td valign="middle" style="padding:0;">{name("[Order number]", th, mb=0)}</td>'
            f'<td valign="middle" align="right" style="padding:0;white-space:nowrap;">{badge("[Status]", th)}</td></tr></table>')
    return card(head + gap(18) + _line_item(th) + gap(16) + small("[Estimate: ship date or window]", th), th, pad="32px", cls="pad-sm")


@module("ABANDONED CART SUMMARY", "Order · Cart summary", "Transactional",
        ["Still in your cart", "System 01 - Lace, Base 06 · $329.00", "Care Kit - Starter · $59.00", "Subtotal $388.00", "Return to cart →"],
        ["Two line items, a subtotal row and the button; line items repeat per cart line in the template",
         "Title in the v6 subtitle role; subtotal on the v6 label/value hairline row; button is the v6 coral pill"])
def order_cart_summary(th):
    return card(subtitle("[Title]", th, mb=16) + _line_item(th) + gap(14) + _line_item(th) + gap(14) +
                kv_rows([("[Subtotal]", "[$00.00]")], th) + gap(22) + button("[Button label]", th), th, pad="32px", cls="pad-sm")


@module("SAVED CHECKOUT SUMMARY", "Order · Saved checkout summary", "Transactional",
        ["Your checkout is saved", "System 01 - Lace, Base 06 · $329.00", "Shipping Free", "Estimated tax $0.00", "Total $329.00", "Complete checkout →"],
        ["One line item, shipping, tax and total rows, and the button",
         "Rows are the v6 label/value hairline rows; button is the v6 coral pill"])
def order_saved_checkout(th):
    return card(subtitle("[Title]", th, mb=16) + _line_item(th) + gap(14) +
                kv_rows([("[Shipping]", "[Value]"), ("[Estimated tax]", "[$00.00]"), ("[Total]", "[$00.00]")], th) +
                gap(22) + button("[Button label]", th), th, pad="32px", cls="pad-sm")


@module("BILLING SUMMARY", "Order · Billing summary", "Transactional",
        ["Billing summary", "Plan: Continuity Plan - Quarterly", "Payment method: Visa •••• 4417", "Renewal date: Aug 19, 2026",
         "Amount due: $249.00", "Update payment method →"],
        ["Four label/value rows on the v6 hairline rows and one button",
         "Card details are slots: never put a real card or number in a bank section (the template supplies the last four digits)"])
def order_billing_summary(th):
    rows = kv_rows([("[Plan]", "[Value]"), ("[Payment method]", "[Value]"), ("[Renewal date]", "[Value]"), ("[Amount due]", "[$00.00]")], th)
    return card(subtitle("[Title]", th, mb=16) + rows + gap(22) + button("[Button label]", th), th, pad="32px", cls="pad-sm")


@module("Order confirmation", "Order · Confirmation details", "Transactional",
        ["ORDER CONFIRMED", "Your order is in production", "Order number #HS-40218", "Specification System 01 · Lace, Base 06",
         "Status In production", "Estimated dispatch Aug 24", "I'll email you at each real step…", "View order status →"],
        ["Eyebrow, title, four detail rows, a note and the button: the post-purchase pattern of the v6 emails",
         "Detail rows on the v6 label/value hairline rows; title in the v6 title role (sentence case); button is the v6 coral pill"])
def order_confirmation_details(th):
    rows = kv_rows([("[Order number]", "[Value]"), ("[Specification]", "[Value]"), ("[Status]", "[Value]"), ("[Estimated dispatch]", "[Value]")], th)
    return card(eyebrow("[Eyebrow]", th, mb=14) + title("[Title]", th, mb=18) + rows + gap(22) +
                body("[Body: two lines]", th, mb=22) + button("[Button label]", th), th, pad="40px")


@module("Shipping confirmation", "Order · Shipping confirmation", "Transactional",
        ["ON ITS WAY", "Your order has shipped", "Carrier UPS Ground", "Tracking number 1Z999AA10123456784", "Estimated delivery Aug 9",
         "Open it over a table, not a sink…", "Track your delivery →"],
        ["Eyebrow, title, three shipping rows, a note and the button",
         "Carrier, tracking number and delivery date are slots wired to the fulfilment variables"])
def order_shipping_confirmation(th):
    rows = kv_rows([("[Carrier]", "[Value]"), ("[Tracking number]", "[Value]"), ("[Estimated delivery]", "[Value]")], th)
    return card(eyebrow("[Eyebrow]", th, mb=14) + title("[Title]", th, mb=18) + rows + gap(22) +
                body("[Body: one line]", th, mb=22) + button("[Button label]", th), th, pad="40px")


@module("Cart reminder", "Order · Cart reminder", "Transactional",
        ["IN YOUR CART", "Still in your cart", "System 01 - Lace, Base 06 · Density: Medium · Qty 1 · $329.00", "Care Kit - Starter · Qty 1 · $59.00",
         "Your selections are saved…", "Return to your cart →"],
        ["Eyebrow, title and two item rows (name and detail left, price right), a note and the button",
         "Item rows are the v6 hairline rows with the price in the serif-italic role; they repeat per cart line in the template"])
def order_cart_reminder(th):
    def row():
        return (f'<tr><td style="border-top:1px solid {th["rule"]};padding:16px 0;" valign="middle">{name("[Product name]", th, mb=2)}'
                f'{small("[Variant details] &middot; [Qty]", th)}</td>'
                f'<td align="right" valign="middle" style="border-top:1px solid {th["rule"]};padding:16px 0 16px 16px;white-space:nowrap;">'
                f'{price("[$00.00]", th, "right", small_=True)}</td></tr>')
    rows = ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;">'
            + row() + row() + '</table>')
    return card(eyebrow("[Eyebrow]", th, mb=14) + title("[Title]", th, mb=18) + rows + gap(22) +
                body("[Body: one line]", th, mb=22) + button("[Button label]", th), th, pad="40px")


@module("Browse reminder", "Order · Browse reminder", "Transactional",
        ["YOU WERE LOOKING AT", "Custom hair system", "LACE FRONT / MEDIUM DENSITY", "View it again →"],
        ["Eyebrow, a wide image slot, product title, two body lines and the button",
         "Image is a labelled slot (use the viewed product's approved render); product name, spec and link come from the browse event"])
def order_browse_reminder(th):
    return card(eyebrow("[Eyebrow]", th, mb=14) + photo_slot("[Photo · product viewed]", th, 150) + gap(18) +
                title("[Product name]", th, mb=12) + meta("[Spec line]", th, mb=10) + body("[Body: two lines]", th, mb=22) +
                button("[Button label]", th), th, pad="40px")


@module("Change summary", "Order · Change summary", "Transactional",
        ["WHAT'S CHANGED", "— Add change one.", "— Add change two.", "— Add change three."],
        ["Eyebrow and three change lines, each on a hairline row; the dash prefix is a text dash, not coral",
         "Lines are slots; use for policy, terms or product-change notices"])
def order_change_summary(th):
    def line(i):
        return (f'<tr><td style="border-top:1px solid {th["rule"]};padding:12px 0;font-family:{SANS};font-size:15px;line-height:22px;'
                f'color:{th["text"]};">&mdash;&nbsp; [Change {i}]</td></tr>')
    rows = ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;">'
            + line(1) + line(2) + line(3) + '</table>')
    return card(eyebrow("[Eyebrow]", th, mb=14) + rows, th, pad="40px")
