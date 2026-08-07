# mg-eba7 — predictions for the INDEPENDENT AUDIT of mg-55f2 (row 3b only)

Committed **before** `git show 276aead` is run, before `STATE.md` is opened, and
before any grep for `0/132`, `166`, `clean sweep` or `row 3b` is executed against
either the pre-state or the post-state. The only things read so far are: `mg show
mg-55f2`, `git log --oneline -- STATE.md` (subjects only), and the blob-identity
check below.

## 0. What version I am auditing — named before anything else

- Dispatch named `STATE.md` at commit **491d42c79f7628c18cb7a5d197faa9f4600cd6c1**.
- `main` HEAD at the start of this audit is **dafe75910f731927affdf366457d681e262acf62**.
- `git rev-parse 491d42c:STATE.md` = `git rev-parse dafe759:STATE.md` =
  **7f73bfc87b4bc4caab6c836f8c3922a2416863cf**.

So STATE.md has **not** moved since the dispatch SHA. The file I audit is blob
`7f73bfc`, reachable at both. mg-55f2 landed at **276aead**; two commits touched
STATE.md *after* it (`21ee93f` mg-9adf, `491d42c` mg-b488), so the post-parent file
is not the parent's own output byte-for-byte and I must not conflate them.

## 1. Prior exposure — disclosed, not laundered into predictions

**H1.** I have read mg-55f2's ticket body in full. It contains pm-onethird's ruling
verbatim, including requirements (a) unconditional dominance REFUTED with 166
refuters at moderate-λ n=7 (mg-8b64), (b) the all-pairs-frozen conditional is open
AND IS L1b, (c) 0/132 always with its frame `n<=6 exhaustive + n=7 top-lambda spot`.
Any prediction that the landed row contains (a)/(b)/(c) is therefore a
**compliance check against a written instruction**, not a blind forecast. Scored as
such below.

**H2 — this one guts my check 1 as an out-of-sample test.** mg-55f2's commit
*subject* is in my dispatch context and in `git log`: *"the ESCAPED 'clean sweep'
phrase is struck at every site it reached, **in BOTH files**"*. So the parent has
already told me its own answer to the sweep question (two files) before I sweep.
P3/P4 below are therefore **reproduction attempts of a stated claim**, and the only
part of check 1 that is genuinely out-of-sample is whether a site exists that the
parent's two-file frame does not reach — non-`.md`/`.html` files, `code/` outputs,
`.tex`, and commit messages. That is where I will spend the effort.

**H3.** I have seen mg-957a's commit subject (`d41d18c`), which discusses rows 3b/9/10
and the FP/FP✗ asymmetry. I have **not** seen its body and have not seen the escaped
sentence itself in situ.

**H4.** My dispatch withdraws checks 6–9 (deliverable 2). I know in advance the
width≥3 row should be ABSENT and that its absence is the correction working.

**H5.** I know from `git log` that mg-9adf and mg-b488 edited row 8 after mg-55f2. I
do not know whether they touched row 3b.

**H6.** I have not read `docs/OneThird-mg65f5-ThreeFollowups.md`, the L1b doc, or
mg-b0a6's / mg-8b64's probe documents.

## 2. Declared search frame for the independent sweep (check 1)

I commit to this frame **before** running it, so that a null result is falsifiable
rather than an artifact of a narrow grep:

- **Corpus:** every tracked file in the repo at `dafe759`, and the same at
  `276aead^` (the parent's input state), with no extension filter — `.md`, `.html`,
  `.tex`, `.py`, `.txt`, `.json`, `.sh`, and anything else tracked.
- **Needles (case-insensitive, regex):** `0/132`, `0 of 132`, `\b132\b`, `clean
  sweep`, `\bsweep\b`, `\b166\b`, `row 3b`, `\b3b\b`, `standard dominance`,
  `all-pairs-frozen`, `all pairs frozen`, `top-lambda`, `top-λ`.
- **Also swept, and reported separately because they are OUT OF REACH of any patch:**
  git commit messages (`git log --all --grep`) and mg ticket bodies. A figure that
  survives only there cannot be struck; recording that is not the same as scoring a
  defect.
- **Defect criterion, bound in advance so I cannot tune it after seeing the hits.**
  A surviving site of `0/132` is a **defect** only if BOTH: (i) it is used as
  evidence for, or support of, a claim — as opposed to a probe document reporting
  its own measurement — AND (ii) the frame `n<=6 exhaustive + n=7 top-lambda spot`
  (or a faithful paraphrase) is not present in the same sentence, same table cell,
  or the immediately adjacent sentence. A source document stating its own result
  inside its own declared scope is NOT the escaped figure and I will not score it as
  one.

## 3. Predictions

Confidence in brackets. Deliverable 1 only; deliverable 2 is withdrawn.

**P1 [80%]** At `276aead^` the string `0/132` occurs at **≥ 3** sites repo-wide,
and at **≥ 2** sites outside STATE.md's row-3b cell.

**P2 [70%]** The exact escaped phrase (`clean sweep` in the same sentence as
`0/132` or `row 3b`) occurs at `276aead^` in **both** `STATE.md` and
`docs/state-of-the-wall.html` — mg-957a landed nine aggregating sentences across
both files, so a single-file escape would be the surprise. *(Reproduction of H2,
scored as such.)*

**P3 [75%]** At `dafe759`, `clean sweep` applied to row 3b / 0/132 occurs **0**
times in `STATE.md` and `docs/state-of-the-wall.html`. *(Reproduction of H2.)*

**P4 [45%] — the genuinely out-of-sample half of check 1.** At `dafe759` there is
**at least one** surviving site of `0/132` outside `{STATE.md,
docs/state-of-the-wall.html}` — most likely in `docs/` (a probe or L1b document) or
a `code/**/out_*.txt`. I predict **most such sites are NOT defects** by my §2
criterion (they are source documents inside their own scope), and I put **[30%]**
on there being at least one that IS a defect: cited as evidence, frame absent.

**P5 [55%]** `166` does **not** appear anywhere in `STATE.md` at `276aead^`, i.e.
mg-55f2 **introduced** it into the ledger. If so, the relocation that check 3 names
did in fact occur, and the whole question is whether provenance travelled with it.

**P6 [40%] — my single most likely finding.** The restated row 3b marks the row
with an empirical/finite-population kind (`FP✗`, `FP`, "refuted by exhaustive
search", or similar) **without** an at-the-cell statement that 166 and 0/132 were
*read from mg-8b64's and mg-b0a6's probe documents and not re-measured here*. That
is precisely the laundering step — a mark that reads as measured attached to a
figure that is U-by-citation. I expect the words "refuted" and "166" to be present
and the words "read"/"not re-measured"/"by citation" to be the thing that is
missing.

**P7 [85%]** The restated row states the unconditional form is REFUTED (a) and
names 166 with mg-8b64. *(Compliance check per H1.)*

**P8 [80%]** The restated row says the all-pairs-frozen conditional is OPEN and
that it **is** L1b (b) and (check 5) does not read as independent empirical support
for L1b. *(Compliance check per H1.)*

**P9 [20%]** The restated row overstates — reads as refuting the conditional too,
killing L1b by accident (check 4). Low, because the ticket names this hazard
explicitly, but it is the expensive direction so I will check it at the sentence
level and not at the keyword level.

**P10 [88%]** No width≥3 ledger row is present at `dafe759`. Its absence is
correct (mg-5998 owns it) and I will not score it.

**P11 [50%]** The escaped phrase survives in at least one **git commit message**,
where it cannot be struck. If so I report it as out-of-reach, not as a defect of
mg-55f2.

**P12 [35%]** Row 3b's cell is **not** byte-identical between `276aead` and
`dafe759` — i.e. one of mg-9adf / mg-b488 disturbed it. Most likely benign
(reflow), but if row 3b moved after the correction landed, the correction's
survival is a separate question from its landing.

**P13 [30%]** There is a *third* file carrying the ledger (beyond `STATE.md` and
`docs/state-of-the-wall.html`) — an aggregating doc or README — that cites row 3b
and that a two-file sweep would miss.

**P14 — the lost-check report.** I predict [60%] that mg-5998 has **not** yet
landed, so the question "did the width≥3 row re-inherit Sah's exception class?"
cannot yet have been asked of it. I will check whether any audit item carries that
check for mg-5998 and say so either way, per my dispatch.

## 4. My two most likely errors, filed in advance

**E1 — scoring a source document as an escaped figure.** mg-b0a6's probe document
is *entitled* to say `0/132`; that is its own measurement inside its own declared
frame. If I count it, I manufacture a defect and the parent gets a false RED. Guard:
the §2 defect criterion is bound above, in writing, before the grep runs, and every
hit gets classified against it in a table with the surrounding sentence quoted, not
summarised.

**E2 — scoring a mark as laundering without reading what the mark means in this
file.** This ledger has its own kind vocabulary (`U`, `U-id`, `FP`, `FP✗`, `OPEN`)
introduced by mg-957a. `FP✗` may already *mean* "finite-population refutation" with
provenance carried elsewhere in the file's legend. Guard: before scoring P6 I will
read the ledger's own legend/key at `dafe759` and quote it, and I will score
"laundered" only if the file's own vocabulary does not already carry the
read-not-measured distinction at a place the reader of row 3b actually meets.

**E3 (third, weaker).** Conflating mg-55f2's output with the current file. Two
commits landed on STATE.md after it. Guard: every finding is reported at BOTH
`276aead` (did the parent do it?) and `dafe759` (does a reader meet it today?), and
where those differ I say so rather than blending them.

## 5. What I am not attempting

- Re-measuring 166 or 0/132. This audit is documentary; both figures stay
  U-by-citation on my side too, and I will not pretend otherwise.
- Deliverable 2 (checks 6–9), withdrawn by pm-onethird's re-scope.
- Any edit to STATE.md, the HTML twin, or any source document. This branch adds an
  audit record only.
