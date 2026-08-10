"""a0 -- the instrument is checked BEFORE it is pointed at the claim.

Two things are established here and nothing else:

  S0  INDEPENDENCE.  This audit imports none of lib5cba / lib789d / libc50b.  Checked
      on the source text of every file in this directory AND on `sys.modules` after
      the whole suite has been imported, because a text grep alone cannot see an
      import performed through `importlib` or a path insertion.

  S1  THE DEVICES DECIDE, in both directions, on matrices whose answer is known
      independently of this arc.  A certifier that says COPOSITIVE to everything
      would confirm the claim under audit just as loudly as a correct one; the
      Horn matrix is the control that separates them, being copositive while NOT
      expressible as PSD + entrywise-nonnegative, so a routine that tests only the
      easy sufficient condition fails it.
"""
import os
import sys
import glob
from fractions import Fraction as Fr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib5e82 as L

FORBIDDEN = ("lib5cba", "lib789d", "libc50b")
ok_all = True


def check(label, got, want):
    global ok_all
    good = got == want
    ok_all = ok_all and good
    print("  [%s] %-64s got=%s want=%s" % ("ok " if good else "FAIL", label, got, want))


print("=" * 78)
print("S0  INDEPENDENCE OF THE INSTRUMENT")
print("=" * 78)
here = os.path.dirname(os.path.abspath(__file__))


def module_bindings(src):
    """Every module name this source could bind, read off the PARSE TREE.

    My first version of this arm grepped the source text for lines containing both
    "import" and a forbidden name.  It went RED on its own docstring -- the sentence
    "This audit imports none of lib5cba / lib789d / libc50b" contains both -- which is
    mg-a0d6's D6 committed a second time, inside an audit of instruments that agree
    with themselves.  A text scan cannot tell a claim from a binding.  `ast` can:
    prose is not a node, and a comment is not a node, so only real imports and real
    dynamic-import CALLS are reported.
    """
    import ast

    names, tree = [], ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            names.append(node.module or "")
        elif isinstance(node, ast.Call):
            fn = node.func
            label = getattr(fn, "attr", None) or getattr(fn, "id", None)
            if label in ("import_module", "__import__", "exec", "eval", "load_module"):
                for a in node.args:
                    if isinstance(a, ast.Constant) and isinstance(a.value, str):
                        names.append(a.value)
                    else:
                        names.append("<DYNAMIC:%s>" % label)
    return names


for path in sorted(glob.glob(os.path.join(here, "*.py"))):
    bound = module_bindings(open(path).read())
    hits = [nm for nm in bound if any(f in nm for f in FORBIDDEN)]
    dyn = [nm for nm in bound if nm.startswith("<DYNAMIC")]
    check("no import of the audited libraries in %s" % os.path.basename(path), hits, [])
    check("  ... and no dynamic import to hide one in %s" % os.path.basename(path), dyn, [])
print("  sys.modules carrying a forbidden name:",
      [m for m in sys.modules if any(f in m for f in FORBIDDEN)])
check("sys.modules clean", [m for m in sys.modules if any(f in m for f in FORBIDDEN)], [])

print()
print("=" * 78)
print("S1  THE DEVICES, ON MATRICES WHOSE ANSWER IS KNOWN OUTSIDE THIS ARC")
print("=" * 78)

I3 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
check("I is PSD", L.is_psd(I3), True)
check("I is copositive", L.is_copositive(I3), True)
check("diag(1,-1) is NOT PSD", L.is_psd([[1, 0], [0, -1]]), False)
check("diag(1,-1) is NOT copositive", L.is_copositive([[1, 0], [0, -1]]), False)

# entrywise nonnegative => copositive, but NOT PSD here
NN = [[0, 1], [1, 0]]
check("[[0,1],[1,0]] copositive (entrywise >= 0)", L.is_copositive(NN), True)
check("[[0,1],[1,0]] NOT PSD", L.is_psd(NN), False)

# PSD => copositive, and this one is singular
SG = [[1, -1], [-1, 1]]
check("[[1,-1],[-1,1]] PSD (singular)", L.is_psd(SG), True)
check("[[1,-1],[-1,1]] copositive", L.is_copositive(SG), True)

# not copositive, off-diagonal too negative
NC = [[1, -2], [-2, 1]]
check("[[1,-2],[-2,1]] NOT copositive", L.is_copositive(NC), False)
w = L.not_copositive_witness(NC)
check("  ... and the witness is >= 0", all(x >= 0 for x in w), True)
check("  ... and c'Rc < 0", L.quad(NC, w) < 0, True)

# THE CONTROL THAT MATTERS.  Horn's matrix: copositive, and NOT PSD + nonnegative.
HORN = [
    [1, -1, 1, 1, -1],
    [-1, 1, -1, 1, 1],
    [1, -1, 1, -1, 1],
    [1, 1, -1, 1, -1],
    [-1, 1, 1, -1, 1],
]
check("Horn matrix IS copositive", L.is_copositive(HORN), True)
check("Horn matrix is NOT PSD", L.is_psd(HORN), False)
check("Horn has negative entries (so not the trivial nonneg case)",
      any(HORN[i][j] < 0 for i in range(5) for j in range(5)), True)
# Horn minus a hair on the diagonal stops being copositive: the routine is not
# saying "yes" out of habit.
HORN_M = [row[:] for row in HORN]
HORN_M[0][0] = Fr(9, 10)
check("Horn with R[0][0]=9/10 is NOT copositive", L.is_copositive(HORN_M), False)

print()
print("=" * 78)
print("S2  THE FOURIER-MOTZKIN ENGINE, DIRECTLY")
print("=" * 78)
# y = y0 + Z t < 0 ?   hand-made cases, answer obvious by inspection.
check("y0=(-1,-1), no free vars -> feasible",
      L._strictly_negative_point_exists([Fr(-1), Fr(-1)], [[], []]), True)
check("y0=(-1, 1), no free vars -> infeasible",
      L._strictly_negative_point_exists([Fr(-1), Fr(1)], [[], []]), False)
# t free: y = (-1 + t, -1 - t).  Both < 0 iff -1 < t < 1.  Feasible.
check("y=(-1+t, -1-t) -> feasible",
      L._strictly_negative_point_exists([Fr(-1), Fr(-1)], [[Fr(1)], [Fr(-1)]]), True)
# y = (1 + t, 1 - t).  Need t < -1 and t > 1.  Infeasible.
check("y=(1+t, 1-t) -> infeasible",
      L._strictly_negative_point_exists([Fr(1), Fr(1)], [[Fr(1)], [Fr(-1)]]), False)
# y = (t, -t): need t<0 and t>0.  Infeasible (STRICTNESS is the whole point: t=0
# satisfies both non-strictly).
check("y=(t,-t) -> infeasible (strictness)",
      L._strictly_negative_point_exists([Fr(0), Fr(0)], [[Fr(1)], [Fr(-1)]]), False)

# a singular face, exercised end to end: R_S rank-deficient and consistent
SINGFACE = [[1, 1, 0], [1, 1, 0], [0, 0, 1]]
L.reset_counters()
res = L.is_copositive(SINGFACE)
check("[[1,1,0],[1,1,0],[0,0,1]] copositive", res, True)
check("  ... and singular faces were SEEN", L.SINGULAR_FACES > 0, True)
check("  ... and every one was DECIDED", L.SINGULAR_FACES_DECIDED, L.SINGULAR_FACES)

print()
print("=" * 78)
print("S3  THE LINEAR-EXTENSION GENERATOR IS COMPLETE, BY BRUTE FORCE AT n <= 7")
print("=" * 78)
# a1 checks that every sequence the generator produces IS a linear extension.  That
# says nothing about whether one was MISSED, and a generator that quietly drops
# extensions would lower LE and move Delta, M, gamma and mu_pref with it.  Here the
# generator is compared against filtering ALL n! permutations, on every naturally
# labelled poset at n <= 6 and a sample at n = 7.
from itertools import permutations


def gen_posets(n):
    if n == 0:
        yield ()
        return
    for dn in gen_posets(n - 1):
        for D in range(1 << (n - 1)):
            m, good = D, True
            while m:
                i = (m & -m).bit_length() - 1
                m &= m - 1
                if dn[i] & ~D:
                    good = False
                    break
            if good:
                yield dn + (D,)


def brute(dn, n):
    out = []
    for p in permutations(range(n)):
        if all(p.index(i) < p.index(j) for j in range(n) for i in L.bits(dn[j])):
            out.append(p)
    return sorted(out)


tot = bad = 0
for n in range(1, 7):
    for dn in gen_posets(n):
        tot += 1
        if sorted(L.linear_extensions(dn, n)) != brute(dn, n):
            bad += 1
check("generator == brute force at every naturally labelled poset, n <= 6 (%d posets)" % tot,
      bad, 0)
n7 = list(gen_posets(7))
sample = n7[::373]          # a fixed stride, so this is reproducible and not a draw
bad7 = sum(1 for dn in sample if sorted(L.linear_extensions(dn, 7)) != brute(dn, 7))
check("generator == brute force at %d of %d posets at n = 7 (stride 373)"
      % (len(sample), len(n7)), bad7, 0)

print()
print("=" * 78)
print("VERDICT: %s" % ("ALL ARMS SATISFACTORY" if ok_all else "*** AN ARM FAILED ***"))
print("=" * 78)
sys.exit(0 if ok_all else 1)
