# mg-3e06 — predictions for the INDEPENDENT AUDIT of mg-5ce3's §5.3 landing

Committed **before** any script of this audit exists, before one byte of the
diff of `4ef64d7` is read, before `STATE.md` is opened, and before
`docs/OneThird-LIBweak-mg-c4f5-IndependentAudit.md` is opened.

Per this programme's convention, prior exposures are **disclosed, not laundered
into predictions**. My exposure here is unusually large and I say so rather than
scoring formalities as hits.

---

## H — WHAT I ALREADY KNOW (exposures, disclosed)

**H1 (LARGE, and it guts several of my checks as bets).** My *first* search of
this audit was `git log --grep='mg-5ce3'`, and this repo writes essay-length
commit subjects. I therefore read the **entire** subject of `4ef64d7` before
writing one word here. That subject already asserts, in mg-5ce3's own voice:

  - the construction it used — `g(n) = n²` below `N₀`, `n²/log₂ n` at and above;
  - the machine check — `N₀ = 15, 100, 900, 10⁶` at `13/13, 98/98, 898/898, 4998/4998`;
  - the site count — ticket said four, there are **six**, line 115 carrying two;
  - which four changed (15, 23, 64, 115a) and which two did not (206, and 23's
    surviving contrastive "unspecified");
  - that the mg-d1a2 guard's **instruction** is untouched and its **reason** kept
    and attributed beneath a stronger one;
  - that row 8 carries an explicit "what it does not claim" class/member rider;
  - both §5.3 figures (`2³⁰⁰ ≈ 10⁹⁰`, `2³⁰⁰⁰⁰ ≈ 10⁹⁰³¹`).

So checks 1, 3 and 4 of my brief are **verifications of a stated claim**, not
blind tests. I cannot un-read it. What I *can* still do independently, and what
this audit is actually worth, is: (a) derive §5.3 from the **audit document**
rather than from mg-5ce3's rendering of it, (b) build a violator by a **different**
route than theirs and check the general principle rather than their one witness,
(c) read the **bytes now on the page** rather than the bytes the subject claims,
and (d) run the one check the parent structurally *could not* run — see H2.

**H2 (STRUCTURAL, established before predictions).** `4ef64d7` is an **ancestor**
of `491d42c`. mg-5ce3 landed, and *then* mg-b488 rewrote STATE.md on top of it.
`git log -1 -- STATE.md` returns `491d42c`, not `4ef64d7`. mg-5ce3 could not
possibly have verified its own survival past a later rewrite of the same file,
and its commit subject makes no claim about it. **This is the live half of this
audit.**

**H3.** `4ef64d7` touched exactly one file, `STATE.md`, `4 insertions(+), 4
deletions(-)`. So it is a four-line change and any claim of a fifth changed site
is false by arithmetic.

**H4.** My dispatch prompt carries the mayor's note that mg-131e REFUTED
`eps_spec = 2/(n+1)` at n=6 and that mg-372e is striking it across source docs.
§5.3's arithmetic uses a scalar `ε_spec = 2×10⁻²`. I have not yet checked whether
those are the same object.

**H5.** My dispatch prompt carries mg-5ce3's ticket body verbatim, including the
PM's paraphrase "**NO N_0 EXISTS**" and the PM's explicit statement that they did
not re-derive it. The commit subject separately flags that this paraphrase is
"a shade looser" than the audit's wording.

**H6.** I have read the `a682e1d` (mg-d1a2) commit subject in full, so I know the
guard's wording, that it was appended to row 8's cell at STATE.md:115, and that
mg-d1a2 *deliberately declined* lines 15 and 23 as "that audit's landing, not
this one".

---

## P — PREDICTIONS

Marked **[BET]** where the outcome is genuinely open to me, **[FORMALITY]** where
H1 has already told me the answer and I am only checking the bytes.

### The mathematics (check 1 — re-derive §5.3, build the violator)

- **P1 [BET, 0.85].** §5.3 of the audit document supports the strong reading —
  i.e. it is a statement quantified as *for every candidate N₀ there exists a
  violator*, not *we could not find an N₀*. Open to me because I have mg-5ce3's
  reading of §5.3 but not §5.3.
- **P2 [BET, 0.93].** I will build a violator **by a different construction than
  mg-5ce3's** and it will work, because the real content is a *general principle*
  and not a particular witness: **(LIB-weak) is an asymptotic hypothesis, and every
  asymptotic hypothesis is invariant under modification on a finite prefix, while
  (LIB-const) is a pointwise inequality that a finite prefix can violate outright.**
  Any `h = o(n²)` satisfying (LIB-const) eventually, redefined to `n²` (or `n²·k`,
  or anything ≥ the bound) on `[1, N₀)`, is still `o(n²)` and still violates
  (LIB-const) on all of `[1, N₀)`. I predict `n²/log log n`, `n²/√(log n)` and a
  plain `n^{1.99}` tail all serve equally, so §5.3's `n²/log₂ n` is illustrative
  and not load-bearing.
- **P3 [BET, 0.80].** The *sharpest* form is stronger than "for any N₀ a violator
  exists": **no function of the hypothesis alone can yield N₀**, because (LIB-weak)
  is a qualitative `o(·)` statement carrying no rate, and N₀ is a rate-derived
  quantity. I predict §5.3 says something of this shape, and that this — not the
  witness — is why the direction is closed.
- **P4 [BET, 0.55].** There is a **degenerate-witness trap** available and I bet
  mg-5ce3 did *not* fall into it, but I will check: a "violator" that fails
  (LIB-const) only at small `n` where the bound is vacuous or where `E[inv_e]` is
  not even defined (e.g. `n = 1`, `n²−1 = 0`) proves nothing. I predict the
  violation is exhibited at `n` where the bound is non-vacuous, and I will re-run
  it at `n ≥ 2` only.
- **P5 [FORMALITY].** `log₁₀(2³⁰⁰) = 90.309`, `6/(2×10⁻²) = 300`,
  `6/(2×10⁻⁴) = 30000`, `log₁₀(2³⁰⁰⁰⁰) = 9030.9`. All four hold.
- **P6 [BET, 0.70].** The `ε_spec = 2×10⁻²` in §5.3 is a **fixed scalar target**
  (a leak-derived constant), not an instance of the n-indexed `2/(n+1)` that
  mg-131e refuted, so the refutation does **not** touch §5.3's arithmetic. If it
  did, this landing would be resting on a dead formula and that would be a
  finding — hence I state the bet rather than assuming the benign reading.

### Did it overshoot (check 2 — the expensive direction)

- **P7 [FORMALITY, per H1].** Ledger row 8 carries an explicit "what it does not
  claim" rider separating **class** from **member**.
- **P8 [BET, 0.40 that at least one site overshoots].** This is my **principal
  live bet**. The short sites — line 15 (one-paragraph state), line 23 (Axis 1),
  and especially **line 64 (the mermaid node label, which mg-5ce3's own subject
  says was "kept short")** — cannot carry the class/member rider without becoming
  long. A rider that exists only at row 8 does not protect a reader who meets the
  claim at line 15 or in the diagram. I predict **at least one short site states
  the universal flatly**, and I predict the **mermaid label at line 64 is the most
  likely offender**, because "kept short" is exactly the pressure that drops
  qualifiers. Whether that rises to BROKEN or to a NOTE depends on whether the
  flat statement is *false* or merely *unqualified* — I pre-commit to that
  distinction now, before seeing it, so I cannot tune it afterwards:
    - **BROKEN** if a site asserts something §5.3 does not prove (e.g. "no family
      satisfying (LIB-weak) has any threshold", or "(LIB-const) never holds").
    - **NOTE** if a site asserts the class statement correctly but tersely, with
      the rider reachable at row 8.
- **P9 [BET, 0.75].** The distinction between "for the implication
  (LIB-weak) ⇒ (LIB-const)" and "for the programme's use of it" is **not**
  separately addressed anywhere, because it is a subtler axis than class-vs-member
  and no one has named it. If row 8's "any argument needing N₀ must first prove
  something strictly stronger than (LIB-weak)" is on the page, that *does* cover
  it, and I will say so — but I bet it arrives as a by-product rather than as a
  distinction someone drew.

### The four/six sites (check 3)

- **P10 [FORMALITY].** Six occurrences of "unspecified" in the pre-image
  (`4ef64d7^`), on five lines, with line 115 carrying two.
- **P11 [BET, 0.85].** The two left behind are genuinely different: line 206 is
  mg-33f5 literature material, and line 23's survivor is contrastive. I predict
  line 206's parenthetical really does carry §5.3 in the same sentence (mg-5ce3
  claims this and it is checkable byte-for-byte), and that leaving it is correct.
- **P12 [BET, 0.90].** No blanket replace: the diff is 4/4 on one file (H3), which
  forecloses a sed sweep, but I will still diff the untouched lines to confirm
  nothing moved silently.

### The mg-d1a2 guard (check 4)

- **P13 [FORMALITY].** `DO NOT CITE THE LITERATURE BOUND AGAINST THIS N₀` and
  `discharges nothing here` are present in the STATE.md I read.
- **P14 [BET, 0.80].** The guard's **original reason** ("an unspecified threshold
  is not a size any number can exceed") is still present *and still attributed to
  mg-d1a2*, not silently overwritten. I bet on present; I flag that the honest
  failure mode here is subtler than deletion — a strengthening can leave the
  instruction intact while replacing the reason such that the guard now only
  refuses citations *for the new reason*, and if the new reason is ever weakened
  the guard falls with it. I will check the guard is **over-determined**, i.e.
  refuses on either reason alone.
- **P15 [BET, 0.85] — THE LIVE ONE, from H2.** mg-b488 rewrote STATE.md **after**
  mg-5ce3. I predict mg-5ce3's four edits and mg-d1a2's guard **all survive
  491d42c intact**, but this is the one check neither parent could run, and a loss
  here is the whole audit. I will verify by diffing `4ef64d7:STATE.md` against the
  working-tree `STATE.md` restricted to the guard and the four sites, byte-for-byte
  on the substrings, not by eye.

### My own most likely errors, filed in advance

- **P16.** *Scoring a reflow as a loss.* STATE.md's row 8 has been edited by
  mg-d1a2, mg-9adf, mg-5ce3 and mg-b488 in one day. Line numbers WILL have moved
  and cell contents WILL have been re-wrapped. I bind myself, before reading:
  **the guard test is a byte-for-byte substring search over the whole file, not a
  line-number or line-content comparison.** A moved line is not a lost line.
- **P17.** *Scoring the audit's careful wording as a hedge.* "No N₀ works for the
  class" is **stronger and more precise** than the PM's "NO N_0 EXISTS", not
  weaker. If I find mg-5ce3 landed the audit's wording over the ticket's, that is
  a **credit**, and I pre-commit to scoring it that way rather than as
  under-delivery against the ticket text.
- **P18.** *Mistaking my own H1 contamination for confirmation.* Where the page
  agrees with the commit subject I must not report that as independent
  verification. Every FORMALITY above is tagged as such and will be reported as
  a byte check, not as a re-derivation.

---

## WHAT I WILL NOT DO (pre-committed)

- I will not re-open line 206 or the mg-33f5 document; out of scope by the
  parent's own instruction and mine.
- I will not audit mg-c4f5's §§ other than 5.3, except where 5.3 depends on them.
- I will not re-derive the poset-side meaning of `E[inv_e]`; §5.3 is an argument
  about function classes and I audit it as such.
