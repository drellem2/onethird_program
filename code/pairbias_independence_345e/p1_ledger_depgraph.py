#!/usr/bin/env python3
"""mg-345e P1 — does the SUPPLY path in mg-88bd's claim ledger reach claim 4?

Claim 4 is "L4's F is n-free; eps must be an absolute constant below a threshold".
It is the ledger's own node for the L4 modulus question that gates mg-6bc2.

SCOPE: this measures the ledger's RECORDED dependency clauses. It is a measurement of a
document, not of the mathematics. Printed at the top of the output, every run.
"""
import sys

from lib345e import parse_ledger, dependents_of, reaches

L4_MODULUS_CLAIM = 4

# The two paths, named from Op-Form's own section structure.
SUPPLY = {
    21: "master bound 1-lambda_std <= 3E[D]/(n^2-1) <= 6E[I]/(n^2-1)  (6.1)",
    22: "E_unif[footrule] = (n^2-1)/3                                 (6.1)",
    25: "frozen => E[inv_e] < m/3                                     (6.3)",
    26: "freezing alone gives (LIB-const) with constant 2/3           (6.3)",
    27: "Claim 6.1 through the master bound reproduces d*n/(n+1)      (6.3)",
}
DEMAND = {
    12: "'<<' in Step 5 = constant fraction                           (4.1)",
    17: "L3 is the last candidate site; chain is n-free end to end    (4.3)",
    18: "operative form: absolute constant, uniform in n              (5.1)",
    23: "(LIB-const) E[inv_e] <= (eps_spec/6)(n^2-1)                  (6.2)",
    28: "the constant budget eps_leak ~ 0.20, eps_spec ~ 2e-2/C_3     (6.4)",
}


def main():
    claims, edges, residue = parse_ledger()
    fail = 0

    print("=" * 78)
    print("mg-345e P1 — LEDGER DEPENDENCY GRAPH of mg-88bd (Op-Form section 9)")
    print("=" * 78)
    print("SCOPE: measures the ledger's RECORDED 'CONDITIONAL on N' / 'given N' clauses.")
    print("       A claim whose label UNDERSTATES its dependencies scores independent here.")
    print("       The doc argues independence from the mechanism too; it does not rest on this.")
    print()
    print(f"claims parsed : {len(claims)}   (P9 predicted 36)")
    n_edges = sum(len(v) for v in edges.values())
    print(f"edges parsed  : {n_edges}       (P9 predicted 12-20)")
    print()

    if len(claims) != 36:
        print(f"  !! expected 36 ledger rows, parsed {len(claims)} — parse is suspect")
        fail = 1

    print("-- recorded dependency edges -------------------------------------------------")
    for c in sorted(edges):
        if edges[c]:
            print(f"   {c:>2} <- {sorted(edges[c])}")
    print()

    dep4 = dependents_of(edges, L4_MODULUS_CLAIM)
    print(f"-- transitive dependents of claim {L4_MODULUS_CLAIM} "
          f"(L4's F is n-free) ------------------------")
    print(f"   {dep4}   (count {len(dep4)}; P2 predicted 4-8)")
    print()

    print("-- SUPPLY path: pair bias -> a constant uniform in n -------------------------")
    supply_hits = []
    for c, desc in sorted(SUPPLY.items()):
        r = reaches(edges, c, L4_MODULUS_CLAIM)
        print(f"   claim {c:>2}  reaches-4={'YES' if r else 'no '}  {desc}")
        print(f"             label: {claims[c][2][:96]}")
        if r:
            supply_hits.append(c)
    print()

    print("-- DEMAND path: what threshold does the architecture consume? ----------------")
    demand_miss = []
    for c, desc in sorted(DEMAND.items()):
        r = reaches(edges, c, L4_MODULUS_CLAIM)
        print(f"   claim {c:>2}  reaches-4={'YES' if r else 'no '}  {desc}")
        if not r:
            demand_miss.append(c)
    print()

    print("-- uncaptured integers in label cells, for HAND adjudication -----------------")
    print("   (the parser captures 'on N' / 'given N'. Anything else a label says about")
    print("    another claim is surfaced here rather than dropped silently.)")
    if not residue:
        print("   none")
    for c in sorted(residue):
        print(f"   claim {c:>2}: {residue[c]}")
        print(f"             {claims[c][2][:110]}")
    print()

    print("=" * 78)
    print("VERDICT")
    print("=" * 78)
    if supply_hits:
        print(f"  SUPPLY path REACHES claim 4 at {supply_hits} — P3 REFUTED.")
        fail = 1
    else:
        print("  SUPPLY path does NOT reach claim 4 at any of "
              f"{sorted(SUPPLY)} — P3 held.")
    if demand_miss:
        print(f"  DEMAND path claims {demand_miss} do NOT reach claim 4.")
        print("  (Read this as located dependency, not as independence: see the doc's")
        print("   section on claim 28, whose gate is C_3 and is NOT an L4 question.)")
    else:
        print(f"  DEMAND path reaches claim 4 at every one of {sorted(DEMAND)}.")
    print()
    print(f"  exit {fail}")
    return fail


if __name__ == "__main__":
    sys.exit(main())
