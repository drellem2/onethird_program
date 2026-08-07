# mg-c4f5 — PREDICTION OUTCOMES

Predictions committed at `1661c7f` before any script of this audit existed, and never amended.
**20 predictions. 6 REFUTED, 1 UNRESOLVED, 13 HIT (2 of them partially).** Every refuted
prediction is kept exactly as written in `PREDICTIONS.md`.

| # | prediction | outcome | measured |
|---|---|---|---|
| **P1** | premise holds; 0 violations of both master-bound forms `n ≤ 7`; equality at the antichain and nowhere else except degenerate `n ≤ 2` | **HIT / partial MISS** | 0 and 0 over 101 658 posets ✓. But there are **2** equality cases at *every* `n` — antichain **and chain** (`0 = 0`). My degenerate case was wrong. |
| **P2** | `λ_std` depends on the reference linear extension; witness at `n ≤ 6`; parent states it at 0 sites | **HIT** | 4 069 of 4 824 at `n = 6`; max spread **1/3**; parent: 0 sites |
| **P3** | 0 items filed against (LIB-weak) before mg-c3ca; ≥ 3 that state it without attacking | **HIT** | 0 title hits among the 4 pre-c3ca items; 4 mention it; 3 merged docs |
| **P3b** | mg-d112 did not separately audit the "never attacked" half (0 mentions) | **UNRESOLVED** | the audit document STATE.md names is **not locatable** in either repo — so this is unverifiable, not 0 |
| **P4** | §1's iff correct, 0 violations both directions; §3's table writes the negation too strongly | **HIT** | 0 and 0 over 4 α-values × 101 658 posets; `Ω(n)` vs "not `o(n)`" confirmed, consequence-free |
| **P5** | Prop 4.1: 0 violations; median looseness ratio `> 10³` at `n = 7` | **HIT / REFUTED** | 0 violations ✓. Median ratio **316**, not `> 10³`. **Ratio half REFUTED.** |
| **P6** | Prop 4.1 has an unstated but true step (all-pairs vs incomparable-pairs inversions) | **HIT** | confirmed; 0 consequence |
| **P7** | §4's Aires–Kahn conditional correctly flagged; no new finding | **HIT** | no new finding; I did not read the paper |
| **P8** | `C_p ⊔ A_q` gives `Θ(n)` elements of `Θ(n)` mass, `E_maj/n² ≥ 0.05`, `δ = 1/2` exactly | **HIT** | `E_maj/n² = 0.1146 … 0.1250` at `n = 4..14`; `δ = 1/2` at every size |
| **P9** | §3's supporting evidence is weaker than the negative, at the two named sites; verdict survives | **HIT** | width-3 transfer unlabelled ✓; "(B) fails via a few" is about a different statement ✓; verdict CONFIRMED ✓ |
| **P10** | 0 frozen posets at `n ≤ 7`; primitive min `δ` falls to `[0.340, 0.353]` at `n = 7` | **HIT / REFUTED** | 0 frozen ✓. Primitive min `δ` **RISES** to `14/39 = 0.3590`. **Value half REFUTED**, and in the direction opposite to the one I bet on. |
| **P11** | the `n = 7` value misses the four-point linear fit by **> 15%** | **REFUTED** | miss is **+13.4%**. The four published points themselves miss by up to 11.3%, so "`Θ(n)`-shaped" is still unsupported — but not by the margin I named. |
| **P12** | the "constant (~50) *rather than* a quantifier" relay sets two different gaps against each other | **HIT** | confirmed; both true, different pairs |
| **P13** | `~50` right, parent's `~5×10³` stale by 100×; **exactly 3** superseded figures | **HIT** | `2×10⁻⁴`, `5×10³`, `10⁵` — one occurrence each, lines 88/88/90 |
| **P14** | class chain false as stated about objects; parent states it without a rider at its own site; MINOR, 1 site | **HIT** | confirmed by construction; and stronger than predicted — **no `N₀` exists at all** |
| **P15** | **no drift** onto `Δ_AT`; ≤ 2 occurrences, confined to §7 | **HIT** | **1** occurrence, line 229, inside §7 "what I did not do"; non-vacuity control fires at 4 on STATE.md |
| **P16** | ≥ 1 printed count not reproducible as printed, first guess §5 or §6; ≥ 9 of 11 reproduce | **REFUTED / HIT** | **11 of 11** reproduce, and §5's counts reproduce too. **0 counts fail.** I guessed the location right (§5) and the mechanism wrong: what fails is the count's **label**, not the count. |
| **P17** | ≤ 2 unearned bound words; the one that fails is "never attacked by any arc" | **REFUTED** | "never attacked" **holds** (§3). The unearned word is **"is false"** in §0/§5 — not on my list at all. |
| **P18** | this instrument has ≥ 3 defects; ≥ 1 passes vacuously | **HIT / partial** | **5 defects**, recorded in `README.md` and left in the code. The closest to vacuous is defect 5 — a search capped at `10⁶` that **printed `None` as the answer** — which is a cap reported as a measurement rather than a check that passed vacuously. |
| **P19** | I will not re-derive Theorem E/G, the Cheeger sandwich, mg-88bd's backward derivation, L4, `ε_leak`; will not read Aires–Kahn or Ma–Shenfeld | **HIT** | all stated in §9 of the audit document |
| **P20** | my own most likely error: reading §3's verdict as a claim about **existence** when it is about **transfer** | **HIT (avoided)** | §8 separates verdict from support explicitly and confirms the verdict |

## Where being wrong changed the finding

**P10 is the one that mattered.** I predicted the primitive minimum `δ` would keep falling toward
`1/3`, because three descending points invite that reading. It **rose**. Had I not run `n = 7`, I
would have written that mg-c3ca's `0.400, 0.364, 0.357` supports a descent it does not support —
which is the same four-point-read error I criticise in §10 of the audit, made by the auditor.

**P16 and P17 together are the shape of the whole audit.** I expected to find a number that does
not reproduce, and I expected the over-claim to live in a familiar bound word. Neither happened.
Every number reproduces exactly and the bound words are ridered. The defect is in a **label** — a
predicate reported as a different predicate — which is not something a figure census or a
word-count can catch, and which I found only by re-deriving the statement instead of the number.
