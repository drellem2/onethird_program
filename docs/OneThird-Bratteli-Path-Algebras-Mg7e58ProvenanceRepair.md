# The provenance apparatus, made right about itself — `mg-7e58`

**Repairs `mg-321d`'s `G-1` and `G-2` against `mg-58da` (`673b4c0`), audited at
`ef38841`.**

`mg-58da` restored the set-level corroboration, and `mg-321d` confirmed it: ten
of ten pairs of sources agreeing at twenty-four of twenty-four cells, all five
of `mg-a218`'s members re-run rather than only the one that changed. That is not
in question here and it is re-derived below rather than repeated on trust.

What `mg-321d` found is that the apparatus which established that provenance was
**wrong about its own**. Two sites, one root:

| | the defect | the grain error |
|---|---|---|
| **G-1** | `g1_provenance.py` asked *"did the measuring half change?"* and answered with a **file sha**. `mg-58da`'s own commit moved `c1_branching.py` and did not move the measurement, so `g1` **exited 1 on a finding its own section (iv) refutes** | a question about a **measurement**, asked of a **file** |
| **G-2** | `g4_fleet.py` attributed with `sha@HEAD != sha@worktree`, so once `673b4c0` landed it reported that `ed9cde4` had touched `c1_branching.py`. **`ed9cde4` never touched it** | a question about a **commit**, asked of *"is it committed yet"* |

Both are now repaired at the grain of the property, and neither is repaired by
turning something off.

---

## 0. The bottom line

* **`g1` exits 0, and its replacement check is shown going red.** The file-sha
  predicate is gone; the question is settled by running **both script revisions
  against the same target** — both target forms — and diffing `c1`'s own
  sections (i)+(ii) and its twenty-four vertex cells. Byte-identical at
  `a8db5dbd4c758765`, **125 lines**, on both forms. Then `g1` itself, unmodified
  and in place, is run in four clones: **4 of 4** directions predicted, and the
  one carrying a real regression in the measuring half makes it **exit 1**.
* **`g4`'s attribution is derived from `git log`, and checked against its own
  rows.** `ed9cde4` touched **1** of the five (`c2_vertexsets.py`); `673b4c0`
  touched **1** (`c1_branching.py`). Both figures come out of the same call that
  produces the row beside them, and a summary-vs-rows gate fires if they part.
  This is also what `mg-58da`'s own `PREDICTIONS.md` predicted — *"touched by
  `ed9cde4` → 1 (c2)"*, *"touched by THIS ticket → 1 (c1)"* — before its
  instrument drifted away from it.
* **The set-level property is intact and re-derived, not quoted.** **10 of 10**
  pairs of sources agree at **24 of 24** cells, over **240** cell comparisons;
  **5 of 5** members re-run in place; `c0_repro.sh` **5 of 5 IDENTICAL**; and
  **5 of 5** locality probes move their own cell and no other, so the agreement
  is a measurement rather than a blind reader's silence.
* **`mg-321d`'s own finder agrees.** `h2_grain.py`, mg-321d's committed
  instrument, unmodified, re-run against the repaired tree: **0 findings**,
  where its committed record has **3**.
* **And the fix was asked whether it carries the defect it removes.** Nine
  branches, each measured or given a stated reason it cannot bite — §4. Two of
  them found real defects in this repair's first draft, and both were fixed.

Still open and untouched: `c3_withdrawal.py` is red (`mg-d330`'s second
finding), and `mg-d330`'s `e4` gate on `mg-a218`'s exit-code sentence is a
presence test. Both are `mg-58da`'s bookings and neither is worked around here.

---

## 1. `G-1` — the disposition, said out loud

`mg-321d` required this to be answered rather than dodged: *either the finding
is real and the section is wrong, or the section is right and `g1` should not
fire.*

**The section is right and `g1` should not fire.** The evidence is not `g1`'s
own; it is re-taken in `k1 (ii)` on this instrument's reader, running **both
script revisions against the same target**:

```
target form                     c1 @ 286d5030    c1 @ ef388417    cells
  the 286d5030 target (COUNT)   a8db5dbd4c7587   a8db5dbd4c7587   24/24  IDENTICAL
  the HEAD target (SET)         a8db5dbd4c7587   a8db5dbd4c7587   24/24  IDENTICAL

the file grain, for contrast:
  c1_branching.py    CHANGED
  kern_a218.py       SAME
```

The file moved; the measurement did not. `kern_a218.py` — the file `g1` itself
labelled *"the measuring half"* — never moved at all.

**And it is not resolved by silencing `g1`.** That was the explicit
instruction, and it is the reason `g1` grew a section rather than losing one.
The old predicate is replaced by a stronger one, and the stronger one is shown
firing on a defect it must catch. `k1 (iii)` runs **`g1` unmodified, in place**,
inside four clones — the mutation is always made to `c1_branching.py`, the thing
`g1` measures, and never to `g1`:

| clone | predicted | `g1` |
|---|---|---|
| unmodified (null probe) | exit 0 | exit 0 |
| `c1`'s vertex **dimensions off by one** | exit 1 | **exit 1, naming the measurement** |
| a comment appended to `c1` | exit 0 | exit 0 |
| an edit inside `c1`'s **comparing** half | exit 0 | exit 0 |

**4 of 4** directions predicted correctly. Rows two and four are the whole
point: the same file sha moves in both, and only one of them is a defect.

`g1` also carries the probe internally, so the check travels with the gate
rather than living only in this directory.

### `G-3` closes with it

`mg-321d`'s `G-3` — *the documented reproduce command does not reproduce* — was
`G-1`'s consequence: `out_g1_provenance.txt` said `FINDINGS 0` and
`PREDICTIONS.md` said `ACTUAL 0 HIT`, both recorded before `673b4c0` existed.
`./run_all.sh` in `code/branching_audit_58da/` **reproduces its committed
outputs up to the revision it names**, and §4's `B1` checks that it still does
**once this repair is itself a commit**.

> **NARROWED BY `mg-76cc`, on `mg-957f`'s `F-2`.** This sentence read
> *"…now reproduces its committed outputs"*, without qualification, and it was
> shut on evidence in which **1 of 5** of those outputs reproduced byte for
> byte. The other four differ, in **9** lines, and every one of the nine is the
> same thing: a revision printed into a file that is then committed. That
> cannot be fixed — a transcript that prints `HEAD` is written **before** the
> commit that commits it, so the byte-identity fixed point does not exist.
> `code/branching_repair_76cc/r2_reproduce.py` demonstrates it at two distinct
> revisions and closes the claim at **5 of 5** under a **named** normalisation
> of that one revision, with **0** differing lines left unexplained and two
> controls showing the normalisation still catches a real difference. What is
> *not* reproduced, and is stated there rather than buried, is the revision
> token itself.

---

## 2. `G-2` — attribution derived from the history

The expression that was wrong:

```python
if sha@286d5030 != sha@HEAD:      touched by mg-13b2
if sha@HEAD     != sha@worktree:  touched by mg-58da
```

True for exactly as long as the change is uncommitted. What replaced it inverts
`git log <range> -- <path>` — the same call that produces the row printed beside
it — into a commit → members map, and labels each commit with the `mg-id` its
**own subject** carries:

```
   ATTRIBUTION, INVERTED FROM THE SAME git log CALLS
     673b4c00  mg-58da   touches: c1_branching.py
     ed9cde49  mg-13b2   touches: c2_vertexsets.py
     (none)    uncommitted  touches: none
```

Nothing there is written down. `k1 (iv)` re-derives the same map by **two**
routes that share no code with `g4` — `git log -- <path>` per member, and
`git show --name-only` per commit — requires them to agree with each other
before either is used, and then compares both against what `g4` prints. They
agree at all five members.

**And the summary is now checked against the rows.** `g4` gates its own
attribution once per member plus the union: if the per-commit map and the sha
rows ever part, that is a finding. `mg-8aae` found the same shape one
instrument over — a summary sitting beside rows that refute it — and the gate is
what stops it here.

The deletion test for `g4` is not a mutated file but **a commit landing**, which
is how `G-2` was born in the first place: `k2`'s `B6` clones the repo, commits a
real change to `c3_withdrawal.py`, and requires `g4`'s attribution to pick it up
with no other edit. It does.

---

## 3. What was not to be lost — re-derived, not quoted

`mg-321d` was explicit that the set-level corroboration is what this arc bought
and that weakening it is a defect in its own right. `k3` re-derives it from the
files, on readers written for this directory:

| | |
|---|---|
| pairs of sources agreeing at all 24 cells | **10 of 10** |
| cells compared, over those pairs | **240** |
| `mg-a218`'s members re-run in place | **5 of 5** |
| members green | **4 of 5** — `c3_withdrawal.py` red, `mg-d330`'s second finding, OPEN |
| `c0_repro.sh` committed outputs identical | **5 of 5** |
| readers moving at their own cell and no other | **5 of 5** |

This repair touched **none** of the five, which is precisely why the check has
to be a re-derivation: *"the member I changed still works"* would say nothing
here, because no member changed. The five sources are the target
(`out_t1_tl.txt`), `c1` live, `c2` live, `mg-2060`'s `b1`, and `mg-d330`'s `e1`.

**The readers are probed because a blind reader agrees with everything.** Each
source is corrupted at the `beta=1, n=6` cell — the only `n=6` cell no other
parameter shares — scoped to one line, and its reader must move at that cell and
nowhere else. The first version of this probe aimed at `beta=3, n=6` and could
not be aimed at all: `beta=2` carries an identical row. That is recorded, not
tidied away.

---

## 4. Could this fix carry the defect it removes?

The remedy is an artifact of the same kind as the defect, so it is subject to
it. The list is `k2`'s, and each branch is measured or given a **stated reason**
it cannot bite — a reason is checkable and an omission is not.

| | branch | verdict |
|---|---|---|
| **B1** | this repair's evidence is recorded **before the commit that commits it** — `G-3`'s exact shape | **checked, not argued.** The worktree is cloned, the repair is **committed there**, and `g1` and `g4` are re-run: self/findings/exit identical on both, and the finding **texts** compared too |
| **B2** | `g1`'s new check compares c1's **printed** measurement; what is it invariant under? | a measurement change that prints nothing. **It cannot bite, and here is why:** every `mine_` name c1's comparing half inherits (`mine_vertices`, `mine_edges`) is one the measuring half prints in full, so printed ⊇ compared, and such a change moves none of the 198 cells either. Read off c1's source and checked |
| **B3** | `g1` runs on "both target forms" — is the second one check reported twice? | the texts differ **and** drive different paths: `c1` reports `Form read: COUNT` on one and `SET` on the other |
| **B4** | `g4`'s attribution derives from a **range**, whose left endpoint is written by hand | the endpoints are **resolved**, and every commit touching each member across **all** history is listed so what the range excludes is visible rather than merely absent. The in-range answer is then cross-checked by the summary-vs-rows gate |
| **B5** | the ticket → commit step reads a commit **subject**, which is prose | the load-bearing map (member → commit) never passes through a subject. Checked: each in-range commit carries exactly one id, no two share one, and the commit whose subject says `(mg-13b2)` is the sha `lib58da` names |
| **B6** | the new checks could fire on a purpose-built hook | `g1`'s probes mutate **`c1`**, never `g1`. `g4`'s probe is **a real commit landing** — the path `G-2` itself took |
| **B7** | the repair could weaken the set-level property | §3: 10 of 10 at 24 of 24, 5 of 5 re-run, checked in `k3` and not restated in `k2` |
| **B8** | this document could assert figures no instrument reads | `k4` gates every figure below at its own site against a committed `out_k*.txt`, each deletion-tested |
| **B9** | regenerating committed outputs could erase the record being answered | `mg-a218`'s `out_c1_branching.txt` and all six of `mg-321d`'s `out_h*.txt` are compared against their blobs: **7 of 7 IDENTICAL** |

**Two branches bit on the first run, and both were real.**

* `B2`'s first version counted `mine_c`, `mine_v` and `mine_named` — names the
  comparing half **binds for itself** — as quantities inherited from the
  measurement, and booked a finding. The check was wrong, not `c1`.
* `B3`'s first version looked for `Form read:` in `g1`'s output. `g1` does not
  echo `c1`'s stdout, so it found nothing and declared the second check vacuous.

And one bit in `k1`, against this repair's own code: `g1`'s internal probe
builds a mutated `c1` from a source string, and in a clone where `c1` had
**already** been mutated the string was absent and `g1` raised `ValueError`
instead of reporting. It now books that as a **SELF-ERROR** and names the probe
as dropped — *"I could not build the probe"* is a fact about `g1`, never a
finding against anyone, and a shrinking population must stay visible.

---

## 5. The instrument

`code/branching_repair_7e58/` — four scripts plus a **65-assertion** self-test.
It is not one of `mg-a218`'s five, not one of `mg-58da`'s four, and not one of
`mg-321d`'s five, and it writes into none of their directories: every mutation
happens in a temp clone or a temp tree.

```
./run_all.sh          # pure Python 3, no dependencies, NO NETWORK
```

| file | what it decides |
|---|---|
| `lib7e58.py` | the readers and the clone helper. Five readers for the five sources, written from the file formats and sharing no line with `lib58da.py` or `lib321d.py`. `scratch_clone()` makes a real clone **with the working tree committed**, which is the only way to ask whether a repair survives being committed |
| `selftest_7e58.py` | the apparatus before it is believed: the readers on known, **absent** and **hostile** input, cell locality, `replace_once` refusing zero sites and two, and `scratch_clone` in all three of its modes |
| `k1_grain.py` | the two sites. The **before** state reproduced at `ef38841` rather than quoted; the measurement re-derived on both target forms; **4 of 4** deletion probes on `g1` itself; the attribution derived twice and compared against `g4` |
| `k2_selfprov.py` | §4 — the nine branches |
| `k3_setlevel.py` | §3 — the property that was not to be lost |
| `k4_doccheck.py` | every figure in this document, read **at its own site** and compared against a committed `out_k*.txt`, each gate deletion-tested with a null probe beside it |

`PREDICTIONS.md` holds every exit code and answer predicted **before** the run,
with the misses kept as written.

## 6. What changed outside this directory

* **`code/branching_audit_58da/g1_provenance.py`** — the file-sha finding is
  replaced by section (v)'s measurement check, with its own three-source probe.
  The note is in the source, per this repo's convention.
* **`code/branching_audit_58da/g4_fleet.py`** — section (ii)'s attribution is
  derived from `git log` and gated against its own rows; the column header and
  the verdict paragraph are computed from `HEAD` rather than written.
* **`code/branching_audit_58da/out_*.txt`** — regenerated, because `G-3` is
  precisely that they no longer reproduced.
* **`docs/…-Mg58daRepair-IndependentAudit.md`** — `mg-321d`'s audit is a record
  and its figures are left exactly as taken; a dated note marks which of its
  present-tense claims about the tree this repair has since made false.
