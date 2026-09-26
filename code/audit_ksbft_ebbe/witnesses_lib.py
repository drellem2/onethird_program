"""shared 2+2 / nesting helpers (audit mg-ebbe)."""
from census import ups

def inc(dn, a, b): return a != b and not dn[a] >> b & 1 and not dn[b] >> a & 1

def has_2p2(dn):
    n = len(dn)
    for a in range(n):
        for x in range(n):
            if not dn[x] >> a & 1: continue
            for c in range(n):
                for y in range(n):
                    if dn[y] >> c & 1 and inc(dn, a, y) and inc(dn, c, x) and inc(dn, a, c) and inc(dn, x, y):
                        return True
    return False

def nonnested(dn):
    up = ups(dn); n = len(dn)
    return sum(1 for a in range(n) for b in range(a + 1, n) if inc(dn, a, b) and
               dn[a] & ~dn[b] and dn[b] & ~dn[a] and up[a] & ~up[b] and up[b] & ~up[a])

