# `state_layer_audit_218d` — mg-218d's audit of mg-4acd / `e4426c9`

The full report is
[`docs/OneThird-STATE-Control-Presentation-mg4acd-IndependentAudit.md`](../../docs/OneThird-STATE-Control-Presentation-mg4acd-IndependentAudit.md).
This file is the directory guide.

**Headline.** The presentation record is correct and the layer it claims is closed —
verified against two real GFM renderers, **140 of 140** comparisons, including the M12/M13
reversal `COVERAGE.md` calls its own weak point and says is unverified. **The blind spot
moved.** Ten of sixteen mutations change what a reader is shown and exit 0, and the sharpest
is that mg-babf's B07 is caught by an accident of placement: the identical retraction
paragraph, moved **one line earlier across a heading**, exits 0.

```
sh code/state_layer_audit_218d/run_all.sh          # ~2 min
```

| file | what it is |
|---|---|
| `harness218d.py` | this audit's mutation harness — own snapshot/restore, own locator, own exit-code reader; shares no code with mg-2216's, mg-babf's or the control's |
| `layers218d.py` | the layer battery: 16 mutations at L0–L4, each carrying **the exit code this audit predicted before the run** |
| `render218d.py`, `render218d.js` | the presentation model against `marked` and `markdown-it` — the comparison `COVERAGE.md` says the next auditor should make |
| `coverage218d.py` | every mechanically checkable sentence of `COVERAGE.md`, against the code and the tree; 40 of 40 hold |
| `out_layers.txt`, `out_coverage.txt`, `out_render.txt` | committed runs of the three |
| `out_battery_babf_218d.txt`, `out_battery_2216_218d.txt` | mg-babf's and mg-2216's batteries re-run **unmodified** by this audit; both reproduce mg-4acd's reported figures |
| `run_all.sh` | all four sections |

**The renderers are not vendored and nothing in `code/state_landing_control_2da3/` depends
on them.** They are audit tooling only:

```
D=$(mktemp -d) && npm install --prefix "$D" marked markdown-it
NODE_PATH="$D/node_modules" sh code/state_layer_audit_218d/run_all.sh
```

Without them section 3 prints the install command and exits 3; sections 1, 2 and 4 are
unaffected and stand on their own.

**Safety.** Sections 1, 2 and 4 mutate tracked files in the working tree and restore them
under a `finally` plus a sha256 check. Each refuses to run on a dirty tree, because a crash
would then restore the wrong bytes.
