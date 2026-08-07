#!/usr/bin/env python3
"""mg-dd8b s1 — census of the 'unspecified N_0' reading and its synonym set.

Two documents, one instrument, and the unit is named at every number.

The whole point of this script is that it reports FOUR different numbers for what
a careless reader would call "the count":

    LINES        distinct 1-indexed lines carrying at least one match
    OCCURRENCES  total matches, so a line carrying two contributes two
    LIVE         occurrences that assert the reading in the document's own voice
    ON-TOPIC     occurrences about the N_0 threshold at all

mg-5ce3's verdict said FIVE and listed SIX.  mg-24fb's own filing of mg-5ce3 said
FOUR when the true figure was six.  Both are unit errors.  This script cannot make
that error because it never emits a bare number.

Classification (LIVE / STRUCK / QUOTED, ON-TOPIC / OFF-TOPIC) is a JUDGEMENT and is
made BY HAND in README.md against the context this script prints.  s1 does not
classify; it enumerates and shows enough context to classify.  A script that both
finds and judges its own findings is not an instrument, it is an opinion.
"""

import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TARGETS = [
    "docs/OneThird-Literature-LowerBound-MinimalCounterexample-mg-33f5.md",
    "docs/OneThird-LIBweak-mg-c3ca.md",
]

# The primary term both prior counts were built from.
PRIMARY = [("unspecified", r"unspecified")]

# The synonym set mg-5ce3 ran on STATE.md and which NOBODY has run on these two
# documents.  Verbatim from my brief, plus the whitespace/hyphen tolerance that a
# literal grep for the phrase would miss (a line break between the two words is
# exactly how an absence gets reported by an instrument that was never tested).
SYNONYMS = [
    ("not specified",     r"not\s+specified"),
    ("unknown threshold", r"unknown\s+threshold"),
    ("sufficiently large", r"sufficiently[\s-]+large"),
    ("for large enough",  r"for\s+large\s+enough"),
    ("eventually",        r"eventually"),
]

# Deliberately wider than the brief's set: if these fire, the brief's set was itself
# incomplete, and that is a finding ABOUT THE BRIEF rather than about the documents.
EXTENDED = [
    ("large enough (bare)", r"large\s+enough"),
    ("some N_0",           r"some\s+N[_ ]?0"),
    ("no explicit",        r"no\s+explicit"),
    ("not made explicit",  r"not\s+made\s+explicit"),
    ("unquantified",       r"unquantified"),
    ("does not specify",   r"does\s+not\s+specify"),
    ("without specifying", r"without\s+specifying"),
    ("2/(n+1)",            r"2\s*/\s*\(\s*n\s*\+\s*1\s*\)"),
]


def scan(text, patterns):
    """Return {label: [(lineno, col, matched_text, line_text)]} over 1-indexed lines."""
    out = {}
    lines = text.split("\n")
    for label, pat in patterns:
        rx = re.compile(pat, re.IGNORECASE)
        hits = []
        for i, line in enumerate(lines, start=1):
            for m in rx.finditer(line):
                hits.append((i, m.start() + 1, m.group(0), line))
        out[label] = hits
    return out


def report(path_label, text, patterns, banner, show_context):
    print()
    print("=" * 78)
    print(f"{banner}   —   {path_label}")
    print("=" * 78)
    res = scan(text, patterns)
    for label, hits in res.items():
        lines = sorted({h[0] for h in hits})
        print()
        print(f"  TERM {label!r}:  {len(hits)} OCCURRENCES on {len(lines)} LINES")
        if lines:
            print(f"    lines: {', '.join(str(x) for x in lines)}")
            multi = {}
            for h in hits:
                multi[h[0]] = multi.get(h[0], 0) + 1
            doubled = sorted(l for l, c in multi.items() if c > 1)
            if doubled:
                print(f"    LINES CARRYING >1 OCCURRENCE: {doubled}   <-- this is the "
                      f"exact gap between the two units")
            else:
                print("    no line carries more than one occurrence "
                      "(so LINES == OCCURRENCES for this term)")
        if show_context and hits:
            for (ln, col, matched, line) in hits:
                body = line.strip()
                if len(body) > 300:
                    body = body[:300] + " ...[truncated]"
                print(f"      :{ln}  col {col}  [{matched}]")
                print(f"         | {body}")
    return res


def positive_control():
    """Prove the instrument can find a PLANTED occurrence before any absence is reported.

    My brief demands this in those words.  An absence reported by an untested grep is
    worth nothing: a typo in one regex reports 'clean' with total confidence.
    """
    planted_lines = [
        "The threshold N_0 is unspecified in the statement, and unspecified again here.",
        "The constant is not specified by the hypothesis.",
        "This leaves an unknown threshold for the argument.",
        "The bound holds for sufficiently large n.",
        "It is true for large enough n, and for large enough m.",
        "The inequality eventually holds.",
        "Wrapped across a line break: sufficiently",
        "large n is what is meant here.",
        "Hyphenated variant: sufficiently-large n.",
        "There exists some N_0 with the property.",
        "The paper gives no explicit constant and does not specify it,",
        "stating the result without specifying the threshold; it is unquantified,",
        "and the value is not made explicit anywhere.",
        "The per-slot value eps_spec = 2/(n+1) is printed here.",
    ]
    planted = "\n".join(planted_lines)
    allpat = PRIMARY + SYNONYMS + EXTENDED
    res = scan(planted, allpat)

    print()
    print("#" * 78)
    print("# POSITIVE CONTROL — planted occurrences, run BEFORE any absence is reported")
    print("#" * 78)
    failures = []
    for label, _ in allpat:
        n = len(res[label])
        # every term is planted at least once; two terms are planted twice on purpose
        ok = n >= 1
        print(f"  {'PASS' if ok else 'FAIL':4}  {label!r:24} found {n} occurrence(s)")
        if not ok:
            failures.append(label)

    # Targeted sub-checks the bare counts would not catch.
    subchecks = []
    subchecks.append((
        "'unspecified' finds BOTH occurrences on one line (the LINES/OCCURRENCES gap)",
        len(res["unspecified"]) == 2 and len({h[0] for h in res["unspecified"]}) == 1,
    ))
    subchecks.append((
        "'for large enough' finds BOTH on the same line",
        len(res["for large enough"]) == 2,
    ))
    subchecks.append((
        "'sufficiently large' finds the HYPHENATED variant",
        any("-" in h[2] for h in res["sufficiently large"]),
    ))
    # A line-break-wrapped phrase is INVISIBLE to a per-line scan.  This subcheck is
    # EXPECTED TO FAIL and is here to make that limitation visible rather than latent.
    wrapped_found = any(h[0] == 7 for h in res["sufficiently large"])
    subchecks.append((
        "KNOWN LIMITATION (expected False): a phrase wrapped ACROSS a line break "
        "is NOT found by a per-line scan",
        wrapped_found is False,
    ))
    print()
    for desc, ok in subchecks:
        print(f"  {'PASS' if ok else 'FAIL':4}  {desc}")
        if not ok:
            failures.append(desc)

    print()
    if failures:
        print(f"  POSITIVE CONTROL FAILED on {len(failures)} check(s) — "
              f"ABSENCES BELOW ARE NOT TRUSTWORTHY")
    else:
        print("  POSITIVE CONTROL PASSED — the instrument can find what it looks for, "
              "so an absence below is evidence.")
    return not failures


def negative_control():
    """A file with none of the terms must produce zero hits.

    Guards the opposite failure from the positive control: a regex so loose it matches
    everything would sail through the planted test and report every document as riddled.
    """
    clean = "\n".join([
        "The poset is graded and its rank function is injective on levels.",
        "We compute the spectral gap by hand for n = 3, 4, 5.",
        "No claim about thresholds appears in this paragraph at all.",
    ])
    allpat = PRIMARY + SYNONYMS + EXTENDED
    res = scan(clean, allpat)
    total = sum(len(v) for v in res.values())
    print()
    print("#" * 78)
    print("# NEGATIVE CONTROL — a passage carrying none of the terms")
    print("#" * 78)
    for label, _ in allpat:
        if res[label]:
            print(f"  FAIL  {label!r} matched {len(res[label])} time(s) in clean text: "
                  f"{[h[2] for h in res[label]]}")
    print(f"  total spurious matches: {total}   "
          f"{'PASS — no term is vacuously wide' if total == 0 else 'FAIL'}")
    return total == 0


def main():
    ok_pos = positive_control()
    ok_neg = negative_control()

    for rel in TARGETS:
        path = os.path.join(REPO, rel)
        if not os.path.exists(path):
            print(f"\n!!! MISSING TARGET: {rel}")
            continue
        with open(path) as f:
            text = f.read()
        nlines = len(text.split("\n"))
        print()
        print("#" * 78)
        print(f"# TARGET {rel}   ({nlines} lines, {len(text)} bytes)")
        print("#" * 78)
        report(rel, text, PRIMARY, "PRIMARY TERM (what both prior counts greped for)",
               show_context=True)
        report(rel, text, SYNONYMS,
               "SYNONYM SET mg-5ce3 RAN ON STATE.md — never run on these two documents",
               show_context=True)
        report(rel, text, EXTENDED,
               "EXTENDED SET (wider than the brief; a hit here indicts the BRIEF's set)",
               show_context=True)

    print()
    print("=" * 78)
    print(f"CONTROLS: positive {'PASS' if ok_pos else 'FAIL'}, "
          f"negative {'PASS' if ok_neg else 'FAIL'}")
    print("=" * 78)
    return 0 if (ok_pos and ok_neg) else 1


if __name__ == "__main__":
    sys.exit(main())
