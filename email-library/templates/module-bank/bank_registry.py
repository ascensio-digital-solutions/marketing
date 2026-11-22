"""Module registry shared by the category files (cat_01.py ... cat_08.py)."""
MODULES = {}


def module(source, name, type_, copy, adaptations, notes=""):
    """Register a module function. `source` is the Figma row name, `name` the bank name (renamed when the
    Figma name described a colour). `copy` is the Figma sample copy, kept for reference only."""
    def deco(fn):
        MODULES[source] = dict(fn=fn, name=name, type=type_, copy=copy, adaptations=adaptations, notes=notes)
        return fn
    return deco
