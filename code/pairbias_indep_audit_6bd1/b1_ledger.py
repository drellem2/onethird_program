"""B1 — re-derive mg-345e's ledger figures from Op-Form §9 with an independent reader.

Re-derived, NOT checked against mg-345e's printed numbers: this script does not read
`out_p1_ledger_depgraph.txt` and does not import `lib345e`.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib6bd1 import read_ledger, edge_count, dependents, ancestors  # noqa: E402

claims, edges, rejected = read_ledger()

print("=" * 78)
print("B1 — Op-Form §9 claim ledger, read by mg-6bd1's own parser")
print("=" * 78)
print()
print("LIMIT OF THIS INSTRUMENT, stated before its output: this graph scores a claim")
print("by its recorded LABEL, not by its mathematics. A claim whose label understates")
print("its dependencies is scored independent here. mg-345e says the same of its own")
print("parser and it is true of mine. The graph CORROBORATES; it does not decide.")
print()

print(f"rows parsed                 : {len(claims)}")
print(f"recorded dependency edges   : {edge_count(edges)}")
print()
print("every edge, exhibited (so a disagreement is locatable, not just a count):")
for cid in sorted(edges):
    if edges[cid]:
        print(f"    claim {cid:>2} <- {sorted(edges[cid])}      [{claims[cid][2][:58]}]")
print()
if rejected:
    print("integers found in a dependency clause that are NOT claim ids (dropped, listed):")
    for cid, r in sorted(rejected.items()):
        print(f"    claim {cid:>2}: {r}")
    print()

TARGET = 4
dep4 = dependents(edges, TARGET)
print(f"claim {TARGET} statement      : {claims[TARGET][0][:70]}")
print(f"transitive dependents of {TARGET}: {dep4}")
print()

SUPPLY = [21, 22, 25, 26, 27]
print("supply-path claims and whether each reaches claim 4:")
reach = 0
for c in SUPPLY:
    a = ancestors(edges, c)
    hit = TARGET in a
    reach += hit
    print(f"    claim {c:>2}  ancestors={sorted(a) or '[]':<18} reaches 4: {hit}"
          f"   label: {claims[c][2][:44]}")
print(f"  -> {reach} of {len(SUPPLY)} supply-path claims reach claim 4")
print()

print("claim 28 (the constant budget) — mg-345e's §4 'machine observation':")
print(f"    ancestors           : {sorted(ancestors(edges, 28)) or '[]'}")
print(f"    reaches claim 4     : {TARGET in ancestors(edges, 28)}")
lab28 = claims[28][2]
print(f"    label mentions L4   : {'L4' in lab28}")
print(f"    label mentions C_3  : {('C_3' in lab28) or ('C_3' in claims[28][0])}")
print()

print("-" * 78)
print("NEGATIVE CONTROLS — a graph that agrees with mg-345e is only worth something")
print("if it could have disagreed. Each control mutates the INPUT and must flip a")
print("printed answer.")
print("-" * 78)

# NC1 — sever 17 <- 4. If dependents(4) still contains 18 and 23, the closure is not
# actually being computed and the agreement above is decoration.
mut = {k: set(v) for k, v in edges.items()}
mut[17].discard(4)
d = dependents(mut, 4)
print(f"NC1  sever edge 17<-4        -> dependents(4) = {d}")
print(f"     FIRES (18 and 23 must leave): {18 not in d and 23 not in d and d == [12]}")

# NC2 — add a fake edge 26 <- 18. A supply claim must then reach 4.
mut = {k: set(v) for k, v in edges.items()}
mut[26].add(18)
r = sum(1 for c in SUPPLY if 4 in ancestors(mut, c))
print(f"NC2  add fake edge 26<-18    -> supply claims reaching 4 = {r}")
print(f"     FIRES (must be >= 1): {r >= 1}")

# NC3 — the under-reading defect mg-345e caught in ITSELF, reproduced deliberately:
# truncate claim 17's clause `on 1, 4, 13, 16` to its first two ids and check that the
# EDGE COUNT, not the verdict, is what moves. If the verdict moves too, mg-345e's
# Defect 1 would have been verdict-bearing and it says it was not.
mut = {k: set(v) for k, v in edges.items()}
mut[17] = {1, 4}
print(f"NC3  truncate 17's clause    -> edges = {edge_count(mut)} (was {edge_count(edges)}),"
      f" dependents(4) = {dependents(mut, 4)}")
print(f"     mg-345e's Defect 1 is NOT verdict-bearing: {dependents(mut, 4) == dep4}")

# NC4 — a parser that under-reads the OTHER way: drop 'given' as a keyword. mg-345e's
# 11 depends on 'PROVEN given 28' counting as an edge. If it does not, the count is 10.
import lib6bd1  # noqa: E402
saved = lib6bd1.KEYWORDS
lib6bd1.KEYWORDS = ("on",)
_, e_on_only, _ = read_ledger()
lib6bd1.KEYWORDS = saved
print(f"NC4  keyword 'on' only       -> edges = {edge_count(e_on_only)}"
      f"  (the difference is the '32 PROVEN given 28' clause)")
print(f"     the 11th edge is 32<-28: {edge_count(edges) - edge_count(e_on_only) == 1}")
print()
print("done.")
