# mg-28b6 — the thing that asks whether mg-0e8c's restatement is still applied

`mg-0e8c` answered Daniel's challenge to row 8 and merged its finding (`b364767`, `ca8d254`,
`799b1ff`). This directory is not a re-derivation of it. It is the **application audit** and the
control that keeps the application from rotting.

---

## 0. What was actually true when this landed — measured, not asserted

The ticket that produced this directory was filed on the premise that *"the finding is not yet
applied to the documents it is about."* **That premise is false, and saying so is the first
finding here.** `mg-0e8c` applied it in the same commit as the finding, at nine sites, and banked
the ceiling raise (`code/state_ratchet_e331/CEILING.json`, 20,784 → 21,328, "IN THE COMMIT THAT
CAUSED IT"). Verified site by site before anything in this directory was written:

| site | state on arrival |
|---|---|
| `STATE.md:21` L1b blockquote | restated + rider, `mg-0e8c` |
| `STATE.md:31` Axis-1 bullet | rider, `mg-0e8c` |
| `STATE.md:67` mermaid node `C` | relabelled — `E[inv_e] ≤ (ε/6)(n²−1)`, *"the SIZE is what is open"* |
| `STATE.md:72` mermaid edge `B→C` | relabelled — *"the CONSTANT must clear `ε_dem`; `ε_sup < 1` is proven and misses by ~50x"* |
| `STATE.md:125` row 8 | restated per the deliverable §3 |
| `docs/CONCEPTS.md:126` §4 | restated, *"equivalently"* replaced |
| `docs/OneThird-ProofShape-mg-3af8.md:46`, `:282` | riders |
| `docs/state-of-the-wall.html:263`, `:409` | reconciled, old text struck |

So the work this ticket actually had to do was the **fourth** thing `mg-0e8c`'s VERDICT REQUIRED
clause asked for and the one it delivered least completely: *the list of other sites carrying the
same phrasing*. Its own scored predictions say so — `P6`, **MISS**: *"there are seven … the
rendered twin's two cells make nine"*, having predicted four.

## 1. The site the enumeration missed, and why the miss was structural

**`docs/state-of-the-wall.html:385–386`** — the twin's proof-chain rendering of the very mermaid
edge and node `mg-0e8c` moved in `STATE.md`. It read:

> **L1b** — bad mixing ⟹ λ_std → 1. This is the anti-concentration LIB / (B), and the one
> genuinely missing implication.
>
> [node] λ_std → 1 · *near-ordinal-sum*

That is the **limit** rendering — which row 8's own cell calls *"a stronger rendering that happens
to be available, not the requirement"* — standing where `STATE.md` now leads with the constant and
names the size as the open content. A reader of the rendered page was still calibrating against
the wrong target, which is the exact failure the whole restatement was filed about.

**The miss was not carelessness.** Three things line up:

1. `code/rendered_twin_pin_9bc2/COVERAGE.md` declares proof-chain prose **out of scope** — *"only
   the `Full ledger` table is digested … the historically most common form of this defect is out
   of scope"*. `mg-0e8c` reconciled the twin's two **ledger** sites, the gate went red when it
   tried to defer them, and it went green again once they moved. Nothing could go red for `:385`.
2. `mg-957a` **named this exact lag a fortnight earlier and left it**: *"its row 8 still says
   `λ_std → 1` where `STATE.md` now leads with `1 − λ_std ≤ ε_spec`"*
   (`docs/OneThird-TheoremE-Width-and-Row-Kinds-mg-957a.md:249`). A known, recorded, unfixed lag
   in an uncovered region is exactly what a later sweep of the same region does not re-find.
3. The lag had already survived one restatement of the same row (`mg-188d`'s limit-vs-constant
   reconciliation, which moved the row-8 cell and not the chain).

**Fixed here**, old text struck rather than deleted, in the same convention `mg-0e8c` used at
`:263` and `:409`.

## 2. What is NOT re-pinned, and why that is the point

`code/rendered_twin_pin_9bc2/COVERAGE.md` item 4 names the single easiest way to defeat the twin
mechanism: *"a caller who edits nothing and re-pins anyway gets a green control over a stale
page."* This work item edits the twin and **does not re-pin it**, because `STATE.md` is byte-identical
to what the pin already names — no ledger row moved, no cell moved, and the whole-file digest is
untouched. Re-pinning here would have been that exact defeat, performed by the work item whose
subject is a control's blind spot. The pin is green before and after (`sh
code/rendered_twin_pin_9bc2/run_all.sh`, exit 0 both times) **and that green says nothing about
`:385`** — which is the whole reason `c0` exists.

## 3. The arms

| arm | what it asks | cost |
|---|---|---|
| `c0_application.py` | Is the restatement applied at all **12** anchored sites right now? And does the discharged phrasing appear anywhere in the four canonical files, in an L1b context, without a rider or a strike? | 0.02 s |
| `c1_controls.py` | Eight planted worlds against COPIES: seven that must fire or refuse, one that must stay **GREEN on purpose**. | 0.30 s |

Suite: **0.34 s measured**, wired into `build.sh` (route 1 *and* route 2, per that file's header).

**A rename must be LOUD.** If an anchor is missing or ambiguous, `c0` exits **2** — refused, not
passed. A gate that quietly stops checking is worse than no gate: it is a gate people believe in.

**The context filter is what makes this a claim sweep and not a phrase sweep.** *"uniform in `n`"*
is used in this corpus about at least four different statements — `C₃^(III) = 1`, `(L*)`, `ε₀`'s
form, and L1b — and `mg-8d63` already measured that (`docs/landing-mg-8d63-the-lstar-refutation.md:57`:
58 hits under `docs/`, *"every one a DIFFERENT statement"*). An occurrence counts only with an L1b
token within 240 characters. Without that filter this arm would fire on `STATE.md:179–180`, which
are about `C₃^(III)` and `(L*)` and are correct as written.

## 4. THIS REMEDY IS AN ARTIFACT OF THE SAME KIND AS THE DEFECT, so here is the enumeration

The defect was: *a claim, in prose, in a region no control reads, that stayed readable after the
thing it describes moved.* Every way this remedy could be that same thing:

| how this fix could exhibit the defect it repairs | checked |
|---|---|
| **The fix is itself prose in the uncovered region.** `:385–386` is exactly as unread by the twin pin after the edit as before. | **TRUE, and it is why `c0` exists rather than the edit standing alone.** `c0` is the first thing in the estate that reads that prose. |
| **`c0` could be prose about a control rather than a control.** | `c1` runs eight planted worlds and every row states an exit *and* a string, with the string checked for **absence from the unmutated baseline** (`mg-9876`'s guard). 8/8. |
| **`c0` could pass by checking something that cannot fail.** | The `mg-9876` guard above is precisely this check; three of my first draft's rows failed it (their expect-strings were site labels that print in the green report too) and were rewritten, not deleted. |
| **`c0`'s green could be read as "the sentences are true".** | It is not, it cannot be, and `c1`'s **W8** measures the gap: put the discharged phrasing back as row 8's lead while keeping the rider and `c0` stays **green**. Structure, not truth — the same split `code/facts_registry_03cf` and `code/concepts_gate_602d` declare. |
| **A new bare sentence could be added right next to an existing rider and pass.** | **TRUE** — the sweep is windowed (±600 chars, or the same line), so it catches a new site elsewhere in the file, not a new sentence inside an already-corrected block. Declared in `c0`'s docstring; not closed. |
| **The env seam `L1B_28B6_ROOT` could be used to make a red run green.** | It only relocates the tree being read; every rule is evaluated against whatever tree that is, and the live tree is never written by either arm. |
| **This README could claim a runtime it never ran.** | `0.34 s` and the gate's `45.6 s` are both `time` output on this host, not addition — `mg-17aa`'s D4, which `build.sh`'s own `mg-602d` block was corrected for. |
| **The audit could "verify" the nine sites by reading `mg-0e8c`'s claim that it moved them.** | Every one was read in the tree, and the two mermaid sites were read against `git show b364767` to confirm what the labels said *before*. |

## 5. What this directory does not do

* **It does not re-litigate `mg-0e8c`.** The finding is merged, measured over 5,230 posets, and
  carries its own pre-correction defect in the record. Nothing here re-derives it.
* **It does not touch the archival sites.** `docs/state-history/` and the write-ups that state the
  form as their own subject at the time they were written are listed in the deliverable's §5 and
  must not be edited — an attempt file records what was believed when it was written.
* **It does not extend the twin pin.** Extending section 2 of `twin_pin.py` to named prose blocks
  is still the obvious next move, still not done, and now has one worked example of what it would
  have caught.
* **It adds no words to `STATE.md`**, so no ceiling raise is due — see the deliverable's
  application-audit section for the ratchet's own arithmetic on that.
