#!/usr/bin/env python3
"""mg-502f — THE SWEEP.  Which tracked scripts run `./build.sh` while a shell redirect is
holding one of the gate's own inputs open?

mg-479c found one — `code/alias_agreement_06d1/x0_exhibit.py` — repaired it, and said in
terms that it had not swept for others: "ANYTHING ELSE IN THE ESTATE THAT SHELLS
`./build.sh` WHILE WRITING INTO `code/**/out_*.txt` HAS THIS BUG.  I did not sweep for
others."  This is that sweep.

WHAT IS ON STDOUT AND WHAT IS ON STDERR, AND WHY THE SPLIT IS NOT COSMETIC.  This is a
LIVE instrument: it reads every tracked script in the estate, so a transcript that recorded
"1164 python files scanned" would move on any branch that adds a file, and mg-f771's
control — which grades this suite's own committed transcript — would call that a
disagreement.  That is mg-f771's own D4, learned on its second run and written into
`g0_fixed_point.py`: "THIS TRANSCRIPT RECORDS ONLY WHAT IS A FUNCTION OF REPO STATE".
Here the rule bites slightly differently — the population IS repo state, it is just
VOLATILE repo state that no reader can act on — so the split is by what a human would do
about it.  STDOUT carries the exec-edge sites and their verdicts, which change only when
somebody writes a new script that runs the gate.  STDERR carries the population counts,
which change constantly and mean nothing on their own.

EXITS 0 if no tracked script is in the class, 1 if one is, 2 if this arm could not reach a
decision.
"""

import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lib_502f as L  # noqa: E402

W = 92


def rule(ch="-"):
    print(ch * W)


def read(root, rel):
    try:
        with open(os.path.join(root, rel), encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return None


def main(root=L.ROOT):
    t0 = time.time()
    print("=" * W)
    print("mg-502f  SELF-RED EXHIBITS — does any tracked script redden the gate it is running?")
    print("=" * W)
    print()

    try:
        files = L.tracked(root)
    except L.Refused as exc:
        print("REFUSED — %s" % exc)
        return 2

    tracked_set = set(files)
    transcripts = [f for f in files if L.is_transcript(f)]
    pys = [f for f in files if f.endswith(".py")]
    shs = [f for f in files if f.endswith(".sh")]
    texts = {}       # every tracked source, for §B's binding rules
    hot = {}         # the prefiltered subset §0 and §1 parse — lib_502f.mentions()
    for rel in files:
        if rel.endswith((".py", ".sh", ".md")):
            body = read(root, rel)
            if body is None:
                continue
            texts[rel] = body
            if L.mentions(body):
                hot[rel] = body

    # ---------------------------------------------------------------- §0
    print("§0  THE TARGET SET — what actually runs mg-f771's control")
    rule()
    print("  The precondition names `./build.sh` OR any target that runs")
    print("  gate_fixed_point_f771.  Those are the same set in this repository, and that is")
    print("  MEASURED here rather than asserted: f771 refuses without the handshake")
    print("  %s, so every route to it passes through a line that" % L.HANDSHAKE)
    print("  sets that variable.  Tracked lines that set it, comments excluded:")
    print()
    setters = L.handshake_setters(hot)
    for rel, i, s in setters:
        print("      %s:%d  %s" % (rel, i, s[:62]))
    if len(setters) != 1 or setters[0][0] != "build.sh":
        print()
        print("  MORE THAN ONE ROUTE, OR A ROUTE THAT IS NOT build.sh.  This sweep's §1 looks")
        print("  for `build.sh` and would miss the others.  REFUSED rather than under-report.")
        return 2
    print()
    print("  TWO DIRECTORIES ARE EXEMPT FROM THIS QUESTION AND FROM THIS QUESTION ONLY.")
    print("  Each is shown with how many handshake mentions in CODE it was not asked about,")
    print("  so the exemption is a stated number rather than a silence.  lib_502f")
    print("  ROUTE_EXEMPT carries the reason for each; s0_controls D16-D18 hold the list to")
    print("  these two and check that a route planted outside them is still caught.")
    for d in L.ROUTE_EXEMPT:
        inside = {k: v for k, v in hot.items() if k.startswith(d)}
        n = len(L.handshake_setters(inside, exempt=()))
        print("      %-34s %d mention(s) in code, not asked about" % (d, n))
    print()
    print("  §1 STILL SCANS BOTH OF THEM for exec edges to `./build.sh`, by the same rule it")
    print("  applies everywhere else — the exemption suppresses §0's question, not §1's.")
    print()
    print("  ONE ROUTE, AND IT IS build.sh.  §1 may therefore look for `build.sh` alone.")
    print()

    # ---------------------------------------------------------------- §1
    print("§1  THE EXEC EDGES — tracked scripts that can reach `./build.sh`")
    rule()
    print("  A gate literal in CODE (not in a docstring, not in a `#` comment) plus an exec")
    print("  primitive somewhere in the same file.  The two conditions are DECOUPLED and")
    print("  the reason is a miss: the tighter rule 'a gate literal inside an exec call'")
    print("  was written first and did not see x1_positive_control.py, which builds the")
    print("  argv and hands it to a local helper.  One hop defeated it.  lib_502f §A.")
    print()
    sites = []
    broken = []
    for rel in pys:
        src = hot.get(rel)
        if src is None:
            continue
        try:
            lits, execs = L.py_gate_edge(src)
        except SyntaxError as exc:
            broken.append((rel, str(exc)[:60]))
            continue
        if lits:
            sites.append((rel, lits, execs))
    sh_sites = []
    for rel in shs + (["build.sh"] if "build.sh" in tracked_set else []):
        src = hot.get(rel)
        if src is None:
            continue
        lines = L.sh_gate_edge(src)
        if lines:
            sh_sites.append((rel, lines))

    for rel, lits, execs in sorted(sites):
        print("  %-52s gate literal in code at %s" % (rel, lits))
        print("  %-52s exec primitive at        %s"
              % ("", execs[:6] if execs else "NONE — prose, not an invocation"))
    for rel, lines in sorted(sh_sites):
        print("  %-52s shell invocation at      %s" % (rel, lines))
    if broken:
        print()
        for rel, exc in broken:
            print("  UNPARSEABLE (reported, not skipped silently): %s — %s" % (rel, exc))
    print()

    # ---------------------------------------------------------------- §2
    print("§2  THE VERDICTS")
    rule()
    print("  INSTANCE  runs the gate, a tracked transcript is bound to it, and the script")
    print("            does NOT write that file itself — so the committed bytes can only")
    print("            have arrived by a capture, and the next capture is self-red.")
    print("  EXPOSED   runs the gate, writes its own transcript (mg-479c's repair), but does")
    print("            not REFUSE the redirect.  The default invocation is safe and the old")
    print("            one is still published — in build.sh's own mg-479c block and in")
    print("            mg-502f's ticket body — and typing it truncates the file again.")
    print("  GUARDED   runs the gate and REFUSES when its stdout is a tracked transcript.")
    print("  NO-BIND   runs the gate; no tracked transcript is bound to it.")
    print("  PROSE     the gate literal is a printed string; nothing here runs the gate.")
    print()
    instances = []
    for rel, lits, execs in sorted(sites):
        src = texts[rel]
        if not execs:
            print("  PROSE     %s" % rel)
            print("            gate named at %s; no exec primitive in the file." % lits)
            continue
        binds = L.bindings(rel, tracked_set, texts)
        if not binds:
            print("  NO-BIND   %s" % rel)
            print("            runs the gate; no tracked out_*.txt is bound to it.")
            continue
        for tr, why in binds:
            writes = L.self_writes(src, tr)
            if L.calls_guard(src):
                v = "GUARDED"
            elif writes:
                v = "EXPOSED"
            else:
                v = "INSTANCE"
            print("  %-9s %s" % (v, rel))
            print("            transcript %s   bound by %s" % (tr, why))
            if v == "GUARDED":
                print("            refuses when stdout IS a tracked transcript, so no run of this")
                print("            script can hand the gate a truncated file.  Writes it: %s."
                      % ("YES" if writes else "NO"))
            elif v == "EXPOSED":
                print("            writes it itself, so the DEFAULT invocation is safe; nothing")
                print("            refuses the published redirect, so the old one is not.")
                instances.append((rel, tr, v))
            else:
                print("            does not write it, so the committed bytes arrived by a capture")
                print("            and every regeneration hands the gate a truncated file.")
                instances.append((rel, tr, v))
    if not sites:
        print("  (no exec edges)")
    print()

    # ---------------------------------------------------------------- §3
    print("§3  WHAT THIS SWEEP CANNOT SEE")
    rule()
    print("  * `cmd | tee code/d/out_s.txt`.  A pipe leaves no literal for §B to bind and")
    print("    no regular file for the guard to recognise.  This estate forbids the pipe")
    print("    form already, for an older and unrelated reason (`cmd | tee f` makes `$?`")
    print("    tee's status — mg-9bc2, restated in three runners), so the forbidden form")
    print("    and the invisible form coincide.  That is luck, not design.")
    print("  * an UNTRACKED script.  Nothing outside `git ls-files` is read, and a script")
    print("    nobody committed is a script this sweep is not claiming anything about.")
    print("  * a shell that reaches the gate through a variable — `G=./build.sh; $G`.")
    print("    §1's shell rule matches a literal.  No tracked shell file does this today")
    print("    and one that did would be reported by nothing here.")
    print()

    err = sys.stderr
    err.write("mg-502f s1: population — %d tracked files, %d .py, %d .sh, %d transcripts, "
              "%d unparseable\n" % (len(files), len(pys), len(shs), len(transcripts),
                                    len(broken)))
    err.write("mg-502f s1: %d exec-edge site(s), %d instance(s)\n"
              % (len(sites) + len(sh_sites), len(instances)))

    if instances:
        n_i = sum(1 for _, _, v in instances if v == "INSTANCE")
        n_e = len(instances) - n_i
        print("VERDICT: RED — %d self-red exhibit(s): %d INSTANCE, %d EXPOSED.  %.2fs"
              % (len(instances), n_i, n_e, time.time() - t0))
        return 1
    print("VERDICT: GREEN — no tracked script runs `./build.sh` into a file the gate reads.")
    print("  %.2fs" % (time.time() - t0))
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
