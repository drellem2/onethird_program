"""R2 -- mg-a61f's X3: WHICH OF THE FIVE COLUMNS CAN FAIL, AND UNDER WHAT.

WHAT WAS WRONG.  mg-7d75 section 0 says

    "0 failures across 5 axioms on 4 399 basis elements"

and its own section 5 says, of the same table,

    "what T5 establishes is CLOSURE of our two subspecies under published
     operations ... and NOT that the operations are forced."

Those two sentences are in one document and they do not agree.  mg-a61f
measured the gap: fed a subset closed under nothing, the identical battery
still returns 0 on associativity, coassociativity and compatibility while
the closure columns fire.  The defect to repair is the DISAGREEMENT, and it
is repaired by making section 0 agree with section 5 -- not by weakening
section 5, which was right.

WHAT THIS FILE ADDS OVER mg-a61f's A3b.  A3b establishes that three columns
do not respond to the COLLECTION.  It does not ask whether they can respond
to anything, so "cannot fail" is left as an inference.  Here every column
gets an explicit two-part verdict --

    can it fail by varying the COLLECTION, the operations held fixed?
    can it fail by varying the OPERATIONS, the collection held fixed?

-- and both halves are DEMONSTRATED, on mutations whose outcome was written
down before the run.

THE PREDICT-FIRST DISCIPLINE.  Every mutation below carries the five-column
outcome THIS REPAIR PREDICTED BEFORE THE RUN, written into this file before
it was executed.  The run prints predicted-vs-actual for all 40 cells.  A
battery whose expectations are written after the run cannot be wrong, which
is the same as saying it cannot be evidence.
"""

import sys

from kern6f61 import (COLUMNS, axioms, bits, concat, faces_on, is_lower_set,
                      compositions_on, part_union, posets_on, restrict_face,
                      restrict_part, restrict_poset, submasks, supp,
                      union_poset)

N = 4
FULL = (1 << N) - 1
bad = 0


def hdr(t):
    print("=" * 78)
    print(t)
    print("=" * 78)
    print()


# ---------------------------------------------------------------------------
# the collections
# ---------------------------------------------------------------------------

def opposite(up):
    out = [0] * N
    for i in range(N):
        for j in bits(up[i]):
            out[j] |= 1 << i
    return tuple(out)


def univ_F(mask):
    return {(up, F) for up in posets_on(mask, N) for F in faces_on(up, mask)}


def univ_ambient(mask):
    return {(up, F) for up in posets_on(mask, N)
            for F in compositions_on(mask)}


def univ_F_opposite(mask):
    """The poset kept, paired with the faces of the OPPOSITE cone.  Same size
    as F, semantically the wrong pairing."""
    return {(up, F) for up in posets_on(mask, N)
            for F in faces_on(opposite(up), mask)}


def univ_F_broken(mask):
    """Every second element of F in a fixed order -- closed under nothing."""
    els = sorted(univ_F(mask))
    return set(els[::2])


def univ_chains(mask):
    """Only the (poset, face) pairs whose poset is a CHAIN.  Chains are not
    closed under disjoint union; they ARE closed under induced subposet and
    the coproduct's restriction."""
    out = set()
    k = len(bits(mask))
    for up in posets_on(mask, N):
        rel = sum(bin(u).count("1") for u in up)
        if rel == k * (k - 1) // 2:
            for F in faces_on(up, mask):
                out.add((up, F))
    return out


def univ_evenblocks(mask):
    """An ARBITRARY predicate with no closure meaning at all: faces with an
    even number of blocks."""
    return {(up, F) for up in posets_on(mask, N) for F in faces_on(up, mask)
            if len(F) % 2 == 0}


def build(fn):
    return {mask: fn(mask) for mask in submasks(FULL)}


# ---------------------------------------------------------------------------
# the operations
# ---------------------------------------------------------------------------

def mu(x, y):
    return (union_poset(x[0], y[0], N), concat(x[1], y[1]))


def de(x, S, T):
    up, F = x
    if not is_lower_set(up, S, N):
        return None
    return ((restrict_poset(up, S, N), restrict_face(F, S)),
            (restrict_poset(up, T, N), restrict_face(F, T)))


def mu_rot(x, y):
    """concatenate, then rotate the blocks by one.  Not associative."""
    F = concat(x[1], y[1])
    F = F[1:] + F[:1] if F else F
    return (union_poset(x[0], y[0], N), F)


def de_swap(x, S, T):
    """restriction, with the two tensor factors interchanged."""
    d = de(x, S, T)
    return None if d is None else (d[1], d[0])


def mu_merge(x, y):
    """concatenate, merging the LAST block of x with the FIRST block of y.

    This is a face of the union cone (block indices only shift, never cross),
    it is associative, and it is not the Hopf-monoid product.
    """
    F, G = x[1], y[1]
    if F and G:
        H = F[:-1] + (F[-1] | G[0],) + G[1:]
    else:
        H = concat(F, G)
    return (union_poset(x[0], y[0], N), H)


# ---------------------------------------------------------------------------
# PREDICTIONS.  Written before the first execution of this file.
#   0  = predicted exactly zero
#   +  = predicted strictly positive
# ---------------------------------------------------------------------------
NZ = "+"

COLLECTION_ROWS = [
    ("B0  F (ours)", univ_F, ("0", "0", "0", "0", "0"),
     "the baseline mg-7d75 reports"),
    ("C1  the full ambient P x Sigma", univ_ambient,
     ("0", "0", "0", "0", "0"),
     "closed, because it is the whole Hadamard product"),
    ("C2  F-opposite (wrong pairing)", univ_F_opposite,
     ("0", "0", "0", "0", "0"),
     "same size as F, semantically wrong, and still closed"),
    ("C3  F-broken (every 2nd element)", univ_F_broken,
     (NZ, NZ, "0", "0", "0"),
     "closed under nothing; only the closure columns may move"),
    ("C4  chains only", univ_chains, (NZ, "0", "0", "0", "0"),
     "not closed under disjoint union; IS closed under restriction"),
    ("C5  even number of blocks", univ_evenblocks, (NZ, NZ, "0", "0", "0"),
     "an arbitrary predicate with no closure meaning"),
]

OPERATION_ROWS = [
    ("O1  product = rotate(concat)", mu_rot, de, (NZ, "0", NZ, "0", NZ),
     "leaves the cone, and is not associative"),
    ("O2  coproduct = restriction, factors swapped", mu, de_swap,
     ("0", NZ, "0", NZ, NZ),
     "lands in the wrong component and is not coassociative"),
    ("O3  product = merge last block with first", mu_merge, de,
     ("0", "0", "0", "0", NZ),
     "stays in the cone and IS associative; only compatibility should go"),
]


missed = 0


def verdict(pred, got):
    if pred == "0":
        return got == 0
    return got > 0


def run_row(label, universe, mu_, de_, pred, note):
    global missed
    f = axioms(universe, mu_, de_, FULL)
    got = tuple(f[c] for c in COLUMNS)
    oks = [verdict(p, g) for p, g in zip(pred, got)]
    miss = oks.count(False)
    missed += miss
    print("  %-42s %6d" % (label, len(universe[FULL])))
    print("      predicted  %s" % "  ".join("%9s" % p for p in pred))
    print("      actual     %s" % "  ".join("%9d" % g for g in got))
    print("      verdict    %s"
          % "  ".join("%9s" % ("ok" if o else "MISS") for o in oks))
    print("      %s" % note)
    print()
    return got, miss


# ---------------------------------------------------------------------------
hdr("R2a  the five columns, the collection varied, the operations fixed")

print("  Operations held fixed at the published ones: product = concatenation")
print("  in the Hadamard product P x Sigma, coproduct = restriction with the")
print("  lower-set condition (Aguiar-Mahajan 13.1.1 / 13.4.2 / 8.13).  Only")
print("  the SET of basis elements changes.")
print()
print("  %-42s %6s" % ("collection", "on [4]"))
print("      %-10s %s" % ("", "  ".join("%9s" % c for c in COLUMNS)))
print()

coll_got = {}
for label, fn, pred, note in COLLECTION_ROWS:
    u = build(fn)
    coll_got[label], _ = run_row(label, u, mu, de, pred, note)

axis1 = {c: any(coll_got[l][i] > 0 for l in coll_got)
         for i, c in enumerate(COLUMNS)}

print("  READING.  Associativity, coassociativity and compatibility return 0")
print("  for a collection closed under NOTHING, for one closed under only")
print("  half of the operations, and for an arbitrary predicate.  They are")
print("  identities of the AMBIENT operations -- associativity of")
print("  concatenation and coassociativity of restriction are identities of")
print("  tuples and of sets -- so no choice of sub-collection can move them.")
print()

# ---------------------------------------------------------------------------
hdr("R2b  the same five columns, the operations varied, the collection fixed")

print("  Collection held fixed at F, 4 399 basis elements on [4].  Only the")
print("  MAPS change.  This is the half A3b does not run, and without it")
print("  'these three columns cannot fail' is an inference rather than a")
print("  measurement.")
print()

op_got = {}
uF = build(univ_F)
for label, m, d, pred, note in OPERATION_ROWS:
    op_got[label], _ = run_row(label, uF, m, d, pred, note)

axis2 = {c: any(op_got[l][i] > 0 for l in op_got)
         for i, c in enumerate(COLUMNS)}

# ---------------------------------------------------------------------------
hdr("R2c  THE PER-COLUMN VERDICT")

print("  %-16s %-24s %-24s" % ("column", "fails on a COLLECTION?",
                               "fails on an OPERATION?"))
for c in COLUMNS:
    print("  %-16s %-24s %-24s"
          % (c, "YES" if axis1[c] else "NO -- pinned at 0",
             "YES" if axis2[c] else "NO"))
print()
print("  So the honest count of what the table in section 5 establishes:")
print()
print("    * TWO columns are tests OF OUR TWO SUBSPECIES -- product closure")
print("      and coproduct closure.  Both can fail and both are measured at")
print("      0, over 4 399 basis elements.  That is the result: F and AC are")
print("      CLOSED under the published operations.")
print("    * THREE columns are tests OF THE AMBIENT HADAMARD PRODUCT.  They")
print("      are verified ONCE, not 4 399 times, and no sub-collection can")
print("      move them.  They are not evidence about F and AC at all.")
print()
print("  And the two columns that CAN fail return 0 for the full ambient and")
print("  for a deliberately wrong pairing as well as for ours, so what they")
print("  establish is CLOSURE and not IDENTIFICATION.")
print()

# ---------------------------------------------------------------------------
hdr("R2d  O3 is a compatibility control that section 5 did not have")

print("  mg-7d75's four controls (i)-(iv) leave compatibility without an")
print("  isolated control: (ii) the Tits product breaks closure,")
print("  associativity and compatibility together -- and mg-a61f's X5 shows")
print("  its 1 442 product failures are exactly the 1 442 disjoint-ground-set")
print("  pairs, so it fires on a type mismatch.  O3 above stays inside the")
print("  cone, is associative, keeps the coproduct, and breaks compatibility")
print("  alone.  That is the control the section was missing, and it is")
print("  reported here rather than folded into the section-5 table, because")
print("  the section-5 table is mg-7d75's and this is a repair.")
print()

# ---------------------------------------------------------------------------
hdr("R2e  THE TWO MISSED PREDICTIONS, AND WHY THEY MISSED")

print("  Written before the run, missed, and kept exactly as written.  Neither")
print("  is edited away and neither changes a per-column verdict; both make")
print("  the reading in R2c stronger rather than weaker.")
print()
print("  C5, product closure: predicted +, got 0.  I called 'an even number of")
print("  blocks' an ARBITRARY predicate with no closure meaning.  It is not")
print("  arbitrary: concatenation ADDS block counts, so the even-block faces")
print("  are closed under the product by parity, and only the coproduct sees")
print("  it.  A predicate with no geometric content whatever passes the")
print("  product-closure column -- which is X3's point about that column, made")
print("  by an accident I did not foresee.")
print()
print("  O2, compatibility: predicted +, got 0.  Interchanging the two tensor")
print("  factors of the coproduct is a SYMMETRY of the compatibility axiom:")
print("  swapping Delta on both sides of")
print("      Delta_{S2,T2} . mu_{S1,T1}  =  (mu (x) mu) . (Delta (x) Delta)")
print("  permutes the four corners A,B,C,D consistently, so the two sides move")
print("  together.  Coassociativity is not symmetric that way and it fires,")
print("  266 459 times.  The lesson is the one X5 states about control (ii):")
print("  a corruption is not a control until you know which column it can")
print("  reach.")
print()

# ---------------------------------------------------------------------------
hdr("R2f  PREDICTED vs ACTUAL, summary")

total = 5 * (len(COLLECTION_ROWS) + len(OPERATION_ROWS))
undemonstrated = [c for c in COLUMNS if not (axis1[c] or axis2[c])]
bad += len(undemonstrated)
print("  %d cells, every one of them predicted before the run." % total)
print("  cells missed: %d  (both explained in R2e)" % missed)
print("  columns with NO demonstrated failure on either axis: %d %s"
      % (len(undemonstrated), undemonstrated if undemonstrated else ""))
print()
print("  TOTAL BAD below counts columns left UNDEMONSTRATED, which is the")
print("  failure mode this file exists to exclude.  The missed predictions are")
print("  reported on their own line, above and in run_all.sh's summary, and")
print("  are not folded into it -- a miss is a finding, and a finding that is")
print("  counted as a fault gets edited away.")
print()
print("=" * 78)
print("R2 PREDICTIONS MISSED: %d of %d" % (missed, total))
print("R2 TOTAL BAD: %d" % bad)
print("=" * 78)
sys.exit(0)
