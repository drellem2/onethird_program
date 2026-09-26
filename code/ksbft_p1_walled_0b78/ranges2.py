#!/usr/bin/env python3
"""mg-0b78 (KSBFT-P1): ranges of the FINITE witnesses and of the remaining named families,
read from the documents that exhibit them (sources in the doc's triage table). Exact.
Bitmask witnesses use the corpus convention dn[i] = bitmask of elements strictly below i
(code/lstar_reaudit_5e82/out_a1_witness.txt prints this decoding)."""
from lib import *


def from_dn(dn):
    n = len(dn)
    rel = [(j, i) for i in range(n) for j in range(n) if (dn[i] >> j) & 1]
    lt = closure(n, rel)
    for i in range(n):  # the bitmasks are full down-sets: check closure added nothing
        assert sum(1 << j for j in range(n) if lt[j][i]) == dn[i], ("not a down-set list", dn)
    return n, lt


def from_rel(n, rel):
    return n, closure(n, rel)


def staircase(m):  # mg-00a1: evens e_k=2k, odds o_l=2l+1, chains; e_k < o_l iff l >= k+1
    n = 2 * m
    rel = [(2 * k, 2 * k + 2) for k in range(m - 1)] + [(2 * l + 1, 2 * l + 3) for l in range(m - 1)]
    rel += [(2 * k, 2 * l + 1) for k in range(m) for l in range(m) if l >= k + 1]
    return n, closure(n, rel)


def star(m):  # chain C_m plus one free point (W_m, 7ae5 family, 88bd satisfiability witness)
    return disjoint_union(chain(m), chain(1))


def dk(k):  # mg-81ff: k disjoint 2-chains
    return disjoint_union(*[chain(2)] * k)


def cp_ak_cp(p, k):  # mg-a58f
    return ordinal_sum(chain(p), antichain(k), chain(p))


def gap_shift(n, g):  # mg-210d G(n,g): x_i < x_j iff j - i >= g
    return n, closure(n, [(i, j) for i in range(n) for j in range(i + g, n)])


def ac8_ac8_minus_cross():  # mg-88bd corroboration: 8AC ⊕ 8AC minus one cross relation
    n = 16
    rel = [(i, 8 + j) for i in range(8) for j in range(8) if (i, j) != (0, 0)]
    return n, closure(n, rel)


FINITE = [
    ("(L*) refuter n=9 #1 (mg-5cba)", from_dn((0, 1, 0, 4, 0, 0, 32, 96, 239))),
    ("(L*) refuter n=9 #2 (mg-5cba)", from_dn((0, 0, 0, 0, 0, 16, 48, 16, 247))),
    ("(L*) refuter n=10 (mg-789d)", from_dn((0, 1, 3, 0, 9, 0, 32, 96, 255, 239))),
    ("(L*) refuter n=11 (mg-789d)", from_dn((0, 1, 3, 7, 0, 1, 1, 113, 1, 257, 257))),
    ("(F)&(M#) n=10 a (mg-b417, 5e82)", from_dn((0, 0, 0, 7, 15, 31, 15, 6, 135, 135))),
    ("(F)&(M#) n=10 b (mg-b417)", from_dn((0, 0, 3, 0, 8, 0, 56, 127, 127, 123))),
    ("(F)&(M#) n=11 (mg-b417, 5e82)", from_dn((0, 0, 0, 7, 15, 15, 63, 6, 135, 135, 647))),
    ("(F)&(M#) n=12 (mg-5e82)", from_dn((0, 0, 3, 7, 15, 7, 63, 2, 135, 391, 7, 1159))),
    ("(F)&(M#) n=12 (mg-b417 frontier)", from_dn((0, 0, 0, 7, 15, 31, 63, 6, 135, 135, 647, 135))),
    ("probe D pair A (mg-e2de)", from_rel(6, [(0, 1), (1, 2), (1, 4), (2, 3)])),   # {a<b} ⊕ ({c<d} ⊔ {e}), f free
    ("probe D pair B (mg-e2de)", from_rel(6, [(0, 1), (0, 3), (1, 2), (2, 4), (3, 4)])),  # {a} ⊕ ({b<c} ⊔ {d}) ⊕ {e}, f free
    ("per-slot n=6 LP poset (mg-131e)", from_rel(6, [(i, j) for i in range(6) for j in range(i + 1, 6)
                                                     if (i, j) not in {(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (1, 4)}])),
    ("N-poset (mg-f5be)", from_rel(4, [(0, 2), (0, 3), (1, 3)])),
    ("fence n=8 (mg-f5be)", from_rel(8, [(0, 2), (0, 3), (1, 3), (1, 4), (2, 4), (2, 5), (3, 5), (3, 6), (4, 6), (4, 7), (5, 7)])),
    ("probe B n=4 (mg-92e6)", from_rel(4, [(0, 3), (1, 2), (1, 3)])),
    ("mg-623a n=5 argmax", from_rel(5, [(1, 2), (1, 4), (3, 0), (3, 4)])),
    ("Kraft-leak (mg-9d9e)", from_rel(4, [(1, 3), (2, 0)])),
    ("V ⊕ V (mg-8748/8b32, inferred)", ordinal_sum(two_chains := disjoint_union(chain(2), chain(1)), two_chains)),
    ("8AC ⊕ 8AC minus one cross (mg-88bd)", ac8_ac8_minus_cross()),
]

FAMILIES = [
    ("staircase (mg-00a1)", staircase, (2, 3, 4, 6, 8)),
    ("C_m ⊔ C_1 = W_m, 7ae5 family, star", star, (3, 5, 7, 9)),
    ("D_k = k disjoint 2-chains (mg-81ff)", dk, (2, 3, 4, 5)),
    ("C_2 ⊕ A_k ⊕ C_2 (mg-a58f)", lambda k: cp_ak_cp(2, k), (2, 3, 4, 6)),
    ("G(n,3) gap-shift (mg-210d)", lambda n: gap_shift(n, 3), (6, 9, 12, 16)),
    ("G(n,4) gap-shift (mg-210d)", lambda n: gap_shift(n, 4), (8, 12, 16)),
]

if __name__ == "__main__":
    print("finite witnesses:")
    for name, (n, lt) in FINITE:
        d = delta(n, lt) if n <= 12 else None
        print(f"  {name:38s} n={n:2d} range={rng(n, lt):2d} width={width(n, lt):2d}"
              + (f" delta={d} = {float(d):.4f}" if d is not None else ""))
    print("families (range as a function of the size parameter):")
    for name, f, ks in FAMILIES:
        print(f"  {name}: " + ", ".join(f"[{k}: n={f(k)[0]} range={rng(*f(k))}]" for k in ks))
