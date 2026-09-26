"""lemmac.py (audit mg-6c30): does Lemma C (no L-consecutive strict-containment step with exactly 2
separators) fire on every Thm-3.1/2.1*/3.1* survivor found by rand_badl.py?  Re-runs the same seeds."""
import sys, random
from eng import Poset
from badl import all_bad, kills, fmt
from rand_badl import stair_iv

def lemmaC_fires(P, iv, L):
    for i in range(P.n - 1):
        a, b = L[i], L[i + 1]
        if not P.inc[a][b]: continue
        (la, ra), (lb, rb) = iv[a], iv[b]
        strict = (lb < la and ra < rb) or (la < lb and rb < ra)
        if strict and len(P.S(a, b)) == 2: return True
    return False

if __name__ == "__main__":
    seed, ns = int(sys.argv[1]), int(sys.argv[2])
    seen = set(); tot = fired = 0
    for i in range(ns):
        iv = stair_iv(random.Random(seed * 10**6 + 500000 + i))
        if iv in seen: continue
        seen.add(iv); P = Poset.from_iv(iv)
        for L in all_bad(P, cap=5000):
            if kills(P, L): continue
            tot += 1; f = lemmaC_fires(P, iv, L); fired += f
            if not f: print("  Lemma C does NOT fire:", fmt(iv), "|", fmt(iv, L))
    print(f"surviving (P,L): {tot}; Lemma C fires on {fired}")
