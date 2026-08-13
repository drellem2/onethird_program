#!/usr/bin/env python3
"""mg-f771 — PLANTED WORLDS.  Can this control fire, and is its blindness the declared one?

The whole risk of `g0_fixed_point.py` sits in one function, `lib_f771.normalise`.  Widen it
and every disagreement goes quiet; narrow it and the gate is red on every host forever.  So
the worlds below are split into two groups that are BOTH required:

  MUST FIRE      six differences that are a function of repo state.  Four of them are drawn
                 from the defect that opened mg-f771 (a registry count and a VERDICT line),
                 and two exist specifically to bound N1: the TAIL after a normalised path
                 is still compared (W6), and a REPO-RELATIVE path is not normalised at all
                 (W7).  If any of these goes quiet the normaliser has become an escape hatch.

  MUST NOT FIRE  three differences that are NOT a function of repo state.  These are
                 WRONG-DIRECTION WORLDS: they are green ON PURPOSE and a red here means the
                 gate has become unsatisfiable, which is the failure mode that would have
                 shipped had "fail when the regenerated output differs" been implemented
                 literally.  W5 is the truncated worktree path that a whole-path normaliser
                 would grade as real on every host.

  REFUSE         two worlds in which no verdict is available.  A control that cannot say
                 "I could not tell" says "nothing is wrong" instead.

  CORPUS (§1b)   mg-05c6's corpus-scoped exemption, which forgives a difference that IS a
                 function of repo state — just not of THIS BRANCH's — and therefore needs a
                 sharper fence than the normaliser's.  Ten worlds, three of them green on
                 purpose.  C2 is the one to read: same pin, moved text, still RED, which is
                 "the instrument changed its answer on an unchanged corpus".

  INVENTORY (§2b)  mg-c15e's replacement for g0's §2.  A transcript that never moves cannot
                 oscillate and buys NOTHING, so both directions are required: four widenings
                 that must move the inventory, one prose edit that must not, two
                 restructurings that must REFUSE, and the inventory's own immunity to N1/N2.
                 I2 found a real defect in the candidate this ticket landed and is the reason
                 the inventory is parsed rather than read by line prefix.

  FIXED POINT (§2c)  the claim itself, on the REAL arm, in three miniature repositories: two
                 that reach DIFFERENT verdicts and must produce IDENTICAL transcripts, and one
                 with a defect planted in it that must crash to stderr without moving the
                 transcript either.  Ported from mg-585e, which built it to answer whether
                 the self-exemption could go.

W10 is the negative control in the other direction: identical text must read AGREES, so the
instrument is shown able to report nothing-wrong rather than only able to complain.

THE PAIRS ARE FED TO `lib_f771.verdict_for`, THE FUNCTION `g0` ITSELF CALLS.  A control that
re-spells the predicate is a statement about the copy — mg-d2c2's arrangement, and its
reason is the same one.

EXITS 0 if every world lands where it must, 1 if any does not, 2 if a world could not be set
up at all.
"""

import os
import shutil
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_f771 as L  # noqa: E402

W = 92

# (id, expected verdict, what it is, committed text, worktree text)
WORLDS = [
    ("W1", "DISAGREES", "the defect that opened mg-f771: a stale VERDICT line",
     "VERDICT: GREEN — 20 entries\n",
     "VERDICT: GREEN — 23 entries\n"),

    ("W2", "DISAGREES", "the same defect one section earlier: a stale count",
     "  STATE.md claims 20 entries; docs/FACTS.md has 20   [PASS]\n",
     "  STATE.md claims 23 entries; docs/FACTS.md has 23   [PASS]\n"),

    ("W3", "NOISE", "wall-clock timing, the churn that makes byte-comparison impossible",
     "  recompute 36.4s · falsification 0.55s · total 37.0s\n",
     "  recompute 30.7s · falsification 0.54s · total 31.3s\n"),

    ("W4", "NOISE", "a foreign worktree's absolute path (N1)",
     "  cannot read /Users/daniel/.pogo/polecats/p28b6/code/x/STATE.md\n",
     "  cannot read /Users/daniel/.pogo/polecats/pf771/code/x/STATE.md\n"),

    ("W5", "NOISE", "an absolute path TRUNCATED at a column limit mid-worktree-name",
     "  N14  STATE.md absent from the tree   CAUGHT   cannot read /Users/daniel/.pogo/polecats/p28\n",
     "  N14  STATE.md absent from the tree   CAUGHT   cannot read /Users/daniel/.pogo/polecats/pf7\n"),

    ("W6", "DISAGREES", "the TAIL after a normalised path still differs — N1 eats the root only",
     "  S1  /Users/daniel/.pogo/polecats/p28b6/code/g/BASELINE.json.no-such-file is missing\n",
     "  S1  /Users/daniel/.pogo/polecats/pf771/code/g/BASELINE.json.OTHER-FILE is missing\n"),

    ("W7", "DISAGREES", "a REPO-RELATIVE path moved — N1 does not touch these at all",
     "  read from : git HEAD:code/control_audit_9876/out_a4_sweep.txt\n",
     "  read from : git HEAD:code/control_audit_9876/out_a9_other.txt\n"),

    ("W8", "DISAGREES", "STATE.md's byte count — a repo-state number, and the declared cost",
     "  bytes             138325\n",
     "  bytes             138335\n"),

    ("W9", "DISAGREES", "a count that sits next to a timing must not be eaten by N2",
     "  12 groups agree at mg-0d1b's measured tolerances; recompute 36.4s\n",
     "  13 groups agree at mg-0d1b's measured tolerances; recompute 30.7s\n"),

    ("W10", "AGREES", "the negative control — identical bytes must read AGREES",
     "  VERDICT: GREEN — 23 entries\n",
     "  VERDICT: GREEN — 23 entries\n"),

    # W11 and W12 are THE REFINERY'S OWN REFUSAL OF THIS BRANCH, planted.  It merges in
    # /Users/daniel/.pogo/refinery/worktrees/onethird_program (54 chars) and not in a
    # polecat worktree (34), so a column-cut line loses 15 more characters of tail there.
    ("W11", "NOISE", "the refinery's longer clone path — a THIRD checkout shape the first "
                     "version's enumerated roots did not know (N1a)",
     "  S1   BASELINE.json does not exist   CAUGHT   /Users/daniel/.pogo/polecats/pf771/code/g/BASELINE.json.no-such-file is missing\n",
     "  S1   BASELINE.json does not exist   CAUGHT   /Users/daniel/.pogo/refinery/worktrees/onethird_program/code/g/BASELINE.json.no-such-file is missing\n"),

    ("W12", "NOISE", "the same line CUT at a column limit, so the longer path keeps less "
                     "tail — the refinery's actual refusal (N3)",
     "  S1  CAUGHT  /Users/daniel/.pogo/polecats/pf771/code/g/BASELINE.json.no-such-file is missing.  A gate\n",
     "  S1  CAUGHT  /Users/daniel/.pogo/refinery/worktrees/onethird_program/code/g/BASELINE.json.no-such\n"),

    ("W13", "DISAGREES", "N3 forgives a SHORTER tail, not a DIFFERENT one — the tail must "
                         "still diverge before the cut to be caught",
     "  S1  CAUGHT  /Users/daniel/.pogo/polecats/pf771/code/g/BASELINE.json.no-such-file is missing\n",
     "  S1  CAUGHT  /Users/daniel/.pogo/refinery/worktrees/onethird_program/code/g/BASELINE.json.OTHER\n"),

    ("W14", "DISAGREES", "N3 must not pair lines across an INSERTION — the shape of the "
                         "defect that opened this ticket",
     "  F20   the reversibility bound   PASS\n§2  VOCABULARY\n  F1    `U`   PASS\n",
     "  F20   the reversibility bound   PASS\n  F21   a new row   PASS\n§2  VOCABULARY\n  F1    `U`   PASS\n"),
]

MUST_NOT_FIRE = {"W3", "W4", "W5", "W11", "W12"}

# ---- mg-05c6: the corpus-scoped exemption, bounded -----------------------------------
#
# THESE WORLDS ARE THE WHOLE DEFENCE OF THE EXEMPTION AND THEY ARE FED THE SAME
# `verdict_for` AS EVERYTHING ABOVE, with the third argument the exemption is reachable
# through.  C2 is the load-bearing one: same pin, moved text, and it must stay RED, because
# that is precisely "the instrument changed its answer on an unchanged corpus".  C3 is the
# other half — the exemption is a DECLARED PATH and not a shape a transcript can grow into
# by printing a pin line, so the identical pair at an undeclared path is red.
#
# (id, relpath, expected verdict, what it is, committed text, worktree text)
DECLARED = sorted(L.CORPUS_SCOPED)[0]
UNDECLARED = "code/control_audit_9876/out_a2_discriminate.txt"


def _census(pin, population, body, producer="dddddddddddd"):
    return ("corpus pin: %s  (%d directories, 2896 files, excluding code/x/)\n"
            "producer pin: %s  (the .py and .sh of code/x/)\n"
            "population: %d directories under code/\n%s"
            % (pin, population, producer, population, body))


CORPUS_WORLDS = [
    ("C1", DECLARED, "CORPUS",
     "the corpus moved under a declared corpus-scoped reading — GREEN ON PURPOSE, and the "
     "conflict this ticket was filed about",
     _census("aaaaaaaaaaaa", 231, "  151 of 231\n"),
     _census("bbbbbbbbbbbb", 232, "  152 of 232\n")),

    ("C2", DECLARED, "DISAGREES",
     "SAME PIN, MOVED TEXT — the instrument changed its answer on an unchanged corpus.  If "
     "this ever goes quiet the exemption has become an escape hatch",
     _census("aaaaaaaaaaaa", 231, "  151 of 231\n"),
     _census("aaaaaaaaaaaa", 231, "  9999 of 231\n")),

    ("C3", UNDECLARED, "DISAGREES",
     "C1's EXACT pair at a path that is not in the declared dict — the exemption is a list, "
     "not a shape, and printing a pin line does not earn it",
     _census("aaaaaaaaaaaa", 231, "  151 of 231\n"),
     _census("bbbbbbbbbbbb", 232, "  152 of 232\n")),

    ("C4", DECLARED, "STALE",
     "drift past the declared bound of %d directories — a pinned report nobody refreshes is "
     "the defect this whole control exists to find" % L.CORPUS_DRIFT_LIMIT,
     _census("aaaaaaaaaaaa", 231, "  151 of 231\n"),
     _census("bbbbbbbbbbbb", 231 + L.CORPUS_DRIFT_LIMIT + 1, "  152 of 242\n")),

    ("C5", DECLARED, "DISAGREES",
     "the declared transcript STOPPED PRINTING ITS PIN — losing the pin is how this "
     "exemption would go silent, so it is graded rather than forgiven",
     _census("aaaaaaaaaaaa", 231, "  151 of 231\n"),
     "population: 232 directories under code/\n  152 of 232\n"),

    ("C6", DECLARED, "NOISE",
     "a wall-clock timing under a corpus-scoped path still reads NOISE — the pin is a "
     "FOURTH family and does not displace N1-N3",
     _census("aaaaaaaaaaaa", 231, "  swept in 36.4s\n"),
     _census("aaaaaaaaaaaa", 231, "  swept in 30.7s\n")),

    ("C7", DECLARED, "AGREES",
     "the negative control in the other direction: identical bytes at a corpus-scoped path "
     "are AGREES and never CORPUS",
     _census("aaaaaaaaaaaa", 231, "  151 of 231\n"),
     _census("aaaaaaaaaaaa", 231, "  151 of 231\n")),

    ("C8", None, "DISAGREES",
     "C1's pair with NO path at all — a caller that does not name the file cannot be handed "
     "the exemption by accident, which is why `relpath` defaults to None",
     _census("aaaaaaaaaaaa", 231, "  151 of 231\n"),
     _census("bbbbbbbbbbbb", 232, "  152 of 232\n")),
    ("C9", DECLARED, "DISAGREES",
     "the CORPUS pin moved AND the PRODUCER pin moved with it — a branch that edits the "
     "instrument and something else under code/ in one go.  Measured on mg-05c6's own branch, "
     "which is that shape, and which C1 alone forgave",
     _census("aaaaaaaaaaaa", 231, "  151 of 231\n", producer="1111aaaa1111"),
     _census("bbbbbbbbbbbb", 232, "  152 of 232\n", producer="2222bbbb2222")),

    ("C10", DECLARED, "DISAGREES",
     "the producer pin went MISSING — the same silence C5 forbids for the corpus pin, and "
     "forbidden here for the same reason",
     _census("aaaaaaaaaaaa", 231, "  151 of 231\n"),
     ("corpus pin: bbbbbbbbbbbb  (232 directories, 2896 files, excluding code/x/)\n"
      "population: 232 directories under code/\n  152 of 232\n")),
]

CORPUS_GREEN_ON_PURPOSE = {"C1", "C6", "C7"}

# WHAT IS NOT IN THE REGISTRY IS AS MUCH OF A CLAIM AS WHAT IS, so both directions are here
# and the exclusions carry the measurement that decided them rather than a preference.
CORPUS_MEMBERSHIP = [
    ("code/control_audit_9876/out_a4_sweep.txt", True,
     "the census: 34 real moves in the last 200 commits on main, the most of any transcript, "
     "and its own counts are `recorded, not gated` in mg-724a's BASELINE.json"),
    ("code/control_gate_724a/out_gate.txt", False,
     "NOT declared, and it is the near miss: 20 real moves, but only 4 of them are the §1 "
     "byte counts that follow the census.  16 are its own gated fields moving, which is "
     "exactly what a merge gate's transcript is for"),
    ("code/gate_fixed_point_f771/out_g1_controls.txt", False,
     "this transcript: its content is a function of the planted worlds, i.e. of code, and a "
     "corpus-scoped grade on it would exempt the control from itself"),
    ("code/grain_axis_audit_03d1/out_a4_sweep.txt", False,
     "mg-03d1's, and it is the sharp case: the SAME BASENAME as the declared one and a "
     "different instrument behind it.  The registry is keyed by full path, so a basename "
     "rule — the obvious spelling — would have exempted this file and nothing would have said so"),
    ("code/libweak_audit_c4f5/out_a4_census.txt", False,
     "mg-c824's, which nothing regenerates — a similar NAME is not a similar subject, and "
     "the registry is read by path"),
]


def rule(ch="-"):
    print(ch * W)


# THE CLASS IS TOTAL AND THESE ROWS ARE WHAT SAYS SO (mg-c15e).  They used to assert an
# exemption and hold it to one file; there is no exemption left to hold, so what they assert
# now is that NO file is outside the class for any reason other than not being a transcript.
# Each row is (id, relpath, watched?, why).
MEMBERSHIP = [
    ("E1", "code/gate_fixed_point_f771/out_g0_fixed_point.txt", True,
     "g0's OWN transcript, and it is WATCHED — the single exemption this instrument used to "
     "carry, deleted at mg-c15e.  It is watchable because §2 no longer records the outcome: "
     "g0's stdout is a function of lib_f771.py's source and of nothing else, so the repair "
     "that empties the disagreement set does not move it.  Worlds F1-F6 measure that on the "
     "real arm rather than asserting it here"),
    ("E2", "code/gate_fixed_point_f771/out_g1_controls.txt", True,
     "THIS transcript is watched, and it is no longer the CONTRAST it was — when E1 was the "
     "exemption this row said `a file, not this directory`.  Both files in this directory "
     "are now in the class on the same terms as every other suite's, which is the whole of "
     "the mg-c15e change stated as a membership"),
    ("E3", "code/gate_fixed_point_f771/README.md", False,
     "not a transcript at all"),
    ("E8", "code/gate_fixed_point_f771/.out_g0_fixed_point.txt.partial", False,
     "run_all.sh's atomic-write temp file — outside the class by NAME, which is the only "
     "reason the `.partial` + `mv` arrangement is safe now that E1 is watched.  A half-"
     "written transcript observed by this arm is mg-479c's defect, and D1 in the README"),
    ("E4", "code/facts_registry_03cf/out_f0_registry_discipline.txt", True,
     "the file that opened mg-f771"),
    ("E5", "code/libweak_audit_c4f5/out_a4_census.txt", True,
     "mg-c824's — IN the class, and safe because nothing regenerates it (README §3)"),
    ("E6", "STATE.md", False,
     "outside the class, so a local STATE.md edit does not trip a transcript control"),
    ("E7", "docs/FACTS.md", False,
     "outside the class"),
]


# ---- mg-c15e: the rule inventory, and the fixed point measured on the real arm --------
#
# g0's §2 used to be the disagreement set and is now the INPUTS the verdict is a function of.
# That is the change the exemption's deletion rests on, so it needs both directions:
#
#   I-WORLDS   the inventory MOVES when a rule moves (it is not a constant file, which would
#              never oscillate and would buy nothing), does NOT move when prose moves, and
#              REFUSES when the instrument has been restructured under it.  String -> string,
#              fed the REAL `lib_f771.rule_inventory` (mg-d2c2).
#   F-WORLDS   the real g0, run as a subprocess against miniature repositories that differ in
#              whether a watched transcript disagrees.  This is the claim itself: the same
#              bytes on stdout, DIFFERENT exit statuses.  Ported from mg-585e, which built it
#              to answer whether this exemption could go.
#
# THE PATCHES ARE ANCHORED ON TEXT THAT MUST EXIST, and a missing anchor is a SETUP FAILURE
# (exit 2) rather than a pass — a world that could not be built has not been run.

INVENTORY_WORLDS = [
    ("I1", True,
     "N2 WIDENED TO EAT INTEGER SECONDS — the exact escape hatch lib_f771's own docstring "
     "calls unfalsifiable.  If this does not move, the inventory is decoration",
     r'SECONDS = re.compile(r"\b\d+\.\d+\s*s\b")',
     r'SECONDS = re.compile(r"\b\d+(?:\.\d+)?\s*s\b")'),

    ("I2", True,
     "ABS_TO_REPO widened — a MULTI-LINE constant, and the tail of it.  mg-585e's draft read "
     "constants by line prefix and reported this one as `re.compile(`, so a widening here "
     "moved neither the printed rule nor the digest (ABS_TO_REPO is inside no deciding "
     "function).  The inventory is parsed and printed in full because of this world",
     r'(?=/(?:code/|docs/|STATE\.md|build\.sh))',
     r'(?=/(?:code/|docs/|STATE\.md|build\.sh|anything/))'),

    ("I3", True,
     "N3 relaxed to forgive ANY two lines — a widening spelled as CONTROL FLOW, which no "
     "constant can show and which only the digest catches",
     "    if ROOT_MARK not in la or ROOT_MARK not in lb:\n        return False",
     "    if False:\n        return False"),

    ("I4", True,
     "THE EXEMPTION REINTRODUCED inside is_watched — the specific regression this ticket "
     "exists to make loud, and it is caught by the digest rather than by a reviewer",
     "    return is_transcript(relpath)",
     "    return is_transcript(relpath) and 'out_g0' not in relpath"),

    ("I5", False,
     "PROSE MOVED AND NOTHING ELSE — the wrong-direction world.  A file that moved whenever "
     "lib_f771.py moved would put this transcript back in every branch's diff, which is the "
     "tax mg-c15e removes.  first_disagreement's docstring is not a rule",
     "    \"\"\"The normalised lines that differ, so the transcript SHOWS the disagreement",
     "    \"\"\"REWORDED, AND NOTHING ELSE.  The normalised lines that differ, so it SHOWS"),
]

# The renames are graded on REFUSAL rather than on movement: a digest returned for a function
# that no longer exists under the name it was asked about is worse than a moved one, because
# it is silent.  mg-585e's D1 found this in its own first draft, where the matcher was a `def
# <name>` PREFIX and `def verdict_for_RENAMED(` starts with it.  Matching the parsed name
# closes it by construction; the world stays because a construction that is not run is a
# claim.
REFUSAL_PATCHES = [
    ("I6", "a deciding function RENAMED — verdict_for -> verdict_for_RENAMED, whose name "
           "STARTS WITH the one being asked about",
     "def verdict_for(committed", "def verdict_for_RENAMED(committed"),
    ("I7", "a named constant DELETED from the module — the inventory must refuse rather than "
           "print a shorter list that reads as a shorter rule set",
     "CORPUS_DRIFT_LIMIT = 10", "_UNUSED_DRIFT_LIMIT = 10"),
]

# ---- the sandboxes (ported from mg-585e) ---------------------------------------------
#
# The RED tree's worktree copy asserts a DIFFERENT COUNT.  A count and not a timing, because
# a timing is N2 and would come back NOISE — the sandbox has to produce the verdict it claims
# to produce, which F3 checks rather than assumes.
_SAMPLE_GREEN = """\
sample suite transcript
  entries          20
  total       12.30s
VERDICT: GREEN — 20 entries
"""

_SAMPLE_RED = """\
sample suite transcript
  entries          23
  total       12.30s
VERDICT: GREEN — 23 entries
"""


def build_sandbox(tmp, disagrees, patch=None):
    """A miniature repository holding a copy of the real g0 and one watched transcript.

    COPIED IN AND RUN AS A SUBPROCESS, not imported: `lib_f771.ROOT` is computed from the
    module's own location, so a copy under the sandbox is the only way to point the real arm
    at a tree that is not this one — and re-implementing its decision here would make every
    finding a statement about the re-implementation (mg-d2c2).

    `patch` is an (old, new) pair applied to the COPIED lib_f771.py, used by F5 to plant a
    crash.  A missing anchor raises rather than silently building an unpatched sandbox.
    """
    dst = os.path.join(tmp, "code", "gate_fixed_point_f771")
    os.makedirs(dst)
    here = os.path.dirname(os.path.abspath(__file__))
    for name in ("lib_f771.py", "g0_fixed_point.py"):
        shutil.copyfile(os.path.join(here, name), os.path.join(dst, name))
    if patch:
        old, new = patch
        path = os.path.join(dst, "lib_f771.py")
        with open(path, encoding="utf-8") as fh:
            copied = fh.read()
        # `copied` and not `body`/`text`: mg-9876's §1 detector counts `in <haystack>` as a
        # whole-output membership candidate, and a control fixture that moves the census it
        # is measured by is the defect mg-05c6 had to neutralise one directory over.
        if copied.count(old) != 1:
            raise L.Refused("sandbox patch anchor is not uniquely in lib_f771.py: %r" % old)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(copied.replace(old, new, 1))
    sample_dir = os.path.join(tmp, "code", "sample_suite")
    os.makedirs(sample_dir)
    sample = os.path.join(sample_dir, "out_sample.txt")
    with open(sample, "w", encoding="utf-8") as fh:
        fh.write(_SAMPLE_GREEN)
    for args in (("init", "-q", "-b", "main"),
                 ("add", "-A"),
                 ("-c", "user.email=mg-f771@local", "-c", "user.name=mg-f771",
                  "commit", "-q", "-m", "sandbox")):
        p = subprocess.run(("git", "-C", tmp) + args, capture_output=True, text=True)
        if p.returncode != 0:
            raise L.Refused("sandbox git %s failed: %s" % (args[0], (p.stderr or "").strip()))
    if disagrees:
        with open(sample, "w", encoding="utf-8") as fh:
            fh.write(_SAMPLE_RED)
    return tmp


def run_g0(sandbox):
    """Run the REAL arm against a sandbox.  Returns (rc, stdout, stderr)."""
    env = dict(os.environ)
    env[L.FRESH_ENV] = "1"
    arm = os.path.join(sandbox, "code", "gate_fixed_point_f771", "g0_fixed_point.py")
    p = subprocess.run([sys.executable, arm], capture_output=True, text=True, env=env)
    return p.returncode, p.stdout, p.stderr


def fixed_point_worlds():
    """The claim itself, on the real arm: same stdout, different outcome.

    Returns (id, what, outcome, ok).  A sandbox that cannot be built raises, and the caller
    turns that into exit 2 — a world that could not be run has not been run.
    """
    # The third world plants a CRASH, which is the hazard mg-c15e introduced: the traceback
    # used to go to stdout precisely so it would land in the tracked file, and that file is
    # now inside the watched class, so a traceback in it is a committed transcript no tree
    # that does not reproduce the crash can agree with.
    CRASH = ('    p = _git(root, "diff", "--name-only", "HEAD", "--", "code")',
             '    raise ValueError("planted defect, world F5")')
    tmps, runs = [], {}
    try:
        for key, disagrees, patch in (("green", False, None), ("red", True, None),
                                      ("crash", False, CRASH)):
            tmp = tempfile.mkdtemp(prefix="f771-fp-%s-" % key)
            tmps.append(tmp)
            runs[key] = run_g0(build_sandbox(tmp, disagrees, patch))
    except Exception:
        for t in tmps:
            shutil.rmtree(t, ignore_errors=True)
        raise
    try:
        g_rc, g_out, g_err = runs["green"]
        r_rc, r_out, r_err = runs["red"]
        out = []
        out.append(("F1", "the two trees really did reach different verdicts",
                    "exit %d green tree, exit %d red tree" % (g_rc, r_rc),
                    g_rc == 0 and r_rc == 1))
        same = g_out == r_out
        out.append(("F2", "AND THE TWO TRANSCRIPTS ARE BYTE-IDENTICAL — no scrubbing on "
                          "either side, because there is no clock in either",
                    "%d bytes vs %d bytes, %s" % (len(g_out), len(r_out),
                                                  "identical" if same else "DIFFER"),
                    same))
        out.append(("F3", "the red run's disagreement is on STDERR, so nothing was lost by "
                          "taking it off stdout",
                    "%d stderr bytes name %s" % (len(r_err),
                                                 "out_sample.txt" if "out_sample.txt" in r_err
                                                 else "NOTHING"),
                    "DISAGREES" in r_err and "out_sample.txt" in r_err))
        out.append(("F4", "the green run's stderr says GREEN — the wrong-direction half, so "
                          "F2 is not two identically empty answers",
                    "VERDICT on stderr: %s" % ("GREEN" if "GREEN" in g_err else "absent"),
                    "VERDICT: GREEN" in g_err))
        c_rc, c_out, c_err = runs["crash"]
        out.append(("F5", "A CRASH LEAVES THE TRANSCRIPT AT ITS FIXED POINT TOO — planted "
                          "defect, traceback on stderr, exit 2, and the SAME bytes on stdout "
                          "as the two runs that reached a verdict.  This is the hazard "
                          "mg-c15e introduced: the traceback used to go to stdout precisely "
                          "so it would land in the tracked file",
                    "exit %d, traceback %s stderr, stdout %s"
                    % (c_rc, "on" if "Traceback" in c_err else "NOT ON",
                       "identical" if c_out == g_out else "MOVED"),
                    c_rc == 2 and "Traceback" in c_err and c_out == g_out))
        no_sandbox_path = all(t not in g_out and t not in r_out and t not in c_out
                              for t in tmps)
        out.append(("F6", "and NO SANDBOX PATH reached any of the three transcripts — this "
                          "directory would otherwise be committing mg-f771's own defect "
                          "while describing it",
                    "clean" if no_sandbox_path else "A SANDBOX PATH IS IN THE TRANSCRIPT",
                    no_sandbox_path))
        return out
    finally:
        for t in tmps:
            shutil.rmtree(t, ignore_errors=True)


def refusal_worlds():
    """Two worlds in which no verdict is available.  Returns (id, what, outcome, ok)."""
    out = []

    # R1 — the tree is not a git repository.  The committed copy is READ FROM GIT, so
    # without one there is no comparison to make and a green would be manufactured.
    tmp = tempfile.mkdtemp(prefix="f771-r1-")
    try:
        try:
            L.changed_transcripts(root=tmp)
            out.append(("R1", "not a git work tree", "returned a verdict", False))
        except L.Refused:
            out.append(("R1", "not a git work tree", "REFUSED", True))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # R2 — the freshness handshake is absent.  g0 is invoked as a subprocess with the
    # variable stripped, because this is a property of the ARM and not of the library.
    env = dict(os.environ)
    env.pop(L.FRESH_ENV, None)
    g0 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "g0_fixed_point.py")
    p = subprocess.run([sys.executable, g0], capture_output=True, text=True, env=env)
    # THE REFUSAL IS READ OFF STDERR AND NOT STDOUT, and that moved at mg-c15e.  g0's stdout
    # is now inside g0's own watched class, so a refusal printed there would be a committed
    # transcript that disagrees with every tree where the handshake IS set — the oscillation
    # this ticket removed, arriving by the back door of the failure path.
    refused = p.returncode == 2 and "REFUSED" in p.stderr
    # AND THE TRANSCRIPT IS STILL THE ORDINARY ONE.  A refusal that emptied stdout, or that
    # wrote its reason there, would leave a tracked file this arm grades DISAGREES on the
    # next green run — which is the same fixed-point argument, on the failure path.
    intact = "§2  THE INPUTS" in p.stdout and "REFUSED" not in p.stdout
    out.append(("R2", "no %s handshake" % L.FRESH_ENV,
                "exit %d, refusal on stderr, transcript %s"
                % (p.returncode, "intact" if intact else "CLOBBERED"), refused and intact))
    return out


def main():
    t0 = time.time()
    print("=" * W)
    print("mg-f771  PLANTED WORLDS — what this control catches, and what it is declared blind to")
    print("=" * W)
    print()

    print("§1  WORLDS THAT MUST FIRE, AND THREE THAT MUST NOT")
    rule()
    bad = 0
    for wid, expect, what, committed, worktree in WORLDS:
        got = L.verdict_for(committed, worktree)
        ok = got == expect
        if not ok:
            bad += 1
        tag = "ok" if ok else "**WRONG**"
        direction = "  <- GREEN ON PURPOSE" if wid in MUST_NOT_FIRE else ""
        print("  %-4s expect %-9s got %-9s %-9s %s%s"
              % (wid, expect, got, tag, what, direction))
    print()
    print("  %d of %d worlds landed where they must." % (len(WORLDS) - bad, len(WORLDS)))
    print()

    print("§1b  THE CORPUS-SCOPED EXEMPTION, AND THE %d WORLDS THAT BOUND IT (mg-05c6)"
          % len(CORPUS_WORLDS))
    rule()
    print("  An exemption forgiving a difference that IS repo state needs a sharper fence")
    print("  than the normaliser's.  C2 is the fence: same pin, moved text, still RED.")
    print()
    corpus_bad = 0
    for cid, path, expect, what, committed, worktree in CORPUS_WORLDS:
        got = L.verdict_for(committed, worktree, path)
        ok = got == expect
        if not ok:
            corpus_bad += 1
        direction = "  <- GREEN ON PURPOSE" if cid in CORPUS_GREEN_ON_PURPOSE else ""
        print("  %-4s expect %-9s got %-9s %-9s %s%s"
              % (cid, expect, got, "ok" if ok else "**WRONG**", what, direction))
        print("       at %s" % (path if path else "<no path given to verdict_for>"))
    print()
    print("  %d of %d corpus worlds landed where they must." % (len(CORPUS_WORLDS) - corpus_bad,
                                                                len(CORPUS_WORLDS)))
    print()
    print("  THE REGISTRY IS A LIST OF %d PATH(S) AND WHAT IS NOT IN IT IS THE OTHER HALF:"
          % len(L.CORPUS_SCOPED))
    reg_bad = 0
    for rel, expect, why in CORPUS_MEMBERSHIP:
        got = rel in L.CORPUS_SCOPED
        if got != expect:
            reg_bad += 1
        print("      %-9s %-9s %s" % ("declared" if expect else "not",
                                      "ok" if got == expect else "**WRONG**", rel))
        print("           %s" % why)
    print()

    print("§2  THE WATCHED CLASS, WHICH IS TOTAL")
    rule()
    print("  An exemption that can widen without a control is not an exemption, it is a hole.")
    print("  There is none left: every row below that is OUT is out because it is not a")
    print("  transcript, and E1 — this arm's sibling, the one file that used to be exempt —")
    print("  is IN.  §2b and §2c are why that became possible.")
    print()
    member_bad = 0
    for eid, rel, expect, why in MEMBERSHIP:
        got = L.is_watched(rel)
        ok = got == expect
        if not ok:
            member_bad += 1
        print("  %-4s %-9s %-9s %s" % (eid,
                                       "watched" if expect else "not",
                                       "ok" if ok else "**WRONG**", rel))
        print("       %s" % why)
    print()
    print("  %d of %d membership rows are as declared." % (len(MEMBERSHIP) - member_bad,
                                                           len(MEMBERSHIP)))
    print()

    print("§2b  THE RULE INVENTORY g0 PRINTS INSTEAD OF ITS OUTCOME (mg-c15e)")
    rule()
    print("  A transcript that never moves cannot oscillate and buys nothing, so BOTH")
    print("  directions are here: %d widenings that must move it, one prose edit that must"
          % sum(1 for _i, m, _w, _o, _n in INVENTORY_WORLDS if m))
    print("  not, and %d restructurings that must REFUSE rather than answer about a rule that"
          % len(REFUSAL_PATCHES))
    print("  is no longer there.  Fed the real lib_f771.rule_inventory.")
    print()
    src = L.lib_source()
    base = L.rule_inventory(src)
    inv_bad = 0
    setup_failed = 0
    for wid, must_move, what, old, new in INVENTORY_WORLDS:
        if old not in src:
            setup_failed += 1
            print("  %-4s SETUP FAILED — the anchor is not in lib_f771.py: %s" % (wid, what))
            continue
        try:
            moved = L.rule_inventory(src.replace(old, new, 1)) != base
            outcome = "moved" if moved else "unmoved"
            ok = moved == must_move
        except L.Refused as exc:
            outcome, ok = "REFUSED (%s)" % str(exc)[:30], False
        if not ok:
            inv_bad += 1
        print("  %-4s expect %-8s got %-8s %-9s %s%s"
              % (wid, "moved" if must_move else "unmoved", outcome,
                 "ok" if ok else "**WRONG**", what,
                 "" if must_move else "  <- MUST NOT MOVE"))
    for wid, what, old, new in REFUSAL_PATCHES:
        if old not in src:
            setup_failed += 1
            print("  %-4s SETUP FAILED — the anchor is not in lib_f771.py: %s" % (wid, what))
            continue
        try:
            L.rule_inventory(src.replace(old, new, 1))
            outcome, ok = "answered anyway", False
        except L.Refused:
            outcome, ok = "REFUSED", True
        if not ok:
            inv_bad += 1
        print("  %-4s expect %-8s got %-8s %-9s %s"
              % (wid, "REFUSED", outcome, "ok" if ok else "**WRONG**", what))
    print()
    scrubbed = L.normalise("\n".join(base))
    inv_clean = scrubbed == "\n".join(base)
    if not inv_clean:
        inv_bad += 1
    print("  %-4s expect %-8s got %-8s %-9s the inventory is a FIXED POINT OF THE NORMALISER"
          % ("I8", "clean", "clean" if inv_clean else "MOVED",
             "ok" if inv_clean else "**WRONG**"))
    print("       itself — no checkout path and no decimal second in it, so it cannot even")
    print("       be forgiven by N1/N2 and has nothing to forgive.")
    print()

    print("§2c  THE CLAIM ITSELF, ON THE REAL ARM, IN THREE MINIATURE REPOSITORIES")
    rule()
    print("  Same instrument, two trees differing in one line of one watched transcript,")
    print("  and a third with a defect planted in it.")
    print("  The exemption is removable exactly if the outcome is absent from the bytes.")
    print()
    fp_bad, fp_rows = 0, []
    try:
        fp_rows = fixed_point_worlds()
        for fid, what, outcome, ok in fp_rows:
            if not ok:
                fp_bad += 1
            print("  %-4s %-9s %s" % (fid, "ok" if ok else "**WRONG**", what))
            print("       %s" % outcome)
    except (L.Refused, OSError) as exc:
        setup_failed += 1
        print("  SETUP FAILED — the sandboxes could not be built: %s" % exc)
    print()

    print("§3  WORLDS IN WHICH NO VERDICT IS AVAILABLE")
    rule()
    print("  A control that cannot say 'I could not tell' says 'nothing is wrong' instead.")
    print()
    refused_bad = 0
    for rid, what, outcome, ok in refusal_worlds():
        if not ok:
            refused_bad += 1
        print("  %-4s %-34s %-24s %s" % (rid, what, outcome, "ok" if ok else "**WRONG**"))
    print()

    print("§4  WHAT IS NOT COVERED HERE")
    rule()
    print("  The worlds above are hand-authored pairs.  They bound the NORMALISER; they say")
    print("  nothing about whether the watched class is the right class.  A gate suite that")
    print("  writes a tracked file NOT named out_*.txt would be invisible to g0 and to every")
    print("  world above, and nothing in this directory would notice.  Named rather than")
    print("  discovered: no such suite exists today, and that is a fact about today.")
    print()

    total_bad = (bad + member_bad + refused_bad + setup_failed + corpus_bad + reg_bad
                 + inv_bad + fp_bad)
    if setup_failed:
        print("VERDICT: REFUSED — %d world(s) could not be set up.  %.2fs"
              % (setup_failed, time.time() - t0))
        return 2
    if total_bad:
        print("VERDICT: RED — %d world(s) landed in the wrong place.  %.2fs"
              % (total_bad, time.time() - t0))
        return 1
    print("VERDICT: GREEN — %d planted worlds, %d corpus worlds, %d membership rows, %d "
          "registry rows, %d inventory worlds, %d fixed-point worlds and %d refusals all "
          "land where they must; the normaliser's blindness and the corpus-scoped exemption "
          "are the declared ones, and there is no self-exclusion left to declare.  %.2fs"
          % (len(WORLDS), len(CORPUS_WORLDS), len(MEMBERSHIP), len(CORPUS_MEMBERSHIP),
             len(INVENTORY_WORLDS) + len(REFUSAL_PATCHES) + 1, len(fp_rows), 2,
             time.time() - t0))
    return 0


if __name__ == "__main__":
    # As in g0: run_all.sh does not fold stderr into the transcript, so a crash is caught
    # here and printed to stdout.  `could not tell` is exit 2, never a silent green.
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except BaseException:                                   # noqa: BLE001 - deliberate
        import traceback
        print()
        print("REFUSED — this arm crashed and therefore reached no verdict:")
        traceback.print_exc(file=sys.stdout)
        sys.exit(2)
