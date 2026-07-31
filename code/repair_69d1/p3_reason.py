"""p3_reason.py -- OPEN 2: THE ROW IS RIGHT AND ITS REASON WAS INVERTED.

mg-76cc added a third row to g1's section (v) -- `both together` -- and gave it
a reason:

    "then both are moved together, because two changes that cancel would pass
     each half on its own."

mg-e34a built the input that sentence names and measured it: a CANCELLING pair
moves BOTH half rows and leaves `both together` IDENTICAL.  The sentence is
exactly inverted, and the finding is against the sentence and not against the
row.

THE REPAIR IS THE REASON.  The row's (script, kernel) pair is untouched.  What
changed is the sentence in g1's docstring, the sentence g1 prints, the row's own
LABEL -- which named the case the row does not catch -- the same paragraph in
the repair's document, and an error message in r1_kernel.py that called it "the
cancellation case".

A RATIONALE IS A CLAIM AND THIS ONE NAMES AN INPUT, SO BOTH DIRECTIONS ARE
BUILT.  The new reason says two things and this script measures both:

  a CANCELLING pair   -- kern's dim L(n,p) one too BIG, c1's vertex dims one
                         too SMALL -- moves BOTH halves and passes `both
                         together`
  a CONSPIRING pair   -- kern gains a name the shipped c1 never reads, c1
                         reads it with a default that changes nothing --
                         passes BOTH halves and is caught by `both together`
                         alone

The second is the input the row exists for and NOTHING in mg-76cc, and nothing
in mg-e34a, ever built one.  Building it is what turns "the row is
load-bearing" from an assertion into a measurement.

Both pairs are shown to really be what they are claimed to be BEFORE any row
rests on them: the cancelling pair must restore the printed measurement exactly
and each of its halves must move it, and each conspiring half must be a NO-OP
on its own.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import lib69d1 as L                                              # noqa: E402

R = L.Report(
    selfpop="every git read and c1 run this script performs, the requirement "
            "that each of the 4 bends really change the file it names, that "
            "the baseline run really produce c1's 24 vertex sets, and that "
            "each pair really be the KIND of pair it is called before any row "
            "rests on it",
    findpop="the 3 rows of g1's section (v) evaluated on a cancelling pair "
            "and again on a conspiring pair -- 6 rows -- and the corrected "
            "reason scored against all 6 wherever it is written")

# The sentence under test, in its two forms.
OLD = "changes that cancel would pass"
NEW_A = "CONSPIRING pair"
NEW_B = "conspiracy"

L.banner("P3", "THE `both together` ROW, AND THE REASON IT IS THERE")
print("""
The row is correct.  Its reason named the one input it does not catch, and that
reason reached five artifacts before anybody built the input.  Both directions
are built here.
""")

# ---------------------------------------------------------------------------
L.rule("(i) THE SENTENCE, ENUMERATED FROM THE WORKING TREE")
print("""   A reason written in five places is five claims.  Every copy is
   found with `git grep` over the working tree, untracked files
   included, so a copy this script did not remember is still in the
   population.  A site that QUOTES the old sentence in order to refute
   it is not a site that ASSERTS it, and the two are told apart by
   whether the correcting ticket id stands within the window.""")
print()
WINDOW = 25
# `under test` and `inverted` are the audit's own refutation language: a
# committed transcript quotes the sentence inside the finding that refutes it
# and names its ticket in a banner hundreds of lines up, so a ticket-id-only
# test would read a record as an assertion.  THE DISCRIMINATOR IS NOT A PATH
# LIST, and §(i-b) below shows it is not vacuous either: run unchanged against
# HEAD -- the committed tree, before this repair -- it reports exactly the
# sites mg-e34a booked.
MARKERS = ("mg-69d1", "mg-e34a", "under test", "inverted", "INVERTED")


def corrected_near(path, lineno, rev=None):
    try:
        text = (L.git_show(rev, path) if rev else L.read_worktree(path))
    except (IOError, OSError, RuntimeError):
        return False
    lines = text.splitlines()
    i = int(lineno) - 1
    window = "\n".join(lines[max(0, i - WINDOW):i + WINDOW + 1])
    return any(m in window for m in MARKERS)


old_sites = L.grep(OLD)
live_old = [s for s in old_sites if not corrected_near(*s)]
print("   THE OLD REASON -- `%s ...`:" % OLD)
for path, lineno in old_sites:
    print("     %-56s line %-5s %s"
          % (path, lineno,
             "refuted within %d lines" % WINDOW if corrected_near(path, lineno)
             else "*** LIVE ASSERTION"))
print()
print("   (i-b) THE SAME DISCRIMINATOR, RUN AGAINST HEAD -- the committed "
      "tree, where\n   the defect is still present.  If it reported 0 live "
      "assertions there it would be\n   measuring nothing here:")
head_sites = L.grep(OLD, rev="HEAD")
head_live = [s for s in head_sites
             if not corrected_near(s[0], s[1], rev="HEAD")]
for path, lineno in head_sites:
    print("     %-56s line %-5s %s"
          % (path, lineno,
             "refuted" if not (path, lineno) in
             [(p, ln) for p, ln in head_live] else "*** LIVE ASSERTION"))
print("   %d copy/copies at HEAD, %d of them live assertions."
      % (len(head_sites), len(head_live)))
R.check(len(head_live) > 0,
        "the discriminator reports 0 live assertions at HEAD, where mg-e34a "
        "booked the finding; it is not distinguishing a quotation from an "
        "assertion and the row above says nothing")
print()
for label, needle in (("the new reason", NEW_A), ("the row's LABEL", NEW_B)):
    hits = L.grep(needle)
    print("   %s -- `%s`: %d site(s)" % (label, needle, len(hits)))
    for path, lineno in hits:
        print("     %-56s line %s" % (path, lineno))
print()
msg = L.commit_message("4755d02")
in_msg = "cancelling pair would pass each half" in msg or OLD in msg
print("   in the COMMIT MESSAGE of 4755d02 : %s -- IMMUTABLE.  A commit "
      "message cannot be\n   repaired without rewriting history, so its "
      "disposition is a POINTER and not a fix:\n   the corrected reason names "
      "4755d02 as the commit that carries the inverted one."
      % ("yes" if in_msg else "no"))
print()
R.gate(not live_old,
       "the inverted reason is still asserted at %d site(s): %s"
       % (len(live_old), ", ".join("%s:%s" % s for s in live_old)))
print()

# ---------------------------------------------------------------------------
L.rule("(ii) THE TWO PAIRS, BUILT AND SHOWN TO BE WHAT THEY ARE CALLED")
print("""   Every bend refuses on zero occurrences and on many, so a bend that
   silently did nothing cannot make a row below say whatever it likes.
   And each pair is verified to be the KIND of pair it is called before
   any row rests on it -- otherwise the six rows below are six readings
   of an input nobody characterised.""")
print()
old_c1 = L.git_show(L.REV_A218, L.C1_REL)
old_kern = L.git_show(L.REV_A218, L.KERN_REL)
head_c1 = L.git_show("HEAD", L.C1_REL)
head_kern = L.git_show("HEAD", L.KERN_REL)
target = L.git_show("HEAD", L.TARGET_REL)

PAIRS = {}
try:
    PAIRS["cancelling"] = (L.bend_c1_down(head_c1), L.bend_kern_up(head_kern))
except ValueError as e:
    R.selferr("the cancelling pair could not be built (%s); its three rows "
              "are DROPPED rather than counted as passing" % e)
try:
    PAIRS["conspiring"] = (L.conspire_c1(head_c1), L.conspire_kern(head_kern))
except ValueError as e:
    R.selferr("the conspiring pair could not be built (%s); its three rows "
              "are DROPPED rather than counted as passing" % e)

for name in sorted(PAIRS):
    c1s, ks = PAIRS[name]
    print("   the %s pair:" % name)
    print("     c1_branching.py : %+d byte(s) against HEAD"
          % (len(c1s) - len(head_c1)))
    print("     kern_a218.py    : %+d byte(s) against HEAD"
          % (len(ks) - len(head_kern)))
print()


def measure(c1s, ks):
    """g1's own measurement: c1's sections (i)+(ii) and its 24 vertex sets."""
    out, _rc = L.run_c1(target, c1s, ks)
    m = L.measuring_half(out)
    return L.sha(m)[:16], L.vertex_cells(out)


ref_sha, ref_v = measure(old_c1, old_kern)
ok_base = R.check(len(ref_v) == 24,
                  "the baseline run produced %d vertex cells, not the 24 c1 "
                  "prints; every comparison below would be against a parse "
                  "and not a measurement, and all six rows are DROPPED"
                  % len(ref_v))
print("   the baseline -- c1 and its kernel both at %s : sha %s, %d cells"
      % (L.REV_A218[:8], ref_sha, len(ref_v)))
print()

# ---------------------------------------------------------------------------
L.rule("(iii) SECTION (v)'S THREE ROWS, ON EACH PAIR")
print("""   The same three (script, kernel) rows g1's HALVES uses, with HEAD
   carrying each pair in turn.  Each is diffed against the baseline
   exactly as g1 diffs it.

   WHAT THE CORRECTED REASON CLAIMS, and it is two claims:

     CANCELLING  both HALF rows MOVE, `both together` IDENTICAL
     CONSPIRING  both HALF rows IDENTICAL, `both together` MOVES

   The first is why the old reason was inverted.  The second is why the
   row is load-bearing anyway, and it is the half nobody had built.""")
print()
verdicts = {}
if ok_base:
    for name in sorted(PAIRS):
        c1s, ks = PAIRS[name]
        rows = [("c1_branching.py", "the script", c1s, head_kern),
                ("kern_a218.py", "its kernel", head_c1, ks),
                ("both together", "conspiracy", c1s, ks)]
        print("   the %s pair" % name.upper())
        print("     %-32s %-16s %-16s %s"
              % ("row", "baseline", "moved", "verdict"))
        v = {}
        for rname, rwhat, rc1, rk in rows:
            s, cells = measure(rc1, rk)
            if not cells:
                R.selferr("the %s / %s run produced no vertex cells; that row "
                          "is DROPPED rather than read as IDENTICAL"
                          % (name, rname))
                continue
            same = (s == ref_sha and cells == ref_v and len(cells) == 24)
            v[rname] = same
            print("     %-32s %-16s %-16s %s"
                  % (rname + " (%s)" % rwhat, ref_sha, s,
                     "IDENTICAL" if same else "MOVED"))
        verdicts[name] = v
        print()

    # -- the pairs are what they are called ---------------------------------
    can = verdicts.get("cancelling", {})
    con = verdicts.get("conspiring", {})
    R.check(can.get("c1_branching.py") is False
            and can.get("kern_a218.py") is False,
            "the `cancelling` pair's halves do not both move, so it is not a "
            "pair of individually-visible changes and the row it is read "
            "against says nothing")
    R.check(con.get("c1_branching.py") is True
            and con.get("kern_a218.py") is True,
            "the `conspiring` pair's halves are not both no-ops, so it is not "
            "a conspiring pair and the row it is read against says nothing")

    print("   THE CORRECTED REASON, SCORED AGAINST BOTH PAIRS")
    print("     %-14s %-12s %-12s %-14s %s"
          % ("pair", "c1 half", "kern half", "both together", "reason says"))
    for name, expect in (("cancelling", "halves catch it"),
                         ("conspiring", "only `both together` catches it")):
        v = verdicts.get(name, {})
        print("     %-14s %-12s %-12s %-14s %s"
              % (name,
                 "IDENTICAL" if v.get("c1_branching.py") else "MOVED",
                 "IDENTICAL" if v.get("kern_a218.py") else "MOVED",
                 "IDENTICAL" if v.get("both together") else "MOVED",
                 expect))
    print()
    cancel_ok = (can.get("c1_branching.py") is False
                 and can.get("kern_a218.py") is False
                 and can.get("both together") is True)
    conspire_ok = (con.get("c1_branching.py") is True
                   and con.get("kern_a218.py") is True
                   and con.get("both together") is False)
    R.gate(cancel_ok,
           "the corrected reason's FIRST half does not hold: a cancelling "
           "pair was measured as c1 %s / kern %s / both together %s, and the "
           "sentence now in g1 says both halves MOVE and `both together` "
           "prints IDENTICAL"
           % ("IDENTICAL" if can.get("c1_branching.py") else "MOVED",
              "IDENTICAL" if can.get("kern_a218.py") else "MOVED",
              "IDENTICAL" if can.get("both together") else "MOVED"))
    R.gate(conspire_ok,
           "the corrected reason's SECOND half does not hold: a conspiring "
           "pair was measured as c1 %s / kern %s / both together %s, and the "
           "sentence now in g1 says both halves print IDENTICAL and `both "
           "together` MOVES.  Without this half the row has no input it "
           "catches alone and the finding would be against the row after all"
           % ("IDENTICAL" if con.get("c1_branching.py") else "MOVED",
              "IDENTICAL" if con.get("kern_a218.py") else "MOVED",
              "IDENTICAL" if con.get("both together") else "MOVED"))
    print()
    print("""   AND SECTION (v) AS A WHOLE CATCHES BOTH, which is why
   r1_kernel.py's OTHER sentence -- "a cancelling pair cannot pass" --
   is TRUE and is left standing.  It is a claim about the section; the
   repaired one is a claim about which ROW.  Scored here rather than
   taken from mg-e34a, which named it as excluded by hand.""")
    print()
    for name in sorted(verdicts):
        v = verdicts[name]
        caught = [r for r in v if not v[r]]
        print("     %-12s caught by section (v) at %d of 3 rows: %s"
              % (name, len(caught), ", ".join(caught) or "NONE"))
        R.gate(bool(caught),
               "a %s pair passes ALL THREE rows of section (v), so the "
               "section does not catch it at any grain and `a cancelling pair "
               "cannot pass` is false too" % name)
print()

L.finish(R)
