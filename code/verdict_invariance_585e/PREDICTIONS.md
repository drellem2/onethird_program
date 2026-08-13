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
