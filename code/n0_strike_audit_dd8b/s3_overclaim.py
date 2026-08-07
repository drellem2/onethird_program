#!/usr/bin/env python3
"""mg-dd8b s3 — the overclaim guard: does every 'no N_0' assertion carry its qualifier?

The distinction, as my brief states it:

    PER-CLASS   there exists one N_0 good for EVERY f in o(n^2)   — FALSE (mg-c4f5 §5.3)
    PER-FAMILY  any GIVEN f = o(n^2) has a threshold of its own   — TRUE by definition of o()

So "no N_0 exists" is true only with the per-class quantifier attached. Bare, it denies a
true statement. My brief calls this "THE TRAP" and notes the strong form was caught once
already by mg-5ce3 — a strike annotation is SHORT, and the short form of 5.3 is the false one.

This script is a BASELINE: it measures the qualifier discipline in the corpus BEFORE
mg-24fb lands, so "was the overclaim reintroduced" is answerable against a recorded number
rather than asserted from memory.

The guard is deliberately CONSERVATIVE — it flags for human reading rather than judging.
A site it flags is a site to READ, not a defect. Every flag below was read by hand and the
adjudication is in README.md, not here.
"""

import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TARGETS = [
    "STATE.md",
    "docs/OneThird-Literature-LowerBound-MinimalCounterexample-mg-33f5.md",
    "docs/OneThird-LIBweak-mg-c3ca.md",
]

# Assertions of the STRONG form. N0 is written variously as N₀, N_0, `N₀`.
N0 = r"[`*]{0,2}N[₀0]?[`*]{0,2}"
STRONG = [
    ("no N0 works",      rf"\bno\s+{N0}\s+works"),
    ("no N0 exists",     rf"\bno\s+{N0}\s+exists"),
    ("N0 does not exist", rf"{N0}\s+does\s+not\s+exist"),
    ("there is none",    r"there\s+is\s+no\s+(threshold|such\s+N)"),
    ("NOT UNSPECIFIED",  rf"{N0}\s+IS\s+NOT\s+UNSPECIFIED"),
    ("no threshold follows", r"no\s+threshold\s+follows"),
    ("underivable",      r"underivable"),
]

# Per-CLASS qualifiers: any of these in the same sentence licenses the strong form.
CLASS_QUAL = [
    r"for\s+the\s+(whole\s+)?class",
    r"for\s+the\s+class",
    r"\bthe\s+class\b",
    r"for\s+(any|every)\s+candidate",
    r"for\s+\*\*?any\*\*?\s+candidate",
    r"every\s+f\b",
    r"uniform(ly)?\s+in",
    r"from\s+the\s+hypothesis",
    r"o\(n[²2]\)\s+hypothesis",
]

# Per-FAMILY acknowledgement: the true half. Its PRESENCE somewhere in the file is what
# stops a reader concluding the false strong form.
FAMILY_ACK = [
    r"some\s+threshold\s+of\s+its\s+own",
    r"\*?some\*?\s+threshold\s+of\s+its\s+own",
    r"threshold\s+of\s+its\s+own",
    r"a\s+single\s+family",
    r"its\s+own\s+`?n`?\b",
    r"at\s+its\s+own\s+`?n`?",
]


def sentences(text):
    """Split into rough sentences, keeping the 1-indexed line of each start.

    Markdown table rows and list items are their own units — a '|'-delimited cell is a
    sentence for our purposes, because that is the granularity a reader meets a claim at.
    """
    out = []
    line_no = 1
    buf, buf_line = [], 1
    i = 0
    while i < len(text):
        ch = text[i]
        buf.append(ch)
        if ch == "\n":
            line_no += 1
        # sentence enders, plus markdown cell/line boundaries
        if ch in ".!?\n|":
            s = "".join(buf).strip()
            if s:
                out.append((buf_line, s))
            buf, buf_line = [], line_no
        i += 1
    if "".join(buf).strip():
        out.append((buf_line, "".join(buf).strip()))
    return out


def window(text, pos, radius=600):
    return text[max(0, pos - radius): pos + radius]


def scan_file(rel, text):
    print()
    print("#" * 78)
    print(f"# {rel}")
    print("#" * 78)
    flags, oks = [], []
    for label, pat in STRONG:
        for m in re.finditer(pat, text, re.IGNORECASE):
            ln = text[:m.start()].count("\n") + 1
            w = window(text, m.start())
            qual = [q for q in CLASS_QUAL if re.search(q, w, re.IGNORECASE)]
            rec = (ln, label, m.group(0).strip(), qual)
            (oks if qual else flags).append(rec)

    print(f"\n  STRONG-FORM ASSERTIONS FOUND: {len(flags) + len(oks)} OCCURRENCES")
    print(f"    QUALIFIED   (per-class qualifier within +/-600 chars): {len(oks)}")
    print(f"    UNQUALIFIED (none found in that window)              : {len(flags)}")

    if oks:
        print("\n  QUALIFIED:")
        for ln, label, matched, qual in oks:
            print(f"    :{ln:<5} [{label}] {matched!r}")
            print(f"            licensed by: {qual[:3]}")
    if flags:
        print("\n  *** UNQUALIFIED — READ THESE BY HAND ***")
        for ln, label, matched, _ in flags:
            print(f"    :{ln:<5} [{label}] {matched!r}")

    fam = []
    for pat in FAMILY_ACK:
        for m in re.finditer(pat, text, re.IGNORECASE):
            fam.append((text[:m.start()].count("\n") + 1, m.group(0).strip()))
    fam = sorted(set(fam))
    print(f"\n  PER-FAMILY ACKNOWLEDGEMENT (the TRUE half) present at "
          f"{len(fam)} site(s):")
    for ln, t in fam:
        print(f"    :{ln}  {t!r}")
    if not fam:
        print("    NONE — a reader of this file alone meets only the negative half.")

    return len(flags), len(oks), len(fam)


def controls():
    print()
    print("#" * 78)
    print("# CONTROLS — run BEFORE any verdict, because an untested guard proves nothing")
    print("#" * 78)

    # POSITIVE: a bare overclaim with NO qualifier anywhere near it MUST be flagged.
    bad = ("The threshold question is settled. No `N₀` exists. "
           "That is the end of the matter and there is nothing further to compute.")
    hits = []
    for label, pat in STRONG:
        for m in re.finditer(pat, bad, re.IGNORECASE):
            w = window(bad, m.start())
            hits.append((label, bool([q for q in CLASS_QUAL
                                      if re.search(q, w, re.IGNORECASE)])))
    caught = [h for h in hits if not h[1]]
    p1 = len(caught) >= 1
    print(f"  {'PASS' if p1 else 'FAIL':4}  POSITIVE: planted BARE overclaim is flagged "
          f"({len(caught)} unqualified hit(s) of {len(hits)})")

    # POSITIVE 2: the compressed form a strike annotation would actually produce.
    bad2 = "**[SUPERSEDED — mg-c4f5 §5.3: no `N₀` exists.]**"
    h2 = []
    for label, pat in STRONG:
        for m in re.finditer(pat, bad2, re.IGNORECASE):
            w = window(bad2, m.start())
            h2.append(bool([q for q in CLASS_QUAL if re.search(q, w, re.IGNORECASE)]))
    p2 = len(h2) >= 1 and not all(h2)
    print(f"  {'PASS' if p2 else 'FAIL':4}  POSITIVE: the COMPRESSED strike-annotation "
          f"form — exactly what my brief predicts — is flagged")

    # NEGATIVE: the correctly qualified form must NOT be flagged.
    good = ("`N₀` IS NOT UNSPECIFIED: no `N₀` works for the class at all — for any "
            "candidate `N₀` an o(n²) function violating (LIB-const) below it exists. "
            "What it does not claim: a single family does have some threshold of its own.")
    h3 = []
    for label, pat in STRONG:
        for m in re.finditer(pat, good, re.IGNORECASE):
            w = window(good, m.start())
            h3.append(bool([q for q in CLASS_QUAL if re.search(q, w, re.IGNORECASE)]))
    p3 = len(h3) >= 1 and all(h3)
    print(f"  {'PASS' if p3 else 'FAIL':4}  NEGATIVE: the correctly QUALIFIED form is "
          f"NOT flagged ({len(h3)} hit(s), all qualified)")

    # NEGATIVE 2: the family acknowledgement detector must fire on the true half.
    p4 = any(re.search(p, good, re.IGNORECASE) for p in FAMILY_ACK)
    print(f"  {'PASS' if p4 else 'FAIL':4}  NEGATIVE: per-family acknowledgement detector "
          f"fires on the TRUE half")

    ok = p1 and p2 and p3 and p4
    print(f"\n  {'CONTROLS PASSED' if ok else 'CONTROLS FAILED — verdicts below are void'}")
    return ok


def main():
    ok = controls()
    totals = {}
    for rel in TARGETS:
        with open(os.path.join(REPO, rel)) as f:
            totals[rel] = scan_file(rel, f.read())
    print()
    print("=" * 78)
    print("BASELINE (pre-mg-24fb) — the numbers a later audit compares against")
    print("=" * 78)
    for rel, (nf, nq, nfam) in totals.items():
        print(f"  {rel}")
        print(f"     unqualified strong-form: {nf}   qualified: {nq}   "
              f"per-family acks: {nfam}")
    print("=" * 78)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
