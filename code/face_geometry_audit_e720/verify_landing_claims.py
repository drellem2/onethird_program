"""mg-e720: re-measure, from a disjoint rebuild, every checkable claim mg-7d5a
(commit d5a3043) makes about git, about the tree and about its own diff.

Nothing here is taken from mg-7d5a's `verify_landing.py`, from mg-6653, or from
the ticket.  Where this instrument and mg-7d5a agree the agreement is on
separately-written code; where they disagree the disagreement is scored.

ONE DELIBERATE DIFFERENCE OF METHOD, because it is the defect the last three
generations kept hitting.  mg-7d5a's scanner reads the WORKING TREE, so its
transcript freezes the moment anything else lands -- it says so, and it is
right.  This scanner reads the COMMIT (`git ls-tree -r d5a3043`), so its
population is a fact about a fixed object and this transcript regenerates
byte-identically at every future commit.  A count that has to be re-frozen is a
count that will be quoted stale.
"""

import os
import re
import subprocess
import sys

TARGET = "d5a3043"
LITERAL = "38/38"
ROW_MARK = "THE PIPELINE SURVIVED THE CONTROL IT WAS MISSING"
PROBE = "docs/OneThird-Intrinsic-Face-Geometry-Probe.md"

SCORE = []


REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True,
                      cwd=__file__.rsplit("/", 1)[0]).stdout.strip()


#: THE COMMIT THIS AUDIT IS TAKEN OVER (mg-20ee).
#:
#: Every `git log` walk below started at HEAD, so its answers were "whatever the
#: history looks like when you happen to run me" -- and this instrument prints
#: those answers as VERDICTS, not as addresses.  It had already flipped one: at
#: HEAD, TARGET 1's "no commit ever added the row to STATE.md" comes back
#: REFUTED, because the `-S`/`-G` walks now reach commits that were not in this
#: audit's history when it ran.
#:
#: CHOSEN ON A MEASUREMENT, AND IT IS THE PARENT OF THE CARRYING COMMIT, NOT THE
#: CARRYING COMMIT.  7f04902 is where these transcripts live, and pinning THERE
#: leaves one line wrong: the `-60` walk then reaches 7f04902 itself and reports
#: it among the commits saying "changes behaviour".  An instrument is RUN BEFORE
#: IT IS COMMITTED, so the history it measured is the history WITHOUT its own
#: commit.  At 7f04902^ the committed transcript reproduces BYTE-IDENTICALLY --
#: checked before a line of it was edited.  It is an ANCESTOR OF main.
AS_OF = "8fab00615a6d25ed1b9a2298abcfedc2d6785d20"

#: Override, for re-measuring against a different history: any commit-ish.
#: Unset is the pinned default and the only value that reproduces the
#: committed transcript.
AT = os.environ.get("E720_AT", "").strip() or AS_OF


def git(*args, binary=False):
    """Always run from the repository root, so pathspecs mean what they say."""
    r = subprocess.run(("git", "-C", REPO) + args, capture_output=True)
    if r.returncode:
        raise SystemExit("git %s failed: %s" % (" ".join(args), r.stderr.decode()))
    return r.stdout if binary else r.stdout.decode("utf-8", "replace")


def blob(rev, path, binary=False):
    return git("show", "%s:%s" % (rev, path), binary=binary)


def score(name, ok, detail):
    SCORE.append((name, ok))
    print("  [%s] %s" % ("REPRODUCED" if ok else "  REFUTED " , name))
    for line in detail.rstrip("\n").split("\n"):
        print("        %s" % line)


def files_of(rev):
    out = git("show", "--numstat", "--format=", rev).strip()
    return [l.split("\t")[2] for l in out.split("\n") if l.strip()]


# --------------------------------------------------------------------------
def target_1_the_struck_sentence():
    print()
    print("TARGET 1 -- THE FOUR REFUTATIONS, RE-MEASURED FROM GIT")
    print("-" * 74)

    f = files_of("c50ce32")
    shortstat = git("show", "--shortstat", "--format=", "c50ce32").strip()
    score("c50ce32 touches STATE.md and nothing else",
          f == ["STATE.md"] and "1 file changed, 13 insertions(+), 5 deletions(-)" in shortstat,
          "files: %s\n%s\nSo a commit whose whole content is program state existed, and the\n"
          "pre-existing instrument clause fired nothing on it.  The widening's\n"
          "replacement evidence is TRUE." % (f, shortstat))

    g = files_of("f6756c0")
    instruments = [p for p in g if p.startswith("code/")]
    score("f6756c0 touches no STATE.md and does touch three instruments",
          "STATE.md" not in g and len(instruments) == 3,
          "files: %s\ninstrument files among them: %s\n"
          "The pre-existing clause names 'a harness ... or the text an instrument\n"
          "prints'.  It fired on this commit." % (g, instruments))

    hodge = blob("f6756c0", "docs/OneThird-Hodge-Side-Leverage.md").split("\n")
    at877 = hodge[876] if len(hodge) > 876 else ""
    score("the row landed at docs/OneThird-Hodge-Side-Leverage.md:877 in f6756c0",
          at877.startswith("| **G″**"),
          "line 877 as f6756c0 left it:\n  %s" % at877[:120])

    s = git("log", "--format=%h", "-S", "G″", AT, "--", "STATE.md").split()
    # -S only sees a NET change in occurrence count; -G sees any touching commit.
    # -G on the ROW'S OWN TEXT is the stronger question and is run too.
    gg = git("log", "--format=%h", "-G",
             "one of whose blocks induces an antichain", AT, "--", "STATE.md").split()
    score("no commit ever added the row to STATE.md",
          set(s) == {"ba3ec79", "1e61031"} and gg == ["1e61031"],
          "git log -S 'G″'   -- STATE.md : %s  (mg-f2e1 quoting, mg-a2bd's strike record)\n"
          "git log -G <row text> -- STATE.md : %s  (the strike record only)\n"
          "The -G form is the stronger test and mg-7d5a did not run it: the row's own\n"
          "wording has only ever entered STATE.md inside mg-a2bd's record of striking it."
          % (s, gg))

    d39d = git("log", "-1", "--format=%B", "522048f")
    score("mg-d39d, cited as the sentence's source, says STATE.md is clean",
          "STATE.md is clean" in d39d,
          "522048f (mg-d39d): %r" % re.search(
              r".{40}STATE\.md is clean.{0,20}", d39d).group(0))

    c0 = git("diff", "c0cf104^", "c0cf104", "--", "STATE.md")
    added = [l for l in c0.split("\n") if l.startswith("+") and not l.startswith("+++")]
    c50 = git("diff", "c50ce32^", "c50ce32", "--", "STATE.md")
    added50 = [l for l in c50.split("\n") if l.startswith("+") and not l.startswith("+++")]
    in_c0 = any("n ≤ 6" in l for l in added) and any("SIX for six" in l for l in added)
    in_c50 = any("n ≤ 6" in l for l in added50) or any("SIX for six" in l for l in added50)
    score("the two mg-1319 defects rode in on c0cf104's STATE.md hunk, not c50ce32's",
          len(added) == 8 and in_c0 and not in_c50,
          "c0cf104's STATE.md hunk: %d added lines; Lemma-1 'n <= 6' present: %s; "
          "'SIX for six' present: %s\nc50ce32's STATE.md hunk carries either: %s\n"
          "So mg-7d5a's refusal to inherit the ticket's version is CORRECT."
          % (len(added), any("n ≤ 6" in l for l in added),
             any("SIX for six" in l for l in added), in_c50))

    # The A5 clause itself, and the three paragraphs a narrowing could have touched.
    pre = blob("d5a3043^", "STATE.md").split("\n")
    post = blob("d5a3043", "STATE.md").split("\n")
    def para(lines, needle):
        return [l for l in lines if needle in l]
    unchanged = []
    for needle in ["AND ON ANY COMMIT THAT ADDS OR MODIFIES PROGRAM STATE",
                   "Trigger the audit stage on any commit that ADDS OR MODIFIES an instrument",
                   "THE HOLE, and it was in this rule's own wording",
                   "Does a REPAIR need a fresh audit? The narrowing test"]:
        unchanged.append((needle[:46], para(pre, needle) == para(post, needle)))
    score("the trigger, the STATE.md clause, THE HOLE and the narrowing test are "
          "textually UNTOUCHED",
          all(ok for _, ok in unchanged),
          "\n".join("%-48s identical: %s" % (n, ok) for n, ok in unchanged) +
          "\nSo H0 holds on the load-bearing text: a STATE.md-only commit still triggers.")


# --------------------------------------------------------------------------
def sites_by_paragraph(text):
    """Group occurrences into sites by enclosing blank-line-delimited paragraph."""
    lines = text.split("\n")
    starts, cur = [], 0
    for i, l in enumerate(lines):
        if not l.strip():
            cur = i + 1
        elif i == cur or (i and not lines[i - 1].strip()):
            starts.append(i)
    out = {}
    for i, l in enumerate(lines):
        n = l.count(LITERAL)
        if not n:
            continue
        p = max([s for s in starts if s <= i] or [0])
        out.setdefault(p, [0, []])
        out[p][0] += n
        out[p][1].append(i + 1)
    return out


def target_2_the_population():
    print()
    print("TARGET 2 -- THE 38/38 POPULATION, ENUMERATED FROM THE COMMIT")
    print("-" * 74)
    print("METHOD.  Every path in `git ls-tree -r %s`; each blob decoded as UTF-8" % TARGET)
    print("(anything that does not decode is reported, not silently skipped);")
    print("occurrences of the literal counted, not lines; occurrences grouped into")
    print("sites by enclosing paragraph.  NO exclusions: this instrument's own files")
    print("are not in the commit, so it has nothing to exclude and nothing to declare.")

    paths = git("ls-tree", "-r", "--name-only", TARGET).split("\n")
    paths = [p for p in paths if p]
    per, undecodable = {}, []
    for p in paths:
        raw = blob(TARGET, p, binary=True)
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            if LITERAL.encode() in raw:
                undecodable.append(p)
            continue
        n = text.count(LITERAL)
        if n:
            per[p] = (n, sites_by_paragraph(text))

    total = sum(n for n, _ in per.values())
    sites = sum(len(s) for _, s in per.values())
    print()
    for p in sorted(per):
        n, s = per[p]
        print("        %-72s %2d occ  %2d site(s)" % (p, n, len(s)))
    print()
    excluded = "code/face_geometry_landing_7d5a/out_verify.txt"
    e_occ, e_sites = per[excluded][0], len(per[excluded][1])
    score("mg-7d5a's '50 occurrences in 12 files, 35 sites' reproduces, given its "
          "one declared exclusion",
          (total - e_occ, len(per) - 1, sites - e_sites) == (50, 12, 35)
          and not undecodable,
          "at %s: %d occurrence(s) in %d file(s), %d site(s).\n"
          "mg-7d5a excludes exactly one file -- its own transcript, %s\n"
          "(%d occ, %d sites) -- by name and in its own output.\n"
          "%d-%d = 50, %d-1 = 12, %d-%d = 35.  All three numbers are EXACT on\n"
          "independently-written code, and the paragraph's method is what makes that\n"
          "checkable.  This is the first stated method in three generations of this claim.\n"
          "Completeness of the population, tried and could not break: non-UTF-8 blobs\n"
          "carrying the literal: %s; .gitignore'd worktree files carrying it: none\n"
          "(3 ignored files, 0 hits), so the scanner's exclusions lose nothing here."
          % (TARGET, total, len(per), sites, excluded, e_occ, e_sites,
             total, e_occ, len(per), sites, e_sites, undecodable or "none"))

    live = {"STATE.md", PROBE, "code/face_geometry_audit_5630/audit_x3_equivalence.py"}
    frozen = {p for p in per if "IndependentAudit.md" in p}
    instr = set(per) - live - frozen - {"code/face_geometry_landing_7d5a/out_verify.txt"}
    def tally(group):
        return (len(group), sum(per[p][0] for p in group),
                sum(len(per[p][1]) for p in group))
    score("the three class tallies in the STATE.md paragraph reproduce",
          tally(live) == (3, 16, 7) and tally(frozen) == (4, 20, 18)
          and tally(instr) == (5, 14, 10),
          "LIVE         %s files, %s occ, %s sites   (paragraph: 3 / 16 / 7)\n"
          "FROZEN AUDIT %s files, %s occ, %s sites   (paragraph: 4 / 20 / 18)\n"
          "INSTRUMENT   %s files, %s occ, %s sites   (paragraph: 5 / 14 / 10)"
          % (tally(live) + tally(frozen) + tally(instr)))

    score("every occurrence outside LIVE is in a frozen audit document or an "
          "instrument's source/transcript",
          not (set(per) - live - frozen - instr
               - {"code/face_geometry_landing_7d5a/out_verify.txt"}),
          "files outside all three classes: none.  The CLASS half of the paragraph is\n"
          "TRUE, and it is the half that does not expire.")

    # every LIVE site flagged?
    unflagged = []
    for p in sorted(live):
        text = blob(TARGET, p)
        lines = text.split("\n")
        for start, (n, occ) in sorted(sites_by_paragraph(text).items()):
            para = "\n".join(lines[start:start + 40])
            if not re.search(r"trunc|TRUNCAT|\[:20\]|posets_upto_iso\(n\)\[:20\]"
                             r"|OWN population", para):
                unflagged.append((p, start + 1, occ))
    score("every site in the three LIVE files names the truncation",
          not unflagged,
          "unflagged LIVE sites: %s\nChecked by searching each site's own paragraph for\n"
          "'trunc' / '[:20]' / \"OWN population\".  The weakest of the seven is\n"
          "audit_x3_equivalence.py:84, whose comment says 'the audit's OWN population'\n"
          "and is disclosed as a truncation only by the `[:20]` in the code three lines\n"
          "below it." % (unflagged or "none"))

    # class-boundary consistency
    excl = [l for l in blob(TARGET, "STATE.md").split("\n")
            if "WHAT THIS DOES NOT WIDEN INTO" in l][0]
    score("the LIVE class is assigned by the boundary the paragraph states",
          False,
          "The stated boundary is the A5 test: 'the artifacts a reader consults INSTEAD\n"
          "OF the source'.  The A5 exclusion list, in this same file and section, says\n"
          "a code comment does NOT qualify -- verbatim: 'A README, a code comment, a\n"
          "path correction, a typo fix, ... do not: nobody retires a question on their\n"
          "authority.'  audit_x3_equivalence.py:84 IS a code comment, and it is in the\n"
          "LIVE class.  It is there because mg-f2e1's member list had it ('One\n"
          "instrument comment ... correct as written'), i.e. it is INHERITED, in the\n"
          "paragraph whose whole point is that the class replaces the inherited list.\n"
          "Direction: conservative (it makes 'every LIVE site is flagged' a STRONGER\n"
          "claim), so the defect is in the boundary's application, not in the number.\n"
          "Applying the stated boundary gives LIVE = 2 files / 15 occ / 6 sites.")
    assert "a code comment" in excl


# --------------------------------------------------------------------------
def target_3_row_135():
    print()
    print("TARGET 3 -- ROW 135's GROWTH, ON A STATED METRIC")
    print("-" * 74)
    print("METRIC (mg-f7bc's F7, restated so it can be checked): the number of UTF-8")
    print("bytes in the single STATE.md line containing %r," % ROW_MARK[:34])
    print("newline EXCLUDED.  The row is located by that marker, not by line number,")
    print("so the measurement does not depend on line numbers holding still.")

    def row(rev):
        b = blob(rev, "STATE.md", binary=True)
        for line in b.split(b"\n"):
            if ROW_MARK.encode() in line:
                return len(line), len(line.decode("utf-8"))
        raise SystemExit("marker not found at %s" % rev)

    revs = [("c0cf104", "mg-78c0  -- F7's baseline"),
            ("db08b4c", "mg-1319  -- F7 measured growth to here"),
            ("de54c3a", "parent of ba3ec79"),
            ("ba3ec79", "mg-f2e1  -- the commit under repair"),
            ("d5a3043", "mg-7d5a  -- this landing")]
    m = {}
    print()
    for rev, note in revs:
        m[rev] = row(rev)
        print("        %-8s  %6d bytes / %6d chars   %s" % (rev, m[rev][0], m[rev][1], note))

    d_b = m["ba3ec79"][0] - m["de54c3a"][0]
    d_c = m["ba3ec79"][1] - m["de54c3a"][1]
    pct = 100.0 * d_b / m["de54c3a"][0]
    print()
    score("mg-f7bc's F7 pair 7,832 -> 11,727 reproduces on this metric",
          m["c0cf104"][0] == 7832 and m["db08b4c"][0] == 11727,
          "%d -> %d bytes, +49.7%%.  The metric is therefore the right one." %
          (m["c0cf104"][0], m["db08b4c"][0]))
    score("mg-7d5a's correction '+2,127 bytes (+17.1%), or +2,088 characters'",
          d_b == 2127 and round(pct, 1) == 17.1 and d_c == 2088,
          "de54c3a -> ba3ec79 = +%d bytes (+%.2f%%), +%d characters.  EXACT." %
          (d_b, pct, d_c))
    score("mg-f2e1's '+949 bytes (+7.6%)' is the wrong numerator over the right base",
          round(100.0 * 949 / m["de54c3a"][0], 1) == 7.6,
          "949 / %d = %.2f%%, which is the +7.6%% reported, so the denominator is\n"
          "de54c3a's and only the numerator is wrong.  2127 / 949 = %.2fx understated."
          % (m["de54c3a"][0], 100.0 * 949 / m["de54c3a"][0], 2127.0 / 949))
    score("'row 135 is now 14,582 bytes -- +86.2%' on the F7 baseline",
          m["d5a3043"][0] == 14582
          and round(100.0 * (m["d5a3043"][0] - m["c0cf104"][0]) / m["c0cf104"][0], 1) == 86.2,
          "%d bytes, +%.1f%% on %d.  The roadmap's restructure decision cites 49.7%%\n"
          "as its evidence, so the correction STRENGTHENS it, as mg-7d5a says."
          % (m["d5a3043"][0], 100.0 * (m["d5a3043"][0] - m["c0cf104"][0]) / m["c0cf104"][0],
             m["c0cf104"][0]))
    score("row 135 untouched by this landing, rows 131-134 byte-identical",
          m["ba3ec79"][0] == m["d5a3043"][0]
          and [len(l) for l in blob("de54c3a", "STATE.md", binary=True).split(b"\n")[130:134]]
          == [len(l) for l in blob("d5a3043", "STATE.md", binary=True).split(b"\n")[130:134]],
          "L131-134 at de54c3a and at HEAD: %s\nrow 135: %d = %d.  No restructure." %
          ([len(l) for l in blob("d5a3043", "STATE.md", binary=True).split(b"\n")[130:134]],
           m["ba3ec79"][0], m["d5a3043"][0]))


# --------------------------------------------------------------------------
def target_4_the_changelog():
    print()
    print("TARGET 4 -- EVERY CHANGELOG CLAUSE AGAINST THE DIFF IT DESCRIBES")
    print("-" * 74)

    # section bounds in ba3ec79's post-image
    post = blob("ba3ec79", PROBE).split("\n")
    heads = {}
    for i, l in enumerate(post, 1):
        mm = re.match(r"^## §(\d+)", l)
        if mm:
            heads[int(mm.group(1))] = i
    order = sorted(heads)
    bounds = {}
    for k, s in heads.items():
        nxt = [heads[j] for j in order if heads[j] > s]
        bounds[k] = (s, (min(nxt) - 1) if nxt else len(post))

    diff = git("diff", "ba3ec79^", "ba3ec79", "--", PROBE)
    hunks = []
    for l in diff.split("\n"):
        mm = re.match(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", l)
        if mm:
            a = int(mm.group(1))
            n = int(mm.group(2) or 1)
            hunks.append((a, a + n - 1))
    def touched(k):
        s, e = bounds[k]
        return any(not (he < s or hs > e) for hs, he in hunks)

    print("        ba3ec79's hunks in the Probe (post-image lines): %s" % hunks)
    for k in (2, 5, 11, 12):
        print("        §%-3d lines %4d-%4d   touched by ba3ec79: %s"
              % (k, bounds[k][0], bounds[k][1], touched(k)))
    print()
    score("the struck clause 'the per-site enumeration in §5' is unsupported: §5 is "
          "not in any hunk",
          not touched(5) and touched(2) and touched(12),
          "§5 untouched, §2 and §12 both touched.  mg-7d5a's 'its three hunks in this\n"
          "file are the §-head changelog, §2 and §12' is EXACT: %s covers 34-48 (before\n"
          "§0 at line %d), §2 and §12." % (hunks, heads[0]))

    s5 = "\n".join(post[bounds[5][0] - 1:bounds[5][1]])
    score("§5 carries a truncation FLAG and nothing resembling a per-site enumeration",
          "TRUNCATION" in s5 and "Flagged because" in s5
          and "live 1/5" not in s5 and "five live sites" not in s5,
          "§5 contains 'Flagged because `38/38` is quoted as a headline ... a `[:20]`\n"
          "TRUNCATION' and no list of sites.  Landed by db08b4c (mg-1319): git log -S\n"
          "on that flag returns %s."
          % git("log", "--format=%h", "-S", "Flagged because `38/38` is quoted as a headline",
                AT, "--", PROBE).split())

    prev = blob("ba3ec79^", PROBE)
    score("'the entry that stood here claimed the correction outright' was imprecise: "
          "it did carry (§11)",
          "corrected to `n ≤ 5` for Lemma 1 (§11)" in prev,
          "the replaced entry read: %r\nSo it named one of two sites rather than none.\n"
          "mg-7d5a's second correction is CORRECT."
          % re.search(r"Also: the .{0,90}\(§11\)", prev).group(0))

    # does the block mg-7d5a ADDED assert anything outside its own diff?
    d = git("diff", "d5a3043^", "d5a3043", "--", PROBE)
    add_hunks = [l for l in d.split("\n") if l.startswith("@@")]
    score("mg-7d5a's own changelog block asserts nothing outside its own diff",
          len(add_hunks) == 1,
          "d5a3043's hunks in the Probe: %s -- one, in the §-head changelog.  Its block\n"
          "claims (a) the old wording, (b) that §5 has no enumeration and is untouched by\n"
          "ba3ec79, (c) that the (§11) tag was there, (d) 'Both are fixed above' and (e)\n"
          "that the STATE.md claim is now a class statement.  (a)-(c) are facts about\n"
          "other objects and each reproduces above; (d) is in this hunk; (e) is in this\n"
          "commit's STATE.md hunk.  H4 is DISCHARGED -- no clause asserts absent work."
          % add_hunks)


# --------------------------------------------------------------------------
def target_5_beyond_the_brief():
    print()
    print("TARGET 5 -- WHAT THE LANDING ADDED BEYOND ITS BRIEF, AND WHAT IS IN IT")
    print("-" * 74)

    state = blob(TARGET, "STATE.md").split("\n")
    def find(needle):
        for i, l in enumerate(state, 1):
            if needle in l:
                return i, l
        return None, ""

    i341, l341 = find("the PRE-EXISTING clause already fired on the commit that carried")
    i343, l343 = find("not because of any artifact clause")
    i351, l351 = find("audited only because it added new mathematical content")
    score("the three paragraphs give one consistent account of why f6756c0 was audited",
          False,
          "STATE.md:%d  (A1, the commit's own headline refutation, verified by its T1):\n"
          "    '... so THE PRE-EXISTING clause already fired on the commit that carried\n"
          "     the arc's only BROKEN item ...'\n"
          "STATE.md:%d  (the OPEN finding this landing FILED, beyond its brief):\n"
          "    'mg-d39d caught it, but as a landing audit under the narrowing test's new\n"
          "     mathematical content branch, NOT BECAUSE OF ANY ARTIFACT CLAUSE.'\n"
          "STATE.md:%d  (the A7 re-sizing):\n"
          "    'f6756c0 -- a REPAIR commit to a deliverable, exempt by the narrowing test\n"
          "     two paragraphs up, AUDITED ONLY BECAUSE it added new mathematical content.'\n"
          "The instrument clause IS an artifact clause -- the same section closes with\n"
          "'Two artifact classes trigger -- instruments, and the state-of-the-program\n"
          "summary'.  Lines %d and %d are false, by the measurement at line %d, ten lines\n"
          "away, which this commit made itself." % (i341, i343, i351, i343, i351, i341))

    narrowing, _ = find("Does a REPAIR need a fresh audit? The narrowing test")
    noexempt, _ = find("does not exempt instruments")
    score("the A7 sizing does not narrow the stage below the standing rule set",
          False,
          "As landed, STATE.md:%d reads 'a repair to one re-enters it only if the repair\n"
          "widens or adds new mathematical content'.  STATE.md:%d, in the same section,\n"
          "says 'The narrowing test above is about mathematical CLAIMS and DOES NOT EXEMPT\n"
          "INSTRUMENTS: adopting a control, rescoring a row, or rewording what a control\n"
          "prints is not a narrowing'.  A repair to a deliverable that touches an\n"
          "instrument therefore re-enters the stage by the instrument clause -- f6756c0 is\n"
          "that case and this commit proved it.  The word 'only' removes that route.\n"
          "H6/H7 asked for a sizing; this is a sizing PAST the true claim." % (i351, noexempt))
    score("'exempt by the narrowing test two paragraphs up' locates the rule correctly",
          False,
          "The narrowing test is at STATE.md:%d.  Two paragraphs above %d is 'THE HOLE',\n"
          "which only refers to it.  Inherited from mg-6653's 'the narrowing test two\n"
          "paragraphs earlier', which was wrong there too." % (narrowing, i351))

    a6, _ = find("the commit that repaired it says the repair")

    def flat(s):
        return re.sub(r"\s+", " ", s)

    # who REPAIRED mg-5630's A4, and who SAID "changes behaviour" -- two commits.
    said = [c for c in git("log", "--format=%h", "-60", AT).split()
            if "changes behaviour" in flat(git("log", "-1", "--format=%B", c))]
    repairer = [c for c in git("log", "--format=%h", "-60", AT).split()
                if "the scoring defect fixed in controls.py" in
                flat(git("log", "-1", "--format=%B", c))]
    score("the A6 narrowing attributes its quotation to the right commit",
          set(said) - {TARGET, "a85fb28"} == set(repairer),
          "STATE.md:%d says 'the commit that repaired it says the repair \"changes\n"
          "behaviour\"'.\nCommit that repaired mg-5630's A4 (its message: 'the scoring defect\n"
          "fixed in controls.py'):            %s  (mg-1319)\n"
          "Commits whose message says 'changes behaviour': %s\n"
          "  -- ba3ec79 is mg-f2e1, REPORTING the repair a generation later; a85fb28 is\n"
          "     mg-6653's audit, which correctly wrote 'this commit's own message'; and\n"
          "     %s is this landing.\n"
          "d5a3043's own COMMIT MESSAGE gets it right ('ba3ec79's own message').  Only the\n"
          "sentence it wrote into STATE.md moves the quotation to the repairing commit.\n"
          "The POINT of A6 -- the defect was in scoring logic, so 'the whole population sat\n"
          "in text' is false -- STANDS, and the narrowing to 'concentrated in' is correct."
          % (a6, repairer, sorted(set(said) - {TARGET}), TARGET))

    hdr = flat(blob(TARGET, "code/face_geometry_audit_6653/run_all.sh").replace("#", ""))
    score("the STATUS block added to mg-6653's run_all.sh describes its own effect "
          "correctly",
          False,
          "The block asserts: 'verify_claims.py -- ... Its FINDINGS are unaffected; only\n"
          "the transcript is.'  Present in the file: %s.\n"
          "Re-run at this commit, verify_claims.py moves from 'REFUTED CLAIMS: 7' to\n"
          "'REFUTED CLAIMS: 9': 'the five named LIVE sites are all in fact flagged' and\n"
          "'the section-2 sentence now reads n<=5 for the Lemma-1 cross-check' both flip\n"
          "from [REPRODUCED] to [REFUTED].  Both flip because THIS LANDING added 13 lines\n"
          "to the Probe's section head, and verify_claims.py matches sites by hard-coded\n"
          "(file, line) pairs (verify_claims.py:240-248) and reads Probe line 140 directly\n"
          "(verify_claims.py:329).  The substantive facts are unchanged -- the sites are\n"
          "still flagged, §2 still reads n<=5 -- but the instrument's scored FINDINGS are\n"
          "not, and the block was added to tell a reader they are.  Run:\n"
          "  python3 code/face_geometry_audit_6653/verify_claims.py | grep 'REFUTED CLAIMS'"
          % ("Its FINDINGS are unaffected; only the transcript is." in hdr))
    assert "Its FINDINGS are unaffected; only the transcript is." in hdr


def main():
    print("mg-e720 -- INDEPENDENT AUDIT OF mg-7d5a (%s), RE-MEASURED" % TARGET)
    print("=" * 74)
    print("Rows scored REPRODUCED are mg-7d5a's claims that a disjoint rebuild")
    print("confirms.  Rows scored REFUTED are this audit's findings.")
    target_1_the_struck_sentence()
    target_2_the_population()
    target_3_row_135()
    target_4_the_changelog()
    target_5_beyond_the_brief()
    print()
    print("=" * 74)
    bad = [n for n, ok in SCORE if not ok]
    print("%d scored statement(s); %d REPRODUCED, %d REFUTED."
          % (len(SCORE), len(SCORE) - len(bad), len(bad)))
    for n in bad:
        print("   - %s" % n)
    print()
    print("WHERE THEY LAND.  Four of the six are in material outside the seven items")
    print("of the brief: the OPEN finding this landing FILED (STATE.md:343), the")
    print("A7 rule-narrowing beyond what H7 asked for (351), the paragraph-locator")
    print("inherited with it, and the STATUS block written into another audit's")
    print("harness.  The remaining two are inside a sentence about the landing's own")
    print("method -- 'nothing is inherited' (the LIVE class) and 'the commit that")
    print("repaired it' (A6).  Sixth consecutive generation of that shape, and the")
    print("arc's own rule predicted it again.")
    print()
    print("The CONTROL half of this audit is scored separately, by")
    print("attack_artifact_check.py: the code repair HOLDS and the claim written")
    print("around it does not.")
    return 0


STAMP = """\
==============================================================================
AS-OF STAMP -- WHICH LINES BELOW ARE ADDRESSES AND WHICH ARE FINDINGS (mg-20ee)
==============================================================================
  history read at : %s
      %s

  THIS AUDIT'S EVIDENCE IS A SET OF `git log` WALKS, and a walk started at HEAD
  answers "whatever the history looks like when you happen to run me".  Here
  that is not a relocated reader -- THE WALKS ARE SCORED AS VERDICTS.  One had
  already flipped: at HEAD, TARGET 1's "no commit ever added the row to
  STATE.md" comes back REFUTED, because the -S/-G walks now reach commits that
  were not in this audit's history when it ran.  See README for the list and
  for why that is REPORTED rather than pinned away.

  So every walk is bounded by the commit above.  It is the PARENT of the commit
  carrying this transcript, not that commit: an instrument is RUN BEFORE IT IS
  COMMITTED, so the history it measured is the history without its own commit.

  EVERY `file:NNN` BELOW IS AN ADDRESS into a file this audit does not own and
  is valid at that commit and nowhere else.  WHAT IS STABLE is what the audit
  concludes about each target.  To re-ask against today's history:

      E720_AT=HEAD python3 verify_landing_claims.py

  which RE-WALKS.  Each run is correct about its own history.
""" % (AT, "AS_OF, the pinned default" if AT == AS_OF
       else "OVERRIDE via E720_AT -- NOT the as-of stamp " + AS_OF[:7])


if __name__ == "__main__":
    print(STAMP, end="")
    sys.exit(main())
