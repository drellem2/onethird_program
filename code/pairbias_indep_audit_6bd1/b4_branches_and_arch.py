"""B4 — the two places mg-345e's §3 argument is weaker than its label.

  (a) THE BRANCH TABLE. §3's arm-B point 1 says "L4 fired from a thin prefix reached
      without L1b contradicts delta(P) < 1/3 OUTRIGHT". That is a claim about L4-AS-
      STATED, which is a THREE-branch disjunction. Enumerate the branches and ask, for
      each, whether the Step-6 contradiction follows — using only authorities mg-345e
      itself cites elsewhere in the same document.

  (b) THE ARCHITECTURE GRAPH'S INFORMATION CONTENT. §3 arm A prints "1 path / 0 paths"
      as if a search happened. Rebuild the graph from mg-345e's own §3 code block and
      measure how much the traversal could possibly have decided.
"""

# ------------------------------------------------------------- (a) branch table
#
# Each row: (branch, does the Step-6 contradiction follow?, authority, and whether
# that authority is one mg-345e cites in its OWN document).

BRANCHES = [
    ("(i)   P contains a 1/3-balanced pair",
     True,
     "definition of delta(P): a 1/3-balanced pair IS delta(P) >= 1/3",
     "yes — mg-345e §5.1 row (i)"),
    ("(ii)  remove/modify <= F(eps)n interface elements -> P[A] (+) P[B]",
     False,
     "mg-3af9 (audited mg-c8c6): unconsumable by Step 6's stated transfer for EVERY "
     "strictly positive F, sub-linear included",
     "yes — mg-345e §5.1 row (ii), cited verbatim with the 'strictly positive' quantifier"),
    ("(iii) AS STATED: a balanced pair remains balanced up to error F(eps)",
     False,
     "Op-Form Claim 3.2 = ledger claim 8, labelled PROVEN: branch (iii) as literally "
     "stated cannot produce the Step 6 contradiction for any F > 0, under either reading",
     "yes — mg-345e reads the same ledger in §2 and §4"),
    ("(iii*) REPAIRED: a balanced pair remains IN [1/3,2/3] in P",
     True,
     "Op-Form §3.4's recommended repair (mg-e35c F5); this is the predicate mg-3ce3 tests",
     "yes — mg-345e §5.1 row (iii)"),
]

print("=" * 78)
print("B4(a) — does 'L4 fires' imply the Step-6 contradiction?")
print("=" * 78)
print()
print("mg-345e §3, arm B, point 1, verbatim:")
print('   "L4 fired from a thin prefix reached without L1b contradicts `delta(P) < 1/3`')
print('    outright - the frozen class is empty, and every statement about minimal')
print('    counterexamples is vacuously true, `eps_spec` included."')
print()
print("L4-AS-STATED is a three-way disjunction. Branch by branch:")
print()
for name, ok, why, cited in BRANCHES:
    print(f"  {name}")
    print(f"      contradiction follows : {'YES' if ok else 'NO'}")
    print(f"      authority             : {why}")
    print(f"      cited by mg-345e      : {cited}")
    print()

stated = [b for b in BRANCHES if not b[0].startswith("(iii*)")]
yes = sum(1 for b in stated if b[1])
print(f"  -> from L4-AS-STATED the contradiction follows on {yes} of {len(stated)}"
      f" branches.")
print("  -> so 'contradicts delta(P) < 1/3 OUTRIGHT' is TRUE ONLY ON BRANCH (i).")
print("     On (ii) it is blocked by mg-3af9 — the same result mg-345e's own §5.1 leans")
print("     on — and on (iii)-as-stated by Op-Form's own PROVEN ledger claim 8.")
print()
print("  WHAT THIS DOES AND DOES NOT TOUCH:")
print("   * It does NOT touch the (A) INDEPENDENT verdict. §2 establishes independence")
print("     by EXHIBITING an L4-free derivation; §3 only argues independence is FORCED.")
print("   * It does NOT reopen §3's conclusion either, because §3's point 2 — the")
print("     direct-prefix route reaches only Delta_1 <= 2/3 against eps_leak ~ 0.20 —")
print("     is independent of point 1 and closes the escape on its own.")
print("   * It DOES mean point 1 is not available as written: an escape that became")
print("     live would not automatically 'dissolve' the question, because L4-as-stated")
print("     firing into (ii) empties nothing.")
print()

# --------------------------------------------- (b) the architecture graph's content
print("=" * 78)
print("B4(b) — how much did §3's reachability computation decide?")
print("=" * 78)
print()

FROZEN, PAIRB, LIB1B = "frozen", "pair bias", "L1b conclusion"
THIN, L4FIRE, BAL, CONTRA = "thin prefix", "L4 fires", "balanced pair", "contradiction"

# transcribed from mg-345e's own lib345e.ARCH_EDGES, unchanged
ARCH = {FROZEN: [PAIRB], PAIRB: [LIB1B], LIB1B: [THIN], THIN: [L4FIRE],
        L4FIRE: [BAL], BAL: [CONTRA]}


def paths(g, src, dst, banned=()):
    if src == dst:
        return 1
    return sum(paths(g, s, dst, banned) for s in g.get(src, []) if s not in banned)


print("out-degree of every node in mg-345e's ARCH_EDGES:")
for k in ARCH:
    print(f"    {k:<18} -> {len(ARCH[k])}")
print(f"    {CONTRA:<18} -> 0")
print()
print("Every node has out-degree <= 1: the graph is a PATH, not a network.")
print("So `0 paths avoiding X` is true of EVERY interior node, not just of L1b —")
print("which is what a traversal over a path graph must return. Exhibited:")
print()
for node in (PAIRB, LIB1B, THIN):
    n_all = paths(ARCH, FROZEN, L4FIRE)
    n_ban = paths(ARCH, FROZEN, L4FIRE, banned=(node,))
    print(f"    paths frozen -> L4 fires            : {n_all}")
    print(f"    paths frozen -> L4 fires avoiding `{node}` : {n_ban}")
print()
print("  -> the traversal has ZERO discriminating power: it returns the same answer for")
print("     `pair bias` and for `thin prefix` as it does for `L1b conclusion`.")
print("     ALL of §3 arm A's content is in the TRANSCRIPTION — i.e. in the claim that")
print("     the architecture has no OTHER route to a thin prefix. mg-345e declares the")
print("     transcription as its Defect 3 and labels the conclusion")
print("     '[PROVEN, on the hand-transcribed step graph]', which is honest; what it")
print("     does not say is that the machine added nothing to it.")
print()
print("  AND THE REAL WORK IS ELSEWHERE AND IS GOOD: mg-345e went looking for the")
print("  missing edge itself (mg-00b9 / mg-2de0, the direct-prefix route) rather than")
print("  trusting the transcription's completeness. That search is the part of §3 that")
print("  carries information, and it is a hand result, not a machine one.")
print()
print("=" * 78)
