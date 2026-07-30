"""Apply the mg-34bf relocation to STATE.md and emit the per-row history files.

Loss-free by construction: every passage of every restructured cell is emitted exactly
once, either into the rewritten row or into that row's history file.  The script asserts
the partition before writing anything.  Run from the repo root.
"""
import os, sys, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cells import split_row, join_row, split_passages
from spec import SPEC, CHECKS

HIST_DIR = "docs/state-history"

HDR = """# {title}

Per-row history for {row_ref}.
Split out of the ledger cell by mg-34bf, 2026-07-30.

Every passage below was **moved verbatim** out of that cell. Nothing was rewritten,
condensed, summarised or dropped, and no citation was changed. The row now asserts current
state and points here; `code/state_restructure_34bf/verify_relocation.py` checks, clause by
clause against the pre-restructure `STATE.md`, that every clause of the old cell is still
present in the row or in this file. See [`README.md`](README.md) for the convention.

"""

SEC_HISTORY = """## Corrections, retractions, supersessions and mechanism notes

*Why this section exists: a ledger row must not be able to contain a claim and its own
retraction. The row states what is true now; what it used to say, what was struck, and why,
is here. Sections are numbered `H1`, `H2`, … and the row cites them by number.*

"""

SEC_SUPPORT = """## Supporting record — derivations, constructions, evidence and audit provenance

*These passages support claims the row still states. They moved so that the row reads as an
assertion rather than as an argument. **No claim moved with them**; where a passage carried
both a claim and its evidence it stayed in the row.*

"""


def emit(buf, passages, keys):
    """Write passages as paragraphs, but keep a bold span that straddles two passages in
    one paragraph -- otherwise markdown would render the dangling `**` literally.  The
    join is the single space the ledger cell itself had, so the text stays verbatim."""
    para, depth = [], 0
    for k in keys:
        t = passages[k].strip()
        para.append(t)
        depth += t.count("**")
        if depth % 2 == 0:
            buf.write(" ".join(para) + "\n\n")
            para = []
    if para:
        buf.write(" ".join(para) + "\n\n")


def build(state_path="STATE.md", write=True):
    lines = open(state_path, encoding="utf-8").read().split("\n")
    report = []

    for lineno, sp in sorted(SPEC.items()):
        line = lines[lineno - 1]
        cols = split_row(line)
        assert join_row(cols) == line

        passages, order = {}, []
        for ci, cell in enumerate(cols):
            if not cell.strip():
                continue
            for pi, p in enumerate(split_passages(cell)):
                key = f"{ci}.{pi}"
                passages[key] = p
                order.append(key)

        for k, want in CHECKS[str(lineno)].items():
            assert k in passages, f"line {lineno}: guard names unknown passage {k}"
            got = passages[k].strip()[:len(want)]
            assert got == want, (
                f"line {lineno}: passage {k} no longer starts with the guarded text.\n"
                f"  expected: {want!r}\n  found:    {got!r}\n"
                "The passage splitter changed; re-derive the spec, do NOT edit the guard.")

        hist, supp = list(sp["history"]), list(sp["support"])
        for k in hist + supp:
            assert k in passages, f"line {lineno}: unknown passage {k}"
        assert len(set(hist + supp)) == len(hist) + len(supp), f"line {lineno}: duplicate key"
        moved = set(hist + supp)

        anchors = [(k, label, stmt) for k, label, stmt in sp["inserts"]]
        for k, _, stmt in anchors:
            assert stmt is None or stmt.count("**") % 2 == 0, \
                f"line {lineno}: pointer at {k} has an unbalanced bold span"

        for k, _, _ in anchors:
            assert k in passages, f"line {lineno}: anchor at unknown passage {k}"
        anchor_keys = [k for k, _, _ in anchors]
        anchor_pos = {k: order.index(k) for k in anchor_keys}
        # every relocated history passage must sit at or after the first anchor
        for k in hist:
            assert order.index(k) >= min(anchor_pos.values()), \
                f"line {lineno}: history passage {k} precedes every anchor"

        def group_of(key):
            best = None
            for a in anchor_keys:
                if anchor_pos[a] <= order.index(key):
                    best = a
            return best

        # ---- rebuild the row -------------------------------------------------
        stmt_by_anchor = {k: (i + 1, label, stmt) for i, (k, label, stmt) in enumerate(anchors)}
        new_cols = []
        for ci, cell in enumerate(cols):
            if not cell.strip():
                new_cols.append(cell)
                continue
            out = []
            for pi, p in enumerate(split_passages(cell)):
                key = f"{ci}.{pi}"
                if key in stmt_by_anchor:
                    n, label, stmt = stmt_by_anchor[key]
                    if stmt is not None:
                        out.append(f"{stmt} — [row history H{n}]({HIST_DIR}/{sp['file']}). ")
                if key not in moved:
                    out.append(p)
            new_cols.append("".join(out))

        # every row links to its history file at least once, and the trailing pointer makes
        # the supporting-record section reachable even from a row that cites no H-section.
        tail_col = max(range(len(cols)), key=lambda i: len(cols[i]))
        new_cols[tail_col] = new_cols[tail_col].rstrip() + (
            f" *(Full per-row record — every passage relocated from this cell, verbatim: "
            f"[`{HIST_DIR}/{sp['file']}`]({HIST_DIR}/{sp['file']}).)* ")
        new_line = join_row(new_cols)

        # markup balance: an odd count of `**` means a relocation cut a bold span in half
        for label, before, after in (("row", cols[tail_col], new_cols[tail_col]),):
            if before.count("**") % 2 == 0 and after.count("**") % 2 == 1:
                raise AssertionError(
                    f"line {lineno}: relocation split a bold span in the {label} cell")

        # ---- history file ----------------------------------------------------
        buf = io.StringIO()
        buf.write(HDR.format(title=sp["title"], row_ref=sp["row_ref"]))
        if hist:
            buf.write(SEC_HISTORY)
            for i, (k, label, stmt) in enumerate(anchors):
                members = [x for x in order if x in hist and group_of(x) == k]
                if not members:
                    continue
                buf.write(f"### H{i + 1} — {label}\n\n")
                emit(buf, passages, members)
        if supp:
            buf.write(SEC_SUPPORT)
            emit(buf, passages, [m for m in order if m in supp])

        emitted = set()
        for i, (k, _, _) in enumerate(anchors):
            emitted |= {x for x in hist if group_of(x) == k}
        emitted |= set(supp)
        assert emitted == moved, f"line {lineno}: partition lost {moved - emitted}"

        if write:
            lines[lineno - 1] = new_line
            os.makedirs(HIST_DIR, exist_ok=True)
            with open(os.path.join(HIST_DIR, sp["file"]), "w", encoding="utf-8") as fh:
                fh.write(buf.getvalue().rstrip() + "\n")

        report.append((lineno, sp["file"], max(len(c) for c in cols),
                       max(len(c) for c in new_cols), len(line), len(new_line)))

    if write:
        open(state_path, "w", encoding="utf-8").write("\n".join(lines))

    print(f"{'line':>5}  {'history file':<32} {'largest cell':>20}  {'row line':>20}")
    for lineno, f, oc, nc, ol, nl in report:
        print(f"{lineno:>5}  {f:<32} {oc:>8} -> {nc:<8}  {ol:>8} -> {nl:<8}")
    return report


if __name__ == "__main__":
    build(write="--dry-run" not in sys.argv)
