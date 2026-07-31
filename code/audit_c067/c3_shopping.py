"""C3 -- THE PRIMARY TARGET: THE CASE THE OTHER ANSWER HANDLES.

The ticket: *"Whichever it chose, construct the case the other answer handles
and confirm the chosen one does too -- or that the deliverable says plainly
that it does not."*

The parent chose **answer (2)**, the commit a figure was MEASURED at.  Answer
(1), `git log -1`, keys on the commit that PUBLISHES it.

⚠️ THE CONSTRUCTIONS BELOW CALL THE PARENT'S OWN `verdict_from_text()`.  That
import is deliberate and is the opposite of `lib_c067`'s rule: re-implementing
the lattice here would test my reading of it, not it.  The population figures
these constructions are judged against are still re-derived independently.

Two cases separate the answers, and they fall opposite ways:

  DISPLACEMENT -- a figure true at its anchor, sitting in a tree that has moved
  on.  (1) calls it red; (2) calls it green.  The parent states this plainly
  and at length, so (2) not handling it is DISCLOSED, not hidden.

  SUBSTITUTION ("anchor shopping") -- a figure that was never true of the tree
  it was actually measured at, carrying a declared anchor pointing at some
  other commit whose tree does hold it.  (1) catches it, because (1)'s examiner
  is fixed by `git log -1` and cannot be chosen.  (2) is told which tree to
  look at BY THE FILE UNDER EXAMINATION.
"""
import sys

sys.path.insert(0, "../publication_anchor_132a")
import anchor_132a as P  # noqa: E402  -- the rule under test, called directly

import lib_c067 as L  # noqa: E402


def main(argv):
    as_of = L.as_of_from_argv(argv)
    L.banner(as_of)

    own = "code/publication_anchor_132a/out_anchor_132a.txt"
    f3b = "code/hodge_leverage_repair_3f3b/out_repair_3f3b.txt"

    # ----------------------------------------------------------------- C3a
    L.head("C3a -- DISPLACEMENT: THE CASE (1) CALLS RED AND (2) CALLS GREEN")
    print("""
Taken from the tree, not constructed.  Both answers are computed for the same
bytes so the disagreement is exhibited rather than described.
""")
    print(f"    {'transcript':<24} {'fig':>5} {'(1) publishing tree':>21} "
          f"{'(2) anchor tree':>17}   (1) says   (2) says")
    disagree = 0
    for path in (own, f3b):
        text = L.blob_at(as_of, path)
        fig = L.published_figure(text)
        pub = L.publishing_commit(path, as_of)
        anc = L.resolve(L.declared_anchor(text)["commit"])
        n_pub, n_anc = L.population_count(pub), L.population_count(anc)
        v1 = "RED" if n_pub != fig else "green"
        v2 = P.verdict_from_text(text, pub, as_of)["verdict"]
        disagree += 1 if (v1 == "RED" and v2 not in P.RED) else 0
        print(f"    {path.split('/')[-1]:<24} {fig:>5} "
              f"{f'{pub[:7]} holds {n_pub}':>21} "
              f"{f'{anc[:7]} holds {n_anc}':>17}   {v1:<9}  {v2}")

    L.record(disagree == 2,
             f"C3a THE TWO ANSWERS DISAGREE ON {disagree} OF THE 2 DECLARED "
             f"FIGURES IN THE TREE, AND THE PARENT SAYS SO IN SO MANY WORDS.  "
             f"Answer (1) calls both red -- the publishing tree holds 496 "
             f"against a published 495 -- and answer (2) calls both "
             f"`DISPLACED`, which is green.  ⚠️ THIS IS DISCLOSED RATHER THAN "
             f"HIDDEN: the README's section `The price, stated rather than "
             f"hidden` opens 'Under (2) a reader can meet 473 beside a tree of "
             f"481 and the check stays green', and `A1c` says NOT RED, AND "
             f"THAT IS THE DECISION.  A deliverable that has named the case it "
             f"does not catch has met the ticket's bar for this one")

    # ----------------------------------------------------------------- C3b
    L.head("C3b -- SUBSTITUTION: THE CASE (1) CATCHES AND (2) IS ASKED TO "
           "TRUST THE FILE ABOUT")
    print("""
CONSTRUCTED.  A transcript publishing a figure that is NOT the population of
the tree it was really measured at, carrying a DECLARED anchor naming a commit
whose tree does hold it.  This is not a forged sha and not a broken digest:
every field is internally consistent and every one of them resolves.  The only
false thing is WHICH TREE IS NAMED.
""")
    # A real figure from this repository's history and a commit that holds it.
    donor = None
    for rev in (L.git("rev-list", "--all", "-n", "700") or "").split():
        if L.population_count(rev) == 481:
            donor = rev
            break
    text = L.blob_at(as_of, own)
    pub = L.publishing_commit(own, as_of)
    n_pub = L.population_count(pub)

    # publishes 481; declares the donor commit, which really does hold 481.
    forged = text.replace("495 .py files", "481 .py files", 1)
    forged = L.DECLARED_RE.sub(
        f"POPULATION ANCHOR: commit={donor} count=481 "
        f"digest={P.population_digest(donor)} scope=code/**/*.py", forged, 1)

    v = P.verdict_from_text(forged, pub, as_of)
    print(f"    the transcript publishes            : 481")
    print(f"    its declared anchor                 : {donor[:12]}")
    print(f"    that commit's tree really holds     : "
          f"{L.population_count(donor)}   (re-derived independently)")
    print(f"    the tree it is actually published in: {pub[:7]} holds {n_pub}")
    print(f"    answer (1) -- `git log -1` -- would say : "
          f"{'RED' if n_pub != 481 else 'green'}")
    print(f"    answer (2) -- the parent's rule -- says : {v['verdict']}")

    L.record(v["verdict"] not in P.RED,
             f"C3b ANCHOR SHOPPING READS `{v['verdict']}` AND IS GREEN.  A "
             f"figure of 481 published in a tree of {n_pub}, declaring an "
             f"anchor at {donor[:7]} whose tree genuinely holds 481.  Every "
             f"check the parent applies passes: the sha resolves, the count "
             f"re-derives from `git ls-tree`, the digest matches, and the "
             f"declared count agrees with the published figure so `A2g`'s "
             f"`INCONSISTENT` does not fire.  ⚠️ ANSWER (1) WOULD HAVE CAUGHT "
             f"THIS, because `git log -1` picks the examiner and the file "
             f"cannot argue with it")
    L.finding(
        f"C3b' ⚠️ AND THE DELIVERABLE DOES NOT SAY THAT IT DOES NOT CATCH "
        f"THIS.  The README's `price` section discloses exactly one cost of "
        f"(2) -- DISPLACEMENT, a true figure that has lost currency -- and "
        f"answers the objection `an anchor is an unfalsifiable assertion` with "
        f"three defences, all of which are about the anchor being RESOLVABLE "
        f"(`A2c` re-derives the count, `A1b` reds an anchor that resolves to "
        f"nothing, `A2d` recovers a pruned one by digest).  SUBSTITUTION "
        f"defeats all three by satisfying them: the anchor resolves, the count "
        f"re-derives, the digest matches.  `A2c` catches a declared anchor "
        f"whose tree does NOT hold the figure; this is the case where it DOES, "
        f"and the number is still wrong about the run that produced it.  Under "
        f"(1) the examiner is fixed by git; under (2) THE PUBLICATION STEP "
        f"NAMES ITS OWN EXAMINER, and that transfer of authority is the actual "
        f"price of the decision -- unnamed in a deliverable that is otherwise "
        f"careful to price itself")

    # ----------------------------------------------------------------- C3c
    L.head("C3c -- HOW MUCH ROOM THE SHOPPER HAS, MEASURED")
    print("""
The finding above is only worth the size of the space it opens.  `A2h` measures
that a digest is many-to-one; the question here is different and sharper -- for
a figure a publication step might want to launder, HOW MANY commits in this
object store would certify it?
""")
    hist = [r for r in (L.git("rev-list", "--all", "-n", "700") or "").split()]
    counts = {}
    for r in hist:
        n = L.population_count(r)
        counts.setdefault(n, []).append(r)
    interesting = sorted(counts.items(), key=lambda kv: -len(kv[1]))[:6]
    print(f"    {len(hist)} commit(s) walked; distinct `code/` populations: "
          f"{len(counts)}")
    for n, revs in interesting:
        print(f"        a figure of {n:<5} would be certified by "
              f"{len(revs):>3} commit(s)")
    biggest = max(len(v) for v in counts.values())
    L.record(None,
             f"C3c A SHOPPER'S CHOICE, NAMED RATHER THAN TOTALLED: over the "
             f"{len(hist)} commit(s) in this object store there are "
             f"{len(counts)} distinct `code/` populations, and the most "
             f"common one is held by {biggest} commit(s).  ⚠️ THE POINT IS NOT "
             f"THAT THE NUMBER IS LARGE -- it is that ANY commit holding the "
             f"figure will do, and the publication step is free to pick it.  A "
             f"figure only has to have been true ONCE, anywhere in the "
             f"history, for a declared anchor to certify it forever")

    # ----------------------------------------------------------------- C3d
    L.head("C3d -- AND THE REPAIR THAT WOULD CLOSE IT ALREADY EXISTS IN THE FILE")
    print("""
Not a redesign.  The parent already computes both numbers and prints them side
by side; what it does not do is ask whether the anchor is one the run could
have measured at.
""")
    text = L.blob_at(as_of, own)
    anc = L.resolve(L.declared_anchor(text)["commit"])
    pub = L.publishing_commit(own, as_of)
    honest_anc_ok = L.reachable(anc, pub) or bool(
        L.refs_containing(anc))
    forged_anc_ok = L.reachable(donor, pub)
    print(f"    the parent's real anchor {anc[:7]} is an ancestor of its "
          f"publishing commit {pub[:7]} : "
          f"{'YES' if L.reachable(anc, pub) else 'NO'}")
    print(f"    the shopped anchor      {donor[:7]} is an ancestor of that "
          f"same commit                : "
          f"{'YES' if forged_anc_ok else 'NO'}")
    L.record(None,
             f"C3d ⚠️ THE ANCESTRY TEST DOES NOT SEPARATE THEM EITHER, AND "
             f"THAT IS WORTH SAYING RATHER THAN PROPOSING A FIX THAT DOES NOT "
             f"WORK.  The obvious repair -- require the declared anchor to be "
             f"an ancestor of the publishing commit -- fails on the parent's "
             f"OWN anchor: {anc[:7]} is "
             f"{'an' if L.reachable(anc, pub) else 'NOT an'} ancestor of "
             f"{pub[:7]}, because the rebase is exactly what took it off that "
             f"line of descent.  A rule strong enough to reject the shopped "
             f"anchor would reject every genuinely rebased one.  The two are "
             f"not distinguishable from inside the repository, which is the "
             f"honest form of this finding: SUBSTITUTION is not a bug in the "
             f"lattice, it is the residue of moving the examiner into the "
             f"file, and it is unnamed")

    return L.summary(as_of)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
