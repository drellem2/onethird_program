#!/usr/bin/env python3
"""mg-585e v1 — THE OSCILLATION, TAKEN FROM THE RECORD RATHER THAN FROM FIVE RUNS.

`lib_f771.SELF_EXCLUDED` justifies the exemption with "measured over five runs, not
anticipated: the oscillation is in README D4, and it does not damp".  Five runs in one
worktree is the evidence that was available when the exemption was written.  The evidence
that is available NOW is the file's own committed history, which is 31 commits of main, and
it says the same thing with three figures the five runs could not produce:

    how many committed versions are RED-shaped,
    how many times the shape FLIPPED,
    and how many commits exist FOR NOTHING ELSE.

The third is the price.  A commit whose entire diff is this one transcript is a `./build.sh`
run and a merge-queue round trip spent turning a file green that was written red by the run
that made the tree green — the oscillation's cost, banked in main, countable.

EVERY FIGURE IS A FUNCTION OF TWO COMMITS.  The walk is pinned at `lib585e.AS_OF` and not at
HEAD, because the history of the file this arm measures grows every time that file is
touched, which is every landing — walked from HEAD, this transcript would go stale on the
next commit and this directory would be shipping its own subject.  The pin is checked: it
must resolve and be an ancestor of origin/main.

WHAT THIS ARM CANNOT SEE, said before the numbers rather than after.  It reads COMMITTED
versions.  A red run whose author re-ran `./build.sh` before committing leaves no trace here,
so every count below is a LOWER BOUND on how often the oscillation happened and an EXACT
count of how often it reached main.

EXITS 0 always on a readable history: this arm reports, it does not grade.  2 if it cannot
reach the history at all.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib585e as L  # noqa: E402

W = 92
RED_MARK = "DISAGREEMENTS, SHOWN"


def rule(ch="-"):
    print(ch * W)


def history(as_of):
    p = L.git(L.ROOT, "log", "--format=%H", "--follow", as_of, "--", L.F771_TRANSCRIPT)
    if p.returncode != 0:
        raise L.Refused("git log failed: %s" % (p.stderr or "").strip())
    return p.stdout.split()


def version(h):
    p = L.git(L.ROOT, "show", "%s:%s" % (h, L.F771_TRANSCRIPT))
    if p.returncode != 0:
        raise L.Refused("cannot read %s:%s" % (h[:8], L.F771_TRANSCRIPT))
    return p.stdout


def touched(h):
    p = L.git(L.ROOT, "show", "--format=", "--name-only", h)
    if p.returncode != 0:
        raise L.Refused("cannot read the file list of %s" % h[:8])
    return [x for x in p.stdout.split("\n") if x.strip()]


def subject(h):
    p = L.git(L.ROOT, "log", "-1", "--format=%s", h)
    return p.stdout.strip()


def main():
    print("=" * W)
    print("mg-585e v1  THE OSCILLATION IN THE RECORD — 'measured over five runs' re-taken over"
          " main")
    print("=" * W)
    print()

    try:
        as_of = L.require_as_of()
        commits = history(as_of)
        rows = []
        for h in commits:
            text = version(h)
            files = touched(h)
            rows.append({
                "h": h,
                "red": RED_MARK in text,
                "bytes": len(text.encode("utf-8")),
                "solo": files == [L.F771_TRANSCRIPT],
                "nfiles": len(files),
                "subject": subject(h),
            })
    except L.Refused as exc:
        print("REFUSED — %s" % exc)
        return 2

    print("§1  THE PIN")
    rule()
    print("  AS_OF                 %s" % as_of)
    print("  resolves, and is an ancestor of origin/main — checked, not assumed.")
    print("  path                  %s" % L.F771_TRANSCRIPT)
    print("  Every figure below is a function of that commit and the walk it defines, so this")
    print("  transcript does not go stale when its subject is next touched.")
    print()

    chrono = list(reversed(rows))
    reds = [r for r in rows if r["red"]]
    solos = [r for r in rows if r["solo"]]
    flips = sum(1 for a, b in zip(chrono, chrono[1:]) if a["red"] != b["red"])

    print("§2  EVERY COMMITTED VERSION, OLDEST FIRST")
    rule()
    print("  shape    is §2 the RED heading (`THE DISAGREEMENTS, SHOWN`)?")
    print("  alone    did this commit touch that file AND NOTHING ELSE?")
    print()
    print("  %-10s %-6s %-7s %-6s %s" % ("commit", "shape", "bytes", "alone", "subject"))
    for r in chrono:
        print("  %-10s %-6s %-7d %-6s %s"
              % (r["h"][:8], "RED" if r["red"] else "green", r["bytes"],
                 "ALONE" if r["solo"] else "%d files" % r["nfiles"],
                 r["subject"][:44]))
    print()

    print("§3  THE THREE FIGURES")
    rule()
    print("  committed versions                        %d" % len(rows))
    print("  RED-shaped                                %d" % len(reds))
    print("  shape flips between consecutive versions  %d" % flips)
    print("  commits touching THAT FILE AND NOTHING ELSE  %d" % len(solos))
    print()
    print("  A flip count near the version count is what 'does not damp' looks like when it is")
    print("  counted instead of described: the shape changes at almost every commit, so almost")
    print("  no commit inherits a transcript that is still true.")
    print()

    greens = [r for r in rows if not r["red"]]
    sizes = sorted({r["bytes"] for r in greens})
    print("§4  ONE SHAPE IS A FIXED POINT AND THE OTHER IS NOT")
    rule()
    print("  distinct byte sizes among the %d green versions   %s"
          % (len(greens), ", ".join(str(s) for s in sizes)))
    print("  distinct byte sizes among the %d RED versions     %s"
          % (len(reds), ", ".join(str(s) for s in sorted({r["bytes"] for r in reds}))))
    print()
    print("  The green versions collapse onto essentially one text; the RED ones do not and")
    print("  cannot, because each names a different set of files.  That asymmetry is the whole")
    print("  mechanism: green is a fixed point of the run, RED is never a fixed point of the")
    print("  commit that carries it, because that commit is the repair.")
    print()

    print("§5  THE PRICE, IN COMMITS THAT EXIST FOR NOTHING ELSE")
    rule()
    if not solos:
        print("  none.")
    for r in solos:
        print("  %-10s %s" % (r["h"][:8], r["subject"][:76]))
    print()
    print("  %d of %d.  Each is a second `./build.sh` run and a second trip through the merge"
          % (len(solos), len(rows)))
    print("  queue, spent on a file that was red because the tree got fixed.")
    print()
    print("  A LOWER BOUND AND NOT A TOTAL.  A red run repaired before the author committed")
    print("  leaves nothing in the record, so the oscillation happened at least this often.")
    print()

    print("VERDICT: REPORTED — %d versions, %d RED, %d flips, %d commits for nothing else."
          % (len(rows), len(reds), flips, len(solos)))
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
