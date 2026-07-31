"""SELFTEST -- THIS INSTRUMENT PUT THROUGH THE RULE IT CAME TO AUDIT.

`Check your own tooling for the defect you are repairing.`  The defect is *a
published figure whose provenance is the commit it came to rest at rather than
the commit it was measured at*.  This audit publishes five transcripts full of
figures, so it is of exactly the kind under examination.

⚠️ AND IT IS JUDGED BY THE PARENT'S LATTICE, NOT BY ONE OF MY OWN.  Writing a
second lattice to grade myself would let me pick a rule I pass.  The rule used
here is `anchor_132a.verdict_from_text()` -- the code under audit, applied to
the auditor.
"""
import pathlib
import sys

sys.path.insert(0, "../publication_anchor_132a")
import anchor_132a as P  # noqa: E402

import lib_c067 as L  # noqa: E402

MINE = "code/audit_c067"
OUTS = ["out_c1_rebase.txt", "out_c2_anchors.txt", "out_c3_shopping.txt",
        "out_c4_independence.txt", "out_c5_vocab.txt", "out_selftest_c067.txt"]


def main(argv):
    as_of = L.as_of_from_argv(argv)
    L.banner(as_of)

    here = pathlib.Path(L.REPO) / MINE

    # ----------------------------------------------------------------- T1
    L.head("T1 -- EVERY TRANSCRIPT THIS AUDIT WRITES DECLARES ITS ANCHOR")
    print("""
The parent's central claim is that a figure without a resolvable measurement
commit is an unfalsifiable assertion in a file.  If that is right, every
transcript in this directory owes one.  Read from DISK here rather than from
git, deliberately: at the moment this runs, these are the bytes about to be
committed, and a check that could only see the previous commit could not see
the thing it is about to ship.
""")
    SELF = "out_selftest_c067.txt"
    print(f"    {'transcript':<28} {'anchor':<9} {'decl':>5} {'mine':>5} "
          f"{'digest ok':<10} banner")
    bad, checked = [], []
    for name in OUTS:
        if name == SELF:
            continue
        f = here / name
        if not f.exists():
            print(f"    {name:<28} (not yet written)")
            bad.append((name, "not written"))
            continue
        text = f.read_text(errors="replace")
        d = L.declared_anchor(text)
        if not d:
            bad.append((name, "no declared anchor"))
            print(f"    {name:<28} MISSING")
            continue
        full = L.resolve(d["commit"])
        mine = L.population_count(full) if full else None
        dig_ok = full is not None and L.population_key(full) == d["digest"]
        banner = "MEASUREMENT AT THE COMMIT ABOVE" in text
        checked.append(name)
        if not (full and mine == d["count"] and dig_ok and banner):
            bad.append((name, f"resolve={bool(full)} count={mine}/"
                              f"{d['count']} digest={dig_ok} banner={banner}"))
        print(f"    {name:<28} {(full or '?')[:7]:<9} {d['count']:>5} "
              f"{str(mine):>5} {'YES' if dig_ok else 'NO':<10} "
              f"{'YES' if banner else 'NO'}")
    L.record(not bad,
             f"T1 all {len(checked)} of this audit's OTHER transcript(s) "
             f"({', '.join(checked)}) carry a `POPULATION ANCHOR:` line whose "
             f"commit RESOLVES, whose `count=` RE-DERIVES from `git ls-tree` "
             f"at that commit, whose `digest=` matches an independent "
             f"recomputation, and whose banner says the file is a measurement "
             f"rather than a live property.  Failures: {bad if bad else 'none'}")

    # ------------------------------------------------------------------ T1'
    self_disk = (here / SELF)
    disk_len = self_disk.stat().st_size if self_disk.exists() else 0
    self_pub = L.publishing_commit(f"{MINE}/{SELF}", as_of)
    from_git = L.blob_at(self_pub, f"{MINE}/{SELF}") if self_pub else None
    d_git = L.declared_anchor(from_git) if from_git else None
    print(f"\n    {SELF:<28} on disk: {disk_len} byte(s) -- TRUNCATED BY THE "
          f"REDIRECT THAT IS WRITING IT")
    print(f"    {'':<28} in git : "
          + (f"{self_pub[:7]}, anchor {d_git['commit'][:7]}, count "
             f"{d_git['count']}" if d_git else "not committed at this rev"))
    L.record(None if not d_git else
             (L.resolve(d_git["commit"]) is not None
              and L.population_count(L.resolve(d_git["commit"]))
              == d_git["count"]),
             f"T1' ⚠️ AND THE ONE TRANSCRIPT THIS ROW CANNOT READ FROM DISK IS "
             f"ITS OWN -- {disk_len} bytes, because the shell redirect in "
             f"`run_all.sh` truncated it before this process started.  "
             f"THE FIRST VERSION OF T1 READ ALL SIX FROM DISK AND REFUTED ON "
             f"EXACTLY THAT, which is kept as `P9` predicted it would be.  "
             f"The fix is the parent's: read the self-transcript FROM GIT at "
             f"its publishing commit -- "
             + (f"{self_pub[:7]}, whose declared anchor "
                f"{d_git['commit'][:7]} re-derives to "
                f"{L.population_count(L.resolve(d_git['commit']))}."
                if d_git else
                "which does not exist yet at this rev, so this row is a "
                "MEASUREMENT and not a pass, and resolves on the next run "
                "after these files are committed.")
             + f"  `anchor_132a.py`'s `verdict_for()` documents this exact "
             f"hazard ('this instrument's own transcript is truncated on disk "
             f"by the redirect that is about to write it') and I walked into "
             f"it anyway")

    # ----------------------------------------------------------------- T2
    L.head("T2 -- AND THIS AUDIT'S OWN FIGURES, THROUGH THE PARENT'S LATTICE")
    print("""
The rule under audit, turned on the auditor.  Before the first commit of these
files there is no publishing commit to read, so the honest answer is
`UNPUBLISHED` and the row says so rather than scoring absence as a pass.
""")
    verdicts = {}
    for name in OUTS:
        rel = f"{MINE}/{name}"
        pub = L.publishing_commit(rel, as_of)
        if pub is None:
            print(f"    {name:<28} UNPUBLISHED  (not committed at "
                  f"{as_of[:7]} -- this becomes a measurement at the commit "
                  f"that lands it)")
            verdicts[name] = "UNPUBLISHED"
            continue
        v = P.verdict_from_text(L.blob_at(pub, rel), pub, as_of)
        verdicts[name] = v["verdict"]
        print(f"    {name:<28} {v['verdict']:<20} anchor "
              f"{(v['anchor'] or '?')[:7]} ({v['anchor_kind']}), published at "
              f"{pub[:7]} which holds {v['published_count']}")
    red = [n for n, v in verdicts.items() if v in P.RED]
    L.record(not red,
             f"T2 {len(red)} of this audit's transcript(s) are RED under the "
             f"parent's own lattice: {red if red else 'none'}.  "
             f"{sum(1 for v in verdicts.values() if v == 'UNPUBLISHED')} are "
             f"UNPUBLISHED at {as_of[:7]}, which is not a pass and is named "
             f"here rather than counted as one")

    # ----------------------------------------------------------------- T3
    L.head("T3 -- THE DEFECT THIS AUDIT WILL COMMIT, PREDICTED BEFORE IT DOES")
    print("""
⚠️ NOT A CLAIM TO HAVE CLOSED THE GAP.  The refinery rebases this branch onto a
`main` that has grown, exactly as it did to mg-132a four commits after mg-132a
argued that it would.  So the population figures in these transcripts will be
RIGHT WHEN WRITTEN and DISPLACED the moment they merge, and nothing in this
directory can run after that.
""")
    n_now = L.population_count(as_of)
    print(f"    `code/` .py population at {as_of[:7]}          : {n_now}")
    print(f"    every figure above is measured against that tree")
    print(f"    after the merge the publishing commit will hold : "
          f"MORE, and these figures will read DISPLACED")
    print(f"""
    THE ONE COMMAND THAT RE-CHECKS IT:

        sh code/audit_c067/run_all.sh --at <post-merge-rev>
        sh code/publication_anchor_132a/run_all.sh --at <post-merge-rev>
""")
    L.record(None,
             f"T3 THIS AUDIT INHERITS THE GAP IT REPORTS, AND SAYS SO BEFORE "
             f"THE FACT RATHER THAN AFTER.  Its {n_now}-file population is a "
             f"measurement at {as_of[:7]}; the merge will move it, no hook "
             f"re-runs, and `C1d` is the row where this audit records that the "
             f"PARENT's identical exposure went unaddressed for the whole "
             f"window between its merge and this audit.  ⚠️ THE DIFFERENCE "
             f"BETWEEN NAMING A GAP AND CLOSING IT IS EXACTLY THE DIFFERENCE "
             f"THE PARENT DREW AT `A3c`, and this instrument is on the same "
             f"side of it")

    # ----------------------------------------------------------------- T4
    L.head("T4 -- PREDICTIONS BEFORE INSTRUMENT, READ OUT OF GIT")
    pred = L.git("log", "--diff-filter=A", "--format=%H", as_of, "--",
                 f"{MINE}/PREDICTIONS.md", ok=True)
    first_script = L.git("log", "--diff-filter=A", "--format=%H", as_of, "--",
                         f"{MINE}/c1_rebase.py", ok=True)
    p_sha = (pred or "").split()
    s_sha = (first_script or "").split()
    if p_sha and s_sha:
        ordered = L.reachable(p_sha[-1], s_sha[-1]) and p_sha[-1] != s_sha[-1]
        print(f"    PREDICTIONS.md first appears at : {p_sha[-1][:7]}")
        print(f"    c1_rebase.py    first appears at : {s_sha[-1][:7]}")
        print(f"    the first is an ancestor of the second : "
              f"{'YES' if ordered else 'NO'}")
        L.record(ordered,
                 f"T4 PREDICTIONS BEFORE INSTRUMENT, FROM `git log`: "
                 f"`PREDICTIONS.md` first appears at {p_sha[-1][:7]} and "
                 f"`c1_rebase.py` at {s_sha[-1][:7]}, and the first is an "
                 f"ancestor of the second.  'Decided before measuring' is a "
                 f"claim about the repository and is read out of git here")
    else:
        L.record(None,
                 f"T4 PREDICTIONS/INSTRUMENT ORDERING IS NOT YET READABLE FROM "
                 f"GIT at {as_of[:7]} -- PREDICTIONS.md committed: "
                 f"{bool(p_sha)}, c1_rebase.py committed: {bool(s_sha)}.  ⚠️ "
                 f"RED-BY-ABSENCE IS CORRECT HERE: before both are committed "
                 f"there is no ordering to read, and a row that went green on "
                 f"missing evidence would be the defect this audit is about.  "
                 f"It resolves on the run that regenerates these transcripts")

    return L.summary(as_of)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
