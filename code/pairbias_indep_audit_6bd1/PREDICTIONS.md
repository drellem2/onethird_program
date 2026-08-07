# mg-6bd1 — PREDICTIONS for the INDEPENDENT AUDIT of mg-345e

Committed **before any script of this audit exists** and **before one line of
`docs/OneThird-PairBias-Independence-mg-345e.md` or of `code/pairbias_independence_345e/*`
has been read**, per this program's pre-registration convention.

The target is mg-345e, landed at `550a7f105c30273b06d376a60d720cd61b652499`
(2026-08-07 14:12:08 +0100).

---

## 0. THE SHA I NAME, AND WHY IT IS TWO SHAS

The dispatch note told me STATE.md was at commit `491d42c79f7628c18cb7a5d197faa9f4600cd6c1`
and warned it may have moved. It has **not** moved as a *blob*. Measured before writing
any prediction:

    git rev-parse 491d42c:STATE.md  ->  7f73bfc87b4bc4caab6c836f8c3922a2416863cf
    git rev-parse 65866c2:STATE.md  ->  7f73bfc87b4bc4caab6c836f8c3922a2416863cf   (HEAD)

`491d42c` is still the most recent commit touching STATE.md; six commits have landed since
without touching it. So **the file I read is blob `7f73bfc87b4bc4caab6c836f8c3922a2416863cf`,
reachable from HEAD `65866c2037ccebba0f6d880ec6be55b4927b3261` and identical to the object
the dispatch named.** I name the blob and not only the commit because the commit SHA is the
thing that rots when a *different* file is edited; the blob SHA is the thing that identifies
what I actually read. mg-a83c, queued to rewrite STATE.md, had not landed as of HEAD.

## 1. HAND MEASUREMENTS ALREADY IN MY HAND — DISCLOSED, NOT LAUNDERED INTO PREDICTIONS

Anything below is something I already know at prediction time. It is disclosed here so that
a later reader cannot mistake a reproduction for a hit.

- **H1. mg-345e's verdict is (A) INDEPENDENT.** I read it off the commit subject of
  `550a7f1`, which is printed verbatim in my own dispatch prompt's git log. Any "prediction"
  that the verdict is INDEPENDENT would be a formality. I do **not** file one.
- **H2. The same subject says "AND THE GATE IT NAMES IS WRONG TWICE".** So mg-345e did not
  stop at the independence question; it made at least two further claims about mg-6bc2's
  gate. That is precisely the region where a scope conflation would live, and it is where I
  will look first.
- **H3. A downstream ticket already alleges an mg-345e error.** mg-6bc2's own predictions
  commit (`515b9d8`, 18:21) records its H5 as "a supply-side 1/6 already in the corpus at
  mg-c4f5:415 that mg-345e's 'occurs twice, none supply-side' missed on both counts". I have
  **not** verified this and it is not my finding; I will check it myself. If I confirm it,
  it is a *reproduction* of mg-6bc2's observation, and I will say so.
- **H4. mg-94c3's audit (`c80a4f1`, 20:11) states "the dependence is on L4's THRESHOLD,
  which mg-345e permits, not its MODULUS".** So mg-345e's document draws a threshold/modulus
  distinction and at least one other landed document already leans on it. That makes the
  distinction load-bearing beyond mg-345e itself.
- **H5. Shape of the deliverable, from `git show --stat` only:** STATE.md +5/-2;
  `docs/OneThird-PairBias-Independence-mg-345e.md` 373 lines new; three instruments
  (`p1_ledger_depgraph.py`, `p2_architecture_graph.py`, `p3_algebra.py`), a `lib345e.py`, a
  selftest, and four `out_*.txt`. The names tell me p1 walks a claim ledger's dependency
  graph and p2 walks an architecture graph — i.e. mg-345e's independence argument is at
  least partly a **graph reachability** claim over a citation structure. That is exactly the
  kind of argument that is right by NAME and wrong one level down.
- **H6. mg-345e pre-registered its own most-likely error** (`755676a`) as P8: "conflating
  'an eps_spec that is CONSTANT' with 'an eps_spec that SUFFICES'". A pre-registered error is
  not a defence; I will check whether it committed it anyway.
- **H7. Chronology.** mg-345e landed 14:12. mg-131e's refutation of `eps_spec = 2/(n+1)` at
  n=6 landed 19:50, and mg-b488 put it on STATE.md at 20:06 — **5h38m after mg-345e**. So if
  mg-345e prints `2/(n+1)` as live, that is not a defect of mg-345e; it could not have known.
  I will still say where I saw it, per the dispatch note.
- **H8. The ticket body of mg-345e already contains the trap warning verbatim** ("That
  answers a CONSUMPTION question about Step 6. It does NOT answer whether L4-as-stated is
  provable at an n-free modulus... pm-onethird conflated them once already"). So mg-345e was
  *told*. A conflation committed after that warning is worse, not better; and an author that
  was warned is also more likely to have guarded correctly.

## 2. PREDICTIONS

Scored HELD / MISSED / VOID after the work, with the measurement that decided each.

**On the dependency re-derivation (trap 1 — the load-bearing direction):**

- **P1.** mg-345e's exhibited dependency list names mg-92e6's diagonal-capacity bound
  (position-matrix / marginal machinery) as an input. — *p = 0.85*
- **P2.** mg-345e's dependency list names the per-element bias `b_x` and a
  Diaconis–Graham footrule conversion as inputs. — *p = 0.8*
- **P3. THE VERDICT SURVIVES MY RE-DERIVATION.** Walking one level down from every named
  input, **no** input is itself conditional on L4-as-stated. I.e. the INDEPENDENT verdict is
  correct, not merely independent-by-citation. — *p = 0.60*. I file this at only 0.60
  deliberately: the audit exists because the other 0.40 is expensive, and I would rather be
  scored MISSED than have written 0.9 to look confident.
- **P4.** At least one input on the list is conditional on **something**, just not on L4 —
  most likely on L2, on the mg-200d conjecture, or on a calibration (mg-3ce3's `eps <= 0.20`
  sweep) rather than a derivation. If mg-345e's document does **not** flag that conditional,
  that is a finding of its own even though it does not overturn INDEPENDENT. — *p = 0.7*
- **P5.** mg-345e's independence argument routes at least partly through a **graph
  reachability** computation over citations (from H5's file names), and therefore its
  strength depends on whether the graph's edges were extracted by *reading the arguments* or
  by *grepping for identifiers*. I predict the edges are extracted from text/identifier
  markers, i.e. the instrument can only see dependence-by-NAME. — *p = 0.65*. If HELD, the
  instrument is structurally incapable of catching the trap this audit was filed to catch,
  and my hand walk is the only thing that can.

**On the scope conflation (trap 3 — the BROKEN condition):**

- **P6. THE MAIN HAZARD.** One of the two "the gate is wrong" claims in mg-345e's subject is
  built on mg-3af9 — specifically arguing that because mg-3af9 kills every positive modulus
  for Step 6's transfer on L4 branch (ii), the gate's *first* disjunct ("until L4's modulus
  question has an answer") is discharged or moot. That is the CONSUMPTION→PROVABILITY
  conflation and would make mg-345e **BROKEN**. — *p = 0.45*
- **P7.** mg-345e explicitly *names* the consumption/provability distinction somewhere in its
  document (having been warned in its own ticket body). — *p = 0.75*
- **P8.** P6 and P7 are **not** mutually exclusive, and I predict the most likely single
  outcome is: it names the distinction correctly in the body **and** its compressed commit
  subject / STATE.md line does not carry the qualifier. That is the failure mode this
  lineage produced at mg-94c3 (conditional at the claim, absent from the commit subject) and
  at mg-76b2 (currency named in §6, absent from the title). — *p = 0.5*

**On the "1/6" census and the arithmetic:**

- **P9.** mg-345e's document contains a claim of the form "1/6 occurs N times in the corpus"
  with N small. Given H3, I predict I will find at least one occurrence it missed, and that
  at least one missed occurrence is supply-side. — *p = 0.7*. HELD here is a **reproduction**
  of mg-6bc2's H5, not an independent discovery, and will be reported that way.
- **P10.** `eps_spec = 2/(n+1)` appears in mg-345e's deliverable or in the STATE.md lines it
  wrote, presented as live. Per H7 this is *not* chargeable to mg-345e. — *p = 0.5*
- **P11.** Every numeric figure printed by mg-345e's three instruments reproduces on my own
  code, written from the document rather than from `lib345e.py`. — *p = 0.7*
- **P12.** mg-345e's STATE.md +5/-2 edit is still present, byte-for-byte, in blob
  `7f73bfc8` despite the three STATE.md rewrites since. — *p = 0.6*

**On the (C) branch (trap 4):** VOID in advance — H1 tells me the verdict is (A), so trap 4
does not fire. I record it as VOID rather than silently dropping it.

**On trap 2 (DEPENDENT-is-a-convenience):** VOID in advance for the same reason. It is the
mirror check and does not apply to an (A) verdict. I keep the *spirit* of it live as P14.

## 3. MY TWO MOST LIKELY ERRORS, FILED IN ADVANCE

- **P13. I score mg-345e BROKEN on a compression.** I read a commit subject or a STATE.md
  one-liner, find the qualifier missing, and report the *document* as having committed the
  conflation when the document's body scopes it correctly. This is exactly P8's shape turned
  against me. **Binding guard, written before I can be tempted:** any BROKEN or CORRECTION
  verdict I issue must quote the offending sentence **byte-for-byte with its file and line**,
  and must separately state whether the same defect is present in the document body, in the
  STATE.md line, and in the commit subject — three columns, not one. A defect present only in
  the subject is reported as a *labelling* finding and may not be called BROKEN.
- **P14. I manufacture a dependency out of a citation.** Walking "one level down" as the
  ticket demands, I reach L4 through some document that merely *mentions* L4 for context or
  cites a lemma whose *statement* is L4-free but whose *paper* discusses L4, and I call that
  a real dependency — overturning INDEPENDENT on a convenience. That is trap 2's error
  committed in the opposite direction, and it is the expensive one here because it re-blocks
  Daniel's ask. **Binding guard:** to call any input L4-dependent I must exhibit the
  *inequality or step* that fails if L4 is withdrawn — naming the document is not enough.

## 4. WHAT I AM COMMITTING TO NOT DOING

- I will not attempt L4.
- I will not attempt the eps_spec derivation itself (mg-6bc2's job).
- I will not reconcile my model against mg-345e's. If my re-derivation disagrees, the
  disagreement is the deliverable.
