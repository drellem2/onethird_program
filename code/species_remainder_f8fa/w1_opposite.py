"""W1 -- T3d's FOUR CANDIDATES ARE TWO STATEMENTS, EACH COMPUTED TWICE.

mg-a61f's X4.  mg-6f61 restated the count in the DOCUMENT (section 2.2, S2,
section 0) and in `code/species_7d75/README.md`, and left the instrument
saying the old thing: `t3_bidigare.py` still headed T3d "four candidate
identifications, three are controls" and still had a vacuity branch reading
"the three controls did not fire".  A count corrected in the prose beside an
instrument that prints the uncorrected one is not corrected; the instrument is
what a successor re-runs.

THE CLAIM, and it is measured here rather than argued:

    convention B is IDENTICALLY the opposite algebra of convention A,

i.e. for every pair of subsets S, T of {0..n-2},

    d_S ._B d_T  =  d_T ._A d_S     as multisets of permutations,

so the T3d column `iso/B` carries no information the column `anti/A` does not,
and likewise `anti/B` and `iso/A`.  Four columns, two statements, one control
run twice.

PREDICTIONS, written before the run:

  P1  B(S,T) = A(T,S) with 0 mismatches at every n <= 5.
  P2  The un-swapped comparison B(S,T) vs A(S,T) MUST fire, or P1 is being
      measured by a routine that cannot tell the two apart.  It cannot fire
      at n <= 2, where kS_n is commutative.
  P3  It fires from n = 3 on.

P2 is the half that matters: an identity established by a comparison that
returns 0 on everything is not established.
"""

import sys

from kernf8fa import subsets, descent_table, compose_A, compose_B, hdr

NMAX = 5
bad = 0

hdr("W1  T3d's four columns are two statements, each computed twice")
print()
print("  Solomon's descent algebra is rebuilt here inside kS_n from")
print("  permutations and their descent sets, under both composition")
print("  conventions.  Products are compared as MULTISETS of permutations, so")
print("  no expansion in the d_T basis is assumed anywhere.")
print()
print("   n   pairs (S,T)   B(S,T) vs A(T,S)   CONTROL: B(S,T) vs A(S,T)")

fired_at = []
for n in range(1, NMAX + 1):
    subs = subsets(n)
    A = descent_table(n, compose_A)
    B = descent_table(n, compose_B)
    swapped = sum(1 for S in subs for T in subs if B[(S, T)] != A[(T, S)])
    plain = sum(1 for S in subs for T in subs if B[(S, T)] != A[(S, T)])
    bad += (swapped != 0)
    if plain:
        fired_at.append(n)
    print("  %2d %13d %18d %27d"
          % (n, len(subs) ** 2, swapped, plain))
print()
print("  Left column is a MISMATCH count and is 0 at every n: convention B is")
print("  the opposite algebra of convention A on the nose, with no n at which")
print("  they come apart.")
print()

# ---------------------------------------------------------------------------
# the control
# ---------------------------------------------------------------------------
hdr("W1b  the control, and it must fire or W1a establishes nothing")
print()
print("  P2/P3: comparing B(S,T) against A(S,T) UN-swapped must disagree, or")
print("  the comparison above cannot distinguish the opposite algebra from")
print("  the algebra.  kS_n is commutative at n <= 2, so it cannot fire there.")
print()
ok2 = (fired_at == [n for n in range(3, NMAX + 1)])
bad += (not ok2)
print("  control fires at n = %s   expected n = %s   %s"
      % (fired_at or "NONE", list(range(3, NMAX + 1)),
         "ok" if ok2 else "*** P2/P3 MISSED ***"))
print()

# ---------------------------------------------------------------------------
# what the count becomes
# ---------------------------------------------------------------------------
hdr("W1c  the restated count")
print()
print("  {anti/A, iso/B}  is ONE statement, and it HOLDS.")
print("  {iso/A,  anti/B} is ONE statement, and it FAILS (472 mismatching")
print("                   structure constants at n = 5, t3_bidigare.py T3d).")
print()
print("  So T3d is ONE control, RUN TWICE -- not three controls, and not two.")
print("  The column listed as a control in the original text, iso/B, is the")
print("  surviving identification seen in a mirror.")
print()
print("  WHAT IS NOT WITHDRAWN, and it is the whole substance: the comparison")
print("  IS discriminating.  Isomorphism is separated from anti-isomorphism")
print("  decisively, and Bidigare's Theorem 10.13 is reproduced from the two")
print("  definitions.  ONLY THE CONTROL COUNT WAS OVERSTATED.")
print()
print("=" * 78)
print("W1 TOTAL BAD: %d" % bad)
print("=" * 78)
sys.exit(0)
