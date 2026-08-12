# OneThird — COMPRESSION W1: **the claim `compression.tex:217` attributes to us is ABSENT from every artifact I searched.** No file states it. Where the corpus addresses the same question it calls it *delicate* and is built to avoid it, and the identification §4 needs in order to call the BK eigenvalue "standard" at all is **refuted** on our own board

**Work item.** `mg-bb60` (repo `onethird_program`), scoped by `pm-onethird` at `mg-bd28` off
Daniel's drop `mg-2ffd`. W1 of four; the one that gates the ranking.
**Subject.** [`docs/imports/compression.tex:217`](imports/compression.tex) — *"So, assuming your
agents' claim that the relevant standard eigenfunction is linear is correct, the spectral question
is essentially transformed into …"*
**Instrument.** Search only. **No computation was performed and none is claimed**; every finding
below is documentary — a file, a line, and what it says. Sections 1–4 of the note are **not**
assessed here; that is `mg-8bc7` (W2).

---

## 0. Verdict

> ## **ABSENT — the claim is not in the corpus, and it is not ours.**
>
> Of the ticket's four statuses — proven / empirically observed / conjectured / audited down —
> the one that holds for the claim **as attributed** is **none of them, because there is no
> artifact to grade.** Outside `compression.tex:217` itself, no file in any repository, work
> item, mailbox, or agent transcript on this machine states that the relevant standard
> eigenfunction is linear, in that or any paraphrase I could construct. Nothing was audited
> down, because nothing was ever put up.
>
> **Two things sit next to the empty space, and both point away from the note:**
>
> 1. **The corpus has a name for exactly this question and its posture toward it is
>    avoidance.** `step8.tex` — the live Step-8 file, in **both** one_third repos — writes that
>    its argument *"avoids the **delicate question** of whether the minimum-energy eigenfunction
>    of the BK Laplacian is itself a pair function."* The superseded `old/width3.tex` names the
>    same object twice more, once inside a proof (*"this is not yet fully developed"*) and once
>    in its own **Summary of Gaps**. So the premise `compression.tex` assumes *we* supplied is,
>    in our own files, an **open question we deliberately routed around** — the corpus's
>    treatment of it is the reason Theorem E is proved by averaging over pair functions instead.
>
> 2. **The adjacent premise §4 needs is worse off than absent — it is refuted.** For the BK
>    eigenvalue to be "the standard-representation eigenvalue" at all requires **standard
>    dominance**, `STATE.md` row 3b, whose **unconditional form is `FP✗` — REFUTED** (166
>    explicit refuters at moderate-λ `n = 7`), and whose surviving conditional form **is L1b —
>    row 8, THE WALL, the open problem the whole programme is stuck on.**
>
> **Consequence — the ticket's third branch, and it fires.** §5's stated relevance to
> (1/3)–(2/3) does not follow from anything in the corpus. It is not conditional on a weak claim
> of ours; it is conditional on a claim that is **not ours at all**, and whose nearest true
> relatives are an avoided open question and a refuted one. **The ranking rests on an
> unestablished premise.** §1–3 are untouched by this finding — their status is W2's.

---

## 1. What I searched, named, before concluding a negative

The ticket asked for the artifact to be named. Every row is a search that ran; the "control"
column is what proves the search could have found something.

| # | Artifact | Scope | Control | Result |
|---|---|---|---|---|
| A1 | `/Users/daniel/research/` — **all seven repos** (`onethird_program`, `one_third`, `one_third_width_three`, `riemann`, `union_closed`, `lineara`, `investments`) | working trees at HEAD, **every file type** (no extension filter; `.git` excluded), proximity regex `eigen*` ↔ `linear`/`pair function` within 140 chars either way | the run returned `compression.tex:217` itself | **1 hit: the note.** Everything else was vendored `mathlib` or the phrase "linear extension" |
| A2 | `onethird_program` **full git history** | all commits, `*.md *.tex *.txt *.py` | returned `44d08ea:docs/imports/compression.tex:217` | **1 hit: the note, at its import commit** |
| A3 | `one_third` (364 commits) and `one_third_width_three` (639 commits) **full git history** | all commits, same globs | `'pair function'` returns **713** / **639** blob hits — the search reaches the right files | **0 hits** |
| A4 | `union_closed` (227), `riemann` (25), `lineara` (65), `investments` (1) **full git history** | all commits, fixed string `eigenfunction` | — | only `riemann/notes/*` (prolate/Slepian — a different subject; A1 already showed no `linear`-proximity there) |
| A5 | `~/.macguffin/work` — **every work item in every state** (`available`, `claimed`, `done`, `archive/2026-04` … `2026-08`) and `~/.macguffin/mail` — **every mailbox** | fixed + proximity | 72 `eigenfunction`/`eigenvector` hits, all read | **0 state the claim.** Nearest: `mg-8201:21`, `mg-740d:19`, `mg-b0a6:25` — see §3 |
| A6 | `~/.macguffin/events.jsonl` | fixed string | — | 0 |
| A7 | `~/.claude/projects` — **1.5 GB of Claude Code transcripts**: every agent session on this machine, all polecats, all crew agents, Daniel's own sessions | fixed-string battery: `standard eigenfunction`, `eigenfunction is linear`, `eigenvector is linear`, `linear eigenfunction`, `eigenfunction is a pair`, `span of pair functions`, `is a linear statistic` | each string was verified findable — `eigenfunction is linear` returns 5 files in 1.4 s | **every hit is from today's compression arc** (mayor, `pm-onethird`, and the W1/W2/W3 polecats), i.e. **quotations of Daniel's note**. The one earlier `span of pair functions` hit (`polecat-7ae7`) is that agent **reading `step8.tex`** |
| A8 | `~/files` — the import drop the note itself came from | listing | — | `compression.tex` + 4 unrelated files; nothing else about eigenfunctions |

**The one place I cannot search, stated because it is where the claim most plausibly lives.**
If "your agents" refers to a conversation that left no artifact on this machine — a web chat, a
different model's UI, a session whose transcript was never written here — then the claim exists
and I would not see it. **A1–A8 cannot rule that out and are not offered as ruling it out.**
What they establish is narrower and is the thing the ticket needs: **nothing anyone can cite
today carries it**, so nothing built on §5 can inherit a status from it.

---

## 2. The corpus's own treatment of the same question — three sightings, all avoidance

These are the nearest statements *in meaning*, not merely in vocabulary. `compression.tex` §2
(`:68–72`) defines its "linear statistic" as `f(L) = a + Σ_{{x,y} ∈ I(P)} c_xy · 1{x <_L y}` —
the span of the pair-orientation indicators. That span is, verbatim, the corpus's **"span of
pair functions"**. So the corpus does discuss the note's premise; it just never grants it.

**S1 — the live file, and it is a refusal to assume it.**
`one_third_width_three/step8.tex:389–394` (identical
text at `one_third/step8.tex:377–382`), inside
*Remark [Why a single-cut argument suffices]*:

> "Lemma `dirichlet-conductance` is what bridges the two formulations: once a frozen pair
> exists, the *single* cut `S_xy` automatically has small conductance, without invoking
> Cheeger's inequality for the full BK walk. **This avoids the delicate question of whether the
> minimum-energy eigenfunction of the BK Laplacian is itself a pair function.**"

And immediately after, `\textbf{G1 status.}` (`:397–406`, the "no … invoked" clause at `:403–405`)
records what the proof does consume:
*"No pair-Poincaré inequality, representation-theoretic input, or rigid-spine lemma is invoked:
averaging over the `C(n,2)`-sized family of pair functions …"*. **The architecture of Theorem E
is what it is because this question is not answered.** `STATE.md` row 6 is `U`/proven at the
price of exactly that.

**S2 — the same object, called undeveloped, inside a proof.**
`one_third/old/width3.tex:509–511`:

> "A rigorous proof would require a careful analysis of the BK adjacency graph on `L(P)` and
> the structure of minimal-energy eigenfunctions of the associated Laplacian, localized in the
> span of `{f_xy}`; **this is not yet fully developed.**"

**S3 — and on the gap list.** Same file, `:674–677`, under *Summary of Gaps and Next Steps*:

> "**Lemma `BK-shape-classification`:** BK shape classification. This requires analyzing
> minimal-energy eigenfunctions of the BK Laplacian on `L(P)` **in the span of pair functions**,
> and proving that any BK-frozen pair forces one of the three shapes …"

`old/` is the superseded outline, so S3 is not live; it is included because it shows the
question was on the books as an **unproved component** from the beginning and left there.

**Status of the premise, graded on the corpus's own words: CONJECTURED AND EXPLICITLY
AVOIDED.** Never proven, never measured, never assumed by any live argument.

---

## 3. The empirical relative — a different object, and it does not say "linear"

`mg-b0a6`'s kill-shot probe is the only place the corpus puts numbers anywhere near this, and
it is worth being exact about what it measured, because it is the likeliest source of a
misremembering.

`one_third_width_three/docs/OneThird-Spectral-NearOrdinalSum-KillShot-Probe.md:127–142`:

- **(a) Soft claim — SUPPORTED.** Kendall-τ between the **dominant standard eigenvector's
  coordinate order** and the **expected-rank order**: **median 0.857, mean 0.842, min 0.286**,
  over 126 both-connected posets at `n ≤ 6`. The document's own gloss: *"'Largely' is fair."*
- **(b) Exact lemmas — FALSE.** *Exact order identification* (eigenvector order = expected-rank
  order) **fails on 85/126**, all 100 inversions genuine, `ΔE[pos]` up to 1.5 positions.
  *Monotone along `<_P`* fails at **2/126**, and — the part that matters — at the **two highest
  `λ_std` in the set** (0.9239, 0.9256), i.e. inside the near-1 bad-mixing regime the programme
  is about. This is `STATE.md` row 9, **refuted as stated**.

Three reasons this cannot stand in for the note's premise, each checkable against the two
definitions rather than argued:

1. **It is an order statistic, not an identity.** τ = 0.86 with a minimum of 0.286 says the
   coordinate *ordering* correlates. It does not say the eigenvector *is* any particular
   function, and the exact form of that guess was tested and **failed on two thirds of the
   population**.
2. **It is about a vector in `R^n`, not a function on `L(P)`.** `λ_std` is *defined* in the
   glossary — and `STATE.md:78` says so in as many words — as `max spec(S_P|_{1⊥})`, an `n × n`
   **transport** object over the **elements of `P`**, **"not a block of the BK spectrum over
   `L(P)`."** `compression.tex`'s eigenfunction is a function on linear extensions.
3. **"Linear" in the corpus means a *test vector*, and a test vector is how we avoid needing
   the eigenfunction.** The "crude linear test vector `u`" of program §9 and the expected-rank
   `r = T_P u` of `OneThird-L1b-ExpectedRank-Certificate.md:84–90`
   are centred-position vectors used to **lower-bound** `λ_std` by a Rayleigh quotient. That
   document calls `r` the eigenvector's *"natural smooth proxy"* — proxy, on the strength of the
   τ = 0.86 above. **A Rayleigh lower bound needs no claim about the eigenfunction whatsoever**,
   which is precisely why the corpus uses one.

**Status of this relative: EMPIRICALLY OBSERVED in its soft form, AUDITED DOWN — false as
stated — in every exact form, and about a different object either way.**

---

## 4. The bigger problem for §4 and §5: the word "standard" is not ours to lend

`compression.tex:201` says the compression converts *"the allegedly important
standard-representation eigenvalue"* into a two-projection problem, and §5 builds the
(1/3)–(2/3) relevance on that. Independently of whether the eigenfunction is linear, **the
identification of the relevant BK eigenvalue with a standard-representation eigenvalue is
`STATE.md` row 3b — and it is refuted.**

[`STATE.md:112`](../STATE.md) (row 3b), verbatim marks:

- **(a) The UNCONDITIONAL statement is REFUTED, not unproven** — `mg-8b64`'s BK-transport probe
  exhibits **166 explicit refuters at moderate-λ `n = 7`**. Mark: **`FP✗`**.
- **(b) The all-pairs-frozen CONDITIONAL is OPEN — and it IS L1b, i.e. row 8**, the wall:
  `L1b ⟺ "all-pairs-frozen ⇒ standard dominance"`.
- **(c) The `0/132` is a SAMPLING ARTIFACT and is NEVER QUOTABLE BARE** — its frame (`n ≤ 6`
  exhaustive + `n = 7` **top-λ spot only**) excludes the known refuters.

And two further facts that bear directly on §4's move:

- **`λ_std` and `λ₂^BK` are INCOMPARABLE.** `STATE.md:78`: no universal inequality holds in
  either direction — `A₂ ⊕ A₂`: `λ_std = 1 > 2/3 = λ₂^BK`; `A₃ ⊕ A₃`: `1 > 9/10`; the reverse
  fails on antichains — **exact rationals, `mg-d1be`**. Theorem E's bound on `λ₂^BK` gives
  **nothing** for `λ_std`.
- **The `0/132` was Cayley-walk evidence, not BK.** [`docs/state-history/threads-chronology.md:38`](state-history/threads-chronology.md)
  (`mg-4a86`, merged + audited): it is *"**Cayley-walk** evidence (all of `S_n`, where Schur
  forces `S_P = ρ_std(η_P)`), **NOT the BK chain**; the brief mis-attributed it."* The same
  entry gives the **honest BK-side statement**: *"slowest BK mode has **Ω(1) standard-sector
  component**"* — an **overlap**, still open, and conspicuously **not** "the slowest BK mode
  *is* a standard/linear function."

So the strongest true thing the corpus can say about the slowest BK mode and the standard sector
is an open Ω(1)-overlap conditional. `compression.tex:217` needs an equality of function
classes. The distance between those two is the whole of §5.

---

## 5. Consequence, stated plainly, as the ticket requires

1. **§5 is not conditional on a weak claim of ours. It is conditional on a claim that is not
   ours.** Nothing on this machine states it. The ranking that put this note above `riemann`
   was made on the strength of §5, and §5's stated bridge to (1/3)–(2/3) currently rests on an
   attribution that does not resolve.
2. **The corpus's own posture on the same question is avoidance, not support.** `step8.tex`
   calls it delicate and is architected to sidestep it; `old/width3.tex` filed it as an
   unproved gap. If someone now sets out to prove it, that is a **new open problem**, not the
   discharging of a known one — which is a fair thing to attempt, but it must be ranked as
   such.
3. **Worse, the premise §4 needs to name the eigenvalue "standard" is refuted unconditionally
   and open exactly where L1b is open.** §5 therefore does not convert an open problem into a
   fact; on the corpus's current board it converts one open problem (bad mixing ⇒ `1 − λ_std`
   small) into another (`Ran Π_o` vs `Ran Π_e` overlap on the standard representation) **while
   passing through a step that is refuted in general**.
4. **§1–3 are untouched by any of this.** Whether the cube foliation and the energy identity are
   correct is `mg-8bc7`'s (W2's) question, and nothing here should be read as bearing on it.
   `pm-onethird` believes they hold; this document neither confirms nor disputes that.
5. **W4** (the alternating-projection / canonical-correlation inequality the note proposes) is
   worth **exactly** what the premise at `:217` is worth. On today's evidence that is: an
   unattributed assumption, sitting on a refuted identification. **Not "worth real effort" on
   the strength of §5.**

---

## 6. A defect of my own, kept

**D1 — my first sweep of the transcripts was a broken instrument that returned a clean zero.**
The regex proximity search over `~/.claude/projects` (`grep -rloE` with an `eigen*`↔`linear`
window) ran for **6 m 35 s**, exited quietly, and reported **0 files**. That zero is **false**:
a fixed-string `grep -rlF 'eigenfunction is linear'` over the same tree finds **5 files in
1.4 s**, one of which is *my own session transcript*. I did not check a positive control before
reading the result, and for some minutes I held a negative that the instrument could not have
produced honestly. It was caught only because a follow-up control on a single large file hung
past its timeout and made the regex's behaviour on long JSONL lines visible.

Every transcript conclusion in §1 (row A7) rests on the **fixed-string battery**, which is
controlled — each probe string was verified to be findable before its absence was read as
information. Row A3's history search was likewise re-run with a positive control (`'pair
function'` → 713 / 639 blob hits) after D1, because it too had reported a bare zero.
**A search whose zero has never been shown to be a zero is not evidence, and this ticket is
about a claim nobody had looked for.**

---

## 7. What this document does not do

- **No file is repaired and no premise is argued to be probably fine** — the ticket forbade
  both, and there is nothing to repair: `compression.tex` is a verbatim import and stays one.
- **`STATE.md` is not edited.** Nothing here is a ledger movement: no row changes kind, and the
  finding is about a document that is not on the ledger. If W2/W3/W4 conclude the note belongs
  on the board, that edit is theirs and it goes through the `mg-e331` ratchet.
- **No mathematics was checked and nothing was computed.** Every claim above is of the form
  *"file F, line L, says S"*, and the figures quoted (166 refuters, `0/132`, τ = 0.857, 2/126,
  85/126) are **read from the documents that publish them and are not re-measured here** — the
  same evidence bound `STATE.md` row 3b puts on its own.

---

## DRIFT NOTE — the two cross-repo anchors in §3, and why neither is edited (mg-96df, 2026-08-12)

**Appended, never inserted: every line number above is exactly where it was.**
This file is itself cited at `:126` and `:83` by
`code/mirror_staleness_cdd5/README.md` and its transcripts, so a banner at the
top would have broken live anchors while repairing a report about broken anchors.

**`KillShot-Probe.md:127–142` (§3) is at `:180–195` at `949c439`.** All sixteen
lines land contiguously at one offset and are **byte-identical** — the quotation
in §3 is faithful, character for character, and only its coordinates moved.
Durable form: `## Kill-shot 3 — Monotonicity (L2) — AMBER`. **`ExpectedRank-Certificate.md:84–90`
did not move at all** and is correct as written; durable form `## 1. The certificate`.

**This anchor is not in the "correct when written" class, and saying so is the
point of dating it.** `7058fbd` wrote it on **2026-08-12T12:44:17Z**; the lines
had moved on **2026-08-07T22:20:29Z** (`a8688f2`), five days earlier. It resolved
at `912f1b1` because the mirror checkout it was read from stood at 2026-07-19 and
had not moved for twenty-four days. **This is a stale read, caught in the act** —
the same evidence mg-cdd5 used to establish that authors here were reading the
mirror checkout and not `origin/main`. It changes nothing in §3: the quoted text
is verbatim and the reasoning that rests on it stands.

**The number is left, deliberately.** mg-cdd5's standing rule is that a record of
what was read at the time is not improved by being re-pointed at what is true now
(`code/mirror_staleness_cdd5/README.md`, §5), and the coordinates above are part
of this document's evidence that the read was stale. Re-derive with
`code/anchor_drift_96df/run_all.sh`; the numbers here are true at `949c439` and
at no other revision, which is why the section name is given beside each one.
