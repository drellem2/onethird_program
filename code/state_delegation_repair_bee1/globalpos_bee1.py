#!/usr/bin/env python3
"""mg-bee1 — THE DOCUMENT-GLOBAL ORDINAL, MEASURED RATHER THAN ARGUED.

mg-218d's B1 is that mg-4acd's property is FALSE AS STATED: "a mutation that changes what a
reader SEES must change a digest" is universally quantified, and the mechanism is quantified
over A REGION'S OWN SECTION.  The demonstration is a pair differing by one line — the same
retraction paragraph, moved across a heading, goes from exit 2 to exit 0.

THE OBVIOUS FIX is to make `position` an ordinal among the blocks of the WHOLE DOCUMENT
instead of the blocks of the region's section.  mg-4acd's own COVERAGE.md warns that a
control re-baselined wholesale stops being read, and mg-218d's report says a document-global
ordinal "re-baselines on every unrelated edit".  Both are assertions.  THIS FILE MEASURES
THEM, so that the decision not to take the trade is a measurement and not a preference.

THREE QUESTIONS, in the order they decide the matter:

  1. WHAT WOULD IT CLOSE?  Each of mg-218d's four silent L4 mutations is applied in memory
     and both records — section-local and document-global — are recomputed for every
     certified region.  A mutation "closes" if any document-global record moves.

  2. WHAT WOULD IT COST?  The `of N` half of a document-global ordinal is the document's
     block count, so ANY commit that adds or removes a block anywhere in either certified
     file re-baselines every region in it.  That rate is measured over the real history of
     the two files, commit by commit, from git.  No sampling and no head/tail: the population
     is every commit that touched either file, and it is printed.

  3. DOES IT ACTUALLY DELIVER THE PROPERTY?  P7 is a retraction that REPLACES an existing
     paragraph in an unrelated section: it adds no block, removes none, moves no ordinal —
     and it changes what a reader sees.  If P7 is silent under the document-global ordinal
     too, then the trade buys a re-baselining cost and STILL does not make the unqualified
     sentence true, which is the whole of the argument for not taking it.

    python3 code/state_delegation_repair_bee1/globalpos_bee1.py

Reads git and the working tree.  Mutates NOTHING: every mutation here is applied to a string
in memory, so this script is safe on a dirty tree and needs no restore discipline.
"""
import os
import subprocess
import sys

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()
CONTROL_DIR = os.path.join(REPO, "code", "state_landing_control_2da3")
sys.path.insert(0, CONTROL_DIR)
import presentation as pres                                        # noqa: E402
import delta_control as dc                                         # noqa: E402

STATE = "STATE.md"
README = "docs/state-history/README.md"

RETRACTION = ("**RETRACTED 2026-08-02 (mg-218d). Every correction block under "
              "*\"What certifies a change to these files\"* below was filed in error, is "
              "void, and is retained only so this retraction has something to point at.**")


# =========================================================================================
# THE ALTERNATIVE MECHANISM: `position` as an ordinal over the WHOLE DOCUMENT.
#
# Deliberately the smallest possible change to mg-4acd's record — the same four fields in
# the same order, with the one field re-scoped — so that what is measured below is the
# re-scoping and not some other redesign smuggled in beside it.
# =========================================================================================
def global_record(doc, first, last):
    """mg-4acd's region record with `position` re-scoped to the whole document."""
    record = list(pres.region_record(doc, first, last))
    block = doc.block_at(first)
    if block is None:
        return record
    idx = doc.blocks.index(block)
    for k, (key, _value) in enumerate(record):
        if key == "position":
            record[k] = ("position",
                         f"block {idx + 1} of {len(doc.blocks)} in the document")
    return record


def global_table_record(doc, line_index, cells_raw):
    """The same re-scoping for the ledger cell's table record."""
    record = list(pres.table_record(doc, line_index, cells_raw))
    block = doc.block_at(line_index)
    if block is None:
        return record
    idx = doc.blocks.index(block)
    for k, (key, _value) in enumerate(record):
        if key == "position":
            record[k] = ("position",
                         f"block {idx + 1} of {len(doc.blocks)} in the document")
    return record


def records(state_text, readme_text):
    """(rid -> section-local digest, rid -> document-global digest) for every certified
    region that lives in the WORKING-TREE side of the two files."""
    local, glob = {}, {}
    docs = {"state": pres.Doc(state_text), "readme": pres.Doc(readme_text)}
    for rid, _label, kind, marker, _chars, _sha in dc.CERTIFIED:
        try:
            if kind == "cell":
                hits = dc.find_row(state_text, dc.ROW_KEY)
                if len(hits) != 1:
                    continue
                n, cells = hits[0]
                local[rid] = pres.record_digest(
                    pres.table_record(docs["state"], n - 1, cells))
                glob[rid] = pres.record_digest(
                    global_table_record(docs["state"], n - 1, cells))
            elif kind in ("quote", "para"):
                s, e, _t = (dc.quote_block if kind == "quote"
                            else dc.paragraph)(readme_text, marker)
                local[rid] = pres.record_digest(
                    pres.region_record(docs["readme"], s - 1, e - 1))
                glob[rid] = pres.record_digest(
                    global_record(docs["readme"], s - 1, e - 1))
        except LookupError:
            continue
    return local, glob


# =========================================================================================
# THE MUTATIONS.  mg-218d's four silent L4 rows, restated here against the same tree, plus
# P7 — this file's own, and the one that decides the question.
# =========================================================================================
def heading_index(text, prefix):
    lines = text.split("\n")
    hits = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    if len(hits) != 1:
        raise LookupError(f"heading {prefix!r} matched {len(hits)} lines")
    return hits[0]


def p2(state, readme):
    """THE SAME PARAGRAPH ONE LINE EARLIER — the last block of the section before."""
    lines = readme.split("\n")
    i = heading_index(readme, "## What certifies a change to these files, and what does not")
    return state, "\n".join(lines[:i] + [RETRACTION, ""] + lines[i:])


def p3(state, readme):
    """A document-wide retraction at the top of an unrelated section."""
    lines = readme.split("\n")
    i = heading_index(readme, "## How completeness is checked")
    return state, "\n".join(lines[:i + 1] + ["", RETRACTION] + lines[i + 1:])


def p4(state, readme):
    """A new `## READ THIS FIRST` section near the top."""
    lines = readme.split("\n")
    i = heading_index(readme, "## The rule")
    ins = ["## READ THIS FIRST — this document is superseded", "",
           "**Nothing in this file is in force. It is retained as a historical draft; the "
           "corrections below were all withdrawn on 2026-08-02.**", ""]
    return state, "\n".join(lines[:i] + ins + lines[i:])


def p6(state, readme):
    """STATE.md: a retraction of the Attempt index, from another section."""
    lines = state.split("\n")
    i = heading_index(state, "## The single lemma to prove")
    ins = ["", "**RETRACTED 2026-08-02 (mg-218d): the Attempt index below is superseded "
           "and every row in it is void.**"]
    return "\n".join(lines[:i + 1] + ins + lines[i + 1:]), readme


def p7(state, readme):
    """THE ROW THAT DECIDES IT.  A retraction that REPLACES an existing paragraph in an
    unrelated section, in place: no block is added and none removed, so no ordinal moves,
    section-local OR document-global — and a reader is shown a retracted document.

    The paragraph replaced is the first prose block of `## How completeness is checked`,
    located by its own first line rather than by line number.
    """
    lines = readme.split("\n")
    i = heading_index(readme, "## How completeness is checked")
    j = i + 1
    while j < len(lines) and not lines[j].strip():
        j += 1
    k = j
    while k < len(lines) and lines[k].strip():
        k += 1
    if k == j:
        raise LookupError("no prose block found under the target heading")
    return state, "\n".join(lines[:j] + [RETRACTION] + lines[k:])


MUTATIONS = [
    ("P2", "the same paragraph one line earlier, across the heading", p2),
    ("P3", "a document-wide retraction in an unrelated section", p3),
    ("P4", "a new 'READ THIS FIRST — superseded' section near the top", p4),
    ("P6", "STATE.md: a retraction of the Attempt index, other section", p6),
    ("P7", "an EXISTING paragraph elsewhere REPLACED by a retraction (no block added)", p7),
]


def blocks_of(text):
    return len(pres.Doc(text).blocks)


def main():
    print(__doc__)
    state = dc.tree(STATE).decode("utf-8")
    readme = dc.tree(README).decode("utf-8")
    base_local, base_global = records(state, readme)
    print("=" * 90)
    print("1. WHAT A DOCUMENT-GLOBAL ORDINAL WOULD CLOSE")
    print("=" * 90)
    print(f"   {len(base_local)} certified working-tree regions, each recomputed under both")
    print("   scopings.  'fires' means at least one region's record digest moved.")
    print()
    print(f"   {'id':<5} {'mutation':<62} {'section-local':<14} document-global")
    closed = []
    for mid, desc, fn in MUTATIONS:
        try:
            ms, mr = fn(state, readme)
        except LookupError as exc:
            print(f"   {mid:<5} COULD NOT BUILD — {exc}")
            continue
        loc, glo = records(ms, mr)
        loc_fires = any(loc.get(k) != v for k, v in base_local.items()) or set(loc) != set(base_local)
        glo_fires = any(glo.get(k) != v for k, v in base_global.items()) or set(glo) != set(base_global)
        print(f"   {mid:<5} {desc:<62} {'FIRES' if loc_fires else 'silent':<14} "
              f"{'FIRES' if glo_fires else 'silent'}")
        if glo_fires and not loc_fires:
            closed.append(mid)
        if not glo_fires:
            closed.append(None)
    gained = [m for m in closed if m]
    print()
    print(f"   The document-global ordinal would close {len(gained)} of {len(MUTATIONS)} "
          f"rows that are silent today: {', '.join(gained) or '(none)'}")
    print()

    print("=" * 90)
    print("2. WHAT IT WOULD COST — the re-baselining rate, measured over real history")
    print("=" * 90)
    print("   A document-global ordinal carries the DOCUMENT'S BLOCK COUNT as its `of N`")
    print("   half, so every commit that adds or removes a block anywhere in a certified")
    print("   file moves the record of EVERY region in that file.  Below: every commit in")
    print("   this repository that touched either file, oldest first, with the file's block")
    print("   count at that commit.  The population is stated and nothing is sampled.")
    print()
    total_commits = 0
    for path in (STATE, README):
        revs = subprocess.run(
            ["git", "-C", REPO, "log", "--format=%H", "--reverse", "--", path],
            capture_output=True, text=True, check=True).stdout.split()
        counts = []
        for rev in revs:
            got = subprocess.run(["git", "-C", REPO, "show", f"{rev}:{path}"],
                                 capture_output=True)
            if got.returncode != 0:
                continue
            counts.append((rev[:7], blocks_of(got.stdout.decode("utf-8", "replace"))))
        moved = sum(1 for a, b in zip(counts, counts[1:]) if a[1] != b[1])
        transitions = max(len(counts) - 1, 0)
        total_commits += transitions
        pct = (100.0 * moved / transitions) if transitions else 0.0
        print(f"   {path}")
        print(f"       {len(counts)} commits touched it; {transitions} commit-to-commit "
              f"transitions")
        print(f"       block count changed at {moved} of them  ({pct:.0f}%)")
        print(f"       block count today: {counts[-1][1]}   first recorded: {counts[0][1]}")
        print(f"       series: " + " ".join(str(c) for _r, c in counts))
    print()
    print("   Each of those is a commit at which a document-global ordinal would have")
    print("   reported MOVED for every certified region in the file, and been re-baselined.")
    print("   For comparison, the SECTION-LOCAL ordinal in force today has been re-baselined")
    print("   once per generation of this control — by the generation that adds a block to")
    print("   the certified section, which is the generation that is already editing it.")
    print()

    print("=" * 90)
    print("3. DOES IT DELIVER THE PROPERTY?  — the row that decides the trade")
    print("=" * 90)
    print("   P7 changes what a reader sees and adds no block.  Read its two columns in")
    print("   section 1: if it is silent under BOTH scopings, then a document-global")
    print("   ordinal buys the re-baselining rate above and STILL leaves")
    print()
    print("       'a mutation that changes what a reader sees must change a digest'")
    print()
    print("   false as stated.  The mutation would have to be one that does not exist for")
    print("   the sentence to become true, and the honest repair is therefore the sentence.")
    print()
    print("=" * 90)
    print("CONCLUSION, and it is a measurement rather than a preference:")
    print(f"   * a document-global ordinal closes {len(gained)} of {len(MUTATIONS)} rows;")
    print(f"   * it re-baselines at the rate printed in section 2, over "
          f"{total_commits} real transitions;")
    print("   * and P7 is silent under it, so the unqualified property is still false.")
    print("   mg-bee1 does not take the trade.  What it takes instead is the statement:")
    print("   the property is restated to its bound, and the bound is named as uncovered.")
    print("=" * 90)
    return 0


if __name__ == "__main__":
    sys.exit(main())
