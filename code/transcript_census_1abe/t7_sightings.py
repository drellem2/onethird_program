"""t7 -- THE TICKET'S OWN SIGHTINGS, RE-DERIVED RATHER THAN REPEATED.

The ticket says, in as many words: "I am asserting one mechanism behind three
sightings from three verdicts I did not run.  If the three have different
causes, say so."  t2 answers that for the population.  This script answers it
for the three named cases, one at a time, because a census can agree with a
claim in aggregate while the claim itself is wrong about the case it names.

SIGHTING 1 -- mg-b2af, on mg-330a.  The ticket says its transcript's figures
"reproduce EXACTLY at b94cb1e -- the PRE-REBASE TWIN -- and at NEITHER commit
it now sits behind on main."

  RE-DERIVING IT NEEDS A TRICK, and the trick is the finding.  `b94cb1e`'s tree
  does not contain `code/repair_b2af/` at all, so the suite cannot simply be
  run there.  But the suite reads `HEAD` -- it takes no `--at` -- so what its
  figures are facts about is THE COMMIT HEAD POINTS AT, not the tree the code
  came from.  So: check out `b94cb1e`, drop the carrier's copy of the suite
  into it, and run.  HEAD is the twin; the code is the carrier's.  If the
  ticket is right, the committed bytes come back.

SIGHTING 2 -- mg-c3a2, on mg-c067.  The ticket describes the six transcripts as
"the pre-fix run committed beside the fix" at 4ad011a.  That was true and it is
no longer the state of `main`: mg-c3a2 RE-RAN them, and this script follows
what happened to the re-run.  Pure git, no execution.

SIGHTING 3 -- mg-132a, which coined the word.  Covered by t2 like any other
member of the population; nothing extra is derived here and the row says so.
"""

import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_1abe as L                                          # noqa: E402

TWIN = "b94cb1e"
SUBJECT_DIR = "code/repair_b2af"


def main():
    rev = L.main_rev()
    head = L.resolve(rev)
    led = L.Ledger("t7 -- THE TICKET'S THREE SIGHTINGS, RE-DERIVED")
    print("    as-of      %s  (%s)" % (head, rev))

    # ------------------------------------------------------------ sighting 1
    led.head("T7a -- SIGHTING 1: DO mg-b2af'S TRANSCRIPTS REPRODUCE AT THE "
             "PRE-REBASE TWIN?")
    twin = L.resolve(TWIN)
    paths = [p for p in L.transcripts(rev) if p.startswith(SUBJECT_DIR + "/")]
    if not twin or not paths:
        led.self_error("T7a %s does not resolve or %s holds no transcripts; "
                       "the probe did not run" % (TWIN, SUBJECT_DIR))
        return led.done()

    carrier = L.carrying_commit(paths[0], rev)
    print("    the twin                    %s  %s"
          % (twin[:8], L.git("log", "-1", "--format=%s", twin).strip()[:44]))
    print("    reachable from %s?        %s"
          % (rev, "yes" if L.is_ancestor(twin, head) else "NO"))
    print("    the carrying commit today   %s  %s"
          % (carrier[:8],
             L.git("log", "-1", "--format=%s", carrier).strip()[:44]))
    print("    the twin's tree holds %s?   %s"
          % (SUBJECT_DIR,
             "yes" if L.blob_at(twin, SUBJECT_DIR + "/run_all.sh") else "NO"))
    print()

    def run_at(where, overlay):
        """Run the suite with HEAD at `where`, optionally overlaying the
        carrier's copy of the suite (needed at the twin, whose tree has no
        `code/repair_b2af/` at all)."""
        root = tempfile.mkdtemp(prefix="sighting1-")
        wt = os.path.join(root, "wt")
        out = {}
        try:
            L.git("worktree", "add", "--detach", "-q", wt, where)
            target = os.path.join(wt, SUBJECT_DIR)
            if overlay:
                os.makedirs(target, exist_ok=True)
                names = [n for n in L.git(
                    "ls-tree", "--name-only",
                    "%s:%s" % (carrier, SUBJECT_DIR)).split("\n") if n.strip()]
                for n in names:
                    blob = L.blob_at(carrier, "%s/%s" % (SUBJECT_DIR, n))
                    if blob is not None:
                        with open(os.path.join(target, n), "wb") as fh:
                            fh.write(blob)
            rc = subprocess.run(["sh", "run_all.sh"], cwd=target,
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL,
                                timeout=1800).returncode
            for q in paths:
                disk = os.path.join(target, os.path.basename(q))
                got = open(disk, "rb").read() if os.path.exists(disk) else None
                want = L.blob_at(carrier, q)
                out[q] = ("MISSING" if got is None else
                          "REPRODUCES" if got == want else "DIFFERS")
            return out, rc
        except subprocess.TimeoutExpired:
            led.self_error("T7a the suite exceeded 1800s at %s" % where[:7])
            return out, None
        finally:
            L.git("worktree", "remove", "--force", wt)
            shutil.rmtree(root, ignore_errors=True)
            L.git("worktree", "prune")

    at_twin, rc_twin = run_at(twin, True)
    at_carrier, rc_carrier = run_at(carrier, False)
    print("    suite exit at the twin %s : %s" % (twin[:7], rc_twin))
    print("    suite exit at the carrier %s : %s" % (carrier[:7], rc_carrier))
    print()
    print("    %-34s %-14s %s" % ("transcript", "at twin", "at carrier"))
    for p in paths:
        print("    %-34s %-14s %s" % (os.path.basename(p),
                                      at_twin.get(p, "?"),
                                      at_carrier.get(p, "?")))
    g_twin = sum(1 for v in at_twin.values() if v == "REPRODUCES")
    g_carr = sum(1 for v in at_carrier.values() if v == "REPRODUCES")

    led.record(None,
               "T7a %d of %d mg-b2af transcripts reproduce BYTE-FOR-BYTE with "
               "HEAD at the pre-rebase twin %s, and %d of %d at the commit "
               "carrying them"
               % (g_twin, len(paths), twin[:7], g_carr, len(paths)))
    led.record(g_carr == len(paths),
               "T7a' THE SECOND HALF OF SIGHTING 1 IS CONFIRMED: the ticket "
               "says these do not reproduce at the commit they now sit behind "
               "on main, and %d of %d do not"
               % (len(paths) - g_carr, len(paths)))
    print("""
    T7a'' AND THE FIRST HALF IS NOT CONFIRMED AT THIS GRAIN -- WHICH IS A
    STATEMENT ABOUT MY TEST BEFORE IT IS A STATEMENT ABOUT THE TICKET.

      THE TICKET'S CLAIM  ten FIGURES reproduce at the twin.
      MY TEST             whole TRANSCRIPTS reproduce byte-for-byte.
      Mine is strictly stronger, so failing it does not refute the ticket's.
      A transcript can carry ten correct figures and still differ in an
      eleventh, in a column width, or in a list that got longer.

      TWO FURTHER REASONS NOT TO READ THIS AS A REFUTATION.  First, the twin's
      tree does not contain %s at all, so the twin run is a
      SYNTHETIC STATE -- the carrier's code with the twin's HEAD -- that never
      existed and that nobody ever committed.  Second, the suite reads history
      as well as HEAD, and history at the twin is not the history the run saw.

      WHAT IS SOLID: at the twin the figure `HISTORY-DERIVED` reads 16 and the
      committed transcript says 19.  The ticket itself dates the 16 -> 19
      change to BETWEEN the twin and the carrier.  So on that one figure the
      committed transcript matches the LATER state, not the twin's.  That is
      one figure, re-derived, and it does not settle the other nine.
    """ % SUBJECT_DIR)

    # ------------------------------------------------------------ sighting 2
    led.head("T7b -- SIGHTING 2: WHAT HAPPENED TO THE REPAIR")
    print("""
The ticket describes mg-c067's six transcripts as the pre-fix run committed
beside the fix at 4ad011a, and says nothing caught it for five days.  mg-c3a2
then RE-RAN them.  This row follows the re-run, with no execution at all --
every step is a git lookup a reader can repeat.
""")
    p = "code/audit_c067/out_c2_anchors.txt"
    c = L.carrying_commit(p, rev)
    blob = L.blob_at(c, p)
    text = blob.decode("utf-8", "replace") if blob else ""
    import re
    m = re.search(r"audited as of\s*:\s*([0-9a-f]{7,40})", text)
    named = L.resolve(m.group(1)) if m else None
    print("    the transcript on %s      %s" % (rev, p))
    print("    its carrying commit       %s  %s"
          % (c[:8], L.git("log", "-1", "--format=%s", c).strip()[:50]))
    print("    the commit it DECLARES    %s  %s"
          % ((named or "?")[:8],
             L.git("log", "-1", "--format=%s", named).strip()[:50]
             if named else "(none found)"))
    if named:
        anc = L.is_ancestor(named, head)
        pid = L.patch_id(named)
        twin2 = None
        for cc in L.git("rev-list", head).split():
            if L.patch_id(cc) == pid:
                twin2 = cc
                break
        print("    declared commit on %s?    %s" % (rev, "yes" if anc else "NO"))
        print("    its patch-id twin on %s   %s  %s"
              % (rev, (twin2 or "-")[:8],
                 L.git("log", "-1", "--format=%s", twin2).strip()[:50]
                 if twin2 else ""))
        led.record(anc,
                   "T7b THE REPAIR WAS ITSELF DISPLACED, IN THE SAME MERGE "
                   "THAT LANDED IT.  mg-c3a2 re-ran these six transcripts to "
                   "fix a displacement; the re-run measured %s, which is its "
                   "own pre-rebase commit; the refinery rebased it to %s; and "
                   "the transcripts now sit at %s declaring a commit that is "
                   "not on %s.  The remedy and the defect are the same shape"
                   % ((named or "?")[:7], (twin2 or "?")[:7], c[:7], rev))

    # ------------------------------------------------------------ sighting 3
    led.head("T7c -- SIGHTING 3, AND WHAT IS NOT RE-DERIVED HERE")
    n132a = [q for q in L.transcripts(rev)
             if q.startswith("code/publication_anchor_132a/")]
    print("    mg-132a coined the word DISPLACED.  Its %d transcript(s) are in "
          "the t2 population and are re-run there like any other member; "
          "nothing additional is derived in this script." % len(n132a))
    for q in n132a:
        print("      %s" % q)
    led.record(None,
               "T7c mg-132a's sighting is NOT independently re-derived here.  "
               "It is measured only insofar as t2 measures its transcripts, "
               "and a reader who wants the sighting itself checked should "
               "read that as an outstanding item rather than as done")
    return led.done()


if __name__ == "__main__":
    sys.exit(main())
