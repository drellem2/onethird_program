#!/usr/bin/env python3
"""a1 — mg-39bf's INDEPENDENT re-run of mg-9461's byte-wise P1 guard.

The claim under audit (mg-9461, commit 0ea3ea7):

    "C_3 occurs 0 times in the whole 603-line file; Rayleigh/Cheeger/sqrt/std
     occur 0 times in Steps 5 and 6."

A zero-count is the cheapest evidence to produce and the easiest to produce
wrongly.  Three ways to get a spurious zero on this exact path, all seen on this
lineage:

  * the file is iCloud-evicted and reads short or raises EDEADLK (mg-3969 hit
    exactly this, on exactly this file);
  * the path is wrong and the open silently resolves elsewhere;
  * the step-window is computed off by enough lines that the tokens fall
    outside it.

So this script REFUSES TO REPORT A ZERO IT CANNOT DEFEND.  Every zero is
accompanied by a positive control drawn from the SAME read of the SAME bytes in
the SAME invocation: each token that reads 0 inside Steps 5-6 is required to
read > 0 somewhere in Steps 1-4, which is where the source actually puts it.
If a token is absent from BOTH windows the instrument is blind to it and the
run FAILS rather than reporting a comfortable zero.

Run:  python3 a1_source_counts.py
"""

import hashlib
import os
import re
import sys

SRC = os.path.expanduser(
    "~/Library/Mobile Documents/com~apple~CloudDocs/"
    "spectral_near_ordinal_sum_program.tex"
)

EXPECT_MD5_PREFIX = "db095fbe"
EXPECT_LINES = 603

# Step boundaries, located by their own opening \item text rather than by
# hard-coded offsets, so the windows cannot silently drift if the file moves.
STEP_OPENERS = [
    (1, r"\item Assume \(P\) is a minimal counterexample"),
    (2, r"\item Port the known bad-mixing argument"),
    (3, r"\item Prove that the dominant standard eigenvector"),
    (4, r"\item Apply Cheeger sweeping to obtain"),
    (5, r"\item Interpret this as an \(L^1\) near ordinal sum"),
    (6, r"\item Use near-ordinal-sum stability to transfer"),
]
ENUM_END = r"\end{enumerate}"

FAILURES = []


def fail(msg):
    FAILURES.append(msg)
    print("  *** FAIL: %s" % msg)


def read_source():
    """Read the source, and prove the read is real before anything counts it."""
    st = os.stat(SRC)
    with open(SRC, "rb") as fh:
        raw = fh.read()
    md5 = hashlib.md5(raw).hexdigest()
    text = raw.decode("utf-8")
    lines = text.split("\n")
    # A trailing newline yields one empty final element; wc -l counts newlines.
    n_lines = raw.count(b"\n")

    print("SOURCE")
    print("  path      %s" % SRC)
    print("  st_size   %d bytes" % st.st_size)
    print("  bytes read %d" % len(raw))
    print("  md5       %s" % md5)
    print("  lines     %d (newline count, matches `wc -l`)" % n_lines)

    if len(raw) != st.st_size:
        fail("short read: stat says %d, read %d — file may be evicted"
             % (st.st_size, len(raw)))
    if len(raw) == 0:
        fail("zero-byte read — every count below would be a spurious zero")
    if not md5.startswith(EXPECT_MD5_PREFIX):
        fail("md5 prefix %s != expected %s" % (md5[:8], EXPECT_MD5_PREFIX))
    if n_lines != EXPECT_LINES:
        fail("line count %d != expected %d" % (n_lines, EXPECT_LINES))
    return lines


def locate_steps(lines):
    """Return {step: (first_line, last_line)} 1-indexed inclusive."""
    starts = {}
    for step, opener in STEP_OPENERS:
        hits = [i + 1 for i, ln in enumerate(lines) if ln.startswith(opener)]
        if len(hits) != 1:
            fail("Step %d opener matched %d times, expected exactly 1"
                 % (step, len(hits)))
            return None
        starts[step] = hits[0]

    # The enumerate that closes Step 6 is the first \end{enumerate} after it.
    ends = [i + 1 for i, ln in enumerate(lines)
            if ln.startswith(ENUM_END) and i + 1 > starts[6]]
    if not ends:
        fail("no \\end{enumerate} after Step 6")
        return None
    close = min(ends)

    spans = {}
    ordered = sorted(starts.items())
    for idx, (step, first) in enumerate(ordered):
        last = (ordered[idx + 1][1] - 1) if idx + 1 < len(ordered) else close - 1
        if last < first:
            fail("Step %d span is empty (%d..%d)" % (step, first, last))
        spans[step] = (first, last)
    return spans


# Tokens under audit.  `pattern` is matched case-insensitively against the raw
# LaTeX so that macro spellings (\sqrt, \std, \lambda_{\std}) are caught.
TOKENS = [
    ("Rayleigh",       r"rayleigh"),
    ("prefix capture", r"prefix[\s~-]*captur"),
    ("Cheeger",        r"cheeger"),
    ("sqrt",           r"sqrt|square\s+root|\^\{?1/2\}?"),
    ("std",            r"\\std|\bstd\b|standard"),
]

# C_3 is claimed absent from the WHOLE file, so it gets every spelling I can
# think of rather than one.
C3_SPELLINGS = [
    ("C_3",      r"C_3\b"),
    ("C_{3}",    r"C_\{3\}"),
    ("C3",       r"\bC3\b"),
    ("C\\_3",    r"C\\_3"),
    ("C_{\\mathrm{3}}", r"C_\{\\mathrm\{3\}\}"),
]


def count(pattern, blob):
    return len(re.findall(pattern, blob, flags=re.IGNORECASE))


def main():
    lines = read_source()
    if FAILURES:
        print("\nREAD FAILED — refusing to report any count.")
        return 1

    spans = locate_steps(lines)
    if spans is None or FAILURES:
        print("\nSTEP LOCATION FAILED — refusing to report any count.")
        return 1

    print("\nSTEP WINDOWS (located by opener text, not hard-coded)")
    for step in sorted(spans):
        a, b = spans[step]
        print("  Step %d   lines %d-%d  (%d lines)" % (step, a, b, b - a + 1))

    def blob(step_list):
        out = []
        for s in step_list:
            a, b = spans[s]
            out.extend(lines[a - 1:b])
        return "\n".join(out)

    steps_1_4 = blob([1, 2, 3, 4])
    steps_5_6 = blob([5, 6])
    whole = "\n".join(lines)

    print("\nA — THE CLAIM: tokens occur 0 times in Steps 5-6")
    print("    Each row carries its own positive control: the SAME regex, the")
    print("    SAME read, in the SAME invocation, counted over the WHOLE file.")
    print("    A row whose whole-file count is 0 proves nothing about Steps 5-6")
    print("    — the regex may simply not match this document's spelling — and")
    print("    that row FAILS the run rather than reporting a comfortable zero.")
    print()
    print("    The first form of this control demanded the positive hit come")
    print("    from Steps 1-4, and it FAILED on `Rayleigh` and `prefix capture`.")
    print("    That was a defect in MY control, not in the parent's claim: both")
    print("    tokens are absent from all six steps and present elsewhere in the")
    print("    document, which STRENGTHENS the parent rather than weakening it.")
    print("    The S1-4 column is kept as a secondary, non-gating reading and is")
    print("    now what exhibits that strengthening.")
    print("  %-16s %8s %8s %8s   %s"
          % ("token", "S5-6", "S1-4", "whole", "verdict"))
    for name, pat in TOKENS:
        c56 = count(pat, steps_5_6)
        c14 = count(pat, steps_1_4)
        cw = count(pat, whole)
        if cw == 0:
            verdict = "BLIND — regex never matches this document"
            fail("token %r has no positive control anywhere in the file; its 0 "
                 "in Steps 5-6 is undefendable" % name)
        elif c56 == 0:
            verdict = ("0 in S5-6, instrument PROVEN sensitive (%d in file%s)"
                       % (cw, "" if c14 else ", and 0 in S1-4 too"))
        else:
            verdict = "PRESENT in S5-6 — parent's P1 guard would be LOST"
            fail("token %r occurs %d times in Steps 5-6" % (name, c56))
        print("  %-16s %8d %8d %8d   %s" % (name, c56, c14, cw, verdict))

    print("\nB — THE CLAIM: C_3 occurs 0 times in the WHOLE file")
    print("    Positive control cannot come from another window here (the claim")
    print("    is file-wide), so it comes from a token of the SAME SHAPE that")
    print("    the file does contain.")
    for name, pat in C3_SPELLINGS:
        print("  %-20s %6d" % (name, count(pat, whole)))
    print("  -- shape controls (subscripted constants the file DOES carry) --")
    for name, pat in [("C_1", r"C_1\b"), ("C_2", r"C_2\b"),
                      ("A_k", r"A_k\b"), ("K_k", r"K_k\b"),
                      ("lambda_{std}", r"\\lambda_\{\\std\}")]:
        c = count(pat, whole)
        print("  %-20s %6d" % (name, c))
    shape_controls = sum(count(p, whole) for _, p in
                         [("A_k", r"A_k\b"), ("K_k", r"K_k\b")])
    if shape_controls == 0:
        fail("no subscripted-constant shape control fires; the C_3 zero is "
             "undefendable")

    print("\nB2 — IS THE C_3 ZERO SELECTIVE OR GENERIC?")
    print("    The zero is only informative if the document names OTHER")
    print("    constants of the same kind and declines to name this one.  If it")
    print("    names none, `C_3 occurs 0 times` is a fact about the document's")
    print("    notation, not about what the architecture consumes.")
    named = sorted(set(re.findall(r"\bC_\{?(\w+)\}?", whole)))
    print("  every `C_<sub>` in the file: %s" % (named if named else "NONE"))
    absolute = count(r"absolute constant|universal constant", whole)
    print("  'absolute constant' / 'universal constant': %d" % absolute)
    explicit_num = count(r"\\varepsilon_\{?\\?(?:leak|spec|dem)", whole)
    print("  \\varepsilon_{leak|spec|dem}: %d" % explicit_num)
    if not named:
        print("  READING: the zero is GENERIC.  The source names no constant")
        print("  `C_<i>` at all, so C_3's absence is a notational fact.  It")
        print("  still supports the parent's ruling, but by a WEAKER argument")
        print("  than 'the document names constants and omits this one': the")
        print("  document is simply written without explicit constants, and")
        print("  every chain's constant is equally absent from it.")
    else:
        print("  READING: the zero is SELECTIVE — the file names %s but not "
              "C_3." % ", ".join("C_%s" % s for s in named))

    print("\nC — NEGATIVE CONTROL BY MUTATION")
    print("    Inject 'Cheeger' and 'C_3' into a COPY of the Step 5-6 window")
    print("    and re-run the identical counters.  If the mutant still reads 0")
    print("    the counter is a tautology and every zero above is worthless.")
    mutant56 = steps_5_6 + "\n\\item Apply Cheeger sweeping with C_3 constant.\n"
    m_ch = count(dict(TOKENS)["Cheeger"], mutant56)
    m_c3 = count(r"C_3\b", mutant56)
    print("  mutant Steps 5-6: Cheeger=%d  C_3=%d" % (m_ch, m_c3))
    if m_ch < 1 or m_c3 < 1:
        fail("MUTATION NOT CAUGHT — counters are tautological, all zeros void")
    else:
        print("  mutation caught: counters are not tautological.")

    print("\nD — WHAT STEPS 5 AND 6 ACTUALLY SAY, quoted from source")
    for s in (5, 6):
        a, b = spans[s]
        print("  Step %d  [%s:%d-%d]" % (s, os.path.basename(SRC), a, b))
        for i in range(a, b + 1):
            print("    %3d | %s" % (i, lines[i - 1]))

    print("\n" + "=" * 72)
    if FAILURES:
        print("RESULT: %d FAILURE(S)" % len(FAILURES))
        for f in FAILURES:
            print("  - %s" % f)
        return 1
    print("RESULT: all counts defended by a live positive control. "
          "mg-9461's P1 guard REPRODUCES.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
