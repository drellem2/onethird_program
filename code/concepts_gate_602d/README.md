# mg-602d — the gate behind `docs/CONCEPTS.md`

`./run_all.sh`, ~0.2 s, standard library only. Two arms; the worst exit wins.

| arm | what it asks |
|---|---|
| `c0_concept_discipline.py` | Does the conceptual document obey its own two rules — a pointer on every claim row, the word `BELIEF` in every unearned claim — and is it short, link-clean, and reachable from `STATE.md`? |
| `c1_controls.py` | Can `c0` fire? Six planted worlds that must go red, one that must **refuse**, and one that must stay **green**. |

## Why there is a gate at all

`docs/CONCEPTS.md` records what the objects **mean**. That makes it the easiest file in the estate
to get wrong in a way nobody notices: prose about meaning carries no population and no arithmetic,
so a sentence that was true when written stays perfectly readable long after the ledger row that
earned it has moved. `STATE.md` row 3b's `0/132` is the same shape one level down — a figure that
outlived its frame — and the answer here is the answer there: **carry the pointer with the claim.**

The ticket that commissioned the document said so in as many words, and this suite is that
paragraph made mechanical:

> every conceptual claim carries a pointer to the item or document that earns it, and anything that
> is intuition-not-yet-earned is marked as such in the sentence, not in a footnote.

## What `c0` checks, and the two things it does not

**Checks.** `POINTERS` (every row of §2 and §5 ends in an `mg-XXXX`, a ledger row, or a link into
`STATE.md`/`FACTS.md`) · `MARKERS` (every §6 item contains `BELIEF`) · `LENGTH` (≤ `WORDS_CEILING`,
declared in `c0` with its reason) · `LINKS` (every relative link resolves) · `FINDABLE` (`STATE.md`
links to the document — otherwise nobody arrives, and `docs/FACTS.md`'s housekeeping section makes
the identical argument about itself).

**Does not check that a pointer is CORRECT.** Only that one is *there*. Whether `mg-8d66` says what
the row claims it says is a reading of a dozen documents; it was done by hand at `mg-602d` and is
not done by this file. The gate is on **structure**, not on truth — the same split, for the same
reason, as `code/facts_registry_03cf/f0_registry_discipline.py`. That limit is **measured, not
asserted**: `c1`'s last world swaps a real item id for `mg-0000` and the gate stays green on
purpose. A reader who takes a green `c0` for *"the citations were checked"* is reading that world's
result backwards.

**Does not survive a silent rename.** Sections are located by anchor phrases in their headings. A
reworded heading makes `c0` **refuse** (exit 2), not pass — *"could not tell"* must never map onto
*"nothing wrong"*, and a gate that quietly stops checking is worse than no gate because it is a gate
people believe in. If you reword a heading, fix the anchor in `c0` **in the same commit**.

## A defect of this suite's own, kept

**`c1` was broken on its first execution, and it broke in the direction that hides a dead gate.**
It planted its corrupted copies in a `mkdtemp` *inside* `docs/`, one level below the real document.
`c0` resolves relative links against the document's own directory, so every honest link in the
planted copy (`FACTS.md`, `../STATE.md`) was dead and every world came back red — including the
**positive control** and the **wrong-direction world**, i.e. precisely the two whose job is to
prove the harness is not simply always-red. Six greens on the must-fire worlds would have looked
like a working control suite; what they actually measured was a harness that could not produce
anything else.

It was caught because the two worlds that must *not* fire are in the suite at all. That is the
entire argument for including them, and it is why the fix is recorded here rather than quietly
applied: this arm exists to rule out a gate that cannot fire, and on its first run it *was* one.

## Raising the word ceiling

One edit, in the commit that causes it: move `WORDS_CEILING` in `c0_concept_discipline.py` and say
in the commit message what the words are and **why they could not be a citation instead**. That
last clause is the whole test — *"cite, do not restate"* is the document's own first rule, so
almost every honest reason to grow the file is a reason to cite something instead.

This is deliberately **not** `STATE.md`'s ratchet (`code/state_ratchet_e331/`). That one is a
monotone floor with a banking rule, because `STATE.md`'s failure mode is unbanked cuts. This is a
plain cap, because `CONCEPTS.md`'s failure mode is the opposite one: nothing here needs to shrink,
and the only thing that must not happen is silent growth into a second `STATE.md`.
