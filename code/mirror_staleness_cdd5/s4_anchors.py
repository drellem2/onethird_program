"""mg-cdd5 s4 -- LINE-ANCHORED CITATIONS, AND THE COST OF THE REPAIR.

The sweep in s2 answers `does the cited FILE differ`.  A citation that names a
LINE asks a second question the file-level answer cannot reach: does line N
still hold what the citing document says it holds?

This section exists because of something the repair itself caused.  Two
citations at `STATE.md:112` carry line numbers, both QUOTE the line they point
at, and both quotes match EXACTLY at `912f1b1` and match NOTHING at
`origin/main` -- because `bde9610` inserted §5.0' above them.  So:

  * the anchors were authored against the STALE tree, which is direct evidence
    that this programme's authors have been reading the mirror checkout and
    not `origin/main`;
  * and the fast-forward, which fixes the withdrawn-text hazard, BREAKS them.

A remedy is an artifact of the same kind as the defect.  This is the defect
the remedy introduced, measured rather than discovered later by a reader.

METHOD.  For each citation carrying `:N` -- IN THE TARGET **OR IN THE LINK
TEXT**, which is where this corpus actually writes them -- read line N at both
revisions.  If they differ, RELOCATE in two strengths, reported separately
because they are different evidence:

  EXACT   the mirror line's text occurs verbatim at exactly one tip line: the
          line moved and is otherwise untouched.
  PREFIX  no verbatim occurrence, but exactly one tip line OPENS with a >= 40
          character prefix of it: the line was EDITED in place (typically by
          gaining the very strike markup this ticket is about).

Neither strength guesses.  AND NEITHER DECIDES AUTHORSHIP: in a file whose
content shifted, both directions relocate.  Authorship is decided only by a
QUOTED SPAN in the citing line matching one candidate and not the other; with
no such quote the row says UNDECIDED.

Exit 0 always -- findings about the corpus do not set this instrument's status.
"""
import os
import re
import sys

import lib_cdd5 as L

MIRROR_PIN = "912f1b1"
TIER1 = ["STATE.md", "docs/state-of-the-wall.html"]


def line_at(text, n):
    if text is L.MISSING:
        return None
    lines = text.splitlines()
    if 1 <= n <= len(lines):
        return lines[n - 1]
    return None


#: A prefix relocation shorter than this is not offered at all -- a short
#: common prefix (`| ` or `**`) would match half the document.
MIN_PREFIX = 40


def relocate(tip_text, needle):
    """Exact-match relocation, or None.  Single match only: two matches means
    the anchor is ambiguous and a guess would be worse than a refusal."""
    if tip_text is L.MISSING or not needle or not needle.strip():
        return None
    hits = [n for n, ln in enumerate(tip_text.splitlines(), 1) if ln == needle]
    return hits[0] if len(hits) == 1 else None


def relocate_prefix(tip_text, needle):
    """WEAKER relocation: the tip line was EDITED, so no exact match exists,
    but it still opens with the same text.  Returns (line, prefix_len) on a
    unique hit at the LONGEST prefix that has one, else None.

    Reported under its own heading and never merged with the exact matches:
    'the line is still there, extended' and 'the line is byte-identical' are
    different strengths of evidence and a repair should say which it used.
    """
    if tip_text is L.MISSING or not needle:
        return None
    lines = tip_text.splitlines()
    for k in range(len(needle), MIN_PREFIX - 1, -1):
        pref = needle[:k]
        hits = [n for n, ln in enumerate(lines, 1) if ln.startswith(pref)]
        if len(hits) == 1:
            return hits[0], k
    return None


def where(haystack_text, needle_line):
    """Locate `needle_line` in `haystack_text`.  Returns (line, prefix_len,
    strength) or None.  `strength` is "exact" or "prefix"."""
    if needle_line is None:
        return None
    hit = relocate(haystack_text, needle_line)
    if hit:
        return hit, len(needle_line), "exact"
    hit = relocate_prefix(haystack_text, needle_line)
    if hit:
        return hit[0], hit[1], "prefix"
    return None


def _how(w):
    return ("(exact text match)" if w[2] == "exact"
            else "(prefix match, %d chars -- the line was edited)" % w[1])


#: A quoted span shorter than this decides nothing -- `λ_std` occurs in half
#: the corpus.  Long enough to be a quotation, not a token.
MIN_QUOTE = 25

_QUOTED = re.compile(r"[`*\"“]{1,3}([^`*\"”\n]{%d,})[`*\"”]{1,3}" % MIN_QUOTE)

_SQUASH = re.compile(r"[\s`*_~]+")


def _squash(s):
    """Compare quotations modulo whitespace and inline markup: the citing
    document re-types the line without its table pipes and bolding."""
    return _SQUASH.sub("", s or "")


def decide_by_quote(root, cit, pin_line, tip_line):
    """Which revision does this anchor's author appear to have read?

    Evidence: the citing document's own line usually QUOTES the anchored text.
    If a quoted span of >= MIN_QUOTE characters appears in exactly one of the
    two candidate lines, that revision is the answer.  Otherwise None.

    This is the only thing here that can decide authorship.  Shifting cannot:
    in a file whose content moved, both directions relocate.
    """
    p = os.path.join(root, cit.src)
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8", errors="replace") as fh:
        lines = fh.read().splitlines()
    if not (1 <= cit.srcline <= len(lines)):
        return None
    return decide_by_quote_text(lines[cit.srcline - 1], pin_line, tip_line)


def decide_by_quote_text(src_line, pin_line, tip_line):
    """The decision itself, on a citing LINE rather than a file.

    Split out so a control can replay it against a citing document read out
    of git -- which is the only way a finding that a repair has since erased
    stays checkable (s3, arm PRE-REPAIR-ANCHORS).
    """
    in_pin = _squash(pin_line)
    in_tip = _squash(tip_line)
    votes = set()
    for q in _QUOTED.findall(src_line):
        sq = _squash(q)
        if len(sq) < MIN_QUOTE:
            continue
        hit_pin = bool(in_pin) and sq in in_pin
        hit_tip = bool(in_tip) and sq in in_tip
        if hit_pin and not hit_tip:
            votes.add("pin")
        elif hit_tip and not hit_pin:
            votes.add("tip")
    return votes.pop() if len(votes) == 1 else None


def main():
    L.banner("mg-cdd5 s4 -- LINE ANCHORS: the second question, and the repair's cost")
    root = L.program_root()
    mirror = L.find_mirror()
    if mirror is None:
        L.die_unreadable("one_third_width_three not found")
        print("== s4 exit: 0 ==")
        return 0

    rels = list(TIER1)
    for sub in ("docs", "code"):
        for dirpath, _dn, fns in os.walk(os.path.join(root, sub)):
            for fn in fns:
                if not fn.lower().endswith((".md", ".html", ".txt", ".tex")):
                    continue
                rel = os.path.relpath(os.path.join(dirpath, fn), root)
                if rel.startswith(os.path.join("code", "mirror_staleness_cdd5")):
                    continue
                if rel not in rels:
                    rels.append(rel)

    cits = []
    for rel in rels:
        p = os.path.join(root, rel)
        if not os.path.isfile(p):
            continue
        with open(p, encoding="utf-8", errors="replace") as fh:
            cits.extend(L.extract_citations(fh.read(), rel))
    cits = L.dedupe(cits)
    anchored = [c for c in cits if c.line]

    print("POPULATION")
    print("  every citation to one_third_width_three in %d scanned files that"
          % len(rels))
    print("  carries an explicit `:LINE` (a range counts as its first line).")
    print("  citations swept  %d" % len(cits))
    print("  of which anchored %d" % len(anchored))
    print("  tier-1 anchored   %d  (STATE.md and the twin)"
          % len([c for c in anchored if c.src in TIER1]))
    print()

    agree = moved = relocated = prefixed = unresolved = 0
    pin_authored = tip_authored = undecided = in_place = 0
    for c in sorted(anchored, key=lambda c: (c.src, c.srcline)):
        old = L.blob_at(mirror, MIRROR_PIN, c.path)
        new = L.blob_at(mirror, "origin/main", c.path)
        lo = line_at(old, c.line)
        ln_ = line_at(new, c.line)
        print("  %s:%d  ->  %s:%d" % (c.src, c.srcline, c.path, c.line))
        if lo is None and ln_ is None:
            print("      line %d exists at NEITHER revision" % c.line)
            unresolved += 1
            print()
            continue
        if lo == ln_:
            print("      SAME at both revisions: %s" % (lo or "")[:88])
            agree += 1
            print()
            continue
        moved += 1
        print("      at %s : %s" % (MIRROR_PIN, (lo if lo is not None
                                                 else "<past end of file>")[:88]))
        print("      at tip     : %s" % ((ln_ if ln_ is not None
                                          else "<past end of file>")[:88]))

        # WHICH REVISION IS THIS ANCHOR AUTHORED AGAINST?
        #
        # ⚠️ THE OBVIOUS ANSWER IS NOT AVAILABLE AND THIS SECTION DOES NOT
        # PRETEND OTHERWISE.  In a file where content SHIFTED, the pin's line
        # N is findable at the tip AND the tip's line N is findable at the
        # pin -- both directions relocate, and neither fact decides which
        # revision the author was looking at.  An earlier version of this
        # section inferred authorship from shifting alone and got 3 of 5 rows
        # wrong in the direction that flatters the repair (README §6, D5).
        #
        # What DOES decide it: the citing document usually QUOTES the line it
        # anchors.  So the quote is the evidence, and where there is no usable
        # quote the row says UNDECIDED.
        fwd = where(new, lo)          # the pin's line N, found at the tip
        bwd = where(old, ln_)         # the tip's line N, found at the pin
        q = decide_by_quote(root, c, lo, ln_)

        if fwd and fwd[0] == c.line:
            in_place += 1
            print("      EDITED IN PLACE: the anchored line is still line %d;"
                  % c.line)
            print("                   it gained text (typically the strike")
            print("                   markup).  THE ANCHOR REMAINS CORRECT.")
        elif q == "tip":
            tip_authored += 1
            print("      TIP-AUTHORED (decided by the citing quote): the text")
            print("                   %s quotes is at tip line %d, not at %s"
                  % (c.src, c.line, MIRROR_PIN))
            print("                   line %d.  CORRECT AS WRITTEN today." % c.line)
        elif q == "pin" and fwd:
            pin_authored += 1
            print("      PIN-AUTHORED (decided by the citing quote): written")
            print("                   against the stale tree.  The anchored text")
            print("                   now sits at tip line %d." % fwd[0])
            print("                   => correct anchor at origin/main is :%d  %s"
                  % (fwd[0], _how(fwd)))
        else:
            undecided += 1
            print("      UNDECIDED: the line SHIFTED, and both directions")
            print("                   relocate, so shifting alone cannot say")
            print("                   which revision the author read.")
            if fwd:
                print("                   if PIN-authored, the tip equivalent is :%d  %s"
                      % (fwd[0], _how(fwd)))
            if bwd:
                print("                   if TIP-authored, the %s equivalent is :%d  %s"
                      % (MIRROR_PIN, bwd[0], _how(bwd)))
            print("                   No quote in the citing line settles it;")
            print("                   REFUSED rather than guessed.")
        print()

    print("TALLY")
    print("  anchors whose line is IDENTICAL at both revisions  %d" % agree)
    print("  anchors whose line DIFFERS                        %d" % moved)
    print("    EDITED IN PLACE (same line number; anchor stands)  %d" % in_place)
    print("    PIN-AUTHORED    (stale-tree anchor; needs repair)  %d"
          % pin_authored)
    print("    TIP-AUTHORED    (correct as written today)         %d"
          % tip_authored)
    print("    UNDECIDED       (shifted, no quote settles it)     %d" % undecided)
    print("  anchors resolving at neither revision              %d" % unresolved)
    print()
    print("  Authorship is decided ONLY by a quoted span of >= %d characters in"
          % MIN_QUOTE)
    print("  the citing line, compared modulo whitespace and inline markup.")
    print("  Shifting alone decides nothing and is not used as evidence.")
    print()

    print("WHAT THE REPAIR COST, STATED PLAINLY")
    print("  The fast-forward is right for the PROSE -- a reader stops being")
    print("  shown a withdrawn claim as live.  It is NOT free for ANCHORS.")
    print("  Two citations at STATE.md:112 were PIN-AUTHORED: both QUOTE the")
    print("  line they point at, and both quotes matched at 912f1b1 and")
    print("  nothing at origin/main, because bde9610 inserted 5.0' above them.")
    print("  That is direct evidence that this programme's authors have been")
    print("  reading the mirror checkout and not origin/main -- the ticket's")
    print("  hazard, caught in the act rather than argued.")
    print()
    print("  THOSE TWO ARE REPAIRED (:310 -> :449, :286 -> :350), each to a")
    print("  number DERIVED above and never typed, which is why they now read")
    print("  TIP-AUTHORED.  s3's arm PRE-REPAIR-ANCHORS keeps the finding")
    print("  checkable after the repair made it invisible: it replays the")
    print("  pre-repair STATE.md out of git and requires PIN-AUTHORED.")
    print()
    print("  ANCHORS IN FROZEN AUDIT RECORDS ARE LEFT.  A record of what was")
    print("  read at the time is not improved by being re-pointed at what is")
    print("  true now; that would erase the very provenance it exists to keep.")
    print()
    print("  A line anchor into another repository is fragile by construction:")
    print("  it is a reference to a POSITION in a file anyone may edit.  This")

    print("== s4 exit: 0 ==")
    return 0


if __name__ == "__main__":
    sys.exit(main())
