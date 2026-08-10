# `mg-a0d6` — INDEPENDENT AUDIT OF THE `mg-d19f` ADJUDICATION

**Subject:** `095260c` — *"THE CONTRADICTION IS DECIDED AGAINST `mg-51f4` AND THE TICKET WAS
FILED AGAINST ONE SITE OF THREE — `mg-28ff:21` is TRUE and is LEFT ALONE"*.

**VERDICT: THE ADJUDICATION WENT THE RIGHT WAY, AND IT IS THE FIRST TIME THE NUMBER IT TURNS
ON HAS BEEN RECOMPUTED BY ANYBODY.** `168 of 86278` reproduces **exactly**, on an instrument
that imports neither library and computes the population, the transport, the leak, the
spectral gap and both certificates from scratch. All three sites are handled, they are one
defect, nothing true was struck, nothing was harmonised, and the surviving site is true in
every one of its three components.

One finding of degree and one caveat on a sentence of the landing's reasoning are recorded in
§5 and §6. Neither reverses anything.

---

## §0. WHAT AN ADJUDICATION RISKS, AND WHY THIS ONE NEEDED AN AUDIT

An adjudication adds no measurement. It declares one of two published statements false. If it
goes the wrong way, the arc has **corrected a true document and left a false one standing**,
with a landed commit saying otherwise — and the commit subject is permanent.

`mg-d19f` landed at HEAD as a HIGH-priority adjudication between two landed canonical
documents **with no independent audit and no verdict mail**, because it was filed by a polecat
as a follow-up and so never went through `pm-onethird`'s standing practice of pre-filing an
audit in the same action. This ticket is that audit, filed late and stating why.

**AND THE NUMBER HAD NEVER BEEN RECOMPUTED.** The landing's own adjudication arm
(`r1_adjudicate.py`) settles the contradiction by reading

```
primitive posets at n=7 where route (F) FAILS  (f* > 1):   168 of 86278
```

**out of `code/sweep_loss_51f4/out_s3_n7.txt`** — `mg-51f4`'s own transcript. `mg-28ff:21`
quotes it, `mg-29fe` took it from the same place, `mg-64cb` never touched it. Four tickets
carried that figure and none recomputed it. Everything downstream — which document is false,
which sentence is struck, what `mg-28ff`'s §4.3 now says on `main` — rests on one 1443-second
run nobody repeated.

---

## §1. THE RE-DERIVATION — `168 of 86278`, INDEPENDENTLY  (`a1`)

`liba0d6.py` builds the naturally labelled posets by extending down-sets, computes the
transport by a down-set dynamic program, reads `leak(A_k)` off it, forms
`M = Σ_k leak(A_k) / Σ_k min(k, n−k)` and `f*(P) = M²/(2γ)`, and decides `f* > 1` as
`γ < M²/2`.

**NO FLOAT DECIDES A VERDICT.** `γ` is the minimum of a Rayleigh quotient over `1^⊥`, so any
exhibited `v ⊥ 1` gives an exact *upper* bound on `γ` — which means a **failure** is certified
by exhibiting one rational vector and checking `⟨v,Lv⟩ < (M²/2)⟨v,v⟩` in `Fraction`
arithmetic, with no eigensolver anywhere. A **hold** is certified in the other direction by an
exact PSD test of `L − (M²/2)(I − J/n)`, decided by the signs of the coefficients of
`det(xI + A)`. Floats appear only in a Jacobi sweep whose job is to order the population.

| | this instrument | `out_s3_n7.txt` / `mg-51f4` §4 |
|---|---|---|
| posets, `n = 2..7` | `2 / 7 / 40 / 357 / 4824 / 96428` | identical |
| primitive | `1 / 4 / 27 / 275 / 4070 / 86278` | identical |
| **(F) fails at `n = 7`** | **168 of 86278, every one certified exactly** | **168 of 86278** |
| max `f*` at `n = 7` | `1.297074` | `1.297074` |
| argmax | `[(0,3),(0,4),(0,5),(1,3),(1,4),(1,5),(1,6),(2,3),(2,4),(2,5),(2,6)]` | the same poset |
| max `c_true` at `n = 7` | `0.340719` | `0.340719` |
| **(F) fails at `n ≤ 6`** | **at NO `n`** | not stated by anybody |

**THE BOUNDARY IS NOT CLOSE.** The largest `f*` at a *holding* poset is `0.996882310`; the
smallest at a *failing* one is `1.006618414`. A gap of `0.0097` against a Jacobi residual of
order `10⁻¹⁴`: no verdict in this population is within ten orders of magnitude of flipping.
All 168 failures and 2153 holds are additionally certified in exact rational arithmetic; the
remaining holds sit outside that gap.

**THE HALF NOBODY HAD STATED, AND IT IS THE ONE THAT MAKES `mg-28ff:21` EXACTLY SCOPED.**
Route (F) fails at **zero** primitive posets for **every** `n ≤ 6`. So `mg-28ff`'s
*"100 % at every enumerated `n`"* is **TRUE of `n ≤ 6` and false only at `n = 7`** — which is
precisely what `mg-28ff:21` claims, no wider and no narrower. Had (F) also failed at `n = 6`,
`mg-28ff:21` would be true for a bigger reason than it gives and the repair landed on that
document would itself be an under-correction. It is not. (`PREDICTIONS.md` P1, P2 — both HIT.)

---

## §2. THE SURVIVING SITE — `mg-28ff:21` IS TRUE  (`a2` §1)

This is the positive claim the landing makes and leaves standing, and it is the one nobody
re-checked. It has three components and each is resolved against a different source:

1. **the sentence** — `mg-28ff@cb496e9:247` reads *"**100 % at every enumerated `n`**, with no
   eigenvector on the left."* Exactly one line in the document matches, and it is line 247.
2. **the row it summarises** — `mg-28ff@cb496e9:245` reads
   `| 7 | 106 *(sample)* | 106 / 106 | 0.832530 |`. Two lines above the sentence, and a sample.
3. **the number** — `168 of 86278`, from §1 above, re-derived rather than quoted.

`cb496e9` is `mg-28ff`'s only revision before `mg-51f4` landed, i.e. the text `mg-51f4`
actually read. **Nothing here is decided by recency and nothing by either document's prose
about the other.**

---

## §3. ALL THREE SITES — HANDLED, AND ONE DEFECT  (`a2` §2, §3)

The ticket named **one** site. The landing struck **three**, and in fact **four spans** across
those three: §4's paragraph carries two false clauses, and the second of them —
*"I do not quote any of them"* — is site 3's blanket stated a second time in a different
section. That is what makes *"all three are one defect"* a finding rather than a slogan, and
it is checked here rather than repeated: **4 of 4 struck spans carry both a universal or
negative quantifier and a labelling or quoting word**, and nothing of any other class was
struck alongside them.

| site | where | struck clause | provenance | verdict |
|---|---|---|---|---|
| **1** | §4, `:148` at `2f76a01` | *"…samples of 40–200 posets, correctly labelled as such at every appearance in its document"* | named by the ticket (`mg-64cb`) | **FALSE — struck correctly** |
| **1b** | §4, same paragraph | *"I do not quote any of them"* | found by the landing | **FALSE — struck correctly** |
| **2** | §11 preamble | *"Every one of `mg-28ff`'s `n = 7` figures was correctly labelled a sample at each appearance. None of these is a labelling failure."* | found by the landing | **FALSE — struck correctly** |
| **3** | §12 "NOT DONE" | *"`mg-28ff`'s `n = 7` sample figures are not quoted anywhere … **The one place** I mention one"* | found by the landing | **FALSE — struck correctly** |
| — | §11 preamble, staleness | *"a superseded `n = 7` figure is wrong on `main` right now"* | found by the landing | **TRUE WHEN WRITTEN — dated, correctly** |

**SITE 1 IS FALSE IN BOTH ITS CLAUSES, AND THE SECOND WAY IS MEASURED HERE.** *"At every
appearance"* is false because `cb496e9:247` is an appearance reading `enumerated`. And
*"samples of 40–200 posets"* has **no unit**: every `sample_posets(7, k)` in `mg-28ff`'s
instrument at `cb496e9` has `k ∈ {90, 200}` — **there is no draw of size 40.** `40` is §4.2's
*primitive count* and `200` is §4.1/§4.3's *draw size*, so the range's two endpoints come from
two different columns of two different populations. (P9 — HIT.)

**SITE 2 IS FALSIFIED FROM INSIDE ITS OWN DOCUMENT.** §11's row 1, three lines *below* the
struck sentence, says in `mg-51f4`'s own words: *"The word `enumerated` sat over a table whose
`n = 7` row was a sample, so the sentence reads as covering `n = 7` and is false there."* That
is a labelling failure. No second document is needed.

**SITE 3 WAS FALSE ON THE DAY THE DOCUMENT LANDED.** At `2f76a01` the three figures occur
**five** times, and two of them — `0.850074` and `0.832530` — are quoted in §11's table and are
not the *"one place"* the bullet names. Each of the three is verified to be an `n = 7` row of
`mg-28ff@cb496e9` labelled `(sample)`.

**THE DATED ROW'S TWO POSITIVE CLAIMS, ALSO UNCHECKED BY ANYBODY, ARE BOTH TRUE:** *"Site 1
has landed"* — `mg-28ff@HEAD:561` carries the repaired sentence; *"site 6 has not"* —
`mg-28ff@HEAD:1022` still reads *"(M♯) and (F) are both OPEN"*.

---

## §4. NOTHING TRUE WAS STRUCK, AND NOTHING WAS HARMONISED  (`a2` §3, §4)

* **Every clause left standing at site 1 is true and reproduces here:** the figures *are*
  deterministic samples; `c_true(7) = 0.176145` is `mg-28ff`'s; the enumerated maximum *is*
  `0.340719` (§1); and `0.340719 / 0.176145 = 1.9343`, so *"low by a factor of 1.93"* stands.
* **The replacement is true too.** *"I do not USE any of them"*: every table row in `mg-51f4`
  carrying one of the three figures is a §11 **repair-proposal row quoting `mg-28ff`'s own
  cell**, and none of the three enters §0's, §4's or §6's tables. That is `mg-29fe`'s verdict
  on this document in `mg-29fe`'s words — *"carried and not used, which is the correct
  handling"* — and it survives.
* **`mg-51f4`'s own `n ≤ 6` numbers are not in question.** Its `f*` and `c_true` columns
  reproduce **exactly** on this instrument at `n = 3,4,5,6`. The strike is confined to prose.
* **The landing edited exactly one document, and it is the one it decided against.**
  `mg-28ff` is byte-identical across `095260c`.
* **Nothing was deleted.** The entire 5038-word text of `mg-51f4` at its own landing is an
  in-order subsequence of HEAD's 6948 words — HEAD is the landing text **with insertions
  only**. A reader arriving with the old sentence still finds it, struck, with the correction
  beside it. (P5, P7 — both HIT.)

---

## §5. WAS *THREE* THE RIGHT NUMBER?  YES — AND THE REPAIR'S OWN BLANKET SURVIVES  (`a3`)

A mechanical sweep of `mg-51f4` at `2f76a01` for the class the landing named — a sentence that
names `mg-28ff`, carries a universal or negative quantifier, and carries a labelling or
quoting word — returns **five** candidates. **Three are the struck sites.** The other two are
false positives of my own rule and are adjudicated in the transcript rather than counted: one
is about a bound direction for `μ_pref`, one is a "why" cell about a replacement figure.
**Nothing of the class was left standing.** (P4 — HIT.)

**A GAP IN MY OWN RULE, STATED:** the DATED row is *not* of this class — it is a claim about
staleness, not labelling — so my sweep does not find it. It is checked separately above.

**THE REPAIR ASSERTS A NEW BLANKET ABOUT LABELLING, AND IT IS TRUE.** §0.0 says the repair
*"makes no universal claim of its own about `mg-28ff`'s labelling in either direction — every
`n = 7` **cell** in that document does carry the word `(sample)`"*. Checked against
`mg-28ff@cb496e9` and not taken on trust: **3 of 3 cells**, at `:200`, `:217`, `:245`. The new
blanket quantifies over **cells**, which are enumerable; the struck one quantified over
**appearances**, which are not. That is the whole difference between the false blanket and the
true one, and the repair says so in the same breath.

### The one finding of degree: *"five appearances"*

The repaired §12 bullet says the three figures appear at **five** sites. Under my rule — an
*appearance* is an occurrence that asserts or quotes the figure as evidence; an occurrence
inside struck text, inside the enumerating sentence itself, or inside prose *about* having
quoted it, is a record of the repair — the count is **exactly 5**, and the five sites the
bullet names are individually correct.

**The raw count at HEAD is 10.** So `five` is recoverable but only under a membership rule the
document does not state, which is the same shape as the three sentences it struck: *a count
asserted over a population whose boundary the reader cannot reconstruct.* The landing saw the
near-miss and filed it as its own `D4`; it did not carry the observation into the bullet's
wording. **A finding of degree, not a reversal** — and the rule I counted with is **mine**,
which is `PREDICTIONS.md` E4 and is why it is printed beside the answer. (P3 — HIT.)

---

## §6. ONE CAVEAT ON THE LANDING'S REASONING — AND `P8` LOSES

The landing's `r1` closes: *"The two documents never disagreed about the FACT. They disagreed
about a SUMMARY of the fact."* True of the **labelling** fact it adjudicates. **Not true as a
statement about the two documents' numbers**, and I bet at 0.55 that it was.

Asking a third instrument — the only way to settle it — `mg-28ff`'s §4.3 `f*` column differs
from `mg-51f4`'s at **two** rows, and mine lands on `mg-51f4`'s both times:

| `n` | `mg-28ff` §4.3 | `mg-51f4` §4 | this instrument (12 places) |
|---|---|---|---|
| 5 | `0.550750` | `0.550747` | `0.550747037145` |
| 6 | `0.811654` | `0.811649` | `0.811648851994` |

Both `mg-28ff` values are high by `3–5 × 10⁻⁶`, exactly the resolution of the 20-step
bisection over `[0,4]` whose **upper bracket end** `b1_footrule.py:77` prints. `mg-51f4` §11
names the `n = 6` one, attributes the cause to `mg-29fe`, calls it *conservative rather than
wrong* and leaves it as `mg-29fe`'s finding to file.

**AND MY FIRST DRAFT OF THIS PARAGRAPH SAID THE `n = 5` ONE WAS NAMED NOWHERE.** One `grep`
refutes that: `mg-29fe`'s audit `doc:311` names **both** values and its
`out_s2_footrule.txt:18` prints `5  0.550747037  0.550750  -2.96e-06` — my value, to nine
places, on an instrument sharing no source line with mine. So this is a **third independent
agreement, not a new finding**. Neither row touches the adjudication: both are `mg-28ff`'s own
column, both are conservative (they *over*-state route (F)'s constant), and neither is `n = 7`.
Recorded for a successor; `mg-28ff` is another ticket's landed document and is not edited here.

---

## §7. PREDICTIONS SCORED — 8 OF 9, AND THE MISS IS THE ONE I HELD LOWEST

| | p | outcome |
|---|---|---|
| P1 | 0.85 | **HIT** — `168 of 86278` reproduced exactly, every failure certified by an exhibited rational vector |
| P2 | 0.90 | **HIT** — (F) fails at zero posets for every `n ≤ 6` |
| P3 | 0.70 | **HIT** — `five appearances` needs an unstated rule; raw count 10 |
| P4 | 0.60 | **HIT** — three is the right number; the two extra sweep hits are my own false positives |
| P5 | 0.65 | **HIT** — no true clause struck, and the replacement clauses are true |
| P6 | 0.80 | **HIT** — `mg-28ff:21` true in all three components |
| P7 | 0.75 | **HIT** — zero measured literals withdrawn |
| P8 | 0.55 | **LOST** — the two documents *did* disagree about numbers, at `f*(5)` and `f*(6)` |
| P9 | 0.50 | **HIT** — `40–200` mixes a primitive count with a draw size; no draw of size 40 exists |

**The exposures declared in `PREDICTIONS.md` §0 stand:** I knew `168` before measuring (H1), I
had read the landing's verdict in full before writing a probe (H2), and I had already grepped
the figure counts (H3). P1 was never a bet about *what the number is*; it was a bet about
whether an independent instrument reaches it, which is the thing four tickets had not done.
H2 is the real limit on this audit and it is E3 below.

---

## §8. SEVEN DEFECTS OF MY OWN, ALL KEPT

* **D1 — my site-count arm asserted ONE strike span per site and went RED at 4 of 3.** My rule
  was wrong, not the landing: §4's paragraph carries two false clauses. The arm now *counts*
  the span→site mapping instead of assuming it — and the thing it was wrong about turned out
  to be the evidence for the landing's *"all three are one defect"*.
* **D2 — my "is this figure labelled?" probe could not read a table inside a blockquote.** It
  required a row to start with `| 7 |` and `mg-28ff@cb496e9:200` starts with `> | 7 |`, so it
  reported the `c_true(7)` sample row as NOT FOUND. **A probe for labelling defects that
  cannot see a quoted table would have reported a labelling defect as absent.**
* **D3 — my "nothing was deleted" arm compared whole LINES and went RED five times** on
  re-wrapping and on bold markers the landing added inside text it was quoting. A deletion
  detector that cannot tell a deletion from a line break. It is a word-subsequence test now.
* **D4 — my table parser read `mg-28ff` §4.2's `c♯` column as §4.1's `c_true`** because the
  three tables have the same column shape, and reported `mg-28ff` as DIFFERING at every `n`.
  **A probe that cannot tell two of a document's tables apart manufactures disagreements** —
  in an audit whose subject is a manufactured disagreement.
* **D5 — I asserted that the `n = 5` disagreement was named nowhere, in the arm whose job is
  to not assert things.** `mg-29fe` names it. This is an over-claim about an unenumerated
  population, inside an audit of over-claims about unenumerated populations. The arm now
  searches.
* **D5b — and the search I wrote to fix D5 printed `named in 0 documents`,** because
  `git grep … -- docs/` resolves the path **relative to the cwd** when a revision is given, and
  the arm runs from inside this directory. **A probe written to catch an assertion, agreeing
  with the assertion because it looked in the wrong place.** Anchored at `:(top)docs/` now.
* **D6 — my import-independence arm matched imports with a regex and went RED on the English
  words *"from the same place"* inside `a1`'s own docstring.** A probe for *"does this file
  import its subject"* answering yes because of a sentence *about* the subject. Parsed with
  `ast` now.
* **D7 — my containment arm read only the COMMITTED diff and was green at every moment before
  the commit.** That is `mg-d19f`'s own `D1`, which I would have committed inside the audit of
  the landing that recorded it. Fixed to read the working tree too — **and the fix fired on its
  first run**, catching a stray `out_a3_scope.txt` I had left at the repository root from a
  run in the wrong directory. The committed-state probe could not see it.

**AND ONE THING I DID NOT REMOVE.** `liba0d6.py` shares exactly **one** substantive source
line with `lib51f4.py`: `den = sum(min(k, n - k) for k in range(1, n))`, `M`'s denominator,
which is `Σ_k min(k, n−k)` written the only way Python writes it. Renaming a variable would
have hidden a true fact about this instrument, so the line stays and arm **A10** recomputes
`M` from the **footrule identity** `E[D_F] / (2⌊n²/4⌋)` over linear extensions — a route that
does not contain that line — agreeing at all 5228 posets `n ≤ 6`. Everything else is unshared,
and no file imports any other tree.

---

## §9. THE ARMS

`sh run_all.sh` — five arms, ~2 minutes, **59 arms green, 1 finding**, exit 0. The runner uses
no `| tee`: `set -e` reads the *last* command of a pipeline, so `python3 arm.py | tee out.txt`
reports `tee`'s success and swallows the arm's failure — `mg-9876` indexed 18 live sites of
exactly that in this corpus. Each arm redirects, its status is captured explicitly, and the
runner's failure path is exercised rather than promised (planted `sys.exit(3)`: `RUN FAILED`).

| arm | what it can refuse |
|---|---|
| `a0_selftest.py` | 18 forced arms in 10 groups. A1 counts the population two ways (down-set extension vs transitive-closure brute force). A2 checks the DP against filtering `n!` permutations at all 5231 posets `n ≤ 6`. A3/A4 check `leak` three ways. A6 shows the PSD test accepting *and* refusing, including the singular boundary case. A7–A9 plant worlds where the certifiers must refuse. A10 is the footrule cross-check. |
| `a1_ground_truth.py` | the re-derivation. Exits 1 if `168 of 86278` does not reproduce, if (F) fails at any `n ≤ 6`, or if any poset is left unresolved by both certifiers. |
| `a2_sites.py` | 26 arms over the three sites, the surviving site, and the harmonisation question. Three of them were genuinely REFUTED during development and are D1–D3. |
| `a3_scope.py` | 8 arms: the blanket sweep, the repair's own new blanket, the `five appearances` count, the literal multiset, and the three-way numeric comparison. |
| `a4_selfcheck.py` | 8 arms: independence (`ast` imports, shared source lines), four planted worlds at `n = 7` — threshold, scalar, **population**, orthogonality — and containment. |

**W3 IS THE MUTATION THAT MATTERS.** Counting `f* > 1` over **all 96428** posets instead of
the **86278 primitive** ones gives **10318**, not 168. Every published *"168 of 86278"* is
stated over the primitive population and **nothing in the phrase carries that** — the same
population hazard `mg-0d1b` reports one commit earlier, arriving here as a control rather than
as a finding.

---

## §10. WHAT THIS TICKET DID NOT DO

* **It edited neither document and no file of `mg-d19f`'s instrument.** Zero files outside
  `code/adjudication_audit_a0d6/` differ from the branch point, committed or in the worktree.
* **It did not re-open route `(M♯)`.** §11 site 4's *"unrepresentative enough to invert a
  universal claim"* concerns `c♯`, which needs the monotone-cone minimisation this instrument
  does not implement. **It is not verified here and is not claimed.**
* **It did not adjudicate §11's other five proposed sites,** which the landing explicitly left
  unadjudicated. That decision is not this ticket's to reverse.
* **It did not repair `mg-28ff`'s `f*(5)`/`f*(6)` bracket-end prints.** Recorded in §6 for a
  successor.

*`mg-a0d6`. Instrument: `code/adjudication_audit_a0d6/`, five arms, `run_all.sh` exit 0.
`liba0d6.py` written from scratch, importing nothing and sharing one forced formula line with
`lib51f4.py`, which is named rather than removed and cross-checked by a route that does not
contain it.*
