#!/usr/bin/env python3
"""mg-ea0e: execute pm-onethird's THREE-MOVE relocation spec on `STATE.md`.

This is a MECHANICAL builder.  It exercises no editorial judgement about what is
load-bearing: pm-onethird made those calls in the spec on mg-ea0e and they are its calls
to make.  Every byte this script moves is moved VERBATIM; the only text it composes is
the link boilerplate left at each site, plus the one short current-position paragraph the
spec explicitly asks for at the *Where the threads converge* site.

The three moves, from the spec:

  MOVE 1  Appendix A ("Audit-stage process", durable home for mg-3a3a)
          -> docs/audit-stage-process.md, whole and unedited; one link line left behind.
  MOVE 2  "Where the threads converge"
          -> docs/state-history/threads-chronology.md, whole and unedited; a short
             current-position paragraph plus the link left behind.
  MOVE 3  The oversize attempt-index cells (every row longer than the spec's own 2,000
          character acceptance threshold: rows :130-:136)
          -> APPENDED to their EXISTING docs/state-history/attempt-<id>.md files, which
             mg-34bf created.  Each row keeps its status label, its own opening sentence
             verbatim, and a link.

Run from the repo root:  python3 code/state_restructure_ea0e/build.py
Verify with:             python3 code/state_restructure_ea0e/verify_relocation_ea0e.py
"""
import io, os, sys

STATE = "STATE.md"

# ---------------------------------------------------------------------------
# MOVE 1 — Appendix A.
#
# The spec names the block "APPENDIX A, lines 180-382".  Line 382 is the HEADER
# `### Why 1/3 - the elementary anchor (proven)`, whose body is lines 383-386, so taking
# the range literally would separate a header from its body and orphan four lines of
# proven mathematics under a heading that had moved.  The block is therefore moved as
# lines 180-381 -- Appendix A's body, up to but excluding that header -- and the
# `### Why 1/3` section, which is proven mathematics and is named by none of the three
# moves, stays in STATE.md untouched.  THIS IS THE ONE PLACE THIS SCRIPT DEPARTS FROM THE
# SPEC'S LINE NUMBERS; it is reported to pm-onethird and to mayor, and reverting it is a
# one-line change of APPENDIX_LAST.
APPENDIX_FIRST, APPENDIX_LAST = 180, 381

# MOVE 2 — the chronology, header included (the header becomes the moved file's subject).
THREADS_FIRST, THREADS_LAST = 142, 177

# MOVE 3 — the oversize attempt-index rows, and the sentence each keeps.
#
# `keep_through` is a VERBATIM tail of the sentence retained in the row; the builder cuts
# at `cell.index(keep_through) + len(keep_through)`, so the retained text is the cell's
# own characters and cannot drift.  The retained sentence is in every case the cell's
# OPENING sentence.  Row :133 is the single exception and it keeps TWO sentences: its
# opening sentence states a condition that its own next sentence records as DISCHARGED,
# and mg-34bf's convention for these files is that a row must not be able to assert a
# claim its own cell records as superseded.  Dropping the discharge marker to the history
# file would leave a superseded condition standing unmarked in the index.  That, too, is
# reported rather than decided quietly.
ROWS = {
    130: ("docs/state-history/attempt-mg-210d.md", "proves = `0`.**"),
    131: ("docs/state-history/attempt-mg-a58f.md", "forces `E[inv_e] ≤ Cn`."),
    132: ("docs/state-history/attempt-mg-88bd.md", "not just the form.**"),
    133: ("docs/state-history/attempt-mg-63e3.md",
          "not because the restriction still binds."),
    134: ("docs/state-history/attempt-mg-3af9.md",
          "and **every** `F(ε) = o(ε)` included."),
    135: ("docs/state-history/attempt-mg-276d.md",
          "is carried by a PROOF, and the proof is sound.**"),
    136: ("docs/state-history/attempt-mg-a3d4.md",
          "THE `2^{Θ(n)}` LOSS IS A THEOREM.**"),
}

APPENDIX_DOC = "docs/audit-stage-process.md"
THREADS_DOC = "docs/state-history/threads-chronology.md"

APPENDIX_HEADER = """# Audit-stage process (durable home for mg-3a3a)

**Relocated whole and unedited out of `STATE.md` Appendix A by mg-ea0e, 2026-08-06**, on
pm-onethird's relocation spec (mg-ea0e): *relocation, not deletion*.  It was 52% of
`STATE.md` and more words than the entire mathematical content of the file, and it is
durable PROCESS documentation rather than state of the programme.  Nothing below was
rewritten, condensed, summarised, reordered or dropped — it is Appendix A's own text,
character for character, from `STATE.md` at `{base}`.  `STATE.md` links here from the site
it left.

---

"""

THREADS_HEADER = """# Where the threads converge — the chronology

**Relocated whole and unedited out of `STATE.md` by mg-ea0e, 2026-08-06**, on
pm-onethird's relocation spec (mg-ea0e): *relocation, not deletion*.  This section is a
CHRONOLOGICAL LOG — one dense paragraph per attempt, in the order the attempts landed —
and history read as state is what made `STATE.md` unreadable.  Nothing below was
rewritten, condensed, summarised, reordered or dropped; it is the section's own text,
character for character, from `STATE.md` at `{base}`, header included.

`STATE.md` keeps, at the site this left, a short paragraph stating only the CURRENT
position — which levers are live, which are retired — and a link here.  **Where the two
disagree, this file is the record of what was said when, and `STATE.md` is the record of
what is true now.**

---

"""

THREADS_REPLACEMENT = """### Where the threads converge

**Current position (2026-08-06).** Three residuals stand, correctly ordered (mg-a58f,
audited mg-d112): **(B-cov)** — *"break the wrong-signed same-side covariance"* (FKG/XYZ
force it `≥ 0`), *"the sharp edge"*, and the object three separate routes converge on;
**(R)** — *"do frozen posets have a density ceiling `d(P) ≤ D < 1`?"* (mg-210d),
elementary, and reopened *quantitatively* by mg-88bd as `D ≤ ε_spec`: *"a door recorded as
the wrong shape is now the right shape with the wrong size"*; and **(EQ)** —
`max_x |E[pos_σ x] − rank_e x| = O(1)`, elementary, *"the only one of the three that is a
cancellation statement rather than a decay statement"*. **Retired or dead:** the *"external
k=1 stability tool"* for Stanley's inequality (refuted, mg-dcae — the reduction to it was
circular, so any usable statement *"must consume the frozen hypothesis directly"*);
mg-0ed7's `Φ→Var` reduction (**REFUTED**, mg-8f56); and the tempering/deformation route to
the BK gap (dead *"for method reasons, not because the conjecture is false"*, mg-4a86).
**Also open, beside the three:** **(RD)** — which reading branch (ii) carries (mg-3af9) —
and the hole mg-3af9 opened at **Step 6** of the architecture, *"independent of L1b"*.

*Every paragraph of the chronology this replaces, verbatim and in order — mg-a1ec, mg-48ab,
mg-dcae, mg-210d, mg-0ed7, mg-4a86, mg-8f56, mg-a58f, mg-88bd, mg-63e3, mg-3af9:*
[`docs/state-history/threads-chronology.md`](docs/state-history/threads-chronology.md).

"""

APPENDIX_REPLACEMENT = """## Appendix A — Audit-stage process (durable home for mg-3a3a)

Audit-stage process: see [`docs/audit-stage-process.md`](docs/audit-stage-process.md)
(standing process, Daniel directive 2026-07-19). Relocated whole and unedited by mg-ea0e,
2026-08-06 — it is durable process documentation, not state of the programme.

"""

CELL_APPEND = """
---

## Full cell text before the mg-ea0e relocation (2026-08-06)

Appended by **mg-ea0e**, 2026-08-06, on pm-onethird's relocation spec, which finishes here
the convention mg-34bf started: **relocation, not deletion**.  The `STATE.md` row now
carries its status label, its own opening sentence verbatim, and a link to this file.

**Everything below is that ledger cell's ENTIRE text as it stood immediately before that
edit** — all three columns, character for character, from `STATE.md` at `{base}`.  Nothing
was rewritten, condensed, summarised or dropped.  Passages mg-34bf had already relocated
appear above under `H1`…; they recur below only because this is the whole cell, and the
sentence the row retained appears below as well, in its place.

### Status-label column, verbatim

> {c1}

### Attempt column, verbatim

> {c2}

### Result column, verbatim

{c3}
"""


def split_row(line):
    """Split a markdown table row on UNESCAPED pipes (cells contain `\\|`)."""
    parts, buf, i = [], [], 0
    while i < len(line):
        if line[i] == "\\" and i + 1 < len(line):
            buf.append(line[i:i + 2]); i += 2; continue
        if line[i] == "|":
            parts.append("".join(buf)); buf = []; i += 1; continue
        buf.append(line[i]); i += 1
    parts.append("".join(buf))
    return parts


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "78ae4d9"
    src = io.open(STATE, encoding="utf-8").read()
    lines = src.split("\n")

    def L(n):                      # 1-indexed line access
        return lines[n - 1]

    report = []

    # ---- MOVE 3 first: it edits inside lines 1-141, which the later moves do not touch.
    new_lines = list(lines)
    for n, (dest, keep_through) in sorted(ROWS.items()):
        row = L(n)
        cols = split_row(row)
        assert len(cols) == 5 and cols[0] == "" and cols[4] == "", (n, len(cols))
        c1, c2, c3 = (c.strip() for c in cols[1:4])
        assert keep_through in c3, (n, keep_through)
        cut = c3.index(keep_through) + len(keep_through)
        kept = c3[:cut]
        link = ("**Full record — this cell's entire text as it stood, verbatim:** "
                "[`{d}`]({d}).".format(d=dest))
        new_lines[n - 1] = "| {c1} | {c2} | {kept} {link} |".format(
            c1=c1, c2=c2, kept=kept, link=link)

        with io.open(dest, "a", encoding="utf-8") as fh:
            fh.write(CELL_APPEND.format(base=base, c1=c1, c2=c2, c3=c3))
        report.append("MOVE 3  row :{n}  cell {old} -> {new} chars, {moved} chars appended "
                      "to {dest}".format(n=n, old=len(c3), new=len(kept), moved=len(c3),
                                         dest=dest))

    # ---- MOVE 1 and MOVE 2: replace line ranges, bottom-up so numbering holds.
    appendix_block = "\n".join(lines[APPENDIX_FIRST - 1:APPENDIX_LAST])
    threads_block = "\n".join(lines[THREADS_FIRST - 1:THREADS_LAST])

    with io.open(APPENDIX_DOC, "w", encoding="utf-8") as fh:
        fh.write(APPENDIX_HEADER.format(base=base) + appendix_block + "\n")
    with io.open(THREADS_DOC, "w", encoding="utf-8") as fh:
        fh.write(THREADS_HEADER.format(base=base) + threads_block + "\n")
    report.append("MOVE 1  STATE.md :{a}-:{b} ({n} chars) -> {d}".format(
        a=APPENDIX_FIRST, b=APPENDIX_LAST, n=len(appendix_block), d=APPENDIX_DOC))
    report.append("MOVE 2  STATE.md :{a}-:{b} ({n} chars) -> {d}".format(
        a=THREADS_FIRST, b=THREADS_LAST, n=len(threads_block), d=THREADS_DOC))

    out = (new_lines[:APPENDIX_FIRST - 1]
           + APPENDIX_REPLACEMENT.split("\n")[:-1]
           + new_lines[APPENDIX_LAST:])
    out = (out[:THREADS_FIRST - 1]
           + THREADS_REPLACEMENT.split("\n")[:-1]
           + out[THREADS_LAST:])

    io.open(STATE, "w", encoding="utf-8").write("\n".join(out))
    for line in report:
        print(line)
    print("STATE.md {} -> {} chars".format(len(src), len("\n".join(out))))


if __name__ == "__main__":
    main()
