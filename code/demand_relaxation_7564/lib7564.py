"""mg-7564 — the demand-side ladder, in exact rationals.

WHAT THIS LIBRARY IS.  Four chains convert a spectral budget `eps_spec` into the ONE
hypothesis Step 6 consumes, `Delta_1 <= eps_leak`.  Each chain is defined here by ITS OWN
`Phi` bound; `eps_dem` is then SOLVED from that bound rather than copied from any table,
so a mis-transcription fails the plug-back check in `d0`.

WHAT IT IS NOT.  It enumerates no posets and measures nothing.  Every empirical input is
typed in with its citation and its status.  It shares no line of code with `lib9461.py`,
`lib76b2.py`, `lib81ff.py` or `lib_00b3.py`; agreement with those is therefore a result and
not inheritance.

TYPING.  `Spec` and `Leak` are distinct types and are not interchangeable.  `eps_spec` is a
bound on `1 - lambda_std`; `eps_leak` is a bound on `Phi = Delta_1`.  Conflating them is
the defect `mg-9461`'s E2 guard exists to catch, and it is caught here the same way.
"""

from fractions import Fraction as F


# ---------------------------------------------------------------------------
# 0.  The two typed quantities.  A Spec where a Leak belongs must RAISE.
# ---------------------------------------------------------------------------

class Spec:
    """A bound on the spectral gap `1 - lambda_std`."""
    __slots__ = ("v",)

    def __init__(self, v):
        self.v = F(v)

    def __repr__(self):
        return f"Spec({self.v})"


class Leak:
    """A bound on the interface leak `Phi = Delta_1`."""
    __slots__ = ("v",)

    def __init__(self, v):
        self.v = F(v)

    def __repr__(self):
        return f"Leak({self.v})"


class TypeGuard(Exception):
    """Raised when a Spec is passed where a Leak belongs, or the reverse."""


def _leak(x):
    if not isinstance(x, Leak):
        raise TypeGuard(f"expected Leak, got {type(x).__name__} — E2 guard "
                        f"(leak/spec conflation)")
    return x.v


def _spec(x):
    if not isinstance(x, Spec):
        raise TypeGuard(f"expected Spec, got {type(x).__name__} — E2 guard "
                        f"(leak/spec conflation)")
    return x.v


# ---------------------------------------------------------------------------
# 1.  The four chains, each as ITS OWN Phi bound.
#     Source: mg-76b2 §6 (the table), read as four DEFINITIONS and not as four
#     answers.  eps_dem is solved from these below, never copied.
# ---------------------------------------------------------------------------

def phi_I(eps_spec):
    """(I) monotone sweep:            Phi <= sqrt(2 * eps_spec).   No constant."""
    return _sqrt(2 * _spec(eps_spec))


def phi_II(eps_spec, c3gap):
    """(II) gap-form prefix capture:  Phi <= C3^gap * eps_spec.    Cheeger square NOT paid."""
    return F(c3gap) * _spec(eps_spec)


def phi_III(eps_spec, c3):
    """(III) degraded prefix Cheeger: Phi <= sqrt(2 * C3 * eps_spec)."""
    return _sqrt(2 * F(c3) * _spec(eps_spec))


def phi_IV(eps_spec, c):
    """(IV) literal prefix capture:   Phi <= 1 - c*(1 - eps_spec)."""
    return 1 - F(c) * (1 - _spec(eps_spec))


def _sqrt(x):
    """Exact square root of a Fraction when it is one; otherwise refuse.

    Chains (I) and (III) are only ever evaluated here at points where the square
    root IS exact (that is what the plug-back check arranges), so a float never
    reaches a decision.  Anywhere else this raises rather than silently rounding.
    """
    x = F(x)
    if x < 0:
        raise ValueError("negative under the root")
    num = _isqrt_exact(x.numerator)
    den = _isqrt_exact(x.denominator)
    if num is None or den is None:
        raise ValueError(f"sqrt({x}) is irrational — refusing to float it")
    return F(num, den)


def _isqrt_exact(m):
    r = 0
    while (r + 1) * (r + 1) <= m:
        r += 1
    return r if r * r == m else None


# ---------------------------------------------------------------------------
# 2.  eps_dem, SOLVED from each chain's own bound: the largest eps_spec whose
#     Phi bound still lands at or under eps_leak.
# ---------------------------------------------------------------------------

def dem_I(eps_leak):
    """Phi = sqrt(2 e) <= L  <=>  e <= L^2/2."""
    L = _leak(eps_leak)
    return Spec(L * L / 2)


def dem_II(eps_leak, c3gap):
    """Phi = g*e <= L  <=>  e <= L/g."""
    L = _leak(eps_leak)
    return Spec(L / F(c3gap))


def dem_III(eps_leak, c3):
    """Phi = sqrt(2 C e) <= L  <=>  e <= L^2/(2C)."""
    L = _leak(eps_leak)
    return Spec(L * L / (2 * F(c3)))


def dem_IV(eps_leak, c):
    """Phi = 1 - c(1-e) <= L  <=>  e <= 1 - (1-L)/c."""
    L = _leak(eps_leak)
    return Spec(1 - (1 - L) / F(c))


# ---------------------------------------------------------------------------
# 3.  THE JOIN NOTHING IN THE CORPUS PERFORMS.
#     mg-6bc2 §3.1's exact identity, in the direction the demand needs.
#
#         eps_spec = 3 * d * qbar * n/(n+1)
#
#     `d`    = m / C(n,2), the incomparability density
#     `qbar` = mean flip probability over incomparable pairs
#
#     At EVERY boundary maximiser at EVERY n <= 7, qbar = 1/3 EXACTLY (mg-6bc2
#     §3.1, finite population, marked as such).  With qbar pinned there the
#     demand collapses to a bound on d alone.
# ---------------------------------------------------------------------------

def dq_from_spec(eps_spec, n=None):
    """The `d*qbar` a given eps_spec permits.  n=None takes the n -> infinity limit."""
    e = _spec(eps_spec)
    if n is None:
        return e / 3
    return e * F(n + 1, n) / 3


def density_from_spec(eps_spec, qbar=F(1, 3), n=None):
    """The incomparability density `d` a given eps_spec permits, at a fixed qbar."""
    return dq_from_spec(eps_spec, n) / F(qbar)


def spec_from_dq(dq, n=None):
    """The inverse direction, used as a plug-back check on the two above."""
    dq = F(dq)
    if n is None:
        return Spec(3 * dq)
    return Spec(3 * dq * F(n, n + 1))


# ---------------------------------------------------------------------------
# 4.  The wall: what the supply gives divided by what the demand needs.
#     eps_sup = 1 — PROVEN, and an EQUALITY for the information pair bias
#     consumes; APPROACHED, NOT ATTAINED in the frozen class (mg-6bc2 Claim
#     3.1, scope mg-832f Correction 2).  Cited, not re-derived.
# ---------------------------------------------------------------------------

EPS_SUP = F(1)


def wall(eps_dem):
    """eps_sup / eps_dem."""
    return EPS_SUP / _spec(eps_dem)


# ---------------------------------------------------------------------------
# 5.  Cited constants, each with its status ON the constant.
# ---------------------------------------------------------------------------

EPS_LEAK = Leak(F(1, 5))
EPS_LEAK_STATUS = ("EMPIRICAL — mg-e35c F5 on mg-3ce3's envelope; an FP non-refutation over "
                   "6681 posets, IS L4's threshold eps_0, and errs OPTIMISTIC in the "
                   "required scope by >= 40% (mg-9461 §4.3)")

# mg-00b3 §0.4 — the staircase S_n, `i < j` iff `j >= i+2`.  Exact rationals for
# min_k Q_k and gap; C3^gap and c as that document prints them.  IN-REGIME means
# gap <= 1/50, which is the chain-(III) budget itself.
STAIRCASE = [
    # n,  min_k Q_k,      gap (decimal),  in regime, C3^gap,   c
    (7,   F(1, 6),        0.0541957607,   False,     3.0753,   0.8810844),
    (12,  F(64, 699),     0.0187781484,   True,      4.8758,   0.9258259),
    (16,  F(441, 6388),   0.0106071789,   True,      6.5084,   0.9409451),
    (20,  F(605, 10946),  0.0068008493,   True,      8.1271,   0.9511976),
    (25,  F(300, 6773),   0.0043572625,   True,      10.1654,  0.9598890),
    (28,  F(142129, 3599603), 0.0034748779, True,    11.3629,  0.9638647),
]

# mg-81ff §5 — its own in-regime family, N(k) = K_{a,a} minus one relation.
NFAMILY = [
    (10, 1.0650, None),
    (16, 1.0275, 0.9999),
]

# mg-94c3 §3 — C3^gap over n = 3..6, on posets exhibiting L2's FIRST disjunct.
# OUT OF REGIME: 0 of 4376 primitive posets at n <= 6 have gap <= 1/50.
C3GAP_MEASURED = [(3, 1.500), (4, 1.473), (5, 1.990), (6, 2.386)]
