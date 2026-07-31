# mg-69d1 — predictions, registered before the runs

Kept as written. A miss is more informative than a hit, so the misses stay with
what was wrong beside them.

## Exit codes

| script | predicted | actual |
|---|---|---|
| `selftest_69d1.py` | 0 | 0 |
| `p1_bound.py` | 0 | 0 — **after two misses, below** |
| `p2_rerun.py` | 0 | 0 — **after two misses, below** |
| `p3_reason.py` | 0 | 0 — **after one miss, below** |
| `p4_kinds.py` | 0 | 0 |
| `run_all.sh` (worst) | 0 | 0 |

`p2` is predicted **0** even though it reports `d2_deletion.py` exiting **1**.
That is deliberate: `p2`'s gate is *the E8 claim is the only broken one*, not
*d2 is green*. A script that required d2 to exit 0 would be requiring this
repair to close mg-eaef's E8, which is not this ticket.

## OPEN 1 — the bound and the classification

| claim | predicted | actual |
|---|---|---|
| explicit boolean operands in `face_complex.py` | 15 | 15 — HIT |
| of those, at the top level of their condition (the sweep's population) | 11 | 11 — HIT |
| of those, nested under a comprehension or quantifier | 4 | 4 — HIT |
| explicit boolean operands in `posets.py` | 2 | 2 — HIT |
| in the `swept` column | 11 | 11 — HIT |
| in `not determined` | 0 | 0 — HIT |
| the 4 nested operands, deleted one at a time: artifact | **CHANGES ×4** | CHANGES ×4 — HIT |
| the pre-repair pair of columns at `bfd7948`, operands in neither | 4 | 4 — HIT |
| deleting the `not swept: nested` column: the totality claim | **goes red** | goes red — HIT |
| `d2_deletion.py` claims scored, before | 49 | 49 — HIT |
| `d2_deletion.py` claims scored, after two are added | 51 | 51 — HIT |
| `d2_deletion.py` BROKEN claims at HEAD | 1 (E8's pin claim) | 1, and it is that claim — HIT |

The four `CHANGES` predictions are **not** foresight: mg-eaef measured them
first and its own registered prediction was `BYTE-IDENTICAL` on all four. This
row re-derives that audit's measurement and the prediction is copied from its
result. Said here rather than presented as insight.

### Misses in `p1`, kept

1. **The grep parser read the wrong output shape.** `git grep -n <needle>` over
   the working tree prints `path:lineno:text`; `git grep -n <needle> HEAD`
   prints `rev:path:lineno:text`. The parser was written for the second and
   applied to the first, so every site printed a **line number where the path
   should be** and `p1` booked a finding naming 7 sites that did not exist.
   The parser now drops the revision only when one was asked for.
   *Why it matters:* the finding it produced was still, by luck, in the right
   direction — the bound really was still wide at that moment — and a check
   that is right for the wrong reason is the class of defect this ticket is
   about.

2. **The quotation discriminator was first a PATH LIST.** It exempted
   `d2_deletion.py`, `face_complex.py` and `run_all.sh` — which are the three
   files the wide sentence was **live** in. The check would have been vacuous
   by construction: it could not have gone red for the defect it was written
   to catch. Replaced by a proximity test (a correcting marker within 25 lines,
   in the same file), which `p3 (i-b)` then demonstrates is non-vacuous by
   running it unchanged against `HEAD` and getting 4 live assertions.

## OPEN 2 — the row, the reason, and the two pairs

| input | c1 half | kern half | `both together` |
|---|---|---|---|
| **cancelling** — kern's `dim L(n,p)` +1, c1's dims −1 | MOVED | MOVED | **IDENTICAL** |
| **conspiring** — kern gains a name, c1 reads it with default 0 | IDENTICAL | IDENTICAL | **MOVED** |

Both rows predicted exactly as written, both HIT. The cancelling row is
mg-e34a's measurement re-derived on a pair built again here; the conspiring row
is **new** — nothing in mg-76cc and nothing in mg-e34a ever built one, and
without it "the row is load-bearing" is an assertion.

| claim | predicted | actual |
|---|---|---|
| section (v) as a whole catches the cancelling pair | at 2 of 3 rows | 2 of 3 — HIT |
| section (v) as a whole catches the conspiring pair | at 1 of 3 rows | 1 of 3 — HIT |
| `g1_provenance.py` exit code after the repair | 0 | 0 — HIT |
| `k4_cancel.py`'s three rows, unchanged by this repair | MOVED / MOVED / IDENTICAL | same — HIT |
| `k4_cancel.py` still books its rationale finding | yes | yes — HIT |

### Miss in `p3`, kept

3. **The staleness check on `g1`'s own stdout was a bare substring test.**
   `g1` still prints the inverted sentence — inside the paragraph that corrects
   it — and the first version of `p2 (ii)` read that as a relapse and booked a
   finding. It is the same substitution the two open sites are about: a check
   aimed at the *string* when the property is about the *claim*. It now applies
   the same proximity discriminator `p3 (i)` uses, to the artifact rather than
   to the tree.

### Miss #4, and it is the largest one — kept

4. **Regenerating ONE transcript of a five-transcript set broke a property that
   lives BETWEEN them.** `out_g1_provenance.txt` was regenerated on its own,
   because it is the only one of `mg-58da`'s five that this repair changes.
   `mg-76cc`'s `r2_reproduce.py` measures a **set-level** property: all five
   must name **one** HEAD revision, so a single normalisation explains every
   differing line. With g1 at `e494515b` and the other four still at
   `e006581c`, the normalisation covered `5 of 9` differing lines instead of
   `9 of 9`, `r2` went to **3 findings**, and `r4_doccheck.py` then booked the
   document's `9 of 9` as a figure appearing in no transcript — one edit, two
   instruments red, neither of them the one being repaired.

   Fixed by regenerating all five with `mg-58da`'s **own** `run_all.sh`, and
   `mg-76cc`'s suite re-run afterwards.

   **This is the ticket's own lesson landing on the ticket.** *Committed
   transcript* looked like one kind of artifact and behaved like a **set**;
   enumerating the kinds is not enough if a kind's members carry an invariant
   between them. `p4 (i)`'s transcript row now says so.

## What is NOT predicted here, because it is not measured here

* Whether the narrowed bound is the **narrowest** true one. It is narrower than
  the sentence it replaces and it matches the sweep operand-for-operand; a
  seventh rung — a decision in no condition at all, which mg-eaef's E3
  demonstrated — is outside every column in this table, and the `expression
  nodes in all` total is where it is counted.
* Whether the `both together` row catches **every** conspiring pair. One was
  built. That is a demonstration, not a proof, and `p4 (iii)` states it.
