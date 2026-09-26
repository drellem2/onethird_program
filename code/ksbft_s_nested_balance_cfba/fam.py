"""fam.py (mg-cfba): shared helpers — run nb.c on a list of posets; poset constructions reused from
mg-ce69 (Q_m: grow/dual/glue) and mg-7bfc (F_N, attach_low, attach_both, hub, prime)."""
import subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../ksbft_q2_both_ends_ce69"))
from lib import parse, fmt, closure, upmasks, rng, connected  # noqa: E402
from longtail import grow, dual, glue  # noqa: E402
import importlib.util  # noqa: E402
_spec = importlib.util.spec_from_file_location("lib7", os.path.join(HERE, "../ksbft_r_window_padding_7bfc/lib.py"))
lib7 = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(lib7)


def lt_to_dn(P):
    n, lt = P
    return [sum(1 << i for i in range(n) if lt[i][j]) for j in range(n)]


def dn_to_lt(dn):
    n = len(dn)
    return n, [[bool(dn[j] >> i & 1) for j in range(n)] for i in range(n)]


def is_prime(dn):
    return lib7.prime(*dn_to_lt(dn))


def run(dns, verbose=False):
    if not dns:
        return "" if verbose else []
    args = [os.path.join(HERE, "nb")] + (["-v"] if verbose else [])
    out = subprocess.run(args, input="\n".join(fmt(d) for d in dns) + "\n", capture_output=True, text=True, check=True).stdout
    if verbose:
        return out
    res = []
    for line in out.strip().split("\n"):
        t = line.split()
        res.append(dict(n=int(t[0]), e=float(t[1]), delta=float(t[2]), deltaN=float(t[3]), nbal=int(t[4]),
                        nbalN=int(t[5]), nnon=int(t[6]), flag=t[7], soft=float(t[8]), deltaP=float(t[9]), pflag=t[10]))
    return res


def is_chain_mask(dn, S):
    v = [i for i in range(len(dn)) if S >> i & 1]
    return all(dn[a] >> b & 1 or dn[b] >> a & 1 for i, a in enumerate(v) for b in v[i + 1:])


def chain_pairs(dn):
    """number of STRUCTURAL good pairs: incomparable (a,b) with down(a) <= down(b) and up(b)-up(a) a chain
    (possibly empty), or the dual (up(a) <= up(b) and down(b)-down(a) a chain).  Zaguia's Thm 2 (with the Swap
    Ladder's 2/3 form) forces a nested balanced pair whenever such a pair has P[a<b] <= 2/3 (resp. dual)."""
    n = len(dn); up = upmasks(dn); c = 0
    for a in range(n):
        for b in range(n):
            if a == b or dn[a] >> b & 1 or dn[b] >> a & 1: continue
            if dn[a] & ~dn[b] == 0 and is_chain_mask(dn, up[b] & ~up[a]): c += 1
            if up[a] & ~up[b] == 0 and is_chain_mask(dn, dn[b] & ~dn[a]): c += 1
    return c


def pair_laws(dns):
    """exact-enough pair laws p[a][b] = P[a before b] (floats from nb -v, 6 decimals) per poset"""
    out = run(dns, verbose=True).split("\n")
    res, cur = [], {}
    for line in out:
        t = line.split()
        if not t: continue
        if t[0] == "pair":
            a, b, p = int(t[1]), int(t[2]), float(t[3][2:]); cur[(a, b)] = p; cur[(b, a)] = 1 - p
        else:
            res.append(cur); cur = {}
    return res


def firing_full_pairs(dn, p):
    """structural good pairs whose Swap Ladder (full chain) FIRES: primal (a,b) with down(a)<=down(b),
    up(b)-up(a) a chain and P[a<b] <= 2/3; or dual with up(a)<=up(b), down(b)-down(a) a chain, P[b<a] <= 2/3.
    Any such pair forces a nested balanced pair (Thm 1.4(c) with a full chain / Zaguia Thm 2)."""
    n = len(dn); up = upmasks(dn); c = 0
    for a in range(n):
        for b in range(n):
            if a == b or (a, b) not in p: continue
            if dn[a] & ~dn[b] == 0 and p[(a, b)] <= 2 / 3 + 1e-9 and is_chain_mask(dn, up[b] & ~up[a]): c += 1
            if up[a] & ~up[b] == 0 and p[(b, a)] <= 2 / 3 + 1e-9 and is_chain_mask(dn, dn[b] & ~dn[a]): c += 1
    return c
