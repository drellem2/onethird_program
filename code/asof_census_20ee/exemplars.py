#!/usr/bin/env python3
"""EXEMPLARS -- A MENTION IS NOT A DATE, AND THAT IS WHY THE NAME ROTS.

mg-e8b0 found that tranche 1 offered the next tranche a cheap starting
instrument BY NAME, and that the instrument had been pinned one tranche later by
this arc's own commit.  The sentence stood for four tranches.  The count was
right the whole time.

    THE COUNT KNEW AND THE NAME DID NOT.  A count is not a record of WHICH, and
    the reader picking the next instrument reads the name.

That tranche declared the limit as N28 and said what would close it: *somebody
taught the rule to read what a sentence SAYS, which is a rule about English*.

THAT ACCOUNT OF THE REMEDY WAS WRONG, AND CORRECTING IT IS THIS FILE.  The rule
`named in this record` is a SUBSTRING COUNT, and it cannot separate a sentence
ACCOUNTING for a pin from one OFFERING the same instrument as remaining work --
but not because the difference is in the English.  IT IS IN THE DATE.  A
sentence accounting for a pin is NECESSARILY YOUNGER than the pin.  A sentence
offering the instrument is OLDER.  The field that separates them was in the
repository the whole time and the rule was throwing it away.

--------------------------------------------------------------------------------
1.  THE RULE, AND WHY IT IS PER (RECORD, NAME) AND NOT PER LINE
--------------------------------------------------------------------------------

For every markdown record in the tree at AS_OF and every work-list instrument it
names, take the NEWEST mention -- `git blame` at AS_OF, so the answer is a
function of one commit -- and ask whether a pin landed on that instrument AFTER
it.  If one did, the record's LAST WORD about that instrument pre-dates a change
to it.  Printed as OVERTAKEN.

    PER LINE IT WOULD BE USELESS AND THE FIRST DRAFT WAS PER LINE.  The record
    here is APPEND-ONLY NARRATIVE: tranche 3 wrote `### The next candidate,
    diagnosed but not pinned -- landscape_repair_audit_3b51`, tranche 4 LANDED
    that pin, and tranche 3's section is still there and still says it.  Per
    line that sentence is overtaken and reads as a live defect; it is not one,
    because the answer is the NEXT SECTION.  A correction in this estate is a
    younger sentence, not an edit to an older one.  140 pairs are overtaken
    where 290 lines are, and the 150 that drop out are that distinction.

So the two halves compose rather than compete: the substring count says WHETHER
the record names it, the blame date says WHETHER IT HAS NAMED IT SINCE.

--------------------------------------------------------------------------------
2.  THE DIRECTION IT CAN ANSWER IN, WHICH IS ONE
--------------------------------------------------------------------------------

OVERTAKEN proves the record's last word is OLDER THAN A PIN ON ITS SUBJECT.  It
does NOT prove the sentence is wrong: a pin is not a repair (out_worklist.txt
§5), and a reference may be to something the pin did not touch.  NOT OVERTAKEN
proves NOTHING AT ALL -- the named instrument may have gone stale with no pin
landing on it, which is the defect class this whole arc exists for.

Reported as OVERTAKEN / NOT OVERTAKEN for that reason, never as STALE / FRESH,
which is worklist.py's FALSIFIED / NOT FALSIFIED discipline one field along.

--------------------------------------------------------------------------------
3.  HOW THIS FILE COULD EXHIBIT THE DEFECT IT REPORTS
--------------------------------------------------------------------------------

  * IT COULD READ ITS SUBJECT OFF DISK.  Every input -- the work-list, the
    records, the blame, the diffs -- is read THROUGH A COMMIT.  P29 plants a
    mutated record IN THE WORKTREE and requires every figure to stand still.

  * ITS OWN HEADLINE COULD BE UNFALSIFIABLE.  The instance this rule was built
    for was CLOSED IN THE COMMIT BEFORE THIS ONE -- tranche 9 annotated the
    sentence -- so at AS_OF the rule correctly reports the census README as
    accounted for, and a rule that reports nothing is indistinguishable from a
    rule that sees nothing.  P30 runs the SAME rule on the SAME pair at AS_OF^
    and requires it to FIRE.  Section 4 prints both.

  * A NAME COULD MATCH INSIDE A WORD.  It does, and by 52 lines: one work-list
    row is `code/mirror_staleness_cdd5/prerepair`, whose basename is an
    ordinary word, and it matches inside `k1_prerepair.py` all over the estate.
    The guard is mg-23af's, one directory over and one file along: A NAME IS A
    WHOLE TOKEN.  P31 measures both directions rather than asserting it.

  * BLAME REPORTS THE LAST TOUCH, NOT THE ORIGIN.  A reflow, a typo fix, a
    renumbering re-dates a sentence it did not change, and a stale offer
    laundered that way reads as accounted for.  THE BIAS IS TOWARD REPORTING
    FEWER OVERTAKEN PAIRS THAN THERE ARE, which is the safe direction for a
    finding and is declared as N29 rather than left to be discovered.

  * IT CANNOT SEE A RECORD THAT SHOULD NAME AN INSTRUMENT AND DOES NOT.  Zero
    mentions is zero pairs.  N30 counts the work-list rows no record names at
    all, which is the population this rule is blind to BY CONSTRUCTION.

--------------------------------------------------------------------------------
4.  USAGE
--------------------------------------------------------------------------------

    python3 exemplars.py                    # in run_all.sh
    python3 exemplars.py --pair <record> <name> [<rev>]
                                            # the rule on ONE pair, at any rev

The second is what P30 calls, and it is the whole rule rather than a summary of
it: a control that had to parse this file's transcript would be reading a report
(mg-937c).
"""

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)

import worklist  # noqa: E402

# THE PIN RULE IS IMPORTED AND NOT RE-TYPED.  worklist.added_revisions is rule B
# -- a resolving revision added to that directory by that commit -- and a second
# copy here would drift from it (mg-1344's P5).  This file therefore CANNOT
# disagree with out_worklist.txt about what a pin is.
from worklist import added_revisions, git, read_rev, text  # noqa: E402

# The commit every figure below is a function of.  An ancestor of origin/main,
# and the reason this transcript has a fixed point.  Move it deliberately.
AS_OF = "0cb0fa4"

SWEEP_TRANSCRIPT = "code/asof_census_20ee/out_ground_truth.txt"

# The sweep's own row format, parsed rather than re-typed, exactly as
# worklist.ROW parses it -- the population is the same 44 rows, and a second
# hand-copied list would be a second copy that drifts.
ROW = worklist.ROW

# A PUBLISHED REMAINING-COUNT.  A digit run and a remainder word close enough
# together to be one clause.  DECLARED RATHER THAN TUNED: it is the shape of
# `25 instruments remain` and `27 of the 32 ... are unrepaired`, and section 3
# reports what it matches so a reader can disagree with it.
COUNT = re.compile(r"\b\d+\b[^.\n]{0,60}?"
                   r"\b(remain|remains|remaining|remainder|left|unrepaired|"
                   r"outstanding)\b", re.I)

HEADING = re.compile(r"^#{1,6} ")


def rev_order(rev):
    """Position of every commit in the history of `rev`, newest = 0.

    An INDEX rather than a `merge-base --is-ancestor` per comparison, which
    would be ~10^5 subprocesses here.  It is exact on a linear history and the
    linearity is COUNTED in section 5 rather than assumed -- this repository has
    no merges because the refinery rebases, and the day that changes the count
    says so.
    """
    return {h: i for i, h in enumerate(text(git("rev-list", rev)).split())}


def worklist_rows(rev):
    got = []
    for line in read_rev(rev, SWEEP_TRANSCRIPT).splitlines():
        m = ROW.match(line)
        if m:
            got.append(m.group(1))
    return got


def name_patterns(dirs):
    """Two spellings of `this record names that instrument`, and the guard.

    LOOSE is the basename anywhere; TOKEN requires the basename to be a whole
    token.  Both are returned because they DISAGREE on real data here -- by 52
    lines, all of them one row whose basename is an ordinary English word -- and
    a file publishing one of them alone would be publishing a choice it had not
    measured (worklist.py section 3, the same arrangement).
    """
    bases = {}
    for d in dirs:
        bases.setdefault(d.split("/")[-1], d)
    alt = "|".join(re.escape(b) for b in sorted(bases, key=len, reverse=True))
    return bases, re.compile(alt), {
        b: re.compile(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(b))
        for b in bases}


def blame(rev, path):
    """line number -> the commit that last wrote that line, at `rev`."""
    got = {}
    for line in text(git("blame", "--line-porcelain", rev, "--", path)).splitlines():
        m = re.match(r"^([0-9a-f]{40}) \d+ (\d+)", line)
        if m:
            got[int(m.group(2))] = m.group(1)
    return got


def sections(body):
    """line number -> (heading text, first line, last line) of its section.

    Markdown headings are DOCUMENT STRUCTURE and not prose, which is the whole
    reason this file uses them: asking whether a count and a name are published
    together must not become a second rule about English.
    """
    starts = [i for i, l in enumerate(body, 1) if HEADING.match(l)]
    bounds = []
    for j, s in enumerate(starts):
        end = (starts[j + 1] - 1) if j + 1 < len(starts) else len(body)
        bounds.append((s, end, body[s - 1].strip()))
    got = {}
    for s, e, head in bounds:
        for i in range(s, e + 1):
            got[i] = (head, s, e)
    return got


def pins_for(dirs, rev):
    """Rule B's commits per directory, over the whole history at `rev`."""
    got = {}
    for d in dirs:
        got[d] = [h for h in text(git("log", "--format=%H", rev, "--", d)).split()
                  if added_revisions(h, d)]
    return got


def scan(rev=AS_OF):
    """Every figure this file publishes, computed from one commit and nothing
    else.  SEPARATE FROM THE PRINTING SO THE CONTROLS CAN CALL IT.
    """
    dirs = worklist_rows(rev)
    bases, loose, token = name_patterns(dirs)
    order = rev_order(rev)
    pins = pins_for(dirs, rev)

    records = [p for p in text(git("ls-tree", "-r", "--name-only", rev)).splitlines()
               if p.endswith(".md")]

    lines_loose, lines_token, pairs = 0, 0, {}
    loose_only = []
    for path in records:
        body = read_rev(rev, path).splitlines()
        if not loose.search("\n".join(body)):
            continue
        marks = blame(rev, path)
        sect = sections(body)
        counts = [i for i, l in enumerate(body, 1) if COUNT.search(l)]
        for i, txt in enumerate(body, 1):
            for base in sorted(set(loose.findall(txt))):
                lines_loose += 1
                if not token[base].search(txt):
                    loose_only.append((path, i, base, txt.strip()))
                    continue
                lines_token += 1
                head, s, e = sect.get(i, ("", 1, len(body)))
                key = (path, base)
                idx = order.get(marks.get(i), 10 ** 9)
                cur = pairs.get(key)
                if cur is None or idx < cur["idx"]:
                    here = [c for c in counts if s <= c <= e]
                    # THE COUNT'S OWN DATE, taken the same way the name's is.
                    # The ticket's claim is a claim about TWO fields of one
                    # sentence-pair, so measuring one of them and asserting the
                    # other would be the defect this arc reports.
                    newest_count = (min(here, key=lambda c: order.get(
                        marks.get(c), 10 ** 9)) if here else None)
                    pairs[key] = {
                        "path": path, "base": base, "dir": bases[base],
                        "line": i, "text": txt.strip(), "idx": idx,
                        "blame": marks.get(i), "head": head,
                        "count_in_section": here,
                        "count_line": (body[newest_count - 1].strip()
                                       if newest_count else ""),
                        "count_blame": (marks.get(newest_count)
                                        if newest_count else None),
                        "count_idx": (order.get(marks.get(newest_count), 10 ** 9)
                                      if newest_count else None),
                    }

    for p in pairs.values():
        p["after"] = [h for h in pins[p["dir"]] if order[h] < p["idx"]]
        p["self"] = p["path"].startswith(p["dir"] + "/")

    # HOW OFTEN THE RECORD ITSELF IS REVISED, for the co-published rows only.
    # This is the column that turned section 3's first draft around: `the count
    # stays right` is not a property of counts, it is a property of a record
    # that is APPENDED TO.  Computed for 11 paths rather than 572 because it is
    # a `git log` each and nothing outside section 3 reads it.
    ages = {}
    for p in pairs.values():
        if p["count_in_section"] and p["path"] not in ages:
            ages[p["path"]] = len(text(git("log", "--format=%h", rev, "--",
                                           p["path"])).split())
    for p in pairs.values():
        p["record_commits"] = ages.get(p["path"], 0)

    over = [p for p in pairs.values() if p["after"]]
    foreign = [p for p in over if not p["self"]]
    return {
        "rev": rev, "dirs": dirs, "records": records, "pins": pins,
        "lines_loose": lines_loose, "lines_token": lines_token,
        "loose_only": loose_only, "pairs": pairs, "over": over,
        "foreign": foreign,
        "self": [p for p in over if p["self"]],
        "cofield": [p for p in pairs.values() if p["count_in_section"]],
        "copublished": [p for p in over if p["count_in_section"]],
        "unnamed": [d for d in dirs
                    if not any(k[1] == d.split("/")[-1] for k in pairs)],
    }


def pair_verdict(record, name, rev=AS_OF):
    """The rule on ONE (record, name) pair, at any revision.

    THE WHOLE RULE AND NOT A SUMMARY OF IT: P30 asks this at AS_OF and at AS_OF^
    and requires the answers to differ, which is what makes the zero this file
    prints for the census README falsifiable.
    """
    body = read_rev(rev, record).splitlines()
    pat = re.compile(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(name))
    hits = [i for i, l in enumerate(body, 1) if pat.search(l)]
    if not hits:
        return {"mentions": 0, "overtaken": False, "after": [], "newest": None}
    marks = blame(rev, record)
    order = rev_order(rev)
    newest = min(hits, key=lambda i: order.get(marks.get(i), 10 ** 9))
    idx = order.get(marks.get(newest), 10 ** 9)
    directory = next((d for d in worklist_rows(rev)
                      if d.split("/")[-1] == name), None)
    after = [] if directory is None else [
        h for h in text(git("log", "--format=%H", rev, "--", directory)).split()
        if order.get(h, 10 ** 9) < idx and added_revisions(h, directory)]
    return {"mentions": len(hits), "overtaken": bool(after), "after": after,
            "newest": marks.get(newest), "line": newest,
            "text": body[newest - 1].strip()}


def per_line_overtaken(record, name, rev=AS_OF):
    """The FIRST DRAFT's rule, kept so the difference can be printed.

    Per LINE rather than per (record, name): every mention older than a pin
    counts.  It is not a worse implementation of the same rule, it is a
    DIFFERENT QUESTION, and on an append-only record it answers `has this
    document ever said anything about X that pre-dates a pin` -- which is yes
    for every document that has been written for more than one tranche.
    """
    body = read_rev(rev, record).splitlines()
    pat = re.compile(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(name))
    hits = [i for i, l in enumerate(body, 1) if pat.search(l)]
    if not hits:
        return 0
    marks, order = blame(rev, record), rev_order(rev)
    directory = next((d for d in worklist_rows(rev)
                      if d.split("/")[-1] == name), None)
    if directory is None:
        return 0
    pins = [h for h in text(git("log", "--format=%H", rev, "--", directory)).split()
            if added_revisions(h, directory)]
    return sum(1 for i in hits
               if any(order.get(h, 10 ** 9) < order.get(marks.get(i), 10 ** 9)
                      for h in pins))


def main(argv):
    if len(argv) > 2 and argv[1] == "--pair":
        rev = argv[4] if len(argv) > 4 else AS_OF
        got = pair_verdict(argv[2], argv[3], rev)
        print("%s / %s at %s: %d mention(s), newest %s, %s"
              % (argv[2], argv[3], rev, got["mentions"],
                 (got["newest"] or "-")[:7],
                 "OVERTAKEN by %s" % ",".join(h[:7] for h in got["after"])
                 if got["overtaken"] else "NOT OVERTAKEN"))
        if got["mentions"]:
            print("    %s" % got["text"][:70])
        return 0

    got = scan()
    bar = "=" * 78
    rule = "-" * 78
    print(bar)
    print("mg-0bf1 -- HAS THE RECORD NAMED IT SINCE?  Read at AS_OF = %s" % AS_OF)
    print(bar)
    print()
    print("  mg-e8b0 declared N28: `named in this record` is a SUBSTRING COUNT")
    print("  and cannot tell a sentence ACCOUNTING for a pin from one OFFERING")
    print("  the same instrument as remaining work.  It said closing that would")
    print("  take a rule about English.  IT TAKES A DATE.  A sentence")
    print("  accounting for a pin is younger than the pin and one offering the")
    print("  instrument is older, so the newest mention of an instrument in a")
    print("  record is the record's LAST WORD about it, and a pin landing after")
    print("  that is a change the record has not met.  METHOD AND BLIND SPOTS")
    print("  are in this file's docstring and are not repeated here; the")
    print("  sentence that matters is section 2's: OVERTAKEN is one-directional.")
    print()

    print(rule)
    print("1  THE POPULATION, AND THE 52 LINES A WHOLE-TOKEN GUARD REMOVES")
    print(rule)
    print()
    print("      %-52s %d" % ("work-list rows (parsed, not re-typed)",
                              len(got["dirs"])))
    print("      %-52s %d" % ("markdown records in the tree at AS_OF",
                              len(got["records"])))
    print("      %-52s %d" % ("mention lines, basename ANYWHERE",
                              got["lines_loose"]))
    print("      %-52s %d" % ("mention lines, basename a WHOLE TOKEN",
                              got["lines_token"]))
    print("      %-52s %d" % ("  removed by the guard", len(got["loose_only"])))
    seen = sorted(set(b for _, _, b, _ in got["loose_only"]))
    print("      %-52s %s" % ("  and every one is this row's basename",
                              ",".join(seen) or "-"))
    print()
    print("  mg-23af's rule, one file along: A NAME IS A WHOLE TOKEN.  One")
    print("  work-list row is a SUBDIRECTORY and its basename is an ordinary")
    print("  English word, so the loose spelling matches inside every")
    print("  `k1_prerepair.py` in the estate.  The guard is a fact about")
    print("  tokenising and not a judgement about the word, and it is not free:")
    print("  it would also silence a real mention spelled inside an identifier.")
    print("  P31 runs both directions rather than asserting either.")
    for path, line, base, txt in got["loose_only"][:3]:
        print("      %s:%d  %s" % (path, line, txt[:52]))
    print("      ... %d more" % max(0, len(got["loose_only"]) - 3))
    print()

    print(rule)
    print("2  THE RECORD'S LAST WORD, AND WHETHER A PIN LANDED AFTER IT")
    print(rule)
    print()
    print("      %-52s %d" % ("(record, name) pairs", len(got["pairs"])))
    print("      %-52s %d" % ("  OVERTAKEN -- a pin landed after the newest",
                              len(got["over"])))
    print("      %-52s %d" % ("    in the named instrument's OWN record",
                              len(got["self"])))
    print("      %-52s %d" % ("    in a FOREIGN record -- the verdict",
                              len(got["foreign"])))
    print("      %-52s %d" % ("  OVERTAKEN and beside a count (section 3)",
                              len(got["copublished"])))
    print()
    print("  SELF AND FOREIGN ARE KEPT APART BECAUSE THEY ARE NOT THE SAME")
    print("  CLAIM.  A directory's own README pre-dating a pin on that")
    print("  directory is ordinary -- the README is written once and the pins")
    print("  come later.  A FOREIGN record is a reader somewhere else in the")
    print("  estate whose last word about this instrument is older than a")
    print("  change to it, and that is the shape mg-e8b0 was bitten by.")
    print()

    print(rule)
    print("3  THE TICKET'S CLAIM: A COUNT AND A NAME PUBLISHED TOGETHER")
    print(rule)
    print()
    print("  mg-0bf1 carries one transferable claim forward: WHEREVER A")
    print("  REMAINING-COUNT AND A NAMED EXEMPLAR ARE PUBLISHED TOGETHER, THE")
    print("  COUNT WILL STAY RIGHT AND THE NAME WILL ROT, and only the name is")
    print("  load-bearing for the next reader.  `Together` is read as THE SAME")
    print("  MARKDOWN SECTION -- document structure, not prose -- so that this")
    print("  half does not smuggle in the rule about English section 2 avoids.")
    print()
    co = got["cofield"]
    younger = [p for p in co if p["count_idx"] < p["idx"]]
    print("      %-52s %d of %d" % ("pairs published beside a count",
                                    len(co), len(got["pairs"])))
    print("      %-52s %d" % ("  the COUNT is the younger of the two",
                              len(younger)))
    print("      %-52s %d" % ("  the NAME is the younger of the two",
                              sum(1 for p in co if p["count_idx"] > p["idx"])))
    print("      %-52s %d" % ("  written in the SAME commit",
                              sum(1 for p in co if p["count_idx"] == p["idx"])))
    print("      %-52s %d" % ("  and OVERTAKEN by a pin",
                              len(got["copublished"])))
    print()
    print("  BOTH DATES ARE MEASURED AND NOT ONE.  The claim has two halves --")
    print("  the count stays right, the name rots -- and a file measuring the")
    print("  name's age while asserting the count's would be the defect this")
    print("  arc reports.  `Younger` is in commits of this repository, which is")
    print("  the unit the record moves in.")
    print()
    for p in sorted(co, key=lambda p: (p["path"], p["line"])):
        print("  %s:%d   %s%s"
              % (p["path"], p["line"], p["base"],
                 "   OVERTAKEN" if p["after"] else ""))
        print("      commits to this record       %d" % p["record_commits"])
        print("      section                      %s" % p["head"][:52])
        print("      the record's last word       %s" % p["text"][:52])
        print("          written at               %s" % (p["blame"] or "-")[:7])
        print("      the count beside it          %s" % p["count_line"][:52])
        print("          written at               %s   %s"
              % ((p["count_blame"] or "-")[:7],
                 "YOUNGER" if p["count_idx"] < p["idx"] else
                 "older" if p["count_idx"] > p["idx"] else "same commit"))
        if p["after"]:
            print("      pinned since, by             %s"
                  % ",".join(h[:7] for h in p["after"]))
    print()
    print("  CO-PUBLICATION IS RARE AND THE POPULATION IS PRINTED RATHER THAN")
    print("  SUMMARISED, because %d rows is a number a reader can check and a"
          % len(co))
    print("  percentage is not.  %d of %d are OVERTAKEN at AS_OF -- and the"
          % (len(got["copublished"]), len(co)))
    print("  instance mg-0bf1 was filed about IS OF THIS SHAPE and is not in")
    print("  the list, because the commit before this one closed it.  Section 4")
    print("  runs the rule at AS_OF^ so that zero is falsifiable rather than")
    print("  merely empty.")
    print()
    print("  AND THE CLAIM AS FILED IS TOO WIDE, WHICH THE COMMITS COLUMN IS")
    print("  WHAT SAYS.  `The count will stay right and the name will rot` is")
    print("  not a property of COUNTS AND NAMES.  %d of the %d pairs have both"
          % (sum(1 for p in co if p["count_idx"] == p["idx"]), len(co)))
    print("  fields written in ONE COMMIT and never touched again -- the count")
    print("  in those records did not stay right by being maintained, it stayed")
    print("  right because NOTHING IN THE RECORD IS MAINTAINED, and a name")
    print("  beside it would rot exactly as fast.  Where the two dates DO come")
    print("  apart it goes both ways: %d have the younger count and %d the"
          % (len(younger), sum(1 for p in co if p["count_idx"] > p["idx"])))
    print("  younger name.  The narrowed claim the corpus does support:")
    print()
    print("      IN A RECORD THAT IS APPENDED TO, THE SUMMARY LINE IS")
    print("      RESTATED EVERY TRANCHE AND THE OFFER LIST IS NOT.")
    print()
    print("  That is a property of a RUNNING LOG and not of a document, and the")
    print("  commits column is where a reader can see which is which -- the")
    print("  extremes here are %d and %d commits.  This directory's own README"
          % (max(p["record_commits"] for p in co) if co else 0,
             min(p["record_commits"] for p in co) if co else 0))
    print("  is the log, and mg-e8b0's instance is what a log does to a name.")
    print()

    print(rule)
    print("4  THE INSTANCE THIS RULE WAS BUILT FROM, BEFORE AND AFTER")
    print(rule)
    print()
    print("  A rule that reports nothing is indistinguishable from a rule that")
    print("  SEES nothing, and this rule's own instance was closed in the")
    print("  commit before this one.  So it is run at BOTH revisions:")
    print()
    for rev in (AS_OF + "^", AS_OF):
        v = pair_verdict("code/asof_census_20ee/README.md",
                         "species_remainder_f8fa", rev)
        print("      at %-12s %d mention(s), newest %s -> %s"
              % (rev, v["mentions"], (v["newest"] or "-")[:7],
                 "OVERTAKEN by %s" % ",".join(h[:7] for h in v["after"])
                 if v["overtaken"] else "NOT OVERTAKEN"))
        print("          %s" % v["text"][:62])
    print()
    print("  AT AS_OF^ THE ONLY SENTENCE NAMING IT WAS TRANCHE 1's OFFER, four")
    print("  tranches older than e29ba2a, which is this arc's own tranche 2.")
    print("  AT AS_OF tranche 9's annotation is the newest mention and it is")
    print("  younger than the pin, so the pair is accounted for.  THE RULE")
    print("  MOVED BECAUSE THE RECORD DID, and P30 asserts exactly that.")
    print()
    print("  AND IT DOES NOT FIRE ON THE CASE THAT LOOKS THE SAME AND IS NOT:")
    v = pair_verdict("code/asof_census_20ee/README.md",
                     "landscape_repair_audit_3b51")
    print("      %-52s %s" % ("landscape_repair_audit_3b51 in this record",
                              "OVERTAKEN" if v["overtaken"] else "NOT OVERTAKEN"))
    print("  Tranche 3 headed a section `the next candidate, diagnosed but NOT")
    print("  pinned` and tranche 4 landed that pin.  Tranche 3's section still")
    print("  says it and always will -- THE CORRECTION IN THIS ESTATE IS A")
    print("  YOUNGER SENTENCE, NOT AN EDIT TO AN OLDER ONE -- which is why the")
    print("  rule is per (record, name) and not per line.  Per line this record")
    print("  has %d overtaken mention(s) of it and none of them is a defect."
          % per_line_overtaken("code/asof_census_20ee/README.md",
                               "landscape_repair_audit_3b51"))
    print()

    print(rule)
    print("5  WHAT THIS FILE CANNOT SAY, RESTATED WHERE IT IS READ")
    print(rule)
    print()
    print("  * OVERTAKEN IS NOT STALE.  A pin is not a repair, and a reference")
    print("    may be to something the pin did not touch.  It says the record")
    print("    has not spoken since; it does not say what changed.")
    print("  * NOT OVERTAKEN IS NOT CURRENT.  %d pairs are not flagged, and"
          % (len(got["pairs"]) - len(got["over"])))
    print("    that is a statement about the REPOSITORY.  An instrument goes")
    print("    stale when its CORPUS moves and no pin lands on it at all.")
    print("  * BLAME IS THE LAST TOUCH, NOT THE ORIGIN.  A reflow re-dates a")
    print("    sentence it did not change, so the OVERTAKEN count is a LOW")
    print("    WATER MARK.  N29 asserts that on the rule.")
    print("  * ZERO MENTIONS IS ZERO PAIRS.  %d work-list row(s) are named by"
          % len(got["unnamed"]))
    print("    no record in the tree -- %s -- and this rule"
          % (", ".join(got["unnamed"]) or "none"))
    print("    is blind to them BY CONSTRUCTION: a record that should name an")
    print("    instrument and never does cannot have a last word about it.")
    print("    N30 counts them, and the count is the one figure here that")
    print("    GROWS when the corpus gets worse.")
    print("  * THE ORDER INDEX ASSUMES A LINEAR HISTORY.  There are %s merge"
          % text(git("rev-list", "--count", "--merges", AS_OF)).strip())
    print("    commits at AS_OF, because the refinery REBASES -- so the")
    print("    comparison is exact HERE by a property of the repository and not")
    print("    by anything this file does.  Counted rather than assumed.")
    print()
    print("CONDITION 0 (exemplars): %d of %d pairs OVERTAKEN, %d in a foreign "
          "record, %d beside a count, at %s"
          % (len(got["over"]), len(got["pairs"]), len(got["foreign"]),
             len(got["copublished"]), AS_OF))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
