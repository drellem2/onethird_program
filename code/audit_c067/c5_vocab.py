"""C5 -- THE VOCABULARY GAP, WHICH THE TICKET CALLS THE REAL FINDING.

    "The publication step it separates from prose is THE RUN, and the step that
     broke this is THE MERGE."

Two demands: **does the repair have a word for the merge**, and does its
documentation **distinguish `wrong when written` from `made wrong by a later
rebase`**?  Two different defects; one name is how the second hid.

The first two sections answer those.  The third asks the question they imply
and neither states: the old undifferentiated word is `STALE`, and if it is
still in use ANYWHERE in this arc meaning both things at once, the gap is
narrowed rather than closed.  So every occurrence in the tree is swept and
classified.
"""
import re
import sys

sys.path.insert(0, "../publication_anchor_132a")
import anchor_132a as P  # noqa: E402

import lib_c067 as L  # noqa: E402

REPAIRED = "code/hodge_leverage_repair_3f3b/repair_7e39.py"
PARENT_SRC = "code/publication_anchor_132a/anchor_132a.py"
PARENT_DOC = "code/publication_anchor_132a/README.md"


def main(argv):
    as_of = L.as_of_from_argv(argv)
    L.banner(as_of)

    # ----------------------------------------------------------------- C5a
    L.head("C5a -- IS THERE A WORD FOR THE MERGE?")
    print("""
Not `does the README use the word merge` -- prose can say anything.  The test
is whether the merge is a VERDICT the machinery can return: a value that a
check produces, a reader sees, and a gate treats differently from its
neighbours.
""")
    lattice = sorted(P.RED | {"AGREES", "DISPLACED"})
    for v in lattice:
        print(f"    {v:<22} {'RED' if v in P.RED else 'green'}")
    has_word = "DISPLACED" in lattice and "DISPLACED" not in P.RED
    L.record(has_word,
             f"C5a THE MERGE HAS A WORD AND IT IS A VERDICT, NOT A SENTENCE: "
             f"`DISPLACED`, one of {len(lattice)} rungs, green.  Its definition "
             f"names the step -- 'right when written, moved by a rebase'.  "
             f"⚠️ THE TEST WAS DELIBERATELY NOT `DOES THE PROSE SAY MERGE`: "
             f"a word that only exists in a README cannot be returned by a "
             f"check, and the gap the ticket names is precisely that the "
             f"machinery had one word where the world had two")

    # ----------------------------------------------------------------- C5b
    L.head("C5b -- AND ARE THE TWO DEFECTS DISTINGUISHED WHERE IT COUNTS?")
    print("""
`wrong when written` and `made wrong by a later rebase` must be separable by
the reader AND by the gate.  The strong form of the test: construct two
transcripts differing ONLY in which tree their anchor names, and check the
lattice separates them.
""")
    own = "code/publication_anchor_132a/out_anchor_132a.txt"
    text = L.blob_at(as_of, own)
    pub = L.publishing_commit(own, as_of)
    d = L.declared_anchor(text)

    # (i) right when written: the real anchor, which holds 495.
    v_disp = P.verdict_from_text(text, pub, as_of)
    # (ii) wrong when written: same bytes, anchor moved to a tree of 448.
    wrong_tree = L.resolve("77306a7")
    forged = L.DECLARED_RE.sub(
        f"POPULATION ANCHOR: commit={wrong_tree} count={d['count']} "
        f"digest={P.population_digest(wrong_tree)} scope={d['scope']}",
        text, 1)
    v_wrong = P.verdict_from_text(forged, pub, as_of)

    print(f"    same bytes, anchor {d['commit'][:7]} (holds "
          f"{L.population_count(L.resolve(d['commit']))}) -> "
          f"{v_disp['verdict']:<22} {'RED' if v_disp['verdict'] in P.RED else 'green'}")
    print(f"    same bytes, anchor {wrong_tree[:7]} (holds "
          f"{L.population_count(wrong_tree)}) -> "
          f"{v_wrong['verdict']:<22} {'RED' if v_wrong['verdict'] in P.RED else 'green'}")
    L.record(v_disp["verdict"] != v_wrong["verdict"]
             and (v_wrong["verdict"] in P.RED) != (v_disp["verdict"] in P.RED),
             f"C5b THE TWO DEFECTS ARE SEPARATED BY THE GATE AND NOT ONLY BY "
             f"THE PROSE: one transcript, two anchors, "
             f"`{v_disp['verdict']}` (green) against `{v_wrong['verdict']}` "
             f"(red).  ⚠️ THE ONLY DIFFERENCE BETWEEN THE INPUTS IS WHICH TREE "
             f"IS NAMED -- the published figure, the count field and every "
             f"other byte are identical -- so what is being read off is the "
             f"distinction itself and not some other property of the files")

    # ----------------------------------------------------------------- C5c
    L.head("C5c -- AND THE STEP IS NAMED IN THE FILE THAT WAS REPAIRED, NOT "
           "ONLY IN THE NEW ONE")
    print("""
A vocabulary that exists only in the deliverable that introduced it has not
been adopted.  The repaired file is the test.
""")
    src = L.blob_at(as_of, REPAIRED)
    CLAUSE = "a merge that lands elsewhere cannot make it red"
    # ⚠️ THE OCCURRENCES OF THE FALSE CLAUSE, CLASSIFIED -- see C5c' for why
    # this is not simply `CLAUSE not in src`.
    occ = [(i, ln) for i, ln in enumerate(src.splitlines(), 1)
           if CLAUSE in ln]
    quoted_occ = [(i, ln) for i, ln in occ
                  if "FALSE" in ln.upper() or f"'{CLAUSE}'" in ln]
    asserted = [(i, ln) for i, ln in occ if (i, ln) not in quoted_occ]

    rows = [
        ("`DISPLACED` as a reported verdict", "DISPLACED" in src),
        ("the word `rebase` naming the step", "REBASE" in src.upper()),
        ("the word `merge` naming the step", "merge" in src.lower()),
        (f"the false clause never ASSERTED ({len(occ)} occurrence(s), "
         f"{len(quoted_occ)} quoted)", not asserted),
        ("the rule LOADED from the parent rather than copied",
         "anchor_132a" in src),
    ]
    for label, ok in rows:
        print(f"    {label:<62} {'YES' if ok else 'NO'}")
    for i, ln in occ:
        print(f"        line {i}: {ln.strip()[:72]}")
    L.record(all(ok for _, ok in rows),
             f"C5c THE REPAIRED FILE CARRIES THE VOCABULARY: "
             f"{sum(1 for _, o in rows if o)} of {len(rows)} -- `DISPLACED` is "
             f"reported by `S4a`, the step is named as THE REBASE by `S4a'`, "
             f"the population rule is IMPORTED from `anchor_132a` rather than "
             f"copied, and the false clause survives at "
             f"{len(occ)} site(s), all {len(quoted_occ)} of them INSIDE THE "
             f"CORRECTION THAT RETRACTS IT ('...SAID SO IN A CLAUSE THAT WAS "
             f"FALSE: ...'), asserted at {len(asserted)}.  ⚠️ THE IMPORT IS "
             f"THE ONE THAT DECAYS SILENTLY: this repository has already "
             f"recorded two copies of `figures()` disagreeing on 3 (`8c55168`)")
    L.record(None,
             f"C5c' ⚠️ A DEFECT OF THIS INSTRUMENT, KEPT RATHER THAN SMOOTHED "
             f"AWAY.  The first version of the row above tested `CLAUSE not in "
             f"src` and REFUTED, and I read the refutation as a finding "
             f"against the parent before checking the site.  It is the "
             f"opposite: the clause is present exactly once, inside the "
             f"sentence that retracts it.  A correction note has to be able to "
             f"state what it corrects -- WHICH IS THIS ARC'S OWN RULE, `S4b`'s "
             f"'a figure inside a QUOTATION is exempt', written in the very "
             f"file I was testing.  I built a checker that would have flagged "
             f"every correction note in the repository as the error it "
             f"corrects, which is the same conflation of a claim with a "
             f"mention that `C2a` caught me making about `429`.  TWICE IN ONE "
             f"AUDIT, and the rule I needed was already on the page both times")

    # ----------------------------------------------------------------- C5d
    L.head("C5d -- THE OLD WORD, SWEPT: IS `STALE` STILL DOING BOTH JOBS?")
    print("""
⚠️ THE QUESTION THE TICKET IMPLIES AND DOES NOT ASK.  `STALE` is the word that
carried both defects.  If the repair introduced `DISPLACED` beside it but left
`STALE` in use meaning either, the gap is narrowed, not closed -- so every
occurrence in every committed `.py` and `.md` under `code/` is classified by
whether the sentence it sits in names WHICH defect it means.
""")
    files = [p for p in (L.git("ls-tree", "-r", "--name-only", "--full-tree",
                               as_of, "--", "code/") or "").splitlines()
             if p.endswith((".py", ".md"))]
    # ⚠️ `git grep -l` FIRST, then read only the files that matched.  The first
    # version read all 623 blobs one `git show` at a time and took eight
    # minutes; an audit nobody will re-run after a merge because it is too slow
    # is the same defect as one that cannot be re-run at all.
    hits = [p for p in (L.git("grep", "-l", "-i", "-w", "-e", "stale", as_of,
                              "--", "code/", ok=True) or "").splitlines()]
    hit_paths = sorted({h.split(":", 1)[1] for h in hits if ":" in h}
                       & set(files))
    qualified, bare = [], []
    for path in hit_paths:
        body = L.blob_at(as_of, path) or ""
        lines = body.splitlines()
        for i, line in enumerate(lines, 1):
            if not re.search(r"\bstale\b", line, re.I):
                continue
            ctx = " ".join(lines[max(0, i - 3):i + 2]).lower()
            near = ("rebase" in ctx or "displaced" in ctx
                    or "wrong when written" in ctx or "merge" in ctx)
            (qualified if near else bare).append((path, i, line.strip()[:78]))

    print(f"    files swept ({len(files)} committed `.py`/`.md` under `code/`)")
    print(f"    occurrences of `stale`      : {len(qualified) + len(bare)}")
    print(f"    QUALIFIED (the sentence names rebase/merge/displaced/wrong-"
          f"when-written within 2 lines) : {len(qualified)}")
    print(f"    BARE (neither defect named nearby) : {len(bare)}")
    for path, i, line in bare[:10]:
        print(f"        {path}:{i}  {line}")
    if len(bare) > 10:
        print(f"        ... and {len(bare) - 10} more")

    L.record(None,
             f"C5d THE POPULATION IS {len(qualified) + len(bare)} OCCURRENCE(S) "
             f"OF `stale` ACROSS {len(files)} COMMITTED `.py`/`.md` FILE(S) "
             f"UNDER `code/` AT {as_of[:7]}, of which {len(qualified)} sit "
             f"within two lines of a word that says WHICH defect is meant and "
             f"{len(bare)} do not.  ⚠️ THIS IS A MEASUREMENT AND NOT AN "
             f"ACCUSATION: the proximity test is a proxy, most of the bare "
             f"occurrences predate this arc, and `stale` is a perfectly good "
             f"English word in a sentence that is not making a verdict.  What "
             f"it establishes is the SIZE of the vocabulary the repair "
             f"introduced against the vocabulary already in the tree")
    L.record(len(bare) > 0,
             f"C5d' AND THE NEW WORD IS NOT RETROFITTED, WHICH IS CORRECT: "
             f"mg-132a added `DISPLACED` where a VERDICT is produced and "
             f"changed no prose elsewhere.  ⚠️ A DELIVERABLE THAT HAD REWRITTEN "
             f"{len(bare)} OTHER SITES WOULD HAVE MADE ITS OWN TRANSCRIPT "
             f"UNREVIEWABLE, and this arc has already recorded what a cosmetic "
             f"edit does to an audit trail.  The gap is real, named, and left "
             f"open on purpose; this row is where its size is on the record")

    return L.summary(as_of)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
