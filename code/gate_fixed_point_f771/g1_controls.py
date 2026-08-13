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
                 sharper fence than the normaliser's.  Eight worlds, three of them green on
                 purpose.  C2 is the one to read: same pin, moved text, still RED, which is
                 "the instrument changed its answer on an unchanged corpus".

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


def _census(pin, population, body):
    return ("corpus pin: %s  (%d directories, 2896 files, excluding code/x/)\n"
            "population: %d directories under code/\n%s" % (pin, population, population, body))


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


# The exemption must be ONE FILE and must not creep to the directory.  Each row is
# (id, relpath, watched?, why).
MEMBERSHIP = [
    ("E1", "code/gate_fixed_point_f771/out_g0_fixed_point.txt", False,
     "g0's own transcript — the one exemption, and the reason is in lib_f771.SELF_EXCLUDED"),
    ("E2", "code/gate_fixed_point_f771/out_g1_controls.txt", True,
     "THIS transcript is watched: the exemption is a file, not this directory"),
    ("E3", "code/gate_fixed_point_f771/README.md", False,
     "not a transcript at all"),
    ("E4", "code/facts_registry_03cf/out_f0_registry_discipline.txt", True,
     "the file that opened mg-f771"),
    ("E5", "code/libweak_audit_c4f5/out_a4_census.txt", True,
     "mg-c824's — IN the class, and safe because nothing regenerates it (README §3)"),
    ("E6", "STATE.md", False,
     "outside the class, so a local STATE.md edit does not trip a transcript control"),
    ("E7", "docs/FACTS.md", False,
     "outside the class"),
]


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
    ok = p.returncode == 2 and "REFUSED" in p.stdout
    out.append(("R2", "no %s handshake" % L.FRESH_ENV,
                "exit %d" % p.returncode, ok))
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

    print("§2  THE WATCHED CLASS, AND THE ONE EXEMPTION IN IT")
    rule()
    print("  An exemption that can widen without a control is not an exemption, it is a hole.")
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

    print("§3  WORLDS IN WHICH NO VERDICT IS AVAILABLE")
    rule()
    print("  A control that cannot say 'I could not tell' says 'nothing is wrong' instead.")
    print()
    refused_bad = 0
    setup_failed = 0
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

    total_bad = bad + member_bad + refused_bad + setup_failed + corpus_bad + reg_bad
    if setup_failed:
        print("VERDICT: REFUSED — %d world(s) could not be set up.  %.2fs"
              % (setup_failed, time.time() - t0))
        return 2
    if total_bad:
        print("VERDICT: RED — %d world(s) landed in the wrong place.  %.2fs"
              % (total_bad, time.time() - t0))
        return 1
    print("VERDICT: GREEN — %d planted worlds, %d corpus worlds, %d membership rows, %d "
          "registry rows and %d refusals all land where they must; the normaliser's "
          "blindness, the corpus-scoped exemption and the one self-exclusion are all the "
          "declared ones.  %.2fs" % (len(WORLDS), len(CORPUS_WORLDS), len(MEMBERSHIP),
                                     len(CORPUS_MEMBERSHIP), 2, time.time() - t0))
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
