"""Per-row relocation spec for mg-34bf.

POLICY (applied uniformly; the prose version is in docs/state-history/README.md).

A passage RELOCATES to the row's history file when it is:
  (a) a report of what this row, this document or a prior ledger row USED TO SAY, or a
      strike / retirement / correction of it;
  (b) an adjudication of a deliverable or an audit (over-wide, BROKEN-as-labelled, struck,
      downgraded, mislabelled), an audit tally, or a nested audit-provenance chain;
  (c) a derivation, construction, enumeration or numeric evidence supporting a claim that
      is asserted elsewhere in the row;
  (d) a defect-mechanism note (why a defect survived, or what let it happen).
(a), (b) and (d) go to the numbered history sections; (c) goes to the supporting record.

A passage STAYS in the row when it is a status or verdict headline, a live claim with its
scope and population, a citation, an open item, an explicit instruction, or the honest net.

Corrections to an EXTERNAL source document (the .tex sketch) are live facts about that
source and stay in the row.  Only corrections to text inside this programme's own record
relocate -- that is the adjacency the ticket forbids.

Columns 1 and 2 (verdict, attempt) are untouched throughout.

`inserts` entries are (anchor_passage, heading_label, row_statement).  The builder appends
the link to `row_statement` and opens a numbered history section at `heading_label`; every
relocated history passage is filed under the nearest preceding anchor.
"""

SPEC = {
 89: dict(
   file="ledger-row-11-L4.md",
   title="Full ledger row 11 — L4 near-ordinal-sum stability",
   row_ref="`STATE.md` § *Full ledger*, row 11",
   history=["2.3", "2.4"],
   support=[],
   inserts=[("2.3", "the superseded conditional form, and the struck \"with no repair available\"",
     " **The conditional form this clause used to carry is SUPERSEDED and the earlier "
     "*\"with no repair available\"* is STRUCK at this site; the candidate repair **(IB)** is "
     "recorded in repaired form at the mg-63e3 row of the attempt index**")],
 ),
 114: dict(
   file="attempt-mg-c47a-drop.md",
   title="Attempt index — DROP (tractability only): width ≥ 4, n ≥ 10 residual gap (mg-c47a)",
   row_ref="`STATE.md` § *Attempt index*, the **DROP (tractability only)** row",
   history=["3.2", "3.3", "3.4"],
   support=[],
   inserts=[("3.2", "the deliverable's rejected leading argument, and two corrected scope claims",
     "**Do not repeat the reason the deliverable led with: that inference is REJECTED, and two "
     "further scope claims of the deliverable are corrected**")],
 ),
 124: dict(
   file="attempt-mg-48ab.md",
   title="Attempt index — GREEN-partial · diagnostic (mg-48ab): AF equality-case vs the frozen hypothesis",
   row_ref="`STATE.md` § *Attempt index*, the **GREEN-partial · diagnostic (mg-48ab)** row",
   history=["3.5"],
   support=[],
   inserts=[("3.5", "corrects mg-a1ec Finding 5.4; quarantines the misattributed Aires–Kahn step",
     "**Corrects mg-a1ec Finding 5.4 and quarantines the misattributed Aires–Kahn step**")],
 ),
 130: dict(
   file="attempt-mg-210d.md",
   title="Attempt index — SOUND negative · actionable (mg-210d): best constant lower bound on λ_std",
   row_ref="`STATE.md` § *Attempt index*, the **SOUND negative · actionable (mg-210d)** row",
   history=["3.8", "3.9", "3.10", "3.11", "3.15"],
   support=[],
   inserts=[("3.8", "the retired \"honest caveat\", and why the row's own verdict is untouched by the retirement",
     "**The \"honest caveat\" this row used to carry is RETIRED (mg-88bd, audited mg-e35c — F8; "
     "see that row), and the verdict *\"best constant this route proves = 0\"* is untouched by "
     "the retirement**")],
 ),
 131: dict(
   file="attempt-mg-a58f.md",
   title="Attempt index — RED-for-lever · AMBER-redirect (mg-a58f): the (B-bias) O(1) locality lemma",
   row_ref="`STATE.md` § *Attempt index*, the **RED-for-lever · AMBER-redirect · CORRECTS MERGED WORK (mg-a58f)** row",
   history=["3.2", "3.3", "3.4", "3.5", "3.11", "3.12", "3.13", "3.17"],
   support=["3.15"],
   inserts=[
     ("3.2", "the first three of the four corrections (this document's § The single lemma to prove, ledger row 8, mg-dbd1 §2.1, the (A)+(B) route's advertised advantage)",
      "**Four corrections landed against prior text; the fourth is current state and stays here**"),
     ("3.11", "the limit-vs-rate scoping question, and its answer",
      "**The limit-vs-rate scoping question this row raised is ANSWERED (mg-88bd, audited "
      "mg-e35c) at the mg-88bd row below**"),
   ],
 ),
 132: dict(
   file="attempt-mg-88bd.md",
   title="Attempt index — OVERSTATED · core CONFIRMED-conditionally · RE-SHAPES (R) (mg-88bd): the operative λ_std form",
   row_ref="`STATE.md` § *Attempt index*, the **OVERSTATED · core CONFIRMED-conditionally · RE-SHAPES (R) (mg-88bd)** row",
   history=["3.4", "3.5", "3.13", "3.15", "3.19", "3.27", "3.28", "3.29", "3.30", "3.31", "3.36"],
   support=["3.8", "3.14", "3.17", "3.18", "3.24", "3.25", "3.26", "3.35", "3.38"],
   inserts=[
     ("3.4", "audit F1's steelman, and F4's \"the source's THIRD form, not a fourth\"",
      "**Two audit corrections to the deliverable's own framing**"),
     ("3.13", "branch (iii) — arithmetic CONFIRMED, framing OVERSTATED (audit F2)",
      "**Branch (iii): arithmetic CONFIRMED, framing OVERSTATED (audit F2); the current status "
      "of (iii) is at ledger row 11 and at the mg-63e3 row below**"),
     ("3.19", "F3's struck second half, \"and there is no repair available\"",
      "**F3's second half — *\"and there is no repair available\"* — is STRUCK (mg-63e3, "
      "audited mg-f825; see that row)**"),
     ("3.27", "why §7.2 did not settle satisfiability; THE FALSE LOSS (audit F8/F9)",
      "**THE FALSE LOSS — *\"the weakening buys the mg-210d route nothing\"* is OVERSTATED "
      "(audit F8/F9); its live consequence is carried at the mg-210d row above and in "
      "*Second clean residual* below**"),
     ("3.30", "the two BROKEN label/attribution derivations, F5 and F6",
      "**Two BROKEN derivations of labels/attributions — F5 (§6.4's budget row) and F6 (the "
      "master bound's attribution); neither changes a mathematical statement. Their live "
      "consequences:**"),
   ],
 ),
 133: dict(
   file="attempt-mg-63e3.md",
   title="Attempt index — RED-conditional · witness fully CONFIRMED (mg-63e3): can Step 6 consume L4's branch (ii)?",
   row_ref="`STATE.md` § *Attempt index*, the **RED-conditional · witness fully CONFIRMED · CORRECTS MERGED WORK (mg-63e3)** row",
   history=["3.3", "3.9", "3.10", "3.11", "3.12", "3.13", "3.16", "3.17", "3.18", "3.19",
            "3.20", "3.21", "3.22", "3.23", "3.24", "3.25", "3.26", "3.28", "3.44", "3.46"],
   support=["3.6", "3.7", "3.8", "3.34", "3.42", "3.43", "3.48"],
   inserts=[
     ("3.3", "the conditional status this row carried before mg-3af9 discharged it",
      "**What this row asserted while the condition was still live**"),
     ("3.9", "the struck universal (Cor. 4.3 / ledger claim 13)",
      "**⚠️ THE UNIVERSAL IS STRUCK — do not restore it: the deliverable's Cor. 4.3 / ledger "
      "claim 13, *\"there is no modulus `F` for which transport is true\"*, is BROKEN as a "
      "universal**"),
     ("3.16", "the n-dependence clause that was deliberately not landed, and the invalid quantifier step under it",
      "**⚠️ THE `n`-DEPENDENCE CLAUSE IS DELIBERATELY NOT LANDED — a decision, not an omission; "
      "it rests on an invalid quantifier step**"),
     ("3.22", "the second BROKEN premise, \"1/n is the smallest nonzero leakage a prefix cut can have\"",
      "**A second premise of the deliverable is BROKEN — *\"`1/n` is (up to constants) the "
      "smallest nonzero leakage a prefix cut can have\"*, false by a factor of `n`; the witness "
      "is undamaged**"),
     ("3.24", "(IB)'s false interface clause, and its two refutations",
      "**(IB) IS RECORDED IN REPAIRED FORM — the stated version is FALSE and must not be pasted**"),
     ("3.42", "the deliverable's seven durable contributions, KEPT VERBATIM",
      "**KEEP VERBATIM — the deliverable's seven durable contributions, all correct, including the "
      "C1/C2/C3 separation, the explicit declining of C3, *\"`W` refutes implications, not "
      "theorems\"*, *\"do not record this as 'branch (ii) is unrepairable'\"* and §7 property 5**"),
     ("3.44", "two calibrations of the deliverable, neither fatal",
      "**Two calibrations of the deliverable, neither fatal — Step 6's licence, and the `:527` box**"),
     ("3.46", "the two roles of `F`, and the audit's ledger tally",
      "**`F` has two roles in L4 — a budget in (ii) and an error tolerance in (iii) — and only the "
      "first admits or excludes a witness; that is the direct cause of the quantifier failure**"),
   ],
 ),
 134: dict(
   file="attempt-mg-3af9.md",
   title="Attempt index — RED · UNCONDITIONAL · witness W* fully CONFIRMED (mg-3af9): does a sub-linear modulus rescue branch (ii)?",
   row_ref="`STATE.md` § *Attempt index*, the **RED · UNCONDITIONAL · witness `W*` fully CONFIRMED · DISCHARGES row 11's condition (mg-3af9)** row",
   history=["3.23", "3.24", "3.25", "3.26", "3.29", "3.31", "3.32", "3.33", "3.34", "3.38",
            "3.40", "3.41"],
   # 3.6 stays in the row: it is where `W*` is defined, and four kept passages name it.
   support=["3.4", "3.5", "3.7", "3.9", "3.18", "3.19", "3.36", "3.49"],
   inserts=[
     ("3.23", "the arguments under Theorem A, the promotion clause and the §4.1 row — "
      "the counterexamples `U*` and `V*`, and the general mechanism",
      "**The proof defect, the counterexamples `U*` and `V*`, and the general mechanism behind all "
      "three**"),
   ],
 ),
 135: dict(
   file="attempt-mg-276d.md",
   title="Attempt index — GREEN · PROVEN, all finite posets (mg-276d): the foundation claims (1)–(3) supply",
   row_ref="`STATE.md` § *Attempt index*, the **GREEN · PROVEN, all finite posets · first proof-carried generalisation in the arc (mg-276d)** row",
   history=["3.2", "3.3", "3.4", "3.5", "3.6", "3.7", "3.8", "3.9", "3.10", "3.11", "3.12",
            "3.13", "3.14", "3.15", "3.16", "3.24", "3.25", "3.36", "3.42", "3.43", "3.44",
            "3.55", "3.56", "3.57", "3.58"],
   support=["3.1", "3.30", "3.31", "3.32", "3.33", "3.34", "3.35", "3.37"],
   inserts=[
     ("3.2", "the step-4d clause — first of the three A3 sites",
      "**⚠️ STEP 4d DID FIRE HERE, and the OUTCOME — not the firing — is what is different: the "
      "over-wide statement was TRUE and provable, so it was repaired by an UPGRADE rather than a "
      "strike, which is why it holds the second 4d tally alone. This row states no count of its "
      "own and points at Appendix A's two tallies instead, so it cannot rot on the next recount. "
      "This is the first of the three A3 sites; the other two are Appendix A, *\"STEP 4d … AND "
      "THEY MUST NOT SHARE ONE TALLY\"* and template step `4d`**"),
     ("3.24", "F1, the one over-labelled universal, repaired by an upgrade",
      "**F1 — the one over-labelled universal — was repaired by an upgrade, not a retraction**"),
     ("3.36", "the all-+1 invariance theorem, and the repair of its citation",
      "**The all-`+1` invariance is a THEOREM for every finite poset, its citation is repaired, "
      "and `controls.py` now measures it as well; prefer the proof to the count**"),
     ("3.42", "the relocated coverage gap, the gauge-conjugation mechanism, and the positive control on the control",
      "**⚠️ THE COVERAGE GAP IS RELOCATED, NOT CLOSED (mg-5630 §2.2–§2.3, landed by mg-1319), and "
      "this row previously read as though it were closed**"),
     ("3.55", "the recommended next probe, and the answer that discharged it",
      "**The cheaper next probe this row recommended WAS RUN AND IS AUDITED (mg-a3d4, audited "
      "mg-86a3, landed by mg-a806 — the next row): the answer is NO for `Δ_AT` and it is carried "
      "by a theorem, so this row's closing suggestion is DISCHARGED, not pending**"),
   ],
 ),
 136: dict(
   file="attempt-mg-a3d4.md",
   title="Attempt index — AMBER-POSITIVE · THE BET IS PRICED (mg-a3d4): does the face/Hodge side carry technique the graph side lacks?",
   row_ref="`STATE.md` § *Attempt index*, the **AMBER-POSITIVE · THE BET IS PRICED (mg-a3d4)** row",
   history=["3.6", "3.10", "3.11", "3.30", "3.31", "3.34", "3.41", "3.43", "3.44", "3.45",
            "3.46", "3.57", "3.58", "3.59", "3.60", "3.63"],
   support=["3.2", "3.3", "3.4", "3.5", "3.13", "3.17", "3.18", "3.19", "3.21", "3.22",
            "3.23", "3.24", "3.32", "3.33", "3.42"],
   inserts=[
     ("3.2", "Theorem G's proof, the independent rebuild to A_12, and its methodological sizing",
      "**Theorem G's proof, the auditor's independent rebuild of it, and what the arc's step-4d "
      "record makes of that**"),
     ("3.10", "the inherited conditional that was carried nowhere else",
      "**The inherited conditional was declared in the self-audit and carried nowhere else — "
      "mg-5630's defect class, repaired rather than annotated (rows N1a/N1b/N1c/N1r, §7.1)**"),
     ("3.30", "what ledger row B6 used to read, and why \"undecided\" was a resting place",
      "**What the proposed row used to read, and why its *\"undecided\"* was a resting place "
      "rather than a fact, with the exact rational LP that decides every open case POSITIVELY "
      "and the infinite family `V_k`**"),
     ("3.41", "the control battery: absorbability, two repaired calibration defects, and what could not be broken",
      "**CONTROLS — the credit was verified rather than assumed. None of the six mutations is a "
      "gauge in disguise, two calibration defects were repaired, no row was downgraded, and the "
      "one control gap the deliverable named itself is CLOSED by the audit's own rebuild**"),
     ("3.57", "the mechanism recorded beside the G″ strike",
      "**STRUCK, with the mechanism recorded next to the strike — the mechanism is the valuable "
      "part and it is this arc's signature failure stated cleanly: singleton blocks contribute no "
      "factor to Theorem L's join, and dropping that hypothesis makes the link a genuine join in "
      "which an exact `1/2` in a factor is strictly less than `1/2` in the join**"),
     ("3.63", "the sweep that established nothing consumed G″",
      "**Nothing consumed `G″`, and that is swept for rather than assumed**"),
   ],
 ),
}

# Anchor guards: passage key -> the first 44 characters that key MUST start with at the
# base commit.  Regenerated by regen_checks.py.  A splitter change that re-maps passages
# fails here instead of silently relocating the wrong text.
CHECKS = {
 "89": {
  "2.3": "(The conditional form this clause used to ca",
  "2.4": "**The earlier *\"with no repair available\"* i"
 },
 "114": {
  "3.2": "**Do not repeat the reason the deliverable l",
  "3.3": "**That inference is REJECTED: equivalence of",
  "3.4": "Also: sec.0 called statement (2) \"the form t"
 },
 "124": {
  "3.5": "Corrects mg-a1ec Finding 5.4 (Correction 2.1"
 },
 "130": {
  "3.8": "**Honest caveat RETIRED (mg-88bd, audited mg",
  "3.9": "This row used to carry *\"(R) ⟹ a constant `λ",
  "3.10": "That is **false as stated**: the `λ_std → δ`",
  "3.11": "So a constant `λ_std` **is** the currency th",
  "3.15": "The row's own verdict is untouched — \"best c"
 },
 "131": {
  "3.2": "**Four corrections:** (1) **this document's ",
  "3.3": "**Ledger row 8's `⟺ LIB ⟺ (B)` was the same ",
  "3.4": "(2) mg-dbd1 §2.1's \"(B) is weaker than LIB\" ",
  "3.5": "(3) The (A)+(B) route's advertised advantage",
  "3.11": "**Scoping question flagged, not picked — sin",
  "3.12": "**Answer: neither.**",
  "3.13": "Backward derivation from L4 fixes the operat",
  "3.15": "`Σ_x m_x = 2E[inv_e]` identically, so `max_x",
  "3.17": "All three arcs that recommended it (mg-dbd1 "
 },
 "132": {
  "3.4": "(Audit F1: §3.3 refutes a steelman for `n`-d",
  "3.5": "**It is the source's THIRD form, not a fourt",
  "3.8": "The source writes `ε` for the spectral `λ_st",
  "3.13": "**Branch (iii) — arithmetic CONFIRMED, frami",
  "3.14": "The arithmetic: (iii) as worded gives `p^P_{",
  "3.15": "But the source's own L4 in the open-lemma li",
  "3.17": "L4's conclusion is a disjunction; (ii) deliv",
  "3.18": "Implied by the deliverable's own §3.3 senten",
  "3.19": "**F3's second half — *\"and there is no repai",
  "3.24": "`W_n = C_n ⊔ C_1` — a chain plus one free po",
  "3.25": "So `W_n` satisfies `1 − λ_std ≤ ε_spec` once",
  "3.26": "Corroborated independently by mg-3ce3's `8AC",
  "3.27": "**Why the deliverable's own §7.2 did not set",
  "3.28": "**THE FALSE LOSS — \"the weakening buys the m",
  "3.29": "The route's *conclusion* survives and more r",
  "3.30": "**Two BROKEN derivations of labels/attributi",
  "3.31": "**F5** — §6.4's \"L4 usable\" budget row is BR",
  "3.35": "mg-210d Thm 2.4 builds it from the **uncondi",
  "3.36": "Two tools merged into one — exactly the Appe",
  "3.38": "**Free audit by-products, recorded not acted"
 },
 "133": {
  "3.3": "As of mg-63e3/mg-f825 it was genuinely *cond",
  "3.6": "`W`: `n = 2a`, `A = C_{a−2} ⊕ AC_2`, `B = C_",
  "3.7": "**Structural cause, CONFIRMED and the docume",
  "3.8": "So no bound `\\|Δp\\| ≤ g(\\|S\\|)` with `g → 0`",
  "3.9": "**⚠️ THE UNIVERSAL IS STRUCK — do not restor",
  "3.10": "The deliverable's Cor. 4.3 / ledger claim 13",
  "3.11": "Branch (ii) is not a free hypothesis: a pose",
  "3.12": "Family **W** lives entirely inside `Δ₁·n = 2",
  "3.13": "**`F(ε) = ε/4` is an ordinary modulus** — it",
  "3.16": "**⚠️ THE `n`-DEPENDENCE CLAUSE IS DELIBERATE",
  "3.17": "The deliverable proposed recording that tran",
  "3.18": "**It rests on an invalid quantifier step.**",
  "3.19": "In **W** the pair `(ε, n)` is **locked** — a",
  "3.20": "**The stakes are why this is recorded and no",
  "3.21": "The deliverable's own ledger row 16 already ",
  "3.22": "**Second BROKEN premise, recorded because it",
  "3.23": "The witness is undamaged (`Δ₁ → 0` is all it",
  "3.24": "**(IB) IS RECORDED IN REPAIRED FORM — the st",
  "3.25": "As proposed it ended *\"…and one may take it ",
  "3.26": "**The defect is the interface clause, not th",
  "3.28": "(Also dropped: the dead quantifier `c > 0`, ",
  "3.34": "For every `ε > 0` take `n ≥ 1/ε`: **W** at `",
  "3.42": "**KEEP VERBATIM — the deliverable's durable ",
  "3.43": "That is the live question**, the auditor cal",
  "3.44": "**Two calibrations, neither fatal:** Step 6'",
  "3.46": "**One coordinate the deliverable introduces ",
  "3.48": "**Ledger tally:** 27 CONFIRMED · 3 CONFIRMED"
 },
 "134": {
  "3.4": "(Exactly quantified, per the audit: the univ",
  "3.5": "The inference runs `ε` **first**, then `n` f",
  "3.7": "**One** modified element (`S = {x}`, confirm",
  "3.9": "**The escape is constructed, not asserted** ",
  "3.18": "**CREDIT, and it is load-bearing for how the",
  "3.19": "Its restraint on the `n`-dependence clause a",
  "3.23": "Its proof silently assumes a certificate's m",
  "3.24": "It is false **by an unbounded factor**: `U*`",
  "3.25": "General mechanism, one line: **if `P[A]` has",
  "3.26": "`W`/`W*` are immune only because their `A`-s",
  "3.29": "(Remark 3.1's relation-counting variant `\\|S",
  "3.31": "The auditor built it: **`V*(N)`**, `A = {u,v",
  "3.32": "**Hand-verified at `N = 3` by enumerating al",
  "3.33": "**The deliverable's claim that better-balanc",
  "3.34": "So the two readings give **different mathema",
  "3.36": "**Its two honest halves are sound and stay: ",
  "3.38": "The deliverable's billing of it as *the sing",
  "3.40": "What it refutes is the route — *\"the pair mi",
  "3.41": "The document violated its own motto two rows",
  "3.49": "**Constraint compliance CLEAN on both docume"
 },
 "135": {
  "3.1": "The auditor, who re-derived it independently",
  "3.2": "After **five consecutive over-wide generalis",
  "3.3": "BOTH FACTS ARE TRUE OF THE SAME DOCUMENT AND",
  "3.4": "⚠️ CONNECTIVE INLINED HERE 2026-07-30 (mg-f7",
  "3.5": "(Cited without the running count on purpose:",
  "3.6": "Read alone — which is how a row gets quoted ",
  "3.7": "This is the site that gets quoted, so it car",
  "3.8": "**⚠️ CORRECTED 2026-07-30 (mg-5630 §5.2, lan",
  "3.9": "Step 4d DID fire here.**",
  "3.10": "§0 asserted a universal in `n` off `n ≤ 5` a",
  "3.11": "**What is genuinely different from EVERY OTH",
  "3.12": "That distinction is worth keeping and this c",
  "3.13": "See Appendix A, *\"STEP 4d … AND THEY MUST NO",
  "3.14": "**⚠️ THE COUNTS THIS SENTENCE USED TO CARRY ",
  "3.15": "It read *\"the other **six** firings\"* and ci",
  "3.16": "Appendix A's own resolution applies verbatim",
  "3.24": "**This is F1, the one over-labelled universa",
  "3.25": "The auditor's proof is adopted and row D2 up",
  "3.30": "**The two degenerate subclasses are named as",
  "3.31": "275 posets with non-trivial `Aut` and 108 di",
  "3.32": "**Controls, and the one gap the audit found ",
  "3.33": "Positive: homology on `S¹`/`S²`/disc/wedge, ",
  "3.34": "Negative: five named mutations, each rejecte",
  "3.35": "**But none of those five perturbed the CONST",
  "3.36": "**That last statement is TRUE and is a THEOR",
  "3.37": "`controls.py` now compares `L^rel` **and** `",
  "3.42": "**⚠️ BUT THE COVERAGE GAP IS RELOCATED, NOT ",
  "3.43": "NC3's corruption is a **diagonal `±1` gauge ",
  "3.44": "The positive control on the control nobody h",
  "3.55": "The cheaper next probe is to price the progr",
  "3.56": "**⭐ THAT PROBE WAS RUN AND IS AUDITED — mg-a",
  "3.57": "The answer is NO for `Δ_AT`, and it is carri",
  "3.58": "So this row's closing suggestion is DISCHARG"
 },
 "136": {
  "3.2": "Every level's link of `F(A_n)` has `λ₂ ≥ 1/2",
  "3.3": "**The deliverable's own §13 named this proof",
  "3.4": "The auditor rebuilt it — by hand, AND from t",
  "3.5": "*\"Complete, `n`-free, no gap; the strongest ",
  "3.6": "**This is the arc's best METHODOLOGICAL resu",
  "3.10": "**That conditional was declared in the self-",
  "3.11": "**That is mg-5630's defect class and it is r",
  "3.13": "Under the *other* reading — no boundary quot",
  "3.17": "Two new theorems license the import — **the ",
  "3.18": "`γ_i ≤ 1/2` on all 404 and attained by 373, ",
  "3.19": "**`1/2` is the fixed point of Oppenheim's tr",
  "3.21": "`F(P)` is a left regular band under successi",
  "3.22": "Verified against the actual matrix by exact ",
  "3.23": "`A_6` was skipped and that is stated in four",
  "3.24": "Sharpest control: the **Tsetlin library** — ",
  "3.30": "The proposed row used to read *\"`Δ_AT` is NO",
  "3.31": "**That \"undecided\" was a resting place, not ",
  "3.32": "§9.4's test is only *sufficient*; the actual",
  "3.33": "**And the `\\|L(P)\\| ≤ 4` threshold is an art",
  "3.34": "**The old clause survived only inside the he",
  "3.41": "**CONTROLS — the credit was verified rather ",
  "3.42": "mg-5630's absorbability test was applied to ",
  "3.43": "Two calibration defects repaired: **X1a's re",
  "3.44": "**The four downstream-failure rows are NOT d",
  "3.45": "**The one control gap the deliverable named ",
  "3.46": "**What could not be broken:** Theorem G; the",
  "3.57": "**STRUCK, with the mechanism recorded next t",
  "3.58": "Drop the singleton requirement — which is ex",
  "3.59": "An exact `1/2` in a factor is STRICTLY LESS ",
  "3.60": "THE STRENGTHENING WAS NOT FREE: THE DROPPED ",
  "3.63": "**Nothing consumed `G″`, and that is swept f"
 }
}
