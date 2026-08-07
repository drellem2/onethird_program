# mg-eba7 — OUTCOMES against `PREDICTIONS.md` (committed at `e5b89c2`)

Full verdict: [`docs/state-history/audit-mg-eba7-of-mg-55f2.md`](../../docs/state-history/audit-mg-eba7-of-mg-55f2.md).

There is **no instrument in this directory** and that is deliberate — this audit is
documentary end to end. Everything below is reproducible with `git grep`, `git
show`, `sed` and `md5`; the commands are named at each row so a reader can re-run
any single line without re-running an audit.

## Version audited

`STATE.md` blob `7f73bfc87b4bc4caab6c836f8c3922a2416863cf`, identical at
`491d42c79f7628c18cb7a5d197faa9f4600cd6c1` (the dispatch SHA) and at
`dafe75910f731927affdf366457d681e262acf62` (`main` HEAD). Parent landing:
`276aead`. Pre-state: `276aead^` = `f8bd3ae`.

## Score: 8 held, 6 refuted, 1 split

| id | prediction | conf | outcome | how to re-check |
|---|---|---|---|---|
| P1 | ≥3 pre-state `0/132` sites, ≥2 outside row 3b | 80% | **HELD** (14 occ / 6 files) | `git grep -c -F 0/132 276aead^` |
| P2 | escaped *phrase* in both `.md` and `.html` pre-state | 70% | **REFUTED** — `STATE.md` only | `git grep -c -i -F 'clean sweep' 276aead^ -- docs/state-of-the-wall.html` → 0 |
| P3 | 0 live "clean sweep" in either file today | 75% | **HELD** | `git grep -n -i -F 'clean sweep' dafe759` |
| P4 | ≥1 surviving `0/132` outside the two ledger files | 45% | **HELD** (5 files) | `git grep -c -F 0/132 dafe759` |
| P4b | ≥1 of those is a **defect** by the §2 criterion | 30% | **REFUTED in the declared frame** (0 in this repo); held only in `one_third_width_three` | §1.4 of the verdict |
| P5 | `166` absent from `STATE.md` pre-state → relocation is real | 55% | **HELD** — 0 → 5 | `git grep -c -E '(^\|[^0-9])166([^0-9]\|$)' 276aead^ -- STATE.md` |
| P6 | `FP✗` marked **without** read-not-measured — *my most likely finding* | 40% | **REFUTED** — written out 4× | `git show dafe759:STATE.md \| sed -n 110p` |
| P7 | row states (a) REFUTED, 166, mg-8b64 | 85% | **HELD** | row 3b |
| P8 | row states (b) conditional OPEN and **is** L1b | 80% | **HELD** | row 3b, `:5`, `:13`, `:76` |
| P9 | refutation overstated — kills L1b | 20% | **REFUTED** — row defends L1b via the δ argument | row 3b |
| P10 | no width ≥ 3 row landed | 88% | **HELD** — rows 1–11 + 3a/3b, no `Linial` | `grep -n Linial` on `dafe759:STATE.md` |
| P11 | phrase survives as a **use** in a commit message | 50% | **REFUTED** — only as self-description | `git log --all --grep='clean sweep' -i` |
| P12 | row 3b disturbed by mg-9adf / mg-b488 | 35% | **REFUTED** — 6/6 lines md5-identical | md5 of lines 5,13,76,95,110,117 at `276aead` vs `dafe759` |
| P13 | a third ledger-carrying file exists | 30% | **REFUTED** — one `.html` tracked | `git ls-tree -r --name-only dafe759 \| grep '\.html$'` |
| P14 | mg-5998 unlanded **and** the Sah check lost in the handover | 60% | **SPLIT** — unlanded **yes**; check **NOT** lost (`mg-8d4b` carries it verbatim in its title) | `mg show mg-5998`, `mg list \| grep 5998` |

## The guards did their job

**E1 — "I score a source document as an escaped figure."** Filed at 30%-ish weight
before the grep ran, with a written criterion: a site counts only if the figure is
*used as evidence* **and** the frame is absent nearby. Four sites tripped the grep
and would have been scored by a looser reading:

- `docs/roadmap.md:669` — quotes the struck phrase *in order to record that it
  escaped*. Mention, not use.
- `KillShot-Probe.md:286` — the source, stating its own measurement, with the frame
  **inside the metric name**. Exempt by construction.
- `ComparisonRoute.md:110–111` — quotes the figure in order to refute its transfer
  to the BK reading. Mention, not use.
- `audit-mg-2eed-of-mg-b488.md` — a *later* ticket inheriting the evidence bound
  unprompted. Evidence the repair took, not a leak.

Scoring those four would have produced a RED against a correct parent. The
criterion was bound in writing first, which is the only reason it didn't.

**E2 — "I score a mark as laundering without reading what the mark means here."**
I read the ledger's own `Kinds` legend at `dafe759:STATE.md:88–97` before scoring
P6, and quoted it in the verdict: `FP✗` = *"a finite population exhibiting a
counterexample"*, **silent on held-vs-read**. So the mark genuinely cannot encode
U-by-citation and the bound must be written out per site — which is exactly what
mg-55f2 did, at 4 of 5 sites. The one gap (`STATE.md:5`) is reported as a minor
finding rather than as laundering, because the row itself — where the reader of row
3b actually meets the figure — carries the bound twice.

**E3 — "I conflate the parent's output with today's file."** Handled by measuring
everything at three points (`276aead^`, `276aead`, `dafe759`) rather than two. It
turned out to matter in the harmless direction: nothing moved, and P12 is refuted
*because* I checked instead of assuming.

## The one finding my declared frame did not cover

`one_third_width_three/docs/OneThird-StandardDominance-ComparisonRoute.md:104`
quotes `0/132` **bare**, in a live status table, with the status cell reading
*"Empirically supported"*. My frame was this repo; I ran the sibling repo anyway
because row 3b links into it. It is **not** mg-55f2's to fix — different repo,
outside its ticket — and it is **not** a claim that SD-Cayley is refuted. It is the
part of the finding that still has no carrier. See §1.4.
