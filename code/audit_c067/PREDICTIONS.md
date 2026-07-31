# mg-c067 — predictions for the independent audit of the mg-132a publishing-commit repair

**Committed BEFORE any script of this instrument exists.** `git log --diff-filter=A` on this
directory is the check: this file must appear at a commit that is an ancestor of the one adding
`c1_rebase.py`. That ordering is a fact about the repository, not a claim in prose, and `C6b` reads
it back out of git.

## Disclosure: what I already knew when I wrote this

Predictions written after reconnaissance are worth less than predictions written blind, so here is
exactly what I had run before this file existed. All of it is `git` plumbing — **no script of this
instrument, and no invocation of the parent's instrument, had been run**:

* `git merge-base --is-ancestor` over the ten commits mg-132a's transcript names. Result:
  `4a06b4c`, `89d6aa1`, `7dc9180`, `d24bbeb`, `2cfd226` (all of mg-132a's own pre-rebase commits)
  and `8a07ae0`, `3d7b32f`, `c1a57fd` (mg-3f3b's) are **unreachable from HEAD**; `3958b5a` and
  `77306a7` are reachable.
* `git log -1 --format=%h -- <path>` for the three transcripts that carry a `.py` population.
  Post-merge publishing commits: `out_anchor_132a.txt` → `1e30484`, `out_repair_3f3b.txt` →
  `cb9f282`, `out_repair_6df0.txt` → `3958b5a`.
* `git ls-tree -r --name-only <rev> -- code/ | grep -c '\.py$'` at nine revs. Relevant values:
  `89d6aa1`=495, `4a06b4c`=495, `7dc9180`=495, `cb9f282`=496, `a91cf9e`=496, `1e30484`=496,
  `3958b5a`=481, `HEAD`(`fba5f63`)=503.
* `cat` of the parent's `README.md`, `out_anchor_132a.txt`, `run_all.sh`, and a `grep` of function
  names in `anchor_132a.py`. **I have not read the body of `anchor_132a.py`.**

So the arithmetic below (495 published, 496 in the post-merge publishing tree) was already in hand.
What is genuinely predicted is **what the parent's code does with it** — which row fires, whether it
is red, and the exit code — since I have not read the code that decides.

## The headline prediction

`out_anchor_132a.txt` publishes **495** and declares its anchor as `89d6aa1` (which holds 495). Its
publishing commit *after the merge* is `1e30484`, which holds **496**. Under the parent's own
lattice that is `DISPLACED`, not `AGREES`.

But row `A3a` of the committed transcript asserts, in words:

> `A3a THIS INSTRUMENT'S OWN TRANSCRIPT reads AGREES under the rule it ships`

**P1. `A3a` goes red when the parent is re-run after the rebase.** The predecessor's transcript said
`0 STALE` while being stale, 2 of 2. I predict the repair's transcript says `AGREES` while being
`DISPLACED`, **2 of 2** — `out_anchor_132a.txt` and `out_repair_3f3b.txt`, the two the committed
transcript records as `AGREES`.

**And I predict this is a self-assertion failure, not a lattice failure.** `DISPLACED` is green by
the parent's own decision, so the verdict machinery survives the rebase intact and returns the
correct answer; what does not survive is the sentence the deliverable wrote *about* that answer.
If that is what I find, the correct verdict on the repair is **it holds**, with a stale row — not
**it repeats its predecessor's defect**. I am writing that distinction down now so I cannot
retro-fit whichever result is more dramatic.

## Exit codes, every one predicted before it is observed

| # | invocation | predicted | why |
|---|---|---|---|
| E1 | `python3 anchor_132a.py --at 4a06b4c` (the rev it was committed at) | **0** | reproduces the committed transcript; 18 checks, 0 refuted |
| E2 | `python3 anchor_132a.py --at HEAD` | **1** | `A3a` asserts `AGREES`; at HEAD its own transcript is `DISPLACED` |
| E3 | `python3 anchor_132a.py --at 1e30484` (the commit that publishes its transcript after merge) | **1** | same row, same reason |
| E4 | `python3 anchor_132a.py --at cb9f282` (post-merge publishing commit of `out_repair_3f3b.txt`) | **1** | `out_anchor_132a.txt` does not exist yet at `cb9f282`; I predict `A3a` goes red on absence rather than on displacement — a *different* route to the same red |
| E5 | `python3 repair_7e39.py` (the repaired mg-3f3b suite) at HEAD | **0** | README says `S4a` is keyed on the anchor and reports `DISPLACED`, which is green |
| E6 | `c1_rebase.py` — re-run the parent after the rebase | **0** | my controls are about *observing* the parent, and I expect them all to hold |
| E7 | `c2_anchors.py` — independent re-derivation of every anchor | **0** | |
| E8 | `c3_shopping.py` — the case answer (1) handles | **0** | the constructed transcript is expected to read `AGREES`, which is the finding, not a refutation of my control |
| E9 | `c4_independence.py` — redundancy by failure mode | **0** | |
| E10 | `c5_vocab.py` — the word for the merge | **0** | |
| E11 | `selftest_c067.py` — my own tooling checked for the defect I am auditing | **0** | |
| E12 | `sh run_all.sh` | **1** | it aggregates; E2's red is inside it |

Where a prediction misses, **the miss is kept as written** and the observation recorded beside it.

## The primary target: measuring commit vs publishing commit

The parent took **answer (2)** — the anchor is the commit a figure was *measured* at.

**P2. The case answer (1) handles and (2) does not is ANCHOR SHOPPING, and I predict the
deliverable does not name it.** Under (1) the examiner is fixed: `git log -1` picks the tree, and the
publication step cannot choose it. Under (2) **the publication step names its own examiner.** A
transcript publishing a figure that is wrong for the tree it was actually measured at reads `AGREES`
so long as its declared anchor points at *any* commit whose tree happens to hold that number — and
the parent's own `A2h` measures that such commits are plentiful (3 of 396 share one population
digest, because a commit adding no `.py` file leaves the population untouched).

I predict:
* a constructed transcript publishing 481 with a declared anchor naming a commit that holds 481,
  committed at a rev whose tree holds something else, reads **`AGREES`** — green;
* the parent's README's *"The price, stated rather than hidden"* section covers **displacement**
  (a true figure that lost currency) and **does not** cover **substitution** (a figure whose anchor
  was chosen to fit);
* `A2c` does not close this: `A2c` catches a declared anchor whose tree does **not** hold the
  figure. Anchor shopping is the case where it **does**.

If the deliverable turns out to say this plainly somewhere I have not read, that is a miss and I
keep it.

**P3. The measuring commit's tree does yield the figure, for every anchor the parent records.** The
parent claims `A2c` re-derives rather than believes. I predict this survives independent
re-derivation by my own `git ls-tree` count, which shares no code with theirs — 3 of 3 declared or
inferred anchors resolve and hold their published figure.

## The staleness check re-run AFTER a rebase

**P4. The rebase has already happened and nobody re-ran anything.** mg-132a's five commits exist
twice: `d24bbeb 7dc9180 89d6aa1 4a06b4c 2cfd226` (pre-rebase, alive only on `polecat-132a`) and
`53f6ca3 aa8309d cb9f282 a91cf9e 1e30484` (post-rebase, on `main`). The committed transcript was
written at `4a06b4c` and has not been regenerated at `1e30484`. **The audit-after-rebase the parent
says is one command has not been run once since the merge that made it necessary.**

**P5. The parent's own A1d exposure now applies to the parent.** `A1d` measures that the two legacy
anchors are verified-but-unreachable and die at the next `git gc`. I predict `89d6aa1` and
`7dc9180` — mg-132a's *own* anchors — are now in exactly that state, reachable only from
`polecat-132a`, and that the count of not-reachable anchors goes **1 → 3**.

## My own choice — the thing no list in the ticket names

**P6. I audit whether the advertised remedy works on the repair's own figure.** `A2d` sells the
digest as the answer to the strongest objection against (2): a pruned anchor recovers because some
other tree holds the same population. The legacy figures have no digest, which the parent names as
an unfixed exposure. **mg-132a's own transcript *does* carry a digest** (`2e41577f5263fbfb`) — so it
is the first figure in this repository for which the remedy can actually be tested.

I predict: **the digest recovers, and recovers to a commit that is itself unreachable from HEAD.**
Every commit holding the 495-file population is an mg-132a-era commit, and the rebase moved all of
them off the mainline; the post-merge tree holds 496. If that is right, the digest buys back
*verifiability against the object store* but not *reachability*, and `A2d`'s claim that "the figure
survives its own anchor" is true only while `polecat-132a` exists — the same fragile condition
`A2i` reports for the legacy figures, one level up. **Predicted: 0 commits reachable from HEAD hold
digest `2e41577f5263fbfb`.**

Second unnamed thing: **P7. `--at <rev>` reads the transcripts FROM GIT at that rev, not from the
working tree.** If it read the working tree for any of them, a post-merge audit would not be
auditing the merge. I predict it reads from git (the committed transcript's `A3` section says "read
FROM GIT at its own publishing commit") and that this survives a constructed working-tree
perturbation: I will corrupt a transcript on disk, re-run `--at`, and confirm the verdict is
unchanged.

## Redundancy, specified by independence of failure mode

The parent has three routes to an anchor: **DECLARED** (the `POPULATION ANCHOR:` line), **INFERRED**
(resolving hex tokens in the transcript's own text), **RECOVERED** (digest search). For each I
construct the input that breaks it and check the others survive.

**P8. DECLARED and RECOVERED are NOT independent — they are one line, written by one code path.**
The declared sha and the digest that is supposed to buy it back live in the same
`POPULATION ANCHOR:` line. Delete or mangle that line and **both** routes die together. The only
surviving route is INFERRED, which the parent's own `A1e` says "selects for agreement and therefore
cannot witness `WRONG WHEN WRITTEN`". So under the common-mode failure of a dropped anchor line, the
remaining redundancy is the route the parent itself calls structurally weaker. I predict this is
real and unnamed.

Predicted verdicts for the four constructions, on a copy of `out_anchor_132a.txt`:

| construction | predicted verdict |
|---|---|
| anchor line deleted, body hex intact | `AGREES` or `DISPLACED` via **INFERRED** — degraded, not red |
| anchor sha mangled, digest intact | `AGREES` via **RECOVERED** |
| anchor sha intact, digest mangled | `AGREES` via **DECLARED** |
| whole anchor line deleted **and** body hex stripped | **`UNANCHORED`** — red, fails closed |

## Checking my own tooling for the defect I am repairing

**P9. My own transcripts must declare their anchor and must not be readable as live.** `selftest_c067.py`
asserts that every `out_*.txt` this instrument writes carries a `POPULATION ANCHOR:` line with a
resolvable commit and a re-derivable count, and a banner saying it is a measurement at a commit.
I predict my first draft fails at least one of these before it passes — and if it does, the failure
is recorded here rather than quietly fixed.

**P10. And my own instrument will be stale the moment it merges,** for exactly the reason the parent
documents: the refinery will rebase these files onto a tree that has grown, so the population figure
in my own transcript will be displaced by my own merge. I predict my committed transcript's anchor
will hold my published count and its post-merge publishing commit will not. **I am not claiming to
have closed this.** I am claiming to have named it before it happened, and `selftest_c067.py` prints
the one command that re-checks it.
