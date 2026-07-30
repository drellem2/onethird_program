#!/usr/bin/env python3
"""mg-34bf: prove that the STATE.md ledger restructure LOST NOTHING.

The check is deliberately independent of the builder.  It does not read the relocation
spec, does not use the builder's passage splitter, and does not trust any list of what was
moved.  It takes the ledger cells as they stood at the base commit, and for each one
decomposes the cell into MAXIMAL VERBATIM RUNS that can still be found, word-for-word, in
the rewritten cell or in a history file that the rewritten cell LINKS TO.

What a pass means, precisely:

  * every word of every old ledger cell is inside some run, so no word was dropped;
  * every run is a verbatim contiguous match, so no wording was altered inside a run;
  * runs are only cut where a relocation moved text to another destination, so the run
    count is an upper bound on how many places the old reading order was interrupted;
  * the corpus searched is only what the row links to, so nothing counts as "kept" unless
    a reader starting at the row can reach it.

What a pass does NOT mean: it says nothing about whether text was ADDED (pointers were),
and nothing about whether the relocation was well judged.  It is a completeness check.

Run from the repo root:   python3 code/state_restructure_34bf/verify_relocation.py [BASE]
"""
import os, re, subprocess, sys

BASE_DEFAULT = "60f4dac0be109513c75ba6985694ec1a0eb4e8d3"
MIN_INTERESTING_RUN = 8      # runs shorter than this are listed individually in the report


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def split_row(line):
    """Split a markdown table row on UNESCAPED pipes."""
    parts, buf, i = [], [], 0
    while i < len(line):
        if line[i] == "\\" and i + 1 < len(line):
            buf.append(line[i:i + 2]); i += 2; continue
        if line[i] == "|":
            parts.append("".join(buf)); buf = []; i += 1; continue
        buf.append(line[i]); i += 1
    parts.append("".join(buf))
    return parts


def table_rows(text):
    """Ledger rows keyed by their verdict column (column 1), which the restructure does
    not touch -- so the key is stable across the change and doubles as a renumbering check."""
    out = {}
    for n, line in enumerate(text.split("\n"), 1):
        s = line.strip()
        if not (s.startswith("|") and s.endswith("|")):
            continue
        cols = split_row(line)
        if len(cols) < 4 or set(norm("".join(cols))) <= set("-| "):
            continue
        key = norm(cols[1])
        if key in out:
            key = f"{key} #{n}"
        out[key] = (n, cols)
    return out


def maximal_runs(words, docs):
    """Greedily decompose `words` into the longest possible verbatim runs found in `docs`."""
    padded = [" " + d + " " for d in docs]

    def found(a, b):
        p = " " + " ".join(words[a:b]) + " "
        return any(p in d for d in padded)

    runs, misses, i, n = [], [], 0, len(words)
    while i < n:
        if not found(i, i + 1):
            misses.append((i, words[i]))
            i += 1
            continue
        lo, hi = i + 1, n                      # largest j with found(i, j)
        while lo < hi:                          # binary search: found() is monotone in j
            mid = (lo + hi + 1) // 2
            if found(i, mid):
                lo = mid
            else:
                hi = mid - 1
        runs.append((i, lo))
        i = lo
    return runs, misses


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else BASE_DEFAULT
    old = subprocess.run(["git", "show", f"{base}:STATE.md"], capture_output=True,
                         text=True, check=True).stdout
    new = open("STATE.md", encoding="utf-8").read()

    old_rows, new_rows = table_rows(old), table_rows(new)

    print(f"base commit        : {base}")
    print(f"ledger rows (old)  : {len(old_rows)}")
    print(f"ledger rows (new)  : {len(new_rows)}")

    bad = 0
    missing = set(old_rows) - set(new_rows)
    added = set(new_rows) - set(old_rows)
    if missing:
        print(f"FAIL  {len(missing)} ledger row(s) disappeared: {sorted(missing)[:3]}")
        bad += 1
    if added:
        print(f"FAIL  {len(added)} ledger row(s) appeared: {sorted(added)[:3]}")
        bad += 1
    if not missing and not added:
        print("OK    every ledger row is still present, under an unchanged verdict column "
              "(no row renumbered, added or removed)")

    # Appendix A must be byte-identical.
    def appendix(t):
        i = t.index("## Appendix A —")
        return t[i:]
    if appendix(old) == appendix(new):
        print("OK    Appendix A is byte-identical to the base commit")
    else:
        print("FAIL  Appendix A changed")
        bad += 1

    # Appendix A pins the live population of the literal `38/38` to three files, one of them
    # this ledger cell.  A relocation that moved it would falsify that paragraph.
    lit = "38/38"
    strays = [p for p in sorted(os.listdir("docs/state-history"))
              if lit in open(os.path.join("docs/state-history", p), encoding="utf-8").read()]
    if strays:
        print(f"FAIL  `{lit}` leaked into new file(s): {strays} — Appendix A's live-site "
              "population names three files and would become false")
        bad += 1
    else:
        print(f"OK    the literal `{lit}` did not leak into any new file "
              "(Appendix A's live-site population is unchanged)")

    print()
    print(f"{'ledger row':<46} {'words':>6} {'runs':>5} {'shortest':>9} {'linked history':>15}")
    print("-" * 90)

    tot_words = tot_runs = tot_miss = 0
    changed = 0
    for key, (oln, ocols) in old_rows.items():
        nln, ncols = new_rows.get(key, (None, None))
        if ncols is None:
            continue
        for ci in range(1, min(len(ocols), len(ncols))):
            ocell, ncell = ocols[ci], ncols[ci]
            if norm(ocell) == norm(ncell):
                continue
            changed += 1
            links = re.findall(r"\]\((docs/state-history/[^)]+)\)", ncell)
            docs = [norm(ncell)]
            for L in dict.fromkeys(links):
                docs.append(norm(open(L, encoding="utf-8").read()))
            words = norm(ocell).split(" ")
            runs, misses = maximal_runs(words, docs)
            covered = sum(b - a for a, b in runs)
            shortest = min((b - a for a, b in runs), default=0)
            tot_words += len(words); tot_runs += len(runs); tot_miss += len(misses)
            flag = "" if not misses and covered == len(words) else "  <-- LOSS"
            label = (key[:42] + "...") if len(key) > 45 else key
            print(f"{label:<46} {len(words):>6} {len(runs):>5} {shortest:>9} "
                  f"{len(dict.fromkeys(links)):>15}{flag}")
            if misses:
                bad += 1
                for idx, w in misses[:12]:
                    ctx = " ".join(words[max(0, idx - 6):idx + 7])
                    print(f"        LOST WORD {w!r} in context: ...{ctx}...")
            for a, b in runs:
                if b - a < MIN_INTERESTING_RUN:
                    print(f"        short run ({b-a} words): "
                          f"{' '.join(words[a:b])[:120]!r}")

    print("-" * 90)
    print(f"cells changed                      : {changed}")
    print(f"words in those cells at base       : {tot_words}")
    print(f"maximal verbatim runs covering them: {tot_runs}")
    print(f"words not found anywhere reachable : {tot_miss}")
    print()
    if bad == 0 and tot_miss == 0:
        print("PASS — every word of every restructured ledger cell is still present, verbatim, "
              "in the cell itself or in a history file that cell links to.")
        return 0
    print(f"FAIL — {bad} problem(s) above.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
