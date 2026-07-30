"""A2 -- the NEW NEGATIVE mg-41aa writes, attacked by construction.

The repaired ledger B2 now says: the posets P for which J(P) is an interval
[mu, lambda] of Young's lattice are EXACTLY the skew cell posets.  The
negative half of that -- NO poset outside the skew class has J(P) isomorphic
to an interval -- is what this probe tries to break.

mg-41aa's own §7 attack 1 says this is its weakest link: its lattice-level
converse stops at n <= 5, and n = 6 is covered by Birkhoff's theorem rather
than by measurement.  So this probe is deliberately BIRKHOFF-FREE and runs to
n = 6:

  * intervals are built DIRECTLY as the set of partitions nu with
    mu <= nu <= lambda under containment (kern5800.interval_poset).  No cell
    poset, no J, no join-irreducibles anywhere in that construction;
  * J(P) is built as the inclusion order on the order ideals of P;
  * the two are compared by CANONICAL FORM OF THE LATTICE.

So a poset lands in "interval poset" only if some genuinely-constructed
interval of Young's lattice is isomorphic to its ideal lattice.
"""
import sys, time
from kern5800 import (canon, decode, enumerate_posets, ideal_lattice,
                      interval_poset, partitions_between, skew_shapes,
                      skew_cell_poset, shape_to_mu_lam, straight_shapes, bits)

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 6

print("=" * 78)
print("A2  'EXACTLY THE SKEW CELL POSETS' -- BOTH DIRECTIONS, WITHOUT BIRKHOFF")
print("=" * 78)

ps = enumerate_posets(NMAX)

# ---------------------------------------------------------- smallest witness

print("\n[R1a] THE SMALLEST WITNESS, ISOMORPHISM CONSTRUCTED ELEMENT BY ELEMENT")
P = (0, 0)                                   # the 2-element antichain
m, jup, ids = ideal_lattice(2, P)
els = partitions_between((1,), (2, 1))
print("  P = 2-antichain.  J(P) ideals: %s" % [sorted(bits(i)) for i in ids])
print("  [(1),(2,1)] = %s" % [tuple(x for x in e) for e in els])
# the map: ideal I -> mu + (cells of I placed in the skew diagram (2,1)/(1))
# cell 0 = (row 0, col 1), cell 1 = (row 1, col 0)
def phi(I):
    return (2 if (I >> 0) & 1 else 1, 1 if (I >> 1) & 1 else 0)
img = [phi(i) for i in ids]
print("  phi:")
for i, e in zip(ids, img):
    print("      %-8s -> %s" % (sorted(bits(i)), e))
bij = sorted(img) == sorted(tuple(e) for e in els)
mono = all(((ids[a] & ids[b]) == ids[a]) ==
           all(x <= y for x, y in zip(img[a], img[b]))
           for a in range(m) for b in range(m))
print("  bijective: %s   order-preserving and -reflecting on every pair: %s"
      % (bij, mono))
straight2 = {canon(*skew_cell_poset(s)) for s in straight_shapes(2)}
print("  the 2-antichain is a straight cell poset D_lam: %s"
      % (canon(2, P) in straight2))
w_bad = 0 if (bij and mono and canon(2, P) not in straight2) else 1

# ------------------------------------------ interval classes, built directly

def interval_classes(n, box):
    """{canon of [mu,lambda]} over skew shapes with n cells in the given box.
    The lattice is built from PARTITIONS ONLY."""
    out = {}
    for sh in skew_shapes(n, box):
        mu, lam = shape_to_mu_lam(sh)
        m, up, _ = interval_poset(mu, lam)
        out.setdefault(canon(m, up), (mu, lam))
    return out

print("\n[R1b] INTERVAL LATTICE CLASSES, and the box-growth control ON THE LATTICES")
ivl = {}
moved = 0
for n in range(1, NMAX + 1):
    t = time.time()
    ivl[n] = interval_classes(n, n)
    c1 = len(interval_classes(n, n + 1))
    c2 = len(interval_classes(n, n + 2))
    stable = len(ivl[n]) == c1 == c2
    if not stable:
        moved += 1
    print("  n=%d  interval lattice classes: box n,n+1,n+2 -> %d,%d,%d  %s  (%.1fs)"
          % (n, len(ivl[n]), c1, c2, "stable" if stable else "MOVED", time.time() - t))
print("  lattice-level box movements: %d" % moved)

# ------------------------------ exhaustiveness control: UNNORMALISED pairs

print("\n[R1b-control] UNNORMALISED (mu, lambda) SWEEP -- no row/column trimming")
print("  every pair mu subset lambda with |lambda/mu| = n and lambda inside a")
print("  (n+2) x (n+2) box, with NO left-edge normalisation and NO empty-row ban.")
def all_pairs_classes(n, side):
    def parts(maxpart, maxrows):
        out = [()]
        def rec(acc, prev, rows):
            if rows == maxrows:
                return
            for v in range(1, min(prev, maxpart) + 1):
                acc.append(v)
                out.append(tuple(acc))
                rec(acc, v, rows + 1)
                acc.pop()
        rec([], maxpart, 0)
        return out
    P = parts(side, side)
    bysize = {}
    for p in P:
        bysize.setdefault(sum(p), []).append(p)
    seen = set()
    npairs = 0
    for lam in P:
        for mu in bysize.get(sum(lam) - n, []):
            mup = mu + (0,) * (len(lam) - len(mu))
            if len(mu) > len(lam) or any(a > b for a, b in zip(mup, lam)):
                continue
            npairs += 1
            m, up, _ = interval_poset(mu, lam)
            seen.add(canon(m, up))
    return seen, npairs

ctrl_bad = 0
for n in range(1, min(NMAX, 5) + 1):
    t = time.time()
    s, npairs = all_pairs_classes(n, n + 2)
    same = s == set(ivl[n])
    if not same:
        ctrl_bad += 1
    print("  n=%d  %6d raw (mu,lambda) pairs -> %d classes; normalised gives %d; %s (%.1fs)"
          % (n, npairs, len(s), len(ivl[n]),
             "IDENTICAL" if same else "DIFFER  <-- BAD", time.time() - t))
print("  unnormalised-sweep disagreements: %d" % ctrl_bad)

# ------------------------------------------- the two directions, at the lattice level

print("\n[R1c] EVERY POSET TESTED AGAINST EVERY INTERVAL, n = 1..%d" % NMAX)
skewset = {n: {canon(*skew_cell_poset(s)) for s in skew_shapes(n, n)}
           for n in range(1, NMAX + 1)}
straightset = {n: {canon(*skew_cell_poset(s)) for s in straight_shapes(n)}
               for n in range(1, NMAX + 1)}

tot_interval = 0
tot_straight = 0
tot_all = 0
fwd_bad = []          # skew poset whose J(P) matches NO interval
rev_bad = []          # non-skew poset whose J(P) matches SOME interval
for n in range(1, NMAX + 1):
    t = time.time()
    ivset = set(ivl[n])
    nint = 0
    for code in ps[n]:
        up = decode(n, code)
        m, jup, _ = ideal_lattice(n, up)
        hit = canon(m, jup) in ivset
        if hit:
            nint += 1
        is_skew = code in skewset[n]
        if is_skew and not hit:
            fwd_bad.append((n, code))
        if hit and not is_skew:
            rev_bad.append((n, code))
    tot_interval += nint
    tot_straight += len(straightset[n])
    tot_all += len(ps[n])
    print("  n=%d  posets %-5d  J(P) IS an interval: %-4d  skew classes: %-4d  "
          "straight: %-3d  (%.1fs)"
          % (n, len(ps[n]), nint, len(skewset[n]), len(straightset[n]),
             time.time() - t))

print("\n  TOTALS to n<=%d: %d of %d posets have J(P) an interval; af28's wording"
      % (NMAX, tot_interval, tot_all))
print("  admits %d of them; %d are interval posets that B2's old wording excluded."
      % (tot_straight, tot_interval - tot_straight))
print("\n  DIRECTION 1 (skew => interval): failures %d" % len(fwd_bad))
print("  DIRECTION 2 (interval => skew): COUNTEREXAMPLES FOUND: %d" % len(rev_bad))
for n, code in rev_bad[:5]:
    up = decode(n, code)
    print("      n=%d relations %s"
          % (n, [(i, j) for i in range(n) for j in range(n) if (up[i] >> j) & 1]))

print("\n  mg-41aa's published figures for n<=6: 107 interval posets of 405, "
      "17 straight, 90 excluded")

print("\nSUMMARY a2_exactly: witness bad %d; lattice box movements %d; "
      "unnormalised-sweep disagreements %d; skew-not-interval %d; "
      "interval-not-skew %d; interval posets to n<=%d = %d of %d (straight %d)"
      % (w_bad, moved, ctrl_bad, len(fwd_bad), len(rev_bad), NMAX,
         tot_interval, tot_all, tot_straight))
