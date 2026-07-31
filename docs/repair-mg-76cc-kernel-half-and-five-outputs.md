# The kernel half of the predicate is back, and `G-3` is shut on five — `mg-76cc`

**Repair of the two sites `mg-957f` left open on `mg-7e58` (`4372fae`).**
Neither was deferred and both are here.

`mg-957f` confirmed the rest: the attribution is right at every row it scored,
and derived; `g1` was not silenced. Nothing below re-opens either, and nothing
below re-states them as though this ticket had established them — `mg-957f`'s
own figures are deliberately not quoted here, because every *"N of M"* in this
document is one `r4` can find in an `out_r*.txt` of this repair's own.

---

## 0. The bottom line

**`OPEN 1` — the kernel half of the predicate is restored, and restored at the
measurement grain.**

`g1_provenance.py`'s deleted file-sha finding ran over **two** files —
`c1_branching.py` and `kern_a218.py`, the file `g1`'s own section (ii) labels
*"its kernel — the measuring half"*. What replaced it ran over one, because
both sides of its comparison went through `run_c1(script_rev=REV_A218)` and
that call loads the kernel from the same revision it loads the script from.
Section (v) now moves **each half to `HEAD` on its own**, with the other held
at `286d5030`, and then moves **both together**; `lib58da.run_c1` grew a
`kernel_source` / `kernel_rev` argument so that it can express *this script
with that kernel* at all.

It was found by running the pre-repair predicate, and it is confirmed the same
way. One clone, `kern_a218.py` bent **as a commit**, three revisions of `g1`:

| `g1` revision | exit | self / find | names `kern_a218.py` |
|---|---|---|---|
| `ef388417` — before `mg-7e58`, file grain | 1 | 0 / 2 | **yes** |
| `e006581c` — before `mg-76cc`, the hole | **0** | 0 / 0 | **no** |
| this repair | **1** | 1 / 3 | **yes** |

The middle row is the defect, reproduced before anything is claimed about
fixing it. The bend moves **24 of 24** of `c1`'s own vertex cells, checked
before it is used for anything.

**`OPEN 2` — `G-3` is shut on five, and the claim is narrowed rather than
re-asserted.**

**1 of 5** committed outputs reproduces byte for byte, over **9** differing
lines, and **9 of 9** of those lines are one revision printed into a file that
is then committed. That number cannot be raised: a transcript that prints
`HEAD` is written **before** the commit that commits it, so no committed set of
these outputs can byte-reproduce. Shown at two distinct revisions rather than
argued. Under a **named** normalisation of that one revision the five
reproduce at **5 of 5** with **0** lines unexplained, and two controls show the
normalisation still catches a real difference. The absolute sentence is
withdrawn where it was written.

**And this deliverable is checked for the defect it repairs** — §5, six
branches, five of which can remove detection and one of which cannot, with the
reason given rather than the branch omitted.

---

## 1. `OPEN 1` — a predicate over two files had become one over one

### What the grain argument got right, and what it dropped

`mg-321d`'s `G-1` was correct: a file sha is the wrong grain for *"did the
measurement move?"*, and `mg-58da`'s own commit proves it — it edited `c1`'s
**comparing** half, so the file moved and the measurement did not. `mg-7e58`
re-grained that correctly.

But the predicate it replaced ranged over `paths[:2]`:

```python
for p, _ in paths[:2]:          # c1_branching.py, kern_a218.py
    if sha@REV_A218 != sha@HEAD:
        finding("%s … the measuring half … is not the same code")
```

and its replacement ranged over one thing, because

```python
out, _ = L.run_c1(target_text, script_rev=L.REV_A218, script_source=script_src)
```

varies `c1` by `script_source` and takes the kernel from `script_rev`, which is
`REV_A218` on **both** sides. The population shrank from two to one and was
not named as shrinking. That is coverage going backwards, and it is invisible
from the new side: every forward-looking check passes, because the thing that
would have complained is gone.

### The repair

`lib58da.run_c1` takes the kernel as an argument of its own — `kernel_rev`
defaulting to `script_rev`, and `kernel_source` overriding it outright, exactly
as `script_source` overrides the script's. Every one of the **11** existing
call sites in the four scripts this repair never opened goes through the
default and is unchanged; §4 shows that by running them, not by reading them.

`g1`'s section (v) then asks the question over a population of two, and names
each member:

```python
HALVES = [("c1_branching.py", "the script",   head_c1, old_kern),
          ("kern_a218.py",    "its kernel",   old_c1,  head_kern),
          ("both together",   "cancellation", head_c1, head_kern)]
```

Each half moved to `HEAD` alone, with the other held at `286d5030`, so a
finding says **which file** moved the measurement; then both together, because
two changes that cancel would pass each half separately. Two target forms
× three halves = **6** measurement-invariance checks where there were 2, and
the findings population line says so.

The direction probes were restored over the same two files: `c1 @ HEAD`
unmodified, `kern @ HEAD` unmodified, `c1` with its vertex dimensions off by
one, `c1` with a line past section (iii), and **`kern` with `dim L(n,p)` off by
one** — the probe that did not exist, and without which nothing here could have
noticed that the kernel was outside the check at all. On this branch: **5 of
5** directions predicted.

### That it is a gate and not a claim

Each unit added is deleted **alone**, in the tree where its effect exists — a
deletion tested in the wrong tree comes back a no-op for a reason that has
nothing to do with the unit:

| unit deleted | kernel bent | exit | self / find | names kern | probes |
|---|---|---|---|---|---|
| the `kern_a218.py` row of `HALVES` | yes | 1 | 1 / 2 | **no** | 3 of 4 |
| the both-together row of `HALVES` | yes | 1 | 1 / 2 | yes | 3 of 4 |
| the kernel row of `PROBES` | no | 0 | 0 / 0 | no | **4 of 4** |
| the one-line repair inside `measurement()` | no | **1** | 0 / 1 | no | **4 of 5** |

The last row is `F-1` **put back**, on an otherwise unmodified tree: re-pin the
kernel and `g1`'s own kernel probe **MISSes** and `g1` exits 1. A gate that
does not catch the defect being repaired is a claim; this one catches its
return.

And the repair did not work by making the predicate red. The unmodified clone:
exit 0, `0/0`, **5 of 5** probes. `mg-7e58`'s own four `c1` directions, re-run
against the repaired `g1`: **4 of 4**, unchanged — restoring one half of a
predicate is a way to break the other, and it did not.

---

## 2. `OPEN 2` — `G-3` was shut on one output of five

### What differs, and it is one thing

`./run_all.sh` in `code/branching_audit_58da/`, run in a clone — in a clone
because that script redirects into the very files under test:

| file | reproduces byte for byte | differing lines |
|---|---|---|
| `out_selftest_58da.txt` | yes | 0 |
| `out_g1_provenance.txt` | no | 5 |
| `out_g2_redo.txt` | no | 1 |
| `out_g3_findings.txt` | no | 1 |
| `out_g4_fleet.txt` | no | 2 |

**1 of 5**, over **9** lines. Every one of the nine is printed in full in
`out_r2_reproduce.txt` beside what it becomes, and **9 of 9** become identical
under **one** substitution: the recorded revision on the committed side, the
clone's own `HEAD` on the fresh one.

### Why it cannot be raised

The transcript prints `HEAD`. Committing the transcript makes a new commit, so
`HEAD` is not what the transcript says by the time the transcript is in the
tree. A record that reproduced byte for byte would have to name the commit
that contains it, which is a sha over its own bytes. **No such file exists.**

Demonstrated rather than argued: the same tree at **two** revisions — the clone
above, and a clone with one further empty commit. Both differ from the record
in **9** lines, at the **same** `(file, line)` positions, and both normalise to
**0**. If the difference were incidental the two would differ in different
places, or one of them would come back clean.

### The claim, narrowed to what it can hold, and gated

`out_r2_reproduce.txt` now closes `G-3` on all five, on four things rather than
on bytes alone:

* every transcript **names the revision it was taken at**;
* the fresh run names the revision it was **actually** run at — exactly, not
  approximately: `9c9328ad93f2` printed, `9c9328ad93f2` in the clone;
* the committed record's revision is an **ancestor** of the tree it sits in,
  with the number of commits between them printed rather than described;
* with that one revision normalised away in both, **0** lines differ — in all
  five, giving **5 of 5**.

The normalisation's population is named and small: the 40-, 12- and
8-character forms of **one** revision, and that revision's subject truncated
the way `g1` truncates it. `286d5030` and `ed9cde49` are pinned constants in
these transcripts and must still reproduce byte for byte, and they do, or the
rows would not be zero. Two controls show it is not a blanket — a figure
changed in `out_g3_findings.txt` and a whole line changed in
`out_g4_fleet.txt` are both still caught after normalisation.

### What remains

**The revision token itself is not reproduced**, and it cannot be. A
transcript naming some *other* real revision would normalise clean; what
constrains it is the ancestry row and the staleness figure, and those are
weaker than bytes. The alternative — factoring the revision out of the
transcripts into a file that is not compared — was not taken, because it is the
move this arc keeps finding: grain to clause, figures to labels, subdirectory
to symlink, a defect relocated rather than removed. Keeping the revision in the
transcript and naming the exception is the honest form of the same fix.

`code/branching_audit_58da/out_*.txt` were regenerated by this repair, because
`g1`'s output changed. They record `e006581c`, which was this branch's `HEAD`
at the moment they were taken — the freshest a transcript can be. `r2` prints
the distance from that revision to the tree's `HEAD` rather than describing it,
so how stale the record has since become is a number a reader can look at
instead of a claim they have to take.

---

## 3. The standing instruction, applied to this repair as well

> When a repair touches a predicate, **run the pre-repair predicate against the
> same inputs** and compare what each catches. Silence from the new one is not
> evidence unless the old one was silent too.

Five inputs, three revisions of `g1`, **15** runs. Each pinned revision runs
with **its own `lib58da`**, under a name of its own, with exactly one edit —
its import line — so that no predicate is judged against a library it never
saw. `g1_provenance.py` itself is never modified.

| input | real defect? | `ef388417` | `e006581c` | this repair |
|---|---|---|---|---|
| unmodified — null | no | exit 1 | exit 0 | exit 0 |
| `kern_a218.py`: `dim L(n,p)` off by one | **yes** | exit 1, names it | **exit 0** | **exit 1, names it** |
| `c1`: vertex dims off by one | **yes** | exit 1 | exit 1 | exit 1 |
| `c1`: a comment appended | no | exit 1 | exit 0 | exit 0 |
| `c1`: a line past section (iii) | no | exit 1 | exit 0 | exit 0 |

**Inputs where an older predicate catches a real defect and this one is silent:
0.** **Non-defect inputs on which this repair fires: 0.** Both are printed
even when empty, because a set that is only printed when non-empty is a set
nobody can check.

Note the `ef388417` column, which is why *"the new predicate must catch
everything the old one caught"* is the **wrong** rule: it exits 1 on four of
the five, three of which are not defects, including the unmodified tree. That
is `mg-321d`'s `G-1`. The right rule is *everything the old one caught **that
was real***, and the "real defect?" column is declared in the script before any
of the five is run.

**A return-site census cannot see this.** `g1` has **12** `finding(` /
`selferr(` sites before this patch and **12** after; two are removed and two
added, and they are the same two returns with edited text. What moved is the
**population two existing returns range over** — `HALVES` from an implicit one
to a named three, `PROBES` from three to five. `mg-7e58`'s own census could
not see `F-1` either, for exactly this reason.

---

## 4. The four scripts this repair never opened

`lib58da.run_c1` is underneath every script in `code/branching_audit_58da/`. A
default argument that quietly changed behaviour would remove detection in four
scripts this repair never opened — the same class as `F-1`, one layer down.

The **11** call sites are enumerated from those scripts' own source (with the
one *prose mention* of `run_c1` in a docstring excluded **by name**, not
silently dropped), and none of them names a kernel, so all 11 go through the
default. Then the four are **run**, end to end, in two clones — one carrying
this repair, one with `g1_provenance.py` and `lib58da.py` put back to
`e006581c` — and compared under the same normalisation §2 uses:

| script | this repair | `e006581c` | lines differing |
|---|---|---|---|
| `selftest_58da.py` | exit 0 | exit 0 | 0 |
| `g2_redo.py` | exit 0, 0 / 0 | exit 0, 0 / 0 | 0 |
| `g3_findings.py` | exit 0, 0 / 0 | exit 0, 0 / 0 | 0 |
| `g4_fleet.py` | exit 1, 0 / 2 | exit 1, 0 / 2 | 0 |

**4 of 4.** `g1` is excluded **by name** and not by silence: it is the thing
that changed, and §3 is where it is compared.

**And `mg-321d`'s own five finders, unmodified, run against this tree by
hand:** `h1_questions.py` 0 findings, `h2_grain.py` 0, `h3_setlevel.py` 1,
`h4_mine.py` 2, `h5_doccheck.py` 0 — exit `0`, `0`, `1`, `1`, `0`. That is
every one of them where `mg-957f` left it; `h3`'s finding and `h4`'s two are
`mg-321d`'s `M-1`, `M-2` and `c3`, all **OPEN** and none touched here. These
figures were taken by hand and are **not** in any `out_r*.txt` — `r4`'s
anchoring gate would reject them, which is why they are labelled rather than
folded in with the measured ones. `g4`'s two findings are
`mg-d330`'s `c3_withdrawal.py` and its `e4` presence test, both booked OPEN by
`mg-58da`, neither closed here and neither counted as a finding of this
repair's own.

---

## 5. This deliverable, checked for the defect it repairs

It restores detection, so it can remove detection. Six branches, enumerated
with where each is checked:

| branch | kind | can remove detection? | checked in |
|---|---|---|---|
| `g1_provenance.py` section (v) | predicate | **yes** | `r1` (v) — each added unit deleted alone, including the `F-1` reintroduction |
| `lib58da.run_c1`'s two new arguments | tool under every predicate in the directory | **yes** | `r3` (iv) — the four untouched scripts run with the library before and after |
| `g1`'s `SELF-ERRORS` population line | declared unit | **yes** | it was a **written** formula, `3 + len(paths) * 3`, that could not move when its own patch moved; it is now **counted** from the reads actually performed |
| `r1` / `r2` / `r3` — this instrument | gates | **yes** | `selftest_76cc.py`'s **93** assertions, plus `r1` (v) and `r2` (vi), each of which contains a control where the gate must go red |
| `run_all.sh` | runner | **yes** | `r4` (iv) — the real runner run with a red stub in it; `mg-c2b3`'s class |
| `PREDICTIONS.md` | record | **no** | — see below |

**`PREDICTIONS.md` cannot exhibit this defect, and the reason is that nothing
reads it.** No script parses it, no gate rests on it, and deleting it changes
no exit code. A record can be *wrong*, which is what §6 is about; it cannot go
quiet.

Two of these deserve their own sentence.

**The `SELF-ERRORS` population line.** It read *"the `3 + len(paths) * 3` git
reads this script needs"* — a figure written beside the code rather than taken
from it. It did not move when this patch added the two kernel reads section
(v) needs, and it had never counted the reads `run_c1` makes on the script's
behalf. It now counts them: **22**, derived. A declared unit that cannot move
when its own patch moves is not derived from it.

**The runner.** `mg-c2b3` swept this arc for runners whose exit code was eaten
by a pipe, which removes detection from every script under it at once. The
real `run_all.sh` is copied into a temp tree with every script replaced by a
stub: all green, it exits 0; one stub made red, it exits 1. Run, not read.

---

## 6. The instrument, and the misses kept

`code/branching_repair_76cc/` — four scripts plus a **93**-assertion self-test.
It is not one of `mg-a218`'s five, not one of `mg-58da`'s four, not one of
`mg-321d`'s five, not one of `mg-7e58`'s four and not one of `mg-957f`'s five,
and it writes into none of their directories: every mutation happens in a temp
git clone or a temp scratch tree, and `r2` runs `mg-58da`'s own `run_all.sh`
**in a clone** for exactly that reason.

Its `run_c1` takes the script and the kernel as two independent sources, which
is the whole of `F-1` and cannot be asked with a signature that inherits the
same defect. Its readers use `str.partition` and import no `re` at all, where
`lib58da` uses one regex per row and `lib957f` uses `ast.literal_eval` — two
readers that share an implementation share a blind spot.

```
./run_all.sh          # pure Python 3, no dependencies, NO NETWORK
```

`PREDICTIONS.md` holds every exit code and answer predicted **before** the run,
with the misses kept as written. There are two.

* The bent-kernel clone was predicted to give the repaired `g1` **4** findings
  and **0** self-errors. It gives **3** and **1**. The kernel *null* probe
  fires there — in that clone `kern @ HEAD` **is** the bent kernel — and the
  kernel *mutation* probe cannot be built at all, because its anchor has
  already been replaced. Both are right; both were missed by predicting a
  mutated tree's behaviour from the tree the script was written against. It is
  `mg-7e58`'s own `k1` failure, repeated.
* The differing-line count was predicted at **9** by counting `HEAD`
  interpolations as they stood *before* this repair. This repair removes one
  from `g1`'s section (v) header and adds one probe label that has one, and the
  two cancel. The answer is 9 for a different reason than the one predicted,
  and a figure that comes out right by cancellation was not derived.

And one caught by an instrument before any conclusion rested on it: the first
enumeration of `run_c1`'s call sites counted a **docstring** line saying
*"`run_c1()` really runs the script…"* as a twelfth call site. A population
inflated by prose is the failure the *no bare totals* rule exists to catch, and
it was committed by the section applying it. The mention is now excluded by
name and printed as excluded.

---

## 7. What is not closed here

* `c3_withdrawal.py` is red, and `g4`'s `e4` presence test with it. Both are
  `mg-d330`'s second finding, booked **OPEN** by `mg-58da`, untouched by
  `mg-7e58` and untouched here. Reported by name, not counted.
* `mg-321d`'s `M-1` and `M-2` remain **OPEN**; nothing here touches them.
* The revision token in the five transcripts is not reproduced and cannot be —
  §2, *what remains*.
