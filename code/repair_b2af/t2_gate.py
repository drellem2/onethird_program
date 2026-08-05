"""t2_gate.py -- OPEN 1 (F-1): THE GATE AT THE POINT OF SPEND.

mg-330a: `ANCHOR_DRIFT` is gated in 2 of the 4 scripts that read an anchor.
`k4_cancel.py` -- the script the repair itself identifies as the one "where
the count actually moved" -- reads `REPAIR_REV` and does not carry the gate.
Neither does `k2_five.py` (`PRE_7E58_REV`).

  (i)   WHO SPENDS AN ANCHOR AND WHO GATES, by walking the parse tree.
        Scored at the commit BEFORE this repair and at the tree, so the
        detector is seen going both red and green.
  (ii)  THE RULE MADE STRUCTURAL -- an AST check, not a list of filenames.
  (iii) DRIFT CONSTRUCTED IN A CLONE, and k4 and k2 re-run there.  The
        difference between the two runs is the whole of F-1.
  (iv)  THE GATE IS SILENT WHEN GREEN.  A gate that prints on a clean tree
        is a banner.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.  This script tests THIS
repair; if it is not 0 the repair is not done.
"""

import ast
import os
import subprocess
import sys

import lib_b2af as L

R = L.Report(
    selfpop="every parse, clone, and foreign-script run this script "
            "performs, plus the requirement that the constructed drift "
            "really reach the scripts under test",
    findpop="each of the scripts in code/branching_audit_e34a/ that names a "
            "derived anchor, checked for a drift gate at the commit before "
            "this repair and at the tree; and k4 and k2 re-run under "
            "constructed drift and under none")

L.banner("T2", "OPEN 1 (F-1) -- THE GATE WHERE THE ANCHOR IS SPENT")

# ---------------------------------------------------------------------------
L.rule("(i) WHO SPENDS AN ANCHOR, AND WHO GATES -- FROM THE PARSE TREE")
# ---------------------------------------------------------------------------
print("""   Not from mg-330a's table.  A finding read out of the document
   that reports it is the document agreeing with itself.  Every `.py`
   in code/branching_audit_e34a/ is parsed, every `L.<NAME>` load of a
   derived anchor is collected, and every gate is collected the same
   way -- a reference to `ANCHOR_DRIFT`, or a call to `gate_spent`.
""")


def scan(tree_root):
    """{script: (anchors spent, gates ANCHOR_DRIFT, anchors gated by name)}"""
    out = {}
    d = os.path.join(tree_root, L.E34A_DIR)
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".py") or fn == "libe34a.py":
            continue
        with open(os.path.join(d, fn)) as fh:
            src = fh.read()
        try:
            node = ast.parse(src)
        except SyntaxError as exc:
            R.selferr("%s did not parse at %s: %s" % (fn, tree_root, exc))
            continue
        spends, whole, by_name = set(), False, set()
        for n in ast.walk(node):
            if isinstance(n, ast.Attribute) and n.attr in L.ANCHOR_NAMES:
                spends.add(n.attr)
            if isinstance(n, ast.Attribute) and n.attr == "ANCHOR_DRIFT":
                whole = True
            if isinstance(n, ast.Name) and n.id == "ANCHOR_DRIFT":
                whole = True
            if isinstance(n, ast.Call):
                f = n.func
                name = (f.attr if isinstance(f, ast.Attribute)
                        else f.id if isinstance(f, ast.Name) else None)
                if name == "gate_spent":
                    for a in n.args:
                        if isinstance(a, ast.Constant) \
                                and isinstance(a.value, str):
                            by_name.add(a.value)
        out[fn] = (spends, whole, by_name)
    return out


landed, pre_gate = L.gate_landed()
for row in L.GATE_FALLBACK:
    print("   NOTE: %s" % row)
print("   the commit that introduces `%s` in %s :" % (L.MARK_GATE,
                                                     L.E34A_LIB))
print("      derived from the property : %s" % (landed[:8] if landed
                                                else "NOT YET COMMITTED"))
print("      the commit before it      : %s" % (pre_gate[:8] if pre_gate
                                                else "-- falling back to "
                                                     "HEAD"))
print()

BEFORE_REV = pre_gate or L.resolve("HEAD")
before_tree = L.clone_at(BEFORE_REV)
STATES = [("BEFORE (%s)" % BEFORE_REV[:8], before_tree),
          ("AFTER (the tree)", L.REPO)]

results = {}
for label, root in STATES:
    results[label] = scan(root)
    print("   %s" % label)
    print("      %-22s %-26s %s" % ("script", "anchors it spends", "gated?"))
    for fn, (spends, whole, by_name) in sorted(results[label].items()):
        if not spends:
            continue
        covered = whole or spends <= by_name
        print("      %-22s %-26s %s"
              % (fn, ",".join(sorted(spends)),
                 "yes -- whole ANCHOR_DRIFT" if whole
                 else "yes -- gate_spent(%s)" % ",".join(sorted(by_name))
                 if covered else "*** NO"))
    n_spend = len([1 for s, _w, _b in results[label].values() if s])
    n_gate = len([1 for s, w, b in results[label].values()
                  if s and (w or s <= b)])
    print("      consumers that gate : %d of %d" % (n_gate, n_spend))
    print()

before = results["BEFORE (%s)" % BEFORE_REV[:8]]
after = results["AFTER (the tree)"]
b_spend = len([1 for s, _w, _b in before.values() if s])
b_gate = len([1 for s, w, b in before.values() if s and (w or s <= b)])
a_spend = len([1 for s, _w, _b in after.values() if s])
a_gate = len([1 for s, w, b in after.values() if s and (w or s <= b)])

print("   BEFORE : %d of %d    AFTER : %d of %d"
      % (b_gate, b_spend, a_gate, a_spend))
R.check(b_gate < b_spend,
        "every consumer already gated at %s, so this detector has never been "
        "seen red and its green means nothing" % BEFORE_REV[:8])
R.gate(a_gate == a_spend,
       "%d of %d scripts that spend a derived anchor still carry no drift "
       "gate: %s"
       % (a_spend - a_gate, a_spend,
          ", ".join(fn for fn, (s, w, b) in sorted(after.items())
                    if s and not (w or s <= b))))

# ---------------------------------------------------------------------------
L.rule("(ii) THE RULE, MADE STRUCTURAL")
# ---------------------------------------------------------------------------
print("""   The rule is not `k2 and k4 have been fixed`.  A list of two
   filenames does not notice a third script being added, which is the
   same defect as a written list of five outputs -- mg-957f's OPEN 2,
   in this very directory.

   THE RULE: every script in code/branching_audit_e34a/ that names a
   derived anchor either references the whole of ANCHOR_DRIFT or calls
   gate_spent for EVERY anchor it names.  Applied above, at both
   states.  It goes red at %s and green at the tree, and both
   readings are printed rather than one.
""" % BEFORE_REV[:8])

print("   scripts that name an anchor and do not cover it:")
for label in (s[0] for s in STATES):
    bad = [fn for fn, (s, w, b) in sorted(results[label].items())
           if s and not (w or s <= b)]
    print("      %-24s %s" % (label, ", ".join(bad) or "none"))

print()
print("   AND THE PARTIAL CASE, which a boolean `calls gate_spent` would")
print("   miss: a script that gates ONE of the two anchors it spends is")
print("   NOT covered.  The rule is a subset test, not a call count.")
for fn, (s, w, b) in sorted(after.items()):
    if s and b and not w:
        print("      %-22s spends %-22s gates %s"
              % (fn, ",".join(sorted(s)), ",".join(sorted(b))))

# ---------------------------------------------------------------------------
L.rule("(iii) DRIFT CONSTRUCTED, AND THE TWO SCRIPTS RE-RUN UNDER IT")
# ---------------------------------------------------------------------------
print("""   The gate is asserted to fire.  So it is made to fire.

   In a clone: one of libe34a's pinned revisions is edited to name a
   DIFFERENT REAL revision.  The derivation is untouched, so every
   other number each script prints is unchanged -- only the
   pin-vs-derivation comparison moves.  Then k4 and k2 are run there.
""")


def run(script, root):
    p = subprocess.run([sys.executable, script],
                       cwd=os.path.join(root, L.E34A_DIR),
                       capture_output=True, text=True)
    tail = [ln for ln in p.stdout.splitlines()
            if ln.startswith("TOTAL BAD:")]
    return p.returncode, (tail[-1] if tail else "(no TOTAL BAD line)"), p.stdout


def perturb(root, old, new):
    path = os.path.join(root, L.E34A_LIB)
    with open(path) as fh:
        src = fh.read()
    if old not in src:
        R.selferr("the pin %s is not in %s in the clone, so the constructed "
                  "drift never reached the scripts under test"
                  % (old[:8], L.E34A_LIB))
        return False
    with open(path, "w") as fh:
        fh.write(src.replace(old, new, 1))
    return True


# A DIFFERENT REAL REVISION.  Not a made-up sha: `_anchored` would then
# report "the marker is in no commit" rather than a disagreement, and the
# construction would be testing the wrong branch of the gate.
OTHER = L.resolve(L.REPAIR_8D5E)
PIN_76CC = "4755d0292fc9175815739e9a77fa24dc6b8baf48"
PIN_7E58 = "4372fae95881bb421099bc715d1924c37d98b7b3"

print("   the substitute revision : %s -- %s"
      % (OTHER[:8], L.subject(OTHER)[:44]))
print()

CASES = [
    ("k4_cancel.py", "REPAIR_REV", PIN_76CC),
    ("k2_five.py", "PRE_7E58_REV", PIN_7E58),
]

print("   %-16s %-14s %-22s %s"
      % ("script", "anchor spent", "clean tree", "under constructed drift"))
moved = {}
for script, anchor, pin in CASES:
    clean_root = L.clone_at("HEAD")
    # carry this repair's uncommitted edits into the clone, so the clone is
    # the tree under test and not the tree before it
    for rel in (L.E34A_LIB, L.E34A_DIR + "/k4_cancel.py",
                L.E34A_DIR + "/k2_five.py"):
        with open(os.path.join(L.REPO, rel)) as fh:
            src = fh.read()
        with open(os.path.join(clean_root, rel), "w") as fh:
            fh.write(src)
    rc_clean, tot_clean, _ = run(script, clean_root)

    drift_root = L.clone_at("HEAD")
    for rel in (L.E34A_LIB, L.E34A_DIR + "/k4_cancel.py",
                L.E34A_DIR + "/k2_five.py"):
        with open(os.path.join(L.REPO, rel)) as fh:
            src = fh.read()
        with open(os.path.join(drift_root, rel), "w") as fh:
            fh.write(src)
    if not perturb(drift_root, pin, OTHER):
        continue
    rc_drift, tot_drift, out_drift = run(script, drift_root)

    n_clean = int(tot_clean.split(":")[1])
    n_drift = int(tot_drift.split(":")[1])
    moved[script] = (n_clean, n_drift, rc_clean, rc_drift)
    print("   %-16s %-14s %-22s %s"
          % (script, anchor, "exit %d, %s" % (rc_clean, tot_clean),
             "exit %d, %s" % (rc_drift, tot_drift)))

    R.gate(n_drift > n_clean,
           "%s spends %s and books the SAME number of findings (%d) whether "
           "that anchor agrees with its pin or not.  The gate is not "
           "reaching this script" % (script, anchor, n_clean))
    names_it = ("ANCHOR DRIFT AT THE POINT OF SPEND" in out_drift
                and anchor in out_drift)
    R.gate(names_it,
           "%s books an extra finding under constructed drift but does not "
           "name the anchor it spends; a reader cannot tell which number "
           "below it is about" % script)

print()
print("   THE DIFFERENCE IS F-1.  Before this repair both scripts printed")
print("   the left-hand column under BOTH conditions: a re-pointed anchor")
print("   changed nothing they said.  That is what `silent where it is")
print("   spent` meant, and it is measured here rather than argued.")

# ---------------------------------------------------------------------------
L.rule("(iv) THE GATE IS SILENT WHEN GREEN")
# ---------------------------------------------------------------------------
print("""   A gate that prints on a clean tree is a banner.  The two
   scripts are run on the unperturbed tree and their output compared
   with what their COMMITTED transcripts say -- so the check is against
   what they said before this repair existed, not against this run.
""")

print("   %-16s %-24s %-24s %s"
      % ("script", "committed transcript", "this tree", "unchanged?"))
clean_now = {}
for script, _anchor, _pin in CASES:
    committed = L.git_quiet("show", "%s:%s/out_%s.txt"
                            % (L.resolve("HEAD"), L.E34A_DIR, script[:-3]))
    want = [ln for ln in committed.splitlines()
            if ln.startswith("TOTAL BAD:")]
    rc, tot, out = run(script, L.REPO)
    clean_now[script] = (rc, tot)
    same = bool(want) and want[-1] == tot
    print("   %-16s %-24s %-24s %s"
          % (script, want[-1] if want else "(not found)", tot,
             "yes" if same else "*** NO"))
    R.gate(same,
           "%s prints %r on this tree and its committed transcript says "
           "%r.  The gate is not silent when green: adding it changed what "
           "the script reports on a tree with no drift"
           % (script, tot, want[-1] if want else "(not found)"))
    R.check("ANCHOR DRIFT AT THE POINT OF SPEND" not in out,
            "%s printed the drift finding on a clean tree" % script)

# ---------------------------------------------------------------------------
L.rule("(v) THE TWO THAT ALREADY GATED ARE NOT TOUCHED")
# ---------------------------------------------------------------------------
print("""   k1_prerepair.py and selftest_e34a.py gate on the WHOLE of
   ANCHOR_DRIFT, which is a superset of what gate_spent asks.
   Rewriting them would move two transcripts for no property gained --
   and k1 takes about ten minutes to regenerate.  Checked, not
   promised: their bytes at %s against their bytes here.
""" % BEFORE_REV[:8])

for fn in ("k1_prerepair.py", "selftest_e34a.py", "k3_undisturbed.py"):
    rel = "%s/%s" % (L.E34A_DIR, fn)
    was = L.git_quiet("show", "%s:%s" % (BEFORE_REV, rel))
    with open(os.path.join(L.REPO, rel)) as fh:
        now = fh.read()
    print("   %-22s %s" % (fn, "byte-identical" if was == now
                           else "*** CHANGED"))
    R.gate(was == now,
           "%s was modified by this repair; it already gated on the whole of "
           "ANCHOR_DRIFT and had nothing to gain" % fn)

# ---------------------------------------------------------------------------
L.rule("PREDICTIONS SCORED")
# ---------------------------------------------------------------------------
L.score(R, "P-5a", 2, b_gate, note="2 of 4 gate before")
L.score(R, "P-5b", 4, a_gate, note="4 of 4 gate after")
L.score(R, "P-5c",
        [("k4_cancel.py", 2, 3), ("k2_five.py", 0, 1)],
        sorted([(s, c, d) for s, (c, d, _rc, _rd) in moved.items()],
               key=lambda x: x[0], reverse=True),
        note="k4 2->3, k2 0->1 under constructed drift")
L.score(R, "P-5d", [(1, "TOTAL BAD: 2"), (0, "TOTAL BAD: 0")],
        [clean_now.get("k4_cancel.py"), clean_now.get("k2_five.py")],
        note="k4 exit 1 / 2, k2 exit 0 / 0, unperturbed")
L.score(R, "P-5e", (True, True), (b_gate < b_spend, a_gate == a_spend),
        note="structural check red before, green after")
L.score(R, "P-5f", 0, len([1 for x in R.findings if "was modified by this "
                           "repair" in x]),
        note="k1 and selftest untouched -- see (v)")

L.rule("VERDICT")
print("""   F-1 IS CLOSED, AND CLOSED BY CONSTRUCTION.  The gate is offered
   at the point of use, both scripts that spend an anchor now take it,
   the rule that says so is an AST check rather than a list of two
   filenames, and the difference it makes was measured by making the
   anchor drift rather than by describing what would happen if it did.

   WHAT THIS REPAIR DID NOT DO: it did not gate the 19 sites t1
   enumerates.  Those live in other tickets' directories and 11 of them
   take their path from a parameter, which means there is nothing at
   the site to gate -- the anchor is at the call site.  That is the
   same lesson as F-1 one level down, and it is named in t1 (iii)
   rather than quietly treated as done.
""")

sys.exit(R.emit())
