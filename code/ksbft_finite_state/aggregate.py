#!/usr/bin/env python3
"""aggregate.py (mg-e8b4) -- sum the per-slice transcripts of a split run.

usage: aggregate.py SPLITDEPTH part_0.txt part_1.txt ...
Depths <= SPLITDEPTH are explored identically by every slice (the split
happens when a depth-SPLITDEPTH node creates its children), so they are
taken from one slice; deeper depths are summed.  Refuses to report a
verdict unless every slice printed RESULT TERMINATED-CLEAN and the slice
indices 0..M-1 are all present exactly once.
"""
import re, sys


def main():
    sd = int(sys.argv[1]); files = sys.argv[2:]
    rows = {}; top = {}; results = []; idx = []; M = None; lp = 0; maxlayer = 0; maxpairs = 0; cex = 0
    for f in files:
        txt = open(f).read()
        m = re.search(r"# split (\d+)/(\d+) at depth (\d+)", txt)
        assert m and int(m.group(3)) == sd, f
        idx.append(int(m.group(1))); M = int(m.group(2))
        r = re.search(r"RESULT (\S+) D=(\d+)", txt)
        results.append(r.group(1) if r else "NO-RESULT")
        D = int(r.group(2)) if r else None
        for line in txt.splitlines():
            t = line.split()
            if t and t[0] == "depth":
                d = int(t[1]); vals = [int(t[i]) for i in (3, 5, 7, 9, 11)]
                if d <= sd:
                    top[d] = vals
                else:
                    rows[d] = [a + b for a, b in zip(rows.get(d, [0] * 5), vals)]
        lp += int(re.search(r"# LP attempts (\d+)", txt).group(1))
        mm = re.search(r"max layer (\d+) states, max tracked pairs (\d+)", txt)
        maxlayer = max(maxlayer, int(mm.group(1))); maxpairs = max(maxpairs, int(mm.group(2)))
        cex += int(re.search(r"counterexamples-to-threshold found: (\d+)", txt).group(1))
    allrows = dict(top); allrows.update(rows)
    print(f"# D={D}: {len(files)} slice transcripts, split {M} ways at depth {sd}")
    print("# depth        nodes    certified       lpcert    cutpruned  frontier")
    tot = 0; front = 0; deepest = 0
    for d in sorted(allrows):
        n, c, l, cp, fr = allrows[d]
        print(f"depth {d:2d} {n:12d} {c:12d} {l:12d} {cp:12d} {fr:9d}")
        tot += n; front += fr
        if n:
            deepest = d
    print(f"# total nodes {tot}; deepest node depth {deepest}; LP attempts {lp}; max layer {maxlayer} states; max tracked pairs {maxpairs}")
    print(f"# counterexamples-to-threshold (complete posets with no pair in [1/3,2/3]): {cex}")
    complete = sorted(idx) == list(range(M))
    clean = all(r == "TERMINATED-CLEAN" for r in results)
    print(f"# slices present exactly once: {complete}; all slices TERMINATED-CLEAN: {clean}")
    print(f"VERDICT D={D}:", "TERMINATED-CLEAN (no counterexample of range <= D)" if complete and clean and front == 0 and cex == 0 else "NOT ESTABLISHED")


if __name__ == "__main__":
    main()
