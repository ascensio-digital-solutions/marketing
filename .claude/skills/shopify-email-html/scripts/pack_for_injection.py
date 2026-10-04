#!/usr/bin/env python3
"""Print a JavaScript snippet that replaces a Shopify notification template's code in place.

Usage: pack_for_injection.py FILE [--out SNIPPET.js]

Run the printed snippet in the admin page at /email_templates/<template>/edit (same-origin
CodeMirror 6). It returns {hash, match}; hash must equal the prefix printed to stderr here.
The payload is gzip+base64, so a 20 KB template is ~5 KB of snippet.
"""
import argparse
import base64
import gzip
import hashlib
import pathlib
import sys

JS = """const b64="{b64}";
const bytes=Uint8Array.from(atob(b64),c=>c.charCodeAt(0));
const text=await new Response(new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'))).text();
const h=[...new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(text)))].map(b=>b.toString(16).padStart(2,'0')).join('').slice(0,16);
const v=document.querySelector('.cm-content').cmView.view;
v.dispatch({{changes:{{from:0,to:v.state.doc.length,insert:text}},userEvent:'input.paste'}});
({{hash:h,match:v.state.doc.toString()===text}})"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--out")
    a = ap.parse_args()
    try:
        raw = pathlib.Path(a.file).read_bytes()
    except OSError as e:
        sys.exit(f"ERROR: {e}")
    snippet = JS.format(b64=base64.b64encode(gzip.compress(raw, 9)).decode())
    print(f"expected hash prefix: {hashlib.sha256(raw).hexdigest()[:16]}  ({len(raw)} bytes → {len(snippet)} chars)", file=sys.stderr)
    if a.out:
        pathlib.Path(a.out).write_text(snippet)
        print(a.out)
    else:
        print(snippet)


if __name__ == "__main__":
    main()
