"""threshold.py (mg-d707): the displacement level mu* at which the local
model of Lemma 4.2 (see local_model.py) first forces a >= 1/3.

max|d| is linear in t (for d_m) and in u (for d_m2) and the feasible (t,u)
set is a triangle, so for fixed (r,s) max|d| is maximised at a vertex; we
evaluate the vertices exactly.  For each (r,s) on an N x N grid we get the
largest achievable max|d| =: Dmax(r,s); then
      g(mu) = min{ a(r,s) : Dmax(r,s) >= mu }.
mu*(1/3) = sup{ mu : g(mu) < 1/3 } = max{ Dmax(r,s) : a(r,s) < 1/3 }.
EMPIRICAL (grid), refined twice around the maximiser.
"""
import math
C = (5 - math.sqrt(5)) / 10

def dmax(r, s):
    Z = 1 + r + s
    t0, u0 = 1 - r, 1 - s
    slack = (r + s) - (1 + s) * t0 - (1 + r) * u0
    if slack < 0:
        return None
    best = 0.0
    for (t, u) in ((t0, u0), (t0 + slack / (1 + s), u0), (t0, u0 + slack / (1 + r))):
        dm = r / Z - (1 + s) * t / Z
        dm2 = (1 + r) * u / Z - s / Z
        best = max(best, abs(dm), abs(dm2))
    return best

def scan(r0, r1, s0, s1, N):
    arg = None; top = -1
    for i in range(N + 1):
        r = r0 + (r1 - r0) * i / N
        for j in range(N + 1):
            s = s0 + (s1 - s0) * j / N
            if not (0 <= r <= 1 and 0 <= s <= 1): continue
            Z = 1 + r + s
            a = max(r, s) / Z
            if a >= 1 / 3: continue
            d = dmax(r, s)
            if d is not None and d > top:
                top = d; arg = (r, s, a)
    return top, arg

top, arg = scan(0, 1, 0, 1, 1000)
print("coarse: mu*(1/3) ~ %.6f at r=%.4f s=%.4f a=%.6f" % (top, *arg))
for w in (0.01, 0.0005):
    top, arg = scan(arg[0] - w, arg[0] + w, arg[1] - w, arg[1] + w, 400)
    print("refine: mu*(1/3) ~ %.8f at r=%.6f s=%.6f a=%.8f" % (top, *arg))
