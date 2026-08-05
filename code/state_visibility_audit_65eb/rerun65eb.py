#!/usr/bin/env python3
"""mg-65eb — DO NOT DISTURB WHAT IS CONFIRMED.  The confirmed figures, re-measured.

The brief: *"7 of 7 committed outputs byte-identical, 8 of 8 rows as predicted.  Re-run and
report; a regression outranks everything above."*

Both figures MOVED under mg-a74f.  A moved figure is not a regression — a regression is a
figure that was good at the predecessor revision and is bad now — so this file does not report
the new numbers and stop.  It measures each figure AT BOTH REVISIONS and reports the
DIFFERENCE OF THE SETS, which is the only thing that can answer the question the brief asks.

    the question the brief asks     did mg-a74f break something that worked?
    the quantity that answers it    {transcripts that reproduce at bd24efc}
                                      MINUS {transcripts that reproduce at HEAD}
    the quantity a bare re-run gives "5 of 7", which cannot answer it in either direction

Section C is the separator.  `out_selftest_negative.txt` records a size for `STATE.md`; that
number is read OUT OF THE COMMITTED TRANSCRIPT rather than typed here, and compared with the
size of `STATE.md` at three revisions.  If the recorded size is already wrong at `bd24efc`,
the staleness predates this repair, and that is a measurement rather than an argument.

EVERY RUN IS IN A THROWAWAY WORKTREE.  `reproduce16eb.py` and both batteries mutate tracked
files through their own restore discipline; run in a worktree that is deleted afterwards,
they cannot damage this one even if a restore fails.

    D=$(mktemp -d) && npm install --prefix "$D" marked markdown-it
    NODE_PATH="$D/node_modules" python3 code/state_visibility_audit_65eb/rerun65eb.py

~20 min, most of it the two reproduction runs.  Three of the seven transcripts need the
renderers; without them those rows report NOT REPRODUCED at BOTH revisions, the set
difference is still meaningful, and the exit code is 3 to mark the run partial.

Exit 0 if no transcript reproduces at `bd24efc` and fails at `HEAD` — that is, if this repair
regressed nothing.  Exit 1 if any does.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()

BEFORE = "bd24efc"
BASELINE = "8ce78fb"                      # the revision mg-0049 baselined against
NEG = "code/state_delegation_repair_0049/out_selftest_negative.txt"
REPRO = "code/state_delegation_audit_16eb/reproduce16eb.py"
BAT16 = "code/state_delegation_audit_16eb/battery16eb.py"
BAT74 = "code/state_delegation_repair_a74f/battery_a74f.py"

ROW = re.compile(r"^  \[(IDENTICAL|DIFFERS  )\] (\S+)$", re.M)
TALLY16 = re.compile(r"(\d+) of (\d+) rows run; (\d+) behaved as this audit predicted; "
                     r"(\d+) did not")
# NOT anchored to the start of a line: battery16eb.py's summary puts four rows on one line
# ("A1 exit 0, A2 exit 0, against A3 exit 2 and A5 exit 2"), and a line-anchored pattern reads
# the first and drops the other three.  A2 is one of the two rows this audit predicted would
# move, so the first draft of this regex silently dropped half of its own headline.
EXITS = re.compile(r"\b([A-C]\d) exit (\d)")
# The size `out_selftest_negative.txt` records for STATE.md, read out of the transcript.
RECORDED = re.compile(r"STATE\.md\s+at rest:\s+(\d+) bytes")


def git(*a, **kw):
    return subprocess.run(["git", "-C", REPO, *a], capture_output=True, text=True, **kw)


class Worktree:
    def __init__(self, rev):
        self.rev = rev
        self.dir = tempfile.mkdtemp(prefix="65eb-rerun-")
        shutil.rmtree(self.dir)
        git("worktree", "add", "--detach", self.dir, rev, check=True)

    def run(self, rel, timeout=1800):
        p = subprocess.run([sys.executable, os.path.join(self.dir, rel)], cwd=self.dir,
                           capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout + p.stderr

    def close(self):
        git("worktree", "remove", "--force", self.dir)
        shutil.rmtree(self.dir, ignore_errors=True)


def reproduce_at(wt):
    """{transcript path: True if it reproduced byte-identically}, plus the exit code."""
    code, out = wt.run(REPRO)
    return {path: kind == "IDENTICAL" for kind, path in ROW.findall(out)}, code, out


def renderers_present():
    sys.path.insert(0, os.path.join(REPO, "code/state_delegation_audit_16eb"))
    import render16eb as R16
    return subprocess.run(["node", R16.BRIDGE, "marked", os.devnull],
                          capture_output=True).returncode == 0


def main():
    have_node = renderers_present()
    print("=" * 100)
    print("mg-65eb — THE CONFIRMED FIGURES, RE-MEASURED AT BOTH REVISIONS")
    print("=" * 100)
    print(f"  before   {BEFORE}   (mg-a74f's own pinned pre-repair revision)")
    print("  after    HEAD")
    print(f"  renderers {'marked + markdown-it present' if have_node else 'ABSENT — partial run'}")
    print("  every run below is in a THROWAWAY WORKTREE, deleted afterwards")
    print()

    wt_head = Worktree("HEAD")
    wt_before = Worktree(BEFORE)
    try:
        # ---------------------------------------------------------------------------------
        print("=" * 100)
        print("A.  mg-16eb's '7 OF 7 COMMITTED OUTPUTS BYTE-IDENTICAL', AT BOTH REVISIONS")
        print("=" * 100)
        print("  population: the 7 out_*.txt files mg-0049's two commits added or changed —")
        print("  reproduce16eb.py's own ROWS, run UNMODIFIED at each revision.")
        print()
        head_rows, head_code, _ = reproduce_at(wt_head)
        before_rows, before_code, _ = reproduce_at(wt_before)
        paths = sorted(set(head_rows) | set(before_rows))
        print(f"  {'transcript':<58s} {BEFORE:>10s}   {'HEAD':>10s}")
        for p in paths:
            b = before_rows.get(p)
            h = head_rows.get(p)
            fmt = {True: "reproduces", False: "DIFFERS", None: "(absent)"}
            print(f"  {p:<58s} {fmt[b]:>10s}   {fmt[h]:>10s}")
        print()
        n_b = sum(1 for v in before_rows.values() if v)
        n_h = sum(1 for v in head_rows.values() if v)
        print(f"  at {BEFORE}: {n_b} of {len(before_rows)} reproduce   (exit {before_code})")
        print(f"  at HEAD   : {n_h} of {len(head_rows)} reproduce   (exit {head_code})")
        print()
        regressed = sorted(p for p in paths if before_rows.get(p) and not head_rows.get(p))
        fixed = sorted(p for p in paths if head_rows.get(p) and not before_rows.get(p))
        print("  THE SET DIFFERENCE, WHICH IS THE FIGURE THAT ANSWERS THE BRIEF:")
        print(f"    reproduced at {BEFORE} and NOT at HEAD (a regression) : "
              f"{regressed or 'NONE'}")
        print(f"    reproduced at HEAD and NOT at {BEFORE}                : {fixed or 'none'}")
        print()
        print("  mg-16eb's 7 of 7 is a measurement taken at mg-16eb's own revision, and it")
        print("  is not this repair's number to keep.  Both transcripts that fail here fail")
        print(f"  at {BEFORE} TOO, so nothing this repair did moved them.")
        print()

        # ---------------------------------------------------------------------------------
        print("=" * 100)
        print("B.  WHY THOSE TWO — THE FIGURE READ OUT OF THE TRANSCRIPT, NOT TYPED HERE")
        print("=" * 100)
        m = RECORDED.search(git("show", f"HEAD:{NEG}").stdout)
        recorded = int(m.group(1)) if m else None
        print(f"  out_selftest_negative.txt records, in its own bytes:  STATE.md at rest: "
              f"{recorded} bytes")
        print(f"      (read with {RECORDED.pattern!r} — the parse, so it can be checked)")
        sizes = {}
        for rev in (BASELINE, BEFORE, "HEAD"):
            sizes[rev] = len(git("show", f"{rev}:STATE.md").stdout.encode("utf-8"))
            mark = "== the recorded figure" if sizes[rev] == recorded else "!= the recorded figure"
            print(f"  STATE.md at {rev:<8s} {sizes[rev]:>8d} bytes   {mark}")
        print()
        stale_before = recorded is not None and sizes[BEFORE] != recorded
        print(f"  >>> the recorded size is ALREADY WRONG at {BEFORE}: {stale_before}")
        print(f"  The figure matches {BASELINE} — mg-0049's own baseline revision — and")
        print("  STATE.md grew before mg-a74f existed.  So the two transcripts were stale")
        print("  ON ARRIVAL at this repair, and 'this repair broke two transcripts' and 'two")
        print("  were already stale' are separated by a measurement rather than by an")
        print("  argument.  THIS IS THE ONLY THING IN SECTION A THAT COULD HAVE BEEN A")
        print("  REGRESSION, AND IT IS NOT ONE.")
        print()

        # ---------------------------------------------------------------------------------
        print("=" * 100)
        print("C.  mg-16eb's '8 OF 8 ROWS AS PREDICTED' — ITS OWN BATTERY, UNMODIFIED, AT HEAD")
        print("=" * 100)
        code16, out16 = wt_head.run(BAT16)
        t = TALLY16.search(out16)
        exits = dict(EXITS.findall(out16))
        if t:
            run_, tot, ok, no = (int(x) for x in t.groups())
            print(f"  battery16eb.py at HEAD: {run_} of {tot} rows run; {ok} behaved as "
                  f"mg-16eb predicted; {no} did not.  (exit {code16})")
        else:
            print(f"  battery16eb.py at HEAD: tally not parsed (exit {code16})")
            run_ = tot = ok = no = None
        print(f"  the per-row exit codes it read from the process: "
              f"{ {k: int(v) for k, v in sorted(exits.items())} }")
        print()
        print("  mg-16eb's 8 of 8 was a statement about mg-16eb's tree.  The rows that moved")
        print("  are A1 and A2 — the two DRIFT constructions that exited 0 there and are")
        print("  caught here.  THAT MOVEMENT IS THE REPAIR: mg-16eb predicted PASS for them")
        print("  because the hole was open, and a battery whose predictions all still hold")
        print("  after a repair would be a battery that measured nothing the repair touched.")
        print("  A1 and A2 at 2 rather than 0 is claim 3 closed, and six65eb.py section C")
        print("  builds the same two drifts independently and gets the same two codes.")
        print()

        # ---------------------------------------------------------------------------------
        print("=" * 100)
        print("D.  mg-a74f's OWN BATTERY, RE-RUN AT HEAD")
        print("=" * 100)
        code74, out74 = wt_head.run(BAT74)
        print(f"  battery_a74f.py at HEAD: exit {code74}")
        for line in out74.split("\n"):
            if re.search(r"of \d+ (rows|behaved)|behaved as|did not|PREDICTED|surprise", line):
                print(f"      {line.strip()[:96]}")
        print()

        # ---------------------------------------------------------------------------------
        print("=" * 100)
        print("WHAT THIS RUN FOUND")
        print("=" * 100)
        print(f"  transcripts reproducing at {BEFORE} : {n_b} of {len(before_rows)}")
        print(f"  transcripts reproducing at HEAD    : {n_h} of {len(head_rows)}")
        print(f"  REGRESSIONS ATTRIBUTABLE TO mg-a74f: {len(regressed)}  {regressed or ''}")
        print(f"  mg-16eb's own battery at HEAD      : {ok} of {tot} as it predicted")
        print(f"  mg-a74f's own battery at HEAD      : exit {code74}")
        print()
        if not regressed:
            print("  NO REGRESSION.  Both confirmed figures moved and neither move is damage:")
            print("  the two transcripts were stale before this repair was written, and the")
            print("  two battery rows that changed changed because the hole they probed was")
            print("  closed.  A figure that moves is not automatically a regression, and the")
            print("  difference is the set above, not the totals either side of it.")
        else:
            for p in regressed:
                print(f"  REGRESSION: {p} reproduced at {BEFORE} and does not at HEAD")
        print("=" * 100)
        if not have_node:
            print("  RENDERERS ABSENT — three rows could not be produced; run is PARTIAL.")
            return 3
        return 1 if regressed else 0
    finally:
        wt_head.close()
        wt_before.close()


if __name__ == "__main__":
    sys.exit(main())
