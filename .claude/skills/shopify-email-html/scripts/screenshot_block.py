#!/usr/bin/env python3
"""Render a block or a whole email with fixture data and save a trimmed 2x PNG (1200px wide).

Usage:
  screenshot_block.py FILE.html -o OUT.png [--head HEAD.html] [--prefix LIQUID.html]
                      [--fixture assets/fixture-order.json] [--full]

FILE is a bank block (card fragment) or, with --full, a complete email document.
--head      the "Email head" block (fonts + <style>) so a lone card renders with its real styles.
--prefix    Liquid prepended before rendering (e.g. the PP-1 "Liquid header" block).
--fixture   JSON context for Liquid; fictional data only (see assets/fixture-*.json).
Liquid is rendered with mini_liquid.py from this folder (previews only).
Needs Google Chrome and Pillow (pip install pillow, in a venv if the system Python is managed).
Every screenshot is rendered in a 600px column at 2x, so all images share one width.
"""
import argparse
import json
import os
import pathlib
import subprocess
import sys
import tempfile

CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
BG = (237, 237, 237)  # neutral canvas, trimmed away afterwards


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--head")
    ap.add_argument("--prefix")
    ap.add_argument("--fixture")
    ap.add_argument("--full", action="store_true", help="FILE is a complete document")
    a = ap.parse_args()
    try:
        from PIL import Image, ImageChops
    except ImportError:
        sys.exit("ERROR: Pillow is missing; create a venv and `pip install pillow`, then rerun with its python")
    if not pathlib.Path(CHROME).exists():
        sys.exit(f"ERROR: Chrome not found at {CHROME}; set CHROME=/path/to/chrome")
    try:
        src = pathlib.Path(a.file).read_text(encoding="utf-8")
        prefix = pathlib.Path(a.prefix).read_text(encoding="utf-8") if a.prefix else ""
        head = pathlib.Path(a.head).read_text(encoding="utf-8") if a.head else ""
        data = json.loads(pathlib.Path(a.fixture).read_text()) if a.fixture else {}
    except (OSError, json.JSONDecodeError) as e:
        sys.exit(f"ERROR: {e}")
    if "{{" in prefix + src or "{%" in prefix + src:
        sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
        import mini_liquid
        try:
            html = mini_liquid.render(prefix + src, data)
        except Exception as e:  # unknown variable/filter: the fixture is missing a field
            sys.exit(f"ERROR: Liquid render failed ({e}); add the missing field to the fixture")
    else:
        html = src
    canvas = f"html,body{{background:rgb{BG} !important;margin:0;}} body{{padding:24px !important;}}"
    if a.full:
        page = html.replace("</head>", f"<style>{canvas}</style></head>", 1)
    else:
        page = (f'<!doctype html><html><head><meta charset="utf-8">{head}<style>{canvas}</style></head>'
                f'<body><div style="width:600px">{html}</div></body></html>')
    out = pathlib.Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as t:
        t.write(page)
    try:
        subprocess.run([CHROME, "--headless=new", "--hide-scrollbars", "--force-device-scale-factor=2",
                        "--window-size=648,6000", "--virtual-time-budget=8000", f"--screenshot={out.resolve()}",
                        pathlib.Path(t.name).as_uri()], check=True, capture_output=True, timeout=120)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        sys.exit(f"ERROR: Chrome screenshot failed: {e}")
    finally:
        os.unlink(t.name)
    im = Image.open(out).convert("RGB")
    bbox = ImageChops.difference(im, Image.new("RGB", im.size, BG)).getbbox()
    if not bbox:
        sys.exit("ERROR: empty render (nothing drawn); check the HTML and fixture")
    im.crop(bbox).save(out)
    w, h = Image.open(out).size
    print(f"{out} {w}x{h}")
    if w != 1200:
        print(f"WARN: width {w}px, expected 1200px; a card is narrower/wider than the 600px column", file=sys.stderr)


if __name__ == "__main__":
    main()
