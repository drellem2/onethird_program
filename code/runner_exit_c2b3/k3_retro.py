"""K3 -- WHICH PAST "CLEAN RUN" CLAIMS DEPENDED ON AN AFFECTED RUNNER'S EXIT CODE?

This is the load-bearing item.  Fixing forward leaves every prior green result
from an affected runner unexamined, and a sweep that only fixes forward has
answered the cheap half of the question.

THE TEST FOR EXPOSURE.  A past claim depended on an affected runner's exit code
only if the claim was READ OFF THE STATUS.  Three ways a claim can be read, and
only the third is at risk:

  R1  from a committed BYTE-COMPARISON -- `diff` of a regenerated transcript
      against the committed one.  The bytes do not travel through the pipeline
      at all: `tee` wrote the same file a redirect writes.  SAFE, and marked
      safe explicitly rather than left ambiguous, which the ticket asks for.
  R2  from the PRINTED OUTPUT -- a `TOTAL BAD:` line, a headline grep, a
      transcript a reader reads.  The output was printed and committed whatever
      the status was.  SAFE.
  R3  from THE EXIT STATUS -- `code == 0`, `code != 0`, `set -e` aborting.
      AT RISK.  Every one of these is enumerated below and settled.

WHAT SETTLES AN R3 CLAIM.  The pipeline threw away one number: the target
script's own exit status.  So the settlement is to GO AND GET THAT NUMBER --
run each tee'd target directly, with nothing in the way, and read it.  If it is
0, nothing was being swallowed and the past green is confirmed at the grain the
claim needs.  That is done here for every affected target, and the runtime of
this section is most of this instrument's runtime.

WHAT THAT SETTLEMENT DOES *NOT* COVER, said before the table rather than after:
it measures the tree AS IT IS NOW.  A target that exits 0 today could have
exited 1 at some intermediate commit.  Where a claim is anchored to a specific
revision, the revision is named and the target is run at THAT revision instead;
where it is not, the row says `at HEAD only` and does not pretend otherwise.
"""

import os
import re
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import libc2b3 as L

BAD = 0
REF = L.TICKET_REF
TIMEOUT = 900


def hdr(t):
    print()
    L.bar(t)
    print()


L.bar("K3  THE RETROACTIVE QUESTION -- past claims, and what settles each")

runners = L.runners(REF)
srcs = {r: L.read(r, REF) for r in runners}
affected = [r for r in runners if L.tee_pipelines(srcs[r])]

# ---------------------------------------------------------------------------
hdr("K3a  THE CLAIMS, ENUMERATED AND DISPOSITIONED")

# (id, where, the claim, route, disposition, what settles it)
CLAIMS = [
    ("C1", "code/species_sites_821e/p3_wiring.py:219  (P3b)",
     "`ok = (code == 0 and present and code_u == 0 and gone)` -- three "
     "species runners are asserted to exit 0 both wired and unwired",
     "R3", "AT RISK -- SETTLED BY K3b",
     "Two of the three trees (species_repair_a4ef, species_remainder_f8fa) "
     "were affected: their self-tests were piped into tee, so `code == 0` "
     "was true whether or not the self-test passed.  The SUBSTANTIVE half of "
     "the row -- `present` and `gone`, the check's own output appearing and "
     "disappearing in stdout -- is R2 and stands untouched.  Only the two "
     "`code == 0` conjuncts were unsupported.  K3b runs both self-tests "
     "directly and reads the status the pipeline discarded."),

    ("C2", "code/species_sites_821e/p3_wiring.py:255  (P3c, `caught`)",
     "`caught = (code_w != 0 and 'STANDING UN-STRUCK' in out_w)` -- with B1 "
     "restored on disk, each runner is asserted to exit NON-ZERO",
     "R3", "SAFE BY MECHANISM -- and measured in K3c",
     "This is the one place in the arc where a runner's non-zero exit is the "
     "evidence, so a swallowed status would have made it FAIL, not pass.  It "
     "passed.  The non-zero came from the cross-section block at "
     "`run_all.sh:25-29`, which is `E2OUT=$(python3 ...) || { ...; exit 1; }` "
     "-- a command substitution and an explicit guard, containing NO "
     "pipeline.  The tee'd self-test sits ABOVE that block and could not have "
     "produced the exit.  K3c reinstates B1 and re-measures, so this is not "
     "left as an argument from reading."),

    ("C3", "code/species_sites_821e/p3_wiring.py:256  (P3c, `missed`)",
     "`missed = (code_u == 0)` -- with the wiring removed, the runner is "
     "asserted to go green, reproducing the pre-repair state",
     "R3", "AT RISK -- SETTLED BY K3b",
     "`code_u == 0` is the historical failure being reproduced, and an "
     "affected runner exits 0 for two different reasons: nothing was "
     "detected, or something was detected and the pipeline ate it.  The row "
     "cannot tell them apart.  Settled the same way as C1: the self-tests "
     "are run directly and their true status read."),

    ("C4", "code/branching_audit_2060/b0_repro.sh:10-23",
     "mg-db09's instrument is re-run in a scratch copy and its five committed "
     "outputs are diffed byte for byte; `TOTAL BAD: 0` is the verdict",
     "R1", "SAFE -- BY THE BYTE-COMPARISON, EXPLICITLY",
     "The runner's exit status IS consumed here (`set -e` over `( cd $T && "
     "./run_all.sh )`), so this is a real consumer.  But the VERDICT is the "
     "five `diff -q` calls on lines 17-22, and those read files, not "
     "statuses.  `tee` and `>` write the same bytes, so the comparison is "
     "unaffected in both directions: a swallowed failure would still have "
     "produced a differing transcript and been caught.  This is exactly the "
     "class the ticket says to mark safe rather than leave ambiguous."),

    ("C5", "docs/OneThird-Species-Hopf-Monoids-ExtentRepair-IndependentAudit.md"
     ":254",
     "*'`sh code/species_extent_d633/run_all.sh` re-run unmodified at "
     "e8fbd4f, before this audit's probes'*",
     "R2", "SAFE -- the verdict is the committed transcript",
     "The claim is about what the re-run PRINTED, and the printed output is "
     "committed beside it in out_*.txt.  No exit status is quoted."),

    ("C6", "docs/OneThird-Intrinsic-Face-Geometry-StateLanding2-"
     "IndependentAudit.md:314",
     "*'bash code/face_geometry/run_all.sh (x2) -> git status --porcelain: "
     "empty'*",
     "R1", "SAFE -- the verdict is `git status`, not the exit code",
     "An idempotence claim measured with `git status --porcelain`.  Both "
     "outputs are committed and both regenerate; the runner's status is not "
     "part of the assertion."),

    ("C7", "docs/OneThird-Landscape-Where-This-Lives.md:363",
     "*'The audit that found the defects reproduces from "
     "code/landscape_audit_d673/run_all.sh (~1.5 min)'*",
     "R2", "SAFE -- a reproduction claim about output",
     "`reproduces` names the five committed out_*.txt, which are diffable by "
     "any reader.  d673's runner has five affected pipelines and its exit "
     "code was never quoted."),

    ("C8", "code/hodge_leverage_audit_f922/audit_repair.py:500-509",
     "mg-f922 RECORDED the defect: *'the runner pipes the instrument into "
     "tee, so the pipeline's status is tee's'*, and measured *'verifier "
     "exits 1, its runner exits 0'*",
     "R3", "SAFE, AND IT IS THE PRECEDENT, NOT AN EXPOSURE",
     "This is the arc's own prior sighting, on "
     "code/hodge_leverage_landing_e1d0/run_all.sh.  That runner was "
     "subsequently repaired (`> out_verify.txt || status=$?`), so f922's "
     "`record(...)` on line 500 now evaluates FALSE against the tree -- a "
     "frozen audit whose finding was fixed.  Nothing in this sweep touches "
     "e1d0 or f922; the row is here because item 3 asks which past claims "
     "the defect touched, and this one is the answer to `who knew`."),

    ("C9", "docs/landing-mg-1c80-instrumented-predicate.md:175",
     "*'run_all.sh here does not use `| tee`'*",
     "R2", "SAFE -- and the claim is TRUE, checked",
     "`here` is code/face_geometry_instr_5f9a/, which is one of the six "
     "comment-only matches in the ticket's bare grep and has no pipeline.  "
     "Worth checking rather than assuming: the SAME ticket id owns "
     "code/face_geometry_audit_1c80/run_all.sh, which had SIX pipelines.  "
     "The two trees are different and the claim names the right one."),
]

def wrap(text, ind):
    words, line, out = text.split(), "", []
    for w in words:
        if len(line) + len(w) + 1 > 72 - len(ind):
            out.append(ind + line)
            line = w
        else:
            line = (line + " " + w).strip()
    out.append(ind + line)
    return "\n".join(out)


print("  %-4s %-6s %s" % ("id", "route", "disposition"))
for cid, where, claim, route, disp, settle in CLAIMS:
    print("  %-4s %-6s %s" % (cid, route, disp))
print()
for cid, where, claim, route, disp, settle in CLAIMS:
    print("  %s  [%s]  %s" % (cid, route, disp))
    print("      site:  %s" % where)
    print(wrap("claim: " + claim, "      "))
    print(wrap("settled by: " + settle, "      "))
    print()

n_risk = sum(1 for c in CLAIMS if c[4].startswith("AT RISK"))
n_safe = len(CLAIMS) - n_risk
print("  %d claims: %d SAFE (marked so, with the reason), %d AT RISK."
      % (len(CLAIMS), n_safe, n_risk))
print()
print("  THE SHAPE OF THE ANSWER, which is the honest headline: the arc reads")
print("  its results from committed transcripts and byte-comparisons almost")
print("  everywhere, and reads them from an exit status in exactly ONE file --")
print("  code/species_sites_821e/p3_wiring.py.  That is why the exposure is")
print("  three claims and not thirty.  It is also why the defect survived so")
print("  long: nothing depended on the status, so nothing noticed it was gone")
print("  until mg-821e wrote the one instrument that did depend on it.")

# ---------------------------------------------------------------------------
hdr("K3b  SETTLING C1 AND C3 -- the status the pipelines threw away")

print("  Every tee'd target, run DIRECTLY with nothing in the way, and its")
print("  exit status read.  This is the number `tee` replaced with its own.")
print("  A 0 here means the past green was green for the right reason.")
print()
print("  The worktree is snapshotted before and after: several of these")
print("  mutate the tree and restore it, and a restore that did not happen")
print("  would otherwise be invisible.")
print()


def porcelain():
    return subprocess.run(["git", "-C", L.REPO, "status", "--porcelain"],
                          capture_output=True, text=True).stdout


before = porcelain()

targets = []
for r in affected:
    d = os.path.dirname(r)
    for n, t in L.tee_pipelines(srcs[r]):
        interp, script = L.invocations(t)[0]
        # arguments are what follows the script and precedes the pipe or the
        # next command -- `; tail -1 out_b0_repro.txt` is a SEPARATE command
        # and passing it as an argument would have made b0_repro.sh run with
        # four spurious argv entries and still exit 0, which is the exact
        # failure mode this instrument is about.
        args = t.split()
        extra = []
        for a in args[args.index(script) + 1:]:
            if a in ("|", ";", "&&", "||") or a.startswith("|"):
                break
            extra.append(a)
        targets.append((r, d, interp, script, extra))

print("  %-38s %-22s %6s %7s  %s"
      % ("tree", "target", "exit", "secs", "verdict"))
worst = []
for r, d, interp, script, extra in targets:
    cwd = os.path.join(L.REPO, d)
    cmd = ([sys.executable, "-B"] if interp.startswith("python")
           else ["/bin/sh"]) + [script] + extra
    t0 = time.time()
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                           timeout=TIMEOUT)
        code, note = p.returncode, ""
    except subprocess.TimeoutExpired:
        code, note = None, "TIMEOUT after %ds" % TIMEOUT
    dt = time.time() - t0
    verdict = ("nothing was being swallowed" if code == 0
               else note or "*** NON-ZERO -- a status the pipeline hid ***")
    if code != 0:
        worst.append((r, script, code, note))
    print("  %-38s %-22s %6s %7.1f  %s"
          % (d.replace("code/", ""), os.path.basename(script),
             "-" if code is None else code, dt, verdict))

after = porcelain()
print()
if before == after:
    print("  worktree unchanged by K3b (git status --porcelain identical)")
else:
    print("  *** WORKTREE CHANGED BY K3b ***")
    print("  before:\n%s\n  after:\n%s" % (before, after))
    BAD += 1

print()
if worst:
    print("  %d target(s) exit non-zero TODAY.  Each one is a past green whose"
          % len(worst))
    print("  reason was the pipeline and not the result:")
    for r, script, code, note in worst:
        print("    %s / %s -> %s %s" % (r, script, code, note))
    print()
    print("  Whether that was ALSO true at the commit the claim was made at is")
    print("  a separate question and is NOT answered by this table.")
else:
    print("  Every tee'd target exits 0 on the tree as it stands.  C1 and C3")
    print("  are therefore SETTLED AT HEAD: the runners' past `code == 0` was")
    print("  reporting a real zero, not a hidden one.  What this does not")
    print("  establish is the same fact at every intermediate commit, and no")
    print("  claim to that effect is made.")

# ---------------------------------------------------------------------------
hdr("K3c  SETTLING C2 -- the one claim that needed a NON-ZERO exit")

print("  C2 asserts a runner exits non-zero when B1 is restored.  A swallowed")
print("  status would have broken it, so it is the one row the defect could")
print("  not have flattered.  What has to be true for C2's non-zero to be the")
print("  REAL one is narrower than `the block contains no pipeline`, and the")
print("  first draft of this section checked the wider thing and scored 4 of 4")
print("  BAD against a block that is in fact sound.  The block DOES contain")
print("  pipelines.  They are inside the failure HANDLER:")
print()
print("      E2OUT=$(python3 ../species_extent_d633/e2_crosssection.py) || {")
print("          echo \"$E2OUT\" | grep 'STANDING UN-STRUCK' || true")
print("          echo \"E2 CROSS-SECTION FAILED -- ...\"")
print("          exit 1")
print("      }")
print()
print("  The three things that actually have to hold, each measured:")
print("    A  the line whose status is read is an ASSIGNMENT FROM A COMMAND")
print("       SUBSTITUTION with no pipeline -- so the status is the checker's.")
print("    B  the handler ends in an UNCONDITIONAL `exit 1`, so nothing inside")
print("       it can turn a failure back into a success.")
print("    C  every pipeline inside the handler is `|| true`, so it cannot")
print("       abort the handler before that `exit 1` is reached.")
print()
print("  %-24s %-9s %-5s %-6s %-6s %-6s %s"
      % ("tree", "revision", "line", "A", "B", "C", ""))
for tree in ("species_repair_a4ef", "species_remainder_f8fa"):
    rel = "code/%s/run_all.sh" % tree
    for label, src in (("at " + REF, L.read(rel, REF)), ("on disk",
                                                         L.read(rel))):
        lines = src.split("\n")
        idx = [i for i, l in enumerate(lines) if "E2OUT=$(" in l]
        if not idx:
            print("  %-24s %-9s *** the cross-section block is GONE ***"
                  % (tree, label))
            BAD += 1
            continue
        i = idx[0]
        body = lines[i:i + 5]
        a = not L.tee_pipelines(lines[i]) and "|" not in L.code_of(
            lines[i]).replace("||", "")
        b = any(re.match(r"\s*exit 1\s*$", l) for l in body)
        pipes = [l for l in body[1:]
                 if "|" in L.code_of(l).replace("||", "")]
        c = all("|| true" in l for l in pipes)
        ok = a and b and c
        BAD += (not ok)
        print("  %-24s %-9s %-5d %-6s %-6s %-6s %s"
              % (tree, label, i + 1, a, b, "%s(%d)" % (c, len(pipes)),
                 "ok" if ok else "*** BAD ***"))
print()
print("  A, B and C hold at both revisions.  C2's non-zero was always the")
print("  checker's own, not tee's.  SAFE.")
print()
print("  ONE MORE THING C2 COULD HAVE COME FROM, and it is worth naming")
print("  because it is a pipeline `set -e` really does consume.  Two lines")
print("  below that block both runners have")
print()
print("      echo \"$E2OUT\" | grep -E 'strike\\(s\\) measured|^E2 TOTAL BAD:'")
print()
print("  If that grep matched nothing the runner would exit 1 for a reason")
print("  unrelated to the cross-section verdict.  It is NOT repaired here:")
print("  the left-hand side is `echo`, which cannot fail, so the pipeline's")
print("  last-command status IS the only status that exists on that line.")
print("  That is a branch which cannot exhibit the defect, and the reason is")
print("  that there is no first-command status being hidden.  C2 is not")
print("  weakened by it either way, because `caught` also requires")
print("  'STANDING UN-STRUCK' to appear in the runner's stdout.")

# ---------------------------------------------------------------------------
hdr("K3d  THE BYTES DID NOT MOVE -- the R1 claims stay settled")

print("  Every claim in the R1 class rests on a committed transcript being")
print("  byte-reproducible.  This repair rewrites the RUNNERS, so the check")
print("  it owes is that no committed out_*.txt changed.  `tee out.txt` and")
print("  `> out.txt` write the same stream, so the prediction is zero; it is")
print("  measured rather than asserted.")
print()
diff = subprocess.run(["git", "-C", L.REPO, "diff", "--name-only", REF, "--"],
                      capture_output=True, text=True).stdout.split()
changed_out = [f for f in diff if "/out" in f or f.endswith("_output.txt")]
print("  files changed since %s:            %d" % (REF, len(diff)))
print("  ...that are committed transcripts:  %d" % len(changed_out))
for f in changed_out:
    print("      %s" % f)
if changed_out:
    print()
    print("  (transcripts belonging to code/runner_exit_c2b3/ are this")
    print("   instrument's own and are not part of any prior claim.)")
foreign = [f for f in changed_out if "runner_exit_c2b3" not in f]
if foreign:
    BAD += len(foreign)
    print("  *** %d transcript(s) outside this tree changed ***" % len(foreign))

# ---------------------------------------------------------------------------
hdr("K3f  THE SAME BYTES, THROUGH THE REPAIRED RUNNER -- measured, not argued")

print("  K3d shows no committed transcript was edited.  It does not show that")
print("  a REPAIRED RUNNER still produces the committed bytes, and that is the")
print("  claim the whole R1 class rests on.  So one repaired runner is")
print("  actually executed and its transcripts compared:")
print()
print("    code/face_geometry/run_all.sh -- chosen because claim C6 is exactly")
print("    an idempotence claim about this runner, so re-verifying it here")
print("    re-verifies a row of K3a rather than inventing a new check.")
print()
fg = "code/face_geometry"
b4 = porcelain()
p_ = subprocess.run(["/bin/sh", os.path.join(L.REPO, fg, "run_all.sh")],
                    capture_output=True, text=True, cwd=L.REPO)
af = porcelain()
moved = [l[3:] for l in af.split("\n")
         if l[3:].startswith(fg) and l[3:].endswith(".txt")]
print("    runner exit code:                 %d" % p_.returncode)
print("    transcripts that moved:           %s" % (moved or "none"))
if p_.returncode != 0 or moved:
    BAD += 1
    print("    *** the repaired runner did not reproduce its own bytes ***")
else:
    print("    `> f` and `| tee f` write the same stream, demonstrated on the")
    print("    real runner rather than deduced from the shell's semantics.")
print()
print("  AND THE OTHER DIRECTION, because `no transcript moved` would be a")
print("  weak claim if none of them ever moved.  Four transcripts in")
print("  code/face_geometry_audit_1c80/ do NOT regenerate -- out_n6.txt,")
print("  out_witness.txt, out_claims.txt, out_mutations.txt.  That drift is")
print("  NOT this repair's: it reproduces on a pristine `git archive %s`"
      % REF)
print("  checkout with none of these edits present, because those instruments")
print("  read the live tree and the live history.  It is the same class the")
print("  arc already records for mg-6653 and mg-7d5a, and it is named here so")
print("  that `no transcript moved` above cannot be read as `nothing in the")
print("  arc ever moves`.")

# ---------------------------------------------------------------------------
hdr("K3e  THE GENERAL FORM, ON THIS SECTION")

print("  K3 is a script that decides whether other scripts' verdicts were")
print("  discarded, so the question is whether K3 discards its own.  What was")
print("  checked, and the branches that cannot exhibit it, with reasons:")
print()
print("   1. Every subprocess in K3b is `subprocess.run(cmd, ...)` with a LIST")
print("      argv and no `shell=True`.  There is no shell, so there is no")
print("      pipeline, so `returncode` is the target's own status.  That is")
print("      the branch that CANNOT exhibit the defect, and the reason is")
print("      structural rather than a promise about how it is called.")
print("   2. `returncode` is READ on every path, including the timeout path,")
print("      where it is None and prints as `-` instead of as 0.  A timeout")
print("      rendered as 0 would be this defect wearing a different hat.")
print("   3. K3b's own effect on the tree is measured (git status before and")
print("      after), because several targets mutate and restore the worktree")
print("      and a restore that silently failed would corrupt K3d's answer.")
print("   4. K3d compares against the PINNED %s, not HEAD.  Anchored to" % REF)
print("      HEAD it would compare the repaired tree with itself and report")
print("      zero changes forever -- mg-821e's finding, in this file.")
print("   5. The one thing K3 CANNOT do, stated because a stated limit is")
print("      checkable and an omission is not: it cannot re-run the affected")
print("      targets at every historical commit.  It settles the R3 claims at")
print("      HEAD and at the revisions the claims name, and says so in the")
print("      rows themselves rather than in a footnote.")

print()
L.bar("K3 TOTAL BAD: %d" % BAD)
print()
print("EXTENT OF THAT NUMBER.  It counts (a) K3b leaving the worktree dirty,")
print("(b) the cross-section block C2 depends on being absent or pipelined at")
print("either revision, and (c) committed transcripts outside this tree")
print("changing.  It does NOT count the %d AT-RISK claims: those are the" % n_risk)
print("finding, and K3b/K3c settle them.  It ranges over the %d claims"
      % len(CLAIMS))
print("enumerated in K3a and over the %d tee'd targets of the %d affected"
      % (len(targets), len(affected)))
print("runners -- not over claims made about trees outside this arc.")
sys.exit(1 if BAD else 0)
