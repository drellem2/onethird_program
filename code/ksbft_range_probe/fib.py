"""fib.py -- exact analysis of the finite Fibonacci posets (mg-2912).

F on {x_i}: x_i < x_j iff j - i >= 2.  The paper's F_m is the restriction to
{x_{-m},...,x_m} (N = 2m+1 elements); we also report even N.  Elements are
indexed 0..N-1 here (paper index i = our index - m for odd N).
Everything exact (exact.py dp); the float columns are for reading only.
"""
import sys
from fractions import Fraction
from math import sqrt
import exact

def fib(k):
    a, b = 0, 1
    for _ in range(k):
        a, b = b, a + b
    return a

def fib_poset(N):
    return [sum(1 << i for i in range(j - 1)) for j in range(N)]

C = (5 - sqrt(5)) / 10
PHI2 = (3 - sqrt(5)) / 2
def main():
    NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 41
    print(f"C_BFT={C:.9f}  (3-sqrt5)/2={PHI2:.9f}")
    print(" N  e(F_N)        delta(F_N)          attained-by          M            M-at  "
          "centre-adjacent  end-adjacent  sort=index  paper-h-formula")
    for N in range(3, NMAX + 1):
        down = fib_poset(N)
        r = exact.analyse(down)
        ordr = r["ord"]
        sort_is_index = ordr == list(range(N))
        c = (N - 1) // 2
        centre = exact.bal(r, down, c - 1, c) if N % 2 == 0 else exact.bal(r, down, c, c + 1)
        end = exact.bal(r, down, N - 2, N - 1)
        Mat = [i + 1 for i, t in enumerate(r["d"]) if abs(t) == r["M"]]
        # paper p.13: h(x_i) - (m+i+1) = F_{2|i|}/F_{2m+2}  (odd N = 2m+1, i = idx - m)
        paper = ""
        if N % 2 == 1:
            m = (N - 1) // 2
            okabs = all(abs(r["h"][k] - (k + 1)) == Fraction(fib(2 * abs(k - m)), fib(2 * m + 2)) for k in range(N))
            oksgn = all(r["h"][k] - (k + 1) == Fraction(fib(2 * abs(k - m)), fib(2 * m + 2)) for k in range(N))
            # corrected (this probe): d(x_i) = sgn(-i) * (-1)^(m-|i|) * F_{2|i|}/F_{2m+2}
            def sg(k):
                i = k - m
                return (1 if i < 0 else -1 if i > 0 else 0) * (-1) ** (m - abs(i))
            okcor = all(r["h"][k] - (k + 1) == sg(k) * Fraction(fib(2 * abs(k - m)), fib(2 * m + 2)) for k in range(N))
            paper = f"abs:{'OK' if okabs else 'NO'} signed:{'OK' if oksgn else 'NO'} corrected:{'OK' if okcor else 'NO'}"
        pairs = r["pairs"]
        print(f"{N:3d} {r['e']:<13d} {str(r['delta']):>18s}={float(r['delta']):.6f} "
              f"{str(pairs[:3]):20s} {float(r['M']):.9f} {str(Mat):6s} {float(centre):.6f}        "
              f"{float(end):.6f}      {sort_is_index}       {paper}")


if __name__ == "__main__":
    main()
