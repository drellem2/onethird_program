"""mg-7085 r1 -- THE REST OF mg-cf83's SWEEP, RUN RATHER THAN READ.

mg-cf83 repaired `s1_rows.py`'s summary block and did not overclaim: its README
and its docstring both scope the three rules to that one file.  mg-407f
CONFIRMED the repair sound in all three arms by a harness sharing no code with
it, and found the SAME DEFECT ALIVE IN TWO SIBLINGS.  This is the rest.

⚠️ THIS SCRIPT SHARES NO CODE WITH THE THING IT REPAIRS.  It does not import
`lib_f3ff`.  It makes REAL clones, breaks REAL remotes AFTER cloning so
`origin/main` still resolves, runs the subject's scripts as SUBPROCESSES, and
greps their REAL stdout for literal strings.  mg-4d3b's whole F-series began
with a `force_fail=True` that RETURNED BEFORE `git fetch` WAS EVER SPAWNED; a
repair verified by a stub reproduces that exact mistake, and so does a sweep.

⚠️ AND IT RUNS THE BEFORE STATE TOO, FROM GIT.  Every "this is repaired" claim
below is a DIFFERENCE between two runs of the same harness -- the subject at
`BEFORE_REV` and the subject in the worktree -- not an absence observed once.
An absence observed once is also what a script that never ran looks like.

THE SPELLING LESSON, WHICH IS THE REUSABLE PART.  mg-cf83's ticket told it to
grep `0 if not gens`.  That spelling finds the site already repaired AND NOTHING
ELSE.  The live defect was spelled `p8_gain.get(1, 0)` -- a DICT DEFAULT that is
the same None-becomes-zero merger wearing different syntax.  So this sweep does
not grep one idiom.  `a2_idiom`-style source census is left to mg-407f; what
this file adds is that EVERY SITE IS CLASSIFIED BY THE PRINTED OUTPUT OF A REAL
FAILING RUN, and the classification LIVE vs LATENT is kept rather than flattened.

THREE ARMS, because a repair verified in one arm is a repair verified in one arm:

  H  both clones healthy            -- THE MUTATION CONTROL.  A script hard-wired
     to print UNMEASURED would pass every failing arm and be useless.  H proves
     the repaired scripts still report real numbers, i.e. that they CAN fail.
  B  both clones broken             -- total fetch failure.
  M  repo 1 healthy, repo 2 broken  -- PARTIAL failure.  This is the arm that
     found s4_crosscheck.py's crash, and no prior ticket ran it on s4 at all.

AND IT RUNS ALL SEVEN SCRIPTS, NOT THREE.  mg-407f recorded that s0_freshness,
s4_crosscheck and selftest_f3ff had never been run in ANY arm and were therefore
UNMEASURED under failure rather than known-good.  They are measured here.
`run_all.sh`'s own aggregate exit, also recorded as unmeasured, is measured too.

EXIT: 0 if THIS INSTRUMENT ran.  ⚠️ FINDINGS ABOUT THE SUBJECT DO NOT SET IT --
the rule `run_all.sh` states for mg-f3ff, for the same reason.  A check of this
harness that FAILS does set it.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
WORKTREE = os.path.abspath(os.path.join(HERE, "..", ".."))
SUBJECT = os.path.join(WORKTREE, "code", "census_repair_f3ff")
SRC2 = "/Users/daniel/research/one_third_width_three"

# The subject as it stood BEFORE this ticket -- mg-407f's landing commit, which
# is this branch's parent.  Materialised from git rather than copied into the
# tree, so the before-state cannot drift from what was actually merged.
BEFORE_REV = "ba67d39"
REL = "code/census_repair_f3ff"

SCRIPTS = ("selftest_f3ff.py", "s0_freshness.py", "s1_rows.py", "s2_controls.py",
           "s3_graph.py", "s4_crosscheck.py")

RED = []          # checks of THIS instrument that failed
FINDINGS = []     # findings about the SUBJECT -- these do NOT set the exit


def check(label, ok, detail=""):
    print(f"    [{'PASS' if ok else 'FAIL'}] {label}")
    if detail:
        print(f"           {detail}")
    if not ok:
        RED.append(label)
    return ok


def finding(label, detail=""):
    print(f"    [FINDING] {label}")
    if detail:
        print(f"           {detail}")
    FINDINGS.append(label)


def sh(args, cwd=None, env=None):
    return subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True)


def make_clone(dst, src):
    r = sh(["git", "clone", "--quiet", "--no-hardlinks", src, dst])
    if r.returncode != 0:
        raise RuntimeError(f"clone failed: {r.stderr.strip()}")
    return dst


def break_remote(path):
    """Break the URL AFTER cloning, so `origin/main` STILL RESOLVES from the ref
    the clone already fetched.  This is mg-4d3b's shape and the incident's own:
    no network at boot, every checkout holding yesterday's refs.  Breaking it
    BEFORE cloning would leave no ref at all, and the UNKNOWN would be an
    artefact of an absent ref rather than of a failed fetch."""
    sh(["git", "-C", path, "remote", "set-url", "origin",
        os.path.join(path, "..", "no_such_remote.git")])


def make_shim(tmp):
    """A `git` on PATH that records every invocation and its exit status.

    Without this, a run that NEVER SPAWNED `git fetch` is indistinguishable from
    one whose fetch failed, and both arms would be the same run reported twice."""
    d = os.path.join(tmp, "shim")
    os.makedirs(d, exist_ok=True)
    real = shutil.which("git")
    p = os.path.join(d, "git")
    with open(p, "w") as fh:
        fh.write("#!/bin/sh\n"
                 'printf "ARGV: %s\\n" "$*" >> "$GITLOG"\n'
                 f'{real} "$@"\n'
                 'rc=$?\n'
                 'printf "  -> exit %s\\n" "$rc" >> "$GITLOG"\n'
                 'exit $rc\n')
    os.chmod(p, 0o755)
    return d


def materialise_before(tmp):
    """The subject at BEFORE_REV, checked out of git into a scratch dir.

    ⚠️ NOT a copy kept in the tree.  A committed `before/` directory is a claim
    about what the code used to be; `git archive` is an observation."""
    dst = os.path.join(tmp, "before_subject")
    os.makedirs(dst)
    r = subprocess.run(["git", "-C", WORKTREE, "archive", f"{BEFORE_REV}:{REL}"],
                       capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"git archive failed: {r.stderr.decode()[:200]}")
    t = subprocess.run(["tar", "-x", "-C", dst], input=r.stdout, capture_output=True)
    if t.returncode != 0:
        raise RuntimeError(f"tar failed: {t.stderr.decode()[:200]}")
    return dst


def stage(host_repo, name, src, repo1, repo2):
    """A copy of `src` with REPOS repointed at the arm's clones.

    ⚠️ THE ONLY EDIT IS THE TWO PATHS.  `lib_f3ff.REPOS` is a hard-coded
    absolute-path constant with no CLI or env override, so there is no other way
    to aim the subject at a clone.  Repointing a path is NOT stubbing the
    failure: every `git fetch` below is real, spawned, and really fails.

    ⚠️ AND IT IS STAGED INSIDE A GIT CHECKOUT ON PURPOSE.  `selftest_f3ff.py`
    resolves `git rev-parse --show-toplevel` FROM ITS OWN CWD.  Staged in a bare
    tmp dir it dies on `not a git repository` -- an artefact of the harness that
    looks exactly like a finding about the subject, and one this harness produced
    on its first run before the staging was moved here."""
    dst = os.path.join(host_repo, "staged_" + name)
    shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(src, dst)
    lib = os.path.join(dst, "lib_f3ff.py")
    with open(lib) as fh:
        t = fh.read()
    old = ('("onethird_program", "/Users/daniel/research/onethird_program"),\n'
           '    ("one_third_width_three", "/Users/daniel/research/one_third_width_three"),')
    new = (f'("onethird_program", "{repo1}"),\n'
           f'    ("one_third_width_three", "{repo2}"),')
    if t.count(old) != 1:
        raise RuntimeError("REPOS block not found exactly once -- the subject "
                           "moved and this sweep is aimed at nothing")
    with open(lib, "w") as fh:
        fh.write(t.replace(old, new))
    return dst


def run(stage_dir, script, tmp, tag):
    """Run one of the subject's scripts as a SUBPROCESS, with the shim on PATH."""
    gitlog = os.path.join(tmp, f"gitlog_{tag}.txt")
    open(gitlog, "w").close()
    env = dict(os.environ)
    env["PATH"] = make_shim(tmp) + os.pathsep + env["PATH"]
    env["GITLOG"] = gitlog
    if script.endswith(".sh"):
        cmd = ["sh", script]
    else:
        cmd = [sys.executable, script]
    r = subprocess.run(cmd, cwd=stage_dir, env=env,
                       capture_output=True, text=True, timeout=3600)
    out = r.stdout + r.stderr
    with open(gitlog) as fh:
        log = fh.read()
    return r.returncode, out, log


def fetches(log):
    """(count, exit codes) for `git fetch origin` -- the anti-vacuity evidence."""
    codes = []
    lines = log.splitlines()
    for i, ln in enumerate(lines):
        if ln.startswith("ARGV:") and "fetch origin" in ln:
            m = re.search(r"exit (\d+)", lines[i + 1]) if i + 1 < len(lines) else None
            codes.append(int(m.group(1)) if m else None)
    return len(codes), codes


def crashed(out):
    return "Traceback" in out


def banner(t):
    print("=" * 78)
    print(t)
    print("=" * 78)


def main():
    banner("mg-7085 r1 -- the rest of the sweep, RUN in three arms, before and after")
    tmp = tempfile.mkdtemp(prefix="mg7085_")
    try:
        print(f"  arena:   {tmp}")
        print(f"  subject: {SUBJECT}")
        print(f"  before:  {BEFORE_REV}:{REL} (materialised via git archive)")
        print()

        before_src = materialise_before(tmp)

        # ⚠️ FROZEN BARE MIRRORS, AND THIS IS METHODOLOGY, NOT PLUMBING.  The
        # healthy arm's `git fetch` really runs and really succeeds -- that is
        # what makes it the mutation control.  If it fetched from the live repos,
        # a commit landing on `main` between the BEFORE run and the AFTER run
        # would change the subject's output and be scored as an effect of the
        # repair.  main moved twice during this ticket's own session.  Every arm
        # therefore fetches from a mirror taken ONCE, here, so `before` and
        # `after` see byte-identical history and the only variable is the code.
        mirror1 = os.path.join(tmp, "mirror1.git")
        mirror2 = os.path.join(tmp, "mirror2.git")
        for m, src in ((mirror1, WORKTREE), (mirror2, SRC2)):
            r = sh(["git", "clone", "--quiet", "--bare", "--no-hardlinks", src, m])
            if r.returncode != 0:
                raise RuntimeError(f"mirror clone failed: {r.stderr.strip()}")
        good1 = make_clone(os.path.join(tmp, "good1"), mirror1)
        good2 = make_clone(os.path.join(tmp, "good2"), mirror2)
        bad1 = make_clone(os.path.join(tmp, "bad1"), mirror1)
        bad2 = make_clone(os.path.join(tmp, "bad2"), mirror2)
        break_remote(bad1)      # cloned FIRST, so origin/main still resolves
        break_remote(bad2)

        print("-" * 78)
        print("ANTI-VACUITY -- the broken arms must be broken FOR THE RIGHT REASON")
        print("-" * 78)
        for lbl, p in (("bad1", bad1), ("bad2", bad2)):
            r = sh(["git", "-C", p, "rev-parse", "--verify", "-q",
                    "origin/main^{commit}"])
            check(f"{lbl}: origin/main RESOLVES LOCALLY despite the broken URL",
                  r.returncode == 0,
                  f"origin/main = {r.stdout.strip()[:12] or '(unresolved)'} -- so an "
                  "UNKNOWN below is a FAILED FETCH, not an absent ref")
            r2 = sh(["git", "-C", p, "fetch", "origin"])
            check(f"{lbl}: a real `git fetch origin` really FAILS", r2.returncode != 0,
                  f"rc={r2.returncode}: "
                  f"{r2.stderr.strip().splitlines()[0][:90] if r2.stderr.strip() else ''}")
        d = sh(["git", "-C", WORKTREE, "diff", "--name-only", BEFORE_REV, "--",
                REL]).stdout.split()
        check("the before-state and the worktree DIFFER (there is a repair to test)",
              bool(d), f"{len(d)} file(s) changed: {', '.join(os.path.basename(x) for x in d)}")
        print()

        # ------------------------------------------------------------------
        # Run every script, in every arm, in both versions.
        # ------------------------------------------------------------------
        arms = {
            "H": ("both clones HEALTHY -- THE MUTATION CONTROL", good1, good2),
            "B": ("both clones BROKEN -- total fetch failure", bad1, bad2),
            "M": ("MIXED: repo 1 healthy, repo 2 BROKEN -- PARTIAL failure",
                  good1, bad2),
        }
        out = {}
        for ver, src in (("before", before_src), ("after", SUBJECT)):
            for arm, (desc, r1, r2) in arms.items():
                # staged INSIDE r1's checkout -- see stage()'s docstring for why
                st = stage(r1, f"{ver}_{arm}", src, r1, r2)
                print("-" * 78)
                print(f"{ver.upper():<7} ARM {arm}  {desc}")
                print("-" * 78)
                for script in SCRIPTS:
                    rc, o, log = run(st, script, tmp, f"{ver}_{arm}_{script}")
                    n, codes = fetches(log)
                    out[(ver, arm, script)] = (rc, o)
                    print(f"    {script:<19} exit={rc:<3} crash={'YES' if crashed(o) else 'no ':<4}"
                          f" git-fetch spawned={n} exits={sorted(set(codes))}")
                    if arm == "H" and script != "selftest_f3ff.py":
                        # ARM H is only a mutation control if its fetch really
                        # ran and really SUCCEEDED.  A healthy arm whose fetch
                        # silently failed is a second broken arm.
                        check(f"{ver}/ARM H/{script}: `git fetch origin` SPAWNED "
                              "and SUCCEEDED", n >= 1 and codes and all(c == 0 for c in codes),
                              f"{n} spawn(s), exit codes {sorted(set(codes))}")
                    if arm in ("B", "M") and script != "selftest_f3ff.py":
                        # Without this, a run that never fetched would look
                        # identical to a run whose fetch failed.
                        check(f"{ver}/ARM {arm}/{script}: `git fetch origin` was "
                              "ACTUALLY SPAWNED", n >= 1,
                              f"{n} spawn(s) observed via the PATH shim")
                        check(f"{ver}/ARM {arm}/{script}: and it ACTUALLY FAILED "
                              "at least once", 128 in codes,
                              f"exit codes {sorted(set(codes))} (128 = git fatal)")
                # run_all.sh, whose aggregate exit was recorded as unmeasured
                rc, o, _log = run(st, "run_all.sh", tmp, f"{ver}_{arm}_runall")
                out[(ver, arm, "run_all.sh")] = (rc, o)
                print(f"    {'run_all.sh':<19} aggregate exit={rc}")
                print()

        # ------------------------------------------------------------------
        banner("CHECK 1 -- F1/F2/F3: s3_graph.py's SCOREBOARD vs ITS OWN ROWS (ARM B)")
        b3 = out[("before", "B", "s3_graph.py")]
        a3 = out[("after", "B", "s3_graph.py")]
        rows_unk = b3[1].count("UNKNOWN -- a repo could not be read.")
        print(f"  BEFORE ({BEFORE_REV}), under a REAL total fetch failure:")
        check("BEFORE: the rows DID say UNKNOWN -- the defect is in the summary, "
              "not the rows", rows_unk >= 1,
              f"{rows_unk} row(s) printed `UNKNOWN -- a repo could not be read.`")
        check("BEFORE: and `OBSERVED: 0` was printed BELOW them  <-- THE DEFECT",
              "OBSERVED: 0" in b3[1],
              "a fixed zero asserting a count from a run that measured nothing")
        check("BEFORE: P8/P9/P10 were SCORED off it", "*** MISS ***" in b3[1])
        check("BEFORE: and it EXITED 0 -- reported success", b3[0] == 0)
        print()
        print("  AFTER, same arm, same clones, same harness:")
        for tag, s in (("F1", "OBSERVED: 0"),
                       ("F2", "P8: *** MISS ***"),
                       ("F3", "P9: *** MISS or PARTIAL ***"),
                       ("F3", "P10: *** MISS ***")):
            check(f"AFTER: {tag} literal {s!r} is ABSENT", s not in a3[1])
        for s in ("OBSERVED: UNMEASURED -- row 1 could not be read",
                  "P8: *** UNMEASURED ***",
                  "row 3 UNMEASURED, row 4 UNMEASURED",
                  "P9: *** UNMEASURED ***",
                  "P10: *** UNMEASURED ***",
                  "THIS RUN DID NOT MEASURE THE GRAPH ON ROW(S) 1, 2, 3, 4"):
            check(f"AFTER: says UNMEASURED where it said 0/no/MISS: {s!r}",
                  s in a3[1])
        check("AFTER: `?` renders the per-row gain, and `0` does not",
              "row 1=?, row 2=?, row 3=?, row 4=?" in a3[1])
        check("AFTER: exit is 1 -- agrees with s1_rows.py", a3[0] == 1,
              f"before {b3[0]}, after {a3[0]}; s1_rows.py exits "
              f"{out[('after', 'B', 's1_rows.py')][0]}")
        check("AFTER: no crash was introduced by the repair", not crashed(a3[1]))
        # P15's guard, borrowed from mg-407f: a crash is not a clean UNMEASURED.
        hdr = "SCORING s3 AGAINST PREDICTIONS.md"
        check("AFTER: the SCORING BLOCK HEADER is present in stdout", hdr in a3[1])
        check("AFTER: stdout CONTINUES past it (>=20 lines) -- not a silent death",
              hdr in a3[1] and len(a3[1].split(hdr)[-1].splitlines()) >= 20,
              f"{len(a3[1].split(hdr)[-1].splitlines()) if hdr in a3[1] else 0} lines after it")
        print()

        banner("CHECK 2 -- THE VERDICT FLIP: does a repo's readability move a score?")
        h3b = out[("before", "H", "s3_graph.py")][1]
        h3a = out[("after", "H", "s3_graph.py")][1]
        for p, hs, bs in (("P9", "P9: HIT", "P9: *** MISS or PARTIAL ***"),
                          ("P10", "P10: HIT", "P10: *** MISS ***")):
            check(f"BEFORE: {p} FLIPPED HIT -> MISS on readability alone",
                  hs in h3b and bs in b3[1],
                  "healthy arm HIT, broken arm MISS, nothing changed but the fetch")
            check(f"AFTER: {p} is HIT on the healthy arm and UNMEASURED on the broken "
                  "one -- THE FLIP IS GONE",
                  hs in h3a and f"{p}: *** UNMEASURED ***" in a3[1])
        print()

        banner("CHECK 3 -- THE MUTATION CONTROL: can the repaired scripts still FAIL?")
        print("  A script hard-wired to print UNMEASURED passes every arm above and")
        print("  is worthless.  ARM H proves these still report real numbers.")
        for script in SCRIPTS:
            hb = out[("before", "H", script)]
            ha = out[("after", "H", script)]
            check(f"ARM H/{script}: healthy exit UNCHANGED by the repair "
                  f"({hb[0]} -> {ha[0]})", hb[0] == ha[0])
            check(f"ARM H/{script}: no crash on the healthy arm", not crashed(ha[1]))
        check("ARM H: s3 still prints REAL per-row gains, not `?`",
              re.search(r"per-row graph-only gain: row 1=\d", h3a) is not None,
              "a genuine 0 and an unread row must render DIFFERENTLY, which is the "
              "whole rule; `?` on ARM B and a digit on ARM H is that difference")
        check("ARM H: s3 exits 0 -- findings about the census still do not set it",
              out[("after", "H", "s3_graph.py")][0] == 0)
        check("ARM H: s2 reports its controls GREEN/RED and says UNMEASURED nowhere",
              "UNMEASURED" not in out[("after", "H", "s2_controls.py")][1],
              "the third state must appear ONLY when something was not measured; a "
              "script that says UNMEASURED on a healthy arm has been hard-wired")
        check("ARM H: s4 reports its bracket and says UNMEASURED nowhere",
              "UNMEASURED" not in out[("after", "H", "s4_crosscheck.py")][1])

        # THE SHARPEST FORM OF THE MUTATION CONTROL: the healthy-arm VERDICTS
        # must be BYTE-IDENTICAL before and after.  A repair that moved a
        # published score would be a different ticket, and `it still exits 0` is
        # far too weak to catch that.
        def verdicts(o):
            return [ln.strip() for ln in o.splitlines()
                    if re.match(r"\s*(P\d+|NC\d):", ln.strip())]
        for script in ("s2_controls.py", "s3_graph.py"):
            vb = verdicts(out[("before", "H", script)][1])
            va = verdicts(out[("after", "H", script)][1])
            # ⚠️ NON-VACUITY GUARD.  `vb == va` is trivially true when the
            # extractor matches nothing, and `0 of 0 identical` reported as PASS
            # is this ticket's own subject.  An earlier form of this check did
            # exactly that for s1_rows.py, whose verdicts are written in a
            # different shape; s1 is now covered by the stronger check below.
            check(f"ARM H/{script}: the verdict extractor is NOT VACUOUS",
                  len(va) > 0, f"{len(va)} verdict line(s) matched")
            check(f"ARM H/{script}: every published verdict line is BYTE-IDENTICAL "
                  "before and after the repair", bool(va) and vb == va,
                  f"{len(vb)} verdict line(s) before, {len(va)} after"
                  + ("" if vb == va else
                     f"; first divergence: {[x for x in zip(vb, va) if x[0] != x[1]][:1]}"))

        # THE STRONGEST FORM, available for the files this ticket did NOT touch:
        # their ENTIRE healthy-arm stdout must be byte-identical.  Whether they
        # were touched is read from `git diff`, not asserted.
        touched = {os.path.basename(x) for x in d}
        for script in SCRIPTS:
            if script in touched:
                continue
            ob = out[("before", "H", script)][1]
            oa = out[("after", "H", script)][1]
            check(f"ARM H/{script}: UNMODIFIED by this ticket (per git diff) and its "
                  "ENTIRE stdout is byte-identical", ob == oa,
                  f"{len(oa.splitlines())} lines"
                  + ("" if ob == oa else "; the diff and the output disagree, which "
                     "means something imported changed underneath it"))
        print(f"    (files this ticket touched, per git diff: "
              f"{', '.join(sorted(touched)) or 'none'})")
        print()

        banner("CHECK 4 -- F4: s2_controls.py's CRASH (ARMS B AND M)")
        for arm in ("B", "M"):
            b2 = out[("before", arm, "s2_controls.py")]
            a2 = out[("after", arm, "s2_controls.py")]
            check(f"BEFORE/ARM {arm}: DIED with mg-4d3b's F5 VERBATIM",
                  "object of type 'NoneType' has no len()" in b2[1],
                  "TypeError at s2_controls.py:80, `sum(len(x) for x in _p.values())`")
            check(f"AFTER/ARM {arm}: no traceback, no NoneType",
                  not crashed(a2[1]) and "NoneType" not in a2[1])
            check(f"AFTER/ARM {arm}: it reaches its OWN exit line",
                  "== s2 exit:" in a2[1])
            check(f"AFTER/ARM {arm}: exit is 1 -- agrees with s1_rows.py", a2[0] == 1)
            check(f"AFTER/ARM {arm}: NC1 is UNMEASURED, not RED",
                  "NC1 UNMEASURED" in a2[1] and "NC1 RED" not in a2[1],
                  "collapsing `moved` to False makes every row compare UNKNOWN to "
                  "UNKNOWN, `deg` empty, and NC1 RED -- a FALSE ACCUSATION against "
                  "this instrument from a run that read no repo")
            check(f"AFTER/ARM {arm}: NC2 does not print `TREE says UPHELD`",
                  "TREE says UPHELD" not in a2[1],
                  "the `or []` at L130 was LATENT behind the crash; repairing the "
                  "crash would have MADE IT LIVE, so it is repaired in the same commit")
            check(f"AFTER/ARM {arm}: NC4 is UNMEASURED, and its `0 of 4 flipped` "
                  "is not printed",
                  "row verdicts flipped at depth" not in a2[1] and "NC4" in a2[1])
        print()

        banner("CHECK 5 -- THE THREE SCRIPTS NO PRIOR ARM EVER RAN")
        print("  mg-407f recorded s0_freshness, s4_crosscheck and selftest_f3ff as")
        print("  never run in ANY arm: UNMEASURED under failure, NOT known-good.")
        print("  They are measured here, in both failing arms.")
        for arm in ("B", "M"):
            for script in ("s0_freshness.py", "selftest_f3ff.py"):
                b = out[("before", arm, script)]
                a = out[("after", arm, script)]
                check(f"ARM {arm}/{script}: CLEAN BEFORE (no crash) -- reported as "
                      "measured-and-sound, not repaired", not crashed(b[1]))
                check(f"ARM {arm}/{script}: unchanged by this ticket "
                      f"(exit {b[0]} -> {a[0]}, no crash)",
                      b[0] == a[0] and not crashed(a[1]))
        # s4: the NEW live defect, and it only shows on the MIXED arm.
        b4B = out[("before", "B", "s4_crosscheck.py")]
        b4M = out[("before", "M", "s4_crosscheck.py")]
        a4M = out[("after", "M", "s4_crosscheck.py")]
        a4B = out[("after", "B", "s4_crosscheck.py")]
        check("BEFORE/ARM B: s4 was CLEAN under TOTAL failure -- which is why no "
              "earlier arm would have found this", not crashed(b4B[1]),
              f"exit {b4B[0]}, guard at s4:47 fires because repo 1 is unreadable")
        if crashed(b4M[1]) and "'NoneType' object is not iterable" in b4M[1]:
            finding("s4_crosscheck.py CRASHED under PARTIAL fetch failure -- a LIVE "
                    "defect no prior ticket measured",
                    "TypeError: 'NoneType' object is not iterable at s4:110 -- its "
                    "guard checked ONE repo, `generations()` ranges over ALL of "
                    "them.  `len(None)` in a new costume, caught by `for gen in "
                    "gens`.  FOUND BY RUNNING THE MIXED ARM.")
        check("BEFORE/ARM M: s4 DID crash -- the finding is reproduced, not asserted",
              crashed(b4M[1]) and "'NoneType' object is not iterable" in b4M[1])
        check("AFTER/ARM M: no crash", not crashed(a4M[1]))
        check("AFTER/ARM M: prints UNMEASURED for both chain modes",
              a4M[1].count("chain: UNMEASURED") == 2)
        check("AFTER/ARM M: does NOT print a miss count from an unread chain",
              "MISSES" not in a4M[1].split("GROUND TRUTH")[-1])
        check("AFTER/ARM M: exit is 1", a4M[0] == 1)
        check("AFTER/ARM B: unchanged -- the first guard still fires",
              a4B[0] == b4B[0] and not crashed(a4B[1]))
        print()

        banner("CHECK 6 -- run_all.sh's AGGREGATE EXIT, also recorded as unmeasured")
        for arm in ("H", "B", "M"):
            rb = out[("before", arm, "run_all.sh")][0]
            ra = out[("after", arm, "run_all.sh")][0]
            print(f"    ARM {arm}: aggregate exit  before={rb}  after={ra}")
        check("ARM H: aggregate exits 0 -- findings about the census do not set it",
              out[("after", "H", "run_all.sh")][0] == 0)
        for arm in ("B", "M"):
            check(f"ARM {arm}: aggregate exits 1", out[("after", arm, "run_all.sh")][0] == 1)
        check("ARM B: it exited 1 BEFORE too -- s3's false 0 was MASKED by its "
              "siblings, and that is why the aggregate did not catch it",
              out[("before", "B", "run_all.sh")][0] == 1,
              "an aggregate that is 1 because SOMETHING failed cannot tell you "
              "WHICH script lied; the per-script exits above can")
        print()

        banner("CHECK 7 -- NO SCRIPT'S SUMMARY CONTRADICTS ITS OWN ROWS (ALL ARMS)")
        print("  The single property this whole lineage exists to hold, grepped out of")
        print("  real stdout in every failing arm after the repair.")
        print()
        print("  ⚠️ A DEFECT OF THIS DETECTOR, KEPT, BECAUSE IT IS THE AUDITED CLASS")
        print("     COMMITTED BY THE AUDITOR.  Its first form matched the bare phrase")
        print("     `row verdicts flipped` and FIRED TWICE against correct code -- on")
        print("     s2's own UNMEASURED branch, whose prose QUOTES the sentence it is")
        print("     refusing to print.  A detector that reads the subject's prose as")
        print("     the subject's output is mg-4d3b's own §6 defect, and finding it in")
        print("     my instrument two hours after quoting that section is the reason it")
        print("     is written down rather than quietly rewritten.  The patterns below")
        print("     now match the ASSERTION -- a figure in its sentence -- and not the")
        print("     vocabulary.  Both failing runs are in this file's git history.")
        print()
        # (pattern, applies-to-script-or-None-for-all, what it would assert)
        FALSE_ZEROS = [
            (r"OBSERVED: 0\b", None, "a scoreboard figure of 0 from an unread graph"),
            (r"all \d+ are now checked against the tree", None,
             "every row checked, when none were"),
            (r"WRONG on 0 of its \d+ rows", None, "two zeros computed from nothing"),
            (r"\d+ of \d+ checked, 0 refuted", None, "a supersession claimed from nothing"),
            (r"\s0 / 0\s", "s1_rows.py", "unmeasured depth rendered as a measured zero"),
            (r"\d+ of \d+ row verdicts flipped at depth", "s2_controls.py",
             "a staleness delta measured against an UNKNOWN live arm"),
            (r"TREE says UPHELD", "s2_controls.py",
             "`the tree could not be read` printed as `the tree found none`"),
            (r"MISSES \d+", "s4_crosscheck.py", "a chain-reader score from an unread chain"),
        ]
        for arm in ("B", "M"):
            for script in SCRIPTS:
                o = out[("after", arm, script)][1]
                if "UNKNOWN" not in o and "UNMEASURED" not in o:
                    continue
                for pat, only, why in FALSE_ZEROS:
                    if only and only != script:
                        continue
                    check(f"ARM {arm}/{script}: does not assert /{pat}/ from an "
                          "unmeasured run", re.search(pat, o) is None, why)
        print()

        banner("VERDICT OF r1")
        print(f"  checks of THIS instrument: {len(RED)} failed")
        for r in RED:
            print(f"    FAILED: {r}")
        print(f"  findings about the SUBJECT: {len(FINDINGS)}")
        for f in FINDINGS:
            print(f"    - {f}")
        print()
        print("  s3_graph.py and s2_controls.py now hold the three rules mg-cf83")
        print("  established for s1_rows.py, and their exits agree with it.")
        print("  s4_crosscheck.py held a THIRD instance that only the MIXED arm")
        print("  reveals, and it is repaired here.")
        print("  s0_freshness.py and selftest_f3ff.py are MEASURED CLEAN in both")
        print("  failing arms -- measured, not assumed, and not repaired.")
        print()
        print(f"== r1 exit: {1 if RED else 0} (findings about the subject do NOT set "
              "this exit; only failures of this instrument do) ==")
        return 1 if RED else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
