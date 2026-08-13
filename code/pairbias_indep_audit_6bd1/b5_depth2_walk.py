"""B5 — THE ONE-LEVEL-DOWN WALK. This is the check mg-6bd1 exists to run.

mg-345e exhibits a dependency list and observes L4 is not on it. The ticket for this
audit says that is not enough: an argument can be independent of L4 BY NAME while
consuming a lemma that is itself conditional on L4. So: for each of the five inputs
mg-345e names, find its RECORDED STATEMENT in the corpus, scan it for every token by
which an L4 dependence could enter, and print the hits so a disagreement is locatable.

THE MACHINE PART OF THIS IS A SCREEN, NOT A PROOF, AND IT IS LABELLED AS ONE. A token
scan over a recorded statement cannot see a dependence that the record does not write
down. The hand adjudication is printed alongside each row and it is the part that
decides. mg-6bd1's P14 binds it: to call an input L4-dependent I must exhibit the
INEQUALITY OR STEP that fails when L4 is withdrawn — naming a document is not enough.
"""

import subprocess

import lib6bd1 as L  # mg-20ee: the corpus is read AT A DECLARED COMMIT
from pathlib import Path

# DEFECT OF THIS SCRIPT, KEPT IN THE SOURCE (mg-6bd1 §D4) — THE SAME FLATTERING SHAPE
# AS §D3, IN A SECOND INSTRUMENT. The first form passed bare relative paths ("STATE.md")
# to grep while running from this subdirectory. grep found no file, returned nothing, and
# the screen printed "L4-indicator tokens: NONE" for every input — i.e. IT CONFIRMED THE
# VERDICT UNDER AUDIT BY FAILING TO OPEN THE EVIDENCE. Caught only because input 3's row
# was known by hand to sit next to a blockquote full of L4 tokens. Paths are now anchored
# to the repo root, and the screen additionally prints the naive-grep confound.
REPO = Path(__file__).resolve().parents[2]

# Every token by which L4 could enter an argument. Deliberately over-broad: a screen
# that misses is worse than one that over-reports, because over-reports get read.
L4_TOKENS = ["L4", "Δ₁", "Delta_1", "\\Delta_1", "near-ordinal-sum", "ordinal sum",
             "modulus", "F(ε)", "F(\\varepsilon)", "prefix", "Cheeger", "C₃", "C_3",
             "Step 6", "interface element", "leak"]

# input -> (human name, where its statement is recorded, how to pull that record)
INPUTS = [
    ("1. inv_e(sigma), the count of incomparable pairs flipped against e",
     "STATE.md glossary",
     ("STATE.md", "Kendall distance: incomparable pairs flipped vs the distinguished")),
    ("2. the frozen hypothesis delta(P) < 1/3",
     "the minimal-counterexample condition — a HYPOTHESIS, not a lemma",
     None),
    ("3. coherence: the >2/3 majorities cohere into a single linear order e (mg-61bb)",
     "STATE.md row 'INERT · proven (probe A, mg-61bb)'",
     ("STATE.md", "INERT · proven (probe A, mg-61bb)")),
    ("4. linearity of expectation",
     "not in this corpus — it is measure theory",
     None),
    ("5. mg-210d's master bound 1-lambda_std <= 6E[inv]/(n^2-1)",
     "docs/state-history/attempt-mg-210d.md, 'Master bound (re-derived from scratch)'",
     ("docs/state-history/attempt-mg-210d.md", "Master bound (re-derived from scratch")),
]

ADJUDICATION = {
    1: ("NOT L4-dependent. A DEFINITION. It names the distinguished order `e`, which is\n"
        "       supplied by input 3, and nothing else. Withdrawing L4 changes no symbol in it."),
    2: ("NOT L4-dependent. It is the HYPOTHESIS of the statement being proved — the\n"
        "       minimal-counterexample condition of the 1/3-2/3 programme. It is upstream of\n"
        "       the entire architecture including L4, not downstream of anything."),
    3: ("NOT L4-dependent, AND IT IS PROVED TWICE INDEPENDENTLY. STATE.md's mg-61bb row\n"
        "       records it as 'a logical consequence of delta<1/3 (same poset class - shrinks\n"
        "       it by zero)', whose only residual is subadditivity of balances\n"
        "       beta(u,w) <= beta(u,v)+beta(v,w). mg-210d's own record re-derives the same\n"
        "       fact from the other side as a 'free by-product': 'frozen => the majority\n"
        "       relation is automatically a linear extension, and 1/3 is exactly the\n"
        "       threshold'. Neither derivation mentions a cut, a prefix, or a modulus.\n"
        "       WITHDRAW L4 AND NOTHING IN EITHER ARGUMENT CHANGES."),
    4: ("NOT L4-dependent. ZFC."),
    5: ("NOT L4-dependent. The bound is 1-lambda_std <= 3E[footrule]/(n^2-1) <=\n"
        "       6E[inv]/(n^2-1). Its two steps are (a) a spectral estimate on lambda_std\n"
        "       against expected displacement, and (b) Diaconis-Graham's D <= 2I, a finite\n"
        "       combinatorial identity about permutations. Op-Form 6.1 hand-checks (b) and\n"
        "       the antichain equality separately; mg-c4f5 re-derived the whole bound by\n"
        "       hand at 0 violations over 101,658 posets n <= 7. NO STEP TAKES A CUT, A\n"
        "       PREFIX, A MODULUS OR A THRESHOLD AS INPUT. Note also that mg-345e marks this\n"
        "       input '(only for the lambda_std rendering)': the ticket's own (LIB-const)\n"
        "       form E[inv_e] <= (eps/6)(n^2-1) does not need it at all."),
}


def pull(spec):
    """The ONE recorded row this input's statement lives in. Anchored to the repo root
    and matched on a distinctive substring of the row itself, not on the mg-id — an
    mg-id grep hits every row that merely CITES the result, including STATE.md's L1b
    blockquote, which is saturated with L4 tokens and would poison the screen."""
    if spec is None:
        return [], 0
    path, pat = spec
    # mg-20ee: read AT A DECLARED COMMIT.  The §D4 defect kept above was the
    # screen running BLIND; this is the same screen running on bytes that move
    # under it, so the addresses it prints were valid at no stated commit.
    text = L.read_at(path)
    if not text:
        raise SystemExit(f"BUG: {path} is empty at {L.AT} — this screen must not run blind")
    rows = [f"{i}: {l}" for i, l in enumerate(text.split("\n"), 1) if pat in l]
    naive = 0
    if "mg-" in pat:
        mgid = [t for t in pat.split() if t.startswith("mg-")][0].strip("()")
        naive = sum(1 for l in text.split("\n") if mgid in l)
    return rows, naive


print("=" * 78)
print("B5 — mg-345e's dependency list, walked ONE LEVEL DOWN")
print("=" * 78)
print()
print(L.asof_stamp(), end="")
print()
print("SCREEN (machine) + ADJUDICATION (hand). The screen cannot see an unrecorded")
print("dependence; the adjudication is what decides, and it is bound by mg-6bd1's P14:")
print("naming a document is not enough — the failing step must be exhibited.")
print()

any_dep = False
for idx, (name, where, spec) in enumerate(INPUTS, 1):
    print(f"  INPUT {name}")
    print(f"     recorded at : {where}")
    recs, naive = pull(spec)
    hits = set()
    for line in recs:
        for t in L4_TOKENS:
            if t in line:
                hits.add(t)
    if spec is None:
        print("     screen      : n/a — not a corpus artefact (see adjudication)")
    else:
        if not recs:
            raise SystemExit(f"BUG: no row matched for input {idx} — screen ran blind")
        print(f"     rows matched: {len(recs)}"
              + (f"   (a naive mg-id grep would have matched {naive} rows, including"
                 f" STATE.md's L1b blockquote — CONFOUND AVOIDED)" if naive else ""))
        print(f"     screen      : L4-indicator tokens in the recorded statement:"
              f" {sorted(hits) if hits else 'NONE'}")
        for line in recs:
            print(f"                   | {line[:150]}")
    print(f"     ADJUDICATION: {ADJUDICATION[idx]}")
    print()

print("-" * 78)
print("THE CHAIN I WALKED, END TO END, WITH NOTHING ELIDED:")
print("-" * 78)
print("""
    delta(P) < 1/3                                        [HYPOTHESIS]
        |
        +--(mg-61bb, and independently mg-210d's by-product)--> e exists and is canonical
        |       inputs: subadditivity of balances. No cut. No modulus.        [L4-FREE]
        |
        +--> for each incomparable pair {i<j}: Pr[j <_sigma i] < 1/3          [HYPOTHESIS]
                |
                +--(linearity of expectation)--> E[inv_e] = sum Pr[...] < m/3 [L4-FREE]
                        |
                        +--(m <= C(n,2), arithmetic)--> E[inv_e] < n(n-1)/6   [L4-FREE]
                                |
                                +--( / (n^2-1)/6 )--> eps_spec < n/(n+1) -> 1 [L4-FREE]
                                +--( / n^2       )--> eps_c3ca < (n-1)/(6n)
                                                                     -> 1/6   [L4-FREE]

    NOT ON THIS CHAIN, ANYWHERE: Delta_1, a cut, a prefix, Cheeger, C_3, Step 6,
    L4's F, L4's threshold, mg-3ce3's calibration, mg-3af9's branch-(ii) result.
""")
print("  The last two lines of the chain are the SAME division applied twice. That is")
print("  the whole of B2/C4, and it is why mg-345e's own headline number IS the 1/6 its")
print("  §6 says it has not attempted.")
print()

print("-" * 78)
print("THE ONE PLACE L4 IS GENUINELY ONE LEVEL DOWN — AND IT IS ON THE OTHER SIDE")
print("-" * 78)
print("""
  Op-Form's ledger records:  23 <- 18 <- 17 <- 4 = "L4's F is n-free".
  Claim 23 IS (LIB-const) — but as the ARCHITECTURE'S REQUIREMENT, i.e. the claim that
  a constant UNIFORM IN n is the right thing to want. That is a DEMAND statement.

  So the honest one-level-down finding is:
    * the INEQUALITY E[inv_e] <= (c/6)(n^2-1) with c uniform in n : L4-FREE (chain above)
    * the claim that a uniform-in-n c is what the architecture NEEDS : L4-CONDITIONAL,
      via ledger 23 <- 18 <- 17 <- 4, and claim 4 literally names F's n-freeness.

  mg-345e's supply/demand split puts exactly this cut in exactly this place (its §1
  table, and its own P1 predicted 'claim 23 in dependents-of-4'). THE SPLIT SURVIVES
  THE WALK.

  BUT ONE STEP OF ITS §5.1 REFINEMENT NEEDED CHECKING AND IT HOLDS: mg-345e says the
  demand needs L4's THRESHOLD, not its MODULUS - while Op-Form derives the threshold's
  n-freeness FROM the modulus reading (§3.2 support 1). If that were the only support,
  mg-345e's refinement would be circular. It is not: Op-Form §3.2 support 2 is
  F-FREE - 'nothing downstream of L4 contains an n ... the window [1/3,2/3] has width
  1/3 at every n ... the entire downstream of Step 5 is dimensionless'. That argument
  never mentions F. SO THE THRESHOLD'S n-FREENESS HAS AN F-FREE SUPPORT AND mg-345e'S
  NARROWER READING IS AVAILABLE. mg-345e does not exhibit this; it is exhibited here.
""")
print("=" * 78)
print("RESULT: 0 of 5 named inputs is L4-dependent at depth 2. VERDICT (A) SURVIVES.")
print("=" * 78)
