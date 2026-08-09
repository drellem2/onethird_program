# mg-d3c7 — PREDICTIONS for the INDEPENDENT AUDIT of mg-3969

Committed **before** `docs/OneThird-L4-Threshold-eps0-mg-3969.md` or any file under
`code/eps0_threshold_3969/` is opened, and before L4's source is read.

Everything I already know is listed in §A as **exposure**, not laundered into a
prediction. Predictions resting on exposed material are tagged `[FORMALITY]`;
only `[BET]` items are live.

---

## A. EXPOSURE — what I already knew before predicting

**H1 (LARGE, unavoidable, dispatch-delivered).** My dispatch prompt printed the
*full essay-length commit subjects* of both of the parent's commits. I did not go
looking for them; they arrived in the "Recent activity" block. They are:

- `f9fb63f` — "L4's THRESHOLD eps_0 IS NOT IN THE SOURCE AT ALL, THREE OBJECTS
  SHARE THE NAME, AND THE ONE mg-845e NAMES IS STRUCTURALLY UNMEASURABLE — while
  the one a proof CAN produce now has a PROVEN n-FREE CEILING 17/78 = 0.2179,
  nine per cent above the corpus's calibrated 0.20"
- `6fdf0ec` — "THE n=7 SWEEP LANDS AND THE HEADLINE CEILING DID NOT MOVE —
  `17/78` survives a 24× larger population intact, while the smaller-side ceiling
  drops to `13/111`"

This **pre-answers the brief's headline shape**: I know before I start that the
parent answered in the *negative* on "is eps_0 in the source", that it claims
three name-sharing objects, that it claims one is unmeasurable, and that it
claims an n-free ceiling of `17/78`. Every prediction about *what the parent
concluded* is therefore a formality. The live content of this audit is
**whether those claims survive re-derivation**, which the subjects do not tell me.

**H2 (small).** A grep for `L4` returned two lines of the parent's document
verbatim without my having opened it:
- `:28` — "> **exactly once** in all eleven lines of L4 (`:464–474`), in `F(ε)n`
  at `:469`, and **nowhere in**…"
- `:234` — "> **Remark 5.0 (the both-sides-chain escape is closed, and not by
  L4).**"

From `:28` I know the parent locates L4 at some file's lines `464–474`, eleven
lines, with `F(ε)n` at `:469`. I do **not** know which file. My check 1 (go to
L4's source myself) is therefore *partially* exposed: I know the line range the
parent claims, so my check is "is L4 there and does it say that", not "where is
L4". I will still locate it by my own route (searching the LaTeX corpus for the
statement, not for the line number) and will say which route found it.

**H3.** From `STATE.md:15`, read incidentally during orientation: the corpus
states the unit map `ε_spec/ε_c3ca = 6n²/(n²−1) → 6` explicitly, and warns the
two are "the same theorem in two normalisations — NOT two results, and NOT a
factor of 6 apart". So the lineage is *already alert* to the normalisation trap
the brief warns about. This lowers my prior that the parent fell into it.

**H4.** I have read mg-3969's own ticket body in full (it is the parent's brief,
not the parent's work). It forbids the modulus conflation *by name* and forbids
citing mg-3af9 for question 1.

**H5.** I have NOT opened: the parent's document, its README, any of
`a1_vacuity.py`/`a2_uniform.py`/`a3_witness.py`/`a4_mechanism.py`/`lib3969.py`,
any `out_*.txt`, or L4's source.

---

## B. THE GATE — the check the brief says comes first

**P1 `[FORMALITY, 0.85]` — the parent did NOT answer the modulus question.**
Its commit subject says "THRESHOLD" in the first four words and the ticket body
forbids the conflation in a named paragraph. A subject that loud is not the
shape of an accidental drift. *But the subject is not the argument*, so:

**P2 `[BET, 0.30]` — mg-3af9 or mg-c8c6 is cited somewhere LOAD-BEARING in the
parent's argument** (i.e. removing the citation would remove a step, not just a
cross-reference). The gate the brief describes is not "does the word MODULUS
appear" but "does the *route* pass through the consumption result". A document
that opens by denying the conflation can still lean on it three sections later
for a subsidiary claim — and the "STRUCTURALLY UNMEASURABLE" verdict is exactly
the kind of claim a consumption result is tempting for.

**Defect criterion, bound now:** I score the gate as FIRED only if a mg-3af9 /
mg-c8c6 citation supports a step in the chain answering question 1 (n-freeness)
or question 2 (value). A citation used to *distinguish* the modulus from the
threshold, or to answer question 3's disjunct (can eps_dem be reached without
eps_0), is CORRECT USE and I will say so rather than scoring it.

---

## C. THE RE-DERIVATIONS

**P3 `[BET, 0.55]` — L4's source is `one_third_width_three/step6.tex` or
`step8.tex`, and the lines `464–474` are in one of those two.** I know from
`OneThird-lambda-std-Operative-Form.md:114` that `step8.tex:2022 ff.` carries a
*different* `(L1)–(L4)` (band invariants), which the corpus already flags as a
name collision. If the parent's L4 is at `:464–474` it is a different file or a
different part. **Sub-bet `[BET, 0.35]`: the "THREE OBJECTS SHARE THE NAME"
finding includes the step8.tex band-invariant `(L4)` as one of the three.** If it
does not, that is a *fourth* collision the parent missed and I will report it.

**P4 `[BET, 0.45]` — the parent's "not in the source at all" is a
FAILURE-TO-FIND reported as an absence, not an enumeration.** This is the brief's
item 4 and it is the cheapest place for this result to be wrong. Specifically I
predict the parent establishes "`ε₀` appears zero times in L4's eleven lines"
(a true, checkable, *lexical* fact) and lets that stand for "L4 states no
threshold" (a *semantic* claim). A statement can carry a threshold without
spelling `ε₀` — "for ε sufficiently small", "there is an ε>0 such that", or a
hypothesis `ε < F(...)` all *are* thresholds. Since `:28` tells me `F(ε)n` occurs
at `:469`, **an `F` is present**, and an `F(ε)` in the conclusion with a
smallness hypothesis on `ε` is exactly a threshold under another name.

**Guard bound now:** I must read all eleven lines and enumerate *every*
smallness-of-ε device in them — named constant, unnamed "sufficiently small",
implicit-in-`F` domain, and quantifier-scope smallness — before I score P4
either way. If I score the parent's negative as sound, I must say which of these
four I checked and found empty.

**P5 `[BET, 0.40]` — the n-freeness of `17/78` is established by a FINITE SWEEP
plus an informal or absent extrapolation.** The two commits are an n≤6 sweep and
an n=7 sweep, and the second commit's own headline is that the ceiling "did not
move" — which is *evidence* of n-freeness, not a proof of it. The word "PROVEN"
in the first subject is doing work that two data points cannot do. To be wrong
here I need to find a monotonicity, padding, or embedding argument that
transports the n=7 ceiling to all n.

**Sub-prediction `[BET, 0.6 | P5 resolves as "there IS an argument"]`: the
argument is a PADDING/EMBEDDING one** — any n-poset embeds in an n'-poset for
n' > n with the ratio non-increasing — and it is stated in prose, not tested.
If it is stated I will try to *break* it by constructing the padded object and
measuring the ratio, not by reading the prose.

**P6 `[BET, 0.30]` — the "nine per cent above the corpus's calibrated 0.20"
comparison mixes normalisations.** Arithmetically `0.2179/0.20 = 1.0895`, so the
"nine per cent" is right *given the two numbers*. The risk is entirely in
whether `17/78` and `0.20` are the same kind of number. H3 lowers this: the
corpus states the `×6` unit map inline in `STATE.md:15` and shouts about it, so
the parent had the warning in front of it. **I will name my normalisation
explicitly** — I intend to check in **`ε_c3ca`** (the `E[inv_e] ≤ ε·n²`
normalisation of `OneThird-LIBweak-mg-c3ca.md:172`), because `0.2179` and the
`1/6 ≈ 0.167` figure the corpus quotes are the same order, whereas `ε_spec`
lands near `1`. **If `17/78 ≈ 0.218` sits in a family whose unconditional value
is `1/6 ≈ 0.167`, then a ceiling ABOVE `1/6` is the interesting object and the
`0.20` is plausibly also `ε_c3ca`.** That reasoning is a guess and I flag it as
one; I will settle it by reading both definitions, not by proximity of digits.

**P7 `[BET, 0.35]` — `78` and `111` are pair counts, not `n`-expressions.**
`78 = C(13,2)` and `111` is not `C(k,2)` for any integer `k` (`C(15,2)=105`,
`C(16,2)=120`). So the two denominators are **not** the same kind of object, and
`13/111` and `17/78` are probably ratios over *different* populations — which is
consistent with the second subject calling one "the smaller-side ceiling". If
they are ratios of the same functional over different denominators, comparing
them (or comparing either to `0.20`) needs the denominators named.

**P8 `[FORMALITY, 0.75]` — the "STRUCTURALLY UNMEASURABLE" object is
unmeasurable because it is defined by an existential over an object the corpus
cannot exhibit** (e.g. "the largest ε for which L4 holds", where L4 is unproved),
rather than because a search failed. This is the honest shape and the subject's
word "STRUCTURALLY" already asserts it. It is a formality because the subject
told me the answer; the live part is whether the *reason* given is a real
structural obstruction or a restatement of "we don't know".

---

## D. WHERE I EXPECT TO AGREE BY REPLICATION, NOT INDEPENDENTLY

**P9.** If I confirm the eleven-line span and the `F(ε)n` at `:469`, that is
**replication** — H2 handed me both. I will label it so and it will carry no
weight as corroboration.

**P10.** If I re-run the parent's `a1`–`a4` scripts and they agree with the
parent's `out_*.txt`, that is **reproduction of a computation**, not independent
confirmation of the mathematics. I intend instead to write my own enumerator
from the definition and compare *numbers*, not code paths. If I run out of road
and fall back to reading the parent's code, I will say the check is not
independent.

---

## E. MY OWN LIKELY ERRORS, filed in advance

**E1 — I score "eps_0 is not in the source" as a defect because I find a
smallness hypothesis, when the parent's claim is narrower** (e.g. "no *named,
consumable* threshold constant"). *Guard:* before scoring, I must quote the
parent's claim verbatim and check my counterexample against **its** words, not
against the commit subject's compressed headline. Commit subjects overstate; the
document is the claim.

**E2 — I declare a normalisation mismatch from digit-proximity.** `0.2179` vs
`0.167` vs `0.20` are all "about 0.2" and I will be tempted to infer the
normalisation from that. *Guard:* I must locate the *definition* of the
functional whose ceiling is `17/78` and the *definition* of the `0.20`, and quote
both, before asserting either is `ε_c3ca` or `ε_spec`.

**E3 — I attack the n-freeness of `17/78` while the parent never claimed the
sweep proved it.** The subject says "PROVEN n-FREE CEILING", but the document may
prove n-freeness by an argument and use the sweep only to show the bound is
*attained* — a completely sound division of labour that I would misread as
extrapolation. *Guard:* I must identify which artifact carries the n-freeness
claim (proof vs sweep) before scoring P5, and if it is a proof I audit the proof
rather than the sweep.

**E4 — I read the wrong L4.** The corpus has at least two `L4`s (ledger row 11,
and the `(L1)–(L4)` band invariants at `step8.tex:2022`), and the parent claims
three objects share the name `ε₀`. I could land on the wrong one and confidently
audit a different theorem. *Guard:* I must tie the L4 I read to **mg-845e's
gate** by an explicit chain of citations, and state that chain.

**E5 — I treat the ticket's framing as established fact.** The brief asserts the
lineage conflated threshold and modulus "twice already". I have not verified
that and I will not use it as evidence about the parent; it is context, not data.

**E6 — I do the forbidden work.** The brief forbids proving L4, deriving
eps_dem, and re-opening C_3. The temptation is largest on eps_dem, because
"is 0.2179 above 0.20" is one step from "so does the architecture close". *Guard:*
I compute ceilings and compare numbers; I do not draw the architectural
conclusion, and if I notice one I state it as out of scope.

---

## F. WHAT WOULD MAKE ME SAY "CONFIRMED"

All of: (i) the gate did not fire — no load-bearing mg-3af9/mg-c8c6 route;
(ii) L4 is where the parent says it is and says what the parent says it says,
read by me from the source file; (iii) the quantifier order is written out and
matches the parent's n-freeness verdict; (iv) `17/78` reproduces from a
definition I implement myself, in a normalisation I can name; (v) the negative
is an enumeration, and my attempt to construct the thing it says does not exist
fails.

Any of (i)–(v) failing is a finding, and I report it whether or not the
conclusion survives it.
