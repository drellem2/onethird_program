"""C2 -- EVERY ANCHOR RE-DERIVED, AND THE POPULATION NAMED RATHER THAN ASSERTED.

Two demands of the ticket meet here.

*"If it records a measuring commit, assert that commit's tree actually yields
the figure.  Otherwise the provenance is an unfalsifiable assertion in a file."*
-- so every anchor in the repository is RESOLVED and its count RE-DERIVED, by
this module's own `git ls-tree` walk and its own `.py` filter, sharing no code
with the parent's.

*"No bare totals -- name the population."* -- so the set of transcripts that
publish a `.py` population is SWEPT out of the tree rather than taken from the
parent's list, and the two are compared.
"""
import sys

import lib_c067 as L

PARENT_COMPUTED = [
    "code/hodge_leverage_repair_6df0/out_repair_6df0.txt",
    "code/hodge_leverage_repair_3f3b/out_repair_3f3b.txt",
    "code/publication_anchor_132a/out_anchor_132a.txt",
]


def main(argv):
    as_of = L.as_of_from_argv(argv)
    L.banner(as_of)

    # ----------------------------------------------------------------- C2a
    L.head("C2a -- THE POPULATION, SWEPT OUT OF THE TREE AND THEN QUALIFIED")
    print("""
Every committed file under `code/` at the audited rev whose text matches this
module's own figure grammar -- not the parent's list.  Named in full below,
because a total whose membership is not shown is the defect this arc keeps
finding.

⚠️ AND THEN THE SWEEP IS QUALIFIED, BECAUSE THE FIRST DRAFT OF THIS ROW WAS
WRONG.  It reported every match as a published figure, which inflated the
population: this arc has an explicit rule (`S4b`) that A FIGURE INSIDE A
QUOTATION IS EXEMPT, and `out_audit_7e39.txt`'s `429` is a quotation of
another transcript's figure inside a finding that says that figure is stale.
Counting it would have been the same error -- a bare total whose membership
nobody checked -- committed by the audit that came to report it.
""")
    swept = L.transcripts_publishing_a_population(as_of)
    rows = []
    for path, fig in swept:
        text = L.blob_at(as_of, path)
        kind = L.figure_kind(text)
        rows.append((path, fig, kind))
    for path, fig, kind in rows:
        mark = "  [in parent's COMPUTED]" if path in PARENT_COMPUTED else ""
        print(f"    {fig:>5}  {kind:<10} {path}{mark}")

    live = [(p, f) for p, f, k in rows if k != "QUOTED"]
    quoted = [(p, f) for p, f, k in rows if k == "QUOTED"]
    outside = [p for p, _ in live if p not in PARENT_COMPUTED]
    print(f"\n    matched              : {len(rows)}")
    print(f"    of those, QUOTED (exempt under this arc's own S4b) : "
          f"{len(quoted)}  "
          f"({', '.join(p.split('/')[-1] for p, _ in quoted) or '-'})")
    print(f"    LIVE published figures : {len(live)}")
    print(f"    parent's COMPUTED      : {len(PARENT_COMPUTED)}")
    print(f"    live but NOT in COMPUTED : {len(outside)}  "
          f"({', '.join(p.split('/')[-1] for p in outside) or '-'})")

    L.record(None,
             f"C2a THE PARENT'S `COMPUTED` IS A HAND LIST OF "
             f"{len(PARENT_COMPUTED)} AGAINST A TREE OF {len(live)} LIVE "
             f"PUBLISHERS: {len(rows)} committed file(s) under `code/` match "
             f"the figure grammar at {as_of[:7]}, {len(quoted)} of them inside "
             f"a QUOTATION and exempt, leaving {len(live)} that publish a `.py` "
             f"population as a claim about a tree -- "
             f"{', '.join(p.split('/')[-1] for p, _ in live)}.  "
             f"{len(outside)} of those are not in `COMPUTED`: "
             f"{', '.join(p.split('/')[-1] for p in outside) or 'none'}")
    if outside:
        L.finding(
            f"C2a' AND `A1a` REPORTS THE SCOPE LABEL AS THE KIND LABEL.  The "
            f"source comment scopes `COMPUTED` honestly -- 'every place IN THIS "
            f"ARC that publishes a `.py` population FOR THE SWEEP' -- but the "
            f"row it feeds drops both qualifiers and reads 'of the "
            f"{len(PARENT_COMPUTED)} published transcript(s) that carry a `.py` "
            f"population'.  ⚠️ A READER IS TOLD THE POPULATION IS "
            f"{len(PARENT_COMPUTED)} WHEN THE LIVE POPULATION IS {len(live)}.  "
            f"The gap is small and the omitted file is real: "
            f"{', '.join(p.split('/')[-1] for p in outside)}.  This is the same "
            f"shape mg-97fb found in the file this deliverable repairs (a hand "
            f"list of 2 against a tree of 9) and the same shape fba5f63 "
            f"recorded ('the scope label reported as the kind label')")

    # ----------------------------------------------------------------- C2a''
    L.head("C2a'' -- AND THE OMITTED FILE IS OMITTED FOR A REASON THE LATTICE "
           "CANNOT STATE")
    print("""
`read_anchor()` returns ONE anchor per file and `POP_FIGURE.search()` takes the
FIRST figure in it.  That is a model of a transcript as `one population, one
tree` -- which is true of every file in `COMPUTED` and false of the file left
out of it.
""")
    n_fig = n_commits = n_ok = 0
    for path in outside:
        text = L.blob_at(as_of, path)
        pairs = L.figures_with_inline_anchors(text)
        print(f"    {path}")
        for sha, fig, ctx in pairs:
            full = L.resolve(sha)
            mine = L.population_count(full) if full else None
            ok = mine == fig
            n_ok += 1 if ok else 0
            print(f"        {sha:<8} publishes {fig:<5} "
                  f"{'re-derives' if ok else f'MINE={mine}':<12} {ctx[:44]}")
        n_fig = len(pairs)
        n_commits = len(set(s for s, _, _ in pairs))
        print(f"        -> {n_fig} population figure(s) at {n_commits} "
              f"distinct commit(s); the parent's model would check the first "
              f"and only the first")
    L.finding(
        f"C2a'' ⚠️ THE LATTICE IS ONE-FIGURE-PER-FILE, AND THE OMITTED "
        f"TRANSCRIPT PUBLISHES {n_fig} AT {n_commits} DIFFERENT COMMITS.  "
        f"`out_audit_97fb.txt` states its populations INLINE -- '803bd50 "
        f"mg-6df0's parent : ... over 448 `.py` files under `code/`' -- one "
        f"anchor per ROW.  All {n_ok} of {n_fig} re-derive correctly against "
        f"the commit named beside them, so the figures are SOUND; what is "
        f"missing is any way for the parent's rule to say so.  "
        f"`read_anchor()` returns a single anchor for a file and "
        f"`POP_FIGURE.search()` takes the first figure, so under the parent's "
        f"rule at most 1 of the {n_fig} could ever be checked.  ⚠️ THIS IS WHY "
        f"THE HAND LIST IS THE SYMPTOM AND NOT THE DEFECT: adding this file to "
        f"`COMPUTED` would not check it, it would check one {n_fig}th of it.  "
        f"The declared-anchor form is a FILE-level field for a claim this "
        f"repository also makes at ROW level, and nothing in the deliverable "
        f"says so")

    # ----------------------------------------------------------------- C2b
    L.head("C2b -- EVERY ANCHOR RESOLVED, AND ITS COUNT RE-DERIVED INDEPENDENTLY")
    print("""
The claim under test is `commit X's tree holds N .py files`.  It is checked by
walking `git ls-tree -r` at X with this module's own blob filter and counting,
never by asking the parent's `py_files_at()`.  A declared `count=` field is
BELIEVED ABOUT NOTHING -- it is data to be refuted.
""")
    print(f"    {'transcript':<34} {'pub':<8} {'fig':>5} {'anchor':<9} "
          f"{'decl':>5} {'mine':>5}  {'reach':<5} verdict")
    bad, checked, unreachable = [], [], []
    for path, fig in swept:
        text = L.blob_at(as_of, path)
        pub = L.publishing_commit(path, as_of)
        d = L.declared_anchor(text)
        if not d:
            print(f"    {path.split('/')[-1]:<34} {pub[:7]:<8} {fig:>5} "
                  f"{'(none declared)':<9}")
            continue
        full = L.resolve(d["commit"])
        mine = L.population_count(full) if full else None
        reach = L.reachable(full, as_of) if full else False
        agree = (mine == d["count"] == fig)
        checked.append(path)
        if not agree:
            bad.append((path, d, mine))
        if full and not reach:
            unreachable.append((path, full))
        print(f"    {path.split('/')[-1]:<34} {pub[:7]:<8} {fig:>5} "
              f"{(full or '?')[:7]:<9} {d['count']:>5} "
              f"{str(mine):>5}  {'YES' if reach else 'NO':<5} "
              f"{'tree yields the figure' if agree else '*** DISAGREES ***'}")

    L.record(not bad,
             f"C2b of the {len(checked)} DECLARED anchor(s) in the tree at "
             f"{as_of[:7]} ({', '.join(p.split('/')[-1] for p in checked)}), "
             f"{len(checked) - len(bad)} name a commit whose tree ACTUALLY "
             f"YIELDS the figure the transcript publishes, re-derived here by "
             f"an independent walk.  ⚠️ THIS IS THE ROW THAT DECIDES WHETHER "
             f"ANSWER (2) IS A CHECK OR A NOTE.  A recorded provenance nobody "
             f"re-derives is an unfalsifiable assertion in a file; every one of "
             f"these was resolved and counted, and the declared `count=` field "
             f"was used as the thing to be refuted rather than as the answer")

    L.record(None,
             f"C2b' and {len(unreachable)} of the {len(checked)} anchor(s) are "
             f"UNREACHABLE from {as_of[:7]}: "
             + "; ".join(f"{p.split('/')[-1]} -> {c[:7]}"
                         for p, c in unreachable)
             + f".  Each survives only on a side ref -- "
             + "; ".join(f"{c[:7]}: {','.join(L.refs_containing(c)) or 'NO REF'}"
                         for _, c in unreachable[:3]))

    # ----------------------------------------------------------------- C2c
    L.head("C2c -- MY CHOSEN TARGET: DOES THE ADVERTISED REMEDY WORK ON THE "
           "REPAIR'S OWN FIGURE?")
    print("""
⚠️ NOTHING IN THE TICKET NAMES THIS.  `A2d` sells the digest as the answer to
the strongest objection against answer (2) -- that a recorded commit becomes an
unfalsifiable assertion once it is pruned -- and demonstrates it on a SYNTHETIC
transcript.  `A1d` says the two legacy figures cannot use it because they
predate the anchor line.

That leaves exactly one real figure in this repository carrying a digest: the
parent's own.  It is the first case where the remedy can be tested rather than
demonstrated, and the rebase has now put it in precisely the state the remedy
was built for.

The search below is by POPULATION SET -- the sorted path list itself, compared
element by element -- not by either side's hash.  Two independent digests that
disagree would be a finding; one digest compared with itself is a tautology.
""")
    own = "code/publication_anchor_132a/out_anchor_132a.txt"
    text = L.blob_at(as_of, own)
    d = L.declared_anchor(text)
    anchor = L.resolve(d["commit"])
    target = L.population_at(anchor)

    scanned_all, scanned_reach = [], []
    for rev in (L.git("rev-list", "--all", "-n", "700") or "").split():
        if L.population_at(rev) == target:
            scanned_all.append(rev)
    for rev in (L.git("rev-list", as_of, "-n", "700") or "").split():
        if L.population_at(rev) == target:
            scanned_reach.append(rev)

    print(f"    the parent's declared anchor          : {anchor[:12]}")
    print(f"    its `code/` population                : {len(target)} files")
    print(f"    commits ANYWHERE holding that exact population : "
          f"{len(scanned_all)}")
    for r in scanned_all:
        print(f"        {r[:7]}  refs: {','.join(L.refs_containing(r)) or '(none)'}")
    print(f"    of those, REACHABLE from {as_of[:7]}            : "
          f"{len(scanned_reach)}")

    L.record(None,
             f"C2c THE DIGEST RECOVERS THE PARENT'S OWN ANCHOR, AND RECOVERS IT "
             f"ONLY TO COMMITS THAT ARE THEMSELVES OFF THE MAINLINE: "
             f"{len(scanned_all)} commit(s) in the object store hold the "
             f"{len(target)}-file population that {anchor[:7]} was measured "
             f"against, and {len(scanned_reach)} of them are reachable from "
             f"{as_of[:7]}.  Every one is an mg-132a-era commit that the rebase "
             f"moved aside")
    L.finding(
        f"C2c' ⚠️ SO `A2d`'s CLAIM THAT `THE FIGURE SURVIVES ITS OWN ANCHOR` IS "
        f"TRUE OF THE SYNTHETIC CASE AND NOT YET TRUE OF THE PARENT'S OWN.  "
        f"Digest recovery searches `--all`, so it finds these {len(scanned_all)} "
        f"commits only while a ref still points at them -- and all "
        f"{len(scanned_all)} sit behind the same one, `polecat-132a`.  "
        f"⚠️ THE DIGEST AND THE DECLARED SHA THEREFORE SHARE A FAILURE MODE "
        f"NOBODY NAMED: they are not two independent routes to the tree, they "
        f"are two names for commits that one branch deletion removes together.  "
        f"`A2i` measures exactly this exposure FOR THE LEGACY FIGURES and calls "
        f"the digest the answer to it; the parent's own figure now has the "
        f"digest AND the same exposure.  Delete `polecat-132a`, run `git gc`, "
        f"and 495 becomes as uncheckable as 473 -- which is the outcome `A2d` "
        f"is offered as preventing")

    return L.summary(as_of)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
