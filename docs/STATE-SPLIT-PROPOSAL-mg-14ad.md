# Splitting `STATE.md` — the proposal, the budgets, and what has already landed (mg-14ad)

**Status: PART LANDED, PART PROPOSED. Read the two apart.** The one-pager and the first
7,110 words of reduction are **landed** and are described in §1–§3 as fact. Everything from
§4 on is a **proposal with word budgets and is not landed**, because the ticket's own
sequencing note is right: *"propose the target structure first … a restructure that lands
and then has to be re-litigated costs more than the outline does."*

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
