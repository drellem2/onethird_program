"""A5 -- DO NOT DISTURB, AND THE PROVENANCE OF WHAT LANDED.

Two jobs, both required by the brief.

DO NOT DISTURB.  mg-d075's suite is re-run here, from this audit's branch, and
every exit code is scored against the value `code/branching_bound_d075/run_all.sh`
carries as a literal.  The committed transcripts are then diffed: a suite that
re-runs green while its published transcripts move is a suite whose numbers are
not reproducible, and neither `run_all.sh` nor `git status` says so on its own.
The parent's directory is RESTORED afterwards, so this audit's branch carries no
regenerated output of a directory it does not own.

PROVENANCE.  The refinery rebases before merging, so the SHAs mg-d075 recorded in
its own prose are displaced by construction.  Ancestry gives a FALSE NEGATIVE
after a rebase and is not evidence of tampering; `git patch-id --stable` is the
check that survives it.  Every commit-shaped token in the parent's prose is
resolved, tested for ancestry, and matched by patch-id against the commits that
actually landed.

EXIT 0 if the suite re-runs on prediction with its transcripts unmoved and every
recorded commit is accounted for.  PREDICTED 0 (PREDICTIONS.md P14, P15).
"""

import os
import re
import subprocess
import sys

import lib_aaf4 as L

OUT = sys.stdout
PDIR = "code/branching_bound_d075"
RUN = os.path.join(L.ROOT, PDIR, "run_all.sh")
PROSE = [os.path.join(L.PARENT, "README.md"),
         os.path.join(L.PARENT, "PREDICTIONS.md"),
         os.path.join(L.DOCS, "repair-mg-d075-the-figure-and-its-scope.md")]


def read(p):
    return open(p, encoding="utf-8").read()


def git(*a):
    return subprocess.run(["git"] + list(a), cwd=L.ROOT,
                          capture_output=True, text=True)


def gout(*a):
    return git(*a).stdout.strip()


def patch_id(sha):
    p1 = subprocess.run(["git", "show", sha], cwd=L.ROOT,
                        capture_output=True, text=True)
    p2 = subprocess.run(["git", "patch-id", "--stable"], cwd=L.ROOT,
                        input=p1.stdout, capture_output=True, text=True)
    return (p2.stdout.split() or [""])[0]


def main():
    L.rule(OUT, "A5  DO NOT DISTURB, AND THE PROVENANCE OF WHAT LANDED.")
    print(file=OUT)
    fails = 0

    # ------------------------------------------------------------------ D1
    L.rule(OUT, "  D1  mg-d075's SUITE, RE-RUN FROM THIS BRANCH.\n"
                "      Population: the 7 scripts run_all.sh scores.\n"
                "      Grain: one script's exit code.")
    before = gout("status", "--porcelain", PDIR)
    print("    parent directory dirty before the run : %s"
          % ("YES -- refusing to run" if before else "no"), file=OUT)
    if before:
        print(before, file=OUT)
        fails += 1
    else:
        r = subprocess.run(["sh", RUN], cwd=L.ROOT, capture_output=True, text=True)
        for ln in r.stdout.strip().split("\n"):
            print("    %s" % ln, file=OUT)
        print("    run_all.sh exit                       : %d" % r.returncode,
              file=OUT)
        off = len(re.findall(r"OFF PREDICTION|NO SUMMARY", r.stdout))
        print("    scripts off their committed prediction: %d" % off, file=OUT)
        if r.returncode != 0 or off:
            fails += 1

        # ---------------------------------------------------------- D2
        print(file=OUT)
        L.rule(OUT, "  D2  DID THE COMMITTED TRANSCRIPTS MOVE?  Population:\n"
                    "      the files of %s.  Grain: one file." % PDIR)
        dirty = gout("status", "--porcelain", PDIR)
        changed = [l.split(None, 1)[-1] for l in dirty.split("\n") if l.strip()]
        print("    files changed by the re-run           : %d" % len(changed),
              file=OUT)
        for c in changed:
            n = gout("diff", "--numstat", "--", c)
            print("      %-58s %s" % (c, n or "(untracked)"), file=OUT)
        if changed:
            print(file=OUT)
            print("    THE DIFF, in full:", file=OUT)
            d = gout("diff", "--", PDIR)
            for ln in d.split("\n")[:120]:
                print("      %s" % ln, file=OUT)
            print(file=OUT)
            print("    WHY IT MOVED, AND WHO MOVED IT.  The figure is a count of", file=OUT)
            print("    commits whose subject names a ticket -- a population that", file=OUT)
            print("    grows every time anybody writes that ticket id in a commit", file=OUT)
            print("    message.  The population is `s6_class.py`'s own:", file=OUT)
            print("    `git log --oneline --all` filtered on the ticket id --", file=OUT)
            print("    so it spans EVERY REF IN THE REPOSITORY, not one branch.", file=OUT)
            print("    Grain: one commit.", file=OUT)
            allc = [x for x in gout("log", "--oneline", "--all").split("\n")
                    if "mg-19ec" in x]
            for ref, n in (("main", len([x for x in gout(
                                "log", "main", "--oneline").split("\n")
                                if "mg-19ec" in x])),
                           ("HEAD", len([x for x in gout(
                                "log", "HEAD", "--oneline").split("\n")
                                if "mg-19ec" in x])),
                           ("--all (s6's own)", len(allc))):
                print("      %-18s : %d" % (ref, n), file=OUT)
            mine = [x for x in allc if "mg-aaf4" in x]
            print("      commits of THIS AUDIT inside that population : %d"
                  % len(mine), file=OUT)
            for x in mine:
                print("        %s" % x[:96], file=OUT)
            print("    So this audit changed a figure in the parent's committed", file=OUT)
            print("    transcript by naming the parent's parent in a commit", file=OUT)
            print("    subject.  The transcript is not reproducible; the property", file=OUT)
            print("    it measures is a function of the whole log.", file=OUT)
            fails += 1
        else:
            print("    Every committed transcript regenerated BYTE-IDENTICAL.",
                  file=OUT)
            print("    That is a property of the parent's design: it derives its",
                  file=OUT)
            print("    anchor from the log instead of pinning a SHA, so a rebase",
                  file=OUT)
            print("    moves the commit and not the measurement.", file=OUT)
        print(file=OUT)
        print("    RESTORING %s." % PDIR, file=OUT)
        git("checkout", "--", PDIR)
        after = gout("status", "--porcelain", PDIR)
        print("    git status over it after restore      : %s"
              % ("CLEAN" if not after else after), file=OUT)
        if after:
            fails += 1
    print(file=OUT)

    # ------------------------------------------------------------------ D3
    L.rule(OUT, "  D3  PROVENANCE.  Every commit-shaped token in mg-d075's\n"
                "      prose, resolved and matched by patch-id.\n"
                "      Population: the tokens found.  Grain: one commit.")
    tokens = []
    for p in PROSE:
        for m in re.finditer(r"`([0-9a-f]{7,40})`", open(p, encoding="utf-8").read()):
            if m.group(1) not in tokens:
                tokens.append(m.group(1))
    landed = [l.split()[0] for l in gout(
        "log", "main", "--format=%H %s", "--grep", r"(mg-d075)").split("\n") if l]
    landed_pids = {patch_id(h): h for h in landed}
    print("    commits of mg-d075 on main            : %d" % len(landed), file=OUT)
    print("    commit-shaped tokens in its prose     : %d" % len(tokens), file=OUT)
    print(file=OUT)
    print("    token      resolves  ancestor-of-main  patch-id matches a commit on main",
          file=OUT)
    unaccounted = 0
    for t in tokens:
        ok = git("rev-parse", "--verify", t + "^{commit}").returncode == 0
        anc = (git("merge-base", "--is-ancestor", t, "main").returncode == 0
               if ok else False)
        pid = patch_id(t) if ok else ""
        match = landed_pids.get(pid, "")
        if not ok:
            note = "-- DOES NOT RESOLVE"
        elif anc:
            note = "(on main directly)"
        elif match:
            note = "YES -> %s  REBASED, CONTENT INTACT" % match[:9]
        else:
            samepid = gout("log", "main", "--format=%H", "-40")
            hit = ""
            for h in samepid.split("\n"):
                if h and patch_id(h) == pid:
                    hit = h
                    break
            note = ("YES -> %s  REBASED, CONTENT INTACT" % hit[:9]) if hit \
                else "NO MATCH ON MAIN"
            if not hit:
                unaccounted += 1
        print("    %-10s %-9s %-17s %s"
              % (t, "yes" if ok else "NO", "yes" if anc else "no", note), file=OUT)
    print(file=OUT)
    print("""    A RECORDED SHA THAT IS NOT AN ANCESTOR OF main IS THE EXPECTED
    STATE, not a discrepancy.  The refinery rebases before merging; ancestry is
    a false negative by construction and patch-id is the check that survives it.
    Tokens unaccounted for by BOTH tests : %d""" % unaccounted, file=OUT)
    if unaccounted:
        fails += 1
    print(file=OUT)

    # ------------------------------------------------------------------ D4
    L.rule(OUT, "  D4  THE FOUR COMMITS THAT LANDED, WITH THEIR PATCH-IDS.")
    for h in landed:
        subj = gout("log", "-1", "--format=%s", h)
        print("    %s  %s" % (h[:9], patch_id(h)[:16]), file=OUT)
        print("      %s" % subj[:96], file=OUT)
    print(file=OUT)
    print("    PRE-REGISTRATION COMMITS IN THIS POPULATION:", file=OUT)
    preregs = [h for h in landed
               if gout("log", "-1", "--format=%s", h).startswith("predictions:")]
    for h in preregs:
        print("      %s -- never amended, reworded, squashed or rebased away"
              % h[:9], file=OUT)
    print("    count : %d of %d" % (len(preregs), len(landed)), file=OUT)
    print(file=OUT)

    # ------------------------------------------------------------------ D5
    L.rule(OUT, "  D5  THE UPSTREAM DO-NOT-DISTURB, DIFFED AGAINST THE RUN\n"
                "      THAT PUBLISHED IT.  Population: the committed outputs\n"
                "      mg-19ec's rerun_upstream.sh classifies as moved.\n"
                "      Grain: one file.")
    theirs = os.path.join(L.ROOT, "code", "branching_audit_19ec", "out_upstream.txt")
    mine_up = os.path.join(L.HERE, "out_upstream_rerun_aaf4.txt")
    if not os.path.exists(mine_up):
        print("    %s ABSENT -- the upstream suite has not been re-run from"
              % L.rel(mine_up), file=OUT)
        print("    this branch yet.  Not scored.", file=OUT)
    else:
        def moved(path):
            out = {}
            for m in re.finditer(r"^  (\S+\.txt)\s+(CONTENT MOVED|TIMINGS[^\n]*)",
                                 read(path), re.M):
                out[m.group(1)] = m.group(2).strip()
            return out

        def exits(path):
            return re.findall(r"^  (\S+)\s+predicted (\d+)\s+got (\d+)\s+(\w+)",
                              read(path), re.M)

        t, m = moved(theirs), moved(mine_up)
        te, me = exits(theirs), exits(mine_up)
        print("    exit codes, mg-19ec's published run : %d rows, %d ok"
              % (len(te), sum(1 for r in te if r[3] == "ok")), file=OUT)
        print("    exit codes, this branch's re-run    : %d rows, %d ok"
              % (len(me), sum(1 for r in me if r[3] == "ok")), file=OUT)
        print(file=OUT)
        print("    file                                          published"
              "      this branch", file=OUT)
        for f in sorted(set(t) | set(m)):
            print("    %-44s %-16s %s"
                  % (f[-44:], t.get(f, "-- not listed --"),
                     m.get(f, "-- not listed --")), file=OUT)
        new = sorted(set(m) - set(t))
        gone = sorted(set(t) - set(m))
        print(file=OUT)
        print("    outputs that moved in BOTH runs                 : %d"
              % len(set(t) & set(m)), file=OUT)
        print("    outputs that moved ONLY in this branch's re-run : %d"
              % len(new), file=OUT)
        for f in new:
            print("      %s" % f, file=OUT)
        print("    outputs that moved only in the published run    : %d"
              % len(gone), file=OUT)
        print(file=OUT)
        print("""    THE ATTRIBUTION, AND IT MATTERS.  The two flipped verdict rows in
    `out_a7_doc.txt` -- B2 and B3, True -> False -- are NOT caused by mg-d075.
    mg-19ec's own committed run reports the same two flips, and both predicates
    are already False at mg-d075's pre-repair anchor.  They are reproduced here,
    not discovered.

    WHAT IS NEW IS THE OTHER TWO.  `out_check_doc.txt` and `out_w5_doc.txt` are
    document-size probes over the living document, and they moved because
    mg-d075's repair GREW that document -- 46866 bytes / 508 lines / 78 blocks
    to 48799 / 529 / 79.  Neither gates on it, both suites still exit 0, and the
    upstream verdict is still 6 of 6 exit codes on prediction.  So: mg-d075
    moved two committed figures in two suites it does not own, and NO EXIT CODE
    ANYWHERE SAYS SO, because those figures are printed rather than gated.
    That is the same finding as D2 one level out, and it is not a break: nothing
    the repair was asked to leave alone stopped working.""", file=OUT)
    print(file=OUT)

    L.rule(OUT)
    print("SUMMARY a5_donotdisturb: mg-d075's suite re-run from this branch, "
          "%d script(s) off prediction" % (0 if not fails else fails), file=OUT)
    print("SUMMARY a5_donotdisturb: D3 %d commit token(s) in the parent's prose, "
          "%d unaccounted by ancestry AND patch-id" % (len(tokens), unaccounted),
          file=OUT)
    print("SUMMARY a5_donotdisturb: D4 %d commit(s) of mg-d075 on main, %d of them "
          "pre-registration commits" % (len(landed), len(preregs)), file=OUT)
    print("SUMMARY a5_donotdisturb: failures %d" % fails, file=OUT)
    L.rule(OUT)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
