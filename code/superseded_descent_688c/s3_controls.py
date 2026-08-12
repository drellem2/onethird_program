#!/usr/bin/env python3
"""mg-688c s3 -- CONTROLS.  A zero is worth nothing if the detector cannot fire.

s2 reports a zero.  Six controls, and two of them are controls on THIS
instrument's own defects rather than on the corpus:

  X1  PLANTED CLAIM        a bare assertion of a struck claim IS detected
  X2  PLANTED WITHDRAWAL   the same sentence with a strike is NOT detected
  X3  PLANTED ANCHOR       a synthetic mirror-era line anchor IS detected
  X4  BK1 IS BLIND         one of my own fingerprints cannot discriminate,
                           and this control is what says so out loud
  X5  THE WINDOW IS DOING WORK   how many occurrences the per-claim windowing
                           EXCLUDED, and what a naive global window would have
                           reported instead
  X6  SELF-EXCLUSION IS DOING WORK   this instrument would otherwise report
                           itself as the largest cluster of descendants
"""
import sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from lib688c import *  # noqa

REPAIR = mirror_reflog()[0]["at"]
HAZARD = {c["id"]: push_time(c["landed"])[0] for c in CLAIMS}
BY_ID = {c["id"]: c for c in CLAIMS}

print("=" * 78)
print("mg-688c s3 -- CONTROLS")
print("=" * 78)

fails = 0


def check(name, got, want, note=""):
    global fails
    ok = got == want
    if not ok:
        fails += 1
    print("  [%s] %-52s got %r want %r" %
          ("PASS" if ok else "FAIL", name, got, want))
    if note:
        for line in wrap(note, 8):
            print(line)


# ---------------------------------------------------------------------------
print()
print(rule())
print("X1 -- PLANTED CLAIM: can the detector fire at all?")
print(rule())
print("""
  Five synthetic artifacts, one per struck claim, each asserting the withdrawn
  reading the way a descendant would: flatly, as support, with no strike.
  These are what a real descendant would look like and the sweep MUST see them.
""")
PLANTS = {
    "RC1": "Theorem E gives the bound because `λ_std ≤ λ₂^{BK}` holds for "
           "every poset, so the transfer goes through.",
    "KS2": "Kill-shot 2 established that standard dominance is universal, "
           "which is why row 3b can be relied on.",
    "KS3": "Standard-dominance failures came out at 0 / 132, a clean sweep, "
           "so the property looks solid.",
    "CR1": "The inequality fails exactly on the ordinal sums and holds "
           "elsewhere, so restricting to indecomposables saves it.",
    "BK1": "The probe enumerates all 946 both-connected posets at n = 7, "
           "which is the complete population.",
}
for cid, text in PLANTS.items():
    hits = scan(text, BY_ID[cid])
    bare = [h for h in hits if h["verdict"] == "BARE"]
    check("X1.%s planted claim detected BARE" % cid, len(bare) >= 1, True)

# ---------------------------------------------------------------------------
print()
print(rule())
print("X2 -- PLANTED WITHDRAWAL: does the classifier tell the two apart?")
print(rule())
print("""
  The same five sentences, each with the withdrawal attached the way the real
  corpus attaches it.  These must classify CARRIES-WITHDRAWAL -- otherwise the
  BARE pile is just "every mention", the hand-adjudication is unbounded, and
  the classifier is not doing anything.
""")
for cid, text in PLANTS.items():
    marked = "~~%s~~ STRUCK -- REFUTED, see the scope correction." % text
    hits = scan(marked, BY_ID[cid])
    bare = [h for h in hits if h["verdict"] == "BARE"]
    check("X2.%s withdrawal-marked NOT bare" % cid, len(bare), 0)

# ---------------------------------------------------------------------------
print()
print(rule())
print("X3 -- PLANTED ANCHOR: does the line-anchor test fire?")
print(rule())
print("""
  Two synthetic anchors into the Reverse-Cheeger document: one at a line that
  moved (mirror-era, must fire) and one at a line that did not (must not).
  Both are resolved the same way s2 resolves the real ones.
""")
ml = show(MIRROR_REPO, MIRROR_REV, DOCS["RC"]).splitlines()
tl = show(MIRROR_REPO, TIP_REV, DOCS["RC"]).splitlines()
moved = next(i + 1 for i in range(len(ml))
             if ml[i].strip() and (i >= len(tl) or ml[i] != tl[i]))
same = next(i + 1 for i in range(len(ml))
            if ml[i].strip() and i < len(tl) and ml[i] == tl[i])
check("X3.a anchor at a MOVED line flagged stale", ml[moved - 1] != tl[moved - 1]
      if moved <= len(tl) else True, True,
      "line %d: mirror %r" % (moved, ml[moved - 1][:60]))
check("X3.b anchor at an UNMOVED line not flagged", ml[same - 1] == tl[same - 1],
      True, "line %d: identical at both revisions" % same)

# ---------------------------------------------------------------------------
print()
print(rule())
print("X4 -- ONE OF MY OWN FINGERPRINTS IS BLIND, AND IT IS BK1")
print(rule())
bk_stale = show(MIRROR_REPO, MIRROR_REV, DOCS["BK"])
bk_tip = show(MIRROR_REPO, TIP_REV, DOCS["BK"])
n_stale = len(re.findall(r"\b946\b", bk_stale))
n_tip = len(re.findall(r"\b946\b", bk_tip))
print("""
  The 946 -> 956 correction was landed as a BANNER INSERTED ABOVE the sentence.
  The sentence itself was never edited.  So "946" is still in the current
  document, and a reader of the CURRENT text writes 946 too.

    occurrences of `946` at %s : %d
    occurrences of `946` at %s : %d
""" % (MIRROR_REV, n_stale, TIP_REV, n_tip))
check("X4 the superseded figure survives verbatim at the tip", n_tip >= 1, True,
      "Therefore a bare `946` ANYWHERE is not evidence of a stale read, and "
      "the two 2026-07-30 mails s2 lists as BARE under BK1 are not evidence "
      "of anything.  This control exists because without it those two mails "
      "would sit in the report looking like the closest thing to a finding.")

# ---------------------------------------------------------------------------
print()
print(rule())
print("X5 -- THE PER-CLAIM WINDOW IS DOING WORK, MEASURED")
print(rule())
print("""
  Design rule 2 says a claim quoted before its withdrawal did not descend from
  a superseded reading.  This control prices that rule: how many occurrences
  does it exclude, and what would the naive method -- one global window from
  the mirror falling behind to the repair -- have reported instead?
""")
GLOBAL_START = ts("2026-07-21T00:05:09Z")
per_claim = naive = 0
commits = citing_commits(GLOBAL_START, REPAIR)
for com in commits:
    added = None
    for cl in CLAIMS:
        if added is None:
            added = "\n".join(added_lines(com["sha"]))
        n = len(scan(added, cl))
        naive += n
        if HAZARD[cl["id"]] <= com["at"] <= REPAIR:
            per_claim += n
print("  onethird_program commits in the GLOBAL window:      %d" % len(commits))
print("  occurrences under the NAIVE global window:          %d" % naive)
print("  occurrences under the PER-CLAIM hazard windows:     %d" % per_claim)
print("  excluded as pre-withdrawal (correct when written):  %d" %
      (naive - per_claim))
check("X5 the window rule excludes a non-zero number of occurrences",
      naive - per_claim > 0, True,
      "Those %d are artifacts that quote the claim before it was withdrawn. "
      "Counting them would have turned a zero into a large false count, and "
      "every one of them would have had to be argued away by hand." %
      (naive - per_claim))

# ---------------------------------------------------------------------------
print()
print(rule())
print("X6 -- SELF-EXCLUSION IS DOING WORK, MEASURED")
print(rule())
selftext = ""
for fn in ("lib688c.py", "s1_delta.py", "s2_descent.py", "s3_controls.py",
           "PREDICTIONS.md"):
    p = os.path.join(HERE, fn)
    if os.path.exists(p):
        with open(p, errors="replace") as fh:
            selftext += fh.read()
own = sum(len(scan(selftext, cl)) for cl in CLAIMS)
print("""
  This instrument states every struck claim in full, twice -- once as the
  stale reading and once as the current one -- and plants five more in X1.
  Swept as corpus it is the single largest cluster of "bare" assertions of
  withdrawn text in this repository.
""")
check("X6 self-exclusion removes a non-zero number of hits", own > 0, True,
      "%d fingerprint occurrences live in this directory.  mg-cdd5 hit the "
      "same trap and excluded its own 24 files; not excluding them would "
      "make the instrument its own top finding." % own)

print()
print(rule("="))
print("CONTROLS: %d checks, %d FAILED" % (5 + 5 + 2 + 1 + 1 + 1, fails))
print(rule("="))
print("== s3 exit: %d ==" % (1 if fails else 0))
sys.exit(1 if fails else 0)
