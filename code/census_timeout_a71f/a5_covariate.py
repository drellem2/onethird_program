"""a5 -- WAS THE TIMED-OUT COUNT A FACT ABOUT THE ARC, OR ABOUT THE BOX?

pm-onethird's ask, and it is the right one: machine load fell during the re-run,
so GROUP ORDER is confounded with timeout probability INSIDE a single run.  A
`TIMED-OUT` count taken across the whole run would then mix two machine
regimes, and any pattern in it could be an artefact of when a group happened to
be scheduled rather than anything about the code it tests.

So the covariate was recorded, and this arm reads it back and answers the
question the covariate exists for: **do the TIMED-OUT rows cluster in the
high-load part of the run?**

WHY THE COVARIATE IS A SIDECAR AND NOT A COLUMN IN `out_t2_census.txt`.  A wall
clock or a load average printed into that transcript would make it
non-reproducible BY CONSTRUCTION -- and the census has already written the
argument against exactly that, about itself, at `t2_census.py:63`, explaining
why `--jobs` is deliberately not printed:

    "The job count is a fact about the machine, not about the subject, so
     printing it would make this transcript fail to reproduce on a
     differently-sized box for a reason that has nothing to do with the arc --
     the exact defect being measured, committed by the instrument measuring
     it."

A timestamp is that argument with the volume up.  So the covariate lives BESIDE
the census, in `covariate_load_by_group.tsv`, sampled every 15 s by a process
outside it that read each worker's cwd and its worktree's HEAD.  Attribution is
therefore per GROUP -- the `(directory, carrying commit)` pair the census
actually keys on -- and not merely per directory, which matters because the same
directory appears in this run under more than one commit.

⚠️  THE COVARIATE HAS A HOLE AND IT IS IN THE WORST PLACE.  Sampling began
after the run had already started, so the earliest groups have NO rows -- and
those ran under the highest load.  A5a prints the size of that hole first,
before any conclusion is drawn over the part that was sampled, because a
covariate with an unstated gap is worse than none.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_a71f as L                                            # noqa: E402

TSV = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "covariate_load_by_group.tsv")
NEW_T2 = os.path.join(L.REPO, L.CENSUS_DIR, "out_t2_census.txt")


def read_tsv(path):
    rows = []
    with open(path, encoding="utf-8", errors="replace") as fh:
        head = fh.readline().rstrip("\n").split("\t")
        for line in fh:
            f = line.rstrip("\n").split("\t")
            if len(f) != len(head):
                continue
            rows.append(dict(zip(head, f)))
    return rows


def main():
    led = L.Ledger("a5 -- THE TIMED-OUT COUNT AGAINST THE LOAD THAT PRODUCED IT")

    if not os.path.exists(TSV):
        led.self_error("no covariate file at %s" % TSV)
        return led.done()
    if not os.path.exists(NEW_T2):
        led.self_error("the repaired census has not been run: %s absent"
                       % NEW_T2)
        return led.done()
    rows = read_tsv(TSV)
    with open(NEW_T2, encoding="utf-8", errors="replace") as fh:
        new_t = fh.read()
    verdicts = L.parse_t2_rows(new_t)

    # group key: (directory, 7-char carrying commit) -- the census's own key
    seen = {}
    for r in rows:
        try:
            load = float(r["load1"])
        except ValueError:
            continue
        # BOTH SIDES NORMALISED TO 7 CHARS.  T2a prints `c[:7]`;
        # `git rev-parse --short` returns 7 UNLESS the prefix is
        # ambiguous, in which case it returns more -- and the join
        # would then miss exactly the groups whose commit prefix
        # collides with another, silently, as an unsampled row.
        k = (r["directory"], r["commit"][:7])
        s = seen.setdefault(k, {"first": r["utc"], "last": r["utc"],
                                "loads": [], "done": r["groups_done"]})
        s["last"] = r["utc"]
        s["loads"].append(load)

    census_groups = {}
    for p, (carry, v) in verdicts.items():
        census_groups.setdefault((p.split("/")[0], carry[:7]),
                                 set()).add(v)

    # ------------------------------------------------------------------ A5a
    led.head("A5a -- THE HOLE IN THE COVARIATE, STATED BEFORE ANYTHING IS "
             "CONCLUDED FROM IT")
    sampled = set(seen)
    allg = set(census_groups)
    missing = sorted(allg - sampled)
    extra = sorted(sampled - allg)
    print("    groups in the census                 %4d" % len(allg))
    print("    groups the sampler observed          %4d" % len(sampled))
    print("    groups with NO covariate row         %4d   <- ran before "
          "sampling began, or finished inside one 15 s gap" % len(missing))
    if extra:
        print("    observed but not in the census       %4d   (SELF/SKIPPED, "
              "or a second worker on the same key)" % len(extra))
    if rows:
        print()
        print("    sampling window   %s .. %s" % (rows[0]["utc"],
                                                  rows[-1]["utc"]))
        loads = [float(r["load1"]) for r in rows
                 if r["load1"].replace(".", "", 1).isdigit()]
        if loads:
            print("    1-min load        min %.2f  max %.2f  mean %.2f"
                  % (min(loads), max(loads), sum(loads) / len(loads)))
    led.record(not missing,
               "A5a %d of %d groups have NO covariate row.  Every conclusion "
               "below ranges over the %d that do, and the unsampled groups are "
               "NOT assumed to resemble them -- they ran EARLIER, which is when "
               "the box was busiest" % (len(missing), len(allg), len(sampled)))

    # ------------------------------------------------------------------ A5b
    led.head("A5b -- DO THE TIMED-OUT GROUPS SIT IN THE HIGH-LOAD PART "
             "OF THE RUN?")
    timed, other = [], []
    for k, s in seen.items():
        vs = census_groups.get(k)
        if not vs:
            continue
        mean = sum(s["loads"]) / len(s["loads"])
        (timed if "TIMED-OUT" in vs else other).append((mean, k, s))
    print("    %-42s %6s %6s %8s" % ("bucket over SAMPLED groups", "n",
                                     "mean", "max"))
    for label, grp in (("groups with a TIMED-OUT row", timed),
                       ("groups with none", other)):
        if grp:
            ms = [m for m, _, _ in grp]
            print("    %-42s %6d %6.2f %8.2f"
                  % (label, len(ms), sum(ms) / len(ms), max(ms)))
        else:
            print("    %-42s %6d %6s %8s" % (label, 0, "-", "-"))
    if timed:
        print()
        print("    every sampled TIMED-OUT group, with the load it ran under:")
        print("      %-40s %-9s %6s  %s" % ("directory", "commit", "load",
                                            "window (utc)"))
        for mean, k, s in sorted(timed):
            print("      %-40s %-9s %6.2f  %s .. %s"
                  % (k[0][:40], k[1], mean, s["first"][11:19],
                     s["last"][11:19]))
    if timed and other:
        mt = sum(m for m, _, _ in timed) / len(timed)
        mo = sum(m for m, _, _ in other) / len(other)
        led.record(abs(mt - mo) < 1.0,
                   "A5b sampled groups that timed out ran under a mean 1-minute "
                   "load of %.2f; groups that did not ran under %.2f.  A gap "
                   "here means the TIMED-OUT count is partly a fact about WHEN "
                   "a group was scheduled and the honest figure is a bracket, "
                   "not a count" % (mt, mo))
    else:
        led.record(None,
                   "A5b one side of the comparison is empty (%d timed out, %d "
                   "did not, among sampled groups), so no load contrast can be "
                   "computed.  That is an outcome, not a failure: if nothing "
                   "timed out, the confound had nothing to act on"
                   % (len(timed), len(other)))

    # ------------------------------------------------------------------ A5c
    led.head("A5c -- WHAT THIS ARM CANNOT DO")
    print("""
It cannot turn an observational covariate into a controlled one.  Nobody set
the load; it fell on its own while the run proceeded in a fixed order, so LOAD
and POSITION IN THE RUN are themselves confounded with each other.  A group
that timed out late under low load is evidence against the confound; a group
that timed out early under high load is consistent with BOTH `this suite is
slow` and `the box was busy`, and this arm cannot separate them.

The clean experiment is the one the census's own T2d already names: re-run with
`--timeout N` on a quiet box and see which rows come back.  That is a different
measurement and it is not made here.
""")
    return led.done()


if __name__ == "__main__":
    sys.exit(main())
