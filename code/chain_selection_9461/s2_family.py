"""mg-9461 · s2 — the one imported fact this ticket LEANS on, re-verified on an
independent path.

The `ε_leak` half of the deliverable rests on `mg-d3c7` §4.3: in the
architecturally required scope (at least one side non-chain) the uniform
`F`-free transfer surrogate has threshold `0`, refuted by the family

    P(n,k) = chain c_1 < … < c_{n-1}  plus one isolated element z
    A = {z, c_1, …, c_{k-1}},  B = {c_k, …, c_{n-1}},  n = 2k+1.

`mg-d3c7` verified it with a down-set DP and an `n!` cross-check. This file
uses only `lib9461.py`, which shares no line with either that instrument or
`mg-3969`'s, and brute-forces linear extensions by filtering permutations.

It also discharges guard **E4**, filed in `PREDICTIONS.md`: the family must NOT
be read as touching L4. Every member has `δ(P) ≥ 1/3`, so L4's disjunct (i)
holds outright and what falls is the (i)-free surrogate, not L4.

Run: python3 s2_family.py
"""

from fractions import Fraction as F

from lib9461 import (Poset, chain_plus_isolated, delta, delta_1, delta_dp,
                     delta_1_dp, transfer_survives, transfer_survives_dp,
                     is_down_set, pair_probabilities, count_extensions)

BRUTE_MAX = 8          # above this, n! is out of reach and only the DP runs


def line(s=""):
    print(s)


def hand_delta_1(n, k):
    """mg-d3c7 §4.3's closed form: Δ₁ = (n−k) / (n · min(k, n−k))."""
    return F(n - k, n * min(k, n - k))


def check_member(k):
    n = 2 * k + 1
    P = chain_plus_isolated(n)
    A = frozenset([0] + list(range(1, k)))          # z plus c_1..c_{k-1}
    B = frozenset(range(k, n))
    assert len(A) == k and len(B) == n - k
    assert is_down_set(P, A), "A must be a legitimate prefix cut"

    eP = count_extensions(P)
    d1 = delta_1_dp(P, A)
    survA, nbalA, wA = transfer_survives_dp(P, A)
    survB, nbalB, wB = transfer_survives_dp(P, B)
    dlt = delta_dp(P)

    crossed = False
    if n <= BRUTE_MAX:                     # the n! path, where it is affordable
        exts = P.linear_extensions()
        assert len(exts) == eP, (n, len(exts), eP)
        assert delta_1(P, A, exts) == d1, n
        assert delta(P, exts) == dlt, n
        assert transfer_survives(P, A, A, exts)[0] == survA, n
        crossed = True

    QA, _ = P.induced(A)
    QB, _ = P.induced(B)
    return dict(n=n, k=k, eP=eP, d1=d1, d1_hand=hand_delta_1(n, k),
                A_is_chain=QA.is_chain(), B_is_chain=QB.is_chain(),
                nbal=nbalA + nbalB, survives=survA or survB,
                delta=dlt, witness=wA or wB, crossed=crossed)


def main():
    line("=" * 78)
    line("mg-9461 s2 — mg-d3c7's FAMILY, RE-VERIFIED ON AN INDEPENDENT PATH")
    line("=" * 78)
    line("Linear extensions by filtering all n! permutations. Exact rationals.")
    line("No line shared with code/eps0_audit_d3c7/ or code/eps0_threshold_3969/.")
    line()

    line("-" * 78)
    line("A. THE n = 7 WITNESS mg-d3c7 PRINTS BY HAND")
    line("-" * 78)
    P = chain_plus_isolated(7)
    exts = P.linear_extensions()
    A = frozenset({0, 1, 2, 3})
    line(f"   P = chain 1<2<3<4<5<6 plus isolated 0,  e(P) = {len(exts)}   "
         f"(mg-d3c7: 7)")
    line(f"   A = {sorted(A)},  B = {sorted(set(range(7)) - A)}")
    line(f"   Delta_1(A) = {delta_1(P, A, exts)}   (mg-d3c7: 1/7)")
    QA, idx = P.induced(A)
    prA = pair_probabilities(QA)
    inv = {i: v for v, i in idx.items()}
    prP = pair_probabilities(P, exts)
    line("   pairs balanced inside P[A], and where they land in P:")
    for (i, j), p in sorted(prA.items()):
        if not (F(1, 3) <= p <= F(2, 3)):
            continue
        x, y = inv[i], inv[j]
        key = (x, y) if (x, y) in prP else (y, x)
        pf = prP[key] if key == (x, y) else 1 - prP[key]
        verdict = "SURVIVES" if F(1, 3) <= pf <= F(2, 3) else "EVICTED"
        line(f"      ({x},{y}): p_side = {p}   ->   p_P = {pf}   {verdict}")
    s, nb, w = transfer_survives(P, A, A, exts)
    line(f"   side A: {nb} balanced-in-side pair(s), survives = {s}   "
         f"(mg-d3c7: no pair survives)")
    line()

    line("-" * 78)
    line("B. THE FAMILY, MEMBER BY MEMBER (n = 2k+1)")
    line("-" * 78)
    line(f"{'k':>3}{'n':>4}{'e(P)':>6}{'Delta_1':>16}{'=hand?':>8}"
         f"{'n! too?':>9}{'#bal':>6}{'survives':>10}{'delta(P)':>10}{'>=1/3?':>8}")
    ks = [3, 4, 5, 6, 8, 10, 15, 20, 30, 50]
    worst = None
    for k in ks:
        r = check_member(k)
        assert r["d1"] == r["d1_hand"], (k, r)
        assert r["d1"] == F(k + 1, (2 * k + 1) * k), (k, r)
        assert r["B_is_chain"], k
        assert not r["A_is_chain"], k
        assert r["survives"] is False, (k, r)
        assert r["delta"] >= F(1, 3), (k, r)
        line(f"{k:>3}{r['n']:>4}{r['eP']:>6}{str(r['d1']):>16}"
             f"{'yes':>8}{('yes' if r['crossed'] else '-'):>9}{r['nbal']:>6}"
             f"{str(r['survives']):>10}{str(r['delta']):>10}{'yes':>8}")
        worst = r["d1"]
    line()
    line(f"   Delta_1 = (k+1)/((2k+1)k) at every member, verified against the")
    line(f"   hand formula on the DP path and cross-checked against the n! path")
    line(f"   wherever n <= {BRUTE_MAX}. At k = {ks[-1]}, "
         f"Delta_1 = {worst} = {float(worst):.6f}, still falling.")
    line("   0 of these members has a surviving pair, and every one has")
    line("   delta(P) >= 1/3 — so L4's disjunct (i) HOLDS and L4 is untouched.")
    line("   E4 GUARD DISCHARGED.")
    line()

    line("-" * 78)
    line("C. WHAT THIS MEANS FOR eps_leak — stated as the limit it is")
    line("-" * 78)
    line("   The family drives Delta_1 -> 0 with every balanced-in-side pair")
    line("   evicted, so the UNIFORM (i)-free surrogate has threshold 0 in the")
    line("   architecturally required scope. There is therefore NO reading in")
    line("   which the corpus's eps_leak = 0.20 is a proven lower bound, and")
    line("   one live reading in which it is already ABOVE a proven ceiling:")
    for lab, val in [("mg-3969, BOTH sides non-chain, n <= 7", F(17, 78)),
                     ("mg-d3c7, ONE+ side non-chain, n <= 7 (required)", F(1, 7)),
                     ("mg-d3c7, ONE+, uniform in n (required)", F(0))]:
        rel = ("ABOVE it" if F(1, 5) > val else "below it")
        line(f"      ceiling {str(val):>6} = {float(val):.6f}   0.20 is {rel:9}"
             f"   [{lab}]")
    line()
    line("   NEGATIVE CONTROL — the surrogate is not trivially false. A cut with")
    line("   both sides non-chain, at a poset with a genuinely thin interface,")
    line("   must be able to SURVIVE, or this predicate would be vacuous:")
    # 2+2: a<b, c<d ; A = {a,c}, B = {b,d}
    Q = Poset(4, [(0, 1), (2, 3)])
    qe = Q.linear_extensions()
    QA_ = frozenset({0, 2})
    sv, nb2, w2 = transfer_survives(Q, QA_, QA_, qe)
    line(f"      P = 2+2 (a<b, c<d), A = {{a,c}}, B = {{b,d}}:  e(P) = {len(qe)}, "
         f"Delta_1 = {delta_1(Q, QA_, qe)}")
    line(f"      balanced-in-side pairs = {nb2}, survives = {sv}   "
         f"(control fires: a surviving case exists)")
    assert sv is True, "control failed — the predicate would be vacuous"
    line()
    line("=" * 78)
    line("s2 COMPLETE — family reproduced independently, E4 discharged, "
         "control fired.")
    line("=" * 78)


if __name__ == "__main__":
    main()
