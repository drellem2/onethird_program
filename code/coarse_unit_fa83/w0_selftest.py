#!/usr/bin/env python3
"""mg-fa83 — THE WITNESS MACHINERY, BROKEN ON PURPOSE.

A witness search that finds a witness everywhere is measuring its own permissiveness, and one
that finds none is measuring nothing.  Both failures are silent in `w1`'s transcript, so they
are planted here and the plants are run.

D6 IS THE ONE WORTH READING, AND IT IS THIS DIRECTORY'S OWN SUBJECT ARRIVING IN THIS
DIRECTORY.  `w1`'s first draft compared each arm's decision as the pair `(exit code, grade
word)`.  That pair is a COARSER UNIT than the arm's own decision sentence: `f0` prints
`VERDICT: GREEN — 26 entries`, so a tree that gains a valid entry leaves `(0, GREEN)` exactly
where it was while the arm's sentence moves.  A `WITNESS` declared in that unit would have
been a control passing over a change it could see — the defect this directory exists to
exhibit, in the instrument exhibiting it.  D6 builds that tree, shows the coarse unit blind
and the shipped unit not, and the unit was made finer rather than the finding softened.

EXITS 0 if every plant lands where it must, 1 if one does not, 2 if this arm could not reach
its own decision.  A HOLE HERE IS WORSE THAN A FINDING IN `w1`: it means `w1`'s numbers are
about the sandbox rather than about the estate.
"""

import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_fa83 as L                                              # noqa: E402
import w1_witnesses as W                                          # noqa: E402

WIDTH = 92
RESULTS = []


def check(pid, name, ok, detail):
    RESULTS.append((pid, name, bool(ok), detail))
    print("  %-4s %-54s %-8s %s" % (pid, name[:54], "CAUGHT" if ok else "HOLE", detail[:26]))


def main():
    print("=" * WIDTH)
    print("mg-fa83  THE WITNESS MACHINERY, BROKEN ON PURPOSE")
    print("=" * WIDTH)
    print()

    before = L.doc_digests()
    work = tempfile.mkdtemp(prefix="fa83-w0-")
    try:
        body(work)
    finally:
        shutil.rmtree(work, ignore_errors=True)

    print()
    print("D9  THE REAL WORKING TREE IS UNMOVED BY EVERYTHING ABOVE")
    print("-" * WIDTH)
    after = L.doc_digests()
    for rel in L.GUARDED_DOCS:
        print("  %-34s %s   %s" % (rel, before[rel],
                                   "unmoved" if before[rel] == after[rel] else "*** MOVED ***"))
    check("D9", "no sandbox wrote through a symlink into the corpus",
          before == after, "4 documents digested")

    print()
    print("=" * WIDTH)
    holes = [r for r in RESULTS if not r[2]]
    print("%d of %d plants CAUGHT; %d hole(s)." % (len(RESULTS) - len(holes), len(RESULTS),
                                                   len(holes)))
    for pid, name, _ok, _d in holes:
        print("  HOLE  %s  %s" % (pid, name))
    print("SELFTEST VERDICT: %s" % ("GREEN" if not holes else "HOLE(S) — w1's numbers are "
                                    "about this sandbox, not about the estate"))
    print("=" * WIDTH)
    return 1 if holes else 0


def body(work):
    state = L.read(L.STATE_REL)
    facts = L.read(L.FACTS_REL)

    print("D1-D2  THE SANDBOX CARRIES THE MUTATION, AND ONLY THE MUTATION")
    print("-" * WIDTH)
    marked = state.replace("# 1/3", "# PLANTED 1/3", 1)
    tree = L.build_tree(os.path.join(work, "d1"), {L.STATE_REL: marked})
    got = open(os.path.join(tree, L.STATE_REL), encoding="utf-8").read()
    check("D1", "the mutated file in the tree is the mutant",
          got == marked and got != state, "STATE.md")
    other = open(os.path.join(tree, L.FACTS_REL), encoding="utf-8").read()
    check("D2", "every other file is the corpus, byte for byte",
          other == facts, "docs/FACTS.md via symlink")

    clean = L.build_tree(os.path.join(work, "d2b"), {L.STATE_REL: state})
    check("D2b", "a second tree does not carry the first tree's mutation",
          open(os.path.join(clean, L.STATE_REL), encoding="utf-8").read() == state,
          "no leakage between worlds")
    print()

    print("D3  THE DECISION CLASSIFIER IS EXERCISED IN EVERY CLASS IT HAS")
    print("-" * WIDTH)
    print("  A classifier only ever observed in one state is a constant.  Each class below is")
    print("  reached by a REAL arm on a REAL tree, not by a stub returning what is expected.")
    seen = {}
    worlds = (
        ("a grade word", "03cf", L.FACTS_REL, facts),
        ("a moved grade", "03cf", L.FACTS_REL, W.m_count_moving(facts)),
        ("REFUSED, by design", "602d", L.CONCEPTS_REL,
         L.inflate_preserving_words(L.read(L.CONCEPTS_REL))),
        ("CRASH, uncaught", "9bc2", L.STATE_REL, L.inflate_preserving_words(state)),
    )
    for label, arm, rel, text in worlds:
        t = L.build_tree(os.path.join(work, "d3-" + arm + label[:4].replace(" ", "")),
                         {rel: text})
        (rc, grade, _line), _ = L.decision(arm, t)
        seen[label] = (rc, grade)
        print("      %-22s %-6s exit %d / %s" % (label, arm, rc, grade))
    classes = {g for _rc, g in seen.values()}
    check("D3", "at least 3 distinct decision classes observed",
          len(classes) >= 3, "|".join(sorted(classes)))
    check("D3b", "REFUSED and CRASH are told apart",
          seen["REFUSED, by design"][1] == "REFUSED" and seen["CRASH, uncaught"][1] == "CRASH",
          "designed vs traceback")
    print()

    print("D4  THE WRONG DIRECTION — a change no arm reads must move nothing")
    print("-" * WIDTH)
    print("  A sandbox in which everything moves is a broken sandbox, not a finding.")
    base_tree = L.build_tree(os.path.join(work, "d4base"), {L.STATE_REL: state})
    inert = L.build_tree(os.path.join(work, "d4"),
                         {"docs/UNREAD-BY-ANY-GATED-ARM-fa83.md": "planted by w0 D4\n"})
    moved = []
    for arm_id, _r, _s, _re in L.ARMS:
        b, _ = L.decision(arm_id, base_tree)
        m, _ = L.decision(arm_id, inert)
        if b != m:
            moved.append(arm_id)
    check("D4", "a new file no arm reads moves 0 of 4 arms",
          not moved, "moved: %s" % (",".join(moved) or "none"))
    print()

    print("D5  A WORLD THAT PLANTS NOTHING IS REFUSED, NOT GRADED")
    print("-" * WIDTH)
    print("  mg-e331's N13 and mg-9876's unfalsifiable-row guard: a probe whose mutation is")
    print("  absent from the tree scores its own expectations.")
    caught = False
    try:
        W.run_recipe(os.path.join(work, "d5"),
                     ("Dx", "witness", "03cf", L.FACTS_REL, "a recipe that changes nothing",
                      lambda t: t, lambda a, b: []),
                     None, {L.FACTS_REL: facts})
    except L.Refusal as exc:
        caught = "did not change" in str(exc)
    check("D5", "a no-op recipe raises rather than reading WITNESS",
          caught, "Refusal on an unchanged file")
    print()

    print("D6  THE COARSE UNIT THIS INSTRUMENT NEARLY SHIPPED")
    print("-" * WIDTH)
    print("  A tree that GAINS a valid registry entry, with STATE.md's pointer moved to match:")
    print("  f0 stays GREEN and its own sentence moves 26 -> 27 entries.  Compared as")
    print("  (exit, grade) that is UNMOVED — a control passing over a change it can see, which")
    print("  is this directory's subject arriving in this directory.")
    grown = facts.rstrip("\n") + "\n\n" + W.FABRICATED
    pointed = state.replace("which holds 26 entries", "which holds 27 entries", 1)
    t = L.build_tree(os.path.join(work, "d6"), {L.FACTS_REL: grown, L.STATE_REL: pointed})
    base_t = L.build_tree(os.path.join(work, "d6base"), {L.FACTS_REL: facts})
    (brc, bgrade, bline), _ = L.decision("03cf", base_t)
    (mrc, mgrade, mline), _ = L.decision("03cf", t)
    print()
    print("      base    exit %d / %-6s %s" % (brc, bgrade, bline))
    print("      mutant  exit %d / %-6s %s" % (mrc, mgrade, mline))
    coarse_blind = (brc, bgrade) == (mrc, mgrade)
    fine_sees = (brc, bgrade, bline) != (mrc, mgrade, mline)
    check("D6", "the (exit, grade) unit is BLIND to it", coarse_blind, "the unit not shipped")
    check("D6b", "the shipped unit — with the decision line — is not",
          fine_sees, "the unit lib_fa83 uses")
    print("      So the finer unit is what `lib_fa83.decision` returns, and it was made finer")
    print("      because a witness was built against it — not because it looked safer.")
    print()

    print("D7  THE MUTATORS DO WHAT THEIR NAMES SAY")
    print("-" * WIDTH)
    inflated = L.inflate_preserving_words(state)
    check("D7", "inflate preserves the token count exactly",
          len(inflated.split()) == len(state.split()),
          "%d tokens" % len(state.split()))
    check("D7b", "and replaces every token",
          L.surviving_word_share(state, inflated) == 0.0, "0.0% survive")
    check("D7c", "surviving_word_share is 1.0 on the identity",
          L.surviving_word_share(state, state) == 1.0, "the wrong direction")
    kept = W.state_ledger_block(state)
    swapped = L.replace_words_outside(state, kept)
    check("D7d", "the ledger block really is held byte-identical",
          all(swapped.split("\n")[i] == state.split("\n")[i] for i in kept) and len(kept) > 10,
          "%d lines held" % len(kept))
    check("D7e", "and the total token count is unmoved by the swap",
          len(swapped.split()) == len(state.split()), "per-line preservation")
    print()

    print("D8  THE TRANSCRIPT CARRIES NO OPERATOR AND NO CLOCK")
    print("-" * WIDTH)
    print("  A transcript naming somebody's temp directory reproduces for exactly one operator")
    print("  and for nobody else, ever (mg-bdb0, on mg-4020's finding).")
    sample = "ran %s/x in 0.37 s under %s" % (work, L.ROOT)
    s = L.scrub(sample, work)
    check("D8", "the sandbox path is scrubbed", work not in s, "<sandbox>")
    check("D8b", "the repository root is scrubbed", L.ROOT not in s, "<repo>")
    check("D8c", "wall-clock is scrubbed", "0.37 s" not in s, "<t>s")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except L.Refusal as exc:
        print()
        print("REFUSED: %s" % exc)
        print("SELFTEST VERDICT: REFUSED — this arm did not reach its own decision.")
        sys.exit(2)
