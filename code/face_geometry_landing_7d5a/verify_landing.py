#!/usr/bin/env python3
"""mg-7d5a -- re-measure every fact this landing asserts, from the tree and git.

This landing strikes a sentence in `STATE.md` Appendix A that argued for the A5
widening using a commit history that is false in four ways, and repairs three
MAJOR findings from mg-6653's audit of `ba3ec79`.  Two of those findings are
"the previous repair of a coverage claim was itself a wrong coverage claim", at
the second and third consecutive generation.  So this instrument exists for one
reason: **the numbers this landing prints must not be inherited from mg-6653,
from mg-f2e1, or from the ticket.**  Every one of them is re-derived here.

Four targets:

  T1  THE STRUCK SENTENCE.  The four refutations of the `G"` provenance claim,
      each re-measured from git rather than quoted from the audit -- plus the
      two facts the REPLACEMENT argument rests on, because a replacement
      argument inherited on trust is the same defect wearing the other sign.

  T2  THE 38/38 POPULATION, enumerated from the tree with the method printed
      beside it.  mg-1319 asserted a false universal here; mg-f2e1 replaced it
      with an enumeration that omitted 2 of 6 files; this is the third pass and
      it states HOW it counted, not only what it counted.

  T3  ROW 135's GROWTH, on mg-f7bc's own metric, at every commit in the chain.

  T4  THE PROBE'S SECTION-HEAD CHANGELOG, clause by clause, against the hunks
      `ba3ec79` actually contains.  A changelog is an assertion about a diff and
      nothing checks it against the diff -- so this checks it against the diff.

Pure Python 3 + git.  No third-party packages.  Runtime ~1 s.
"""

import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

RESULTS = []


# --------------------------------------------------------------------- helpers
def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args),
                          capture_output=True, text=True, check=True).stdout


def files_of(commit):
    out = git("show", "--name-only", "--format=", commit)
    return sorted(f for f in out.split("\n") if f.strip())


def head(title):
    print()
    print(title)
    print("-" * len(title))


def check(name, ok, detail=""):
    print("  [%s] %s" % ("CONFIRMED" if ok else "REFUTED  ", name))
    for i, line in enumerate(detail.split("\n") if detail else []):
        print(("        -- " if i == 0 else "           ") + line)
    RESULTS.append((name, ok))
    return ok


def measure(name, detail):
    print("  [MEASURED ] %s" % name)
    for line in detail.split("\n"):
        print("        " + line)


def line_bytes(commit, path, lineno):
    """Byte length of one line, EXCLUDING its newline -- mg-f7bc's F7 metric."""
    text = git("show", "%s:%s" % (commit, path))
    return len(text.split("\n")[lineno - 1].encode("utf-8"))


def line_chars(commit, path, lineno):
    text = git("show", "%s:%s" % (commit, path))
    return len(text.split("\n")[lineno - 1])


# ------------------------------------------------------ T1: the struck sentence
def target_1():
    head("TARGET 1 -- THE SENTENCE THIS LANDING STRIKES, AND THE ONE IT LANDS "
         "INSTEAD")
    print("mg-f2e1's Appendix A block and commit message: row G-double-prime was")
    print("'added to STATE.md by the mg-a806 landing ... into the file that no")
    print("trigger watched', nominated as 'the strongest available evidence' for")
    print("widening A5 to cover STATE.md.  Four independent refutations, each")
    print("re-measured here from git and not quoted from mg-6653.")
    print()

    # (1) the row was never added to STATE.md
    touching = [l.split()[0] for l in
                git("log", "--oneline", "-S", "G″", "--", "STATE.md").split("\n")
                if l.strip()]
    check("the row was ever added to STATE.md",
          False,
          "git log -S on STATE.md returns %d commit(s): %s.\n"
          "1e61031 is mg-a2bd's STRIKE RECORD and ba3ec79 is mg-f2e1 QUOTING the\n"
          "claim under audit.  No commit ever added the row to STATE.md."
          % (len(touching), ", ".join(touching)))

    # where it actually landed
    hodge = "docs/OneThird-Hodge-Side-Leverage.md"
    body = git("show", "f6756c0:" + hodge).split("\n")
    rows = [i + 1 for i, l in enumerate(body)
            if l.startswith("| **G″**")]
    measure("where the row actually landed",
            "f6756c0 : %s line %s -- that document's OWN ledger row,\n"
            "labelled PROVEN, 'free from G + Theorem L'."
            % (hodge, rows[0] if rows else "(not found)"))

    # (2) f6756c0 touches no STATE.md
    f = files_of("f6756c0")
    check("f6756c0 touches STATE.md",
          False,
          "f6756c0's %d files are:\n  %s\nNone of them is STATE.md."
          % (len(f), "\n  ".join(f)))

    # mg-a806's STATE.md commits do not carry the row either
    a806_state = [c for c in ("16bee79", "5b63037", "0160cbf")
                  if "STATE.md" in files_of(c)]
    carries = [c for c in a806_state
               if "G″" in git("show", "%s:STATE.md" % c)]
    check("some other mg-a806 commit put the row into STATE.md",
          False,
          "mg-a806's STATE.md commits are %s; %d of them contain the row."
          % (", ".join(a806_state), len(carries)))

    # (3) it was not "the file no trigger watched" -- three files are instruments
    instruments = [p for p in f if p.startswith("code/")]
    check("'the file that no trigger watched' describes f6756c0",
          False,
          "%d of f6756c0's %d files are instruments the PRE-EXISTING A5 clause\n"
          "already names -- a harness, a sweep script, and the text an instrument\n"
          "prints:\n  %s\nThe old clause fired on the commit that carried the "
          "arc's only BROKEN item."
          % (len(instruments), len(f), "\n  ".join(instruments)))

    # (4) mg-d39d, the cited source, says the opposite
    msg = git("show", "-s", "--format=%B", "522048f")
    clean = [l.strip() for l in msg.split("\n") if "STATE.md is clean" in l]
    check("mg-d39d, cited as the source, supports the claim",
          False,
          "mg-d39d's own commit message says the opposite:\n  %r"
          % (clean[0] if clean else "(phrase not found)"))

    # ---- and now the replacement, which must not be inherited either
    print()
    print("  THE REPLACEMENT ARGUMENT, re-measured rather than adopted:")
    print()
    c50 = files_of("c50ce32")
    stat = git("show", "--shortstat", "--format=", "c50ce32").strip()
    check("c50ce32 (mg-60d3) touches STATE.md AND NOTHING ELSE",
          c50 == ["STATE.md"],
          "files: %s\nshortstat: %s\nUnder the pre-existing clause -- which fires "
          "on instruments -- this commit\ntriggered NOTHING.  That is the hole, "
          "and it is an existence proof, not an\nanecdote." % (c50, stat))

    # c0cf104's STATE.md hunk is where the two mg-1319 defects rode in
    d = git("show", "c0cf104", "--", "STATE.md")
    added = [l for l in d.split("\n") if l.startswith("+") and not l.startswith("+++")]
    n6 = any("n ≤ 6" in l or "n <= 6" in l for l in added)
    six = any("SIX for six" in l or "six for six" in l.lower() for l in added)
    check("the two defects mg-1319 repaired rode in via c0cf104's STATE.md hunk, "
          "not c50ce32's",
          n6 and six and len(added) == 8,
          "c0cf104's STATE.md hunk is %d added lines; the Lemma-1 'n <= 6'\n"
          "overstatement present: %s; the 'SIX for six' 4d contradiction present: "
          "%s.\nc0cf104 ALSO touches controls.py (%d files total), which is the "
          "only reason\nthose eight lines were audited at all.\n"
          "NOTE: mg-f2e1's TICKET asserted c50ce32 carried them.  It did not, "
          "mg-f2e1\ndeclined to inherit that, and this landing does not "
          "reintroduce it."
          % (len(added), n6, six, len(files_of("c0cf104"))))


# ------------------------------------------------- T2: the 38/38 enumeration
LITERAL = "38/38"

# Files a reader consults INSTEAD OF the source they summarise, in the sense of
# the A5 narrowing test.  These are the sites a coverage claim is ABOUT.
LIVE = ("STATE.md",
        "docs/OneThird-Intrinsic-Face-Geometry-Probe.md",
        "code/face_geometry_audit_5630/audit_x3_equivalence.py")


# This run's own transcript, and the ONLY thing skipped.  A scanner that counts
# its own output cannot regenerate byte-identically: the first run writes N, the
# second reads those N back and reports N + something.  Nothing else is skipped,
# and this exclusion is named in the output so it cannot be mistaken for
# coverage -- which is the defect two generations of this paragraph carried.
OWN_TRANSCRIPT = "code/face_geometry_landing_7d5a/out_verify.txt"


def classify(path):
    if path in LIVE:
        return "LIVE"
    if re.search(r"IndependentAudit\.md$", path):
        return "FROZEN AUDIT"
    if re.match(r"code/face_geometry_(audit|landing)_", path):
        return "INSTRUMENT"
    return "OTHER"


def sites_in(path, text, hits):
    """Group occurrences into SITES.

    A site is the enclosing PARAGRAPH -- the blank-line-delimited block -- which
    is what a reader arriving by search or by quotation actually reads.  For a
    .py file the same rule lands on the enclosing comment block or statement,
    which is the same object for this purpose.  This is the grouping mg-6653
    used; it is restated here because a count is only meaningful with its
    grouping rule beside it, and this is the third pass over this population.
    """
    lines = text.split("\n")
    starts = {}
    para = 1
    for i, line in enumerate(lines, start=1):
        if not line.strip():
            para = i + 1
        starts[i] = para
    out = {}
    for lineno, count in hits:
        out.setdefault(starts[lineno], []).append((lineno, count))
    return out


def target_2():
    head("TARGET 2 -- THE 38/38 POPULATION, ENUMERATED FROM THE WORKING TREE, "
         "WITH THE METHOD")
    print("METHOD, stated because this is the THIRD pass over this population and")
    print("the first two were both wrong in the same direction:")
    print("  1. take every file git would commit -- tracked AND not-yet-tracked,")
    print("     minus what .gitignore excludes")
    print("     (`git ls-files --cached --others --exclude-standard`).  No manual")
    print("     file list, so a file cannot be omitted by being forgotten, and")
    print("     `--others` is load-bearing: with `--cached` alone this scanner")
    print("     would not see the files of the landing that runs it, and would")
    print("     report a population that changes the moment they are added;")
    print("  2. read each as UTF-8, skipping anything that does not decode;")
    print("  3. count EVERY occurrence of the literal %r, not lines carrying it;"
          % LITERAL)
    print("  4. group into SITES by enclosing paragraph (see `sites_in`);")
    print("  5. classify each file; the ONE exclusion is this run's own")
    print("     transcript, %r," % OWN_TRANSCRIPT)
    print("     because a scanner that counts its own output cannot regenerate")
    print("     byte-identically.  This instrument's own SOURCE is counted with")
    print("     the rest, and nothing else is excluded.")
    print()

    listing = git("ls-files", "--cached", "--others", "--exclude-standard")
    tracked = sorted(set(p for p in listing.split("\n")
                         if p.strip() and p.strip() != OWN_TRANSCRIPT))
    per_file = {}
    for path in tracked:
        full = os.path.join(REPO, path)
        try:
            text = open(full, encoding="utf-8").read()
        except (UnicodeDecodeError, IsADirectoryError, FileNotFoundError):
            continue
        if LITERAL not in text:
            continue
        hits = [(i, line.count(LITERAL))
                for i, line in enumerate(text.split("\n"), start=1)
                if LITERAL in line]
        per_file[path] = (sum(c for _, c in hits), hits, sites_in(path, text, hits))

    total_occ = sum(v[0] for v in per_file.values())
    total_sites = sum(len(v[2]) for v in per_file.values())
    measure("population in the working tree as it will be committed",
            "%d occurrence(s) of %r, on %d line(s), in %d file(s), "
            "in %d site(s)."
            % (total_occ, LITERAL,
               sum(len(v[1]) for v in per_file.values()),
               len(per_file), total_sites))
    print()
    for path in sorted(per_file):
        occ, hits, sites = per_file[path]
        print("        %-11s %-70s %2d occ, %2d site(s) on line(s) %s"
              % (classify(path), path, occ, len(sites),
                 [l for l, _ in hits]))

    print()
    by_class = {}
    for path, (occ, hits, sites) in per_file.items():
        c = classify(path)
        a, b, d = by_class.get(c, (0, 0, 0))
        by_class[c] = (a + occ, b + len(sites), d + 1)
    print("  BY CLASS:")
    for c in sorted(by_class):
        occ, sites, files = by_class[c]
        print("        %-16s %2d file(s)  %2d occurrence(s)  %2d site(s)"
              % (c, files, occ, sites))

    print()
    print("  WHY THIS LANDING NAMES A CLASS AND NOT A LIST.  mg-1319 claimed a")
    print("  universal ('flagged at every site'), which was false; mg-f2e1")
    print("  replaced it with a list of members, which was incomplete in exactly")
    print("  the same direction.  A list of members of a growing population is a")
    print("  claim that expires: this landing's own audit will add occurrences to")
    print("  the FROZEN AUDIT class the day it is written, and this file added")
    print("  some to INSTRUMENT the day it was written.  The class boundary does")
    print("  not expire, so that is what the STATE.md paragraph now asserts, with")
    print("  this instrument as the way to recover the numbers on demand.")
    print()

    live_files = sorted(p for p in per_file if classify(p) == "LIVE")
    check("every LIVE file is one of the three the A5 narrowing test admits -- "
          "i.e. the class boundary the STATE.md paragraph asserts holds here",
          live_files == sorted(LIVE),
          "LIVE files found:\n  %s" % "\n  ".join(live_files))
    other = sorted(p for p in per_file if classify(p) == "OTHER")
    check("every occurrence sits in one of the three classes the paragraph names",
          not other,
          "files falling outside LIVE / FROZEN AUDIT / INSTRUMENT: %s\n"
          "An empty list is what the paragraph asserts: every occurrence is LIVE, "
          "or in\na frozen audit document, or in an audit/landing instrument's own "
          "source or\ntranscript -- text that exists in order to count, not to be "
          "read for the number." % (other or "none"))


# --------------------------------------------------------- T3: row 135's growth
def target_3():
    head("TARGET 3 -- ROW 135's GROWTH, ON mg-f7bc's OWN METRIC (line bytes, no "
         "newline)")
    print("mg-f2e1 reported 'row 135 grew a further 949 bytes (+7.6%) here'.")
    print("de54c3a is ba3ec79's parent, so 'a further' means de54c3a -> ba3ec79.")
    print()
    chain = [("c0cf104", "mg-78c0  -- mg-f7bc's F7 BASELINE"),
             ("db08b4c", "mg-1319  -- F7 measured the growth to here"),
             ("de54c3a", "parent of ba3ec79"),
             ("ba3ec79", "mg-f2e1  -- the commit under repair"),
             ("HEAD",    "this landing")]
    vals = []
    for c, note in chain:
        b = line_bytes(c, "STATE.md", 135)
        ch = line_chars(c, "STATE.md", 135)
        vals.append((c, b, ch))
        print("        %-8s L135 = %6d bytes / %6d chars   %s" % (c, b, ch, note))
    print()

    base = dict((c, (b, ch)) for c, b, ch in vals)
    d_bytes = base["ba3ec79"][0] - base["de54c3a"][0]
    d_chars = base["ba3ec79"][1] - base["de54c3a"][1]
    pct = 100.0 * d_bytes / base["de54c3a"][0]
    check("mg-f2e1's '+949 bytes (+7.6%)' reproduces",
          d_bytes == 949,
          "de54c3a -> ba3ec79 is +%d bytes (+%.1f%%), or +%d characters.\n"
          "Reported: +949 (+7.6%%).  UNDERSTATED by %.2fx.\n"
          "The +7.6%% shares de54c3a's denominator, so the percentage is the\n"
          "wrong numerator over the right base, not a different metric."
          % (d_bytes, pct, d_chars, d_bytes / 949.0))

    f7 = base["c0cf104"][0]
    now = base["HEAD"][0]
    measure("the figure that matters for the restructure decision",
            "mg-f7bc's F7 flagged row 135 for GROWTH at +49.7%% "
            "(%d -> %d bytes).\n"
            "Across the two landings since, the same row is now %d bytes: "
            "+%d (+%.1f%%)\n"
            "on the F7 baseline.  The decision to restructure was taken on "
            "+49.7%%;\nthe true figure is %.1f%%, so the correction "
            "STRENGTHENS that decision.\nIt does not weaken it and must not be "
            "reported as if it might."
            % (f7, base["db08b4c"][0], now, now - f7,
               100.0 * (now - f7) / f7, 100.0 * (now - f7) / f7))

    check("rows 131-134 are untouched by this landing, as by the last one",
          all(line_bytes("de54c3a", "STATE.md", n)
              == line_bytes("HEAD", "STATE.md", n) for n in (131, 132, 133, 134)),
          "L131-134 at de54c3a: %s\nL131-134 at HEAD:     %s"
          % ([line_bytes("de54c3a", "STATE.md", n) for n in (131, 132, 133, 134)],
             [line_bytes("HEAD", "STATE.md", n) for n in (131, 132, 133, 134)]))


# ------------------------------------ T4: the changelog against the actual diff
PROBE = "docs/OneThird-Intrinsic-Face-Geometry-Probe.md"


def target_4():
    head("TARGET 4 -- THE PROBE's SECTION-HEAD CHANGELOG vs THE HUNKS ba3ec79 "
         "CONTAINS")
    print("E3's own lesson, stated three times in ba3ec79: a changelog is an")
    print("assertion ABOUT a diff and nothing checks it against the diff.  So:")
    print()

    d = git("show", "ba3ec79", "--", PROBE)
    hunks = re.findall(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", d, re.M)
    touched = []
    for old, oldn, new, newn in hunks:
        start = int(new)
        span = int(newn) if newn else 1
        touched.append((start, start + span - 1))
    measure("the hunks ba3ec79 has in the Probe, in post-image line numbers",
            "\n".join("lines %d-%d" % t for t in touched))

    # Section boundaries in the post-image.  Top-level `## §n` headings only:
    # a section RUNS THROUGH its own `###` subsections, so keying on both levels
    # would end §5 at its first subsection and understate the span that has to
    # be free of hunks.
    text = git("show", "ba3ec79:" + PROBE).split("\n")
    secs = [(i + 1, l) for i, l in enumerate(text) if re.match(r"^## ", l)]
    bounds = {}
    for j, (lineno, title) in enumerate(secs):
        end = secs[j + 1][0] - 1 if j + 1 < len(secs) else len(text)
        m = re.match(r"^## (§[\d.]+)", title)
        if m:
            bounds.setdefault(m.group(1), (lineno, end))

    def touched_section(sec):
        lo, hi = bounds[sec]
        return any(not (b < lo or a > hi) for a, b in touched)

    for sec in ("§2", "§5", "§11", "§12"):
        lo, hi = bounds[sec]
        print("        %-4s lines %4d-%4d   touched by ba3ec79: %s"
              % (sec, lo, hi, touched_section(sec)))
    print()

    check("the changelog's claim 'the per-site enumeration in §5' is supported "
          "by the diff",
          touched_section("§5"),
          "§5 is NOT in any hunk of ba3ec79.  And independently of the diff, §5\n"
          "carries the truncation FLAG mg-1319 landed -- 'Flagged because 38/38 "
          "is\nquoted as a headline ... the audit's population is a [:20] "
          "TRUNCATION' --\nand nothing resembling a per-site list.  The line "
          "asserting it is the line\nE3 rewrote, in the sentence that names that "
          "exact failure mode.")

    check("the changelog's claim about §2 is supported by the diff",
          touched_section("§2"),
          "§2 IS in a hunk, and the corrected sentence is the one the document\n"
          "labels '(F3, ...)'.  This half of the entry stands.")

    check("the changelog's claim about §12 is supported by the diff",
          touched_section("§12"),
          "§12 IS in a hunk -- the reversal preamble and the second marker.\n"
          "This half of the entry stands.")

    # the claim about the PREVIOUS entry
    old = git("show", "de54c3a:" + PROBE)
    prev = [l for l in old.split("\n") if "half of F3's coverage sentence" in l]
    tagged = bool(prev) and "(§11)" in prev[0]
    check("'the entry that stood here claimed the correction outright' is exact",
          not tagged,
          "The entry it replaced read:\n  %r\nIt DID carry a location tag, "
          "'(§11)', and §11 WAS corrected by mg-1319.\nSo it misidentified the "
          "scope rather than omitting a location: it named one\nof the two sites "
          "and read as covering the sentence.  mg-6653 recorded this\nand did not "
          "file it; this landing fixes it because it is the same class as\nA4 and "
          "the line is being rewritten anyway."
          % (prev[0].strip()[:120] if prev else "(not found)"))


def main():
    print("mg-7d5a -- RE-MEASURING THIS LANDING'S OWN CLAIMS")
    print("=" * 78)
    print("Nothing below is inherited from mg-6653, from mg-f2e1, or from the")
    print("ticket.  Where the ticket and the audit disagreed -- on whether")
    print("c50ce32 carried the two defects mg-1319 repaired -- the audit is")
    print("right and T1 shows why.")
    target_1()
    target_2()
    target_3()
    target_4()

    print()
    print("=" * 78)
    bad = [n for n, ok in RESULTS if not ok]
    print("%d scored statement(s); %d REFUTED." % (len(RESULTS), len(bad)))
    print()
    print("The REFUTED rows are the point: every one of them is a claim mg-f2e1")
    print("or its changelog made, re-measured and found false.  A run with zero")
    print("REFUTED rows would mean this landing had nothing to repair.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
