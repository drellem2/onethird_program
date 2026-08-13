#!/usr/bin/env python3
"""mg-585e v3 — THE CANDIDATE ANSWER, BUILT AND RUN RATHER THAN PROPOSED.

The ticket's first carry-forward candidate, word for word:

    Whether a self-exempting transcript can be made NON-OSCILLATING — e.g. by recording the
    verdict's *inputs* rather than its *outcome*, so its text is not a function of what it
    reports.

`lib585e.invariant_report` is that transcript.  This arm subjects it to four tests, and three
of them are tests it could fail:

  §1  DOES IT OSCILLATE?  Run it on the red tree and the green tree of v2.  Byte-identical or
      the candidate is dead.

  §2  IS THE ANSWER VACUOUS?  A transcript of constant text also never oscillates and buys
      nothing: un-exempting it would add a file to the watched class that CANNOT disagree.
      So the report must still be a function of repo state.  Measured by moving the one piece
      of repo state it claims to read — the normaliser — and requiring the report to move.
      THIS IS THE WRONG-DIRECTION TEST and it is what makes §1's green falsifiable.

  §3  WAS ANYTHING LOST?  The outcome has to still exist somewhere.  Checked on the same red
      tree: g0's exit status and its stderr already carry the disagreement, so the proposal
      moves the outcome to a channel that is already carrying half of it.

  §4  IS THE OTHER INVARIANT CONTENT — A COUNT — THE BETTER TRADE?  A census of the watched
      class is also invariant under the repair, so it would also stop the oscillation.  It is
      priced here against the record rather than argued about, because it moves on every
      commit that adds or removes an out_*.txt, and that is mg-05c6's conflict class.

ONE PLANTED DEFECT, LIVE.  §1's byte-identity is exactly the kind of test that passes because
both sides are empty or because the comparison was never made.  So a deliberately broken
writer — the proposal with the verdict appended, i.e. the defect the proposal exists to
remove — is run through the same comparison and MUST come back CAUGHT.

EXITS 0 if every test lands where it must, 1 if any does not, 2 if a sandbox or the history
could not be reached.
"""

import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib585e as L  # noqa: E402

W = 92

# The plant.  A writer that is the proposal PLUS the outcome — which is what g0 does today.
# If the comparison in §1 cannot tell this apart from the proposal, the comparison is not a
# test and §1's green means nothing.
def broken_report(root, verdict):
    return L.invariant_report(root) + "VERDICT: %s\n" % verdict


def rule(ch="-"):
    print(ch * W)


def with_sandbox(world, fn, normaliser_patch=None):
    tmp = tempfile.mkdtemp(prefix="mg585e-v3-%s-" % world)
    try:
        L.build_sandbox(tmp, world, normaliser_patch=normaliser_patch)
        return fn(tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def membership_moves(as_of, since):
    """Commits in (since, as_of] that ADD or DELETE a tracked code/**/out_*.txt.

    One `git log --name-status` and not one call per commit: the question is about a range and
    a per-commit loop would be the same answer at 100x the git invocations.
    """
    p = L.git(L.ROOT, "log", "--format=@%H", "--name-status",
              "%s..%s" % (since, as_of), "--", "code")
    if p.returncode != 0:
        raise L.Refused("git log --name-status failed: %s" % (p.stderr or "").strip())
    movers, total, cur, hit = [], 0, None, False
    for ln in p.stdout.splitlines():
        if ln.startswith("@"):
            if cur and hit:
                movers.append(cur)
            if cur:
                total += 1
            cur, hit = ln[1:], False
            continue
        if not ln.strip():
            continue
        parts = ln.split("\t")
        status = parts[0][:1]
        paths = parts[1:]
        if status in ("A", "D"):
            for rel in paths:
                base = os.path.basename(rel)
                if rel.startswith("code/") and base.startswith("out_") and rel.endswith(".txt"):
                    hit = True
    if cur:
        total += 1
        if hit:
            movers.append(cur)
    return movers, total


def main():
    print("=" * W)
    print("mg-585e v3  A TRANSCRIPT OF THE INPUTS — built, run on both verdicts, and priced")
    print("=" * W)
    print()

    failures = []

    print("§1  DOES THE PROPOSED TRANSCRIPT OSCILLATE?")
    rule()
    try:
        red_text = with_sandbox("red", L.invariant_report)
        green_text = with_sandbox("green", L.invariant_report)
        noise_text = with_sandbox("noise", L.invariant_report)
    except L.Refused as exc:
        print("REFUSED — %s" % exc)
        return 2

    same_rg = red_text == green_text
    same_rn = red_text == noise_text
    print("  the SAME trees v2 ran the real g0 against, and the same one-line difference.")
    print()
    print("  proposed report on red tree == on green tree                    %s"
          % ("YES — BYTE-IDENTICAL" if same_rg else "NO"))
    print("  proposed report on red tree == on noise tree                    %s"
          % ("YES" if same_rn else "NO"))
    print("  bytes                                                          %d" % len(red_text))
    print("  and no scrubbing was applied to either side: there is no clock in it at all.")
    if not (same_rg and same_rn):
        failures.append("the proposed report is not verdict-invariant")
    print()

    print("  THE PLANT.  The same writer with the outcome appended — today's arrangement —")
    print("  put through the identical comparison.")
    try:
        b_red = with_sandbox("red", lambda r: broken_report(r, "RED — 1 disagreement"))
        b_green = with_sandbox("green", lambda r: broken_report(r, "GREEN — 0 disagreements"))
    except L.Refused as exc:
        print("REFUSED — %s" % exc)
        return 2
    caught = b_red != b_green
    print("  planted writer, red == green                                    %s"
          % ("no — CAUGHT" if caught else "YES — THE TEST IS BLIND"))
    if not caught:
        failures.append("the byte-identity test cannot tell the proposal from the defect it "
                        "removes; §1's green means nothing")
    print()

    print("§2  IS IT VACUOUS?  — THE WRONG-DIRECTION TEST")
    rule()
    print("  A constant file never oscillates and never disagrees, so admitting it to the")
    print("  watched class would buy exactly nothing.  The report must still MOVE when the")
    print("  thing it reports moves.  So: widen the normaliser in a sandbox and look.")
    print()
    # Widening N2 to eat integers too is the exact escape hatch lib_f771's own docstring
    # names as the unfalsifiable one, so it is the right mutation to plant.
    patch = (r'SECONDS = re.compile(r"\b\d+\.\d+\s*s\b")',
             r'SECONDS = re.compile(r"\b\d+(?:\.\d+)?\s*s\b")')
    try:
        widened = with_sandbox("green", L.invariant_report, normaliser_patch=patch)
    except L.Refused as exc:
        print("REFUSED — %s" % exc)
        return 2
    moved = widened != green_text
    print("  mutation      N2 widened to eat integer seconds as well as decimal ones")
    print("  report moved under the mutation                                 %s"
          % ("YES" if moved else "NO — THE REPORT IS CONSTANT AND THE ANSWER IS VACUOUS"))
    if not moved:
        failures.append("the proposed report does not move when the normaliser does")
    else:
        for a, b in zip(green_text.splitlines(), widened.splitlines()):
            if a != b:
                print("      -  %s" % a.strip()[:80])
                print("      +  %s" % b.strip()[:80])
    print()
    print("  SO THE EXEMPTION BECOMES REMOVABLE AND THE REMOVAL BUYS SOMETHING SPECIFIC.")
    print("  lib_f771's own docstring names its main risk: 'A WIDER NORMALISER IS AN")
    print("  UNFALSIFIABLE ESCAPE HATCH — an operator facing a real disagreement can silence")
    print("  it by widening the rule, and nothing in the machinery tells that edit from a")
    print("  correct one.'  With the report inside the watched class, an operator who widens")
    print("  the rule and does not re-run the gate is caught BY THE CONTROL THEY WIDENED.")
    print()

    print("§3  WAS ANYTHING LOST?")
    rule()
    try:
        rc, out, err = with_sandbox("red", L.run_g0)
    except L.Refused as exc:
        print("REFUSED — %s" % exc)
        return 2
    named = "out_sample.txt" in err
    print("  On the red tree, TODAY, with no change to g0 at all:")
    print("    exit status                                                   %d" % rc)
    print("    stderr names the disagreeing transcript                       %s"
          % ("YES" if named else "NO"))
    for ln in err.splitlines()[:4]:
        print("      %s" % ln[:86])
    print()
    if rc != 1 or not named:
        failures.append("the outcome is not already available off stdout")
    print("  The exit status is what `run_all.sh` reads and what `build.sh` folds into the")
    print("  gate verdict — the outcome has never travelled to the merge gate through the")
    print("  transcript.  And the per-file grading is ALREADY on stderr: g0 puts the")
    print("  moved/NOISE census there for exactly this reason (README D4).  The proposal")
    print("  moves ONE more line to a channel that is already carrying its neighbours.")
    print()
    print("  WHAT IS GENUINELY LOST, STATED RATHER THAN GLOSSED: the committed file stops")
    print("  being quotable for 'was the gate green'.  That is a real cost and mg-f771's own")
    print("  diagnosis is the reply — the file that opened that ticket was stale precisely")
    print("  BECAUSE the quotable part was the verdict, and lib_f771 says so in its first")
    print("  paragraph: 'the part written to be quotable was the wrong half'.")
    print()

    print("§4  THE OTHER INVARIANT CONTENT — A COUNT — IS THE WORSE TRADE, PRICED")
    rule()
    try:
        as_of = L.require_as_of()
        first = L.git(L.ROOT, "log", "--format=%H", "--follow", "--reverse", as_of,
                      "--", L.F771_TRANSCRIPT).stdout.split()[0]
        movers, total = membership_moves(as_of, first)
    except (L.Refused, IndexError) as exc:
        print("REFUSED — %s" % exc)
        return 2
    print("  window        %s..%s" % (first[:8], as_of[:8]))
    print("                from the commit that introduced the transcript, to the pin.")
    print("  commits in the window touching code/                            %d" % total)
    print("  ... that ADD or DELETE a tracked code/**/out_*.txt               %d" % len(movers))
    print()
    print("  A watched-class CENSUS is invariant under the repair, so it would not oscillate.")
    print("  It moves on each of those %d commits instead — and a moved census is the file"
          % len(movers))
    print("  every concurrent branch must regenerate, which is mg-05c6's conflict class in")
    print("  the merge queue rather than an extra commit in a worktree.")
    print()

    # THE TWO COUNTS CAN COME OUT EQUAL AND THEY ARE NOT THE SAME QUANTITY.  One is commits
    # that moved the watched-class MEMBERSHIP; the other is commits that touched the
    # transcript.  Printing the overlap is the only thing that keeps a reader from reading
    # the coincidence as an identity — mg-e8b0's `THE TWO 25s` discipline, applied here
    # because this arm produced exactly that shape.
    # Both counts over the IDENTICAL range `first..as_of`, which excludes the introducing
    # commit on both sides.  Two figures taken over windows that differ by one commit are
    # not comparable, and the fencepost is where a coincidence gets manufactured.
    touched_hist = set(L.git(L.ROOT, "log", "--format=%H", "--follow",
                             "%s..%s" % (first, as_of),
                             "--", L.F771_TRANSCRIPT).stdout.split())
    both = set(movers) & touched_hist
    print("  ⚠ commits that moved the MEMBERSHIP          %d" % len(movers))
    print("    commits that touched THE TRANSCRIPT        %d" % len(touched_hist))
    print("    in BOTH sets                              %d" % len(both))
    print("    These are different quantities over the same window; where they agree in size")
    print("    that is arithmetic and not identity, and the overlap row is what says so.")
    print()
    print("  THE INVENTORY IN §2 MOVES ON NEITHER.  It is a function of lib_f771.py, which")
    print("  neither the repair nor a new directory under code/ touches — so it is the only")
    print("  one of the three candidates that is invariant under BOTH.")
    print()

    if failures:
        print("VERDICT: RED — %d test(s) landed in the wrong place." % len(failures))
        for f in failures:
            print("    %s" % f)
        return 1
    print("VERDICT: GREEN — a verdict-invariant transcript exists, is not constant, loses only")
    print("  a quotable verdict, and is the only candidate invariant under the repair AND")
    print("  under a new directory landing.")
    return 0


if __name__ == "__main__":
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
