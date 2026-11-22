#!/usr/bin/env python3
"""Write self-contained HTML documents of bank sections for Figma's html_to_figma tool.

Each module is one `.mod` element (600px wide on the neutral email canvas), so the tool turns every match into one
Figma frame. Logos are inlined as base64 (the tool does not fetch external URLs); everything else is already inline.

Usage:
    figma_export.py OUT_DIR                # all 282 sections, 12 per document (the tool captures at most 20 matches per call; smaller documents avoid gateway timeouts)
    figma_export.py OUT_DIR ID [ID ...]    # only these section ids, one document

Output: OUT_DIR/batch-NN.html and OUT_DIR/manifest.json (document -> ordered section ids).
"""
import base64
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
BLOCKS = ROOT / "templates/email-blocks"
IMAGES = ROOT / "templates/hsc-v6-emails/images"
FILES = "https://cdn.shopify.com/s/files/1/0276/9115/5508/files/"
CANVAS = "#ededed"
PER_DOC = 12


def data_uri(path):
    """The logo, resized to 2x its display width (256px for the 128px header logo): small documents upload fast."""
    from PIL import Image
    import io
    im = Image.open(path).convert("RGBA")
    im = im.resize((256, round(256 * im.height / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


LOGOS = {FILES + n: data_uri(IMAGES / n) for n in ("hsc-email-logo-ink.png", "hsc-email-logo-bone.png")}


def section_html(sid):
    html = (BLOCKS / sid / "section.html").read_text(encoding="utf-8")
    for url, uri in LOGOS.items():
        html = html.replace(url, uri)
    return html


def document(ids):
    mods = "".join(
        f'<div class="mod" id="{sid}" data-name="{sid}" style="width:600px;background-color:{CANVAS};">{section_html(sid)}</div>'
        for sid in ids)
    return ('<!doctype html><html><head><meta charset="utf-8"><title>Module bank V6</title>'
            f'<style>html,body{{margin:0;padding:0;background:{CANVAS};}}.mod{{display:block;margin:0 0 40px 0;}}</style>'
            f'</head><body>{mods}</body></html>')


def main():
    out = pathlib.Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    ids = sys.argv[2:] or sorted(p.name for p in BLOCKS.glob("mb-*") if p.is_dir())
    batches = [ids[i:i + PER_DOC] for i in range(0, len(ids), PER_DOC)]
    manifest = {}
    for n, batch in enumerate(batches, 1):
        name = f"batch-{n:02d}.html"
        (out / name).write_text(document(batch), encoding="utf-8")
        manifest[name] = batch
    (out / "manifest.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    print(f"{len(ids)} sections -> {len(batches)} documents in {out}")


if __name__ == "__main__":
    main()
