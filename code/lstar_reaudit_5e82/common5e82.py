"""The one poset under audit, and the two published rationals, in one place.

Every arm builds the poset from `DN` through `lib5e82.Poset`, which enumerates all
10584 linear extensions.  Nothing here is read from another instrument's output.
"""
import os
import sys
from fractions import Fraction as Fr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib5e82 as L

# mg-5cba's C5 / mg-b417's n = 12 witness.
DN = (0, 0, 3, 7, 15, 7, 63, 2, 135, 391, 7, 1159)
N = 12

# The two rationals cb417 certified.  They are INPUTS to this audit -- quoted from the
# work item so that this audit checks the SAME claim -- and every property asserted of
# them is re-derived here.
G_UB = Fr(529992611, 8589934592)             # claim: gamma   <  G_UB
M_LO = Fr(550121491741, 8388608000000)       # claim: mu_pref >= M_LO

# The decimals mg-5cba PUBLISHED on main, for the provenance arm.
G_UB_PUBLISHED = Fr(61699262, 10 ** 9)       # "gamma in [0.061699260, 0.061699262]"
M_LO_PUBLISHED = Fr(65579592, 10 ** 9)       # "mu_pref >= 0.065579592"


def build():
    return L.Poset(DN, N)


def isqrt_frac(x, prec=10 ** 40):
    """Rational lower/upper bounds for sqrt(x), verified by squaring before return."""
    from math import isqrt

    r = isqrt(x.numerator * prec * prec // x.denominator)
    lo, hi = Fr(r, prec), Fr(r + 1, prec)
    assert lo * lo <= x <= hi * hi, "sqrt bracket failed"
    return lo, hi


def banner(t):
    print("=" * 78)
    print(t)
    print("=" * 78)
