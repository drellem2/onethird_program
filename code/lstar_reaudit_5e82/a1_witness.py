"""a1 -- STEP A.  The poset itself, before any spectral claim is looked at.

A witness that is not primitive is not a counterexample to anything this arc has
claimed, so all four structural facts are re-derived rather than accepted: naturally
labelled, transitively closed, n = 12, LE = 10584, primitive.  Delta and M come out
of the same enumeration.

THE METHOD IS DELIBERATELY NOT THE CORPUS'S.  cb417 warned that lib5cba, lib789d and
libc50b agree on LE, Delta and M but all three descend from one reading of one
definition.  So this arm runs no transport DP: it enumerates EVERY ONE of the linear
extensions and counts.
"""
import sys
from fractions import Fraction as Fr
from common5e82 import DN, N, build, banner

ok = True


def check(label, got, want):
    global ok
    good = got == want
    ok = ok and good
    print("  [%s] %-58s got=%s want=%s" % ("ok " if good else "FAIL", label, got, want))


banner("a1  STEP A -- THE POSET, RE-DERIVED BY EXPLICIT ENUMERATION")
P = build()
print("  dn =", DN)
print("  strict lower sets:")
import lib5e82 as L

for i in range(N):
    print("     down(%2d) = %s" % (i, L.bits(DN[i])))
print()
check("n", P.n, 12)
check("naturally labelled", P.natural, True)
check("transitively closed", P.transitive, True)
check("LE (counted, one per enumerated extension)", P.LE, 10584)
check("Delta = max_i (1 - (S_P)_ii)", P.Delta, Fr(195, 196))
check("M = sum_k leak(A_k) / floor(n^2/4)", P.M, Fr(7717, 21168))
check("primitive (leak(A_k) > 0 for every k)", P.primitive, True)
print()
print("  argmax of d_i (the near-free element):",
      [i for i in range(N) if P.d[i] == P.Delta], " at d =", P.Delta)
print("  leaks:", [str(x) for x in P.leaks])
print("  min leak:", min(P.leaks), "=", float(min(P.leaks)), "> 0")
print()
print("  CROSS-CHECKS THAT THE ENUMERATION IS INTERNALLY CONSISTENT")
check("every row of PI sums to LE", all(sum(P.PI[i]) == P.LE for i in range(N)), True)
check("every column of PI sums to LE",
      all(sum(P.PI[i][j] for i in range(N)) == P.LE for j in range(N)), True)
check("S_P is doubly stochastic", all(
    sum(P.S[i][j] for j in range(N)) == 1 for i in range(N)) and all(
    sum(P.S[i][j] for i in range(N)) == 1 for j in range(N)), True)
# The enumeration is only "every linear extension" if every sequence it produced
# really is one.  Checked on all 10584, against the relation, rather than trusted.
# (My first version of this arm wrote the condition with an `and False` in it and so
# could not fail -- a vacuous clause inside a suite whose subject is claims that were
# never computed.  This one is scored on real sequences.)
exts = L.linear_extensions(DN, N)
check("the enumeration produced exactly LE sequences", len(exts), P.LE)
check("all sequences distinct", len(set(exts)), P.LE)
check("every sequence is a permutation of [0,n)",
      all(sorted(e) == list(range(N)) for e in exts), True)
check("every sequence respects every relation of P", all(
    e.index(i) < e.index(j) for e in exts for j in range(N) for i in L.bits(DN[j])), True)
# Those three arms say every sequence produced IS a linear extension.  They do not say
# none was MISSED, and a generator that silently drops extensions would lower LE and
# move every scalar below.  Completeness is checked in a0 arm S3, by filtering all n!
# permutations at n <= 7 and comparing -- brute force, where brute force is affordable.
print()
print("  THE CORPUS'S CLOSED FORMS FOR Q AND N, CHECKED AGAINST THE DEFINITION")
qcf, ncf = P.closed_form_agrees()
check("Q_kl == sum_{i<min(k,l)} sum_{j>=max(k,l)} a_ij", qcf, True)
check("N_kl == min(k,l) - kl/n", ncf, True)
check("Q symmetric", all(P.Q[i][j] == P.Q[j][i] for i in range(P.m) for j in range(P.m)), True)
check("N positive definite (Gram matrix of the psi_k)", L.is_psd(P.NI), True)
print()
banner("a1 VERDICT: %s" % ("ALL ARMS SATISFACTORY" if ok else "*** AN ARM FAILED ***"))
sys.exit(0 if ok else 1)
