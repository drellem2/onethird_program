# `code/species_remainder_f8fa` — the instrument for mg-f8fa

The remainder of the mg-a61f audit not carried by the mg-6f61 repair.
Supports `docs/OneThird-Species-Hopf-Monoids-Repair-Remainder.md`.

```
./run_all.sh        # ~15 s, pure Python 3, no dependencies, NO NETWORK
```

## What was left, and why it was left

mg-6f61 repaired the **document**. Its checker, `code/species_repair_6f61/
check_doc.py`, reads exactly one file —
`docs/OneThird-Species-Hopf-Monoids-Where-This-Lives.md` — and requires every
false sentence to survive only inside the strike that replaces it. That is the
right test, applied to half the artefact. **Three of mg-a61f's findings were
corrected in the prose and left standing in `code/species_7d75/`, which is the
copy a successor re-runs**, and no checker looked there.

| left standing | where | now |
|---|---|---|
| **X4** — *"four candidate identifications, three are controls"* | `t3_bidigare.py` T3d header and its vacuity branch, and the committed `out_t3_bidigare.txt` | restated, and the corrected count is **computed** by a new **T3e** that fails if it is wrong |
| **X5** — control (ii)'s counts read as measuring *"how differently"* the two products behave | `code/species_7d75/README.md`, under *Conventions that have bitten this repo before* | the **type mismatch** is stated and measured as a **set equality**; the conclusion is explicitly not withdrawn |
| **S4/S5** — the `S_n` half printed as an unqualified equality | `t4_one_operation.py` and `t6_fock_and_record.py`, inside runs ending `TOTAL BAD: 0` | scoped in place, naming the ledger row and both unread sources |

The other five items of the audit were already carried by mg-6f61 and are **not
redone here** — see the remainder document for the item-by-item check.

## What each file does

| file | what it decides |
|---|---|
| `kernf8fa.py` | posets as sets of strict pairs, ordered set compositions, the cone test, the Tits product, `μ_{S,T}`, the descent basis under both composition conventions. **Shares no code** with `kern7d75.py`, `hopf7d75.py`, `kern6f61.py` or `kerna61f.py`, and imports nothing from the instrument it checks |
| `w1_opposite.py` | **X4.** Convention B is identically the opposite algebra of convention A — 0 mismatches at every `n ≤ 5` — so T3d's four columns are two statements each computed twice. **With its control:** the un-swapped comparison must disagree, and fires 2 / 26 / 170 at `n = 3, 4, 5` |
| `w2_typemismatch.py` | **X5.** The Tits control's 1 442 product-closure failures **are** the 1 442 of 11 301 pairs with both ground sets non-empty — checked as a **set equality**, with every failure returning the empty composition. **With its controls:** a type-*correct* corruption fails the column 0 times, and the control's own guard, removed, takes the count to 11 300 |
| `w3_scope.py` | **S4/S5, and the gap itself.** `check_doc.py` for the instrument: no corrected statement may survive outside a marker quoting it as corrected, and **every** occurrence of the character-ring identification must carry its ledger row. Takes an optional directory argument so it can be pointed at the pre-repair tree |
| `selftestf8fa.py` | 2 114 assertions anchored to A000110 / A000670 / A001035 / A000142, plus a second construction of the cone test that shares no code with the first |

## The detector was seen to fail before it was seen to pass

`out_w3_scope_before.txt` is `w3_scope.py` — **the same file, unmodified** — run
against `code/species_7d75` as it stood at `83ac472`, the mg-6f61 repair commit:

```
python3 w3_scope.py /path/to/pre-repair/code/species_7d75
```

It reports **12 problems** there and **0** here. A checker written after the fix
and never observed to fail is not a checker, and this repo has filed that
finding against others.

**One false negative was found and fixed while doing it, and it is kept on the
record.** The first version of `w3_scope.py` accepted a bare *"REPAIRED"* or
*"CORRECTED"* near a forbidden string as evidence that the string was being
quoted rather than asserted. The pre-repair README disarmed it **by accident**:
an unrelated *"the error mg-1953 repaired"* sat four lines above the near-miss
bullet, so the bullet read as already corrected and X5 scored `ok` on a tree
where it was plainly false. The marker now has to name **this** repair or say
in so many words that the sentence no longer holds.

## Independence

`kernf8fa.py` builds every object from its definition. Where it recomputes
something `code/species_7d75` also builds, the two are compared rather than
shared: `|F[4]| = 4 399`, `|F[3]| = 121`, the 1 442 of 11 301, and T3e's
0 / 0 / 0 / 0 / 0 with control 2 / 26 / 170 all appear independently on both
sides and agree.

## What is NOT withdrawn by anything in this directory

* **Bidigare's theorem** still reproduces entry for entry. Only the control
  *count* was overstated.
* **The band product is invisible to the Hopf structure.** The correction makes
  this **stronger**: a type mismatch holds at every ground set, where the counts
  held on `[4]`.
* **The poset half of the headline** is confirmed — 87 of 87 with no size cap,
  179 of 179 out of sample — and §2.3 is a corollary with no `n` dependence.
  Nothing here softens any of that, and softening it would be a second wrong
  report.
