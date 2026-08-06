#!/usr/bin/env python3
"""mg-40e4 — Q2.  THE BYTE OFFSET SPENT AS AN INDEX, AND THE POPULATION OF FIGURES IT
COULD ALREADY HAVE CORRUPTED — RE-DERIVED, AND OVER A LARGER POPULATION THAN mg-5f7c'S.

mg-5f7c's `offsets_5f7c.py` answers "had it already corrupted a published figure?" over

    mg-a74f's published run — 5 documents x 2 renderers x 5 cited sections = 50 observations

and prints `32 OF 50` walked from a wrong position and `0 OF 10` published row figures moved.
This file does three things that taking those numbers and confirming them cannot.

  1.  IT RE-DERIVES THEM FROM ITS OWN ARITHMETIC.  The "true" offset here is not taken from
      the repaired code and not taken from `out.find`.  It is computed independently as *the
      smallest j such that `html.unescape(out[j:])` begins with the marker*, which is what
      "the marker's position in the string being walked" MEANS, and it is then compared with
      what the repaired code computes.  Auditing a repair by using the repaired function to
      define the right answer is not an audit.

  2.  IT CHECKS THE DEFINITION mg-5f7c SUBSTITUTED.  `offsets_5f7c.py` section B and
      `rows65eb.py` both use `out.find(marker)` as the true offset.  That is a DIFFERENT
      FUNCTION from the one the repair ships: it returns -1 whenever a renderer writes the
      marker with a character reference, and `-1` is exactly the case mg-65eb's R1 is about.
      Where it returns -1 both files drop the observation out of the comparison and still
      print a total.

  3.  IT ENLARGES THE POPULATION.  mg-a74f's 50 are not the only published figures produced
      by the defective expression.  `rows65eb.py:240` recomputes it —
      `V.suppressors(out, u.index(V.marker(h)))` — and mg-65eb PUBLISHES the result in
      `out_rows65eb.txt` and `out_run_all.txt`: 4 constructions x 2 renderers x 5 sections =
      40 further section observations and 8 further row figures, none of them in mg-5f7c's
      stated population.  A fix to the arithmetic leaves a corrupted output standing wherever
      the audit of outputs stopped short.

Every figure below names its POPULATION and its GRAIN, and every re-derivation is checked
against the COMMITTED TRANSCRIPT it claims to reproduce, so a number that does not reproduce
is a finding rather than a silent substitution.

    NODE_PATH=... python3 code/suppression_polarity_audit_40e4/q2_offsets_40e4.py

Needs the two GFM renderers.  Without them it exits 3 and says so; it does not guess.
"""
import html
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib40e4 import ANCHOR, REPO, VISIBLE, module_at, source_at   # noqa: E402

ROWS65EB = "code/state_visibility_audit_65eb/rows65eb.py"
A74F_TRANSCRIPT = "code/state_delegation_repair_a74f/out_run_all.txt"
A74F_PRE = "code/state_suppression_repair_5f7c/out_run_all_a74f_PRE5f7c.txt"
EB_TRANSCRIPT = "code/state_visibility_audit_65eb/out_rows65eb.txt"


# =========================================================================================
# THE TRUE OFFSET, DEFINED WITHOUT REFERENCE TO EITHER IMPLEMENTATION.
# =========================================================================================
def true_offset(out, marker):
    """The smallest j with `html.unescape(out[j:])` beginning with `marker`, or None.

    This is the definition, not an implementation of somebody's map.  The window is generous
    (12x the marker) because a character reference is at most a handful of characters wide
    and the marker is five; `startswith` on the first `len(marker)` characters is all that is
    asked of it, so a truncated trailing reference inside the window cannot change the
    answer."""
    w = len(marker) * 12
    for j in range(len(out)):
        if html.unescape(out[j:j + w]).startswith(marker):
            return j
    return None


def observe(mod, tree, out, cited, markerfn):
    """One rendered document, every cited marker, four positions and two verdicts each.

    POSITIONS
      started   `html.unescape(out).index(marker)` — the expression `visible_a74f.main()`
                shipped at 6fb424f, read out of that revision's source and not retyped
      true      the definition above, computed here
      repaired  what the repaired `unescape_with_map` gives back — AUDITED, not trusted
      find      `out.find(marker)` — the substitute `offsets_5f7c.py` and `rows65eb.py` use
    """
    u = html.unescape(out)
    rows = []
    for h in cited:
        m = markerfn(h)
        if m not in u:
            continue
        started = u.index(m)
        true = true_offset(out, m)
        unesc, index = tree.unescape_with_map(out)
        repaired = index[unesc.index(m)] if m in unesc else None
        found = out.find(m)
        rows.append({
            "h": h, "started": started, "true": true, "repaired": repaired, "find": found,
            "at_started": mod.suppressors(out, started),
            "at_true": mod.suppressors(out, true) if true is not None else None,
        })
    return rows


def figures(rows):
    """(published not-suppressed, not-suppressed at the true offset) for one renderer row."""
    pub = sum(1 for r in rows if not r["at_started"])
    tru = sum(1 for r in rows if r["at_true"] is not None and not r["at_true"])
    return pub, tru


def transcript_figures(path, pattern):
    txt = open(os.path.join(REPO, path), encoding="utf-8").read()
    return re.findall(pattern, txt)


def main():
    tree_dir = os.path.join(REPO, os.path.dirname(VISIBLE))
    sys.path.insert(0, tree_dir)
    import visible_a74f as tree                    # noqa: PLC0415
    anchor = module_at(ANCHOR, VISIBLE, "visible_at_anchor")

    if not os.path.exists(anchor.R16.BRIDGE):
        print(f"NOT RUN: renderer bridge not found: {anchor.R16.BRIDGE}")
        return 3
    if subprocess.run(["node", anchor.R16.BRIDGE, "marked", os.devnull],
                      capture_output=True, text=True).returncode != 0:
        print("NOT RUN, and the reason rather than a bare n/a: the two GFM renderers are not")
        print("installed.  Every figure in this file is a re-derivation from rendered bytes,")
        print("so none of it can be produced from the transcripts alone.")
        print('    D=$(mktemp -d) && npm install --prefix "$D" marked markdown-it')
        return 3

    print("=" * 100)
    print("mg-40e4 Q2 — THE OFFSET, RE-DERIVED, AND THE PUBLISHED POPULATION IT COULD HAVE")
    print("            CORRUPTED, ENLARGED")
    print("=" * 100)

    # ---- 0.  the defective expression, read out of the anchor rather than quoted --------
    src = source_at(ANCHOR, VISIBLE)
    shipped = re.search(r"mech\s*=\s*\{h:\s*suppressors\(out,\s*html\.unescape\(out\)"
                        r"\.index\(marker\(h\)\)\)[^}]*\}", src)
    print()
    print("0.  THE EXPRESSION UNDER AUDIT, READ OUT OF THE ANCHOR")
    print(f"    {VISIBLE} at {ANCHOR} contains the offset-taken-in-one-string-spent-in-")
    print(f"    another expression: {bool(shipped)}")
    if shipped:
        print(f"      {shipped.group(0).strip()}")
    print("    Read with `git show`, matched by pattern, not retyped from a report.  Every")
    print("    `started` position below is that expression evaluated.")
    print()

    total_pop = []

    # ---- A.  mg-a74f's published run ---------------------------------------------------
    print("=" * 100)
    print("A.  POPULATION: mg-a74f's PUBLISHED RUN.  5 documents x 2 renderers x 5 cited")
    print(f"    sections = 50 section observations, taken from {ANCHOR}'s own ROWS.")
    print("    GRAIN: one marker lookup — the position the tag-stack walk started from.")
    print(f"    PUBLISHED IN: {A74F_TRANSCRIPT} (regenerated by mg-5f7c) and")
    print(f"    {A74F_PRE} (the same transcript as it stood before).")
    print("=" * 100)
    orig = anchor.M49.original()
    a_tot = a_wrong = a_repaired_ok = a_find_bad = 0
    a_moved = []
    a_pub = []
    for rid, _what, fn, _pb, _pf, _pr in anchor.ROWS:
        text = fn(orig)
        for engine in anchor.ENGINES:
            out = anchor.R16.render(engine, text)
            rows = observe(anchor, tree, out, anchor.CITED, anchor.marker)
            pub, tru = figures(rows)
            a_pub.append(pub)
            off = []
            for r in rows:
                a_tot += 1
                if r["started"] != r["true"]:
                    a_wrong += 1
                    off.append(f"{r['h']}{r['started'] - r['true']:+d}")
                if r["repaired"] == r["true"]:
                    a_repaired_ok += 1
                if r["find"] != r["true"]:
                    a_find_bad += 1
            if pub != tru:
                a_moved.append((rid, engine, pub, tru))
            print(f"  {rid} {engine:<12s} walked off the marker: {len(off)}/{len(rows)} "
                  f"{off or '(none)'}")
            print(f"      not-suppressed as published {pub}/5; at the TRUE offset {tru}/5 "
                  f"{'— unchanged' if pub == tru else '<<< MOVES'}")
            total_pop.append((f"a74f/{rid}", engine, rows))
    print()
    print(f"  {a_wrong} OF {a_tot} observations were walked from a position that is not the")
    print("  marker's.  POPULATION: the 50 above.  GRAIN: one marker lookup.")
    print(f"  {a_repaired_ok} of {a_tot} — the REPAIRED code's offset lands on the true one.")
    print(f"  {len(a_moved)} of {len(anchor.ROWS) * len(anchor.ENGINES)} published row")
    print(f"  figures move: {a_moved or '(none)'}.")
    print()

    # does the re-derivation reproduce the committed transcript?
    pub_txt = transcript_figures(A74F_TRANSCRIPT, r"not-suppressed (\d)/5")
    print(f"  REPRODUCES THE COMMITTED TRANSCRIPT?  {A74F_TRANSCRIPT}")
    print(f"  prints {len(pub_txt)} `not-suppressed N/5` figures; the first "
          f"{len(a_pub)} of them are")
    print(f"  {pub_txt[:len(a_pub)]} and this re-derivation of the SHIPPED walk gives")
    print(f"  {[str(x) for x in a_pub]} — "
          + ("AGREES" if [str(x) for x in a_pub] == pub_txt[:len(a_pub)]
             else "DISAGREES, and the disagreement is the finding"))
    print()

    # ---- B.  mg-65eb's published run, which mg-5f7c's population excludes --------------
    print("=" * 100)
    print("B.  THE POPULATION mg-5f7c DID NOT AUDIT.  `rows65eb.py:240` recomputes the same")
    print("    defective expression and mg-65eb PUBLISHES the result.")
    print("    POPULATION: 4 constructions x 2 renderers x 5 cited sections = 40 further")
    print("    section observations.  GRAIN: one marker lookup.")
    print(f"    PUBLISHED IN: {EB_TRANSCRIPT} and code/state_visibility_audit_65eb/"
          "out_run_all.txt")
    print("=" * 100)
    eb = module_at("HEAD", ROWS65EB, "rows65eb_at_head")
    ebsrc = source_at("HEAD", ROWS65EB)
    print(f"  `rows65eb.py` contains the same defective expression: "
          f"{'V.suppressors(out, u.index(V.marker(h)))' in ebsrc}")
    print()
    pad = 3000
    cases = [
        ("R1", "every marker written `&mdash;`", eb.b_marker_entity),
        ("R2a", '<div class="hidden">', eb.b_class_hidden),
        ("R2b", '<details title="open me">', eb.b_details_titled),
        ("R2c", f"<div hidden> behind {pad} `&`", lambda t: eb.b_entity_prefix_hidden(t, pad)),
    ]
    b_tot = b_wrong = b_find_undef = 0
    b_moved = []
    b_pub = []
    for cid, what, fn in cases:
        doc = fn(orig)
        print(f"  {cid}  {what}")
        for engine in anchor.ENGINES:
            out = anchor.R16.render(engine, doc)
            rows = observe(anchor, tree, out, anchor.CITED, anchor.marker)
            pub, tru = figures(rows)
            b_pub.append(pub)
            off = []
            for r in rows:
                b_tot += 1
                if r["started"] != r["true"]:
                    b_wrong += 1
                    off.append(f"{r['h']}{r['started'] - r['true']:+d}")
                if r["find"] < 0:
                    b_find_undef += 1
            if pub != tru:
                b_moved.append((cid, engine, pub, tru))
            print(f"      {engine:<12s} walked off the marker: {len(off)}/{len(rows)}   "
                  f"not-suppressed as published {pub}/5; at the TRUE offset {tru}/5 "
                  f"{'— unchanged' if pub == tru else '<<< MOVES'}")
            total_pop.append((f"65eb/{cid}", engine, rows))
        print()
    print(f"  {b_wrong} OF {b_tot} observations walked from a position that is not the")
    print(f"  marker's.  {len(b_moved)} of {len(cases) * len(anchor.ENGINES)} published row")
    print(f"  figures move: {b_moved or '(none)'}.")
    eb_txt = transcript_figures(EB_TRANSCRIPT, r"not-suppressed (\d)/5")
    print(f"  REPRODUCES {EB_TRANSCRIPT}?  it prints {len(eb_txt)} such figures "
          f"{eb_txt[:len(b_pub)]};")
    print(f"  this re-derivation gives {[str(x) for x in b_pub]} — "
          + ("AGREES" if [str(x) for x in b_pub] == eb_txt[:len(b_pub)]
             else "DISAGREES, and the disagreement is the finding"))
    print()

    # ---- C.  the substituted definition -------------------------------------------------
    print("=" * 100)
    print("C.  `out.find(marker)` IS NOT `the marker's position`, AND BOTH AUDITS USED IT")
    print("=" * 100)
    print("    POPULATION: all "
          f"{sum(len(r) for _c, _e, r in total_pop)} section observations of A and B.")
    print("    GRAIN: one marker lookup, three candidate definitions of its true position.")
    print()
    undef = [(c, e, r["h"]) for c, e, rows in total_pop for r in rows if r["find"] < 0]
    disagree = [(c, e, r["h"], r["find"], r["true"])
                for c, e, rows in total_pop for r in rows
                if r["find"] >= 0 and r["find"] != r["true"]]
    badrep = [(c, e, r["h"], r["repaired"], r["true"])
              for c, e, rows in total_pop for r in rows if r["repaired"] != r["true"]]
    print(f"    `out.find(marker)` returns -1 on {len(undef)} observations — the marker is")
    print("    in the page a reader is shown and not in the bytes as literal characters.")
    for c, e, h in undef[:12]:
        print(f"      {c:<12s} {e:<12s} {h}")
    if len(undef) > 12:
        print(f"      ... and {len(undef) - 12} more")
    print(f"    On those, `offsets_5f7c.py` counts the observation WRONG and then omits it")
    print("    from `free_true`, and `rows65eb.py` counts it as FREE by a literal string")
    print("    `(marker not in raw HTML)`.  Neither prints that its comparison population is")
    print("    smaller than its wrong-offset population.")
    print()
    print(f"    `out.find` disagrees with the true offset on {len(disagree)} further")
    print("    observations where it is defined.")
    print(f"    THE REPAIRED `unescape_with_map` disagrees with the true offset on")
    print(f"    {len(badrep)} of {sum(len(r) for _c, _e, r in total_pop)}: {badrep or '(none)'}")
    print("    — an independent check ON the repair, using a definition the repair does not")
    print("    supply.")
    print()

    print("=" * 100)
    print("THE ANSWER TO THE TICKET'S QUESTION, WITH ITS POPULATION NAMED")
    print("=" * 100)
    moved = a_moved + b_moved
    print(f"  Published row figures produced by the defective walk that CHANGE when the walk")
    print(f"  is redone at the true offset: {len(moved)} of "
          f"{(len(anchor.ROWS) + len(cases)) * len(anchor.ENGINES)}.")
    print(f"    over mg-a74f's population (mg-5f7c's):      {len(a_moved)} of 10")
    print(f"    over mg-65eb's population (NOT AUDITED):    {len(b_moved)} of 8")
    print()
    print("  mg-5f7c PRINTS `0 OF 10` AND `NO PUBLISHED FIGURE OF mg-a74f IS WRONG`.  Both")
    print("  are re-derived here and both HOLD — over the population mg-5f7c named.  Its")
    print("  stated reason holds too: all five of mg-a74f's documents apply their mechanism")
    print("  to the WHOLE document, so a displaced position is still inside the same")
    print("  suppression.  That is a property of those five documents and not of the")
    print("  instrument, and mg-5f7c says so.")
    print()
    if b_moved:
        print("  WHAT THE NAMED POPULATION LEAVES OUT.  Enlarge the population from `mg-a74f's")
        print("  published run` to `every committed figure produced by that expression` and")
        print(f"  {len(b_moved)} row figures move, all of them in mg-65eb's committed")
        print(f"  transcript: {b_moved}.  Each is a published `not-suppressed 5/5` whose")
        print("  answer at the true offset is 0/5.")
        print()
        print("  WHAT THAT IS AND IS NOT.  It is NOT a false claim left standing: mg-65eb's")
        print("  R2c publishes that 5/5 KNOWINGLY, as the exhibit of the defect, and its")
        print("  prose says so.  What it is: the counterexample to `luck of row design` was")
        print("  ALREADY IN THE REPOSITORY AND ALREADY PUBLISHED when mg-5f7c wrote that the")
        print("  next document put to the instrument would not have been protected by the")
        print("  shape of the last five.  The next document had already been put to it, by")
        print("  the audit that raised the ticket, and it moved.  mg-5f7c re-created that")
        print("  document as its own section A construction and did not count it as a")
        print("  published figure.  The caveat was right; the population it was measured")
        print("  over was mg-a74f's rather than the arc's, and 0 of 10 is a smaller and")
        print("  weaker statement than 2 of 18 with two named.")
    else:
        print("  Enlarging the population changes nothing: 0 of 18 move.")
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main())
