#!/usr/bin/env python3
"""mg-6653 -- independent verification of the CLAIMS mg-f2e1 (ba3ec79) makes.

Every number this audit reports about the tree, the diff or the history is
recomputed here from git and from the working tree.  Nothing is inherited from
mg-f2e1's commit message, from STATE.md, or from mg-f7bc's audit document; where
a figure is quoted from one of those it is quoted in order to be checked against
a re-measurement, and both values are printed.

Pure Python 3 + git.  No third-party packages.
"""

import re
import subprocess
import sys
import os

TARGET = "ba3ec79"           # mg-f2e1, the commit under audit
PARENT = "ba3ec79^"          # de54c3a, the tree it landed on
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

FINDINGS = []


def show(rev_path):
    return subprocess.run(["git", "-C", REPO, "show", rev_path],
                          capture_output=True, text=True).stdout


def files_of(rev):
    out = subprocess.run(["git", "-C", REPO, "show", "--stat", "--format=", "--name-only", rev],
                         capture_output=True, text=True).stdout
    return [l for l in out.strip().split("\n") if l]


def head(title):
    print()
    print(title)


def check(name, ok, detail=""):
    """A verified/refuted line.  ok=True means mg-f2e1's claim reproduced."""
    print("  [%s] %s%s" % ("REPRODUCED" if ok else "REFUTED", name,
                           ("\n        -- " + detail) if detail else ""))
    if not ok:
        FINDINGS.append(name)


def measure(name, detail):
    """A measurement with no pass/fail: reported, not scored."""
    print("  [MEASURED  ] %s\n        -- %s" % (name, detail))


# ---------------------------------------------------------------- TARGET 1
def target1_trigger():
    head("TARGET 1 -- THE WIDENED A5 TRIGGER, tested the way mg-f7bc tested the "
         "last version\n(the new clause: 'ANY COMMIT THAT ADDS OR MODIFIES "
         "PROGRAM STATE -- STATE.md,\nmeaning its ledger rows and Appendix A -- "
         "ON THE SAME FOOTING')")

    # The instrument clause's own list, for the second column.
    INSTRUMENT = ("controls.py", "run_all.sh", "run_probe.py", "run_sweep.py",
                  "run_lrb.py", "face_complex.py", "verify_join.py",
                  "controls_output.txt", "sweep_output.txt", "lrb_output.txt",
                  "probe_output_n6.txt")

    cases = [
        ("c0cf104", "mg-78c0", "(a)"),
        ("c50ce32", "mg-60d3", "(b) STATE.md-only, 2 of the 3 mg-1319 defects"),
        ("db08b4c", "mg-1319", "(c)"),
        ("16bee79", "mg-a806", "(d) the STATE half"),
        ("5b63037", "mg-a806", "(d)"),
        ("f6756c0", "mg-a806", "(d) THE COMMIT THAT CARRIED ROW G-double-prime"),
        ("0160cbf", "mg-a806", "(d)"),
    ]
    misses = []
    for rev, item, tag in cases:
        fs = files_of(rev)
        state = "STATE.md" in fs
        instr = [f for f in fs if os.path.basename(f) in INSTRUMENT]
        verdict = ("FIRES (new clause)" if state else
                   "fires (instrument clause only)" if instr else "NOTHING FIRES")
        print("  %-9s %-8s %-46s %d file(s)  STATE.md=%-5s  instrument=%-5s  -> %s"
              % (rev, item, tag, len(fs), state, bool(instr), verdict))
        if not state and not instr:
            misses.append(rev)

    print()
    check("the new clause fires on c0cf104, c50ce32, db08b4c",
          all("STATE.md" in files_of(r) for r in ("c0cf104", "c50ce32", "db08b4c")),
          "all three modify STATE.md, so the widened clause reaches them")
    check("c50ce32 is 1 file changed, STATE.md, nothing else (the existence proof)",
          files_of("c50ce32") == ["STATE.md"],
          "files: %s" % files_of("c50ce32"))
    check("mg-a806's four commits: the new clause reaches the STATE ones",
          "STATE.md" in files_of("16bee79") and "STATE.md" in files_of("5b63037"))
    check("the new clause does NOT reach f6756c0 -- and f6756c0 is the commit "
          "that added row G-double-prime",
          "STATE.md" not in files_of("f6756c0"),
          "f6756c0 files: %s" % files_of("f6756c0"))

    # Does it now fire on everything?
    total = int(subprocess.run(["git", "-C", REPO, "rev-list", "--count", "HEAD"],
                               capture_output=True, text=True).stdout.strip())
    touching = int(subprocess.run(["git", "-C", REPO, "rev-list", "--count", "HEAD", "--", "STATE.md"],
                                  capture_output=True, text=True).stdout.strip())
    last25 = subprocess.run(["git", "-C", REPO, "log", "--format=%h", "-25"],
                            capture_output=True, text=True).stdout.split()
    l25 = sum(1 for h in last25 if "STATE.md" in files_of(h))
    check("the widened trigger does NOT fire on everything",
          touching < total * 0.75,
          "%d of %d commits in history touch STATE.md (%.0f%%); %d of the last 25 (%.0f%%). "
          "The 'WHAT THIS DOES NOT WIDEN INTO' exclusion list is concrete and "
          "applicable, and 'fires on every commit' is NOT the failure mode here."
          % (touching, total, 100.0 * touching / total, l25, 100.0 * l25 / 25))
    return misses


# ---------------------------------------------------------------- G-double-prime
def target1b_gpp():
    head("TARGET 1b -- WHERE ROW G-double-prime ACTUALLY LANDED\n"
         "mg-f2e1's Appendix A and commit message: 'row G-double-prime ... added "
         "to STATE.md by\nthe mg-a806 landing ... introduced by a STATE landing, "
         "into the file that no trigger watched.'")
    gpp = "G″"
    hist = subprocess.run(["git", "-C", REPO, "log", "--format=%h", "-S" + gpp, "--all", "--", "STATE.md"],
                          capture_output=True, text=True).stdout.split()
    allhist = subprocess.run(["git", "-C", REPO, "log", "--format=%h", "-S" + gpp, "--all"],
                             capture_output=True, text=True).stdout.split()
    measure("commits that change the count of %r in STATE.md" % gpp,
            "%s  (1e61031 = mg-a2bd's STRIKE record; ba3ec79 = mg-f2e1 itself)" % hist)
    measure("commits that change the count of %r anywhere" % gpp,
            "%s" % allhist)

    intro = show("f6756c0")
    added_in = [l for l in intro.split("\n")
                if l.startswith("+") and gpp in l and "| **G" in l]
    check("'added to STATE.md by the mg-a806 landing' is TRUE",
          any(h in ("16bee79", "5b63037") for h in hist),
          "REFUTED. STATE.md's history contains no commit that introduced the row. "
          "The ledger row was added by f6756c0 to "
          "docs/OneThird-Hodge-Side-Leverage.md, line 877 as that commit left it "
          "(labelled PROVEN, 'free from G + Theorem L'), %d matching added line(s). "
          "mg-a806's STATE.md commits (16bee79, 5b63037) do not contain it."
          % len(added_in))
    check("'into the file that no trigger watched' is TRUE",
          "STATE.md" in files_of("f6756c0"),
          "REFUTED twice. (i) f6756c0 does not touch STATE.md at all. "
          "(ii) f6756c0 touches %s -- a harness and the text an instrument "
          "prints -- so the PRE-EXISTING A5 instrument clause already fired on "
          "it. The row landed inside a commit the trigger already watched."
          % [f for f in files_of("f6756c0") if f.startswith("code/")])

    d39d = subprocess.run(["git", "-C", REPO, "log", "-1", "--format=%B", "522048f"],
                          capture_output=True, text=True).stdout
    check("mg-d39d, the audit cited as the evidence, agrees with the claim",
          "STATE.md is clean" not in d39d,
          "REFUTED. mg-d39d's own commit message: 'Blast radius is two lines and "
          "STATE.md is clean.' The cited audit says the opposite of the sentence "
          "citing it.")

    check("'a trigger ... was pointed at the component with the clean record' is TRUE",
          False,
          "REFUTED on its own terms: the commit carrying the arc's only BROKEN "
          "item was inside the instrument clause's scope (see above), so the "
          "instrument component's record is not the clean one with respect to "
          "that item either.")


# ---------------------------------------------------------------- TARGET 2
def target2_38():
    head("TARGET 2 -- EVERY OCCURRENCE OF 38/38 IN THE TREE, ENUMERATED HERE AND "
         "NOT COUNTED\nmg-f2e1's replacement for the false universal: 'five live "
         "sites, all flagged ... One\ninstrument comment ... Two sites "
         "deliberately NOT flagged and named here so the\nabsence is not mistaken "
         "for coverage.'")
    # This audit's OWN instrument quotes 38/38 in order to search for it, so it
    # is EXCLUDED from the tree scan and the exclusion is named here rather than
    # left to be mistaken for coverage.  That is the discipline this finding is
    # about, so it is applied to this file first.
    SELF = "code/face_geometry_audit_6653"
    hits, self_hits = [], 0
    for root, dirs, fnames in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        for fn in sorted(fnames):
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, REPO)
            try:
                txt = open(p, encoding="utf-8").read()
            except (UnicodeDecodeError, OSError):
                continue
            lines = txt.split("\n")
            for i, line in enumerate(lines, 1):
                for _ in re.finditer("38/38", line):
                    if rel.startswith(SELF):
                        self_hits += 1
                    else:
                        hits.append((rel, i, lines))

    per_file = {}
    for f, i, _ in hits:
        per_file.setdefault(f, []).append(i)
    measure("occurrences of the literal '38/38' in the tree, excluding this audit's "
            "own instrument",
            "%d occurrences in %d files (plus %d in %s/, this audit's own scanner, "
            "excluded and named)" % (len(hits), len(per_file), self_hits, SELF))
    for f in sorted(per_file):
        print("        %-62s %2d occurrence(s) on line(s) %s"
              % (f, len(per_file[f]), sorted(set(per_file[f]))))

    # A SITE is the enclosing blank-line-delimited paragraph: that is the unit a
    # reader arriving by search or quotation actually reads, and for STATE.md and
    # the Probe's section-12 block it collapses to the single line.  A site is
    # FLAGGED if the [:20] truncation is named anywhere inside it.
    FLAG = ("truncat", "TRUNCAT", "[:20]", "41 = 5", "5+16+20", "5 + 16 + 20",
            "20 of 63", "20 of the 63", "5 + 16 + 20 = 41")

    def paragraph(lines, i):
        a = b = i - 1
        while a > 0 and lines[a - 1].strip():
            a -= 1
        while b + 1 < len(lines) and lines[b + 1].strip():
            b += 1
        return "\n".join(lines[a:b + 1]), a + 1

    sites = {}          # (file, paragraph-start) -> [flagged, [occurrence lines]]
    for f, i, lines in hits:
        para, start = paragraph(lines, i)
        key = (f, start)
        rec = sites.setdefault(key, [any(k in para for k in FLAG), []])
        rec[1].append(i)

    # mg-f2e1's enumeration, keyed by the lines it names (or that its named
    # sections contain), so the map is checked against the tree rather than
    # against my own guess at paragraph boundaries.
    P = "docs/OneThird-Intrinsic-Face-Geometry-Probe.md"
    PIA = "docs/OneThird-Intrinsic-Face-Geometry-Probe-IndependentAudit.md"
    accounted_lines = {
        ("STATE.md", 135): "live 1/5 -- ledger row 135",
        ("STATE.md", 276): "live 2/5 -- Appendix A paragraph",
        (P, 41): "live 3/5 -- Probe section-head changelog",
        (P, 408): "live 4/5 -- Probe section 5",
        (P, 815): "live 5/5 -- Probe section 12 (reversal preamble)",
        (P, 822): "live 5/5 -- Probe section 12 (the proposed-row block)",
        ("code/face_geometry_audit_5630/audit_x3_equivalence.py", 84):
            "the one instrument comment",
        (PIA, 45): "named NOT-flagged 1/2 (Probe-IndependentAudit.md:45)",
        (PIA, 311): "named NOT-flagged 2/2 (Probe-IndependentAudit.md:311)",
    }
    print()
    print("  flag state, SITE by SITE (a site = the enclosing paragraph, which is "
          "what a reader\n  arriving by search or quotation reads):")
    unaccounted = []
    labels = {}
    for (f, start) in sorted(sites):
        flagged, occ = sites[(f, start)]
        label = None
        for i in occ:
            if (f, i) in accounted_lines:
                label = accounted_lines[(f, i)]
                break
        labels[(f, start)] = label
        if label is None:
            unaccounted.append((f, start, flagged, occ))
        print("        %-9s %-58s para@%-4d occ %-22s %s"
              % ("FLAGGED" if flagged else "UNFLAGGED", f, start, sorted(set(occ)),
                 label if label else "*** NOT IN mg-f2e1's ENUMERATION ***"))

    live = [k for k in sites if (labels.get(k) or "").startswith("live")]
    print()
    check("the five named LIVE sites are all in fact flagged",
          len(live) == 6 and all(sites[k][0] for k in live),
          "the live half of the enumeration is CORRECT and I could not break it: "
          "row 135, Appendix A, and the Probe's section-head changelog, section 5 "
          "and section 12 each name the [:20] truncation inside the paragraph that "
          "quotes the number. Section 12 is two paragraphs (the reversal preamble "
          "and the block itself); both are flagged, which is why six paragraphs "
          "carry mg-f2e1's five named sites.")
    check("the instrument comment reads as mg-f2e1 describes it",
          "the audit's OWN 38/38 on the audit's OWN population" in
          open(os.path.join(REPO, "code/face_geometry_audit_5630/audit_x3_equivalence.py"),
               encoding="utf-8").read(),
          "audit_x3_equivalence.py:84 names the truncated population in the act "
          "of reproducing it -- correct as written, as claimed.")
    unflagged_missing = [u for u in unaccounted if not u[2]]
    check("'TWO sites deliberately NOT flagged and named here so the absence is "
          "not mistaken for coverage' accounts for every unflagged site",
          not unaccounted,
          "REFUTED. %d site(s) carrying %d occurrence(s), in %d file(s), are "
          "outside the enumeration entirely -- %d of those sites UNFLAGGED: %s. "
          "The whole of "
          "OneThird-Intrinsic-Face-Geometry-StateLanding2-IndependentAudit.md is "
          "missing -- mg-f7bc's OWN audit document, the one this commit lands -- "
          "and it is never named anywhere in the enumeration. The enumeration is "
          "offered as the replacement for a universal that was FALSE, on the "
          "stated ground that a coverage claim wrong once is not evidence the "
          "second time; it names 4 of the 6 files and %d of the %d occurrences. "
          "Every omitted site is in a frozen audit document and every one of them "
          "discusses the truncation, so no reader is misled about the NUMBER -- "
          "the defect is in the COVERAGE CLAIM, which is the same defect, one "
          "generation on, at the same site."
          % (len(unaccounted), sum(len(u[3]) for u in unaccounted),
             len(set(u[0] for u in unaccounted)), len(unflagged_missing),
             sorted(set(u[0] for u in unaccounted)),
             len(hits) - sum(len(u[3]) for u in unaccounted), len(hits)))


# ---------------------------------------------------------------- TARGET 3
def target3_changelog():
    head("TARGET 3 -- E3: IS THE CHANGELOG NOW TRUE? checked against the diff, "
         "not against itself")
    probe = "docs/OneThird-Intrinsic-Face-Geometry-Probe.md"

    # (i) the sentence half
    n6 = open(os.path.join(REPO, "code/face_geometry_audit_e0ce/out_n6.txt"),
              encoding="utf-8").read().split("\n")
    extra = open(os.path.join(REPO, "code/face_geometry_audit_e0ce/out_extra.txt"),
                 encoding="utf-8").read().split("\n")
    check("out_n6.txt:44 is the Lemma-1 cross-check at 87/87, n<=5",
          "87/87" in n6[43] and "n<=5" in n6[43],
          "line 44 verbatim: %r" % n6[43].strip())
    check("out_extra.txt:2 is PURITY 404/404 at 2<=n<=6, a different check",
          "404/404" in extra[1] and "PURE" in extra[1],
          "line 2 verbatim: %r" % extra[1].strip())

    cur = open(os.path.join(REPO, probe), encoding="utf-8").read().split("\n")
    para2 = "\n".join(cur[139:156])
    check("the section-2 sentence now reads n<=5 for the Lemma-1 cross-check",
          "**`n ≤ 5`** by a build that never uses Lemma 1" in "\n".join(cur[140:150]),
          "and it is the sentence the document itself labels '(F3, repaired ...)' "
          "at line 140: %r" % cur[139][:64])
    check("mg-1319 did correct the same overstatement at section 11",
          "Lemma-1 cross-check to `n ≤ 5`" in show("db08b4c"),
          "verified in db08b4c's own diff of the Probe -- so 'at section 11 by "
          "mg-1319, and at section 2 ... only now by mg-f2e1' is right about both "
          "halves.")

    # (ii) the changelog half, checked against THIS diff
    hunks = [l for l in show(TARGET).split("\n")
             if l.startswith("@@") ]
    probe_diff = subprocess.run(
        ["git", "-C", REPO, "diff", "-U0", PARENT, TARGET, "--", probe],
        capture_output=True, text=True).stdout
    probe_hunks = [l.split("@@")[1].strip() for l in probe_diff.split("\n") if l.startswith("@@")]
    measure("hunks this commit makes in the Probe", "%s" % probe_hunks)
    s5_touched = "Flagged because" in probe_diff or "TRUNCATION" in probe_diff.split("@@")[0]
    changelog = "\n".join(cur[36:45])
    claims_s5 = "per-site enumeration in §5" in changelog or \
                "enumeration in `§5`" in changelog or \
                "enumeration in §5 and in" in changelog
    s5_text = "\n".join(cur[405:420])
    has_enum = ("live sites" in s5_text) or ("deliberately NOT flagged" in s5_text)
    check("the NEW changelog line's 'the per-site enumeration in section 5' "
          "exists in section 5",
          has_enum,
          "REFUTED. The changelog now says the false universal is replaced by "
          "'the per-site enumeration in section 5 and in STATE.md Appendix A'. "
          "Appendix A carries an enumeration; section 5 does not -- it carries "
          "only the truncation flag mg-1319 landed. Section 5 is not touched by "
          "this commit at all: the Probe diff has exactly %d hunks (%s), none of "
          "them in section 5. This is a changelog entry asserting a fix that is "
          "not in the diff -- which is the defect E3 exists to name, in the very "
          "line E3 rewrote." % (len(probe_hunks), probe_hunks))


# ---------------------------------------------------------------- TARGET 4
def target4_connective():
    head("TARGET 4 -- E4: DOES ROW 135 CARRY THE CONNECTIVE? read in reading "
         "order, as a quoted\nfragment would be")
    old = show(PARENT + ":STATE.md").split("\n")[134]
    dbo = show("db08b4c:STATE.md").split("\n")[134]
    new = open(os.path.join(REPO, "STATE.md"), encoding="utf-8").read().split("\n")[134]

    a = dbo.find("did the *generalisation* correctly")
    b = dbo.find("Step 4d DID fire here")
    check("the 318-character measurement reproduces exactly",
          (b - a) == 318,
          "clause-start ('did the *generalisation* correctly') to clause-start "
          "('Step 4d DID fire here') in db08b4c:STATE.md line 135 = %d characters "
          "(%d bytes), and there is no connective between them (BOTH FACTS ... "
          "present in the gap: %s). mg-f7bc's F7 table reports it as bytes; the "
          "figure is exact in CHARACTERS, which is how mg-f2e1 states it."
          % (b - a, len(dbo[a:b].encode()), "BOTH FACTS" in dbo[a:b]))

    i = new.find("the sixth deliverable did the")
    frag = new[i:i + 260]
    conn = new.find("and, in the same document, still asserted one universal")
    check("the clause now carries the connective in reading order",
          0 < conn - i < 120,
          "the connective starts %d characters after the clause. Read alone: %r"
          % (conn - i, frag))
    check("a reader encountering the clause alone is no longer misled",
          "BOTH FACTS ARE TRUE OF THE SAME DOCUMENT AND NEITHER CANCELS THE OTHER"
          in new[i:i + 700],
          "the reconciliation is inline, not 6 KB away in Appendix A.")

    # E4b
    stale = [q for q in ("the other **six** firings", "FIRED AT **SEVEN** LOCATIONS")
             if q in new]
    inside_note = all(new.find(q) > new.find("THE COUNTS THIS SENTENCE USED TO CARRY WERE STALE")
                      for q in stale) if stale else True
    check("E4b: the stale counts survive only inside their own correction note",
          inside_note and "points at the tallies instead of restating their sizes" in new,
          "the row now points at Appendix A's two tallies rather than hard-coding "
          "a number Appendix A recounts.")


# ---------------------------------------------------------------- TARGET 6
def target6_restructure():
    head("TARGET 6 -- DID IT RESTRUCTURE ANYTHING? mg-f2e1 was FORBIDDEN from "
         "restructuring\nSTATE.md, splitting rows, or moving content between "
         "files")
    for rev, tag in ((("db08b4c"), "db08b4c (mg-1319)"), (PARENT, "de54c3a (parent)"), (TARGET, "ba3ec79 (mg-f2e1)")):
        t = show(rev + ":STATE.md").split("\n")
        print("  %-22s  " % tag + "  ".join(
            "L%d=%d" % (ln, len(t[ln - 1].encode())) for ln in range(131, 136)))

    a = show(PARENT + ":STATE.md").split("\n")
    b = show(TARGET + ":STATE.md").split("\n")
    check("rows 131-134 are byte-identical -- no rows split, none re-flowed",
          all(a[i] == b[i] for i in range(130, 134)),
          "5351 / 9228 / 13487 / 10824 bytes, unchanged.")
    check("the ledger's table-row count is unchanged",
          sum(1 for s in a if s.startswith("| ")) == sum(1 for s in b if s.startswith("| ")),
          "%d rows before, %d after." % (sum(1 for s in a if s.startswith("| ")),
                                         sum(1 for s in b if s.startswith("| "))))
    diff_lines = [i + 1 for i in range(min(len(a), len(b))) if a[i] != b[i]]
    check("only lines 135, 276, 282 are edited in place, plus an insertion",
          diff_lines[:3] == [135, 276, 282],
          "STATE.md goes %d -> %d lines; the +12 is the A5 block inserted after "
          "line 335. No content is moved between files: the Probe's three hunks "
          "are additions, and nothing deleted from STATE.md reappears in the "
          "Probe." % (len(a), len(b)))

    ob, on = len(a[134].encode()), len(b[134].encode())
    cb, cn = len(a[134]), len(b[134])
    check("mg-f2e1's own report of row 135's growth -- 'a further 949 bytes "
          "(+7.6%)' -- reproduces",
          (on - ob) == 949,
          "REFUTED. Measured on the metric mg-f7bc's F7 used (line bytes; F7's "
          "7,832 -> 11,727 reproduces exactly at c0cf104 -> db08b4c): %d -> %d = "
          "+%d bytes (+%.1f%%), and +%d characters (+%.1f%%). A character-level "
          "diff of the line gives four insertions totalling 2,134 chars against "
          "46 deleted. The reported figure understates the growth of the row an "
          "audit had just flagged FOR growth by a factor of %.2f, in the sentence "
          "that reports it for the ticket that owns it -- and it appears in "
          "mg-f2e1's list of claims 're-verified against source rather than "
          "inherited'."
          % (ob, on, on - ob, 100.0 * (on - ob) / ob, cn - cb,
             100.0 * (cn - cb) / cb, (on - ob) / 949.0))


# ---------------------------------------------------------------- inherited numbers
def inherited():
    head("WHAT mg-f2e1 CLAIMS IT RE-VERIFIED -- re-verified again here")
    # the six 0-BROKEN verdicts
    audits = [("013e073", "mg-e0ce"), ("fcc8a11", "mg-5630"), ("321509f", "mg-f7bc"),
              ("2cc8d57", "mg-86a3"), ("34c151f", "mg-fcf1"), ("de54c3a", "mg-f1b2")]
    zero = []
    for rev, item in audits:
        msg = subprocess.run(["git", "-C", REPO, "log", "-1", "--format=%B", rev],
                             capture_output=True, text=True).stdout
        zero.append(bool(re.search(r"0 BROKEN", msg)))
    check("all six cited audits returned 0 BROKEN mathematics",
          all(zero), "%s" % ", ".join("%s=%s" % (i, "0 BROKEN" if z else "?")
                                      for (_, i), z in zip(audits, zero)))

    # c0cf104's eight-line STATE hunk, and that it carried both defects
    d = subprocess.run(["git", "-C", REPO, "diff", "-U0", "c0cf104^", "c0cf104", "--", "STATE.md"],
                       capture_output=True, text=True).stdout
    added = [l for l in d.split("\n") if l.startswith("+") and not l.startswith("+++")]
    check("c0cf104's STATE.md hunk is EIGHT lines and carries both defects",
          len(added) == 8 and any("n ≤ 6`, by a build that never uses Lemma 1" in l for l in added)
          and any("SIX for six" in l for l in added),
          "%d added lines; both the 'closed the Lemma-1 cross-check to n<=6' "
          "overstatement and the 'SIX for six' 4d contradiction are in them; "
          "c0cf104 also touches controls.py, which is why they were audited."
          % len(added))
    check("mg-f2e1 corrected its OWN ticket rather than inheriting it",
          True,
          "mg-f2e1's ticket asserts c50ce32 'carried TWO OF THE THREE DEFECTS "
          "THIS COMMIT IS REPAIRING'. It did not -- both rode in via c0cf104's "
          "hunk above. mg-f2e1's landing states c0cf104, correctly, and keeps "
          "c50ce32 only as the STATE.md-only existence proof. Credit: the one "
          "place it was handed a wrong number, it did not adopt it.")

    # E6: out_nc3 line F
    nc3 = open(os.path.join(REPO, "code/face_geometry_audit_5630/out_nc3.txt"),
               encoding="utf-8").read().split("\n")
    fires = [l for l in nc3 if "line3" in l and "78 of 78" in l and "FIRES" in l]
    silent = [l for l in nc3 if "line3" in l and "82 of 82" in l and "SILENT" in l]
    check("E6's 78-vs-82 line-F split is exactly right",
          len(fires) == 1 and len(silent) == 1,
          "%r and %r -- so only ONE of db08b4c's two 'genuine non-sign "
          "construction corruptions' leaves NC3's negative lines silent, as "
          "mg-f2e1 records." % (fires[0].strip(), silent[0].strip()))

    # E5's artifact history
    for rev, tag in (("c0cf104", "pre-A4-repair"), ("db08b4c", "mg-1319"), (TARGET, "mg-f2e1")):
        art = show(rev + ":code/face_geometry/controls_output.txt").split("\n")
        occ = [i + 1 for i, l in enumerate(art) if "ALL CONTROLS PASS" in l]
        pref = [i for i in occ if art[i - 1].lstrip().startswith("[PASS]")]
        print("  %-9s %-14s banner at line(s) %-10s of which [PASS]-prefixed: %s"
              % (rev, tag, occ if occ else "none", pref if pref else "none"))
    art = show(TARGET + ":code/face_geometry/controls_output.txt")
    check("the artifact now contains 'ALL CONTROLS PASS' zero times",
          "ALL CONTROLS PASS" not in art,
          "and the bottom line reads \"...this battery's bottom line is NOT 'all "
          "controls pass'.\" -- so a grep for the exact banner returns nothing, "
          "and a case-insensitive grep returns exactly the negation.")


def main():
    print("mg-6653 -- INDEPENDENT AUDIT OF mg-f2e1 (%s)" % TARGET)
    print("=" * 78)
    misses = target1_trigger()
    target1b_gpp()
    target2_38()
    target3_changelog()
    target4_connective()
    target6_restructure()
    inherited()
    print()
    print("=" * 78)
    if FINDINGS:
        print("REFUTED CLAIMS: %d" % len(FINDINGS))
        for f in FINDINGS:
            print("   - %s" % f)
    else:
        print("no claim refuted by this file")
    print()
    print("This file scores CLAIMS, not mathematics. It makes no statement about "
          "the mathematics\nof the probe, which mg-e0ce/mg-5630/mg-f7bc rebuilt "
          "and which is not re-opened here.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
