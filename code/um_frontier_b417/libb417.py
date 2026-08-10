"""libb417 -- mg-b417's instrument for THE u_M FRONTIER and the fate of the DISJUNCTION.

THE QUESTION, RESTATED SO THE INSTRUMENT CANNOT DRIFT OFF IT.

  (F)  holds at P  <=>  M(P)^2 <= 2 gamma(P)                       u_F := M/sqrt(2 gamma)
  (M#) holds at P  <=>  sweep(mu_pref, Delta) <= 2 gamma           u_M := mu_pref/t*
                        sweep(mu,D) = mu(2D-mu) for mu <= D, D^2 beyond
                        t*(P)       = Delta - sqrt(Delta^2 - 2 gamma)   (+inf if D^2 <= 2gamma)

  THE DISJUNCTION at n:   every primitive P on [n] satisfies (F) or (M#)
                     <=>  W(n) := max_P min(u_F, u_M)  <=  1.

  A poset REFUTES the disjunction iff u_F > 1 AND u_M > 1 -- BOTH.  This is the single
  most important line in this file.  `u_M > 1` on its own is NOT an event: 4 primitive
  posets at n = 7 already have it (mg-c50b s2, column "(M#)f"), and (F) holds at every
  one of them.  A hill climb pointed at bare u_M reports a spectacular non-result.

THE IDENTITY THIS TREE IS ORGANISED AROUND.  Write rho = mu_pref/gamma and
v_L = rho*Delta = mu_pref*Delta/gamma -- (L*)'s own scalar, the one whose crossing of 1
refuted (L*).  Then, whenever Delta^2 > 2 gamma,

        u_M  =  v_L * D,       D := (1 + sqrt(1 - 2 gamma/Delta^2)) / 2   <  1.

  PROOF.  t* = Delta(1 - s) with s = sqrt(1 - 2gamma/Delta^2), so
  mu/t* = mu(1+s) / (Delta(1-s^2)) = mu(1+s)Delta / (2 gamma) = v_L (1+s)/2.  []

  Equivalently, since (M#) is (L*)'s conclusion relaxed by exactly mu_pref^2/2
  (mu*Delta <= gamma  vs  mu*Delta - mu^2/2 <= gamma):

        (M#) FAILS  <=>  v_L  >  1 + rho*mu_pref/2 .

  So THE (M#) FRONTIER IS THE (L*) FRONTIER DISCOUNTED BY D, and the discount is
  governed by gamma/Delta^2 alone.  Two consequences that steer the search:

    (i) a poset needs to violate (L*) by MORE than mu_pref/2 (times rho), so the
        winning direction is SMALL mu_pref -- a thin cut -- and not merely large v_L;
   (ii) on the (F)-failing set 2 gamma < M^2 <= Delta^2, hence D > 1/2 always, and
        D -> 1 exactly as gamma/Delta^2 -> 0.

THE TWO-STAGE DISCIPLINE, AND WHICH DIRECTION EACH STAGE IS ALLOWED TO ERR IN.

  STAGE 1 (SCREEN, floats, fast).  mu is taken from mg-789d's `mu_ub_float`, an UPPER
  bound on mu_pref exhibited by a nonincreasing f.  Therefore the screen's u_M is an
  UPPER bound on the true u_M and its min(u_F,u_M) is an UPPER bound on the true one.
  A screen that can only OVER-state the hunted quantity cannot lose a counterexample.
  It also cannot be quoted: every figure it produces is inflated by construction, and
  quoting one as a result is mg-5cba's R6 committed a second time.

  STAGE 2 (FLOAT VERDICT).  mu is taken from mg-5cba's `mu_pref_float`, the EXHAUSTIVE
  minimum over all 2^(n-1) faces of the monotone cone with the minimiser checked to lie
  in the cone.  This is the true mu_pref up to float error, and it is what the reported
  float figures are.

  STAGE 3 (EXACT).  Nothing is CLAIMED without integers.  And the direction flips with
  the claim:

      to certify (M#) HOLDS  :  mu from ABOVE, gamma from BELOW
      to certify (M#) FAILS  :  mu from BELOW, gamma from ABOVE     <-- the hard one

  The hard one needs mu_pref bounded BELOW, which no exhibited vector can do; it needs
  exact COPOSITIVITY of b*n*QI - 2*LE*a*NI.  That is the trap mg-51f4 named and the
  reason `certify_fails` below never touches a float on its verdict path.

WHAT IS IMPORTED AND WHY.

  `lib5cba`  -- P5, mu_pref_float, gamma_float, and the exact devices.  This is the
                AUDITED exact instrument of this thread and it is used UNMODIFIED.
                Re-deriving a certifier to be "independent" of the audited one would
                trade an audited routine for an unaudited one on the verdict path.
  `lib789d`  -- P789 and mu_ub_float, for the screen only.  Never on a verdict path.

  Screen and verdict therefore run on two different implementations of the same
  objects, which is a control and not an accident: b0 arm S3 checks they agree.
"""

import math
import os
import sys
from fractions import Fraction

_HERE = os.path.dirname(os.path.abspath(__file__))
_CODE = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_CODE, "audit_5cba"))
sys.path.insert(0, os.path.join(_CODE, "lstar_789d"))

from lib5cba import P5, mu_pref_float, gamma_float, height          # noqa: E402
from lib789d import P789                                             # noqa: E402


# ---------------------------------------------------------------------------
# 1.  The five scalars, and the frontier objective
# ---------------------------------------------------------------------------


def tstar(delta, gamma):
    """t* = Delta - sqrt(Delta^2 - 2 gamma).  None when Delta^2 <= 2 gamma, i.e. when
    (M#) CANNOT fail however large mu_pref is."""
    disc = delta * delta - 2.0 * gamma
    if disc <= 0.0:
        return None
    return delta - math.sqrt(disc)


def scalars(delta, M, gamma, mu):
    """Every published reading of one poset, from the four primitives.

    u_M and c# are TWO NUMBERS SHARING ONE PREDICATE (mg-0d1b): they are not equal and
    they cross 1 together on the primitive population.  Both are returned at every
    witness so that no caller has to pick one and name the other.
    """
    ts = tstar(delta, gamma)
    u_F = M / math.sqrt(2.0 * gamma) if gamma > 0 else float("inf")
    if ts is None:
        u_M = 0.0                      # (M#) cannot fail here
    elif ts <= 0:
        u_M = float("inf")
    else:
        u_M = mu / ts
    sweep = mu * (2.0 * delta - mu) if mu <= delta else delta * delta
    c_sharp = sweep / (2.0 * gamma) if gamma > 0 else float("inf")
    f_star = M * M / (2.0 * gamma) if gamma > 0 else float("inf")
    rho = mu / gamma if gamma > 0 else float("inf")
    v_L = rho * delta
    disc = 1.0 - 2.0 * gamma / (delta * delta) if delta > 0 else -1.0
    Dfac = (1.0 + math.sqrt(disc)) / 2.0 if disc >= 0 else None
    return dict(Delta=delta, M=M, gamma=gamma, mu=mu, tstar=ts,
                u_F=u_F, u_M=u_M, c_sharp=c_sharp, f_star=f_star,
                rho=rho, v_L=v_L, D=Dfac, J=min(u_F, u_M))


def score_screen(dn, n):
    """STAGE 1.  Fast, and OVER-states u_M by construction.  Returns None on a poset
    that is not primitive or has no usable gamma."""
    q = P789(dn, n)
    if not q.primitive():
        return None
    g = q.gamma_float()
    if g <= 1e-13:
        return None
    mu = q.mu_ub_float()[0]
    if mu == float("inf"):
        return None
    return scalars(float(q.Delta()), float(q.M()), g, mu)


def score_float(dn, n):
    """STAGE 2.  Exhaustive over all 2^(n-1) faces -- the true mu_pref up to float
    error.  Slow: O(2^n) faces, ~1 s at n = 12."""
    p = P5(dn, n)
    if not p.primitive():
        return None
    g = gamma_float(p)
    if g <= 1e-13:
        return None
    mu, _ = mu_pref_float(p)
    if mu is None:
        return None
    return scalars(float(p.Delta()), float(p.M()), g, mu)


# ---------------------------------------------------------------------------
# 2.  Exact certification -- the only thing allowed to produce a CLAIM
# ---------------------------------------------------------------------------


def _gamma_upper(p, steps=34):
    """A rational g_ub with gamma < g_ub, CERTIFIED by R(g_ub) not being PSD.

    The bracket's top is re-asserted with a standalone `gamma_ge` call rather than
    inherited from the loop (E6): a bracket whose endpoint was never tested is a float
    wearing a Fraction's clothes.
    """
    lo, hi = Fraction(0), Fraction(2)
    for _ in range(steps):
        mid = (lo + hi) / 2
        if p.gamma_ge(mid):
            lo = mid
        else:
            hi = mid
    ok = (p.gamma_ge(hi) is False)
    return hi, lo, ok


def _mu_lower(p, mu_hint, steps=24):
    """A rational m_lo with mu_pref >= m_lo, CERTIFIED by R(m_lo) being COPOSITIVE.

    The seed is a float and is therefore NOT trusted: the returned m_lo is re-asserted
    with a standalone `mu_ge` call (E6).  If that call is False the certificate is
    REFUSED, not repaired -- a refusal here is a real outcome and is reported as one.
    """
    lo = Fraction(int(mu_hint * 10 ** 7) - 20, 10 ** 7)
    if lo < 0:
        lo = Fraction(0)
    hi = Fraction(int(mu_hint * 10 ** 7) + 200, 10 ** 7)
    lo2, hi2 = p.mu_bracket(steps, lo=lo, hi=hi)
    ok = (p.mu_ge(lo2) is True)
    return lo2, hi2, ok


def certify(dn, n, mu_hint=None, gamma_steps=34, mu_steps=24):
    """EXACT.  Decide, on integers, whether P refutes the DISJUNCTION.

    Returns a dict.  Every verdict field is a Python bool obtained from exact
    Fraction arithmetic over certificates produced by `psd_int` / `copositive_int`.
    No float reaches a verdict; the floats present are printing shadows.

    THE CERTIFICATE, in the FAILS direction:

        gamma  <  g_ub                    R(g_ub)  NOT PSD
        mu     >= m_lo                    R(m_lo)  COPOSITIVE
        (F) fails      <=>  gamma < M^2/2                       [R(M^2/2) NOT PSD]
        (M#) fails     <==  sweep(m_lo, Delta) > 2 g_ub
                            (sweep is increasing on [0,Delta] and mu >= m_lo,
                             gamma <= g_ub, so sweep(mu) >= sweep(m_lo) > 2 g_ub >= 2 gamma)

    Both implications are one-directional and both point the safe way: a poset this
    routine calls a counterexample IS one, and a poset it declines may still be one.
    """
    p = P5(dn, n)
    out = dict(dn=dn, n=n, primitive=p.primitive(), LE=p.LE)
    out["natural"] = all(dn[i] >> i == 0 for i in range(n))
    tr = True
    for i in range(n):
        m = dn[i]
        while m:
            j = (m & -m).bit_length() - 1
            m &= m - 1
            if dn[j] & ~dn[i]:
                tr = False
    out["transitive"] = tr
    if not p.primitive():
        out["verdict"] = "NOT PRIMITIVE"
        return out

    D = p.Delta()
    M = p.M()
    out["Delta"], out["M"] = D, M

    g_ub, g_lo, g_ok = _gamma_upper(p, gamma_steps)
    out["g_ub"], out["g_lo"], out["gamma_cert_ok"] = g_ub, g_lo, g_ok

    if mu_hint is None:
        mu_hint, _ = mu_pref_float(p)
    m_lo, m_hi, m_ok = _mu_lower(p, mu_hint, mu_steps)
    out["m_lo"], out["m_hi"], out["mu_cert_ok"] = m_lo, m_hi, m_ok

    # -- (F) --
    out["F_fails"] = (p.gamma_ge(M * M / 2) is False)

    # -- (M#) --
    out["Delta2_gt_2g"] = (D * D > 2 * g_ub)
    sweep_lo = m_lo * (2 * D - m_lo) if m_lo <= D else D * D
    out["sweep_lo"] = sweep_lo
    out["M_sharp_fails"] = bool(g_ok and m_ok and out["Delta2_gt_2g"]
                                and sweep_lo > 2 * g_ub)
    out["margin"] = sweep_lo - 2 * g_ub

    # -- the disjunction --
    out["refutes_disjunction"] = bool(out["F_fails"] and out["M_sharp_fails"])

    # -- certified LOWER bounds on the published readings --
    out["c_sharp_lo"] = sweep_lo / (2 * g_ub)
    out["f_star_lo"] = M * M / (2 * g_ub)
    fD, fg, fm = float(D), float(g_ub), float(m_lo)
    ts_ub = fD - math.sqrt(fD * fD - 2 * fg) if fD * fD > 2 * fg else None
    out["u_M_lo"] = fm / ts_ub if ts_ub and ts_ub > 0 else None
    out["u_F_lo"] = float(M) / math.sqrt(2 * fg)
    out["v_L_lo"] = float(m_lo * D) / fg
    # -- (M#) HOLDS certificate, the OTHER direction, for witnesses below 1 --
    sweep_hi = m_hi * (2 * D - m_hi) if m_hi <= D else D * D
    out["M_sharp_holds"] = bool(sweep_hi <= 2 * g_lo)
    return out


# ---------------------------------------------------------------------------
# 3.  Population and moves
# ---------------------------------------------------------------------------


def close_natural(rel, n):
    """Transitive closure of `rel` (bitmask of strict predecessors), refused unless the
    result is still naturally labelled.  Returns None on refusal."""
    dn = list(rel)
    for _ in range(n):
        changed = False
        for i in range(n):
            m, acc = dn[i], dn[i]
            while m:
                j = (m & -m).bit_length() - 1
                m &= m - 1
                acc |= dn[j]
            if acc != dn[i]:
                dn[i] = acc
                changed = True
        if not changed:
            break
    for i in range(n):
        if dn[i] >> i:
            return None
    return tuple(dn)


def neighbours(dn, n):
    """The move set.  THREE kinds, and the third is the one the family studies never
    varied (mg-789d's own point): gamma, Delta, M and mu_pref ALL move when the natural
    LABELLING moves, because A_P couples element index to position index.

      (a) delete one relation        (b) add one relation, transitively closed
      (c) transpose adjacent labels k, k+1 when the two elements are incomparable
    """
    out = []
    for i in range(n):
        m = dn[i]
        while m:
            j = (m & -m).bit_length() - 1
            m &= m - 1
            rel = list(dn)
            rel[i] = dn[i] & ~(1 << j)
            d2 = close_natural(rel, n)
            if d2 is not None and d2 != dn:
                out.append(d2)
    for i in range(n):
        for j in range(i):
            if dn[i] >> j & 1:
                continue
            rel = list(dn)
            rel[i] = dn[i] | (1 << j)
            d2 = close_natural(rel, n)
            if d2 is not None and d2 != dn:
                out.append(d2)
    for k in range(n - 1):
        if dn[k + 1] >> k & 1:
            continue
        perm = list(range(n))
        perm[k], perm[k + 1] = perm[k + 1], perm[k]
        inv = [0] * n
        for a, b in enumerate(perm):
            inv[b] = a
        rel = [0] * n
        for i in range(n):
            m, mask = dn[i], 0
            while m:
                j = (m & -m).bit_length() - 1
                m &= m - 1
                mask |= 1 << inv[j]
            rel[inv[i]] = mask
        if all(rel[i] >> i == 0 for i in range(n)):
            out.append(tuple(rel))
    # DEFECT OF MY OWN, CAUGHT BY b0 ARM S7 AND KEPT IN THE FILE.  The `d2 != dn`
    # guard was applied to the add and delete moves and NOT to the transposition: when
    # the two swapped labels are order-isomorphic in P, the relabelling is the identity
    # and `neighbours` returned the CURRENT POINT as a neighbour of itself.  2 of 209
    # neighbours over the five gap witnesses.  The climb was unaffected -- it accepts a
    # move only on `> cur + eps`, so a self-neighbour can never be selected -- but a
    # move set that contains the identity is wrong whether or not anything downstream
    # notices, and "nothing noticed" is the reason it survived to be found by a control
    # rather than by the search.
    seen, uniq = set(), []
    for d in out:
        if d != dn and d not in seen:
            seen.add(d)
            uniq.append(d)
    return uniq


def random_poset(rnd, n, p=0.35):
    """A random naturally-labelled primitive poset with usable gamma."""
    while True:
        dn = []
        for i in range(n):
            mask = 0
            for j in range(i):
                if rnd.random() < p:
                    mask |= 1 << j
            m = mask
            while m:
                j = (m & -m).bit_length() - 1
                m &= m - 1
                mask |= dn[j]
            dn.append(mask)
        dn = tuple(dn)
        q = P789(dn, n)
        if q.primitive() and q.gamma_float() > 1e-12:
            return dn


def lifts(dn, n):
    """Every one-element extension of `dn` to n+1 elements: the new top element takes
    each order ideal of `dn` as its strict lower set.  Capped where the ideal count
    explodes; the cap is REPORTED by the caller, never silent."""
    from lib5cba import order_ideals
    ide = order_ideals(dn, n)
    return [(dn + (D,), n + 1) for D in ide]


def climb(dn, n, max_steps=60, eps=1e-12, objective=None):
    """Best-improvement hill climb on `objective` (default: min(u_F,u_M), the frontier).

    Returns (dn, score_dict, steps, evaluations).  The score is a SCREEN score and is
    therefore an UPPER bound on the truth -- the caller must re-score champions with
    `score_float` and certify them with `certify` before printing anything as a result.
    """
    if objective is None:
        objective = lambda s: s["J"]                                   # noqa: E731
    s = score_screen(dn, n)
    if s is None:
        return dn, None, 0, 0
    cur = objective(s)
    evals = 1
    steps = 0
    for _ in range(max_steps):
        best, bestdn, bests = cur, None, None
        for d2 in neighbours(dn, n):
            s2 = score_screen(d2, n)
            evals += 1
            if s2 is None:
                continue
            v = objective(s2)
            if v > best + eps:
                best, bestdn, bests = v, d2, s2
        if bestdn is None:
            break
        dn, cur, s = bestdn, best, bests
        steps += 1
    return dn, s, steps, evals


# ---------------------------------------------------------------------------
# 4.  The five certified (L*) counterexamples -- the (L*)-gap population
# ---------------------------------------------------------------------------

LSTAR_GAP = [
    ("C1", (0, 1, 0, 4, 0, 0, 32, 96, 239), 9),
    ("C2", (0, 0, 0, 0, 0, 16, 48, 16, 247), 9),
    ("C3", (0, 1, 3, 0, 9, 0, 32, 96, 255, 239), 10),
    ("C4", (0, 1, 3, 7, 0, 1, 1, 113, 1, 257, 257), 11),
    ("C5", (0, 0, 3, 7, 15, 7, 63, 2, 135, 391, 7, 1159), 12),
]

# mg-5cba's n = 8 search argmax.  (L*) HOLDS there (certified 0.968818).  Present as a
# NEGATIVE control and NOT as a seed for the counterexample hunt.
N8_ARGMAX = ((0, 0, 2, 0, 8, 24, 63, 62), 8)


# ---------------------------------------------------------------------------
# 5.  A TABLE THAT CANNOT HAVE A BLANK CELL
# ---------------------------------------------------------------------------
#
# WHY THIS EXISTS, AND IT IS NOT STYLE.  mg-5cba's audit table has a `u_M` column with
# four values and one dash.  The dash meant NOT COMPUTED.  It read as NOT APPLICABLE.
# STATE.md then published "(M#) HOLDS at 4 of 4" -- true of the four it names, and it
# names four because the fifth cell was blank.  A BLANK BECAME A BOUND, and it stood on
# main until this ticket multiplied the two halves that were printed either side of it.
#
# So this module refuses to render a blank.  A value that was not computed is printed as
# the word NOT-COMPUTED, in the column, in the row, where a reader scanning for a
# missing figure will hit it.  A value that is genuinely inapplicable must say
# N/A-<reason> and the reason is required.  There is no third option and no empty
# string: `emit_table` raises on one.


class BlankCell(Exception):
    """Raised when a table would render a cell that is neither a value, an explicit
    NOT-COMPUTED, nor an N/A carrying its reason."""


def cell(value, fmt="%.6f", na_reason=None):
    """Render one cell.  None becomes a LOUD marker, never a dash and never a space."""
    if value is None:
        if na_reason:
            return "N/A-" + str(na_reason)
        return "NOT-COMPUTED"
    if isinstance(value, str):
        if not value.strip():
            raise BlankCell("a blank string reached cell()")
        return value
    return fmt % value


def emit_table(headers, rows, widths=None):
    """Render a table, REFUSING any cell that is blank.

    `rows` are lists of already-rendered strings (use `cell`).  A cell that is empty,
    whitespace, '-', '--' or '---' is a refusal: those are exactly the renderings that
    let NOT COMPUTED masquerade as NOT APPLICABLE.
    """
    BANNED = {"", "-", "--", "---", "—", "–"}
    for r, row in enumerate(rows):
        if len(row) != len(headers):
            raise BlankCell("row %d has %d cells for %d headers" % (r, len(row), len(headers)))
        for c, v in enumerate(row):
            if str(v).strip() in BANNED:
                raise BlankCell("row %d column %r would render as %r -- use "
                                "cell(None) so it reads NOT-COMPUTED"
                                % (r, headers[c], v))
    if widths is None:
        widths = [max([len(str(h))] + [len(str(row[i])) for row in rows])
                  for i, h in enumerate(headers)]
    out = ["  " + " | ".join(str(h).ljust(widths[i]) for i, h in enumerate(headers))]
    out.append("  " + "-+-".join("-" * w for w in widths))
    for row in rows:
        out.append("  " + " | ".join(str(v).ljust(widths[i]) for i, v in enumerate(row)))
    return "\n".join(out)
