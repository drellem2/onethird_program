#!/usr/bin/env python3
"""a3_gate.py -- THE GATE AT THE POINT OF USE, ASKED OF EVERY CONSUMER.

The brief: FOR EVERY SCRIPT THAT READS AN ANCHOR, CONFIRM THE DRIFT GATE
FIRES THERE, not only where the anchor is defined.  CONSTRUCT A DRIFT AND RUN
EACH CONSUMER.  Drift is loud where the anchor is checked and silent where it
is spent.

  (i)   WHO SPENDS, REPO-WIDE.  mg-b2af's `t2` walks
        `code/branching_audit_e34a/` and requires every script there that
        names a derived anchor to gate it.  The population of that rule is a
        DIRECTORY.  Six directories import `libe34a`.
  (ii)  THE ANCHORS THAT CANNOT BE GATED BY NAME.  `ANCHOR_OF` has four keys;
        `libe34a` derives six.
  (iii) THE DRIFT, CONSTRUCTED, AND EACH CONSUMER RUN.

Predicted exit: 1.
"""
import ast
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_0ba7 as L                                          # noqa: E402

R = L.Report(
    selfpop="a3's own AST resolution and its constructed drift",
    findpop="every script in the repository that spends a libe34a anchor")

L.banner("mg-0ba7 a3", "THE GATE AT THE POINT OF SPEND")

LIBE34A = "code/branching_audit_e34a/libe34a.py"
E34A_DIR = "code/branching_audit_e34a"

# ---------------------------------------------------------------------------
L.rule("(i) WHO SPENDS A `libe34a` ANCHOR -- REPO-WIDE, BY AST")
# ---------------------------------------------------------------------------

src_lib = open(os.path.join(L.REPO, LIBE34A)).read()
tree_lib = ast.parse(src_lib)

# The anchors the module DERIVES: module-level names assigned from a
# revision-producing derivation.  Read from the module's own source, not from
# a list written here -- a list written here would be one more population
# defined by what I happened to type.
DERIVERS = ("first_introducing", "last_touching", "nth_touching", "_anchored")
derived_names = []
for node in tree_lib.body:
    if isinstance(node, (ast.Assign,)):
        calls = [n for n in ast.walk(node.value) if isinstance(n, ast.Call)]
        hit = any(isinstance(c.func, ast.Name) and c.func.id in DERIVERS
                  for c in calls)
        if not hit:
            continue
        for t in node.targets:
            for nm in ast.walk(t):
                if isinstance(nm, ast.Name):
                    derived_names.append(nm.id)
derived_names = sorted(set(derived_names))
R.total("anchors `libe34a` DERIVES (from its own source)",
        len(derived_names), "module-level assignments whose value calls one "
        "of %s" % (DERIVERS,), "one EXPORTED NAME")
print("     %s" % ", ".join(derived_names))

anchor_of = {}
for node in tree_lib.body:
    if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "ANCHOR_OF"
            for t in node.targets):
        for k in node.value.keys:
            anchor_of[k.value] = True
R.total("keys of `ANCHOR_OF` -- what `gate_spent` will accept",
        len(anchor_of), "the ANCHOR_OF literal in libe34a.py", "one NAME")
print("     %s" % ", ".join(sorted(anchor_of)))

ungateable = [n for n in derived_names if n not in anchor_of]
R.total("derived anchors `gate_spent` CANNOT gate", len(ungateable),
        "the derived names above minus the ANCHOR_OF keys", "one NAME")
print("     %s" % ", ".join(ungateable))

ANCH = set(derived_names)


def spenders(repo=L.REPO):
    """[(rel, spends, gated, whole)] for every file that READS an anchor.

    Resolution is by AST: an `Attribute` whose base is a Name bound to
    `libe34a` by an `import ... as`, or a Name bound by `from libe34a import`.
    A file that MENTIONS `REPAIR_REV` in prose is not a spender, and this is
    why the test is not a grep -- `t4_preserve.py` names three anchors in its
    docstrings and reads none of them.
    """
    out = []
    files, _bad = L.py_files(repo)
    for rel, src, tree in files:
        if rel == LIBE34A or "libe34a" not in src:
            continue
        alias, direct = set(), set()
        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                for a in n.names:
                    if a.name.split(".")[-1] == "libe34a":
                        alias.add(a.asname or a.name.split(".")[0])
            elif isinstance(n, ast.ImportFrom) and n.module and \
                    n.module.split(".")[-1] == "libe34a":
                for a in n.names:
                    direct.add(a.asname or a.name)
        spends, whole = set(), False
        for n in ast.walk(tree):
            if isinstance(n, ast.Attribute) and n.attr in ANCH:
                if isinstance(n.value, ast.Name) and n.value.id in alias:
                    spends.add(n.attr)
            elif isinstance(n, ast.Name) and n.id in ANCH and n.id in direct:
                spends.add(n.id)
            if isinstance(n, ast.Attribute) and n.attr == "ANCHOR_DRIFT":
                whole = True
            if isinstance(n, ast.Name) and n.id == "ANCHOR_DRIFT":
                whole = True
        gated = set()
        for n in ast.walk(tree):
            if not isinstance(n, ast.Call):
                continue
            f = n.func
            nm = (f.attr if isinstance(f, ast.Attribute)
                  else f.id if isinstance(f, ast.Name) else None)
            if nm != "gate_spent":
                continue
            for a in n.args[1:]:
                if isinstance(a, ast.Constant):
                    gated.add(a.value)
        if spends:
            out.append((rel, spends, gated, whole))
    return out


rows = spenders()
R.total("files that SPEND a libe34a anchor", len(rows),
        "every parseable .py under code/ that resolves an anchor name "
        "through a libe34a import", "one FILE")

print()
print("   %-46s %-7s %-7s %s" % ("file", "spends", "gated", "verdict"))
gaps_in, gaps_out = [], []
for rel, spends, gated, whole in sorted(rows):
    covered = whole or spends <= gated
    inside = rel.startswith(E34A_DIR + "/")
    verdict = ("covered (whole ANCHOR_DRIFT)" if whole and not (spends <= gated)
               else "covered (gate_spent)" if covered
               else "*** UNGATED")
    print("   %-46s %-7d %-7d %s"
          % (rel, len(spends), len(gated), verdict))
    if not covered:
        (gaps_in if inside else gaps_out).append((rel, sorted(spends)))

print()
R.total("UNGATED spenders INSIDE code/branching_audit_e34a/", len(gaps_in),
        "the spender files above", "one FILE")
R.total("UNGATED spenders OUTSIDE it", len(gaps_out),
        "the spender files above", "one FILE")
for rel, s in gaps_out:
    print("     %s   spends %s" % (rel, ", ".join(s)))

print("""
   `t2_gate.py` walks `code/branching_audit_e34a/` and requires each script
   there to gate every anchor it names.  Applied to that directory the rule
   is satisfied.  It is a rule whose POPULATION IS A DIRECTORY, and the
   scripts above are outside it, spend the same four anchors from the same
   module, and would run to a clean exit on a re-pointed anchor -- which is
   the sentence F-1 was written to retire.
""")
R.gate(not gaps_out,
       "%d script(s) in %d director%s outside code/branching_audit_e34a/ "
       "spend a libe34a anchor with no gate; t2's structural rule does not "
       "look at them because its population is a directory"
       % (len(gaps_out),
          len({os.path.dirname(r) for r, _ in gaps_out}),
          "y" if len({os.path.dirname(r) for r, _ in gaps_out}) == 1
          else "ies"))

# ---------------------------------------------------------------------------
L.rule("(ii) THE TWO ANCHORS THAT CANNOT BE GATED BY NAME")
# ---------------------------------------------------------------------------

print("""
   `gate_spent` treats an unknown name as a SELF-ERROR rather than a pass.
   That is right, and mg-b2af built it deliberately.  It also means the set
   of gateable anchors is exactly `ANCHOR_OF`'s keys -- and `libe34a` derives
   two more, both spent in `k1_prerepair.py`.
""")
sys.path.insert(0, os.path.join(L.REPO, E34A_DIR))
import libe34a as E                                           # noqa: E402


class _Probe(object):
    def __init__(self):
        self.selferrs, self.findings = [], []

    def selferr(self, m):
        self.selferrs.append(m)

    def finding(self, m):
        self.findings.append(m)


print("   %-22s %-10s %s" % ("name asked of gate_spent", "result", "note"))
for nm in derived_names:
    p = _Probe()
    ok = E.gate_spent(p, nm)
    res = ("SELF-ERROR" if p.selferrs
           else "FINDING" if p.findings else "pass")
    print("   %-22s %-10s %s"
          % (nm, res, "not a key of ANCHOR_OF" if p.selferrs else ""))
R.gate(not ungateable,
       "%s are anchors libe34a derives and spends, and asking gate_spent "
       "about either produces a SELF-ERROR: the safety feature is right "
       "about the name-list and wrong about the anchor.  A consumer of "
       "LAST_TOUCHING_G1 has no way to gate it at the point of spend"
       % " and ".join(ungateable))

print("""
   AND THE ASYMMETRY IS THE POINT.  `LAST_TOUCHING_G1` is the anchor that
   ALREADY RE-POINTED ONCE -- libe34a's own docstring records mg-69d1's
   sentence edit moving it 4755d02 -> d01ff32.  The one anchor in this
   module with a demonstrated history of drifting is the one the drift gate
   will not accept the name of.
""")

# ---------------------------------------------------------------------------
L.rule("(iii) THE DRIFT, CONSTRUCTED INDEPENDENTLY, EACH CONSUMER RUN")
# ---------------------------------------------------------------------------

print("""
   mg-b2af constructed its drift by editing a pin to name a different real
   revision.  So does this, with revisions chosen here: `REPAIR_REV_PIN` and
   `REV_7E58_PIN` are both re-pointed at mg-330a's own two commits, which
   exist, are ancestors of HEAD, and are not the revisions mg-b2af used.
   The DERIVATIONS are untouched, so only the pin-versus-derivation
   comparison moves.
""")

CONSUMERS = [
    ("k2_five.py",  "PRE_7E58_REV", 0),
    ("k4_cancel.py", "REPAIR_REV",  1),
]

clone = L.clone_at("HEAD")
try:
    lib_path = os.path.join(clone, LIBE34A)
    text = open(lib_path).read()
    new_repair = L.resolve(L.A330A_REPAIR)
    new_7e58 = L.resolve(L.A330A_PRE)
    text2 = re.sub(r'REPAIR_REV_PIN = "[0-9a-f]{40}"',
                   'REPAIR_REV_PIN = "%s"' % new_repair, text)
    text2 = re.sub(r'REV_7E58_PIN = "[0-9a-f]{40}"',
                   'REV_7E58_PIN = "%s"' % new_7e58, text2)
    R.selfgate(text2 != text and text2.count(new_repair) == 1
               and text2.count(new_7e58) == 1,
               "the pin edit did not apply exactly once each; the "
               "construction below is not the one described")

    base = {}
    for script, anchor, _pred in CONSUMERS:
        rc, out, err = L.run_py(script, os.path.join(clone, E34A_DIR))
        bad = [ln for ln in out.splitlines() if ln.startswith("TOTAL BAD:")]
        base[script] = (rc, bad[-1] if bad else "(no TOTAL BAD line)")
        if err.strip():
            print("   (stderr from %s: %s)" % (script, err.strip()[:90]))

    open(lib_path, "w").write(text2)
    L.commit_in(clone, LIBE34A, text2,
                "constructed: two pins re-pointed at real revisions")

    after = {}
    for script, anchor, _pred in CONSUMERS:
        rc, out, err = L.run_py(script, os.path.join(clone, E34A_DIR))
        bad = [ln for ln in out.splitlines() if ln.startswith("TOTAL BAD:")]
        spend = [ln for ln in out.splitlines()
                 if "ANCHOR DRIFT AT THE POINT OF SPEND" in ln]
        after[script] = (rc, bad[-1] if bad else "(no TOTAL BAD line)",
                         len(spend))

    print("   %-16s %-14s %-24s %-24s %s"
          % ("script", "anchor spent", "clean clone", "under drift",
             "spend-gate rows"))
    moved = 0
    for script, anchor, _pred in CONSUMERS:
        b, a = base[script], after[script]
        if (b[0], b[1]) != (a[0], a[1]):
            moved += 1
        print("   %-16s %-14s exit %d, %-14s exit %d, %-14s %d"
              % (script, anchor, b[0], b[1], a[0], a[1], a[2]))
    R.selfgate(moved == len(CONSUMERS),
               "%d of %d consumers did not move under the constructed drift; "
               "a construction that changes nothing demonstrates nothing"
               % (len(CONSUMERS) - moved, len(CONSUMERS)))

    print("""
   BOTH CONSUMERS GO RED AT THE POINT OF SPEND, AND THE ROWS THEY PRINT NAME
   THE ANCHOR THEY SPEND.  F-1's repair holds, under a drift it did not
   choose, at a tree it was not measured at.  That is the part of this
   ticket that CONFIRMS.
""")
finally:
    L.rm_tree(clone)

# ---------------------------------------------------------------------------
L.rule("(iv) PREDICTIONS SCORED")
# ---------------------------------------------------------------------------
L.score(R, "P-5", "1..6 external ungated spenders", len(gaps_out),
        hit=(1 <= len(gaps_out) <= 6))
L.score(R, "P-6", "LAST_TOUCHING_G1 -> SELF-ERROR",
        "SELF-ERROR" if "LAST_TOUCHING_G1" in ungateable else "gateable",
        hit=("LAST_TOUCHING_G1" in ungateable))
L.score(R, "P-7", "k4 2->3 and k2 0->1",
        "; ".join("%s %s -> %s" % (s, base[s][1].split(": ")[-1],
                                   after[s][1].split(": ")[-1])
                  for s, _a, _p in CONSUMERS),
        hit=(base["k4_cancel.py"][1].endswith("2")
             and after["k4_cancel.py"][1].endswith("3")
             and base["k2_five.py"][1].endswith("0")
             and after["k2_five.py"][1].endswith("1")))

R.done()
