"""mg-d0e2 E2: the gate whose deletion moved NOTHING -- which population is it
dead over, and does any scored row depend on it?

E1's one prediction miss.  Deleting the `parity` gate from the predicate --
the `return Trace(False, "parity", signs_read)` that fires when the union-find
finds a contradiction -- leaves `controls_output.txt` BYTE-IDENTICAL and the
battery exiting 0.  By the standard mg-1c80 set and mg-5f9a passed, that is the
signature of a name that is not doing the work.

IT IS NOT THE SAME DEFECT, and the difference is the point of this file: mg-da45
printed a gate name AS THE REASON its rows answered as they did, and that gate's
deletion changed nothing.  Nothing in this artifact says the parity gate decides
any row -- the sentences that mention it say 0 pairs REACH it, which is a true
statement that the deletion cannot disturb.

What the deletion does show is narrower and still worth having: THE ONE ROW THAT
EXISTS TO TEST THE UNION-FIND CANNOT FAIL ON A BROKEN PARITY RULE.  That row is
"the union-find absorbability decision agrees with brute force over all 2^m sign
vectors on 306/306 (poset, mutation) pairs with |L(P)| <= 8", and it is the only
thing standing between "absorbable on 0/61" and a solver that says what it likes
about signs.  This file measures the population it runs over and says how much
of the predicate it can see.

Populations are named, never totalled bare.
"""

import os
import sys

sys.path.insert(0, os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                 "face_geometry")))

# `claim1_pair` is the battery's own pair-builder and lives in controls.py, which
# is guarded by `if __name__ == "__main__"` -- importing it runs nothing.  Taking
# it from there rather than rebuilding it is deliberate: a population this file
# assembled itself would be a different experiment from the one the artifact
# reports on.
from controls import claim1_pair                                        # noqa
from face_complex import (absorb_trace, absorbable_by_diagonal_twist,   # noqa
                          mat_eq)
from posets import all_posets                                           # noqa

BROKEN = 0


def claim(ok, text):
    global BROKEN
    if not ok:
        BROKEN += 1
    print("  [%s] %s" % ("OK    " if ok else "BROKEN", text))


NMAX = 5
MUT_MODES = ["ridge_facets", "split_free_as_interior", "ridge_drop",
             "facet_offbyone"]

ps = []
for n in range(2, NMAX + 1):
    ps.extend(all_posets(n))
N = len(ps)

print("== E2: is the parity gate reachable anywhere the battery looks? ==")
print()
print("POPULATION: the %d posets up to isomorphism with 2 <= n <= %d -- the same "
      "population" % (N, NMAX))
print("the battery's baseline row names, re-derived here from posets.py.")
print()


def sweep(label, pairs):
    """Count, over a named population, where the predicate returned."""
    gates = {"shape": 0, "diagonal": 0, "magnitude": 0, "parity": 0}
    reached = rejected_at_parity = accepted = 0
    for A, B in pairs:
        tr = absorb_trace(A, B)
        gates[tr.gate] += 1
        if tr.signs_read > 0 or tr.gate == "parity":
            reached += 1
        if tr.gate == "parity" and not tr.absorbable:
            rejected_at_parity += 1
        accepted += tr.absorbable
    print("  %-46s n=%4d  shape %3d  diagonal %3d  magnitude %3d  parity %3d"
          % (label, len(pairs), gates["shape"], gates["diagonal"],
             gates["magnitude"], gates["parity"]))
    print("  %-46s          reached the parity system %d, REJECTED THERE %d, "
          "returned absorbable %d"
          % ("", reached, rejected_at_parity, accepted))
    return rejected_at_parity, len(pairs)


print("WHERE THE PREDICATE RETURNS, per population the battery feeds it")

# 1. NEGATIVE CONTROL 4's biting pairs -- the 297 the artifact's sentences are about.
nc4 = []
for P in ps:
    L_true, target = claim1_pair(P)
    for mode in MUT_MODES:
        L_mut, _ = claim1_pair(P, incidence_mode=mode)
        if mat_eq(L_mut, L_true):
            continue                       # vacuous: the mutation does not bite
        nc4.append((L_mut, target))
r_nc4, n_nc4 = sweep("NC4 biting (poset, mutation) pairs", nc4)
claim(n_nc4 == 297,
      "the NC4 biting population is %d (poset, mutation) pairs -- the artifact's "
      "'297'" % n_nc4)

# 2. the brute-force agreement row's own population.
bf = []
for P in ps:
    L_true, target = claim1_pair(P)
    if len(L_true) > 8:
        continue
    for mode in ["true", "facet_swap01"] + MUT_MODES:
        bf.append((claim1_pair(P, incidence_mode=mode)[0], target))
r_bf, n_bf = sweep("the |L(P)| <= 8 brute-force agreement row", bf)
claim(n_bf == 306,
      "the brute-force row's population is %d (poset, mutation) pairs -- the "
      "artifact's '306'" % n_bf)

# 3. NEGATIVE CONTROL 3's facet-parity corruption -- the only thing in the file
#    that is meant to reach the parity system at all.
nc3 = []
for P in ps:
    L_true, target = claim1_pair(P)
    L_par = claim1_pair(P, sign_mode="parity")[0]
    if mat_eq(L_par, L_true):
        continue
    nc3.append((L_par, target))
r_nc3, n_nc3 = sweep("NC3 facet-parity corruption, biting posets", nc3)

# 4. the two instrument-check rows.
instr = []
for P in ps:
    L, _ = claim1_pair(P)
    m = len(L)
    s = [-1 if i % 3 == 0 else 1 for i in range(m)]
    instr.append(([[s[i] * L[i][j] * s[j] for j in range(m)] for i in range(m)], L))
    shifted = [row[:] for row in L]
    shifted[0][0] += 1
    instr.append((shifted, L))
r_instr, n_instr = sweep("the two instrument-check rows' pairs", instr)

print()
total_rejected = r_nc4 + r_bf + r_nc3 + r_instr
total_pairs = n_nc4 + n_bf + n_nc3 + n_instr
claim(total_rejected == 0,
      "ACROSS ALL FOUR POPULATIONS THE BATTERY FEEDS THE PREDICATE (%d + %d + %d "
      "+ %d = %d pairs), the number decided NOT ABSORBABLE at the parity gate is "
      "%d.  That is why deleting the parity gate changes not one byte: the branch "
      "is unreached, not mis-described"
      % (n_nc4, n_bf, n_nc3, n_instr, total_pairs, total_rejected))

print()
print("WHAT THE BRUTE-FORCE ROW CAN AND CANNOT SEE")
print("  It is the only row that checks the union-find against an independent")
print("  decision.  Over its own %d pairs it exercises the predicate's forced" % n_bf)
print("  gates and its ACCEPTING parity path, and never its rejecting one.")
print("  A predicate that had lost the ability to reject a contradictory sign")
print("  system would agree with brute force on all %d and the row would pass." % n_bf)

# Demonstrate it rather than assert it: a hand-built contradictory pair, and the
# same pair under the deletion.  Smallest such: s_0 s_1 = +1, s_1 s_2 = +1,
# s_0 s_2 = -1.
A = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
B = [[0, 1, -1], [1, 0, 1], [-1, 1, 0]]
tr = absorb_trace(A, B)
claim(tr.gate == "parity" and not tr.absorbable,
      "a contradictory 3x3 sign system IS decided at the parity gate by the "
      "shipped predicate: gate=%r absorbable=%s signs_read=%d -- so the branch "
      "is live code, reachable in principle, and simply not reached by anything "
      "this battery constructs" % (tr.gate, tr.absorbable, tr.signs_read))
brute = any(all((-1 if bits >> i & 1 else 1) * A[i][j] *
                (-1 if bits >> j & 1 else 1) == B[i][j]
                for i in range(3) for j in range(3))
            for bits in range(8))
claim(brute is False,
      "and brute force over all 2^3 sign vectors agrees it is not absorbable, "
      "so this pair WOULD separate a broken parity rule -- no pair of its kind "
      "is in the %d the row tests" % n_bf)


# ---------------------------------------------------------------------------
# THE TICKET'S SECOND QUESTION, ANSWERED AS A NUMBER.
#
# "If it wrote prose again, measure the prose against the predicate the way
# mg-1c80 did -- agreement on how many of the 297 pairs?"  It did not write
# prose: the label is emitted at the `return` that fired, so the printed gate
# and the predicate's gate are the same object and agreement is 297 of 297 BY
# CONSTRUCTION.  That is worth stating as the trivial identity it is, and worth
# contrasting with the thing it replaced -- so mg-da45's `deciding_gate` is
# re-run here (from the verbatim copy mg-5f9a kept) against the same 297.
# ---------------------------------------------------------------------------
print()
print("HOW WELL DOES THE PRINTED REASON AGREE WITH THE PREDICATE?")
sys.path.insert(0, os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                 "face_geometry_instr_5f9a")))
from kern5f9a import priority_gate                                      # noqa

agree_trace = sum(1 for A, B in nc4 if absorb_trace(A, B).gate ==
                  absorb_trace(A, B).gate)
agree_prio = sum(1 for A, B in nc4 if priority_gate(A, B) == absorb_trace(A, B).gate)
print("  the SHIPPED label vs the predicate ... %d of %d biting pairs" %
      (agree_trace, len(nc4)))
print("  mg-da45's deciding_gate vs the same ... %d of %d biting pairs" %
      (agree_prio, len(nc4)))
claim(agree_trace == len(nc4),
      "the shipped label agrees with the predicate on %d of the %d NC4 biting "
      "pairs -- necessarily, because it IS the predicate's return value and not "
      "a second procedure.  That is the whole content of the repair"
      % (agree_trace, len(nc4)))
claim(len(nc4) - agree_prio == 57,
      "and the thing it replaced agrees on %d of %d, DIFFERING on %d -- "
      "mg-1c80's '57 of 297', re-measured here and not quoted.  (Note for the "
      "record: the audit ticket phrases this as a relabelling 'agreeing on 57'; "
      "the measurement is that it DISAGREES on 57 and agrees on %d.  mg-5f9a's "
      "commit and landing doc both state it the right way round)"
      % (agree_prio, len(nc4), len(nc4) - agree_prio, agree_prio))

print()
print("E2 claims broken: %d" % BROKEN)
sys.exit(1 if BROKEN else 0)
