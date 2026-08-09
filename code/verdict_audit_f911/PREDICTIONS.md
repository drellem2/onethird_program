# mg-f911 — PRE-REGISTERED PREDICTIONS

INDEPENDENT AUDIT of mg-bf3f's verdict-delivery detector.

Committed **before one byte of `code/verdict_delivery_bf3f/` is read** and before
any detector is run. Eighteen files exist in that directory (10 evidence/doc, 8
code); I have their **names and line counts only**, from `git show --stat`.

Everything I already knew is filed below as an EXPOSURE (H-item), not laundered
into a prediction. Every prediction is tagged `[BET]` (genuinely open when
written) or `[FORMALITY]` (already answered by an exposure; I am recording that I
will *reproduce* a stated claim, not that I predicted it).

---

## EXPOSURES — what I already had before predicting

**H1.** I read mg-bf3f's ticket body in full. It states the eleven, the
`done`-or-`archived` predicate, the two candidate causes, and "the eleven are the
first deliverable".

**H2 — THE LARGE ONE.** My first search returned mg-bf3f's **three commit
subjects in full**, and this arc writes essay-length subjects. They already state:

- a matched pair on a throwaway `MG_ROOT` through the real `mg` binary, arm A's
  verdict deliberately unmailed and arm B's sent, "exactly 1 and exactly 0";
- a mutation test killing always-DELIVERED (8 constructions) and always-DROPPED (5);
- the count is **122, not 11**, over **149 landed** tickets;
- the cause is discriminated: mayor's reap is REAL (`requested`, 0–1 s after
  landing, 122/122) but the **same distribution holds in the delivered group** and
  every delivered verdict was sent *before* that window, so the reap cannot be the
  suppressor; nine dropped items carry positive proof of liveness (10–73 min);
- the real cause is **instruction drift, not compliance drift**: the ask appears in
  16 of 191 filed items, last 2026-07-31T10:02Z, 0 of the 55 filed since; present →
  14 delivered / 0 dropped, absent → 7 of 45; Fisher exact p = 8.7e-09;
- the `mg done --result` half is reap-shaped and was **routed to mayor**, not fixed;
- P16 was filed in advance that mg-bf3f's **own** verdict was scheduled to be lost,
  and both states of its live row are committed
  (`out_d4_live_BEFOREMAIL_DROPPED.txt` vs `out_d4_live.txt`);
- five/six self-declared defects, the worst a **vacuously passing control** (P6b:
  a msg-id scan returned `None` because `mg mail send` prints a path, so the
  construction skipped its own setup);
- the 21-delivery false-positive control was **hand-verified outside the repo and
  pasted in as a literal**.

**This pre-answers brief items 1, 2 and 4 almost completely.** My checks on those
are therefore REPRODUCTIONS — I mark them `[FORMALITY]`, and the only honest way
to make them evidence is to build my own positive and negative controls rather
than re-read the parent's. That is what section C does.

**H3.** I read `~/.macguffin/work/done/mg-bf3f.result.json`. It is
`{"branch":"polecat-dbf3f","completed_by":"refinery","mr":"mr-d9qhms2tjv1h244d85m0","target":"main"}`
— **no `verdict` key**. The parent's own sidecar carries no verdict.

**H4.** My own dispatch prompt carries a retrofit `== VERDICT ROUTING ==` block
from pm-onethird quoting "122 of 149" and "every worker that was ASKED delivered
(14 of 14)". So the parent's headline numbers were handed to me by the filer
*before* I started, and pm-onethird has already acted on the finding.

**H5.** `mg list` shows pm-onethird tickets `mg-d075` ("mg-19ec verdict RECOVERED
from commit messages"), `mg-a74f` ("DROPPED VERDICT mg-16eb"), `mg-6df0`
("mg-ec07 verdict repairs … NEVER ROUTED TO ME"), and several `*-followup`
"verdict repairs" items. So *some* recovery exists in the mg store, **filed by
pm-onethird by hand and predating mg-bf3f in at least one case**. Whether mg-bf3f
recovered anything is still open.

**H6.** `ls ~/.macguffin/work/` → `archive available claimed done pending shelved`.
The archived directory is spelled **`archive`**, singular, not `archived`.

**H7.** The three commits appear twice in `git log --all` with identical subjects
(f1683d4/609cf31, e5f22d5/977da36, 73e229c/7cb7a18) — a rebase, standard here.
Only one lineage is on `main`; I have read neither.

**H8.** mg-bf3f's status is `done`. Its brief demanded "state what you did not do",
and I have not yet seen whether it did.

---

## DEFECT CRITERION — bound in advance, so it cannot be tuned afterwards

- **DEFECT**: the detector misses a real drop, reports a drop that was not one, or
  the deliverable asserts something that is false. I.e. it changes what a reader
  would believe or do.
- **NOTE**: correct but incomplete, *where the deliverable itself says so*. Scoped
  work is not a defect. (This guard exists because two prior audits in this arc
  scored correct-but-scoped mathematics as defects.)
- **CORRECTION**: a place where my own brief, or pm-onethird's framing, is wrong.
  I owe these regardless of how the parent scored.

A count I print is only a finding if it **moved** relative to the parent's, or is
explicitly labelled **FORCED** with the thing that forced it named.

---

## A. THE DETECTOR ITSELF

**P1 [BET, 0.85]** `verdictwatch.py` runs today against the live store without
editing and exits non-zero.

**P2 [BET, 0.45] — PRINCIPAL LIVE BET, brief item 5, the `archived` case.**
I predict the population code enumerates **`work/done/` only** and does **not**
read `work/archive/`, so an item that reached `archived` is invisible to it.
Grounds: (a) the parent's own self-declared sixth defect is a *glob* bug in this
exact code (`*.md` missing the `.md.PID` in-flight form), so the enumeration is
hand-written and has already been wrong once; (b) the directory is spelled
`archive`, not `archived` (H6), which is exactly the kind of mismatch a
`done`-shaped predicate written from the ticket's wording produces; (c) none of
the three commit subjects mentions `archived` or `mg-c3ca` even once, while they
mention almost everything else at length.
- **Refuted if** the enumeration reads `archive/` (or is status-independent, e.g.
  driven off `events.jsonl` or the sidecars rather than directory membership).
- **Sub-bet P2a [BET, 0.40]**: `mg-c3ca` appears nowhere in the parent's output files.

**P3 [BET, 0.70] — brief item 6, "does not depend on me".**
`verdictwatch.py` is a script somebody must remember to run: no `pogo schedule`
entry, no cron, no pogod hook exists that runs it. It therefore still depends on
pm-onethird's habit — the same mechanism it replaces, one level up.
- **Refuted if** `pogo schedule list` shows an entry that runs it, or a merged
  hook/crew-agent duty invokes it.
- **Guard**: a *documented* duty in a crew agent's prompt counts as not depending
  on pm-onethird only if the duty is on someone else. I will check who.

**P4 [BET, 0.60]** The detector's filer-resolution has at least one class it
cannot resolve and silently drops or mislabels: items whose creator is `human`/
`daniel`, or self-filed items where filer == worker. H2 discloses a
`daniel: 999 = CREATOR UNKNOWN` row, so *that* one is [FORMALITY]; the bet is that
there is a **second** such class.

## B. THE NUMBERS

**P5 [BET, 0.75]** My own independent implementation of the predicate, written
without reading the parent's, lands within ±10 of the parent's 122 on the landed
population, but **not exactly on 122**, because the population has moved since
2026-08-07. Any count I publish will be dated and labelled.

**P6 [BET, 0.55]** The landed population is **larger** than 149 today.

**P7 [FORMALITY]** The Fisher p, the 16-of-191, the 14/14 — reproductions of H2,
not predictions. I will recompute them anyway; agreement is not evidence of
independence and I will not present it as such.

## C. MY OWN CONTROLS (brief items 1 and 2) — the only part that is not a reproduction

**P8 [BET, 0.80]** I can force the detector to fire on a **throwaway `MG_ROOT`**
driven through the real `mg` binary: item → claim → `done`, no verdict mail, and
it reports exactly that item. FORCED, and I will say so.

**P9 [BET, 0.80]** The matched negative — same store, same shape, verdict mailed
to the filer — is **not** reported. FORCED.

**P10 [BET, 0.35]** The negative arm is the fragile one. I predict I can find at
least one **realistic** shape that the detector calls DROPPED although the verdict
did arrive: e.g. mail sent to the work-item box (`mg-XXXX`) rather than the filer
name, mail sent from a differently-named agent, or a verdict carried in
`--result` rather than mail. Over-reporting is the failure mode the brief says
retires the detector in a week.

**P11 [BET, 0.30]** The converse: a shape the detector calls DELIVERED on mail
that is not a verdict at all — any mail from worker to filer counts. If so the
122 is a **lower** bound on drops and the 27 delivered is an upper bound on
deliveries.

## D. THE ELEVEN (brief item 3) — recovered, not counted

**P12 [BET, 0.65]** The parent's deliverable is a **census**, and fewer than 11 of
the eleven have an actual recovered verdict *body* in it. I expect ids, timings
and a cause analysis, and I expect the recovery half to be the part that was
scoped out.
- **Refuted if** ≥11 recovered verdict bodies exist in the parent's files.
- **Partial credit is not credit**: a commit-subject quotation *is* recovered
  content and counts; a row saying "recoverable from commit subjects" does not.

**P13 [BET, 0.55]** mg-ec63 specifically — the one the ticket names as most
important, the 86-of-109 truncated-transcript finding — has **no** recovered
verdict body in the parent's deliverable.

**P14 [BET, 0.50]** The "eleven" are not enumerated as eleven anywhere in the
parent's output: the parent replaced the number with 122 and the specific eleven
pm-onethird named were not tracked as a named set. If so that is a **defect
against the brief's first deliverable**, not against the mathematics.

## E. THE DELIVERABLE'S OWN DEFECT CLASS (standing target)

**P15 [FORMALITY→BET, 0.50]** H3 shows mg-bf3f's sidecar carries no verdict. Its
commit subject claims a live mail was sent (`out_d4_live.txt` reads DELIVERED
after one mail). So the parent's verdict survives **only** in mail + commit
subjects, and its `mg done --result` is exactly the loss it documented. The open
half — my bet — is whether **anything a future reader will actually open** carries
it. I predict the mail exists (0.85) and the sidecar never gets it (0.95).

**P16 [BET, 0.60]** This audit, mg-f911, will itself be at risk: I will mail my
verdict to pm-onethird *before* submit (my dispatch tells me to, and H2's own
finding is that being ASKED is what works — 14/14). I predict my `--verdict-file`
sidecar **will** land too, because pogod's `--verdict-file` path was fixed under
mg-dfea. If both land, that is one data point that the repair works; if the
sidecar is empty, mg-dfea's fix is not live and that is a finding.

---

## MY OWN MOST LIKELY ERRORS — filed in advance

**E1 (most likely).** I score P2 (`archive/` not covered) as a defect when the
population is actually resolved status-independently — from `events.jsonl`, from
the refinery, or from the `.result.json` sidecars, all of which survive an
archive move. **Guard: I must read the enumeration code and name the exact line
before scoring P2, and I must construct an archived item and see what happens.**

**E2.** I score "the eleven were not recovered" when the recovery lives somewhere
I did not look — pm-onethird's own follow-up tickets (H5), `OUTCOMES.md`,
`README.md`, or mail. **Guard: search the mg store, the mail store and the repo
before scoring P12–P14, and count a recovery wherever it lives, crediting mg-bf3f
only for what mg-bf3f produced but reporting the rest as CORRECTION to my brief.**

**E3.** I build my own predicate with a different filer-resolution or a different
"landed" definition than the parent's, get a different number, and call the
difference a defect when my rule is the wrong one. **Guard: any disagreement gets
diffed item-by-item and attributed to a named rule difference before it is scored.**

**E4.** I treat a control the parent already ran as my own evidence. **Guard:
sections C's controls must be written by me and run by me; if I end up running
the parent's script instead, the row says REPRODUCTION.**

**E5.** I pollute the live `~/.macguffin` store with a forced positive control.
**Guard: forced controls run on a throwaway `MG_ROOT` under my scratchpad. The
only live-store write I will make is my own item's normal lifecycle.**

---

## WHAT I AM COMMITTING TO STATE AT THE END

- every count, with its date and whether it moved or was FORCED;
- corrections to pm-onethird's framing **and to my own brief's**;
- what I did not do.
