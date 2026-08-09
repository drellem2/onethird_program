# `code/chain_audit_39bf/` — mg-39bf's instrument for the INDEPENDENT AUDIT of `mg-9461`

Four scripts, no dependency on `code/chain_selection_9461/`. That independence is
deliberate and is guard **E6**, filed in `PREDICTIONS.md` before the parent's deliverable
was opened: the ticket forbids treating agreement reached by `mg-9461`'s own route as
confirmation, so every number here is re-derived from the object it is defined by, and the
parent's figures are only ever the *comparand*.

```
PREDICTIONS.md        pre-registration, committed at 7764114 before
                      docs/OneThird-ChainSelection-mg-9461.md was opened
a1_source_counts.py   the byte-wise P1 guard, re-run with live positive controls
a2_chains.py          the four chains re-solved from their own Phi bounds
a3_timeline.py        mg-9461's run timeline, from artefacts only
a4_optimism.py        the 40 %, and the universal negative against a
                      pre-registered enumeration
out_*.txt             captured output of each
```

Run: `python3 aN_*.py`. Pure stdlib, exact rationals throughout, no float on any
decision path.

---

## What each one is for, and what it caught

### `a1` — the zero-counts, with the instrument proving it can find something

The ticket's warning is the whole design: *"a path typo, a subdirectory-relative glob, or an
iCloud-evicted file reading `EDEADLK` all yield zero"*, and a prior audit on this lineage
shipped a broken instrument that returned a number agreeing with the party under audit.

So `a1` refuses to report a zero it cannot defend. Three layers:

1. **The read is proved real before anything counts it** — `st_size` compared against bytes
   actually returned, md5 prefix, newline count. A short or empty read fails the run rather
   than producing comfortable zeros.
2. **Every zero carries a positive control from the same read, same regex, same
   invocation.** A token that matches nowhere in the file is a *blind* regex, and its zero
   in Steps 5–6 proves nothing; that row fails.
3. **A mutation test.** `Cheeger` and `C_3` are injected into a copy of the Step 5–6 window
   and the identical counters re-run. If the mutant still reads 0, the counters are
   tautological and every zero above is void.

Step windows are located by their own `\item` opener text, not by hard-coded line offsets,
so they cannot silently drift.

> **A DEFECT IN MY OWN CONTROL, CAUGHT BY THE GUARD I FILED IN ADVANCE.** The first version
> of layer 2 demanded the positive hit come from **Steps 1–4**. It **failed** on `Rayleigh`
> and `prefix capture` — both read 0 there. That was a defect in my control, not in the
> parent's claim, and the failure turned out to be a *strengthening*: those two tokens are
> absent from **all six steps** and present elsewhere in the document. The control was
> widened to the whole file (which is what actually establishes sensitivity) and the
> Steps 1–4 column kept as a secondary, non-gating reading — it is now what exhibits the
> strengthening.

`B2` asks a question the parent does not: is the `C_3` zero **selective or generic**? It is
generic. The source names **no** `C_<i>` at all, and `absolute constant` occurs 0 times
(independently reported by `mg-d3c7` at `6e5d88b`). The zero is true and it supports the
ruling, but by a weaker argument than *"the document names constants and omits this one"*.

### `a2` — the four chains, re-solved

Nothing is copied. Each `ε_dem` is derived from the inequality its chain is defined by:

| chain | its bound | derivation | `ε_dem` |
|---|---|---|---|
| (I)/(III) | `Φ_pref ≤ √(2C₃ε_spec)` | `√(2C₃ε_spec) ≤ ε_leak` | `ε_leak²/(2C₃)` |
| (II) gap | `1−ρ_pref ≤ C₃(1−λ_std)` | dictionary `Φ ≤ 1−ρ`, then `C₃ε_spec ≤ ε_leak` | `ε_leak/C₃` |
| (IV) literal | `ρ_pref ≥ c·λ_std` | `Φ_pref ≤ 1−ρ_pref ≤ (1−c)+c·ε_spec ≤ ε_leak` | `(ε_leak−(1−c))/c` |

`E2` fires live rather than being asserted: `Leak` and `Spec` are distinct types and a
`Spec` handed where a `Leak` belongs **raises**. `E7` is discharged by every printed figure
carrying its unit in the same line — the Cheeger square is the live trap on this lineage
and `mg-d3c7` named it.

Section **E** is what the ticket asked for directly and is where the one arithmetic finding
is: the two thresholds on `c` are **different numbers** and the parent's verdict box
conflates them.

### `a3` — the timeline, from artefacts only

`E3`, filed in advance: three sources state the correction's timing and they disagree, so
none of them is evidence. Every time comes from a file mtime, a mail `Date:` header, or a
git **author** date — committer dates are rewritten by the refinery's rebase and date the
merge, not the work.

> **MY SECOND DEFECT, CAUGHT BY THIS SCRIPT'S OWN ASSERTION.** The first version used the
> mail **file's** mtime as the read time. `mv` preserves mtime, so that timestamp survives
> the `new`→`cur` move unchanged and dates the **delivery**. It was wrong by 10.5 minutes,
> and it made me briefly score the parent's ordering claim FALSE. What records the move is
> the `cur/` **directory** ctime. Fixed, and the wrong reading is documented in the script
> so the next reader does not repeat it.

### `a4` — the 40 %, and the universal negative

`A` recomputes the required-scope ceiling in **closed form** at every `n` from `mg-d3c7`'s
proved family, which shows what `40 %` is a reading *of*. `B` scores the universal negative
against the four candidate experiments named in `PREDICTIONS.md` **before** the parent's
§4.4 was read, so the enumeration cannot have been fitted to the answer.

---

## What this instrument does NOT do

- It does not run any script in `code/chain_selection_9461/`. By design (E6).
- It does not re-run `mg-3969`'s 604 230-cut sweep or `mg-d3c7`'s `n = 7` exhaustive sweep,
  and it does not re-verify `mg-d3c7`'s family numerically — `a4` re-evaluates its **closed
  form** only, citing the family as landed.
- It does not re-measure `mg-76b2` §7's four columns, does not attempt L2, does not bound
  `C₃`, and does not re-derive `C₃ = 1` or re-attack `ε₀` — all four forbidden by the ticket.
- It enumerates no posets at all. There is no sweep in this directory; every claim is
  either a byte-count at source, a closed-form derivation, or a filesystem timestamp.
