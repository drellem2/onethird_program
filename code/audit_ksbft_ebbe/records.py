"""records.py (audit mg-ebbe): mg-2912 records (code/ksbft_range_probe/out/*.jsonl, deduplicated as in
audit mg-6e7c): NB/PNB/DNB via ./aud, interval-order share, and the delta<0.35 subset.  Exit 1 on NB failure."""
import glob, json, subprocess, sys
from census import parse
from witnesses_lib import has_2p2
seen = {}
for f in sorted(glob.glob("../ksbft_range_probe/out/*.jsonl")):
    for line in open(f):
        d = json.loads(line)["rec"]["down"]
        if len(d) >= 3: seen[tuple(d)] = 1
pos = [" ".join([str(len(k))] + [format(m, "x") for m in k]) for k in seen]
out = subprocess.run(["./aud"], input="\n".join(pos) + "\n", capture_output=True, text=True).stdout.splitlines()
tot = io = low = lowio = fail = pfail = dfail = lowwidth2 = 0
for s, l in zip(pos, out):
    kv = dict(t.split("=") for t in l.split(" | ")[1].split()); e = int(kv["e"])
    if kv["chain"] == "1": continue
    tot += 1; i = not has_2p2(parse(s)); io += i
    fail += kv["NB"] != "1"; pfail += kv["PNB"] != "1"; dfail += kv["DNB"] != "1"
    if int(kv["d"]) / e < 0.35: low += 1; lowio += i
print(f"records: {len(pos)} distinct, {tot} non-chain; NB fails {fail}, PNB fails {pfail}, dual-PNB fails {dfail}")
print(f"interval orders: {io}/{tot}; delta<0.35: {low}, of which interval orders {lowio}")
sys.exit(1 if fail or len(out) != len(pos) else 0)
