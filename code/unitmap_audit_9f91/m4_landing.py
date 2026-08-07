#!/usr/bin/env python3
"""mg-9f91 / steps 2, 3, 6 -- what the LANDED text does and does not say.

Mechanical scans over the two changed lines only (STATE.md :15 and :115), plus the
provenance checks that decide whether a defect is mg-9adf's or inherited.

  S1  reserved question: does the landed text DECIDE which 1/6 Daniel meant?
  S2  closure: did max = n/(n+1), ATTAINED, and the EQUALITY reading travel?
  S3  citation: is mg-c4f5:415 CITED, and how many copies of its sentence now exist?
  S4  the mg-6bc2 Defect-2 conflict: the source's own blanket caveat vs the landing
  S5  provenance of the doubled 'lambda_std->1' sentence mg-9adf disclosed
  S6  scope: were row 11 / C_3 / eps_dem touched?
"""
import re
import subprocess

def show(rev, path):
    return subprocess.run(["git", "show", f"{rev}:{path}"],
                          capture_output=True, text=True, check=True).stdout

PARENT, LANDED = "72a6e33", "21ee93f"
p = show(PARENT, "STATE.md").split("\n")
l = show(LANDED, "STATE.md").split("\n")
sites = {15: (p[14], l[14]), 115: (p[114], l[114])}
# the inserted text = landed minus parent, per line (parent is a subsequence here)
import difflib
ins = {}
for ln, (a, b) in sites.items():
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    ins[ln] = "".join(b[j1:j2] for t, i1, i2, j1, j2 in sm.get_opcodes()
                      if t in ("insert", "replace"))

print("=" * 78)
print("S1  DID IT DECIDE DANIEL'S QUESTION?  (reserved to him)")
print("=" * 78)
DECIDERS = [
    r"conjecture is (confirmed|refuted|right|wrong|proven|correct)",
    r"Daniel(?:'s)? (?:conjecture|number|1/6) is (?:confirmed|refuted|right|wrong)",
    r"he meant the ",
    r"the 1/6 he meant is",
]
RESERVERS = [
    r"NOT DECIDED HERE", r"NOT decided here", r"is Daniel's", r"question is his",
    r"true under either reading", r"true either way",
]
for ln in (15, 115):
    t = ins[ln]
    d = [pat for pat in DECIDERS if re.search(pat, t, re.I)]
    r = [pat for pat in RESERVERS if re.search(pat, t)]
    print(f"  :{ln}  decider phrases matched : {d if d else 'NONE'}")
    print(f"  :{ln}  reserving phrases matched: {len(r)} -> {r}")
    # the only allowed use of confirmed/refuted is a DENIAL
    for m in re.finditer(r"[^.]*\b(confirmed|refuted)\b[^.]*", t):
        print(f"  :{ln}  'confirmed/refuted' occurrence: ...{m.group(0).strip()[-120:]}")
print()

print("=" * 78)
print("S2  DID THE CLOSURE TRAVEL?")
print("=" * 78)
CLOSURE = {
    "the max expression": r"max\{ 6E_μ\[inv_e\]/\(n²−1\) : μ ∈ M_n \} = n/\(n\+1\)",
    "the word ATTAINED": r"ATTAINED",
    "EQUALITY reading": r"EQUALITY for the information it consumes",
    "not-a-bound rider": r"not a bound awaiting a better argument",
    "realizability rider": r"realizability",
    "M_n defined": r"M_n",
}
for ln in (15, 115):
    print(f"  :{ln}")
    for k, pat in CLOSURE.items():
        print(f"      {'YES' if re.search(pat, ins[ln]) else 'no '}  {k}")
print()

print("=" * 78)
print("S3  WAS THE 1/6 FORM CITED, OR RESTATED?  (and how many copies now exist)")
print("=" * 78)
CITE = r"OneThird-LIBweak-mg-c4f5-IndependentAudit\.md"
DEFN = r"OneThird-LIBweak-mg-c3ca\.md"
for ln in (15, 115):
    print(f"  :{ln}  cites mg-c4f5 audit : {bool(re.search(CITE, ins[ln]))}"
          f"   cites mg-c3ca defn : {bool(re.search(DEFN, ins[ln]))}")
    print(f"  :{ln}  names the line :415 : {':415' in ins[ln]}"
          f"   names :172 : {':172' in ins[ln]}")
QUOTE = "Freezing unconditionally gives only"
out = subprocess.run(["grep", "-rn", "--include=*.md", QUOTE, "."],
                     capture_output=True, text=True).stdout.strip().split("\n")
out = [o for o in out if o and "unitmap_audit_9f91" not in o]
print(f"\n  verbatim copies of the :415 sentence corpus-wide: {len(out)}")
for o in out:
    print(f"      {o.split(':')[0]}:{o.split(':')[1]}")
print()

print("=" * 78)
print("S4  THE SOURCE CONTRADICTS THE LANDING -- mg-6bc2 Defect 2")
print("=" * 78)
src = open("docs/OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md", encoding="utf-8").read()
srcl = src.split("\n")
for i, line in enumerate(srcl, 1):
    if "every attainment statement is finite" in line:
        print(f"  mg-6bc2:{i}  {' '.join(srcl[i-2:i+1]).strip()[:300]}")
for i, line in enumerate(srcl, 1):
    if "PROVEN, all `n`, by hand" in line:
        print(f"  mg-6bc2:{i}  {line.strip()[:200]}")
landed_claims_all_n = any(re.search(r"both directions PROVEN FOR ALL `n`|`≤` and `≥` BOTH PROVEN FOR ALL `n`", ins[ln]) for ln in (15, 115))
print(f"\n  landed text asserts all-n ATTAINMENT for the inversion form : {landed_claims_all_n}")
mentions_defect2 = any("finite population" in ins[ln] and "every attainment" in ins[ln] for ln in (15, 115))
msg = subprocess.run(["git", "log", "-1", "--format=%B", LANDED],
                     capture_output=True, text=True).stdout
print(f"  landed text names mg-6bc2's blanket caveat                  : {mentions_defect2}")
print(f"  commit message names 'Defect 2'                             : {'Defect 2' in msg}")
print(f"  commit message names 'every attainment statement'            : "
      f"{'every attainment statement' in msg}")
print()

print("=" * 78)
print("S5  PROVENANCE OF THE DOUBLED SENTENCE mg-9adf DISCLOSED")
print("=" * 78)
S = "`λ_std→1` is a stronger rendering that happens to be available, not the requirement."
print(f"  occurrences in row 8 at PARENT {PARENT} : {p[114].count(S)}")
print(f"  occurrences in row 8 at LANDED {LANDED} : {l[114].count(S)}")
print("  -> pre-existing, unchanged by this edit" if p[114].count(S) == l[114].count(S) == 2
      else "  -> CHANGED BY THIS EDIT")
print()

print("=" * 78)
print("S6  SCOPE -- what else moved?")
print("=" * 78)
changed = [i + 1 for i, (a, b) in enumerate(zip(p, l)) if a != b]
print(f"  lines changed: {changed}   (parent {len(p)} lines, landed {len(l)} lines)")
row11 = next(i + 1 for i, s in enumerate(l) if s.startswith("| 11 |"))
print(f"  row 11 is line {row11}; touched: {row11 in changed}")
for tok in ("ε_dem", "C₃"):
    print(f"  '{tok}' count in row 8: parent {p[114].count(tok)} -> landed {l[114].count(tok)}")
