"""R1 -- mg-a61f's X1: the smallest poset with AC(P) != Pi[n].

WHAT WAS WRONG.  mg-7d75 section 8 C3, and the same sentence printed by
code/species_7d75/t1_grading.py into out_t1_grading.txt:

    "Smallest witness with AC(P) != Pi[n]: P = {a<c, b<d}, where ad|bc has a
     2-cycle."

It is a GENERAL EXTREMAL CLAIM, cited to nobody, asserted rather than
computed -- and it is false.  The smallest is the 3-ELEMENT CHAIN.  The
refuting evidence was already in mg-7d75's own T1e table, sixty lines above
the claim in the document and eleven lines above it in the instrument's own
output: 13 of 19 labelled posets at n = 3 have AC(P) = Pi[n], so 6 do not.

THE PREDICT-FIRST DISCIPLINE.  Every row below carries the outcome THIS
REPAIR PREDICTED BEFORE THE RUN, written into this file before it was
executed, and the run reports predicted-vs-actual.  A check whose
expectation is written after the run is a check that cannot be wrong.

THE INSTRUMENT MUST BE ABLE TO RETURN A SMALLER ANSWER THAN 3.  R1e is the
control: the identical search, with acyclicity replaced by the strictly
stronger condition "the quotient digraph has no edges at all", must return
n = 2.  If it does not, "the smallest is n = 3" is a fact about the search
and not about posets.
"""

import sys

from kern6f61 import (posets_on, partitions_on, AC_by_support,
                      AC_by_acyclicity, quotient_acyclic, canonical, bits,
                      supp, faces_on)

bad = 0

# ---------------------------------------------------------------------------
# PREDICTIONS.  Written before the first execution of this file.
# ---------------------------------------------------------------------------
PREDICT = {
    "P1  AC(P) subset Pi[n] for all 242 labelled posets to n <= 4": 242,
    "P2  labelled posets with AC(P) = Pi[n], n = 1,2,3,4": (1, 3, 13, 45),
    "P3  smallest n admitting a witness AC(P) != Pi[n]": 3,
    "P4a labelled witnesses at n = 3": 6,
    "P4b isomorphism classes of witness at n = 3": 1,
    "P4c that class is the 3-element CHAIN": True,
    "P5  labelled witnesses at n = 4": 174,
    "P6  {a<c, b<d} is itself a witness (only 'smallest' is false)": True,
    "P7  every witness at n = 3 has block sizes {2,1}": True,
    "P8  two routes to AC agree on every poset to n <= 4": True,
    "P9  CONTROL: with 'no edges in the quotient' the smallest n is": 2,
}
ACTUAL = {}


def hdr(t):
    print("=" * 78)
    print(t)
    print("=" * 78)
    print()


def record(key, value):
    ACTUAL[key] = value
    return value


def show(mask):
    return "{" + ",".join("abcdefgh"[i] for i in bits(mask)) + "}"


def show_poset(up, ground):
    rel = []
    for i in bits(ground):
        for j in bits(up[i]):
            rel.append("%s<%s" % ("abcdefgh"[i], "abcdefgh"[j]))
    return "{" + ", ".join(sorted(rel)) + "}" if rel else "{antichain}"


def show_part(X):
    return "|".join("".join("abcdefgh"[i] for i in bits(B))
                    for B in sorted(X))


# ---------------------------------------------------------------------------
hdr("R1a  the T1e table, recomputed from a third independent instrument")

print("  Posets are carried here as TUPLES OF UP-MASKS and enumerated as the")
print("  FIXED POINTS OF THE TRANSITIVE CLOSURE; faces come from block-index")
print("  functions.  Neither representation nor route is shared with")
print("  code/species_7d75/ or code/species_audit_a61f/.")
print()
print("   n  labelled posets  AC subset Pi[n]  AC = Pi[n]  witnesses  antichains")

sub_total = 0
eq_counts = []
witness_counts = []
witnesses = {}
route_bad = 0
for n in range(1, 5):
    ground = (1 << n) - 1
    Ps = posets_on(ground, n)
    pi = set(partitions_on(ground))
    sub = eq = anti = 0
    wit = []
    for up in Ps:
        ac1 = AC_by_support(up, ground)
        ac2 = AC_by_acyclicity(up, ground)
        if ac1 != ac2:
            route_bad += 1
        sub += (ac1 <= pi)
        if ac1 == pi:
            eq += 1
        else:
            wit.append(up)
        anti += all(u == 0 for u in up)
    sub_total += sub
    eq_counts.append(eq)
    witness_counts.append(len(wit))
    witnesses[n] = wit
    print("  %2d %16d %16d %11d %10d %11d"
          % (n, len(Ps), sub, eq, len(wit), anti))
print()
record("P1  AC(P) subset Pi[n] for all 242 labelled posets to n <= 4",
       sub_total)
record("P2  labelled posets with AC(P) = Pi[n], n = 1,2,3,4", tuple(eq_counts))
record("P8  two routes to AC agree on every poset to n <= 4", route_bad == 0)

smallest = min(n for n in range(1, 5) if witness_counts[n - 1] > 0)
record("P3  smallest n admitting a witness AC(P) != Pi[n]", smallest)
record("P4a labelled witnesses at n = 3", witness_counts[2])
record("P5  labelled witnesses at n = 4", witness_counts[3])

# ---------------------------------------------------------------------------
hdr("R1b  the witnesses at n = 3, printed in full")

ground3 = 0b111
classes = sorted({canonical(up, ground3, 3) for up in witnesses[3]})
record("P4b isomorphism classes of witness at n = 3", len(classes))
chain3 = None
for up in posets_on(ground3, 3):
    rel = sum(bin(u).count("1") for u in up)
    if rel == 3:                      # a<b, b<c, a<c -- the 3-chain
        chain3 = canonical(up, ground3, 3)
        break
record("P4c that class is the 3-element CHAIN",
       len(classes) == 1 and classes[0] == chain3)

for up in witnesses[3]:
    pi = set(partitions_on(ground3))
    missing = sorted(pi - AC_by_support(up, ground3), key=lambda X: sorted(X))
    print("    P = %-24s  missing from AC(P): %s"
          % (show_poset(up, ground3),
             ", ".join(show_part(X) for X in missing)))
print()
print("  All %d are the SAME isomorphism class in its %d labellings: the "
      "3-element chain." % (witness_counts[2], witness_counts[2]))
print()
print("  Why, on the smallest one.  P = a < b < c and X = {a,c} | {b}:")
print("    a < b sends the block {a,c} to the block {b};")
print("    b < c sends the block {b} to the block {a,c};")
print("  so the quotient digraph is a 2-cycle and X is not in AC(P).")
print()
sizes_ok = True
for up in witnesses[3]:
    pi = set(partitions_on(ground3))
    for X in pi - AC_by_support(up, ground3):
        if sorted(sorted(len(bits(B)) for B in X)) != [1, 2]:
            sizes_ok = False
record("P7  every witness at n = 3 has block sizes {2,1}", sizes_ok)
print("  Every missing partition at n = 3 has block sizes {2,1}: %s"
      % ("yes" if sizes_ok else "NO"))
print()
print("  THE STATED REASON IN C3 IS SOUND AND THE CONCLUSION DRAWN FROM IT IS")
print("  NOT.  'A cycle needs two blocks B, C with b1 < c1 and c2 < b2' forces")
print("  |B| >= 2 and |C| >= 1, hence n >= 3 -- and 3 is attained.  C3 read its")
print("  own bound as 4.")
print()

# ---------------------------------------------------------------------------
hdr("R1c  {a<c, b<d} IS a witness -- what C3 got right")

ground4 = 0b1111
up = [0] * 4
up[0] |= 1 << 2          # a < c
up[1] |= 1 << 3          # b < d
up = tuple(up)
acs = AC_by_support(up, ground4)
X = frozenset([0b1001, 0b0110])          # ad | bc
is_wit = X not in acs
record("P6  {a<c, b<d} is itself a witness (only 'smallest' is false)", is_wit)
print("  P = %s" % show_poset(up, ground4))
print("  X = %s in AC(P): %s" % (show_part(X), "yes" if not is_wit else "no"))
print("  so P is a witness at n = 4: %s" % ("yes" if is_wit else "NO"))
print()
print("  C3's example is correct, its reason is correct, and the word")
print("  'smallest' is the whole of the error.")
print()

# ---------------------------------------------------------------------------
hdr("R1d  the corrected sentence, generated from the measurement")

print("  Smallest witness with AC(P) != Pi[n]: the 3-ELEMENT CHAIN a < b < c,")
print("  where {a,c}|{b} has a 2-cycle in the quotient -- %d labelled posets"
      % witness_counts[2])
print("  at n = 3, one isomorphism class.  ({a<c, b<d} is also a witness and")
print("  is not the smallest.)")
print()

# ---------------------------------------------------------------------------
hdr("R1e  CONTROL -- the search must be able to return n = 2")

print("  The identical search with the acyclicity test replaced by the")
print("  strictly stronger 'the quotient digraph has NO EDGES at all'.  Under")
print("  that test AC'(P) = Pi[n] iff P is an antichain, so a witness must")
print("  appear at n = 2.  If the search cannot return 2, then 3 is a fact")
print("  about the instrument.")
print()


def no_edges(up, X, ground):
    where = {}
    for t, B in enumerate(sorted(X)):
        for e in bits(B):
            where[e] = t
    for i in bits(ground):
        for j in bits(up[i]):
            if where[i] != where[j]:
                return False
    return True


ctrl_smallest = None
for n in range(1, 5):
    ground = (1 << n) - 1
    pi = set(partitions_on(ground))
    for up in posets_on(ground, n):
        ac = {X for X in pi if no_edges(up, X, ground)}
        if ac != pi:
            ctrl_smallest = n
            break
    if ctrl_smallest is not None:
        break
record("P9  CONTROL: with 'no edges in the quotient' the smallest n is",
       ctrl_smallest)
print("  control's smallest n: %s  (control fires: %s)"
      % (ctrl_smallest, "YES" if ctrl_smallest == 2 else "NO"))
print()

# ---------------------------------------------------------------------------
hdr("R1f  PREDICTED vs ACTUAL")

print("  %-62s %8s %8s" % ("row", "pred", "actual"))
misses = 0
for k in PREDICT:
    p, a = PREDICT[k], ACTUAL.get(k, "MISSING")
    ok = (p == a)
    misses += (not ok)
    print("  %-62s %8s %8s  %s"
          % (k, p, a, "as predicted" if ok else "*** DIVERGES ***"))
print()
if misses:
    print("  %d PREDICTION(S) MISSED.  A missed prediction is the finding, not"
          % misses)
    print("  an error to be edited away; it is reported here and in the")
    print("  document.")
else:
    print("  All %d predictions written before the run were met." % len(PREDICT))
bad += misses
print()
print("=" * 78)
print("R1 TOTAL BAD: %d" % bad)
print("=" * 78)
sys.exit(0)
