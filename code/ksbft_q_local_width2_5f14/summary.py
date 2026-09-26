"""summary.py (mg-5f14): collate out_{all,d3,d4,d5,d6}.txt into the census table of
docs/KSBFT-Q-local-width2.md section 4, and assert the two PROVEN statements' checks are clean
(LL_VIOLATION and MONO_VIOLATION absent) while their firing controls in out_negctrl.txt fired."""
import re
import sys

rows = []
bad = []
for pop in ["all", "d3", "d4", "d5", "d6"]:
    try:
        txt = open("out_%s.txt" % pop).read()
    except FileNotFoundError:
        continue
    for blk in txt.split("== file ")[1:]:
        name = blk.split()[0].replace(".txt", "")
        agg = {}
        for m in re.finditer(r"^AGG (.*) (\d+)$", blk, re.M):
            agg[m.group(1)] = int(m.group(2))
        g = lambda k: agg.get(k, 0)
        if g("LL_VIOLATION") or g("MONO_VIOLATION") or g("NO_BALANCED_PAIR"):
            bad.append(name)
        rows.append((name, g("ALL"), g("LLq_any True"), g("LLq_bottom True"), g("LLs_any True"),
                     g("BR_either_end False"), g("BR_fail_has_isolated False"), g("WIN_either_end False"),
                     g("nmin>=3_balmin False")))
print("| population | indecomposable | LL fires, either end | LL fires, bottom | structural LL (Cor 2.3), either end | BR fails, both ends | ... of which no isolated element | WIN fails, both ends | >=3 minimal, no balanced minimal pair |")
print("|---|---|---|---|---|---|---|---|---|")
for r in rows:
    tot = r[1]
    pct = lambda v: "%d (%.1f%%)" % (v, 100.0 * v / tot) if tot else str(v)
    print("| %s | %d | %s | %s | %s | %d | %d | %d | %d |" % (r[0], tot, pct(r[2]), pct(r[3]), pct(r[4]), r[5], r[6], r[7], r[8]))
neg = open("out_negctrl.txt").read()
fired_ll = "AGG LL_VIOLATION" in neg
fired_mono = "AGG MONO_VIOLATION" in neg
print()
print("checks: LL/MONO/NO_BALANCED violations in", bad if bad else "no population (clean)")
print("firing controls: LL narrowed to [0.34,0.66] fires:", fired_ll, "; MONO on non-minimal elements fires:", fired_mono)
sys.exit(0 if (not bad and fired_ll and fired_mono) else 1)
