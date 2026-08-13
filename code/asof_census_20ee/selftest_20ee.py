#!/usr/bin/env python3
"""mg-20ee — CONTROLS ON THE CENSUS CLASSIFIER, run before its number is quoted.

mg-9876's sweep is right to flag a directory that ships code and no control:
a directory with neither has no evidence its instrument can fail, which is
weaker than saying it cannot.  This census's ENTIRE claim is that it counts the
right things, and an uncontrolled classifier reporting `125` is an assertion.

So each of the classifier's three conditions is exercised in BOTH directions on
a planted corpus -- a case it must catch, and a case it must NOT.  The negative
controls matter more than the positives here, because the declared bias of this
census is that it OVER-counts: a classifier that fires on everything would
report a large number and look thorough.

N4 is the one that earns its place.  It plants the exact shape this census was
found to miscount -- an instrument that ALREADY reads its corpus at a declared
commit -- and asserts that the classifier COUNTS IT ANYWAY.  That is a control
that CONFIRMS A KNOWN DEFECT rather than a repair, and it is kept in that form
deliberately: the bias is declared in census.py and in out_ground_truth.txt, and
a control that quietly passed would hide it.  If somebody teaches the classifier
to see pinned reads, N4 FAILS and that is the signal to update both declarations.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import census  # noqa: E402

FAILED = []


def check(name, got, want, why):
    ok = got == want
    print("  %-4s %-52s %s" % ("PASS" if ok else "FAIL", name,
                               "" if ok else "got %r, want %r" % (got, want)))
    print("        %s" % why)
    if not ok:
        FAILED.append(name)


def classify(transcript_text, instrument_src, owner, tracked_paths):
    """The classifier's three conditions, applied exactly as census.main does.

    Deliberately a re-statement rather than an import: census.main is welded to
    `git show`, and a control that could only run against the real repository
    could not plant a corpus at all.  The conditions below are the ones the
    docstring states, and any drift between the two is itself a finding.
    """
    tracked = set(tracked_paths)
    hits = []
    for m in census.ADDR.finditer(transcript_text):
        token, path = m.group(0), m.group(1)
        tgt = path if path in tracked else None
        if tgt is None:
            cand = os.path.normpath(os.path.join(owner, path))
            tgt = cand if cand in tracked else None
        if tgt is None or os.path.dirname(tgt) == owner:
            continue
        if token in instrument_src:
            continue
        base = os.path.basename(tgt)
        if not (tgt in instrument_src or base in instrument_src
                or base.rsplit(".", 1)[0] in instrument_src
                or os.path.dirname(tgt) in instrument_src):
            continue
        hits.append(tgt)
    return hits


OWNER = "code/inst_x"
TRACKED = ["code/inst_x/out_a.txt", "code/inst_x/a.py",
           "docs/FOREIGN.md", "code/inst_y/other.py"]

print("=" * 78)
print("mg-20ee — CONTROLS ON THE CENSUS CLASSIFIER")
print("=" * 78)
print()
print("POSITIVE CONTROLS — shapes the classifier MUST count")
print("-" * 78)

check("P1 computed address into a foreign doc",
      classify("see docs/FOREIGN.md:12 for the row",
               "text = read('docs/FOREIGN.md')", OWNER, TRACKED),
      ["docs/FOREIGN.md"],
      "the instrument reads the file and the token is not in its source — the "
      "defect mg-20ee repairs.")

check("P2 computed address into another instrument's source",
      classify("code/inst_y/other.py:88 defines it",
               "scan('code/inst_y/other.py')", OWNER, TRACKED),
      ["code/inst_y/other.py"],
      "foreignness is about the OWNING DIRECTORY, not about the file extension.")

print()
print("NEGATIVE CONTROLS — shapes it MUST NOT count.  These carry the weight,")
print("because the declared bias of this census is that it OVER-counts.")
print("-" * 78)

check("N1 an address into the instrument's OWN directory",
      classify("code/inst_x/out_a.txt:4 says so",
               "read('code/inst_x/out_a.txt')", OWNER, TRACKED),
      [],
      "not foreign, so not this defect: the instrument owns what it addresses "
      "and nobody else can move it under it.")

check("N2 a HARDCODED citation, token present in the source",
      classify("as docs/FOREIGN.md:12 records",
               "print('as docs/FOREIGN.md:12 records')", OWNER, TRACKED),
      [],
      "a stale-citation hazard and a DIFFERENT repair — pinning the corpus "
      "would not fix a number typed by hand.")

check("N3 a file the instrument never reads",
      classify("docs/FOREIGN.md:12", "nothing relevant here", OWNER, TRACKED),
      [],
      "an echo of someone else's prose citation, not a computed address.")

check("N4 an untracked path",
      classify("/elsewhere/probe.py:7", "read('/elsewhere/probe.py')",
               OWNER, TRACKED),
      [],
      "UNDER-COUNT, DECLARED AND CONFIRMED: addresses outside this repository "
      "are invisible to git and so to this census. a4_census's mg-3ce3 probe "
      "is one such. The floor is real and this control is why it is a floor.")

print()
print("THE CONTROL THAT CONFIRMS A KNOWN DEFECT RATHER THAN A REPAIR")
print("-" * 78)

check("N5 an instrument that ALREADY reads at a declared commit",
      classify("docs/FOREIGN.md:12 at the pinned rev",
               "git('show', AS_OF + ':docs/FOREIGN.md')", OWNER, TRACKED),
      ["docs/FOREIGN.md"],
      "COUNTED ANYWAY — this is the census's second declared over-count, "
      "planted so it cannot be forgotten. code/state_audit_6a2f is the real "
      "instance. If somebody teaches the classifier to see pinned reads this "
      "control FAILS, and that is the signal to update census.py's docstring "
      "and out_ground_truth.txt together.")

print()
print("CONTROLS ON consumers.py — mg-20ee's THIRD CONDITION (mg-6e4f)")
print("-" * 78)
print()
print("  The consumer census decides, for a file that NAMES a script, whether")
print("  it EXECUTES it and whether it passes a path.  A pin disturbs the")
print("  no-arg callers and not the others, so the whole value of the")
print("  instrument is in telling those three apart.  Planted lines, because a")
print("  classifier only ever run against the real corpus has no evidence it")
print("  can distinguish anything.")
print()

import consumers  # noqa: E402


def kinds(text, needle="w3_scope.py"):
    return [k for k, _n, _l in consumers.classify_text(text, needle)]


check("C1 an exec with no path argument",
      kinds('    rc, out = run_checker("code/a/w3_scope.py")'),
      ["EXEC-NO-ARG"],
      "the shape that GETS the pinned default and must be re-measured. "
      "kern6cb9.py, kern4700.py and v2_layer2.py are the real instances.")

check("C2 an exec that passes a scratch path",
      kinds('    r = subprocess.run([sys.executable, "w3_scope.py", scratch])'),
      ["EXEC-EXPLICIT-PATH"],
      "the caller chose the tree, so the pin does not reach it. MEASURED on "
      "the real instance: species_audit_73df/c4_scope.py is byte-identical "
      "with and without the pin.")

check("C3 a name with no exec token near it",
      kinds('CHECKERS = [("w3_scope.py", "code/a/w3_scope.py")]'),
      ["MENTION"],
      "THE CONTROL THAT CONFIRMS A KNOWN DEFECT RATHER THAN A REPAIR. This "
      "is e1_extents.py's real line. E1 DOES execute it -- through two "
      "variables and a tracer -- and this census CANNOT SEE THAT. It lands "
      "in the residue, and section C's work-list is C1 PLUS C2 for exactly "
      "this reason. If somebody teaches the rule to follow variables, this "
      "control FAILS, and that is the signal to update the docstring's "
      "blind-spot list and section C's warning together. DO NOT `FIX` THIS "
      "CONTROL BY MAKING THE CENSUS PASS IT: a control that confirms a DEFECT "
      "rather than a repair is unusual, and the failing case IS the assertion. "
      "It is here in the form N4 and N5 already use one directory up, for the "
      "same reason -- a declared bias that no control holds in place is a "
      "sentence that goes quietly false.")

check("C4 the exec token may stand on a LATER line",
      kinds('    p = subprocess.run(\n        [sys.executable, "w3_scope.py"])'),
      ["EXEC-NO-ARG"],
      "a two-line call is the common formatting in this repository and a "
      "same-line-only rule would have reported half the estate as inert.")

print()
print("THE CONTROL FOR THE CRASH THAT MADE THIS CENSUS UNUSABLE (mg-4020)")
print("-" * 78)
print()
print("  `git grep` exits 1 for NO MATCH and 2+ for a real error, and this")
print("  census read every non-zero as fatal.  So a subject script that")
print("  nothing outside its own directory names -- a library, a numbered")
print("  step, or ANY run_all.sh, since a shared basename is searched by full")
print("  path -- took the whole run down.  MEASURED: it died on 23 of the 27")
print("  instruments still on mg-20ee's pinning work-list, and ran on 4, one")
print("  of which is the single subject it was built against.  The evidence")
print("  that it worked came entirely from the one directory where every")
print("  script happened to be named elsewhere.")
print()

check("C5 a needle nothing outside the subject names",
      consumers.git_grep_l("zzz_no_such_script_mg4020.py", ("*.py", "*.sh")),
      [],
      "FINDING NOTHING IS AN ANSWER, and it is the ordinary answer for a "
      "library or a numbered step. Before this it was a crash, after a "
      "correct-looking header had already printed.")

_narrow = "no SystemExit -- rc>=2 was swallowed"
try:
    consumers.git_grep_l("x", (":(bogus)x",))
except SystemExit:
    _narrow = "SystemExit"

check("C6 a REAL git error is still fatal",
      _narrow, "SystemExit",
      "THE NEGATIVE HALF, AND IT CARRIES THE WEIGHT. Widening the tolerance "
      "to `any non-zero means empty` would turn a bad pathspec or a broken "
      "index into a census of nothing that reports `none` in section A -- "
      "which reads exactly like a subject no instrument consumes. Only rc 1 "
      "is no-match; rc 2 and above stays fatal.")

print()
print("=" * 78)
if FAILED:
    print("RED — %d control(s) failed: %s" % (len(FAILED), ", ".join(FAILED)))
else:
    print("GREEN — 2 positive, 4 negative and 1 known-defect control on the "
          "address census, and 3 positive, 1 known-defect and 2 rc-tolerance "
          "controls on the consumer census, all land where they must.")
print("=" * 78)
raise SystemExit(1 if FAILED else 0)
