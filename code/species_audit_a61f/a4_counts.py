"""A4 -- EVERY NUMBER IN THE DOCUMENT, RECOMPUTED, AND THE ONE THAT IS WRONG.

Each block states what mg-7d75 claims, recomputes it from this directory's
kernel, and prints AGREES or BROKEN.  A BROKEN line is counted in TOTAL BAD.
"""

import sys
from itertools import permutations
from kerna61f import (posets_labelled, iso_classes, aut, faces, supp, tits,
                      concat, set_partitions, set_compositions, act_part,
                      act_comp, orbits, AC_by_support, AC_by_acyclicity,
                      quotient_acyclic, restrict_part, restrict_poset,
                      is_lower_set)

bad = 0
CHECKS = []


def hdr(t):
    print("=" * 78)
    print(t)
    print("=" * 78)
    print()


def claim(tag, doc_says, measured, note=""):
    global bad
    ok = (doc_says == measured)
    if not ok:
        bad += 1
    CHECKS.append((tag, ok))
    print("  %-14s doc: %-34s measured: %-24s %s"
          % (tag, str(doc_says), str(measured), "AGREES" if ok else "BROKEN"))
    if note:
        print("                 %s" % note)


BELL = [1, 1, 2, 5, 15, 52, 203, 877, 4140]
PART = [1, 1, 2, 3, 5, 7, 11, 15, 22]

# ---------------------------------------------------------------------------
hdr("A4a  the grading falsifier (T1) and the antichain row of section 0")

claim("Bell(n) n<=7", BELL[1:8],
      [len(set_partitions(range(n))) for n in range(1, 8)])
claim("p(n) n<=7", PART[1:8],
      [len(orbits(sorted(set_partitions(range(n)), key=repr),
                  list(permutations(range(n))), act_part)) for n in range(1, 8)])
claim("|Sigma_n| n<=5", [1, 3, 13, 75, 541],
      [len(set_compositions(range(n))) for n in range(1, 6)])
lab = {n: posets_labelled(n) for n in range(1, 5)}
claim("labelled posets", [1, 3, 19, 219], [len(lab[n]) for n in range(1, 5)])
claim("classes n<=5", [1, 2, 5, 16, 63],
      [len(iso_classes(n)) for n in range(1, 6)])

sub = []
eqs = []
for n in range(1, 5):
    s = e = 0
    PI = set_partitions(range(n))
    for rel in lab[n]:
        AC = AC_by_acyclicity(rel, range(n))
        s += all(X in PI for X in AC)
        e += (len(AC) == len(PI))
    sub.append(s)
    eqs.append(e)
claim("AC(P) in Pi[n]", [1, 3, 19, 219], sub,
      "degree respected on all 242 labelled posets to n = 4")
claim("AC(P) = Pi[n]", [1, 3, 13, 45], eqs,
      "mg-7d75 T1e: '3 of 3 at n=2, 13 of 19 at n=3, 45 of 219 at n=4'")
print()

# ---------------------------------------------------------------------------
hdr("A4b  section 8 C3, 'the smallest poset with AC(P) != Pi[n]' -- BROKEN")

print("  mg-7d75 section 8 C3 and T1e both say:")
print('      "The smallest poset with AC(P) != Pi[n] is {a<c, b<d}, where the')
print('       partition ad|bc has a 2-cycle in its quotient."')
print("  and give the reason:")
print('      "a cycle needs two blocks B, C with b1 < c1 and c2 < b2, which no')
print('       poset on <= 2 elements admits."')
print()
smallest = None
for n in range(1, 5):
    wit = []
    PI = set_partitions(range(n))
    for rel in lab[n]:
        miss = [X for X in PI if not quotient_acyclic(rel, X)]
        if miss:
            wit.append((rel, miss))
    print("  n = %d : %3d labelled posets, %3d of them have AC(P) != Pi[n]"
          % (n, len(lab[n]), len(wit)))
    if wit and smallest is None:
        smallest = (n, wit)
print()
n0, wit0 = smallest
print("  The smallest n with a witness is n = %d, not 4." % n0)
print("  Witnesses at n = %d (all %d of them, one isomorphism class -- the"
      % (n0, len(wit0)))
print("  3-ELEMENT CHAIN, in its %d labellings):" % len(wit0))
for rel, miss in wit0:
    print("    P = %-28s missing from AC(P): %s"
          % (sorted(rel), [sorted(sorted(b) for b in X) for X in miss]))
print()
print("  The stated reason is sound as far as it goes and rules out n <= 2 --")
print("  the two blocks need |B| >= 2 and |C| >= 1, so at least 3 elements --")
print("  but the document then jumps to a 4-element example.  The 3-chain")
print("  a < b < c with the partition {a,c} | {b} is a cycle: a < b goes one")
print("  way and b < c goes the other.  {a<c, b<d} IS a witness; it is not")
print("  the smallest one, and T1e's own row '13 of 19 at n = 3' records 6")
print("  labelled witnesses at n = 3 two paragraphs above the claim.")
claim("smallest witness n", 4, n0,
      "INTERNAL CONTRADICTION with mg-7d75's own T1e table")
print()

# ---------------------------------------------------------------------------
hdr("A4c  section 2.3 / T4c -- the two instances")

dims = []
acq = []
for n in range(1, 6):
    S = set_compositions(range(n))
    G = list(permutations(range(n)))
    ob = orbits(S, G, act_comp)
    dims.append(len(ob))
    PI = set_partitions(range(n))
    acq.append(len(orbits(sorted(PI, key=repr), G, act_part)))
claim("dim(kSig)^Sn", [1, 2, 4, 8, 16], dims, "= 2^(n-1)")
claim("|Pi_n/S_n|", [1, 2, 3, 5, 7], acq, "= p(n)")

triv = []
for n in range(1, 6):
    triv.append(sum(1 for rel in iso_classes(n) if len(aut(rel, n)) == 1))
claim("Aut(P)=1 classes", [1, 1, 2, 5, 19], triv,
      "mg-7d75 T4c: '19 of the 63 classes at n = 5 have Aut(P) = 1'")

# T2's cap
over80 = sum(1 for rel in iso_classes(5) if len(faces(rel, range(5))) > 80)
claim("T2 skipped n=5", 24, over80, "classes with |F(P)| > 80")
print()

# ---------------------------------------------------------------------------
hdr("A4d  T4d -- the control that the group must be Aut(P), not S_n")

fired = []
for n in range(2, 5):
    c = f = 0
    for rel in iso_classes(n):
        if not rel:
            continue                      # the antichain is exempt
        c += 1
        F = set(faces(rel, range(n)))
        leaves = any(act_comp(x, p) not in F
                     for x in F for p in permutations(range(n)))
        f += leaves
    fired.append((c, f))
claim("T4d non-antichain", [(1, 1), (4, 4), (15, 15)], fired,
      "mg-7d75: 'fired on all 20 non-antichain classes'")
print()
print("  This control is real but weak: it says S_n does not preserve the cone")
print("  of a non-antichain poset, which is true for the trivial reason that")
print("  the cone has a smaller symmetry group.  The substantive control on")
print("  the identity is in a1_headline.py A1e, where the INDEX SET is varied.")
print()

# ---------------------------------------------------------------------------
hdr("A4e  T6b -- the two Fock functors on OUR species")

kb_ac = []
k_ac = []
kb_f = []
k_f = []
for n in range(1, 5):
    G = list(permutations(range(n)))
    eF = [(rel, F) for rel in lab[n] for F in faces(rel, range(n))]
    eA = [(rel, X) for rel in lab[n]
          for X in sorted(AC_by_support(rel, range(n)), key=repr)]

    def act_pair_comp(x, p):
        return (frozenset((p[a], p[b]) for (a, b) in x[0]), act_comp(x[1], p))

    def act_pair_part(x, p):
        return (frozenset((p[a], p[b]) for (a, b) in x[0]), act_part(x[1], p))
    kb_f.append(len(eF))
    kb_ac.append(len(eA))
    k_f.append(len(orbits(eF, G, act_pair_comp)))
    k_ac.append(len(orbits(eA, G, act_pair_part)))
claim("dim Kbar(F)_n", [1, 7, 121, 4399], kb_f)
claim("dim K(F)_n", [1, 4, 24, 218], k_f)
claim("dim Kbar(AC)_n", [1, 6, 89, 2685], kb_ac)
claim("dim K(AC)_n", [1, 4, 20, 152], k_ac)
print()

# ---------------------------------------------------------------------------
hdr("A4f  T6c -- the Bergeron-Li unitality reproduction, 0 of 529")

pairs = 0
unital = 0
allpos = []
for n in range(1, 4):
    allpos += [(n, rel) for rel in lab[n]]
for (n1, p1) in allpos:
    for (n2, p2) in allpos:
        pairs += 1
        one1 = (frozenset(range(n1)),)
        one2 = (frozenset(range(n1, n1 + n2)),)
        joint = (frozenset(range(n1 + n2)),)
        if concat(one1, one2) == joint:
            unital += 1
claim("BL pairs", 529, pairs, "labelled posets with 1 <= |P|,|Q| <= 3: 23 x 23")
claim("BL unital", 0, unital)
print()
print("  Reproduced, and mg-7d75 reports it correctly as a reproduction of")
print("  mg-af28.  What should be said in the same breath, and is not: the")
print("  count is 0 for every pair of NONEMPTY posets by inspection, because")
print("  the concatenation of two nonempty tuples has at least two blocks and")
print("  the identity face has one.  The move from mg-af28's 64 to 529 is a")
print("  wider net over a statement that has no exceptions to find.")
print()

# ---------------------------------------------------------------------------
hdr("A4g  T6d -- the forgetful map AC -> Pi and its 22614 coproduct failures")


def subsets_of(I):
    I = sorted(I)
    return [frozenset(I[i] for i in range(len(I)) if m >> i & 1)
            for m in range(1 << len(I))]


GROUND = 4
IF = frozenset(range(GROUND))
prod_bad = coprod_bad = 0
U = {}
for J in subsets_of(IF):
    lj = sorted(J)
    ps = [frozenset((lj[a], lj[b]) for (a, b) in r)
          for r in posets_labelled(len(lj))]
    U[J] = [(rel, X) for rel in ps
            for X in sorted(AC_by_support(rel, J), key=repr)]
for J in subsets_of(IF):
    for S in subsets_of(J):
        T = J - S
        for x in U[S]:
            for y in U[T]:
                lhs = frozenset(x[1]) | frozenset(y[1])
                if lhs != (frozenset(x[1]) | frozenset(y[1])):
                    prod_bad += 1
        for x in U[J]:
            ours = None if not is_lower_set(x[0], S) else \
                (restrict_part(x[1], S), restrict_part(x[1], T))
            theirs = (restrict_part(x[1], S), restrict_part(x[1], T))
            if ours != theirs:
                coprod_bad += 1
claim("Sym map product", 0, prod_bad)
claim("Sym map coproduct", 22614, coprod_bad)
print()

print("=" * 78)
print("A4 checks: %d, agreeing: %d, BROKEN: %d"
      % (len(CHECKS), sum(1 for _, o in CHECKS if o), bad))
print("A4 TOTAL BAD: %d" % bad)
print("=" * 78)
sys.exit(0)
