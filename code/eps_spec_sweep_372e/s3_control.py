#!/usr/bin/env python3
"""mg-372e — NEGATIVE CONTROL: prove s2's detector can FAIL.

s2 passes.  A check that has never failed is indistinguishable from a check that
cannot fail, so this mutates the repaired documents IN MEMORY and asserts the
detector fires.  Nothing on disk is touched.

Four mutations.  M0 is EXPECTED NOT TO FIRE and is kept for what it shows:

  M0  strip every `~~` from mg-6bc2 -- the strike GLYPHS vanish, the prose stays.
      This does NOT fire, and that is correct rather than a miss: the detector is
      keyed on the REFUTATION TRAVELLING WITH THE SITE, not on the glyph, and the
      words "REFUTED"/"mg-131e" survive the mutation in the same block, so a
      reader still learns the formula is false.  Reported, not tuned away.
  M1  undo the repair in mg-6bc2 -- strip the glyphs AND every marker word
  M2  the same for mg-200d
  M3  plant a fresh LIVE site in mg-6bc2, spelled the way the ticket did NOT
      name it (`2/(n + 1)`, spaced) -- the failure mode a sibling sweep hit
      tonight, where the live site was written in a spelling the ticket missed
"""
import re
import sys

import s2_classify as S


def check(rel, lines):
    """s2's marked-or-allowlisted check, run against supplied lines."""
    blk = S.blocks(lines)
    allow = S.ALLOWLIST.get(rel, [])
    bad = []
    for i, line in enumerate(lines, 1):
        if not any(p.search(line) for _, p in S.ALL):
            continue
        if S.MARKED.search(blk.get(i, line)):
            continue
        if any(a in line for a in allow):
            continue
        bad.append((i, line.strip()[:80]))
    return bad


def load(rel):
    import os
    with open(os.path.join(S.ROOT, rel), encoding="utf-8") as fh:
        return fh.read().splitlines()


BC = "docs/OneThird-PairBias-EpsSup-Sharpening-mg-6bc2.md"
PS = "docs/OneThird-PerSlot-AdjacencySymmetry-mg-200d.md"

print("mg-372e NEGATIVE CONTROL — does the s2 detector fire when the repair is undone?")
print("=" * 78)
print()

MARKERS = re.compile(r"~~|REFUTED|STRUCK|VOID|mg-131e|mg-372e|mg-00a1|⛔")


def undo(ls):
    """Undo the repair: remove the strike glyphs AND every marker word."""
    return [MARKERS.sub("", l) for l in ls]


rc = 0
for name, rel, mutate, expect in [
    ("M0  strip only the `~~` glyphs from mg-6bc2 (PRE-DECLARED: NO FIRE)", BC,
     lambda ls: [l.replace("~~", "") for l in ls], False),
    ("M1  undo the repair in mg-6bc2 (glyphs AND marker words)", BC, undo, True),
    ("M2  undo the repair in mg-200d (glyphs AND marker words)", PS, undo, True),
    ("M3  plant a LIVE site in an UNNAMED spelling", BC,
     lambda ls: ls + ["", "The per-slot form buys `eps_spec = 2/(n + 1)` today.", ""], True),
]:
    base = load(rel)
    clean = check(rel, base)
    dirty = check(rel, mutate(base))
    fired = len(dirty) > len(clean)
    print(f"{name}")
    ok = (fired == expect)
    print(f"    unmutated: {len(clean)}   mutated: {len(dirty)}   "
          f"-> {'FIRED' if fired else 'DID NOT FIRE'}   "
          f"(pre-declared {'FIRE' if expect else 'NO FIRE'}: {'ok' if ok else 'MISMATCH'})")
    for ln, txt in dirty[:2]:
        print(f"      e.g. {rel}:{ln}  {txt}")
    if not ok:
        rc = 1
    print()

# M3 deserves its own note: it is the ticket's named hazard, and it is the reason
# the sweep patterns tolerate whitespace rather than matching one literal string.
print("M3 is the hazard the ticket names: a live site written `2/(n + 1)` with spaces.")
print("The EPS pattern is whitespace-tolerant, so the plant is caught.  A sweep that")
print("grepped the literal string `2/(n+1)` would have returned a clean zero.")
print()
print("CONTROL PASSED — every mutation behaved as pre-declared" if rc == 0
      else "CONTROL FAILED — a mutation did not behave as pre-declared")
sys.exit(rc)
