# mg-585e — PRE-REGISTERED PREDICTIONS

Written and committed **before any arm in this directory existed**, so that what the run says
can be compared against what was expected rather than against a memory of what was expected.

---

## §0  WHAT WAS ALREADY MEASURED BEFORE THIS FILE WAS WRITTEN — these are NOT predictions

Honesty about the order of operations, because a "prediction" of something already run is a
record of nothing.  While scoping the ticket I ran three `git log` / `git show` sweeps over
`code/gate_fixed_point_f771/out_g0_fixed_point.txt` by hand.  What they said:

| S | what was already known before this file was written |
|---|---|
| S1 | 31 commits have touched that file.  15 of them carry a **RED** §2 (`THE DISAGREEMENTS, SHOWN`). |
| S2 | Every GREEN version is 1908 bytes except the two earliest, which pre-date the `VERDICT:` line. |
| S3 | 7 of the 31 commits touch **that file and nothing else** — they exist only to close the oscillation. |

`v1_oscillation.py` re-takes all three as an instrument rather than by hand, which is the
point of building it; but it must not be read as having *predicted* them.  Everything below
this line was unrun when the line was written.

---

### §0a  AND TWO OF THE THREE WERE WRONG — SCORED AFTER THE INSTRUMENT RAN

Appended after `v1_oscillation.py` re-took them.  Kept as originally written above rather than
corrected in place, because the point of §0 is the hand sweep and not the answer.

- **S1 was WRONG BY ONE.** The hand sweep counted **15** RED versions; the instrument counts
  **16** over the same 31 commits.  A hand tally of a `git show` loop is exactly the kind of
  figure that is right until it is not, and nothing about the sweep announced the miscount.
- **S2 WAS RIGHT IN THE WRONG UNIT.** `1908` is *characters*; the transcript is `1922` **bytes**
  — the em-dashes.  The shape of the claim ("one text, plus two pre-`VERDICT:` ancestors")
  stands, and `v1` §4 prints three distinct sizes, `1728, 1771, 1922`.
- **S3 stands unchanged at 7.**

---

## §1  PREDICTIONS

**P1 — the oscillation is confined to §2 and the VERDICT line.**  Run the *real* `g0` on two
sandbox trees that differ only in whether one watched transcript disagrees; the two stdouts
will be byte-identical from the header through the end of §1, and differ from the `§2`
heading onward.  *Risk: §1 prints the exemption list and nothing else that could move, so the
prediction is that nothing ELSE leaks — the `changed` set is computed before §1 is printed and
could in principle be referenced there.*

**P2 — run-to-run jitter on a fixed tree is decimal seconds and nothing else.**  Two runs of
`g0` against the same green sandbox differ only in the `%.2fs` field.

**P3 — a verdict-invariant transcript exists and is exhibited.**  A writer that emits the
verdict's *inputs* (watched-class rule, exemption list, normaliser rule inventory, digest of
the deciding functions) produces **byte-identical** output on the red tree and the green tree.

**P4 — and it is not vacuous.**  That output is *not* a constant: mutate the normaliser's
source in a sandbox and the output moves.  So un-exempting the file buys something rather than
buying a file that can never disagree.  *This is the prediction most likely to be wrong in the
interesting direction — if the only invariant content is constant text, candidate 1 in the
ticket is answerable "yes, and pointlessly".*

**P5 — nothing is lost, it changes channel.**  On the red tree the proposed arrangement still
exits 1 and still names the disagreeing files, on stderr and in the exit status, exactly where
the `NOISE`/`moved` counts already go.

**P6 — swapping the oscillation for a census would be a bad trade, and by a measurable
margin.**  The other obvious invariant content is a *count* of watched transcripts.  It is
invariant under the repair, so it would not oscillate — but it moves on every commit that adds
or removes an `out_*.txt`, which is most landings on this arc, and that is `mg-05c6`'s conflict
class.  Predicted: over the history the file has existed, **the number of commits that moved
the watched-class membership is at least half the number that moved the verdict** — i.e. the
census trade buys little and pays into a class that conflicts in the merge queue instead of
oscillating in a worktree.

**P7 — this branch will pay the toll it is describing.**  Landing this directory adds files
under `code/`, so `./build.sh` will find committed transcripts that disagree, `g0` will write
a RED `out_g0_fixed_point.txt`, and a **second** `./build.sh` run and a **second commit** will
be needed to turn it green.  The 32nd commit to that file will be RED and the 33rd will be a
`refresh:`.

**P8 — the exemption's stated reason is narrower than the true one.**  `lib_f771.SELF_EXCLUDED`
gives the reason as "its text depends on the verdict".  Predicted finding: the operative
property is *reporting a quantity that the repair sets to zero*, and "depends on the verdict"
is a symptom of it.  Predicted consequence: `g0`'s own docstring rule — "only the DISAGREES
list, which is repo state, is on stdout" — is the mistake, because the repo state it is a
function of is the tree **before** the repair and the file is committed into the tree
**after**.

---

## §2  OUTCOMES — scored after `sh run_all.sh`, and P7 after `./build.sh`

| P | outcome | where |
|---|---|---|
| P1 | **CONFIRMED** — head identical (24 lines), `§2` onward 7 lines green vs 18 red | `v2` §3 |
| P2 | **CONFIRMED, AND IT BIT THIS DIRECTORY** — see below | `v2` §2 |
| P3 | **CONFIRMED** — 1745 bytes, byte-identical on red / green / noise, no scrubbing needed | `v3` §1 |
| P4 | **CONFIRMED** — the report moves under a widened `N2`, one legible line | `v3` §2 |
| P5 | **CONFIRMED** — exit 1, and stderr already names the disagreeing transcript | `v3` §3 |
| P6 | **CONFIRMED, AND UNDERSTATED** — see below | `v3` §4 |
| P7 | *pending — scored in the landing commit, after `./build.sh` runs on the committed tree* | commit history of this branch |
| P8 | **CONFIRMED** — *is it repo state* is the wrong test; *does the repair move it* is the right one | `v2` §4 |

**P2 was confirmed the expensive way.**  The prediction was about `g0`'s jitter.  It turned out
to be true of **this directory's own `v2` transcript**: its first draft printed `g0`'s verdict
line verbatim, so `out_v2_partition.txt` failed to reproduce across two runs (`0.03s` → `0.04s`)
and the raw-identity row flipped with the rounding.  That is mg-f771's README D4 happening
inside the directory quoting README D4, and it was caught by running the suite twice, not by
reading it.  Remedy: D4's own — scrub before printing, and put the raw-identity result on
stderr.  README §7.

**P6 predicted "at least half" and the measurement is 31 against 30**, on a window of 129
commits, with an overlap of **4**.  So a census would move about as often as the verdict does,
on a nearly disjoint set of commits — the trade buys nothing and pays into `mg-05c6`'s conflict
class.  ⚠ The 31 and the 30 are different quantities and their near-equality is arithmetic.

**One prediction is missing and its absence is the honest part.**  Nothing above predicted that
`D1` — the plant guarding the digest — would come back **INERT** on its first run because
`"def verdict_for"` is a prefix of `def verdict_for_RENAMED(`.  It did.  The matcher was
tightened rather than the plant relaxed (README §7), and a plant that fires on its author's own
construction is the only evidence that the plants are doing anything.
