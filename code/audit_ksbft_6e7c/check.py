"""check.py (audit mg-6e7c): assert every figure AUDIT-mg-6e7c.md relies on, from the transcripts.  Exit 1 otherwise."""
import re, sys
bad = []
def tot(files):
    agg = {}
    for f in files:
        for line in open(f):
            if line.startswith("file "):
                for k, v in re.findall(r"(\w+)=(\d+)", line):
                    agg[k] = agg.get(k, 0) + int(v)
    return agg
def need(tag, cond):
    print(("ok   " if cond else "FAIL ") + tag)
    if not cond: bad.append(tag)
s = tot(["out_census_small.txt"]); p9 = tot(["out_census_p9a.txt", "out_census_p9b.txt"])
r = tot(["out_census_records.txt"]); d4 = tot(["out_census_d4_9.txt"])
for name, c in (("n<=8", s), ("n=9", p9), ("records", r), ("d4_9", d4)):
    need(f"{name}: theorem checks STEP/SLV/DBL/EQV/PINCH/CPRE all 0", all(c.get(k, 0) == 0 for k in ("STEP", "SLV", "DBL", "EQV", "PINCH", "CPRE")))
    need(f"{name}: controls CH1, CWIN, CDBL fire", all(c[k] > 0 for k in ("CH1", "CWIN", "CDBL")))
    need(f"{name}: SL fires == NESTBAL == posets", c["SL"] == c["NESTBAL"] == c["posets"])
need("n<=8 controls CPINCH, CCPRE fire", s["CPINCH"] > 0 and s["CCPRE"] > 0)
need("n<=8: 14099 posets, GOOD 14094, STRUCT 14094", (s["posets"], s["GOOD"], s["STRUCT"]) == (14099, 14094, 14094))
need("n=9: 146468 posets, GOOD misses 114, STRUCT misses 138", (p9["posets"], p9["posets"] - p9["GOOD"], p9["posets"] - p9["STRUCT"]) == (146468, 114, 138))
need("records: 2534, GOOD misses 21", (r["posets"], r["posets"] - r["GOOD"]) == (2534, 21))
need("d4_9: 4327, STRUCT misses 0", (d4["posets"], d4["STRUCT"]) == (4327, 4327))
rng9 = {}
for f in ("out_census_p9a.txt", "out_census_p9b.txt"):
    for line in open(f):
        m = re.match(r"\s+STRUCT_FAILS: \d+ by range \{(.*)\}", line)
        if m:
            for k, v in re.findall(r"(\d+): (\d+)", m.group(1)):
                rng9[int(k)] = rng9.get(int(k), 0) + int(v)
need("n=9 STRUCT misses by range {5:46,6:86,7:5,8:1}", rng9 == {5: 46, 6: 86, 7: 5, 8: 1})
g = open("out_gencheck.txt").read()
need("generator complete+dup-free n<=9 (A001035)", "RESULT OK" in g and g.count(" OK") >= 9)
need("witnesses all match", "RESULT ALL MATCH" in open("out_witnesses.txt").read())
w = open("out_witnesses.txt").read()
need("B7 + tail r=3 loses (2,5) (doc 'survives any tail' refuted)", "tail r=3 m=20: range=6 conn=True WIN_bot=holds  (2, 4)=0.6627* (2, 5)=0.7206 " in w)
need("release-time lemma 10750/0, control 4072", "elements=10750 violations=0 control_violations=4072 OK" in open("out_release.txt").read())
need("twin-pair balance differs P vs R on 95 gadget pairs", "differs between P and R: 95" in open("out_reduction.txt").read())
print("RESULT", "ALL CHECKS PASS" if not bad else f"FAILED {bad}")
sys.exit(1 if bad else 0)
