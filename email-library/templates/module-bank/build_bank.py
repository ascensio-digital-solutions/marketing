#!/usr/bin/env python3
"""Generate the HSC email module bank: every module in three real themes (Bone, Ink, White).

Source of the module list: Figma page "Modules Library + Hubspot Source" (now only in the snapshot file a01FHSyLdgi6ppzaThHl2B),
frame "Email module library — organized by function" (489:7305). `modules.tsv` holds the 94 definitions
with the Figma module node of each theme cell. Each implemented module is one function below,
`fn(theme) -> card rows`, rebuilt to the v6 email design system (see v6_html.py).

Output: templates/email-blocks/mb-<NN>-<slug>-<theme>/{section.html, section.json}. These folders are
generated: change the module function here, never the files. The gallery, READMEs and previews are
produced afterwards by .claude/skills/shopify-email-html/scripts/build_library.py.

Usage:
    python3 templates/module-bank/build_bank.py            # write the folders
    python3 templates/module-bank/build_bank.py --check    # fail if any generated file is stale or a module lacks a theme
    python3 templates/module-bank/build_bank.py --status   # coverage report (implemented / total per category)
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude/skills/shopify-email-html/scripts"))
import v6_html as V  # noqa: E402
from v6_html import section  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bank_registry import MODULES  # noqa: E402
for _f in sorted(Path(__file__).resolve().parent.glob("cat_*.py")):
    __import__(_f.stem)

BLOCKS = ROOT / "templates/email-blocks"
THEME_ORDER = ["bone", "ink", "white"]
CATEGORIES = {"01": "Global chrome", "02": "Heroes", "03": "Titles & editorial", "04": "Products & commerce",
              "05": "Services & proof", "06": "CTAs & promotions", "07": "Transactional lifecycle", "08": "Utility"}
FIGMA_FILE = "https://www.figma.com/design/9Il504CQE8jLaUTBVzphqc/Email-Design-System?node-id="


def slugify(s):
    s = s.lower().replace("·", " ").replace("&", " and ").replace("+", " plus ")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def load_index():
    rows = []
    for line in (Path(__file__).parent / "modules.tsv").read_text(encoding="utf-8").splitlines():
        cat, src, ids = line.split("|")
        rows.append({"cat": cat, "source": src, "figma": dict(zip(THEME_ORDER, ids.split(",")))})
    return rows


# ---------------------------------------------------------------- generation
def generate():
    """Return {relative path: text} for every implemented module in every theme."""
    files, index = {}, load_index()
    seen = set()
    for row in index:
        spec = MODULES.get(row["source"])
        if not spec:
            continue
        seen.add(row["source"])
        slug = slugify(spec["name"])
        for t in THEME_ORDER:
            th = V.THEMES[t]
            sid = f"mb-{row['cat']}-{slug}-{t}"
            html = section(spec["fn"](th))
            meta_ = {
                "name": f"{spec['name']} · {th['label']}",
                "type": spec["type"],
                "context": "any",
                "surfaces": ["messaging-code-your-own", "messaging-section"],
                "liquid_variables": [],
                "placeholders": True,
                "notes": ("Module bank. All copy is a labelled slot: replace it before use. " + spec["notes"]).strip(),
                "bank": {
                    "category": f"{row['cat']} · {CATEGORIES[row['cat']]}",
                    "module": spec["name"],
                    "theme": t,
                    "figma_source": row["source"],
                    "figma_node": FIGMA_FILE + row["figma"][t].replace(":", "-"),
                    "sample_copy": spec["copy"],
                    "adaptations": spec["adaptations"],
                },
            }
            files[f"templates/email-blocks/{sid}/section.html"] = html
            files[f"templates/email-blocks/{sid}/section.json"] = json.dumps(meta_, indent=2, ensure_ascii=False) + "\n"
    unknown = set(MODULES) - seen
    if unknown:
        raise SystemExit(f"modules without a row in modules.tsv: {sorted(unknown)}")
    return files


def status():
    index = load_index()
    by_cat = {}
    for r in index:
        c = by_cat.setdefault(r["cat"], [0, 0])
        c[1] += 1
        c[0] += r["source"] in MODULES
    for cat, (done, total) in sorted(by_cat.items()):
        print(f"{cat} · {CATEGORIES[cat]:<26} {done:>2}/{total:<2}")
    done = sum(v[0] for v in by_cat.values())
    total = sum(v[1] for v in by_cat.values())
    print(f"{'total':<31} {done:>2}/{total:<2}  ({done * 3} of {total * 3} sections)")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "--status":
        return status()
    files = generate()
    if mode == "--check":
        stale = []
        for rel, text in files.items():
            p = ROOT / rel
            if not p.exists() or p.read_text(encoding="utf-8") != text:
                stale.append(rel)
        existing = {str(p.relative_to(ROOT)) for d in BLOCKS.glob("mb-*") for p in d.iterdir()
                    if p.name in ("section.html", "section.json")}
        orphans = sorted(existing - set(files))
        if stale or orphans:
            print("STALE:", *stale, *["ORPHAN: " + o for o in orphans], sep="\n  ")
            raise SystemExit(1)
        print(f"ok: {len(files) // 2} bank sections up to date")
        return
    for rel, text in files.items():
        p = ROOT / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    keep = {Path(rel).parent.name for rel in files}
    for d in BLOCKS.glob("mb-*"):  # bank folders are generated: drop the ones no module produces any more
        if d.is_dir() and d.name not in keep:
            shutil.rmtree(d)
            print("removed orphan", d.name)
    print(f"wrote {len(files) // 2} sections")
    status()


if __name__ == "__main__":
    main()
