# mg-97fb — predictions, written BEFORE any script of this instrument exists

Committed before `audit_97fb.py` exists in this tree and before any transcript of it exists.
`git log --follow` on this file and on `audit_97fb.py` is the check; `S6a`'s shape, re-derived.

**What I had read when these were written.** The *source* of `verify_landing.py`,
`repair_ec07.py` and `repair_7e39.py`; the committed transcripts `out_audit_7e39.txt` and
`out_repair_3f3b.txt`; both READMEs. I had run **no probe** — no mutation, no subprocess run of
the gate, no sweep, no `git ls-tree`. Every number below is a prediction from reading code, and
the ones I got wrong are kept as written.

The audited object: mg-3f3b's repair of mg-7e39's four findings, landed at `4785086`
(`docs+repair: mg-7e39's FOUR FINDINGS LANDED`) and completed through `75333b2`. My tree is at
`dfa263c`.

---

## P0 — preflight

- **P0a** `verify_landing.py` on the unmutated tree at HEAD: **exit 0**.
- **P0b** my own runner `sh code/hodge_leverage_audit_97fb/run_all.sh`: **exit 0**.
- **P0c** my instrument's own `.py` file joins the population it counts. The `.py` count under
  `code/` in my working tree will be **1 more** than at `dfa263c` once `audit_97fb.py` exists.

## P1 — the matrix, from the gate's own stdout

- **P1a** 36 cells in the product (12 kinds × 3 sites), **29 FIRES, 0 SILENT, 7 n/a**.
- **P1b** counted **from the cells**, not by `l.count("FIRES")` over the printed line. I predict
  the two methods agree at HEAD (no kind title contains `FIRES`, `SILENT` or `n/a`) — so the
  substring census is *wrong in construction and right in value*, which is the only reason it has
  never been noticed.

## P2 — every `n/a` read as a claim, and the case it says is impossible CONSTRUCTED

Seven cells. For each I write a mutation **of the same kind, from the KIND TITLE**, apply it to
**the file on disk**, and run the gate as a subprocess.

- **P2a** **7 of 7 survive.** 0 failures. I predict the repair did not leave an `n/a` that is a
  fact about the derivation.
- **P2b** The riskiest two are `K10 @ H8` and `K10 @ the STATE.md row`. "Marked quotation" is a
  *declared convention* — `QUOTE_PATTERNS` is `*"…"*` and `*'…'*` only. Ordinary `"…"`, a
  markdown blockquote, backticks and `**bold**` are not quotations to this gate. **I predict I
  will find at least one quotation-shaped span at at least one of those two sites that
  `quoted_spans` does not recognise and that carries a `FIGURE_TOKEN`** — and I predict that
  altering that token **FIRES**, but through the **assertion** half (`FIGURE CENSUS` /
  `FIGURE ORDER`), not through the record's segment half, **because a span the gate does not
  treat as a quotation is a span `partition` treats as an assertion.** That is a fire of kind
  K01, not of kind K10, so **the K10 `n/a` still stands** — and the boundary is named rather
  than left as "no such text here".
- **P2c** `K08 @ the STATE.md row` survives, and its *reason* is measured on the wrong
  population: `_table_lines` counts the header line and the `|---|` **delimiter** as table rows,
  so "1 of this site's **3** table row(s) carry a figure" is 1 of 3 lines where the site holds
  exactly **one data row**. True sentence, checkable count, denominator that is not rows.
- **P2d** `K08 @ §14`, `K09 @ §14`, `K11 @ §14` survive **iff §14 really holds no table**. The
  three derivations that decline there each key on a different recogniser (`_table_lines`,
  `_header_line`, `k_layout`'s pipe clause, which requires `l.startswith("| ")` — with the
  space). I predict §14 holds **0 pipe rows and 0 whitespace-column rows** and all three survive.
  If §14 holds a pipe row indented by even one space, all three are facts about the derivation.
- **P2e** `K12 @ the STATE.md row` survives: the site is 3 lines with no blank line, so it is one
  paragraph, and relocating the only paragraph changes the site's line count, which
  `splice_framed_row` refuses.

## P3 — the `n/a` that was DELETED, and whether it was replaced by an untested FIRE

- **P3a** Exactly **1** cell moved from `n/a` to a FIRE between the pre-repair and post-repair
  matrix: `K11 @ the STATE.md row`, now `FIRES (rec)`.
- **P3b** My own alignment shift, written from the kind title *"the table's ALIGNMENT shifted, no
  figure moved"* and applied **on disk**: **exit 1**, at least one `SITE RECORD` row refuted,
  **0** `FIGURE CENSUS`/`FIGURE ORDER` rows refuted, and **0 figure tokens moved** (the token
  multiset of the site is identical before and after). The FIRE is real, not asserted.
- **P3c** **The same probe at `803bd50`, the pre-repair commit, ALSO fires (exit 1).** The gate
  never had this hole; only the matrix said there was nothing to catch. So F1 was a defect **of
  the matrix**, not of the gate — and any control that fires only at HEAD would be measuring my
  probe. I predict `1` cell moved and `0` cells moved from `n/a` to `SILENT`.

## P4 — FLOOR (the thing no list in the brief names): the fail-closed rule is `\d`

`kind_matrix` makes an `n/a` with no measurement in it RED. The test is
`re.search(r"\d", reason)` — **any digit anywhere in the sentence**.

- **P4a** A decline reason with **no measurement at all** but carrying a ticket id (`mg-ec07`,
  `mg-9207`, `K11`) **PASSES** the rule. Predicted: passes. The control that makes a decline
  carry its count is satisfiable by an id.
- **P4b** Demonstrated at **HEAD**, where the defect is present: I patch one `k_*` decline reason
  in a copy of the gate to a measurement-free sentence carrying `mg-ec07`, and predict the gate
  still records that row **CONFIRMED** — i.e. exit 0 on that row — where the same sentence
  without the id makes it **REFUTED**. Two runs, one differing by four characters.
- **P4c** SECOND FLOOR ITEM. `repair_ec07.py`'s `R3a` censuses the matrix with
  `sum(l.count("FIRES") for l in cells)` / `l.count("n/a")` / `l.count("SILENT")` over the whole
  printed line, **kind title included** — a substring test over a whole row, which is the
  construct this entire arc repairs, in the census of the very matrix whose `n/a` cells are the
  finding. I predict: renaming one kind title to contain the literal `n/a` moves the reported
  `n/a` count by **+1** with **no cell changing**. Demonstrated at HEAD.

## P5 — EXISTED / TOUCHED / LIVE, counted by me at each commit

My rule: AST over every `.py` under `code/` at the commit, a `Compare` whose op is `In` and whose
right side is a row-shaped name, keyed on a vocabulary **derived at that same commit**. Reported
per commit, never as a bare total, with the population named.

- **P5a** at `803bd50` (mg-6df0's parent, where mg-7e39 says **6 existed**): I predict **7**.
  mg-7e39's vocabulary was regexed out of the gate's `print` calls and could not see
  `WRITTEN ONCE`; mg-3f3b found a seventh occurrence (`audit_a318_repair.py`, `WRITTEN ONCE`)
  the moment the vocabulary came from the gate's declaration, and that occurrence is older than
  either repair.
- **P5b** at `77306a7` (mg-6df0 landed): **6 live**, not 5. mg-6df0 TOUCHED **1**.
- **P5c** at `4785086` (mg-3f3b's repair landed): **0 live**. mg-3f3b TOUCHED **6**.
- **P5d** at `dfa263c` (HEAD): **0 live** — but three deliverables have landed since
  (`mg-70c7`, `mg-19ec`, `mg-8d5e`) and nothing re-runs this sweep on merge, so a new occurrence
  would be live and unseen. If it is not 0, that is the finding.
- **P5e** **THE RECONCILIATION.** mg-7e39 says `1 of 6`; mg-3f3b's landing commit says `0 of 6`.
  I predict **neither denominator is the population**, and that they are not even the same 6:
  mg-7e39's 6 = (1 touched + 5 live) **at `803bd50`**, missing `WRITTEN ONCE`; mg-3f3b's 6 =
  what was **live when it started** (5 + the seventh), which is a different set from mg-7e39's 6
  and excludes the one mg-6df0 had already repaired. Predicted answer: **7 existed at
  `803bd50`; 1 touched by mg-6df0; 6 live at `77306a7`; 6 touched by mg-3f3b; 0 live at
  `4785086`.** Both numerators survive; **both denominators are wrong**, and they are wrong in
  opposite directions.

## P6 — the four that select 6 gate rows where 3 were meant, row by row

- **P6a** The gate returns **34** rows at HEAD.
- **P6b** For each of the four sites (`audit_8916_repair.py`, `audit_ec07.py`, `repair_ec07.py`,
  `repair_835f.py`): **6 by substring, 3 by heading**, 4 of 4.
- **P6c** The 3 extras for `'SITE RECORD'` are the three **`RECORD PARTITION`** rows, one per
  site, whose own explanation names `SITE RECORD`. For `'FIGURE CENSUS'` I predict the 3 extras
  are **also the three `RECORD PARTITION` rows** — lower confidence; the explanation that names
  the record's two halves is the same sentence.
- **P6d** Each extra is named individually, per site. No cell of this is reported as a total.

## P7 — the vocabulary, DERIVED rather than hand-listed

- **P7a** `ROW_NAMES` in `repair_ec07.py` is `row_vocabulary(read(LANDING_REL))`, which reads
  `ROW_KINDS` **by AST**. Declared = **7**.
- **P7b** **Derived vs hand:** the hand list mg-6df0 shipped is **5**; declared∖hand =
  `{READ AT THE SITE, WRITTEN ONCE}` — **2 names, not 1**. mg-7e39's regex-derived list was
  **6** and found **5 occurrences where the hand list found 4**; I predict the *declared* list
  finds **6 where the hand list finds 4** at `803bd50`.
- **P7c** **Derived from what the gate PRINTS:** I take the kind of every one of the gate's 34
  live rows from a subprocess run. Predicted: **6 distinct kinds printed**, `CENSUS ROSTER`
  declared and never printed, and **printed∖declared = 0** — the fail-closed direction holds.
- **P7d** CONTROL, at HEAD where nothing is wrong: remove one name from `ROW_KINDS` in a copy of
  the gate and the gate goes **exit 1** with the declared-vocabulary row REFUTED. A fail-closed
  rule that cannot be made to fail is a sentence.

## P8 — the population, recomputed at the publishing commit by me

- **P8a** `.py` under `code/` from `git ls-tree`: at `77306a7` = **448**; at `803bd50` = **448**;
  and `out_repair_6df0.txt` as committed at `77306a7` publishes **429**. Wrong when written, not
  drifted — **19** in the population and not in the number. Re-derived by me from `git ls-tree`,
  not quoted.
- **P8b** The figure is now **computed at publication**: `out_repair_6df0.txt` and
  `out_repair_3f3b.txt` each agree with the tree at their own publishing commit. Predicted
  **0 stale of 2**.
- **P8c** **AND THAT 2 IS A HAND LIST.** `COMPUTED` is two paths written out by hand and `PROSE`
  is four. That is F5's defect — a scope nobody chose — landed on F2's axis by the same
  deliverable that landed F5 on the vocabulary axis. I predict, sweeping the tree by the
  repair's **own** `POP_FIGURE` rule: **at least 3 committed transcripts** publish a `.py`
  population where `COMPUTED` names 2, and **at least 6 prose files** where `PROSE` names 4.
  Named in advance: `code/hodge_leverage_audit_7e39/out_audit_7e39.txt` is omitted from
  `COMPUTED`, and `docs/OneThird-Hodge-Side-Leverage-Mg6df0Repair-Audit.md` and
  `code/hodge_leverage_audit_7e39/README.md` are omitted from `PROSE`.
- **P8d** I predict at least one omitted file **would be flagged** if it were in the list — most
  likely under `S4b`, because the quotation exemption is keyed on `"…"` / `“…”` and this arc
  states its corrected figures in **bold** (`**429 `.py` files swept**`), which the exemption
  does not see. Lower confidence on which file.

## P9 — what must not be disturbed

- **P9a** Site cutters written from the **disclosure sentences** in `EXTENT_OF` rather than from
  the code reproduce the artifact's three sites **byte for byte, 3 of 3**.
- **P9b** The refusal probed **one row at a time**: `partition` bent lossy at one site only, then
  `--reseal` → **exit 1, REFUSED, record sha unchanged, 3 of 3** at HEAD; and the same probe at
  `803bd50` → **exit 0, BLESSED, record sha CHANGED, 3 of 3**.
- **P9c** **29 of 29** applicable cells fire, **0 silent**, scored by running the artifact as a
  **subprocess** and reading its stdout — nothing imported from it.

## P10 — my own instrument, checked for the shapes it audits

- **P10a** Every decline reason **this file** writes carries a count measured at the site:
  predicted **0** without one — and by a rule stronger than `\d`, since that is P4.
- **P10b** **0** lines of this file identify a gate row by a substring of the whole row outside
  one declared function.
- **P10c** Every population figure this deliverable publishes is **computed by the run** at a
  named commit and printed into the transcript. Its README points at the transcript line rather
  than carrying a number.

---

## The exit codes, all of them, predicted

| probe | predicted |
|---|---|
| gate at HEAD, unmutated | 0 |
| gate under my K11 pipe-padding shift, at HEAD | 1 |
| gate under the same shift, at `803bd50` | 1 |
| gate under each of my 7 `n/a` constructions | 1 where a construction exists, and I predict **0 constructions exist** — so: **not run, 7 of 7 declined by me too** |
| gate with one `ROW_KINDS` name removed | 1 |
| gate with a measurement-free decline reason **carrying `mg-ec07`** | 0 |
| gate with the same reason **without** the id | 1 |
| `--reseal` after `partition` bent at one site, HEAD | 1 (record unchanged) |
| `--reseal` after `partition` bent at one site, `803bd50` | 0 (record rewritten) |
| `sh run_all.sh` | 0 |

**Named in advance as the way this audit could be worse than the thing it audits:** every probe
here mutates files **on disk** and restores them. If a restore is not byte-identical I have
rewritten the artifact in the act of auditing it — the same failure mg-3f3b named for itself.
Every on-disk probe reports its own `restored byte-identical` flag, and a single False makes the
run RED.
