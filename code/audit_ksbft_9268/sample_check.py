#!/usr/bin/env python3
"""sample_check.py (mg-9268) -- exact, from-scratch re-verification of
certificates emitted by the search itself (`aud D 58 sample:R`, every R-th
closed node), plus a test of each certificate's CONCLUSION on random
continuations.

For each sampled node (prefix of N elements in canonical order, cut k):
  (a) V_k(prefix) by brute force; CERT: every J contains a,b and
      rho_J in [1/3,2/3]; LP: each pair one-sided as claimed, and
      sum_q lam_q a_qJ >= 0 exactly for every J (Lemma 4);
  (b) CONT random continuations (range <= D kept, canonical order kept,
      0..3D extra elements, generated here independently of both search
      programs): V_k(completion) == V_k(prefix) (safe cut, Lemma 2b), and the
      certified pair (CERT) / some pair of the set (LP) has exact
      probability in [1/3,2/3] in the completion.
usage: sample_check.py D SAMPLE_FILE CONT SEED
"""
import random, sys
from fractions import Fraction
from follow_check import downsets, ext_counts, rho, LO, HI


def inc_counts(dm):
    n = len(dm)
    return [n - 1 - bin(dm[x]).count("1") - sum(1 for y in range(n) if dm[y] >> x & 1) for x in range(n)]


def extend(dm, D, rng):
    """one random new element keeping range <= D and the canonical order; None if no luck"""
    n = len(dm); inc = inc_counts(dm); lo = max(0, n - 2 * D + 1)
    for _ in range(200):
        U = 0
        for pos in range(n - 1, lo - 1, -1):
            succ = sum(1 << j for j in range(pos + 1, n) if dm[j] >> pos & 1)
            if bin(U).count("1") < D and inc[pos] < D and succ & ~U == 0 and rng.random() < 0.5:
                U |= 1 << pos
        Dn = ((1 << n) - 1) & ~U
        dp = bin(dm[-1]).count("1"); d = bin(Dn).count("1")
        if (d, Dn) >= (dp, dm[-1]):
            return dm + [Dn]
    return None


def main():
    D, fn, cont, seed = int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    rng = random.Random(seed)
    nc = nl = bad = ncomp = 0
    for line in open(fn):
        if not line.startswith("SAMPLE"):
            continue
        t = line.split(); N = int(t[1].split("=")[1]); dm = list(map(int, t[2].strip("[]").split(",")))
        kind = t[3]; k = int(t[4].split("=")[1]); toks = t[5:]
        assert len(dm) == N
        Vpre = downsets(dm, N, k)[k] if k > 0 else {0}
        if kind == "CERT":
            nc += 1
            pairs = [tuple(map(int, x.split(","))) for x in toks]
            a, b = pairs[0]
            for J in Vpre:
                r = rho(dm, J, a, b)
                if r is None or not LO <= r <= HI:
                    bad += 1; print("CERT FAILS AT J", line.strip(), J); break
        else:
            nl += 1
            cert = [tuple(map(int, x.split(","))) for x in toks]
            pairs = [(a, b) for (a, b, _, _) in cert]
            for J in Vpre:
                s = Fraction(0)
                for (a, b, side, lam) in cert:
                    r = rho(dm, J, a, b)
                    if r is None or (side < 0 and r > HI) or (side > 0 and r < LO):
                        bad += 1; print("LP SIDE/UNDET FAIL", line.strip()); s = Fraction(-1); break
                    s += lam * ((r - LO) if side < 0 else (HI - r))
                if s < 0:
                    bad += 1; print("LP CERT FAILS AT J", line.strip(), J); break
        for _ in range(cont):
            P = dm
            for _ in range(rng.randint(0, 3 * D)):
                Q = extend(P, D, rng)
                if Q is None:
                    break
                P = Q
            n = len(P)
            assert max(inc_counts(P)) <= D
            Vfull = downsets(P, n, k)[k] if k > 0 else {0}
            if Vfull != Vpre:
                bad += 1; print("SAFE CUT FAILS", line.strip(), P)
            tot, cnt = ext_counts(P, (1 << n) - 1, pairs if kind == "LP" else pairs[:1])
            if not any(LO <= Fraction(c, tot) <= HI for c in cnt.values()):
                bad += 1; print("CONCLUSION FAILS", line.strip(), P)
            ncomp += 1
    print(f"D={D}: {nc} CERT + {nl} LP certificates re-verified from scratch; {ncomp} random range<={D} canonical continuations tested; failures {bad}")


if __name__ == "__main__":
    main()
