#!/usr/bin/env python3
"""mg-345e P2 — can L4's HYPOTHESIS be reached without passing through L1b?

This is the load-bearing structural question behind the answer, and it is the one I would
otherwise have to assert. If L4's hypothesis (a thin prefix) is reachable ONLY through
L1b's conclusion, then no derivation of L1b can invoke L4 without circularity — the
independence is STRUCTURALLY FORCED, not merely observed.

The corpus contains a candidate escape and this probe is written to find it rather than to
confirm the tidy answer: the direct-prefix route (mg-00b9 Lemma A/B, REPAIRED by mg-2de0)
converts an inversion bound straight to prefix thinness with no spectral statement.

SCOPE: ARCH_EDGES is a HAND TRANSCRIPTION of the stated architecture. It is not derived
from any file. Its provenance is printed per edge.
"""
import sys

from lib345e import (ARCH_EDGES, DIRECT_EDGE, SPECTRAL_NODE,
                     FROZEN, PAIRB, THIN, L4FIRE)


def paths(edges, src, dst, banned=()):
    """All simple paths src -> dst avoiding every node in `banned`."""
    out = []

    def walk(node, sofar):
        if node == dst:
            out.append(sofar)
            return
        for nxt in edges.get(node, ()):
            if nxt in banned or nxt in sofar:
                continue
            walk(nxt, sofar + [nxt])

    if src in banned:
        return out
    walk(src, [src])
    return out


def show(label, ps):
    print(f"   {label}: {len(ps)} path(s)")
    for p in ps:
        print("      " + "\n        -> ".join(p))


def main():
    fail = 0
    print("=" * 78)
    print("mg-345e P2 — ARCHITECTURE REACHABILITY: is L4's hypothesis behind L1b?")
    print("=" * 78)
    print("SCOPE: hand-transcribed step graph. Provenance per edge:")
    print("   frozen -> pair bias        Op-Form Claim 6.1 [PROVEN]")
    print("   pair bias -> L1b concl.    mg-210d master bound (Op-Form 6.1)")
    print("   L1b concl. -> thin prefix  Steps 2-5: Cheeger + L2/L3 prefix restriction")
    print("   thin prefix -> L4 fires    L4's hypothesis IS Delta_1 <= eps")
    print("   L4 fires -> balanced pair  Step 6 stated transfer")
    print()

    # ---- arm A: the architecture as stated in the source
    A = {k: list(v) for k, v in ARCH_EDGES.items()}
    print("-- ARM A: architecture as stated (spectral route only) -----------------------")
    all_p = paths(A, FROZEN, L4FIRE)
    show("frozen -> L4 fires", all_p)
    banned_p = paths(A, FROZEN, L4FIRE, banned=(SPECTRAL_NODE,))
    show(f"frozen -> L4 fires WITHOUT '{SPECTRAL_NODE}'", banned_p)
    armA_forced = (len(all_p) > 0 and len(banned_p) == 0)
    print(f"   => circularity argument holds in arm A: {armA_forced}")
    print()

    # ---- arm B: with the direct-prefix route added
    B = {k: list(v) for k, v in ARCH_EDGES.items()}
    B[DIRECT_EDGE[0]] = B.get(DIRECT_EDGE[0], []) + [DIRECT_EDGE[1]]
    print("-- ARM B: + direct-prefix route (mg-00b9 Lemma A/B, repaired by mg-2de0) ------")
    print("   edge added: pair bias -> thin prefix, with NO spectral statement.")
    print("   Audit headline: the repaired route reaches Delta_1 <= 2/3 (mg-2de0 sec 0).")
    all_pB = paths(B, FROZEN, L4FIRE)
    show("frozen -> L4 fires", all_pB)
    banned_pB = paths(B, FROZEN, L4FIRE, banned=(SPECTRAL_NODE,))
    show(f"frozen -> L4 fires WITHOUT '{SPECTRAL_NODE}'", banned_pB)
    armB_forced = (len(all_pB) > 0 and len(banned_pB) == 0)
    print(f"   => circularity argument holds in arm B: {armB_forced}")
    print()

    print("=" * 78)
    print("VERDICT")
    print("=" * 78)
    if not armA_forced:
        print("  ARM A: L4's hypothesis is NOT behind L1b even in the stated architecture.")
        print("         The circularity argument fails outright. Report and stop.")
        fail = 1
    else:
        print("  ARM A: L4's hypothesis is reachable ONLY through L1b's conclusion.")
        print("         => a derivation of L1b that invoked L4 would be circular.")
    if armB_forced:
        print("  ARM B: the direct-prefix route does NOT bypass L1b. (unexpected)")
        fail = 1
    else:
        print("  ARM B: the direct-prefix route DOES bypass L1b — the circularity")
        print("         argument has a NAMED ESCAPE and is therefore CONDITIONAL, not")
        print("         absolute. What the escape would buy is not an L4-dependent")
        print("         eps_spec but a VACUOUS one: L4 + a thin prefix reached without")
        print("         L1b contradicts delta(P)<1/3, emptying the hypothesis class, and")
        print("         every statement about minimal counterexamples becomes vacuously")
        print("         true. That is the pair-bias question dissolved, not answered.")
        print("         LIVE? NO at the numbers on record: the repaired direct route")
        print("         reaches Delta_1 <= 2/3 and L4 is calibrated at eps_leak ~ 0.20.")
        print("         2/3 > 0.20, so the escape is not open today.")
    print()
    print(f"  exit {fail}")
    return fail


if __name__ == "__main__":
    sys.exit(main())
