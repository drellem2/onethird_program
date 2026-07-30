#!/usr/bin/env python3
"""mg-e1d0 -- re-measure every fact this landing asserts, from the tree and git.

This landing closes mg-3c24, the audit of `1e61031` (mg-a2bd's strike of ledger
row `G"`).  mg-3c24 merged with findings and no successor was ever filed; the
audit-successor detector recovered the drop.  Four findings are landed here.

The mathematics of mg-3c24 is NOT re-opened and nothing below re-derives it:
that audit found 0 BROKEN mathematics and every committed number reproduced
from a disjoint route.  What is re-measured here is the DOCUMENTARY claim set,
because every one of the four findings is a claim a document makes about
itself, about another document, or about a ticket -- and each was wrong.

  T1  THE ENLARGEMENT (F1).  mg-d39d's finding A5 says the deliverable's §14
      asserts the `STATE.md` row "carries the same clauses" and it does not.
      mg-a2bd edited that very paragraph, inserted a sentence asserting the
      row was UNCHANGED, left the false sentence standing, and in the SAME
      commit more than doubled the mismatch A5 reports.  Measured from git at
      every commit in the chain, AND MEASURED AGAIN IN THE WORKING TREE --
      because the `STATE.md` restructure (mg-34bf, `57f962f`) moved the row's
      history out to a per-row file, so the char-gap the finding was OPENED on
      no longer measures what it measured.  A reader of A5 must meet the
      CURRENT gap.

      ⚠️ CORRECTED 2026-07-30 (mg-f922 findings B/C/E/F, landed by mg-8e30).
      THE LIVE ROW OF THIS TABLE READS THE WORKING TREE, NOT `HEAD`, AND THAT
      IS THE WHOLE POINT.  As first written it read the cell from `git show
      HEAD:STATE.md` and the row history from the tree, and it printed HEAD's
      sha.  Run before a commit that edits those files, it therefore measured
      the PRE-EDIT cell -- and mg-e1d0, the landing this instrument ships
      with, wrote the pre-edit figure (−875) into three documents in the same
      commit that added +1 630 characters to the cell being measured.  The
      figure was false the moment it was committed.

      THE GENERAL SHAPE, because the numbers are the smaller half of it:
      WHEN A COMMIT REPORTS A MEASUREMENT OF SOMETHING THAT COMMIT ALSO
      MODIFIES, THE MEASUREMENT MUST BE TAKEN FROM THE POST-COMMIT STATE, AND
      THE DOCUMENT MUST SAY WHICH SIDE OF THE EDIT IT IS ON.  Reading the
      working tree is how an instrument run before `git commit` sees the
      post-commit state; reading `HEAD` is how it sees the parent's.  The
      GATE below no longer string-matches a frozen figure either: it FORMATS
      what it has just measured and requires the documents to carry that.

  T2  TWO SITE COUNTS IN ONE COMMIT (F2).  §6's disposition table is counted
      row by row from the tree; §14's count word is read out of §14.  Neither
      is quoted from the audit.

  T3  THE DROPPED CONDITION (F3).  "the per-level max is attained exactly at
      the one-big-block face" is a conclusion of Theorem J PLUS the base case
      `lambda_2(F(A_m)) <= 1/2`.  Two checks: (a) which of the four sites
      carry the condition, read from the tree; (b) the condition is
      LOAD-BEARING rather than decorative -- re-derived here by evaluating
      Theorem J's closed form over every block-size multiset, under the
      verified base case and under a counterfactual one.  If the argmax is
      the one-big-block face under both, the condition is decorative and F3
      is wrong.  It is not.

  T4  A RULE ABOUT ENUMERATING A BRIEF (F4).  mg-a806's brief has six items;
      the rule's evidence paragraph said four, at two sites.  `STATE.md` was
      corrected by mg-ae62; the deliverable's §13 copy was not.  Both sites
      are read from the tree and reported separately -- a repair that fixed
      one site and left the other is this arc's most-repeated defect, and
      this landing must not report it as closed on one site's evidence.

Pure Python 3 + git.  No third-party packages.  Runtime ~1 s.
"""

import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DELIV = "docs/OneThird-Hodge-Side-Leverage.md"
STATE = "STATE.md"
HIST = "docs/state-history/attempt-mg-a3d4.md"

STRIKE = "1e61031"          # mg-a2bd, the audited commit
RESTRUCTURE = "57f962f"     # mg-34bf, the STATE.md restructure
LANDING = "bbe83b5"         # mg-e1d0, the commit this instrument shipped in
TREE = None                 # sentinel: the WORKING TREE, never a sha

RESULTS = []


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args),
                          capture_output=True, text=True, check=True).stdout


def blob(commit, path):
    """File contents at a commit, or None if it does not exist there."""
    r = subprocess.run(["git", "-C", REPO, "show", f"{commit}:{path}"],
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def tree(path):
    with open(os.path.join(REPO, path), encoding="utf-8") as fh:
        return fh.read()


def find_line(text, prefix):
    """The single line starting with `prefix`.  Located by CONTENT, never by
    line number: the row moves between commits and a frozen index would
    silently measure a different row."""
    hits = [l for l in text.split("\n") if l.startswith(prefix)]
    if len(hits) != 1:
        raise SystemExit(f"expected exactly 1 line starting {prefix!r}, got {len(hits)}")
    return hits[0]


def state_row(text):
    return find_line(text, "| **AMBER-POSITIVE")


def deliv_row(text):
    return find_line(text, "> **AMBER-POSITIVE")


def record(ok, detail):
    RESULTS.append((detail, ok))
    mark = {True: "[CONFIRMED]", False: "[REFUTED  ]", None: "[MEASURED ]"}[ok]
    print(f"  {mark} {detail}")


def head(title):
    print()
    print(title)
    print("-" * len(title))


def doc_num(v, signed=False):
    """A number in the format the documents write it: space thousands
    separator, U+2212 for a negative sign.  Used by the GATE to FORMAT what it
    has just measured and then look for that in the prose -- never to match a
    figure frozen into the source of this file."""
    s = f"{v:+,}" if signed else f"{v:,}"
    return s.replace(",", " ").replace("-", "−")


# --------------------------------------------------------------------------
# T1 -- THE ENLARGEMENT
# --------------------------------------------------------------------------
def t1():
    head("TARGET 1 (F1) -- THE FINDING WAS ENLARGED WHILE A SENTENCE SAID IT WAS UNCHANGED")
    print("""mg-d39d A5 (MODERATE, open): §14 asserts the `STATE.md` row 'carries the
same clauses'; it does not.  mg-a2bd edited that paragraph and did not land A5.
The question this target answers is not whether A5 was landed -- the commit says
three times that it was not -- but whether the same commit ENLARGED it, and
whether the enlargement was disclosed anywhere.
""")

    chain = [(f"{STRIKE}^", "before mg-a2bd"),
             (STRIKE, "after  mg-a2bd"),
             (f"{RESTRUCTURE}^", "before mg-34bf restructure"),
             (RESTRUCTURE, "after  mg-34bf restructure"),
             (f"{LANDING}^", "before mg-e1d0 (this instrument's landing)"),
             (LANDING, "at     mg-e1d0 -- the commit that printed the row ABOVE as current"),
             (TREE, "the WORKING TREE -- this run's own side of the edit")]

    print("  commit-by-commit, all three files located BY CONTENT, not by line")
    print("  number.  The last row is the TREE and is deliberately NOT a sha: a")
    print("  transcript that embeds the commit it happened to be run at can never")
    print("  regenerate at any later one, and reading the tree rather than HEAD is")
    print("  what makes a pre-commit run report the POST-commit state.")
    print()
    print(f"    {'commit':<10} {'STATE.md row':>13} {'row history':>12} "
          f"{'§14 copy':>10} {'gap':>10}  when")
    rows = {}
    for ref, label in chain:
        if ref is TREE:
            st, dl, hs, name = tree(STATE), tree(DELIV), tree(HIST), "tree"
        else:
            st, dl, hs = blob(ref, STATE), blob(ref, DELIV), blob(ref, HIST)
            name = git("rev-parse", "--short", ref).strip()
        a, b = len(state_row(st)), len(deliv_row(dl))
        h = len(hs) if hs is not None else None
        rows[ref] = (a, b, h)
        hcol = f"{h:>12,}" if h is not None else f"{'—':>12}"
        print(f"    {name:<10} {a:>13,} {hcol} {b:>10,} {a - b:>+10,}  {label}")
    print()

    a0, b0, _ = rows[f"{STRIKE}^"]
    a1, b1, _ = rows[STRIKE]
    record(None,
           f"mg-a2bd: STATE.md row {a0:,} -> {a1:,} chars (+{a1 - a0:,}); "
           f"§14 copy {b0:,} -> {b1:,} (+{b1 - b0:,})")
    record(a1 - b1 > 2 * (a0 - b0) - 1 and a0 - b0 == 2928 and a1 - b1 == 6069,
           "the mismatch A5 reports MORE THAN DOUBLED in the commit that edited "
           f"the paragraph: {a0 - b0:,} -> {a1 - b1:,} chars")

    # Both files in one commit?
    touched = git("show", "--name-only", "--format=", STRIKE).split()
    record(STATE in touched and DELIV in touched,
           f"one commit, both files: `{STRIKE}` touches {STATE} and {DELIV}")

    # The inserted sentence, and the sentence left standing.
    d_before, d_after = blob(f"{STRIKE}^", DELIV), blob(STRIKE, DELIV)
    ins = "row below is\nUNCHANGED by mg-a2bd's strike"
    ins_flat = "row below is UNCHANGED by mg-a2bd's strike"
    false_sentence = "the corresponding `STATE.md` row carries the same clauses"

    def has(text, needle):
        return needle in " ".join(text.split())

    record(not has(d_before, ins_flat) and has(d_after, ins_flat),
           "mg-a2bd INSERTED 'the row below is UNCHANGED by mg-a2bd's strike of "
           "G″, and that is a fact rather than an omission'")
    record(has(d_before, false_sentence) and has(d_after, false_sentence),
           "and LEFT STANDING the sentence A5 is about -- "
           f"'{false_sentence}' -- present before and after")

    # Was the enlargement disclosed?  Search the commit message and the tree.
    msg = git("log", "-1", "--format=%B", STRIKE)
    disclosed = re.search(r"A5", msg) and re.search(r"enlarg|widen|doubl|gap", msg, re.I)
    record(not disclosed,
           "the enlargement is NOT disclosed in `%s`'s commit message "
           "(it declares A2-A8 unlanded, which is a different act)" % STRIKE)

    # ---- and now the CURRENT state, which is not the state A5 was opened on.
    print()
    print("  THE CURRENT GAP, MEASURED IN THE TREE THIS RUN IS PART OF -- and the")
    print("  metric A5 was opened on no longer means what it meant, which is")
    print("  itself the thing a reader must be told:")
    print()
    aH, bH, histlen = rows[TREE]
    hist = tree(HIST)
    print(f"    STATE.md row cell                        : {aH:>7,} chars")
    print(f"    relocated per-row history ({os.path.basename(HIST)}) : {histlen:>7,} chars")
    print(f"    STATE.md row, cell + relocated history    : {aH + histlen:>7,} chars")
    print(f"    §14 copy (frozen since mg-a806)           : {bH:>7,} chars")
    print(f"    gap, cell only                            : {aH - bH:>+7,} chars")
    print(f"    gap, cell + relocated history             : {aH + histlen - bH:>+7,} chars")
    print()

    # ⚠️ This line used to read "the SIGN of the cell-only gap has FLIPPED",
    # scored as `aH < bH`, and the three documents printed the −875 it went
    # with.  Both were true at `bbe83b5^` and false at `bbe83b5`, because
    # `bbe83b5` added chars to the cell it was measuring.  The durable claim is
    # not the sign at any one commit -- it is that the char gap moves in BOTH
    # directions while the clause mismatch only grows, which is exactly why a
    # char count cannot stand in for it.  (mg-f922 B/C, landed by mg-8e30.)
    gaps = [rows[r][0] - rows[r][1]
            for r in (f"{STRIKE}^", STRIKE, RESTRUCTURE, f"{LANDING}^", LANDING, TREE)]
    deltas = [g2 - g1 for g1, g2 in zip(gaps, gaps[1:])]
    record(any(d < 0 for d in deltas) and any(d > 0 for d in deltas),
           "the cell-only gap is NON-MONOTONE across the chain ("
           + " -> ".join(f"{g:+,}" for g in gaps)
           + ") while the clause mismatch below only grew -- so a char count "
             "does not measure it, in EITHER direction")
    grew = rows[LANDING][0] - rows[f"{LANDING}^"][0]
    record(rows[f"{LANDING}^"][0] - rows[f"{LANDING}^"][1] == -875 and grew > 0,
           f"and the −875 this instrument's own landing printed as CURRENT is "
           f"the figure at its PARENT: `{LANDING}` added {grew:+,} chars to the "
           "cell it was measuring, so the figure was stale in the commit that "
           "published it -- the defect this instrument exists to check for, "
           "one generation on (mg-f922 B/C)")
    record(None,
           "so this landing records the CLAUSE mismatch, measured below, and "
           "records the char history as history rather than as the live figure")

    # Clause-level probe: clauses asserted in the STATE.md row (cell or its
    # relocated history) and absent from §14.  Probes are phrased as content,
    # not as quotations of the audit.
    probes = [
        ("the one control gap the deliverable named itself is CLOSED",
         ["control gap the deliverable named itself", "CLOSED by the audit"]),
        ("the second-generation audit mg-d39d and its 1 BROKEN item",
         ["SECOND-GENERATION AUDIT"]),
        ("ledger row J / the 48 846 genuine-join links",
         ["48 846", "48 846"]),
        ("row G″ struck, with the mechanism recorded",
         ["G″"]),
        ("the A2-A8 not-landed declaration",
         ["NOT landed"]),
        ("the per-row history links added by the restructure",
         ["row history H1"]),
    ]
    state_all = state_row(tree(STATE)) + "\n" + hist
    d14 = deliv_row(tree(DELIV))
    print("  clause probes -- asserted by the STATE.md row, absent from §14:")
    missing = 0
    for label, needles in probes:
        in_state = any(n in state_all for n in needles)
        in_d14 = any(n in d14 for n in needles)
        if in_state and not in_d14:
            missing += 1
            print(f"    [ONLY IN STATE.md] {label}")
        elif in_state and in_d14:
            print(f"    [IN BOTH         ] {label}")
        else:
            print(f"    [NOT IN STATE.md ] {label}")
    print()
    record(missing >= 5,
           f"{missing} of {len(probes)} probed clauses are asserted by the "
           "STATE.md row and by nothing in §14 -- A5 stands, on clauses rather "
           "than on chars")

    # ---- THE GATE: what this landing leaves in the tree.
    print()
    flat_d_now = " ".join(tree(DELIV).split())
    flat_s_now = " ".join(tree(STATE).split())
    false_now = "the corresponding `STATE.md` row carries the same clauses"
    # It must survive ONLY as a quotation of what was struck, never as an
    # assertion -- a strike that deletes the sentence without trace leaves a
    # reader unable to check what was struck.
    occurrences = flat_d_now.count(false_now)
    quoted = flat_d_now.count('used to end *"and ' + false_now + '"*')
    record(occurrences == 1 and quoted == 1,
           f"GATE: the false sentence is STRUCK -- it appears {occurrences} time "
           f"in §14 and {quoted} of those is inside 'used to end \"...\"', i.e. "
           "quoted as the struck text and asserted nowhere")
    record("2 928 → 6 069" in flat_d_now and "2 928 → 6 069" in flat_s_now,
           "GATE: the enlargement 2 928 -> 6 069 is stated at BOTH the §14 "
           "paragraph and the place A5 is recorded (the STATE.md row)")
    flat_h_now = " ".join(tree(HIST).split())

    # THE FIGURE GATE.  Formatted from the measurement three lines up, never
    # from a constant in this file.  The version this replaced looked for the
    # literal strings "−875" and "+9 608", so it went on passing after the very
    # commit it was gating made both of them false (mg-f922 B/C).  A gate built
    # out of what it has just measured cannot do that: change the cell and the
    # needle changes with it.
    gap_now = doc_num(aH - bH, signed=True)
    both_now = doc_num(aH + histlen - bH, signed=True)
    cell_now, hist_now = doc_num(aH), doc_num(histlen)
    # Anchored on the ROW, not on STATE.md as a whole: A5 is recorded in the
    # row, and a figure that satisfies the gate from somewhere else in the file
    # is not a figure a reader of A5 meets.
    flat_row_now = " ".join(state_row(tree(STATE)).split())
    where = {"the STATE.md row": flat_row_now, "§14": flat_d_now, "H8": flat_h_now}
    hits = {n: gap_now in t for n, t in where.items()}
    record(all(hits.values()) and "row history H8" in flat_row_now,
           f"GATE: the CURRENT cell-only gap, FORMATTED FROM THIS RUN'S OWN "
           f"MEASUREMENT ({gap_now}), is stated at every place A5 is recorded -- "
           + ", ".join(f"{n} {'yes' if v else 'NO'}" for n, v in hits.items()))
    record(cell_now in flat_row_now and hist_now in flat_h_now
           and both_now in flat_row_now and both_now in flat_h_now
           and both_now in flat_d_now,
           f"GATE: and so are the parts it is built from -- cell {cell_now}, "
           f"relocated history {hist_now}, cell + history {both_now}")
    side = "measured AFTER this commit's own edit"
    record(all(side in t for t in where.values()),
           f"GATE: and every site says WHICH SIDE OF THE EDIT its figure is on "
           f"-- '{side}' at all three.  A measurement of something the same "
           "commit modifies is only checkable from the post-commit state")
    record("A5 itself is still NOT landed" in flat_s_now
           and "remains pm-onethird's to size and is NOT done here" in flat_d_now,
           "GATE: and both say A5 is MARKED, not landed -- marking a finding and "
           "landing it are also different acts")


# --------------------------------------------------------------------------
# T2 -- TWO SITE COUNTS
# --------------------------------------------------------------------------
def t2():
    head("TARGET 2 (F2) -- TWO SITE COUNTS IN ONE COMMIT")
    d_at_strike = blob(STRIKE, DELIV)

    def count_table(text):
        """Rows of §6's disposition table, counted from the table itself."""
        lines = text.split("\n")
        start = next(i for i, l in enumerate(lines)
                     if l.startswith("| site | what it was | disposition |"))
        n = 0
        for l in lines[start + 2:]:
            if not l.startswith("|"):
                break
            n += 1
        return n

    def count_word(text):
        flat = " ".join(text.split())
        m = re.search(r"\*\*(\w+) sites, all now carrying the strike", flat)
        return m.group(1) if m else None

    n_rows = count_table(d_at_strike)
    word = count_word(d_at_strike)
    record(None, f"§6 table, counted row by row at `{STRIKE}`: {n_rows} sites")
    record(word is not None and word.lower() == "three" and n_rows == 3,
           f"§6's prose says '{word} sites' and its table has {n_rows} rows -- these agree")

    flat_before = " ".join(blob(f"{STRIKE}^", DELIV).split())
    flat_after = " ".join(d_at_strike.split())
    s14 = "The strike therefore touches §6 and the ledger and nothing else."
    record(s14 not in flat_before and s14 in flat_after,
           "§14's '%s' was added by the SAME commit" % s14)
    record(True,
           "so one commit reports THREE (§6) and TWO (§14) for the same object "
           "-- exactly the shape STATE.md's own Appendix A warns about")

    # ---- THE GATE: the state this landing leaves in the tree.
    d_now = tree(DELIV)
    flat_now = " ".join(d_now.split())
    quoted14 = "used to end `" + s14[0].lower() + s14[1:-1] + "`"
    record(s14 not in flat_now and quoted14 in flat_now,
           "GATE: §14 no longer ASSERTS a second site count -- the sentence "
           "survives only as the quotation of what was struck")
    record(count_table(d_now) == 3 and count_word(d_now).lower() == "three",
           f"GATE: §6 remains the single source, {count_table(d_now)} table rows "
           f"and prose saying '{count_word(d_now)}' -- unchanged by this landing")
    record(flat_now.count("THREE sites, as §6's own") == 1,
           "GATE: §14 now defers to §6's table for the count rather than "
           "carrying an independent one")


# --------------------------------------------------------------------------
# T3 -- THE DROPPED CONDITION
# --------------------------------------------------------------------------
def t3():
    head("TARGET 3 (F3) -- A CONDITION DROPPED IN THE SUMMARY")
    print("""Theorem G gives `lambda_2(F(A_m)) >= 1/2` in BOTH directions and no upper
bound.  Concluding that the per-level max is attained AT the one-big-block face
needs J plus the computational base case `lambda_2(F(A_m)) <= 1/2`.  Part (a):
which sites carry it.  Part (b): whether it is load-bearing.
""")
    d, s = tree(DELIV), tree(STATE)
    flat_d, flat_s = " ".join(d.split()), " ".join(s.split())

    cond_markers = ["lambda_2(F(A_b)) <= 1/2", "λ₂(F(A_b)) ≤ 1/2",
                    "λ₂(F(A_m)) ≤ 1/2", "base case"]

    def carries(segment):
        return any(m in segment for m in cond_markers)

    def near(line, anchor="one-big-block face", span=700):
        k = line.find(anchor)
        return line[max(0, k - span):k + span] if k >= 0 else ""

    def sites(state_text, deliv_text):
        fd = " ".join(deliv_text.split())
        i, j = fd.find("The second consequence:"), fd.find("Why this is structural")
        return [
            ("deliverable §6.1 (the body)", fd[i:j]),
            ("deliverable ledger row G′", find_line(deliv_text, "| **G'** |")),
            ("STATE.md row (the summary)", near(state_row(state_text))),
            ("STATE.md Appendix A tally bullet",
             near(find_line(state_text, "- **Over-wide AND FALSE"))),
        ]

    print("  the four sites, at the audited commit and in the tree this landing leaves:")
    print()
    print(f"    {'site':<36} {'at ' + STRIKE:>14} {'in the tree':>14}")
    before = dict(sites(blob(STRIKE, STATE), blob(STRIKE, DELIV)))
    after = dict(sites(s, d))
    for label in before:
        print(f"    {label:<36} {'carries' if carries(before[label]) else 'DROPS IT':>14}"
              f" {'carries' if carries(after[label]) else 'DROPS IT':>14}")
    print()
    record(sum(1 for v in before.values() if not carries(v)) == 2,
           f"at `{STRIKE}` the condition was carried by the two BODY sites and "
           "dropped by the two SUMMARY sites -- the finding, re-measured")
    record(all(carries(v) for v in after.values()),
           "GATE: all four sites now carry the condition")

    # ---- (b) is the condition load-bearing?
    print()
    print("  IS THE CONDITION LOAD-BEARING?  Theorem J's closed form, evaluated over")
    print("  every block-size multiset of every level of A_n, n <= 9 -- once with the")
    print("  verified base case lambda_2(F(A_b)) = 1/2, once with a counterfactual")
    print("  lambda_2(F(A_4)) = 9/10.  Nothing here is quoted; J is applied.")
    print()

    def multisets(total, maxpart):
        """Partitions of `total` into parts >= 1, each <= maxpart (block excesses)."""
        if total == 0:
            yield ()
            return
        for p in range(min(total, maxpart), 0, -1):
            for rest in multisets(total - p, p):
                yield (p,) + rest

    def lam2(b, base):
        """lambda_2(F(A_b)) for a factor of a link.  b = block size >= 2."""
        return base.get(b, 0.5) if b >= 3 else 0.0

    def scan(base):
        """For each (n, i): the argmax block-size multiset under J."""
        out = {}
        for n in range(4, 10):
            for i in range(0, n - 2):
                D = n - i - 3
                if D < 1:
                    continue
                # non-singleton blocks: excesses (b_j - 1) summing to n-i-2 = D+1
                best, arg = None, None
                for exc in multisets(D + 1, D + 1):
                    blocks = tuple(e + 1 for e in exc)
                    val = max([(bj - 2) / D * lam2(bj, base) for bj in blocks]
                              + [-1.0 / D])
                    if best is None or val > best + 1e-12:
                        best, arg = val, blocks
                out[(n, i)] = (best, arg)
        return out

    true_base = {b: 0.5 for b in range(3, 10)}
    cf_base = dict(true_base)
    cf_base[4] = 0.9

    a = scan(true_base)
    b = scan(cf_base)

    def is_one_big_block(blocks):
        return len(blocks) == 1

    bad_true = [k for k, (v, blk) in a.items() if not is_one_big_block(blk)]
    bad_cf = [k for k, (v, blk) in b.items() if not is_one_big_block(blk)]

    record(not bad_true,
           f"under the verified base case the argmax is the one-big-block face at "
           f"ALL {len(a)} levels of A_4..A_9 -- the claim is TRUE on its population")
    record(bool(bad_cf),
           f"under the counterfactual lambda_2(F(A_4)) = 9/10 it FAILS at "
           f"{len(bad_cf)} of {len(b)} levels, first at "
           f"A_{bad_cf[0][0]}, i = {bad_cf[0][1]}: argmax {b[bad_cf[0]][1]} "
           f"at {b[bad_cf[0]][0]:.3f} > 1/2")
    record(True,
           "so the base case is LOAD-BEARING, not decorative: the summary that "
           "drops it attributes to Theorem J alone a conclusion J does not carry")


# --------------------------------------------------------------------------
# T4 -- THE BRIEF
# --------------------------------------------------------------------------
def t4():
    head("TARGET 4 (F4) -- A RULE ABOUT ENUMERATING A BRIEF, MIS-ENUMERATING ITS BRIEF")
    flat_s = " ".join(tree(STATE).split())
    flat_d = " ".join(tree(DELIV).split())

    four = "mg-a806 was scoped to land B6, the stronger scope sentence, N1's label and the §10 table"
    six_s = "mg-a806 was scoped to land **six** things"
    six_d = "mg-a806 was scoped to land **six** items"

    # The finding, re-measured at the audited commit rather than quoted.
    fs_at, fd_at = (" ".join(blob(STRIKE, STATE).split()),
                    " ".join(blob(STRIKE, DELIV).split()))
    four_s = ("mg-a806 was scoped to land four things: ledger row B6, the "
              "stronger replacement scope sentence, N1's label, and the §10 table")
    record(four_s in fs_at and four in fd_at,
           f"at `{STRIKE}` BOTH sites enumerate FOUR (ledger row B6, the scope "
           "sentence, N1's label, the §10 table) -- against a ticket with six. "
           "Two sites, worded differently, wrong the same way")

    record(six_s in flat_s and "four things" in flat_s,
           "STATE.md Appendix A: corrected to six by mg-ae62, and its correction "
           "note still names the old 'four things' -- the site is right and the "
           "record of it having been wrong survives")
    record(six_d in flat_d and four not in flat_d,
           "GATE: deliverable §13 now enumerates SIX (B1-B6) -- the second site, "
           "left uncorrected by mg-ae62, closed here")
    record(True,
           "F4 was HALF-landed for a generation: mg-ae62 fixed the site it found "
           "by quoting it and the other stood.  A repair covering only the "
           "instance already known is this arc's most-repeated defect, so this "
           "is reported as half-landed rather than as new")

    # The conclusion the enumeration supports is checked independently.
    record("none of the six" in flat_d
           or "G″ is none of the six" in flat_s,
           "the CONCLUSION survives at both sites: G″ is none of mg-a806's "
           "items, whether the count is written four or six")


# --------------------------------------------------------------------------
# NEGATIVE CONTROL -- can the new figure gate fail?
# --------------------------------------------------------------------------
def negative_control():
    """The gate this replaced could NOT fail on the thing it existed to catch:
    it matched the literal string `−875`, so the commit that made −875 false
    left it passing.  A replacement gate is worth nothing unless it is shown to
    fire, so each mutation below is applied IN MEMORY with its expected verdict
    written down first.  Nothing on disk is touched."""
    head("NEGATIVE CONTROL -- THE FIGURE GATE, MUTATED")
    print("""The gate this replaced string-matched `−875` and therefore survived the
commit that falsified it.  This one formats what it has just measured, so a
change to the measured object must break it.  Four mutations, verdicts written
before the run.  Nothing is written to disk.
""")
    a = len(state_row(tree(STATE)))
    b = len(deliv_row(tree(DELIV)))
    h = len(tree(HIST))
    docs = {"the STATE.md row": " ".join(state_row(tree(STATE)).split()),
            "§14": " ".join(tree(DELIV).split()),
            "H8": " ".join(tree(HIST).split())}

    def gate(cell, hist, texts):
        """The live gate, parameterised on the measurement and the documents."""
        gap = doc_num(cell - b, signed=True)
        both = doc_num(cell + hist - b, signed=True)
        return (all(gap in t for t in texts.values())
                and doc_num(cell) in texts["the STATE.md row"]
                and doc_num(hist) in texts["H8"]
                and both in texts["the STATE.md row"] and both in texts["H8"])

    cases = [
        ("M1  the cell grows by one char after the figure was taken",
         "GATE FIRES", lambda: gate(a + 1, h, docs)),
        ("M2  the row history grows (cell+history figure goes stale)",
         "GATE FIRES", lambda: gate(a, h + 1, docs)),
        ("M3  one site drops the gap figure (H8)",
         "GATE FIRES", lambda: gate(a, h, dict(docs, **{"H8": docs["H8"].replace(doc_num(a - b, signed=True), "")}))),
        ("M4  unmutated -- the tree as it stands",
         "gate passes", lambda: gate(a, h, docs)),
    ]
    print(f"    {'mutation':<58}{'predicted':<20}{'observed'}")
    ok = True
    for name, predicted, fn in cases:
        fired = not fn()
        observed = "GATE FIRES" if fired else "gate passes"
        agree = observed == predicted
        ok = ok and agree
        print(f"    {name:<58}{predicted:<20}{observed}"
              f"{'' if agree else '   <-- DISAGREES'}")
    print()
    record(ok, "4 of 4 mutations moved the gate as predicted -- the figure gate "
               "is falsifiable by exactly the edit that defeated the one it "
               "replaces (a change to the object being measured)")


def main():
    print("mg-e1d0 -- RE-MEASURING THIS LANDING'S OWN CLAIMS")
    print("=" * 78)
    print("""Nothing below is inherited from mg-3c24 or from the ticket.  mg-3c24's
MATHEMATICS is not re-opened: it found 0 BROKEN and every number reproduced
from a disjoint route.  What is measured here is the four DOCUMENTARY findings,
each of which is a claim a document makes about itself, another document, or a
ticket.  All four are measured from git and the tree.

Note on regeneration, stated because it is the same caveat mg-7d5a recorded,
and CORRECTED 2026-07-30 (mg-f922 B/C/E/F, landed by mg-8e30): T1's live row,
T2's tree line and T4 measure the WORKING TREE, so they describe the state the
commit containing this run LEAVES BEHIND -- not `HEAD`, which during a run
taken before `git commit` is that commit's PARENT.  That distinction is the
whole of mg-f922 B: the version of this file that shipped with mg-e1d0 read
`HEAD`, so it published the pre-edit figure as the current one in the commit
that made it stale.  Nothing here embeds a sha of its own.""")

    t1()
    t2()
    t3()
    t4()
    negative_control()

    head("BOTTOM LINE")
    bad = [t for t, ok in RESULTS if ok is False]
    print(f"  checks recorded : {len(RESULTS)}")
    print(f"  measurements    : {sum(1 for _, ok in RESULTS if ok is None)}")
    print(f"  confirmed       : {sum(1 for _, ok in RESULTS if ok is True)}")
    print(f"  refuted         : {len(bad)}")
    print()
    if bad:
        print("  REFUTED, which for this instrument means a claim this landing")
        print("  makes did not hold and the prose must not be written:")
        for t in bad:
            print(f"    - {t}")
        return 1
    print("  All four findings are measured and all four stand.  F4 stands as")
    print("  HALF-landed -- mg-ae62 fixed the STATE.md site and left the")
    print("  deliverable's; this landing closes the second.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
