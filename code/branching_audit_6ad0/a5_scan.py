"""A5 -- ledger B8, and the control set that could not have caught its one
documented failure mode.

af28's B8: "Brown (2000) contains none of the branching-graph vocabulary",
measured by a keyword census of the arXiv PDF "with five present-word controls".

af28's own section 5 item 6 records that the extraction routine DROPS LIGATURES
-- it renders "finite" as "nite" -- and asks an auditor to re-read the two
verbatim quotations because of it.  The caveat is not carried across to the
census in the same file.  It should have been:

  * of the twelve absent-word keywords, TWO contain a ligature pair:
    "differential" and "differential poset" (the "ff");
  * of the five controls, NONE contains one: "distributive lattice",
    "maximal chains", "left regular band", "Tsetlin", "derangement";

so a genuine occurrence of "differential" in Brown would have been reported as
0 occurrences, and no control in the battery could have fired.

This file re-runs the census with ligature-aware matching and with
ligature-bearing controls added, and reports whether B8's conclusion survives.
Conclusion first, so that this is not mistaken for a refutation of B8: it does
survive.  What does not survive is the claim that the controls established it.

REQUIRES NETWORK.  On failure it says so and exits 0.
"""

import re
import sys
import zlib
import urllib.request

URL = "https://arxiv.org/pdf/math/0006145"

# the twelve keywords whose ABSENCE af28's B8 asserts
ABSENT = ["Young", "tableau", "Bratteli", "branching", "differential poset",
          "differential", "Gelfand", "Okounkov", "Vershik", "Fomin",
          "dual graded", "tower of algebras"]

# af28's five controls -- every one of them is ligature-free
CTRL_AF28 = ["distributive lattice", "maximal chains", "left regular band",
             "Tsetlin", "derangement"]

# controls this file adds: every one contains an fi or ff ligature, so each
# must be found in BOTH spellings for the scan to be trustworthy
CTRL_LIG = ["finite", "defined", "fixed", "different", "coefficient"]

LIGS = {"ffi": "", "ffl": "", "fi": "", "fl": "", "ff": ""}


def pdf_text(data):
    """Independent extraction: same PDF-content-stream idea (there is only one
    way to read a Flate-compressed PDF without a library), but the text-showing
    operators are collected differently -- TJ arrays are joined explicitly and
    octal escapes are resolved before, not after, concatenation."""
    chunks = []
    for m in re.finditer(rb"stream\r?\n", data):
        s = m.end()
        e = data.find(b"endstream", s)
        if e < 0:
            continue
        try:
            chunks.append(zlib.decompress(data[s:e]))
        except Exception:
            pass
    raw = b"\n".join(chunks).decode("latin1")
    out = []
    for m in re.finditer(r"\((?:[^()\\]|\\.)*\)", raw):
        piece = m.group()[1:-1]
        piece = re.sub(r"\\(\d{1,3})", lambda mm: chr(int(mm.group(1), 8)), piece)
        piece = re.sub(r"\\(.)", r"\1", piece)
        out.append(piece)
    return " ".join(out)


def delig(s):
    """The spelling a ligature-dropping extractor produces."""
    for a, b in LIGS.items():
        s = s.replace(a, b)
    return s


def count(flat, kw):
    return len(re.findall(re.escape(re.sub(r"\s+", "", kw)), flat, re.I))


def main():
    print("=" * 78)
    print("A5  Brown (2000) keyword census, re-run with ligature-aware matching")
    print("    and with ligature-bearing controls.  arXiv:math/0006145.")
    print("=" * 78)
    print()
    try:
        data = urllib.request.urlopen(URL, timeout=120).read()
    except Exception as exc:
        print("  DOWNLOAD FAILED (%s).  This script requires network." % exc)
        return 0
    print("  bytes downloaded: %d   (af28 recorded 532339)" % len(data))
    txt = pdf_text(data)
    flat = re.sub(r"[\s-]+", "", txt)
    print("  characters extracted (whitespace and hyphens removed): %d" % len(flat))
    print("  (af28 recorded 123453 by its own routine)")
    print()

    print("  STEP 1 -- is the extraction dropping ligatures?  Each control word")
    print("  is searched BOTH as spelt and as a ligature-dropping reader would")
    print("  render it.  If the second column dominates, ligatures are gone.")
    print()
    print("    word            as spelt   ligature-dropped spelling   count")
    lig_dropped = 0
    for w in CTRL_LIG:
        a = count(flat, w)
        d = delig(w)
        b = count(flat, d)
        if b > a:
            lig_dropped += 1
        print("    %-14s %8d   %-27s %5d" % (w, a, d, b))
    print()
    print("    LIGATURES ARE DROPPED: %s (%d of %d controls found only in the"
          % ("YES" if lig_dropped else "no", lig_dropped, len(CTRL_LIG)))
    print("    ligature-dropped spelling).")
    print()

    print("  STEP 2 -- af28's five controls, and whether any of them could have")
    print("  detected the ligature loss.")
    print()
    print("    control                     count   contains fi/ff/fl?")
    for w in CTRL_AF28:
        has = (delig(w) != w)
        print("    %-26s %6d   %s" % (w, count(flat, w), "YES" if has else "no"))
    print()
    n_lig_ctrl = sum(1 for w in CTRL_AF28 if delig(w) != w)
    print("    %d of %d af28 controls bear a ligature.  So the failure mode af28"
          % (n_lig_ctrl, len(CTRL_AF28)))
    print("    documents in its own section 5 item 6 was OUTSIDE the reach of its")
    print("    own control set.")
    print()

    print("  STEP 3 -- the census, each absent-word keyword searched in BOTH")
    print("  spellings.  A nonzero in EITHER column refutes B8 for that word.")
    print()
    print("    keyword                  as spelt   ligature-dropped   verdict")
    bad = 0
    for w in ABSENT:
        a = count(flat, w)
        d = delig(re.sub(r"\s+", "", w))
        b = count(flat, d)
        risky = (d != re.sub(r"\s+", "", w))
        if a or b:
            bad += 1
        print("    %-24s %8d   %16d   %s%s"
              % (w, a, b, "absent" if not (a or b) else "PRESENT",
                 "   <- ligature-bearing keyword" if risky else ""))
    print()
    print("  STEP 4 -- verdict.")
    print()
    if bad == 0:
        print("    B8 SURVIVES.  All twelve keywords are absent in both spellings,")
        print("    including the two that af28's instrument could not have")
        print("    detected: 'differential' and 'differential poset'.")
    else:
        print("    B8 REFUTED for %d keyword(s)." % bad)
    print()
    print("    What does NOT survive is B8's scope note, 'keyword census ... with")
    print("    five present-word controls'.  The controls establish that the")
    print("    extraction produces text.  They do not establish that it produces")
    print("    the text of the two keywords whose absence the finding needs, and")
    print("    af28 had already identified the mechanism by which it does not.")
    print()
    return bad


if __name__ == "__main__":
    sys.exit(0 if main() == 0 else 0)
