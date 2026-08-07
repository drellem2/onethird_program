# mg-4f88 — INDEPENDENT AUDIT of mg-2860's STATE.md leading-form correction

## VERDICT

**THE PARENT IS CONFIRMED ON FOUR OF FIVE CHECKS, AND MY OWN BRIEF IS REFUTED ON
THE FIFTH — IN BOTH HALVES.** The one finding against mg-2860 is that its
presentational edit **did** move the mathematics, at four sites, and its own
commit message's defence names the mechanism.

**THE SHA I AUDITED — STATE.md is at `491d42c79f7628c18cb7a5d197faa9f4600cd6c1`**
(blob `7f73bfc87b4bc4caab6c836f8c3922a2416863cf`; worktree HEAD `dafe759`, which
does not touch STATE.md). It had **not** moved from the sha the dispatch named.

| # | check | (A) at `f85a4e8` | (B) at `491d42c` |
|---|---|---|---|
| 1 | condition travelled | **PASS**, 1 site gap | **PASS**, 1 site gap |
| 2 | (LIB-weak) stated *as unattacked* | **REFUSED — CORRECTLY. MY BRIEF IS WRONG.** | scoped form present, added by mg-c4f5 |
| 3 | mathematics must not move | **MECHANICALLY PERFECT / SEMANTICALLY FAILED** | repaired by mg-325c + mg-5ce3 |
| 4 | finite-n numbers | **PASS** — and I can name the kind | PASS, one live currency defect (not the parent's) |
| 5 | did not break mg-b0ae's subject | **PASS — and by 69 seconds** | n/a |

---

## 0. THE BRIEF I WAS GIVEN DESCRIBES A FILE THAT STOPPED EXISTING TWELVE COMMITS AGO

Pre-registered as the framing correction, before I opened anything. My ticket says
*"Read the **new first screen** as a stranger."* Between `f85a4e8` and the file a
reader meets today there are **12 commits to STATE.md** and the file has gone
**33,638 → 82,559 characters**. So every check below is reported twice — **(A)**
the parent's frozen edit, **(B)** the current file — and no finding crosses
between them without its attributing commit printed.

---

## 1. THE CONDITION — PASS AT BOTH, WITH ONE NAMED GAP

The condition is not merely *present*; it is at the site a reader meets the
constant form **first**, in the same sentence, at both commits.

Char offsets are given for **both ends** of the condition sentence — its opening
(`CONFIRMED CONDITIONALLY, not settled`) and its operative clause (`…the answer
flips`) — because only the second one clearing the screen means a reader actually
gets the condition:

| | line | opens at | operative clause at | file size | inside my pre-declared 4,000-char screen? |
|---|---|---|---|---|---|
| (A) `f85a4e8` | 13 | 1,195 | **1,321** | 33,638 | ✅ with 67% headroom |
| (B) `491d42c` | 15 | 3,528 | **3,654** | 82,559 | ✅ **by 346 characters — 8.7%** |

Verbatim at both: *"**CONFIRMED CONDITIONALLY, not settled**: L4-as-stated is the
thing whose provability at an `n`-free modulus is in doubt, and **if L4 needs an
`n`-dependent modulus the answer flips**."* Both halves my pre-declared definition
demanded — *conditional* AND *what the condition is* — are there. In (B) it has
been **strengthened**, not weakened, by mg-345e: *"WHICH SIDE FLIPS — the flip is
on the DEMAND side only."*

**THE GAP, and it is at one of the two sites the ticket itself named as
defective.** The Axis 1 summary (`:21` at (A), `:23` at (B)) states the constant
form and adds the claim **"the form the architecture consumes"** — the very claim
that is conditional — with **no conditional marker of any kind**, at both commits.
The parent's commit message asserts *"It is not presented as settled anywhere."*
**That is an overclaim about its own edit**, false at exactly one of its four
sites. The mermaid node (`:57`) also carries no marker, but it sits as the target
of an edge labelled `OPEN ★ THE WALL`, so the diagram carries the status
structurally; I do not score it.

**I file this as FRAMING, not as mathematics** — per my pre-registered P23 guard.

⚠️ **(B) is one insertion from failing.** The condition's operative clause sits at
char 3,654 of my declared 4,000-char screen — **346 characters of headroom, 8.7%**
— and the sentence does not close until ~3,707. Text inserted *ahead* of it by the
twelve intervening commits is what consumed the other 91%. Nobody owns this
budget, and roughly one more paragraph above line 15 pushes the only conditional
marker on the page off the first screen. **This is the single thing in this audit
most likely to become a defect, and it will do so silently.**

---

## 2. (LIB-weak) "AS UNATTACKED" — MY BRIEF IS WRONG IN BOTH HALVES, AND THE PARENT HAD ALREADY SAID SO

This is the headline. My ticket instructs me to *"confirm … that (LIB-weak) is
stated as unattacked"* and to *"CHECK THAT FACT"*. I checked it. **It is false,
it was already false when my ticket was written, and mg-2860 refused to write it
on exactly those grounds five hours before my ticket's premise could be tested.**

### 2a. "unattacked" is FALSE, and the dating is not close

| event | timestamp |
|---|---|
| mg-c3ca's attack on (LIB-weak) **merged** at `81214a9` | **2026-08-06 00:48 UTC** |
| mg-2860 lands `f85a4e8`, refusing the word | 2026-08-06 17:52 UTC |
| **my own ticket mg-4f88 created**, asking me to confirm it | **2026-08-06 17:15:28 UTC** |

**My brief was filed 16 h 27 m after the corpus's own commit falsified its
premise.** `81214a9` is titled *"(LIB-weak) IS NOT BLOCKED BY THE ARC'S NAMED
OBSTRUCTION"* and `docs/OneThird-LIBweak-mg-c3ca.md` §0 is a five-line verdict on
(LIB-weak) — it is an attack by any definition, and its own §0.1 says so:
*"that gap is … the reason 'never attacked' is an opportunity, not an oversight."*

**Measured, not asserted:** `"never attacked"` occurs **0 times** in STATE.md at
`f758468` and **0 times at `f85a4e8`**. The parent did not write it. It first
enters at `05a0061` (mg-c4f5's landing) and is present once at `491d42c`, in the
**correctly scoped** form *"`never attacked` holds, 0 of 4 pre-c3ca items filed
against it"* — a true statement about the population *before* mg-c3ca, not a
claim of present unattackedness.

**My independent census reproduces mg-c4f5's population exactly.** Sweeping all
2,466 mg items for bodies naming (LIB-weak): the pre-c3ca population is
**4 items — mg-1fdb, mg-88bd, mg-d112 (all 2026-07-29) and mg-e768
(2026-08-05)** — and **0** has (LIB-weak) as a deliverable. Same count, same
verdict as mg-c4f5, reached from the item store rather than from its transcript.
Post-c3ca I find **no second attacker**: mg-325c, mg-5ce3 and mg-3e06 are about
the *ordering* and `N₀`, not about (LIB-weak) itself. So (LIB-weak) has been
attacked **exactly once**, by mg-c3ca, verdict *neither proved nor blocked* — and
that is what the current page says.

**My brief says an attack "changes what mg-c3ca should do". It does not: the arc
that attacked it IS mg-c3ca.** The conditional is self-referential and
discharges to nothing.

### 2b. THE CHAIN MY BRIEF ASKS ME TO CONFIRM IS THE DEFECT ITS PARENT WAS FILED TO REMOVE

My ticket: *"Confirm the strength chain reads `(B) => LIB => (LIB-weak) =>
lambda_std -> 1`."*

**That endpoint is the limit.** mg-2860 exists because the limit was leading. Had
the parent obeyed my brief, it would have re-landed `λ_std → 1` as the terminus of
the file's central chain — the exact over-strong rendering the ticket was filed to
demote. **My audit brief carries the defect its subject removed**, and pm-onethird
wrote both documents ~2 minutes apart (mg-2860 at 17:13:23Z, mg-4f88 at 17:15:28Z).

The parent refused, in writing, and mg-325c independently confirmed the refusal
was right (*"mg-2860's polecat REFUSED BOTH IN ITS COMMIT MESSAGE"*). **I reached
the same conclusion from the diff before reading mg-325c's body.**

`(LIB-weak)` count in STATE.md: **0 → 5** across `f85a4e8` (18 today). It is on the
board, as the parent's subject claims. That half of my check passes — as a
*reproduction*, since the parent's commit subject already told me so (H2).

---

## 3. THE MATHEMATICS — MECHANICALLY PERFECT, SEMANTICALLY FAILED

### 3a. The mechanical half reproduces exactly, from my own diff

Not checked against the parent's transcript; recomputed line-by-line:

- **Exactly 5 lines differ**, and they are **exactly `13, 21, 57, 62, 86`** — the
  five the commit message names. **0 lines outside 1..129 differ.** "FOUR SITES,
  FIVE LINES, NOTHING ELSE" is literally true.
- **Every marker survives, 8/8, on my own count**: STRUCK 2, SUPERSEDED 1,
  REFUTED 3, DISCHARGED 2, BROKEN 11, withdrawn 1, void 2, UNPROVEN 2 — identical
  at `f758468` and `f85a4e8`. The parent's table reproduces cell for cell.
- **One ledger row touched (row 8) and its status stayed `OPEN`.** No other row,
  no other verdict cell. (P12 refuted — I bet a second row would move.)

### 3b. THE FINDING: A FALSE IMPLICATION WAS INTRODUCED AT FOUR SITES

Exhibited in `git diff f758468 f85a4e8 -- STATE.md`, per my P22 guard:

| | before | after |
|---|---|---|
| `:13` | `(B) ⟹ LIB ⟹ λ_std → 1` | `(B) ⟹ LIB ⟹ (LIB-weak) ⟹ (LIB-const)` |
| `:21` | `(B) ⟹ LIB ⟹ λ_std → 1` | `(B) ⟹ LIB ⟹ (LIB-weak) ⟹ (LIB-const)` |
| `:62` | `bad mixing ⟹ λ_std→1 (= LIB / B)` | `bad mixing ⟹ 1−λ_std ≤ ε_spec (⟸ LIB-weak ⟸ LIB ⟸ B)` |
| `:86` | `(B) ⟹ LIB ⟹ λ_std→1` | `(B) ⟹ LIB ⟹ (LIB-weak) … ⟹ (LIB-const)` |

`(LIB-weak) ⟹ (LIB-const)` count: **0 at `f758468`, 4 at `f85a4e8`.**

**The old terminus was true. The new one is not.** `(LIB-weak)` is `E[inv_e] =
o(n²)`; `(LIB-const)` is `E[inv_e] ≤ (ε_spec/6)(n²−1)` **at every `n`**. An
`o(n²)` function is eventually below `c·n²`, not below it at every `n` — the step
holds only for `n ≥ N₀`, and mg-c4f5 §5.3 (landed mg-5ce3) later established that
**no `N₀` works for the class at all**. Every other arrow in that chain is a plain
implication; this one is rendered identically and is not one.

**My P23 guard is satisfied**: the object that changed is the terminal consequent
of the sufficiency chain, both sides printed, and its truth status changed from
true to false. This is mathematics, not framing.

It was live **5 h 42 m** (18:52 → 00:34) until mg-325c caught it — *"THE GAP IS A
QUANTIFIER, NOT A CONSTANT"* — and needed two further landings (mg-c4f5, mg-5ce3)
to be fully stated. In (B) it is repaired: `:23` now reads *"the last step is not
even an implication."*

**The parent's own defence names the mechanism.** Its commit says *"That chain is
mg-88bd's own recommended wording … **not new mathematics**"* and *"**I RE-DERIVED
NO MATHEMATICS**."* Both are true as statements about *effort* and both are the
reason the defect shipped: the chain was **transcribed** rather than checked, and
an edit that re-derives nothing cannot notice that a transcribed arrow is false.
This is exactly what my check 3 predicted — *"a mathematical change smuggled into
it would be invisible"* — and it was invisible to its own author.

### 3c. I REFUTE A PRIOR AUDIT'S ATTRIBUTION OF A DEFECT TO THIS PARENT

mg-c4f5's commit subject states that STATE.md's *"row 8 CONTRADICTS ITSELF EIGHT
WORDS APART … **introduced by mg-2860** when it rewrote the row's lead and carried
mg-c3ca's `as written` forward."*

**Measured across every commit that has ever touched STATE.md:**

| clause | first appears |
|---|---|
| `closes **this row as phrased**` | **`905526f` (mg-325c)** — and only there |
| `does not supply the constant form this row leads with` | **`905526f` (mg-325c)** |

**Neither clause exists at `f85a4e8`.** Row 8 at the parent is self-consistent.
Both halves of the contradiction arrived together, in the commit that was
*repairing* mg-2860. The defect mg-c4f5 found is real and its repair was right;
**its attribution is wrong.**

The mechanism is precisely the error I pre-registered against myself as **P22** —
read the current file, find a flaw, score it against an earlier commit. mg-c4f5
committed it; I avoided it only because I had bound the diff-exhibition guard
before opening anything.

---

## 4. THE FINITE-n NUMBERS — VERIFIED, AND I CAN NAME THE KIND

**Both figures were added by `f85a4e8`** (P16 refuted — instruction 3 was not
dropped).

**The crossover formula, confirmed at two independent corpus points.** mg-d1a2
asserts `18C/ε_spec`; I confirm it at a second point it was never fitted to:

| ε_spec | `18/ε_spec` | what the corpus prints |
|---|---|---|
| `2×10⁻²` (repaired) | **900** | `n ≈ 900` ✅ |
| `2×10⁻⁴` (superseded) | **90,000** | `n ~ 10⁵` ✅ |

**The `2×10⁻²` is NOT a fit, and check 4's fear does not materialise.** It is the
file's own formula evaluated: `ε_dem = ε_leak²/(2C₃)` at `ε_leak ≈ 0.20`, `C₃ = 1`
gives `0.04/2 = 0.02` **exactly**. So it is a formula with one empirical input
(`ε_leak`) and one currency-dependent constant (`C₃`) — and it is labelled
**"under the repaired calibration"** at *both* commits, with "unpinned by ~2
orders of magnitude" beside it. It is **not** presented as a derivation. My brief
feared it would be; it is not.

**I identify mg-d1a2's anonymous `C`: it is `C₃`.** `18/ε_dem = 36C₃/ε_leak² =
900·C₃` identically. The corpus carried "900C" and "900" as two unlinked numbers
until mg-d1a2 reconciled them; the reconciliation is right and the `C` has a name.

**THE UNDERSTATEMENT — the mirrored defect the standing target asks about.** The
file states its input is unpinned by ~2 orders of magnitude and prints **one point
estimate, the most optimistic one**:

| | crossover |
|---|---|
| `ε` at the stated 2-order unpinning | 900 → **90,000** |
| `C₃` at mg-94c3's measured gap-form values (1.500 … 2.386) | 900 → **2,147** |

Since a *larger* crossover means a *larger* regime in which the distinction
matters, printing `900` understates the very hazard the ticket was filed about.
**`900` is a floor and the page renders it `≈`** — that is my bound-word finding
(P21) and my mirrored-defect finding (P20), and they are the same instance:
`n ≥ 900·C₃` is correct, `n ≈ 900` is not. The parent printed a bare `900`
(`"900C"` count **0** at `f85a4e8`, **2** at `491d42c`), which is why mg-d1a2 had
to reconcile it four commits later. **Mitigation, stated because it is real:**
mg-e35c's correction told the parent not to carry `2×10⁻⁴`/`10⁵`, and it obeyed;
stating the *sensitivity* is a different act from re-asserting a superseded value,
and that is the act that is missing.

**A LIVE CURRENCY DEFECT IN (B) — and it is NOT the parent's.** At `491d42c` line
15 splits `ε_spec` into two named constants (*"`ε_spec` names two numbers … the
constant we can **prove** (`ε_sup`) and the constant that **suffices**
(`ε_dem`)"*) and then, ~3,000 characters later in the same paragraph, ends with a
bare, unlabelled **`ε_spec ≲ 2×10⁻²`**. Which one is it? Recoverable but not
stated: the paragraph's own *"gap factor of ~50 is `ε_sup/ε_dem`"* with
`ε_sup < 1` forces `ε_dem ≈ 2×10⁻²`. **Attribution, printed per P22:** `ε_sup` and
`ε_dem` occur **0 times at `f85a4e8`** and enter at **`550a7f1` (mg-345e)** at 9
and 8 occurrences. mg-2860's figure was unambiguous when written; **mg-345e split
the name without disambiguating the figure downstream of the split.** This is the
currency-conflation class mg-94c3/mg-01ea landed for `C₃`, in a paragraph that
already carries an explicit currency guard for a *different* constant pair (*"THE
`1` AND THE `1/6` ARE THE SAME THEOREM IN TWO NORMALISATIONS"*).

**`2/(n+1)` sighting, as the dispatch asked.** STATE.md at `491d42c` carries it
**4 times, all as REFUTED** — *"IS A SMALL-`n` COINCIDENCE, AND IT IS FALSE, NOT
CONJECTURAL"*. **0 live sightings.** The file itself names the surviving live site:
*"§5.1's 'what it buys' table still prints `ε_spec = 2/(n+1)` as live"* in
`docs/OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md` — mg-372e's known in-flight
correction, recorded here as instructed rather than raised as a finding.

---

## 5. mg-b0ae — PASS, AND THE HAZARD WAS REAL TO WITHIN 69 SECONDS

The parent's commit message ends: *"mg-b0ae is cold-reading the restructure and
this edit changes the first screen it reads — landed 2026-08-06, after
`f758468`."* It **says so, dates it, and names the base commit** — the last being
stronger than a date, because a commit sha cannot rot.

**And the disclosure was not ceremonial:**

| | timestamp |
|---|---|
| mg-2860 lands `f85a4e8` | 2026-08-06 **18:52:48** +0100 |
| mg-b0ae's audit lands `20614ef` | 2026-08-06 **18:53:57** +0100 |

**69 seconds.** mg-b0ae's cold read was of the pre-mg-2860 first screen and was
superseded 69 seconds before it committed. My pre-registered P19 — that mg-b0ae
had already finished, making my check 5 a worry about a resolved race — is
**REFUTED**: the race was live and closed by about a minute. The parent's note is
the only artifact that lets a later reader tell.

---

## 6. PREDICTION SCORING — 12 HELD, 8 REFUTED, 1 REFRAMED, kept as written

| P | claim | result |
|---|---|---|
| P1 (0.90) | condition present somewhere at (A) | **HELD** (formality, as declared) |
| P2 (0.65) | condition on first screen at (A) | **HELD** — char 1,195 |
| P3 (0.45) | condition on first screen at (B) | **HELD** — operative clause at char 3,654, 8.7% headroom |
| P3b (0.35) | condition detached from constant form somewhere | **HELD** — at `:21`/`:23` |
| P4 (0.95) | (LIB-weak) added by (A) | **HELD** (reproduction, H2) |
| P5 (0.55) | chain ends at `λ_std → 1` | **REFUTED** — ends at (LIB-const), *and my brief was wrong to ask* |
| P6 (0.80) | "never attacked" appears at (A) | **REFUTED** — 0 occurrences; the parent refused |
| P7 (0.75) | the fact survives to (B) | **REFRAMED** — it never was at (A); it *enters* at mg-c4f5, scoped |
| P8 (0.30) | a second arc attacked (LIB-weak) | **REFUTED** — exactly one, mg-c3ca |
| P9 (0.60) | headline = "true of hypothesis, false of implication" | **REFUTED as stated** — the page scopes it correctly; the real headline is that *my brief's premise* was 16 h stale |
| P10 (0.80) | a non-leading-form change exists | **HELD** — by the false-implication route, not the row-8 one I was handed |
| P11 (0.75) | no theorem statement changed | **REFUTED** — a stated implication's truth status changed |
| P12 (0.55) | a second ledger row's cell moved | **REFUTED** — row 8 only |
| P13 (0.85) | `900 = 18C/ε_spec` reconciles | **HELD** (reproduction, extended to a 2nd point) |
| P14 (0.55) | (A) prints a bare 900, no C | **HELD** — `"900C"` count 0 |
| P15 (0.50) | `2×10⁻²` unmarked as a calibration | **REFUTED** — "under the repaired calibration" at both |
| P16 (0.35) | the finite-n numbers were never added | **REFUTED** — both added by (A) |
| P17 (0.35) | commit names mg-b0ae | **HELD** |
| P18 (0.30) | …and dates it | **HELD** — and names the base commit too |
| P19 (0.55) | mg-b0ae had already completed | **REFUTED** — it landed 69 s *after* |
| P20 (0.30) | the edit understates in mirror | **HELD** — `900` as a point estimate of a floor |
| P21 (0.60) | a bound word is loose | **HELD** — `n ≈ 900` where `n ≥ 900·C₃` |

**My two pre-filed errors.** **P22 (mis-attributing a later defect to the parent):
NOT COMMITTED** — the guard held and it is what let me refute mg-c4f5's
attribution, which is the same error. **P23 (inflating framing into mathematics):
NOT COMMITTED** — the false implication passes the named-object test and the
missing condition at `:21` is filed as framing, explicitly.

**ONE DEFECT OF MY OWN INSTRUMENT, kept here rather than tidied away.** My first
attribution sweep for the row-8 contradiction used `grep -F 'closes this row as
phrased'` and returned **0 at every commit in STATE.md's history** — a result
that, taken at face value, says mg-c4f5 quoted a phrase that never existed. It
was my grep that was wrong: the file reads `closes **this row as phrased**`, with
markdown bold *inside* the quoted span, so neither the literal nor my looser
`closes this row` regex could match. A markdown-tolerant regex found it
immediately, at one commit. **A cleaner-looking run would have produced a
confident, false accusation against a prior audit** — and the only thing that
caught it was re-reading the raw cell instead of trusting a zero.

---

## 7. WHAT I DID NOT DO

- **I re-derived no mathematics of the program.** Not L4, not the master bound,
  not `(LIB-weak) ⟹ λ_std → 1`, not mg-88bd's constant form. This is a
  presentational audit by construction and every mathematical statement above is
  either arithmetic on the file's own printed formulas or a class-membership
  argument (`o(n²)` vs `≤ cn²`) that I did check.
- **I did not verify `ε_leak ≈ 0.20`, `C₃ = 1`, or the `18 = 6·3` numerator.** The
  `6` is the file's own `(ε_spec/6)`; the `3` I did not attribute to a source.
- **I ran no poset census.** mg-c4f5's 101,658-poset check and mg-131e's dual
  certificates are untouched; my (LIB-weak) census is over the **mg item store**,
  not the mathematics.
- **I did not open `docs/state-of-the-wall.html`**, so I cannot say whether the
  twin carries any of this.
- **I edited nothing.** No repair to STATE.md is proposed or made here — the
  `:21`/`:23` missing condition and the mg-345e currency defect are reported for
  pm-onethird to route, not landed. The false implication of §3b is **already
  repaired** in (B) and needs nothing.
- **I did not audit the other 11 intervening commits.** Findings about (B) are
  confined to the two I attribute explicitly.
