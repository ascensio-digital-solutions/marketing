#!/usr/bin/env python3
"""Minimal Liquid renderer — just enough of Shopify Liquid to render these templates with fixture data.

Supports: {{ }} output with filters, assign, capture, if/elsif/else, unless, for (limit, forloop.first/last/index),
comment, whitespace control (-). Unknown variables or filters raise, so unsupported Liquid is caught, not silently blanked.

Usage: mini_liquid.py FILE.html --fixture ../assets/fixture-order.json [-o OUT.html]
Also importable: mini_liquid.render(src, data). Previews only; Shopify renders the real email.
"""
import re
import datetime as dt

TOKEN = re.compile(r"({%-?.*?-?%}|{{-?.*?-?}})", re.S)


class Blank:
    pass


def tokenize(src):
    parts = TOKEN.split(src)
    toks = []
    for part in parts:
        if not part:
            continue
        if part.startswith("{%") or part.startswith("{{"):
            ltrim = part[2] == "-"
            rtrim = part[-3] == "-"
            inner = part[3 if ltrim else 2: -3 if rtrim else -2].strip()
            kind = "tag" if part.startswith("{%") else "out"
            if ltrim and toks and toks[-1][0] == "text":
                toks[-1] = ("text", toks[-1][1].rstrip())
            toks.append((kind, inner, rtrim))
        else:
            if toks and toks[-1][0] != "text" and len(toks[-1]) == 3 and toks[-1][2]:
                part = part.lstrip()
            toks.append(("text", part))
    return toks


def parse(toks, i=0, stop=()):
    nodes = []
    while i < len(toks):
        t = toks[i]
        if t[0] == "text":
            nodes.append(("text", t[1])); i += 1; continue
        if t[0] == "out":
            nodes.append(("out", t[1])); i += 1; continue
        word = t[1].split(None, 1)[0]
        rest = t[1][len(word):].strip()
        if word in stop:
            return nodes, i
        if word == "comment":
            while not (toks[i][0] == "tag" and toks[i][1].startswith("endcomment")):
                i += 1
            i += 1; continue
        if word in ("if", "unless"):
            branches = []
            cond = rest
            i += 1
            while True:
                body, i = parse(toks, i, ("elsif", "else", "endif", "endunless"))
                branches.append((cond, body))
                w = toks[i][1].split(None, 1)[0]
                if w == "elsif":
                    cond = toks[i][1][5:].strip(); i += 1
                elif w == "else":
                    cond = None; i += 1
                else:
                    i += 1; break
            nodes.append((word, branches)); continue
        if word == "for":
            body, i = parse(toks, i + 1, ("endfor",))
            nodes.append(("for", rest, body)); i += 1; continue
        if word == "capture":
            body, i = parse(toks, i + 1, ("endcapture",))
            nodes.append(("capture", rest, body)); i += 1; continue
        if word == "assign":
            nodes.append(("assign", rest)); i += 1; continue
        raise ValueError(f"unsupported tag: {t[1]}")
    return nodes, i


def split_top(s, sep):
    out, buf, q = [], "", None
    for ch in s:
        if q:
            buf += ch
            if ch == q: q = None
        elif ch in "'\"":
            q = ch; buf += ch
        elif ch == sep:
            out.append(buf); buf = ""
        else:
            buf += ch
    out.append(buf)
    return out


class Ctx:
    def __init__(self, data):
        self.scopes = [dict(data)]

    def get(self, name):
        for s in reversed(self.scopes):
            if name in s:
                return s[name]
        raise KeyError(name)

    def set(self, k, v):
        self.scopes[-1][k] = v


def lookup(ctx, expr):
    expr = expr.strip()
    if expr in ("blank", "empty"):
        return Blank
    if expr == "nil":
        return None
    if expr in ("true", "false"):
        return expr == "true"
    if (expr[0] == expr[-1]) and expr[0] in "'\"":
        return expr[1:-1]
    if re.fullmatch(r"-?\d+", expr):
        return int(expr)
    if re.fullmatch(r"-?\d+\.\d+", expr):
        return float(expr)
    parts = re.findall(r"[^.\[\]]+|\[[^\]]+\]", expr)
    val = ctx.get(parts[0])
    for p in parts[1:]:
        if p.startswith("["):
            key = lookup(ctx, p[1:-1])
        else:
            key = p
        if key == "size" and not (isinstance(val, dict) and "size" in val):
            val = len(val) if val is not None else 0
        elif key == "first" and isinstance(val, list):
            val = val[0] if val else None
        elif key == "last" and isinstance(val, list):
            val = val[-1] if val else None
        elif isinstance(val, dict):
            val = val.get(key)
        elif isinstance(val, list) and isinstance(key, int):
            val = val[key]
        elif val is None:
            return None
        else:
            raise KeyError(f"{expr}: cannot read {key}")
    return val


def is_blank(v):
    return v is None or v == "" or v == [] or v is False


def to_dt(v):
    if isinstance(v, (int, float)):
        return dt.datetime.fromtimestamp(v, dt.timezone.utc)
    if isinstance(v, str) and re.fullmatch(r"\d+", v):
        return dt.datetime.fromtimestamp(int(v), dt.timezone.utc)
    return dt.datetime.fromisoformat(v)


def apply_filter(val, name, args):
    if name == "default":
        return args[0] if is_blank(val) else val
    if name == "plus":
        return num(val) + num(args[0])
    if name == "minus":
        return num(val) - num(args[0])
    if name == "times":
        return num(val) * num(args[0])
    if name == "append":
        return str(val) + str(args[0])
    if name == "first":
        return val[0] if val else None
    if name == "size":
        return len(val) if val is not None else 0
    if name == "money":
        return f"${num(val) / 100:,.2f}"
    if name == "date":
        d = to_dt(val)
        if args[0] == "%s":
            return str(int(d.timestamp()))
        return d.strftime(args[0])
    if name == "escape":
        return str(val).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    raise ValueError(f"unsupported filter: {name}")


def num(v):
    if isinstance(v, (int, float)):
        return v
    return float(v) if "." in str(v) else int(v)


def evaluate(ctx, expr):
    segs = split_top(expr, "|")
    val = lookup(ctx, segs[0])
    for f in segs[1:]:
        f = f.strip()
        if ":" in f:
            name, a = f.split(":", 1)
            args = [lookup(ctx, x) for x in split_top(a, ",")]
        else:
            name, args = f, []
        val = apply_filter(val, name.strip(), args)
    return val


def cond(ctx, c):
    ors = re.split(r"\s+or\s+", c)
    for o in ors:
        if all(cmp(ctx, a) for a in re.split(r"\s+and\s+", o)):
            return True
    return False


def cmp(ctx, c):
    m = re.match(r"(.+?)\s*(==|!=|>=|<=|>|<|\bcontains\b)\s*(.+)", c)
    if not m:
        v = lookup(ctx, c)
        return not (v is None or v is False)
    a, op, b = lookup(ctx, m.group(1)), m.group(2), lookup(ctx, m.group(3))
    if b is Blank:
        return is_blank(a) if op == "==" else not is_blank(a)
    if op == "==": return a == b
    if op == "!=": return a != b
    if op == "contains": return a is not None and b in a
    a, b = num(a or 0), num(b or 0)
    return {">": a > b, "<": a < b, ">=": a >= b, "<=": a <= b}[op]


def run(nodes, ctx):
    out = []
    for n in nodes:
        k = n[0]
        if k == "text":
            out.append(n[1])
        elif k == "out":
            v = evaluate(ctx, n[1])
            out.append("" if v is None else str(v))
        elif k == "assign":
            name, expr = n[1].split("=", 1)
            ctx.set(name.strip(), evaluate(ctx, expr.strip()))
        elif k == "capture":
            ctx.set(n[1].strip(), run(n[2], ctx))
        elif k in ("if", "unless"):
            for c, body in n[1]:
                ok = True if c is None else cond(ctx, c)
                if k == "unless" and c is not None:
                    ok = not ok
                if ok:
                    out.append(run(body, ctx)); break
        elif k == "for":
            m = re.match(r"(\w+)\s+in\s+(\S+)(?:\s+limit:\s*(\d+))?", n[1])
            items = lookup(ctx, m.group(2)) or []
            if m.group(3):
                items = items[: int(m.group(3))]
            for idx, it in enumerate(items):
                ctx.scopes.append({m.group(1): it, "forloop": {"first": idx == 0, "last": idx == len(items) - 1, "index": idx + 1}})
                out.append(run(n[2], ctx))
                ctx.scopes.pop()
    return "".join(out)


def render(src, data):
    nodes, _ = parse(tokenize(src))
    return run(nodes, Ctx(data))


def main():
    import argparse, json, sys
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--fixture", required=True, help="JSON context (fictional data only)")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()
    try:
        html = render(open(a.file, encoding="utf-8").read(), json.load(open(a.fixture)))
    except Exception as e:
        sys.exit(f"ERROR: {e}")
    if a.out:
        open(a.out, "w", encoding="utf-8").write(html)
        print(f"rendered {a.file} -> {a.out} ({len(html)} chars)")
    else:
        sys.stdout.write(html)


if __name__ == "__main__":
    main()
