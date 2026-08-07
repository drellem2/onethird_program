#!/usr/bin/env python3
"""
mg-1df8 / CHECK 2 ("differ in kind must be visible") + the STANDING TARGETS.

Three tests, each mechanical, each with the surviving sites READ BY HAND in the
deliverable rather than tuned away.

T1  THE CLASS-CHAIN RIDER.  My own m1_ordering.py R5 proves (LIB-weak) and
    (LIB-const) are INCOMPARABLE as sets of functions: the chain `⊊` is true
    ONLY as a statement about growth-rate classes / germs at infinity.  So every
    site printing `⊊` must carry that rider IN ITS OWN CONTIGUOUS UNIT, or a
    reader takes it as a plain implication and is wrong in the second direction.
    (mg-c4f5 §5.4 reached the same requirement independently and calls it
    "the class chain needs its rider at its own site".)

T2  THE TWO GAPS.  mg-c4f5 §5.1 names the live hazard: there are TWO gaps in
    this material — gap 1, the QUANTIFIER between (LIB-weak) and (LIB-const);
    gap 2, the CONSTANT FACTOR ~50 between what freezing gives and what the
    architecture needs.  "A relay of the form 'the residual is a constant (~50)
    RATHER THAN a quantifier' is a category error."  Test: does any single unit
    of STATE.md carry both numbers without naming them as two distinct gaps?

T3  STATUS LANGUAGE BOTH WAYS.  The standing target.  A row that says "not
    blocked" must also say what is NOT proved, and vice versa.

Target: STATE.md at 491d42c79f7628c18cb7a5d197faa9f4600cd6c1
"""

import re
import subprocess

SHA = "491d42c79f7628c18cb7a5d197faa9f4600cd6c1"
RIDER = [r"[Aa]s asymptotic classes", r"growth-rate class", r"as an asymptotic class"]
FINDINGS = []


def rule(t):
    print()
    print("=" * 78)
    print(t)
    print("=" * 78)


def main():
    raw = subprocess.run(["git", "show", f"{SHA}:STATE.md"],
                         capture_output=True, text=True, check=True).stdout
    lines = raw.split("\n")

    # ------------------------------------------------------------------ T1
    rule("T1  THE CLASS-CHAIN RIDER — every ⊊ site must carry it ITSELF.")
    chain_sites = [(i + 1, l) for i, l in enumerate(lines) if "⊊" in l]
    print(f"  '⊊' appears on {len(chain_sites)} lines: "
          f"{[n for n, _ in chain_sites]}\n")
    bad = []
    for n, text in chain_sites:
        has = [p for p in RIDER if re.search(p, text)]
        chains = re.findall(r"`\([^`]*⊊[^`]*`", text) or re.findall(
            r"[^ ]*⊊[^ ]*", text)
        print(f"  line {n:>4}  rider: {'YES ' + str(has) if has else 'NO'}")
        for c in chains[:3]:
            print(f"            chain printed: {c[:90]}")
        if not has:
            bad.append(n)
    if bad:
        FINDINGS.append(f"T1: ⊊ printed without its rider at lines {bad}")
        print(f"\n  >> {len(bad)} site(s) print the chain WITHOUT the rider: {bad}")
    else:
        print("\n  >> ALL ⊊ sites carry the rider in their own contiguous unit.")
        print("     So no reader meets the chain as a bare implication, and my")
        print("     m1 R5 incomparability result — true as it is — does NOT")
        print("     convict this file.  (PREDICTIONS.md P17 guard fires: I do")
        print("     not get to score correct-but-scoped mathematics as a defect.)")

    # NEGATIVE CONTROL for T1
    print("\n  NC-T1: the detector must FAIL on a chain with no rider.")
    fake = "As classes `(LIB) ⊊ (LIB-weak) ⊊ (LIB-const)`, so (LIB-weak) is stronger."
    got = bool([p for p in RIDER if re.search(p, fake)])
    print(f"         synthetic unriddered chain -> rider found = {got} "
          f"(must be False)")
    assert got is False, "NC-T1 failed: detector is vacuous"
    print("         PASS — the detector can tell the difference.")

    # ------------------------------------------------------------------ T2
    rule("T2  THE TWO GAPS (mg-c4f5 §5.1's named live hazard).")
    gap2 = [r"~50", r"factor of ~50", r"gap factor"]
    gap1 = [r"quantifier", r"QUANTIFIER"]
    print("  gap 1 = QUANTIFIER, (LIB-weak) vs (LIB-const)")
    print("  gap 2 = CONSTANT FACTOR ~50, ε_sup vs ε_dem")
    print("  HAZARD: a unit carrying both, without naming them as two gaps,")
    print("  invites 'the residual is a constant RATHER THAN a quantifier'.\n")
    both = []
    for i, text in enumerate(lines):
        h1 = [p for p in gap1 if re.search(p, text)]
        h2 = [p for p in gap2 if re.search(p, text)]
        if h1 and h2:
            both.append(i + 1)
            named = bool(re.search(r"two (different )?gaps|gap 1|gap 2", text))
            print(f"  line {i+1}: carries BOTH.  names them as two gaps? "
                  f"{named}")
            # locate the two mentions to measure separation
            m1 = re.search(r"quantifier|QUANTIFIER", text)
            m2 = re.search(r"~50", text)
            if m1 and m2:
                print(f"           character separation in the same unit: "
                      f"{abs(m1.start() - m2.start())}")
            if not named:
                FINDINGS.append(
                    f"T2: line {i+1} carries both the ~50 constant gap and the "
                    f"quantifier gap without naming them as two distinct gaps")
    if not both:
        print("  No unit carries both.  Hazard not present.")
    else:
        print(f"\n  >> units carrying both: {both}")

    # ------------------------------------------------------------------ T3
    rule("T3  STATUS LANGUAGE BOTH WAYS.")
    pos = [r"not blocked", r"Not\* blocked", r"\*Not\* blocked"]
    neg = [r"neither proved nor blocked", r"no route", r"UNPROVEN",
           r"undecided", r"OPEN"]
    for i, text in enumerate(lines):
        p = [x for x in pos if re.search(x, text)]
        if not p:
            continue
        q = [x for x in neg if re.search(x, text)]
        print(f"  line {i+1}: says 'not blocked' {p}")
        print(f"           counterweight in the SAME unit: "
              f"{q if q else 'ABSENT'}")
        if not q:
            FINDINGS.append(
                f"T3: line {i+1} says 'not blocked' with no counterweight")
        else:
            print("           >> BALANCED.")

    # also the reverse direction: does any unit claim progress toward LIB-weak?
    print("\n  Reverse direction — any unit reading as PROGRESS toward "
          "(LIB-weak)?")
    prog = [r"progress toward", r"on track", r"nearly", r"close to proving",
            r"promising", r"should follow", r"expect to prove"]
    found = False
    for i, text in enumerate(lines):
        if "LIB-weak" in text:
            h = [x for x in prog if re.search(x, text, re.I)]
            if h:
                found = True
                print(f"    line {i+1}: {h}")
                FINDINGS.append(f"T3-rev: line {i+1} reads as progress")
    if not found:
        print("    None.  0 optimism markers at any (LIB-weak) site.")

    # ------------------------------------------------------------------ SUM
    rule("SUMMARY")
    if FINDINGS:
        print(f"  {len(FINDINGS)} finding(s):")
        for f in FINDINGS:
            print(f"    - {f}")
    else:
        print("  No findings from T1-T3.")


if __name__ == "__main__":
    main()
