"""mg-4d3b a4 -- EVERY PRINTED COUNT: CONSTRUCT AN INPUT THAT MOVES IT.

The standing rule is that a count which cannot move is FORCED and must say so.
Two counts are tested here, and they behave differently.

  PART 1  THE ROW COUNTS.  A synthetic commit is written into a throwaway
          clone -- naming the parent, owned by another ticket, back-dated
          before the filing instant -- and the row is re-derived.  A count
          that moves is a count.  Rows 3 and 4 are the ones that matter: they
          print 0, and a 0 that cannot be made non-zero is not a measurement.

  PART 2  NC4's `0 of 4 verdicts flip`.  mg-f3ff pins origin/main~10, ~25 and
          ~60 and reports 0 flips at each.  Its README then writes that up as
          **`0 of 4 verdicts flip at ANY pinned depth`** -- three samples
          quantified into all depths.  This sweeps EVERY depth from 0 to the
          full height of each repo and reports the first depth at which each
          row flips, if one exists.  Pre-registered as P11 of PREDICTIONS.md
          at 60% confidence.

          ⚠️ THE ASYMMETRY MATTERS AND IS REPORTED RATHER THAN AVERAGED:
          pinning can only REMOVE commits from a window that was already
          closed on 2026-07-31, so it can turn REFUTED into UPHELD and can
          NEVER turn UPHELD into REFUTED.  For rows 3 and 4 the NC4 answer is
          therefore FORCED, and naming the forcing is the point of this
          section.  For rows 1 and 2 it is not forced, and a flip depth
          exists or it does not -- that is the measurement.

No command here touches either source repo: everything runs on clones under
the scratchpad.

EXIT: 1 if a control of THIS instrument fails.
"""
import os
import subprocess
import sys
import tempfile

import lib4d3b as L


def sh(args, cwd=None, env=None):
    e = dict(os.environ)
    e.setdefault("GIT_AUTHOR_NAME", "mg-4d3b")
    e.setdefault("GIT_AUTHOR_EMAIL", "mg-4d3b@local")
    e.setdefault("GIT_COMMITTER_NAME", "mg-4d3b")
    e.setdefault("GIT_COMMITTER_EMAIL", "mg-4d3b@local")
    if env:
        e.update(env)
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, env=e)


def clone(dst, src):
    r = sh(["git", "clone", "--quiet", "--no-hardlinks", src, dst])
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip())
    return dst


def inject(path, subject, when):
    """One commit on `main`, back-dated, then origin/main is moved to it so the
    derivation (which reads origin/main, never HEAD) sees it."""
    sh(["git", "-C", path, "checkout", "--quiet", "-B", "main", "origin/main"])
    with open(os.path.join(path, "mg4d3b_probe.txt"), "a") as fh:
        fh.write(subject + "\n")
    sh(["git", "-C", path, "add", "mg4d3b_probe.txt"])
    r = sh(["git", "-C", path, "commit", "--quiet", "-m", subject],
           env={"GIT_AUTHOR_DATE": when, "GIT_COMMITTER_DATE": when})
    if r.returncode != 0:
        raise RuntimeError(f"probe commit failed: {r.stderr.strip()}")
    sha = sh(["git", "-C", path, "rev-parse", "HEAD"]).stdout.strip()
    sh(["git", "-C", path, "update-ref", "refs/remotes/origin/main", sha])
    return sha


class Pinned(L.Repo):
    """A repo resolved to origin/main~k WITHOUT fetching -- the stale-checkout
    hazard, constructed.  It is a subclass rather than a flag because the
    UNKNOWN rule must keep applying: `.unknown` is still driven by `.sha`."""

    def __init__(self, label, path, depth):
        self.label, self.path, self.remote = label, path, "origin"
        self.fetch_rc, self.fetch_err = 0, ""
        self.head = self.behind = None
        self.reason = f"pinned to origin/main~{depth}"
        self._cache = None
        self.depth = depth
        r = sh(["git", "-C", path, "rev-parse", "--verify", "-q",
                f"origin/main~{depth}^{{commit}}"])
        self.sha = r.stdout.strip() if r.returncode == 0 and r.stdout.strip() else None

    @property
    def ref(self):
        return self.sha or "(unresolved)"


def height(path):
    r = sh(["git", "-C", path, "rev-list", "--count", "origin/main"])
    return int(r.stdout.strip()) if r.returncode == 0 else 0


def main():
    L.banner("mg-4d3b a4 -- every printed count, and whether it can be moved")
    tmp = L.scratch_dir("move-")
    print(f"  throwaway clones under {tmp}")
    print("  NO command in this section runs inside /Users/daniel/research/*.\n")

    c1 = clone(os.path.join(tmp, "r1"), L.WORKTREE)
    c2 = clone(os.path.join(tmp, "r2"), L.SRC2)
    base = [L.Repo("onethird_program", c1, fetch=False) for _ in (0,)]
    # fetch=False would be UNKNOWN by design (see lib4d3b); use the pinned
    # subclass at depth 0, which resolves origin/main exactly.
    repos = [Pinned("onethird_program", c1, 0), Pinned("one_third_width_three", c2, 0)]
    del base
    for r in repos:
        print(r.line())
    print()

    red = 0
    print("=" * 78)
    print("PART 1 -- MOVING EACH ROW COUNT WITH A CONSTRUCTED COMMIT")
    print("=" * 78)
    for n, row, filed, parent, _prem in L.ROWS:
        T = L.utc(filed)
        before = L.row_verdict(repos, parent, T)
        nb = sum(len(v) for v in before[1].values())

        probe = clone(os.path.join(tmp, f"probe{n}"), L.WORKTREE)
        subj = (f"probe: a constructed successor naming {parent} "
                f"(mg-4d3b)")
        when = "2026-07-01T00:00:00+0000"          # well before every instant
        sha = inject(probe, subj, when)
        moved = [Pinned("onethird_program", probe, 0),
                 Pinned("one_third_width_three", c2, 0)]
        after = L.row_verdict(moved, parent, T)
        na = sum(len(v) for v in after[1].values())

        # and the negative twin: the SAME commit dated AFTER the instant must
        # NOT move the count.  Without this the mover proves only that adding
        # text changes a grep, not that the date bound is live.
        probe2 = clone(os.path.join(tmp, f"late{n}"), L.WORKTREE)
        inject(probe2, subj, "2026-08-01T00:00:00+0000")
        late = [Pinned("onethird_program", probe2, 0),
                Pinned("one_third_width_three", c2, 0)]
        nl = sum(len(v) for v in L.row_verdict(late, parent, T)[1].values())

        print(f"  row {n} ({parent}): {before[0]} {nb}"
              f"  --probe@2026-07-01-->  {after[0]} {na}"
              f"   [{sha[:9]}]")
        red += L.check(f"row {n}'s count MOVES (not forced)", na == nb + 1,
                       f"{nb} -> {na}")
        red += L.check(f"row {n}: the same commit dated AFTER the instant does NOT move it",
                       nl == nb, f"{nb} -> {nl}; the date bound is live, not decorative")
        if nb == 0 and na > 0:
            print(f"      >>> the 0 flipped {before[0]} -> {after[0]}.  Rows that print 0")
            print(f"          are measurements, not defaults.")
    print()

    print("=" * 78)
    print("PART 2 -- NC4's `0 of 4 verdicts flip`, SWEPT OVER EVERY DEPTH")
    print("=" * 78)
    h1, h2 = height(c1), height(c2)
    print(f"  heights: onethird_program={h1}, one_third_width_three={h2}")
    print(f"  mg-f3ff sampled depths 10, 25, 60.  This sweeps EVERY depth 0..{min(h1, h2) - 1}.")
    print()
    # `git log origin/main` is newest-first, and a0 measured 0 merge commits in
    # either repo, so history is linear and origin/main~k is exactly the list
    # with its first k entries dropped.  ASSERTED, not assumed:
    lists = {r.label: r.commits() for r in repos}
    paths = {"onethird_program": c1, "one_third_width_three": c2}
    for lab, lst in lists.items():
        for k in (0, 1, 7, 40):
            if k >= len(lst):
                continue
            want = sh(["git", "-C", paths[lab], "rev-parse",
                       f"origin/main~{k}"]).stdout.strip()
            red += L.check(f"slicing control: {lab} list[{k}] == origin/main~{k}",
                           lst[k].sha == want,
                           "the sweep below slices a cached list instead of "
                           "re-running git 3000 times; this is what licenses it")
    print()

    def verdict_at(parent, T, k):
        tot = 0
        for lab, lst in lists.items():
            for c in lst[k:]:
                if not c.names(parent) or c.owner == parent.lower():
                    continue
                if c.adate is None or c.adate > T:
                    continue
                tot += 1
        return ("REFUTED" if tot else "UPHELD"), tot

    flip, counts0 = {}, {}
    for n, row, filed, parent, _prem in L.ROWS:
        T = L.utc(filed)
        v0, counts0[n] = verdict_at(parent, T, 0)
        flip[n] = None
        for k in range(0, min(h1, h2)):
            v, _t = verdict_at(parent, T, k)
            if v != v0:
                flip[n] = (k, v)
                break
        f = flip[n]
        print(f"  row {n} ({parent}): at depth 0 = {v0} ({counts0[n]})"
              + (f"   FIRST FLIP at depth {f[0]} -> {f[1]}" if f
                 else f"   NEVER FLIPS at any depth 0..{min(h1, h2) - 1}"))
    print()
    forced = [n for n in flip if counts0[n] == 0]
    print("  FORCING, NAMED:")
    print("    Pinning origin/main~k can only REMOVE commits from a window closed")
    print("    on 2026-07-31.  So REFUTED->UPHELD is reachable and UPHELD->REFUTED")
    print(f"    is NOT.  Rows {forced} print 0 and their NC4 answer is FORCED: no")
    print("    depth can flip them, by construction and not by evidence.  mg-f3ff's")
    print("    NC4 does not say so.")
    print()
    flipped = {n: f for n, f in flip.items() if f}
    print("  P11 SCORING (pre-registered at 60%):")
    print("    predicted: at least one printed figure is forced and unlabelled;")
    print("               named candidate = NC4's `0 of 4 verdicts flip`.")
    if forced:
        print(f"    observed : HIT on the forcing -- rows {forced} cannot flip at any k.")
    else:
        print("    observed : MISS -- every row can flip at some depth.")
    if flipped:
        print(f"    AND the `any pinned depth` quantifier is FALSE as written: rows")
        print(f"    {sorted(flipped)} DO flip, at depth(s) "
              + ", ".join(f"{n}@{v[0]}" for n, v in sorted(flipped.items())) + ".")
        print("    mg-f3ff's own s2 transcript is careful -- it says `at depth 10`,")
        print("    `at depth 25`, `at depth 60`.  It is the README that writes three")
        print("    samples up as `at any pinned depth`.  The defect is in the")
        print("    SUMMARY, not in the instrument, which is the same place a3 found")
        print("    F1-F4.")
    else:
        print("    The quantifier survives the sweep: no row flips at any depth")
        print("    reachable in either repo, so `at any pinned depth` is true here")
        print("    for a reason mg-f3ff does not give -- the forcing above.")
    print(f"\n== a4 exit: {1 if red else 0} ==")
    return 1 if red else 0


if __name__ == "__main__":
    sys.exit(main())
