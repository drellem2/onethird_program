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

check("N18 prose quoting the INVOCATION, flag and all — FIRES (mg-885d)",
      bool(pinnable.unordered_walks(
          "    which is an ordered read of a commit; there is no `grep -r` here")),
      True,
      "A KNOWN-DEFECT CONTROL, in the form N4, N5 and C3 already take. N11 "
      "below plants the BARE word and passes; the rule matches the word plus a "
      "following short-flag cluster, so a sentence NAMING the invocation is a "
      "shape N11 does not reach. MEASURED across the estate at 12aa5f8 rather "
      "than supposed: 3 of R3's 92 hits sit on comment lines, and BOTH hits in "
      "audit_scope_text.py — THE INSTRUMENT TRANCHE 4 PINNED — are comments "
      "explaining the defect it already repaired, so condition 0 still tells a "
      "repaired instrument to expect a permuted transcript. That is N9's own "
      "rationale failing by PROSE instead of by the git form. Asserted rather "
      "than repaired, because R3 is mg-0e77's rule: teach it to see prose and "
      "this control goes RED, which is the signal to update its self-hit count.")

check("N11 the word `grep` in prose",
      pinnable.unordered_walks(
          "  # the census greps for a basename rather than a full path"),
      [],
      "R3 reads the subject's SCRIPTS, which in this estate carry more "
      "commentary than code — every docstring in this directory names its "
      "own method. A rule that matched the word rather than the invocation "
      "would fire on the file explaining it.")

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
print("=" * 78)
if FAILED:
    print("RED — %d control(s) failed: %s" % (len(FAILED), ", ".join(FAILED)))
else:
    print("GREEN — 2 positive, 4 negative and 1 known-defect control on the "
          "address census, 3 positive, 1 known-defect and 2 rc-tolerance "
          "controls on the consumer census, 4 positive, 6 negative and 1 known-defect "
          "control on the pinnable pre-condition, and 5 positive plus 2 negative on "
          "the condition-2 comparator, all land where they must.")
print("=" * 78)
raise SystemExit(1 if FAILED else 0)
