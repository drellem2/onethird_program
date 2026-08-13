#!/usr/bin/env python3
"""mg-5987 `g0` — CONTROLS.  Nothing in `g1`–`g3` is worth reading if this arm is not green.

The verdicts in this directory are of the form *"the minimum of `Q` over the primitive class is
bounded"*, and every one of them is a statement about two numbers per poset — `max_x |h − rank|`
and `Σ_x C_x / E[inv_e]`.  So the controls are almost entirely about those two numbers being what
they are claimed to be, computed twice by different routes: once by the closed-form machinery
`lib5987.profile` uses (order-ideal DP, no permutation ever built) and once by brute-force
enumeration of `L(P)` (every permutation built, no DP anywhere).

Also here: the three planted defects, the ONE that comes back inert and is printed rather than
swapped out, and the wrong-direction control that makes `g1`'s emptiness a fact about the
hypothesis rather than a limitation of the tool.
"""

import sys
from fractions import Fraction

import lib5987 as M
import lib6ff4 as L

FAIL = []
RAN = []


def check(name, ok, detail=""):
    print(f"  [{'ok ' if ok else 'FAIL'}] {name}{('  — ' + detail) if detail else ''}")
    RAN.append(name)
    if not ok:
        FAIL.append(name)


def brute(n, down):
    """h, Var(pos), Σdisp² and the same-side covariance, by ENUMERATING `L(P)`.

    Shares no line of code with `lib5987.profile`: no order-ideal DP, no closure, no `p_before`.
    That is the point — a shared enumerator would move both readings the same way."""
    exts = L.linear_extensions(n, down)
    N = len(exts)
    h = [Fraction(sum(M.rank_of(e)[x] for e in exts), N) for x in range(n)]
    var = [Fraction(sum(M.rank_of(e)[x] ** 2 for e in exts), N) - h[x] ** 2 for x in range(n)]
    return h, var, N


print("=" * 96)
print("mg-5987  g0 — CONTROLS")
print("=" * 96)

CL = L.all_classes(7)

print("\n1. THE ENUMERATOR, against OEIS A000112 (posets up to isomorphism).")
A000112 = [1, 1, 2, 5, 16, 63, 318, 2045]
check("A000112 at n = 1..7", [len(CL[n]) for n in range(1, 8)] == A000112[1:],
      str([len(CL[n]) for n in range(1, 8)]))

print("\n2. `count_ext` (ideal DP) against BRUTE-FORCE enumeration of L(P), every class n ≤ 6.")
bad = [(n, d) for n in range(1, 7) for d in CL[n] if L.count_ext(n, d) != len(L.linear_extensions(n, d))]
check("|L(P)| agrees at all %d classes n ≤ 6" % sum(len(CL[n]) for n in range(1, 7)), not bad, str(bad[:2]))

print("\n3. `profile()` against BRUTE FORCE — h, Var, and the variance split Var = diag + C.")
print("   The split is the ONE identity every (B-cov) number in this directory rests on:")
print("   pos_σ(x) = 1 + Σ_y s_xy, so Var(pos_x) = Σ_y Var(s_xy) + Σ_{y≠z} Cov(s_xy, s_xz).")
nbad = vbad = sbad = 0
pop3 = [(n, d) for n in range(2, 6) for d in CL[n] if L.incomparable_pairs(n, d)]
pop3 += [(6, d) for d in CL[6][::7] if L.incomparable_pairs(6, d)]
for n, d in pop3:
    pr = M.profile(n, d)
    h, var, _ = brute(n, d)
    nbad += (pr["h"] != h)
    vbad += (pr["var"] != var)
    sbad += any(pr["var"][x] != pr["diag"][x] + pr["C"][x] for x in range(n))
check("E[pos_σ x] agrees at all %d posets" % len(pop3), nbad == 0, "%d mismatches" % nbad)
check("Var(pos_σ x) agrees — so Σ_x C_x is what it says it is", vbad == 0, "%d mismatches" % vbad)
check("Var = diag + C holds identically", sbad == 0, "%d mismatches" % sbad)

print("\n3b. `E[inv_e]` — (B-cov)'s DENOMINATOR — against brute force, at two reference orders.")
ebad = 0
for n, d in pop3:
    pr = M.profile(n, d)
    exts = L.linear_extensions(n, d)
    for ref in (M.barycentric(n, pr["h"]), exts[0]):
        r = M.rank_of(ref)
        want = Fraction(sum(L.inv_against(n, d, e, r) for e in exts), len(exts))
        ebad += (M.e_inv(n, d, r, pr) != want)
check("E[inv_e] agrees at %d posets × 2 reference orders" % len(pop3), ebad == 0, "%d mismatches" % ebad)

print("\n4. mg-dcae's SPLIT, against brute force: E[Σ disp²] = Σ Var(pos_x) + Σ (h(x) − rank_e x)².")
print("   This is the identity that makes (B-cov) and (B-bias) a decomposition of (B) rather than")
print("   two unrelated obligations.  It holds at EVERY reference order and is checked at two.")
ibad = 0
for n, d in pop3[:60]:
    pr = M.profile(n, d)
    exts = L.linear_extensions(n, d)
    for ref in (M.barycentric(n, pr["h"]), exts[0]):
        r = M.rank_of(ref)
        lhs = Fraction(sum(sum((M.rank_of(e)[x] - r[x]) ** 2 for x in range(n)) for e in exts), len(exts))
        rhs = sum(pr["var"]) + sum((pr["h"][x] - r[x]) ** 2 for x in range(n))
        ibad += (lhs != rhs)
check("the split holds at %d posets × 2 reference orders" % len(pop3[:60]), ibad == 0, "%d mismatches" % ibad)

print("\n5. docs/FACTS.md F11's SIGN, reproduced: C_x ≥ 0 at every (poset, element) row.")
print("   ⚠️  NOT an independent corroboration of F11 — `p_before` is shared with the library F11")
print("   was measured through.  What IS independent is the population: F11 sampled n = 5, 6;")
print("   this is exhaustive to n = 7, and `g3` carries the sign to every n by a closed form.")
rows = neg = 0
for n in range(2, 8):
    for d in (CL[n] if n <= 6 else CL[7][::5]):
        if not L.incomparable_pairs(n, d):
            continue
        pr = M.profile(n, d)
        rows += n
        neg += sum(1 for c in pr["C"] if c < 0)
check("C_x ≥ 0 at %d (poset, element) rows" % rows, neg == 0, "%d negative" % neg)

print("\n6. THE CLOSED FORMS, term by term against the general machinery.")
zbad = abad = 0
for n in range(3, 12):
    z, cf = M.zigzag(n), M.zigzag_closed_form(n)
    pr = M.profile(n, z)
    r = M.rank_of(M.barycentric(n, pr["h"]))
    zbad += (pr["total"] != cf["ext"] or M.bias(n, pr, r) != cf["bias"]
             or M.cov_total(pr) != cf["cov"] or M.e_inv(n, z, r, pr) != cf["inv"]
             or M.rho(n, z, pr, r) != cf["rho"])
    a, ca = M.antichain(n), M.antichain_closed_form(n)
    pa = M.profile(n, a)
    ra = M.rank_of(M.barycentric(n, pa["h"]))
    abad += (M.bias(n, pa, ra) != ca["bias"] or M.rho(n, a, pa, ra) != ca["rho"]
             or M.cov_total(pa) != ca["cov"])
check("Z_n: |L| = F_{n+1}, bias, Σ C_x, E[inv], ρ  (n = 3..11)", zbad == 0, "%d mismatches" % zbad)
check("A_n: bias = (n−1)/2, ρ = (n−2)/3, Σ C_x     (n = 3..11)", abad == 0, "%d mismatches" % abad)
check("Z_n is primitive at n = 3..11", all(L.is_primitive(n, M.zigzag(n)) for n in range(3, 12)))
check("A_n is primitive at n = 3..11", all(L.is_primitive(n, M.antichain(n)) for n in range(3, 12)))

print("\n7. THE PRICE MACHINERY, against mg-9b6b's OWN PUBLISHED FIGURE.")
print("   `delivers()` is fed (R)'s floor — `2/n`, the primitive density floor — at row 8's D.")
print("   ⚠️  Computed THROUGH lib9b6b, so this is a consistency check on this arm's price")
print("   machinery, NOT a second measurement of mg-9b6b's 84.")
rd = [n for n in range(3, 400) if M.V.primitive_floor(n) > M.V.d_needed(n)]
check("(R) at row 8 forbids a frozen primitive up to n = 98", max(rd) == 98, "max n = %d" % max(rd))
check("(R) at row 8 delivers 96 orders, 84 of them unreached (n > 14)",
      len(rd) == 96 and len([n for n in rd if n > 14]) == 84,
      "%d orders, %d unreached" % (len(rd), len([n for n in rd if n > 14])))
synth = {3: Fraction(1, 2), 4: Fraction(1, 4), 5: Fraction(1, 8)}
check("`delivers` on a hand table", M.delivers(synth, Fraction(1, 5)) == [3, 4])
check("`coverage` on a hand list", M.coverage([Fraction(1), Fraction(0), None], Fraction(1, 2)) == (1, 3))

print("\n8. PLANTED DEFECTS — three live, and the fourth is reported inert rather than swapped out.")


def replant(fn):
    """Run `fn` against the same brute force `profile()` is checked against; True = the plant was
    CAUGHT.  A plant that is not caught means the control in §3 is not doing its job."""
    for n, d in pop3[:40]:
        if fn(n, d):
            return True
    return False


def plant_no_factor_two(n, d):
    """P1 — count each unordered {y,z} once instead of twice.  `Var = diag + C` must break."""
    pr = M.profile(n, d)
    total = pr["total"]
    for x in range(n):
        inc = pr["inc"][x]
        c = sum(M.joint_before(n, d, y, z, x, total) - pr["p"][(y, x)] * pr["p"][(z, x)]
                for i, y in enumerate(inc) for z in inc[i + 1:])
        if pr["var"][x] != pr["diag"][x] + c:
            return True
    return False


def plant_h_forgets_forced(n, d):
    """P2 — h(x) = 1 + Σ_{y ∥ x} p, dropping the elements FORCED below x.  Must break vs brute."""
    pr = M.profile(n, d)
    h, _, _ = brute(n, d)
    return any(Fraction(1) + sum(pr["p"][(y, x)] for y in pr["inc"][x]) != h[x] for x in range(n))


def plant_inv_ignores_reference(n, d):
    """P3 — `E[inv_e]` taking the same orientation at every pair instead of the reference's.

    The denominator of (B-cov) is the one quantity that is a function of the READING, so a plant
    that ignores the reading is the plant that matters most here."""
    pr = M.profile(n, d)
    exts = L.linear_extensions(n, d)
    r = M.rank_of(M.barycentric(n, pr["h"]))
    bad = sum(pr["p"][(b, a)] for a in range(n) for b in range(a + 1, n)
              if not L.comparable(d, a, b))
    want = Fraction(sum(L.inv_against(n, d, e, r) for e in exts), len(exts))
    return bad != want


check("P1  C_x without the factor 2 — CAUGHT by Var = diag + C", replant(plant_no_factor_two))
check("P2  h dropping the forced-below count — CAUGHT by brute force", replant(plant_h_forgets_forced))
check("P3  E[inv_e] ignoring the reference order — CAUGHT by brute force", replant(plant_inv_ignores_reference))

print("\n   TWO CANDIDATE PLANTS CAME BACK INERT.  Both are printed rather than swapped out, and")
print("   both fail for the same reason in two costumes: a plant has to be a defect the DOMAIN")
print("   can express, and `joint_before`'s two skipped branches are skipped because the domain")
print("   forbids the case, not because the author preferred to.")
reach = same = fired_asc = fired_desc = 0
for n, d in pop3:
    pr = M.profile(n, d)
    for x in range(n):
        for order, tag in ((pr["inc"][x], "asc"), (pr["inc"][x][::-1], "desc")):
            for i, y in enumerate(order):
                for z in order[i + 1:]:
                    dd = L._closure_with(n, d, y, x)
                    if tag == "asc" and L.is_below(dd, x, z):
                        reach += 1
                    if L.is_below(dd, z, x):
                        if tag == "asc":
                            fired_asc += 1
                        else:
                            fired_desc += 1
                            same += (L._closure_with(n, dd, z, x) == dd)
toposort = all(d[i] < (1 << i) for n, d in pop3 for i in range(n))
print(f"  [inert] P4  the `return 0` branch is UNREACHABLE: fired {reach} times over {len(pop3)} posets,")
print( "          and the reason is structural rather than a shortage of population — adding `y < x`")
print( "          creates only `{a ≤ y} < {b ≥ x}`, and `x ≤ y` is false because y ∥ x, so `x < z`")
print( "          can never arise.  A plant on it would report green against a correct library.")
print(f"  [inert] P5  re-closing an already-forced `z < x` fired {fired_asc} times as the code runs —")
print( "          and the reason is an IMPORTED INVARIANT rather than a fact about posets, which is")
print( "          why it is checked in both directions instead of asserted: `lib6ff4`'s canonical")
print( "          labelling is a linear extension, and the inner loop runs over an ASCENDING")
print(f"          sublist, so `z ≤ y` cannot hold.  Reverse the sublist and the case arises")
print(f"          {fired_desc} times — where `_closure_with` returns its own INPUT at {same} of")
print(f"          {fired_desc}.  So the skip is an optimisation, not a correctness guard.")
check("P4's branch really is unreachable (fired 0 times)", reach == 0, "%d" % reach)
check("lib6ff4's canonical labelling IS a linear extension (down[i] ⊆ {0..i−1})", toposort)
check("P5's case is unreachable as the loop runs, and reachable when it is reversed",
      fired_asc == 0 and fired_desc > 0, "%d asc, %d desc" % (fired_asc, fired_desc))
check("and there the re-close is a no-op — an optimisation, not a guard",
      same == fired_desc, "%d of %d" % (same, fired_desc))

print("\n9. WRONG-DIRECTION CONTROL — the same machinery on a class that is NOT empty.")
print("   g1's central measurement is a zero: STATE.md's reference order `e` is fully decided at")
print("   almost no reachable poset.  A zero over an empty class is worth nothing unless the same")
print("   instrument returns something on a class that is not empty, so it is asked twice.")


def decided(n, d, pr, beta):
    """Is every incomparable pair `(1−β)`-decided?  At β = 1/3 this is `δ(P) ≤ 1/3` verbatim."""
    return all(max(pr["p"][(x, y)], 1 - pr["p"][(x, y)]) >= 1 - beta
               for (x, y) in L.incomparable_pairs(n, d))


for beta in (Fraction(1, 3), Fraction(2, 5)):
    tot = hits = agree = 0
    for n in range(3, 7):
        for d in M.primitives(CL, n):
            pr = M.profile(n, d)
            tot += 1
            if decided(n, d, pr, beta):
                hits += 1
                e, _ = M.majority_reference(n, d, pr, beta)
                agree += (e is not None and e == M.barycentric(n, pr["h"]))
    print(f"  β = {beta}: fully decided at {hits:3d} of {tot} primitives, n ≤ 6"
          f" — and the majority order EQUALS the barycentric order at {agree} of {hits}")
    if beta == Fraction(1, 3):
        check("at β = 1/3 the class is all but empty (≤ 1 member)", hits <= 1, "%d" % hits)
    else:
        check("at β = 2/5 the class is NOT empty — the instrument still returns orders", hits > 1,
              "%d" % hits)
        check("and where `e` exists at all it IS the barycentric order", agree == hits,
              "%d of %d" % (agree, hits))

print("\n10. `majority_reference` at β = 1/3 against lib6ff4's own `majority_order`.")
mbad = 0
for n in range(3, 7):
    for d in M.primitives(CL, n):
        pr = M.profile(n, d)
        tbl = {(x, y): pr["p"][(x, y)] for (x, y) in L.incomparable_pairs(n, d)}
        mbad += (M.majority_reference(n, d, pr, Fraction(1, 3))[0] != L.majority_order(n, d, tbl)[0])
check("the parametrised reference reproduces lib6ff4 at its own threshold", mbad == 0, "%d" % mbad)

print("\n" + "=" * 96)
print("g0 VERDICT: " + (f"GREEN — {len(RAN)} controls" if not FAIL else "RED — " + "; ".join(FAIL)))
print("=" * 96)
sys.exit(1 if FAIL else 0)
