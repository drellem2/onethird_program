"""B8 — THE TICKET'S §5, MEASURED: did the relocation move the answer, or move the noise?

The ticket asks me to read the new STATE.md cold and answer "is there a Cheeger/spectral-gap
route to 1/3-2/3, and what have we proven?" — the question that defeated two expert readers
against the old file on 2026-08-05.  The reading is prose and lives in README.md.

This script measures the thing the reading cannot: WHERE the answer sits, in both files.  It
matters because lines 1-129 are byte-identical, which forces a conclusion the byte accounting
cannot reach — the relocation did not move the answer one character.  Everything it changed is
the DENOMINATOR.  If the summary now works, it works by deleting distance, not by rewriting.
"""

import libb0ae as L

L.hdr("B8  WHERE THE ANSWER SITS — the same content, two denominators")

old_t = L.text(L.git_show(L.OLD_REV, "STATE.md"))
new_t = L.text(L.git_show(L.NEW_REV, "STATE.md"))
old_lines, new_lines = old_t.split("\n"), new_t.split("\n")

# The answer-bearing spans, located by content rather than asserted by line number.
NEEDLES = {
    "the one-paragraph state": "## The one-paragraph state",
    "L1b stated as the wall": "**L1b (the wall):**",
    "the proof chain diagram": "```mermaid",
    "'Two links are open'": "Two links are open",
    "the full ledger header": "### Full ledger",
    "Cheeger/Buser row (row 5)": "easy/Buser",
    "the single lemma section": "## The single lemma to prove",
}

print("  %-28s %8s %8s   %s" % ("span", "old:", "new:", "moved?"))
last = 0
for name, needle in NEEDLES.items():
    o = next((i + 1 for i, l in enumerate(old_lines) if needle in l), None)
    n = next((i + 1 for i, l in enumerate(new_lines) if needle in l), None)
    last = max(last, n or 0)
    print("  %-28s %8s %8s   %s" % (name, o, n, "NO" if o == n else "yes"))

POPQ = ("the %d line-anchored spans a reader needs in order to answer 'is there a "
        "Cheeger/spectral route, and what is proven'" % len(NEEDLES))
L.row("spans that changed line number", 0 if all(
    next((i + 1 for i, l in enumerate(old_lines) if nd in l), None) ==
    next((i + 1 for i, l in enumerate(new_lines) if nd in l), None) for nd in NEEDLES.values())
    else sum(1 for nd in NEEDLES.values()
             if next((i + 1 for i, l in enumerate(old_lines) if nd in l), None) !=
             next((i + 1 for i, l in enumerate(new_lines) if nd in l), None)),
      POPQ, "spans — a non-zero value would mean the relocation repositioned the answer")

L.row("last line the answer needs", last, POPQ, "1-based line number, identical in both files")

ans_bytes = len("\n".join(new_lines[:last]).encode())
L.row("answer-bearing prefix", L.commas(ans_bytes), "lines :1-%d of either file" % last,
      "utf-8 bytes — the SAME bytes in both, since :1-129 are byte-identical")

L.hdr("B8.1  THE DENOMINATOR IS THE WHOLE CHANGE")
L.row("answer as a share of OLD file, by lines", "%.0f%%" % (100.0 * last / len(old_lines)),
      "the %d lines of old STATE.md" % len(old_lines), "percent of lines a reader must survive")
L.row("answer as a share of NEW file, by lines", "%.0f%%" % (100.0 * last / len(new_lines)),
      "the %d lines of new STATE.md" % len(new_lines), "percent")
L.row("answer as a share of OLD file, by bytes", "%.0f%%" % (100.0 * ans_bytes / len(old_t.encode())),
      "the %s bytes of old STATE.md" % L.commas(len(old_t.encode())), "percent")
L.row("answer as a share of NEW file, by bytes", "%.0f%%" % (100.0 * ans_bytes / len(new_t.encode())),
      "the %s bytes of new STATE.md" % L.commas(len(new_t.encode())), "percent")
L.row("bytes a reader passes AFTER the answer, old",
      L.commas(len(old_t.encode()) - ans_bytes), "old STATE.md", "utf-8 bytes")
L.row("bytes a reader passes AFTER the answer, new",
      L.commas(len(new_t.encode()) - ans_bytes), "new STATE.md", "utf-8 bytes")

L.hdr("B8.2  IS THE SUMMARY CURRENT?  (a corpus question, not mg-ea0e's)")
recent = ["mg-2de0", "mg-00b9", "mg-c3ca", "mg-1abe", "mg-ea0e"]
head_new = L.text(L.sh(["git", "show", "HEAD:STATE.md"]))
L.row("STATE.md unchanged since the audited commit", head_new == new_t,
      "STATE.md at HEAD vs at %s" % L.NEW_REV,
      "boolean — if False every figure in this suite is about a superseded file")
for i in recent:
    when = L.sh(["git", "log", "--oneline", "-1", "--grep", i]).decode().split()
    print("      %-9s named in STATE.md: %-5s   landed at: %s"
          % (i, i in head_new, when[0] if when else "n/a"))
L.row("work items landed on main and NOT named in STATE.md",
      sum(1 for i in recent if i not in head_new),
      "the %d most recent work-item ids visible in `git log` on main" % len(recent),
      "ids — a staleness measure of the SUMMARY, caused by later commits, not by mg-ea0e")

print("\nB8 DONE")
