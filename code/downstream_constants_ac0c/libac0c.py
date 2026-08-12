"""mg-ac0c — the downstream of L1b as DATA, plus the closure arithmetic.

TWO RULES THIS FILE ENFORCES, because they are the whole point of the ticket:

  1. **NO CONSTANT WITHOUT ITS STATUS.**  A constant is a `Const`, and a `Const` cannot be
     built without a `status`, a `scope` and a `source`.  There is no way to type a bare
     number into this instrument, which is the failure mode `STATE.md`'s standing rule at
     `:107` names: a figure quoted away from the population that makes it true.

  2. **NO FLOAT ON A DECISION PATH.**  Everything is `Fraction`.  `_check_exact` refuses
     anything else, and it is called on every value that reaches a verdict.

**THIS INSTRUMENT ENUMERATES NO POSETS AND MEASURES NOTHING.**  Every empirical or measured
input below is typed in from the document that measured it, with that document named in the
`source` field.  Agreement with those documents is *arithmetic reproduction* and is NEVER
corroboration of the underlying measurement — the same refusal `mg-7564`'s `lib7564` makes,
and for the same reason.
"""

from fractions import Fraction as F

# --------------------------------------------------------------------------- status vocabulary

# The ticket's four classes, plus the two riders the corpus's own kinds force us to keep.
PROVED = "PROVED"        # a theorem, unconditionally, at every n
PROVED_C = "PROVED*"     # a theorem CONDITIONAL on an open lemma — the condition is in `scope`
EMPIRICAL = "EMPIRICAL"  # a finite-population calibration or measurement (STATE.md kind `FP`)
ASSUMED = "ASSUMED"      # asserted with no warrant on the board
ABSENT = "ABSENT"        # no value, and no derivation route to one
REFUTED = "REFUTED"      # a witness kills it (STATE.md kind `FP✗`)

ORDER = [PROVED, PROVED_C, EMPIRICAL, ASSUMED, REFUTED, ABSENT]


def _check_exact(x, where):
    """Refuse anything that is not an exact rational (or the two sentinels)."""
    if x is None or x == "-":
        return x
    if isinstance(x, F):
        return x
    if isinstance(x, int):
        return F(x)
    raise TypeError(f"{where}: {x!r} is {type(x).__name__}, not an exact rational. "
                    f"This instrument refuses floats on a decision path.")


class Const:
    """One row of the enumeration.  Cannot be built without its status and its scope."""

    def __init__(self, key, step, what, status, value, scope, source, hole=None):
        if status not in ORDER:
            raise ValueError(f"{key}: unknown status {status!r}")
        if not scope:
            raise ValueError(f"{key}: a constant with no SCOPE is the defect this ticket exists "
                             f"to close (STATE.md:107)")
        if not source:
            raise ValueError(f"{key}: a constant with no SOURCE cannot be checked")
        if status != PROVED and hole is None:
            raise ValueError(f"{key}: status {status} requires an explicit PIN-or-HOLE clause "
                             f"(the ticket's step 2)")
        self.key, self.step, self.what = key, step, what
        self.status, self.scope, self.source, self.hole = status, scope, source, hole
        self.value = _check_exact(value, key) if not isinstance(value, str) else value

    def value_str(self):
        if isinstance(self.value, str):
            return self.value
        if self.value is None:
            return "—"
        return f"{self.value}" + (f" = {float(self.value):.6g}" if self.value.denominator != 1 else "")


# --------------------------------------------------------------------------- the enumeration
#
# Ordered as the argument runs: L1b's CONCLUSION is row 00, the contradiction is the last row.

ROWS = [
    Const("00", "L1b out", "`1 − λ_std ≤ ε_spec`, equivalently `E[inv_e] ≤ (ε_spec/6)(n²−1)` — the chain's INPUT",
          ABSENT, None,
          "row 8 is OPEN; ε_spec is whatever a proof of L1b would deliver, and no proof exists",
          "STATE.md row 8; Op-Form §6.2",
          hole="HOLE — but it is the WALL itself, not a downstream hole. Everything below prices it."),

    Const("01", "supply", "`ε_sup` — the best ε_spec PROVED today, from pair bias alone",
          PROVED, F(1),
          "sup over the frozen class; at each n the value is n/(n+1) < 1, APPROACHED not attained",
          "mg-6bc2 Claim 3.1; scope mg-832f Correction 2; STATE.md:21",
          hole=None),

    Const("02", "Step 3 / L2", "L2 as a DISJUNCTION — eigenvector monotone in `e`, OR directly produce a low-conductance prefix",
          ASSUMED, "-",
          "OPEN as a disjunction; no constant of its own",
          "STATE.md row 9; source `:560–566` read at second hand via mg-76b2 §2",
          hole="HOLE — an open lemma, not a constant. It gates rows 03 and 05."),

    Const("03", "Step 3 / L2(a)", "L2's FIRST disjunct — the eigenvector clause",
          REFUTED, "2/126 fail",
          "n = 6 data; refutes the FIRST disjunct only, NOT L2",
          "STATE.md row 9, scope repaired mg-3329",
          hole="PINNED at REFUTED-as-stated. The route that survives is the second disjunct, row 05."),

    Const("04", "Step 4", "the Cheeger square — `(Φ*)²/2 ≤ 1 − λ_std`, giving `Φ* ≤ √(2 ε_spec)`",
          PROVED, F(2),
          "the hard half of the Cheeger sandwich, at every poset; PROVEN in the source `:318–324`",
          "Op-Form §4.2; source read at second hand via mg-9461 §5.2",
          hole=None),

    Const("05", "Step 3 / L2(b)", "`K` — the prefix's own conductance constant on L2's SECOND disjunct; effective `C₃ = K²/2`",
          ABSENT, None,
          "L2's second disjunct; *low-conductance* occurs 5× in the 603-line source and is "
          "UNQUANTIFIED at every one (`:40`, `:325`, `:500`, `:525`, `:562`)",
          "mg-fa70 §12 (at source); carried mg-3329, STATE.md:179",
          hole="PINNED COARSELY at its only PROVED universal value — see `a2` §C. The pin is "
               "Δ₁ ≤ 1, i.e. K ≤ 1/√ε_spec, i.e. C₃ ≤ 1/(2ε_spec), at which the chain is VACUOUS."),

    Const("06", "L3 / Step 4", "`C₃^(III)` — the prefix-restriction loss in `Φ_pref ≤ √(2 C₃ ε_spec)`",
          PROVED_C, F(1),
          "CONDITIONAL ON L2's FIRST DISJUNCT — which row 03 records REFUTED as stated. "
          "Uniform in n within that condition; confirmed 1032/1032",
          "mg-76b2 §3, audited mg-94c3; STATE.md:179",
          hole="PINNED at 1 on a condition that is FP✗-false as stated. On the live branch "
               "(L2's second disjunct) it is row 05 and is ABSENT."),

    Const("07", "L3", "`C₃^gap` — `1 − ρ_pref ≤ C₃(1 − λ_std)`, chain (II)'s constant",
          EMPIRICAL, F(101654, 10000),
          "MEASURED; `1.500, 1.473, 1.990, 2.386` at n = 3..6 (out of regime) and `10.1654` at "
          "n = 25 on the staircase S_25, which IS in regime; `≥ 1` unconditionally",
          "mg-94c3 §3; mg-00b3 §0.4; joined mg-7564 §2",
          hole="PINNED at ≥ 10.1654 in regime by an exact witness — which is where chain (II) "
               "STOPS BEING A RELAXATION. Rising in n; no upper bound proved."),

    Const("08", "L3", "`C₃^cut` — `Φ*_pref/Φ*`, L3's own wording",
          EMPIRICAL, F(15, 8),
          "MEASURED, n ≤ 6, up to 15/8; must be SQUARED to meet chain (III)'s C₃",
          "mg-9461 §2.3 (read from mg-76b2 §7); within L2's population up to 10/9, mg-94c3 §3",
          hole="PINNED at its largest measured value 15/8 at n ≤ 6. FP: says nothing above n = 6."),

    Const("09", "L3 (row 10)", "best-cut-is-a-prefix",
          EMPIRICAL, "125/126",
          "n ≤ 6 data, and the population is NOT unanimous — one instance already fails",
          "STATE.md row 10",
          hole="PINNED at 125/126, n ≤ 6. FP — not usable against a minimal counterexample at all."),

    Const("10", "chain IV", "`c` — the literal capture fraction of the Prefix-capture conjecture",
          EMPIRICAL, F(9258259, 10000000),
          "MEASURED on three families; worst IN-REGIME value 0.9258259 at S_12. On the FULL "
          "population min c falls: 0.750, 0.618, 0.536, 0.453, 0.413 at n = 3..7 — below the "
          "threshold 1 − ε_leak = 4/5 at every one",
          "mg-00b3 §0.4; mg-81ff §5; joined mg-7564 §3",
          hole="PINNED at 0.9258259 in regime — but the class is NON-EMPTY AND UNENUMERABLE, so "
               "`c` over the class is UNMEASURED. And chain (IV) is gated on a conjecture that is "
               "NOT on the source's list of four main open lemmas."),

    Const("11", "Step 5", "`Φ_P(A) = Δ₁(A,B)` — the Step-4 → Step-5 conversion",
          PROVED, F(1),
          "an IDENTITY for 0 < |A| ≤ n/2, not a bound; no loss at all",
          "Op-Form Lemma 2.1 / Corollary 2.2",
          hole=None),

    Const("12", "Step 5 out", "`ε_leak` — Step 5's conclusion `Δ₁(A_k, A_kᶜ) ≤ ε_leak`",
          EMPIRICAL, F(1, 5),
          "an FP non-refutation: the largest ε at which mg-3ce3's `survives` predicate produced "
          "0 RED over 6681 posets. In STATE.md's own taxonomy it says NOTHING above the largest n "
          "checked, and it ERRS OPTIMISTIC in the required scope",
          "mg-e35c F5; mg-3ce3 envelope; identified as ε₀ at mg-9461 §4.1",
          hole="PINNED at 1/5 — and this IS row 13 wearing a decimal point. See row 13."),

    Const("13", "Step 6 / L4", "`ε₀^cons` — L4's threshold AS STEP 6 CONSUMES IT",
          ABSENT, None,
          "the class where it is consumed is minimal counterexamples, where disjunct (i) is FALSE "
          "BY HYPOTHESIS; on every poset anyone can exhibit (i) is TRUE at ε = 1, so the statement "
          "is satisfied vacuously — (i) fired at all 604 230 swept prefix cuts",
          "mg-3969 Claims 5.1 and 5.2; mg-9461 §4.2",
          hole="⭐ THE HOLE. No positive value can be bounded above without refuting the "
               "conjecture, and none below without proving it. NOT a constant awaiting "
               "measurement — the last lemma of the programme wearing a number's clothes."),

    Const("14", "Step 6 / L4", "`ε₀^unif(U_either)` — the refutable (i)-free surrogate, RESTRICTED scope",
          PROVED, F(17, 78),
          "an UPPER bound, over cuts at which BOTH sides are non-chain (335 496 cuts, n ≤ 7) — "
          "which is NOT the population Step 6 must survive",
          "mg-3969 §6, reproduced exactly by mg-d3c7 on a disjoint code path",
          hole=None),

    Const("15", "Step 6 / L4", "`ε₀^unif(U_either)` — the same surrogate, ARCHITECTURALLY REQUIRED scope",
          REFUTED, F(0),
          "AT LEAST ONE side non-chain — the population Step 6 must survive. REFUTED at every "
          "positive ε by an explicit n-free family, not merely capped",
          "mg-d3c7 §4 (chain c₁<…<c_{n−1} plus one isolated z; Δ₁ = (k+1)/((2k+1)k) → 0)",
          hole="PINNED at 0. This is the coarse, real, PROVED value the ticket asks for — and it "
               "is the value at which no positive ε_dem exists on any chain."),

    Const("16", "Step 6 / L4", "`F` — L4's modulus",
          ABSENT, None,
          "UNCONSUMED: Step 6 consumes no branch in which F appears, so F's VALUE does not gate "
          "the chain. mg-3ce3's fitted envelope F(ε) ≈ 0.32·ε^0.55 is EMPIRICAL and is a fit",
          "mg-345e; mg-3969 Claim 4.1; Op-Form §3.3",
          hole="HOLE, AND IT DOES NOT GATE. Recorded so nobody prices it: the split buys the "
               "demand side independence from F's value and does NOT buy it a number."),

    Const("17", "Step 6 / L4(i)", "branch (i) — `P` contains a 1/3-balanced pair",
          PROVED, "-",
          "TRUE at ε = 1 on every poset satisfying the conjecture; FALSE BY HYPOTHESIS at a "
          "minimal counterexample",
          "mg-3969 §5.1",
          hole=None),

    Const("18", "Step 6 / L4(ii)", "branch (ii) — remove/modify ≤ F(ε)n interface elements",
          REFUTED, F(0),
          "UNCONSUMABLE by Step 6's stated transfer for EVERY strictly positive modulus, "
          "unconditional, via the witness W*; the only escape F ≡ 0 makes L4 STRICTLY STRONGER",
          "mg-3af9, audited mg-c8c6; STATE.md row 11",
          hole="PINNED at 0 — no modulus rescues it. THIS IS THE STEP-6 HOLE, and it is "
               "INDEPENDENT of L1b."),

    Const("19", "Step 6 / L4(iii)", "branch (iii) AS LITERALLY STATED — balanced up to error F(ε)",
          REFUTED, F(0),
          "cannot produce the Step-6 contradiction for ANY F(ε) > 0, under either reading of "
          "*up to error F*; and minimality cannot be strengthened to supply interior slack — "
          "P₀ = {a<b} ⊔ {c} attains δ = 1/3 exactly, with ZERO slack",
          "Op-Form Claims 3.2 and 3.3; STATE.md row 11 (standalone universal refuted at every ε)",
          hole="PINNED at 0. The live reading is the F-FREE repaired (iii), which is rows 13–15."),

    Const("20", "minimality", "`δ(P[A]), δ(P[B]) ≥ 1/3` — each side is a proper induced subposet",
          PROVED, F(1, 3),
          "by minimality, at every n — UNLESS a side is a chain",
          "mg-3969 §5.1; STATE.md diagram E→F",
          hole=None),

    Const("21", "minimality", "the both-sides-chain escape",
          PROVED, F(2),
          "both sides chains ⟹ width(P) ≤ 2, where 1/3–2/3 is a THEOREM (Linial) — literature, "
          "not this corpus",
          "mg-3969 Remark 5.0",
          hole=None),

    Const("22", "contradiction", "a balanced pair in `P` contradicts `δ(P) < 1/3`",
          PROVED, F(1, 3),
          "the window [1/3, 2/3] has width 1/3 at EVERY n; the whole downstream of Step 5 is "
          "dimensionless",
          "Op-Form §3.2 support 2; STATE.md diagram E→F",
          hole=None),

    Const("23", "demand", "`ε_dem` on chain (I) ≡ (III) — `ε_leak²/(2C₃)`",
          PROVED_C, F(1, 50),
          "the relation is PROVEN; the NUMBER is C₃ = 1 (row 06, conditional) times ε_leak = 1/5 "
          "(row 12, EMPIRICAL) — so the number inherits the weakest of its inputs",
          "mg-9461 §5.1; Op-Form §4.3",
          hole="The RELATION is proved; the VALUE is EMPIRICAL-squared. Pinned across row 12's "
               "whole range in `a2` §A."),

    Const("24", "demand", "`ε_dem ≤ 2·ε_leak` — the CHAIN-FREE cap",
          PROVED_C, F(2, 5),
          "caps EVERY derivation of Step 5's conclusion, including one nobody has written. "
          "CONDITIONAL ON NON-VACUITY — the alternative branch is L1b at 2/5, i.e. the open "
          "lemma. Quoted at ε_leak = 1/5, which errs optimistic, so the cap is itself optimistic",
          "mg-7564 §4 and §4.1",
          hole="The cap is PROVED; its VALUE moves with row 12. 2/7 at the n ≤ 7 required-scope "
               "ceiling, and 0 at the required-scope uniform value."),
]

assert len({r.key for r in ROWS}) == len(ROWS), "duplicate row key"


# --------------------------------------------------------------------------- the four chains
#
# Each chain is a function ε_leak ↦ ε_dem, taken from mg-9461 §2.2 / mg-76b2 §6.  They are
# re-solved here from the stated Φ bound rather than copied as a table, so a mis-transcription
# fails the plug-back check in `a0`.

def chain_I_III(eps_leak, C3=F(1)):
    """Cheeger square paid, prefix restriction charged C₃:  ε_dem = ε_leak²/(2 C₃)."""
    _check_exact(eps_leak, "chain_I_III eps_leak"); _check_exact(C3, "chain_I_III C3")
    return eps_leak ** 2 / (2 * C3)


def chain_II(eps_leak, C3_gap):
    """Gap-form: Φ ≤ 1−ρ ≤ C₃(1−λ_std), so the square is never paid:  ε_dem = ε_leak/C₃^gap."""
    _check_exact(eps_leak, "chain_II eps_leak"); _check_exact(C3_gap, "chain_II C3_gap")
    return eps_leak / C3_gap


def chain_IV(eps_leak, c):
    """Literal capture ρ ≥ c·λ_std:  ε_dem = 1 − (1−ε_leak)/c, usable only for c > 1−ε_leak."""
    _check_exact(eps_leak, "chain_IV eps_leak"); _check_exact(c, "chain_IV c")
    if c <= 1 - eps_leak:
        return None                     # the chain does not exist at this c
    return 1 - (1 - eps_leak) / c


def cap(eps_leak):
    """mg-7564 §4: EVERY derivation of Step 5's conclusion obeys ε_dem ≤ 2·ε_leak."""
    _check_exact(eps_leak, "cap eps_leak")
    return 2 * eps_leak


def eps_sup(n):
    """The PROVED pair-bias supply at n:  ε_spec < n/(n+1), an EQUALITY for the information
    pair bias consumes (mg-6bc2 Claim 3.1)."""
    return F(n, n + 1)


def closes(supply, demand):
    """Does the chain close?  It closes iff what L1b delivers is at most what Steps 3–6 need."""
    if demand is None:
        return None
    _check_exact(supply, "closes supply"); _check_exact(demand, "closes demand")
    return supply <= demand


def wall(supply, demand):
    """The residual factor.  `None` for an infinite wall (demand 0 / chain absent)."""
    if demand is None or demand == 0:
        return None
    return supply / demand


def d3c7_leak(k):
    """mg-d3c7's refuting family, closed form: chain c₁<…<c_{n−1} plus one isolated z,
    A = {z, c₁, …, c_{k−1}}, n = 2k+1.  Δ₁ = (k+1)/((2k+1)k) → 0.

    ⚠️ THIS REPRODUCES AN ARITHMETIC FORMULA, NOT A POSET PROPERTY.  That every
    balanced-in-side pair is evicted at every k ≥ 3 is mg-d3c7's measurement and is NOT
    re-verified here."""
    return F(k + 1, (2 * k + 1) * k)
