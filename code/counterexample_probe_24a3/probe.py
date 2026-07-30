"""mg-24a3 -- how would a 1/3-2/3 counterexample behave under the semigroup action?

EVERYTHING HERE IS CONDITIONAL ON EXISTENCE.  No counterexample to the 1/3-2/3
conjecture is known and none exists at any size this probe reaches.  Every
statement about one has the form "IF a counterexample exists THEN ...".  Where a
real poset is measured, it is a real poset and is labelled as one; the
worst-balanced posets are a stated PROXY and never a counterexample.

Sections, in the order the ticket's ADDENDUM prioritises them:

  1  THE BRIDGE OBJECT (primary).  The majority tournament M(P), the
     distinguished linear extension L*, the identity E[inv(L,L*)] = sum of
     min(p,1-p), and the concentration ratio R(P) = 3 E[inv]/|Inc| that a
     counterexample must have below 1.  Measured on every poset to n = 7 and on
     named families beyond it.
  2  THE FACE-SIDE BALANCE CONSTANT.  The action has its own balance constant,
     computed from move counts with no reference to L(P).  It tracks delta
     closely -- this is the one place a signal appears -- and its error is
     measured against the margin it would have to resolve.
  3  THE QUOTIENT SIDE.  Is the acyclic-partition lattice organised around L*'s
     own chain more in the worst-balanced posets than in size-matched others?
     Effect size against a null model, with a saturation control.
  4  NECESSARY CONDITIONS in this language, proved and verified exhaustively.
  5  SPECTRAL SEPARATION (secondary; the brief's original (a)).  The invariant
     ladder, its resolution, and the null model.  Reported because a clean null
     is a deliverable, and demoted because the ADDENDUM calls it a fishing
     expedition.
  6  TRENDS in n, and 7 THE ISOPERIMETRIC QUESTION stated as a question.

Deterministic: seeded PRNG, everything sorted.  The committed probe_output.txt
must reproduce byte-identically.
"""

import random
import sys
from fractions import Fraction

import core
from core import (Poset, PartitionLattice, all_posets_bruteforce,
                  all_posets_by_extension, linear_extensions, restriction_counts,
                  pair_before_counts, delta_of, levels_of, multiplicities,
                  moves_of, act, support_index, order_ideals, part_key,
                  set_partitions)
import bridge
from bridge import (Bridge, quotient_concentration, lstar_interval_levels,
                    chain_sum_family, one_plus_two, fence)

SEED = 20260730
NMAX_FULL = 6      # full invariant suite (needs explicit move enumeration)
NMAX = 7           # reduced suite


def hr(title, ch="="):
    print()
    print(ch * 78)
    print(title)
    print(ch * 78)


def sub(title):
    print()
    print("-- " + title + " " + "-" * max(0, 74 - len(title)))


def fs(x):
    """Format a Fraction/None compactly."""
    if x is None:
        return "-"
    if isinstance(x, Fraction):
        return "%d/%d" % (x.numerator, x.denominator) if x.denominator != 1 else str(x.numerator)
    return str(x)


# --------------------------------------------------------------------------
# derived quantities
# --------------------------------------------------------------------------

def count_topological_sorts(k, succ):
    """#linear orderings of k nodes consistent with the DAG `succ` (bitmasks)."""
    f = [0] * (1 << k)
    f[0] = 1
    for S in range(1, 1 << k):
        tot = 0
        m = S
        while m:
            x = (m & -m).bit_length() - 1
            m &= m - 1
            if not (succ[x] & S):
                tot += f[S & ~(1 << x)]
        f[S] = tot
    return f[(1 << k) - 1]


def level_move_counts(P, lat, level_idx):
    """mc[X] = #P-compatible moves whose commitment level is X = #topological
    sorts of the quotient of P by X."""
    mc = {}
    for X in level_idx:
        blocks = lat.parts[X]
        k = len(blocks)
        of = [0] * P.n
        for idx, B in enumerate(blocks):
            m = B
            while m:
                x = (m & -m).bit_length() - 1
                m &= m - 1
                of[x] = idx
        succ = [0] * k
        for (a, b) in P.less:
            if of[a] != of[b]:
                succ[of[a]] |= 1 << of[b]
        mc[X] = count_topological_sorts(k, succ)
    return mc


def is_convex(P, B):
    """B is convex: i < j < k in P with i,k in B forces j in B."""
    m = B
    elems = []
    while m:
        x = (m & -m).bit_length() - 1
        m &= m - 1
        elems.append(x)
    for i in elems:
        for k in elems:
            if i == k:
                continue
            mid = P.up[i] & P.dn[k] & ~B
            if mid:
                return False
    return True


def spearman(xs, ys):
    """Spearman rank correlation with average ranks for ties.  Exact-ish via
    Fraction-free float at the last step only; the ranks themselves are exact."""
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1.0
            for t in range(i, j + 1):
                r[order[t]] = avg
            i = j + 1
        return r
    rx, ry = ranks(xs), ranks(ys)
    n = len(xs)
    mx = sum(rx) / n
    my = sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    dx = sum((a - mx) ** 2 for a in rx) ** 0.5
    dy = sum((b - my) ** 2 for b in ry) ** 0.5
    if dx == 0 or dy == 0:
        return None
    return num / (dx * dy)


def perm_pvalue(xs, ys, reps, rng):
    """Two-sided permutation p-value for |rho|, shuffling ys."""
    obs = spearman(xs, ys)
    if obs is None:
        return None, None
    ys = list(ys)
    hits = 0
    for _ in range(reps):
        rng.shuffle(ys)
        r = spearman(xs, ys)
        if r is not None and abs(r) >= abs(obs) - 1e-12:
            hits += 1
    return obs, (hits + 1) / (reps + 1)


# --------------------------------------------------------------------------
# per-poset record
# --------------------------------------------------------------------------

class Rec:
    __slots__ = ("P", "n", "cover", "e", "delta", "dmin", "per_pair", "primitive",
                 "is_chain", "nlev", "levprof", "multprof", "nlev_pos", "maxmult",
                 "lam", "lam2", "nmoves", "mc", "levels", "mult", "walkstats",
                 "delta_walk", "s_max", "signimb", "height", "width", "ncomp",
                 "inv4", "br", "qfrac", "qmass")

    def key_I0(self):
        return (self.e,)

    def key_I1(self):
        return (self.nlev, self.levprof)

    def key_I2(self):
        return (self.nlev, self.levprof, self.multprof)

    def key_I3(self):
        if self.lam is None:
            return None
        spec = tuple(sorted((self.lam[X], self.mult[X]) for X in self.levels
                            if self.mult[X] > 0))
        return (self.nlev, self.levprof, self.multprof, spec)

    def key_I4(self):
        return self.inv4


def build(P, lat, want_moves):
    r = Rec()
    r.P = P
    r.n = P.n
    r.cover = P.cover_string()
    e = restriction_counts(P)
    full = (1 << P.n) - 1
    r.e = e[full]
    before = pair_before_counts(P, e)
    r.delta, r.dmin, r.per_pair = delta_of(P, e, before)
    r.primitive = P.incomparability_connected()
    r.is_chain = P.is_chain()
    r.levels = levels_of(P, lat)
    r.mult = multiplicities(P, lat, r.levels, e)
    r.nlev = len(r.levels)
    lp = [0] * (P.n + 1)
    mp = [0] * (P.n + 1)
    for X in r.levels:
        k = lat.nblocks[X]
        lp[k] += 1
        mp[k] += r.mult[X]
    r.levprof = tuple(lp[1:])
    r.multprof = tuple(mp[1:])
    r.nlev_pos = sum(1 for X in r.levels if r.mult[X] > 0)
    r.maxmult = max(r.mult.values())
    # structural controls
    r.height = max((len(_longest_chain(P, x)) for x in range(P.n)), default=0)
    r.width = _width(P)
    r.ncomp = _ncomponents(P)
    les = linear_extensions(P)
    r.signimb = abs(sum(_perm_sign(w) for w in les))
    # the uniform-move weight
    r.mc = level_move_counts(P, lat, r.levels)
    r.nmoves = sum(r.mc.values())
    lam = {}
    for X in r.levels:
        tot = 0
        for Y, c in r.mc.items():
            if X in lat.refiners[Y]:
                tot += c
        lam[X] = Fraction(tot, r.nmoves)
    r.lam = lam
    cands = [lam[X] for X in r.levels if r.mult[X] > 0 and X != lat.bottom]
    r.lam2 = max(cands) if cands else Fraction(0)
    # s(x,y) = probability a uniform move does NOT separate the pair
    r.s_max = None
    if r.per_pair:
        smax = Fraction(0)
        for (x, y) in r.per_pair:
            tot = 0
            for X in r.levels:
                for B in lat.parts[X]:
                    if ((B >> x) & 1) and ((B >> y) & 1):
                        tot += r.mc[X]
                        break
            smax = max(smax, Fraction(tot, r.nmoves))
        r.s_max = smax
    # directional pair statistics (needs explicit moves): the face-side delta
    r.walkstats = None
    r.delta_walk = None
    if want_moves and r.per_pair:
        mvs = moves_of(P)
        assert len(mvs) == r.nmoves, (len(mvs), r.nmoves)
        ws = {}
        for (x, y) in r.per_pair:
            same = bx = by = 0
            for mv in mvs:
                ix = iy = -1
                for idx, B in enumerate(mv):
                    if (B >> x) & 1:
                        ix = idx
                    if (B >> y) & 1:
                        iy = idx
                if ix == iy:
                    same += 1
                elif ix < iy:
                    bx += 1
                else:
                    by += 1
            pi = Fraction(bx, bx + by) if bx + by else None
            ws[(x, y)] = (Fraction(same, r.nmoves), Fraction(bx, r.nmoves),
                          Fraction(by, r.nmoves), pi)
        r.walkstats = ws
        cand = [min(v[3], 1 - v[3]) for v in ws.values() if v[3] is not None]
        r.delta_walk = max(cand) if cand else None
    # the bridge object of the ADDENDUM
    r.br = Bridge(P, e, before)
    r.qfrac = r.qmass = None
    if r.br.Lstar is not None and not r.is_chain:
        qc = quotient_concentration(r, r.br, lat)
        if qc:
            r.qfrac, r.qmass, _ = qc
    # I4: a relabelling-invariant fingerprint of the whole (Q(P), m) structure
    fp = []
    for X in r.levels:
        blocks = lat.parts[X]
        prof = tuple(sorted((bin(B).count("1"), e[B]) for B in blocks))
        fp.append((prof, r.mult[X], r.mc[X]))
    r.inv4 = (r.nlev, tuple(sorted(fp)))
    return r


def _perm_sign(w):
    s = 1
    n = len(w)
    for i in range(n):
        for j in range(i + 1, n):
            if w[i] > w[j]:
                s = -s
    return s


def _longest_chain(P, x):
    best = [x]
    for y in range(P.n):
        if (P.up[x] >> y) & 1:
            c = _longest_chain(P, y)
            if len(c) + 1 > len(best):
                best = [x] + c
    return best


def _width(P):
    """Largest antichain, by brute force over subsets."""
    best = 0
    for S in range(1 << P.n):
        elems = [i for i in range(P.n) if (S >> i) & 1]
        if all(not P.comparable(a, b) for i, a in enumerate(elems) for b in elems[i + 1:]):
            best = max(best, len(elems))
    return best


def _ncomponents(P):
    parent = list(range(P.n))
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for (a, b) in P.less:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    return len(set(find(i) for i in range(P.n)))


# --------------------------------------------------------------------------
# SECTION 1 -- THE BRIDGE OBJECT (the ADDENDUM's primary handle)
# --------------------------------------------------------------------------

def section1_bridge(pop_by_n):
    hr("SECTION 1  THE BRIDGE OBJECT: majority tournament, L*, and concentration")
    print("IF a counterexample P exists, then no incomparable pair of P is undecided,")
    print("so orienting every pair by its majority gives a TOTAL orientation -- a")
    print("tournament M(P) canonically determined by P.  If M(P) is acyclic it is a")
    print("distinguished linear extension L* of P.  Acyclicity is NOT assumed below; it")
    print("is tested.  Both branches are reported.")

    sub("1a  THEOREM: a counterexample's majority relation is a LINEAR ORDER")
    print("This is not tested, because it is proved.  Let P be a counterexample, so no")
    print("incomparable pair has p in [1/3, 2/3].  Orient x -> y iff p(x,y) > 2/3.")
    print()
    print("  TOTAL.  1/2 lies in the forbidden band, so no pair is tied and every pair is")
    print("  oriented.  Comparable pairs have p = 1 and orient with P.")
    print("  TRANSITIVE.  Suppose x -> y and y -> z.  Then")
    print("      Pr[x<y AND y<z]  >=  p(x,y) + p(y,z) - 1  >  2/3 + 2/3 - 1  =  1/3,")
    print("  and the event {x<y and y<z} is contained in {x<z}, so p(x,z) > 1/3.  The")
    print("  hypothesis forbids p(x,z) in [1/3, 2/3], hence p(x,z) > 2/3, hence x -> z.")
    print()
    print("So M(P) is a total, transitive, antisymmetric relation containing P: a linear")
    print("extension L* of P, unconditionally, GIVEN that P is a counterexample.  The")
    print("FORBIDDEN MIDDLE BAND is what closes the composition -- 'every pair has a")
    print("majority' alone would not, and Condorcet cycles are a real phenomenon in")
    print("majority tournaments in general.  That is the trap, and 1a' measures it.")
    print()
    print("STATEMENT DISCIPLINE.  The theorem is conditional on a counterexample")
    print("existing.  It says nothing about a general poset, and the sweep in 1a' is a")
    print("DIFFERENT population where the hypothesis is false -- its results are not")
    print("evidence for the theorem and must not be read as any.")

    sub("1a' GENERAL POSETS ARE A DIFFERENT QUESTION -- swept, and NOT claimed")
    print("M(P) here is the STRICT majority digraph of an arbitrary poset: x -> y iff")
    print("p(x,y) > 1/2.  Ties (p = 1/2 exactly) are left unoriented.  General posets do")
    print("NOT satisfy the counterexample hypothesis, so 1a does not apply to them and")
    print("nothing below is offered as support for it.  NO CLAIM of general transitivity")
    print("is made here: the sweep bounds the range in which no cycle occurs, and that")
    print("is all it does.")
    print("%-4s %8s %10s %10s %10s %12s" %
          ("n", "posets", "cyclic M", "tie-free", "with ties", "strongest cycle"))
    tot_all = tot_cyc = 0
    for n, recs in sorted(pop_by_n.items()):
        cyc = [r for r in recs if not r.br.acyclic]
        tf = [r for r in recs if r.br.tie_free]
        strongest = max((r.br.cyc_best for r in recs if r.br.cyc_best is not None),
                        default=None)
        tot_all += len(recs)
        tot_cyc += len(cyc)
        print("%-4d %8d %10d %10d %10d %12s"
              % (n, len(recs), len(cyc), len(tf), len(recs) - len(tf), fs(strongest)))
    print()
    print("RESULT: %d cyclic majority digraphs out of %d posets on 3..%d elements."
          % (tot_cyc, tot_all, max(pop_by_n)))
    if tot_cyc == 0:
        print("So no poset in the exhaustive range has a majority cycle.  THAT IS NOT A")
        print("THEOREM AND NOT EVIDENCE FOR ONE: it is a statement about posets of size")
        print("<= %d, on a population where the counterexample hypothesis does not hold."
              % max(pop_by_n))
        print("The next block exhibits a majority cycle just outside this range, which is")
        print("why the sweep must not be read as general transitivity.")
    else:
        print("Cyclic examples occur in the exhaustive range; the strongest-cycle column")
        print("is the largest over cycles of the minimum edge strength max(p,1-p).")
    print()
    print("THERE IS NO CYCLIC BRANCH FOR A COUNTEREXAMPLE.  An earlier version of this")
    print("brief forked on acyclicity; 1a's proof closes the fork, and the fork is")
    print("deleted rather than left as a caveat.  A counterexample's majority relation is")
    print("a linear order, full stop.  What follows concerns GENERAL posets only.")
    print()
    print("AND THEY DO EXIST FOR GENERAL POSETS, just not in the exhaustive range.  A")
    print("witness, rebuilt and re-verified here from its cover relations:")
    Pw = Poset(11, [(0, 2), (0, 6), (0, 9), (1, 3), (1, 9), (2, 10),
                    (3, 6), (3, 7), (4, 5), (4, 6), (6, 10)])
    ew = restriction_counts(Pw)
    bw = pair_before_counts(Pw, ew)
    totw = ew[(1 << 11) - 1]
    pw = {}
    sw = [0] * 11
    for x in range(11):
        for y in range(11):
            if x != y:
                pw[(x, y)] = Fraction(bw[(x, y)], totw)
                if pw[(x, y)] > Fraction(1, 2):
                    sw[x] |= 1 << y
    tri = None
    for a in range(11):
        for b2 in range(11):
            for c in range(11):
                if len({a, b2, c}) < 3:
                    continue
                if ((sw[a] >> b2) & 1) and ((sw[b2] >> c) & 1) and ((sw[c] >> a) & 1):
                    tri = (a, b2, c)
                    break
            if tri:
                break
        if tri:
            break
    print("    n = 11, e(P) = %d, covers: %s" % (totw, Pw.cover_string()))
    if tri:
        a, b2, c = tri
        print("    majority 3-CYCLE  %d -> %d -> %d -> %d, with margins" % (a, b2, c, a))
        for (u, v) in ((a, b2), (b2, c), (c, a)):
            print("        p(%d,%d) = %-14s = %.5f   incomparable in P: %s"
                  % (u, v, fs(pw[(u, v)]), float(pw[(u, v)]), not Pw.comparable(u, v)))
        weak = min(pw[(a, b2)], pw[(b2, c)], pw[(c, a)])
        print("    weakest edge %s = %.5f, which is INSIDE the band [1/3, 2/3] that the"
              % (fs(weak), float(weak)))
        print("    counterexample hypothesis forbids.  So the cycle is real, and 1a's")
        print("    proof excludes it for exactly the stated reason: every edge of a")
        print("    counterexample's majority relation is decided by a margin above 2/3,")
        print("    and this cycle's edges are decided by margins of about 1/2.")
    print()
    print("    Found by random search (seed 4242; no cycle in 4200 random posets at each")
    print("    of n = 8, 9, 10, and none in the exhaustive sweep to n = 7).  n = 11 is")
    print("    NOT claimed to be minimal -- only that a witness exists and that the")
    print("    exhaustive range above is too small to see one.  The moral is the one the")
    print("    corrected brief states: an imported general caveat is not an obstruction")
    print("    until it is checked against the strength of the specific hypothesis, and")
    print("    here the sweep above would have been read as support for a theorem it")
    print("    cannot support.")

    sub("1b  L* is a linear extension of P  (verified, not assumed)")
    bad = tot = 0
    for n, recs in sorted(pop_by_n.items()):
        for r in recs:
            if r.br.Lstar is None:
                continue
            tot += 1
            les = set(linear_extensions(r.P))
            if r.br.Lstar not in les:
                bad += 1
    bcheck("L* in L(P): 0 bad of %d posets" % tot, bad == 0, "%d bad" % bad)
    print("       (it must be: a comparable pair has p = 1, so M contains P.)")

    sub("1c  THE IDENTITY  E[inv(L,L*)] = sum over Inc(P) of min(p, 1-p)")
    print("Verified against direct enumeration of L(P), and shown INDEPENDENT of the")
    print("tie-break in L* (a tied pair contributes 1/2 whichever way L* orients it).")
    bad = tot = 0
    badtb = 0
    for n, recs in sorted(pop_by_n.items()):
        if n > 6:
            continue
        for r in recs:
            if r.br.Lstar is None or r.is_chain:
                continue
            tot += 1
            dist = r.br.inv_distribution()
            direct = sum(Fraction(d * c, r.e) for d, c in dist.items())
            if direct != r.br.Einv:
                bad += 1
            # tie-break independence: reverse every tied pair's orientation and
            # recompute against the same closed form
            if r.br.ties:
                alt = _alt_lstar(r.br)
                if alt is not None:
                    d2 = _inv_mean(r, alt)
                    if d2 != r.br.Einv:
                        badtb += 1
    bcheck("closed form == enumeration: 0 bad of %d posets (n<=6)" % tot, bad == 0,
           "%d bad" % bad)
    bcheck("tie-break independent: 0 bad", badtb == 0, "%d bad" % badtb)

    sub("1d  THE CONCENTRATION RATIO  R(P) = 3 E[inv(L,L*)] / |Inc(P)|")
    print("IF a counterexample exists THEN R(P) < 1.  Since R is 3x the MEAN and")
    print("3 delta is 3x the MAX of the same per-pair numbers, R <= 3 delta always, so")
    print("R < 1 is strictly weaker than the counterexample condition 3 delta < 1.")
    print("The point of this table is HOW MUCH weaker.")
    print()
    print("%-4s %8s %10s %10s %12s %14s %10s" %
          ("n", "non-chain", "min 3delta", "min R", "#R<1", "%R<1", "#3delta<1"))
    for n, recs in sorted(pop_by_n.items()):
        pop = [r for r in recs if not r.is_chain]
        if not pop:
            continue
        m3d = min(3 * r.delta for r in pop)
        mR = min(r.br.R for r in pop)
        nR = sum(1 for r in pop if r.br.R < 1)
        n3d = sum(1 for r in pop if 3 * r.delta < 1)
        print("%-4d %8d %10s %10s %12d %13.1f%% %10d"
              % (n, len(pop), fs(m3d), fs(mR), nR, 100.0 * nR / len(pop), n3d))
    print()
    print("READ THE LAST TWO COLUMNS TOGETHER.  #3delta<1 is 0 everywhere: no")
    print("counterexample exists at these sizes, as expected.  #R<1 is NOT 0.  So the")
    print("concentration condition is satisfied by posets that are PROVABLY NOT")
    print("counterexamples, and satisfied by more of them as n grows.")

    sub("1e  WHICH posets satisfy the concentration bound, and where the extremal ones sit")
    for n, recs in sorted(pop_by_n.items()):
        pop = [r for r in recs if not r.is_chain]
        if not pop or n < 5:
            continue
        dmin = min(r.delta for r in pop)
        ext = [r for r in pop if r.delta == dmin]
        byR = sorted(pop, key=lambda r: (r.br.R, r.cover))
        print("  n=%d:" % n)
        print("    delta-EXTREMAL posets (delta = %s, %d of them): R = %s"
              % (fs(dmin), len(ext), ", ".join(sorted(set(fs(r.br.R) for r in ext)))))
        print("    smallest R in the population:")
        for r in byR[:3]:
            print("        R=%-8s 3delta=%-8s |Inc|=%-3d e=%-6d %s"
                  % (fs(r.br.R), fs(3 * r.delta), r.br.ninc, r.e, r.cover))
    print()
    print("The mechanism is the mean/max gap and nothing subtler: a poset with many")
    print("heavily-decided pairs and a few balanced ones has a small MEAN while its MAX")
    print("stays large.  Disjoint unions of two chains are the extreme case, and they are")
    print("this programme's own canonical UNFROZEN family (STATE: C_n + C_n has")
    print("delta = 1/2).  Section 1f follows that family out past the exhaustive range.")

    sub("1f  NAMED FAMILIES beyond the exhaustive range")
    print("Cost note: these use the same exact O(2^n n) count DP; nothing here is")
    print("enumerated over L(P), so n up to 12 is seconds.  No poset beyond n = 12 is")
    print("computed anywhere in this probe.")
    print()
    print("%-22s %4s %8s %10s %10s %10s %8s" %
          ("family", "n", "e(P)", "3delta", "R", "R<1?", "|Inc|"))
    fams = []
    for a in range(2, 7):
        for b in range(2, 7):
            if a <= b and 4 <= a + b <= 12:
                fams.append(("C_%d + C_%d" % (a, b), chain_sum_family(a, b)))
    for k in range(3, 10):
        fams.append(("1+2 under C_%d" % (k - 3), one_plus_two(k)))
    for k in range(4, 11):
        fams.append(("fence_%d" % k, fence(k)))

    for name, P in fams:
        if P.is_chain():
            continue
        e = restriction_counts(P)
        before = pair_before_counts(P, e)
        br = Bridge(P, e, before)
        if br.R is None:
            continue
        print("%-22s %4d %8d %10s %10s %10s %8d"
              % (name, P.n, br.e, fs(3 * br.delta), fs(br.R),
                 "YES" if br.R < 1 else "no", br.ninc))

    print()
    print("The 1+2-under-a-chain family holds delta = 1/3 exactly at every n -- it is the")
    print("family that MEETS the conjecture's bound -- and its R is exactly 1 at every n.")
    print("So the family that comes closest to the conjecture's boundary sits exactly ON")
    print("the concentration boundary and never inside it, while two-chain families sit")
    print("strictly inside it with delta far above 1/3.")
    print()
    print("HONEST PRICING OF THE ADDENDUM'S QUANTITY.  R(P) < 1 is a true consequence of")
    print("the counterexample hypothesis and it is correctly stated in the ticket as a")
    print("consequence rather than a test.  What this section adds is the size of the")
    print("slack: the condition is already met by real posets whose delta is far from")
    print("1/3, its satisfying fraction GROWS with n, and the delta-extremal family sits")
    print("on its boundary rather than inside it.  So it is not a usable filter on the")
    print("search space, and the reason is structural (mean versus max), not a matter of")
    print("the range being too small.")
    return None


def _alt_lstar(br):
    """A second valid L*: re-run the topological sort after reversing nothing but
    preferring the largest available element (a different completion of the same
    strict majority order)."""
    n = br.n
    succ = br.succ
    indeg = [0] * n
    for i in range(n):
        m = succ[i]
        while m:
            j = (m & -m).bit_length() - 1
            m &= m - 1
            indeg[j] += 1
    out = []
    avail = [i for i in range(n) if indeg[i] == 0]
    while avail:
        avail.sort(reverse=True)
        i = avail.pop(0)
        out.append(i)
        m = succ[i]
        while m:
            j = (m & -m).bit_length() - 1
            m &= m - 1
            indeg[j] -= 1
            if indeg[j] == 0:
                avail.append(j)
    return tuple(out) if len(out) == n else None


def _inv_mean(r, Lstar):
    rank = {x: k for k, x in enumerate(Lstar)}
    tot = 0
    for w in linear_extensions(r.P):
        pos = {x: k for k, x in enumerate(w)}
        for (a, b) in r.per_pair:
            if (pos[a] < pos[b]) != (rank[a] < rank[b]):
                tot += 1
    return Fraction(tot, r.e)


# --------------------------------------------------------------------------
# SECTION 2 -- THE QUOTIENT SIDE
# --------------------------------------------------------------------------

def section2_facebalance(pop_by_n, rng):
    hr("SECTION 2  THE FACE-SIDE BALANCE CONSTANT -- the one place a signal appears")
    print("The action supplies its OWN balance constant, and it needs no linear")
    print("extensions to compute.  For an incomparable pair, over the weight that is")
    print("uniform on the P-compatible moves, let")
    print("    s   = Pr[the move leaves x,y in one block]         (pair not separated)")
    print("    q   = Pr[x's block strictly before y's],  q' = the other way.")
    print("The walk's own stationary marginal is pi(x<y) = q/(q+q') -- exact, proved in")
    print("SECTION 4, and checked against the stationary vector of the actual matrix in")
    print("selftest.py control C8.  Define, in exact parallel with delta,")
    print("    delta_walk(P) = max over incomparable pairs of min(pi, 1-pi).")
    print()
    print("delta uses the uniform measure on L(P); delta_walk uses a count of faces of")
    print("the order cone.  They are different functionals of P.  How close are they?")

    sub("2a  per-PAIR agreement, over every incomparable pair of every non-chain poset")
    print("%-4s %8s %10s %10s %12s %12s %14s" %
          ("n", "#pairs", "rho", "%equal", "mean |err|", "max |err|", "max err as frac"))
    trend = []
    for n, recs in sorted(pop_by_n.items()):
        rows = []
        for r in recs:
            if r.is_chain or r.walkstats is None:
                continue
            for pr, mn in r.per_pair.items():
                pi = r.walkstats[pr][3]
                if pi is not None:
                    rows.append((mn, min(pi, 1 - pi)))
        if len(rows) < 5:
            continue
        rho = spearman([float(a) for a, _ in rows], [float(b) for _, b in rows])
        eq = sum(1 for a, b in rows if a == b)
        errs = [abs(a - b) for a, b in rows]
        mean_e = sum(errs) / len(errs)
        max_e = max(errs)
        print("%-4d %8d %10.4f %9.1f%% %12.5f %12s %14.5f"
              % (n, len(rows), rho, 100.0 * eq / len(rows), float(mean_e),
                 fs(max_e), float(max_e)))
        trend.append((n, float(mean_e), float(max_e)))

    sub("2b  per-POSET agreement, and whether it survives controlling for e(P)")
    print("%-4s %8s %12s %12s %14s" % ("n", "N", "rho(d,d_walk)", "perm p", "rho | e(P)"))
    for n, recs in sorted(pop_by_n.items()):
        grp = [r for r in recs if not r.is_chain and r.delta_walk is not None]
        if len(grp) < 6:
            continue
        xs = [float(r.delta_walk) for r in grp]
        ys = [float(r.delta) for r in grp]
        rho, p = perm_pvalue(xs, ys, 2000, random.Random(SEED))
        byE = {}
        for r in grp:
            byE.setdefault(r.e, []).append(r)
        px, py = [], []
        for _, v in sorted(byE.items()):
            if len(v) < 3:
                continue
            a = [float(q.delta_walk) for q in v]
            b = [float(q.delta) for q in v]
            ma, mb = sum(a) / len(a), sum(b) / len(b)
            px += [t - ma for t in a]
            py += [t - mb for t in b]
        prho = spearman(px, py) if len(px) >= 4 else None
        print("%-4d %8d %12.4f %12.4f %14s"
              % (n, len(grp), rho, p, "%.4f" % prho if prho is not None else "n/a"))
    print()
    print("This is the ONLY invariant in the whole probe whose correlation with delta")
    print("survives removing e(P).  Every other one in SECTION 5 collapses to near zero")
    print("under that control.  So the signal is real and it is not the size axis.")

    sub("2c  BUT IT IS NOT AN INEQUALITY IN EITHER DIRECTION")
    print("A one-sided bound would make this a certificate.  It is not one-sided:")
    print("%-4s %14s %16s %16s" %
          ("n", "#pairs", "min(pi,1-pi) > min(p,1-p)", "delta_walk > delta"))
    for n, recs in sorted(pop_by_n.items()):
        grp = [r for r in recs if not r.is_chain and r.walkstats is not None]
        if not grp:
            continue
        vp = tp = 0
        vd = 0
        for r in grp:
            for pr, mn in r.per_pair.items():
                pi = r.walkstats[pr][3]
                if pi is None:
                    continue
                tp += 1
                if min(pi, 1 - pi) > mn:
                    vp += 1
            if r.delta_walk > r.delta:
                vd += 1
        print("%-4d %14d %16d %16d" % (n, tp, vp, vd))
    print()
    print("Both directions occur.  So delta_walk can neither certify delta >= 1/3 nor")
    print("witness delta < 1/3, and no rigorous filter follows from it.")

    sub("2d  AND AT THE 1/3 THRESHOLD IT ALREADY MISFIRES")
    print("The only thing that matters for detection is behaviour at the decision line.")
    print("%-4s %10s %14s %16s %14s" %
          ("n", "N", "#d_walk < 1/3", "#delta < 1/3", "false positives"))
    for n, recs in sorted(pop_by_n.items()):
        grp = [r for r in recs if not r.is_chain and r.delta_walk is not None]
        if not grp:
            continue
        a = [r for r in grp if r.delta_walk < Fraction(1, 3)]
        b = [r for r in grp if r.delta < Fraction(1, 3)]
        print("%-4d %10d %14d %16d %14d" % (n, len(grp), len(a), len(b), len(a) - len(b)))
        for r in sorted(a, key=lambda r: r.cover)[:2]:
            print("       FALSE POSITIVE: d_walk=%-8s delta=%-8s  %s"
                  % (fs(r.delta_walk), fs(r.delta), r.cover))
    print()
    print("THE TREND THAT DECIDES IT.  The approximation error grows with n while the")
    print("margin it must resolve shrinks -- the delta-extremal posets sit AT 1/3, so the")
    print("quantity to resolve is the distance from 1/3, which is 0 for them:")
    print("%-4s %14s %14s" % ("n", "max |err|", "min(delta) - 1/3"))
    for n, mean_e, max_e in trend:
        grp = [r for r in pop_by_n[n] if not r.is_chain]
        print("%-4d %14.5f %14.5f" % (n, max_e, float(min(r.delta for r in grp) - Fraction(1, 3))))
    print()
    print("So: a genuine, e(P)-independent signal, and a heuristic only.  IF a")
    print("counterexample exists, delta_walk gives no way to recognise it: the error at")
    print("n = %d already exceeds the entire margin between the extremal posets and the"
          % max(n for n, _, _ in trend))
    print("conjecture's boundary, and the error is growing.  Stated as a filter rather")
    print("than a test, 'delta_walk < 1/3' retains a small fraction of the population and")
    print("is the most selective heuristic in this probe -- see SECTION 5, table A5.")


def _mean_sd(vals):
    n = len(vals)
    if n == 0:
        return None, None
    m = sum(vals) / n
    if n < 2:
        return m, 0.0
    v = sum((x - m) ** 2 for x in vals) / (n - 1)
    return m, v ** 0.5


def section2_quotient(pop_by_n, lats):
    hr("SECTION 3  THE QUOTIENT SIDE: is Q(P) organised around L*'s own chain?")
    print("L* singles out one chain inside the acyclic-partition lattice Q(P): the")
    print("partitions whose blocks are contiguous INTERVALS of L*.  There are exactly")
    print("2^(n-1) of them and every one is a level, because ordering those blocks along")
    print("L* is P-compatible (verified by the assertion in bridge.quotient_concentration).")
    print()
    print("Two statistics, both 1 for a chain:")
    print("  qfrac = 2^(n-1) / |Q(P)|                       share of the LEVELS")
    print("  qmass = (sum of m_X over those levels) / e(P)   share of the SPECTRUM")
    print()
    print("POPULATION: the TIE-FREE non-chain posets.  A counterexample is tie-free, and")
    print("on tie-free posets L* is UNIQUE, so both statistics are canonical.  On posets")
    print("with a tied pair L* depends on the tie-break and these numbers would not be")
    print("well defined -- those posets are excluded and counted.")
    print()
    print("%-4s %8s %10s %26s %26s" %
          ("n", "tie-free", "#extremal", "qmass: extremal vs rest", "qfrac: extremal vs rest"))
    out = []
    for n, recs in sorted(pop_by_n.items()):
        pop = [r for r in recs if not r.is_chain and r.br.tie_free and r.qmass is not None]
        if len(pop) < 6:
            print("%-4d %8d %10s %26s %26s" % (n, len(pop), "-", "(too few)", ""))
            continue
        dmin = min(r.delta for r in pop)
        ext = [r for r in pop if r.delta == dmin]
        rest = [r for r in pop if r.delta != dmin]
        if not rest:
            continue
        me, _ = _mean_sd([float(r.qmass) for r in ext])
        mr, sr = _mean_sd([float(r.qmass) for r in rest])
        fe, _ = _mean_sd([float(r.qfrac) for r in ext])
        fr, sfr = _mean_sd([float(r.qfrac) for r in rest])
        zm = (me - mr) / sr if sr else float("nan")
        zf = (fe - fr) / sfr if sfr else float("nan")
        print("%-4d %8d %10d  %.3f vs %.3f  z=%+5.2f  %.3f vs %.3f  z=%+5.2f"
              % (n, len(pop), len(ext), me, mr, zm, fe, fr, zf))
        out.append((n, len(pop), len(ext), me, mr, sr, zm, fe, fr, sfr, zf))
    print()
    print("z is the EFFECT SIZE: (extremal mean - rest mean) / SD of the rest.  This is")
    print("one null model -- 'the rest' at the same n is the size-matched comparison")
    print("population, and it is the whole of it, not a sample.  IT IS NOT SUFFICIENT,")
    print("and 2a says why.")

    sub("3a  THE SATURATION CONTROL -- and it dissolves most of the effect above")
    print("Every extremal poset has qmass = 1 EXACTLY, i.e. its whole spectrum sits on")
    print("L*'s chain.  But qmass is bounded above by 1, so 'extremal posets have")
    print("qmass = 1' is only informative if reaching 1 is rare.  It is not:")
    print()
    print("%-4s %10s %14s %14s %16s" %
          ("n", "tie-free", "#qmass = 1", "%qmass = 1", "of those, %ext"))
    for n, recs in sorted(pop_by_n.items()):
        pop = [r for r in recs if not r.is_chain and r.br.tie_free and r.qmass is not None]
        if len(pop) < 6:
            continue
        dmin = min(r.delta for r in pop)
        sat = [r for r in pop if r.qmass == 1]
        ext = [r for r in pop if r.delta == dmin]
        print("%-4d %10d %14d %13.1f%% %15.1f%%"
              % (n, len(pop), len(sat), 100.0 * len(sat) / len(pop),
                 100.0 * len(ext) / len(sat) if sat else 0.0))
    print()
    print("So qmass = 1 is a large, mostly non-extremal club, and being in it is weak")
    print("evidence.  The honest one-sided statement is the last column: among the posets")
    print("that saturate, the extremal ones are a small minority.  A predicate satisfied")
    print("by all extremal posets AND by many others is a filter on the search space only")
    print("to the extent that it excludes the rest of the population -- quantified next.")

    sub("3b  the same comparison controlling for e(P), WITH TIES REPORTED")
    print("A stricter size-match: compare each extremal poset only against tie-free")
    print("posets with the SAME linear-extension count, since e(P) drives both qmass and")
    print("delta.  Rank 1 means nobody is strictly higher -- which is uninformative if")
    print("many are TIED, so the tie count is printed and is the number to read.")
    for n, recs in sorted(pop_by_n.items()):
        pop = [r for r in recs if not r.is_chain and r.br.tie_free and r.qmass is not None]
        if len(pop) < 6:
            continue
        dmin = min(r.delta for r in pop)
        ext = sorted([r for r in pop if r.delta == dmin], key=lambda r: (r.e, r.cover))
        lines = 0
        for r in ext:
            grp = [q for q in pop if q.e == r.e]
            if len(grp) < 3:
                continue
            better = sum(1 for q in grp if q.qmass > r.qmass)
            tied = sum(1 for q in grp if q.qmass == r.qmass and q is not r)
            print("    n=%d e=%-5d %-26s qmass=%-6s rank %d of %-3d TIED WITH %d"
                  % (n, r.e, r.cover[:26], fs(r.qmass), better + 1, len(grp), tied))
            lines += 1
            if lines >= 3:
                break
        if lines == 0:
            print("    n=%d: no extremal poset has an e-group of size >= 3" % n)
    print()
    sub("3c  the ONE-SIDED constraint, which is what survives")
    print("IF a counterexample exists, is it forced into the qmass = 1 club?  No -- that")
    print("does not follow from anything proved here, and the extremal posets are a PROXY")
    print("not a counterexample.  What IS measurable is how selective the club is, i.e.")
    print("the fraction of the population a 'qmass = 1' filter would retain, and whether")
    print("that fraction shrinks with n (a usable filter) or not.")
    print("%-4s %14s %14s %20s" % ("n", "%retained", "%retained qfrac>=ext", "verdict at this n"))
    for n, recs in sorted(pop_by_n.items()):
        pop = [r for r in recs if not r.is_chain and r.br.tie_free and r.qmass is not None]
        if len(pop) < 6:
            continue
        dmin = min(r.delta for r in pop)
        ext = [r for r in pop if r.delta == dmin]
        fmin = min(r.qfrac for r in ext)
        keep = sum(1 for r in pop if r.qmass == 1) / len(pop)
        keep2 = sum(1 for r in pop if r.qmass == 1 and r.qfrac >= fmin) / len(pop)
        print("%-4d %13.1f%% %13.1f%% %20s"
              % (n, 100 * keep, 100 * keep2,
                 "selective" if keep2 < 0.10 else "weak"))
    print()
    print("VERDICT ON SECTION 3 is stated in the deliverable, not here; the numbers above")
    print("are the whole evidence for it, saturation control included.")
    return out


# --------------------------------------------------------------------------
# SECTION 4 -- SPECTRAL SEPARATION (the brief's original (a); secondary)
# --------------------------------------------------------------------------

SCALARS = [
    ("e(P)            ", lambda r: r.e,               "linear-extension count (the axis STATE already tracks)"),
    ("nlev            ", lambda r: r.nlev,            "#commitment levels = #acyclic-quotient partitions"),
    ("nlev_pos        ", lambda r: r.nlev_pos,        "#levels carrying nonzero multiplicity"),
    ("nmoves          ", lambda r: r.nmoves,          "#P-compatible moves (faces of the order cone)"),
    ("maxmult         ", lambda r: r.maxmult,         "largest multiplicity"),
    ("lambda_2        ", lambda r: r.lam2,            "2nd eigenvalue, uniform-move weight (exact)"),
    ("gap             ", lambda r: 1 - r.lam2,        "1 - lambda_2"),
    ("s_max           ", lambda r: r.s_max,           "max over incomp pairs of Pr[move does not separate]"),
    ("delta_walk      ", lambda r: r.delta_walk,      "the action's own balance constant (face-side delta)"),
    ("signimb         ", lambda r: r.signimb,         "|sign imbalance| of P"),
    ("width           ", lambda r: r.width,           "largest antichain (structural control)"),
    ("height          ", lambda r: r.height,          "longest chain (structural control)"),
    ("nlev/e          ", lambda r: Fraction(r.nlev, r.e), "levels per linear extension"),
]


def fiber_table(recs, keyfn):
    fib = {}
    for r in recs:
        k = keyfn(r)
        fib.setdefault(k, []).append(r)
    return fib


def collision_prob(fib, N):
    """Probability that two distinct uniformly-random members of the population
    land in the same fiber -- the null model for 'this invariant distinguishes'."""
    if N < 2:
        return None
    num = sum(len(v) * (len(v) - 1) for v in fib.values())
    return Fraction(num, N * (N - 1))


def analyse_detection(n, recs, rng, have_full):
    pop = [r for r in recs if not r.is_chain]
    prim = [r for r in pop if r.primitive]
    hr("(a) DETECTION at n = %d" % n)
    print("population: %d posets up to isomorphism; %d non-chains "
          "(chains excluded: delta undefined); %d of those primitive "
          "(incomparability graph connected = can be a MINIMAL counterexample)"
          % (len(recs), len(pop), len(prim)))

    for label, group in (("all non-chains", pop), ("primitive non-chains", prim)):
        if not group:
            continue
        sub("delta distribution over %s" % label)
        vals = sorted(set(r.delta for r in group))
        dmin = vals[0]
        print("min delta = %s   (conjecture asserts >= 1/3; %s)"
              % (fs(dmin), "TIGHT" if dmin == Fraction(1, 3) else
                 ("VIOLATED" if dmin < Fraction(1, 3) else "slack")))
        print("distinct delta values (lowest 6): %s"
              % ", ".join("%s x%d" % (fs(v), sum(1 for r in group if r.delta == v))
                          for v in vals[:6]))
        ext = [r for r in group if r.delta == dmin]
        print("EXTREMAL set (delta = min): %d posets" % len(ext))
        for r in sorted(ext, key=lambda r: r.cover)[:8]:
            print("    %-34s e=%-5d nlev=%-4d lam2=%-9s dwalk=%s"
                  % (r.cover, r.e, r.nlev, fs(r.lam2), fs(r.delta_walk)))
        if len(ext) > 8:
            print("    ... and %d more" % (len(ext) - 8))

    # everything below is on the primitive non-chains: the population that a
    # minimal counterexample lives in.
    group = prim if len(prim) >= 4 else pop
    gname = "primitive non-chains" if group is prim else "all non-chains"
    N = len(group)
    if N < 4:
        print("\n(too few posets at n=%d for the separation tests)" % n)
        return None
    dmin = min(r.delta for r in group)
    vals = sorted(set(r.delta for r in group))
    ext = [r for r in group if r.delta == dmin]
    near = [r for r in group if r.delta <= (vals[1] if len(vals) > 1 else vals[0])]

    sub("A1  resolution of each invariant, and the NULL MODEL (%s, N=%d)" % (gname, N))
    print("%-6s %-58s %8s %10s %10s" % ("rung", "invariant", "#fibers", "P[collide]", "%singleton"))
    ladder = [("I0", "e(P) alone -- the control", Rec.key_I0),
              ("I1", "#levels + level-size profile", Rec.key_I1),
              ("I2", "I1 + multiplicity profile", Rec.key_I2),
              ("I3", "I2 + exact spectrum with multiplicities (uniform-move w)", Rec.key_I3),
              ("I4", "full (Q(P), m, move-count) fingerprint", Rec.key_I4)]
    fibs = {}
    for tag, desc, kf in ladder:
        if kf(group[0]) is None:
            print("%-6s %-58s %8s" % (tag, desc, "n/a"))
            continue
        fib = fiber_table(group, kf)
        fibs[tag] = fib
        cp = collision_prob(fib, N)
        singles = sum(1 for v in fib.values() if len(v) == 1)
        print("%-6s %-58s %8d %10.4f %9.1f%%"
              % (tag, desc, len(fib), float(cp), 100.0 * singles / N))
    print()
    print("READ THIS AS THE NULL MODEL.  '%%singleton' is the fraction of ALL posets in")
    print("the population that are already alone in their fiber.  An extremal poset being")
    print("alone in its fiber carries information only to the extent that this number is")
    print("below 100%.")

    sub("A2  are the extremal / near-extremal posets ISOLATED, and are their fibers PURE?")
    print("EXTREMAL = delta = %s (%d posets).  NEAR = delta <= %s (%d posets)."
          % (fs(dmin), len(ext), fs(vals[1] if len(vals) > 1 else vals[0]), len(near)))
    print("%-6s %14s %14s %26s" % ("rung", "extremal alone", "baseline alone", "delta-range in extremal fibers"))
    for tag, desc, kf in ladder:
        if tag not in fibs:
            continue
        fib = fibs[tag]
        alone = sum(1 for r in ext if len(fib[kf(r)]) == 1)
        lo = hi = None
        for r in ext:
            for q in fib[kf(r)]:
                lo = q.delta if lo is None else min(lo, q.delta)
                hi = q.delta if hi is None else max(hi, q.delta)
        base = sum(1 for v in fib.values() if len(v) == 1) / N
        print("%-6s %8d/%-5d %13.1f%% %26s"
              % (tag, alone, len(ext), 100.0 * base,
                 "[%s , %s]" % (fs(lo), fs(hi))))
    print()
    print("A fiber whose delta-range is a single point would mean the invariant PINS delta")
    print("on that fiber.  A wide range means posets the invariant cannot tell apart have")
    print("different balance -- i.e. the invariant provably cannot detect delta.")

    # explicit witnesses of indistinguishability
    sub("A3  WITNESSES: pairs the finest invariant (I4) cannot separate but delta can")
    wit = []
    if "I4" in fibs:
        for k, v in sorted(fibs["I4"].items(), key=lambda kv: str(kv[0])[:80]):
            if len(v) < 2:
                continue
            ds = sorted(set(r.delta for r in v))
            if len(ds) > 1:
                wit.append((max(ds) - min(ds), v))
    wit.sort(key=lambda t: (-t[0], t[1][0].cover))
    if not wit:
        print("NONE: at n=%d every I4-fiber has constant delta." % n)
        print("(That does not mean I4 determines delta -- it means no counterexample to")
        print(" that is visible at this size.  See the fiber sizes in A1.)")
    else:
        print("%d I4-fibers contain posets with DIFFERENT delta.  The %d widest:"
              % (len(wit), min(3, len(wit))))
        for spread, v in wit[:3]:
            print("  spread %s over %d posets in one fiber:" % (fs(spread), len(v)))
            for r in sorted(v, key=lambda r: (r.delta, r.cover)):
                print("      delta=%-8s e=%-5d lam2=%-9s  %s"
                      % (fs(r.delta), r.e, fs(r.lam2), r.cover))
    n_i4_nonsingleton = sum(1 for v in fibs.get("I4", {}).values() if len(v) > 1)
    print()
    print("I4 non-singleton fibers: %d (so I4 %s a complete invariant of the poset here)"
          % (n_i4_nonsingleton, "is NOT" if n_i4_nonsingleton else "is"))

    sub("A4  does any invariant PREDICT delta?  rank correlation + permutation null")
    reps = 2000
    print("%-18s %8s %9s %9s   %s" % ("scalar", "rho", "perm p", "rho|e(P)", "meaning"))
    rows = []
    for name, fn, desc in SCALARS:
        xs = [fn(r) for r in group]
        if any(x is None for x in xs):
            print("%-18s %8s %9s %9s   %s" % (name.strip(), "n/a", "", "", desc))
            continue
        xs = [float(x) for x in xs]
        ys = [float(r.delta) for r in group]
        rho, p = perm_pvalue(xs, ys, reps, random.Random(SEED))
        # partial: pooled within-fiber-of-e(P) correlation (controls for e(P))
        byE = {}
        for r in group:
            byE.setdefault(r.e, []).append(r)
        px, py = [], []
        for _, v in sorted(byE.items()):
            if len(v) < 3:
                continue
            a = [float(fn(q)) for q in v]
            b = [float(q.delta) for q in v]
            ma, mb = sum(a) / len(a), sum(b) / len(b)
            px += [t - ma for t in a]
            py += [t - mb for t in b]
        prho = spearman(px, py) if len(px) >= 4 else None
        rows.append((abs(rho) if rho is not None else -1, name, rho, p, prho, desc))
        print("%-18s %8s %9s %9s   %s"
              % (name.strip(),
                 "%.3f" % rho if rho is not None else "n/a",
                 "%.4f" % p if p is not None else "",
                 "%.3f" % prho if prho is not None else "n/a",
                 desc))
    print()
    print("rho    = Spearman correlation with delta over the %d posets." % N)
    print("perm p = two-sided permutation p-value, %d reps, seed %d (1/%d is the floor)."
          % (reps, SEED, reps + 1))
    print("rho|e  = the SAME correlation computed within groups of equal e(P) and pooled,")
    print("         i.e. after removing everything explainable by the linear-extension")
    print("         count.  A face-side invariant earns its keep only here.")

    sub("A5  one-sided SEARCH-SPACE constraints: 'a counterexample must have s <= t'")
    print("For each scalar, t = the extreme value over the EXTREMAL posets, and the")
    print("fraction of the population satisfying the resulting one-sided bound.  A")
    print("fraction near 1 means the condition is vacuous; near 0 means it is a real")
    print("constraint on the search space (valid as a heuristic only -- the extremal")
    print("posets are a PROXY for counterexamples, which do not exist at these sizes).")
    print("%-18s %12s %12s %10s" % ("scalar", "t (max ext)", "frac s<=t", "direction"))
    for name, fn, desc in SCALARS:
        xs = [fn(r) for r in group]
        if any(x is None for x in xs):
            continue
        te = max(fn(r) for r in ext)
        frac = sum(1 for r in group if fn(r) <= te) / N
        tl = min(fn(r) for r in ext)
        fracl = sum(1 for r in group if fn(r) >= tl) / N
        if frac <= fracl:
            print("%-18s %12s %11.1f%% %10s" % (name.strip(), fs(te), 100.0 * frac, "s <= t"))
        else:
            print("%-18s %12s %11.1f%% %10s" % (name.strip(), fs(tl), 100.0 * fracl, "s >= t"))

    return {"n": n, "N": N, "gname": gname, "dmin": dmin, "next": vals[1] if len(vals) > 1 else None,
            "nfib": {t: len(f) for t, f in fibs.items()},
            "single": {t: sum(1 for v in f.values() if len(v) == 1) / N for t, f in fibs.items()},
            "i4_bad": n_i4_nonsingleton, "nwit": len(wit),
            "ext": len(ext)}


def analyse_pairs(n, recs, rng):
    """The per-PAIR experiment: delta and lambda_2 are both maxima over
    incomparable pairs of a pair statistic.  Do the pair statistics agree?"""
    hr("(a-bis) THE PER-PAIR EXPERIMENT at n = %d" % n)
    print("delta(P)     = max over incomparable pairs of  min(p, 1-p),  p from L(P).")
    print("lambda_2(P)  = max over incomparable pairs of  s(x,y) = Pr[a uniform move")
    print("               leaves the pair in one block]   (proved in (b), checked below).")
    print("The action also has its own pair marginal pi(x<y) = q(x<y)/(q(x<y)+q(y<x)).")
    print("If the action detected balance, min(pi,1-pi) would track min(p,1-p).")
    rows = []
    for r in recs:
        if r.is_chain or r.walkstats is None:
            continue
        for pr, mn in r.per_pair.items():
            s, qx, qy, pi = r.walkstats[pr]
            if pi is None:
                continue
            rows.append((float(mn), float(min(pi, 1 - pi)), float(s), r))
    if len(rows) < 10:
        print("\n(too few pairs)")
        return None
    xs = [t[0] for t in rows]
    ys = [t[1] for t in rows]
    zs = [t[2] for t in rows]
    sub("A6  correlation over ALL %d incomparable pairs of ALL %d non-chain posets"
        % (len(rows), sum(1 for r in recs if not r.is_chain and r.walkstats is not None)))
    r1, p1 = perm_pvalue(xs, ys, 2000, random.Random(SEED))
    r2, p2 = perm_pvalue(xs, zs, 2000, random.Random(SEED + 1))
    print("min(p,1-p)  vs  min(pi,1-pi)   [the action's own balance]:  rho = %.4f  p = %.4f"
          % (r1, p1))
    print("min(p,1-p)  vs  s(x,y)         [non-separation mass]     :  rho = %.4f  p = %.4f"
          % (r2, p2))
    exact = sum(1 for a, b, _, _ in rows if abs(a - b) < 1e-12)
    print("pairs where the two balances are EQUAL: %d of %d (%.1f%%)"
          % (exact, len(rows), 100.0 * exact / len(rows)))
    mad = sum(abs(a - b) for a, b, _, _ in rows) / len(rows)
    mx = max(abs(a - b) for a, b, _, _ in rows)
    print("|min(p,1-p) - min(pi,1-pi)|: mean %.4f, max %.4f" % (mad, mx))
    # does the argmax pair agree?
    agree = tot = 0
    for r in recs:
        if r.is_chain or r.walkstats is None or not r.per_pair:
            continue
        tot += 1
        bp = max(r.per_pair.items(), key=lambda kv: (kv[1], kv[0]))[0]
        bs = max(((pr, v[0]) for pr, v in r.walkstats.items()),
                 key=lambda kv: (kv[1], kv[0]))[0]
        if bp == bs:
            agree += 1
    print("the pair attaining delta = the pair attaining lambda_2: %d of %d posets (%.1f%%)"
          % (agree, tot, 100.0 * agree / tot))
    print()
    print("A poset with k incomparable pairs would agree by chance about 1/k of the time;")
    print("the mean 1/k over this population is %.3f."
          % (sum(1.0 / len(r.per_pair) for r in recs
                 if not r.is_chain and r.walkstats is not None and r.per_pair) / tot))
    return {"n": n, "rho_pi": r1, "rho_s": r2, "argmax_agree": agree / tot}


# --------------------------------------------------------------------------
# (b) NECESSARY CONDITIONS -- the structural checks
# --------------------------------------------------------------------------

BFAIL = []


def bcheck(name, ok, detail=""):
    print("  [%s] %s%s" % ("ok  " if ok else "FAIL", name, ("  -- " + detail) if detail else ""))
    if not ok:
        BFAIL.append(name)


def part_b(pop_by_n, lats):
    hr("SECTION 4  NECESSARY CONDITIONS -- structural statements, verified exhaustively")

    sub("B1  every block of every commitment level is CONVEX in P")
    bad = tot = 0
    for n, recs in sorted(pop_by_n.items()):
        lat = lats[n]
        for r in recs:
            for X in r.levels:
                for B in lat.parts[X]:
                    tot += 1
                    if not is_convex(r.P, B):
                        bad += 1
    bcheck("0 bad of %d (level, block) pairs, n=%s"
           % (tot, ",".join(str(k) for k in sorted(pop_by_n))), bad == 0, "%d bad" % bad)

    sub("B2  {B} + singletons is a level  <==>  B is convex")
    bad = tot = 0
    for n, recs in sorted(pop_by_n.items()):
        lat = lats[n]
        for r in recs:
            isl = set(r.levels)
            for B in range(1, 1 << n):
                blocks = [B] + [1 << i for i in range(n) if not ((B >> i) & 1)]
                idx = lat.index[part_key(blocks)]
                tot += 1
                if (idx in isl) != is_convex(r.P, B):
                    bad += 1
    bcheck("0 bad of %d (poset, subset) pairs" % tot, bad == 0, "%d bad" % bad)
    print("       => the level data exposes e(P|_B) for exactly the CONVEX subsets B.")

    sub("B3  m_X = 0 for every all-chain level EXCEPT the finest one")
    print("    If every block of X is a chain of P then prod_B e(P|_B) = 1, and the")
    print("    finest level already contributes m = 1 to that sum, so every other level")
    print("    refining X -- X included -- has m = 0.  The finest level is the ONE")
    print("    exception and it always has m = 1: its blocks are singletons, hence chains.")
    bad = tot = 0
    bad_not_bottom = 0
    for n, recs in sorted(pop_by_n.items()):
        lat = lats[n]
        for r in recs:
            for X in r.levels:
                allchain = True
                for B in lat.parts[X]:
                    el = [i for i in range(n) if (B >> i) & 1]
                    if any(not r.P.comparable(a, b) for i, a in enumerate(el) for b in el[i + 1:]):
                        allchain = False
                        break
                if not allchain:
                    continue
                if X == lat.bottom:
                    if r.mult[X] != 1:
                        bad_not_bottom += 1
                    continue
                tot += 1
                if r.mult[X] != 0:
                    bad += 1
    bcheck("0 bad of %d all-chain levels other than the finest" % tot, bad == 0,
           "%d bad" % bad)
    bcheck("the finest level has m = 1 on all posets", bad_not_bottom == 0,
           "%d bad" % bad_not_bottom)

    sub("B4  lambda_2 (uniform-move weight) = max over incomparable pairs of s(x,y)")
    bad = tot = 0
    for n, recs in sorted(pop_by_n.items()):
        for r in recs:
            if r.is_chain:
                continue
            tot += 1
            if r.lam2 != r.s_max:
                bad += 1
    bcheck("0 bad of %d non-chain posets" % tot, bad == 0, "%d bad" % bad)
    print("       => the action's spectral gap is a PAIR statistic of exactly the same")
    print("          shape as delta: max over incomparable pairs of a per-pair number.")

    sub("B5  2-block levels are exactly {A, complement} with A a nontrivial order ideal or filter")
    bad = tot = 0
    for n, recs in sorted(pop_by_n.items()):
        lat = lats[n]
        for r in recs:
            ideals = set(order_ideals(r.P))
            full = (1 << n) - 1
            isl = set(r.levels)
            for i, blocks in enumerate(lat.parts):
                if len(blocks) != 2:
                    continue
                tot += 1
                A, B = blocks
                want = (A in ideals) or (B in ideals)
                if (i in isl) != want:
                    bad += 1
    bcheck("0 bad of %d 2-block partitions" % tot, bad == 0, "%d bad" % bad)

    sub("B6  PRIMITIVE  <==>  every 2-block level has strictly positive excess")
    print("    excess({A,A^c}) := e(P) - e(P|_A) e(P|_A^c) = sum of m_Y over levels Y")
    print("    that do NOT refine {A,A^c}.  Zero excess at some 2-block level == P is an")
    print("    ordinal sum there == the incomparability graph is disconnected.")
    bad_id = bad_eq = tot = tot_lv = 0
    for n, recs in sorted(pop_by_n.items()):
        lat = lats[n]
        for r in recs:
            e = restriction_counts(r.P)
            full = (1 << n) - 1
            refX = lat.refiners
            allpos = True
            for X in r.levels:
                if lat.nblocks[X] != 2:
                    continue
                A, B = lat.parts[X]
                if e[full] == e[A] * e[B]:
                    allpos = False
                # the excess equals the multiplicity mass NOT refining X.
                # refiners[X] is the list of Y that refine X, so "Y does not
                # refine X" is  Y not in refiners[X].
                below = set(refX[X])
                off = sum(r.mult[Y] for Y in r.levels if Y not in below)
                tot_lv += 1
                if off != e[full] - e[A] * e[B]:
                    bad_id += 1
            tot += 1
            if allpos != r.primitive:
                bad_eq += 1
    bcheck("excess identity: 0 bad of %d 2-block levels" % tot_lv, bad_id == 0,
           "%d bad" % bad_id)
    bcheck("PRIMITIVE <==> all-positive excess: 0 bad of %d posets" % tot,
           bad_eq == 0, "%d bad" % bad_eq)

    sub("B7  frozen (delta < 1/3) forces e(P) >= 4; and what the extremal posets do")
    print("    Proof: for an incomparable pair the two one-relation extension counts are")
    print("    positive integers summing to e(P), and min < e(P)/3 needs e(P) > 3.")
    for n, recs in sorted(pop_by_n.items()):
        pop = [r for r in recs if not r.is_chain]
        if not pop:
            continue
        dmin = min(r.delta for r in pop)
        ext = [r for r in pop if r.delta == dmin]
        print("    n=%d: min delta = %-6s over %d posets; e(P) on them: min %d max %d"
              % (n, fs(dmin), len(ext), min(r.e for r in ext), max(r.e for r in ext)))
    bcheck("no poset with delta < 1/3 found at any n tested (the conjecture holds here)",
           all(r.delta >= Fraction(1, 3) for recs in pop_by_n.values() for r in recs
               if not r.is_chain))
    print()
    print("    AND THIS IS A GENUINE CONSTRAINT, not a translation.  Most of the")
    print("    delta-extremal posets have e(P) = 3, but e(P) >= 4 is forced for anything")
    print("    frozen -- so IF a counterexample exists it does NOT resemble the extremal")
    print("    posets in the coordinate the multiplicity identity reads off, and the")
    print("    extremal posets are not near-misses there.  Counts:")
    for n, recs in sorted(pop_by_n.items()):
        pop = [r for r in recs if not r.is_chain]
        if not pop:
            continue
        dmin = min(r.delta for r in pop)
        ext = [r for r in pop if r.delta == dmin]
        n3 = sum(1 for r in ext if r.e == 3)
        print("        n=%d: %d of %d extremal posets have e(P) = 3 (below the frozen "
              "floor of 4)" % (n, n3, len(ext)))

    sub("B8  NO FREE LUNCH: delta is weight-invariant on the uniformising polytope,")
    print("    lambda_2 is not.  w_t = t.(do-nothing) + (1-t).(uniform on the FINEST")
    print("    moves) has the uniform distribution on L(P) as its stationary law for")
    print("    every t, and lambda_2(w_t) = t.")
    bad = tot = 0
    detail = []
    for n in sorted(pop_by_n):
        if n > 4:
            continue
        lat = lats[n]
        for r in pop_by_n[n]:
            if r.is_chain:
                continue
            les = linear_extensions(r.P)
            if len(les) > 24:
                continue
            N = len(les)
            pos = {w: k for k, w in enumerate(les)}
            finest = [tuple(1 << x for x in w) for w in les]
            donothing = (((1 << n) - 1),)
            for t in (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)):
                tot += 1
                M = [[Fraction(0)] * N for _ in range(N)]
                for w0 in les:
                    M[pos[act(donothing, w0)]][pos[w0]] += t
                for mv in finest:
                    for w0 in les:
                        M[pos[act(mv, w0)]][pos[w0]] += (1 - t) / N
                # uniform is stationary iff every row sums to 1
                if any(sum(row) != 1 for row in M):
                    bad += 1
                    detail.append("n=%d %s t=%s stationarity" % (n, r.cover, fs(t)))
                    continue
                # lambda_2 of w_t: levels other than the bottom all get exactly t
                lam2 = t if r.e > 1 else Fraction(0)
                lamX = {}
                for X in r.levels:
                    tot_p = Fraction(0)
                    if lat.top in lat.refiners[lat.top] and X in lat.refiners[lat.top]:
                        tot_p += t
                    if X in lat.refiners[lat.bottom]:
                        tot_p += (1 - t)
                    lamX[X] = tot_p
                cands = [lamX[X] for X in r.levels if r.mult[X] > 0 and X != lat.bottom]
                if (max(cands) if cands else Fraction(0)) != lam2:
                    bad += 1
                    detail.append("n=%d %s t=%s lambda2" % (n, r.cover, fs(t)))
    bcheck("0 bad of %d (poset, t) cases at n<=4" % tot, bad == 0, "; ".join(detail[:3]))
    print("       => delta(P) is the SAME for every weight in the polytope while")
    print("          lambda_2 sweeps (0,1).  No spectral quantity of a measure-correct")
    print("          walk can be a function of delta unless the weight is pinned by a")
    print("          rule outside the stationarity requirement.")

    sub("B9  the exact reformulation of the counterexample condition")
    print("    For any weight w whose walk has the uniform law on L(P) stationary,")
    print("    p(x<y) = q_w(x<y) / (q_w(x<y) + q_w(y<x)).  Hence:")
    print()
    print("      P is a counterexample  <==>  P is not a chain and for EVERY incomparable")
    print("      pair {x,y},  min(q_w, q'_w) < (1/3)(q_w + q'_w):  the moves that")
    print("      SEPARATE the pair are more than 2:1 lopsided.")
    print()
    print("    Checked on the canonical uniform-move weight: the identity")
    print("    pi = q/(q+q') is control C8; below, how far the uniform-move weight's own")
    print("    pi is from the conjecture's p (it is NOT a uniformising weight in general).")
    for n, recs in sorted(pop_by_n.items()):
        rows = [(pr, r) for r in recs if r.walkstats for pr in r.per_pair]
        if not rows:
            continue
        eq = 0
        worst = Fraction(0)
        for pr, r in rows:
            pi = r.walkstats[pr][3]
            if pi is None:
                continue
            d = abs(min(pi, 1 - pi) - r.per_pair[pr])
            worst = max(worst, d)
            if d == 0:
                eq += 1
        tot_pairs = sum(1 for pr, r in rows if r.walkstats[pr][3] is not None)
        print("    n=%d: %d of %d pairs have min(pi,1-pi) = min(p,1-p) exactly; "
              "worst gap %s" % (n, eq, tot_pairs, fs(worst)))
    print()
    print("    So the uniform-move weight -- the only canonical weight the action")
    print("    supplies without extra input -- does NOT reproduce the conjecture's pair")
    print("    marginals.  That is the honest statement of the obstruction.")


# --------------------------------------------------------------------------

def section7_isoperimetry(pop_by_n):
    hr("SECTION 7  THE ISOPERIMETRIC QUESTION -- stated as a question, with the")
    print("            argument actually available, and its gap named.")
    print()
    print("THE QUESTION.  IF a counterexample P exists, its uniform measure on L(P) has")
    print("E[inv(L,L*)] < |Inc(P)|/3, while being supported on all e(P) chambers of the")
    print("adjacent-transposition graph, whose degree is at most n-1.  Does 'most of the")
    print("mass in a small inversion-ball, but spread over many chambers of a")
    print("bounded-degree graph' force a contradiction?")
    print()
    print("THE ARGUMENT I ACTUALLY HAVE, AND IT IS NOT ENOUGH.  Unconditionally, only")
    print("Markov applies: Pr[inv >= t |Inc|/3] <= 1/t, so at least half the mass lies")
    print("within inv < 2|Inc|/3.  With |Inc| <= n(n-1)/2 that radius is up to n(n-1)/3,")
    print("which is 2/3 of the maximum possible inversion count -- not a small ball.  The")
    print("count of permutations with fewer than that many inversions is a constant")
    print("fraction of n!, so no counting contradiction follows.  Numbers on the actual")
    print("population, to show the radius really is that loose:")
    print()
    print("%-4s %-30s %10s %12s %14s" %
          ("n", "poset", "|Inc|/3", "Markov r", "Pr[inv < r]"))
    for n, recs in sorted(pop_by_n.items()):
        if n > 6:
            continue
        pop = [r for r in recs if not r.is_chain and r.br.Lstar is not None]
        if not pop:
            continue
        dmin = min(r.delta for r in pop)
        show = sorted([r for r in pop if r.delta == dmin], key=lambda r: r.cover)[:1]
        show += sorted(pop, key=lambda r: (-r.e, r.cover))[:1]
        for r in show:
            rad = Fraction(2 * r.br.ninc, 3)
            bm = r.br.ball_mass(rad)
            print("%-4d %-30s %10s %12s %14s"
                  % (n, r.cover[:30], fs(Fraction(r.br.ninc, 3)), fs(rad), fs(bm)))
    print()
    print("WHAT WOULD BE NEEDED, AND WHERE IT ALREADY LIVES.  To shrink the radius from")
    print("Markov's 2|Inc|/3 to something like c|Inc| with c small, one needs a")
    print("concentration inequality for inv(L,L*) under the linear-extension measure --")
    print("the |Inc| pair-indicators are not independent, and their correlation structure")
    print("is exactly the FKG/XYZ same-side-covariance obstruction already recorded in")
    print("STATE.md as the (B-cov) half of the open (B) obligation.  So this question")
    print("does not open a new route: it REDUCES to an obligation the ledger already")
    print("carries as open.  It is written down here as a question with its gap named,")
    print("and it is NOT offered as a route.")


def main():
    hr("mg-24a3  --  A 1/3-2/3 COUNTEREXAMPLE UNDER THE SEMIGROUP ACTION")
    print("Populations, methods and null models are stated inline.  No claim here")
    print("depends on a random choice except the permutation p-values, which use")
    print("seed %d.  All spectra and all balance statistics are EXACT rationals." % SEED)
    print()
    print("Reminder of the definitions in use (see core.py and bridge.py docstrings):")
    print("  delta(P) = max over incomparable pairs {x,y} of min(p, 1-p), p = Pr[x<y]")
    print("             over the UNIFORM distribution on linear extensions.")
    print("  A COUNTEREXAMPLE is a non-chain with delta(P) < 1/3.  NONE IS KNOWN, and")
    print("  none exists at any size below.  Every statement about a counterexample is")
    print("  of the form 'IF one exists THEN ...'.  Where the worst-balanced posets are")
    print("  used they are a stated PROXY for one, and never called one.")

    lats = {}
    pop = {}
    prev = [Poset(1, [])]
    summary = []
    pairsum = []
    for n in range(2, NMAX + 1):
        posets = all_posets_by_extension(n, prev)
        prev = posets
        if n < 3:
            continue
        lats[n] = PartitionLattice(n)
        want = (n <= NMAX_FULL)
        recs = [build(P, lats[n], want) for P in posets]
        pop[n] = recs
        sys.stdout.flush()

    section1_bridge(pop)
    sys.stdout.flush()
    section2_facebalance(pop, random.Random(SEED))
    sys.stdout.flush()
    section2_quotient(pop, lats)
    sys.stdout.flush()
    part_b(pop, lats)
    sys.stdout.flush()

    hr("SECTION 5  SPECTRAL SEPARATION (the brief's original (a)) -- SECONDARY")
    print("The ADDENDUM calls a search for spectral separation a fishing expedition, and")
    print("it is right that nothing here predicts which invariant should move.  It is")
    print("reported in full anyway, because a clean quantified NULL is a deliverable: it")
    print("closes the route cheaply rather than leaving it open and unmeasured.")
    for n in sorted(pop):
        s = analyse_detection(n, pop[n], random.Random(SEED), n <= NMAX_FULL)
        if s:
            summary.append(s)
        if n <= NMAX_FULL:
            ps = analyse_pairs(n, pop[n], random.Random(SEED))
            if ps:
                pairsum.append(ps)
        sys.stdout.flush()

    section7_isoperimetry(pop)

    hr("SECTION 6  TREND: does the separation sharpen or wash out as n grows?")
    print("%-4s %-22s %6s %8s %10s %10s %10s" %
          ("n", "population", "N", "min d", "I1 %sing", "I3 %sing", "I4 %sing"))
    for s in summary:
        print("%-4d %-22s %6d %8s %9.1f%% %9.1f%% %9.1f%%"
              % (s["n"], s["gname"], s["N"], fs(s["dmin"]),
                 100 * s["single"].get("I1", 0), 100 * s["single"].get("I3", 0),
                 100 * s["single"].get("I4", 0)))
    print()
    print("%-4s %10s %10s %12s %14s" %
          ("n", "#extremal", "I4 collide", "witnesses", "argmax agree"))
    for s in summary:
        pa = next((p for p in pairsum if p["n"] == s["n"]), None)
        print("%-4d %10d %10d %12d %13s"
              % (s["n"], s["ext"], s["i4_bad"], s["nwit"],
                 ("%.1f%%" % (100 * pa["argmax_agree"])) if pa else "-"))
    print()
    print("%-4s %14s %14s" % ("n", "rho(delta,pi)", "rho(delta,s)"))
    for p in pairsum:
        print("%-4d %14.4f %14.4f" % (p["n"], p["rho_pi"], p["rho_s"]))
    print()
    print("AND THE TREND THAT MATTERS -- the ADDENDUM's concentration bound:")
    print("%-4s %10s %10s %12s %12s" %
          ("n", "min 3delta", "min R", "%pop R<1", "slack min R"))
    for n in sorted(pop):
        grp = [r for r in pop[n] if not r.is_chain]
        if not grp:
            continue
        mR = min(r.br.R for r in grp)
        print("%-4d %10s %10s %11.1f%% %12.4f"
              % (n, fs(min(3 * r.delta for r in grp)), fs(mR),
                 100.0 * sum(1 for r in grp if r.br.R < 1) / len(grp), float(1 - mR)))
    print()
    print("min 3delta is pinned at 1 (the conjecture is TIGHT and unviolated at every n")
    print("reached).  min R falls away from 1 monotonically over the range, and the share")
    print("of the population meeting the concentration bound rises.  The bound loosens")
    print("as n grows; it does not sharpen.")

    hr("CONTROL STATUS")
    if BFAIL:
        print("STRUCTURAL CHECKS FAILED: %s" % ", ".join(BFAIL))
        return 1
    print("all structural checks in (b) pass; run selftest.py for the instrument controls")
    return 0


if __name__ == "__main__":
    sys.exit(main())
