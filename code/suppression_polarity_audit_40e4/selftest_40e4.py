#!/usr/bin/env python3
"""mg-40e4 — the controls on THIS audit's own instruments.

Every count this audit prints has to be shown capable of being a different count, or it is a
row name and not a measurement.  Nothing here checks mg-5f7c; everything here checks mg-40e4.

    python3 code/suppression_polarity_audit_40e4/selftest_40e4.py

Exit 0 iff every control fires.  Renderer-free.
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import q1_polarity_40e4 as Q1                              # noqa: E402
import q3_claims_40e4 as Q3                                # noqa: E402
from lib40e4 import ANCHOR, REPO, VISIBLE, module_at       # noqa: E402
from q2_offsets_40e4 import true_offset                    # noqa: E402

RESULTS = []


def check(name, got, want, why):
    ok = got == want
    RESULTS.append((name, ok, got, want, why))
    print(f"  {'ok  ' if ok else 'FAIL'}  {name:<38s} got {got!r:<28s} want {want!r}")
    if not ok:
        print(f"          {why}")
    return ok


def main():
    print("=" * 100)
    print("mg-40e4 — CONTROLS ON THIS AUDIT'S OWN INSTRUMENTS")
    print("=" * 100)
    print()

    print("T1  `true_offset` — the definition Q2 rests on, on strings with known answers")
    check("marker with no entity before it", true_offset("<p>xyMARKz</p>", "MARK"), 5,
          "a plain string: the answer is the plain index")
    check("marker behind 3 `&amp;`", true_offset("&amp;&amp;&amp;MARK", "MARK"), 15,
          "the RAW position, not the unescaped one (which is 3)")
    check("that unescaped position is NOT 15",
          html.unescape("&amp;&amp;&amp;MARK").index("MARK"), 3,
          "the two differ, which is the whole defect Q2 measures")
    check("marker written as an entity", true_offset("a&mdash;b", "a—b"), 0,
          "the marker exists only after unescaping; `out.find` returns -1 here and this "
          "definition returns 0")
    check("absent marker", true_offset("<p>nothing</p>", "MARK"), None,
          "it must be able to say `not there` rather than 0")
    print()

    print("T2  `by_posture` — both branches, so the verdict is not a constant")
    check("shown + reported = FAILS CLOSED", Q1.by_posture(Q1.SHOWN, ["S5"])[0],
          "FAILS CLOSED", "the verdict that falsifies the fail-open sentence")
    check("shown + nothing = ok", Q1.by_posture(Q1.SHOWN, [])[0], "ok (fails open)", "")
    check("blank + reported = ok", Q1.by_posture(Q1.BLANK, ["S4"])[0], "ok (fails open)",
          "finding a real suppression is not a posture violation")
    check("blank + nothing = ok", Q1.by_posture(Q1.BLANK, [])[0], "ok (fails open)",
          "a miss is the posture working as designed")
    print()

    print("T3  Q1's population can MOVE — the same 28 documents at the pre-repair anchor")
    tree_dir = os.path.join(REPO, os.path.dirname(VISIBLE))
    sys.path.insert(0, tree_dir)
    import visible_a74f as tree                            # noqa: PLC0415
    anchor = module_at(ANCHOR, VISIBLE, "visible_anchor_selftest")
    counts = {}
    for label, mod in (("tree", tree), (ANCHOR, anchor)):
        closed = wrong = 0
        for cid, doc, _m, reader, _s, _i, correct, _w in Q1.CASES:
            got = mod.suppressors(doc, doc.index(Q1.MARK))
            if not Q1.by_posture(reader, got)[1]:
                closed += 1
            if not Q1.by_set(correct, got)[1]:
                wrong += 1
        counts[label] = (closed, wrong)
        print(f"      at {label:<12s} FAILS CLOSED {closed}/28   vs SET wrong {wrong}/28")
    check("the two revisions differ", counts["tree"] != counts[ANCHOR], True,
          "if the repaired and unrepaired instruments scored my population identically, "
          "the population could not see the repair at all and no row of Q1 is evidence")
    check("the repair strictly improved `vs SET`",
          counts["tree"][1] < counts[ANCHOR][1], True,
          "the repair must reduce the count it was written to reduce")
    print()

    print("T4  every Q1 document contains its marker exactly once")
    bad = [cid for cid, doc, *_ in Q1.CASES if doc.count(Q1.MARK) != 1]
    check("markers unique", bad, [], "a second occurrence would make `doc.index` ambiguous")
    print()

    print("T5  Q3's instrument rule can return FALSE")
    check("a file that is not an instrument",
          Q3.is_instrument("def f():\n    return 1\n"), False,
          "a rule that says yes to everything cannot refute an existence claim")
    check("visible_a74f is one",
          Q3.is_instrument(open(os.path.join(REPO, VISIBLE), encoding="utf-8").read()),
          True, "and it must say yes to the instrument the claim is about")
    print()

    n_ok = sum(1 for _n, ok, *_ in RESULTS if ok)
    print("=" * 100)
    print(f"  {n_ok} of {len(RESULTS)} controls fire.")
    print("  POPULATION: this audit's own functions.  GRAIN: one control.")
    print("=" * 100)
    return 0 if n_ok == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
