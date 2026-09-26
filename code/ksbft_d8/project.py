#!/usr/bin/env python3
"""project.py (mg-c493) -- D = 8 cost projection from the measured D = 4..7 runs.

Inputs (all committed transcripts):
  ../ksbft_finite_state/out_d1to5.txt, out_d6.txt, out_d7.txt   tree per-depth node counts (mg-e8b4)
  out_keystat_d{3,4,5,6}.txt                                    distinct future keys, full trees (this ticket)
  out_keystat_d7_slices.txt, out_keystat_d6_slices.txt          the same on 2 split slices each
Model: log10(nodes) quadratic in D, least squares over D = 4..7 (4 points,
3 parameters; the residuals are printed).  Everything here is EMPIRICAL
extrapolation; nothing is a bound on D = 8.
"""
import re, math, os
H = os.path.dirname(os.path.abspath(__file__)); FS = os.path.join(H, "..", "ksbft_finite_state")


def depth_counts(path, D=None):
    txt = open(path).read()
    if D is not None:   # out_d1to5.txt holds several runs: take the block of the full D run
        blocks = re.split(r"(?=# D=\d+ MAXDEPTH)", txt)
        txt = [b for b in blocks if b.startswith("# D=%d MAXDEPTH" % D)][0]
        txt = txt.split("==")[0]
    out = {}
    for line in txt.splitlines():
        t = line.split()
        if t and t[0] == "depth":
            out[int(t[1])] = int(t[3]) if t[2] == "nodes" else int(t[2])   # tree.c vs aggregate.py layouts
    return out


tree = {4: depth_counts(os.path.join(FS, "out_d1to5.txt"), 4), 5: depth_counts(os.path.join(FS, "out_d1to5.txt"), 5),
        6: depth_counts(os.path.join(FS, "out_d6.txt")), 7: depth_counts(os.path.join(FS, "out_d7.txt"))}
tot = {D: sum(v.values()) for D, v in tree.items()}
assert tot == {4: 4758, 5: 235851, 6: 18169307, 7: 2181780336}, tot


def keystat(path):
    """list of (nodes, M, S, X) totals per run in the file"""
    runs = []; cur = None
    for line in open(path):
        if line.startswith("# keystat"):
            cur = [0, 0, 0, 0]; runs.append(cur)
        m = re.match(r"keys\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)", line)
        if m:
            for i in range(4): cur[i] += int(m.group(2 + i))
    return runs


def fit(xs, ys):   # least-squares quadratic
    import itertools
    n = len(xs); S = [[sum(x ** (i + j) for x in xs) for j in range(3)] for i in range(3)]
    b = [sum(y * x ** i for x, y in zip(xs, ys)) for i in range(3)]
    # solve 3x3
    A = [row[:] + [bb] for row, bb in zip(S, b)]
    for i in range(3):
        p = max(range(i, 3), key=lambda r: abs(A[r][i])); A[i], A[p] = A[p], A[i]
        for r in range(3):
            if r != i:
                f = A[r][i] / A[i][i]; A[r] = [a - f * c for a, c in zip(A[r], A[i])]
    return [A[i][3] / A[i][i] for i in range(3)]


print("# D=8 projection (mg-c493).  EMPIRICAL extrapolation from D=4..7; not a bound.")
print("# 1. tree node totals (mg-e8b4 transcripts)")
for D in sorted(tot):
    print("   D=%d  nodes %14d%s" % (D, tot[D], "" if D == 4 else "   growth x%.1f" % (tot[D] / tot[D - 1])))
Ds = sorted(tot); ys = [math.log10(tot[D]) for D in Ds]
c = fit(Ds, ys)
res = [y - (c[0] + c[1] * D + c[2] * D * D) for D, y in zip(Ds, ys)]
N8 = 10 ** (c[0] + 8 * c[1] + 64 * c[2])
print("   quadratic fit log10(nodes) = %.4f %+.4f D %+.4f D^2 ; residuals %s" % (c[0], c[1], c[2], " ".join("%+.3f" % r for r in res)))
print("   -> D=8 tree nodes ~ %.2e  (growth x%.0f over D=7)" % (N8, N8 / tot[7]))
# leave-one-out spread: fit on the three-point sub-sets that contain D=7 and extrapolate by the growth-ratio rule
g = [tot[D] / tot[D - 1] for D in (5, 6, 7)]
alt = tot[7] * g[-1] * (g[-1] / g[-2])
print("   ratio-of-ratios rule (x%.2f per step, mg-e8b4's method) -> %.2e" % (g[-1] / g[-2], alt))

print("# 2. share of nodes at depth <= 2D-1 (PROVEN floor for any window-keyed merge: the window is the whole prefix there)")
fl = {}
for D in Ds:
    fl[D] = sum(v for d, v in tree[D].items() if d <= 2 * D - 1) / tot[D]
    print("   D=%d  %.3f" % (D, fl[D]))
cf = fit(Ds, [fl[D] for D in Ds]); fl8 = cf[0] + 8 * cf[1] + 64 * cf[2]
lin = fl[7] + (fl[7] - fl[6])
print("   -> D=8 share: quadratic %.3f, linear from D=6,7 %.3f; used: min = %.3f" % (fl8, lin, min(fl8, lin)))
fl8 = min(fl8, lin)

print("# 3. distinct future keys / tree nodes (full trees; keystat)")
fr = {}
for D in (3, 4, 5, 6):
    n, M, S, X = keystat(os.path.join(H, "out_keystat_d%d.txt" % D))[0]
    assert n == (tot[D] if D in tot else n)
    fr[D] = (M / n, S / n, X / n)
    print("   D=%d  nodes %10d  M %.4f  S %.4f  X %.4f   (max merge speed-up: M x%.3f, S x%.3f, X x%.3f)" % (D, n, M / n, S / n, X / n, n / M, n / S, n / X))
print("#    per-slice (distinct counted inside one slice only: over-states the fractions)")
for tag, f in (("D=6", "out_keystat_d6_slices.txt"), ("D=7", "out_keystat_d7_slices.txt")):
    for n, M, S, X in keystat(os.path.join(H, f)):
        print("   %s slice  nodes %10d  M %.4f  S %.4f  X %.4f" % (tag, n, M / n, S / n, X / n))

print("# 4. D=8 cost lines (per-node cost: see doc §4; 9.0 us at D=7 measured by mg-e8b4, taken as a floor for D=8)")
us = 9.0e-6
for name, share in (("tree (mg-e8b4)", 1.0),
                    ("exact-key memo DP (X, D=6 share)", fr[6][2]),
                    ("ideal structural merge (S, D=6 share)", fr[6][1]),
                    ("any window-keyed merge, M floor (D=6 share)", fr[6][0]),
                    ("any window-keyed merge, PROVEN floor (depth<=2D-1 share)", fl8)):
    print("   %-58s nodes %.2e   core-hours %7.0f" % (name, N8 * share, N8 * share * us / 3600))
print("   target: 20 core-hours = %.1e nodes at 9.0 us" % (20 * 3600 / us))
