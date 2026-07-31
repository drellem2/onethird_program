"""j5_doccheck.py -- EVERY FIGURE IN THIS AUDIT'S DOCUMENT, GATED AT ITS SITE.

A document that asserts figures no instrument reads is the shape mg-8aae found
and mg-9207 found again: a summary sitting beside rows that refute it.  So every
number in docs/audit-mg-957f-attribution-and-the-kernel.md is read back OUT of
the committed out_j*.txt and required to appear AT ITS OWN SITE -- inside the
window of text a reader meets it in, not merely somewhere in the file.

And each gate is deletion-tested WHERE IT STANDS: the figure is bumped inside
that window and the gate must go red, with the unbumped window green beside it.
A gate that cannot fail has not checked anything.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import os
import re
import sys

import lib957f as L

R = L.Report("j5", "every figure gated below (one finding each), plus one "
                   "corruption probe and one null probe per gate")

L.banner("J5", "EVERY FIGURE IN THIS AUDIT'S DOCUMENT, READ AT ITS OWN SITE")

HERE = os.path.dirname(os.path.abspath(__file__))
DOC_REL = "docs/audit-mg-957f-attribution-and-the-kernel.md"
DOC = L.read_worktree(DOC_REL)

OUTS = {}
for name in ["selftest_957f", "j1_attribution", "j2_silencing",
             "j3_setlevel", "j4_reproduce"]:
    p = os.path.join(HERE, "out_%s.txt" % name)
    if not os.path.isfile(p):
        R.selferr("out_%s.txt is not committed beside this script; every gate "
                  "that reads it is DROPPED from the population rather than "
                  "counted as passing" % name)
        continue
    with open(p) as fh:
        OUTS[name] = fh.read()


def grab(src, pattern, group=1):
    """One figure, out of one committed transcript."""
    m = re.search(pattern, OUTS.get(src, ""))
    return m.group(group) if m else None


# label, which out_j*.txt, how to read the figure, the doc site anchor (which
# must NOT itself contain the figure), and the template the figure must appear
# in inside that site's window.
GATES = [
    ("self-test assertions", "selftest_957f", r"ASSERTIONS: (\d+)",
     "five scripts plus a", "**%s-assertion**"),
    ("attributions AGREES", "j1_attribution", r"AGREES\s+:\s+(\d+)",
     "that `g1` or `g4` prints —", "**%s**"),
    ("attributions WRONG COMMIT", "j1_attribution",
     r"WRONG COMMIT\s+:\s+(\d+)",
     "**17 AGREES /", "%s WRONG COMMIT"),
    ("attributions UNVERIFIABLE", "j1_attribution",
     r"UNVERIFIABLE\s+:\s+(\d+)",
     "**17 AGREES /", "%s UNVERIFIABLE"),
    ("two routes agreeing", "j1_attribution",
     r"THE TWO ROUTES AGREE at (\d+) of \d+ members",
     "they agree at", "**%s of 5**"),
    ("history clones following", "j1_attribution",
     r"followed the history: (\d+) of \d+",
     "| a commit touching **nothing** among the five (null probe) |",
     "**%s of 3.**"),
    ("disposition sites", "j2_silencing",
     r"sites stating the disposition: (\d+) of \d+",
     "demanded is stated at", "**%s of 3** sites"),
    ("c1 clone directions", "j2_silencing",
     r"c1 clones whose direction was predicted correctly: (\d+) of \d+",
     "| a line appended past `c1`'s section (iii) | exit 0 | **exit 0** | 0 / 0 |",
     "**%s of 4.**"),
    ("cells the bent kernel moves", "j2_silencing",
     r"the measurement MOVES -- (\d+) of 24 vertex cells move",
     "does the bend really move `c1`'s measurement?", "**%s of 24** vertex"),
    ("the pinned measurement sha", "j2_silencing",
     r"with kern @ HEAD   : sections \(i\)\+\(ii\) sha ([0-9a-f]{16})",
     "does the bend really move `c1`'s measurement?", "`%s`"),
    ("the bent measurement sha", "j2_silencing",
     r"with kern BENT     : sections \(i\)\+\(ii\) sha ([0-9a-f]{16})",
     "does the bend really move `c1`'s measurement?", "`%s`"),
    ("g1 return sites before", "j2_silencing",
     r"g1 @ ef388417 : (\d+) return sites",
     "begins `finding(` or\n`selferr(`:", "**%s before"),
    ("g1 return sites after", "j2_silencing",
     r"g1 @ HEAD     : (\d+) return sites",
     "begins `finding(` or\n`selferr(`:", "%s after**"),
    ("pairs agreeing at all cells", "j3_setlevel",
     r"pairs agreeing at all 24 cells : (\d+) of \d+",
     "| pairs of sources agreeing at all 24 cells |", "**%s of 10**"),
    ("cell comparisons", "j3_setlevel",
     r"cell comparisons made\s+: (\d+)",
     "| cell comparisons made |", "**%s**"),
    ("members re-run", "j3_setlevel",
     r"members re-run : (\d+) of \d+",
     "| `mg-a218`'s members re-run in place |", "**%s of 5**"),
    ("members green", "j3_setlevel",
     r"members green  : (\d+) of \d+", "| members green |", "**%s of 5**"),
    ("locality probes", "j3_setlevel",
     r"own cell and no other : (\d+) of \d+",
     "| readers moving at their own cell and no other |", "**%s of 5**"),
    ("mg-321d finder directions", "j3_setlevel",
     r"mg-321d finders whose direction was predicted correctly: (\d+) of 5",
     "| `h5_doccheck.py` | 0 findings | **0** |", "**%s of 5** directions"),
    ("outputs that reproduce", "j4_reproduce",
     r"byte: (\d+) of \d+\.  Population",
     "| `out_g4_fleet.txt` | **no** | 2 |", "**%s of 5.**"),
    ("g1 HEAD-print sites after", "j4_reproduce",
     r"g1_provenance\.py       print\(\.\.\. HEAD\[:8\] \.\.\.\) \d+\s+(\d+)",
     "arguments include `HEAD[:8]`:", "**2 \u2192 %s**"),
    ("g4 HEAD-print sites after", "j4_reproduce",
     r"g4_fleet\.py            print\(\.\.\. HEAD\[:8\] \.\.\.\) \d+\s+(\d+)",
     "arguments include `HEAD[:8]`:", "**0 \u2192 %s**"),
]

print("   gate                              figure  at its site  null  bumped")
print("   " + "-" * 68)
ngate = ok_site = ok_null = ok_bump = 0
WINDOW = 140
for label, src, pat, anchor, tmpl in GATES:
    if src not in OUTS:
        R.selferr("gate %r reads out_%s.txt, which is absent; the gate is "
                  "DROPPED from the population rather than counted as passing"
                  % (label, src))
        continue
    fig = grab(src, pat)
    if fig is None:
        R.selferr("gate %r could not read its figure out of out_%s.txt with "
                  "%r; the gate is DROPPED rather than counted as passing"
                  % (label, src, pat))
        continue
    if anchor not in DOC:
        R.finding("the document does not carry the site %r that gate %r is "
                  "aimed at, so the figure %s is not gated anywhere"
                  % (anchor[:40], label, fig))
        continue
    ngate += 1
    i = DOC.index(anchor)
    win = DOC[i:i + len(anchor) + WINDOW]
    want = tmpl % fig
    at_site = want in win
    # the deletion test, AT THE SITE: bump the figure inside this window only
    bumped_fig = str(int(fig) + 7) if fig.isdigit() else fig[:-1] + "0"
    bumped_win = win.replace(want, tmpl % bumped_fig, 1)
    null_green = want in win
    bump_red = want not in bumped_win
    ok_site += at_site
    ok_null += null_green
    ok_bump += bump_red
    print("     %-33s %-7s %-12s %-5s %s"
          % (label[:33], fig, "yes" if at_site else "NO",
             "green" if null_green else "RED",
             "red" if bump_red else "GREEN -- VACUOUS"))
    R.check(at_site, "the document's site %r does not carry %r, which is what "
                     "out_%s.txt reports for %s"
            % (anchor[:36], want, src, label))
    R.check(bump_red,
            "the gate on %s is vacuous: bumping the figure at its own site "
            "leaves the gate green" % label)

print()
print("   gates: %d.  Population: every figure in %s that any out_j*.txt "
      "reports -- each located by a site string taken from the document and "
      "checked inside that site's own window, never file-wide."
      % (ngate, DOC_REL))
print("     figures present at their own site : %d of %d" % (ok_site, ngate))
print("     null probes green                 : %d of %d" % (ok_null, ngate))
print("     corruption probes red             : %d of %d" % (ok_bump, ngate))
print()

# ---------------------------------------------------------------------------
L.rule("AND THE FINDINGS THEMSELVES, NOT ONLY THE NUMBERS")
print("""   Two findings are claimed.  Each must be the finding an out_j*.txt
   actually carries, matched on its own opening words rather than on a count.""")
print()
CLAIMED = [("F-1", "j2_silencing", "COVERAGE LOST IN THE REPAIR"),
           ("F-2", "j4_reproduce", "G-3 IS NOT SHUT, IT IS SHUT AT ONE "
                                   "REVISION")]
for tag, src, opening in CLAIMED:
    got = [x for x in L.findings_of(OUTS.get(src, "")) if x.startswith(opening)]
    print("     %-5s %-16s %s" % (tag, src, "present" if got else "ABSENT"))
    R.check(bool(got), "this audit claims %s but out_%s.txt carries no finding "
                       "opening %r" % (tag, src, opening))
totals = {}
for src in OUTS:
    s, f = L.totals_of(OUTS[src])
    totals[src] = (s, f)
print()
print("   committed transcript   self  findings")
for src in ["j1_attribution", "j2_silencing", "j3_setlevel",
            "j4_reproduce"]:
    if src in totals:
        print("     %-20s %-5s %s" % (src, totals[src][0], totals[src][1]))
tot = sum(f for k, (s, f) in totals.items()
          if f is not None and k != "selftest_957f")
print("   findings across the committed transcripts: %d.  Population: the 4 "
      "out_j*.txt read above; out_selftest_957f.txt reports ASSERTIONS and "
      "not FINDINGS and is not in it." % tot)
R.check(tot == 2, "this audit's document claims exactly 2 findings and its "
                  "committed transcripts carry %d" % tot)
print()

sys.exit(R.emit())
