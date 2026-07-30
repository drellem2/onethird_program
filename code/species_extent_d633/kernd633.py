"""KERNEL for mg-d633 -- verbatim runs, paragraphs, and a sandbox.

WHAT THIS SHARES WITH NOTHING IT MEASURES.  mg-a4ef's `kerna4ef.py` matches a
LIST OF SENTENCES against a text.  That is the right instrument for "is this
sentence still asserted" and it is the wrong one for "is this CLAIM asserted
somewhere else", which is mg-7dd3's B1: §0 said the sentence §4 strikes, with
a different lead-in, and every list-of-sentences checker was green.

So the unit here is the VERBATIM RUN.  For a struck span S and the same
document with every strike removed, the longest run of consecutive tokens they
share, as a fraction of S, separates the two cases cleanly and was measured
before the thresholds were set (see PREDICTIONS.md):

    ten strikes in the target document   run/len  13%, 17%, 20%, 26%, 28%,
                                                  31%, 34%, 43%, 45%, 62%
    the eleventh -- the claim said again          74%   (31 tokens of 42)

The 62% one is 8 tokens: §2.2's control count, quoted back in the repair banner
IN ORDER TO CORRECT IT.  That is what the exoneration rule is for, and it is
why the rule is not a length threshold alone.
"""

import os
import re
import shutil
import subprocess
import sys

__all__ = ["hdr", "toks", "paragraphs", "longest_run", "strike_findings",
           "REPO", "DOCS", "sandbox", "run_checker", "md_files",
           "RUN_MIN", "RUN_FRAC", "NEGATES"]

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
DOCS = os.path.join(REPO, "docs")

# A run of this many tokens, AND this fraction of the strike, is the claim
# itself said again rather than a shared lead-in.  Both conditions, because
# either alone misfires: 17 tokens of a 50-token strike is a quoted opening,
# and 3 of 7 is "about the term".
RUN_MIN = 8
RUN_FRAC = 0.50

# The occurrence is exonerated only if the paragraph carrying it SAYS the claim
# does not hold.  Deliberately NOT "a ticket id is nearby": mg-a4ef's kernel
# exonerates on `mg-[0-9a-f]{4}` within six lines, and the paragraph five lines
# below §0's misquotation contains an unrelated `mg-6f61`, so that rule
# exonerates B1 -- the one occurrence in this repository that must fire.  That
# is measured in e2's own controls, not assumed.  Fourth narrowing of an
# exoneration rule in this arc, and the fourth after a recorded false negative.
NEGATES = re.compile(
    r"refut|STRICKEN|struck|strikes|FORBIDDEN|WITHDRAWN|withdrawn|misquot"
    r"|printed\s+it\s+wrong|is\s+FALSE|was\s+\*?\*?false|no\s+longer"
    r"|used\s+to\s+(?:say|read|assert|claim)|does\s+not\s+hold"
    r"|corrected|correction|retract", re.I)

# ...or if it sits inside a fenced code block that is quoting a checker's own
# table of stricken strings.  An audit document that reproduces
# `check_doc.py`'s STRICKEN table is not asserting its contents, and one does:
# docs/OneThird-Audit-mg-73df-Species-Repair-Final-State.md.  Narrow: the fence
# or the paragraph introducing it must NAME the table.
DECLARED_TABLE = re.compile(
    r"\b(STRICKEN|FORBIDDEN|CORRECTIONS|GONE_FROM_DOC|REQUIRED_IN_DOC"
    r"|PATTERNS|DISARMERS)\b")


def hdr(t):
    print("=" * 78)
    print(t)
    print("=" * 78)
    print()


def toks(s):
    """Words and single punctuation marks, lowercased.  Blockquote markers are
    stripped so a sentence tokenises the same in prose and inside a quote."""
    s = re.sub(r"(?m)^(?:\s*>)+\s?", " ", s)
    return re.findall(r"[a-z0-9]+|[^\sa-z0-9]", s.lower())


def paragraphs(text):
    """(start, end) offsets of blank-line-delimited blocks."""
    out, start = [], 0
    for m in re.finditer(r"\n[ \t]*\n", text):
        out.append((start, m.start()))
        start = m.end()
    out.append((start, len(text)))
    return out


def fences(text):
    """(start, end) offsets of ``` fenced blocks."""
    marks = [m.start() for m in re.finditer(r"(?m)^\s*```", text)]
    return [(marks[i], marks[i + 1]) for i in range(0, len(marks) - 1, 2)]


def longest_run(a, b, bindex):
    """Longest common run of consecutive tokens; (length, index into b)."""
    best, at = 0, None
    for i in range(len(a)):
        for j in bindex.get(a[i], ()):
            k = 0
            while i + k < len(a) and j + k < len(b) and a[i + k] == b[j + k]:
                k += 1
            if k > best:
                best, at = k, j
    return best, at


def strike_findings(text):
    """[(strike_line, restated_line, run, strike_len, exonerated, why)] for
    every `~~struck~~` span whose claim also stands OUTSIDE every strike.

    Every strike is returned with its measurement, firing or not, so a reader
    sees the margins instead of a verdict.  `exonerated` is None when the run
    is too short or too small a fraction to be the claim at all.
    """
    strikes = [(m.start(), m.group(1))
               for m in re.finditer(r"~~(.+?)~~", text, re.S)]
    if not strikes:
        return []
    # tokens of the text OUTSIDE every strike, each with its original offset
    spans, prev = [], 0
    for m in re.finditer(r"~~(.+?)~~", text, re.S):
        spans.append((prev, m.start()))
        prev = m.end()
    spans.append((prev, len(text)))
    outside = []
    for a, b in spans:
        seg = text[a:b]
        for mm in re.finditer(r"[a-z0-9]+|[^\sa-z0-9]", seg.lower()):
            outside.append((mm.group(0), a + mm.start()))
    otoks = [t for t, _ in outside]
    index = {}
    for i, t in enumerate(otoks):
        index.setdefault(t, []).append(i)
    paras, fncs = paragraphs(text), fences(text)

    out = []
    for pos, s in strikes:
        a = toks(s)
        run, at = longest_run(a, otoks, index)
        sl = text[:pos].count("\n") + 1
        if not a or at is None:
            out.append((sl, None, run, len(a), None, ""))
            continue
        off = outside[at][1]
        rl = text[:off].count("\n") + 1
        if run < RUN_MIN or run < RUN_FRAC * len(a):
            out.append((sl, rl, run, len(a), None, ""))
            continue
        para = next((p for p in paras if p[0] <= off <= p[1]), (off, off))
        ptext = text[para[0]:para[1]]
        why = ""
        if NEGATES.search(ptext):
            why = "the paragraph says it does not hold"
        else:
            fence = next((f for f in fncs if f[0] <= off <= f[1]), None)
            if fence is not None:
                lead = text[max(0, fence[0] - 400):fence[0]]
                if DECLARED_TABLE.search(text[fence[0]:fence[1]]) \
                        or DECLARED_TABLE.search(lead):
                    why = "quoted inside a declared table of stricken strings"
        out.append((sl, rl, run, len(a), bool(why), why))
    return out


def md_files(root):
    """Every .md file under `root`, repo-relative, sorted."""
    out = []
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d != "__pycache__"]
        for fn in sorted(fns):
            if fn.endswith(".md"):
                out.append(os.path.relpath(os.path.join(dp, fn), REPO))
    return sorted(out)


# ---------------------------------------------------------------------------
# The sandbox.  Every mutation probe runs against a COPY, so no probe can
# leave the repository changed -- which matters here more than usual, because
# the probes deliberately plant forbidden sentences in files the checkers read.
# ---------------------------------------------------------------------------
SANDBOX_TREES = [
    "species_7d75",
    "species_repair_6f61",
    "species_remainder_f8fa",
    "species_repair_a4ef",
    "species_audit_73df",
    "species_extent_d633",
]


def sandbox(dest):
    """Copy docs/ and the trees the checkers read into `dest`; return `dest`."""
    shutil.copytree(os.path.join(REPO, "docs"), os.path.join(dest, "docs"))
    for t in SANDBOX_TREES:
        src = os.path.join(REPO, "code", t)
        if os.path.isdir(src):
            shutil.copytree(src, os.path.join(dest, "code", t),
                            ignore=shutil.ignore_patterns("__pycache__"))
    return dest


def run_checker(root, rel, args=()):
    """Run a checker inside a sandbox root; return (exit code, output)."""
    path = os.path.join(root, rel)
    p = subprocess.run([sys.executable, os.path.basename(path)] + list(args),
                       cwd=os.path.dirname(path), capture_output=True,
                       text=True)
    return p.returncode, p.stdout + p.stderr
