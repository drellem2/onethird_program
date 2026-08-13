"""mg-96df a1 -- RE-DERIVE the broken-anchor population and relocate every
member of it, at the revision that is current NOW.

This does not quote mg-688c's POP-D table.  The ticket's own instruction is not
to: that table is pinned to 949c439 and goes stale the moment the ref moves,
which is the defect it is about.  Everything below is re-extracted from the
citing documents and re-resolved against the mirror's live `origin/main`, with
the measured ref printed and compared to the pin.

WHAT IS SWEPT, said before the numbers so the population is not a surprise:
  * the THREE citing documents the ticket names -- adjudicated line by line;
  * the whole repository -- counted only, as a CHECK ON THE TICKET'S
    POPULATION.  "I repaired the nine I was handed" and "the nine are all
    there are" are different claims and only the second is worth anything.

D1 (mg-cdd5's, and it bites here for the same reason): an instrument that
sweeps for anchors must not sweep the directories that DISCUSS anchors.  This
directory and mg-688c's are excluded and the exclusion is printed.
"""
import os
import re
import sys
from collections import OrderedDict

import lib96df as L

CITING = [
    "docs/state-history/audit-mg-eba7-of-mg-55f2.md",
    "code/row3b_audit_eba7/OUTCOMES.md",
    "docs/OneThird-Compression-W1-LinearEigenfunction-Provenance-mg-bb60.md",
]

EXCLUDED_DIRS = [
    "code/anchor_drift_96df",          # this instrument -- D1
    "code/superseded_descent_688c",    # the table under audit -- D1
    "code/mirror_staleness_cdd5",      # the prior repair's transcripts -- D1
]

MIRROR_DOC_DIR = "docs/"

#: An anchor with its path attached.
RE_EXPLICIT = re.compile(
    r"(?P<doc>(?:[A-Za-z0-9._/-]*/)?OneThird-[A-Za-z0-9._-]+\.md)"
    r":(?P<a>\d+)(?:[–—-](?P<b>\d+))?")

#: A backticked bare line reference -- `:198`, `:127-142`.  Attributed to the
#: nearest file named ABOVE it, within BARE_WINDOW lines.
#:
#: ATTRIBUTION MUST NOT BE SELECTIVE, and this is the one place this instrument
#: could have flattered itself.  A first version looked back only for
#: `OneThird-*.md` names -- so `:662`, a reference to THIS repo's own
#: `docs/roadmap.md`, was attributed to whichever mirror document happened to
#: be named in the table three lines above it, and swept as a broken
#: cross-repo anchor.  It invented a defect out of a document it had not read.
#: The look-back now accepts ANY filename, and a bare reference under a
#: non-mirror file is reported OUT-OF-SCOPE rather than adjudicated.
RE_BARE = re.compile(r"`:(?P<a>\d+)(?:[–—-](?P<b>\d+))?`")
RE_ANYFILE = re.compile(r"([A-Za-z0-9._-]+\.(?:md|html|tex|json|py|txt))")
BARE_WINDOW = 12


class Anchor(object):
    def __init__(self, citing, cline, doc, a, b, kind):
        self.citing = citing
        self.cline = cline
        self.doc = doc
        self.a = a
        self.b = b
        self.kind = kind          # EXPLICIT | BARE
        self.match = None

    @property
    def key(self):
        return (self.citing, self.doc, self.a, self.b)

    @property
    def shown(self):
        return "%s:%d%s" % (self.doc, self.a, "-%d" % self.b if self.b else "")


def extract(root, relpath):
    """Anchors in one citing document, in file order."""
    with open(os.path.join(root, relpath), encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    out = []
    for i, line in enumerate(lines, start=1):
        for m in RE_EXPLICIT.finditer(line):
            doc = os.path.basename(m.group("doc"))
            out.append(Anchor(relpath, i, doc, int(m.group("a")),
                              int(m.group("b")) if m.group("b") else None,
                              "EXPLICIT"))
        for m in RE_BARE.finditer(line):
            doc = None
            for back in range(i, max(0, i - BARE_WINDOW) - 1, -1):
                found = RE_ANYFILE.findall(lines[back - 1])
                if found:
                    doc = found[-1]
                    break
            out.append(Anchor(relpath, i, doc or "(UNATTRIBUTED)",
                              int(m.group("a")),
                              int(m.group("b")) if m.group("b") else None,
                              "BARE"))
    return out


def in_mirror(mirror, doc):
    """Is `doc` a document of the cited repo at either revision?  Asked of the
    repo, not of the name -- a filename that merely LOOKS like a mirror
    document is not one."""
    for rev in (L.READ_REV, "origin/main"):
        if L.blob_lines(mirror, rev, MIRROR_DOC_DIR + doc) is not L.MISSING:
            return True
    return False


def in_this_repo(root, doc):
    """Does a file of that basename exist in THIS repository, as of SELF_AT?

    E1b (mg-20ee): asked of a NAMED COMMIT, not of whatever is checked out."""
    return any(os.path.basename(p) == doc for p in L.self_tracked(root))


def scope_bare(mirror, root, doc, cache):
    """Where does a BARE `:N` under the filename `doc` point?

    MIRROR / LOCAL / BOTH / NEITHER.  BOTH is the answer that matters and it is
    not hypothetical: `docs/roadmap.md` exists in the cited repo AND in this
    one, and the two bare references under it in the audit document are to
    THIS repo's roadmap -- pm-onethird's evening sweep, as the surrounding
    sentence says in as many words.  Adjudicating them against the cited repo
    invents two broken cross-repo anchors out of a file that was never cited.
    BOTH is therefore reported and NOT adjudicated; guessing is what produced
    the wrong answer.
    """
    if doc not in cache:
        m, l = in_mirror(mirror, doc), in_this_repo(root, doc)
        cache[doc] = ("BOTH" if m and l else "MIRROR" if m else
                      "LOCAL" if l else "NEITHER")
    return cache[doc]


def dedupe(anchors):
    """Unique by (citing file, cited doc, line span) -- mg-688c's key, kept so
    the two populations are comparable at all."""
    seen = OrderedDict()
    for a in anchors:
        seen.setdefault(a.key, a)
    return list(seen.values())


def repo_files(root):
    """The repo-wide sweep's corpus, as of SELF_AT (E1b, mg-20ee)."""
    for path in L.self_tracked(root):
        rel = os.path.dirname(path)
        if any(rel == e or rel.startswith(e + os.sep) for e in EXCLUDED_DIRS):
            continue
        if path.endswith((".md", ".txt", ".py", ".tex", ".json", ".sh", ".yml")):
            yield path


def main():
    root = L.program_root()
    st = L.mirror_state()

    print("=" * 78)
    print("mg-96df a1 -- WHERE THE CITED TEXT IS NOW, re-derived")
    print("=" * 78)
    print()

    if st.error:
        print("  CANNOT MEASURE: %s" % st.error)
        return 2

    now = st.remote_main or st.origin_main
    print("  citing repo, read at        : %s%s" % (
        L.SELF_AT,
        "" if L.SELF_AT == L.SELF_AS_OF
        else "   <- OVERRIDE, not the as-of stamp " + L.SELF_AS_OF[:7]))
    print("      (E1b, mg-20ee: A COMMIT, NOT A CHECKOUT.  This line used to print")
    print("       the absolute worktree path, which made the transcript reproduce")
    print("       for exactly one operator.  Every `doc:NNN` below is an offset")
    print("       into THESE bytes and is valid at no other commit; the repo-wide")
    print("       counts are corpus-valued for the same reason.  To re-measure")
    print("       against the current tree: ANCHOR_DRIFT_AT=HEAD, or =WORKTREE.)")
    print("  cited repo                  : %s" % st.path)
    print("  its HEAD                    : %s [%s]" % (st.head[:12], st.branch))
    print("  its origin/main             : %s" % (st.origin_main or "-")[:12])
    print("  the TRUE remote main        : %s   <- everything below is measured here"
          % (st.remote_main or "(ls-remote unavailable)")[:12])
    print()
    print("  the revision the citing authors READ : %s" % L.READ_REV)
    print("      (mg-cdd5 caught this in the act: STATE.md's quoted anchors")
    print("       matched exactly at that revision and nothing at origin/main.")
    print("       mg-cdd5 then fast-forwarded that branch, so it is reachable")
    print("       by name only -- never off disk.)")
    print()
    pinned_still_current = now is not None and now.startswith(L.PINNED_REV)
    print("  mg-688c pinned its table to  : %s" % L.PINNED_REV)
    print("  is that still the remote main: %s" % ("YES -- the pinned table has not"
          " yet gone stale" if pinned_still_current else
          "NO -- THE PIN HAS MOVED; the ticket's table is stale and this run is not"))
    print()
    print("  excluded from the repo-wide count (D1): %s" % ", ".join(EXCLUDED_DIRS))
    print()

    # ---------------------------------------------------------------- caches
    blobs = {}

    def get(rev, doc):
        k = (rev, doc)
        if k not in blobs:
            blobs[k] = L.blob_lines(st.path, rev, MIRROR_DOC_DIR + doc)
        return blobs[k]

    # ------------------------------------------------- the three named files
    print("-" * 78)
    print("THE THREE CITING DOCUMENTS -- every anchor, adjudicated")
    print("-" * 78)

    all_anchors = []
    for rel in CITING:
        all_anchors.extend(extract(root, rel))
    unique = dedupe(all_anchors)
    print("  anchors found: %d raw, %d unique (citing file, cited doc, span)"
          % (len(all_anchors), len(unique)))
    print("  bare-anchor attribution window: %d lines" % BARE_WINDOW)
    print()

    rows, out_of_scope, cache = [], [], {}
    for a in unique:
        if a.kind == "EXPLICIT":
            scope = "MIRROR" if a.doc.startswith("OneThird-") else "LOCAL"
        else:
            scope = ("NEITHER" if a.doc == "(UNATTRIBUTED)"
                     else scope_bare(st.path, root, a.doc, cache))
        a.scope = scope
        if scope != "MIRROR":
            out_of_scope.append(a)
            continue
        old = get(L.READ_REV, a.doc)
        new = get(now, a.doc)
        a.match = (L.relocate_block(old, a.a, a.b, new) if a.b
                   else L.relocate(old, a.a, new))
        rows.append(a)

    resolving = [r for r in rows if r.match.resolves]
    moved = [r for r in rows if r.match.determinate and not r.match.resolves]
    lost = [r for r in rows if not r.match.determinate]
    quote_broken = [r for r in rows if r.match.determinate and not r.match.verbatim]

    print("  anchors INTO THE CITED REPO      : %d" % len(rows))
    print("  bare refs to other files, skipped: %d  (this repo's own STATE.md,"
          " roadmap.md," % len(out_of_scope))
    print("                                      the HTML twin, compression.tex)")
    print()
    print("  of the %d:" % len(rows))
    print("    the cited NUMBER still lands on the cited row : %d" % len(resolving))
    print("    the number MOVED, new number determinate      : %d" % len(moved))
    print("    NO DETERMINATE TARGET                         : %d   <-- the only"
          " rows needing a human" % len(lost))
    print("    the cited TEXT was CHANGED (quotation stale)  : %d" % len(quote_broken))
    print()

    for a in rows:
        m = a.match
        drift = ("" if m.line is None or m.line == a.a
                 else "  ->  :%d" % m.line)
        flag = ("" if m.verbatim or not m.determinate else
                "   [CITED TEXT CHANGED -- a quotation of it is stale]")
        print("  [%-8s] %s:%d" % (a.kind, a.citing, a.cline))
        print("      %s%s%s" % (a.shown, drift, flag))
        print("      tier: %-20s %s" % (m.tier, m.detail))
        if m.line:
            head = L.enclosing_heading(get(now, a.doc), m.line)
            if head:
                dur = ("DURABLE" if L.heading_is_unique(get(now, a.doc), head[1])
                       else "NOT UNIQUE -- no better than a line number")
                print("      durable form at the new revision: %s  [%s]"
                      % ("#" * head[0] + " " + head[1][:56], dur))
        print()

    print("  REFERENCES NOT ADJUDICATED, WITH THE REASON (%d):" % len(out_of_scope))
    why = {"LOCAL": "this repo's own file",
           "BOTH": "AMBIGUOUS -- that name exists in BOTH repos; not guessed",
           "NEITHER": "no filename within %d lines above" % BARE_WINDOW}
    for a in out_of_scope:
        print("    %-46s -> %-34s %s"
              % (a.citing + ":" + str(a.cline), a.shown, why[a.scope]))
    print()

    # ---------------------------------------------------- repo-wide check
    print("-" * 78)
    print("REPO-WIDE CHECK ON THE TICKET'S POPULATION -- explicit anchors only")
    print("-" * 78)
    wide = []
    for rel in repo_files(root):
        try:
            text = L.self_read(root, rel)
        except (UnicodeDecodeError, OSError):
            continue
        for i, line in enumerate(text.split("\n"), start=1):
            for m in RE_EXPLICIT.finditer(line):
                wide.append(Anchor(rel, i, os.path.basename(m.group("doc")),
                                   int(m.group("a")),
                                   int(m.group("b")) if m.group("b") else None,
                                   "EXPLICIT"))
    wide = dedupe(wide)

    # THE PREDICATE HAS TO ALLOW FOR ANCHORS WRITTEN AFTER THE SHIFT.  An
    # earlier version resolved every anchor from READ_REV forward, and so
    # reported STATE.md's two anchors -- the ones mg-cdd5 had already REPAIRED
    # to their new numbers -- as broken, because :449 does not exist at the old
    # revision.  A sweep that scores a completed repair as a defect is the
    # mg-d0e2 shape, and it goes red precisely because its own finding was
    # acted on.  So: unchanged-at-both is FINE whatever its history, and an
    # anchor absent at the read revision is AUTHORED-LATER, not broken.
    wskip, wfine, wlater, wdrift = [], [], [], []
    for a in wide:
        old, new = get(L.READ_REV, a.doc), get(now, a.doc)
        if old is L.MISSING or new is L.MISSING:
            wskip.append(a)
            continue
        o, n = L.line_at(old, a.a), L.line_at(new, a.a)
        if o is not None and n is not None and L.norm(o) == L.norm(n):
            wfine.append(a)
            continue
        if o is None:
            wlater.append(a)
            continue
        a.match = (L.relocate_block(old, a.a, a.b, new) if a.b
                   else L.relocate(old, a.a, new))
        wdrift.append(a)

    print("  explicit anchors into the cited repo, whole tree: %d unique" % len(wide))
    print("    the cited path is not a doc of that repo : %d" % len(wskip))
    print("    line UNCHANGED between the two revisions : %d" % len(wfine))
    print("    line absent at the read rev (authored later, incl. mg-cdd5's")
    print("      already-repaired STATE.md anchors)     : %d" % len(wlater))
    print("    DRIFTED                                  : %d" % len(wdrift))
    print()
    outside = [a for a in wdrift if a.citing not in CITING]
    print("  DRIFTED OUTSIDE THE THREE NAMED DOCUMENTS: %d" % len(outside))
    for a in outside:
        print("    %-58s %s -> %s" % (a.citing + ":" + str(a.cline),
                                      a.shown, a.match.tier))
    if not outside:
        print("    (none.  For EXPLICIT anchors the ticket's three documents are")
        print("     the whole surface -- the population is confirmed, not taken")
        print("     on trust.  Bare anchors are swept only inside the three,")
        print("     because attributing one needs a filename nearby.)")
    print()

    print("=" * 78)
    print("a1: %d anchors into the cited repo across the three documents -- "
          "%d MOVED, %d still\n    land on their row, %d WITHOUT A DETERMINATE "
          "TARGET, %d quoting text that changed."
          % (len(rows), len(moved), len(resolving), len(lost), len(quote_broken)))
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
