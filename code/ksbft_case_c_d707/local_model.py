"""local_model.py (mg-d707): the relaxation Lemma 4.2's proof actually uses.

Variables r, s in [0,1], t >= 1-r, u >= 1-s, subject to (4.6):
    alpha + beta <= v/(1+v),  alpha = (1+s)t/Z,  beta = (1+r)u/Z,  Z = 1+r+s, v = r+s
i.e.  (1+s)t + (1+r)u <= r+s.
Derived quantities (paper eqs 4.3, 4.5, 4.10):
    a     = max(r, s)/Z                  (the triple's best balance)
    eps   = a - C_BFT
    d_m   = r/Z - alpha                   (displacement of x = v_m)
    d_m2  = beta - s/Z                    (displacement of z = v_{m+2})
Every finite poset satisfying Lemma 3.2's conclusions gives a point of this
set, so a bound proved on the set holds for those posets; the converse
fails (it is a relaxation), so a sup over the set is only an upper bound.

Checks printed:
  C1  a >= C_BFT everywhere                      (the BFT bound, paper p.15)
  C2  max|d| <= a everywhere (Prop A of the deliverable; hence max|d| <= 1/2)
  C3  max|d| <= 21 sqrt(eps) when eps <= 1e-5     (Lemma 4.2's content)
  and the empirical sup of max|d|/sqrt(eps) on eps <= 1e-5 (how loose 21 is).
  C4  max|d| <= 24.5 eps everywhere (Prop C, the LINEAR conversion) and the
      empirical sup of max|d|/eps over the whole set.
  C5  the tradeoff g(mu) = inf{ a : max|d| >= mu } on a grid of mu, which
      says whether ANY displacement level forces a >= 1/3 in this model.
EMPIRICAL instrument: random + locally refined sampling, fixed seed.
"""
import math, random
C = (5 - math.sqrt(5)) / 10
RHO = (math.sqrt(5) - 1) / 2

def point(r, s, tf, uf):
    """tf, uf in [0,1] parametrise t, u between their lower bound and the
    largest value (4.6) allows; returns None if infeasible."""
    t0, u0 = 1 - r, 1 - s
    slack = (r + s) - (1 + s) * t0 - (1 + r) * u0
    if slack < 0:
        return None
    t = t0 + tf * slack / (1 + s)
    u = u0 + uf * (slack - (t - t0) * (1 + s)) / (1 + r)
    Z = 1 + r + s
    a = max(r, s) / Z
    dm = r / Z - (1 + s) * t / Z
    dm2 = (1 + r) * u / Z - s / Z
    return a, a - C, max(abs(dm), abs(dm2))

def main():
    rnd = random.Random(20260926)
    minA = 1.0; maxD = 0.0; viol2 = 0; worst_ratio = 0.0; viol3 = 0; n_small = 0; n_feas = 0
    for it in range(400000):
        if it % 2 == 0:
            r, s = rnd.random(), rnd.random()
        else:  # concentrate near the extremal point r = s = rho
            w = 10 ** rnd.uniform(-7, -1)
            r = min(1, max(0, RHO + rnd.uniform(-w, w))); s = min(1, max(0, RHO + rnd.uniform(-w, w)))
        p = point(r, s, rnd.random() ** 3, rnd.random() ** 3)
        if p is None:
            continue
        n_feas += 1
        a, eps, d = p
        minA = min(minA, a); maxD = max(maxD, d)
        if d > a + 1e-12: viol2 += 1
        if eps <= 1e-5:
            n_small += 1
            if eps > 0:
                worst_ratio = max(worst_ratio, d / math.sqrt(eps))
            if d > 21 * math.sqrt(max(eps, 0)) + 1e-12:
                viol3 += 1
    print("feasible samples: %d  (eps<=1e-5: %d)" % (n_feas, n_small))
    print("C1 min a - C_BFT = %.3e   (must be >= -1e-12)" % (minA - C))
    print("C2 violations of max|d| <= a: %d ; max over samples of max|d| = %.6f (Prop A => <= 1/2)" % (viol2, maxD))
    print("C3 violations of max|d| <= 21 sqrt(eps) on eps<=1e-5: %d" % viol3)
    print("   empirical sup max|d|/sqrt(eps) on eps<=1e-5: %.4f   (paper uses 21)" % worst_ratio)
    # C4 / C5 on a dense grid (deterministic)
    K = 0.0; G = 200; best = {}
    mus = [i / 40 for i in range(0, 28)]
    for i in range(G + 1):
        r = i / G
        for j in range(G + 1):
            s = j / G
            for tf in (0, 0.25, 0.5, 0.75, 1):
                for uf in (0, 0.25, 0.5, 0.75, 1):
                    p = point(r, s, tf, uf)
                    if p is None: continue
                    a, eps, d = p
                    if eps > 1e-9: K = max(K, d / eps)
                    for mu in mus:
                        if d >= mu and a < best.get(mu, 9): best[mu] = a
    for it in range(400000):
        r, s = rnd.random(), rnd.random()
        p = point(r, s, rnd.random(), rnd.random())
        if p is None: continue
        a, eps, d = p
        if eps > 1e-9: K = max(K, d / eps)
    print("C4 empirical sup max|d|/eps over the model: %.4f   (Prop C proves <= 24.5)" % K)
    print("C5 g(mu) = min a subject to max|d| >= mu (grid 201x201x5x5):")
    for mu in mus:
        if mu in best: print("     mu=%.3f  g=%.6f  g-C_BFT=%.6f  %s" % (mu, best[mu], best[mu] - C, ">=1/3" if best[mu] >= 1/3 - 1e-12 else "<1/3"))
        else: print("     mu=%.3f  infeasible (no point of the model has max|d| >= mu)" % mu)
    # the two named posets as points of the model
    for name, r, s, t, u in [("2+1 (L'={x}, U'={z})", 1, 1, 0, 0)]:
        Z = 1 + r + s
        print("   %s: a=%.6f M_loc=%.6f" % (name, max(r, s) / Z, max(abs(r / Z - (1 + s) * t / Z), abs((1 + r) * u / Z - s / Z))))

if __name__ == "__main__":
    main()
