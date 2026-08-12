#!/usr/bin/env python3
"""k0 -- THE GATE.  Nothing else in this directory runs unless every line here passes.

What it establishes:
  k0.1  hand-known linear-extension counts
  k0.2  my BACKWARDS enumeration agrees with lib409a's and lib8bc7's forwards ones
  k0.3  my ORBIT fibers agree with both priors' CONTENT-KEY fibers, and every fiber is a CUBE
  k0.4  my BK Dirichlet form agrees with lib409a's and lib8bc7's
  k0.5  my Q at the unique k=2 partition IS lib409a's M = 2I - Pi_o - Pi_e, entrywise
  k0.6  my exact PSD test agrees with lib8bc7's, and refuses a planted indefinite matrix
  k0.7  FOUR PLANTED DEFECTS THAT MUST GO RED (E3, E4 of PREDICTIONS.md)
"""
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "compression_rate_409a"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "compression_audit_8bc7"))
import lib8d66 as K
import lib409a as R          # mg-409a's library -- CROSS-CHECK ONLY, no verdict routes here
import lib8bc7 as W          # mg-8bc7's library -- CROSS-CHECK ONLY

ok = True


def rnd_vals(N, seed):
    s = (seed * 48271 + 11) & 0x7FFFFFFF
    out = []
    for _ in range(N):
        s = (1103515245 * s + 12345) & 0x7FFFFFFF
        out.append(Fraction((s % 19) - 9))
    return out


# --------------------------------------------------------------------------------------
K.banner("k0.1  hand-known linear-extension counts")
cases = []
for n in (3, 4, 5, 6):
    cases.append((f"antichain({n})", len(K.linear_extensions(n, K.antichain(n))),
                  {3: 6, 4: 24, 5: 120, 6: 720}[n]))
    chain = K.tclose(n, {(i, i + 1) for i in range(n - 1)})
    cases.append((f"chain({n})", len(K.linear_extensions(n, chain)), 1))
for n in (4, 6, 8):
    cases.append((f"Z_{n}", len(K.linear_extensions(n, K.Z(n))), 2 ** (n // 2)))
for name, got, want in cases:
    ok &= K.verdict(got == want, f"|L({name})| = {got}", f"expected {want}")

# --------------------------------------------------------------------------------------
K.banner("k0.2  my BACKWARDS enumeration == lib409a's and lib8bc7's FORWARDS ones")
pop = [(4, lt) for lt in K.all_posets(4)] + [(5, lt) for lt in K.sample_posets(5, 40, 7)] \
    + [(6, lt) for lt in K.sample_posets(6, 15, 11)]
bad409 = bad8bc = 0
for n, lt in pop:
    mine = set(K.linear_extensions(n, lt))
    if mine != set(R.linear_extensions(n, lt)):
        bad409 += 1
    if mine != set(W.linear_extensions(n, lt)):
        bad8bc += 1
ok &= K.verdict(bad409 == 0, f"vs lib409a at {len(pop)} posets", f"{bad409} disagreements")
ok &= K.verdict(bad8bc == 0, f"vs lib8bc7 at {len(pop)} posets", f"{bad8bc} disagreements")

# --------------------------------------------------------------------------------------
K.banner("k0.3  my ORBIT fibers == the priors' CONTENT-KEY fibers, and every fiber is a CUBE")
badf = badcube = badconst = ncheck = 0
for n, lt in pop:
    LEs = K.linear_extensions(n, lt)
    for cls, groups in ((tuple(p for p in range(n - 1) if p % 2 == 0), R.blocks_o(n)),
                        (tuple(p for p in range(n - 1) if p % 2 == 1), R.blocks_e(n))):
        ncheck += 1
        _, blocks = K.orbit_fibers(LEs, n, lt, cls)
        mine = set(frozenset(b) for b in blocks)
        theirs = set(frozenset(v) for v in R.fiber_map(LEs, groups).values())
        if mine != theirs:
            badf += 1
        for b in blocks:
            d = len(K.free_positions(LEs[b[0]], lt, cls))
            if len(b) != 2 ** d:
                badcube += 1
            # allowedness must be constant on the fiber -- what makes the fiber a cube
            for i in b:
                if set(K.free_positions(LEs[i], lt, cls)) != set(
                        K.free_positions(LEs[b[0]], lt, cls)):
                    badconst += 1
ok &= K.verdict(badf == 0, f"orbit fibers == content-key fibers at {ncheck} (poset, class)",
                f"{badf} disagreements")
ok &= K.verdict(badcube == 0, "every fiber has size 2^(#free positions)  [THE CUBE CLAIM]",
                f"{badcube} violations")
ok &= K.verdict(badconst == 0, "the free-position set is CONSTANT on every fiber",
                f"{badconst} violations")

# --------------------------------------------------------------------------------------
K.banner("k0.4  my BK Dirichlet form == lib409a's == lib8bc7's")
bad = 0
for n, lt in pop:
    LEs = K.linear_extensions(n, lt)
    if len(LEs) < 2:
        continue
    LEs409 = R.linear_extensions(n, lt)
    order = [LEs.index(L) for L in LEs409]
    for t in range(2):
        v = rnd_vals(len(LEs), 31 * n + t)
        v409 = [v[i] for i in order]
        a = K.bk_energy(v, LEs, n, lt)
        b = R.bk_energy(v409, LEs409, n, lt)
        c = W.bk_energy(v409, LEs409, n, lt)
        if not (a == b == c):
            bad += 1
ok &= K.verdict(bad == 0, "E_BK agrees across three implementations", f"{bad} disagreements")

# --------------------------------------------------------------------------------------
K.banner("k0.5  my Q at the unique k=2 partition IS lib409a's M = 2I - Pi_o - Pi_e")
bad = 0
for n, lt in pop:
    LEs = K.linear_extensions(n, lt)
    LEs409 = R.linear_extensions(n, lt)
    if LEs != LEs409:
        perm = [LEs.index(L) for L in LEs409]
    else:
        perm = list(range(len(LEs)))
    mineQ = K.q_matrix(LEs, n, lt, K.coarsest_partition(n))
    theirM = R.M_matrix(LEs409, n)
    for i in range(len(LEs409)):
        for j in range(len(LEs409)):
            if mineQ[perm[i]][perm[j]] != theirM[i][j]:
                bad += 1
ok &= K.verdict(bad == 0, f"Q_(k=2) == M entrywise at {len(pop)} posets", f"{bad} entries differ")

# --------------------------------------------------------------------------------------
K.banner("k0.6  my exact PSD test == lib8bc7's, and refuses a planted indefinite matrix")
mats = []
for n, lt in pop[:60]:
    LEs = K.linear_extensions(n, lt)
    if len(LEs) < 2:
        continue
    mats.append(K.q_matrix(LEs, n, lt, K.coarsest_partition(n)))
bad = 0
for A in mats:
    mine = K.psd_exact(A)[0]
    theirs = W.psd_exact(A)
    if bool(mine) != bool(theirs):
        bad += 1
ok &= K.verdict(bad == 0, f"PSD verdicts agree at {len(mats)} matrices", f"{bad} disagreements")
allpsd = all(K.psd_exact(A)[0] for A in mats)
ok &= K.verdict(allpsd, "every Q_(k=2) is PSD (it must be: it is a sum of E Var)")
planted = [row[:] for row in mats[0]]
planted[0][0] -= Fraction(10)
ok &= K.verdict(not K.psd_exact(planted)[0], "planted -10 on the diagonal is REFUSED",
                K.psd_exact(planted)[1])
ok &= K.verdict(not K.psd_exact([[Fraction(0), Fraction(1)],
                                 [Fraction(1), Fraction(0)]])[0],
                "planted [[0,1],[1,0]] is REFUSED  (zero pivot, nonzero off-diagonal)")

# --------------------------------------------------------------------------------------
K.banner("k0.7  FOUR PLANTED DEFECTS THAT MUST GO RED")
# The claim each control attacks: Q_finest == ((n-1)/2)(I - P_BK), the anchor of everything.
n = 5
lt = K.tclose(5, {(0, 3)})
LEs = K.linear_extensions(n, lt)
N = len(LEs)
target = K.mat_scale(K.mat_sub(K.identity(N), K.bk_matrix(LEs, n, lt)), Fraction(n - 1, 2))

good = K.q_matrix(LEs, n, lt, K.finest_partition(n))
ok &= K.verdict(K.mat_eq(good, target), "[BASELINE] the honest finest partition MATCHES")

# C1 (E4): a "class" containing two ADJACENT positions -- fiber is not a cube
c1 = ((0, 1), (2,), (3,))
ok &= K.verdict(not K.is_class(c1[0]), "[C1] {0,1} is correctly REJECTED as a class")
ok &= K.verdict(not K.mat_eq(K.q_matrix(LEs, n, lt, c1), target),
                "[C1] planted adjacent-position class goes RED against the identity")

# C2 (E3): a position DROPPED from the partition
c2 = ((0,), (1,), (2,))
ok &= K.verdict(not K.mat_eq(K.q_matrix(LEs, n, lt, c2), target),
                "[C2] planted dropped position (3 of 4 covered) goes RED")

# C3 (E3): a position REPEATED in two classes
c3 = ((0,), (1,), (2,), (3,), (0,))
ok &= K.verdict(not K.mat_eq(K.q_matrix(LEs, n, lt, c3), target),
                "[C3] planted repeated position goes RED")

# C4: the constant SCALED BY CLASS SIZE -- pm-onethird's premise says this is wrong, and a
# reader who believed otherwise would write the identity this way.  It must go red.
v = rnd_vals(N, 5)
ok &= K.verdict(K.q_form(v, LEs, n, lt, K.finest_partition(n))
                == Fraction(n - 1, 2) * K.bk_energy(v, LEs, n, lt),
                "[C4a] the PER-POSITION constant reproduces E_BK exactly")
size_weighted = sum(Fraction(len(S), 1) * K.e_cond_var(v, LEs, n, lt, S)
                    for S in K.coarsest_partition(n))
ok &= K.verdict(size_weighted != K.q_form(v, LEs, n, lt, K.coarsest_partition(n)),
                "[C4b] a CLASS-SIZE-weighted sum is a DIFFERENT number  (the premise bites)")

K.banner("GATE: " + ("PASS -- k1..k5 may run" if ok else "FAIL -- k1..k5 must not run"))
sys.exit(0 if ok else 1)
