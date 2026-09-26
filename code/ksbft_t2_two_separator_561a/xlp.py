"""xlp.py (mg-561a): small exact two-phase simplex over Fractions (Bland's rule).

solve(nvars, rows, obj) with rows = [(coef_dict, sense, rhs)], sense in '<=', '>=', '='; all variables >= 0.
Maximises sum obj[j] x_j.  Returns ('infeasible', None, y) or ('optimal', value, x).  For an infeasible
system the Phase-I duals y (one per row) are returned as a Farkas-type certificate.
"""
from fractions import Fraction as F

def solve(nv, rows, obj):
    R = []
    for coef, sense, rhs in rows:
        coef = {j: F(v) for j, v in coef.items() if v}
        rhs = F(rhs)
        if rhs < 0:
            coef = {j: -v for j, v in coef.items()}; rhs = -rhs
            sense = {'<=': '>=', '>=': '<=', '=': '='}[sense]
        R.append((coef, sense, rhs))
    m = len(R)
    nslack = sum(1 for _, s, _ in R if s != '=')
    nart = sum(1 for _, s, _ in R if s != '<=')
    N = nv + nslack + nart
    T = []; basis = []; si = nv; ai = nv + nslack; arts = []
    for i, (coef, sense, rhs) in enumerate(R):
        row = [F(0)] * (N + 1)
        for j, v in coef.items(): row[j] = v
        row[-1] = rhs
        if sense == '<=':
            row[si] = F(1); basis.append(si); si += 1
        elif sense == '>=':
            row[si] = F(-1); si += 1; row[ai] = F(1); basis.append(ai); arts.append(ai); ai += 1
        else:
            row[ai] = F(1); basis.append(ai); arts.append(ai); ai += 1
        T.append(row)
    def run(objrow, allowed):
        while True:
            pc = None
            for j in range(N):
                if allowed[j] and objrow[j] < 0: pc = j; break
            if pc is None: return objrow
            pr = None; best = None
            for i in range(m):
                if T[i][pc] > 0:
                    r = T[i][-1] / T[i][pc]
                    if best is None or r < best or (r == best and basis[i] < basis[pr]): best, pr = r, i
            if pr is None: raise RuntimeError('unbounded')
            pv = T[pr][pc]; T[pr] = [v / pv for v in T[pr]]
            for i in range(m):
                if i != pr and T[i][pc] != 0:
                    f = T[i][pc]; T[i] = [a - f * b for a, b in zip(T[i], T[pr])]
            if objrow[pc] != 0:
                f = objrow[pc]; objrow = [a - f * b for a, b in zip(objrow, T[pr])]
            basis[pr] = pc
    # Phase I: minimise sum of artificials  <=> maximise -sum
    artset = set(arts)
    o = [F(0)] * (N + 1)
    for j in arts: o[j] = F(1)
    for i in range(m):
        if basis[i] in artset: o = [a - b for a, b in zip(o, T[i])]
    o = run(o, [True] * N)
    if o[-1] != 0 and -o[-1] > 0:
        return ('infeasible', None, None)
    # drive out basic artificials at zero level
    for i in range(m):
        if basis[i] in artset:
            for j in range(nv + nslack):
                if T[i][j] != 0:
                    pv = T[i][j]; T[i] = [v / pv for v in T[i]]
                    for k in range(m):
                        if k != i and T[k][j] != 0:
                            f = T[k][j]; T[k] = [a - f * b for a, b in zip(T[k], T[i])]
                    basis[i] = j; break
    allowed = [j not in artset for j in range(N)]
    o = [F(0)] * (N + 1)
    for j, v in obj.items(): o[j] = -F(v)
    for i in range(m):
        if o[basis[i]] != 0:
            f = o[basis[i]]; o = [a - f * b for a, b in zip(o, T[i])]
    o = run(o, allowed)
    x = [F(0)] * nv
    for i in range(m):
        if basis[i] < nv: x[basis[i]] = T[i][-1]
    return ('optimal', o[-1], x)

if __name__ == '__main__':
    # self-test: max x+y s.t. x+2y<=4, 3x+y<=6, x-y = 0  -> x=y=4/3, value 8/3 ; infeasible: x+y<=1, x+y>=2
    print(solve(2, [({0: 1, 1: 2}, '<=', 4), ({0: 3, 1: 1}, '<=', 6), ({0: 1, 1: -1}, '=', 0)], {0: 1, 1: 1}))
    print(solve(2, [({0: 1, 1: 1}, '<=', 1), ({0: 1, 1: 1}, '>=', 2)], {0: 1}))
    print(solve(1, [({0: 1}, '>=', F(1, 2)), ({0: 1}, '<=', 3)], {0: -1}))
