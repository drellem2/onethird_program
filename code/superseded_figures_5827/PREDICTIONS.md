# PREDICTIONS — `mg-5827`, the superseded-figure sweep

**Committed BEFORE any script of this instrument exists.** Nothing below has been run.

**What this instrument is for.** `mg-2860` swept four sites for the superseded-`ε_spec` class on
2026-08-06 and missed a fifth, which `ab6fa` then found by reading the right document. The two edits
are already landed (commits `c413c9e`, `7645941`). This instrument answers the question underneath
them: **is there a repeatable way to find every site quoting a superseded input**, so that this stops
being discovered one at a time.

---

## Measurements already taken BY HAND — disclosed, not laundered into predictions

These are things I already know because I did the repair. They are **not** predictions and must not
be scored as hits.

* **M1.** `docs/OneThird-lambda-std-Operative-Form.md` carried the superseded `ε_spec = 2×10⁻⁴` and
  its dependents at **12 sites**, not the one the ticket named. I repaired all 12 in `c413c9e`.
* **M2.** The ticket named `docs/OneThird-lambda-std-Operative-Form.md:389`. **That line number is
  itself stale** — line 389 at HEAD-before-my-change was blank; the figure was at `:368–369`.
* **M3.** `docs/OneThird-LIBweak-mg-c3ca.md` carried **2** sites (`:88`, `:90`). Repaired in the same
  commit. `mg-c4f5` independently found these; its branch `polecat-uc4f5` is **NOT merged** and is
  not an ancestor of `main`, so at `main` they were live.
* **M4.** `docs/state-history/attempt-mg-88bd.md:98` carries the **standing instruction** in bold:
  *"do not carry `2×10⁻⁴` or the `n ≈ 10⁵` crossover as flat text"*, together with both the
  superseded and the repaired value. It is the **authority**, not a defect. Any detector that flags
  it is wrong.
* **M5.** `docs/OneThird-lambda-std-Operative-Form-IndependentAudit.md` is the document that
  *performed* the correction; its ~11 occurrences are the refutation itself and are not defects.
* **M6.** `mg-2860`'s own commit message (`f85a4e8`) says **"FOUR SITES, FIVE LINES, NOTHING ELSE"**
  and names them: `STATE.md:13, :21, :57, :62, :86` — every one in **one file**. It also says
  *"adding (LIB-weak) there would be a fifth site and is outside what this ticket lists."*
* **M7.** `git grep` for `2×10⁻⁴` at `f85a4e8~1` (mg-2860's base commit, `f758468`) returns **5
  files**, of which **4 are outside `STATE.md`**.
* **M8.** The token `SPREAD` occurs in exactly four tracked places: `STATE.md:72`, `STATE.md:82`,
  `docs/state-history/attempt-mg-a58f.md:70`, and `docs/state-of-the-wall.html` (two lines).

---

## The hypothesis this instrument tests

**H.** `mg-2860` did not search. It executed a **fixed list supplied by its own ticket**, scoped to a
**single file**, for a **different defect class** (which *form* leads — limit vs constant) than the
one that bit; the numeric figure was a rider it landed correctly *into* `STATE.md` while never
looking outside it. **If H holds, the list is the defect and the sweep will miss the sixth site too.**

---

## Predictions

Scored **HIT** / **MISS**. Misses are kept as written.

| # | prediction |
|---|---|
| **P1** | At `mg-2860`'s base commit `f758468`, the detector finds **≥ 8** flat-text sites *outside* `STATE.md`. Point estimate **14**, range 8–22. |
| **P2** | At that same commit the detector finds **0** flat-text sites *inside* `STATE.md` — i.e. `mg-2860`'s ticket was right about its own file, and the whole of the miss is the file boundary, not a bad list within the file. |
| **P3** | The **positive control fires**: a planted stale figure in a throwaway tree is reported, exit non-zero. |
| **P4** | The **mutation test kills both constant detectors** — an always-CLEAN detector and an always-DEFECT detector each fail at least one control construction. |
| **P5** | At HEAD (after `c413c9e`) the detector reports **0** flat-text sites in `docs/` and in `STATE.md`. |
| **P6** | The detector reports a **non-empty** set of occurrences it classifies as NOT defects (authority / quoted-refutation / frozen transcript). Point estimate **> 15** such occurrences. If this set were empty the classifier would be doing nothing and the census would be a `grep`. |
| **P7** | At least one occurrence lands in a **committed transcript under `code/`** (frozen evidence at an old commit, which must never be repaired). Named candidate from M7: `code/state_audit_6a2f/out_audit.txt`. |
| **P8** | **The proximity rule will misfire at least once** on this corpus and I will have to adjudicate by hand. I predict the failure is a **false NEGATIVE** — a flat-text site that happens to sit near an unrelated repair marker — rather than a false positive. |
| **P9** | `docs/state-of-the-wall.html` contains **0** occurrences of the superseded `ε_spec` constants, so the rendered snapshot carries the stale *SPREAD sentence* but no stale *figure*. |
| **P10** | Running the detector against the **`SPREAD` critical-path claim** (defect 2's class — a superseded *claim*, not a superseded *number*) will **fail**: the registry mechanism is value-shaped and cannot express "this sentence asserts something a later audited row denies". I expect to have to record this as a **declared limit**, not to fix it. |
| **P11** | The instrument will find **at least one occurrence I did not already know about from M1–M8** — i.e. my hand sweep was itself incomplete. This is the prediction I most expect to lose, and losing it is the good outcome. |
| **P12** | **This instrument's own files will match its own patterns** (the registry names the superseded value in order to search for it), so the detector will flag itself unless it excludes its own directory — and I predict I will get that wrong on the first form and have to repair it, because that is the shape that has bitten this arc repeatedly. |

---

## What this instrument is NOT

* It is **not** a proof that the corpus is clean. It reports what its registry knows about. A
  superseded input nobody has entered is invisible to it, and the registry is the new single point of
  failure — moved from "whoever happens to read the right document" to "whoever remembers to file the
  registry row", which is strictly better but is not nothing.
* It does **not** re-derive any mathematics. Repaired values are `mg-e35c`'s.
* It does **not** repair anything. It reports, and exits non-zero when it finds a defect.
