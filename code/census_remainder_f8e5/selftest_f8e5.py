"""selftest_f8e5 -- every arm FORCED, and every one able to print the other answer.

The rule this file is written under, taken from this arc: a control that has
only ever been green has not been shown able to fire.  So each arm below either
(a) asserts a fact that a mutation of this suite's own code would break, or
(b) is a NEGATIVE arm that must come out FALSE and would be a self-error if it
came out true.

TWO ARMS EXIST ONLY BECAUSE THEY ALREADY CAUGHT SOMETHING:

  S3'' the moving-ref detector must find the shape in mg-1abe's suite at the
       commit before its fix.  My first detector did NOT -- it read only the
       driven scripts, and mg-1abe's eight scripts do not name `main`; they
       call `lib_1abe.main_rev()`, whose default is `main`.  The detector
       scored the one directory in this repository where the answer is known in
       advance as ONE-SCRIPT, and this arm is why that shipped fixed.

  S4   a producer re-run in a DIRTY worktree must be refused.  My own first
       re-run of `hodge_leverage_repair_ff3e` was killed mid-mutation by a
       two-minute timeout; the next run refused, and the refusal read exactly
       like a census verdict for about a minute.
"""

import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_f8e5 as L
import lib_1abe as C


def main():
    rev = L.resolve(L.main_rev())
    led = L.Ledger("selftest -- mg-f8e5's own arms, all forced",
                   reads_outside_tree=True)
    print("    as-of: %s" % rev[:12])

    # -------------------------------------------------------------- S1
    led.head("S1 -- THE CENSUS'S DEFINITIONS ARE IMPORTED, NOT PARAPHRASED")
    for name in ("conclusion_verdict", "verdict_tags", "carrying_commit",
                 "transcripts", "code_digest", "parse_producers"):
        same = getattr(L, name) is getattr(C, name)
        led.record(same, "S1 `%s` IS `lib_1abe.%s`, the same object -- not a "
                         "second definition that agrees today" % (name, name))
    led.record(L.SELF_DIR != C.SELF_DIR,
               "S1' ...and `SELF_DIR` is NOT shared: this suite declares its "
               "OWN directory.  It did not, at first, and that is the defect "
               "`lib_f8e5.Ledger` exists to keep (%s vs %s)"
               % (L.SELF_DIR, C.SELF_DIR))

    # -------------------------------------------------------------- S2
    led.head("S2 -- PRODUCER RECOVERY, EACH TIER FORCED ON A REAL DIRECTORY")
    cases = [
        ("code/transcript_census_1abe/out_t1_population.txt", "T1-RUNNER",
         "a suite with a `run_all.sh` -- the census's own rule"),
        ("code/face_geometry_audit_f1b2/out_gates.txt", "T2-OTHER-SH",
         "a suite whose runner is called `run_audit.sh`"),
        ("code/libweak_c3ca/out_p1_census.txt", "T3-NAME-MAP",
         "a suite with no runner of any name"),
    ]
    for path, want, why in cases:
        c = L.carrying_commit(path, rev)
        if c is None:
            led.self_error("S2 %s is not tracked at %s" % (path, rev[:7]))
            continue
        spec, tier, note = L.recover_producer(path, c)
        led.record(tier == want,
                   "S2 %s at %s -> %s (%s; recovered via `%s`)"
                   % (path[5:], c[:7], tier, why, note))
        if want != "T4-NONE":
            led.record(spec is not None and spec["script"].endswith((".py",
                                                                     ".sh")),
                       "S2' ...and the recovered producer names a script that "
                       "exists in that tree: %s"
                       % (spec["script"] if spec else "(none)"))

    # NEGATIVE ARM: a transcript name that maps to nothing must recover NOTHING.
    fake = "code/libweak_c3ca/out_this_name_maps_to_no_script.txt"
    c = L.carrying_commit("code/libweak_c3ca/out_p1_census.txt", rev)
    spec, tier, _ = L.recover_producer(fake, c)
    led.record(tier == "T4-NONE" and spec is None,
               "S2'' NEGATIVE: an invented transcript name recovers T4-NONE, "
               "not a producer.  A recovery rule that finds a producer for a "
               "file that does not exist would find one for anything")

    # -------------------------------------------------------------- S3
    led.head("S3 -- THE MOVING-REF DETECTOR, BOTH ANSWERS ON ONE DIRECTORY")
    census = "code/transcript_census_1abe"
    before = L.resolve("a7d7fb9^")
    v_before, det_b = L.moving_ref_scan(census, before)
    v_after, det_a = L.moving_ref_scan(census, rev)
    led.record(v_before == "SHAPE",
               "S3 at %s (before mg-1abe's own fix) the detector says SHAPE, "
               "with %d of %d driven scripts resolving a moving ref"
               % (before[:7], len(det_b["movers"]), len(det_b["scripts"])))
    led.record(v_after == "PASSES-DOWN",
               "S3' at %s (after it) the SAME detector says PASSES-DOWN.  Two "
               "answers, one directory, one detector" % rev[:7])
    led.record(bool(det_b["helpers"]),
               "S3'' and the shape is reached THROUGH A LOCAL HELPER (%s): "
               "mg-1abe's scripts do not name `main` at all.  A detector "
               "reading only the driven scripts scores this directory "
               "ONE-SCRIPT, which is what mine did before this arm"
               % ", ".join(det_b["helpers"][:4]))

    # NEGATIVE ARM: a directory with no producing code cannot carry the shape.
    v_none, _ = L.moving_ref_scan("code/hodge_leverage_audit_f922", rev)
    led.record(v_none != "SHAPE",
               "S3''' NEGATIVE: a one-script suite is not the shape -- one "
               "process, one tree, no seam between two measurements (%s)"
               % v_none)

    # -------------------------------------------------------------- S4
    led.head("S4 -- A RE-RUN IN A DIRTY WORKTREE IS REFUSED, NOT MEASURED")
    path = "code/transcript_census_1abe/out_t1_population.txt"
    carrier = L.carrying_commit(path, rev)
    spec, _ = L.producer_for(path, carrier)
    if spec is None:
        led.self_error("S4 could not resolve a producer to test with")
    else:
        try:
            with L.worktree(carrier) as wt:
                clean = L.dirty_paths(wt)
                target = os.path.join(wt, "STATE.md")
                with open(target, "a", encoding="utf-8") as fh:
                    fh.write("\nmg-f8e5 selftest S4 mutation\n")
                dirty = L.dirty_paths(wt)
                led.record(not clean and dirty == ["STATE.md"],
                           "S4 a fresh worktree reports 0 dirty paths and one "
                           "appended byte makes it report exactly 1 (%s)"
                           % ", ".join(dirty))
                subprocess.run(["git", "checkout", "--", "STATE.md"], cwd=wt,
                               capture_output=True)
                led.record(not L.dirty_paths(wt),
                           "S4' ...and restoring it returns the worktree to "
                           "clean, so the guard is measuring the tree and not "
                           "the clock")
        except RuntimeError as exc:
            led.self_error("S4 worktree: %s" % exc)

    # -------------------------------------------------------------- S5
    led.head("S5 -- `shas_named_in` RESOLVES, IT DOES NOT PATTERN-MATCH")
    real = L.shas_named_in("the audit ran at 81214a9 and at eacc5e1")
    fake = L.shas_named_in("deadbee and 0123456789abcdef0123456789abcdef01234567")
    led.record(len(real) == 2,
               "S5 two real abbreviations resolve to %d commit(s)" % len(real))
    led.record(fake == [],
               "S5' NEGATIVE: two well-formed hex tokens that are NOT commits "
               "resolve to nothing (%d).  A regex that accepted them would "
               "make every transcript look like it named a revision" % len(fake))

    # -------------------------------------------------------------- S6
    led.head("S6 -- THE STATIC REACH TEST ANSWERS BOTH WAYS")
    yes, ev = L.static_reach("code/transcript_census_1abe", rev)
    no, _ = L.static_reach("code/anticorrelation_c50b", rev)
    led.record(yes,
               "S6 a suite whose library calls `git log` reads outside its "
               "tree: yes (%s)" % ", ".join(ev[:2]))
    led.record(not no,
               "S6' NEGATIVE: a pure-arithmetic suite does not.  A test that "
               "said `yes` everywhere would be `x == x` with a name on it")

    # -------------------------------------------------------------- S7
    led.head("S7 -- THE CONCLUSION GRAIN IS THE CENSUS'S, AND IT SEPARATES")
    a = "[OK       ] the count is 5\nTOTAL BAD: 0\n"
    b = "[OK       ] the count is 7\nTOTAL BAD: 0\n"
    c2 = "[FINDING  ] the count is 5\nTOTAL BAD: 0\n"
    led.record(L.conclusion_verdict(a, b) == "HELD-DRIFTED",
               "S7 a moved FIGURE inside a standing decision is HELD-DRIFTED, "
               "not a flip -- the distinction mg-1abe's defect 1 exists for")
    led.record(L.conclusion_verdict(a, c2) == "FLIPS",
               "S7' a changed DECISION on the same figure is FLIPS")
    led.record(L.conclusion_verdict(a, "") == "FLIPS",
               "S7'' AND AN EMPTY TRANSCRIPT IS ALSO FLIPS, which is how a "
               "suite killed at the census's budget comes to be reported as a "
               "false record (see `out_d5_timeout.txt`)")

    # -------------------------------------------------------------- S8
    led.head("S8 -- A PRODUCER THAT DIED IS NOT A TRANSCRIPT THAT DISAGREES")
    print("""THIS ARM EXISTS BECAUSE THIS SUITE COMMITTED THE DEFECT IT REPORTS,
inside an hour of reporting it.  `lib_1abe._RE_RED` captures the producer
command WITHOUT its interpreter, because mg-1abe never executes it -- it runs
the whole `run_all.sh`.  `d1` did execute it, so every one of the five ran as
`-u c1_rebase.py > out_c1_rebase.txt`, the shell answered 127, the redirection
had ALREADY created an empty transcript, and d1 printed
`FLIP re-derived -- 8 decision rows lost` off a file nothing had written.

That is `d5_timeout.py`'s entire finding, reproduced by the instrument that
reports it.  Two arms below: the interpreter is put back, and a run that dies
is refused rather than compared.
""")
    spec = {"cmd": "-u t1_population.py", "script": "t1_population.py"}
    inv = L.invocation(spec)
    led.record(inv.split()[0] == "python3",
               "S8 `invocation` puts the interpreter back: %r -> %r"
               % (spec["cmd"], inv))
    led.record(L.invocation({"cmd": "./x.sh", "script": "x.sh"}).startswith("sh "),
               "S8' ...and chooses `sh` for a `.sh` producer, not `python3`")

    broken = {"cmd": "-u this_script_does_not_exist.py", "combined": True,
              "script": "t1_population.py", "dir": census}
    res = L.rerun_at(carrier, path, broken, timeout=120,
                     committed=L.blob_at(rev, path))
    led.record(res["status"] == "RUNNER-FAILED",
               "S8'' NEGATIVE AND THE ONE THAT MATTERS: a producer that cannot "
               "run still leaves a transcript, because its own redirection "
               "created one -- and `rerun_at` reports %s rather than `ok`, so "
               "no caller can compare it against the committed bytes and call "
               "the difference a flip" % res["status"])
    led.record(bool(res["bytes"]) and res["rc"] not in (0, 127),
               "S8''' ...and the file it left behind is NOT empty (%d bytes of "
               "shell error, because the runner folds stderr in) -- so a guard "
               "keyed on emptiness alone would have called this a measurement. "
               "It is refused because it carries NO verdict-bearing line "
               "while the transcript it claims to reproduce is made of them"
               % len(res["bytes"] or b""))

    return led.done()


if __name__ == "__main__":
    sys.exit(main())
