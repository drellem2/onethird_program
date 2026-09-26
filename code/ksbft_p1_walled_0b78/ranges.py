#!/usr/bin/env python3
"""mg-0b78 (KSBFT-P1): compute (not guess) the range pi(P), width and delta of each
witness family that killed a walled route, at several sizes, to read off how the range grows.
Exact arithmetic. Deterministic. An INSTRUMENT: it proves nothing beyond the sizes printed;
the growth laws quoted in the doc are proved there by hand, and this checks them."""
from lib import *

def fib(m):  # Z_m / F_m: i < j iff j - i >= 2
    return m, closure(m, [(i, j) for i in range(m) for j in range(i + 2, m)])

def two_chains(p, q):
    return disjoint_union(chain(p), chain(q))

def chain_plus_free(p, q):  # C_p ⊔ A_q (mg-c4f5)
    return disjoint_union(chain(p), antichain(q))

def tight3():  # (2+1) = {a<b} ⊔ {c}
    return two_chains(2, 1)

def wstar_t(a, b, t):
    # A = C_{a-2} ⊕ {x,y}; B = chain b_1<...<b_b; A below B except x !< b_1..b_t
    n = a + b
    rel = []
    cs = list(range(a - 2)); x, y = a - 2, a - 1; bs = list(range(a, a + b))
    rel += [(cs[i], cs[i + 1]) for i in range(len(cs) - 1)]
    if cs:
        rel += [(cs[-1], x), (cs[-1], y)]
    rel += [(bs[i], bs[i + 1]) for i in range(b - 1)]
    rel += [(y, bs[0])]
    rel += [(x, bs[t])] if t < b else []
    return n, closure(n, rel)

def V_boundary(k, s):  # mg-872c boundary class: k copies of V=(2+1)... ordinal sum with s singletons
    return ordinal_sum(*([tight3()] * k + [chain(1)] * s))

def show(name, P, want_delta=True):
    n, lt = P
    d = delta(n, lt) if want_delta and n <= 16 else None
    print(f"  {name:38s} n={n:3d} range={rng(n, lt):3d} width={width(n, lt):3d}"
          + (f" delta={float(d):.6f}" if d is not None else ""))

FAM = [
    ("C_m ⊔ C_m (mg-dcae stability refuter)", lambda m: two_chains(m, m)),
    ("C_m ⊔ C_1 (block-crosser, W_m)", lambda m: two_chains(m, 1)),
    ("C_m ⊔ A_m (mg-c4f5)", lambda m: chain_plus_free(m, m)),
    ("antichain A_m", lambda m: antichain(m)),
    ("Z_m = F_m Fibonacci", lambda m: fib(m)),
    ("(2+1)^{⊕m} (872c boundary, s=0)", lambda m: V_boundary(m, 0)),
    ("W*_2(4, m)", lambda m: wstar_t(4, max(m, 3), 2)),
]
if __name__ == "__main__":
    for name, f in FAM:
        print(name)
        for m in (2, 3, 4, 6, 8):
            try:
                show(name.split(" (")[0], f(m), want_delta=(f(m)[0] <= 12))
            except AssertionError:
                pass
    # CONTROL: the instrument must be able to see a large range
    n, lt = antichain(9)
    assert rng(n, lt) == 8 and width(n, lt) == 9, "control failed"
    n, lt = fib(9)
    assert rng(n, lt) == 2 and width(n, lt) == 2, "control failed"
    assert delta(*tight3()) == Fr(1, 3), "control failed"
    print("controls: antichain range 8 width 9, Z_9 range 2 width 2, delta(2+1)=1/3 — OK")
