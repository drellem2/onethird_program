"""mg-8311 R3 — THE RULING, and the census that has to precede it.

The ticket is explicit: "Do not assume the definition wins because it is the definition -- if
the convention is load-bearing somewhere, say where. State the ruling explicitly before
changing code."

So this script does three things, in this order:

  R3.1  the POSITIVE argument for the definition: it is the quantity the corpus's own matrix
        identity computes. <1_A, (I - S_P) 1_A> = E|A\\sigma(A)| for the definition, and the
        identical test against the convention. S_P is built here from its definition; no
        eigenvalue is taken and lib76b2 is not imported.

  R3.2  the CENSUS of call sites, by PARSING the source with `ast` rather than grepping it.
        mg-4d3b's audit recorded a source census that read the auditor's own PROSE as CODE.
        A grep for `phi_star` matches this docstring. An AST walk cannot.

  R3.3  the LOAD-BEARING test, which is the one the ticket actually asks for: is there any
        published assertion of mg-2de0 that is TRUE under the convention and FALSE under
        the definition? If yes, the convention is load-bearing and the ruling is not
        automatic. Measured, not assumed.

OPERATOR SCOPE: leak counts and one matrix quadratic form. lambda_std is never computed;
S_P appears only as a matrix whose quadratic form is compared against a combinatorial count.
Transport axis. Not Delta_AT, not A(P), not Hodge.
"""

import ast
import os
import sys
from fractions import Fraction as F

from lib8311 import all_posets_8311, antichain, S_P, quad_form_I_minus_S, Tally

T = Tally()
HERE = os.path.dirname(os.path.abspath(__file__))
LIB2DE0_DIR = os.path.join(os.path.dirname(HERE), "direct_prefix_audit_2de0")

print("=" * 78)
print("R3 — THE RULING: the definition or the convention, and which is load-bearing")
print("=" * 78)

NMAX = 5
POP = {n: all_posets_8311(n) for n in range(2, NMAX + 1)}
ALL = [P for n in sorted(POP) for P in POP[n]]

# ---------------------------------------------------------------------------
print()
print("R3.1  THE POSITIVE ARGUMENT. The corpus's identity (Op-Form :220-227, quoted in")
print("      mg-76b2 Lemma 2.1) reads <1_A,(I-S_P)1_A> = E|A\\sigma(A)|. That identity is")
print("      what makes 'a bound on 1-rho' and 'a bound on Phi' the same statement, and it")
print("      is the hinge the whole Cheeger conversion turns on. It is a statement about a")
print("      MATRIX on one side and a COMBINATORIAL COUNT on the other, so it can decide")
print("      between two candidate counts. Both are tested against it here.")
print()
print("      Derivation, for the record, so the machine check is checking something known:")
print("        S_P is an average of permutation matrices M_sigma with (M_sigma)[x,y] = 1")
print("        iff y = sigma(x). <1_A,(I-M_sigma)1_A> = |A| - |{x in A : sigma(x) in A}|")
print("        = |A| - |A n sigma^{-1}(A)| = |A\\sigma^{-1}(A)| = |A\\sigma(A)| by R1.2.")
print("        Averaging over L(P) gives the identity. The CONVENTION has no such")
print("        representation: |A| - |A n set(p[:|A|])| is not a bilinear form in 1_A at")
print("        all -- it reads |A| twice, once as a set and once as a LENGTH.")
res = {}
for which in ("def", "conv"):
    bad = tot = 0
    first = None
    for P in ALL:
        S = S_P(P)
        for A in P.cuts():
            tot += 1
            lhs = quad_form_I_minus_S(P, A, S)
            rhs = P.E_leak(A, which)
            if lhs != rhs:
                bad += 1
                if first is None:
                    first = (P.n, sorted(P.rel), sorted(A), lhs, rhs)
    res[which] = bad
    label = ("DEFINITION matches <1_A,(I-S_P)1_A>" if which == "def"
             else "CONVENTION against the SAME identity")
    T.report(label, bad, tot,
             "per-(poset, cut), exact Fraction equality; matrix side built from "
             "Pr[pos_sigma(x)=i] and symmetrised, count side from the leak function",
             f"all {len(ALL)} posets on {{0..n-1}} with identity a linear extension, "
             f"n=2..{NMAX}, x all 2^n-2 proper cuts = {tot} (poset, cut) pairs",
             fatal=(which == "def"))
    if first is not None:
        n, rel, A, lhs, rhs = first
        print(f"       first failure: n={n}, rel={rel}, A={A}: "
              f"matrix {lhs} vs leak {rhs}")
print("       => the DEFINITION is the quantity the identity computes, on every pair. The")
print("          CONVENTION is not. This is an independent confirmation of the reading --")
print("          independent of STATE.md:41's notation, and independent of mg-76b2's")
print("          instrument, which is not imported here.")
print()
print("      and the same test carried to n=6, so the population matches the 310404 pairs")
print("      mg-76b2 checked its own version of this identity on (about 20s of CPU):")
P6 = all_posets_8311(6)
b6d = b6c = t6 = 0
for P in P6:
    S = S_P(P)
    for A in P.cuts():
        t6 += 1
        lhs = quad_form_I_minus_S(P, A, S)
        if lhs != P.E_leak(A, "def"):
            b6d += 1
        if lhs != P.E_leak(A, "conv"):
            b6c += 1
T.report("DEFINITION matches the identity at n=6 as well", b6d, t6,
         "per-(poset, cut), exact Fraction equality",
         f"all {len(P6)} posets at n=6 x all 62 proper cuts = {t6} pairs")
T.report("CONVENTION at n=6 -- EXPECTED TO FAIL", b6c, t6,
         "per-(poset, cut), exact Fraction equality",
         f"the same {t6} pairs", fatal=False)
print(f"       CUMULATIVE n=2..6: definition {b6d} / {t6 + 11316}, "
      f"convention {b6c + res['conv']} / {t6 + 11316}")
T.report("the cumulative population is mg-76b2's 310404 pairs, from a disjoint enumerator",
         0 if t6 + 11316 == 310404 else 1, 1,
         "integer equality against the figure at "
         "docs/OneThird-C3-PrefixCapture-mg-76b2.md:140",
         "all posets n=2..6 with identity a linear extension x all proper cuts")
print("       => mg-76b2 checked `<1_A,(I-S_P)1_A> = E|A\\sigma(A)|` on 310404 pairs and")
print("          got 0. This instrument checks it on the same 310404 pairs, from its own")
print("          enumerator and its own matrix builder, and gets 0. That is a")
print("          REPRODUCTION of mg-76b2's identity check, not a re-run of it -- and it is")
print("          the strongest single reason the DEFINITION is the right reading.")

# ---------------------------------------------------------------------------
print()
print("R3.2  THE CENSUS, by PARSING rather than grepping. mg-4d3b's audit recorded a source")
print("      census that read its own PROSE as CODE; a grep for `phi_star` matches this")
print("      docstring. An `ast` walk over mg-2de0's own files cannot. Every attribute")
print("      access or definition named E_leak / phi / phi_star / K_k / E_K, with its line:")
NAMES = {"E_leak", "phi", "phi_star", "K_k", "E_K", "delta_1_prefix"}
sites = []
for fn in sorted(os.listdir(LIB2DE0_DIR)):
    if not fn.endswith(".py"):
        continue
    path = os.path.join(LIB2DE0_DIR, fn)
    with open(path) as fh:
        src = fh.read()
    tree = ast.parse(src, filename=fn)
    lines = src.splitlines()
    for node in ast.walk(tree):
        nm = kind = None
        if isinstance(node, ast.Attribute) and node.attr in NAMES:
            nm, kind = node.attr, "call/attr"
        elif isinstance(node, ast.FunctionDef) and node.name in NAMES:
            nm, kind = node.name, "def"
        elif isinstance(node, ast.Name) and node.id in NAMES:
            nm, kind = node.id, "name"
        if nm is not None:
            sites.append((fn, node.lineno, nm, kind,
                          lines[node.lineno - 1].strip()[:52]))
sites.sort()
print(f"       {'file':>22s} {'line':>5s} {'name':>14s} {'kind':>9s}  source")
for fn, ln, nm, kind, txt in sites:
    print(f"       {fn:>22s} {ln:>5d} {nm:>14s} {kind:>9s}  {txt}")
leak_reachers = sorted({(fn, ln) for fn, ln, nm, _, _ in sites
                        if nm in ("E_leak", "phi", "phi_star") and fn != "lib2de0.py"})
print()
print(f"       => {len(leak_reachers)} call sites OUTSIDE lib2de0.py reach E_leak, all of them")
print("          through phi / phi_star, and they live in exactly two files:")
for fn in sorted({fn for fn, _ in leak_reachers}):
    print(f"            {fn}: lines {[ln for f, ln in leak_reachers if f == fn]}")
files = sorted({fn for fn, _ in leak_reachers})
T.report("E_leak is reached from exactly two files, a3_nonvacuity.py and selftest2de0.py",
         0 if files == ["a3_nonvacuity.py", "selftest2de0.py"] else 1, 1,
         "set equality on the parsed file names",
         f"every .py file in {os.path.relpath(LIB2DE0_DIR, os.path.dirname(HERE))}, "
         f"AST-walked, {len(sites)} sites total")
kk = sorted({fn for fn, ln, nm, _, _ in sites
             if nm in ("K_k", "E_K", "delta_1_prefix") and fn != "lib2de0.py"})
print(f"       and the PREFIX machinery (K_k / E_K / delta_1_prefix) is reached from {kk},")
print("       which by R1.4 is UNAFFECTED by the repair. The blast radius is Phi only.")

# ---------------------------------------------------------------------------
print()
print("R3.3  THE LOAD-BEARING TEST -- the question the ticket actually asks. Is there any")
print("      assertion mg-2de0 PUBLISHED that is TRUE under the convention and FALSE under")
print("      the definition? If there is, the definition does not simply win. mg-2de0's")
print("      Phi assertions are three, and each is evaluated under BOTH conventions:")
print()
print("        (i)   Phi_P(A) <= 1 for every cut                 [A3.2, published 0/12702]")
print("        (ii)  Phi* <= min_k Delta_1(A_k) for every poset  [A3.4, published 0/431]")
print("        (iii) Phi* == min_k Delta_1(A_k) at the antichain [A3.5, published 0/6]")
print()
print("      on MY population (all posets n=2..5) rather than mg-2de0's -- R4 re-runs")
print("      mg-2de0's own population through mg-2de0's own scripts:")
print(f"       {'assertion':>12s} {'convention':>22s} {'definition':>22s}")
rows = []
b1c = b1d = t1 = 0
for P in ALL:
    for A in P.cuts():
        t1 += 1
        if P.phi(A, "conv") > 1:
            b1c += 1
        if P.phi(A, "def") > 1:
            b1d += 1
rows.append(("(i)", f"{b1c} / {t1}", f"{b1d} / {t1}"))
b2c = b2d = t2 = 0
for P in ALL:
    t2 += 1
    m = P.prefix_min()
    if P.phi_star("conv") > m:
        b2c += 1
    if P.phi_star("def") > m:
        b2d += 1
rows.append(("(ii)", f"{b2c} / {t2}", f"{b2d} / {t2}"))
b3c = b3d = t3 = 0
for n in range(2, 8):
    Aq = antichain(n)
    t3 += 1
    m = Aq.prefix_min()
    if Aq.phi_star("conv") != m:
        b3c += 1
    if Aq.phi_star("def") != m:
        b3d += 1
rows.append(("(iii)", f"{b3c} / {t3}", f"{b3d} / {t3}"))
for a, c, d in rows:
    print(f"       {a:>12s} {c:>22s} {d:>22s}")
bad = b1d + b2d + b3d
T.report("all three of mg-2de0's Phi assertions hold under the DEFINITION too",
         bad, t1 + t2 + t3,
         "exact Fraction comparisons, three assertions at their own grains",
         f"(i) {t1} (poset, cut) pairs; (ii) {t2} posets; (iii) antichains n=2..7")
survive = (b1c == b1d == 0 and b2c == b2d == 0 and b3c == b3d == 0)
T.report("NO published assertion is true under the convention and false under the "
         "definition -- the convention is NOT load-bearing",
         0 if survive else 1, 1,
         "conjunction: every assertion holds in both columns",
         "the three assertions above")

# ---------------------------------------------------------------------------
print()
print("R3.4  THE RULING, stated explicitly before any code changes.")
print()
print("      THE DEFINITION IS CORRECT. lib2de0.E_leak IS DEFECTIVE AND IS REPAIRED.")
print()
print("      The ruling rests on three things, in order of weight, and NOT on the fact")
print("      that the definition is the definition:")
print()
print("      1. THE CONVENTION IS NOT A CONDUCTANCE. Conductance is a property of a CUT.")
print("         R1.3 measured |A\\sig(A)| != |A^c\\sig(A^c)| under the convention on 457132")
print("         of 683656 (permutation, cut) pairs to n=7. lib2de0.py:17 calls Phi_P 'the")
print("         same quantity, read as a CONDUCTANCE, minimised over ALL cuts A'. Under the")
print("         convention 'the cut' does not determine the value, so minimising over cuts")
print("         is not a well-posed operation in the sense the Cheeger argument needs.")
print("         The definition satisfies the symmetry on all 683656 pairs.")
print()
print("      2. THE DEFINITION IS WHAT THE CORPUS'S MATRIX IDENTITY COMPUTES. R3.1, 0")
print("         exceptions for the definition and a failure count for the convention, on a")
print(f"         matrix built here from Pr[pos_sigma(x)=i] and on {len(ALL)} posets.")
print()
print("      3. THE CONVENTION IS NOT LOAD-BEARING. R3.3: all three of mg-2de0's published")
print("         Phi assertions hold under BOTH readings, so nothing mg-2de0 concluded")
print("         requires the convention. R3.2 bounds the blast radius by PARSING: two")
print("         files, and the prefix machinery is untouched.")
print()
print("      WHAT THE CONVENTION ACTUALLY IS, named so it is not mistaken for a variant")
print("      reading: |A| - |A n set(p[:|A|])| measures how far A is from being an INITIAL")
print("      SEGMENT under sigma. That is a real and meaningful quantity -- it is the")
print("      natural generalisation of K_k in the direction of 'prefix-ness' rather than of")
print("      'function application', which is why the slip is an easy one and why it agrees")
print("      with K_k on prefixes. It is simply not Delta_1 and not Phi_P.")

print()
print("=" * 78)
print(f"R3 TOTAL BAD: {T.bad}")
print("=" * 78)
sys.exit(0 if T.bad == 0 else 1)
