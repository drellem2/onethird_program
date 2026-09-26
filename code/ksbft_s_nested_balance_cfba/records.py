"""records.py (mg-cfba): on mg-2912's kept records (the low-delta extremal posets), how many have ANY
non-nested incomparable pair, and does delta = deltaN (price of nesting 0)?  NB itself was already checked
on these by audit mg-6e7c (0 failures); this re-runs it with nb.c as a consistency control."""
import glob, json, os
from fam import run, upmasks
here = os.path.dirname(os.path.abspath(__file__))
seen = {}
for f in sorted(glob.glob(os.path.join(here, "../ksbft_range_probe/out/*.jsonl"))):
    for line in open(f):
        rec = json.loads(line)["rec"]
        if len(rec["down"]) >= 3:
            seen[tuple(rec["down"])] = rec
dns = [list(d) for d in seen]
res = run(dns)
res_dns = [(d, r) for d, r in zip(dns, res) if r["nbal"] + (r["delta"] > 0) > 0 and r["delta"] > 0]
tot = len(res_dns)
withnon = sum(r["nnon"] > 0 for _, r in res_dns)
price = [r["delta"] - r["deltaN"] for _, r in res_dns]
low = [(d, r) for d, r in res_dns if r["delta"] < 0.36]
print(f"records (non-chain, n>=3): {tot}; NB failures {sum(r['flag'] != 'NB' for _, r in res_dns)}")
print(f"  with >=1 non-nested pair: {withnon}; price of nesting delta-deltaN > 0 on {sum(p > 1e-12 for p in price)}, max {max(price):.5f}")
print(f"  records with delta < 0.36: {len(low)}, of which with a non-nested pair: {sum(r['nnon'] > 0 for _, r in low)}, price>0: {sum(r['delta'] - r['deltaN'] > 1e-12 for _, r in low)}")
from fam import fmt, rng
worst = sorted(res_dns, key=lambda t: t[1]["deltaN"])[:6]
print("  smallest deltaN on the records:")
for d, r in worst:
    print(f"    n={r['n']} range={rng(d)} delta={r['delta']:.5f} deltaN={r['deltaN']:.5f} nnon={r['nnon']} | {fmt(d)}")
pr = sorted(res_dns, key=lambda t: t[1]["deltaN"] - t[1]["delta"])[:4]
print("  largest price of nesting on the records:")
for d, r in pr:
    print(f"    n={r['n']} range={rng(d)} delta={r['delta']:.5f} deltaN={r['deltaN']:.5f} nnon={r['nnon']} | {fmt(d)}")
pf = [(d, r) for d, r in res_dns if r["pflag"] != "PNB"]
print(f"  PRIMAL-only nested balance (down-set comparability only) fails on {len(pf)} records")
for d, r in pf[:5]:
    print(f"    n={r['n']} range={rng(d)} delta={r['delta']:.5f} deltaN={r['deltaN']:.5f} deltaP={r['deltaP']:.5f} | {fmt(d)}")
from io import StringIO  # noqa
import importlib.util
spec = importlib.util.spec_from_file_location("iochk", os.path.join(here, "io.py"))
src = open(os.path.join(here, "io.py")).read().split("P9 = parse")[0]
ns = {}; exec(src, ns)
io_all = [ns["has_2p2"](d) for d, _ in res_dns]
lowmask = [r["delta"] < 0.36 for _, r in res_dns]
print(f"  interval orders (no induced 2+2) among the records: {sum(not h for h in io_all)} / {len(io_all)}; "
      f"among records with delta < 0.36: {sum((not h) for h, l in zip(io_all, lowmask) if l)} / {sum(lowmask)}")
for thr in (0.34, 0.35, 0.37, 0.40):
    sel = [(h, r) for h, (_, r) in zip(io_all, res_dns) if r["delta"] < thr]
    print(f"    delta < {thr}: {len(sel)} records, {sum(not h for h, _ in sel)} interval orders")
