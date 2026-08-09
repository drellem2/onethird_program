"""mg-9461 · s1 — the four chains, as exact-rational objects that can be
plugged back into the inequality they claim to solve.

Nothing here is a bound on anything. Every number is arithmetic on
`ε_leak = 1/5` (EMPIRICAL, mg-e35c F5) and on hypothetical values of `C₃` / `c`.
The point of the script is that each chain's `ε_dem` is *derived by solving its
own stated `Φ` bound*, not copied from a table — so a mis-transcribed chain
fails its own plug-back check.

Guards, bound in `PREDICTIONS.md` before this file existed:
  E2 — `Leak` and `Spec` are distinct types; mixing them raises.
  E3 — chain (II) REFUSES `C₃ = 1` unless the caller says `unlicensed=True`,
       because `C₃^(III) = 1` is a chain-(III) statement and `C₃^gap` is
       measured at 1.500/1.473/1.990/2.386 (mg-94c3 §3).
  E1 — no window column is computed or printed anywhere in this directory.

Run: python3 s1_chains.py
"""

from fractions import Fraction as F


# ---------------------------------------------------------------- E2: typed sides

class Leak(F):
    """A bound on `Φ_P(A_k) = Δ₁` — the LEAKAGE side, what Step 5 delivers and
    Step 6 consumes."""
    __slots__ = ()


class Spec(F):
    """A bound on `1 − λ_std` — the SPECTRAL side, what Step 2 delivers."""
    __slots__ = ()


def _require(v, T, what):
    if not isinstance(v, T):
        raise TypeError(f"{what}: expected {T.__name__}, got {type(v).__name__} "
                        f"— E2 guard (leak/spec conflation)")
    return F(v)


# ---------------------------------------------------------------- the four chains
#
# Each chain is (a) the `Φ` bound it asserts, as a function of `ε_spec`, and
# (b) the `ε_dem` it yields, as the solution of `Φ_bound(ε_spec) ≤ ε_leak`.
# `phi_sq` returns `Φ²` so that no square root is ever taken: comparisons are
# done squared, in exact rationals.

class Chain:
    def __init__(self, tag, name, phi_sq, dem, needs):
        self.tag, self.name, self.phi_sq, self._dem, self.needs = \
            tag, name, phi_sq, dem, needs

    def demand(self, eps_leak, **kw):
        eps_leak = _require(eps_leak, Leak, "eps_leak")
        return Spec(self._dem(eps_leak, **kw))

    def plugback(self, eps_leak, **kw):
        """Verify the solve: at `ε_spec = ε_dem` the chain's own `Φ` bound is
        exactly `ε_leak` (tight), and one notch above it is strictly worse."""
        eps_leak = _require(eps_leak, Leak, "eps_leak")
        d = F(self.demand(Leak(eps_leak), **kw))
        if d <= 0:
            return None  # chain does not close at these parameters
        at = self.phi_sq(d, **kw)
        above = self.phi_sq(d * F(101, 100), **kw)
        return (at == eps_leak ** 2, above > eps_leak ** 2)


def _ii_guard(C3, unlicensed):
    if C3 == 1 and not unlicensed:
        raise ValueError(
            "E3 GUARD: refusing to evaluate chain (II) at C_3 = 1. "
            "`C_3 = 1` is PROVEN (on L2's FIRST DISJUNCT) only in chain (III)'s currency "
            "`Phi_pref <= sqrt(2 C_3 eps_spec)`. The gap-form constant this "
            "chain carries is measured at 1.500, 1.473, 1.990, 2.386 over "
            "n = 3..6 and exceeds 1 at 1023 of 1032 posets (mg-94c3 s3). "
            "Substituting 1 here is FALSE, not merely unlicensed.")


# SCOPE REPAIR, mg-3329 (LABELS ONLY — NO MATHEMATICS RE-OPENED).  Three
# strings in this file said "under L2" / "either disjunct" where the truth is
# "L2's FIRST disjunct": chain (I)'s `needs`, chain (III)'s row label, and the
# E3 guard message.  `L2` is a DISJUNCTION, so those spellings asserted the
# unestablished half (mg-fa70, after mg-39bf s2.2).  No formula, parameter,
# population or verdict is touched.  VERIFIED, not asserted: this script
# reproduced `out_s1_chains.txt` BYTE-IDENTICALLY before the edit, and after it
# the diff is exactly three lines, all of them label text, with every number
# unchanged.  mg-9461's ruling is NOT re-opened.
CHAINS = [
    Chain("I", "monotone sweep",
          lambda s, **kw: 2 * s,
          lambda L, **kw: L ** 2 / 2,
          # mg-3329 (on mg-fa70 §3.3): this read "L2 (either disjunct) — Step 3
          # as written".  Chain (I) is the C_3-FREE chain (eps_dem =
          # eps_leak^2/2), so on L2's SECOND disjunct that label asserted
          # precisely the unestablished half: there the delivered prefix's own
          # constant is L2's and is UNNAMED IN THE SOURCE, i.e. an effective
          # C_3 = K^2/2, not 1.  LABEL ONLY — `needs` is never printed and no
          # number in this directory moves (see the note above CHAINS).
          "L2's FIRST DISJUNCT — Step 3 as written. On L2's SECOND disjunct "
          "this chain is NOT established: the prefix is the output, so there "
          "is no CONVERSION to charge for, but its constant is L2's own and "
          "is unnamed in the source (mg-fa70, mg-39bf s2.2)"),
    Chain("II", "gap-form prefix capture",
          lambda s, C3=None, unlicensed=False: (_ii_guard(C3, unlicensed),
                                                (C3 * s) ** 2)[1],
          lambda L, C3=None, unlicensed=False: (_ii_guard(C3, unlicensed),
                                                L / C3)[1],
          "a gap-form prefix-capture theorem `1-rho_pref <= C_3 (1-lambda_std)`"),
    Chain("III", "degraded prefix Cheeger",
          lambda s, C3=None: 2 * C3 * s,
          lambda L, C3=None: L ** 2 / (2 * C3),
          "L3 at a constant loss C_3; = chain (I) at C_3 = 1"),
    Chain("IV", "literal prefix capture",
          lambda s, c=None: (1 - c * (1 - s)) ** 2,
          lambda L, c=None: 1 - (1 - L) / c,
          "Prefix-capture as literally worded, at capture fraction c"),
]
BY_TAG = {ch.tag: ch for ch in CHAINS}


# ---------------------------------------------------------------- report

EPS_LEAK = Leak(F(1, 5))          # mg-e35c F5, EMPIRICAL
EPS_SUP = F(1)                    # sup_{eta>0} (1-3eta) n/(n+1) — approached, not
                                  # attained in the frozen class (E6: carry the eta)


def line(s=""):
    print(s)


def main():
    line("=" * 78)
    line("mg-9461 s1 — THE FOUR CHAINS, SOLVED AND PLUGGED BACK")
    line("=" * 78)
    line(f"eps_leak = {EPS_LEAK}  (= {float(EPS_LEAK)})  EMPIRICAL, mg-e35c F5")
    line("Every eps_dem below is a bound on eps_spec = 1 - lambda_std (SPEC side).")
    line("eps_leak is a bound on Phi = Delta_1 (LEAK side). They are not the same")
    line("quantity and this script types them separately (E2 guard).")
    line("NO WINDOW FIGURE IS COMPUTED ANYWHERE IN THIS DIRECTORY (E1 guard):")
    line("mg-76b2's windows rest on the supply eps_spec = 2/(n+1), REFUTED at")
    line("n = 6 by mg-131e. The replacement is unknown and is not this ticket's.")
    line()

    line("-" * 78)
    line("A. eps_dem AT THE PARAMETERS EACH CHAIN IS ACTUALLY AVAILABLE AT")
    line("-" * 78)
    rows = [
        ("I",   {},                    "no free parameter"),
        ("III", {"C3": F(1)},          "C_3 = 1, PROVEN on L2's FIRST DISJUNCT "
                                       "(mg-76b2, audited; scope mg-fa70/mg-3329)"),
        ("III", {"C3": F(2)},          "C_3 = 2, hypothetical"),
        ("II",  {"C3": F(3, 2), "unlicensed": False},
         "C_3^gap = 3/2, the n=3 MEASUREMENT (mg-94c3)"),
        ("II",  {"C3": F(2386, 1000), "unlicensed": False},
         "C_3^gap = 2.386, the n=6 MEASUREMENT — and RISING"),
        ("IV",  {"c": F(40, 49)},      "c = 40/49, the self-consistent threshold"),
        ("IV",  {"c": F(9, 10)},       "c = 0.90"),
        ("IV",  {"c": F(1)},           "c = 1, the conjecture's own `1-o(1)`"),
    ]
    line(f"{'chain':<6}{'eps_dem':>18}{'decimal':>12}{'tight?':>9}  parameters")
    for tag, kw, note in rows:
        ch = BY_TAG[tag]
        d = ch.demand(EPS_LEAK, **kw)
        pb = ch.plugback(EPS_LEAK, **kw)
        ok = "yes" if pb and pb[0] and pb[1] else ("n/a" if pb is None else "NO")
        line(f"({tag}){'':<2}{str(F(d)):>18}{float(d):>12.6f}{ok:>9}  {note}")
    line()
    line("`tight?` = the chain's own Phi bound evaluated at eps_spec = eps_dem")
    line("equals eps_leak EXACTLY, and is strictly worse 1% above it. A")
    line("mis-transcribed chain fails this.")
    line()

    line("-" * 78)
    line("B. E3 GUARD — chain (II) at C_3 = 1 must REFUSE")
    line("-" * 78)
    try:
        BY_TAG["II"].demand(EPS_LEAK, C3=F(1))
        line("FAIL — the guard did not fire")
        raise SystemExit(1)
    except ValueError as e:
        line("REFUSED, as designed:")
        for w in str(e).split(". "):
            line("   " + w.strip())
    line()
    d_ii = BY_TAG["II"].demand(EPS_LEAK, C3=F(1), unlicensed=True)
    d_iii = BY_TAG["III"].demand(EPS_LEAK, C3=F(1))
    line(f"Forced anyway: (II) at C_3=1 gives {F(d_ii)} vs (III)'s {F(d_iii)} — "
         f"ratio {F(d_ii)/F(d_iii)} = 2/eps_leak.")
    line("That ratio is the ticket's 10x, and it is EXACTLY 2/eps_leak at EVERY")
    line("C_3, because (II)/(III) = (L/C)/(L^2/(2C)) = 2/L with C cancelling.")
    for C in (F(1), F(3, 2), F(7, 3), F(10)):
        r = F(BY_TAG['II'].demand(EPS_LEAK, C3=C, unlicensed=True)) / \
            F(BY_TAG['III'].demand(EPS_LEAK, C3=C))
        assert r == 2 / F(EPS_LEAK), (C, r)
    line("   verified at C_3 = 1, 3/2, 7/3, 10 — ratio is 10 at all four.")
    line()

    line("-" * 78)
    line("C. E2 GUARD — a Spec passed where a Leak belongs must RAISE")
    line("-" * 78)
    try:
        BY_TAG["I"].demand(Spec(F(1, 5)))
        line("FAIL — the guard did not fire")
        raise SystemExit(1)
    except TypeError as e:
        line("REFUSED, as designed: " + str(e))
    line()

    line("-" * 78)
    line("D. NEGATIVE CONTROL — a deliberately wrong chain must FAIL plug-back")
    line("-" * 78)
    bad = Chain("X", "chain (II) mis-derived with a Cheeger square it never pays",
                lambda s, C3=None: (C3 * s) ** 2,
                lambda L, C3=None: L ** 2 / (2 * C3), "-")
    pb = bad.plugback(EPS_LEAK, C3=F(1))
    line(f"wrong-chain plug-back tight? {pb[0]}  (must be False)")
    assert pb[0] is False
    good = BY_TAG["II"].plugback(EPS_LEAK, C3=F(1), unlicensed=True)
    line(f"right-chain plug-back tight? {good[0]}  (must be True)")
    assert good[0] is True
    line("So the plug-back check DISCRIMINATES; it is not vacuously true.")
    line()

    line("-" * 78)
    line("E. SENSITIVITY TO eps_leak — THE SQUARE, MADE EXPLICIT")
    line("-" * 78)
    line("eps_leak is EMPIRICAL. It enters (I)/(III) SQUARED and (IV) LINEARLY.")
    line()
    probes = [
        (F(1, 5),    "0.20   — the live calibration (mg-e35c F5, EMPIRICAL)"),
        (F(17, 78),  "17/78  — mg-3969's ceiling, BOTH-sides-non-chain scope only"),
        (F(1, 7),    "1/7    — mg-d3c7's ceiling in the REQUIRED scope, n <= 7"),
        (F(1, 10),   "0.10   — a factor-2 error in eps_leak"),
        (F(1, 50),   "0.02   — the SUPERSEDED pre-mg-e35c value"),
    ]
    line(f"{'eps_leak':>10}{'(I)/(III,C=1)':>18}{'(IV) at c=1':>16}   note")
    for L, note in probes:
        d1 = F(BY_TAG["I"].demand(Leak(L)))
        d4 = F(BY_TAG["IV"].demand(Leak(L), c=F(1)))
        line(f"{str(L):>10}{str(d1):>18}{str(d4):>16}   {note}")
    line()
    r = F(BY_TAG['I'].demand(Leak(F(1, 5)))) / F(BY_TAG['I'].demand(Leak(F(1, 10))))
    line(f"  A factor-2 move in eps_leak is a factor-{r} move in eps_dem on the")
    line(f"  squared chains, and a factor-2 move on chain (IV) at c=1:")
    r4 = F(BY_TAG['IV'].demand(Leak(F(1, 5)), c=F(1))) / \
         F(BY_TAG['IV'].demand(Leak(F(1, 10)), c=F(1)))
    line(f"    (I)/(III): {r}x      (IV) at c=1: {r4}x")
    r100 = F(BY_TAG['I'].demand(Leak(F(1, 5)))) / F(BY_TAG['I'].demand(Leak(F(1, 50))))
    line(f"  And the corpus's own history is this sensitivity firing: the")
    line(f"  mg-e35c F5 repair moved eps_leak 0.02 -> 0.20, a 10x, and eps_dem")
    line(f"  moved {r100}x. The '100x too pessimistic' banner IS the square.")
    line()

    line("-" * 78)
    line("F. SENSITIVITY TO c — chain (IV) does not close below c = 1 - eps_leak")
    line("-" * 78)
    line(f"  existence threshold      c > 1 - eps_leak            = {1 - F(EPS_LEAK)}")
    e_self = F(BY_TAG['I'].demand(EPS_LEAK))
    line(f"  self-consistent          c >= (1-eps_leak)/(1-eps_dem) = "
         f"{(1 - F(EPS_LEAK)) / (1 - e_self)}")
    line("  and that self-consistent threshold MOVES WITH eps_leak, so an error")
    line("  in eps_leak is not merely a scaling of chain (IV) — it relocates the")
    line("  point at which chain (IV) exists at all:")
    line(f"{'eps_leak':>10}{'existence c >':>16}{'self-consistent c >=':>24}")
    for L, _ in probes:
        ed = F(BY_TAG["I"].demand(Leak(L)))
        line(f"{str(L):>10}{str(1 - L):>16}{str((1 - L) / (1 - ed)):>24}")
    line()

    line("-" * 78)
    line("G. THE DISTANCE TO THE SUPPLY SIDE — what any chain choice can buy")
    line("-" * 78)
    line("Supply: pair bias PROVES 1 - lambda_std <= eps_sup, and")
    line("  max{6 E_mu[inv_e]/(n^2-1) : mu in M_n(eta)} = (1-3eta) n/(n+1),")
    line("  so eps_sup = sup_{eta>0} (1-3eta) n/(n+1) = 1 — APPROACHED, NOT")
    line("  ATTAINED in the frozen class (mg-832f Correction 2; E6 guard).")
    line("  It is an EQUALITY for the information pair bias consumes: no")
    line("  rearrangement moves it (mg-6bc2 Claim 3.1).")
    line()
    line(f"{'chain':<8}{'eps_dem':>14}{'eps_sup/eps_dem':>18}  parameters")
    for tag, kw, note in rows:
        d = F(BY_TAG[tag].demand(EPS_LEAK, **kw))
        if d <= 0:
            continue
        line(f"({tag}){'':<4}{str(d):>14}{str(EPS_SUP / d):>18}  {note}")
    best = max(F(BY_TAG[t].demand(EPS_LEAK, **k)) for t, k, _ in rows)
    worst_of_live = F(BY_TAG["III"].demand(EPS_LEAK, C3=F(1)))
    line()
    line(f"  MOST PERMISSIVE chain in the enumeration: eps_dem = {best} "
         f"(= {float(best)}), at (IV), c = 1.")
    line(f"  ARCHITECTURE-AS-WRITTEN:                  eps_dem = {worst_of_live} "
         f"(= {float(worst_of_live)}), at (I) = (III) at C_3 = 1.")
    line(f"  The chain question is worth exactly {best / worst_of_live}x.")
    line(f"  The gap to the supply side is {EPS_SUP / worst_of_live}x at the")
    line(f"  architecture's own chain and STILL {EPS_SUP / best}x at the most")
    line("  permissive one. NO CHOICE AMONG THE FOUR CHAINS CLOSES THE WALL.")
    line()
    line("=" * 78)
    line("s1 COMPLETE — all guards fired, all plug-backs tight, control fired.")
    line("=" * 78)


if __name__ == "__main__":
    main()
