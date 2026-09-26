"""flp.py (mg-785e): FLOAT LP for probing only (scipy/HiGHS, from a scratch venv; not needed to reproduce
any certificate).  Every claimed refutation is re-certified EXACTLY by xlp.py (Fractions) on the rows that
the float dual marks active (certify()).
solve(M, eps, free_eps=True): max eps; returns (value or None, x, duals)."""
from fractions import Fraction as F

def solve(M, eps, free_eps=True):
    import numpy as np
    from scipy.optimize import linprog
    from scipy.sparse import lil_matrix
    nv = M.nv
    Aub, bub, Aeq, beq, idx_ub, idx_eq = [], [], [], [], [], []
    for r, (coef, sense, rhs) in enumerate(M.rows):
        if sense == '<=': Aub.append(coef); bub.append(float(rhs)); idx_ub.append(r)
        elif sense == '>=': Aub.append({k: -v for k, v in coef.items()}); bub.append(-float(rhs)); idx_ub.append(r)
        else: Aeq.append(coef); beq.append(float(rhs)); idx_eq.append(r)
    def mat(rows):
        A = lil_matrix((len(rows), nv))
        for i, c in enumerate(rows):
            for k, v in c.items(): A[i, k] = float(v)
        return A.tocsr()
    c = np.zeros(nv); c[eps] = -1
    bounds = [(0, None)] * nv
    if free_eps: bounds[eps] = (-1, None)
    res = linprog(c, A_ub=mat(Aub) if Aub else None, b_ub=bub or None, A_eq=mat(Aeq) if Aeq else None,
                  b_eq=beq or None, bounds=bounds, method='highs')
    if res.status == 2: return None, None, None
    duals = {}
    for i, r in enumerate(idx_ub): duals[r] = res.ineqlin.marginals[i]
    for i, r in enumerate(idx_eq): duals[r] = res.eqlin.marginals[i]
    return -res.fun, res.x, duals

def certify(M, eps, rows):
    """exact: is the subsystem `rows` (with eps >= 0 implicit, xlp vars >= 0) infeasible or eps* <= 0?"""
    import xlp
    st, val, x = xlp.solve(M.nv, [M.rows[r] for r in rows], {eps: 1})
    return st, val
