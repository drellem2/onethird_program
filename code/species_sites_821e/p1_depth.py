"""P1 -- OPEN 1: "EVERY REGULAR FILE" IS NOW TRUE BY CONSTRUCTION.

mg-6cb9's F1, MAJOR, and it named a flavour worth keeping: a claim that is
MEASURED, TRUE, and CONTINGENT ON A CONDITION NOBODY STATED.  `s1_extent.py`
and `w3_scope.py` printed "EVERY REGULAR FILE in each tree is read -- there is
no extension rule"; both walked with a single `os.listdir` and a `continue`
past anything that is not `os.path.isfile`.  The sentence was true, and true
for exactly one reason: no tree under `code/species_*` contains a directory.
It would have gone false silently, with the run green, the day somebody added
one.  And `e1_extents.py` -- whose entire job is deciding whether a printed
extent is true -- listed the same way, so it certified the sentence over a file
it also could not see (mg-6cb9 Q10, Q17, Q17e).

THE BRIEF OFFERED TWO REPAIRS AND THIS IS THE FIRST ONE.  "Either make the walk
actually recurse, so the claim is true by construction, or state the condition
in the extent."  Stating it would have left the tree carrying a promise -- `no
subdirectories present` -- that nothing in this repository can keep, and the
next person to add a directory would have had to notice a sentence.  All three
walks now recurse.  ONE directory rule survives, `__pycache__`, and it is
printed in both extent lines rather than left to be inferred from the code.

  P1a  the probes: INSIDE the claimed extent must FIRE, OUTSIDE must be silent.
  P1b  THE DELETION TEST, one line per site, each declaring what it removes.
  P1c  E1 no longer shares the blind spot -- the guard that did not exist.

    python3 code/species_sites_821e/p1_depth.py
"""

import os
import sys

from kern821e import (hdr, REPO, git_status, Probe, run_checker, flat,
                      replace_once, NO_RECURSE)

bad = 0

W3 = "code/species_remainder_f8fa/w3_scope.py"
S1 = "code/species_repair_a4ef/s1_extent.py"
E1 = "code/species_extent_d633/e1_extents.py"

PAD = "\n" * 9

# The source-code spellings the checkers actually match, each avoiding its own
# row's exoneration regex.  Taken from the checkers' own pattern tables, not
# from the document: `stricken_a4ef.py` matches ASCII `<=`, not `≤`.
X1_SRC = ("Smallest witness with AC(P) != Pi[n]: P = {a<c, b<d}, where ad|bc "
          "has a 2-cycle.")
X3_SRC = ("T5 passes every Hopf-monoid axiom with 0 failures on 4399 basis "
          "elements.")
X4_SRC = "Of the four columns, three are controls, and they fire."


def payload(body):
    """A planted block padded well clear of every exoneration window in this
    arc -- kerna4ef's is 6 lines, w3_scope's is 4 -- and marked with a ticket
    id no exoneration rule in this repository matches."""
    return PAD + "<!-- 821e probe -->\n" + PAD + body.strip() + "\n" + PAD


NR = {name: (rel, a, b) for name, rel, a, b in NO_RECURSE}


def unrecurse(name):
    rel, a, b = NR[name]
    return (rel, replace_once(a, b))


PROBES = [
    # id, checker, direction, what, expected exit, edits
    ("P0a", W3, "-", "unmutated", 0, []),
    ("P0b", S1, "-", "unmutated", 0, []),
    ("P0c", E1, "-", "unmutated", 0, []),

    ("P1", W3, "IN", "X4 one level down: species_7d75/sub/leak.md", 1,
     [("code/species_7d75/sub/leak.md", lambda _o: payload(X4_SRC))]),
    ("P2", S1, "IN", "X3 one level down: species_7d75/sub/leak.md", 1,
     [("code/species_7d75/sub/leak.md", lambda _o: payload(X3_SRC))]),
    ("P3", S1, "IN", "X1 TWO levels down, another tree: a4ef/sub/deep/n.md", 1,
     [("code/species_repair_a4ef/sub/deep/n.md",
       lambda _o: payload(X1_SRC))]),
    ("P4", S1, "IN", "X1 in an EXTENSIONLESS file in a subdirectory", 1,
     [("code/species_repair_6f61/sub/NOTES", lambda _o: payload(X1_SRC))]),
    ("P5", S1, "IN", "X1 in sub/PREDICTIONS.md -- EXCLUDE is not a basename",
     1, [("code/species_repair_a4ef/sub/PREDICTIONS.md",
          lambda _o: payload(X1_SRC))]),

    ("P6", S1, "OUT", "X1 under __pycache__ -- the ONE stated directory rule",
     0, [("code/species_7d75/__pycache__/leak.md",
          lambda _o: payload(X1_SRC))]),
    ("P7", S1, "OUT", "X1 in a subdirectory of a tree S1 DISCLAIMS", 0,
     [("code/species_extent_d633/sub/leak.md", lambda _o: payload(X1_SRC))]),
    ("P8", W3, "OUT", "X4 in a subdirectory of ANOTHER tree", 0,
     [("code/species_repair_a4ef/sub/leak.md", lambda _o: payload(X4_SRC))]),
    ("P9", S1, "OUT", "a named exclusion at the ROOT still excluded", 0,
     [("code/species_repair_a4ef/PREDICTIONS.md",
       lambda o: o.rstrip("\n") + "\n\n" + payload(X1_SRC))]),

    # The deletion test, as probes: the same plant with the recursion removed.
    ("P10", W3, "DEL", "P1's plant, with w3_scope.py's descent line removed",
     0, [("code/species_7d75/sub/leak.md", lambda _o: payload(X4_SRC)),
         unrecurse("w3_scope.py")]),
    ("P11", S1, "DEL", "P2's plant, with s1_extent.py's descent line removed",
     0, [("code/species_7d75/sub/leak.md", lambda _o: payload(X3_SRC)),
         unrecurse("s1_extent.py")]),

    # E1: the guard that did not exist.
    ("P12", E1, "GUARD",
     "a subdirectory planted and S1 NOT recursing -- E1 must catch it", 1,
     [("code/species_7d75/sub/leak.md", lambda _o: payload(X3_SRC)),
      unrecurse("s1_extent.py")]),
    ("P13", E1, "GUARD",
     "the same, with W3 not recursing -- E1 must catch that too", 1,
     [("code/species_7d75/sub/leak.md", lambda _o: payload(X4_SRC)),
      unrecurse("w3_scope.py")]),
    ("P14", E1, "GUARD",
     "a subdirectory planted, everything recursing -- nothing is false", 0,
     [("code/species_7d75/sub/leak.md", lambda _o: payload(X3_SRC))]),
    ("P15", E1, "GUARD",
     "E1's OWN descent line removed: it must not certify what it cannot see",
     1, [("code/species_7d75/sub/leak.md", lambda _o: payload(X3_SRC)),
         unrecurse("e1_extents.py")]),
]


hdr("P1a  EVERY PROBE, PREDICTED EXIT FIRST")
print("  `exp` was written into PREDICTIONS.md before any of this ran.")
print("  IN    = inside what the printed extent claims -> must FIRE (exit 1).")
print("  OUT   = outside it, or under the one stated directory rule -> 0.")
print("  DEL   = the deletion test: the same plant with the ONE line that")
print("          makes the walk descend removed.  Must go SILENT again, or")
print("          the repair is not what is doing the work.")
print("  GUARD = run against `e1_extents.py`, whose exit 1 means AN EXTENT")
print("          LINE IS FALSE.  Its polarity is the opposite of a checker's.")
print()
print("  %-6s %-16s %-6s %-50s %-4s %-4s %s"
      % ("id", "checker", "dir", "mutation", "exp", "got", "verdict"))

BASE = git_status()
results, outputs = {}, {}
for pid, checker, direction, what, expect, edits in PROBES:
    with Probe(edits):
        code, out = run_checker(checker)
    after = git_status()
    if after != BASE:
        print("\n*** THE RESTORE DID NOT RESTORE -- stopping.  probe %s" % pid)
        print(after)
        sys.exit(2)
    results[pid], outputs[pid] = code, out
    ok = (code == expect)
    bad += (not ok)
    print("  %-6s %-16s %-6s %-50s %-4d %-4d %s"
          % (pid, os.path.basename(checker), direction, what[:50], expect,
             code, "as predicted" if ok else "*** MISSED ***"))
print()

ins = [p for p in PROBES if p[2] == "IN"]
outs = [p for p in PROBES if p[2] == "OUT"]
dels = [p for p in PROBES if p[2] == "DEL"]
gds = [p for p in PROBES if p[2] == "GUARD"]
print("  INSIDE  %d of %d fired      (mg-6cb9 measured 0 of 2 at these sites)"
      % (sum(1 for p in ins if results[p[0]] == 1), len(ins)))
print("  OUTSIDE %d of %d silent"
      % (sum(1 for p in outs if results[p[0]] == 0), len(outs)))
print("  DELETED %d of %d went silent again"
      % (sum(1 for p in dels if results[p[0]] == 0), len(dels)))
print("  GUARD   %d of %d as predicted"
      % (sum(1 for p in gds if results[p[0]] == p[4]), len(gds)))
print()


# ---------------------------------------------------------------------------
# P1b  the extent line says what the code does
# ---------------------------------------------------------------------------
hdr("P1b  THE PRINTED SENTENCE, AND THE ONE RULE THAT SURVIVES")

code_s1, out_s1 = run_checker(S1)
code_w3, out_w3 = run_checker(W3)
for label, out, needles in [
    ("s1_extent.py", out_s1,
     ["AT ANY DEPTH", "no depth rule", "__pycache__"]),
    ("w3_scope.py", out_w3,
     ["AT ANY DEPTH", "no depth rule", "__pycache__"]),
]:
    for n in needles:
        ok = n.lower() in out.lower()
        bad += (not ok)
        print("  %-16s says %-32s %s"
              % (label, "'%s'" % n, "ok" if ok else "*** DOES NOT ***"))
print()
print("  The point of P1b is that the surviving rule is CARRIED BY A SENTENCE.")
print("  mg-6cb9's finding was not that a rule existed -- it was that the rule")
print("  was in the code and in no sentence, so the claim rested on a")
print("  condition of the tree that nobody had stated.  One rule is left and")
print("  it is printed; P6 is the probe that shows it is real.")
print()


# ---------------------------------------------------------------------------
# P1c  what mg-6cb9's own instrument will say now
# ---------------------------------------------------------------------------
hdr("P1c  mg-6cb9's OWN ROWS, AND ONE OF THEM WILL STILL READ RED")

print("  Q10 and Q17 planted X4 and X3 in `code/species_7d75/sub/leak.md` and")
print("  got exit 0.  P1 and P2 are the same plants: %d and %d."
      % (results["P1"], results["P2"]))
print()
print("  Q17e is different and this file says so rather than leaving it to be")
print("  discovered.  It plants the same subdirectory and runs `e1_extents.py`,")
print("  and mg-6cb9 scores a WIDE row as good ONLY when the exit is 1.  That")
print("  polarity is right for a checker and inverted for a CHECKER OF")
print("  CHECKERS: E1 exits 1 when an extent line is FALSE.  With the walks")
print("  repaired no extent line is false, so Q17e's exit is 0 -- P14 above,")
print("  predicted 0 -- and mg-6cb9's table will print `*** EXTENT WIDER ***`")
print("  against a tree where the extent is true.  THAT LABEL IS THAT")
print("  INSTRUMENT'S SCORING, NOT A SURVIVING DEFECT, and the way to tell the")
print("  two apart is P12/P13/P15: with a walk put back to non-recursive, E1")
print("  exits %d, %d and %d.  It could not do that before this ticket, which"
      % (results["P12"], results["P13"], results["P15"]))
print("  is precisely what Q17e found.")
print()

print("=" * 78)
print("P1 TOTAL BAD: %d" % bad)
print("=" * 78)
print()
print("EXTENT OF THIS NUMBER.  %d probes over THREE files -- `w3_scope.py`,"
      % len(PROBES))
print("`s1_extent.py` and `e1_extents.py` -- each one mutation applied to the")
print("REAL worktree and undone, with `git status --porcelain` compared before")
print("and after every probe.  It says NOTHING about `check_doc.py` (P2 is its")
print("file), about `s2_seam.py` or `e2_crosssection.py` (P3 is theirs), and")
print("nothing about any tree other than the four `s1_extent.py` names and the")
print("one `w3_scope.py` names.  Depth is tested to TWO levels and to an")
print("extensionless file; it is not tested against a symlink, a device node")
print("or a directory the walk cannot read, and those are not claimed.")
sys.exit(1 if bad else 0)
