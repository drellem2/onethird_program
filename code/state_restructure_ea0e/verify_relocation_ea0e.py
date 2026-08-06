#!/usr/bin/env python3
"""mg-ea0e: prove that the three-move `STATE.md` relocation LOST NOTHING.

It does not read the builder's spec, does not trust any list of what moved, and does not
ask the builder where anything went.  It takes `STATE.md` AS IT STOOD at the base commit,
decomposes it, and for every piece asks one question: **is this text still present,
character for character, somewhere a reader starting at the new `STATE.md` can reach?**

The five checks answer pm-onethird's five acceptance items directly.

  A1  BYTE ACCOUNTING.  Three numbers, and the arithmetic between them.
  A2  The new file's word count and longest line, against the 6,000-word / 2,000-char
      targets.
  A3  Every `mg-<id>` in the old file is still reachable.
  A4  The mg-id population, enumerated rather than assumed, counted per file.
  A5  Every STRUCK / RETRACTED / RETIRED / CORRECTED / SUPERSEDED / REFUTED marker in the
      old file survives.  (mayor's third acceptance item: a silently-dropped correction
      reinstates a claim that was withdrawn.)

Plus the check the other five stand on:

  C0  VERBATIM COVERAGE.  Every line of the old file -- and, for the rewritten ledger
      rows, every COLUMN of the old cell -- is present character for character either in
      the new `STATE.md` or in a file the new `STATE.md` links to.

Exit code 0 iff every check passes.

Run from the repo root:  python3 code/state_restructure_ea0e/verify_relocation_ea0e.py [BASE]
"""
import io, re, subprocess, sys

BASE_DEFAULT = "78ae4d9"
STATE = "STATE.md"
WORD_TARGET = 6000
LINE_TARGET = 2000

MARKERS = ["STRUCK", "RETRACTED", "RETIRED", "CORRECTED", "SUPERSEDED", "REFUTED",
           "DISCHARGED", "BROKEN", "withdrawn", "void"]

fails = []


def check(ok, label, detail=""):
    print("  {:4}  {}{}".format("PASS" if ok else "FAIL", label,
                                ("  --  " + detail) if detail else ""))
    if not ok:
        fails.append(label)


def git_show(rev, path):
    """The file at `rev`.  A path that did not exist at `rev` raises, which is how the
    byte accounting learns that a destination file is NEW rather than appended to."""
    with open("/dev/null", "wb") as devnull:
        return subprocess.check_output(["git", "show", "{}:{}".format(rev, path)],
                                       stderr=devnull).decode("utf-8")


def read(path):
    return io.open(path, encoding="utf-8").read()


def nbytes(s):
    return len(s.encode("utf-8"))


def split_row(line):
    """Split a markdown table row on UNESCAPED pipes (cells contain `\\|`)."""
    parts, buf, i = [], [], 0
    while i < len(line):
        if line[i] == "\\" and i + 1 < len(line):
            buf.append(line[i:i + 2]); i += 2; continue
        if line[i] == "|":
            parts.append("".join(buf)); buf = []; i += 1; continue
        buf.append(line[i]); i += 1
    parts.append("".join(buf))
    return parts


def is_table_row(line):
    return line.startswith("|") and line.rstrip().endswith("|")


def linked_files(text, root="docs"):
    """Every repo-relative markdown target the text links to, one hop."""
    out = set()
    for m in re.finditer(r"\]\(([^)\s]+\.md)\)", text):
        t = m.group(1)
        if not t.startswith("http"):
            out.add(t)
    return sorted(out)


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else BASE_DEFAULT
    old = git_show(base, STATE)
    new = read(STATE)

    print("=" * 78)
    print("mg-ea0e RELOCATION VERIFICATION -- STATE.md at {} vs the working tree".format(base))
    print("=" * 78)

    # ---- the reachable corpus: every .md the new STATE.md links to, one hop, plus the
    # files THOSE link to (the history files link to their README and to each other).
    hop1 = linked_files(new)
    corpus = {}
    frontier = list(hop1)
    seen = set()
    while frontier:
        path = frontier.pop()
        if path in seen:
            continue
        seen.add(path)
        try:
            corpus[path] = read(path)
        except IOError:
            continue
        for nxt in linked_files(corpus[path]):
            if nxt not in seen:
                # history files link with bare basenames relative to their own directory
                cand = nxt if "/" in nxt else "docs/state-history/" + nxt
                frontier.append(cand)
    print("\nReachable corpus from the new STATE.md: {} linked markdown files".format(len(corpus)))

    def reachable(s):
        if s in new:
            return STATE
        for path, text in corpus.items():
            if s in text:
                return path
        return None

    # ------------------------------------------------------------------ C0
    print("\n[C0] VERBATIM COVERAGE -- every old line, or every column of every rewritten "
          "row, still present character for character")
    old_lines = old.split("\n")
    new_lines = new.split("\n")
    missing, moved, in_place, cells_checked = [], 0, 0, 0
    for i, line in enumerate(old_lines, 1):
        if not line.strip():
            continue
        if line in new:
            in_place += 1
            continue
        if is_table_row(line):
            cols = [c.strip() for c in split_row(line)[1:-1]]
            cells_checked += 1
            for j, col in enumerate(cols):
                if not col.strip():
                    continue
                where = reachable(col)
                if where is None:
                    missing.append("line {} column {}: {!r}".format(i, j + 1, col[:120]))
                elif where != STATE:
                    moved += 1
            continue
        where = reachable(line)
        if where is None:
            missing.append("line {}: {!r}".format(i, line[:160]))
        else:
            moved += 1
    check(not missing,
          "every old line/column is present verbatim in STATE.md or a linked file",
          "{} lines in place, {} relocated verbatim, {} rewritten rows decomposed, "
          "{} missing".format(in_place, moved, cells_checked, len(missing)))
    for m in missing[:20]:
        print("        MISSING  " + m)

    # ------------------------------------------------------------------ A1
    print("\n[A1] BYTE ACCOUNTING -- a relocation that loses bytes lost content")
    old_b, new_b = nbytes(old), nbytes(new)

    # Bytes of the new STATE.md that are NOT old text: the link boilerplate, the one
    # composed current-position paragraph, and the composed appendix pointer.
    composed = 0
    for line in new_lines:
        if not line.strip() or line in old:
            continue
        if is_table_row(line):
            cols = split_row(line)
            for col in cols:
                c = col.strip()
                if not c:
                    continue
                # the largest prefix of this column that is verbatim old text
                lo, hi = 0, len(c)
                while lo < hi:
                    mid = (lo + hi + 1) // 2
                    if c[:mid] in old:
                        lo = mid
                    else:
                        hi = mid - 1
                composed += nbytes(c[lo:])
            continue
        composed += nbytes(line) + 1
    surviving = new_b - composed

    # Bytes that left STATE.md and are now carried by the destination files, counted only
    # where they are found VERBATIM in a reachable file.
    relocated = 0
    for i, line in enumerate(old_lines, 1):
        if not line.strip() or line in new:
            continue
        if is_table_row(line):
            for col in [c.strip() for c in split_row(line)[1:-1]]:
                if col and col not in new and reachable(col):
                    relocated += nbytes(col)
            continue
        if reachable(line):
            relocated += nbytes(line) + 1

    print("      (1) old STATE.md                                  {:>9,} bytes".format(old_b))
    print("      (2) new STATE.md                                  {:>9,} bytes".format(new_b))
    print("          of which composed link boilerplate            {:>9,} bytes".format(composed))
    print("          of which old text, still in place             {:>9,} bytes".format(surviving))
    print("      (3) old text relocated, found VERBATIM elsewhere  {:>9,} bytes".format(relocated))
    print("      ------------------------------------------------------------------")
    print("          (2)-composed + (3) = {:,} + {:,} = {:,}  vs old {:,}   surplus {:+,}".format(
        surviving, relocated, surviving + relocated, old_b, surviving + relocated - old_b))
    check(surviving + relocated >= old_b,
          "kept + relocated >= old  (no byte of STATE.md was dropped)",
          "surplus is text carried in BOTH places: each row's retained sentence is also "
          "in its history file")

    grown = {}
    for path in sorted(corpus):
        try:
            was = nbytes(git_show(base, path))
        except subprocess.CalledProcessError:
            was = 0
        now = nbytes(corpus[path])
        if now != was:
            grown[path] = (was, now)
    print("\n      destination files, before -> after:")
    tot_was = tot_now = 0
    for path, (was, now) in sorted(grown.items()):
        tot_was += was; tot_now += now
        print("        {:<52} {:>8,} -> {:>8,}  ({:+,})".format(path, was, now, now - was))
    print("        {:<52} {:>8,} -> {:>8,}  ({:+,})".format("TOTAL", tot_was, tot_now,
                                                            tot_now - tot_was))
    print("      corpus total, old: {:,}   new: {:,}   ({:+,})".format(
        old_b + tot_was, new_b + tot_now, (new_b + tot_now) - (old_b + tot_was)))
    check(new_b + tot_now >= old_b + tot_was,
          "the corpus as a whole did not shrink")

    # ------------------------------------------------------------------ A2
    print("\n[A2] THE NEW FILE'S SHAPE")
    words = len(new.split())
    longest = max((len(l), i + 1) for i, l in enumerate(new_lines))
    print("      words        {:>7,}   (target < {:,})".format(words, WORD_TARGET))
    print("      lines        {:>7,}".format(len(new_lines)))
    print("      longest line {:>7,} chars at :{}   (target < {:,})".format(
        longest[0], longest[1], LINE_TARGET))
    print("      was          {:>7,} words / {:,} lines / longest {:,} chars".format(
        len(old.split()), len(old_lines),
        max(len(l) for l in old_lines)))
    check(words < WORD_TARGET, "word count under target")
    check(longest[0] < LINE_TARGET, "longest line under target")

    # ------------------------------------------------------------------ A3 / A4
    print("\n[A3/A4] mg-id REACHABILITY -- the population enumerated, not assumed")
    ids_old = sorted(set(re.findall(r"mg-[0-9a-f]{4}", old)))
    ids_new = sorted(set(re.findall(r"mg-[0-9a-f]{4}", new)))
    lost = []
    where_counts = {}
    for i in ids_old:
        w = reachable(i)
        if w is None:
            lost.append(i)
        else:
            where_counts[w] = where_counts.get(w, 0) + 1
    print("      mg-ids in the OLD STATE.md: {}".format(len(ids_old)))
    print("      mg-ids in the NEW STATE.md: {}  ({} of the old population)".format(
        len(ids_new), len([i for i in ids_old if i in new])))
    print("      first reachable in:")
    for w, c in sorted(where_counts.items(), key=lambda kv: -kv[1]):
        print("        {:<52} {:>4}".format(w, c))
    only_elsewhere = [i for i in ids_old if i not in new]
    print("      mg-ids that left STATE.md but remain reachable: {}".format(len(only_elsewhere)))
    if only_elsewhere:
        print("        " + ", ".join(only_elsewhere))
    check(not lost, "every mg-id of the old file is still reachable",
          "unreachable: {}".format(lost) if lost else "0 unreachable")
    print("      per-file mg-id counts (A4):")
    print("        {:<52} {:>4} distinct".format(STATE, len(ids_new)))
    for path in sorted(corpus):
        n = len(set(re.findall(r"mg-[0-9a-f]{4}", corpus[path])))
        if n:
            print("        {:<52} {:>4} distinct".format(path, n))

    # ------------------------------------------------------------------ A5
    print("\n[A5] CORRECTION MARKERS -- none may vanish silently")
    corpus_all = new + "\n" + "\n".join(corpus.values())
    bad = []
    for marker in MARKERS:
        was = old.count(marker)
        now_state = new.count(marker)
        now_all = corpus_all.count(marker)
        flag = "" if now_all >= was else "   <-- LOST"
        if now_all < was:
            bad.append(marker)
        print("      {:<12} old {:>4}   new STATE.md {:>4}   reachable corpus {:>5}{}".format(
            marker, was, now_state, now_all, flag))
    check(not bad, "every correction/retraction marker survives in the reachable corpus",
          "lost: {}".format(bad) if bad else "0 lost")

    print("\n" + "=" * 78)
    if fails:
        print("RESULT: FAIL -- {} check(s) failed: {}".format(len(fails), fails))
        return 1
    print("RESULT: PASS -- every check green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
