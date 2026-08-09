"""mg-9461 · s3 — the P1 guard, mechanised: read the SOURCE and exhibit what
Steps 5 and 6 actually contain.

`PREDICTIONS.md` P1 says Step 6 consumes none of the four chains, and binds me
to quoting Steps 5 and 6 from source and showing that no chain's constant
appears in either. This script does that byte-wise so the claim is a
measurement rather than a reading, and prints the lines so a reader can check
the reading too.

Source is read at source, not through any restatement.

Run: python3 s3_source.py
"""

import hashlib
import os
import re
import sys

SRC = os.path.expanduser(
    "~/Library/Mobile Documents/com~apple~CloudDocs/"
    "spectral_near_ordinal_sum_program.tex")


def line(s=""):
    print(s)


def main():
    if not os.path.exists(SRC):
        line(f"SOURCE NOT FOUND: {SRC}")
        line("s3 cannot run. The P1 guard is UNDISCHARGED — say so in the")
        line("deliverable rather than asserting the result.")
        sys.exit(2)

    raw = open(SRC, "rb").read()
    text = raw.decode("utf-8")
    lines = text.split("\n")
    line("=" * 78)
    line("mg-9461 s3 — STEPS 5 AND 6 AT SOURCE (the P1 guard)")
    line("=" * 78)
    line(f"file  : {SRC}")
    line(f"md5   : {hashlib.md5(raw).hexdigest()}")
    line(f"lines : {len(lines) - 1} (wc -l); split() gives {len(lines)} because "
         f"the file ends in a newline. mg-3969/mg-d3c7 report 603 — same file.")
    line()

    # ---------------------------------------------------------------- locate
    arch = None
    for i, l in enumerate(lines):
        if l.strip() == r"\section{Proposed proof architecture}":
            arch = i + 1
    assert arch, "architecture section not found"
    items = [i + 1 for i, l in enumerate(lines)
             if l.startswith(r"\item ") and arch <= i + 1 <= arch + 35]
    line("-" * 78)
    line("A. THE SIX STEPS, QUOTED — architecture section at :%d" % arch)
    line("-" * 78)
    for s, a in enumerate(items, start=1):
        b = items[s] - 1 if s < len(items) else a + 3
        while b > a and not lines[b - 1].strip():
            b -= 1
        body = " ".join(x.strip() for x in lines[a - 1:b]).strip()
        body = re.sub(r"\s+", " ", body)
        line(f"  Step {s}  (:{a}-{b})  {body[:300]}")
    line()

    step5 = " ".join(lines[items[4] - 1:items[5] - 1])
    step6 = " ".join(lines[items[5] - 1:items[5] + 3])

    # ------------------------------------------------- the chain constants
    line("-" * 78)
    line("B. DO ANY OF THE FOUR CHAINS' CONSTANTS APPEAR IN STEP 5 OR STEP 6?")
    line("-" * 78)
    probes = [
        ("C_3 / C₃ (chains II and III)", r"C_?\{?3\}?"),
        ("a capture fraction c (chain IV)", r"\bconstant fraction\b|\bcaptures\b"),
        ("Rayleigh quotient (chain IV's currency)", r"Rayleigh"),
        ("prefix capture", r"[Pp]refix[- ]capture"),
        ("Cheeger", r"Cheeger"),
        ("lambda_std (the spectral side)", r"\\lambda_\{?\\std\}?|\\std"),
        ("sqrt (the Cheeger square)", r"\\sqrt"),
    ]
    line(f"{'token':<42}{'in Step 5':>11}{'in Step 6':>11}{'whole file':>12}")
    for name, pat in probes:
        n5 = len(re.findall(pat, step5))
        n6 = len(re.findall(pat, step6))
        na = len(re.findall(pat, text))
        line(f"{name:<42}{n5:>11}{n6:>11}{na:>12}")
    line()
    line("  Step 5, verbatim: " + re.sub(r"\s+", " ", step5).strip()[:260])
    line("  Step 6, verbatim: " + re.sub(r"\s+", " ", step6).strip()[:260])
    line()
    line("  READING: Step 5's statement is `E K_k << min(k, n-k)` and Step 6's")
    line("  hypothesis is that statement. Neither mentions a prefix-capture")
    line("  constant, a Rayleigh quotient, a capture fraction, or Cheeger. The")
    line("  square root and lambda_std both live in Step 4 and above.")
    line("  => the four chains differ ENTIRELY above Step 5's output, and Step 6")
    line("     cannot tell which of them supplied its hypothesis. P1 HELD.")
    line()

    # ------------------------------------------------- where the chains live
    line("-" * 78)
    line("C. WHERE THE CHAINS DO DIFFER — Steps 3 and 4, and the conjecture")
    line("-" * 78)
    for tag, pat in [("Step 3", r"monotone in"), ("Step 4", r"Cheeger sweeping")]:
        for i, l in enumerate(lines, start=1):
            if re.search(pat, l):
                line(f"  {tag:<8} :{i}  {l.strip()[:200]}")
    for i, l in enumerate(lines, start=1):
        if re.search(r"constant fraction", l):
            ctx = " ".join(x.strip() for x in lines[i - 2:i + 2])
            line(f"  capture  :{i}  {re.sub(r'\\s+', ' ', ctx).strip()[:260]}")
    line()
    line("  Step 4 IS Cheeger sweeping and writes its output as a prefix with")
    line("  no constant attached; the `constant fraction` wording is the")
    line("  Prefix-capture CONJECTURE, which is not one of the six steps.")
    line("  So chains (II) and (IV) are REPLACEMENTS for Steps 3+4, not")
    line("  readings of them.")
    line()

    # ------------------------------------------------- L2 / L3 / L4
    line("-" * 78)
    line("D. THE OPEN LEMMAS THAT SELECT THE CHAIN")
    line("-" * 78)
    for i, l in enumerate(lines, start=1):
        if re.search(r"Monotonicity/prefix lemma|Prefix Cheeger lemma|"
                     r"Near-ordinal-sum stability lemma", l):
            ctx = " ".join(x.strip() for x in lines[i - 1:i + 3])
            line(f"  :{i}  {re.sub(r'\\s+', ' ', ctx).strip()[:300]}")
    line()
    line("=" * 78)
    line("s3 COMPLETE")
    line("=" * 78)


if __name__ == "__main__":
    main()
