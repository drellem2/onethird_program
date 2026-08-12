# mg-9134 — the clean-verdict tag is ONE name, and the detector still fires on it

**Executes pm-onethird's decision: `audit-clean` survives, `audit-verdict-pass` retires. Then
asks the question that decision could not settle — has anyone ever observed this detector in the
context it RUNS in?**

Two parts, and they came out differently. Part 1 is done and measured. Part 2 is a finding.

---

## PART 1 — THE CONSOLIDATION

### The table, re-run after the rename (ticket step 5)

Measured against the live `~/.macguffin` store with the installed binary `/Users/daniel/go/bin/pogo`
(daemon revision `103693c7`), varying only the `[audit_successor]` section — the same protocol
mg-7ff8, mg-a882 and mg-a518 used, so these rows are comparable to theirs and not merely similar.

| `audit_tags` | examined | answered | reported | false reports |
|---|---|---|---|---|
| `["independent-audit"]` (as armed by mg-7ff8) | 4 | 4 | 0 | — |
| `["audit"]` **before** mg-a518's four tags | 9 | 6 | 3 | **2 of 3** |
| `["audit"]` **after**, with `clean_verdict_tags = ["audit-clean"]` | **9** | **9** | **0** | **0** |

`answered = 9` is `8 answered by a successor + 1 by a recorded clean verdict`, and **the 1 is the
whole subject of this ticket** — it is `mg-a0d6`, answered under the surviving name. The detector
counts the two kinds separately on purpose; the split is carried here for the same reason.

**VERDICT: consolidated-and-confirmed-unattended.** The first unattended `pogo doctor --check`
after the config landed printed that row character for character — see Part 2, which is not a
footnote, and which also records why that run had to be *procured* and what nothing on this host
does on its own.

### What changed, in the order it was changed, and the order IS the safety argument

pa518's warning was *do not delete a name from the config while any item still carries it*. That
is not fussiness. The clean-verdict half of this detector is a **string match between a tag on an
item and a list in a config file**, and the detector's failure mode is **silence** — so breaking
that match in either direction turns an answered audit into an unreported one, and it surfaces as
**one number moving in a line most people read as "green"**.

1. **`mg-a0d6` was confirmed to carry `audit-clean`** — read out of `~/.macguffin/work/done/mg-a0d6.md`,
   not assumed, not taken from the ticket. (The ticket said it had done this at 14:15 and to
   re-verify anyway. Correct instruction: verified independently.)
2. **`audit-verdict-pass` was removed from `mg-a0d6`** (`mg edit --rm-tags`), and `doctor --check`
   was re-run **before the config changed**: still `9 examined / 8 successor / 1 clean verdict /
   0 silent`. So the surviving name was already carrying the item on its own, with the retiring
   name still configured and no longer present — the one intermediate state in which a mistake is
   recoverable and visible.
3. **Every item file in the store was scanned for either name, BY TWO ROUTES** — 2781 files,
   every status including `archive/` and `shelved/`, every repo, by walking the tree rather than
   by `mg list` (a listing that filters is the wrong instrument for finding a carrier nobody knew
   about). **Exactly one file carries either tag: `done/mg-a0d6.md`.** Checked rather than
   reasoned, because the reason this ticket exists is a name nobody knew about.

   The second route exists because **the claim is an absence and one of the routes is a parser.**
   A frontmatter read can be defeated by a `tags:` line in a shape it does not recognise, so a
   dumb substring sweep runs beside it and every disagreement is printed. Four files mention
   `audit-verdict-pass` anywhere in their text and **all four are prose** — `mg-a882` and `mg-a518`
   (the tickets that created and found the collision), `mg-9134` itself, and `mg-a0d6`, whose body
   is corrected below. `289` files declare no `tags:` key at all — untagged older archived items
   and `.bodybak/` body backups, which cannot carry a tag — and **`0` have a `tags:` key that
   could not be read**, which is the number the absence claim actually rests on.
4. **Only then** `clean_verdict_tags = ["audit-clean"]`, in `~/.config/pogo/config.toml`.

Step 4 landed at **2026-08-12T13:35:53Z**. The XDG file is the right layer and that is not
stylistic: `ConfigFilePaths()` adds the `$POGO_HOME` layer **only when `POGO_HOME` is set**, so a
policy whose whole value is being ON must not live in `~/.pogo/config.toml` — mg-7ff8 measured
that and wrote the reason into the file it moved the section out of.

### Is it green because the name works, or green because the detector stopped looking?

That question is the only interesting one about any remedy of this shape, and `consolidate_9134.py`
answers it by mutation. Every arm changes one thing and requires the report to move.

| arm | what it does | required | observed |
|---|---|---|---|
| R1 | `["independent-audit"]`, pristine store | green, 4 examined | green, 4 examined |
| R2 | `["audit"]`, mg-a518's four tags removed | names `mg-07fd`, `mg-5cba`, `mg-a0d6` | exactly those three |
| R3 | `["audit"]` as armed now | green, clean-verdict count ≥ 1 | green, 9/8/1/0 silent |
| **N1** | **config on `audit-clean`, item on the RETIRED name** | names `mg-a0d6` | names `mg-a0d6`, clean-verdict **1 → 0** |
| **N2** | **item on `audit-clean`, config on the RETIRED name** | names `mg-a0d6` | names `mg-a0d6`, clean-verdict **1 → 0** |
| N3 | strip `audit-clean` from `mg-a0d6` | names `mg-a0d6` | names `mg-a0d6` |
| N4 | no clean tags configured at all | names `mg-a0d6`, offers no tag | names it, remedy offers none |

**N1 and N2 are the two halves of the rename hazard, run as experiments rather than argued in
prose.** N1 is the exact state that would exist had step 4 run before step 2 — the ticket
predicted `answered` would drop 9 → 8, and it does, with `mg-a0d6` back on the warn line. N2 is
the same break in the other direction and it settles something mg-a518 could only suspect: **the
two names are not interchangeable to the detector.** Configuring both while a decider was still
deciding was the right call, and the collision was a live hazard rather than a cosmetic one.

**N3 is what stops R3's green from being worthless.** Without it, "9 answered" is equally
explained by a detector that has stopped looking at `mg-a0d6` altogether.

### ARM D — my own instrument's failure mode, reproduced on purpose

pa518 disclosed that its own first control copied the store with `cp -R`, which does not preserve
mtimes. The detector ages an audit's silence from its `result.json` **mtime**, so on that copy
every unanswered audit read as `0 seconds silent`, landed in `waiting` instead of `silent`, and
**all four mutation arms came back PASS** — a control that could not fire, reporting green, inside
the remedy for a detector that could not fire and reported green. My ticket told me to assume the
same class of error was available to me.

It is, so **arm D takes it deliberately**: it copies the store *without* preserving mtimes and runs
the N3 mutation — the one that fires above.

```
    store copied WITHOUT preserving mtimes — result.json drift 182289s
[D] the N3 mutation, run on a store whose mtimes were destroyed by the copy
    status     : pass
    silent     : (none)
    population : examined=9 answered_by_successor=8 clean_verdict=0 waiting=1 undated=0
```

`clean_verdict` correctly falls to 0 — the tag really is gone — and the audit lands in **`waiting`**,
so the line stays **green** and names nobody. **The identical mutation that fires in N3 is silent
here.** `copy_store()`'s mtime assertion is therefore a *measured* refusal in this file rather than
a remembered one, and pa518's D1 is reproduced instead of quoted.

### Two defects of my own, both kept

**D1 — MY CHECK ON THE SWEEP WENT RED FOR A NON-REASON, INSIDE A TICKET WHOSE COMPANION DOCUMENT
NAMES THAT AS THE FAILURE.** Having added the two-route scan, I guarded it with "how many files
could this parser not read?" and counted every file whose `tags:` line `read_tags` returned `None`
for. That fired: **259 archived items**, and the run went red. They are not unreadable — they
**have no `tags:` key at all**, which is the ordinary state of items filed before this store used
tags, and an item with no tags cannot carry the retired name. I had conflated *"declares no tags"*
with *"declares tags I cannot read"*, and only the second undermines an absence claim. `mg-a518`'s
own runner says a gate that goes red for a non-reason is how gates get turned off; mine did it on
its first run. Split into `read_tags` and `tags_unreadable`, both now bounded to the frontmatter
block rather than the whole file — because these bodies quote `tags:` in prose, and **this item's
body does**, which is how a whole-file key scan turns prose into metadata. Now: `289` untagged,
**`0` unreadable**.

**D2 — I RENAMED THE TAG AND LEFT THE ITEM'S OWN BODY NAMING THE OLD ONE.** `mg-a0d6`'s frontmatter
said `audit-clean` while its body carried a dated section headed *"VERDICT TAG APPLIED:
`audit-verdict-pass`"* and a sentence explaining that both names are configured. Anyone opening the
item to learn which tag to use would have been told the retired one, by the item that is the
store's only instance of it — **archaeology, in the exact shape mg-a518 warned about when it
insisted a second tag needs an explanation beside it.** Caught by the raw-text route I had added to
guard the *absence* claim, not by anything looking for it. A dated correction is appended to
`mg-a0d6` (the original section is left standing as the record of what mg-a518 applied), and the
sweep now prints every prose mention so the next reader sees them rather than discovering them.

### The one edit outside this directory's own code

`code/audit_successor_arming_a518/controls_a518.py` had `audit-verdict-pass` in two places: the
`FIX2` tuple and its pinned config overlay. Left alone, mg-a518's C3 arm would strip a tag that no
longer exists, `strip_tag` would return `False`, and the arm would report *"the fix this arm
mutates is NOT IN THE STORE"* — **red for the right reason and the wrong world.** Both moved to
`audit-clean`; the arm's subject is unchanged. Re-run afterwards: **all seven arms behave**, C0 at
9/8/1 with nothing silent, C4 naming the same three. mg-a518's README is not rewritten — a dated
supersession note is appended to it, because its table and its COLLISION section are the record of
what was true when it landed.

---

## PART 2 — THE GATE NOBODY HAS DISCHARGED, AND WHY NOBODY COULD

mg-7ff8's acceptance condition 2 is *observe it in the context it RUNS in*. pa518 stated plainly
that this is **NOT MET**: every measurement — mg-7ff8's, mg-a882's, mg-a518's seven mutation arms,
and every arm above — is a **hand-run**. A hand-run proves the detector CAN speak. It does not
prove the scheduled invocation reaches it with the same config, the same store and the same mtimes.

**Before waiting for that scheduled invocation, I went looking for it. There is not one.**
`p2_who_runs_it.sh` prints the evidence; `out_p2_who_runs_it.txt` is what it printed on
2026-08-12T13:41:52Z.

| where an unattended run could come from | what is there |
|---|---|
| pogod itself | **nothing.** The check's renderer has exactly one call site in the whole pogo tree: `cmd/pogo/main.go:3472`, inside `pogo doctor --check`. pogod never invokes it. |
| launchd | 13 `com.pogo.*` agents scanned, **none** mentions doctor |
| cron | `crontab: no crontab for daniel` |
| `pogo schedule` | 24 entries, **0** mentioning doctor |
| host scripts (`~/.pogo/**/bin/*.sh`) | **no** invocation; the only `doctor` hits in `pogo-deploy.sh` are comments about the *agent* |
| **the doctor crew agent** | its prompt (`crew/doctor.md:69`) makes `pogo doctor --check` the first-line health check — and `auditsuccessors.go` names that agent as the reason the check reports on this checklist at all. **It was stopped 2026-08-10T17:14:23Z (`reason: requested`), its mail-check schedule removed as `agent_gone`, and it is not in `pogo agent list` — not running, not parked.** |

Its last actual run of the command was **2026-08-10T04:35:57Z**. Since then, 30 days of agent
transcripts contain 379 invocations across 35 agents and **every one is a person, a PM or a polecat
typing it** — including all 7 of mine.

**So the detector has had no unattended reader for the two days it has been armed.** mg-7ff8 armed
it, mg-a518 widened it, mg-9134 consolidated its tag list, three tickets measured it green — and on
current fleet state the only thing that ever fires it is somebody typing the command. **Arming a
detector and observing it are different acts, and only the first has been performed on this one.**

This is not a defect in the arming and it is not repaired here: bringing a crew agent up is the
mayor's call, not a polecat's. **It was requested** — mayor was mailed at 13:36Z with the evidence
above and an explicit request *not* to run the command and paste the output, since that is a
hand-run with extra steps and fails the condition in exactly the way the ticket warns about.

### STEP 6 — THE FIRST UNATTENDED RUN, AND IT AGREES CHARACTER FOR CHARACTER

The doctor crew agent was brought up at **14:02:46.525138Z** (pogod `agent_spawned`, pid 96791)
after I mailed mayor at 13:36Z and human at 13:47Z asking for exactly that, and asking explicitly
**not** to be sent a pasted hand-run. Seventy-one seconds later, off its own startup checklist and
with no instruction from me, it ran:

```
cd /Users/daniel && timeout 90 pogo doctor --check 2>&1 | head -40; echo "EXIT=$?"
```

and received, **verbatim**:

```
  ✓  audit successors      no merged audit has gone unanswered past 4h — 9 merged audit(s) examined: 8 answered by a successor, 1 by a recorded clean verdict, 0 still inside the 4h window, 0 with no recorded completion time
```

**Step 4 landed at 13:35:53Z; this is the first unattended run after it.** Against my hand-run of
13:35:56Z the difference is **none** — character for character past the `✓ audit successors` column
that only the human renderer prints. Same window, same population, same 8/1 split.
`out_p2_unattended.txt` carries the capture and its provenance.

**What it confirms.** The detector is reached, from a process that is not mine, **with this
config**: `9 merged audit(s) examined` is printable only by a run that found `[audit_successor]`
populated — an unconfigured one prints *"not configured"* instead. mg-7ff8 placed the section in
the XDG layer (read unconditionally) rather than the `$POGO_HOME` layer (read **only** when
`POGO_HOME` is set) precisely so this would hold across contexts, and **this is the first evidence
that it does.** And `audit-clean` was in the tag list that run actually used: `mg-a0d6` is ~50h past
the window and carries only that name, so `1 by a recorded clean verdict` is unreachable without
it — N1 shows the same store printing `0` and naming `mg-a0d6` when the name is absent.

**What it cannot confirm, and no observable could.** That the retired name was dropped. See the
limit below: a green line prints no tag list, and nothing carries `audit-verdict-pass` anyway.

**What is disclosed rather than glossed.** This run was **procured, not performed**. I asked for the
agent to be started; I did not run the command, choose its arguments, its environment or its timing.
Two hours earlier the path had **no runner at all**, so the honest reading is *"the path works when
the path is running"* — which is the strongest claim available on this host, and which is a
different sentence from *"the path runs"*. The finding above stands: **nothing schedules it.**

### A limit on what step 6 could ever have confirmed, found while measuring for it

Step 6 asks to *confirm the tag list it actually used matches step 4*. **A green run cannot show
that, by construction.** The configured names are rendered by `cleanVerdictAdvice`, which is called
from the **warn** branch of `auditSuccessorLine` and from nowhere else — a `pass` prints counts and
no tag list at all. That is why the arms above which verify a tag list are exactly the arms that go
red (R2, N1–N4 print `tags in the remedy`; R1 and R3 print `(none printed — this run is GREEN)`).

What a green run **does** discriminate is the population's third number. `mg-a0d6` is hours past
the 4h window and now carries **only** `audit-clean`, so `1 by a recorded clean verdict` is
reachable only if the list in force contained `audit-clean` — N1 shows the same run printing 0 when
it does not. So a green unattended line reading `8 answered by a successor, 1 by a recorded clean
verdict` **is** positive evidence that the surviving name was in force in that process.

It is **not** evidence that the retired name was dropped, and nothing observable could be: no item
carries it. That is precisely the condition that made dropping it safe, and it is the honest
statement of what this ticket can and cannot show.

### Recorded, not fixed, per the ticket

**Nothing checks that any audit was READ.** Both artifacts the detector counts — a successor ticket
and a clean-verdict tag — are cheap. `mg-a0d6`'s tag was applied against its recorded verdict
sidecar and its merged audit document, which is a stronger basis than the tag requires and is still
not a reading. **Zero false reports is not "every audit was acted on".** Out of scope here; filed
in `docs/audit-stage-process.md` beside the two limits it already carries.

---

## Files

```
consolidate_9134.py       arms S, R1–R3, N1–N4, D — the store scan, the table, the rename hazard
p2_who_runs_it.sh         PART 2 — every unattended path that could run the checklist, enumerated
run_all.sh                the runner, NOT wired into ./build.sh (reason inside)
out_consolidate.txt       transcript, 2026-08-12
out_p2_who_runs_it.txt    transcript, 2026-08-12
out_p2_unattended.txt     the first unattended run's `audit successors` row, verbatim, with its
                          provenance and what it does and does not confirm
```

Nothing here is imported by any other suite, and `./build.sh` is unchanged. The only files this
ticket touches outside this directory are `code/audit_successor_arming_a518/controls_a518.py` (one
tag's spelling, so its C3 arm can still fire), that directory's `README.md` (an appended
supersession note), and `docs/audit-stage-process.md` (the filing rule now names one tag).
`~/.config/pogo/config.toml` is host state and is not in any repository; its `clean_verdict_tags`
line and the comment block above it were rewritten to record the order and the limit.
