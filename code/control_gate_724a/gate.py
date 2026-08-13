#!/usr/bin/env python3
"""mg-724a — THE GATE.  This is the thing that ASKS the two control suites, on every merge.

WHAT WAS WRONG.  mg-9876 enumerated 50 arms across 59 sites, repaired 7, and demonstrated all
50 RED against a known-bad input.  Nothing ran any of it.  No hook, no CI, no gate, no
schedule — both suites were inert until a human typed `sh run_all.sh`.  MEASURED, not
assumed: of the 48 merge requests this repository has put through the refinery, 46 merged
carrying the refinery's own sentence `(no quality gates configured)` in their gate output,
and the other 2 failed before reaching the gate step.  Zero gates have ever run here.

WHY THIS IS NOT SIMPLY `[gates] commands = ["sh .../run_all.sh"]`.  Because that gate is RED
ON ARRIVAL and would block every merge in this repository from the moment it landed:

    code/control_audit_9876/run_all.sh        exits 1 today — a2 scores arm C3
                                              UNFALSIFIABLE, a standing recorded finding
    code/rendered_twin_pin_9bc2/run_all.sh    exits 0 today, ON DRIFT, deliberately

and the second half is the worse one.  The twin's runner exits 0 whether its drift worklist
is `8` or `7 8` or `1 2 7 8`, because drift is the normal condition of a hand-maintained
rendering and its header says so.  A gate reading THAT suite's exit code cannot see a
published ledger row moving away from its rendered twin — the exact event mg-64cb is about.
DEMONSTRATED rather than argued: change row 7 of STATE.md's ledger and the worklist goes from
`8` to `7 8` while the runner still exits 0 (out_exhibit_local.txt in this directory).

SO THE GATE IS A COMPARISON AGAINST A DECLARED BASELINE, NOT AN EXIT CODE.  BASELINE.json
declares, per field, the value this repository stands at today and WHY.  RED is:

    a GATED field's observed value differs from its declared value — IN EITHER DIRECTION.

The green direction matters as much as the red one.  If `audit.arms_not_shown` goes 1 -> 0,
some branch either repaired arm C3 or stopped asking, and those have opposite meanings.  The
remedy is the same for both and it is one line: move the value in BASELINE.json IN THE SAME
COMMIT and write the reason into its `why`.  That is this gate's whole cost to an author who
legitimately changes the estate, and it is the point — a control's power may change, but not
silently.

THE GATE IS ITSELF A CONTROL, so it demonstrates that it can fail (§4) and that it can refuse
(§5) on every run, against the bytes of that run.  See negative_control.py.

EXITS: 0 baseline matched · 1 a gated field diverged · 2 REFUSED, or a hole in this gate.
DECISION LINE: `GATE VERDICT: ...`, printable only by reaching the end of the reasoning.
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib724a as L                 # noqa: E402
import negative_control as NC       # noqa: E402


def main():
    print("=" * 92)
    print("mg-724a — MERGE GATE over the two control suites mg-9876 audited")
    print("=" * 92)
    print()

    # ---- §1 -------------------------------------------------------------------------------
    print("§1  THE SUITES, RUN — and what each one costs on the merge critical path")
    print("-" * 92)
    transcripts, exits, timings = {}, {}, {}
    t_all = time.time()
    try:
        for suite, rel in L.SUITES:
            t0 = time.time()
            rc, text = L.run_suite(rel)
            timings[suite] = time.time() - t0
            exits[suite], transcripts[suite] = rc, text
            # THE TIMING IS NOT COLUMN-PADDED, AND THAT IS A REPAIR RATHER THAN A STYLE
            # CHOICE (mg-1344).  It read `%6.1fs`, which right-aligns, so `97.6s` carries one
            # more leading space than `100.4s`.  mg-f771's normaliser rewrites the NUMBER to
            # `<t>s` and cannot touch the padding around it, so this line disagreed with its
            # committed copy across the 100-second boundary and the merge gate went RED for a
            # wall-clock difference it had already declared to be noise.  MEASURED, not
            # predicted: two consecutive runs on this host at 97.6s and 100.4s did exactly
            # that.  The fix belongs HERE and not in the normaliser — widening that is the
            # unfalsifiable escape hatch lib_f771's own header refuses, and it would swallow
            # real differences to hide a formatting one.
            print("  %-6s %-42s exit %-3d %.1fs  %d bytes"
                  % (suite, rel, rc, timings[suite], len(text)))
        t_suites = time.time() - t_all
        baseline = L.load_baseline()
        observed = L.extract(transcripts, exits)
        rows, gated = L.compare(observed, baseline)
    except L.Refusal as exc:
        print()
        print("REFUSED while reading the estate:")
        for line in str(exc).splitlines():
            print("  " + line)
        print()
        print("GATE VERDICT: REFUSED — this gate did not reach a decision, so nothing above is")
        print("evidence about the branch.  A gate that maps 'could not tell' onto 'nothing")
        print("wrong' is the defect this whole line of work exists to remove.")
        return 2
    print("  %-6s %-42s      %.1fs total" % ("", "(both suites)", t_suites))
    print()

    # ---- §2 -------------------------------------------------------------------------------
    print("§2  OBSERVED vs BASELINE.json")
    print("-" * 92)
    base_rows = {r["field"]: r for r in rows}
    print(L.render_report(rows))
    print()
    moved = [r for r in rows if r["status"] != "MATCH"]
    if moved:
        print("  Why each field that moved is declared the way it is:")
        for r in moved:
            print("    %s (%s):" % (r["field"], r["class"]))
            for line in _wrap(r["why"], 84):
                print("      " + line)
    else:
        print("  Every field matches.  Nothing moved.")
    print()

    # ---- §3 -------------------------------------------------------------------------------
    recorded = [r["field"] for r in rows if r["class"] == "recorded"]
    print("§3  WHAT THIS GATE DELIBERATELY DOES NOT GATE — named, not omitted")
    print("-" * 92)
    print("  %d of %d fields are RECORDED rather than gated:" % (len(recorded), len(rows)))
    for f in recorded:
        print("      " + f)
    print("  They are population counts over EVERY directory under code/, so they move when")
    print("  any ticket adds code — including this one.  Gating them would turn unrelated work")
    print("  red, and a gate that fails for reasons its author cannot act on is a gate that")
    print("  gets removed six weeks later.  Both values are printed in §2 so the drift stays")
    print("  visible, and probe T10 below demonstrates the silence rather than promising it.")
    print()

    # ---- §4 -------------------------------------------------------------------------------
    print("§4  CAN THIS GATE FAIL?  Mutations of the bytes THIS run captured")
    print("-" * 92)
    t0 = time.time()
    muts = NC.run_mutations(transcripts, exits, baseline, base_rows, gated)
    t_mut = time.time() - t0
    width = max(len(m[1]) for m in muts)
    holes = sum(1 for m in muts if m[2] in ("HOLE", "SETUP FAILED"))
    unfals = sum(1 for m in muts if m[2] == "UNFALSIFIABLE")
    for mid, what, status, detail in muts:
        print("  %-4s %-*s  %-26s  %s" % (mid, width, what, status, detail))
    print()
    print("  %d of %d probes CAUGHT; %d hole(s)/setup failure(s); %d unexplained "
          "UNFALSIFIABLE.  %.2fs." % (len(muts) - holes - unfals, len(muts), holes, unfals, t_mut))
    print()

    # ---- §5 -------------------------------------------------------------------------------
    print("§5  CAN THIS GATE REFUSE?  Self-contained worlds, nothing borrowed from the estate")
    print("-" * 92)
    t0 = time.time()
    worlds = NC.run_synthetic_worlds(baseline, observed)
    t_world = time.time() - t0
    wwidth = max(len(w[1]) for w in worlds)
    wholes = sum(1 for w in worlds if w[2] != "CAUGHT")
    for wid, what, status, detail in worlds:
        print("  %-4s %-*s  %-7s  %s" % (wid, wwidth, what, status, detail))
    print()
    print("  %d of %d worlds refused as required; %d hole(s).  %.2fs."
          % (len(worlds) - wholes, len(worlds), wholes, t_world))
    print()

    # ---- decision --------------------------------------------------------------------------
    print("=" * 92)
    if holes or wholes or unfals:
        print("GATE VERDICT: BROKEN — %d hole(s) in this gate's own falsification.  It is not"
              % (holes + wholes + unfals))
        print("evidence about the branch, and it is not a green one.")
        print("=" * 92)
        return 2
    if gated:
        print("GATE VERDICT: RED — %d gated field(s) differ from BASELINE.json: %s"
              % (len(gated), ", ".join(gated)))
        print("=" * 92)
        print()
        print("WHAT TO DO.  Either this branch changed what a control can see — fix the branch —")
        print("or it changed the estate on purpose, in which case move the value in")
        print("BASELINE.json IN THIS COMMIT and write the reason into that field's `why`.")
        print("Both are one-line diffs.  What is not available is landing the change and")
        print("leaving the declared state behind it, which is the whole of what this gate buys.")
        return 1
    print("GATE VERDICT: GREEN — every gated field matches BASELINE.json, and this gate was")
    print("shown able to fail on %d probes and to refuse in %d worlds, on this run, against"
          % (len(muts), len(worlds)))
    print("these bytes.  Total %.1fs." % (time.time() - t_all))
    print("=" * 92)
    return 0


def _wrap(text, width):
    words, line, out = text.split(), "", []
    for w in words:
        if len(line) + len(w) + 1 > width:
            out.append(line)
            line = w
        else:
            line = (line + " " + w).strip()
    if line:
        out.append(line)
    return out


if __name__ == "__main__":
    sys.exit(main())
