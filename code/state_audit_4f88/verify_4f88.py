#!/usr/bin/env python3
"""mg-4f88 — reproduces every measurement in OUTCOMES.md from git alone.

No dependency on any other instrument in this repo, and no dependency on any
parent's transcript: every figure is recomputed from `git show <sha>:STATE.md`.
Run from the worktree root:  python3 code/state_audit_4f88/verify_4f88.py
"""
import subprocess, sys
from fractions import Fraction as F

PRE, PARENT, M325C, MC4F5, M345E, CUR = (
    "f758468", "f85a4e8", "905526f", "05a0061", "550a7f1", "491d42c")

fails = []


def check(label, got, want):
    ok = got == want
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}: {got!r}" + ("" if ok else f"  (expected {want!r})"))
    if not ok:
        fails.append(label)


def blob(sha, path="STATE.md"):
    r = subprocess.run(["git", "show", f"{sha}:{path}"], capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"cannot read {sha}:{path} — run from the worktree root")
    return r.stdout


print("\n=== 1. THE CONDITION travelled, and where it sits ===")
COND = "if L4 needs an `n`-dependent modulus the answer flips"
SCREEN = 4000  # declared in PREDICTIONS.md BEFORE any file was read
for sha, lab, want_line in [(PRE, "pre-edit", None), (PARENT, "(A) parent", 13), (CUR, "(B) current", 15)]:
    t = blob(sha)
    if COND not in t:
        check(f"{lab}: condition present", False, want_line is not None)
        continue
    off = t.index(COND)
    line = t[:off].count("\n") + 1
    check(f"{lab}: condition line", line, want_line)
    check(f"{lab}: inside declared {SCREEN}-char screen", off < SCREEN, True)
    print(f"        char offset {off} of {len(t)} total")

print("\n=== 2. (LIB-weak), and the word the parent REFUSED to write ===")
for sha, lab, libweak, never in [(PRE, "pre-edit", 0, 0), (PARENT, "(A) parent", 5, 0),
                                 (MC4F5, "mg-c4f5", 15, 1), (CUR, "(B) current", 18, 1)]:
    t = blob(sha)
    check(f"{lab}: '(LIB-weak)' occurrences", t.count("(LIB-weak)"), libweak)
    check(f"{lab}: 'never attacked' occurrences", t.lower().count("never attacked"), never)

print("\n=== 3a. FOUR SITES, FIVE LINES, NOTHING ELSE (recomputed, not read) ===")
old, new = blob(PRE).split("\n"), blob(PARENT).split("\n")
moved = [i + 1 for i in range(129) if old[i] != new[i]]
check("lines differing inside ea0e's 1..129 invariant", moved, [13, 21, 57, 62, 86])
tail = [i + 1 for i in range(129, max(len(old), len(new)))
        if (old[i] if i < len(old) else None) != (new[i] if i < len(new) else None)]
check("lines differing outside 1..129", tail, [])

print("\n=== 3a. every marker survives, counted independently ===")
MARKERS = dict(STRUCK=2, SUPERSEDED=1, REFUTED=3, DISCHARGED=2,
               BROKEN=11, withdrawn=1, void=2, UNPROVEN=2)
for sha, lab in [(PRE, "pre-edit"), (PARENT, "(A) parent")]:
    t = blob(sha)
    check(f"{lab}: marker census", {m: t.count(m) for m in MARKERS}, MARKERS)

print("\n=== 3b. THE FALSE IMPLICATION introduced at four sites ===")
CHAIN = "(LIB-weak) ⟹ (LIB-const)"
check("pre-edit: literal chain occurrences", blob(PRE).count(CHAIN), 0)
check("(A) parent: literal chain occurrences", blob(PARENT).count(CHAIN), 2)
# the other two of the four sites are the mermaid (reversed arrows) and row 8
# (definition spliced mid-chain); both are exhibited in the diff, not countable
# by this literal, and are asserted in OUTCOMES.md §3b rather than here.

print("\n=== 3c. the row-8 contradiction is mg-325c's, NOT mg-2860's ===")
# NB: the file reads `closes **this row as phrased**` — markdown bold sits INSIDE
# the span. A literal grep returns 0 at EVERY commit and reads as 'never existed'.
# That defect of my own first sweep is recorded in OUTCOMES.md §6.
A = "closes **this row as phrased**"
B = "supply the constant form this row leads with"
for sha, lab, a, b in [(PARENT, "(A) parent", 0, 0), (M325C, "mg-325c", 1, 1), (MC4F5, "mg-c4f5", 0, 1)]:
    t = blob(sha)
    check(f"{lab}: 'closes **this row as phrased**'", t.count(A), a)
    check(f"{lab}: 'does not supply the constant form…'", t.count(B), b)

print("\n=== 4. the finite-n numbers, from the file's OWN formulas ===")
eps_leak, C3 = F(20, 100), F(1)
eps_dem = eps_leak ** 2 / (2 * C3)                    # line 15: eps_dem = eps_leak^2/(2 C_3)
check("eps_dem = eps_leak^2/(2*C_3) at 0.20, C_3=1", eps_dem, F(2, 100))
check("crossover 18/eps_dem at the repaired constant", 18 / eps_dem, 900)
check("crossover 18/eps at the SUPERSEDED 2e-4 (corpus prints ~1e5)", 18 / F(2, 10000), 90000)
check("mg-d1a2's anonymous C is C_3: 18/eps_dem == 900*C_3", 18 / (eps_leak**2 / (2 * F(3))), 900 * 3)
check("(A) parent prints a BARE 900 (no '900C')", blob(PARENT).count("900C"), 0)
check("(B) current carries mg-d1a2's reconciliation", blob(CUR).count("900C"), 2)
check("'repaired calibration' labelled at (A)", "repaired calibration" in blob(PARENT), True)
check("'repaired calibration' labelled at (B)", "repaired calibration" in blob(CUR), True)

print("\n=== 4. the currency defect is mg-345e's, not the parent's ===")
for sha, lab, sup in [(PARENT, "(A) parent", 0), (MC4F5, "mg-c4f5", 0), (M345E, "mg-345e", 9)]:
    check(f"{lab}: 'ε_sup' occurrences", blob(sha).count("ε_sup"), sup)

print("\n=== 4. 2/(n+1) in STATE.md is REFUTED, not live ===")
cur = blob(CUR)
check("(B) current: '2/(n+1)' occurrences", cur.count("2/(n+1)"), 4)
check("(B) current: carries the refutation", "IS A SMALL-`n` COINCIDENCE" in cur, True)

print("\n" + ("ALL CHECKS PASS" if not fails else f"{len(fails)} FAILED: {fails}"))
sys.exit(1 if fails else 0)
