"""mg-cf83 c1 -- THE POSITIVE CONTROL FOR THE SUMMARY-BLOCK REPAIR.

mg-4d3b ran mg-f3ff's `s1_rows.py` against a repo whose `git fetch` really
failed.  The per-row sections were right and the SUMMARY BLOCK, in the same
transcript, printed:

  F1  four rows of `0 / 0` in the depth columns  (`0 if not gens else len(gens)`
      -- `not None` is True, so unreadable rendered as measured-and-empty)
  F2  `n = 4, and all 4 are now checked against the tree`, when 0 were
  F3  `The census was WRONG on 0 of its 4 rows and RIGHT on 0`
  F4  `4 of 4 checked, 0 refuted`, in the paragraph whose next sentence is
      `this does not round toward either`
  F5  then a TypeError: `len(L.successors(...))` on None at :131

This file is the acceptance for the repair of all five, and it is a POSITIVE
CONTROL rather than a re-read of the source: it drives mg-f3ff's REAL
`s1_rows.py` -- copied byte-for-byte out of `code/census_repair_f3ff/`, with
the single-constant `REPOS` patch and nothing else -- against real throwaway
clones, and greps the REAL stdout for the literal strings.

THREE ARMS.  ⚠️ ARM H IS NOT OPTIONAL AND IT IS FIRST:

  H  BOTH CLONES HEALTHY -- THE MUTATION CONTROL.  A summary that printed
     UNKNOWN unconditionally would pass arms D and P and be worthless.  Arm H
     requires real verdicts, the `all 4 are now checked` sentence, no `?` in
     any depth cell, and mg-4d3b's CONFIRMED `2 of 4` reproduced unchanged --
     the repair must not have moved a number.
  D  BOTH remotes broken, CLONE FIRST THEN BREAK THE URL, so `origin/main`
     still RESOLVES LOCALLY while `git fetch` fails.  This is the incident's
     own shape -- no network at boot, every checkout holding yesterday's refs
     -- and it is the arm mg-4d3b's F1-F5 came from.  The ref is asserted to
     resolve, so a pass cannot be an artefact of an absent ref.
  P  ONE remote broken.  UNKNOWN is sticky per lib_f3ff, so the rows are
     UNKNOWN while half the population is perfectly readable; this is the arm
     where a summary is most tempted to report the half it can see.

AND A STRUCTURAL CHECK IN EVERY ARM, which is the repair's third rule: the
verdict column of the summary table is compared, row by row, against the
verdict the ROW SECTION printed for the same row.  The two are read out of the
same transcript by regex.  `The summary must not be able to disagree with the
rows` is a property, and a property is checked, not asserted.

⚠️ NOT A RE-DERIVATION OF THE CENSUS.  mg-4d3b confirmed 7/5/0/0 and
REFUTED/REFUTED/UPHELD/UPHELD from a disjoint reader.  Nothing here re-derives
them; arm H merely requires that they did not change.

EXIT: 1 if any check of this control fails.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
WORKTREE = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC2 = "/Users/daniel/research/one_third_width_three"
F3FF = os.path.abspath(os.path.join(HERE, "..", "census_repair_f3ff"))
BAD_URL = "ssh://git@no-such-host-mgcf83.invalid:22/daniel/nope.git"


def sh(args, cwd=None):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)


def banner(t):
    print("=" * 78)
    print(t)
    print("=" * 78)


def check(label, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f" -- {detail}" if detail else ""))
    return 0 if ok else 1


def make_clone(dst, src):
    r = sh(["git", "clone", "--quiet", "--no-hardlinks", src, dst])
    if r.returncode != 0:
        raise RuntimeError(f"clone failed: {r.stderr.strip()}")
    return dst


def break_remote(path):
    sh(["git", "-C", path, "remote", "set-url", "origin", BAD_URL])


def ref_resolves(path):
    r = sh(["git", "-C", path, "rev-parse", "--verify", "-q", "origin/main^{commit}"])
    return r.returncode == 0 and bool(r.stdout.strip())


# --------------------------------------------------------------------------
# Running mg-f3ff's own script, with one constant changed
# --------------------------------------------------------------------------
def run_s1(tmp, tag, repo1, repo2):
    """Copy census_repair_f3ff verbatim, patch REPOS ONLY, run s1_rows.py.

    Returns (returncode, stdout+stderr, staging dir).  A patch that did not
    apply would run the real repo list and pass everything VACUOUSLY, so the
    substitution count is checked by the caller, not assumed."""
    stage = os.path.join(tmp, f"stage_{tag}")
    shutil.copytree(F3FF, stage)
    lib = os.path.join(stage, "lib_f3ff.py")
    src = open(lib, encoding="utf-8").read()
    new_repos = ('REPOS = [\n'
                 f'    ("onethird_program", {repo1!r}),\n'
                 f'    ("one_third_width_three", {repo2!r}),\n'
                 ']\n')
    patched, nsub = re.subn(r"REPOS = \[\n(?:.*\n)*?\]\n", new_repos, src, count=1)
    open(lib, "w", encoding="utf-8").write(patched)
    if nsub != 1:
        return None, "", stage
    r = subprocess.run([sys.executable, "s1_rows.py"], cwd=stage,
                       capture_output=True, text=True, timeout=1800)
    return r.returncode, r.stdout + r.stderr, stage


# mg-4d3b's five findings as the literal strings it read off stdout, plus the
# two claims-from-nothing they imply.  Under a fetch failure NONE of these may
# appear anywhere in the transcript.
FORBIDDEN_ANYWHERE = [
    (r"UNKNOWN\s+0 / 0", "F1  UNKNOWN's depth columns rendered `0 / 0`"),
    (r"all 4 are now checked against the tree",
     "F2  `all 4 are now checked` when 0 were"),
    (r"WRONG on 0 of its 4 rows", "F3  `WRONG on 0 of its 4 rows`"),
    (r"RIGHT on 0\b", "F3  `RIGHT on 0`"),
    (r"4 of 4 checked, 0 refuted", "F4  `4 of 4 checked, 0 refuted`"),
    (r"has no len\(\)", "F5  the TypeError on len(None)"),
    (r"MISSES on row", "predictions scored MISS off rows nobody read"),
    (r"0 of 4 hit", "a hit rate reported by a run with no measurements"),
]

ROW_VERDICT_RE = re.compile(r"^\s+author\s+clock:\s+(\w+)", re.M)
TABLE_ROW_RE = re.compile(
    r"^\s+(\d)\s+(mg-[0-9a-f]{4})\s+(mg-[0-9a-f]{4})\s+(\w+)\s+(\S+)\s*/\s*(\S+)"
    r"\s+(\S+)\s*/\s*(\S+)\s+(\w+)", re.M)


def summary_block(out):
    """Everything from the accuracy banner on -- the part a human reads."""
    i = out.find("THE CENSUS'S ACCURACY")
    return out[i:] if i >= 0 else ""


def echo(out, keys):
    for line in out.splitlines():
        if any(k in line for k in keys):
            print("    | " + line.rstrip()[:160])


def structural_agreement(out):
    """THE REPAIR'S RULE 3, CHECKED RATHER THAN ASSERTED.

    Read the per-row verdicts out of the ROW SECTIONS and the verdict column
    out of the SUMMARY TABLE, from the same transcript, and require them equal
    row by row.  This is the check that would have caught the whole defect
    class: mg-4d3b's transcript had UNKNOWN in the rows and 0-shaped figures
    in the summary, and no assertion anywhere compared them."""
    rows = ROW_VERDICT_RE.findall(out)
    table = [m[3] for m in TABLE_ROW_RE.findall(out)]
    return rows, table, (len(rows) == 4 and len(table) == 4 and rows == table)


def depth_cells(out):
    """The four depth columns per table row, as printed."""
    return [(m[4], m[5], m[6], m[7]) for m in TABLE_ROW_RE.findall(out)]


# --------------------------------------------------------------------------
# ARM H -- the mutation control
# --------------------------------------------------------------------------
def arm_healthy(tmp, good1, good2):
    print("-" * 78)
    print("ARM H  both clones HEALTHY -- THE MUTATION CONTROL")
    print("-" * 78)
    print("  A summary hard-wired to say UNKNOWN would pass arms D and P.  This arm")
    print("  is what makes them mean something, and it is also the regression check:")
    print("  mg-4d3b CONFIRMED `2 of 4` from a disjoint reader, and the repair is not")
    print("  allowed to have moved it.")
    rc, out, _ = run_s1(tmp, "healthy", good1, good2)
    red = 0
    red += check("REPOS patch applied (an unpatched arm passes VACUOUSLY)", rc is not None)
    if rc is None:
        return 1, ""
    print(f"  s1_rows.py exit: {rc}")
    echo(out, ["clock:", "checked against the tree", "WRONG on", "of 4 checked",
               "gens/commits", "  1   mg-", "  2   mg-", "  3   mg-", "  4   mg-",
               "Predictions scored", "Traceback", "TypeError", "s1 exit"])
    print()
    red += check("exit 0 on the healthy path", rc == 0)
    red += check("no crash", "Traceback" not in out)
    rows, table, agree = structural_agreement(out)
    red += check("summary table agrees with the row sections, row by row", agree,
                 f"rows={rows} table={table}")
    red += check("real verdicts, no UNKNOWN", "UNKNOWN" not in rows,
                 "the fix must not answer UNKNOWN when it CAN look")
    red += check("F2's sentence is still printed when it is TRUE",
                 "all 4 are now checked against the tree" in out)
    red += check("mg-4d3b's confirmed figure is unmoved: WRONG on 2, RIGHT on 2",
                 "The census was WRONG on 2 of its 4 rows and RIGHT on 2." in out,
                 "a repair that changes a confirmed number is a regression")
    red += check("the supersession still reads `4 of 4 checked, 2 refuted`",
                 "4 of 4 checked, 2 refuted" in out)
    cells = depth_cells(out)
    red += check("no `?` in any depth cell when every repo was read",
                 bool(cells) and all("?" not in c for row in cells for c in row),
                 f"{cells}")
    red += check("nothing is marked UNMEASURED on a fully measured run",
                 "UNMEASURED" not in summary_block(out))
    print()
    return red, out


# --------------------------------------------------------------------------
# ARMS D and P -- the acceptance
# --------------------------------------------------------------------------
def arm_broken(tmp, tag, desc, repo1, repo2, assert_resolves):
    print("-" * 78)
    print(f"ARM {tag.upper()}  {desc}")
    print("-" * 78)
    red = 0
    for p in assert_resolves:
        red += check("anti-vacuity: origin/main RESOLVES LOCALLY in the broken clone",
                     ref_resolves(p),
                     "so a pass cannot come from an absent ref -- this is the "
                     "incident's shape, not a missing repo")
    rc, out, _ = run_s1(tmp, tag, repo1, repo2)
    red += check("REPOS patch applied (an unpatched arm passes VACUOUSLY)", rc is not None)
    if rc is None:
        return 1, ""
    print(f"  s1_rows.py exit: {rc}")
    echo(out, ["clock:", "checked against the tree", "WRONG on", "of 4 checked",
               "DID NOT MEASURE", "  1   mg-", "  2   mg-", "  3   mg-", "  4   mg-",
               "Predictions scored", "UNMEASURED", "Traceback", "TypeError",
               "s1 exit", "DOES NOT SUPERSEDE", "VERDICT VALUES"])
    print()
    blk = summary_block(out)
    red += check("there IS a summary block to judge", bool(blk))

    # ---- F5 first: before mg-cf83 the script never reached the end.
    red += check("F5 GONE: no TypeError, no traceback -- the script completes",
                 "Traceback" not in out and "has no len()" not in out,
                 "`len(None)` at :131, 30 lines from the docstring forbidding it")
    red += check("exit is 1, deliberately, and printed with its reason",
                 rc == 1 and "THIS RUN MEASURED NOTHING" in out,
                 "an unmeasurable run is not a finding about the census")

    # ---- F1
    cells = depth_cells(out)
    red += check("F1 GONE: no UNKNOWN row renders its depths as `0 / 0`",
                 re.search(r"UNKNOWN\s+0 / 0", out) is None)
    red += check("F1 GONE: every depth cell of an UNKNOWN row prints `?`",
                 len(cells) == 4 and all(c == "?" for row in cells for c in row),
                 f"{cells}")

    # ---- F2
    red += check("F2 GONE: `all 4 are now checked against the tree` is not printed",
                 "all 4 are now checked against the tree" not in out)
    red += check("F2 GONE: the count of checked rows is 0 and says so",
                 "0 of 4 are checked against the tree" in out)
    red += check("F2 GONE: the unreadable rows are NAMED",
                 re.search(r"ROW\(S\) 1, 2, 3, 4 ARE UNKNOWN", out) is not None)

    # ---- F3
    red += check("F3 GONE: `WRONG on 0 of its 4 rows and RIGHT on 0` is not printed",
                 "WRONG on 0 of its 4 rows" not in out)
    red += check("F3 GONE: the accuracy sentence says UNKNOWN in both slots",
                 "The census was WRONG on UNKNOWN of its 4 rows and RIGHT on UNKNOWN."
                 in out)
    red += check("F3 GONE: the verdict-value tally is labelled as one, not as a finding",
                 "these are counts of VERDICT VALUES" in out,
                 "`REFUTED 0 of 4` must not read as `nothing was refuted`")

    # ---- F4
    red += check("F4 GONE: `4 of 4 checked, 0 refuted` is not printed",
                 not re.search(r"4 of 4 checked, 0 refuted", out))
    red += check("F4 GONE: the brief's figure is NOT declared superseded",
                 "DOES NOT SUPERSEDE" in out and "now SUPERSEDED" not in out)

    # ---- the prediction scoring, which is also a claim from zero measurement
    red += check("no prediction is scored MISS off an unread row",
                 "MISSES on row" not in out and "*** MISS ***" not in blk)
    red += check("the prediction tally reports NONE, not a hit rate of zero",
                 "Predictions scored: NONE -- all 4 rows UNMEASURED" in out,
                 "`0 of 4 hit, 0 missed` is true of the tally and false as a report")
    red += check("P5 is UNMEASURED rather than refuted",
                 re.search(r"P5.*", blk) is not None
                 and "*** UNMEASURED ***" in blk)
    red += check("P2's per-repo sub-clause prints no count at all",
                 "UNMEASURED -- row 2 came back UNKNOWN above" in out
                 and not re.search(r"onethird_program=\d", blk))

    # ---- rule 3
    rows, table, agree = structural_agreement(out)
    red += check("summary table agrees with the row sections, row by row", agree,
                 f"rows={rows} table={table}")
    red += check("the rows really did say UNKNOWN (else this arm is vacuous)",
                 rows == ["UNKNOWN"] * 4, f"rows={rows}")

    # ---- and the blunt one, over the WHOLE transcript rather than the block
    #
    # ⚠️ DEFECT OF THIS INSTRUMENT, KEPT AND FIXED AT ITS CAUSE.  The first
    # version of this check swept for `\b0 (of its|refuted|missed)\b` and
    # FAILED TWICE against a correctly repaired script.  One hit was
    # s1_rows.py's own new prose QUOTING the string it no longer prints -- a
    # grep reading a sentence about the defect as the defect, which is
    # mg-4d3b's a5 defect committed by the polecat sent to repair mg-4d3b's
    # finding.  The other was `0 missed`, which is TRUE and not a claim from
    # zero measurement, so the pattern was wrong and not merely unlucky.
    #
    # The repair is at the cause: s1_rows.py no longer reproduces any of the
    # five literal strings anywhere in its output, not even as a quotation, so
    # a whole-transcript grep is legitimate and needs no prose/code
    # classifier.  ZEROS ABOUT THE RUN SURVIVE ON PURPOSE -- `0 of 4 are
    # checked` and `REFUTED 0 of 4` are measured facts about what this run
    # did, and a rule banning every zero would have deleted F2's own
    # replacement.  What is forbidden is a zero standing where a MEASUREMENT
    # OF THE CENSUS would go.
    forb = [(p, d) for p, d in FORBIDDEN_ANYWHERE if re.search(p, out)]
    red += check("none of mg-4d3b's five literal defect strings appears ANYWHERE",
                 not forb, "; ".join(d for _, d in forb) or
                 "not in a heading, not in a caveat, not as a quotation")
    print()
    return red, out


def main():
    banner("mg-cf83 c1 -- the summary block under a REAL fetch failure")
    print("  SUBJECT: code/census_repair_f3ff/s1_rows.py, run as-is from disk.")
    print("  Clones are throwaway; NO command here runs inside /Users/daniel/research/*")
    print("  and nothing is fetched, checked out, stashed or pulled in either source.")
    print()

    base = os.environ.get("MGCF83_SCRATCH")
    if base:
        os.makedirs(base, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="cf83-", dir=base or None)
    print(f"  scratch: {tmp}")
    print()

    good1 = make_clone(os.path.join(tmp, "good1"), WORKTREE)
    good2 = make_clone(os.path.join(tmp, "good2"), SRC2)
    bad1 = make_clone(os.path.join(tmp, "bad1"), WORKTREE)
    break_remote(bad1)          # cloned FIRST, so origin/main still resolves
    bad2 = make_clone(os.path.join(tmp, "bad2"), SRC2)
    break_remote(bad2)

    red_h, _ = arm_healthy(tmp, good1, good2)
    red_d, _ = arm_broken(
        tmp, "d", "BOTH remotes broken AFTER cloning -- THE ACCEPTANCE",
        bad1, bad2, (bad1, bad2))
    red_p, _ = arm_broken(
        tmp, "p", "ONE remote broken -- half the population is perfectly readable",
        bad1, good2, (bad1,))

    red = red_h + red_d + red_p
    banner("VERDICT OF c1")
    if red_h:
        print("  ⚠️ ARM H IS RED.  The healthy arm did not produce real verdicts, so")
        print("     arms D and P are consistent with a summary that says UNKNOWN")
        print("     unconditionally and THEY ESTABLISH NOTHING.")
    else:
        print("  Arm H produced real verdicts and mg-4d3b's confirmed `2 of 4`")
        print("  unchanged, so arms D and P are non-vacuous and the repair did not")
        print("  buy its UNKNOWNs by giving up the measurements.")
    print()
    print(f"  arm H (healthy):        {red_h} failed check(s)")
    print(f"  arm D (both broken):    {red_d} failed check(s)")
    print(f"  arm P (one broken):     {red_p} failed check(s)")
    print()
    print("  WHAT THIS CONTROL DOES AND DOES NOT ESTABLISH.  It establishes that")
    print("  mg-4d3b's F1-F5 do not reproduce, in the real stdout of the real")
    print("  script, under a real `git fetch` failure against a repo whose")
    print("  origin/main resolves.  It does NOT re-derive the census figures --")
    print("  those are mg-4d3b's, confirmed, and arm H only requires them unmoved.")
    print("  It does not test s2/s3/s4, whose summaries were not in this ticket.")
    print()
    print(f"\n== c1 exit: {1 if red else 0} ==")
    return 1 if red else 0


if __name__ == "__main__":
    sys.exit(main())
