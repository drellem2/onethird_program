"""s2_perturb.py -- BUILD THE FAILURE.  Do not recall it.

The brief: *touch the anchor file with a cosmetic edit and confirm the anchor
now refuses or reports a change, rather than silently following.  If it
follows silently, the repair did not fix this.*

Four probes, each a COMMIT in its own clone:

  (i)   COSMETIC, AT HEAD.  A comment appended to g1_provenance.py -- the
        same shape of edit as mg-69d1's sentence correction, and by
        construction with nothing to do with the property.  What moves, what
        does not, and what SAYS SO.
  (ii)  COSMETIC, AT e2577e5 -- A COMMIT WHERE THE DEFECT IS STILL PRESENT.
        The control.  A detector that has never been seen to go red is a
        detector whose red is unmeasured, and the same is true of a repair
        that has never been seen NOT to hold.
  (iii) THE REFUSAL.  Three constructed failures at HEAD -- a wrong pin, an
        absent marker, a non-monotone marker -- each its own clone, each
        scored by mg-e34a's OWN selftest.  If the three pieces of the anchor
        all failed the same way, one commit would silence all three.
  (iv)  AND THE THING (i) CANNOT SHOW: a cosmetic edit does not make the
        repaired anchor RED, and the brief allows either `refuses` or
        `reports`.  Which is it?  Answered by measurement, with the
        difference between the two printed rather than asserted.

Nothing here writes into code/branching_audit_e34a/.  Every mutation is a
commit in a clone under the system temp directory.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib330a as L                                          # noqa: E402

R = L.Report(
    selfpop="every clone, git read and subprocess run this script performs, "
            "plus the requirement that each constructed commit really change "
            "the file it names, that the cosmetic edit really leave the "
            "property marker where it was, and that mg-e34a's selftest be "
            "GREEN in each untouched clone before any probe is read against "
            "it",
    findpop="the 2 derivations libe34a can make of `the revision before "
            "mg-76cc's repair`, each re-derived under a cosmetic commit at "
            "HEAD and again at e2577e5 where the defect is still present; "
            "the 3 constructed failures of the repaired anchor, each scored "
            "for whether it is LOUD and for whether it is loud in a "
            "DIFFERENT way from the other two; and the question of whether "
            "the repaired anchor refuses or reports")

L.banner("S2", "THE FAILURE, CONSTRUCTED -- NOT RECALLED")

# The driver printed into each clone.  It imports that clone's OWN libe34a,
# so the code under test is the code AT THAT REVISION and not this one.
DRIVER = r'''
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import libe34a as E
def g(n, d="-"):
    v = getattr(E, n, None)
    return (v or d)[:8] if isinstance(v, str) else d
print("REPAIR_REV=%s" % g("REPAIR_REV"))
print("PRE_REV=%s" % g("PRE_REV"))
print("REV_7E58=%s" % g("REV_7E58"))
print("PRE_7E58_REV=%s" % g("PRE_7E58_REV"))
print("LAST_TOUCHING_G1=%s" % g("LAST_TOUCHING_G1"))
drift = getattr(E, "ANCHOR_DRIFT", None)
print("HAS_ANCHOR_DRIFT=%s" % ("yes" if drift is not None else "NO"))
print("DRIFT_ROWS=%d" % (len(drift) if drift is not None else -1))
for row in (drift or []):
    print("DRIFT: %s" % row)
'''

COSMETIC = ("\n# mg-330a probe: a comment appended.  A cosmetic edit, with "
            "nothing\n# whatever to do with the kernel half.  This is the "
            "SHAPE of the edit\n# mg-69d1 made -- it corrected a sentence -- "
            "and the shape is the point.\n")


def probe_at(rev, label, edit=COSMETIC, mutate=None):
    """Clone at `rev`, apply `edit` (or `mutate(tree)`), report anchors."""
    tree = L.clone_at(rev)
    try:
        d = os.path.join(tree, L.E34A_DIR)
        rc0, out0 = L.run_py_src(DRIVER, d, "mg330a_driver.py")
        R.selfgate(rc0 == 0, "%s: the driver failed in the UNTOUCHED clone "
                             "(exit %d): %s" % (label, rc0, out0[-300:]))
        before = parse_driver(out0)

        if mutate is not None:
            new_commit, what = mutate(tree)
        else:
            src = L.show_or_empty("HEAD", L.G1_REL, repo=tree)
            R.selfgate(L.MARK_76CC in src,
                       "%s: the property marker is not in g1 at %s, so the "
                       "cosmetic probe has nothing to leave alone"
                       % (label, rev))
            new_commit = L.commit_in(
                tree, L.G1_REL, src + COSMETIC,
                "probe: a comment appended to g1_provenance.py (mg-330a)")
            what = "a comment appended to g1_provenance.py"
            after_src = L.show_or_empty("HEAD", L.G1_REL, repo=tree)
            R.selfgate(after_src != src,
                       "%s: the cosmetic commit did not change the file"
                       % label)
            R.selfgate(L.MARK_76CC in after_src,
                       "%s: the cosmetic commit REMOVED the property marker "
                       "-- it is not cosmetic and nothing can be read from it"
                       % label)

        rc1, out1 = L.run_py_src(DRIVER, d, "mg330a_driver.py")
        after = parse_driver(out1)
        return {"tree": tree, "before": before, "after": after,
                "commit": new_commit, "what": what, "rc": rc1, "raw": out1}
    finally:
        pass  # caller frees; the tree is needed for the selftest run


def parse_driver(out):
    d = {"DRIFT": []}
    for ln in out.splitlines():
        if ln.startswith("DRIFT: "):
            d["DRIFT"].append(ln[7:])
        elif "=" in ln and not ln.startswith(" "):
            k, v = ln.split("=", 1)
            d[k.strip()] = v.strip()
    return d


# ---------------------------------------------------------------------------
L.rule("(i) A COSMETIC COMMIT TO g1_provenance.py, AT HEAD")
# ---------------------------------------------------------------------------

print("""   The edit is a comment appended to the end of the file.  It is the
   same SHAPE as mg-69d1's edit -- that one corrected a sentence -- and
   the shape is the whole point: an edit with nothing to do with the
   property must not move an anchor that claims to be about the
   property.

   The libe34a imported below is the one IN THE CLONE, so the code
   under test is the code at the revision named, not the code here.
""")

p = probe_at("HEAD", "HEAD/cosmetic")
try:
    print("   %-22s %-10s %-10s %s" % ("name", "before", "after", ""))
    MOVED = {}
    for k in ("REPAIR_REV", "PRE_REV", "REV_7E58", "PRE_7E58_REV",
              "LAST_TOUCHING_G1"):
        b, a = p["before"].get(k, "-"), p["after"].get(k, "-")
        MOVED[k] = (b != a)
        print("   %-22s %-10s %-10s %s"
              % (k, b, a, "*** MOVED" if b != a else "unmoved"))
    print("\n   the cosmetic commit                            : %s"
          % p["commit"][:8])
    print("   ANCHOR_DRIFT rows after the edit               : %s"
          % p["after"].get("DRIFT_ROWS"))

    R.gate(not MOVED["REPAIR_REV"],
           "A COSMETIC EDIT MOVED REPAIR_REV at HEAD (%s -> %s).  The repair "
           "did not fix A-1: the anchor still follows an edit that has "
           "nothing to do with the property it names"
           % (p["before"].get("REPAIR_REV"), p["after"].get("REPAIR_REV")))
    R.gate(not MOVED["PRE_REV"],
           "A COSMETIC EDIT MOVED PRE_REV at HEAD (%s -> %s) -- the "
           "pre-repair predicate is now a different predicate and no number "
           "said so"
           % (p["before"].get("PRE_REV"), p["after"].get("PRE_REV")))
    R.gate(not MOVED["PRE_7E58_REV"],
           "A COSMETIC EDIT MOVED PRE_7E58_REV at HEAD -- the second history "
           "anchor still re-points")

    print("""
   AND THE HALF THAT MUST MOVE.  If NOTHING moved, this probe would
   prove only that the edit never reached git.  LAST_TOUCHING_G1 --
   the derivation the repair KEPT as evidence -- is the control on the
   probe itself:
     LAST_TOUCHING_G1  %s -> %s   %s
""" % (p["before"].get("LAST_TOUCHING_G1"),
       p["after"].get("LAST_TOUCHING_G1"),
       "MOVED, so the edit reached git"
       if MOVED["LAST_TOUCHING_G1"] else "*** DID NOT MOVE"))
    R.selfgate(MOVED["LAST_TOUCHING_G1"],
               "the cosmetic commit did not move LAST_TOUCHING_G1, so the "
               "probe never reached git and nothing above can be read")
    R.selfgate(p["after"].get("LAST_TOUCHING_G1") == p["commit"][:8],
               "LAST_TOUCHING_G1 after the edit is %s, not the cosmetic "
               "commit %s" % (p["after"].get("LAST_TOUCHING_G1"),
                              p["commit"][:8]))

    print("""   SO THE ANCHOR DOES NOT FOLLOW -- and it is not silent either.
   The derivation that DID follow is still computed and still printed,
   so the reader is shown the edit happened and shown that the anchor
   ignored it.  That is `reports a change`, and (iv) asks whether it
   is also `refuses`.
""")

    d = os.path.join(p["tree"], L.E34A_DIR)
    rc_self, out_self = L.run_py("selftest_e34a.py", d)
    print("   mg-e34a's OWN selftest, in the perturbed clone : exit %d"
          % rc_self)
    R.gate(rc_self == 0,
           "mg-e34a's selftest goes RED (exit %d) on a purely cosmetic edit "
           "to g1_provenance.py -- an instrument that cannot survive a "
           "comment cannot be run on a live tree" % rc_self)
    for ln in out_self.splitlines():
        if ln.strip().startswith("FAIL"):
            print("      %s" % ln.strip()[:96])
finally:
    L.rm_tree(p["tree"])

# ---------------------------------------------------------------------------
L.rule("(ii) THE CONTROL -- THE SAME EDIT AT e2577e5, WHERE THE DEFECT LIVES")
# ---------------------------------------------------------------------------

print("""   e2577e5 is dfa263c's first parent: mg-8d5e's own predictions
   commit, the last commit before the repair.  At that revision
   libe34a.py reads

       REPAIR_REV = last_touching(G1_REL)
       PRE_REV = resolve(REPAIR_REV + "^")

   and there is no ANCHOR_DRIFT at all.  The same cosmetic commit is
   applied there.  If the repair is real, the defect reproduces here
   and does not reproduce above.
""")

pc = probe_at(L.PRE_8D5E, "e2577e5/cosmetic")
try:
    print("   %-22s %-10s %-10s %s" % ("name", "before", "after", ""))
    CMOVED = {}
    for k in ("REPAIR_REV", "PRE_REV", "PRE_7E58_REV", "LAST_TOUCHING_G1"):
        b, a = pc["before"].get(k, "-"), pc["after"].get(k, "-")
        CMOVED[k] = (b != a)
        print("   %-22s %-10s %-10s %s"
              % (k, b, a, "*** MOVED" if b != a else "unmoved"))
    print("\n   the cosmetic commit                            : %s"
          % pc["commit"][:8])
    print("   does libe34a AT e2577e5 have ANCHOR_DRIFT?     : %s"
          % pc["after"].get("HAS_ANCHOR_DRIFT"))

    R.selfgate(CMOVED.get("REPAIR_REV", False),
               "the control did NOT reproduce: REPAIR_REV at e2577e5 did not "
               "move under a cosmetic edit, so this probe demonstrates "
               "nothing about the repair")
    R.selfgate(pc["after"].get("HAS_ANCHOR_DRIFT") == "NO",
               "libe34a at e2577e5 already has ANCHOR_DRIFT, so e2577e5 is "
               "not a commit where the defect is still present")

    print("""
   THE DEFECT REPRODUCES.  At e2577e5 the cosmetic commit becomes
   `mg-76cc's repair` and its parent becomes `the pre-repair
   predicate`, with no drift row anywhere, because there is nothing
   for the derivation to disagree with.  What the run would then print
   is a table of numbers about a pair of revisions nobody chose.

     at e2577e5, after a comment was appended:
       REPAIR_REV names %s -- %s
       and its subject is         : %s
""" % (pc["after"].get("REPAIR_REV"),
       "the cosmetic commit" if pc["after"].get("REPAIR_REV")
       == pc["commit"][:8] else "something else",
       "probe: a comment appended to g1_provenance.py (mg-330a)"))

    d = os.path.join(pc["tree"], L.E34A_DIR)
    rc_self, _ = L.run_py("selftest_e34a.py", d)
    print("   mg-e34a's selftest AT e2577e5, perturbed       : exit %d  %s"
          % (rc_self, "(and it is a DIFFERENT selftest -- the one at HEAD "
                      "carries assertions e2577e5 does not)"))

    print("""   AND THE COMPARISON THE WHOLE AUDIT TURNS ON:

     probe                                   REPAIR_REV follows?
       cosmetic edit at e2577e5 (pre-repair)   %s
       cosmetic edit at HEAD    (repaired)     %s
""" % ("YES -- silently" if CMOVED.get("REPAIR_REV") else "no",
       "YES" if MOVED["REPAIR_REV"] else "NO"))
finally:
    L.rm_tree(pc["tree"])

# ---------------------------------------------------------------------------
L.rule("(iii) THE REFUSAL -- THREE FAILURES, AND WHETHER THEY DIFFER")
# ---------------------------------------------------------------------------

print("""   The claim is that the anchor is THREE things and NO TWO OF THEM
   FAIL THE SAME WAY: derived from the property, pinned, and compared.
   Built here rather than read out of r1 (iii).  Each failure is its
   own clone and its own commit, and each is scored by mg-e34a's OWN
   selftest -- if one commit could silence all three, the three would
   be one.
""")


def mutate_pin(tree):
    """A WRONG PIN: the derivation is right and the pin is not."""
    rel = L.E34A_DIR + "/libe34a.py"
    src = L.read_worktree(rel, repo=tree)
    bad = src.replace('REPAIR_REV_PIN = "4755d029',
                      'REPAIR_REV_PIN = "0000000000')
    assert bad != src, "the pin line was not found"
    return L.commit_in(tree, rel, bad,
                       "probe: a WRONG PIN (mg-330a)"), "a wrong pin"


def mutate_marker(tree):
    """AN UNFINDABLE MARKER: the pin is right and the property is not."""
    rel = L.E34A_DIR + "/libe34a.py"
    src = L.read_worktree(rel, repo=tree)
    bad = src.replace('MARK_76CC = "kernel_source="',
                      'MARK_76CC = "no_such_marker_mg330a="')
    assert bad != src, "the marker line was not found"
    return L.commit_in(tree, rel, bad,
                       "probe: an UNFINDABLE MARKER (mg-330a)"), \
        "an unfindable marker"


def mutate_monotone(tree):
    """A NON-MONOTONE MARKER: present, then absent again."""
    src = L.show_or_empty("HEAD", L.G1_REL, repo=tree)
    assert L.MARK_76CC in src
    bad = src.replace(L.MARK_76CC, "kernel_SOURCE_mg330a=")
    return L.commit_in(tree, L.G1_REL, bad,
                       "probe: the marker REMOVED from g1 (mg-330a)"), \
        "a non-monotone marker"


FAILURES = [("a wrong pin", mutate_pin),
            ("an unfindable marker", mutate_marker),
            ("a non-monotone marker", mutate_monotone)]

print("   %-26s %-6s %-8s %s"
      % ("constructed failure", "exit", "drift", "the selftest line that "
         "goes red"))
seen_reasons = {}
for name, fn in FAILURES:
    tree = L.clone_at("HEAD")
    try:
        d = os.path.join(tree, L.E34A_DIR)
        rc0, _ = L.run_py("selftest_e34a.py", d)
        R.selfgate(rc0 == 0,
                   "%s: mg-e34a's selftest is not green in the untouched "
                   "clone (exit %d)" % (name, rc0))
        fn(tree)
        rc, out = L.run_py("selftest_e34a.py", d)
        rc_drv, out_drv = L.run_py_src(DRIVER, d, "mg330a_driver.py")
        drift = parse_driver(out_drv).get("DRIFT_ROWS", "-")
        fails = [ln.strip() for ln in out.splitlines()
                 if ln.strip().startswith("FAIL")]
        first = fails[0][5:60] if fails else "(none)"
        print("   %-26s %-6d %-8s %s" % (name, rc, drift, first))
        for f in fails:
            print("        %s" % f[:100])
        seen_reasons[name] = (rc, tuple(sorted(f[:70] for f in fails)))
        R.gate(rc != 0,
               "the constructed failure `%s` leaves mg-e34a's selftest GREEN "
               "(exit %d) -- that piece of the three-part anchor cannot fail "
               "loudly" % (name, rc))
    finally:
        L.rm_tree(tree)

print("\n   AND THE CLAIM THAT NO TWO FAIL THE SAME WAY.  Two failures fail\n"
      "   the same way iff they make the SAME assertions go red:")
names = [n for n, _ in FAILURES]
same = []
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        a, b = seen_reasons.get(names[i]), seen_reasons.get(names[j])
        ident = a is not None and a == b
        print("     %-24s vs %-24s : %s"
              % (names[i], names[j],
                 "*** IDENTICAL" if ident else "different"))
        if ident:
            same.append((names[i], names[j]))
R.gate(not same,
       "two of the three constructed failures make the SAME assertions go "
       "red (%s), so the anchor is not three independent things -- one "
       "commit silences more than one of them"
       % "; ".join("%s == %s" % p for p in same))

# ---------------------------------------------------------------------------
L.rule("(iv) REFUSES, OR REPORTS?  THE ANSWER, MEASURED")
# ---------------------------------------------------------------------------

print("""   The brief allows either.  The measurement above says which:

     a COSMETIC edit to g1_provenance.py at HEAD
       moves the property anchor            : no
       moves the kept history derivation    : YES, and it is printed
       makes mg-e34a's selftest red         : no
       => REPORTS.  The change is on the page and the anchor ignores it.

     a PROPERTY-MOVING edit (the marker removed)
       makes mg-e34a's selftest red         : yes (iii)
       => REFUSES.

   So `refuses rather than follows` is satisfied in the strong sense
   for the edits that move the property, and in the reporting sense
   for the edits that do not -- which is the correct division, because
   an instrument that refused to run on every comment could not be run
   on a live tree at all.  What the repair must not do is FOLLOW, and
   it does not.
""")

R.done()
