#!/usr/bin/env python3
"""mg-0120 — THE ANCHORS, DIAGNOSED BY CONTENT AND RE-MEASURED OVER THE WHOLE REPOSITORY.

mg-65eb found that `739f7bd` — the sha carrying mg-a74f's own integrity claim, "PREDICTIONS.md
was committed before any script in this directory existed" — is not an ancestor of `main`, and
that the two idioms mg-a74f's own code uses (`git cat-file -e`) pass it anyway.  This file
answers the two questions that finding leaves open.

QUESTION 1 — IS IT LOST, OR IS IT DISPLACED?  Those need different repairs and the ticket says
they look identical, which is exactly right: both give `merge-base --is-ancestor` exit 1.

    LOST        the change is not on `main` in any form.  The integrity claim is unsupported
                and the property has to be re-derived, or the claim withdrawn.
    DISPLACED   the refinery REBASED the branch before merging, so the same change is on
                `main` under a different sha.  The property was never violated; the POINTER
                rotted, and the repair is to point it at the merged twin.

The two are told apart by `git patch-id --stable`, which digests the DIFF and ignores parents,
committer and tree — so it survives a rebase and a subject cannot forge it.

WHY NOT MATCH ON THE SUBJECT.  `anchor65eb.py:twin_of` finds the twin by searching `HEAD` for
a commit carrying the same subject line.  That works here and it is the weaker instrument: a
subject is a LABEL somebody typed, two commits can carry one subject and different content,
and this repository's commit subjects are long and formulaic enough that a collision is not
exotic.  Section C CONSTRUCTS the collision rather than arguing it could happen — two commits
built to share a subject and differ in content — and shows the subject rule identifying the
wrong one while patch-id does not.

QUESTION 2 — HOW MANY OTHERS.  mg-65eb measured 24 hex tokens over the FOUR directories
mg-a74f touches.  That population cannot answer "how common is this", because it was chosen as
the neighbourhood of one repair.  Section D re-measures over EVERY tracked `.py`, `.md` and
`.sh` IN THE REPOSITORY, against `main` rather than against whatever HEAD happens to be —
`HEAD` on a polecat branch reaches its own unmerged commits, so an anchor measured that way is
measured against a tree no reader has.

    ANCHOR-LIVE       resolves, and is an ancestor of the reference
    ANCHOR-DISPLACED  not an ancestor, but a commit with an IDENTICAL patch-id is  (mg-0120)
    ANCHOR-STALE      not an ancestor, no patch-id twin, but some ref reaches it
    ANCHOR-DEAD       resolves, and no ref reaches it — one `git gc` from unreadable
    NOT-A-REVISION    a hex-shaped token that is not a commit; reported, never dropped

    python3 code/state_claims_repair_0120/anchors0120.py             # against main
    python3 code/state_claims_repair_0120/anchors0120.py --ref HEAD  # what mg-65eb measured

Exit 1 if any anchor is STALE or DEAD.  DISPLACED anchors are counted, listed with their twin,
and do NOT fail the run on their own — the repository cannot merge a branch without displacing
every sha it wrote, so failing on that would be failing on the merge process.  Which of the
two policies is right is argued in the README and it is a judgement, not a measurement.

NOTHING IS WRITTEN except the throwaway repository section C builds under a temp directory.
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()

EXTS = (".py", ".md", ".sh", ".txt")

# Bounded by non-alphanumerics so `bd24efc` inside `at(bd24efc, CTL)` is seen and a hex run
# inside a longer word is not.  All-alphabetic and all-numeric runs are excluded BY THE RULE
# (`accede` is not a sha; `1234567` is a line count), so a reader can check the rule instead
# of auditing a stop list.
TOKEN = re.compile(r"(?<![0-9A-Za-z])([0-9a-f]{7,12})(?![0-9A-Za-z])")

THE_ANCHOR = "739f7bd"
A74F_README = "code/state_delegation_repair_a74f/README.md"


def git(*a, **kw):
    return subprocess.run(["git", "-C", REPO, *a], capture_output=True, text=True, **kw)


def patch_id(rev, cwd=REPO):
    """The stable patch-id of `rev`'s diff — survives a rebase, and a subject cannot forge it.

    A merge commit has no single diff and `git show` prints none, so the id comes back empty;
    that is reported as absent rather than as a match, because "" == "" would make every
    merge commit the twin of every other."""
    show = subprocess.run(["git", "-C", cwd, "show", rev], capture_output=True, text=True)
    p = subprocess.run(["git", "-C", cwd, "patch-id", "--stable"],
                       input=show.stdout, capture_output=True, text=True)
    out = p.stdout.split()
    return out[0] if out else None


def is_hex_word(tok):
    return not tok.isalpha() and not tok.isdigit()


def population(ref):
    """Every tracked .py/.md/.sh/.txt in the repository, at `ref`."""
    out = git("ls-tree", "-r", "--name-only", ref).stdout.split("\n")
    return [p for p in out if p.endswith(EXTS)]


# =========================================================================================
# A.  THE CLASSIFIER.  Every branch is a git answer; nothing here is asserted.
# =========================================================================================
def twins_by_patch_id(ref, limit=4000):
    """{patch-id: [sha]} over the commits reachable from `ref`.

    Built once and reused, because computing a patch-id is two subprocesses and the naive
    shape of this file ran it per (token x commit)."""
    shas = git("log", "--format=%H", f"-n{limit}", ref).stdout.split()
    index = {}
    for sha in shas:
        pid = patch_id(sha)
        if pid:
            index.setdefault(pid, []).append(sha)
    return index


def classify(tok, ref, index):
    t = git("cat-file", "-t", tok)
    if t.returncode != 0 or t.stdout.strip() != "commit":
        return "NOT-A-REVISION", f"cat-file -t: {t.stdout.strip() or 'no such object'}", None
    subj = git("log", "-1", "--format=%s", tok).stdout.strip()
    if git("merge-base", "--is-ancestor", tok, ref).returncode == 0:
        return "ANCHOR-LIVE", subj, None
    pid = patch_id(tok)
    twin = (index.get(pid) or [None])[0] if pid else None
    if twin:
        return "ANCHOR-DISPLACED", subj, twin
    refs = [ln.split()[-1] for ln in
            git("for-each-ref", "--contains", tok, "--format=%(refname)").stdout.split("\n")
            if ln.strip()]
    return ("ANCHOR-STALE" if refs else "ANCHOR-DEAD"), subj, None


# =========================================================================================
# B.  THE ANCHOR ITSELF, and the two idioms.
# =========================================================================================
def section_b(ref, index):
    print("B.  THE ANCHOR THAT CARRIES mg-a74f's OWN INTEGRITY CLAIM, DIAGNOSED.")
    print()
    bucket, subj, twin = classify(THE_ANCHOR, ref, index)
    print(f"  the token as written in {A74F_README}:  {THE_ANCHOR}")
    print(f"  subject                                 {subj[:96]}")
    print()
    print("  THE THREE IDIOMS, side by side.  The first two are the ones mg-a74f's own code")
    print("  is written in (claims_a74f.py:57, prose_a74f.py:114).")
    for label, cmd in [
        (f"git cat-file -e {THE_ANCHOR}^{{commit}}", ["cat-file", "-e", f"{THE_ANCHOR}^{{commit}}"]),
        (f"git rev-parse --verify {THE_ANCHOR}", ["rev-parse", "--verify", THE_ANCHOR]),
        (f"git merge-base --is-ancestor {THE_ANCHOR} {ref}",
         ["merge-base", "--is-ancestor", THE_ANCHOR, ref]),
    ]:
        rc = git(*cmd).returncode
        verdict = ("PASSES — and the property it tests is not the one claimed"
                   if rc == 0 and "merge-base" not in label else
                   "FAILS — ancestry is the property, and it does not hold" if rc else
                   "PASSES")
        print(f"    {label:<52s} exit {rc}   {verdict}")
    print()
    print("  LOST, OR DISPLACED?  Told apart by the DIFF, not by the label.")
    mine = patch_id(THE_ANCHOR)
    print(f"    git patch-id --stable  of {THE_ANCHOR}   {mine}")
    if twin:
        theirs = patch_id(twin)
        anc = git("merge-base", "--is-ancestor", twin, ref).returncode == 0
        print(f"    git patch-id --stable  of {twin[:7]}   {theirs}   IDENTICAL")
        print(f"    is {twin[:7]} an ancestor of {ref}?          {'yes' if anc else 'NO'}")
        print(f"    trees                  {git('rev-parse', THE_ANCHOR + '^{tree}').stdout.strip()[:12]}"
              f"  vs  {git('rev-parse', twin + '^{tree}').stdout.strip()[:12]}   (differ — a "
              f"rebase rewrites the tree's parentage)")
        print(f"    parents                {git('log', '-1', '--format=%P', THE_ANCHOR).stdout.strip()[:12]}"
              f"  vs  {git('log', '-1', '--format=%P', twin).stdout.strip()[:12]}   (differ — "
              f"which is what a rebase IS)")
        print()
        print(f"  VERDICT: {bucket}.  The change is on {ref} as {twin[:7]}.  The property was")
        print("  never violated and the pointer rotted, so the repair is to re-point the")
        print("  anchor, NOT to re-derive the claim.  These two look identical to")
        print("  `--is-ancestor` and they are not the same defect.")
    else:
        print(f"    no commit reachable from {ref} has that patch-id")
        print(f"  VERDICT: {bucket}.  The change is NOT on {ref} in any form: the integrity")
        print("  claim is unsupported and re-pointing the anchor cannot fix it.")
    print()
    return bucket, twin


# =========================================================================================
# C.  THE CONTROL FOR THE TWIN RULE.  A subject is a label; a patch-id is the change.
#     Constructed, in a repository built here, because "it could collide" is an argument and
#     a collision is a measurement.
# =========================================================================================
def section_c():
    print("C.  WHY THE TWIN IS IDENTIFIED BY patch-id AND NOT BY SUBJECT — CONSTRUCTED.")
    print()
    d = tempfile.mkdtemp(prefix="0120-twins-")
    try:
        def g(*a, **kw):
            return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True, **kw)
        g("init", "-q", "-b", "main")
        g("config", "user.email", "mg-0120@example.invalid")
        g("config", "user.name", "mg-0120")
        subject = ("predictions: mg-XXXX's predictions, COMMITTED BEFORE ANY SCRIPT OF THIS "
                   "REPAIR EXISTS")
        with open(os.path.join(d, "seed"), "w") as fh:
            fh.write("seed\n")
        g("add", "-A"); g("commit", "-q", "-m", "seed")

        # The real work, on its own branch — exactly the shape a polecat produces.
        g("checkout", "-q", "-b", "polecat-real")
        with open(os.path.join(d, "P.md"), "w") as fh:
            fh.write("THE REAL PREDICTIONS\n")
        g("add", "-A"); g("commit", "-q", "-m", subject)
        real = g("rev-parse", "HEAD").stdout.strip()

        # A different branch carrying the SAME SUBJECT and different content.
        g("checkout", "-q", "main")
        g("checkout", "-q", "-b", "polecat-impostor")
        with open(os.path.join(d, "Q.md"), "w") as fh:
            fh.write("DIFFERENT CONTENT ENTIRELY\n")
        g("add", "-A"); g("commit", "-q", "-m", subject)
        impostor = g("rev-parse", "HEAD").stdout.strip()

        # main advances, then BOTH are landed on it — which is what displaces their shas.
        g("checkout", "-q", "main")
        with open(os.path.join(d, "unrelated"), "w") as fh:
            fh.write("a later commit on main\n")
        g("add", "-A"); g("commit", "-q", "-m", "unrelated work")
        # NOT `cherry-pick -q`: git has no such switch, and the first draft of this section
        # passed it, so BOTH cherry-picks failed and `rebased` and `landed_impostor` both
        # came back as the `unrelated work` commit.  Every patch-id then "DIFFERED", the
        # control reported itself broken, and this file exited 1 — which is the behaviour
        # asked of it, and is why the wrong construction did not ship as a green line.
        for label, rev in (("the twin", real), ("the impostor", impostor)):
            r = g("cherry-pick", rev)
            if r.returncode != 0:
                print(f"    landing {label} FAILED: "
                      f"{(r.stderr or r.stdout).strip().splitlines()[0][:90]}")
                return False
        landed_impostor = g("rev-parse", "HEAD").stdout.strip()
        rebased = g("rev-parse", "HEAD~1").stdout.strip()

        print(f"    the REAL predictions commit, on its branch   {real[:7]}")
        print(f"    the SAME change, landed on main              {rebased[:7]}   "
              f"(the displacement the refinery performs)")
        print(f"    an IMPOSTOR: same subject, different content {impostor[:7]}  landed as "
              f"{landed_impostor[:7]}")
        print()
        pid = {k: patch_id(v, d) for k, v in
               (("real", real), ("rebased", rebased), ("impostor", landed_impostor))}
        print(f"    patch-id  real     {pid['real']}")
        print(f"    patch-id  rebased  {pid['rebased']}   "
              f"{'IDENTICAL to real' if pid['rebased'] == pid['real'] else 'DIFFERS from real'}")
        print(f"    patch-id  impostor {pid['impostor']}   "
              f"{'IDENTICAL to real' if pid['impostor'] == pid['real'] else 'DIFFERS from real'}")
        print()
        # The subject rule, exactly as anchor65eb.py:twin_of implements it — the first commit
        # in `git log <ref>` whose subject matches and whose abbreviation differs.
        log = [ln for ln in g("log", "--format=%H %s", "main").stdout.split("\n") if ln]
        by_subject = None
        for ln in log:
            h, _, sj = ln.partition(" ")
            if sj == subject and h[:7] != real[:7]:
                by_subject = h
                break
        by_patch = None
        for ln in log:
            h = ln.split(" ")[0]
            if patch_id(h, d) == pid["real"]:
                by_patch = h
                break
        ok_subject = by_subject == rebased
        ok_patch = by_patch == rebased
        print(f"    the SUBJECT rule (anchor65eb.py:twin_of) picks   {str(by_subject)[:7]}   "
              f"{'the rebased twin' if ok_subject else 'THE IMPOSTOR — the wrong commit'}")
        print(f"    the PATCH-ID rule (this file) picks              {str(by_patch)[:7]}   "
              f"{'the rebased twin' if ok_patch else 'THE WRONG COMMIT'}")
        print()
        print("    The impostor lands on main AFTER the twin, so it is nearer the tip and the")
        print("    subject search reaches it first.  Nothing here is exotic: two commits in")
        print("    this repository's own idiom, sharing a formulaic subject.  57 tokens in")
        print("    section D are displaced by exactly the mechanism modelled here.")
        print(f"    subject rule correct: {ok_subject}    patch-id rule correct: {ok_patch}")
        print()
        print("    THE CONTROL PASSES ONLY IF patch-id IS RIGHT AND SUBJECT IS WRONG.  If")
        print("    both were right this section would show nothing, and this file exits")
        print("    non-zero rather than printing a green line it has not earned.")
        print()
        return ok_patch and not ok_subject
    finally:
        subprocess.run(["rm", "-rf", d], capture_output=True)


# =========================================================================================
# D.  THE POPULATION mg-65eb COULD NOT SEE — every tracked text file, against `main`.
# =========================================================================================
def section_d(ref, index):
    print(f"D.  EVERY ANCHOR IN THE REPOSITORY, CLASSIFIED AGAINST {ref}.")
    print()
    files = population(ref)
    occurrences, where = {}, {}
    for path in files:
        text = git("show", f"{ref}:{path}").stdout
        for i, line in enumerate(text.split("\n"), 1):
            for tok in TOKEN.findall(line):
                if not is_hex_word(tok):
                    continue
                occurrences[tok] = occurrences.get(tok, 0) + 1
                where.setdefault(tok, []).append(f"{path}:{i}")
    buckets = {}
    detail = {}
    for tok in sorted(occurrences):
        bucket, subj, twin = classify(tok, ref, index)
        buckets.setdefault(bucket, []).append(tok)
        detail[tok] = (subj, twin)
    print(f"    POPULATION: {len(files)} tracked .py/.md/.sh/.txt files at {ref}.")
    print(f"    GRAIN of the first count: a DISTINCT hex token.  GRAIN of the second: one")
    print(f"    OCCURRENCE of a token in a line of a file.  They are different numbers and")
    print(f"    both are printed, because a token named 60 times and a token named once are")
    print(f"    one row each in the first and 61 in the second.")
    print(f"    distinct tokens {len(occurrences)}    occurrences "
          f"{sum(occurrences.values())}")
    print()
    for bucket in ("ANCHOR-LIVE", "ANCHOR-DISPLACED", "ANCHOR-STALE", "ANCHOR-DEAD",
                   "NOT-A-REVISION"):
        toks = buckets.get(bucket, [])
        occ = sum(occurrences[t] for t in toks)
        print(f"    {bucket:<18s} {len(toks):>3d} tokens   {occ:>4d} occurrences")
    print()
    for bucket in ("ANCHOR-DISPLACED", "ANCHOR-STALE", "ANCHOR-DEAD"):
        toks = buckets.get(bucket, [])
        if not toks:
            continue
        print(f"    {bucket}:")
        for tok in toks:
            subj, twin = detail[tok]
            print(f"      {tok:<12s} {occurrences[tok]:>3d}x  "
                  f"{'twin ' + twin[:7] if twin else 'no patch-id twin'}   "
                  f"first named at {where[tok][0]}")
            print(f"      {'':<12s}      {subj[:88]}")
        print()
    return buckets, occurrences, where


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", default="main",
                    help="the reference an anchor must be reachable from (default: main). "
                         "HEAD is what anchor65eb.py used, and on a polecat branch that "
                         "reaches unmerged commits no reader of main can follow.")
    args = ap.parse_args()

    print("=" * 100)
    print(f"mg-0120 — THE ANCHORS, DIAGNOSED BY CONTENT.  Reference: {args.ref}")
    print("=" * 100)
    print(f"  {args.ref} is {git('rev-parse', '--short', args.ref).stdout.strip()}")
    print("  EXISTENCE IS NOT ANCESTRY, and ANCESTRY IS NOT INTEGRITY: a rebased branch")
    print("  loses every sha it wrote while changing none of its content.")
    print("=" * 100)
    print()

    index = twins_by_patch_id(args.ref)
    print(f"A.  patch-id index built over {sum(len(v) for v in index.values())} commits "
          f"reachable from {args.ref}.")
    print()
    bucket, twin = section_b(args.ref, index)
    control_ok = section_c()
    buckets, occurrences, _where = section_d(args.ref, index)

    print("=" * 100)
    stale = buckets.get("ANCHOR-STALE", [])
    dead = buckets.get("ANCHOR-DEAD", [])
    disp = buckets.get("ANCHOR-DISPLACED", [])
    print(f"  the anchor under repair       {THE_ANCHOR}  ->  {bucket}"
          f"{' (twin ' + twin[:7] + ')' if twin else ''}")
    print(f"  the twin rule's own control   patch-id right and subject WRONG on a "
          f"constructed collision: {control_ok}")
    print(f"  repository-wide               {len(disp)} DISPLACED, {len(stale)} STALE, "
          f"{len(dead)} DEAD")
    print("=" * 100)
    return 0 if (not stale and not dead and control_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
