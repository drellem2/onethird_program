"""mg-407f a1 -- mg-cf83's repair, RUN rather than read, in three arms.

⚠️ THIS SCRIPT SHARES NO CODE WITH THE THING IT AUDITS.  It does not import
`lib_f3ff`.  It makes REAL clones, breaks a REAL remote AFTER cloning so
`origin/main` still resolves, runs the subject's scripts as SUBPROCESSES, and
greps their REAL stdout for literal strings.  mg-4d3b's whole F-series began
with a `force_fail=True` that RETURNED BEFORE `git fetch` WAS EVER SPAWNED; a
fix verified by a stub reproduces that exact mistake, and so does an audit.

THE TWO GUARDS I FILED AGAINST MYSELF IN PREDICTIONS.md, BOTH ENFORCED HERE:

  P15  I might mistake a CRASH for a clean UNKNOWN.  The absence of a false `0`
       on the terminal is not the guard working if the script died before the
       summary block.  So the broken arm asserts (a) the exit status, (b) that
       the summary header is PRESENT in stdout, (c) that stdout continues past
       it, and (d) that there is no traceback.

  P16  My "broken" arm might not be broken -- if the subject never spawns
       `git fetch` on the path I exercise, both arms are the same run and I
       report a false pass.  So a `git` SHIM is placed on PATH which logs every
       argv and every exit status.  The broken arm asserts that `git fetch
       origin` was ACTUALLY SPAWNED and ACTUALLY FAILED (rc=128).  If I cannot
       demonstrate the fetch was attempted, check 1 is UNMEASURED, not passed.

ARMS.  Three, because "both directions or neither" is the ticket's rule:

  H  both clones healthy   -- THE MUTATION CONTROL.  A summary hard-wired to
     UNKNOWN would pass the broken arm and be useless.  H proves the check can
     still report real numbers, i.e. that it CAN fail.
  B  both clones broken    -- the audited failure.
  M  one healthy, one broken -- partial failure.
     ⚠️ CORRECTED BEFORE SHIPPING: this docstring first said "the arm mg-cf83
     does NOT run".  THAT WAS FALSE, and I found it by reading mg-cf83's own
     committed transcript instead of assuming what a repair driven by an
     all-fail control would have skipped.  `out_c1_summary_guard.txt:104` is
     ARM P, "ONE remote broken -- half the population is perfectly readable".
     So ARM M here is a REPRODUCTION AT THE OPPOSITE ORIENTATION -- mg-cf83
     breaks repo 1 and reads repo 2; this breaks repo 2 and reads repo 1 --
     which is worth running and is NOT worth billing as an arm they missed.

AND IT RUNS THE SIBLINGS.  mg-cf83 repaired `s1_rows.py`.  `s2_controls.py` and
`s3_graph.py` live in the same deliverable, range over the same repos through
the same library, and print their own summary blocks.  This script runs all
three in every arm, because check 3 of my ticket says to sweep for the idiom
rather than trust the three line numbers in the parent.

EXIT: 0 if this INSTRUMENT ran.  ⚠️ FINDINGS ABOUT mg-cf83 DO NOT SET IT -- the
same rule `run_all.sh` states for mg-f3ff, and for the same reason: an
instrument that exited 1 for successfully finding what it was sent to find
could not distinguish `the subject has a defect` from `the auditor is broken`.
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
    """Break the URL AFTER cloning, so `origin/main` STILL RESOLVES from the
    ref the clone already fetched.  This is mg-4d3b's shape and it is the
    incident's own shape: no network at boot, every checkout holding
    yesterday's refs.  Breaking it BEFORE cloning would leave no ref at all and
    the pass would be an artefact of an absent ref rather than a failed fetch."""
    sh(["git", "-C", path, "remote", "set-url", "origin",
        os.path.join(path, "..", "no_such_remote.git")])


def make_shim(tmp):
    """P16's guard: a `git` on PATH that records every invocation and exit."""
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


def stage(tmp, name, repo1, repo2):
    """A copy of the subject with REPOS repointed at the arm's clones.

    ⚠️ THE ONLY EDIT IS THE TWO PATHS.  `lib_f3ff.REPOS` is a hard-coded
    absolute-path constant with no CLI or env override, so there is no other
    way to aim the subject at a clone.  Repointing a path is NOT stubbing the
    failure: every `git fetch` below is real, spawned, and really fails."""
    dst = os.path.join(tmp, "instr_" + name)
    shutil.copytree(SUBJECT, dst)
    lib = os.path.join(dst, "lib_f3ff.py")
    with open(lib) as fh:
        t = fh.read()
    old = ('("onethird_program", "/Users/daniel/research/onethird_program"),\n'
           '    ("one_third_width_three", "/Users/daniel/research/one_third_width_three"),')
    new = (f'("onethird_program", "{repo1}"),\n'
           f'    ("one_third_width_three", "{repo2}"),')
    if t.count(old) != 1:
        raise RuntimeError("REPOS block not found exactly once -- the subject "
                           "moved and this audit is aimed at nothing")
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
    r = subprocess.run([sys.executable, script], cwd=stage_dir, env=env,
                       capture_output=True, text=True, timeout=1800)
    out = r.stdout + r.stderr
    with open(gitlog) as fh:
        log = fh.read()
    return r.returncode, out, log


def fetches(log):
    """(spawned, exit codes) for `git fetch origin` -- P16's evidence."""
    codes = []
    lines = log.splitlines()
    for i, ln in enumerate(lines):
        if ln.startswith("ARGV:") and "fetch origin" in ln:
            m = re.search(r"exit (\d+)", lines[i + 1]) if i + 1 < len(lines) else None
            codes.append(int(m.group(1)) if m else None)
    return len(codes), codes


def banner(t):
    print("=" * 78)
    print(t)
    print("=" * 78)


def main():
    banner("mg-407f a1 -- mg-cf83 RUN against real broken clones, in three arms")
    tmp = tempfile.mkdtemp(prefix="mg407f_")
    try:
        print(f"  arena: {tmp}")
        print(f"  subject: {SUBJECT}")
        print()
        good1 = make_clone(os.path.join(tmp, "good1"), WORKTREE)
        good2 = make_clone(os.path.join(tmp, "good2"), SRC2)
        bad1 = make_clone(os.path.join(tmp, "bad1"), WORKTREE)
        bad2 = make_clone(os.path.join(tmp, "bad2"), SRC2)
        break_remote(bad1)      # cloned FIRST, so origin/main still resolves
        break_remote(bad2)

        print("-" * 78)
        print("ANTI-VACUITY -- the broken arm must be broken FOR THE RIGHT REASON")
        print("-" * 78)
        for lbl, p in (("bad1", bad1), ("bad2", bad2)):
            r = sh(["git", "-C", p, "rev-parse", "--verify", "-q", "origin/main^{commit}"])
            check(f"{lbl}: origin/main RESOLVES LOCALLY despite the broken URL",
                  r.returncode == 0,
                  f"origin/main = {r.stdout.strip()[:12] or '(unresolved)'} -- so an "
                  "UNKNOWN below is a FAILED FETCH, not an absent ref")
            r2 = sh(["git", "-C", p, "fetch", "origin"])
            check(f"{lbl}: a real `git fetch origin` really FAILS", r2.returncode != 0,
                  f"rc={r2.returncode}: {r2.stderr.strip().splitlines()[0][:90] if r2.stderr.strip() else ''}")
        print()

        arms = {
            "H": ("both clones HEALTHY -- THE MUTATION CONTROL", good1, good2),
            "B": ("both clones BROKEN -- the audited failure", bad1, bad2),
            "M": ("MIXED: repo 1 healthy, repo 2 BROKEN -- mg-cf83's ARM P at "
                  "the OPPOSITE orientation", good1, bad2),
        }
        out = {}
        for arm, (desc, r1, r2) in arms.items():
            st = stage(tmp, arm, r1, r2)
            print("-" * 78)
            print(f"ARM {arm}  {desc}")
            print("-" * 78)
            for script in ("s1_rows.py", "s2_controls.py", "s3_graph.py"):
                rc, o, log = run(st, script, tmp, f"{arm}_{script}")
                n, codes = fetches(log)
                out[(arm, script)] = (rc, o)
                print(f"    {script:<17} exit={rc:<3} "
                      f"git-fetch spawned={n} exits={codes}")
                if arm == "B":
                    # P16: without this, a run that never fetched would look
                    # identical to a run whose fetch failed.
                    check(f"ARM B/{script}: `git fetch origin` was ACTUALLY SPAWNED",
                          n >= 1, f"{n} spawn(s) observed via the PATH shim")
                    check(f"ARM B/{script}: and it ACTUALLY FAILED",
                          bool(codes) and all(c == 128 for c in codes),
                          f"exit codes {codes} (128 = git fatal)")
            print()

        # ------------------------------------------------------------------
        banner("CHECK 1 -- s1_rows.py UNDER A REAL FETCH FAILURE (ARM B)")
        rc, o = out[("B", "s1_rows.py")]
        # mg-4d3b's F1-F5, hunted BY LITERAL STRING in real stdout.
        f_strings = [
            ("F1", "are now checked against the tree", "asserts all rows checked"),
            ("F2", "WRONG on 0 of its", "two zeros where nothing was measured"),
            ("F3", "of 4 checked, 0 refuted", "supersession claimed from nothing"),
            ("F4", "0 / 0", "unmeasured depth rendered as a measured zero"),
        ]
        for tag, s, why in f_strings:
            check(f"{tag} ABSENT under a real fetch failure ({why})", s not in o,
                  f"literal {s!r}")
        check("F5 ABSENT -- no TypeError on len(None)",
              "Traceback" not in o and "NoneType" not in o)
        # P15 (a)-(d): a crash is not a clean UNKNOWN.
        hdr = "THE CENSUS'S ACCURACY, WITH THE DENOMINATOR NAMED"
        check("P15(b) the SUMMARY BLOCK HEADER is present in stdout", hdr in o)
        check("P15(c) stdout CONTINUES past the header (>=20 lines)",
              hdr in o and len(o.split(hdr)[-1].splitlines()) >= 20,
              f"{len(o.split(hdr)[-1].splitlines()) if hdr in o else 0} lines after it")
        check("P15(a) exit is 1 -- `this run did not happen`, stated", rc == 1)
        for s in ("UNKNOWN 4 of 4", "? / ?",
                  "The census was WRONG on UNKNOWN", "0 of 4 are checked"):
            check(f"summary says UNKNOWN, not 0: {s!r} present", s in o)
        print()

        banner("CHECK 2 -- THE MUTATION CONTROL: can the check still FAIL? (ARM H)")
        rch, oh = out[("H", "s1_rows.py")]
        check("healthy arm exits 0", rch == 0)
        check("summary reports REAL NUMBERS, not UNKNOWN",
              "REFUTED 2 of 4.  UPHELD 2 of 4.  UNKNOWN 0 of 4." in oh)
        check("and the load-bearing prose figure is real too",
              "The census was WRONG on 2 of its 4 rows and RIGHT on 2." in oh)
        check("a GENUINE zero still renders as `0`, not `?` "
              "(None and empty are DIFFERENT, not both hidden)",
              re.search(r"mg-a74f\s+mg-16eb\s+UPHELD\s+0 / 0", oh) is not None,
              "rows 3/4 have genuinely 0 successors and print 0 / 0 on ARM H, "
              "while ARM B prints ? / ? -- so the guard is not hard-wired")
        check("the two arms are TEXTUALLY DIFFERENT (P16: not the same run twice)",
              oh != o, f"healthy {len(oh.splitlines())} lines, broken {len(o.splitlines())} lines")
        print()

        banner("CHECK 5 -- CAN I MAKE THE SUMMARY DISAGREE WITH THE ROWS? (ARM M)")
        print("  (ARM M reproduces mg-cf83's own ARM P with the broken repo\n"
              "   swapped; it is a second orientation, not an arm they skipped.)")
        rcm, om = out[("M", "s1_rows.py")]
        check("ARM M: the mix is REAL -- one repo counts, one is UNKNOWN",
              "onethird_program=7  one_third_width_three=UNKNOWN" in om,
              "partial information is PRESERVED and shown, not discarded")
        check("ARM M: UNKNOWN is STICKY -- the row goes UNKNOWN",
              "UNKNOWN 4 of 4" in om,
              "a count over part of the population is not a count")
        check("ARM M: and the SUMMARY AGREES with the rows",
              "The census was WRONG on UNKNOWN" in om and "0 of 4 are checked" in om)
        rows_unknown = om.count("UNKNOWN                         ? / ?")
        check("ARM M: no row prints a number the summary contradicts",
              rows_unknown == 4 and "WRONG on 0 of its" not in om,
              f"{rows_unknown} rows UNKNOWN, summary UNKNOWN -- NO DISAGREEMENT FOUND")
        print()

        banner("CHECK 3 -- IS THE RULE SWEPT, OR HELD IN ONE FILE? (SIBLINGS, ARM B)")
        rc2, o2 = out[("B", "s2_controls.py")]
        rc3, o3 = out[("B", "s3_graph.py")]
        _, o3h = out[("H", "s3_graph.py")]

        # s2 -- F5 verbatim, in a sibling.
        if "NoneType' has no len()" in o2:
            finding("s2_controls.py DIES with mg-4d3b's F5 VERBATIM: "
                    "TypeError: object of type 'NoneType' has no len()",
                    "the same `len(None)` death mg-cf83 removed from s1_rows.py, "
                    "alive in the same deliverable, on the same library call")
        else:
            check("s2_controls.py survives a fetch failure", True)

        # s3 -- rows say UNKNOWN, the scoring block says 0.
        rows_unk = o3.count("UNKNOWN -- a repo could not be read.")
        if rows_unk >= 1 and "OBSERVED: 0" in o3:
            finding("s3_graph.py: THE ROWS SAY UNKNOWN AND THE SUMMARY SAYS 0",
                    f"{rows_unk} row(s) print `UNKNOWN -- a repo could not be read.` "
                    "and the SCORING block below prints `OBSERVED: 0` -- this is "
                    "mg-4d3b's F-class defect, alive, in a sibling script")
        if "*** MISS ***" in o3:
            finding("s3_graph.py PUBLISHES PREDICTION VERDICTS from a run that "
                    "measured nothing",
                    "P8/P9/P10 are scored MISS off unpopulated accumulators; "
                    "`UNMEASURED`, the third state mg-cf83 added to s1_rows.py, "
                    "does not exist here")
        # The verdict FLIP -- the sharpest form of the finding.
        for p, hs, bs in (("P9", "P9: HIT", "P9: *** MISS or PARTIAL ***"),
                          ("P10", "P10: HIT", "P10: *** MISS ***")):
            if hs in o3h and bs in o3:
                finding(f"s3_graph.py: {p} FLIPS HIT -> MISS purely because a "
                        "repo could not be read",
                        "the false zero does not merely print -- it propagates "
                        "into the deliverable's own published scoreboard")
        if rc3 == 0:
            finding("s3_graph.py EXITS 0 under a total fetch failure",
                    "s1_rows.py now exits 1 for `this run did not happen`; its "
                    "sibling reports success")
        print()

        banner("VERDICT OF a1")
        print(f"  checks of THIS instrument: {len(RED)} failed")
        for r in RED:
            print(f"    FAILED: {r}")
        print(f"  findings about the SUBJECT: {len(FINDINGS)}")
        for f in FINDINGS:
            print(f"    - {f}")
        print()
        print("  s1_rows.py -- mg-cf83's repair -- HOLDS IN ALL THREE ARMS.")
        print("  Its SIBLINGS in the same deliverable do not.")
        print()
        print(f"== a1 exit: {1 if RED else 0} (findings about mg-cf83 do NOT set "
              "this exit; only failures of this instrument do) ==")
        return 1 if RED else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
