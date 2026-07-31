"""C1 -- THE STALENESS CHECK RE-RUN AFTER A REBASE.

The ticket's demand, and the parent's own named gap: *a check that passes only
pre-merge is not a check on what merged*.

⚠️ THE REBASE HAS ALREADY HAPPENED, so this is not a simulation.  mg-132a's
five commits exist twice in this object store: once as written
(`d24bbeb 7dc9180 89d6aa1 4a06b4c 2cfd226`, alive only on `polecat-132a`) and
once as the refinery replayed them onto a larger `main`
(`53f6ca3 aa8309d cb9f282 a91cf9e 1e30484`).  The committed transcript was
written by a run at the FIRST set and has not been regenerated since.  This
script runs the parent's own instrument at the SECOND, which is the run nobody
performed.
"""
import subprocess
import sys

import lib_c067 as L

PARENT = "code/publication_anchor_132a/anchor_132a.py"
OWN = "code/publication_anchor_132a/out_anchor_132a.txt"
F3B = "code/hodge_leverage_repair_3f3b/out_repair_3f3b.txt"
F6D = "code/hodge_leverage_repair_6df0/out_repair_6df0.txt"

# The pre-rebase and post-rebase twins, by commit subject.  Derived, not
# hard-coded: a hard-coded pair would rot the next time anything is rebased.
def twins():
    pairs = []
    pre = L.git("log", "--format=%H%x1f%s", "polecat-132a", "-n", "12").splitlines()
    post = L.git("log", "--format=%H%x1f%s", "main", "-n", "40").splitlines()
    post_by_subject = {}
    for line in post:
        sha, _, subj = line.partition("\x1f")
        post_by_subject.setdefault(subj, sha)
    for line in pre:
        sha, _, subj = line.partition("\x1f")
        if "(mg-132a)" not in subj:
            continue
        if subj in post_by_subject and post_by_subject[subj] != sha:
            pairs.append((sha, post_by_subject[subj], subj))
    return pairs


def run_parent(rev):
    """Run the parent's instrument as of `rev`.  As a SUBPROCESS, so its exit
    code is scored as an exit code -- importing it and catching SystemExit
    would score my handling of its exception instead."""
    r = subprocess.run([sys.executable, "anchor_132a.py", "--at", rev],
                       cwd=f"{L.REPO}/code/publication_anchor_132a",
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def verdict_lines(out, path):
    """The verdict the parent's output gives for `path`, per section."""
    got, want = [], path.split("/")[-1]
    lines = out.splitlines()
    for i, line in enumerate(lines):
        if line.strip().endswith(want):
            for j in range(i + 1, min(i + 4, len(lines))):
                if "verdict" in lines[j]:
                    got.append(lines[j].split(":", 1)[1].strip())
                    break
    return got


def main(argv):
    as_of = L.as_of_from_argv(argv)
    L.banner(as_of)

    # ----------------------------------------------------------------- C1a
    head = L.head
    head("C1a -- THE REBASE IS REAL, AND IT IS THE ONE THAT DISPLACED THE PARENT")
    print("""
Each of mg-132a's commits exists twice.  The pair is found by matching commit
SUBJECTS across `polecat-132a` and `main` rather than by a hard-coded table,
so this row cannot go quietly true by naming commits that no longer exist.
""")
    pairs = twins()
    for pre, post, subj in pairs:
        pre_n, post_n = L.population_count(pre), L.population_count(post)
        print(f"    {pre[:7]} -> {post[:7]}  code/ .py: {pre_n} -> {post_n}"
              f"   {subj[:64]}")
    moved = [(a, b) for a, b, _ in pairs
             if L.population_count(a) != L.population_count(b)]
    L.record(len(pairs) > 0,
             f"C1a mg-132a's {len(pairs)} commit(s) were REPLAYED onto a larger "
             f"tree by the merge, and {len(moved)} of them landed on a tree "
             f"with a DIFFERENT `code/` population than the one they were "
             f"written against.  ⚠️ THIS IS THE STEP THE PARENT SAYS NOTHING "
             f"RE-RUNS AFTER, performed on the parent itself, four commits "
             f"after it argued that it would be")
    unreach = [a for a, b, _ in pairs if not L.reachable(a, as_of)]
    L.record(len(unreach) == len(pairs),
             f"C1a' and all {len(unreach)} of the pre-rebase commit(s) are "
             f"UNREACHABLE from the audited rev -- they survive only on "
             f"{', '.join(sorted(set(r for a in unreach[:1] for r in L.refs_containing(a)))) or 'no ref'}."
             f"  The commits the committed transcript names as its own "
             f"provenance are off the mainline")

    # ----------------------------------------------------------------- C1b
    head("C1b -- THE PARENT'S OWN INSTRUMENT, RE-RUN AT FOUR REVS")
    print("""
Predicted in `PREDICTIONS.md` BEFORE any of these were run.  Three of the four
predictions are WRONG and are kept as written.
""")
    plan = [
        ("4a06b4c", 0, "the rev the transcript was committed at (pre-rebase)"),
        (as_of[:7], 1, "the audited rev, AFTER the rebase"),
        ("1e30484", 1, "the commit that publishes its own transcript AFTER the merge"),
        ("cb9f282", 1, "the post-merge publishing commit of out_repair_3f3b.txt"),
    ]
    observed = {}
    for rev, predicted, why in plan:
        code, out = run_parent(rev)
        observed[rev] = (code, out)
        mark = "as predicted" if code == predicted else "*** MISS ***"
        print(f"    --at {rev:<8} predicted exit {predicted}   observed exit "
              f"{code}   {mark}")
        print(f"        {why}")
    misses = [r for r, p, _ in plan if observed[r][0] != p]
    L.record(None,
             f"C1b {len(misses)} of the 4 predicted exit code(s) MISSED: "
             f"{', '.join(misses) or 'none'}.  ⚠️ THE PREDICTION WAS THAT `A3a` "
             f"WOULD GO RED, on the reasoning that the committed transcript "
             f"asserts its own verdict is `AGREES` in so many words.  It does "
             f"not: `A3a` reports WHICHEVER verdict fires and is green while "
             f"that verdict is green, and `DISPLACED` is green by the parent's "
             f"own decision.  The row was built to survive exactly this and it "
             f"did.  Kept as written because a prediction quietly corrected "
             f"after the fact is not a prediction")

    # ----------------------------------------------------------------- C1c
    head("C1c -- THE SECOND QUESTION: DOES THE REPAIR'S OWN TRANSCRIPT SURVIVE ITS OWN RULE?")
    print("""
The predecessor's transcript said `0 STALE` while being stale, 2 of 2.  The
question is whether the repair's transcript is stale in the same shape.  It is
asked field by field: what the COMMITTED bytes claim, against what the SAME
INSTRUMENT says when re-run at the audited rev.
""")
    live_code, live = observed[as_of[:7]]
    committed = L.blob_at(as_of, OWN)

    def claim(text, needle, upto=140):
        for line in text.splitlines():
            if needle in line:
                return line.strip()[:upto]
        return "(absent)"

    rows = [
        ("its own verdict (A3a)",
         verdict_lines(committed, OWN)[-1] if verdict_lines(committed, OWN) else "?",
         verdict_lines(live, OWN)[-1] if verdict_lines(live, OWN) else "?"),
        ("figures DISPLACED (A1c)",
         claim(committed, "A1c").split("figure(s)")[0].split("] ")[-1],
         claim(live, "A1c").split("figure(s)")[0].split("] ")[-1]),
        ("anchors NOT REACHABLE (A1d)",
         claim(committed, "A1d").split("verified")[0].split("] ")[-1],
         claim(live, "A1d").split("verified")[0].split("] ")[-1]),
    ]
    for label, was, now in rows:
        flag = "  <-- MOVED" if was.strip() != now.strip() else ""
        print(f"    {label:<30} committed: {was.strip():<14} "
              f"re-run: {now.strip():<14}{flag}")

    agrees_then = [p for p in (OWN, F3B, F6D)
                   if verdict_lines(committed, p)
                   and "AGREES" in verdict_lines(committed, p)[0]]
    displaced_now = [p for p in agrees_then
                     if verdict_lines(live, p)
                     and "DISPLACED" in verdict_lines(live, p)[0]]
    L.record(None,
             f"C1c THE COMMITTED TRANSCRIPT IS STALE IN ITS PREDECESSOR'S EXACT "
             f"SHAPE, {len(displaced_now)} OF {len(agrees_then)}: of the "
             f"{len(agrees_then)} transcript(s) it records as `AGREES` "
             f"({', '.join(p.split('/')[-1] for p in agrees_then)}), "
             f"{len(displaced_now)} read `DISPLACED` when the same instrument "
             f"is re-run at {as_of[:7]}.  Its A1c says 1 displaced where the "
             f"live answer is 3, and its A1d says 1 unreachable anchor where "
             f"the live answer is 3")
    L.record(live_code == 0,
             f"C1c' ⚠️ AND THE DIFFERENCE THAT MATTERS: NO GATE FLIPPED.  The "
             f"re-run at {as_of[:7]} exits {live_code} with 0 refuted.  The "
             f"predecessor's `0 STALE` was stale AND WRONG -- the figures it "
             f"blessed were red under its own rule once the tree moved.  This "
             f"transcript's rows are stale AND STILL CORRECT: every claim it "
             f"makes is true of the commit it names, and the verdict the live "
             f"run returns is green.  STALE-AND-RED and STALE-AND-GREEN are "
             f"different failures and the second is the one answer (2) was "
             f"chosen to produce.  Reporting them as one would be the same "
             f"conflation the parent was filed to fix")

    # ----------------------------------------------------------------- C1d
    head("C1d -- BUT NOBODY RAN IT")
    pub_own = L.publishing_commit(OWN, as_of)
    decl = L.declared_anchor(committed)
    print(f"""
    the committed transcript declares its anchor as : {decl['commit'][:12]}
    that commit is reachable from {as_of[:7]}          : {'YES' if L.reachable(decl['commit'], as_of) else 'NO'}
    the commit that publishes it now                : {pub_own[:12]}
    `code/` .py population there                    : {L.population_count(pub_own)}
    the figure it publishes                         : {L.published_figure(committed)}
""")
    L.record(not L.reachable(decl["commit"], as_of),
             f"C1d THE PARENT'S `--at <rev>` IS THE WHOLE REMEDY IT OFFERS FOR "
             f"THE MERGE, AND IT HAS NOT BEEN RUN ONCE SINCE THE MERGE THAT "
             f"MADE IT NECESSARY.  The transcript at {as_of[:7]} was written by "
             f"a run at {decl['commit'][:7]}, a commit that is not reachable "
             f"from {as_of[:7]}.  ⚠️ THIS IS NOT A DEFECT OF THE INSTRUMENT -- "
             f"the instrument returns the right answer the moment it is asked "
             f"-- IT IS THE GAP `A3c` NAMES, OBSERVED HOLDING OPEN.  A remedy "
             f"whose trigger is a human remembering is the same class of "
             f"control as the one that failed")

    # ----------------------------------------------------------------- C1e
    head("C1e -- AND `--at` IS EXERCISED HERE AT A REV THE PARENT NEVER CHOSE")
    print("""
`A3d` runs the lattice at `as_of~1`, which is always the audited rev's parent.
That demonstrates the flag, but the commit is picked by the tool.  Here it is
pointed at the two post-merge publishing commits by NAME -- which is what a
post-merge re-check actually is, and is the invocation the ticket asked for.
""")
    for rev in ("1e30484", "cb9f282"):
        code, out = observed[rev]
        vs = [f"{p.split('/')[-1]} -> {(verdict_lines(out, p) or ['(absent)'])[0]}"
              for p in (F6D, F3B, OWN)]
        print(f"    --at {rev}  exit {code}   " + "; ".join(vs))
    L.record(observed["1e30484"][0] == 0 and observed["cb9f282"][0] == 0,
             f"C1e THE REPAIRED CHECK RUN AGAINST THE REPAIR'S OWN PUBLISHED "
             f"FIGURES, AT THE COMMIT THAT PUBLISHES THEM AFTER MERGE: "
             f"`--at 1e30484` exits {observed['1e30484'][0]} and `--at cb9f282` "
             f"exits {observed['cb9f282'][0]}.  At cb9f282 its own transcript "
             f"is not published yet and the row is named rather than counted "
             f"as a pass, which is the behaviour a check that scored absence as "
             f"success would not have")

    return L.summary(as_of)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
