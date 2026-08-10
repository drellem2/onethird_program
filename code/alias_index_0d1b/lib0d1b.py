"""lib0d1b — the bridge that lets one poset be handed to twelve trees at once.

THE WHOLE POINT OF THIS FILE is that it adds NO mathematics.  Every scalar reported by
`x3_values.py` is computed by the tree that owns it, through that tree's own entry point,
under that tree's own name.  This module only

  (1) fixes ONE canonical poset representation and converts it into each tree's
      constructor argument, and
  (2) records, per tree, which of its symbols is a scalar and how to call it.

If this file computed a quantity itself, an "agreement" it reported would be an agreement
with *me*, not between two trees — which is the exact laundering the ticket is about.

CANONICAL FORM.  `(dn, n)` where `dn[i]` is the bitmask of STRICT PREDECESSORS of `i`, in
a natural labelling (the identity permutation is a linear extension).  This is `lib789d`'s
and `lib5cba`'s native form; `rel` (the set of pairs `(i, j)`, `i < j`, meaning `i < j` in
the poset) is derived from it for the trees that want pairs.
"""

import importlib.util
import os
import sys
from fractions import Fraction as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # .../code


# --------------------------------------------------------------- module loading

_CACHE = {}


def load(rel_path, modname):
    """Import a corpus module by path, with its own directory on sys.path.

    Its directory goes on sys.path because several of these libraries are imported by
    their siblings under a bare name.  It is removed again immediately: leaving twelve
    directories on sys.path makes `import lib...` resolution order load-bearing, and a
    probe whose answer depends on import order is not a probe.
    """
    if modname in _CACHE:
        return _CACHE[modname]
    path = os.path.join(ROOT, rel_path)
    d = os.path.dirname(path)
    sys.path.insert(0, d)
    try:
        spec = importlib.util.spec_from_file_location(modname, path)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
    finally:
        sys.path.pop(0)
    _CACHE[modname] = m
    return m


# --------------------------------------------------------------- canonical posets

def dn_to_rel(dn, n):
    """(dn, n) -> {(i, j) : i < j in P}, transitively closed, i < j as integers."""
    return {(i, j) for j in range(n) for i in range(n) if (dn[j] >> i) & 1}


def transitive_ok(dn, n):
    for i in range(n):
        if dn[i] >> i:
            return False
        m = dn[i]
        while m:
            j = (m & -m).bit_length() - 1
            m &= m - 1
            if dn[j] & ~dn[i]:
                return False
    return True


def _downsets(dn, n):
    out = []
    for D in range(1 << n):
        ok = True
        m = D
        while m:
            i = (m & -m).bit_length() - 1
            m &= m - 1
            if dn[i] & ~D:
                ok = False
                break
        if ok:
            out.append(D)
    return out


def gen_dn(n):
    """Every naturally-labelled poset on {0..n-1}, as `dn` tuples."""
    if n == 0:
        yield ()
        return
    for dn in gen_dn(n - 1):
        for D in _downsets(dn, n - 1):
            yield dn + (D,)


def population(spec):
    """spec = [(n, stride), ...] -> ordered list of (n, dn).  Deterministic, no RNG.

    `stride` is stated rather than hidden: a strided population is a SAMPLE and the
    transcript says so.  The order is the generation order and never changes, so a
    fingerprint vector is comparable between runs.
    """
    out = []
    for n, stride in spec:
        ps = [dn for dn in gen_dn(n) if transitive_ok(dn, n)]
        out.extend((n, dn) for dn in ps[::stride])
    return out


# --------------------------------------------------------------- adapters
#
# Each adapter takes (dn, n) and returns {local_name: float}.  `local_name` is the name
# THE TREE USES, because the names are the subject of this ticket and renaming them here
# would destroy the evidence.  A scalar that a tree cannot produce for a given poset
# returns None and is reported as absent rather than as zero.

def _f(x):
    return None if x is None else float(x)


def ad_28ff(dn, n):
    L = load("l2_conditionality_28ff/lib28ff.py", "z28ff")
    P = L.Poset(n, dn_to_rel(dn, n))
    lo, hi = L.gap_exact_bounds(P, iters=50)
    Q, N = L.pencil(P)
    mu, _ = L.cone_min(Q, N)
    return {
        "delta_max": _f(P.delta_max()),
        "phi_star_prefix": _f(P.phi_star_prefix()[0]),
        "phi_star": _f(P.phi_star()[0]),
        "E_footrule": _f(P.E_footrule()),
        "E_sq_displacement": _f(P.E_sq_displacement()),
        "gap_exact_bounds": _f((lo + hi) / 2),
        "cone_min": _f(mu),
        "leak(A_1)": _f(P.leak(frozenset([0]))),
    }


def ad_29fe(dn, n):
    L = load("l2_audit_29fe/lib29fe.py", "z29fe")
    P = L.Poset(n, dn_to_rel(dn, n))
    glo, ghi = L.bracket_gap(P, iters=40)
    mlo, mhi = L.bracket_mu_pref(P, iters=40)
    return {
        "Delta": _f(P.Delta),
        "Phi_star_pref": _f(P.Phi_star_pref()),
        "Phi_star_all": _f(P.Phi_star_all()),
        "EDF": _f(P.EDF),
        "bracket_gap": _f((glo + ghi) / 2),
        "bracket_mu_pref": _f((mlo + mhi) / 2),
        "leak[1]": _f(P.leak[1]),
    }


def ad_789d(dn, n):
    L = load("lstar_789d/lib789d.py", "z789d")
    P = L.P789(dn, n)
    g = P.gamma_float()
    mu, _c = P.mu_ub_float()
    mu_faces = P.mu_faces()[0]
    return {
        "Delta": _f(P.Delta()),
        "M": _f(P.M()),
        "Phi_star": _f(P.Phi_star()),
        "gamma_float": _f(g),
        "mu_ub_float": _f(mu),
        "mu_faces": _f(mu_faces),
        "rho_float": None if not g else _f(P.rho_float()),
        "rho*Delta": None if not g else float(P.rho_float()) * float(P.Delta()),
        "LK[1]/LE": _f(F(P.LK[1], P.LE)),
    }


def ad_5cba(dn, n):
    L = load("audit_5cba/lib5cba.py", "z5cba")
    P = L.P5(dn, n)
    g = L.gamma_float(P)
    mu, _v = L.mu_pref_float(P)
    return {
        "Delta": _f(P.Delta()),
        "M": _f(P.M()),
        "gamma_float": _f(g),
        "mu_pref_float": _f(mu),
        "v_L": None if (g in (None, 0) or mu is None) else float(mu) * float(P.Delta()) / float(g),
        "LK[1]/LE": _f(F(P.LK[1], P.LE)),
    }


def ad_3bb9(dn, n):
    L = load("l2_underclaim_audit_3bb9/lib3bb9.py", "z3bb9")
    P = L.P3bb9(n, dn_to_rel(dn, n))
    Q, N = L.pencil(P)
    g = L.gap_float(Q, N)
    mu, _ = L.mu_pref_float(Q, N)
    D = float(P.Delta)
    return {
        "Delta": D,
        "gap_float": _f(g),
        "mu_pref_float": _f(mu),
        "V10": None if (not g or mu is None) else float(mu) / float(g) * D,
        "V00": None if (not g or mu is None) else float(mu) / float(g),
        "leak[0]": _f(P.leak[0]),
    }


def ad_c50b(dn, n):
    L = load("anticorrelation_c50b/libc50b.py", "zc50b")
    P = L.Poset(dn, n)
    g = P.gamma_float()
    mu_ub, _c = P.mu_upper()
    D = float(P.Delta())
    ts = None
    disc = D * D - 2.0 * g
    if disc > 0:
        ts = D - disc ** 0.5
    return {
        "Delta": D,
        "M": _f(P.M()),
        "Phi_star": _f(P.Phi_star()),
        "gamma_float": _f(g),
        "mu_upper": _f(mu_ub),
        "mu_exhaustive": _f(L.mu_exhaustive(P)[0]),
        "f_star_float": None if not g else _f(P.f_star_float()),
        "c_true_float": None if not g else _f(P.c_true_float()),
        "c_sharp_float(mu_exh)": None if not g else _f(P.c_sharp_float(L.mu_exhaustive(P)[0])),
        "u_M": None if not g else (0.0 if ts is None else
                                   (float(mu_ub) / ts if ts > 0 else float("inf"))),
        "leak(1)": _f(P.leak(1)),
    }


def ad_51f4(dn, n):
    L = load("sweep_loss_51f4/lib51f4.py", "z51f4")
    P = L.Pos(n, dn_to_rel(dn, n))
    mu, _ = L.cone_min(P)
    return {
        "delta_max": _f(P.delta_max()),
        "phi_star_pref": _f(P.phi_star_pref()[0]),
        "phi_max_pref": _f(P.phi_max_pref()),
        "M_mean": _f(P.M_mean()),
        "E_footrule": _f(P.E_footrule()),
        "gap_float": _f(L.gap_float(P)),
        "cone_min": _f(mu),
        "leak_pref(1)": _f(P.leak_pref(1)),
    }


def ad_76b2(dn, n):
    L = load("c3_prefix_capture_76b2/lib76b2.py", "z76b2")
    P = L.Poset(n, dn_to_rel(dn, n))
    return {
        "phi_star": _f(P.phi_star()[0]),
        "phi_star_prefix": _f(P.phi_star_prefix()[0]),
        "leak(A_1)": _f(P.leak(frozenset([0]))),
        "rho_prefix(1)": _f(P.rho_prefix(1)),
    }


def ad_2de0(dn, n):
    L = load("direct_prefix_audit_2de0/lib2de0.py", "z2de0")
    P = L.Poset(n, dn_to_rel(dn, n), "p")
    return {
        "E_footrule": _f(P.E_footrule()),
        "E_inv": _f(P.E_inv()),
        "phi_star": _f(P.phi_star()),
        "E_leak(A_1)": _f(P.E_leak(frozenset([0]))),
        "delta_1_prefix(1)": _f(P.delta_1_prefix(1)),
    }


def ad_8311(dn, n):
    L = load("eleak_repair_8311/lib8311.py", "z8311")
    P = L.P8311(n, dn_to_rel(dn, n), "p")
    return {
        "phi_star(def)": _f(P.phi_star("def")),
        "phi_star(inv)": _f(P.phi_star("inv")),
        "phi_star(conv)": _f(P.phi_star("conv")),
        "E_leak(A_1,def)": _f(P.E_leak(frozenset([0]), "def")),
        "prefix_min": _f(P.prefix_min()),
    }


def ad_a94c3(dn, n):
    L = load("c3_audit_a94c3/libA94.py", "za94c3")
    rel = dn_to_rel(dn, n)
    exts = L.linear_extensions(n, rel)
    T = L.T_matrix(n, exts)
    return {
        "spectral_gap": _f(L.spectral_gap(n, T)[0]),
        "leak(A_1)": _f(L.leak(n, exts, frozenset([0]))),
        "delta1(A_1)": _f(L.delta1(n, exts, frozenset([0]))),
        "one_minus_rho(1)": _f(L.one_minus_rho(n, exts, 1)),
    }


def ad_81ff(dn, n):
    L = load("chain_iv_c_81ff/lib81ff.py", "z81ff")
    P = L.Poset(n, list(dn))
    lo, hi = P.lambda2_bracket(prec=F(1, 10 ** 9))
    return {
        "min_prefix_Q": _f(P.min_prefix_Q()[0]),
        "prefix_Q(1)": _f(P.prefix_Q(1)),
        "lambda2_bracket": _f((lo + hi) / 2),
    }


# tree name -> (adapter, the file the scalars actually live in)
ADAPTERS = [
    ("l2_conditionality_28ff", ad_28ff, "lib28ff.py"),
    ("l2_audit_29fe", ad_29fe, "lib29fe.py"),
    ("l2_underclaim_audit_3bb9", ad_3bb9, "lib3bb9.py"),
    ("lstar_789d", ad_789d, "lib789d.py"),
    ("audit_5cba", ad_5cba, "lib5cba.py"),
    ("anticorrelation_c50b", ad_c50b, "libc50b.py"),
    ("sweep_loss_51f4", ad_51f4, "lib51f4.py"),
    ("c3_prefix_capture_76b2", ad_76b2, "lib76b2.py"),
    ("direct_prefix_audit_2de0", ad_2de0, "lib2de0.py"),
    ("eleak_repair_8311", ad_8311, "lib8311.py"),
    ("c3_audit_a94c3", ad_a94c3, "libA94.py"),
    ("chain_iv_c_81ff", ad_81ff, "lib81ff.py"),
]


# --------------------------------------------------------------- fingerprints

TOL = 1e-9


def fingerprint(vals, tol=TOL):
    """A hashable key for a value vector.  None survives as None; inf survives as inf.

    Rounding is to `tol`, and the observed intra-group spread is printed separately by
    the caller, because a tolerance loose enough to merge two libraries' bracket widths is
    loose enough to merge two nearby scalars (E6).
    """
    key = []
    for v in vals:
        if v is None:
            key.append(None)
        elif v != v or v in (float("inf"), float("-inf")):
            key.append(repr(v))
        else:
            key.append(round(v / tol))
    return tuple(key)


def spread(a, b):
    """Max |a_i - b_i| over positions where both are finite; None if never comparable."""
    best = None
    for x, y in zip(a, b):
        if x is None or y is None:
            continue
        if x != x or y != y:
            continue
        if x in (float("inf"), float("-inf")) or y in (float("inf"), float("-inf")):
            continue
        d = abs(x - y)
        best = d if best is None else max(best, d)
    return best


def is_constant(vals):
    seen = {round(v / TOL) for v in vals if v is not None and v == v
            and v not in (float("inf"), float("-inf"))}
    return len(seen) <= 1


# --------------------------------------------------------------- populations
#
# The population is not a detail of this instrument, it IS the instrument (E9).  Two are
# declared and both are reported on, because the sweep's own first reading was WRONG for
# want of one: the ratio quantities (rho, rho*Delta, u_M, c#) are published over PRIMITIVE
# posets and are dominated by float noise off that set, where gamma -> 0.

POP_SPEC = [(3, 1), (4, 1), (5, 1)]


def primitive_here(dn, n):
    """leak(A_k) > 0 for every prefix cut — i.e. P is not an ordinal sum at any cut.

    This is lib0d1b's OWN predicate and it exists only to define the population.  Arm V4
    of `x3_values.py` checks it against every probed tree's own primitivity predicate; if
    that arm ever went red, the population itself would be in dispute and no other number
    in the transcript would be citable.
    """
    dnr = dn_to_rel(dn, n)
    from itertools import permutations
    les = [p for p in permutations(range(n))
           if all(p.index(i) < p.index(j) for (i, j) in dnr)]
    for k in range(1, n):
        lk = sum(1 for p in les for i in range(k) if p.index(i) >= k)
        if lk == 0:
            return False
    return True


# --------------------------------------------------------------- composed columns
#
# These are NOT native scalars.  Each is a ratio that the owning tree forms in a SCRIPT
# rather than in its library, and the citation is the line that forms it.  They are
# flagged COMPOSED in the transcript so that no reader mistakes an identification made
# here for one the tree publishes.

COMPOSED_CITE = {
    "l2_conditionality_28ff:V10": "docs/OneThird-L2-Conditionality-mg-28ff.md:279 (cell R5), identified as rho*Delta_P by l2_audit_29fe/s3_counterfactual.py:15",
    "l2_audit_29fe:V10": "code/l2_audit_29fe/s3_counterfactual.py:63  `V10 = rho*Delta`",
    "anticorrelation_c50b:rho*Delta": "code/anticorrelation_c50b/s2_theory.py:76,81  `rho = mu/g` then `rho*d`",
}


def composed(tree, native):
    """Ratio columns, formed exactly as the owning tree's own script forms them."""
    out = {}
    if tree == "l2_conditionality_28ff":
        g, mu, D = native["gap_exact_bounds"], native["cone_min"], native["delta_max"]
        out["V10"] = None if not g else mu / g * D
    elif tree == "l2_audit_29fe":
        g, mu, D = native["bracket_gap"], native["bracket_mu_pref"], native["Delta"]
        out["V10"] = None if not g else mu / g * D
    elif tree == "anticorrelation_c50b":
        g, mu, D = native["gamma_float"], native["mu_exhaustive"], native["Delta"]
        out["rho*Delta"] = None if not g else mu / g * D
        out["rho"] = None if not g else mu / g
    return out


# --------------------------------------------------------------- clustering

def cluster(cols, tol):
    """Single-linkage clustering of columns by MAX ABSOLUTE DIFFERENCE <= tol.

    DEFECT D1, RECORDED.  The first version of this instrument keyed columns by a rounded
    fingerprint (`round(v/tol)`) and grouped equal keys.  That splits a true alias whose
    two values straddle a rounding boundary — it split the gamma group into three, putting
    `l2_audit_29fe:bracket_gap` and `chain_iv_c_81ff:lambda2_bracket` (which agree to
    4.7e-10) in different groups while calling them different scalars.  A detector for
    "same number under two names" that answers by rounding is a detector for "same number
    AND same rounding", which is not the question.  `fingerprint()` is kept in this file
    because arm V5 of x3 demonstrates the defect rather than describing it.
    """
    keys = list(cols)
    parent = {k: k for k in keys}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            s = spread(cols[a], cols[b])
            if s is not None and s <= tol:
                ra, rb = find(a), find(b)
                if ra != rb:
                    parent[ra] = rb
    out = {}
    for k in keys:
        out.setdefault(find(k), []).append(k)
    return list(out.values())


def max_intra(cols, group):
    best = 0.0
    for i, a in enumerate(group):
        for b in group[i + 1:]:
            s = spread(cols[a], cols[b])
            if s is not None:
                best = max(best, s)
    return best
