# mg-a518 — the audit-successor detector is armed WIDE, and here is the evidence it can still fire

**Executes pm-onethird's decision on mg-a882 (2026-08-12), in the order that decision made
load-bearing: retro-link, then verdict-tag, then widen, then re-measure.**

## The table, which is the whole deliverable

Measured against the live `~/.macguffin` store with the installed binary
`/Users/daniel/go/bin/pogo` (built 2026-08-12 03:00; daemon revision `103693c7`), varying only
the `[audit_successor]` section of `~/.config/pogo/config.toml` — the same protocol mg-a882
and mg-7ff8 used, so the rows are comparable to theirs and not merely similar.

| `audit_tags` | examined | answered | reported | false reports |
|---|---|---|---|---|
| `["independent-audit"]` (as armed by mg-7ff8) | 4 | 4 | 0 | — |
| `["audit"]` **before** FIX 1 and FIX 2 | 9 | 6 | 3 | **2 of 3** |
| `["audit"]` **after** FIX 1 and FIX 2 — **as armed now** | **9** | **9** | **0** | **0** |

`answered = 9` is `8 answered by a successor + 1 by a recorded clean verdict`. The detector
counts those separately on purpose — a clean verdict is the weaker artifact and folding it in
would hide how much of a green report rests on it — so the split is carried here too.

**VERDICT: widened-and-clean.** The first two rows reproduce mg-a882's own measurement
exactly, including which three items it named. The third is new.

## What was changed, in the order it was changed

**FIX 1 — three repair tickets retro-linked to the AUDIT they came from.** This program's
convention is that a repair is tagged after the item that was *audited*, not after the audit.
That convention is **kept**; the audit reference is **additive**, which is what the decision
asked for.

| ticket | already carried | added |
|---|---|---|
| `mg-2f44` | `mg-3329-followup` | `mg-07fd-followup` |
| `mg-8d63` | `mg-789d-followup` | `mg-5cba-followup` |
| `mg-b417` | `mg-789d-followup` | `mg-5cba-followup` |

Each also gained a dated note in its body saying what the second tag is for, because a tag
with no explanation is archaeology for the next reader.

**NO FOURTH CASE EXISTS, and this was checked rather than assumed.** The ticket said to add a
fourth if one turned up and to say so rather than widen silently. Every `done` item in the
store carrying `audit` or `independent-audit` was enumerated, in every repository, together
with its successors and its recorded verdict. The three audits the detector reported are the
only three with no successor, and FIX 1 and FIX 2 between them cover exactly those three.

**FIX 2 — one verdict tag, and it is the only one the store needs.** `mg-a0d6` audited the
mg-d19f landing and UPHELD it; its result sidecar records `verdict: pass`, it has no repair
ticket and correctly never will. It now carries `audit-verdict-pass`.

**HOW MANY OTHERS: ZERO, and the search was not restricted to this program.** Ten `done`
items across the whole store carry an audit marker. Three record a passing verdict —
`mg-a0d6` (`pass`), `mg-5e82` (`pass`) and `mg-7a20` (`pass`, in the pogo repository) — and
of those, only `mg-a0d6` has no successor. `mg-5e82` is answered by `mg-77f4` and `mg-7a20`
by `mg-57c0`, so tagging either would silence nothing and assert something nobody measured.
**One item needed the tag; one item got it.**

**FIX 3 — `audit_tags = ["audit"]`.** What licenses `audit` as the marker is that it is not a
loose one here: all nine `done` items carrying it are titled `INDEPENDENT AUDIT of ...`,
re-verified from the store for this ticket rather than quoted from mg-a882. `independent-audit`
is the tag people *forget* — five of the nine lack it — so arming on it made the detector's
coverage depend on the habit that had already failed.

## THE COLLISION NOBODY WAS TOLD ABOUT — two names for one concept, and both are recognised

mg-a882 says to introduce `audit-verdict-pass`. **A clean-verdict tag already existed:**
mg-7ff8 armed `clean_verdict_tags = ["audit-clean"]`, named it in the `doctor` remedy text,
and published it in pogo's `docs/CONFIGURATION.md`. The decision appears not to have known
that, and nothing in the ticket names it.

`clean_verdict_tags` is now `["audit-clean", "audit-verdict-pass"]`. **Both, not one, and the
direction is the fail-safe one:** this detector's failure mode is silence, so dropping a name
means an audit tagged with the dropped one is silently unreported, while carrying both costs
only a wordier remedy line (`doctor` prints every configured tag joined with `or`). Zero items
carried `audit-clean`, so nothing is orphaned either way.

**This is a defect and it is left standing rather than resolved here.** Consolidating onto one
name is pm-onethird's call, not a polecat's, and it is flagged to them. Do not resolve it by
deleting a name from that list while any item carries it.

## Why a green report from a detector is worth nothing on its own

The defect mg-a882 recorded is *a detector that reported GREEN while blind to 56% of its
population*. The remedy is **an artifact of the same kind**: a detector that reports green. So
the only interesting question about the remedy is the question that was interesting about the
defect — **is it green because it looked, or green because it cannot see?**

`controls_a518.py` answers it by mutation. Every arm removes something this ticket added and
requires the report to move.

| arm | mutation | required | observed |
|---|---|---|---|
| C0 | none | green | green |
| C1 | `mg-2f44` loses `mg-07fd-followup` | names `mg-07fd` | names `mg-07fd` |
| C2 | **both** of `mg-5cba`'s repairs lose theirs | names `mg-5cba` | names `mg-5cba` |
| C2b | **one** of them loses it | **green** — either alone answers | green |
| C3 | `mg-a0d6` loses `audit-verdict-pass` | names `mg-a0d6` | names `mg-a0d6` |
| C4 | **every** fix reverted | names all three | names all three |
| C5 | restored | identical to C0 | identical to C0 |

**C4 is the load-bearing arm.** With the four tags removed the detector names exactly
`mg-07fd`, `mg-5cba`, `mg-a0d6` — the same three, by name, that mg-a882 measured as false
reports before any of this landed. So C0's green is the fixes doing work, and not the detector
having gone blind a second time in a new place.

**C2b is the arm that stops C2 proving the wrong thing.** Without it, C2 is equally satisfied
by a detector that requires *every* successor rather than *any*, and that detector would report
falsely the moment an audit has two repairs and one of them is retired.

**Population counts are printed and deliberately NOT asserted.** The store grows. A control
pinned to `9 examined` goes red on the next audit that lands, for a reason its reader cannot
act on — which is the failure mg-a882's closing paragraph names, arriving inside the remedy
for it. What is asserted is WHICH ITEMS are named, which is drift-proof.

## Five defects of my own, all kept

**D1 — THE CONTROL SHIPPED UNABLE TO FIRE, AND THAT IS THE DEFECT THIS TICKET IS ABOUT.** The
first run of the mutation arms copied the store with `cp -R`. The detector ages an audit's
silence from its `<id>.result.json` **mtime**, and a plain copy stamps every file with the time
of the copy — so on the copied store every unanswered audit was *zero seconds silent*, landed
in `waiting` instead of `silent`, and **all four mutation arms came back `pass`**. That reads
exactly like *the fixes are load-bearing and the store is healthy*. A control that cannot fire,
reporting green, inside the remedy for a detector that could not fire and reported green — one
level down and within the hour. It was caught because the counts moved into a column
(`waiting`) that had no business moving, not because anything checked. The copy now asserts
mtime preservation and **refuses** rather than passing; `x1_positive_control.py` P1 plants the
exact mistake and shows the guard bites.

**D2 — my first mutation was a string replace, and the detector matches successors by
substring.** Removing `mg-5cba-followup` with a naive replace would corrupt a neighbouring tag
that contains it, changing the detector's answer without changing the arm. Rewritten to parse
and rebuild the tag list; P4 plants the case.

**D3 — the arm-A check on the live config is weak on purpose and should be read that way.** It
asserts only that more than four audits were examined. It cannot tell `audit` from any other
tag that happens to match nine items, and it would not notice `repos` being widened. It
detects *"someone narrowed this back"*, which is the regression that actually threatens this
work, and nothing finer.

**D4 — I did not observe the detector in the context it will RUN in.** mg-7ff8's acceptance
condition 2 asks for the unattended run's artifact rather than a hand-run, on the correct
grounds that they are different claims. Every measurement here is a hand-run from an
interactive shell. The first unattended `pogo doctor --check` after this lands is the one that
confirms the arming in the context that matters, and it has not happened yet.

**D5 — this suite is not on the merge gate, so nothing runs it unless a person does.** That is
argued for in `run_all.sh` and it is still a cost: the committed transcript is a statement
about 2026-08-12, and the widening could regress the day after with nothing to notice. A
transcript is weaker than a gate and it is what this measurement, whose every input lives
outside this repository, can honestly be.

## What none of this establishes

**Nothing here checks that any audit was READ.** Both artifacts the detector counts — a
successor ticket and a clean-verdict tag — are cheap to produce, and this ticket produced four
of them. Tagging an unread audit `audit-verdict-pass` silences the line exactly as filing an
unread audit satisfies the pairing gate. That is limit 1 of the detector, it is not repaired by
anything here, and the false-report count reaching zero must not be read as saying otherwise.
`mg-a0d6`'s tag was applied against its recorded verdict sidecar and its merged audit document
at `744cfd5`, not against its ticket body alone — which is a stronger basis than the tag
requires, and still not a reading.

**The detector still detects after the fact rather than preventing**, and it still refuses
nothing.

## Files

```
controls_a518.py        the mutation arms — C0..C5
x1_positive_control.py  five planted worlds against the controls themselves
run_all.sh              the runner, NOT wired into ./build.sh (reason inside)
out_controls.txt        transcript, 2026-08-12
out_x1_positive.txt     transcript, 2026-08-12
```

Nothing in this directory is imported by any other suite, and `./build.sh` is unchanged.

---

## 2026-08-12, LATER THE SAME DAY — SUPERSEDED IN EXACTLY ONE RESPECT BY mg-9134

**Nothing above is retracted. One name changed, and this note exists so a reader of the
COLLISION section does not act on a config that no longer exists.**

pm-onethird decided the collision this ticket declined to resolve: **`audit-clean` survives and
`audit-verdict-pass` is retired.** `clean_verdict_tags` is now `["audit-clean"]`, `mg-a0d6`
carries `audit-clean` and not `audit-verdict-pass`, and no item in any repo carries the retired
name (2780 item files scanned, every status including `archive/` and `shelved/`).

The one edit to this directory is `controls_a518.py`'s `FIX2`, whose tag text moved
`audit-verdict-pass` → `audit-clean`. **The arm's subject is unchanged** — a passing audit with
no successor must become visible when its clean-verdict tag goes away — and left alone it would
have gone red for the right reason and the wrong world: `strip_tag` would have found no such tag
and reported "the fix this arm mutates is NOT IN THE STORE". Re-run after the edit: **all seven
arms behave, C0 9/8/1/silent-0, C4 names the same three.**

This README's table, its C3 row and its COLLISION section are left as written. They are the
record of what was true when this landed, and the collision *was* real — mg-9134's arm N2 shows
the two names are not interchangeable to the detector, so configuring both was the right call to
make while a decider was still deciding.

`code/audit_successor_consolidation_9134/` carries the consolidation's own controls, including
the two halves of the rename hazard run as experiments and a deliberate reproduction of this
directory's D1 (the `cp -R` copy that could not fire).
