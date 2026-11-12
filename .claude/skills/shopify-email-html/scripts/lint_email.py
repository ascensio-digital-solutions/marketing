#!/usr/bin/env python3
"""Lint an HTML email before installing it in Shopify.

Usage: lint_email.py FILE [FILE ...] --mode notification|section|code-your-own

Prints ERROR/WARN lines per file; exits 1 if any ERROR was found.
Design rules enforced: rounded cards (no coloured table without border-radius), no gap between
cards (card rows padding:0), transparent <body> and outer wrapper, radius tokens 12/8/999.
"""
import argparse
import re
import sys

PAIRS = [("if", "endif"), ("for", "endfor"), ("unless", "endunless"), ("capture", "endcapture"),
         ("case", "endcase"), ("comment", "endcomment")]


def lint(text, mode):
    errors, warns = [], []
    for open_tag, close_tag in PAIRS:
        o = len(re.findall(r"\{%-?\s*" + open_tag + r"\b", text))
        c = len(re.findall(r"\{%-?\s*" + close_tag + r"\b", text))
        if o != c:
            errors.append(f"unbalanced Liquid {open_tag}/{close_tag}: {o} vs {c}")
    for tag in ("table", "tr", "td"):
        o = len(re.findall(r"<%s[\s>]" % tag, text))
        c = len(re.findall(r"</%s>" % tag, text))
        if o != c:
            errors.append(f"unbalanced <{tag}>: {o} open vs {c} close")
    if mode == "code-your-own":
        for req in ("{{ unsubscribe_link }}", "{{ open_tracking_block }}"):
            if req not in text:
                errors.append(f"Code your own requires {req}")
    if mode in ("section", "code-your-own") and "{{ open_tracking }}" in text:
        errors.append("{{ open_tracking }} is not a Messaging tag; use {{ open_tracking_block }} (Code your own) or remove it (sections)")
    if mode == "section" and "{{ open_tracking_block }}" in text:
        warns.append("open_tracking_block inside a section is redundant; Shopify tracks opens itself")
    if mode == "section" and re.search(r"<!DOCTYPE|<html|<body", text, re.I):
        errors.append("section fragments must not contain <!DOCTYPE>, <html> or <body>")
    if re.search(r"padding:\s*0 0 2px 0", text):
        errors.append("card spacer padding:0 0 2px 0 found; cards stack with no gap")
    for m in re.finditer(r"<td style=\"padding:([^\"]+)\">\s*<table\b[^>]*border-radius:\s*(?:1\d|[2-9]\d)px", text):
        if m.group(1).strip().rstrip(";") != "0":
            errors.append(f"card row padding:{m.group(1)} leaves a gap; card rows are <td style=\"padding:0;\">")
            break
    body = re.search(r"<body\b[^>]*>", text, re.I)
    outer = re.search(r"<table\b[^>]*>", text[body.end():] if body else text)
    for label, tag in (("<body>", body), ("outer wrapper table", outer)):
        if tag and re.search(r"background(?:-color)?:\s*(?!transparent)[#a-z(]|bgcolor=", tag.group(0), re.I):
            errors.append(f"{label} paints a background; it must be transparent (colour only on cards/insets)")
    for m in re.finditer(r"<table\b[^>]*style=\"([^\"]*)\"", text):
        st = m.group(1)
        if re.search(r"background(?:-color)?:\s*(?!transparent)[#a-z(]", st, re.I) and "border-radius" not in st:
            errors.append("coloured table without border-radius (square card); cards 12px, insets 8px")
            break
    for m in re.finditer(r"<td[^>]*style=\"[^\"]*border-radius:999px[^\"]*border:\s*1px[^\"]*\"", text):
        errors.append("outlined button border is on the <td>; move it to the <a> (Messaging collapses table borders)")
        break
    for r in set(re.findall(r"border-radius:\s*(\d+)px", text)):
        if r not in {"12", "8", "999", "0"}:
            warns.append(f"border-radius {r}px is off-token (cards 12, insets 8, pills 999)")
    if "variant_title" in text and "Default Title" not in text:
        warns.append("variant_title used without a 'Default Title' guard")
    if re.search(r"\[[A-Z][^\]]{2,60}\]", re.sub(r"<[^>]+>", "", text)):
        warns.append("bracketed placeholder text found (e.g. [Name]); confirm before shipping")
    if mode != "notification" and 'style="display:none' in text:
        warns.append("hidden preheader present; Messaging's Preview text field will duplicate it")
    for src in re.findall(r"<img[^>]+src=\"([^\"]+)\"", text):
        if src.startswith("http") and "cdn.shopify.com" not in src:
            warns.append(f"image not on Shopify Files CDN: {src}")
    return errors, warns


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--mode", required=True, choices=["notification", "section", "code-your-own"])
    a = ap.parse_args()
    failed = False
    for f in a.files:
        try:
            text = open(f, encoding="utf-8").read()
        except OSError as e:
            print(f"ERROR {f}: {e}", file=sys.stderr)
            failed = True
            continue
        errors, warns = lint(text, a.mode)
        for e in errors:
            print(f"ERROR {f}: {e}", file=sys.stderr)
        for w in warns:
            print(f"WARN  {f}: {w}")
        if not errors:
            print(f"OK    {f} ({len(warns)} warnings)")
        failed |= bool(errors)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
