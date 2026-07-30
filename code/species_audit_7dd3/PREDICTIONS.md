# mg-7dd3 — PREDICTIONS, written BEFORE any run and before any instrument existed

**Rule for this file: it is written once and never edited.** Where a prediction is wrong the
wrong text stays and `OUTCOMES.md` records the miss beside it. mg-73df missed 4 of 60 and kept
them; mg-a4ef missed 5 of 22 and kept them. That is the bar.

Written after READING `106e121` (the mg-a4ef repair) and `ebecd89` (mg-73df), and after
reading `s1_extent.py`, `s2_seam.py`, `kerna4ef.py`, `stricken_a4ef.py`, `check_doc.py`,
`w3_scope.py`, `c5_doc.py` and the two committed outputs `out_s1_extent.txt` /
`out_s2_seam.txt` — and **before executing a single one of them.** Reading is how a prediction
is made; running is what it is a prediction about.

---

## A. REPRODUCTION (exit codes are the process exit code of the named script)

| # | prediction | exit |
|---|---|---|
| **A1** | `code/species_7d75/run_all.sh` re-runs; T1–T6 all `TOTAL BAD: 0`; all **7** committed `out_*.txt` byte-identical, `git status` clean for that tree | 0 |
| **A2** | `code/species_repair_6f61/run_all.sh` re-runs; `CHECK_DOC: PASS`; all committed outputs byte-identical | 0 |
| **A3** | `code/species_remainder_f8fa/run_all.sh` re-runs; `W3 SCOPE: PASS`; byte-identical | 0 |
| **A4** | `code/species_repair_a4ef/run_all.sh` re-runs; `S1 TOTAL BAD: 0`, `S2 TOTAL BAD: 0`; byte-identical | 0 |
| **A5** | mg-73df's `c4_scope.py` and `c5_doc.py`, re-run **unmodified**, reproduce `code/species_repair_a4ef/out_c4_scope_73df_after.txt` and `out_c5_doc_73df_after.txt` **byte for byte** | 0 / 1 |
| **A6** | `code/species_audit_73df`'s own committed outputs do **not** regenerate (declared, on purpose) | — |

## B. THE CLAIMED CORRECTIONS, CHECKED AT SOURCE AND NOT THROUGH ANY CHECKER

| # | prediction |
|---|---|
| **B1** | X3's struck sentence is absent from `t6_fock_and_record.py` except inside a passage that names mg-a4ef; the live prose there now says only *"T5 measures it on 4399 basis elements"* — **HOLDS** |
| **B2** | The same in the committed `out_t6_fock_and_record.txt` — **HOLDS** |
| **B3** | The AM §17.5 quotation in `t6_fock_and_record.py`'s docstring reads `Pi*` in both slots — **HOLDS** |
| **B4** | `t4_one_operation.py:22` reads ANTI-isomorphic with the correction marked — **HOLDS** |
| **B5** | §0's headline box reads *"anti-isomorphic to Solomon's descent algebra"* — **HOLDS** |
| **B6** | `w3_scope.py`'s docstring says 12 (not 6); `r2_columns.py`'s says 45 (not 40) — **HOLDS** |
| **B7** | §14 carries exactly ONE limitation box, and it is §14.2's — **HOLDS** |
| **B8** | *"a second, shelved filing"* is gone from the document — **HOLDS** |
| **B9** | §14.3's quoted sentence *"outside every beam currently pointed at this document"* is present in §14.2, so the by-name answer still resolves — **HOLDS** |
| **B10** | The deleted duplicate box said nothing §14.2 does not say (mg-a4ef: *"it said less"*) — **HOLDS** |

## C. EXTENT — the primary target

| # | prediction |
|---|---|
| **C1** | All three checkers print an extent statement in their own output — **HOLDS** |
| **C2** | `check_doc.py` reads exactly ONE file, as its extent line says — **MISS PREDICTED: it reads TWO** (the document and `OneThird-Species-Hopf-Monoids-Repair.md`, in C4). The `10 × 1 file` claim is about the STRICKEN list only and I predict that half is exact. |
| **C3** | `s1_extent.py`'s named exclusion list is the whole exclusion — **MISS PREDICTED: `tree_files()` filters on `.py/.txt/.md`, so the four `run_all.sh` are excluded silently and are not in the printed `SKIPPED, NAMED` list.** |
| **C4** | Injecting X3's sentence, unmarked, into `code/species_7d75/run_all.sh` → `s1_extent.py` **does not see it** | exit **0** |
| **C5** | Injecting the same sentence into a NEW `.md` inside `code/species_7d75` → seen | exit **1** |
| **C6** | Injecting it into `code/species_audit_73df` (declared silent) → not seen | exit **0** |
| **C7** | Injecting it into `docs/OneThird-Species-Hopf-Monoids-Repair-Extent.md` (declared silent) → not seen | exit **0** |
| **C8** | Running the union list over the **whole repo** finds ≥ 1 statement still asserted OUTSIDE the declared extent — i.e. the declared silence is not vacuous | ≥1 |
| **C9** | **THE BEYOND-LIST TARGET (see §E).** The exoneration rule `NAMES_A_REPAIR` matches any of five ticket ids within ±6 lines. I predict the fraction of `code/species_7d75` lines that sit on such "exonerated ground" is **> 10 % and < 50 %** |
| **C10** | `w3_scope.py` now exits **1** when it fails: run against `83ac472`'s tree it reports 12 problems | exit **1** |
| **C11** | `w3_scope.py` run against `ebecd89`'s tree — the state mg-73df audited — **PASSES**, which is mg-73df's control (b) | exit **0** |

## D. THE SEAM

| # | prediction |
|---|---|
| **D1** | The document has exactly **17** block quotes; `s2_seam.py` compares only the **11** longer than 300 characters, so **6 are compared against nothing and the printed EXTENT does not say so** — **HOLDS** (a defect of the target class) |
| **D2** | My own sweep over **all 17** block quotes, no length floor, threshold **0.45**: **no pair above 45 %** | 0 pairs |
| **D3** | My own sweep at threshold **0.30** over all 17: **at least one pair above 30 %** (short quotes share boilerplate) | ≥1 |
| **D4** | `s2_seam.py`'s local variable `quoted` (the sentence §14.3 quotes back at §14.2) is **never used** — dead code — and had it been used the check would have **FAILED**, because the document wraps that sentence across a `> `-prefixed line — **HOLDS** |
| **D5** | Every internal `§N.M` reference resolves — **HOLDS** |
| **D6** | `s2_seam.py`'s `subheaded` restriction silently drops **≥ 5** `§N.M`-shaped references from the resolution check | ≥5 |
| **D7** | `s2_seam.py` calls S2c *"THE THREE STALENESS PATTERNS"* but its `PATTERNS` table has **2** rows (5 checks print) — a count that disagrees with its own artifact, which is the five-versus-eight defect in miniature — **HOLDS** |

## E. OVER-CORRECTION — the live risk

| # | prediction |
|---|---|
| **E1** | All **15** of `c5_doc.py`'s `MUST_SURVIVE` rows still hold — **HOLDS** |
| **E2** | The 5 `MUST_ONLY_SURVIVE_STRUCK` rows still hold — **HOLDS** |
| **E3** | The document diff `ebecd89..106e121` **removes no claim and adds no hedge**; the one narrowing (§0's banner: *"the checker for the instrument"* → *"the checker for two of those corrections"*) is a correction of a **coverage** claim that mg-73df itself demanded, not a mathematical retreat — **HOLDS** |
| **E4** | Control (ii) is still stated as strengthened, in §5, §6 item 5, S7 and `t5_hopf_monoid.py` — **HOLDS** |
| **E5** | No `TOTAL BAD` anywhere in the four trees moved — **HOLDS** |

## F. MUTATIONS — exit code predicted for every one, before the run

All run against a **scratch copy** of `docs/` + the four code trees. In that copy there is no
git, so I predict `s1_extent.py`'s controls (a) and (b) print *"git unavailable -- SKIPPED"*
and are **not** counted as bad — so a clean scratch copy still exits 0.

| # | mutation | script | exit |
|---|---|---|---|
| **M0** | none (control on my own harness) | `s1_extent.py` / `s2_seam.py` | **0 / 0** |
| **M1** | restore `ebecd89:t6_fock_and_record.py` | `s1_extent.py` | **1** |
| **M2** | restore `ebecd89:out_t6_fock_and_record.txt` | `s1_extent.py` | **1** |
| **M3** | restore `ebecd89:t4_one_operation.py` | `s1_extent.py` | **1** |
| **M4** | restore `ebecd89:` the document | `s1_extent.py` | **1** |
| **M5** | restore `ebecd89:` the document | `s2_seam.py` | **1** |
| **M6** | §0 headline box back to *"is **Solomon's descent algebra**"* | `s1_extent.py` | **1** |
| **M7** | re-insert the deleted duplicate box into §14 | `s2_seam.py` | **1** |
| **M8** | delete the *"Eight things changed"* banner | `s2_seam.py` | **1** |
| **M9** | rename heading `### 14.2` to `### 14.5` | `s2_seam.py` | **1** |
| **M10** | delete the `CORRECTED AT SOURCE (mg-a4ef …)` marker line only, from `t6_fock_and_record.py`, leaving the struck sentence | `s1_extent.py` | **0** — over-determined: `mg-6f61` / `mg-f8fa` and the word `CLOSURE` all sit inside the same ±6-line window |
| **M11** | as M10, and strip every `mg-XXXX` token and the word `CLOSURE` from that window | `s1_extent.py` | **1** |
| **M12** | inject X3 into `run_all.sh` (= C4) | `s1_extent.py` | **0** |
| **M13** | inject X3 into a new `.md` in `species_7d75` (= C5) | `s1_extent.py` | **1** |
| **M14** | mutate the document so `check_doc.py` fails | `check_doc.py` | **1** |
| **M15** | my own detector, unmutated tree | `d2_extent.py` | **0** |
| **M16** | my own detector, one statement injected | `d2_extent.py` | **1** |

## G. THE ELEVENTH STRIKE — added in the same pre-run sitting, still before any execution

Counting the `~~strike~~` spans in the document (a `grep`, not a run) gives **11**. The "one
list" has 11 rows, but one of them is **Y2**, which has **no** struck sentence. So the list
covers **10 of the document's 11 strikes**, and the missing one is
*"as three independent agreements about the term"* (§1, line 301) — **mg-a61f's X8**, which is
on **mg-73df's `c4_scope.py`** list and on no other. The repair defines its union over
`check_doc.py` and `w3_scope.py` and stops there; the third list in the arc — the one it re-runs
unmodified and cites as independent corroboration — has a row neither of those two has.

| # | prediction | exit |
|---|---|---|
| **G1** | X8 is on `c4_scope.py`'s list and on **none** of `check_doc.py`'s `STRICKEN`, `w3_scope.py`'s `FORBIDDEN`, `stricken_a4ef.py`'s `CORRECTIONS` — **HOLDS** | — |
| **G2** | X8 is **not** currently asserted anywhere in the declared extent — it is a coverage hole, not a live falsehood — **HOLDS** | — |
| **G3** | **M17.** Un-strike §1's *"as three independent agreements about the term"* in a scratch copy — restore mg-a61f's X8 to live prose — and every checker in the arc still passes | `check_doc.py` **0**, `s1_extent.py` **0**, `s2_seam.py` **0**, `w3_scope.py` **0** |
| **G4** | **M18.** Assert X8 unmarked in `code/species_7d75` (a new `.md`): `s1_extent.py` still passes, `c4_scope.py` (mg-73df's, unmodified) **fires** | `s1_extent.py` **0**, `c4_scope.py` **1** |

If G3 holds, the repair's own generalisation — *"a union of lists is still a list"* — is true of
its own list one turn earlier than it says: the union was taken over two of the three lists that
existed when it was written.

## H. THE STRENGTHENED BRIEF — is each printed extent WIDER than what the code reads?

Added 21:20 after pm-onethird strengthened mg-7dd3. **Still before any execution.** One
mutation inside the claimed region and one outside it, per checker, both directions.

| # | checker, and the claim its extent line makes | probe | exit |
|---|---|---|---|
| **H1** | `check_doc.py`: *"enforces all 10 stricken sentences over ONE FILE … It reads no code."* | INSIDE: un-strike X3 in the document | **1** |
| **H2** | same | OUTSIDE: assert X3 unmarked in `code/species_7d75` | **0** — and the extent says so |
| **H3** | same — is it wider? | I predict **NOT wider, and NARROWER**: it also reads `OneThird-Species-Hopf-Monoids-Repair.md` in C4, which *"ONE FILE"* does not mention | narrower |
| **H4** | `w3_scope.py`: *"enforces TWO corrected statements — X4 and X5 — plus the character-ring rule, over ONE tree."* | INSIDE: assert *"three are controls"* unmarked in `species_7d75` | **1** |
| **H5** | same | OUTSIDE: assert it in `species_repair_6f61` | **0** |
| **H6** | same — is it wider? | I predict **NOT wider, and NARROWER**: W3c also enforces six positive readings in three named files, which the extent line omits | narrower |
| **H7** | `s1_extent.py`: *"11 corrections over the document and 4 code trees"*, *"SKIPPED, NAMED, so the exclusion cannot grow unseen — 5 file(s)"* | INSIDE: assert X3 in a new `.md` in a declared tree | **1** |
| **H8** | same | BOUNDARY: assert X3 in `code/species_7d75/run_all.sh` — a file inside a declared tree, not among the 5 named skips | **0 — WIDER THAN IT READS** |
| **H9** | same | OUTSIDE: assert X3 in `code/species_audit_73df` and in another `docs/` file | **0**, and declared |
| **H10** | `s2_seam.py`: *"S2a is a similarity sweep over ONE document and cannot see a duplicate spread across two documents, or one paraphrased below 45 %."* | INSIDE: duplicate a **long** block quote verbatim | **1** |
| **H11** | same | BOUNDARY: duplicate a **short** (≤ 300 normalised chars) block quote **verbatim, 100 % similar, in the same document** | **0 — WIDER THAN IT READS**, the 300-character floor is in no extent line |
| **H12** | same | the same for a short prose paragraph | **0** |

**Predicted verdict on the strengthened brief's own question:** two of the four printed extents
are wider than what the code reads — `s1_extent.py`'s named-exclusion claim and `s2_seam.py`'s
S2a limit paragraph — and the other two are narrower, which is the safe direction and still a
false statement. I predict **no printed extent overstates the STATEMENT COUNT**; both
overstatements are about **which text is read**.

---

## THE ONE I AM MOST LIKELY TO BE WRONG ABOUT

**M10.** The whole finding of this arc is that a `0` can be produced by an extent nobody
stated. The mirror of that is an exoneration nobody measured: if a hit is exonerated by four
independent phrases at once, deleting the marker the repair *points at* changes nothing, and
the marker is decoration. I predict exit **0** — i.e. that the marker is not load-bearing. If
it comes back **1** I was wrong and the marker really is what is holding.

## MY DECLARED BEYOND-BRIEF TARGET

**C9 — the reach of the exoneration rule, measured rather than argued.** No brief in this arc
names it. Every finding so far has been about what a checker *reads* or what it *looks for*.
Nobody has asked how much of the tree is ground on which a hit *cannot be reported at all*. A
`0 still asserted` over a tree that is 40 % exonerated ground is a different number from a `0`
over a tree that is 2 %, and neither is printed.
