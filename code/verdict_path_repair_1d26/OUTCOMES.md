# mg-1d26 — OUTCOMES

`PREDICTIONS.md` was committed in `28c8029`, whose tree contains that file and
nothing else of this instrument. It is scored here against
`out_run_all_1d26.txt`, `out_p1_population.txt`, `out_p3_vacuous.txt`,
`out_selftest_1d26.txt` and `out_p2_FIRSTRUN_one_lost.txt`, and **it has not
been edited**. Three predictions missed. A refuted prediction is a result and
all three are kept as written.

**17 predictions, 14 held, 3 missed, 1 of the 17 never exercised.**
**4 disclosures, 4 true.**

---

## The disclosures — measurements already taken, never scored as hits

| | what was disclosed | what the run measured | |
|---|---|---|---|
| **D1** | 83, 85, 87 (255); e2 299; kernd633 252; total 806 | P1a re-derives 83/85/87 and 255; the two checker files are now 401 and 402 **because this repair edited them**, and P1c prints both grains | **true** |
| **D2** | the tree is ALREADY RED and both parents' clean-tree rows are false of it | `P2a`: the untouched sandbox exits **1** with **1** standing occurrence, in `code/face_geometry_repair_e35b/README.md` | **true** |
| **D3** | 264 markdown files, 18 with a strike, 37 strikes | `out_e2_crosssection.txt` at the publishing tree: **266**, and the count moves with every commit that adds a `*.md` — which is why it is anchored to a revision | **true, and already stale by construction** |
| **D4** | e2 imports only stdlib plus `kernd633`; `kernd633` only stdlib | `P1b`: closure beyond e2 is exactly `kernd633.py`; unresolved, none | **true** |

## The population

| | predicted | measured | |
|---|---|---|---|
| **P1a** | exactly five files, the same five mg-d53d names | 5 files, the same five, derived by the rule and not read from the list | **HELD** |
| **P1b** | the closure adds nothing beyond `kernd633.py`; nothing unresolved; the four siblings are off the path | exactly that; 4 of 4 siblings off the path | **HELD** |
| **P1c** | 255 rows over 3 files | 255 rows over 3 files | **HELD** |
| **P1d** | the last command of all three runners is the cross-section call | 3 of 3 | **HELD** |

## The before-state

| | predicted | measured | |
|---|---|---|---|
| **P2a** | exactly 6, and they are the six mg-d53d names | **6**, and they are the six, line for line | **HELD** |
| **P2b** | 4 of the 6 silent, and *which* four | **4**, and those four | **HELD** |
| **P2c** | `kernd633:127` is directional — it hides restatements that FOLLOW their strike — and E2b's five controls all restate BEFORE, which is why all five stay green | in the pre-repair sweep, deleting line 127 leaves the checker **exit 0, silent**, so none of controls (a)–(e) fired; with controls (f)/(g) present the same deletion exits **1 attributed to one of E2b's controls** (`P2e`) | **HELD** |
| **P2d** | `e2:52` deleted makes the population 0, prints no row and exits 0 | pre-repair: **exit 0**, 61 lines of output, nothing about a population (`P3e`); repaired: **exit 2**, `FOUND NOTHING TO CHECK`, which is the population being 0 said out loud | **HELD** |

## The repair

| | predicted | measured | |
|---|---|---|---|
| **P3a** | 0 deletions leave the checker exiting 0, over the WHOLE repaired population | **first run: 1 of 787** — `kernd633.py:172`, the `sys.exit` inside `deliver` itself (`out_p2_FIRSTRUN_one_lost.txt`). **Second run, after that defect was repaired: 0 of 803.** | **MISSED on the first run, HELD on the second** |
| **P3b** | 18 of 18 runner executions exit non-zero | **18 of 18** | **HELD** |
| **P3c** | the repaired checker cannot exit 0 over an empty population; the pre-repair one exits 0 on the same tree | pre-repair **0**, repaired **2** with its own sentence; and the three states have three distinct exit codes (0/2/9) and three distinct sentences | **HELD** |
| **P3d** | the population size is printed on every run, passes included | a green run of the repaired checker prints `E2 POPULATION EXAMINED: 265` and exits 0 | **HELD** |
| **P3e** | the repaired verdict path is **more than 806 and fewer than 950** lines | **1058** | ***MISSED*** |
| **P3f** | the repair adds no exclusion list | `P2c`'s population is 803 = 401 + 402, every line of both files | **HELD** |

## What I expected to get wrong

| | predicted | measured | |
|---|---|---|---|
| **P4a** | if P2a misses, it misses in the direction of MORE | P2a held at exactly 6, so this was **never exercised**. It is not a hit. | **not exercised** |
| **P4b** | `kernd633:196` and `:205` are structurally suspect — an `IndentationError` would make them *held* gates rather than lost ones | **both are GATE LOST and both are SILENT.** Neither raises. | ***MISSED, and it is the most useful miss in this file*** |
| **P4c** | the first post-repair sweep goes red on its first run — some line of the repair is itself a hole, and I expect to find it by running and not by reading | it did, at `kernd633.py:172`, and that is exactly how it was found | **HELD** |

---

## The three misses, in full

### P3e — off by 108 lines, and it is a miss about the size of a patch

I predicted the repaired verdict path would be under 950 lines. It is **1058**:
the two checker files went 299 → 401 and 252 → 402. Most of that is comment.
The prediction was an estimate of how much code four mechanisms and two controls
would take and it was wrong by about a third. Nothing else rests on it, and it is
kept because a prediction revised after the fact is not a prediction.

### P4b — Python's indentation is not a safety net, it is the mechanism

This is the miss worth reading. I predicted that deleting a `for` header or an
`else:` from an indented block would raise `IndentationError` and therefore leave
a **held** gate — red for the wrong reason, but red. mg-d53d's Q6 predicted the
same thing about the whole of `kernd633.py`, in the same direction, and missed it
the same way.

Both are **silent GATE LOSTs**, and neither raises, because in both cases the
line below is still legally indented **relative to a different block**:

* deleting `for dp, dns, fns in os.walk(root, onerror=onerror):` re-parents the
  entire loop body into the `def onerror(err):` defined immediately above it —
  the walk function then falls straight through to its `return` and hands back
  **three empty lists**;
* deleting `else:` re-parents `keep.append(d)` into the
  `elif os.path.islink(p):` above it, so the walk descends only into symlinked
  directories.

**A deleted line that changes which block the next line belongs to is the most
dangerous member of this population**, and nothing in this arc had named it. It
produces no traceback, no message and a smaller population, and every count
downstream is then honestly reported over the wrong set. It is why the repair
counts the population twice with two enumerations rather than checking the walk
more carefully: no amount of care *inside* the walk survives the walk being
re-parented.

### P3a — missed on the first run, by this ticket's own defect

`out_p2_FIRSTRUN_one_lost.txt` is the transcript of the run that refuted it. One
`GATE LOST` over 787 lines: `kernd633.py:172`, the `sys.exit(1 if bad else 0)`
**inside `deliver`**. The first dead man's switch recorded the *fact* that a
verdict had been delivered, so deleting the exit recorded it, returned normally,
and the process ran off the end of e2 with status 0. **The vacuous-pass defect,
inside the function written to close the vacuous-pass defect.** P4c predicted
this class of outcome and it was found by running the sweep, not by reading the
patch. The switch now records the **exit code** and returns it, so the verdict is
carried by two lines and either alone delivers it; `P3c` has both halves as rows,
including the case where the code is 0 and the switch must not turn it into 9.

---

## Five defects of this instrument, kept

1. **The repair's own first version was defeatable** — above, and the transcript
   is committed rather than replaced.
2. **The sweep edits the tree it measures.** `neutralise()` strips the strike
   markers from one named document in the sandbox, because a second live finding
   masks four of the six. Stated, named, counted, proved green afterwards, never
   done to the worktree — and still an instrument that had to change a tree to
   measure it. No row in P2 is a fact about the unedited tree.
3. **`attribution()` reports the FIRST sentence it recognises, not the sentence
   that caused the red.** In `P2e`, `bad += len(fires)` is attributed to *the
   cross-section finding itself* and the line that delivers the verdict likewise,
   because `STANDING UN-STRUCK` is printed in both runs and comes first in the
   list — although what actually produced the red was the two-witness
   disagreement in one case and the dead man's switch in the other. **The exit
   code is the reliable column** — `2` is the floor and `9` is the switch — and
   the attribution column should be read as *this sentence was present*, not
   *this control fired*.
4. **`attribution()` is a fixed list of strings.** A control added later, with a
   sentence nobody adds to `ATTRIBUTIONS`, is scored `UNATTRIBUTED` — wrong in
   the direction of noise. `selftest1d26.py` S4 checks every string in the list
   and checks that a traceback matches none, which is the most it can do about
   a sentence that does not exist yet.
5. **189 of 803 repaired rows are `GATE HELD, UNATTRIBUTED`** and this repair does
   not reduce that number. They are tracebacks: red, and mute about which control
   fired. The instruction this ticket carries is that a deletion must not change
   the *verdict* silently, and a traceback changes nothing silently — so they are
   counted and printed rather than filed as findings, and the figure is here
   rather than left to be inferred.

## The figures, with their populations and their grains

| figure | population | grain | whose |
|---|---|---|---|
| 5 | the verdict path of the e2 cross-section gate | file | **mine**, derived in P1a; mg-d53d names the same five |
| 1058 | the same | line, at the publishing tree | **mine** |
| 806 | the same | line, at mg-d53d's tree | **mg-d53d's**, re-derived at D1 and not re-run |
| 255 | mg-4adb's certified deletion population | row of its transcript | **mg-4adb's**, re-counted in P1c |
| 6 / 4 | deletions outside that certificate that lost the gate / of those, silent, PRE-repair | line | **mine**, re-derived in P2b; agrees with mg-d53d's 6 and 4 |
| 0 / 0 | the same, POST-repair | line | **mine**, P2c |
| 18 | runner executions over the six at the repaired tree | (line, runner) | **mine**, P2d |
| 266 | the documents the checker examines | file | **mine**, and stale the next time a `*.md` lands |
| 1 | live standing occurrences on the untouched tree | occurrence | **mine**, P2a |
