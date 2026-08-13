#!/usr/bin/env python3
"""
mg-3b51 AUDIT 4 -- DID THE REPAIR STAY INSIDE ITS SCOPE?

Mechanical checks on the document itself, run against the ORIGINAL
(714aceb) and the REPAIRED (6b1eacf) text, so that "everywhere" and
"not re-opened" are measured rather than read.

  D1  THE BOUND WORD.  Every occurrence of "sharper" in the repository,
      classified: is it a LIVE claim, or a quotation inside a refutation?
  D2  THE ADOPTION ARGUMENT.  "we use a weaker tool / adopt Brown's
      Theorem 2" is refuted and a ticket for it was deliberately NOT
      filed.  Check it is not re-introduced anywhere.
  D3  RE-OPENING.  The eleven ledger status words, original vs repaired.
      A locating identification that has been re-derived, re-tested or
      hedged shows up here as a changed status.
  D4  OVER-CORRECTING.  The document's own headline and NOT CLAIMED row,
      original vs repaired.
  D5  ROW Q.  The candidate space, counted; and which members carry a
      claim in either direction.
  D6  BEYOND THE BRIEF.  Every marked repair site, mapped to the item of
      mg-1953's brief that authorises it.  Sites with no authorising
      item are listed.

BOTH SIDES ARE NOW PINNED (mg-0e77).  The original was pinned at OLD_REV from
the first line of this file; the REPAIRED side and every repository-wide walk
below read the live worktree, and so measured whatever docs/ happened to hold
on the day somebody ran this.  Both now read at AS_OF, which is a parameter.
"""

import re
import subprocess
import sys

DOC = "docs/OneThird-Landscape-Where-This-Lives.md"
OLD_REV = "714aceb"

# THE CORPUS SIDE OF THE PIN (mg-0e77).  OLD_REV pinned the SUBJECT -- the
# pre-repair document -- from the first line this file was written.  It did not
# pin the CORPUS: read_new() opened the live worktree and rg() shelled out to
# `grep -rn` over it, so D1, D2, D5, D6 and D7 measured whatever docs/ happened
# to contain on the day somebody ran this.  That is the drift, and it is
# reachable: a declared revision fixes it.
#
# AS_OF is a CORPUS revision and is deliberately a parameter (argv[2]), because
# ONE PIN DOES NOT SERVE BOTH TRANSCRIPTS OF THIS SCRIPT.  mg-1953's runner
# re-runs this file unmodified against the document as mg-aec7 later left it,
# and the POINT of that transcript is that it DISAGREES with this one -- D5's
# contact-criterion detector reports False here and True there.  Pinning both at
# the same commit would not repair mg-1953's transcript, it would delete the
# comparison it exists to make.  See README section "one pin, two transcripts".
AS_OF = "e924590"

REPO = "../.."


def git(args):
    return subprocess.run(["git"] + args,
                          capture_output=True, text=True, cwd=REPO).stdout


def read_old(path):
    return git(["show", "%s:%s" % (OLD_REV, path)])


def read_new(path):
    return git(["show", "%s:%s" % (AS_OF, path)])


def rg(pattern, *paths):
    # `git grep <rev>` and not `grep -rn`, for two reasons measured rather than
    # assumed (mg-0e77):
    #   1. it is the only form that reads the corpus AT A COMMIT at all;
    #   2. its output is SORTED.  `grep -rn` emits directory-enumeration order,
    #      which on this repository's own tree is the filesystem's name-hash
    #      order -- deterministic per filesystem, and in NO COMMIT.  The price
    #      is that the committed transcripts' LINE ORDER changes once, here; the
    #      set of lines does not.  Published in the README rather than absorbed.
    out = git(["grep", "-n", "-E", pattern, AS_OF, "--"] + list(paths))
    lines = []
    for l in out.split("\n"):
        if not l.strip():
            continue
        # git prefixes every hit with "<rev>:"; strip exactly that one field so
        # the rest of this file keeps reading "path:line:text".
        if l.startswith(AS_OF + ":"):
            l = l[len(AS_OF) + 1:]
        lines.append(l)
    return lines


def main():
    global REPO, AS_OF
    if len(sys.argv) > 1:
        REPO = sys.argv[1]
    if len(sys.argv) > 2:
        AS_OF = sys.argv[2]
    print("=" * 78)
    print("mg-3b51 AUDIT 4 -- SCOPE OF THE REPAIR, MEASURED ON THE TEXT")
    print("=" * 78)
    print()
    print("  subject document : %s" % DOC)
    print("  ORIGINAL text    : %s (pre-repair, pinned since mg-3b51)" % OLD_REV)
    print("  CORPUS as of     : %s (repaired text and every -r walk below)"
          % AS_OF)
    print("  Every number in this transcript is a function of those two commits")
    print("  and of nothing else.  Pass a corpus revision as argv[2] to ask the")
    print("  same questions of a different state of the repository.")
    print()

    new = read_new(DOC)
    old = read_old(DOC)

    print("-" * 78)
    print("D1  THE BOUND WORD.  Occurrences of 'sharper' in docs/ and STATE.md")
    print("-" * 78)
    hits = rg("sharper", "docs", "STATE.md")
    landscape = [h for h in hits if "Landscape-Where-This-Lives.md" in h
                 and "IndependentAudit" not in h]
    print("  total occurrences in docs/ + STATE.md : %d" % len(hits))
    print("  of those, in the repaired document    : %d" % len(landscape))
    for h in landscape:
        ln, rest = h.split(":", 2)[1], h.split(":", 2)[2]
        quoted = ('"strictly sharper"' in rest.lower()
                  or '"STRICTLY SHARPER"' in rest
                  or 'REFUTED' in rest or 'refuted' in rest
                  or 'not sharp' in rest or 'not sharper' in rest)
        print("    line %-5s %s" % (ln, "QUOTED/REFUTED" if quoted
                                    else "*** LIVE CLAIM ***"))
    other = [h for h in hits if "Landscape-Where-This-Lives" not in h]
    print("  elsewhere (unrelated arcs / other documents):")
    for h in other:
        f, ln = h.split(":")[0], h.split(":")[1]
        print("    %s:%s" % (f, ln))
    print()

    print("-" * 78)
    print("D2  THE ADOPTION ARGUMENT ('we use a weaker tool; adopt Theorem 2')")
    print("-" * 78)
    pats = ["weaker tool", "weaker form", "adopt.{0,40}Theorem 2",
            "Theorem 2.{0,40}adopt"]
    NEG = ["not", "false premise", "withdrawn", "refuted", "must not",
           "no longer", "is refuted"]
    filecache = {}
    for p in pats:
        hs = rg(p, "docs", "STATE.md")
        print("  /%s/ : %d hit(s)" % (p, len(hs)))
        for h in hs:
            parts = h.split(":", 2)
            path, ln = parts[0], int(parts[1])
            if path not in filecache:
                filecache[path] = read_new(path).split("\n")
            # the documents are hard-wrapped, so a claim and its negation
            # routinely sit on different physical lines; read a window.
            lines = filecache[path]
            win = " ".join(lines[max(0, ln - 3):ln + 2]).lower()
            neg = any(w in win for w in NEG)
            print("     %s:%s  %s" % (path, ln,
                                      "negated/withdrawn (window +/-2 lines)"
                                      if neg else "*** ASSERTED ***"))
    print()

    print("-" * 78)
    print("D3  RE-OPENING.  Ledger status words, ORIGINAL vs REPAIRED.")
    print("-" * 78)

    def ledger(t):
        out = {}
        for line in t.split("\n"):
            m = re.match(r"\|\s*\*\*(E\d+)\*\*\s*(?:⚠️)?\s*\|(.*)", line)
            if m:
                cells = m.group(2).split("|")
                if len(cells) >= 2:
                    st = cells[1].strip()
                    st = re.sub(r"⚠️.*", "", st).strip().rstrip(",")
                    out[m.group(1)] = st
        return out

    o, n_ = ledger(old), ledger(new)
    changed = 0
    for k in sorted(set(o) | set(n_), key=lambda s: int(s[1:])):
        a, b = o.get(k, "(absent)"), n_.get(k, "(absent)")
        if a != b:
            changed += 1
        print("  %-5s %-38s -> %-38s %s"
              % (k, a[:36], b[:36], "CHANGED" if a != b else ""))
    print()
    print("  status words changed: %d of %d" % (changed, len(set(o) | set(n_))))
    print("  Anything other than E8 changing here would be a re-opening of the")
    print("  locating, which mg-1953's brief forbids.")
    print()

    print("-" * 78)
    print("D4  OVER-CORRECTING.  Headline and NOT CLAIMED row.")
    print("-" * 78)
    for tag, t in (("ORIGINAL", old), ("REPAIRED", new)):
        m = re.search(r"\*\*The construction is a known special case[^*]*", t)
        print("  %s headline present: %s" % (tag, bool(m)))
    on = [l for l in old.split("\n") if "NOT CLAIMED" in l]
    nn = [l for l in new.split("\n") if "NOT CLAIMED" in l]
    print("  NOT CLAIMED row identical: %s" % (on == nn))
    print("  §0 item 1 (F(P) = Brown §4.3)  still 'The monoid is Brown's': %s"
          % ("The monoid is Brown's" in new))
    print("  §0 item 3 (worked example)     still present: %s"
          % ("Brown's own illustration is the repo's worked example" in new))
    print()

    print("-" * 78)
    print("D5  ROW Q.  The candidate space.")
    print("-" * 78)
    row = [l for l in new.split("\n") if l.startswith("| **Q**")]
    if row:
        r = row[0]
        numbered = re.findall(r"\((\d)\)\s+(?:the\s+)?\*\*([^*]+)\*\*", r)
        print("  enumerated candidates: %d" % len(numbered))
        for k, name in numbered:
            print("    (%s) %s" % (k, name.strip()))
        print("  'no contact' claimed for : %s"
              % re.findall(r"for \(([^)]*)\) (?:and \((\d)\) )?I looked", r))
        print("  claimed NEITHER WAY      : %s"
              % re.findall(r"For \(([^.]*?)\) I make no claim", r))
        print("  withdrawn to a hedge     : %s" % ("hedge, not a" in r))
        print("  booked under a ledger row: %s" % ("E10" in r))
        print("  states a CONTACT CRITERION (what would have counted as a hit)")
        print("                           : %s"
              % any(w in r for w in ["would count as contact",
                                     "what would have counted",
                                     "criterion for contact"]))
    print()

    print("-" * 78)
    print("D6  BEYOND THE BRIEF.  Marked repair sites vs the enumerated brief.")
    print("-" * 78)
    marks = [(i + 1, l) for i, l in enumerate(new.split("\n")) if "⚠️" in l]
    print("  marked lines: %d" % len(marks))
    brief = {
        "acyclic": "BROKEN 1 (closed form)",
        "submonoid": "BROKEN 2 (E8)",
        "homomorph": "BROKEN 2 (E8)",
        "greedoid": "BROKEN 2 (E8)",
        "candidate space": "MAJOR (row Q)",
        "FI-modules": "MAJOR (row Q)",
        "since 2000": "MAJOR (L3 dating)",
        "2010s": "MAJOR (L3 dating)",
        "three examples": "MAJOR (L3 dating, audit M2)",
        "single paradigm": "MAJOR (L3 dating, audit M2)",
        "sharper": "REFUTED (strictly sharper)",
        "more informative": "REFUTED (strictly sharper)",
        "405": "MINOR (populations)",
        "404": "MINOR (populations)",
        "402": "MINOR (populations)",
        "922 073": "MINOR (populations)",
        "936 261": "MINOR (populations)",
        "63 classes": "MINOR (populations)",
        "87": "MINOR (populations)",
        "6 197": "MINOR (populations)",
        "rotation": "MINOR (item 6 description)",
        "§4.2": "MINOR (6x6 matrix section)",
        "§4.1": "MINOR (6x6 matrix section)",
        "REPAIRED": "the repair record itself",
        "RESULT": "the pre-filed audit scoreboard",
        "REPAIR RECORD": "the repair record itself",
        "R1": "the repair record itself",
    }
    unmapped = []
    for ln, l in marks:
        if not any(k in l for k in brief):
            unmapped.append((ln, l))
    print("  sites with no authorising brief item: %d" % len(unmapped))
    for ln, l in unmapped:
        print("    line %-4d %s" % (ln, l.strip()[:110]))
    print()
    print("  Two text corrections in the repaired document are outside the")
    print("  enumerated brief and outside mg-d673's findings; both are checked")
    print("  by hand in the audit document (one place -> two places; thirty")
    print("  years old -> twenty-six).")
    print()

    print("-" * 78)
    print("D7  THE SAME SLIP R4 REPAIRS, IN THE FIGURE R3 RESTS ON.")
    print("    R4 fixes two 'n = 5 ROW quoted as an n <= 5 TOTAL' slips.  The")
    print("    headline figure for R3 is carried elsewhere in the repo as")
    print("    '2,353 levels to n <= 5'.  Levels by n are 1, 4, 24, 206, 2 353,")
    print("    so the n <= 5 total is 2 588 (2 587 for 2 <= n <= 5) and 2 353")
    print("    is the n = 5 ROW.")
    print("-" * 78)
    for h in rg("2,353|2 353", "docs", "STATE.md"):
        parts = h.split(":", 2)
        txt = parts[2]
        if re.match(r"\|\s*\d+\s*\|", txt):          # a markdown data row: the
            verdict = "table row, per-n column -- correct"
        elif ("n = 5" in txt or "n=5" in txt or "by `n`" in txt
              or ", 2 353," in txt):
            verdict = "labelled as the n = 5 row -- correct"
        else:
            verdict = "*** quoted as an n <= 5 TOTAL -- the R4 slip ***"
        print("     %s:%-4s %s" % (parts[0], parts[1], verdict))
    print()
    print("     The repaired document itself is CLEAN here: it writes")
    print("     '(4, 24, 206, 2 353, 37 029 by n)' and '1 674 of 2 353 at n = 5'.")
    print()
    print("=" * 78)


if __name__ == "__main__":
    main()
