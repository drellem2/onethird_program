"""The primitivity PREDICATE, as ten trees compute it — carried verbatim from x3's V4.

THE LARGEST ALIAS IN THE CORPUS IS NOT A SCALAR.  mg-0d1b's V4 found ten trees carrying
ten names for one BOOLEAN (`is_primitive` / `primitive` / `not decomposable`), agreeing at
all 404 posets, and said why that row matters more than any float row: it defines the
population every published `6 of 275` is stated over.  A sweep looking for computed NUMBER
columns would never have found it, and an index that found it has still never gated it.

WHY THIS TABLE IS COPIED AND NOT IMPORTED.  It lives inline in `x3_values.py`, which is a
90 s script that also rewrites `alias_groups.json` — the file this gate's baseline is
derived from.  A merge gate that imported it would run the discovery instrument on every
merge and let it overwrite its own input.  The table is therefore carried here, and
`g2_predicate.py` checks the carried copy against the committed record: if x3's ten trees
and this file's ten trees ever stop being the same ten, that is RED, not a silent drift
between two lists nobody compares.  (Which is, precisely, this ticket's subject.)

NOTHING IS RENAMED.  Each entry's label is `tree:symbol` exactly as the tree spells it,
because the names are load-bearing in their own threads and are cited by transcripts.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "alias_index_0d1b"))

import lib0d1b as L                                                  # noqa: E402


def build():
    """[(label, fn(dn, n) -> bool)] — one entry per tree, in x3 V4's order."""
    _28 = L.load("l2_conditionality_28ff/lib28ff.py", "z28ff")
    _29 = L.load("l2_audit_29fe/lib29fe.py", "z29fe")
    _3b = L.load("l2_underclaim_audit_3bb9/lib3bb9.py", "z3bb9")
    _78 = L.load("lstar_789d/lib789d.py", "z789d")
    _5c = L.load("audit_5cba/lib5cba.py", "z5cba")
    _c5 = L.load("anticorrelation_c50b/libc50b.py", "zc50b")
    _51 = L.load("sweep_loss_51f4/lib51f4.py", "z51f4")
    _76 = L.load("c3_prefix_capture_76b2/lib76b2.py", "z76b2")
    _a9 = L.load("c3_audit_a94c3/libA94.py", "za94c3")
    _81 = L.load("chain_iv_c_81ff/lib81ff.py", "z81ff")

    return [
        ("l2_conditionality_28ff:is_primitive",
         lambda dn, n: _28.Poset(n, L.dn_to_rel(dn, n)).is_primitive()),
        ("l2_audit_29fe:not decomposable",
         lambda dn, n: not _29.Poset(n, L.dn_to_rel(dn, n)).decomposable),
        ("l2_underclaim_audit_3bb9:not decomposable()",
         lambda dn, n: not _3b.P3bb9(n, L.dn_to_rel(dn, n)).decomposable()),
        ("lstar_789d:primitive", lambda dn, n: _78.P789(dn, n).primitive()),
        ("audit_5cba:primitive", lambda dn, n: _5c.P5(dn, n).primitive()),
        ("anticorrelation_c50b:primitive", lambda dn, n: _c5.Poset(dn, n).primitive()),
        ("sweep_loss_51f4:is_primitive",
         lambda dn, n: _51.Pos(n, L.dn_to_rel(dn, n)).is_primitive()),
        ("c3_prefix_capture_76b2:is_primitive",
         lambda dn, n: _76.Poset(n, L.dn_to_rel(dn, n)).is_primitive()),
        ("c3_audit_a94c3:is_primitive",
         lambda dn, n: _a9.is_primitive(n, L.dn_to_rel(dn, n))),
        ("chain_iv_c_81ff:is_primitive",
         lambda dn, n: _81.Poset(n, list(dn)).is_primitive()),
    ]


def vectors(pop):
    """{label: [bool per poset]}, plus lib0d1b's own population predicate.

    `bool()` is applied deliberately and is itself a hazard the caller must handle: a
    predicate that started returning a non-empty list instead of True would coerce to
    True at every poset and go on agreeing.  `g2_predicate.py` records the returned TYPE
    for that reason — an equality check on a boolean can pass for reasons a float check
    would not, and coercion is the first of them.
    """
    out, types = {}, {}
    for label, fn in build():
        raw = [fn(dn, n) for (n, dn) in pop]
        out[label] = [bool(v) for v in raw]
        types[label] = sorted({type(v).__name__ for v in raw})
    out["lib0d1b:primitive_here"] = [bool(L.primitive_here(dn, n)) for (n, dn) in pop]
    types["lib0d1b:primitive_here"] = ["bool"]
    return out, types
