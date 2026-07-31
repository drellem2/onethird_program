# The attribution is right; the kernel half of the predicate is gone — `mg-957f`

**Independent audit of `mg-7e58` (`4372fae`), which repaired `mg-58da`'s
provenance apparatus on `mg-321d`'s `G-1`, `G-2` and `G-3`.** Pre-filed in the
same action as its parent. Audited at `2d23d880`.

`mg-321d`'s defect was an apparatus built to establish provenance getting
provenance wrong **about itself**. So the first question this audit asks is not
whether the repair's instrument says the right thing — it is whether the
*apparatus* does, re-derived here from `git log` and never read out of the
apparatus and checked back against it.

---

## 0. The bottom line

**Confirmed.**

* **The attribution is right, at every row.** Every claim of the form *"X was
  touched by Y"* that `g1` or `g4` prints — **17** of them — was re-derived here
  from `git log` by two routes that had to agree with each other first.
  **17 AGREES / 0 WRONG COMMIT / 0 UNVERIFIABLE.** `ed9cde4 → 1 (c2)`,
  `673b4c0 → 1 (c1)`, and `c3`, `c4`, `c5` touched by nothing in the range.
* **And it is *derived*, proven by changing the history rather than by reading
  the code.** Three clones, one new commit each: a commit touching
  `c3_withdrawal.py` (which nothing in the range had touched) makes `g4` grow a
  row for it; a second commit touching `c1_branching.py` makes `c1`'s row name
  **two** commits; and a commit touching nothing among the five moves nothing.
  **3 of 3 followed.**
* **`g1` was not silenced — in the `c1` case.** The disposition `mg-321d`
  demanded is stated at **3 of 3** sites (`g1`'s source, the repair's document,
  and `g1`'s own stdout), each check deletion-tested. And `g1`, unmodified and
  in place, was run in **4** clones whose `c1_branching.py` is mutated as a
  commit: **4 of 4** directions predicted, with the file sha moving in two of
  them and only one a defect.
* **The set-level property survives, re-derived on readers written here.**
  **10 of 10** pairs agreeing at **24 of 24** cells over **240** cell
  comparisons; **5 of 5** of `mg-a218`'s members re-run in place, not only the
  ones the repair touched — it touched none; **5 of 5** locality probes move
  their own cell and no other.
* **`mg-321d`'s own finder agrees.** `h2_grain.py`, unmodified, re-run against
  the repaired tree at today's `HEAD`: **0 findings**, where its committed
  record has **3**.

**Two findings.**

* **`F-1` — the kernel half of the predicate was deleted, not re-grained.**
  `g1`'s file-sha finding covered **two** files. Its replacement covers one.
* **`F-2` — `G-3` is shut at one revision, not shut.** `1 of 5` committed
  outputs still reproduces on this branch. The branch aimed at exactly this
  question compares everything except the thing that moves.

---

## 1. `F-1` — the old predicate covered two files; the new one covers one

`g1`'s section (ii) names three paths and labels the second of them itself:

```python
paths = [(A218_DIR + "/c1_branching.py", "the script"),
         (A218_DIR + "/kern_a218.py",    "its kernel -- the measuring half"),
         (TARGET_REL,                    "the target … the read path")]
```

The predicate `mg-321d` objected to ran over `paths[:2]` — **both** the script
and the kernel:

```python
for p, _ in paths[:2]:
    if sha@REV_A218 != sha@HEAD:
        finding("%s changed …; the measuring half of the reproduction is not
                 the same code" % p)
```

`mg-321d` was right that this is the wrong grain for `c1_branching.py`, and the
repair re-grains it correctly. But the replacement — section (v) — asks its
question like this:

```python
def measurement(script_src, target_text):
    out, _ = L.run_c1(target_text, script_rev=L.REV_A218,
                      script_source=script_src)
```

and `lib58da.run_c1` loads the kernel from that same `script_rev`:

```python
with open(os.path.join(a, "kern_a218.py"), "w") as fh:
    fh.write(git_show(script_rev, A218_DIR + "/kern_a218.py"))
```

`script_source` varies `c1` across revisions. `script_rev` is `REV_A218` on
**both** sides. So `kern_a218.py` is pinned at `286d5030` for both runs, and a
kernel that moved between `286d5030` and `HEAD` cannot reach either side of the
comparison that replaced the finding which used to catch it.

**Measured, not argued.** One clone, `kern_a218.py` bent **as a commit** — every
simple's dimension off by one, the same shape as the repair's own `c1` probe,
moved one file down to where `c1` gets its numbers from —
with `c1_branching.py` and `g1_provenance.py` both byte-identical to this
branch:

| | | |
|---|---|---|
| does the bend really move `c1`'s measurement? | `a8db5dbd4c758765` → `cb329be9d6265c27` | **24 of 24** vertex cells move |
| the **pre**-repair `g1` (`ef388417`), same clone | **exit 1**, 0 self / 2 findings | one names `kern_a218.py` |
| the **post**-repair `g1` (this branch), same clone | **exit 0**, 0 self / **0** findings | names it nowhere |

The measurement really moves; the predicate that was removed caught it; the
predicate that replaced it is silent.

This is not the silencing `mg-321d` warned about — the `c1` half was genuinely
re-grained, and §2 shows the replacement going red on a real regression. It is
the narrower thing: a predicate over a population of **two** was replaced by one
over a population of **one**, and the population shrank without being named.

`g1`'s own findings population line still says the file-sha comparisons are
`REPORTED and are not in this population`, which is true and is the right
disposition for `c1_branching.py`. For `kern_a218.py` it means nothing now asks
the question at any grain.

**Why it has not bitten yet:** `kern_a218.py` has not moved in the audited range
— `git log 286d5030..HEAD -- code/branching_audit_a218/kern_a218.py` is empty,
re-derived here and agreeing with what `g1` and `g4` both print. `F-1` is a hole,
not a wrong answer.

**The narrowest repair** is one argument: give `measurement()` the kernel of the
revision whose `c1` it is running. That is `run_c1(..., kernel_rev=…)`, and it
makes section (v)'s comparison cover exactly what the deleted predicate covered.

---

## 2. `G-1` — how `g1` was reconciled, and it was not by silencing

`mg-321d` required one of two answers out loud: *either the finding is real and
the section is wrong, or the section is right and `g1` should not fire.*

**It is stated, at three sites, and each check goes red when the text is cut:**

| site | stated | check goes red without it |
|---|---|---|
| `g1_provenance.py`, module docstring — *"The finding was not silenced"* | yes | yes |
| `docs/…Mg7e58ProvenanceRepair.md` §1 — *"The section is right and `g1` should not fire"* | yes | yes |
| `g1`'s own stdout, section (v) — *"THE FILE MOVED AND THE MEASUREMENT DID NOT"* | yes | yes |

**And the replacement goes red on a real defect.** `g1` unmodified and in place,
four clones, the mutation always to `c1_branching.py` and always **committed**,
because `g1` reads `c1` with `git_show(HEAD, …)` and a working-tree edit would
reach nothing:

| clone | predicted | `g1` | self / find |
|---|---|---|---|
| unmodified — null probe | exit 0 | **exit 0** | 0 / 0 |
| `c1`'s vertex **dimensions** off by one | exit 1 | **exit 1** | 1 / 3 |
| a comment appended to `c1` | exit 0 | **exit 0** | 0 / 0 |
| a line appended past `c1`'s section (iii) | exit 0 | **exit 0** | 0 / 0 |

**4 of 4.** Rows two and four are the point: the file sha moves in both and only
one is a defect. In row two a finding naming *the measurement* is present, so
the redness is the new predicate's and not an accident of the self-error the
same clone provokes — `g1` cannot build its own internal probe out of an
already-bent `c1` and books that as a `SELF-ERROR`, exactly as `mg-7e58`
recorded.

**Which returns went away, counted off the patch.** Every line in either
revision of `g1_provenance.py` whose stripped form begins `finding(` or
`selferr(`: **10 before, 12 after**. Removed: **one**, the file-sha finding.
Added: three — the measurement-invariance finding, the probe-direction finding,
and the probe-build self-error.

**And the two new returns are separable.** In the bent-`c1` clone all three
findings fire. Deleting the measurement-invariance `finding(...)` **alone** takes
`FINDINGS` 3 → 2 and removes exactly that one; deleting the probe-direction
`finding(...)` alone takes it 3 → 1 and removes exactly its two. Neither
deletion is a no-op, so section (v) is two checks and not one check written
twice.

---

## 3. `G-2` — every attribution, re-derived, and then made to follow the history

**The ground truth, derived here first.** Route one asks the log about a path;
route two asks a commit what it did. They are different questions with the same
answer and the answer is used only if both give it — they agree at **5 of 5**
members.

```
route one -- git log 286d5030..2d23d880 -- <path>
  c1_branching.py    673b4c00
  c2_vertexsets.py   ed9cde49
  c3_withdrawal.py   NONE
  c4_seam.py         NONE
  c5_record.py       NONE
route two -- git show --name-only, per commit touching the directory
  673b4c00  c1_branching.py
  ed9cde49  c2_vertexsets.py
```

**Then every attribution either script prints, scored one row at a time:**

| where | attributions | AGREES | WRONG COMMIT | UNVERIFIABLE |
|---|---|---|---|---|
| `g4` (ii) member rows | 5 | 5 | 0 | 0 |
| `g4` (ii) per-commit rows | 2 | 2 | 0 | 0 |
| `g4` (ii) ticket labels | 2 | 2 | 0 | 0 |
| `g4` (ii) summary lines | 3 | 3 | 0 | 0 |
| `g1` (ii) read-path rows | 3 | 3 | 0 | 0 |
| `g1` (ii) reported sha rows | 2 | 2 | 0 | 0 |
| **total** | **17** | **17** | **0** | **0** |

The population is *every claim of the form "X was touched by Y" either script
prints* — not a sample, and `UNVERIFIABLE` is its own row rather than being
folded into agreement.

**And the derivation is tested by changing the history.** A derivation
regenerated by hand is not one, so three clones, one new commit each and no other
edit:

| clone | `g4` follows |
|---|---|
| a commit touching `c3_withdrawal.py`, which nothing in the range had touched | **yes** — new commit row appears, `c3`'s member row names it |
| a **second** commit touching `c1_branching.py` | **yes** — `c1`'s row now names two commits |
| a commit touching **nothing** among the five (null probe) | **yes** — no commit row, no member row moved |

**3 of 3.**

### What else the apparatus asserts about itself

Four claims about `g4`'s own machinery that its instrument does not gate:

* **the range's left endpoint resolves** to a commit (`286d5030`) and is a full
  sha, not a prefix — ok;
* **no two in-range commits carry the same `(mg-id)`**, so the ticket → commit
  step is unambiguous here — ok;
* **the summary's two halves are cross-checked asymmetrically.** `g4` cross-
  checks the `mg-13b2` row against `lib58da`'s named `REV_13B2`; there is no
  `REV_58DA` in `lib58da` and the `mg-58da` row is not cross-checked against
  anything. Reported, not booked: that row's **member list** still comes from
  `git log` and is scored above; only its *ticket* label rests on a subject, and
  the subjects are unambiguous in this range.
* **`g1` books no file-sha finding at all** any more — 0 findings of that form,
  which is the disposition stated and not a claim about coverage. That is `F-1`.

---

## 4. `F-2` — `G-3` is shut at one revision, and that is not shut

*This is the thing no list named, and it is the one I chose.*

`mg-321d`'s `G-3` is *the documented reproduce command does not reproduce*:
`mg-58da`'s committed evidence was recorded before its own commit existed and
stopped reproducing the instant that commit landed. `mg-7e58` closes it by
regenerating `code/branching_audit_58da/out_*.txt` at `ef388417` and stating
that *"`./run_all.sh` in `code/branching_audit_58da/` now reproduces its
committed outputs"*.

Run in a clone — in a clone because `run_all.sh` redirects into the very files
under test:

| file | reproduces byte for byte | lines differing |
|---|---|---|
| `out_selftest_58da.txt` | yes | 0 |
| `out_g1_provenance.txt` | **no** | 5 |
| `out_g2_redo.txt` | **no** | 1 |
| `out_g3_findings.txt` | **no** | 1 |
| `out_g4_fleet.txt` | **no** | 2 |

**1 of 5.** Every differing line is the same thing — a revision that moves,
printed into a file that is committed:

```
out_g1  line  16   ef38841710ed  HEAD of this branch      -> <the new HEAD>
out_g2  line 100   REDONE at ef38841710ed and it stands   -> <the new HEAD>
out_g3  line   6   run against out_t1_tl.txt at ef388417. -> <the new HEAD>
out_g4  line  39   script  286d5030 -> ef388417  …        -> <the new HEAD>
```

**The mechanism, and the repair's own hand in it.** `print()` sites whose
arguments include `HEAD[:8]`: `g1_provenance.py` **2 → 3**, `g4_fleet.py`
**0 → 4**. `g4`'s (ii) column header was a *written* string before the repair
(`286d5030 -> d1dd84d2`) and is computed from `HEAD` after it. That is the right
direction for provenance and the wrong one for a committed transcript, and no
branch in the repair's list weighs the two against each other.

**Why the branch aimed at this came back green.** `k2`'s `B1` is *"this repair's
evidence is recorded before the commit that commits it — `G-3`'s exact shape"*,
and it clones the repo, commits the repair there and re-runs `g1` and `g4`. Read
out of `k2_selfprov.py`'s own source, `B1` compares:

| | present in `B1` |
|---|---|
| self-errors | yes |
| findings count | yes |
| exit code | yes |
| finding **texts** | yes |
| the output **bytes** | **no** |

Every one of the four it compares is invariant under a moving `HEAD`. Bytes are
the one that is not, and bytes are what `G-3` was about.

**This is not "the repair failed".** `G-3`'s *substance* — the evidence
contradicting the tree — is genuinely closed: `g1` exits 0 with 0 findings,
`g4` exits 1 with the **two** findings its committed record already carries
(`c3_withdrawal.py` red, and `mg-d330`'s `e4` presence test — both booked OPEN
by `mg-58da` and neither closed by `mg-7e58`), and the re-run's
self / finding / exit figures match the committed record at 5 of 5. What does not
survive is the **byte-level reproduce claim**, and it does not survive by
construction rather than by accident. Either the claim wants narrowing to
*"reproduces up to the revision it names"*, or the outputs want the revision
factored out of them. Both are the repair's call, not this audit's.

---

## 5. What was not to be lost — re-derived on readers written here

`mg-7e58` touched **none** of `mg-a218`'s five, which is exactly why *"the
member I changed still works"* would say nothing: no member changed, and
corroboration is a property of the set.

| | |
|---|---|
| pairs of sources agreeing at all 24 cells | **10 of 10** |
| cell comparisons made | **240** |
| `mg-a218`'s members re-run in place | **5 of 5** |
| members green | **4 of 5** — `c3_withdrawal.py` red, `mg-d330`'s second finding, **OPEN** |
| readers moving at their own cell and no other | **5 of 5** |

The five sources are the target (`out_t1_tl.txt`), `c1` live, `c2` live,
`mg-2060`'s `b1` and `mg-d330`'s `e1`. The readers are written in `lib957f.py`
from the file formats on different mechanics from `lib58da`, `lib321d` and
`lib7e58` — token splitting and `ast.literal_eval` rather than one regex per row
— because two readers that share an implementation share a blind spot. Each is
probed at `beta=1, n=6`, the only `n=6` cell no other parameter carries
identically, and a source whose reader returns nothing is a **SELF-ERROR** and is
**withdrawn**, never scored as agreement.

`c3_withdrawal.py`'s redness is `mg-d330`'s second finding, booked OPEN by
`mg-58da` and untouched by `mg-7e58`. It is reported here by name and is not
counted as a finding of this audit's own.

---

## 6. `mg-321d`'s own finders, unmodified, on the repaired tree

| script | committed record | re-run at `2d23d880` |
|---|---|---|
| `h1_questions.py` | 0 findings | **0** |
| `h2_grain.py` — the finder for `G-1` and `G-2` | **3 findings** | **0** |
| `h3_setlevel.py` | 1 finding | **1** |
| `h4_mine.py` | 2 findings | **2** |
| `h5_doccheck.py` | 0 findings | **0** |

**5 of 5** directions predicted: `h2` was the one required to move and the only
one that did. `h2` going 3 → 0 is the repair confirmed by the instrument that
raised the findings, unmodified, and it is worth more than any figure this audit
computes itself. `h3`'s remaining finding and `h4`'s two are `mg-321d`'s `M-1`,
`M-2` and `c3` — all three OPEN, none in `mg-7e58`'s scope, none touched here.

Note the shape: `F-1` and `F-2` are both invisible to `h2`. `h2` asks whether
`g1` fires on a finding its own section refutes and whether `g4` names the wrong
commit; neither question can see a predicate whose *population* shrank, or a
transcript that reproduces only at the revision it was taken at.

---

## 7. The instrument

`code/branching_audit_957f/` — five scripts plus a **74-assertion** self-test.
It is not one of `mg-a218`'s five, not one of `mg-58da`'s four, not one of
`mg-321d`'s five and not one of `mg-7e58`'s four, and it writes into none of
their directories: every mutation happens in a temp git clone or a temp tree.

```
./run_all.sh          # pure Python 3, no dependencies, NO NETWORK
```

`PREDICTIONS.md` holds every exit code and answer predicted **before** the run,
**with the misses kept as written**. There are two, and both are the shape this
lineage keeps producing: *the thing being audited was right and my instrument
for checking it was wrong.*

* The kernel probe was first written to bend `kern_a218.py` in a clone's
  **working tree** without committing it. `g1` reads the kernel with
  `git_show(HEAD, …)`, never from the worktree, so the probe changed nothing and
  **both** `g1` revisions came back silent — which I would have been entitled to
  read as *"the old predicate does not fire either, so there is no hole"*. It
  does. The probe had to be a **commit**. That is `G-2`'s own shape: a question
  about a commit, asked of a working tree.
* `P6` predicted **2 of 5** outputs would stop reproducing and the answer is
  **4 of 5**. I had found the `HEAD[:8]` interpolation in `g1` and `g4` and did
  not look in `g2` or `g3`, which print the revision in prose rather than in a
  format string. The direction was right and the population was undercounted —
  which is the failure mode a *"no bare totals"* rule exists to expose, committed
  by the audit that was applying it.

And one found by the self-test before any conclusion rested on it: the first
kernel-bending probe inserted `pass` as the first statement of `vertices()`,
which is a no-op — a corruption probe that corrupts nothing. It was caught
because the self-test asserts the probe **reaches `c1`'s output**, not merely
that it edits the file.
