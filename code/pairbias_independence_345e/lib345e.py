"""mg-345e — shared machinery for the pair-bias / L4 independence question.

Two graphs live here and they are DIFFERENT KINDS OF OBJECT. Keep them apart:

  * `parse_ledger` / `ledger_edges` read the *recorded* dependency clauses out of
    mg-88bd's claim ledger (`docs/OneThird-lambda-std-Operative-Form.md` §9). This is a
    measurement of a document, not of the mathematics. A claim whose label understates its
    true dependencies is scored independent here, and that limit is printed at every use.

  * `ARCH_EDGES` is HAND-ENCODED from the architecture's stated steps. It is a transcription
    and is labelled as one. Its purpose is to answer a reachability question I would
    otherwise have to assert: can L4's hypothesis be reached without passing through L1b?
"""

import re
from fractions import Fraction
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OPFORM = REPO / "docs" / "OneThird-lambda-std-Operative-Form.md"

# ---------------------------------------------------------------- ledger parsing

LEDGER_HEADER = "## 9. Claim ledger"


def ledger_block(text):
    """The §9 table body, from its header to the next horizontal rule."""
    i = text.index(LEDGER_HEADER)
    rest = text[i + len(LEDGER_HEADER):]
    j = rest.find("\n---")
    return rest if j < 0 else rest[:j]


ROW = re.compile(r"^\|\s*(\d+)\s*\|(.*)\|(.*)\|(.*)\|\s*$")

# `CONDITIONAL on 18, 21`, `PROVEN given 28`, `CONDITIONAL on claim 4`.
# Requires a digit immediately after the keyword (plus optional "claim"), so
# `on \`:360-364\`` and `given the sandwich` do not match.
# NOTE the quantifier is GREEDY. It was lazy in the first form of this file, which
# truncated `on 1, 4, 13, 16` to `1, 4` and silently dropped two dependency edges —
# including 17 <- 13. Caught by selftest construction S4, not by eye. Kept as a rule:
# a dependency parser that under-reads is exactly the failure this ticket is about.
DEP = re.compile(r"\b(?:on|given)\s+(?:claims?\s+)?(\d[\d,\s]*\d|\d)(?![\d–—-])")
NUMS = re.compile(r"\d+")

# every bare integer in a label cell that is NOT part of a captured dependency clause and
# NOT one of these is surfaced for hand adjudication rather than silently dropped.
NOT_A_CLAIM_REF = re.compile(
    r"(?:mg-[0-9a-f]{4})|(?:\d+\s*[×x]\s*10)|(?:10[⁴⁵⁻³²])"
    r"|(?::\d)|(?:\d+\.\d)|(?:n\s*[≤<>=]\s*\d)|(?:100×)|(?:\bF\d\b)|(?:\bA\d\b)"
)


def parse_ledger(text=None):
    """-> (claims: {id: (statement, section, label)}, edges: {id: set(ids)}, residue)."""
    if text is None:
        text = OPFORM.read_text()
    claims, edges, residue = {}, {}, {}
    for line in ledger_block(text).splitlines():
        m = ROW.match(line)
        if not m:
            continue
        cid = int(m.group(1))
        statement, section, label = (g.strip() for g in m.group(2, 3, 4))
        claims[cid] = (statement, section, label)
        dep = set()
        for hit in DEP.finditer(label):
            dep.update(int(v) for v in NUMS.findall(hit.group(1)))
        edges[cid] = dep
        # uncaptured integers in the label, for hand adjudication
        masked = DEP.sub(" ", NOT_A_CLAIM_REF.sub(" ", label))
        left = sorted({int(v) for v in NUMS.findall(masked)})
        if left:
            residue[cid] = left
    return claims, edges, residue


def reaches(edges, start, target):
    """Is `target` reachable from `start` along dependency edges?"""
    seen, stack = set(), [start]
    while stack:
        c = stack.pop()
        for d in edges.get(c, ()):
            if d == target:
                return True
            if d not in seen:
                seen.add(d)
                stack.append(d)
    return False


def dependents_of(edges, target):
    """Every claim that transitively depends on `target`."""
    return sorted(c for c in edges if reaches(edges, c, target))


# ---------------------------------------------------------- architecture graph
# HAND-ENCODED TRANSCRIPTION of the stated architecture. Sources named per edge.

FROZEN = "frozen: delta(P) < 1/3"
PAIRB = "pair bias: E[inv_e] < m/3"
LIB1B = "L1b conclusion: 1 - lambda_std <= eps_spec"
THIN = "thin prefix: Delta_1(A_k) <= eps_leak"
L4FIRE = "L4 fires: (i) or (ii) or (iii)"
BAL = "P has a balanced pair"
CONTRA = "contradiction with delta(P) < 1/3"

ARCH_EDGES = {
    # step                            -> consequences            (source)
    FROZEN: [PAIRB],                  # Op-Form Claim 6.1, PROVEN
    PAIRB: [LIB1B],                   # mg-210d master bound, Op-Form 6.1/6.3
    LIB1B: [THIN],                    # Steps 2-5: Cheeger + L2/L3 prefix restriction
    THIN: [L4FIRE],                   # L4's hypothesis IS Delta_1 <= eps
    L4FIRE: [BAL],                    # Step 6 stated transfer
    BAL: [CONTRA],
}

# The direct-prefix route (mg-00b9 Lemma A/B, REPAIRED by mg-2de0) converts an inversion
# bound to a prefix-thinness bound with NO spectral statement. Headline constant 2/3.
DIRECT_EDGE = (PAIRB, THIN)

SPECTRAL_NODE = LIB1B
