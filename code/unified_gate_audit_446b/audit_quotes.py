#!/usr/bin/env python3
"""mg-446b, target 1: FIDELITY of the L1 answer in docs/OneThird-Unified-Framework-Gate.md.

Three checks, none of them trusting the gate document's own account of what it quoted:

 (1) every block quote in the gate doc is matched line-by-line against the cited
     source (docs/OneThird-Hodge-Side-Leverage.md) and against the mg-86a3 audit,
     after stripping markdown quote markers from BOTH sides -- the source's own
     Proposition N2 is itself inside a blockquote, so a naive comparison misses it;
 (2) every line-number citation the gate doc makes is dereferenced and printed;
 (3) inline quoted fragments are searched in the whole-document normalised text
     (not line by line), so a fragment spanning a line break is still found --
     which is where the interesting result is.

Run from code/unified_gate_audit_446b/.
"""
import re

GATE = "../../docs/OneThird-Unified-Framework-Gate.md"
SRC = "../../docs/OneThird-Hodge-Side-Leverage.md"
AUD = "../../docs/OneThird-Hodge-Side-Leverage-IndependentAudit.md"

def norm(s):
    return re.sub(r"\s+", " ", s).strip()

def unquote(s):
    return re.sub(r"^> ?", "", s)

raw = {p: open(p).read() for p in (GATE, SRC, AUD)}
ls = {p: raw[p].split("\n") for p in raw}
flat = {p: norm(re.sub(r"(?m)^> ?", "", raw[p])) for p in raw}
pool = {p: [norm(unquote(l)) for l in ls[p]] for p in (SRC, AUD)}

def blocks(lines_):
    out, cur, start = [], [], None
    for i, l in enumerate(lines_, 1):
        if l.startswith(">"):
            if not cur:
                start = i
            cur.append(unquote(l))
        else:
            if cur:
                out.append((start, cur))
            cur = []
    if cur:
        out.append((start, cur))
    return out

print("=" * 78)
print("(1) BLOCK QUOTES IN THE GATE DOC vs THE CITED DOCUMENTS, line by line")
print("=" * 78)
bad = 0
for start, blk in blocks(ls[GATE]):
    body = [norm(l) for l in blk if norm(l)]
    if not body:
        continue
    if any("Theorem (mg-8fd1)" in l for l in body):
        print("gate:%-4d  %2d lines  the gate's OWN theorem statement, not a quotation"
              % (start, len(body)))
        continue
    for doc, name in ((SRC, "source"), (AUD, "mg-86a3 audit")):
        miss = [l for l in body if l not in pool[doc]]
        if not miss:
            first = pool[doc].index(body[0]) + 1
            last = pool[doc].index(body[-1]) + 1
            print("gate:%-4d  %2d lines  EXACT MATCH in %s lines %d..%d"
                  % (start, len(body), name, first, last))
            break
    else:
        bad += 1
        miss = [l for l in body if l not in pool[SRC]]
        print("gate:%-4d  %2d lines  *** %d LINE(S) NOT VERBATIM ***"
              % (start, len(body), len(miss)))
        for l in miss:
            print("      MISSING: %s" % l[:140])
print()
print("VERDICT on the quotations: %s"
      % ("all block quotes are exact, no paraphrase smuggled into a quote"
         if bad == 0 else "%d BLOCK(S) NOT VERBATIM" % bad))

print()
print("=" * 78)
print("(2) LINE-NUMBER CITATIONS, DEREFERENCED")
print("=" * 78)
def show(p, no, tag=""):
    t = ls[p][no - 1] if 0 < no <= len(ls[p]) else "<out of range>"
    print("   %-4s %-34s :%-5d %s" % (tag, p.split("/")[-1][:34], no, t[:100]))

print('gate 1.1 cites source SS8 as "lines 691-723":')
show(SRC, 691, "691")
show(SRC, 723, "723")
nxt = [i + 1 for i, l in enumerate(ls[SRC]) if l.startswith("## ") and i + 1 > 691][0]
print("   next '## ' heading is line %d, so the section body is 691..%d -- "
      "citation %s" % (nxt, nxt - 1,
                       "covers the prose (the remainder is a horizontal rule)"
                       if nxt - 1 >= 723 else "WRONG"))
print('gate 1.1 cites ledger rows N2 / N2-prime as "lines 1019-1020":')
for no in (1019, 1020):
    show(SRC, no, str(no))
print('gate 1 cites the mg-86a3 audit "rows at lines 75, 475, 500-501":')
for no in (75, 475, 500, 501):
    show(AUD, no, str(no))

print()
print("=" * 78)
print("(3) INLINE FRAGMENTS, SEARCHED IN THE WHOLE NORMALISED DOCUMENT")
print("=" * 78)
frags = [
 (SRC, "N2 ledger scope line, quoted in gate 1.1",
  "all finite posets, all `α` with `≥ 2` parts; checked on all posets `n ≤ 5` "
  "(exactly 1 exception per `n`, the antichain)"),
 (AUD, "auditor restatement, quoted in gate 1.2",
  "the AT graph of a non-antichain has no `S_n` symmetry"),
 (AUD, "auditor verdict words, quoted in gate 1.2",
  "the Young-module dress adds nothing but costs nothing"),
 (AUD, "'proof checked line by line', quoted in gate 1",
  "proof checked line by line"),
 (SRC, "source SS9.4 heading, paraphrased in gate 1.3",
  "this family reaches `Δ_AT` only where `Δ_AT` is already free"),
 (SRC, "the words gate 2.6 attributes to SS9.1", "NOT closed under refinement"),
 (SRC, "SS9.1's parenthetical CONTINUED past what gate 2.6 quotes",
  "So `L_P` is a lattice for the reverse-refinement order and the join is the "
  "common refinement, not a sublattice of the partition lattice under refinement."),
 (SRC, "ledger row B2's operation (opposite convention to the gate's 'join')",
  "closed under join = common refinement"),
]
for doc, label, frag in frags:
    ok = norm(frag) in flat[doc]
    print("  [%s] %-58s %s" % ("OK " if ok else "***", label,
                               "found" if ok else "NOT FOUND"))
    if not ok:
        print("        %s" % frag[:120])

print()
print("Context for the last three rows: the SS9.1 parenthetical is ONE sentence.")
print("Gate 2.6 quotes its first clause and calls the content of its last clause")
print("unrecorded.  Both clauses, verbatim from the source:")
i = [k for k, l in enumerate(ls[SRC]) if "Note that the acyclic partitions" in l][0]
for k in range(i, i + 4):
    print("   src:%-5d %s" % (k + 1, ls[SRC][k]))
print()
print("and what gate 2.6 says about them:")
j = [k for k, l in enumerate(ls[GATE]) if "The source (§9.1) records" in l][0]
for k in range(j, j + 3):
    print("   gate:%-4d %s" % (k + 1, ls[GATE][k]))
