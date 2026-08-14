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
import collections
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)

import census  # noqa: E402

FAILED = []
RAN = []

# The controls that assert a DEFECT or a LIMIT rather than a repair.  Named
# rather than counted, because which ones they are is the load-bearing fact --
# each says in its own text what it would mean if it ever went the other way,
# and N18 is absent from this list for the first time: mg-e5f3 repaired what
# it asserted, which is the event its own text asked to be told about.
#
# N25 joined it at mg-44da, and it was found by WRITING ANOTHER CONTROL rather
# than by reading: N24's first draft asserted find(1)'s guard with a subject
# spelled as a LIST, the pair came back (False, False), and the reason is that
# R3's find half could not see that spelling at all.  A control that fails for a
# reason its author did not predict is the cheapest finding in this directory.
#
# N25 LEAVES AT mg-23af AND N27 TAKES ITS PLACE, so this tuple TURNS OVER rather
# than shrinking, and that is deliberate: the repair for an under-count left an
# under-count of its own -- a list spelling longer than the 24-character window
# -- and a tranche that repaired the first while quietly dropping the count from
# 5 to 4 would be publishing a smaller number for a defect that moved.
# N28 JOINS AT mg-e8b0 AND NOTHING LEAVES, so this tuple GROWS: the `record
# knows about this pin` rule is a substring count and cannot tell a sentence
# ACCOUNTING for a pin from one OFFERING the same instrument as remaining work.
# ITS LIVE INSTANCE WAS CLOSED IN THE SAME COMMIT -- tranche 1's `the small ones
# ... are cheap` had been offering an instrument this arc pinned at tranche 2,
# for four tranches -- and the control was moved ONTO THE RULE rather than
# dropped, because a control that goes red when somebody closes its instance
# invites the next tranche to `repair` it by re-opening the trap.
# N33 JOINS AT mg-bdc0 AND NOTHING LEAVES, so this tuple GROWS AGAIN (10 -> 11).
# RENUMBERED ON LANDING AND THE MAP IS PRINTED: this branch issued P35-P39 and
# N32, mg-5058's semantic.py landed first with the same six names, and a number
# in this directory is NEVER REISSUED -- so pathlist.py's six became P40, P41,
# P42, P43, P44 and N33, in that order, and not one word of the argument moved.
# That is mg-5058's own resolution one branch later, and the second time in two
# landings that two instruments picked the same six names out of one namespace.
# WHAT N33 ASSERTS: pathlist.py decides what a producer reads by matching
# SPELLINGS, so a read spelled a way its pattern does not name grades that
# producer a PROOF.  It is asserted rather than repaired because the repair is
# unbounded -- there is no closed set of ways to spell a read -- and because its
# DIRECTION is what makes the published figure safe: every error of this kind
# can only make the PATH-LIST-ONLY class look BIGGER, and that class is EMPTY,
# so the 0 in out_pathlist.txt cannot be an over-count.
# N29 AND N30 JOIN AT mg-0bf1 AND NOTHING LEAVES, so this tuple GROWS AGAIN --
# and N28 STAYS, which is the load-bearing part.  mg-0bf1 gives the question a
# mechanical answer that reads no English (a sentence accounting for a pin is
# YOUNGER than the pin), but it does that in a NEW rule in a NEW file:
# worklist.py's `named in this record` is still a substring count, so N28 is
# still true of the field it is asserted on.  What the date buys is an
# IMPOSSIBILITY -- an older sentence CANNOT be an accounting -- and N29 is
# where the limit went rather than where it died: a YOUNGER sentence MIGHT be
# an accounting and need not be, so N28's remedy (THE INSTRUMENT PRINTS THE
# SENTENCE) survives unchanged.  N30 is the complement: an instrument no record
# names at all has no last word and is invisible to the rule at every revision.
# N31 JOINS AT mg-ede8 AND NOTHING LEAVES, so this tuple GROWS AGAIN.  It is the
# limit of the census that answers `was this transcript already stale when it
# was written`: only figures that are a function of the TRACKED PATH LIST can be
# re-derived at a commit without running the instrument there, so a STALE
# verdict is a proof and an AGREES verdict covers four figures out of a
# transcript that has many.  It is asserted on the RULE for N28's reason -- its
# live instances are the content-valued figures, and a control sitting on one of
# those would go red the day somebody found a way to re-derive it.
# N32 JOINS AT mg-5058 AND NOTHING LEAVES, so this tuple GROWS AGAIN.  It is the
# limit of the registry in semantic.py: a row proves that no commit-level rule
# separates its two witnesses BECAUSE they share a commit, and the READINGS the
# two witnesses are given are hand judgements a person wrote into REGISTRY --
# derived from nothing the repository holds.  Asserted on the row that is its
# own instance (R2), because that row's two witnesses agree on every field the
# repository has and disagree only in that sentence.  It was issued as N31 on
# the branch and RENUMBERED ON LANDING: mg-ede8's N31 merged first and a number
# in this directory is never reissued, which is what BURNED is for.
# N34 JOINS AT mg-6b2d AND NOTHING LEAVES, so this tuple GROWS AGAIN (11 -> 12),
# and it is the SAME LIMIT N31 declared, arriving on a different rule.  N31 says
# `was this transcript already stale at its own commit` is answerable only for
# figures a path list determines; N34 says the neighbouring rule -- `has the
# producer moved since` -- is blind in exactly the complementary place, because
# a transcript goes stale when its CORPUS moves and its producer does not.
# THAT IS THE SHAPE out_consumers.txt HAS SHIPPED IN 5 OF ITS 8 VERSIONS, so the
# defect is not hypothetical and the control plants it.  ITS DIRECTION IS WHY
# THE PUBLISHED FIGURE IS SAFE: every error of this kind makes OVERTAKEN look
# SMALLER, so 30 of 883 is a LOW WATER MARK and cannot be an over-count.
KNOWN_DEFECT = ("N4", "N5", "C3", "N21", "N27", "N28", "N29", "N30", "N31",
                "N32", "N33", "N34")


def check(name, got, want, why):
    RAN.append(name)
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

# THE NEEDLE IS ASSEMBLED AT RUNTIME AND THAT IS NOT A STYLE CHOICE.  Written
# as one literal it FAILED THE MOMENT IT WAS COMMITTED: this file is a tracked
# *.py, git_grep_l greps tracked *.py at HEAD, and the control duly found
# itself and reported one hit where it required none.  A control that plants
# its own probe into the corpus it searches is the measurement environment
# leaking into the measurement -- the same class as mg-6e4f's dirty-worktree
# baseline and mg-54b1's `the sweep runs in a clone of the branch that carries
# it`, reached here by a third route.  code/species_repair_a4ef/run_all.sh
# already avoids writing out a pattern for this reason; this is that rule
# applied to a self-test.
_ABSENT = "mg4020_" + "absent_" + "needle.py"

check("C5 a needle nothing outside the subject names",
      consumers.git_grep_l(_ABSENT, ("*.py", "*.sh")),
      [],
      "FINDING NOTHING IS AN ANSWER, and it is the ordinary answer for a "
      "library or a numbered step. Before this it was a crash, after a "
      "correct-looking header had already printed. THE NEEDLE IS ASSEMBLED "
      "FROM PIECES: spelled as one literal this control FOUND ITSELF the "
      "moment it was committed, because it is a tracked *.py and this rule "
      "greps tracked *.py.")

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

check("C7 a needle that is a SUFFIX of a longer filename",
      kinds('    python3 s1_census.py 7  > out_s1_census.txt', "census.py"),
      [],
      "MEASURED, and found by running condition 3 against the census's OWN "
      "directory: `census.py` is a UNIQUE basename, so it was searched for "
      "by basename, and a substring test matched every numbered step in the "
      "estate whose name ENDS in it. 76 of 81 occurrences were this. THE "
      "INVERSE OF `A BASENAME IS NOT A NAME`, which fixes a basename SHARED "
      "by many files -- that rule cannot see this one, because census.py "
      "really is unique among tracked paths.")

check("C8 a FULL-PATH needle still matches after a slash",
      kinds('    subprocess.run(["sh", "code/a/w3_scope.py"])',
            "code/a/w3_scope.py"),
      ["EXEC-NO-ARG"],
      "THE NEGATIVE HALF OF C7, AND IT CARRIES THE WEIGHT. `/` must be "
      "ALLOWED as a preceding character or a full-path needle would never "
      "match and EVERY SHARED BASENAME would go silent -- converting a loud "
      "over-count into the exact under-count section D warns about. A "
      "word-boundary regex would have done that.")

print()
print("CONTROLS ON pinnable.py — mg-20ee's CONDITION 0 (mg-4020)")
print("-" * 78)
print()
print("  Conditions 1-3 all assume a pin is the remedy.  pinnable.py asks")
print("  whether it is, by classifying a drift the caller has already")
print("  produced.  Planted diffs and an INJECTED resolver, so the controls")
print("  do not depend on which commits this clone happens to contain.")
print()

import pinnable  # noqa: E402

check("P3 an IGNORED path in a changed line",
      [a for a in pinnable.addresses_of(
          "+          code/species_7d75/__pycache__   directory rule")
       if pinnable.is_ignored(a)],
      ["code/species_7d75/__pycache__"],
      "species_repair_a4ef's real line. .gitignore's `__pycache__/` carries "
      "a TRAILING SLASH and matches directories only, so check-ignore says "
      "NO to this path as written — both forms are tested, and a rule that "
      "tested one would have missed the instance it was built from.")

check("N6 a TRACKED path in a changed line",
      [a for a in pinnable.addresses_of("+    docs/roadmap.md:41")
       if pinnable.is_ignored(a)],
      [],
      "landscape_repair_1953's real line, and the contrast that makes R1 "
      "mean anything: a pin CAN restore a tracked file's old content, so "
      "this drift is mg-20ee's remedy working as designed and must not be "
      "swept into `no pin reaches it`.")

check("N7 a diff HEADER is not an address",
      pinnable.addresses_of(
          "--- a/code/x/out_a.txt\n+++ b/code/x/out_a.txt\n+ nothing here"),
      [],
      "every unified diff names its own file twice at the top. Counting "
      "those would make each instrument address itself and put a path in "
      "EVERY diff, which is the shape that turns a prefilter into noise.")

check("P4 a declared revision the repository RESOLVES",
      pinnable.declared_revs("OLD_REV = \"78ae4d9\"", lambda t: True),
      ["78ae4d9"],
      "state_relocation_audit_b0ae's real line — the instrument that is "
      "ALREADY PINNED and drifts anyway.")

check("N8 a hex-SHAPED english word, not resolvable",
      pinnable.declared_revs("the figure was defaced by the rebase",
                            lambda t: False),
      [],
      "THE NEGATIVE HALF, AND IT CARRIES THE WEIGHT. `defaced` is seven "
      "characters and every one of them is a hex digit. RESOLUTION is what "
      "makes R2 a rule rather than a regex: without `git cat-file -e` this "
      "rule reports prose as a pin, and R2's whole claim is that SOMEBODY "
      "DECLARED A REVISION.")

print()
print("CONTROLS ON R3 — THE UNORDERED WALK (mg-0e77)")
print("-" * 78)
print()
print("  R3 says a subject enumerates the filesystem, so its transcript's")
print("  LINE ORDER is in no commit and a correct pin will permute it.  The")
print("  NEGATIVE half is the load-bearing one: `git grep` is the form R3")
print("  exists to recommend, and a rule that fired on it would tell every")
print("  repaired instrument in the estate that it is still defective.")
print()

check("P5 `grep -r` spelled as a Python LIST",
      pinnable.unordered_walks(
          '    out = subprocess.run(["grep", "-rn", "-E", pattern] + paths,'),
      ['out = subprocess.run(["grep", "-rn", "-E", pattern] + paths,'],
      "landscape_repair_audit_3b51's real line, before this branch. The two "
      "tokens are separated by a quote, a comma and a space, so a pattern "
      "requiring `grep -r` adjacently sees nothing — and the ONLY subject "
      "this rule has ever had is spelled that way.")

check("P6 `grep -rn` spelled as a SHELL command",
      pinnable.unordered_walks("grep -rn 'sharper' docs STATE.md"),
      ["grep -rn 'sharper' docs STATE.md"],
      "the same read in a run_all.sh. Half this estate's corpus reads are "
      "shell and half are Python; a rule that saw one spelling would report "
      "`none` for the other and look like a clean subject.")

check("N9 `git grep` is an ORDERED READ OF A COMMIT",
      pinnable.unordered_walks(
          '    out = git(["grep", "-n", "-E", pattern, AS_OF, "--"] + paths)'),
      [],
      "THE NEGATIVE HALF, AND IT CARRIES THE WEIGHT. This is the repaired "
      "line R3 exists to recommend, and it contains the literal `grep` plus "
      "a `-n` flag. git SORTS its output and reads a COMMIT, which is the "
      "whole point; a rule that fired here would condemn the repair as the "
      "defect and there would be nothing left to advise.")

check("N10 a walk the subject has already SORTED",
      pinnable.unordered_walks("    for p in sorted(os.walk(root)):"),
      [],
      "an instrument that ordered its own walk has already removed the "
      "difference R3 warns about, and the transcript is repo-valued without "
      "any pin. Firing here would price a repair that is already paid.")

print()
print("  R3 READS CODE, NOT PROSE (mg-e5f3).  N18 was a KNOWN-DEFECT control")
print("  asserting the over-count; its own text said `teach R3 to see prose")
print("  and this control goes RED, which is the signal to update it`.  It is")
print("  updated here, and every control below is written as a PAIR -- what")
print("  mg-0e77's rule said, beside what the repaired rule says -- because a")
print("  repair whose BEFORE is not printed beside its AFTER is an assertion.")
print()

DOCSTRING_PROSE = (
    'def read(paths):\n'
    '    """The corpus read.\n'
    '\n'
    '    It used to be a `grep -rn` over the live worktree, which is the\n'
    '    defect this instrument has already repaired.\n'
    '    """\n'
    '    return ordered_read(paths)\n')

TRAILING_COMMENT = (
    'def read(paths):\n'
    '    hits = ordered_read(paths)      # was a `grep -rn` over docs/\n'
    '    return hits\n')

SHELL_COMMENT = (
    '#!/bin/sh\n'
    '# this step used to `grep -rn` over docs/ and no longer does\n'
    'python3 s1_scope.py > out_scope.txt\n')

LIST_FORM_IN_FILE = (
    'def read(paths, pat):\n'
    '    return subprocess.run(["grep", "-rn", "-E", pat] + paths)\n')

HASH_INSIDE_A_STRING = (
    'def read(paths, pat):\n'
    '    strip = subprocess.run(["sed", "-e", "s/#.*//"] + paths)\n'
    '    return subprocess.run(["grep", "-rn", pat] + paths), strip\n')

COMMENT_ONLY_SUPPRESSOR = (
    'def read(paths, pat):\n'
    '    out = subprocess.run(["grep", "-rn", pat] + paths)\n'
    '    # the caller applies sorted( ) to this before it is printed\n'
    '    return out\n')


def pair(src, path=None):
    """(what mg-0e77's rule sees, what the repaired rule sees)."""
    return (bool(pinnable.unordered_walks(src, path, prose="read")),
            bool(pinnable.unordered_walks(src, path)))


check("N18 prose naming the invocation, in a DOCSTRING (was the defect)",
      pair(DOCSTRING_PROSE, "s1_scope.py"),
      (True, False),
      "THE CONTROL THIS REPAIR EXISTS FOR, and it is the SUCCESSOR to a "
      "known-defect control rather than a new claim: mg-885d asserted this "
      "shape FIRING and said updating it would be the signal that R3 had been "
      "taught to see prose. MEASURED across the estate at 12aa5f8, not "
      "supposed: 9 of R3's 92 hits were prose, in 8 files, and the file it "
      "landed hardest on was audit_scope_text.py — THE INSTRUMENT TRANCHE 4 "
      "REPAIRED AND PINNED — whose only two hits were comments explaining the "
      "defect it no longer has. Condition 0 was telling a repaired instrument "
      "to expect a permuted transcript, which is N9's own rationale failing by "
      "PROSE instead of by the git form.")

check("N19 the same sentence as a TRAILING comment on a code line",
      pair(TRAILING_COMMENT, "s1_scope.py"),
      (True, False),
      "N11 plants a WHOLE-LINE comment, and a rule that only skipped lines "
      "beginning with `#` would pass N11 and still fire here — which is what "
      "mg-885d's own count of `3 hits on comment lines` was measuring, and it "
      "is why that count was an UNDER-count of the over-count: it tested "
      "`startswith('#')` and could not see this shape or N18's at all.")

check("N20 a SHELL comment naming the invocation",
      pair(SHELL_COMMENT, "run_all.sh"),
      (True, False),
      "half this estate's corpus reads are shell, so half its commentary is "
      "too, and `#` is the comment in both languages. A shell script gets the "
      "line scanner rather than `tokenize` — Python has no answer about a "
      "language that is not Python — and that narrowness is declared in "
      "code_only's docstring rather than hidden behind a shared code path.")

check("P19 the LIST form of the invocation, inside a real file",
      pair(LIST_FORM_IN_FILE, "s1_scope.py"),
      (True, True),
      "THE NEGATIVE DIRECTION, AND IT IS THE ONE THAT WOULD BE SILENT. The "
      "only subject R3 has ever had spells its corpus read as STRING LITERALS "
      "IN A LIST (P5), so a repair that blanked STRINGS rather than DOCSTRINGS "
      "would go blind to the one form the rule was built to see — an "
      "UNDER-count, which section D of consumers.py names as the worse of the "
      "two ways to be wrong because nothing in the output would say so. A "
      "docstring is a string STANDING ALONE AS A STATEMENT and no other string "
      "is touched; this is that boundary, planted.")

check("P20 a `#` INSIDE a string does not blank the walk after it",
      pair(HASH_INSIDE_A_STRING, "s1_scope.py"),
      (True, True),
      "the reason `tokenize` is asked rather than a regex written, which is "
      "R2's shape one rule over: `git cat-file -e` is git's own answer to `is "
      "this a revision`, and `tokenize` is Python's own answer to `is this a "
      "comment`. A scanner cutting at the first `#` would blank a real walk "
      "sitting after one in a string — and THIS FILE'S OWN `WALK` PATTERN "
      "CONTAINS A `#`, so the naive rule would misread the rule.")

check("P21 a walk whose ONLY ordering is claimed in a COMMENT — now FIRES",
      pair(COMMENT_ONLY_SUPPRESSOR, "s1_scope.py"),
      (False, True),
      "THE HALF THAT GOES THE OTHER WAY, and it is why the two prose surfaces "
      "MOVE TOGETHER. R3's negative half read the whole enclosing block, so a "
      "SENTENCE containing `sorted(` silenced a real walk. Blanking comments "
      "ALONE was measured before it was rejected: it removes 3 hits and ADDS "
      "ONE — to pinnable.py itself, whose docstring line was being suppressed "
      "by a `sorted(` in a block comment. A repair introducing the defect it "
      "repairs, in the half nobody would have looked at. PLANTED RATHER THAN "
      "FOUND: at 12aa5f8 the full repair adds ZERO hits, so no instrument in "
      "the estate is ordered only in prose — this world says what would "
      "happen, and the estate scan says it does not happen.")

check("N21 a bare FRAGMENT still reads prose — a DECLARED LIMIT",
      pair("    the corpus read was a `grep -r` over docs/ until tranche 4"),
      (True, True),
      "A KNOWN-LIMIT CONTROL in the form N18 used to take. Separating code "
      "from prose needs SYNTAX, and a fragment has none: `tokenize` refuses "
      "it, the fallback removes comments only, and a sentence that is neither "
      "a comment nor a docstring is indistinguishable from code. This does "
      "not reach pinnable.py's own reads — main() passes whole files, and the "
      "count of files that FAIL to tokenize is printed in its R3 section "
      "rather than swallowed, because a repair that quietly stops applying is "
      "worse than one that never did.")

check("N11 the word `grep` in prose",
      pinnable.unordered_walks(
          "  # the census greps for a basename rather than a full path"),
      [],
      "R3 reads the subject's SCRIPTS, which in this estate carry more "
      "commentary than code — every docstring in this directory names its "
      "own method. A rule that matched the word rather than the invocation "
      "would fire on the file explaining it.")

print()
print("  A FLAG'S DASH STARTS A WORD (mg-44da).  Tranche 7 named this")
print("  over-count in its own transcript and DECLINED it -- `R3's flag half")
print("  is mg-0e77's rule and one rule change measured in both directions is")
print("  this tranche's whole claim`.  This is that change, and the pairs below")
print("  are (what mg-0e77's rule sees, what the repaired rule sees) so the")
print("  BEFORE is printed beside the AFTER rather than asserted.")
print()


def fpair(src, path=None):
    """(what the LOOSE flag half sees, what the repaired one sees).

    Both halves pin `finds="space"`, which is mg-23af's own subject applied to
    mg-23af's own controls: these controls are about the FLAG repair, and a
    later repair to another half of the same rule must not be allowed to move
    what they assert while their text goes on naming the flag half.
    """
    return (bool(pinnable.unordered_walks(src, path, flags="loose",
                                          finds="space")),
            bool(pinnable.unordered_walks(src, path, finds="space")))


def ftriple(src, path=None):
    """(mg-0e77's rule, tranche 8's rule, THE RULE) -- the find(1) half.

    Three because the find half has now been repaired at a different axis from
    the flag half, and a pair could not say which of the two moved a control.
    """
    return (bool(pinnable.unordered_walks(src, path, flags="loose",
                                          finds="space")),
            bool(pinnable.unordered_walks(src, path, finds="space")),
            bool(pinnable.unordered_walks(src, path)))


check("N22 a HYPHENATED WORD is not a flag cluster",
      fpair("""print("  echo \\"$E2OUT\\" | grep 'STANDING UN-STRUCK' || true")"""),
      (True, False),
      "THE CONTROL THIS TRANCHE EXISTS FOR, and the line is runner_exit_c2b3's "
      "real one rather than a shape invented to fail. The 24-character window "
      "that buys the LIST spelling (P5) let ANY dash in it open a cluster, so "
      "`UN-STRUCK` read as `-STR`. It is one of the two hits tranche 7 printed "
      "as surviving prose inside a `print(...)` — so the residue that tranche "
      "reported at its low water mark is where this one's subject came from, "
      "and the estate scan says 83 -> 80 with ZERO added.")

check("N23 a hyphenated word in the ARGUMENT, not in a quoted snippet",
      fpair('     "bare grep over run_all.sh @%s re-derives %d" % (L.PINNED, bare)),'),
      (True, False),
      "runner_exit_repair_7522's real line, and the SECOND spelling of the "
      "same defect: here the hyphen is in ordinary English (`re-derives` -> "
      "`-der`), not in a shell snippet the file is quoting. One example would "
      "have left the rule looking like a special case for `UN-STRUCK`; the "
      "defect is the window, and two unrelated hyphenations are what says so.")

check("P22 `grep --recursive` still fires",
      fpair("    subprocess.run(['grep', '--recursive', pat, root])"),
      (True, True),
      "THE BOUNDARY IS A WORD BOUNDARY, NOT `PRECEDED BY WHITESPACE`, and that "
      "distinction is the whole reason the guard is a lookbehind for a WORD "
      "CHARACTER. A long flag's second dash is preceded by a dash, which is "
      "not one, so the tolerant half keeps working. A guard written as `\\s-` "
      "would have silenced this and the counts would not have said so — it is "
      "outside the estate at 12aa5f8, which is exactly why it is planted.")

check("P23 a real `-r` on the SAME LINE as a hyphenated word still fires",
      fpair("""    run("grep 'UN-STRUCK' x"); run(["grep", "-rn", pat])"""),
      (True, True),
      "the repair can only remove a line where EVERY candidate dash in the "
      "window is word-internal, because the engine backtracks over the lazy "
      "window and tries each one. Asserting that from the pattern would be "
      "reading a regex rather than running it; this runs it. A repair that "
      "stopped at the first rejected dash would be an UNDER-count, which is "
      "the silent direction.")

check("N24 find(1)'s `-type` takes the same guard — and it moves NOTHING",
      (fpair('  find "$ROOT" -type f -name "*.py"'),
       fpair("  find the well-type marker in docs and STATE.md")),
      ((True, True), (True, False)),
      "A GUARD THAT MOVES NOTHING, DECLARED RATHER THAN SMUGGLED IN. The same "
      "hyphenated-word defect is in R3's find(1) half, and the repair is "
      "applied there too — but measured separately at 12aa5f8 it removes ZERO "
      "hits, so it contributes nothing to the 83 -> 80 and this control is "
      "how that is said out loud rather than left to look like it helped. It "
      "is applied anyway because it is the same defect in the same rule, and "
      "a guard that waits for its first false positive is one somebody has to "
      "find twice.")

check("N25 find(1) in the LIST spelling — WAS INVISIBLE, NOW SEEN",
      ftriple("""    subprocess.run(["find", root, "-type", "f"], check=True)"""),
      (False, False, True),
      "FOUND BY WRITING N24's CONTROL AND GETTING THE WRONG ANSWER, which is "
      "this arc's own pattern: the figure moves when somebody builds the next "
      "thing. R3's find half required `find` followed by WHITESPACE, so the "
      "LIST spelling P5 exists for was invisible to it — the exact blind spot "
      "P5 was written about, one alternative along, and an UNDER-count rather "
      "than an over-count. Tranche 8 declined it and said what would have to "
      "happen first: `find` is an ordinary English verb where `grep` is not, "
      "so the false-positive direction had to be measured. mg-23af measured "
      "it and this control is now the repair's own — a command name is a WHOLE "
      "TOKEN, so the closing quote of its string literal counts where a `(` "
      "does not. It leaves KNOWN_DEFECT the way N18 did, in the tranche that "
      "did the thing its own text asked to be told about.")

check("N26 `doc.find(x)` is a CALL, not a command — the direction that was declined",
      ftriple("""    i = line.find(sep, line.index("-name"))"""),
      (False, False, False),
      "THE FALSE-POSITIVE DIRECTION TRANCHE 8 REFUSED TO WIDEN WITHOUT, and it "
      "is PLANTED because the estate has no instance — 0 lines at 12aa5f8 fire "
      "under the rejected shape and do not fire under the rule, so the counts "
      "could not have said so and permuted.py section 5 prints that zero. Had "
      "the find half simply taken the GREP half's shape (`find` then any 24 "
      "characters) this line would fire, and 238 more lines would join the "
      "exposed population, nearly all of them Python spelling `find` as a "
      "method. The separating fact is grammatical rather than statistical: "
      "there is no spelling of find(1) whose next character is `(`.")

check("N27 a LIST spelling PAST the 24-char window is still invisible — A LIMIT",
      ftriple('    subprocess.run(["find", os.path.join(root, sub), "-type", "f"])'),
      (False, False, False),
      "THE UNDER-COUNT THIS UNDER-COUNT REPAIR LEAVES, which is the defect "
      "class arriving inside its own remedy and is why it is asserted rather "
      "than mentioned. The window is P5's and its price was declared for the "
      "grep half when the window was written; nobody had measured it on the "
      "find half, and the answer is that it bites the same way. It takes N25's "
      "place in KNOWN_DEFECT — the count of known defects does not fall for "
      "this tranche, it turns over, and a tranche that let it fall would be "
      "reporting a repair as a reduction. Widening the window is the next "
      "change and its own false-positive direction is unmeasured, which is "
      "the sentence tranche 8 wrote about this one.")

print()
print("CONTROLS ON permuted.py — mg-20ee's CONDITION 2 (mg-885d)")
print("-" * 78)
print()
print("  R3 established that a CORRECT pin permutes its transcript, so")
print("  condition 2 was re-read as SET-IDENTITY PLUS A DECLARED PERMUTATION.")
print("  permuted.py is the first thing that can MEASURE that reading, and it")
print("  amends it: a SET forgets multiplicity, so the test is a BAG.  P11 is")
print("  the control that carries this whole file's weight — it is the case")
print("  the wording as written gets WRONG, and it is silent when it does.")
print()

import permuted  # noqa: E402

check("P11 a line's MULTIPLICITY changed — SET says nothing happened",
      (permuted.compare(["a", "addr:1", "addr:1", "b"],
                        ["a", "addr:1", "b"])["set"],
       permuted.compare(["a", "addr:1", "addr:1", "b"],
                        ["a", "addr:1", "b"])["bag"]),
      (True, False),
      "THE CONTROL THIS INSTRUMENT EXISTS FOR. mg-3b51's own pinned "
      "transcript prints one address twice and mg-1953's prints one three "
      "times; a pin that dropped one occurrence moves an ADDRESS and the "
      "COUNT it belongs to, and `set-identity` — the wording condition 2 was "
      "amended to — scores it IDENTICAL. 123 tracked transcripts carry a "
      "repeated line naming a path, so this is a shape the estate has.")

check("P12 a pure PERMUTATION is bag-identical and not byte-identical",
      [permuted.compare(["a", "b", "c"], ["c", "a", "b"])[k]
       for k in ("byte", "bag", "moved_min")],
      [False, True, 1],
      "the case R3 predicts for every correct pin of a `grep -r` corpus: "
      "`git grep <rev>` sorts, the walk did not, and no line's content "
      "changed. Scored byte-wise this is a FAILED pin; it is a clean one.")

check("N15 an unchanged transcript is BYTE-identical",
      permuted.compare(["a", "b"], ["a", "b"])["byte"],
      True,
      "the negative half of P12, and the reason condition 2 is not simply "
      "loosened: byte-identity still holds where it can, and ./build.sh and "
      "mg-f771's fixed point are RIGHT to keep comparing bytes. R3's "
      "permutation appears at the PIN TRANSITION, not run to run.")

check("P13 a MOVED VERDICT is not a permutation and is not hidden by one",
      sorted((permuted.compare(["hdr", "CRITERION : False", "tail"],
                               ["tail", "CRITERION : True", "hdr"]
                               )["only_new"]).elements()),
      ["CRITERION : True"],
      "3b51's and 1953's transcripts differ on exactly this line BY DESIGN. "
      "A comparator that reported `permuted` for a shuffle that also moved a "
      "verdict would absorb mg-20ee's own discrimination — `if a verdict "
      "moves, that is a FINDING` — into a pass.")

check("N16 a DECLARED residue is excused",
      sum(permuted.declared(collections.Counter(["  CORPUS as of : e924590"]),
                            ["  CORPUS as of : e924590"])[1].values()),
      0,
      "a pin ADDS an AS_OF block, and mg-20ee's discrimination expressly "
      "allows it to move. Without this the correct outcome of every pin "
      "would print as a finding, and the instrument would be unusable on the "
      "only case it is for.")

check("P14 a declaration is matched BY OCCURRENCE, not as a set",
      sum(permuted.declared(collections.Counter({"  total : 23": 2}),
                            ["  total : 23"])[1].values()),
      1,
      "THE NEGATIVE HALF OF N16 AND IT CARRIES THE WEIGHT. Declaring a line "
      "once must not excuse it twice, or P11's defect returns one level up — "
      "inside the mechanism built to catch it. A set-shaped declaration "
      "would pass a pin that dropped one of three identical addresses.")

check("P15 a declaration written from the DIFF traces to nothing",
      permuted.provenance("    docs/INVENTED.md:99  never published",
                          ['  subject document : '], "a commit message"),
      "UNSOURCED",
      "THIS FILE'S OWN DEFECT, CONTROLLED. `--declare` is an artifact of the "
      "same kind as the thing it scores: a declaration written by reading "
      "the diff excuses that diff entirely and turns CONTENT MOVED into a "
      "silent pass. Provenance is what stops that being invisible, and both "
      "declarations shipped here are traced to the pin's own source or its "
      "published record — never to the diff.")

check("N17 an AS_OF header line traces to the pin's own SOURCE",
      permuted.provenance("  CORPUS as of     : e924590 (repaired text)",
                          ["  CORPUS as of     : "], ""),
      "script",
      "audit_scope_text.py:104 prints exactly this, with the revision as a "
      "%s. The pin's author wrote the header in CODE before any transcript "
      "existed, which is why `script` is the strong half of provenance and "
      "`record` — a token quoted in prose — is declared weak.")

print()
print("CONTROLS ON THIS DIRECTORY'S OWN POINTERS (mg-23af)")
print("-" * 78)
print()

print()
print("CONTROLS ON worklist.py — IS THE WORK-LIST ITSELF STILL TRUE (mg-e8b0)")
print("-" * 78)
print()
print("  out_ground_truth.txt is the number this directory tells everybody to")
print("  quote and it is ONE DATED RUN, ~70 minutes, executing instrument code.")
print("  So it has the property every instrument on it is on it FOR, and five")
print("  tranches have quoted its count without re-taking it.  worklist.py asks")
print("  the repository instead, and the three controls below are the three")
print("  ways it could be wrong: it could read its own subject LIVE (P26), it")
print("  could publish one of two pin rules without measuring the other (P27),")
print("  and its `the record knows about this pin` rule cannot tell a sentence")
print("  ACCOUNTING for a pin from one OFFERING the same instrument as work")
print("  still to do (N28) -- which is the defect this tranche was told by.")
print()

import worklist  # noqa: E402

# ONE SCAN, SHARED.  Three controls calling it separately would triple this
# suite's cost for three copies of the same answer, and a control that got a
# DIFFERENT answer from its neighbour would be reporting on a moving tree,
# which is the defect the file under test is about.
_WL_OPENED = []
_real_open = open


def _watched_open(file, *a, **kw):
    try:
        p = os.path.abspath(file if isinstance(file, str) else str(file))
    except Exception:                                   # a file descriptor
        p = ""
    if p.startswith(ROOT + os.sep):
        _WL_OPENED.append(os.path.relpath(p, ROOT))
    return _real_open(file, *a, **kw)


try:
    import builtins
    builtins.open = _watched_open
    _WL = worklist.scan()
finally:
    builtins.open = _real_open

check("P26 worklist reads its own subject AT A COMMIT, never off disk",
      (_WL_OPENED, len(_WL["rows"])),
      ([], 44),
      "THE DEFECT THIS FILE COULD MOST EASILY HAVE. Its subject is a "
      "TRANSCRIPT IN THIS DIRECTORY, and permuted.py had to repair exactly "
      "this in itself at mg-e5f3 — a section 4 figure taken by reading the "
      "LIVE WORKTREE, in the file arguing that a transcript must be a "
      "function of repo state. So it is RUN rather than promised: `open` is "
      "replaced for the whole scan and every path under the repository root "
      "it is asked for is recorded. The list must be EMPTY — out_ground_truth."
      "txt, README.md, the log and the diffs all arrive through `git show` "
      "and `git log`. The row count is beside it so that a scan which read "
      "nothing because it did nothing cannot pass this.")

check("P27 the two pin rules DISAGREE, in both directions, at AS_OF",
      (sorted(_WL["only_a"]), sorted(_WL["only_b"])),
      ([("code/species_extent_d633", "e29ba2a")],
       [("code/absent_step_7ae5", "6af53b9")]),
      "RULE A reads the commit SUBJECT and RULE B reads the DIFF for a "
      "revision that resolves, and the verdict rests on B. That choice is "
      "worth nothing unless the two are known to differ, so the instances are "
      "PINNED here rather than described: e29ba2a calls itself a pin and its "
      "diff to species_extent_d633 declares no revision — the pin landed in "
      "species_remainder_f8fa, which the same commit touches, so A over-counts "
      "because A SUBJECT IS A PROPERTY OF A COMMIT AND A COMMIT TOUCHES "
      "SEVERAL DIRECTORIES. And 6af53b9 is the other direction: `fix: REPIN "
      "a4_novelty TO A main-REACHABLE COMMIT` declares a revision under a verb "
      "the convention does not cover, which is mg-daba's own defect being "
      "repaired. Change either rule and this control says so.")

# THE TWO SENTENCES ARE THE REAL ONES, one from the record as tranche 9 found
# it and one from the annotation tranche 9 replaced it with.
_OFFERS = "(`species_remainder_f8fa` at `2+/2-`, `species_repair_a4ef`) are cheap"
_ACCOUNTS = "`species_remainder_f8fa` was **pinned at `e29ba2a`** and reproduces"
_f8fa = [r for r in _WL["moved"] if r["dir"] == "code/species_remainder_f8fa"][0]
check("N28 `the record knows` cannot tell ACCOUNTING from OFFERING — A LIMIT",
      (_ACCOUNTS.count("species_remainder_f8fa"),
       _OFFERS.count("species_remainder_f8fa"),
       bool(_f8fa["by_content"]), _f8fa["named"] > 0),
      (1, 1, True, True),
      "A DECLARED LIMIT, ASSERTED ON THE RULE AND NOT ON ITS INSTANCE — AND "
      "THE MOVE FROM ONE TO THE OTHER IS THE POINT. `named in this record` is "
      "a SUBSTRING COUNT, so a sentence ACCOUNTING for a pin and a sentence "
      "OFFERING THE SAME INSTRUMENT AS REMAINING WORK score IDENTICALLY, and "
      "the two planted here are the real ones. THE LIVE INSTANCE WAS CLOSED IN "
      "THIS COMMIT: species_remainder_f8fa was pinned at e29ba2a — this arc's "
      "OWN tranche 2, mg-6e4f — and the only sentence naming it was tranche "
      "1's `the small ones … are cheap`, which went on offering a pinned "
      "instrument for four tranches and is now annotated. HAD THIS CONTROL "
      "STAYED ON THAT SENTENCE, closing the trap would have turned it RED, and "
      "a later tranche could have `repaired` the control by re-opening the "
      "trap. The last two clauses keep a live foot in the estate: that row IS "
      "pinned and the rule DOES score it accounted for, so the UNACCOUNTED "
      "count in out_worklist.txt is a LOW WATER MARK. WHAT TURNING THIS GREEN "
      "WOULD MEAN: somebody taught the rule to read what a sentence SAYS, "
      "which is a rule about English — that is why this is a LIMIT and not a "
      "bug, and why the instrument PRINTS the sentence instead.")

print()
print("CONTROLS ON exemplars.py — HAS THE RECORD NAMED IT SINCE (mg-0bf1)")
print("-" * 78)
print()
print("  N28 says `named in this record` cannot tell a sentence ACCOUNTING for")
print("  a pin from one OFFERING the same instrument as remaining work, and it")
print("  says closing that would take a rule about ENGLISH.  IT TAKES A DATE:")
print("  a sentence accounting for a pin is younger than the pin.  These five")
print("  are the ways that rule could be worth nothing -- it could read its")
print("  subject off disk (P29), it could report a zero it is incapable of")
print("  ever moving off (P30), its name matcher could fire inside words")
print("  (P31), and it moves N28's limit rather than removing it (N29, N30).")
print()

import exemplars  # noqa: E402

# ONE SCAN, SHARED, for P26's reason one file along.
_EX_OPENED = []


def _watched_open_ex(file, *a, **kw):
    try:
        p = os.path.abspath(file if isinstance(file, str) else str(file))
    except Exception:                                   # a file descriptor
        p = ""
    if p.startswith(ROOT + os.sep):
        _EX_OPENED.append(os.path.relpath(p, ROOT))
    return _real_open(file, *a, **kw)


try:
    builtins.open = _watched_open_ex
    _EX = exemplars.scan()
finally:
    builtins.open = _real_open

check("P29 exemplars reads its subject AT A COMMIT, never off disk",
      (_EX_OPENED, len(_EX["records"]) > 500, len(_EX["pairs"])),
      ([], True, 352),
      "THE SAME DEFECT P26 IS FOR, AND A WIDER SUBJECT: this file reads EVERY "
      "markdown record in the tree, not one transcript, so a single `open` "
      "would make its whole census a statement about somebody's dirty "
      "worktree. RUN rather than promised — `open` is replaced for the entire "
      "scan and every path under the repository root is recorded. The record "
      "count and the pair count sit beside it so a scan that read nothing "
      "because it did nothing cannot pass, which is the failure mode an "
      "empty list would otherwise reward.")

_REC = "code/asof_census_20ee/README.md"
_BEFORE = exemplars.pair_verdict(_REC, "species_remainder_f8fa",
                                 exemplars.AS_OF + "^")
_AFTER = exemplars.pair_verdict(_REC, "species_remainder_f8fa")
check("P30 the rule FIRES at AS_OF^ on the instance closed at AS_OF",
      (_BEFORE["mentions"], _BEFORE["overtaken"],
       [h[:7] for h in _BEFORE["after"]],
       _AFTER["overtaken"], _AFTER["mentions"] > _BEFORE["mentions"]),
      (1, True, ["e29ba2a"], False, True),
      "THE WRONG-DIRECTION CONTROL, AND IT IS WHAT MAKES THIS FILE'S ZERO "
      "FALSIFIABLE. The instance the rule was built from was CLOSED IN THE "
      "COMMIT BEFORE AS_OF — mg-e8b0 annotated tranche 1's sentence — so at "
      "AS_OF the rule correctly reports this record as accounted for, and a "
      "rule that reports nothing is indistinguishable from a rule that SEES "
      "nothing. So the SAME rule is asked the SAME pair one commit earlier, "
      "where the only sentence naming the instrument was tranche 1's offer, "
      "four tranches older than e29ba2a — this arc's own tranche 2 — and it "
      "must FIRE, naming that commit. Both halves are asserted: turning "
      "either one green alone means the rule stopped depending on the record "
      "or stopped depending on the repository.")

_loose_names = sorted(set(b for _, _, b, _ in _EX["loose_only"]))
_tok_prerepair = [k for k in _EX["pairs"] if k[1] == "prerepair"]
check("P31 a directory name is a WHOLE TOKEN — both directions, on real data",
      (len(_EX["loose_only"]), _loose_names, len(_tok_prerepair)),
      (52, ["prerepair"], 1),
      "mg-23af's rule arriving in a new file and on a new subject: the loose "
      "spelling of `does this record name that instrument` matches inside "
      "words, and it costs 52 lines. ONE WORK-LIST ROW IS A SUBDIRECTORY "
      "WHOSE BASENAME IS AN ORDINARY ENGLISH WORD — code/mirror_staleness_"
      "cdd5/prerepair — and it matches inside every `k1_prerepair.py` in the "
      "estate, which is where all 52 come from. THE SECOND DIRECTION IS THE "
      "ONE THAT KEEPS THE GUARD HONEST and it is real data rather than a "
      "plant: the guard must not silence the row itself, and the path "
      "spelling `mirror_staleness_cdd5/prerepair/out_s0_state.txt` in this "
      "directory's own README still fires because `/` is not a word "
      "character. A guard measured only where it removes things is a guard "
      "nobody has checked for over-reach.")

_3b51 = exemplars.pair_verdict(_REC, "landscape_repair_audit_3b51")
check("N29 a YOUNGER mention closes the pair whatever it says — A LIMIT",
      (_3b51["overtaken"], _3b51["newest"][:7],
       "go silent" in _3b51["text"], "pin" in _3b51["text"]),
      (False, "93ead80", True, False),
      "A DECLARED LIMIT, ASSERTED ON THE RULE, AND IT IS WHERE N28 ACTUALLY "
      "WENT RATHER THAN WHERE IT DIED. The date orders ACCOUNTING and "
      "OFFERING because a sentence accounting for a pin is NECESSARILY "
      "younger than it — that is an impossibility, which is the only thing a "
      "rule can have. IT DOES NOT IDENTIFY ACCOUNTING: a younger sentence "
      "MIGHT be one, and this one is not. The newest mention of "
      "landscape_repair_audit_3b51 in this record is tranche 6's sentence "
      "about TWO DIRECTORIES GOING SILENT in a grep census, which says "
      "nothing whatever about the pin tranche 4 landed on it, and it closes "
      "the pair anyway. So the remedy N28 named survives unchanged: THE "
      "INSTRUMENT PRINTS THE SENTENCE. What turning this green would mean is "
      "what turning N28 green would have meant — somebody taught a rule to "
      "read English — and the honest statement of this tranche is that the "
      "date moved the limit one step and did not remove it.")

check("N30 zero mentions is zero pairs — the population it cannot see",
      (len(_EX["unnamed"]), _EX["unnamed"]),
      (1, ["code/summary_guard_audit_407f"]),
      "THE BLIND SPOT IS THE COMPLEMENT OF THE RULE AND IS COUNTED RATHER "
      "THAN CONCEDED. This rule reads a record's LAST WORD about an "
      "instrument; a record that has never had a word about it has no last "
      "one, so an instrument no document in the estate names is invisible "
      "here at every revision. It is the one figure in out_exemplars.txt that "
      "GROWS WHEN THE CORPUS GETS WORSE, which is why it is pinned: a "
      "successor that widens the record population must move this number or "
      "explain why not.")

print()
print("CONTROLS ON liveindex.py — WAS IT STALE AT ITS OWN COMMIT (mg-ede8)")
print("-" * 78)
print()
print("  consumers.py reads the LIVE INDEX by design, so out_consumers.txt is a")
print("  function of WHEN it was run and not of the commit it is attached to.")
print("  These are the ways a census of that could be worth nothing: it could")
print("  fire on everything it looks at (P32), it could read its subject off")
print("  disk and become a statement about somebody's worktree (P33), its")
print("  re-derivation could have drifted from the rule it re-states or its")
print("  reader could report `clean` for a line it never found (P34) -- and it")
print("  answers about four figures out of a transcript that has many (N31).")
print()

import io  # noqa: E402
import contextlib  # noqa: E402

import liveindex  # noqa: E402

# ONE SCAN, SHARED, for P26's reason two files along.
_LI_OPENED = []


def _watched_open_li(file, *a, **kw):
    try:
        p = os.path.abspath(file if isinstance(file, str) else str(file))
    except Exception:                                   # a file descriptor
        p = ""
    if p.startswith(ROOT + os.sep):
        _LI_OPENED.append(os.path.relpath(p, ROOT))
    return _real_open(file, *a, **kw)


try:
    builtins.open = _watched_open_li
    _LI = liveindex.scan()
finally:
    builtins.open = _real_open

_LIV = _LI["watched"][0]["versions"]
_LIBY = {v["commit"][:7]: v["verdict"] for v in _LIV}


def _said_tree(short, label):
    for v in _LIV:
        if v["commit"][:7] != short:
            continue
        for lab, was, now, _grade in v["rows"]:
            if lab == label:
                return was, now
    return None


check("P32 the census fires, and DOES NOT fire, on real committed history",
      (_LIBY.get("ccd925c"), _LIBY.get("3d9ad71"), _LIBY.get("828a0fa"),
       _said_tree("ccd925c", "shared basename counts"),
       _said_tree("3d9ad71", "shared basename counts"),
       sorted(set(g for v in _LIV for _l, _w, _n, g in v["rows"]
                  if _l != "shared basename counts"))),
      ("STALE", "STALE", "AGREES",
       ([("run_all.sh", 196)], [("run_all.sh", 197)]),
       ([("run_all.sh", 193)], [("run_all.sh", 192)]),
       ["AGREES"]),
      "THE WRONG-DIRECTION HALF IS TWO DIFFERENT THINGS HERE AND BOTH ARE "
      "REQUIRED. First, a version that AGREES: 828a0fa is mg-e8b0's own "
      "recorded expectation — tranche 8's transcript was NOT stale at its own "
      "commit — so a census that graded every version STALE would be caught by "
      "a commit whose answer was already published. Second, the OTHER THREE "
      "FIGURES MUST STAND STILL AT EVERY VERSION: `subject scripts`, the "
      "unique/shared split and the shared count are read by the same reader "
      "and re-derived by the same rule, and only ONE of them has ever drifted. "
      "A census whose every figure moved would be measuring its own reader. "
      "AND THE DRIFT GOES BOTH WAYS: ccd925c under-counts by 1 (the ticket's "
      "own finding) and 3d9ad71 OVER-counts by 1 — a figure taken on a tree "
      "holding MORE of the named file than the commit that carries it, which "
      "is consumers.py's own header sentence about the day main folded one "
      "suite into another, and which nobody had looked for.")

check("P33 liveindex reads its subject AT A COMMIT, never off disk",
      (_LI_OPENED, len(_LIV), len(liveindex.FIELDS)),
      ([], 8, 4),
      "THE SAME DEFECT P26 AND P29 ARE FOR, ON THE FILE WHOSE WHOLE SUBJECT IS "
      "A FIGURE THAT DEPENDS ON WHEN IT WAS TAKEN. A single `open` here would "
      "make a census of `was this transcript stale at its own commit` into a "
      "statement about the reader's worktree, which is the defect it reports "
      "wearing the remedy's clothes. RUN rather than promised: `open` is "
      "replaced for the entire scan and every path under the repository root "
      "is recorded. The version count and the figure count sit beside it so a "
      "scan that read nothing because it did nothing cannot pass.")

_CONS = io.StringIO()
with contextlib.redirect_stdout(_CONS):
    consumers.main(os.path.join("code", "species_remainder_f8fa"))
_REAL = liveindex.figures_from_transcript(_CONS.getvalue())
_MINE = liveindex.figures_from_paths(_REAL["subject"],
                                     liveindex.paths_at(None))
_PAGE = liveindex.git("show", "%s:%s"
                      % (liveindex.AS_OF, liveindex.WATCHED[0][0]))
_BLIND = liveindex.SHARED_LINE.sub("  basename is shared -- ", _PAGE)
_GONE = liveindex.figures_from_transcript(_BLIND)
check("P34 the re-derivation AGREES with the real consumers.py, and the "
      "reader refuses",
      ((_REAL["n_scripts"], _REAL["n_unique"], _REAL["n_shared"],
        _REAL["shared"]) ==
       (_MINE["n_scripts"], _MINE["n_unique"], _MINE["n_shared"],
        _MINE["shared"]),
       _REAL["subject"], _MINE["n_shared"],
       _GONE["shared"] is liveindex.UNREADABLE,
       [g for _l, _w, _n, g in liveindex.compare(_GONE, _MINE)
        if g == "UNREADABLE"]),
      (True, "code/species_remainder_f8fa", 1, True, ["UNREADABLE"]),
      "liveindex.figures_from_paths IS A RE-STATEMENT of consumers.main's freq "
      "loop and its unique/shared split, not an import — consumers.main is one "
      "function that prints as it goes, and the figures have to be computable "
      "for a tree that is not checked out. A re-statement DRIFTS, so the REAL "
      "consumers.py is run here and its printed page is fed to the same reader "
      "the census uses: the two must agree on all four figures at the live "
      "index, and the subject name is asserted beside them so a run that "
      "compared two empty answers cannot pass. THE SECOND HALF IS THE ONE THAT "
      "KEEPS `AGREES` HONEST — with the shared-basename line emptied, the "
      "reader must return UNREADABLE and the comparison must GRADE it "
      "UNREADABLE — and THIS CONTROL FIRED ON ITS OWN FILE THE FIRST TIME IT "
      "RAN. liveindex's first reader took the emptied line as ZERO PAIRS and "
      "the comparison graded it STALE: a census reporting a FINDING about a "
      "figure it had failed to read, which is git_grep_l's original defect one "
      "file over — reporting a number because it never looked — arriving "
      "inside the remedy for it. The reader was tightened rather than the "
      "plant relaxed: the payload must be `none` or must reconstruct EXACTLY "
      "in consumers.py's own spelling.")

check("N31 AGREES is one-directional — the class this census cannot see",
      (sorted(l for l, _k in liveindex.FIELDS), len(liveindex.WATCHED)),
      (["shared basename counts", "shared-basename scripts",
        "subject scripts", "unique-basename scripts"], 1),
      "A DECLARED LIMIT, ASSERTED ON THE RULE AND NOT ON AN INSTANCE, AND IT "
      "IS worklist.py's FALSIFIED / NOT FALSIFIED DISCIPLINE ONE SUBJECT "
      "ALONG. A figure is re-derivable at an arbitrary commit exactly when it "
      "is a function of the TRACKED PATH LIST ALONE; the four above are, and "
      "everything else in out_consumers.txt — the prose count, the "
      "named-in-no-tracked-file count, and the whole of sections A, B and C — "
      "is a function of FILE CONTENT, and re-deriving those means running "
      "TODAY'S rule against an OLD tree and calling the difference staleness, "
      "which conflates the corpus moving with the instrument changing. So "
      "STALE is a proof and AGREES is not. THE SECOND HALF IS THE POPULATION: "
      "the registry is ONE transcript because one transcript IN THIS DIRECTORY "
      "reads the live index, and nothing scans code/ for the others — a "
      "live-index producer one directory over is invisible here at every "
      "revision, which is N30's shape on a new subject. What turning this "
      "green would mean is that somebody found a way to re-derive a "
      "content-valued figure at a commit without re-running the instrument "
      "there, and that is a different rule and not a wider one.")

print()
print("CONTROLS ON semantic.py — IS THE LIMIT A DATE QUESTION (mg-5058)")
print("-" * 78)
print()
print("  mg-0bf1 closed by asking whether any REMAINING `read what the")
print("  sentence says` rule in this estate is likewise a date question.  The")
print("  answer is worth nothing without both directions: a file that")
print("  returned COLLIDES on every row would be indistinguishable from one")
print("  that cannot separate anything (P36), a registry whose declarations")
print("  have been deleted underneath it would stand as a claim about a")
print("  document that no longer says it (P37), and a prefilter narrower than")
print("  the rule it feeds would drop sites in silence (P38).")
print()

import semantic  # noqa: E402

# ONE SCAN, SHARED, and `open` is replaced for ALL of it -- including the estate
# census in section 3, which is by far the largest reader here.  Leaving the
# biggest reader outside the watch would be the gap this arc reports.
_SEM_OPENED = []


def _watched_open_sem(file, *a, **kw):
    try:
        p = os.path.abspath(file if isinstance(file, str) else str(file))
    except Exception:                                   # a file descriptor
        p = ""
    if p.startswith(ROOT + os.sep):
        _SEM_OPENED.append(os.path.relpath(p, ROOT))
    return _real_open(file, *a, **kw)


try:
    builtins.open = _watched_open_sem
    _POP = semantic.declarations(semantic.AS_OF)
    _ROWS = [semantic.resolve(r, semantic.AS_OF) for r in semantic.REGISTRY]
    _PREREG = semantic.prereg_census(semantic.AS_OF)
finally:
    builtins.open = _real_open

check("P35 semantic reads the estate AT A COMMIT, never off disk",
      (_SEM_OPENED, len(_POP["prose"]), len(_PREREG["preds"])),
      ([], 43, 129),
      "P26's defect and P29's subject, on the widest reader yet: this file "
      "greps every tracked source in the estate and then reads every "
      "candidate, and THIS BRANCH EDITS TWO OF ITS SUBJECTS — selftest_20ee.py "
      "is one of the 37 files section 1 counts and the site of the two "
      "declarations R1 and R2 check. If any of that came off disk the "
      "transcript would be a statement about the worktree it was run in, and "
      "the edit would move the numbers it is about. RUN rather than promised: "
      "`open` is replaced for the whole scan, the census included. The two "
      "population figures sit beside the empty list because a scan that read "
      "nothing because it did nothing would otherwise pass.")

_V = {r["id"]: r["verdict"] for r in _ROWS}
check("P36 the four verdicts — and TWO of them must SEPARATE",
      (_V, len(_PREREG["proved"]), len(_PREREG["only_pred"])),
      ({"R1": "SEPARATED", "R2": "COLLIDES", "R3": "COLLIDES",
        "R4": "SEPARATED"}, 3, 5),
      "THE WRONG-DIRECTION CONTROL, AND IT IS WHAT MAKES THE TWO `NO` ROWS "
      "WORTH READING. COLLIDES is the direction that PROVES — two readings "
      "written by one commit share every commit-level field, so no rule "
      "reading one of them can separate the pair — which means a file "
      "returning COLLIDES everywhere would prove nothing and look identical "
      "to a file that sees nothing. R1 IS THE CALIBRATION: the limit mg-0bf1 "
      "ALREADY closed, asked by this file's machinery, and it must come back "
      "SEPARATED naming the pin. R4 is the new one and it is asserted twice — "
      "on its two witnesses and on the estate, where the row fires through a "
      "PREDICTIONS.md alone in 5 directories and the date proves 3 of them "
      "are not transcripts. Turning any one of the four green alone means the "
      "machinery stopped depending on the repository.")

_PLANT_GONE = dict(semantic.REGISTRY[0], id="X1", declared=(
    "file", "code/asof_census_20ee/selftest_20ee.py",
    "a declaration that has never been written in this file"))
_PLANT_AMBIG = dict(semantic.REGISTRY[0], id="X2", witnesses=[
    ("code/asof_census_20ee/README.md", "the", "a needle that matches often"),
    ("code/asof_census_20ee/README.md", "and", "and so does this one")])
_G = semantic.resolve(_PLANT_GONE, semantic.AS_OF)
_A = semantic.resolve(_PLANT_AMBIG, semantic.AS_OF)
check("P37 a row whose declaration or witness has moved SAYS SO",
      (_G["declared"][0], bool(_G["errors"]), _G["verdict"],
       _A["verdict"], len(_A["errors"])),
      ("GONE", True, "SEPARATED", "UNRESOLVED", 2),
      "THE DELETION TEST ON THE ROT GUARD, BOTH HALVES. A registry of other "
      "people's declared limits is a set of claims about documents this "
      "branch does not own, and the failure mode is SILENCE: the declaration "
      "is deleted, the row keeps printing, and a reader is told a file says "
      "something it no longer says. So the declaration is located at AS_OF "
      "and a row that cannot find it reads GONE — AND KEEPS ITS VERDICT, "
      "which is deliberate: what the witnesses do is a fact about the "
      "repository whether or not anyone still declares it, and collapsing the "
      "row would hide that. The second half is the witness locator: a needle "
      "matching TWO lines is a witness a reader cannot check, and it is a "
      "self-error rather than a silent first-match — the same rule pinnable.py "
      "applies to an empty diff.")

_STRICT_D, _LOOSE_D = semantic.DECLARES, re.compile(semantic.GREP, re.I)
_RED = semantic.red_tokens(semantic.AS_OF)
_LOOSE_R = re.compile("(%s)" % _RED.pattern.replace(r"\b", ""))
_PROBES = ["cannot tell a use from a mention", "CANNOT DISTINGUISH two things",
           "cannot telling", "it cannot separately"]
check("P38 both prefilters are WIDER than the rules they feed",
      (all(bool(_LOOSE_D.search(s)) for s in _PROBES if _STRICT_D.search(s)),
       bool(_STRICT_D.search("cannot telling")),
       bool(_LOOSE_D.search("cannot telling")),
       bool(_RED.search("REFUTEDLY")), bool(_LOOSE_R.search("REFUTEDLY"))),
      (True, False, True, False, True),
      "`git grep` speaks POSIX ERE and has neither `(?:` nor `\\b`, so both "
      "prefilters in that file are the rule with those dropped. THE DIRECTION "
      "IS THE WHOLE SAFETY ARGUMENT: a prefilter WIDER than the rule may hand "
      "over files the rule then rejects and CANNOT hide one, while a narrower "
      "one drops sites in silence and the count still looks like a count. "
      "Both halves are asserted, because a prefilter that were merely EQUAL "
      "to the rule would pass the first half and would be a second spelling "
      "of the rule — the thing mg-1344's P5 forbids — so a string the loose "
      "form takes and the strict one refuses is exhibited for each. The "
      "measured confirmation is one level up: section 3's census was run BOTH "
      "ways at AS_OF, prefiltered and reading every tracked .txt/.md in the "
      "estate, and the two transcripts are byte-identical.")

_ABSENT_SEM = "mg5058_" + "absent_" + "declaration_needle"
check("P39 a prefilter that matches NOTHING returns nothing, and does not die",
      (semantic.grep_files(semantic.AS_OF, _ABSENT_SEM, ("*.py", "*.md")),
       len(semantic.grep_files(semantic.AS_OF, semantic.GREP,
                               ("*.py", "*.md", "*.sh", "*.txt"))) > 50),
      ([], True),
      "mg-4020'S CRASH, ONE FILE ALONG AND REACHED BY A THIRD ROUTE. `git "
      "grep` exits 1 for NO MATCH and 2+ for a real error, and worklist's "
      "`git()` — which semantic.py IMPORTS — treats every non-zero as fatal, "
      "so both prefilters in that file would have died on the day their "
      "pattern stopped matching. For the red-token one that is a day somebody "
      "could bring about by tidying the estate, and the failure would arrive "
      "AFTER a correct-looking header. The tolerance is consumers.git_grep_l's "
      "and is deliberately narrow: rc 1 is empty, rc 2 and above stays fatal, "
      "because a mistyped revision returning `none` is a census that reports "
      "nothing because it never looked. THE NEEDLE IS ASSEMBLED FROM PIECES "
      "for C5's reason — spelled as one literal it would be a tracked *.py "
      "line and would find itself — and the live pattern's count sits beside "
      "it so a prefilter that had silently stopped matching anything could "
      "not pass this control by returning the empty list twice.")

_R2ROW = next(r for r in _ROWS if r["id"] == "R2")
check("N32 the registry's readings are HAND JUDGEMENTS — A LIMIT",
      (_R2ROW["verdict"],
       _R2ROW["witnesses"][0]["sha"] == _R2ROW["witnesses"][1]["sha"],
       _R2ROW["witnesses"][0]["reading"] != _R2ROW["witnesses"][1]["reading"]),
      ("COLLIDES", True, True),
      "A DECLARED LIMIT, ASSERTED ON THE ROW THAT IS ITS OWN INSTANCE. This "
      "control says in three fields what the whole file cannot do: R2's two "
      "witnesses AGREE on every field the repository has — one commit, one "
      "author, one date, one order index — and DISAGREE only in a sentence a "
      "person wrote into REGISTRY. That is exactly why the row is a proof "
      "that no commit-level rule separates them, and exactly why the labels "
      "themselves are not derived from anything. WHAT TURNING THIS GREEN "
      "WOULD MEAN: somebody derived the readings mechanically, which is the "
      "rule about English N28 declared and mg-0bf1 avoided rather than "
      "supplied — so the remedy is the one N28 named and it is why every "
      "witness prints with its line: THE INSTRUMENT PRINTS THE SENTENCE. A "
      "reader who disagrees with a label disagrees with text on the page.")

print()

print("=" * 78)
print("CONTROLS ON pathlist.py — IS THE METHOD FREE ON ANYTHING (mg-bdc0)")
print("=" * 78)
print()
print("  liveindex.py's method re-derives a figure at an old commit from the")
print("  tracked path list alone. pathlist.py asks how many committed")
print("  transcripts that is free on, and the answer is NONE — which is")
print("  exactly the answer a BROKEN detector prints too. So the controls that")
print("  matter here are the ones that make the empty class falsifiable.")
print()

import pathlist  # noqa: E402


def _grade(producer_src, extra=None):
    """pathlist's real grader over a planted corpus, through its real closure.

    A RE-STATEMENT WOULD DRIFT (P34's rule one instrument along), so the
    patterns and the closure are the module's own; only `source_at`'s cache is
    pre-loaded, which is how a corpus gets planted without a repository.
    """
    files = dict(extra or {})
    files["code/plant/p.py"] = producer_src
    for path, body in files.items():
        pathlist._SRC[("PLANT", path)] = body
    index = pathlist.module_index(set(files))
    closed = pathlist.closure("PLANT", "code/plant/p.py", index)
    body = "\n".join(pathlist.source_at("PLANT", f) for f in closed)
    reads_paths = bool(pathlist.PATHLIST.search(body))
    return ("PATH-LIST-ONLY" if reads_paths and not pathlist.OTHER.search(body)
            else "MIXED" if reads_paths else "NO PATH-LIST READ")


check("P40 a producer reading ONLY a path list is PATH-LIST-ONLY",
      _grade('out = git("ls-tree", "-r", "--name-only", rev)\n'),
      "PATH-LIST-ONLY",
      "THE ONLY CONTROL THAT KEEPS SECTION 3'S EMPTY LIST WORTH PRINTING. "
      "out_pathlist.txt reports 0 of 840, and a rule that had stopped being "
      "able to say PATH-LIST-ONLY at all would report the same 0 and read as "
      "the same finding. This arm fires the REAL grader on the shape the class "
      "is defined by, so `the class is empty` is a fact about the corpus and "
      "not about the detector. If it ever goes red, section 3 is measuring "
      "nothing and its 0 must not be quoted.")

check("P41 a path-list read beside a content read is MIXED",
      _grade('paths = git("ls-tree", "-r", "--name-only", rev)\n'
             'text = open(paths[0]).read()\n'),
      "MIXED",
      "the wrong-direction half of P40: the grade must turn on WHAT ELSE is "
      "read and not merely on the path-list read being present. MIXED is not a "
      "refutation — consumers.py is MIXED and three of its figures are "
      "path-list-valued — it means a reader per figure is still owed.")

check("P42 running a NON-git binary is a content read",
      (_grade('paths = os.walk(root)\n'
              'subprocess.run([MG_BIN, "show", "mg-1"], capture_output=True)\n'),
       _grade('paths = os.walk(root)\n'
              'subprocess.run(["git", "ls-tree", "-r", rev])\n')),
      ("MIXED", "PATH-LIST-ONLY"),
      "BOTH HALVES, BECAUSE THE CLAUSE IS INERT ON THE LIVE CORPUS AND AN "
      "INERT CLAUSE IS INDISTINGUISHABLE FROM A BROKEN ONE. Re-grading all 840 "
      "paired producers with the exec clause amputated moves 0 of them — "
      "a1_controls.py, the producer that shells out to the real `mg`, is "
      "already MIXED through the foreign lib P44's closure follows — so "
      "nothing in out_pathlist.txt would move if this clause silently stopped "
      "matching. The second half is the over-reach guard: a producer whose "
      "only subprocess is `git` must NOT be dragged out of the class, or the "
      "clause would empty it by construction and section 3's 0 would be an "
      "artifact of this control's own patch.")

check("P43 the walk is SORTED, so the page is a function of the commit",
      (pathlist.pairs_at("PLANT", {"code/d/out_a.txt", "code/d/a.py",
                                   "code/d/out_b.txt", "code/d/b.py",
                                   "code/d/out_z.txt"})[0],
       pathlist.pairs_at("PLANT", {"code/d/out_z.txt", "code/d/b.py",
                                   "code/d/out_b.txt", "code/d/a.py",
                                   "code/d/out_a.txt"})[0]),
      ([("code/d/out_a.txt", "code/d/a.py"),
        ("code/d/out_b.txt", "code/d/b.py")],
       [("code/d/out_a.txt", "code/d/a.py"),
        ("code/d/out_b.txt", "code/d/b.py")]),
      "THIS FILE FAILED ITS OWN HEADLINE CLAIM ON ITS FIRST RE-RUN AND THIS IS "
      "THE PIN. out_pathlist.txt prints `this transcript has a fixed point`; "
      "it did not have one, because `tracked` is a SET, section 4's "
      "per-directory table inherited hash order through most_common's "
      "insertion-order tie-break, and three runs at ONE commit produced three "
      "different tables. A transcript whose subject is figures that were "
      "already wrong at their own commit, published as a function of "
      "PYTHONHASHSEED, is this directory's subject arriving inside the file "
      "that measures it. Both spellings of the same set are asserted so that a "
      "walk which is merely LUCKY is not mistaken for one that is ordered.")

check("P44 the closure does NOT stop at the directory boundary",
      _grade('import lib_far\npaths = os.walk(root)\n',
             {"code/far/lib_far.py": 'text = open(p).read()\n'}),
      "MIXED",
      "THE REPAIR THAT EMPTIED THE CLASS, PINNED AS THE SHAPE THAT DEFEATED "
      "THE DRAFT BEFORE IT. Both survivors of the 2-transcript class — "
      "code/verdict_audit_f911/a1_controls.py and "
      "code/verdict_staleness_30bd/prose_30bd.py — `sys.path.insert` a FOREIGN "
      "directory and import a content-reading lib out of it, so a "
      "same-directory closure read neither and graded both a PROOF. The "
      "previous draft had DECLARED that stopping at the boundary would make "
      "the class look bigger than it is; it did, by the whole class. 6 of the "
      "6 candidates ever adjudicated by hand have been false positives.")

check("N33 the pattern is a SPELLING MATCHER and its residue is one-directional",
      (_grade('paths = os.walk(root)\ntext = read_it_some_other_way(paths[0])\n'),
       "PATH-LIST-ONLY"),
      ("PATH-LIST-ONLY", "PATH-LIST-ONLY"),
      "A KNOWN DEFECT, ASSERTED RATHER THAN REPAIRED. pathlist.py decides what "
      "a producer reads by matching SPELLINGS, so a read spelled a way the "
      "pattern does not name is invisible and grades the producer a PROOF — "
      "this arm plants exactly that and requires the WRONG answer, so the "
      "limit is a run and not a paragraph. Its direction is the load-bearing "
      "part and it is one-directional: every error of this kind makes "
      "PATH-LIST-ONLY look BIGGER, and the class is already EMPTY, so the "
      "published 0 cannot be an over-count and the residue is a class that "
      "cannot be smaller than it is. Turning this green would mean pathlist.py "
      "had stopped deciding from source. The other limit is counted rather "
      "than asserted and is in section 4 of its own transcript: 270 "
      "transcripts have no producer under the naming convention and are NOT "
      "counted as clean.")

print()

print("=" * 78)
print("CONTROLS ON overtaken.py — HAS THE PRODUCER MOVED SINCE (mg-6b2d)")
print("=" * 78)
print()
print("  OVERTAKEN is a proof about the PRODUCER and not about the transcript,")
print("  and its headline is a SMALL NUMBER — 30 of 883 — which is what a")
print("  narrowed pairing, a widening that recovered nothing, or a rule that")
print("  can no longer fire all return for free. So P45 runs first and")
print("  establishes that the rule can fire at all, and every other arm here")
print("  fires overtaken.grade itself rather than a re-statement of it.")
print()

import overtaken  # noqa: E402

_PROD = "code/plant/p.py"
_BASE = ('"""A docstring."""\n'
         'def main():\n'
         '    print("the population is %d file(s)" % n)\n')


def _grade(before, after, text="", producer=_PROD):
    got = overtaken.grade("code/plant/out_p.txt", producer, before, after, text)
    return None if got is None else got["grade"]


check("P45 the rule fires when the producer moved, and NOT when it did not",
      (_grade(_BASE, _BASE.replace("%d file(s)", "%d directory(ies)")),
       _grade(_BASE, _BASE)),
      ("CODE", None),
      "THE ARM THAT MAKES THE HEADLINE FALSIFIABLE, and it runs first for the "
      "reason D0 runs first next door: out_overtaken.txt reports 30 of 883, "
      "and a pairing that reached nothing, a widening that recovered nothing "
      "or a comparison that could no longer see a difference would each "
      "publish a SMALLER number and read as the same finding. The second half "
      "is the one that keeps it honest — an identical producer must return "
      "None and not a grade, because a rule that flagged every pair would look "
      "thorough and accuse 883 transcripts of nothing.")

check("P46 a PROSE-only edit and a CODE edit are told apart",
      (_grade(_BASE, _BASE.replace("A docstring.", "A much longer docstring.")),
       _grade(_BASE, _BASE.replace("# nothing", "# nothing")
              .replace("def main():", "def main(argv):"))),
      ("PROSE-ONLY", "CODE"),
      "BOTH DIRECTIONS, BECAUSE THE SPLIT IS THE ONLY THING STANDING BETWEEN "
      "`30 OVERTAKEN` AND `30 STALE`. A producer whose docstring grew cannot "
      "print anything different, and out_overtaken.txt reports 3 of 24 live "
      "rows in that class — a page that filtered them out silently would "
      "publish the same 21 with no way to check it. The separator is "
      "pinnable.code_only, IMPORTED, so this arm cannot disagree with "
      "permuted.py's section 4 about what prose is; if the two ever disagree "
      "it is because somebody re-spelled one of them, which is the defect "
      "mg-d2c2 named.")

check("P47 the widening still FINDS the pair the hand table refuses",
      (("code/state_suppression_repair_5f7c/out_run_all_a74f_PRE5f7c.txt",
        "code/state_suppression_repair_5f7c/run_all.sh")
       in overtaken.widen(
           ["code/state_suppression_repair_5f7c/out_run_all_a74f_PRE5f7c.txt"],
           {"code/state_suppression_repair_5f7c/run_all.sh"}),
       overtaken.WIDENED_VERDICT[
           "code/state_suppression_repair_5f7c/out_run_all_a74f_PRE5f7c.txt"]),
      (True, False),
      "A MATCHER TIGHTENED UNTIL ITS OUTPUT IS CLEAN PROVES NOTHING, so this "
      "asserts that the matcher STILL PRODUCES the one candidate a person had "
      "to refuse and that the refusal lives in the TABLE. "
      "out_run_all_a74f_PRE5f7c.txt is "
      "code/state_delegation_repair_a74f/out_run_all.txt copied in before a "
      "repair — its own README says so in a sentence — and no rule over "
      "basenames can read a sentence. If the first half ever goes False "
      "somebody narrowed the widening to hide a false positive, and section "
      "3's `1 adjudicated FALSE` would then be a fact about the matcher rather "
      "than about the estate.")

check("P48 the widening reaches ONLY what the strict rule missed",
      overtaken.widen(["code/d/out_a.txt"],
                      {"code/d/a.py", "code/d/out_a.txt", "code/d/o.py"}),
      [],
      "THE OVER-REACH GUARD, AND IT IS THE DIRECTION THAT WOULD BE SILENT. "
      "`widen` strips trailing `_`-separated segments, and a transcript with no "
      "`_` left to strip must yield NOTHING rather than falling through to some "
      "other producer in the directory — otherwise a strictly-paired "
      "transcript could be re-pointed at a producer it has nothing to do with "
      "and the row would still look exactly like a finding. scan() only ever "
      "offers it pathlist.pairs_at's MISSED list, so this is the guard on the "
      "function and not on the call.")

check("P49 the archival marker fires on the convention and NOT on an argument",
      (overtaken.is_archival("code/d/out_a4_sweep_PREREPAIR.txt"),
       overtaken.is_archival("code/d/out_r1_sweep_FIRSTRUN_2FAIL.txt"),
       overtaken.is_archival("code/asof_census_20ee/out_pinnable_3b51.txt"),
       overtaken.is_archival("code/d/out_a1_vacuity_n7.txt")),
      (True, True, False, False),
      "THE HEADLINE SPLITS 30 INTO 24 LIVE AND 6 ARCHIVAL, so a marker wide "
      "enough to eat the live rows would make `24` an artifact of this list "
      "and not a measurement. The last two halves are the ones that matter: "
      "out_pinnable_3b51.txt and out_a1_vacuity_n7.txt carry a trailing "
      "segment that is an ARGUMENT — a directory hash and a parameter — and "
      "those are exactly the rows this tranche was filed about. If either ever "
      "goes True the three files section 5 is about have been quietly "
      "reclassified as `preserved on purpose` and the page reports nothing.")

check("P50 the witness reads the TRANSCRIPT and not only the two sources",
      (len(overtaken.grade("t", _PROD, _BASE,
                           _BASE + '    print("a wholly new banner line")\n',
                           "")["witness"]),
       len(overtaken.grade("t", _PROD, _BASE,
                           _BASE + '    print("a wholly new banner line")\n',
                           "... a wholly new banner line ...")["witness"])),
      (1, 0),
      "SECTION 4 IS A WITNESS AND NOT A COUNT OF EDITS, and this is the half "
      "that makes the difference. A new literal ALREADY PRESENT in the "
      "committed transcript is evidence of nothing — the transcript already "
      "says it — so it must not be counted, and a witness that skipped the "
      "membership test would report a positive number for every producer that "
      "grew a string. 19 of 30 rows are positive with the test in place. The "
      "residue is declared in section 4 and is deliberately in the weakening "
      "direction: a regex and an unreachable branch's message both count, so a "
      "positive OVER-states and a zero proves nothing at all.")

check("N34 NOT OVERTAKEN PROVES NOTHING — the corpus is invisible here",
      _grade(_BASE, _BASE, text="the population is 194 file(s)"),
      None,
      "A KNOWN DEFECT, ASSERTED RATHER THAN REPAIRED, and it is the silent "
      "direction. This plants the exact shape out_consumers.txt has shipped in "
      "5 of its 8 committed versions — a producer nobody touched, a CORPUS "
      "that moved underneath it, and a printed figure that was already wrong "
      "at its own commit — and requires the answer NOT OVERTAKEN. The repair "
      "is not available at this cost: knowing whether the corpus moved means "
      "knowing what the producer reads, which is pathlist.py's question, and "
      "pathlist.py's answer is that the free method applies to ZERO of 840. So "
      "the direction is what makes the published 30 safe: every error of this "
      "kind makes OVERTAKEN look SMALLER, and 30 is therefore a LOW WATER MARK "
      "for `committed transcripts nothing re-takes`. Turning this green would "
      "mean somebody found a way to re-derive a content-valued figure at an "
      "old commit, which is the thing mg-ede8, mg-bdc0 and this tranche have "
      "each declined for the same measured reason.")

print()

# EVERY `SEE CONTROL X` IN THIS DIRECTORY RESOLVES, AND IT IS CHECKED PER SITE.
# mg-23af found two that did not: pinnable.py said `--recursive` staying lit was
# "a control (P24) rather than a claim" and no P24 has ever existed, and
# permuted.py's section 2 credited its literal-matching half to a control this
# suite has never issued.  Both sentences exist ONLY to say `go and check`, and
# both named somewhere with nothing at it.  The second was worse, because that
# number is a real control of ANOTHER suite -- a reader who went looking found
# something, and it was about something else.  So the population is (file, name)
# pairs and a name resolving somewhere in the estate is not enough.
#
# THE REPAIR IS AN INSTRUMENT AND NOT A REWORDING (mg-937c's rule), because a
# hand-fixed pointer is exactly as unbacked as the one it replaces.
#
# FOREIGN references are legal and DECLARED, and the declaration is MEASURED:
# the owning directory must really run a control by that name, or this control
# is a way to excuse any pointer at all -- P15's shape, one file over.
FOREIGN = {("README.md", "N14"): "code/state_ratchet_e331",
           # R4's witness line is a94c3's own P4, quoted verbatim so a
           # reader can check the label; the pointer is foreign and backed.
           ("semantic.py", "P4"): "code/c3_audit_a94c3"}
# BURNED numbers are never issued to a new control.  P24 is burned because
# pinnable.py's dead pointer named it: issuing it would make that pointer
# RESOLVE, to a control about something else, which is strictly worse than
# leaving it dangling.  A burned name may be discussed anywhere and must NEVER
# be defined here, and this control fails in BOTH directions.
BURNED = ("P24",)
CTL = re.compile(r'check\("([NPC][0-9]+[a-z]?)\b')
REF = re.compile(r"\b([NPC][0-9]+[a-z]?)\b")
_here = sorted(f for f in os.listdir(HERE)
               if f.endswith((".py", ".sh", ".md")))
# .txt is excluded because transcripts are GENERATED -- including this control's
# own output, which names every id it checked and would back itself.
_defined = set(CTL.findall(open(os.path.join(HERE, "selftest_20ee.py"),
                                encoding="utf-8").read()))
# THE REGISTER MAY NAME ITS OWN ENTRIES, AND NOTHING ELSE.  THIS CONTROL FIRED
# ON ITSELF THE FIRST TIME IT RAN -- on the FOREIGN literal three lines up, which
# is a DECLARATION and not a pointer -- which is this directory's own rule (a
# remedy is an artifact of the same kind as the defect it remedies) arriving
# live rather than as a paragraph.  The exemption is the narrowest one that is
# true: selftest_20ee.py may write a name it declares, and a name it does not
# declare is a pointer here like anywhere else.
_DECLARED = set(BURNED) | {k[1] for k in FOREIGN}
_dangling, _burnt_issued, _foreign_unbacked = [], [], []
for _f in _here:
    with open(os.path.join(HERE, _f), encoding="utf-8", errors="replace") as _h:
        for _name in sorted(set(REF.findall(_h.read()))):
            if _name in BURNED or _name in _defined:
                continue
            if _f == "selftest_20ee.py" and _name in _DECLARED:
                continue
            _owner = FOREIGN.get((_f, _name))
            if _owner is None:
                _dangling.append("%s:%s" % (_f, _name))
            elif not any(_name in open(os.path.join(ROOT, _owner, _g),
                                       encoding="utf-8",
                                       errors="replace").read()
                         for _g in sorted(os.listdir(os.path.join(ROOT, _owner)))
                         if _g.endswith(".py")):
                _foreign_unbacked.append("%s:%s -> %s" % (_f, _name, _owner))
_burnt_issued = [b for b in BURNED if b in _defined]

check("P25 every `see control X` in this directory RESOLVES",
      (_dangling, _foreign_unbacked, _burnt_issued),
      ([], [], []),
      "THE DEFECT THIS CONTROL IS BUILT FROM IS IN THE TWO SENTENCES THAT SAID "
      "`THIS IS CONTROLLED, NOT CLAIMED` — %d source files and %d control ids "
      "at this commit, cross-referenced rather than read. The three lists are "
      "kept apart on purpose: a DANGLING pointer names nothing, a FOREIGN one "
      "names another suite's control and is legal only when declared AND when "
      "that suite really runs it, and a BURNED one must never be issued here. "
      "The middle list is the one that keeps this control honest — an "
      "undeclared-foreign escape would let any pointer through, which is P15's "
      "shape one file over. Its own limit, declared: it reads .py/.sh/.md and "
      "NOT the transcripts, because a transcript is generated and this "
      "control's own output names every id it checked. AND IT FIRED ON ITSELF "
      "THE FIRST TIME IT RAN — on the FOREIGN literal in its own source, which "
      "is a declaration and not a pointer — so the register may name its own "
      "entries and nothing else."
      % (len(_here), len(_defined)))

print()
print("=" * 78)
if FAILED:
    print("RED — %d control(s) failed: %s" % (len(FAILED), ", ".join(FAILED)))
else:
    # COUNTED, NOT HAND-TALLIED (mg-e5f3).  This sentence used to spell the
    # breakdown out per instrument, and this branch added seven controls to
    # one section, which is exactly how it would have gone quietly false --
    # the shape mg-30bd's census counts, in the file whose subject is that a
    # rule must be measured rather than stated.  The controls that confirm a
    # KNOWN DEFECT rather than a repair are NAMED and not counted: which they
    # are is the load-bearing fact, and a number cannot carry it.
    print("GREEN — %d control(s) land where they must: %d positive, %d "
          "negative and %d on the consumer census's three-way classification, "
          "across the address census, the consumer census, the pinnable "
          "pre-condition, the condition-2 comparator, the work-list's own "
          "re-take, the record's last word about an instrument, the "
          "registry of declared limits and whether a transcript's producer "
          "has moved since it was taken.  %s confirm a KNOWN "
          "DEFECT or a DECLARED LIMIT rather than a repair, and each says in "
          "its own text what turning it green would mean."
          % (len(RAN), sum(1 for n in RAN if n[0] == "P"),
             sum(1 for n in RAN if n[0] == "N"),
             sum(1 for n in RAN if n[0] == "C"),
             ", ".join(n.split()[0] for n in RAN
                       if n.split()[0] in KNOWN_DEFECT)))
print("=" * 78)
raise SystemExit(1 if FAILED else 0)
