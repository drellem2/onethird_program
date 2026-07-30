"""Regenerate spec.CHECKS from the CURRENT STATE.md.  Only ever run against the
pre-restructure file; the guards exist so that a change to cells.split_passages cannot
silently re-map passage keys onto different text."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cells import split_row, split_passages
from spec import SPEC

lines = open(sys.argv[1] if len(sys.argv) > 1 else "STATE.md", encoding="utf-8").read().split("\n")
out = {}
for lineno, sp in sorted(SPEC.items()):
    P = {}
    for ci, cell in enumerate(split_row(lines[lineno - 1])):
        if not cell.strip():
            continue
        for pi, p in enumerate(split_passages(cell)):
            P[f"{ci}.{pi}"] = p
    keys = sorted(set(sp["history"] + sp["support"] + [k for k, _, _ in sp["inserts"]]),
                  key=lambda k: tuple(int(x) for x in k.split(".")))
    out[lineno] = {k: P[k].strip()[:44] for k in keys}
print(json.dumps(out, ensure_ascii=False, indent=1))
