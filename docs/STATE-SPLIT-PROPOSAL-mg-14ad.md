# Splitting `STATE.md` — the proposal, the budgets, and what has already landed (mg-14ad)

**Status: §1–§3 LANDED (mg-14ad). §4 LANDED EXCEPT ITS LEDGER ROW (mg-927a, 2026-08-13).**
`STATE.md` is **5,987 words**, inside mg-ea0e's standing 6,000-word target for the first time
since that target was set, and the ceiling is banked at 5,987 / 5,487. **§8 at the foot of this
document records what landed, which two budgets were not met and why, and the one row that
cannot land at all.** Read §4's table as the estimate it was, and §8 as the measurement.

---

## 0. What Daniel asked for

> *"STATE.md is failing at its function of being a high-level executive summary, because
> it's just way too verbose. Should be like a one-pager, followed by maybe a 5-pager with a
> bit more depth, and then reference material can be linked at the bottom"*
> — 2026-08-13 11:13Z

> *"Nothing should consume my executive summary document. If you guys need a state document
> for internal tracking do so but that's 2 functions in one. Also I recommend your internal
> state document is also short with links"*
> — 2026-08-13 11:35Z

Two documents, then. One for him, consumed by nothing. One for us, short, with links.

## 1. The design decision, which INVERTS the migration the ticket anticipated

The ticket's framing was: `STATE.md` becomes the executive summary, an internal document
is created beside it, **and every instrument, pin and line-number address migrates to the
new file.** It named the live collisions — `mg-20ee`/`mg-6e4f` (transcripts pinning
addresses into it), `mg-30bd` (verdict drift), `mg-7cc3`/`mg-daba` (the twin's pin), and
`code/state_ratchet_e331`'s ceiling.

**Measured before deciding: 516 tracked files reference `STATE.md`**, and every one of the
ten suites in `./build.sh`'s gated set is among them:

| gated suite | files referencing `STATE.md` |
|---|---|
| `code/state_ratchet_e331` | 8 |
| `code/alias_agreement_06d1` | 7 |
| `code/control_gate_724a` | 4 |
| `code/concepts_gate_602d` | 4 |
| `code/c3_audit_a94c3` | 4 |
| `code/gate_fixed_point_f771` | 4 |
| `code/facts_registry_03cf` | 3 |
| `code/l1b_application_28b6` | 3 |
| `code/twin_disposition_audit_3902` | 2 |
| `code/face_geometry_repair_e35b` | 1 |

**So the file that keeps the name keeps the readers, and moving 516 references is the most
expensive way to satisfy a requirement about function.** Daniel's requirement is that *his*
document is consumed by nothing. It says nothing about which file is called what.

**Therefore: `STATE.md` STAYS the internal document, and the executive summary is a NEW
file — [`EXECUTIVE-SUMMARY.md`](../EXECUTIVE-SUMMARY.md) at the repository root.** Zero
readers migrate. The ratchet does not move — it is already on the internal document, which
is where the ticket says it should end up. The twin pin, the address pins and the
verdict-drift census all keep pointing at exactly what they point at today.

**Why the root and not `docs/`:** `docs/` holds 167 markdown files and would bury it; more
importantly, several instruments in this corpus walk `docs/**/*.md` and `code/**/*.md`
(`code/species_extent_audit_6cb9/e2_crosssection.py` is one), and the root is outside every
such sweep. **Checked, not assumed: no suite in the gated set globs `*.md`** — they address
`STATE.md` by literal path and by content regex. A new root file is reachable by no
instrument in the loop.

**The half of the requirement that cannot be enforced, stated rather than implied.** Nothing
stops a future instrument from being pointed at `EXECUTIVE-SUMMARY.md`. What is available is
a declaration at the top of both files saying it must not be, and the absence of any
existing reader to imitate. **The exec summary deliberately gets no word-ratchet** — a
one-pager that needs a gate to stay a one-pager has already failed, which is the ticket's
line and it is correct.

## 2. What landed: the one-pager

[`EXECUTIVE-SUMMARY.md`](../EXECUTIVE-SUMMARY.md) — **721 words**, prose, no tables of rows,
reference links at the bottom. It states what the programme is trying to prove, the shape of
the attack, that the whole thing is reduced to one implication, that the open content of
that implication is the *size of a constant* and not its existence, that the ~50× gap is
**provably unreachable by the method that produced everything so far**, why the step is hard,
what else is open, and one caution about small-`n` evidence not supporting universal claims.

Nothing in it is restated from `STATE.md` mechanically; it was written from the ledger, the
proof chain, the L1b blockquote and the convergence section.

## 3. What landed: 7,110 words out of `STATE.md`, and the ceiling banked

**`STATE.md`: 21,328 → 14,218 words** (138,345 → ~92,000 bytes).

This is not a freehand cut. It is **the remedy the ratchet's own transcript already names**
— `code/state_ratchet_e331/out_p1_growth.txt` §3: *"The gap is 13077 words and it is a DEBT
with a named remedy (relocate attempt rows to their per-attempt files)"*, measured there at
**5 rows, 44,837 characters, 7,351 words**. Those five rows had never been relocated.

Done under **mg-34bf's existing convention** — move the Result column verbatim into
`docs/state-history/attempt-mg-XXXX.md`, leave the row asserting current state with a
pointer:

| row | attempt | Result column before | after |
|---|---|---|---|
| `:174` | `mg-345e` | 4,231 | 208 |
| `:177` | `mg-200d` | 10,099 | 483 |
| `:178` | `mg-ba78` | 5,483 | 199 |
| `:179` | `mg-76b2` | 9,954 | 571 |
| `:180` | `mg-51f4` | 14,241 | 966 |

**Line numbers did not move.** The relocation rewrites cells *within* existing lines and adds
no line to `STATE.md`; the pointer to the executive summary was appended to the existing
intro line for the same reason. `STATE.md` has the same 222 lines it had before. That is
deliberate — the documentary line-number addresses scattered through this corpus are already
partly rotted (`code/state_layer_audit_218d/render218d.py` addresses `STATE.md:382` in a
222-line file) and this landing does not add to the rot.

**The ceiling was banked in the same commit**, which the ratchet *forces*: it scores a cut
that leaves the ceiling behind as `SLACK`, a failure, precisely because *"mg-34bf cut 28,321
bytes and the file was back eight hours later; mg-ea0e cut 153,938 and it was 59% back in
four days."*

**A correction to the ticket's premise, since it is load-bearing for what to do next.** The
ticket reads the ratchet as complicit — *"the ratchet is holding it there … the target is
~40× wrong."* The ceiling is not a target and its own config says so at length: it is a
monotone floor under regression, set where the file stood so it binds from the day it lands
rather than being red-on-arrival and deleted within a week. **`CEILING.json` already records
6,000 words as the standing target and the 13,077-word gap as a DEBT with a named remedy.**
The ratchet was not defending 21,328 as correct; it was the only thing preventing 21,329,
and it carries the banking rule that makes this landing stick. It needed **using**, not
re-arguing.

---

# PROPOSED FROM HERE — NOT LANDED

## 4. Where the remaining 14,218 words are

Measured with the ratchet's own `sections()` decomposition:

| § | now (words) | proposed | what moves, and where |
|---|---|---|---|
| preamble / header riders | 946 | **150** | Five multi-hundred-word riders (FACTS.md, CONCEPTS.md, the twin, the ratchet, the `Kind` warning) → one line each, pointing out |
| The one-paragraph state | 1,987 | **250** | **It is a single 2,027-character line and it is not a paragraph.** Its three superseded readings and their correction history → `docs/state-history/headline-corrections.md`. Keep the current claim |
| Two axes, one bridge | 735 | **200** | The mg-05ec three-leg rider → its own document; keep the two axes and the dictionary |
| Glossary | 270 | **270** | **Keep as is.** Correctly sized and genuinely reference |
| The proof, and what's proven | 1,947 | **400** | Keep the mermaid and the two-open-links sentence. The machinery bullets' strike/re-derivation history → `docs/state-history/` |
| Kinds | 492 | **250** | Keep the mark table and the standing rule verbatim — they are load-bearing. Scope prose → reference |
| Full ledger | 2,887 | **600** | Rows 3b (8.5 KB), 6, 8 and 11 are essays inside cells. Per-row files, exactly as `ledger-row-11-L4.md` already does for row 11 |
| The single lemma to prove | 348 | **300** | Keep |
| Attempt index | 3,784 | **300** | **All rows to per-attempt files.** Keep verdict + attempt + one line. This is the section that regrows |
| Where the threads converge | 215 | **215** | Keep |
| Appendix A (audit-stage process) | 37 | **0** | → `docs/` |
| Why 1/3 — the elementary anchor | 689 | **0** | → `docs/`. Proven background, pure reference, no consumer in the argument |
| **total** | **14,218** | **~2,935** | ≈ 5 pages |

## 5. What makes this a judgement about the mathematics, not formatting

The rule proposed: **a row stays in `STATE.md` if the current argument consumes it; its
history leaves.** Three consequences worth arguing about before anyone moves a paragraph:

1. **Row 3b should probably not be a ledger row at all.** Its unconditional form is refuted
   and its open form *is row 8*. It is 8.5 KB explaining that it is not independent support
   for anything. A one-line row pointing at row 8 and a history file says the same thing.
2. **The `Kind` column and the standing rule are the most valuable 500 words in the file**
   and should be *promoted*, not compressed — they are what stops a reader aggregating an
   `n ≤ 7` exhaustive check into a universal claim.
3. **"Why 1/3 — the elementary anchor" is proven and consumed by nothing.** By this file's
   own rule (`docs/FACTS.md` exists for exactly this) it does not belong here.

## 6. Reader migration — the list, and why it is empty

Under the §1 decision **no reader migrates**: the internal document keeps its path.
What the §4 reduction *would* disturb, and must be coordinated with, is different and
smaller — instruments keyed to **content that moves out of a cell**:

| reader | keyed on | disturbed by §4? |
|---|---|---|
| `code/state_ratchet_e331` | word count of `STATE.md` | **Yes, by design** — ceiling re-banked in the same commit |
| `code/l1b_application_28b6` | 5 content regexes (L1b blockquote, Axis-1 bullet, mermaid node `C`, edge `B→C`, row 8) | **Yes** — all five are in sections §4 keeps; the regexes must survive rewording |
| `code/concepts_gate_602d` | `STATE.md` links to `CONCEPTS.md` | No, if the pointer stays |
| `code/facts_registry_03cf` | `STATE.md` links to `FACTS.md` | No, same |
| `code/rendered_twin_pin_9bc2` + `mg-7cc3`/`mg-daba` | per-ledger-row digest of `STATE.md` | **Yes** — the pin must be re-derived; the ledger rows §4 moves are the ones it digests |
| `mg-20ee` / `mg-6e4f` | line-number addresses | Only if lines shift. §3 shifted none; §4 will |
| `mg-30bd` | verdict drift | **Yes** — verdict text moving to a history file reads as drift unless told |
| `code/state_restructure_34bf` | rebuilds `STATE.md` from base `60f4dac` and requires byte-identity | **Already broken by every landing since 2026-07-30; not gated.** Named here, not fixed |

**§4 should not land until `mg-7cc3`/`mg-daba` and `mg-30bd` are told**, which is the
ticket's own sequencing point and the reason this document exists rather than a bigger diff.

## 7. Recommendation

Land §1–§3 (done). **Agree §4's budgets before moving a paragraph**, then land it as one
commit that re-derives the twin pin and re-banks the ceiling in the same landing. Do not
give the executive summary a ratchet.

---

# §8 — WHAT LANDED (mg-927a, 2026-08-13), AND THE TWO BUDGETS THAT WERE WRONG

`STATE.md` **14,337 → 5,987 words**. Ceiling banked **14,337 → 5,987**, `tighten_below`
**13,837 → 5,487**, in the same commit, per `CEILING.json`'s own `how_to_change_this`.

## 8.1 The measured outcome against §4's estimate

| § | §4 said | landed | what actually happened |
|---|---|---|---|
| preamble / header riders | 150 | **~400** | The `docs/FACTS.md` pointer must carry a live **entry count** (`code/facts_registry_03cf` §3 gates it) and the `docs/CONCEPTS.md` pointer must exist (`code/concepts_gate_602d`). Full riders → [`docs/state-history/state-preamble-riders.md`](state-history/state-preamble-riders.md) |
| The one-paragraph state | 250 | **~420** | The 1,634-word L1b blockquote → [`l1b-statement-full.md`](state-history/l1b-statement-full.md); the three superseded readings → [`headline-corrections.md`](state-history/headline-corrections.md). The struck clause and its replacement stay **together** in the row (mg-957a) |
| Two axes, one bridge | 200 | **~250** | mg-05ec's three legs → [`proof-chain-riders.md`](state-history/proof-chain-riders.md) |
| Glossary | 270 | **270** | kept, as proposed |
| The proof, and what's proven | 400 | **~490** | mermaid and the two-open-links sentence kept; node-`B` rider, machinery strike history and mg-65f5's fork resolution → `proof-chain-riders.md` |
| Kinds | 250 | **492 — UNCHANGED, DELIBERATELY** | **§4 and §5.2 of this document contradict each other and §5.2 wins.** §5.2 calls these "the most valuable 500 words in the file" and says they should be *promoted, not compressed* |
| Full ledger | 600 | **2,814 — NOT MOVED** | see §8.3. It was a blocker; §8.3a records the deadlock being broken (mg-1344) and it is now a **sequenced** deferral of two landings |
| The single lemma to prove | 300 | **~190** | plain-language restatement → `proof-chain-riders.md` |
| Attempt index | 300 | **~150 — the section LEFT** | see §8.2 |
| Where the threads converge | 215 | **215** | kept, as proposed |
| Appendix A | 0 | **0** | folded into the new *Reference material, linked* table |
| Why 1/3 — the elementary anchor | 0 | **0** | → [`docs/why-one-third-elementary-anchor.md`](why-one-third-elementary-anchor.md) |
| **total** | **~2,935** | **5,987** | |

## 8.2 The attempt index could not reach 300 with its rows in place — so the rows left

§4 budgets it **300 from 3,784** with the rows *staying* and only their Result cells relocating.
**Measured, that is unreachable.** mg-14ad's own relocation convention keeps each row's
Status-label and Attempt columns **verbatim in the row**, and across the 28 rows those two columns
alone are **~2,200 words** before a single Result cell is counted. The convention and the budget
cannot both hold.

**§5's own rule decides which gives way:** *"a row stays in `STATE.md` if the current argument
consumes it; its history leaves."* An attempt-index row is **by construction** a record of
something already walked, and no live ledger row consumes any of them. So the section moved whole
and verbatim to [`docs/state-history/attempt-index.md`](state-history/attempt-index.md), which is
also Daniel's own instruction — *"reference material can be linked at the bottom"*.

## 8.3 The ledger row of §4 cannot land in a merge request at all — and that is a finding

§4 budgets the **Full ledger 2,887 → 600**. §6 correctly flags that
`code/rendered_twin_pin_9bc2` digests those rows and that the pin must be re-derived after.
**It cannot be.** Four facts, each read out of the estate rather than assumed:

1. The twin's drift **worklist is a gated field** — `twin.worklist` in
   `code/control_gate_724a/BASELINE.json`. Move a pinned row without re-pinning and `./build.sh`
   goes RED, so the edit cannot merge on its own.
2. `twin_pin.py`'s `reconcile()` **refuses** while `STATE.md` on disk differs from `STATE.md` at
   `HEAD` — so the re-pin cannot be in the same commit as the row edit. Its own comment:
   *"THE COST IS TWO COMMITS INSTEAD OF ONE."*
3. `pin_target()` then looks for an **integration-reachable** commit carrying those `STATE.md`
   bytes. For a row that exists only on a branch there is none, so it falls back to `HEAD` and
   prints its own warning: *"THE REFINERY REBASES: this hash is rewritten out of existence when
   the branch lands and the pin becomes an ORPHAN, which section 7 grades RED."*
4. This is not hypothetical. `7e7bfb7 twin: point the pin at the commit that survives the rebase
   — 2fbd5ce did not exist after it (mg-cdd5)` is this repository's record of it happening, and
   mg-3902's audit records that the repair traded correct-and-unreachable for reachable-and-wrong.

**So a ledger-row relocation needs two landings — move + reconcile the twin's cell, then re-pin
once those bytes are on `main` — and nothing in the estate sequences that today.** That is the
carried remainder, and it is a sequencing gap in the pin mechanism rather than a paragraph nobody
got round to moving.

### 8.3a The estate sequences it now — mg-1344, 2026-08-13

**The sentence above is superseded in exactly one word: `today`.** `twin_pin.py` grew a
**section 8** and the two landings are a protocol the merge gate can tell apart from drift.

**Which of the four facts changed: (1), and not by making the gate quieter.** A relocation
declares its rows in `code/rendered_twin_pin_9bc2/IN-FLIGHT.json`; a declared row leaves
section 2's worklist and enters a second gated field, `twin.inflight`. `twin.worklist`'s
baseline is **unchanged at `[]`** — moving *that* value is the laundering-shaped edit and it
was refused. Facts 2, 3 and 4 are untouched and still correct.

**What buys the subtraction is an expiry nobody has to remember.** The declaration is
honoured only while `reachable_state_commit()` — *the same search `pin_target()` runs* —
finds no integration-reachable commit carrying those `STATE.md` bytes, i.e. only while
landing B is impossible. **The instant landing A merges, its own declaration is graded RED**
and stays red until landing B lands. Measured in both directions against a real git history,
not argued; `code/rendered_twin_pin_9bc2/README.md`'s section-8 table has the six worlds.

**The declared cost.** Between the two landings `main` is red for every branch, not only the
declaring one. The remedy is one command, section 8 prints it in the failure, and anyone may
run it. `COVERAGE.md` item 6 prices the three alternatives and why each is worse.

**THE LEDGER ROW STILL HAS NOT MOVED, AND mg-1344 DID NOT MOVE IT.** That branch ships the
mechanism and nothing else. The relocation is two further landings and they are a different
kind of work — deciding which of rows 3b, 6, 8 and 11's essay text §5's rule sends to
`docs/state-history/` is a judgement about the mathematics, not about formatting, and mg-927a
declined the same class of call for the same reason. **When landing A happens, `CEILING.json`
must be banked DOWN in that commit** to the **measured** post-cut word count with
`tighten_below` 500 under it — measured, never the §4 estimate, and never ~2,935, which §8.4
already refuses.

## 8.4 The two targets, reconciled explicitly

**mg-ea0e's 6,000 words STANDS and is now MET. The ~2,935 in §4 does NOT supersede it.** The
distance from 5,987 to ~2,935 is essentially the Full ledger, i.e. §8.3's blocker, so ~2,935 is
not a target that can be aimed at until that is sequenced. The ceiling is set at **5,987, the
achieved measurement** — not at 6,000 and not at 2,935: a ceiling is a monotone floor and binds
from where it is set, and 2,935 today would be **red on arrival by 3,052 words**, blocking every
merge in this repository for a reason no author of an unrelated branch could act on.

## 8.5 Coordination, done before a paragraph moved

`mg-30bd` / `p30bd`, `pm-onethird` (the `mg-7cc3` / `mg-daba` twin-pin lineage) and the mayor were
mailed before the first edit, with the section-by-section plan and the headline that **none of the
12 pinned ledger rows moves**. Verified after: `twin_pin.py` reports `VERDICT: CLEAN`, all 12 row
digests unchanged, worklist `(none)`. **Nothing needed re-deriving.**

## 8.6 The executive summary is still outside every instrument

Checked, not assumed: `grep -rl EXECUTIVE-SUMMARY` over the tree returns `STATE.md`, `README.md`,
this document, `state-preamble-riders.md`, and `code/state_ratchet_e331/CEILING.json` +
`out_ratchet.txt` — the last two being the ratchet's **prose declaration that it excludes the
file**, not a read of it. **No instrument reads `EXECUTIVE-SUMMARY.md`.** It gained no ratchet, no
pin and no address here.
