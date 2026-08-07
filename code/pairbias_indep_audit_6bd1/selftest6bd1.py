"""selftest6bd1 — constructions with KNOWN answers, run against this audit's own code.

Every construction here has an answer computable by hand. If the machinery is right, it
returns that answer; if it is wrong, at least one construction says so. Two of these
(S3, S6) are the ones that would have caught the two defects this audit shipped with
and kept (§D3, §D4): an instrument that reads no evidence and reports a clean screen.
"""

import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lib6bd1  # noqa: E402
from lib6bd1 import (  # noqa: E402
    C2, E_unif_footrule, E_unif_footrule_bruteforce, E_unif_footrule_sum,
    E_unif_inv, ancestors, dependents, edge_count, eps_c3ca_from_Einv,
    eps_spec_from_Einv, frozen_sup_Einv, read_ledger,
)

FAILS = []


def S(name, got, want):
    ok = got == want
    if not ok:
        FAILS.append(name)
    print(f"  [{'ok  ' if ok else 'FAIL'}] {name}")
    if not ok:
        print(f"          got  {got}\n          want {want}")


print("=" * 78)
print("selftest6bd1")
print("=" * 78)

# ---- S1. a synthetic ledger whose closure is known by hand.
SYN = """## 9. Claim ledger

| # | Claim | § | Label |
|---|---|---|---|
| 1 | a | 1 | **PROVEN** |
| 2 | b | 1 | **CONDITIONAL** on 1 |
| 3 | c | 1 | **CONDITIONAL** on claim 2 |
| 4 | d | 1 | **PROVEN** given 3 |
| 5 | e | 1 | **PROVEN** |

---
"""
p = HERE / "_syn_ledger.md"
p.write_text(SYN)
claims, edges, rej = read_ledger(p)
S("S1a synthetic ledger row count", len(claims), 5)
S("S1b synthetic edge count (1<-none, 2<-1, 3<-2, 4<-3, 5<-none)", edge_count(edges), 3)
S("S1c transitive dependents of claim 1", dependents(edges, 1), [2, 3, 4])
S("S1d claim 5 is isolated", ancestors(edges, 5), set())
p.unlink()

# ---- S2. a ledger row whose STATEMENT contains literal pipes inside math.
# This is the exact shape of Op-Form's claim 1 (`$|A|\\le n/2$`) that the first form of
# this reader DROPPED, giving 35 rows and 10 edges where mg-345e correctly had 36 and 11.
SYN2 = """## 9. Claim ledger

| # | Claim | § | Label |
|---|---|---|---|
| 1 | for $|A|\\le n/2$ the map is an identity | 2.1 | **PROVEN** |
| 2 | b | 1 | **CONDITIONAL** on 1 |

---
"""
p = HERE / "_syn_ledger2.md"
p.write_text(SYN2)
claims, edges, rej = read_ledger(p)
S("S2a pipe-in-math row is NOT dropped", sorted(claims), [1, 2])
S("S2b and its dependency edge survives", edge_count(edges), 1)
p.unlink()

# ---- S3. THE BLIND-SCREEN CONSTRUCTION. A path that does not exist must RAISE, never
# return an empty clean result. This is the defect at §D3/§D4 in miniature.
import b5_depth2_walk as W  # noqa: E402
try:
    W.pull(("docs/THIS-FILE-DOES-NOT-EXIST.md", "anything"))
    S("S3 nonexistent evidence path raises rather than reporting clean", "returned", "raised")
except SystemExit:
    S("S3 nonexistent evidence path raises rather than reporting clean", "raised", "raised")

# ---- S4. arithmetic with hand-computable answers.
S("S4a E_unif[footrule] at n=3 is 8/3 (all 6 permutations by hand)",
  E_unif_footrule_bruteforce(3), Fraction(8, 3))
S("S4b closed form agrees at n=3", E_unif_footrule(3), Fraction(8, 3))
S("S4c direct double sum agrees at n=3", E_unif_footrule_sum(3), Fraction(8, 3))
# n=3, m=C(3,2)=3 (the 3-antichain): E[inv] < 1, eps_spec < 6*1/8 = 3/4 = n/(n+1).
S("S4d eps_spec ceiling at n=3, m=3", eps_spec_from_Einv(frozen_sup_Einv(3, 3), 3),
  Fraction(3, 4))
S("S4e eps_c3ca ceiling at n=3, m=3 is (n-1)/(6n) = 1/9",
  eps_c3ca_from_Einv(frozen_sup_Einv(3, 3), 3), Fraction(1, 9))
S("S4f their ratio is 6n^2/(n^2-1) = 27/4 at n=3",
  Fraction(3, 4) / Fraction(1, 9), Fraction(27, 4))
S("S4g E_unif[inv] at n=4 is C(4,2)/2 = 3", E_unif_inv(4), Fraction(3))
S("S4h claim 26's 2/3 at n=4: (m/3)/E_unif[inv] with m=6",
  frozen_sup_Einv(4, int(C2(4))) / E_unif_inv(4), Fraction(2, 3))

# ---- S5. NEGATIVE construction: a WRONG conversion must be rejected.
S("S5a eps_spec is NOT 6E/n^2 at n=3",
  eps_spec_from_Einv(frozen_sup_Einv(3, 3), 3) == Fraction(6) * 1 / 9, False)
S("S5b 1/6 is NOT attained at any finite n",
  any(eps_c3ca_from_Einv(frozen_sup_Einv(n, int(C2(n))), n) == Fraction(1, 6)
      for n in range(2, 300)), False)

# ---- S6. THE CENSUS BLIND-SCAN CONSTRUCTION. `tracked` must see docs/ from HERE.
import b3_census_scope as B3  # noqa: E402
paths = B3.tracked("550a7f105c30273b06d376a60d720cd61b652499", "docs/")
S("S6 census sees docs/ when run from this subdirectory (>=100 files)",
  len(paths) >= 100, True)

# ---- S7. the dependency reader must not invent edges out of non-claim integers.
SYN3 = """## 9. Claim ledger

| # | Claim | § | Label |
|---|---|---|---|
| 1 | a | 1 | **PROVEN** given the sandwich `:318-324` |
| 2 | b | 1 | **CONDITIONAL** on `:360-364` being the intended statement |
| 3 | c | 1 | **PROVEN** (arithmetic on `:360-364`) |

---
"""
p = HERE / "_syn_ledger3.md"
p.write_text(SYN3)
claims, edges, rej = read_ledger(p)
S("S7 line-number references are NOT read as claim ids", edge_count(edges), 0)
p.unlink()

print()
print("=" * 78)
print("ALL SELFTESTS PASS" if not FAILS else f"FAILURES: {FAILS}")
print("=" * 78)
sys.exit(1 if FAILS else 0)
