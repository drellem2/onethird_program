"""a4_rowcheck — P13's guard: are MY rows mg-200d's rows?

Prediction P13 bound me, before `lp200d.py` was opened, to establish row-equality
before scoring any numeric disagreement as mathematics.  "Per-slot adjacency
symmetry" has several defensible formalisations and picking a different one and
then calling mg-200d wrong would be scoring a reading as a theorem.

This is the ONLY place in this audit that touches mg-200d's code, and it is an
ASSERTION, not a dependency: no value reported anywhere else comes from it.  It
imports `lp200d.build` solely to compare constraint matrices.

A row is normalised to a canonical, order-free form:
    (sense, rhs, frozenset of (permutation_word, coefficient))
keyed by the PERMUTATION rather than by a column index, so a different column
ordering cannot make two different systems look alike or two alike systems differ.
Rows are compared as MULTISETS, and a row is also matched against its own negation,
since `a = b` and `b = a` are the same equality written with opposite sign.
"""
import sys
from fractions import Fraction as F
import liba41b7 as L

sys.path.insert(0, "../perslot_symmetry_200d")
import lp200d as T   # noqa: E402   -- ASSERTION TARGET ONLY


def canon_mine(n, keep, rows):
    out = []
    for (c, sense, b) in rows:
        s = {"<=": "<=", ">=": ">=", "=": "=="}[sense]
        items = frozenset(("".join(map(str, keep[j])), F(v)) for j, v in c.items() if v != 0)
        neg = frozenset(("".join(map(str, keep[j])), -F(v)) for j, v in c.items() if v != 0)
        out.append((s, F(b), items, neg))
    return out


def canon_theirs(n, perms, rows):
    out = []
    for (c, sense, b) in rows:
        items = frozenset(("".join(map(str, perms[j])), F(v)) for j, v in c.items() if v != 0)
        neg = frozenset(("".join(map(str, perms[j])), -F(v)) for j, v in c.items() if v != 0)
        out.append((sense, F(b), items, neg))
    return out


def compare(n, C):
    """Compare my branch(C) rows with lp200d.build(n,'slot_eq',comparable=C)."""
    P_all = L.perms(n)
    keep = [s for s in P_all if not any(L.pos(s, b) < L.pos(s, a) for (a, b) in C)]
    I = [p for p in L.pairs(n) if p not in C]
    mine = [L.row_normalisation(n, keep)]
    for (a, b) in I:
        col = {j: F(1) for j, s in enumerate(keep) if L.pos(s, b) < L.pos(s, a)}
        if col:
            mine.append((col, "<=", F(1, 3)))
    mine.extend(L.rows_perslot_symmetry(n, keep, pairset=I))

    theirs_perms = [p for p in T.permutations(range(n)) if not (T.flips(p) & frozenset(C))]
    tp, trows = T.build(n, "slot_eq", frozenset(C), perms=theirs_perms)

    A = canon_mine(n, keep, mine)
    B = canon_theirs(n, tp, trows)

    # support first
    if set("".join(map(str, s)) for s in keep) != set("".join(map(str, p)) for p in tp):
        return "SUPPORT DIFFERS", len(A), len(B), None

    unmatched_mine, poolB = [], list(B)
    for (s, b, items, neg) in A:
        hit = None
        for i, (s2, b2, items2, neg2) in enumerate(poolB):
            if s == s2 and b == b2 and items == items2:
                hit = i
                break
            # an equality written with the opposite sign is the same row
            if s == s2 == "==" and b == b2 == 0 and neg == items2:
                hit = i
                break
        if hit is None:
            unmatched_mine.append((s, b, sorted(items)[:3]))
        else:
            poolB.pop(hit)
    return ("IDENTICAL" if not unmatched_mine and not poolB else "DIFFER",
            len(A), len(B), (unmatched_mine[:2], [(x[0], x[1], sorted(x[2])[:3]) for x in poolB[:2]]))


print("=" * 78)
print("P13 GUARD -- my per-slot rows vs lp200d.build(..., 'slot_eq', comparable=C)")
print("=" * 78)
bad = 0
tested = 0
for n in (3, 4, 5):
    prs = L.pairs(n)
    masks = range(1 << len(prs)) if n <= 4 else range(0, 1 << len(prs), 7)
    for mask in masks:
        C = frozenset(prs[i] for i in range(len(prs)) if mask >> i & 1)
        keep = [s for s in L.perms(n) if not any(L.pos(s, b) < L.pos(s, a) for (a, b) in C)]
        if not keep:
            continue
        verdict, na, nb, detail = compare(n, C)
        tested += 1
        if verdict != "IDENTICAL":
            bad += 1
            if bad <= 5:
                print("  n=%d C=%s  %s   mine %d rows, theirs %d rows\n     %s"
                      % (n, sorted(C), verdict, na, nb, detail))
print("  branches compared: %d    row-systems that DIFFER: %d" % (tested, bad))
print("  => %s" % ("MY ROWS ARE ITS ROWS. A numeric disagreement would be mathematics."
                   if bad == 0 else
                   "ROWS DIFFER -- any numeric disagreement is about the READING, not the maths."))

print()
print("=" * 78)
print("Negative control: the guard must REJECT a system that is genuinely different")
print("=" * 78)
# aggregate rows against their per-slot rows, at a branch where they must differ
n = 4
C = frozenset()
P_all = L.perms(n)
keep = list(P_all)
I = L.pairs(n)
mine_agg = [L.row_normalisation(n, keep)]
for (a, b) in I:
    col = {j: F(1) for j, s in enumerate(keep) if L.pos(s, b) < L.pos(s, a)}
    mine_agg.append((col, "<=", F(1, 3)))
mine_agg.extend(L.rows_aggregate_symmetry(n, keep, pairset=I))
tp, trows = T.build(n, "slot_eq", frozenset())
A = canon_mine(n, keep, mine_agg)
B = canon_theirs(n, tp, trows)
same = len(A) == len(B) and all(any(a[0] == b[0] and a[1] == b[1] and a[2] == b[2] for b in B) for a in A)
print("  aggregate rows vs their per-slot rows at n=4: %s  (must be REJECTED)"
      % ("MATCHED -- GUARD IS VACUOUS" if same else "rejected, as required"))
# and the cap perturbed
mine_bad = [L.row_normalisation(n, keep)]
for (a, b) in I:
    col = {j: F(1) for j, s in enumerate(keep) if L.pos(s, b) < L.pos(s, a)}
    mine_bad.append((col, "<=", F(1, 4)))          # wrong cap
mine_bad.extend(L.rows_perslot_symmetry(n, keep, pairset=I))
A2 = canon_mine(n, keep, mine_bad)
same2 = all(any(a[0] == b[0] and a[1] == b[1] and a[2] == b[2] for b in B) for a in A2)
print("  cap 1/4 instead of 1/3 at n=4: %s  (must be REJECTED)"
      % ("MATCHED -- GUARD IS VACUOUS" if same2 else "rejected, as required"))
sys.exit(1 if bad else 0)
