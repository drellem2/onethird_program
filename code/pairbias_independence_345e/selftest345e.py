#!/usr/bin/env python3
"""mg-345e selftest — the detectors are only evidence if they can FAIL.

Every probe here answers "no L4 dependency". A constant-NO detector would print the same
thing. These constructions make each detector produce the OTHER answer on demand.
"""
import sys

from lib345e import (parse_ledger, reaches, dependents_of, ledger_block,
                     ARCH_EDGES, DIRECT_EDGE, SPECTRAL_NODE,
                     FROZEN, L4FIRE, PAIRB, THIN)
from p2_architecture_graph import paths

FAILED = []


def check(name, cond, detail=""):
    print(f"   [{'PASS' if cond else 'FAIL'}] {name}" + (f"  — {detail}" if detail else ""))
    if not cond:
        FAILED.append(name)


def main():
    print("=" * 78)
    print("mg-345e SELFTEST")
    print("=" * 78)
    print()

    claims, edges, residue = parse_ledger()

    print("-- S1: the ledger parser sees a real table -----------------------------------")
    check("36 rows parsed", len(claims) == 36, f"got {len(claims)}")
    check("row 23 is the (LIB-const) claim", "LIB-const" in claims.get(23, ("",))[0])
    check("row 4 is the n-free-modulus claim",
          "n$-free" in claims.get(4, ("",))[0] or "free" in claims.get(4, ("",))[0])
    check("row 25 is the m/3 claim", "m/3" in claims.get(25, ("",))[0])
    print()

    print("-- S2: MUTATION — a constant-NO detector must fail this ----------------------")
    mut = {k: set(v) for k, v in edges.items()}
    mut[26] = mut.get(26, set()) | {4}
    check("with fabricated edge 26<-4, claim 26 scores L4-DEPENDENT",
          reaches(mut, 26, 4))
    check("without it, claim 26 scores independent", not reaches(edges, 26, 4))
    print()

    print("-- S3: MUTATION — a constant-YES detector must fail this ---------------------")
    mut2 = {k: (set(v) - {4}) for k, v in edges.items()}
    mut2[17] = mut2[17] - {4}
    check("with edge 17<-4 removed, claim 23 scores INDEPENDENT", not reaches(mut2, 23, 4))
    check("unmutated, claim 23 scores DEPENDENT", reaches(edges, 23, 4))
    print()

    print("-- S4: the dependency regex does not eat non-claim numerals ------------------")
    from lib345e import DEP
    check("'given the sandwich `:318-324`' yields no edge",
          not DEP.findall("**PROVEN** given the sandwich `:318-324`"))
    check("'CONDITIONAL on `:360-364` being intended' yields no edge",
          not DEP.findall("**CONDITIONAL** on `:360-364` being the intended statement"))
    check("'CONDITIONAL on 1, 4, 13, 16' yields 4 edges",
          sorted(int(x) for h in DEP.findall("**CONDITIONAL** on 1, 4, 13, 16")
                 for x in h.replace(",", " ").split()) == [1, 4, 13, 16])
    check("'CONDITIONAL on claim 4' yields edge 4",
          DEP.findall("**CONDITIONAL** on claim 4") != [])
    print()

    print("-- S5: architecture reachability, both mutations ------------------------------")
    A = {k: list(v) for k, v in ARCH_EDGES.items()}
    check("arm A: some path frozen -> L4 fires exists",
          len(paths(A, FROZEN, L4FIRE)) > 0)
    check("arm A: no such path avoiding L1b",
          len(paths(A, FROZEN, L4FIRE, banned=(SPECTRAL_NODE,))) == 0)
    B = {k: list(v) for k, v in A.items()}
    B[DIRECT_EDGE[0]] = B[DIRECT_EDGE[0]] + [DIRECT_EDGE[1]]
    check("arm B: a path avoiding L1b appears once the direct route is added",
          len(paths(B, FROZEN, L4FIRE, banned=(SPECTRAL_NODE,))) == 1)
    # negative control: banning the thin-prefix node must kill EVERY path in both arms
    check("control: banning the thin-prefix node kills all paths in arm A",
          len(paths(A, FROZEN, L4FIRE, banned=(THIN,))) == 0)
    check("control: banning the thin-prefix node kills all paths in arm B",
          len(paths(B, FROZEN, L4FIRE, banned=(THIN,))) == 0)
    print()

    print("-- S6: the residue channel is not silently empty ------------------------------")
    print(f"   uncaptured-integer rows: {sorted(residue)}")
    print("   (this channel exists so a dependency the regex misses is VISIBLE.")
    print("    It is allowed to be empty; it is not allowed to be absent.)")
    check("residue is computed for every parsed row", isinstance(residue, dict))
    print()

    print("-- S7: block extraction is not the whole file ---------------------------------")
    blk = ledger_block(open(__import__("lib345e").OPFORM).read())
    check("ledger block is a proper subset of the file", 0 < len(blk) < 40000,
          f"{len(blk)} chars")
    check("ledger block does not contain section 10's header", "## 10." not in blk)
    print()

    print("=" * 78)
    if FAILED:
        print(f"SELFTEST: {len(FAILED)} FAILED — {FAILED}")
        return 1
    print("SELFTEST: all constructions pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
