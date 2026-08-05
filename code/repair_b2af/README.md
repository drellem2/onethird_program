# mg-b2af — the repair of mg-330a's population and its two OPENs

`code/repair_b2af/` — 5 scripts, 53 self-test assertions, worst exit 1.

`PREDICTIONS.md` was committed **before any script of this instrument
existed** (`7bd0056`), 37 rows. **31 hit, 6 missed, and every miss is kept as
written** with what was wrong recorded beside it. Nothing in `PREDICTIONS.md`
was edited after a run.

Run it with `./run_all.sh`. Two scripts exit 1 **by design and by
prediction** — `t1` because three published figures reproduce at no commit,
`t3` because the sentence it scores is in a commit message and cannot be
edited.

---

## THE HEADLINE: mg-330a's CENSUS IS NOT WRONG, IT IS DISPLACED — AND THE DOCUMENT'S IS NEITHER

The brief for this ticket quotes mg-330a's answer as *16 history-derived
across 13 directories, of 36 sites*. mg-330a's own committed transcript says
**37 sites, 16 history-derived, 12 directories**. Four of the ten figures the
document and its own transcript state disagree, **and both landed in the same
commit, `fba5f63`**.

So the first thing `t1` does is ask where each figure reproduces. The sweep is
re-run at four commits: mg-330a's two as they now sit on `main`, and their
**pre-rebase twins**, found in the object store by matching the subject line
and checked to be unreachable from `main`.

| figure | doc | transcript | `ea97d0a`/`fba5f63` (on main) | `b94cb1e`/`0ef9af9` (pre-rebase) |
|---|---|---|---|---|
| ALL call sites | **36** | 37 | 40 | **37** |
| `NEWEST` | 7 | 7 | 8 | **7** |
| `INDEXED` | 8 | 8 | 10 | **8** |
| `UNRESTRICTED` | 1 | 1 | 1 | **1** |
| `OLDEST` | **10** | 11 | 11 | **11** |
| `PICKAXE` | 6 | 6 | 6 | **6** |
| `RANGE` | 4 | 4 | 4 | **4** |
| history-derived | 16 | 16 | 19 | **16** |
| directories | **13** | 12 | 13 | **12** |
| helper call sites | **16** | 12 | 12 | **12** |

**The transcript's ten figures reproduce EXACTLY at `b94cb1e`, and at neither
commit it now sits behind on `main`.** The refinery rebased mg-330a's branch,
and the tree the sweep ran against is not the tree inside the commit that
carries its output. mg-132a's word for that is **DISPLACED**, and it is the
right word here: nothing mg-330a measured was wrong.

What moved between the two trees is nameable: mg-132a's own
`code/publication_anchor_132a/anchor_132a.py` landed — **three**
history-derived sites in one file — and `repair_7e39.py` lost the one it had
when mg-132a's repair moved it out. Four sites in, one out; 16 → 19.

**The document's four bolded figures are a different matter.** Three of them
reproduce at *no* commit measured — not on `main`, not pre-rebase, not at the
worktree:

- **`OLDEST 10`** — the sweep says 11 at every tree. The document's table then
  sums its own rows to its own total, `7+8+1+10+6+4 = 36`, so **the `36` is
  arithmetic over a row that is off by one, not a measurement.**
- **`16 call sites of the two named helpers`** — the sweep found **4 `DEF` and
  12 `CALL`**, 16 rows in all. **16 is the ROW count reported under the
  CALL-SITE label.** One number over two populations — which is F-2's own
  defect, committed inside the census that names F-2.
- **`16 history-derived across 13 directories`** — 16 is the pre-rebase figure
  (12 directories there); 13 is the post-rebase figure (19 sites there). **No
  tree gives 16 and 13 together.** The two halves of one sentence are right
  about two different trees, which is why neither reading catches it.

---

## OPEN 1 (F-1) — THE GATE IS NOW WHERE THE ANCHOR IS SPENT

`ANCHOR_DRIFT` was gated in `k1_prerepair.py` and `selftest_e34a.py` — the two
scripts that **check** the anchor — and in neither of the two that **spend**
it. `k4_cancel.py` reads `REPAIR_REV`; `k2_five.py` reads `PRE_7E58_REV`.

`libe34a.py` now offers **`gate_spent(report, *names)`**, and both consumers
take it. Three properties, each measured rather than asserted:

- **It is named, not passed by value.** `gate_spent(R, REPAIR_REV)` could not
  work — the value is a sha, two anchors can resolve to the same sha, and a
  sha carries no record of which derivation produced it.
- **An unknown name is a SELF-ERROR, not a pass.** A typo'd anchor name would
  otherwise gate on an empty list and report green.
- **It is silent when green.** Both scripts print exactly what their committed
  transcripts printed before this repair existed.

**The rule is structural.** `t2` walks the parse tree of every `.py` in
`code/branching_audit_e34a/` and requires that a script naming a derived
anchor either reference the whole of `ANCHOR_DRIFT` or call `gate_spent` for
**every** anchor it names — a subset test, not a call count, so a script that
gates one of two anchors is not covered. **It goes red at the commit before
this repair and green at the tree, and `t2` prints both readings.**

**And the difference was constructed.** In a clone, a pin is edited to name a
different *real* revision; the derivation is untouched, so only the
pin-versus-derivation comparison moves:

| script | anchor spent | clean tree | under constructed drift |
|---|---|---|---|
| `k4_cancel.py` | `REPAIR_REV` | exit 1, `TOTAL BAD: 2` | exit 1, **`TOTAL BAD: 3`** |
| `k2_five.py` | `PRE_7E58_REV` | exit 0, `TOTAL BAD: 0` | exit 1, **`TOTAL BAD: 1`** |

Before this repair both scripts printed the left column under **both**
conditions. That is what *silent where it is spent* meant, and it is now a
measurement.

`k1_prerepair.py`, `selftest_e34a.py` and `k3_undisturbed.py` are
**byte-identical** to their state before this repair.

---

## OPEN 2 (F-2) — `every one a record` IS TWO LABELS, AND THEY ARE NOW TWO

`r3 (iii)` derives a site's **KIND** from its **PATH**, and that is the rule
that decides whether a site gets edited. `r3 (iv)` labels the same residue by
**SCOPE** — whose ticket owns the file. `dfa263c`'s summary reports the scope
label as though it were the kind label.

Re-derived at this tree with mg-2c77's rule unchanged — and the rule is first
checked on two constructed inputs, so a widened ruler cannot close sites
silently — the residue is **20 sites, the same 20, none missed**:

> **20 sites remain unqualified in the tree. By SCOPE — `r3 (iv)` — every one
> is another ticket's. By KIND — `r3 (iii)`, the path rule that decides
> treatment — 5 are records (3 transcripts, 2 prediction files) and 15 are
> LIVE CLAIMS.**

That is the repair: **two rules, two functions (`kind_of` and `scope_of`), two
columns, two counts.** `t3` gates on the corrected sentence reporting both
labels and on its counts being the measured ones.

**The finding stands and is not closed.** The sentence is in the commit
message of `dfa263c`. A commit message is immutable without rewriting history,
and rewriting a merged commit to make this ticket's summary come out is a far
worse act than the defect it would hide. `t3` exits 1 for that reason and
`PREDICTIONS.md` said it would.

**None of the 20 is a defect.** They are other tickets' statements of what
those tickets found. The declining is right; the *sentence* was not.

---

## DO NOT DISTURB

`t4` re-derives rather than repeats:

- **All four anchors resolve to the pairs their prose names**, with the
  **subject printed beside each sha** — because *"`4755d029` agrees with
  `4755d029`"* is true of any derivation that has drifted onto its own pin.
  The pins are read out of `libe34a.py`'s **source**, and the derivation is
  this file's own `first_introducing`; an instrument that checks a derivation
  by calling it has checked nothing.
- **The sharpened lesson is a running check, not a sentence.** On the pair
  (`d01ff32d`, HEAD), a distinctness check on **commit shas passes** and a
  distinctness check on **the blob of `g1_provenance.py` fails** — `ca90929f`
  both sides. Both are run every time `t4` runs, and it prints that they
  disagree. *Where two anchors must differ, compare what they resolve to, not
  what they are called.*
- **The kernel-half triples are READ and labelled READ** — `3bc2cf76 → 0/0/0`,
  `HEAD → 1/1/3`, and the drifted pair both `1/1/3`, one predicate asked
  twice. Re-deriving them costs ten minutes of `k1_prerepair.py` and mg-330a
  already did it from scratch. **Saying `READ` is the point.**
- **The division survives, constructed:** a cosmetic edit to
  `g1_provenance.py` leaves `selftest_e34a.py` green (**REPORTS**); removing
  the property marker makes it red (**REFUSES**). An instrument that refused
  on every comment could not be run on a live tree.

---

## THE POPULATION, AND WHAT WAS ACTUALLY DONE TO IT

The brief: *convert the history-derived 16 to property-derived, or
pin-and-compare each, and report converted-count against 16.*

**Converted to property-derived: 0 of 19**, written as `0` rather than
replaced by a count of some other treatment. Every one of these sites lives in
another ticket's directory, and rewriting another ticket's instrument to make
this ticket's number come out is the failure this arc exists to avoid.

**Pinned and compared: 4 of 19**, in one file — `ANCHORS.tsv` — re-resolved by
`t1` on every run, so drift in any of the thirteen directories becomes loud in
**one place**.

Why only 4, and why that is the answer rather than an excuse:
`classify_call` reads the flags of one call. It cannot see that
`log -1 --format=%H e5787e1 -- <path>` **cannot move** while
`log -1 --format=%H -- <path>` moves on any edit, and it calls both `NEWEST`.
`t1` refines the 19 **without touching the denominator** — a repair that
shrinks a defect population by re-reading it is the mirror of the `OLDEST`
inflation mg-330a declined:

| | sites |
|---|---|
| population by mg-330a's classifier, **unchanged** | **19** |
| of which the revision is **PINNED**, so frozen | 1 |
| of which the path is a **PARAMETER** — a facility, not an anchor | 11 |
| of which a literal path and no pinned revision meet — a real, moving anchor | 5 |
| remainder (no pathspec, or a path this instrument could not resolve) | 2 |

**11 of the 19 have nothing at the site to pin**: the path arrives as an
argument, so the anchor is at the *call site*. **That is F-1's own lesson one
level down**, and it is named here rather than quietly counted as done.

**The refinement is demonstrated by construction.** A clone, a cosmetic commit
to each path, every spendable site re-resolved before and after: the site
called FROZEN returned the same revision, the three called MOVING returned
different ones, **0 contradicted their label**.

**`OLDEST` was not absorbed.** `t1` gates on the treated population containing
zero `OLDEST` rows. mg-330a named it apart deliberately — a file's creation
does not move when the file is edited — and letting the count grow by
swallowing a class that does not have the defect is A-2's mistake.

---

## THE SIX MISSES, KEPT AS WRITTEN

| row | predicted | measured | what was wrong |
|---|---|---|---|
| **P-2a** | the transcript reproduces exactly at `ea97d0a` | it reproduces at `b94cb1e` | The prediction named the commit the transcript **sits in**, not the commit it was **run at**. `P-2` explicitly reserved the word DISPLACED for this outcome and still guessed the wrong commit — I reasoned about the rebase and then wrote the row as though it had not happened. |
| **P-2b** | …and at `fba5f63` too | it reproduces at `0ef9af9` | Same error. The **reason** given for the row holds exactly: no revision-anchor call site was added between the two commits, and both pre-rebase trees measure identically. Right about the repo, wrong about which tree the commits carry. |
| **P-2d** | the doc's `13` is history-derived directories alone; the transcript's `12` is that set unioned with helper call sites | at every tree measured, **both readings give the same number** | The mechanism is refuted outright: the two readings never differ, so they cannot be what separates 12 from 13. The real answer is worse — `13` is the **post-rebase** directory count printed beside a **pre-rebase** site count. Same displacement, inside one sentence. |
| **P-3a** | 2–4 sites carry a constant revision argument | **1** | I generalised from `q4_prerepair.py`, the one I had already seen. A prediction about how common a construct is, made from a sample of one — which is the same error mg-330a's own P-1d records making. |
| **P-4b** | 6–10 sites pinnable | **4** | I expected module-level path constants to be common. They are not: 11 of the 19 take the path as a parameter. The row's own sentence — *"a parameterised helper has no revision to pin; what gets pinned there is its call sites"* — had the right idea and I still counted the helpers as pinnable. |
| **P-6c** | including this ticket's own files the residue is `20 + 2..8` | **20 + 0** | The row confused **two different words under test**: the residue is scored on the census term, and the word *this* ticket argues about is `record`. My files state the census term once, qualified. **A prediction about one word over two populations, itself running two words together.** |

---

## THREE DEFECTS OF THIS INSTRUMENT, FOUND BY IT AND KEPT

1. **`resolve_site` dropped the site's own pinned revision.** The one FROZEN
   site would have re-resolved as MOVING and `t1`'s construction would have
   reported a contradiction that was mine, not the site's. Found before the
   first full run, by reading what the function actually passed to `git`.
2. **`t3`'s two-label gate went red on `t3`'s own corrected sentence.** The
   sentence wrote `r3 iii` and the gate looked for `r3 (iii)`. **The gate was
   right and the sentence was wrong**, which is the only reason the gate is
   worth having.
3. **`t4`'s content-identity gate was inverted.** It fired on the *preserved*
   state and printed a message claiming two blobs differed **while printing
   the same sha twice** — visibly self-contradicting output that a gate
   nobody reads would have shipped. Found by reading the transcript.

---

## A FORECAST THIS TICKET MAKES ABOUT ITSELF

`t2` needs a tree where F-1 is still present. It does **not** pin one. It
derives it: *the commit that introduces `def gate_spent(` into
`libe34a.py`*, and takes that commit's first parent — a property-derived
anchor, in a ticket about anchors.

The committed transcript therefore names `1d2a8a19` and `7bd0056b`. **Those
two shas will not survive the merge.** The refinery rebases, and this branch's
commits will be rewritten exactly as mg-330a's were — which is the whole
finding at the top of this document, and it will happen to this deliverable
too.

**The derivation will still resolve; only the printed shas will move.** That
is the difference between a pin and a property, and it is why this ticket
declined to pin a sha it could see was about to be rewritten. A reader who
re-runs `t2` after the merge should expect two different shas in that row and
the same `BEFORE : 2 of 4 AFTER : 4 of 4` beneath it. **If the transcript's
shas and a fresh run's shas disagree, that is this forecast being confirmed,
not a defect.**

---

## WHAT IS STILL OPEN

- **The 11 parameterised sites are not gated.** There is nothing at the site
  to gate; the anchor is at the call site, and those call sites are in eleven
  other tickets' directories. Naming them is what this ticket does; treating
  them is not.
- **`code/repair_69d1/p3_reason.py` (i-b) still anchors its control on
  `HEAD`** — `UNRESTRICTED`, the loudest form of the defect. mg-330a pointed
  at it and did not repair it; neither does this ticket, and it is the one
  site in the 19 that no pin can help, because `HEAD` moves on every commit to
  the repository rather than to a file.
- **The document's three unreproducible figures are in a merged commit**
  (`fba5f63`) and in `docs/`. This ticket measures them and publishes the
  correction here; it does not rewrite another ticket's document.

---

## THE FILES

| file | what it is |
|---|---|
| `PREDICTIONS.md` | 37 rows, committed at `7bd0056` before any script existed |
| `lib_b2af.py` | the apparatus: the census (mg-330a's classifier, imported on purpose), the refinement (written here), the pre-rebase search, both F-2 label rules |
| `selftest_b2af.py` | 53 assertions on constructed inputs, including `gate_spent` itself |
| `t1_population.py` | the census at four commits, the refinement, `ANCHORS.tsv` |
| `t2_gate.py` | F-1: who gates, the structural rule, drift constructed |
| `t3_term.py` | F-2: both labels, the corrected sentence, the standing finding |
| `t4_preserve.py` | the four anchors, content identity, the triples, refuse/report |
| `ANCHORS.tsv` | the pin-and-compare file — 4 rows, re-resolved by `t1` |
| `out_*.txt` | the committed transcripts of the run that ships |
