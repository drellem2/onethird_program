"""Exact rational LP feasibility:  does there exist x >= 0 with A x = b ?

Phase-I simplex with Bland's rule (so it terminates), all arithmetic in
Fraction.  Returns (feasible, x) with x an exact rational certificate when
feasible.  Used to DECIDE the cases §9.4 of the deliverable leaves undecided.
"""

from fractions import Fraction


def feasible(A, b):
    m = len(A)
    k = len(A[0]) if m else 0
    A = [[Fraction(v) for v in row] for row in A]
    b = [Fraction(v) for v in b]
    # make b >= 0
    for i in range(m):
        if b[i] < 0:
            b[i] = -b[i]
            A[i] = [-v for v in A[i]]
    # tableau: [A | I] with artificial variables, minimise sum of artificials
    n = k + m
    T = [A[i] + [Fraction(1 if j == i else 0) for j in range(m)] + [b[i]]
         for i in range(m)]
    basis = [k + i for i in range(m)]
    # objective row = -sum of rows (cost of artificials driven to zero)
    obj = [Fraction(0)] * (n + 1)
    for i in range(m):
        for j in range(n + 1):
            obj[j] -= T[i][j]
    for j in range(k, n):
        obj[j] += 1          # artificials have cost 1, already basic

    while True:
        # Bland: smallest index with negative reduced cost
        piv = -1
        for j in range(n):
            if obj[j] < 0:
                piv = j
                break
        if piv < 0:
            break
        # ratio test, Bland tie-break on basis index
        row = -1
        best = None
        for i in range(m):
            if T[i][piv] > 0:
                r = T[i][n] / T[i][piv]
                if best is None or r < best or (r == best and basis[i] < basis[row]):
                    best = r
                    row = i
        if row < 0:
            return False, None          # unbounded phase-I: cannot happen
        pv = T[row][piv]
        T[row] = [v / pv for v in T[row]]
        for i in range(m):
            if i != row and T[i][piv] != 0:
                f = T[i][piv]
                T[i] = [T[i][j] - f * T[row][j] for j in range(n + 1)]
        if obj[piv] != 0:
            f = obj[piv]
            obj = [obj[j] - f * T[row][j] for j in range(n + 1)]
        basis[row] = piv

    if -obj[n] > 0:
        return False, None
    x = [Fraction(0)] * k
    for i in range(m):
        if basis[i] < k:
            x[basis[i]] = T[i][n]
    return True, x
