#!/usr/bin/env python3
"""Assemble a Shopify email from an ordered list of block files.

Usage:
  assemble_email.py --mode code-your-own|notification BLOCK.html [BLOCK.html ...] -o OUT.html [--title T]
  assemble_email.py --mode sections BLOCK.html [BLOCK.html ...] -o OUT_DIR

To rebuild every template in templates/emails/ from its recipe, use build_library.py instead.
Blocks are the library's section files (templates/email-blocks/*/section.html) (each a fluid 600px shell with one card, padding:0 wrapper, no gap).
Pass the "Email head" block (fonts + <style>) first; a "Liquid header" block (Liquid assigns only)
may come before it. Modes:
  code-your-own  full document for Shopify Messaging "Code your own"; appends {{ open_tracking_block }}
                 and fails unless a block contains {{ unsubscribe_link }}.
  notification   full document for a Settings → Notifications template (Liquid header kept on top).
  sections       one file per Messaging Custom Liquid section; the head is merged into section 01.
"""
import argparse
import html
import pathlib
import re
import sys

DOC = """{liquid}<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="x-apple-disable-message-reformatting">
<meta name="color-scheme" content="light">
<meta name="supported-color-schemes" content="light">
<title>{title}</title>
<!--[if mso]><noscript><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml></noscript><![endif]-->
{head}
</head>
<body style="margin:0;padding:0;background-color:transparent;">
{preheader}<!--[if mso]><table role="presentation" width="600" align="center" cellpadding="0" cellspacing="0" border="0"><tr><td><![endif]-->
{body}<!--[if mso]></td></tr></table><![endif]-->
{tracking}
</body>
</html>
"""


def classify(text):
    if re.search(r"<style>|fonts\.googleapis", text) and "<table" not in text:
        return "head"
    if "<table" not in text and "{%" in text:
        return "liquid"
    return "block"


class AssemblyError(Exception):
    pass


PREHEADER = ('<div style="display:none;max-height:0;max-width:0;overflow:hidden;opacity:0;mso-hide:all;'
             'font-size:1px;line-height:1px;color:#ffffff;">{text}' + "&zwnj;&nbsp;" * 40 + "</div>\n")


def build(mode, texts, title="", preheader=""):
    """Return the full document (str) or, for mode "sections", a list of section strings.

    preheader: inbox preview text, written as a hidden div in notification mode only
    (Messaging has its own Preview text field; both together duplicate the snippet).
    """
    liquid, head, body = [], [], []
    for t in texts:
        {"head": head, "liquid": liquid, "block": body}[classify(t)].append(t.strip() + "\n")
    if not head:
        raise AssemblyError("no Email head block (fonts + <style>) in the list; pass it first")
    if not body:
        raise AssemblyError("no card blocks in the list")
    if mode == "sections":
        if liquid:
            raise AssemblyError("Liquid header blocks belong to notification templates, not Messaging sections")
        return [("".join(head) if i == 0 else "") + b for i, b in enumerate(body)]
    joined = "".join(body)
    if mode == "code-your-own" and "{{ unsubscribe_link }}" not in joined:
        raise AssemblyError("code-your-own needs a block containing {{ unsubscribe_link }} (the Messaging preferences footer)")
    pre = PREHEADER.format(text=html.escape(preheader, quote=False)) if mode == "notification" and preheader else ""
    return DOC.format(liquid="".join(liquid), title=html.escape(title), head="".join(head).strip(), body=joined, preheader=pre,
                      tracking="{{ open_tracking_block }}\n" if mode == "code-your-own" else "")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mode", required=True, choices=["code-your-own", "notification", "sections"])
    ap.add_argument("blocks", nargs="+")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--title", default="")
    ap.add_argument("--preheader", default="", help="inbox preview text (notification mode only)")
    a = ap.parse_args()
    try:
        texts = [pathlib.Path(p).read_text(encoding="utf-8") for p in a.blocks]
        result = build(a.mode, texts, a.title, a.preheader)
    except (OSError, AssemblyError) as e:
        sys.exit(f"ERROR: {e}")
    out = pathlib.Path(a.out)
    if a.mode == "sections":
        out.mkdir(parents=True, exist_ok=True)
        for i, sec in enumerate(result, 1):
            (out / f"{i:02d}.html").write_text(sec, encoding="utf-8")
        print(f"{len(result)} sections → {out}")
        return
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(result, encoding="utf-8")
    print(f"{a.mode}: {len(texts)} blocks → {out} ({len(result)} chars)")


if __name__ == "__main__":
    main()
