# mg-ec63 — PREDICTIONS for the ARC-WIDE truncate-before-probe sweep

**Committed BEFORE any script of this instrument exists.** Nothing in this
directory but this file at the moment of the commit that carries it. The commit
message begins `predictions:` and will never be amended.

The ticket's ask is the **sweep**, not the idiom fix: for each tree where a
probe reads a transcript its own run has already emptied, *what did the probe
fail to see, and what was published on the strength of it?* The fix is the easy
part and it is explicitly not the deliverable. Fixing first would destroy the
evidence, so every measurement below is taken **against the defect**.

---

## D — DISCLOSURES: measurements I had ALREADY TAKEN before writing any of this

These are not predictions. They are facts I read off the tree during
reconnaissance, and laundering them into predictions would be the exact
dishonesty this arc keeps recording. Each is stated with its population.

- **D-1.** Population `directories under code/ containing a run_all.sh`, at my
  HEAD `fe6a495`: **109**. Enumerated by the glob `code/*/run_all.sh`, which is
  a property and not a list. `code/` holds 116 directories, so 7 hold no runner.
- **D-2.** mg-03d1's `109` and my `109` are **the same total over different
  populations.** mg-03d1 counted `code/grain_axis_audit_03d1` — its own tree —
  and that tree does **not** exist at my HEAD: its MR `mr-d9pt5e2tjv1h244d8540`
  was still `queued` in the refinery at 01:18 and `git merge-base --is-ancestor
  d33970b main` exits non-zero. So the agreement at 109 is a coincidence of
  composition: mg-03d1's population is (my 109) − (some tree) + (its own), or my
  109 is a different set entirely. I have not yet diffed the two sets. **A
  number that matches is not a population that matches**, and this arc has
  already lost a night to an orphaned number that travelled.
- **D-3.** Population `the 109 runners`, by the shape of the redirect I could
  see with a one-line grep: **1** carries the `.new`-then-`mv` structural fix
  (`code/runner_exit_repair_bf79`). mg-03d1 reported **2** because it had
  adopted the fix in its own runner, which is the tree D-2 says I do not have.
  So `2` and `1` do **not** disagree; they are counts over the two different
  populations of D-2.
- **D-4.** Population `the 109 runners`, by runner idiom, from a crude grep:
  **73** invoke `python3 …X.py … > …` directly, **16** call a `run` shell
  function with the probe named as an argument, and **20** match neither. The
  `run`-function trees redirect through a positional parameter, and at least one
  (`face_geometry_instr_5f9a`) takes its arguments in the order
  `run <outfile> <probe>` while another (`runner_exit_repair_bf79`) takes them
  as `run <probe> <outfile>`. **A regex that only matches `python3 … > out_…`
  cannot see the 16, and cannot get the argument order right for the ones it
  does see.**
- **D-5.** Population `the .py files inside the 109 runner trees`: **574**.
  Population `files matching code/*/out_*.txt`: **518**.
- **D-6.** I have read mg-03d1's `a4_sweep.py` out of the object store at
  `d33970b` (it is not checked out on my branch). Its `bites` rule is:
  *(i)* the runner matches a truncation regex, **and** *(ii)* **some** `.py` in
  the tree matches `READS_OWN`, a regex over source text. It is a rule about
  **text**, at the grain of **the tree**, and it does not require that the probe
  whose transcript is emptied is the probe that reads it.

---

## P — PREDICTIONS

### P1 — the population rule, and the three counts

- **P1a.** My count of `runners that truncate a transcript with a plain >` will
  **not** be 86, because D-4 shows a text rule of that shape mis-parses the 16
  `run`-function trees. I predict my number over the population `109 runners`
  lands in **[80, 100]** and that I will publish the exact rule beside it.
- **P1b.** At least **10** of the 109 runners write **no** transcript at all
  (the runner streams to stdout and the transcript is captured outside it), so
  they are in no truncation population. `state_claims_repair_0120` is one; I
  name it now so the prediction is checkable.
- **P1c.** My parse will leave at least **1** runner **UNRESOLVED** — a shape my
  rule cannot decide — and I will print it as UNRESOLVED rather than silently
  binning it. Zero UNRESOLVED would make me suspect the rule of guessing.

### P2 — the biting count, and why I expect to disagree with 43

The ticket says a probe *"reads a file the same run has ALREADY EMPTIED."* That
is a strictly narrower claim than D-6's rule. Under `>`, the file emptied at the
instant probe *X* starts is **`out_X.txt` alone**; every *other* `out_*.txt` in
the tree still holds the **previous run's bytes** and is *stale*, not empty. A
tree where `p1.py` reads `out_p3.txt` matches D-6's rule and does **not** match
the ticket's sentence.

- **P2a.** Under the tightened rule *"the probe reads its OWN out target"*, the
  count will be **lower than 43**. I predict **≤ 40** over the population `109
  runners`.
- **P2b.** At least **8** of mg-03d1's 43 will fall out under the tightened
  rule — they read some other probe's transcript, which is a **stale-read**
  defect and a real one, but not the emptied-file defect this ticket is about.
  I will report the stale-read class separately rather than merge it away.
- **P2c.** I will determine "reads its own out target" **by observing the
  process open the file**, not by a regex over source text, via a
  `sys.addaudithook` shim on the `open` audit event. I predict the observed set
  and D-6's text-matched set **differ in both directions**: at least **1**
  false positive (source mentions `out_` but the process never opens one) and at
  least **1** false negative (the process opens one but the source never spells
  `out_` literally — a path built from a variable, a `Path` join, or a
  `subprocess` `cat`).

### P3 — the three outcomes, which I will not collapse

For each confirmed bite I run the probe twice **at the same tree state**:
**A** = the defect reproduced (its own out target emptied first), **B** = the
same probe with that transcript holding its committed bytes. `diff(A,B)` is
attributable to the shape and to nothing else.

- **P3a. SAME** (`A == B`, harmless ordering bug): the **majority** class. I
  predict **≥ 60%** of confirmed bites.
- **P3b. DIFFERENT** (`A != B`, a published figure is wrong): **at least 1**
  beyond mg-bf79's own. This is the class that costs something.
- **P3c. NEVER EXERCISED** (B cannot run at all — traceback, or a non-zero exit
  A did not have): **at least 1**, and I expect this to be the class I nearly
  miss, because a probe that has only ever run against an empty file looks
  identical in the transcript to one that ran and found nothing. If it comes out
  **0** I will say so plainly rather than promote a near-miss into it.
- **P3d.** I predict at least **1** confirmed bite where `A` does **not**
  reproduce the committed `out_X.txt` byte-for-byte — the tree has drifted since
  publication — and that this must be reported as a **third** comparison and not
  folded into `diff(A,B)`, because a drifted tree makes the published-claim
  question un-answerable from `diff(A,B)` alone.

### P4 — the damage, which is the only part that cannot be recovered later

- **P4a.** For every DIFFERENT tree I will name the specific published claim
  (README / OUTCOMES / commit subject) that rests on the empty-file reading, or
  state explicitly that **none does**. "The transcript changed" is not damage;
  "a sentence a human will read is false" is.
- **P4b.** I predict **at least 1** DIFFERENT tree where the delta is confined
  to the transcript and **no** prose claim rests on it — a genuine no-damage
  result, which must be recorded as a result and not as an absence.

### P5 — the positive control

- **P5a.** `code/runner_exit_repair_bf79/p5_self.py` is the known instance: it
  hid **NINE** of its own labels. That tree has the structural fix now, so it is
  outside the biting population — I will run it **both ways by hand** as the
  instrument's calibration. I predict the A/B delta there is **exactly 9 labels**
  and that if my instrument reports any other number the instrument is wrong,
  not the record.

### P6 — the fix, and the order

- **P6a.** I will apply the structural fix to **no other tree in this ticket**.
  The ticket orders sweep-then-fix and says inverting it destroys the evidence;
  step 2 of the ticket ("then apply the fix to the other 84") is a **second**
  action and I predict I will not reach it, and will say so under
  WHAT I DID NOT DO rather than let silence imply it was done.
- **P6b.** Every probe I run writes to a scratch path outside the repo, and I
  predict `git status --porcelain` over `code/` is **byte-identical before and
  after** the whole sweep. If any tree is left dirty, that is a finding against
  **this** instrument and goes in OUTCOMES.

### P7 — the floor nothing names

- **P7a.** The class this ticket calls "vacuous pass" has a member nobody has
  counted: a probe whose own out target is emptied and which reads it **through
  a corpus glob** — so the file is not merely empty, it is **silently present in
  the denominator as an empty member**. That inflates a "N of M" figure's M
  while contributing nothing to N. I predict at least **1** published `N of M`
  in this arc where **M counts an empty file**.

---

## Scoring

OUTCOMES.md will score every row above as HIT / PART / MISS against what the
scripts actually print, **and no row here will be revised**.
