# mg-502f — SELF-RED EXHIBITS: the class swept, and it has two members

mg-479c found one script that shells `./build.sh` while a shell redirect holds one of the
gate's own inputs open, repaired it, and said in terms that it had not looked for others:

> ANYTHING ELSE IN THE ESTATE THAT SHELLS `./build.sh` WHILE WRITING INTO
> `code/**/out_*.txt` HAS THIS BUG. I did not sweep for others — out of scope, and it is
> worth a ticket.

This is that sweep. **The class has two members and mg-479c had found one of them.** Both
are repaired here, and the enumeration is an instrument rather than a paragraph, so the
question can be re-asked on any future tree at 0.4 s.

    sh code/self_red_sweep_502f/run_all.sh

---

## 1. THE ANSWER, IN THE FORM THE TICKET ASKED FOR

The ticket asked for more than a list: *"for each instance found, say whether it was
red-for-itself during the window, and for how long — a control that was inert is a
different fact from a control that was merely fragile, and only the first needs
re-establishing."*

| | `x0_exhibit.py` (mg-06d1) | `x1_positive_control.py` (mg-e331) |
|---|---|---|
| found by | mg-479c | **this sweep** |
| in the class from | mg-f771 landing, `137bc4c`, 2026-08-13 04:43:26 | same |
| in the class until | mg-479c's repair, `2489681`, 2026-08-13 09:07:27 | this commit |
| **window** | **4 h 24 min** | **~6 h** |
| commits that landed on `main` inside it | **11** | 11, plus this branch's |
| **INERT or FRAGILE?** | **INERT** — its E0 arm refused and no arm ran | **FRAGILE** — 8 of 8 arms scored, exit 0 |
| runs inside the window, on the record | **1**, and it is committed (`da2f9db`) | **0** |
| needs re-establishing? | **no — mg-479c re-established it** | **no — it never stopped scoring** |

**Neither control needs re-establishing, and the reasons are different, which is exactly
the distinction the ticket asked for.** `x0_exhibit.py` was inert and mg-479c ran it after
repairing it. `x1_positive_control.py` was never inert: its X6 arm REQUIRES the gate to go
red and attributes the red by the ratchet's own decision line, so a gate red for two
reasons and a gate red for one are the same observation to it.

### The measurement behind the FRAGILE verdict

Not inferred — run, twice, on 2026-08-13, on this branch:

    python3 x1_positive_control.py > code/state_ratchet_e331/out_x1_positive.txt   110.3 s  exit 0   8 of 8 AS REQUIRED
    python3 x1_positive_control.py > <a file outside the watched class>            109.0 s  exit 0   8 of 8 AS REQUIRED

The two transcripts differ in **12 lines, all of them inside the "N transcript(s) left
modified by this arm" listings**. Every arm, every verdict, and the exit code are identical.

**The self-redness IS in the redirected run's own transcript, under the wrong owner.** X0
reports:

    3 transcript(s) left modified by this arm (expected; mg-724a D5):
      code/control_gate_724a/out_gate.txt, code/rendered_twin_pin_9bc2/out_control.txt,
      code/state_ratchet_e331/out_x1_positive.txt

The arm did not modify that third file. The shell did, before the arm existed, and
mg-724a's D5 — "the gate leaves tracked files modified in directories that are not mine" —
is the wrong owner for that line. A self-caused truncation was being read as a known and
accepted side effect of somebody else's gate.

### Why the difference in outcome, and why it is not luck

The two arms differ in **which polarity they require**:

* `x0_exhibit.py`'s **E0** requires the gate to be **GREEN before anything is planted**. A
  self-caused red falsifies its precondition, so it refused — correctly, about a redness it
  had caused itself — and every arm after it was skipped.
* `x1_positive_control.py`'s **X6** requires the gate to be **RED**. A self-caused red is
  absorbed into a red it was asking for.

So the same defect made one control inert and left the other scoring, and **the sign of the
arm's own requirement decided which**. That is worth stating because it generalises past
these two: a self-red defect is invisible in exactly the arms that expect red, and those
are the arms whose whole job is to demonstrate that something fires.

---

## 2. THE MECHANISM, COMPUTED RATHER THAN REMEMBERED

The shell opens a redirect target **before** the process starts. So for the whole of a run
of `python3 s.py > code/d/out_s.txt` that tracked transcript is first empty and then
partial. `./build.sh` ends with mg-f771's control, which grades every tracked
`code/**/out_*.txt` that differs from its committed copy.

`s0_controls.py` §M hands **mg-f771's own `verdict_for`** — the function that actually
grades every transcript on every merge, isolated by f771 so controls could exercise it —
the real committed bytes of a real tracked transcript against exactly those two states:

| | | |
|---|---|---|
| M1 | EMPTY — the instant the shell opens the redirect | `DISAGREES` |
| M2 | PARTIAL — the file while the script is still running | `DISAGREES` |
| M3 | UNTOUCHED — the control | `AGREES` |

`DISAGREES` **is** the gate exiting 1. M3 is not decoration: without it, M1 and M2 are
consistent with a grader that returns `DISAGREES` for everything, which would make this a
report about a broken grader instead of a broken invocation.

The mechanism was also caught **live** on this branch. Running the old published invocation
against the repaired `x1_positive_control.py`, the guard refused at exit 2 — and
`git diff --stat` on the file the shell had already opened read:

    1 file changed, 128 deletions(-)

Zero bytes, before a line of the script had run.

---

## 3. HOW THE CLASS WAS ENUMERATED, AND WHY A GREP WOULD HAVE FOUND NOTHING

The precondition has two halves, and **they are not equally answerable**.

**A — THE EXEC EDGE is in the source, so it is decidable.** A gate literal in *code* (not a
docstring, not a `#` comment, and not solely an argument to `print()`/`.write()`), plus an
exec primitive somewhere in the same file. The two conditions are **decoupled**, and that
is a finding rather than sloppiness: the tighter rule *"a `build.sh` literal inside an exec
call"* was written first, and **it missed `x1_positive_control.py`**, which builds
`["sh", os.path.join(L.ROOT, "build.sh")]` and hands it to a local helper that is the one
calling `subprocess.run`. One hop of indirection defeated it. `s0_controls.py` D1 keeps
that shape as a world so the rule cannot drift back.

**B — THE REDIRECT IS NOT IN ANY FILE, AND THIS IS THE FINDING THAT SHAPES THE INSTRUMENT.**

> **A detector that greps for `> out_*.txt` would have found ZERO of the two real
> instances.**

`x0_exhibit.py`'s redirect was written down nowhere until mg-479c wrote it into `build.sh`'s
header *after* the repair. `x1_positive_control.py`'s appears only as a README table row,
`| x1_positive_control.py → out_x1_positive.txt |` — a producer/artifact mapping, not a
command. The redirect lives in the operator's fingers, which is precisely why the defect was
silent.

So §B asks the question the grep was a proxy for: **is a tracked transcript bound to this
script that the script does not write itself?** If so, the committed bytes can only have
arrived by a capture, and a capture into a tracked transcript is the defect. Three binding
rules, and **each caught an instance the one before it missed**:

| rule | | caught |
|---|---|---|
| `NAME` | `code/d/w.py` ↔ `code/d/out_w.txt` | `x0_exhibit.py` |
| `REDIRECT` | a literal `script … > out_*.txt` in a tracked `.sh`/`.md` | **neither** |
| `ARROW` | a documented pairing on one line of a tracked `.md` | `x1_positive_control.py`, whose transcript name is not its own stem |

### The target set is measured, not assumed

The ticket says "`./build.sh` **or any target that runs `gate_fixed_point_f771`**". §0
measures that those are the same set here rather than inheriting it from a comment: f771
refuses without `BUILD_SH_RAN_THE_SUITES`, and exactly one tracked line sets it. **If a
second route ever appears, this sweep REFUSES at exit 2** rather than reporting a green it
cannot support.

That refusal fired twice during construction, on this instrument, against a clean tree —
once because the rule counted a README sentence as a route, once because it counted
`lib_f771.py`'s own `FRESH_ENV = "BUILD_SH_RAN_THE_SUITES"`. Both are kept in
`handshake_setters`'s docstring. The refusals were the right *behaviour* on a wrong rule,
which is the order this estate prefers to the alternative.

---

## 4. THE FAMILY IS OLDER THAN THIS TICKET, AND THE FIX WAS ALREADY IN THE GATE

"The shell truncates the redirect target before the process starts" has been found in this
repository **four times, by four tickets, from four directions** — and this is the first
time anyone has counted them together:

| ticket | how it presented | where it is written |
|---|---|---|
| **mg-ec63** | a killed probe leaves a zero-byte file **that reads as a pass** | `code/corpus_universe_1d6c/run_all.sh:12` |
| **mg-bf79 / mg-fd9c** | a census of `code/*/out_*.txt` **cannot see its own transcript** | `code/corpus_fixedpoint_fd9c/run_all.sh:28` |
| **mg-f771** | `g0` would open its own transcript, find it EMPTY, and grade the committed copy DISAGREES — *"on every run, forever, in the file written to detect exactly that"* | `code/gate_fixed_point_f771/run_all.sh:15` |
| **mg-479c** | `x0_exhibit.py` reddens the gate it is exhibiting | `build.sh`, mg-479c block |

**The fix was already deployed, inside `build.sh`'s own last suite, on the day the defect
was created.** mg-f771's runner writes to `.out_$arm.txt.partial` and `mv`s it into place,
and its comment explains why. mg-ec63 and mg-bf79 reached the same `.tmp`+`mv` earlier still.

So why did `x0_exhibit.py` and `x1_positive_control.py` not have it? **Because the fix lives
in the runner, and these two scripts have no runner.** Both are explicitly excluded from
their suites' `run_all.sh` — mg-e331's says so in a paragraph headed `WHAT THIS DOES NOT
RUN`, mg-06d1's README marks x0 **"Not run by the gate"** — because both are expensive
end-to-end exhibits, not merge-gate arms. Having no runner is exactly why they were
redirected by hand, and having been redirected by hand is exactly why nothing carried the
estate's own fix to them.

> **The class is not "scripts that run `./build.sh`". It is "scripts that run `./build.sh`
> and that no runner runs."** That is a stronger predicate than the ticket's, and it is the
> one that explains all four historical instances.

---

## 5. THE REPAIRS, AND WHY THE EXISTING ONE WAS NOT ENOUGH

`x1_positive_control.py` gets **mg-479c's shape**: buffer the output, write
`out_x1_positive.txt` after the last gate run.

Both scripts additionally get a **guard**, and the reason is a defect in the existing
repair. **mg-479c changed the default invocation; it did not remove the old one.** The
command `python3 x0_exhibit.py > out_x0_exhibit.txt` is still published — in `build.sh`'s
own mg-479c block, and in this ticket's body — and typing it truncates the file at the
moment the shell opens it, *whether or not the script later rewrites it*. A repaired
self-writer is safe by default and unsafe on demand.

`guard_502f.refuse_if_self_red()` asks whether this process's stdout **is** a tracked
transcript, **by inode rather than by path string** — `> out_s.txt` from the directory,
`> code/d/out_s.txt` from the root, `>>`, and a symlinked path are one situation and
`os.fstat` gives them one answer — and refuses at exit 2 if it is. It imports the watched
class from `lib_f771` rather than re-spelling it, so there is one definition of what a
transcript is and it belongs to the control that grades them.

Measured end to end, on this branch: both scripts under the old published invocation now
exit **2** with a refusal naming the file, instead of running.

**`out_x1_positive.txt` is regenerated by this commit, and that is a consequence of the
repair rather than a decision about another ticket's content.** The repaired script writes
its own transcript, so running it once — which is how the repair was verified — produced
one. The committed copy was from `42b5bb0`, 2026-08-10, three days and 11 landings stale:
`STATE.md` has gone 19,077 → 21,328 words and X5's counterfactual 20 → 31 blocked landings.
**All 8 arms still score AS REQUIRED and the exit is still 0**, so nothing mg-e331 claims
has changed; the numbers under those claims have. It is not gate-watched — no suite rewrites
it, which is precisely the condition mg-f771's §1 names — so this refresh was optional and
is done because a dated measurement that can be re-taken and is not is the neighbouring
defect (mg-20ee's population).

The sweep's verdict vocabulary tracks the distinction:

* **INSTANCE** — runs the gate, a transcript is bound, the script does not write it. *Every*
  regeneration is self-red. (`x1_positive_control.py`, before this commit.)
* **EXPOSED** — writes its own transcript but does not refuse the redirect. Default safe,
  published invocation not. (`x0_exhibit.py`, after mg-479c and before this commit.)
* **GUARDED** — refuses. (Both, now.)

---

## 6. NOT ADDED TO `build.sh`, AND THE REASON IS THIS TICKET'S OWN SUBJECT

Measured first: **0.41 / 0.41 / 0.40 s**, three runs, against a gate measured at **88.9 s**
on this host minutes earlier. Cost is not the objection. Two things are.

**First, mg-d72e's warning applies to me more literally than to anyone.** *"Adding a suite
to the loop is exactly the operation that created this bug."* mg-f771 joined the gate and
broke an existing control as a side effect; the ticket I am answering exists because of it.

**Second, and this is the one that decides it: my §2 verdicts would be red-on-improvement.**
This suite goes GREEN only while the class is empty. The moment somebody writes a legitimate
new end-to-end exhibit that runs `./build.sh` — the kind of control this estate keeps
deciding it wants more of — this suite goes RED and **blocks every merge in the repository
until they adopt the guard**. That is a gate that refuses a category of good work in order
to enforce one line of it. mg-79ba declined to gate its own suite for a neighbouring reason
and said so in `build.sh`; mg-e35b named red-on-improvement as a shape; I am not the ninth
generation to ship its own subject.

**What is wired instead is the thing that actually prevents the defect:** the guard, in the
two scripts that can hit it, refusing at exit 2 with a message that names the file. That
costs nothing on the merge path and cannot be red for an innocent branch. This suite is what
you run — or what the next ticket about this class runs — to ask whether the population has
changed. `run_all.sh` is a single command and its transcripts are committed.

**The residual is stated rather than discovered: nothing runs this on a schedule, so a new
instance is found by somebody choosing to look.** That is strictly better than mg-479c left
it (nothing to run) and strictly worse than a gate. It is the filed successor.

---

## 7. DEFECTS AND LIMITS OF MY OWN

**D1 — my first exec-edge rule missed a live instance.** *"A `build.sh` literal inside an
exec call"* is the obvious rule, it is what I wrote, and `x1_positive_control.py` — the one
new instance this whole ticket exists to find — defeated it with one hop of indirection. Had
I not read the file by hand first, this sweep would have shipped GREEN with the answer
"mg-479c found the only one". Kept as world D1.

**D2 — my first version of §3's honesty was a grep, and the grep finds nothing.** See §3B.
The instrument is built around this miss.

**D3 — this instrument refused itself three times before it ran clean, and the third one is
the interesting one.** The first two were §0's route rule counting a README sentence, and
then `lib_f771.py`'s own `FRESH_ENV = "BUILD_SH_RAN_THE_SUITES"`, as second routes to f771.
The third arrived **only after the suite was committed**: until then its own files were
untracked, `git ls-files` did not show them to it, and it could not see that
`lib_502f.py:40` and `s0_controls.py`'s planted world both name the handshake in code.

> **It passed while uncommitted and refused the moment it was committed.** An instrument
> that reads `git ls-files` is blind to itself for exactly as long as it is new, which is
> exactly the period during which its author is deciding whether it works.

The resolution is a **declared, named exemption of two directories** — `ROUTE_EXEMPT`, the
callee and this instrument, each with its reason — modelled on `lib_f771.SELF_EXCLUDED`,
which is one *file* and is held to one file by worlds E1–E7. Same discipline here: §0
**prints the exemption and the number of mentions it did not ask about**, so it is a stated
number rather than a silence, and D16–D18 hold the list to exactly those two and check that
a route planted outside them is still caught. The exemption suppresses §0's route question
only; **§1 scans both directories for exec edges by the same rule it applies everywhere
else**, so a self-red script placed inside either one is found.

**D4 — the `EXPOSED`/`INSTANCE` split did not exist in the first draft,** which called
mg-479c's repaired script an `INSTANCE` outright. That overstates a real repair. The split
is the honest form and it is what surfaced the guard as the missing half.

**D5 — the sweep parsed all 1164 tracked `.py` files and took 8.74 s** before a prefilter
took it to 0.22 s. Reported because a "0.4 s" in §6 that was never 8.74 s would be
mg-17aa's D4.

**D6 — I did not regenerate `out_x1_positive.txt` from a red gate.** The FRAGILE verdict
rests on two full 110 s runs whose arm-by-arm results are identical, plus the mechanism
computed in §M. I did not separately capture `./build.sh`'s full stdout inside X6 to see
f771's own `VERDICT: RED` line, because X6 filters its subprocess output to lines starting
`RATCHET VERDICT:` or `GATE VERDICT:` and f771's verdict line starts with neither. **That
filter is itself the reason the arm could not see what was happening to it**, and saying so
is worth more than the extra run would have been.

### What this sweep cannot see, declared

* **`cmd | tee code/d/out_s.txt`.** stdout is a pipe; nothing in the process can name tee's
  argument, and no literal exists for §B to bind. This estate already forbids the pipe form
  for an older and unrelated reason (`cmd | tee f` makes `$?` tee's status — mg-9bc2,
  restated in three runners), so the forbidden form and the invisible form coincide. **That
  is luck, not design.**
* **An untracked script.** Nothing outside `git ls-files` is read.
* **A shell reaching the gate through a variable** (`G=./build.sh; $G`). §1's shell rule
  matches a literal. No tracked shell file does this today.
* **A script that `open()`s a tracked transcript by name while `./build.sh` runs.** The
  guard reads stdout's identity, not the process's future writes.

---

## 8. THE FRAMING THE TICKET ASKED ME TO CARRY, ANSWERED

The ticket's own words: *"A correct new control broke an existing one as a side effect, and
the breakage was invisible because the victim failed in a well-formed way. mg-f771's
fixed-point invariant is right and I would authorise it again."*

**Confirmed, and the cost is now a number.** The estate had one fewer working end-to-end
control than its transcripts claimed for **4 h 24 min**, across **11 commits landing on
`main`**, and the second member of the class was never inert at all. The inert state is on
the record: `da2f9db` commits `out_x0_exhibit.txt` reading *"REFUSED — the gate is ALREADY
RED before anything was planted"*, and the very next commit repairs it.

**And the cost was smaller than the ticket's framing implies, for a reason worth writing
down.** "On every run, forever, since mg-f771 landed" is true of the mechanism. It is not
true of the damage: exactly **one** run of `x0_exhibit.py` happened inside the window, and
it was the run that found the defect. The exposure was four hours, not days, because the
first person to exercise the control after f771 landed exercised it *in order to change it*.
Nothing in this estate arranged that.

---

## 9. THE FILES

| | |
|---|---|
| `lib_502f.py` | the detector rules, isolated so `s0_controls.py` tests these and not a re-spelling |
| `guard_502f.py` | the runtime refusal; imports `lib_f771.is_transcript` so there is one definition of the watched class |
| `s0_controls.py` → `out_s0_controls.txt` | 30 planted worlds: the mechanism (§M), the detector (§D), the guard (§G) |
| `s1_sweep.py` → `out_s1_sweep.txt` | the estate, swept |
| `run_all.sh` | the runner. `.tmp` + `mv`, stdout only, no pipe — for this suite's own subject |

Two files outside this directory are edited, and both are class members:
`code/alias_agreement_06d1/x0_exhibit.py` (guard added) and
`code/state_ratchet_e331/x1_positive_control.py` (self-write + guard).

**Related, and deliberately not merged with:** mg-20ee (the 64-instrument stale-address
census) is a different defect over the same population. mg-d72e is checked and named in §6.
