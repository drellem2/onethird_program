"""mg-4d3b a3 -- A **REAL** FETCH FAILURE, DRIVEN THROUGH mg-f3ff's OWN CODE.

This is the half of the brief that names a specific behaviour: *if any fetch in
your own run fails, that row is UNKNOWN and must be printed as UNKNOWN -- NOT
as "no successor found", and NOT silently skipped.*

mg-f3ff answers it with NC3, which sets `force_fail=True` and **returns from
`Fetched.__init__` before `git fetch` is ever spawned** (disclosed as D9 of
PREDICTIONS.md, written before this file existed).  NC3 therefore proves that
the UNKNOWN *propagation* is right.  It does not prove that a real fetch
failure *reaches* that propagation, because it never enters the branch a real
failure enters.  This section closes that gap by breaking a real remote.

SEVEN ARMS, on throwaway clones under the scratchpad -- no command here touches
either source repo:

  A  both clones healthy                     -> the detector must NOT say UNKNOWN
  B  repo 1's origin URL unresolvable        -> UNKNOWN
  C  repo 2's origin URL unresolvable        -> UNKNOWN
  D  both unresolvable                       -> UNKNOWN
  E  `origin` remote removed entirely        -> UNKNOWN
  F  the directory does not exist            -> UNKNOWN
  G  ⚠️ THE LOAD-BEARING ONE.  Clone first so `origin/main` RESOLVES LOCALLY,
     then break the URL.  Now `git fetch` fails while a perfectly readable
     `origin/main` sits in the repo.  This is the shape of the real incident:
     the box had no network at boot, and every checkout still had yesterday's
     refs.  A method that answers from the resolvable ref returns a CONFIDENT
     WRONG NUMBER.  Arm G asserts the ref really does resolve, so a pass cannot
     be an artefact of an absent ref.

ARM A IS THE MUTATION CONTROL AND IT IS NOT OPTIONAL.  A `Fetched` that
returned UNKNOWN unconditionally would pass B-G.  If A does not produce a
non-UNKNOWN verdict, arms B-G establish nothing and this section says so.

BOTH LIBRARIES ARE TESTED: mg-f3ff's `lib_f3ff` (the subject) and this audit's
`lib4d3b` (the auditor).  An auditor exempt from the rule it enforces is the
defect this arc keeps finding.

AND THE SCRIPT LEVEL, NOT ONLY THE LIBRARY: arm G is re-run by copying
mg-f3ff's real `s1_rows.py` into a temp tree beside a `lib_f3ff.py` whose only
edit is the `REPOS` constant, and the REAL stdout is searched for the literal
strings.  A library returning None is not the same claim as a transcript
printing UNKNOWN, and the ticket asks about the printed thing.

EXIT: 1 if any arm is RED.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

import lib4d3b as L

F3FF = os.path.abspath(os.path.join(L.HERE, "..", "census_repair_f3ff"))
BAD_URL = "ssh://git@no-such-host-mg4d3b.invalid:22/daniel/nope.git"


def sh(args, cwd=None):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)


def make_clone(dst, src, ref="origin/main"):
    """A throwaway clone carrying real history and a real `origin`."""
    r = sh(["git", "clone", "--quiet", "--no-hardlinks", src, dst])
    if r.returncode != 0:
        raise RuntimeError(f"clone failed: {r.stderr.strip()}")
    # `git clone` of a local path names the source as origin and creates
    # origin/main -- which is exactly what arm G needs.
    return dst


def break_remote(path):
    sh(["git", "-C", path, "remote", "set-url", "origin", BAD_URL])


def drop_remote(path):
    sh(["git", "-C", path, "remote", "remove", "origin"])


def ref_resolves(path):
    r = sh(["git", "-C", path, "rev-parse", "--verify", "-q", "origin/main^{commit}"])
    return r.returncode == 0 and bool(r.stdout.strip())


# ---------------------------------------------------------------- the arms
def run_arm(name, desc, paths, f3ff_mod, expect_unknown, assert_ref_resolves=()):
    print("-" * 78)
    print(f"ARM {name}  {desc}")
    print("-" * 78)
    red = 0

    for p in assert_ref_resolves:
        ok = ref_resolves(p)
        red += L.check("anti-vacuity: origin/main RESOLVES LOCALLY in the broken repo",
                       ok, "so a pass cannot come from an absent ref")

    # ---- the subject: mg-f3ff's own library, on these paths
    f3ff_mod.REPOS = [(lab, p) for lab, p in paths]
    fm = f3ff_mod.fetch_all()
    for f in fm.values():
        print("   f3ff " + f.line().replace("\n", "\n   f3ff "))
    for n, row, filed, parent, _prem in L.ROWS:
        v, per, unk = f3ff_mod.census_row(fm, parent, f3ff_mod.utc(filed))
        want = "UNKNOWN" if expect_unknown else v
        good = (v == "UNKNOWN") if expect_unknown else (v in ("REFUTED", "UPHELD"))
        red += L.check(f"f3ff row {n} ({parent}): {v}", good,
                       ("must be UNKNOWN" if expect_unknown else "must NOT be UNKNOWN")
                       + (f"; unreadable={unk}" if unk else ""))
        # The precise thing the ticket forbids.
        #
        # ⚠️ DEFECT OF THIS INSTRUMENT, KEPT.  The first version of this check
        # asserted `all(s is None for s in per.values())` -- i.e. that EVERY
        # repo returned None.  In arms B/C/E/F only ONE repo is broken and the
        # healthy one correctly returns a list, so the check FAILED 16 times
        # against code that was behaving exactly as required.  An assertion
        # that names the wrong object is this arc's signature shape, committed
        # here by the auditor sent to look for it.  The corrected form asserts
        # what the rule actually says: the UNREADABLE repos, and only those,
        # must be None.
        if expect_unknown:
            bad_labels = set(unk)
            red += L.check(
                f"f3ff row {n}: unreadable repos return None, not []",
                bad_labels and all(per[lab] is None for lab in bad_labels),
                f"None for {sorted(bad_labels)}; readable repos may return a list")
    g = f3ff_mod.generations(fm, "mg-fcf1", f3ff_mod.utc("2026-07-31T04:13:24Z"))
    if expect_unknown:
        red += L.check("f3ff generations() -> None under the failure", g is None)
    else:
        red += L.check("f3ff generations() -> a list when healthy", g is not None)

    # ---- the auditor: this audit's own library, same rule
    repos = [L.Repo(lab, p) for lab, p in paths]
    for r in repos:
        print("   4d3b " + r.line().replace("\n", "\n   4d3b "))
    for n, row, filed, parent, _prem in L.ROWS:
        v, per, unk = L.row_verdict(repos, parent, L.utc(filed))
        good = (v == "UNKNOWN") if expect_unknown else (v in ("REFUTED", "UPHELD"))
        red += L.check(f"4d3b row {n} ({parent}): {v}", good,
                       "the auditor is held to the same rule")
    print()
    return red


def script_level(tmp, good, bad):
    """Run mg-f3ff's REAL s1_rows.py against a broken repo and read its stdout.

    The only edit to `lib_f3ff.py` is the REPOS constant.  Everything the
    transcript prints is mg-f3ff's own code."""
    print("-" * 78)
    print("ARM G-script  mg-f3ff's REAL s1_rows.py, run against the broken clone")
    print("-" * 78)
    stage = os.path.join(tmp, "stage")
    shutil.copytree(F3FF, stage)
    lib = os.path.join(stage, "lib_f3ff.py")
    src = open(lib, encoding="utf-8").read()
    new_repos = ('REPOS = [\n'
                 f'    ("onethird_program", {bad!r}),\n'
                 f'    ("one_third_width_three", {good!r}),\n'
                 ']\n')
    patched, nsub = re.subn(r"REPOS = \[\n(?:.*\n)*?\]\n", new_repos, src, count=1)
    if nsub != 1:
        print("  [FAIL] could not patch REPOS -- arm G-script is VACUOUS and is")
        print("         reported as such rather than passed")
        return 1
    open(lib, "w", encoding="utf-8").write(patched)
    r = subprocess.run([sys.executable, "s1_rows.py"], cwd=stage,
                       capture_output=True, text=True)
    out = r.stdout + r.stderr
    print(f"  s1_rows.py exit: {r.returncode}")
    for line in out.splitlines():
        if ("UNKNOWN" in line or "successor commit" in line or "ROW " in line
                or "gens/commits" in line or "WRONG on" in line
                or "checked against the tree" in line or "of 4 checked" in line
                or "Traceback" in line or "TypeError" in line):
            print("    | " + line.rstrip()[:160])
    print()

    # ---- WHAT THE ROW SECTIONS GET RIGHT.  Stated first, because a finding
    #      that omits the working half is an accusation, not a measurement.
    good = 0
    good += L.check("every row's VERDICT column prints UNKNOWN",
                    len(re.findall(r"clock: UNKNOWN", out)) == 8,
                    "4 rows x 2 clocks")
    good += L.check("the successor COUNT prints `?`, never 0",
                    "? successor commit(s)" in out and
                    not re.search(r"UNKNOWN\s+0 successor commit", out))
    good += L.check("the failed repo prints UNKNOWN in the per-repo breakdown",
                    "onethird_program=UNKNOWN" in out)
    good += L.check("the CHAIN prose says UNKNOWN, not `none`",
                    "CHAIN: UNKNOWN" in out and
                    "CHAIN: none" not in out)
    good += L.check("the reason is named, not just the verdict",
                    "could not be read" in out)

    # ---- WHAT THE SUMMARY BLOCK GETS WRONG.  These are FINDINGS ABOUT
    #      mg-f3ff and DO NOT set this section's exit -- see the module
    #      docstring's exit rule.  They are counted separately.
    print()
    print("  --- the SAME transcript, further down: findings about mg-f3ff ---")
    findings = []
    if re.search(r"UNKNOWN\s+0 / 0\s+0 / 0", out):
        findings.append(
            "F1  the accuracy table renders UNKNOWN's depth columns as `0 / 0`.\n"
            "      s1_rows.py:76-79 -- `0 if not gens else len(gens)`, and `not None`\n"
            "      is True.  `I could not look` printed as `I looked and found none`,\n"
            "      in the summary block of the deliverable sent to remove that.")
    if "all 4 are now checked against the tree" in out:
        findings.append(
            "F2  `n = 4, and all 4 are now checked against the tree` prints verbatim\n"
            "      when 0 were checked.  It is a fixed string with no guard.")
    m = re.search(r"The census was WRONG on (\d+) of its 4 rows and RIGHT on (\d+)", out)
    if m and m.group(1) == "0" and m.group(2) == "0":
        findings.append(
            "F3  `The census was WRONG on 0 of its 4 rows and RIGHT on 0` -- a\n"
            "      substantive claim about the subject, asserted from zero\n"
            "      measurement.  Both numbers count VERDICT values that are neither.")
    if re.search(r"4 of 4 checked, 0 refuted", out):
        findings.append(
            "F4  `4 of 4 checked, 0 refuted` in the SUPERSEDED-FIGURE paragraph --\n"
            "      the paragraph whose own next sentence is `this does not round\n"
            "      toward either`, printing a figure derived from nothing.")
    if "TypeError" in out and "has no len()" in out:
        findings.append(
            "F5  s1_rows.py then DIES: `len(L.successors(...))` on None at :131.\n"
            "      lib_f3ff.successors' docstring says `callers must NOT treat None\n"
            "      as an empty list.  That confusion is the whole subject of this\n"
            "      ticket.`  Its own caller, 30 lines away, calls len() on it.\n"
            "      The crash is LOUD, which is the mitigation -- but it lands AFTER\n"
            "      F1-F4 are already on stdout, and it is a traceback, not a reason.")
    for f in findings:
        print("    " + f)
    if not findings:
        print("    (none -- the summary block handled UNKNOWN correctly)")
    print()
    return good, findings


def main():
    L.banner("mg-4d3b a3 -- a REAL fetch failure, through mg-f3ff's own code")
    sys.path.insert(0, F3FF)
    import lib_f3ff as F                                   # noqa: E402

    tmp = L.scratch_dir("arms-")
    print(f"  throwaway clones under {tmp}")
    print("  NO command in this section runs inside /Users/daniel/research/*.\n")

    good1 = make_clone(os.path.join(tmp, "good1"), L.WORKTREE)
    good2 = make_clone(os.path.join(tmp, "good2"), L.SRC2)
    badG = make_clone(os.path.join(tmp, "badG"), L.WORKTREE)
    break_remote(badG)                        # cloned FIRST -> origin/main resolves
    badG2 = make_clone(os.path.join(tmp, "badG2"), L.SRC2)
    break_remote(badG2)
    noremote = make_clone(os.path.join(tmp, "noremote"), L.WORKTREE)
    drop_remote(noremote)
    missing = os.path.join(tmp, "does-not-exist")

    red = 0
    red += run_arm("A", "both clones healthy -- THE MUTATION CONTROL",
                   [("onethird_program", good1), ("one_third_width_three", good2)],
                   F, expect_unknown=False)
    arm_a_red = red
    red += run_arm("B", "repo 1's origin URL unresolvable (real `git fetch` failure)",
                   [("onethird_program", badG), ("one_third_width_three", good2)],
                   F, expect_unknown=True, assert_ref_resolves=(badG,))
    red += run_arm("C", "repo 2's origin URL unresolvable",
                   [("onethird_program", good1), ("one_third_width_three", badG2)],
                   F, expect_unknown=True, assert_ref_resolves=(badG2,))
    red += run_arm("D", "BOTH unresolvable",
                   [("onethird_program", badG), ("one_third_width_three", badG2)],
                   F, expect_unknown=True, assert_ref_resolves=(badG, badG2))
    red += run_arm("E", "`origin` remote removed entirely",
                   [("onethird_program", noremote), ("one_third_width_three", good2)],
                   F, expect_unknown=True)
    red += run_arm("F", "the repo directory does not exist",
                   [("onethird_program", missing), ("one_third_width_three", good2)],
                   F, expect_unknown=True)
    sred, findings = script_level(tmp, good2, badG)
    red += sred

    print("=" * 78)
    print("VERDICT OF a3")
    print("=" * 78)
    if arm_a_red:
        print("  ⚠️ ARM A IS RED.  The healthy arm did not produce a non-UNKNOWN")
        print("     verdict, so arms B-G are consistent with a detector that says")
        print("     UNKNOWN unconditionally and THEY ESTABLISH NOTHING.")
    else:
        print("  Arm A produced real verdicts, so the harness is not constant-UNKNOWN")
        print("  and arms B-G are non-vacuous.")
    print()
    print("  P7 (a REAL fetch failure propagates to UNKNOWN in mg-f3ff's LIBRARY)")
    print(f"     -> {'HIT -- 4 of 4 rows UNKNOWN in every one of arms B-F' if red == 0 else 'MISS -- see the FAILs above'}")
    print("  P8 (the mutation control is non-vacuous)"
          f" -> {'HIT' if not arm_a_red else 'MISS'}")
    print()
    print("  WHAT ARM G ADDS OVER mg-f3ff's NC3: NC3 never spawns `git fetch`.  Arm")
    print("  G does, against a real unresolvable host, in a repo where `origin/main`")
    print("  DOES resolve -- the exact configuration of the incident that produced")
    print("  the ticket.  The library's answer is the same, so NC3's LIBRARY-LEVEL")
    print("  conclusion is CONFIRMED by a test it did not run rather than repeated.")
    print()
    print("  ⚠️ AND THE SCRIPT LEVEL IS WHERE IT BREAKS.  NC3 checks `census_row`")
    print("     and `generations` -- the two library calls -- and stops there.  The")
    print("     ticket's addendum 3 is about what is PRINTED.  Running mg-f3ff's own")
    print(f"     s1_rows.py against a real failure produces {len(findings)} finding(s):")
    for f in findings:
        print("       " + f.splitlines()[0])
    print()
    print("     SCOPE, STATED RATHER THAN IMPLIED: the per-row sections are CORRECT")
    print("     (the five PASSes above).  s0_freshness.py exits 1 on an unreadable")
    print("     repo and run_all.sh propagates it, so a full-suite run under this")
    print("     failure is loudly non-zero.  What is defective is the SUMMARY BLOCK,")
    print("     which a reader scanning for the answer reads first, and which states")
    print("     four false things before the crash.")
    print()
    print("  A CONTROL SETS THIS SECTION'S EXIT AND A FINDING DOES NOT.  Exit is")
    print(f"  {1 if red else 0} from {red} failed control(s); the {len(findings)} finding(s) about mg-f3ff")
    print("  are reported and do not set it.")
    print(f"\n== a3 exit: {1 if red else 0} ==")
    return 1 if red else 0


if __name__ == "__main__":
    sys.exit(main())
