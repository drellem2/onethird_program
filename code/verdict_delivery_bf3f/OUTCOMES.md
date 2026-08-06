# mg-bf3f — predictions scored

Sixteen predictions were committed in `PREDICTIONS.md` at 7cb7a18, before any
script of this instrument existed. Scored here against the committed
transcripts. **Misses are kept as written.** Five are refuted, and two of the
five are refuted by repairs I made to my own instrument after predicting against
its first form — which is recorded rather than tidied away.

| | prediction | outcome |
|---|---|---|
| P1 | drops > 11, and in 35–45 | **REFUTED** |
| P2 | 0 of 21 hand-verified deliveries reported dropped | HOLDS |
| P3 | ≥1 other filer with drops; daniel ≥ 20 | HOLDS (with a correction) |
| P4 | UNDECIDABLE bucket is exactly 4 | **REFUTED by my own repair** |
| P5 | hermetic matched pair reports exactly 1 and exactly 0 | HOLDS |
| P6 | the first form fails ≥1 edge case; (c) breaks first | HOLDS on the claim, **REFUTED on the named case** |
| P7 | quiet while claimed, fires once landed with no mail | HOLDS |
| P8 | H-REAP refuted for the mail channel | HOLDS |
| P9 | H-REAP confirmed for `--result`; ≥95% refinery sidecars | HOLDS on the claim, **REFUTED on the number** |
| P10 | Fisher exact p < 1e-5 | HOLDS |
| P11 | ≥3 of 7 instruction-absent deliveries from a never-asked worker | HOLDS |
| P12 | pm-onethird's framing corrected, not confirmed | HOLDS |
| P13 | mg-ec63 recoverable in < 6 commits | HOLDS |
| P14 | ≥1 more item joins the dropped list during this ticket | **REFUTED** |
| P15 | ≥2 defects of this instrument found and recorded | HOLDS (6) |
| P16 | this ticket's own verdict is scheduled to be lost | HOLDS |
| — | six declared exit codes | 6 of 6 on prediction |

---

## The five that were refuted

**P1 — drops in 35–45. Measured: 122.**
The "more than eleven" half held decisively. The RANGE was badly wrong, and the
reason is worth stating because it is the same error pm-onethird made: I anchored
on the population I had been *looking at* — the last two evenings — and predicted
a number for it while writing a predicate that ranges over everything
pm-onethird has ever filed. The ticket says eleven because eleven is what was
noticed. I said forty because forty is what I had read. The predicate says 122.

**P4 — UNDECIDABLE is exactly 4. Measured: 2.**
This held exactly, for the instrument's first form, and was then refuted by my
own repair. Two of the four undecidables (mg-9a19, mg-65eb) were items I had
personally hand-verified as DELIVERED in M3 — the sidecar-only worker resolver
could not see their workers, so the instrument was filing known deliveries under
"cannot tell". That is the same silence this ticket is about, in the detector for
it. DEFECT-2 adds a second resolver and the bucket drops to 2. Scored REFUTED
because the number I published moved; the repair is the reason and it is a good
one.

**P6 — the first form fails an edge case, and (c) breaks first.**
The first form was indeed broken, so the claim holds. But it broke on **(b)**,
not (c), and it broke in the worst available way: `mail()` read the MSG-ID by
scanning for a dotted token, `mg mail send` prints a *path*
(`filer-a/new/1786…`), the scan matched nothing and returned `None`, and the
P6b construction then **skipped its own setup and asserted DELIVERED against a
verdict that had never been archived**. A vacuous pass — this arc's signature
shape — inside the file whose entire job is to prove the detector is not
vacuous. (c), which I named as most likely, passed first time. The setup is now
verified by an assertion rather than reported by a `print`.

**P9 — ≥95% refinery-written sidecars. Measured: 93% (139 of 149).**
The claim it was testing is intact and the mechanism is confirmed; the threshold
I picked was simply too tight. Kept as a miss rather than restated at 90%.

**P14 — the population moves under my own hand.**
Three tickets in this arc were refuted by exactly this trap, so I filed it in
advance, and it did not fire. The store moved a great deal while I worked —
items on disk 2321 → 2336, pm-onethird's filed count 184 → 191 — but the LANDED
population stayed at 149 throughout, so no new row joined the dropped list. The
trap is real and visible in the filed count; my prediction named the wrong
counter.

## The one that is stronger than predicted

**P11** predicted ≥3 of 7. It is **7 of 7**: every instruction-absent item that
was delivered anyway was worked by an agent that had never seen the instruction
on any ticket. That weakens my own headline and is reported for that reason —
ticket text is a very strong predictor of delivery, and it is not the whole
mechanism.

## Predictions I most wanted to keep, and did

**P2** was named in `PREDICTIONS.md` as "the prediction I least want to lose".
The 21-item control list was established by hand outside the repository before
any of this code existed and pasted into `d1_population.py` as a literal, so it
is an independent list and not something the instrument derived from itself.
0 of 21 are reported as dropped.

**P16** — that this ticket's own verdict was scheduled to be lost — is confirmed
in `out_d4_live_BEFOREMAIL_DROPPED.txt`, a transcript taken on the live store
before the verdict mail existed, in which the detector reports `mg-bf3f` DROPPED.
The verdict mail was then sent and `out_d4_live.txt` records the same live row
reading DELIVERED. Both states of one row, neither inferred from the other.
