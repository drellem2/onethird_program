"""relax.py (mg-3a14) -- independent sampler of the Lemma 4.2 relaxation:
r,s in [0,1], t >= 1-r, u >= 1-s, (1+s)t + (1+r)u <= r+s  (this is (4.6)
with alpha=(1+s)t/Z, beta=(1+r)u/Z).  Checks Prop A (|d| <= a), Prop C
(|d| <= 24.5 eps), and the threshold sup{max|d| : a < 1/3}.  Deterministic."""
import random, math
random.seed(3141)
C = (5 - math.sqrt(5)) / 10
worstA = -1; worstC = 0; mu = 0; n = 0; bestC_pt = None
def point(r, s, t, u):
    global worstA, worstC, mu, n, bestC_pt
    if not (t >= 1-r-1e-15 and u >= 1-s-1e-15 and (1+s)*t + (1+r)*u <= r+s+1e-15): return
    Z = 1 + r + s; a = max(r, s)/Z
    dm = r/Z - (1+s)*t/Z; dm2 = (1+r)*u/Z - s/Z
    d = max(abs(dm), abs(dm2)); n += 1
    worstA = max(worstA, d - a)
    eps = a - C
    if eps > 1e-12 and d/eps > worstC: worstC = d/eps; bestC_pt = (r, s, t, u)
    if a < 1/3: mu = max(mu, d)
for _ in range(2_000_000):
    r = random.random(); s = random.random()
    # sample t,u on the feasible slice
    t0, u0 = 1-r, 1-s
    slack = r + s - (1+s)*t0 - (1+r)*u0
    if slack < 0: continue
    lam = random.random()**random.choice([1, 3, 10]); w = random.random()
    point(r, s, t0 + lam*w*slack/(1+s), u0 + lam*(1-w)*slack/(1+r))
# near the golden point and near r=s=1
for _ in range(1_000_000):
    rho = (math.sqrt(5)-1)/2
    sc = 10**random.uniform(-8, -1)
    r = min(1, max(0, rho + random.uniform(-1, 1)*sc)); s = min(1, max(0, rho + random.uniform(-1, 1)*sc))
    t0, u0 = 1-r, 1-s; slack = r + s - (1+s)*t0 - (1+r)*u0
    if slack < 0: continue
    lam = random.random(); w = random.random()
    point(r, s, t0 + lam*w*slack/(1+s), u0 + lam*(1-w)*slack/(1+r))
for k in range(1, 12):
    eta = 10**-k; point(1-eta, 1-eta, eta, eta)
print(f"feasible points={n}")
print(f"Prop A: max(|d| - a) = {worstA:.3e}  (<= 0 means no violation)")
print(f"Prop C: sup |d|/eps sampled = {worstC:.4f} at (r,s,t,u)={tuple(round(x,6) for x in bestC_pt)}  (claim: < 24.5; doc's C4 says ~5.85)")
print(f"threshold: sup max|d| over a<1/3 = {mu:.8f}  (doc: 1/3, approached at r=s->1)")
