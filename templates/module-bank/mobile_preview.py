#!/usr/bin/env python3
"""Render bank sections in a 375px mobile viewport (the email head's max-width:480px rules apply).

Usage: mobile_preview.py OUT.png SECTION_ID [SECTION_ID ...]
Stacks the given sections in one 375px column at 2x, on the neutral canvas, using the shared email head.
Needs Google Chrome and Pillow (run with a venv python).
"""
import os, pathlib, subprocess, sys, tempfile
from PIL import Image, ImageChops

ROOT = pathlib.Path(__file__).resolve().parents[2]
CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
BG = (237, 237, 237)


def main():
    out, ids = pathlib.Path(sys.argv[1]), sys.argv[2:]
    head = (ROOT / "templates/email-blocks/00-email-head-fonts-styles/section.html").read_text(encoding="utf-8")
    body = "".join((ROOT / f"templates/email-blocks/{i}/section.html").read_text(encoding="utf-8") for i in ids)
    page = (f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=375">{head}'
            f'<style>html,body{{background:rgb{BG} !important;margin:0;padding:0 !important;}}</style></head>'
            f'<body><div style="width:375px">{body}</div></body></html>')
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as t:
        t.write(page)
    try:
        subprocess.run([CHROME, "--headless=new", "--hide-scrollbars", "--force-device-scale-factor=2",
                        "--window-size=375,6000", "--virtual-time-budget=8000", f"--screenshot={out.resolve()}",
                        pathlib.Path(t.name).as_uri()], check=True, capture_output=True, timeout=120)
    finally:
        os.unlink(t.name)
    im = Image.open(out).convert("RGB")
    bbox = ImageChops.difference(im, Image.new("RGB", im.size, BG)).getbbox()
    im.crop(bbox).save(out)
    print(out, Image.open(out).size)


if __name__ == "__main__":
    main()
