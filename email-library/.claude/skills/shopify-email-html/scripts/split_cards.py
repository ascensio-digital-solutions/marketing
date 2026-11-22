#!/usr/bin/env python3
"""Split a full table-based email into one Shopify Messaging Custom Liquid fragment per card.

Usage: split_cards.py EMAIL.html OUT_DIR [--card-open '<tr><td style="padding:0;">']

Each card row (a row starting with --card-open inside the .shell table) becomes OUT_DIR/NN.html,
wrapped in a fluid 600px shell. 01.html also carries the <link> and <style> from <head>.
The hidden preheader and {{ open_tracking }}/{{ open_tracking_block }} are dropped.
"""
import argparse
import pathlib
import re
import sys

WRAP = ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" '
        'style="background-color:transparent;"><tr><td align="center" style="padding:0;">\n'
        '<table role="presentation" class="shell" width="100%" cellpadding="0" cellspacing="0" '
        'border="0" style="width:100%;max-width:600px;">\n{card}</table>\n</td></tr></table>\n')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("email")
    ap.add_argument("out_dir")
    ap.add_argument("--card-open", default='<tr><td style="padding:0;">\n')
    a = ap.parse_args()
    html = pathlib.Path(a.email).read_text(encoding="utf-8")
    head = "".join(re.findall(r'<link href="https://fonts\.googleapis\.com[^>]*>', html)[:1])
    style = re.search(r"<style>.*?</style>", html, re.S)
    head = (head + "\n" if head else "") + (style.group(0) + "\n" if style else "")
    body_m = re.search(r'class="shell"[^>]*>(.*)</body>', html, re.S)
    if not body_m:
        sys.exit("ERROR: no table with class=\"shell\" found")
    body = body_m.group(1)
    body = body.replace("{{ open_tracking_block }}", "").replace("{{ open_tracking }}", "")
    parts = body.split(a.card_open)[1:]
    if not parts:
        sys.exit(f"ERROR: no card rows start with {a.card_open!r}; pass --card-open")
    cards = []
    for i, c in enumerate(parts):
        if i == len(parts) - 1:
            c = re.sub(r"<!--\[if mso\]>.*?<!\[endif\]-->", "", c, flags=re.S).rstrip()
            # close the card row, drop the shell/outer closers that follow it
            depth, out = 0, None
            for m in re.finditer(r"<(/?)td\b", c):
                depth += -1 if m.group(1) else 1
                if depth < 0:
                    out = c[: m.start()] + "</td></tr>"
                    break
            if out is None:
                sys.exit("ERROR: could not find the end of the last card")
            c = out.rstrip() + "\n"
        else:
            c = c.rstrip() + "\n"
        cards.append(a.card_open + c)
    out = pathlib.Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for i, card in enumerate(cards, 1):
        (out / f"{i:02d}.html").write_text((head if i == 1 else "") + WRAP.format(card=card), encoding="utf-8")
    print(f"{len(cards)} sections → {out}")


if __name__ == "__main__":
    main()
