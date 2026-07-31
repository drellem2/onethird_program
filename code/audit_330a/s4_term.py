"""s4_term.py -- THE TERM, AT EVERY SITE IT APPEARS.

  (i)   COUNT THE POPULATION THE TERM DENOTES AND THE POPULATION THE WALK
        VISITS, AND PRINT BOTH.  By an independent AST walk of the census's
        two files.  The parent's were 39 and 17, with 22 in no column.
  (ii)  AND THE 22, NAMED.  A number for what is uncovered that cannot be
        pointed at is the same silence as no number at all.
  (iii) THE QUALIFIER AT ALL 15 SITES.  The 15 unqualified in-d01ff32 sites
        mg-2c77's finding names, re-derived at mg-2c77's own revision by
        mg-2c77's own rule, then re-scored at HEAD.
  (iv)  THE RULER WAS NOT MOVED.  A site carrying only the HYPHENATED
        `deciding-condition` must still score UNQUALIFIED; asserted on a
        constructed site and on the real tree.
  (v)   MY OWN CHOICE, AND IT IS NOT ON ANY LIST IN THE BRIEF.  The repair
        scores the term over `the files d01ff32 touched` -- a population
        PINNED at d01ff32.  Four commits landed after the repair.  The same
        rule is re-scoped to the WHOLE TREE AT HEAD, so that a live claim
        introduced after the repair would be seen.  A population pinned at a
        revision is the correct choice for a finding stated at that
        revision, and it is also a population that stops growing while the
        tree does not.

No number here is taken from anybody's transcript except where a row says
READ.  Nothing here writes into any other ticket's directory.
"""

import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib330a as L                                          # noqa: E402

# mg-2c77's own revision for its census transcript, and the repair mg-2c77
# audited.  PINNED, with the reason: they are the revisions the finding is
# STATED at, and re-deriving them would be A-1 inside an audit of A-1.
Q3_REV = "adcfb1f18a8d102e0496a7060d0ae38d913c6a27"
QUOTE_MARKERS = ("NO FURTHER", "is read as")

R = L.Report(
    selfpop="every git read, source read and AST parse this script performs, "
            "the requirement that both census files parse at both revisions "
            "and that neither operand walk come back empty, and the "
            "requirement that the scoring rule return more than one label "
            "over the tree it scores",
    findpop="every operand of every `and`/`or` anywhere in the census's two "
            "files, against the operands inside a deciding condition, at "
            "HEAD; the 15 unqualified in-d01ff32 sites mg-2c77's finding "
            "names, re-derived at adcfb1f by mg-2c77's rule and re-scored at "
            "HEAD; the hyphenated-form control on the rule itself; and every "
            "site in the WHOLE TREE at HEAD stating the term, scored for the "
            "qualifier and classified live / transcript / record")

L.banner("S4", "THE TERM -- BOTH POPULATIONS, AND THE QUALIFIER AT EVERY SITE")

# ---------------------------------------------------------------------------
L.rule("(i) THE POPULATION THE TERM DENOTES, AND THE ONE THE WALK VISITS")
# ---------------------------------------------------------------------------

print("""   `explicit boolean operand`, UNQUALIFIED -- i.e. NOT narrowed to a
   deciding condition -- denotes every operand of every `and`/`or`
   ANYWHERE in the census's two files: in a `while`, in an assignment,
   in an `if` whose body assigns and breaks.  The census's four
   columns classify only the ones inside a deciding condition, which
   is the narrower population.  Both are walked here, from kern5f9a's
   sentence for `decides a return`, and both are printed so the
   subtraction is on the page.
""")

print("   %-24s %-38s %-22s %s"
      % ("file", "operands of every and/or, anywhere", "of those, deciding",
         "in no column"))
tot_all = tot_dec = 0
OUTSIDE = []
for rel in L.CENSUS_FILES:
    src = L.read_worktree(rel)
    base = os.path.basename(rel)
    try:
        allo = L.all_operands(src, base)
        deco = L.deciding_operands(src, base)
    except SyntaxError as exc:
        R.selferr("%s does not parse: %s" % (rel, exc))
        continue
    R.selfgate(bool(allo) or bool(deco),
               "both walks come back empty for %s" % rel)
    dspans = {o["span"] for o in deco}
    out = [o for o in allo if o["span"] not in dspans]
    OUTSIDE.extend(out)
    print("   %-24s %-38d %-22d %d"
          % (base, len(allo), len(deco), len(out)))
    tot_all += len(allo)
    tot_dec += len(deco)
print("   %-24s %-38d %-22d %d"
      % ("ALL", tot_all, tot_dec, tot_all - tot_dec))

print("""
   COUNTED HERE, not read: %d operands denoted, %d visited by the
   census's columns, %d in no column of it.  mg-69d1's repaired
   p1_bound.py (ii) prints 39 / 17 / 22.
""" % (tot_all, tot_dec, tot_all - tot_dec))

R.gate(tot_all == 39,
       "the term denotes %d operands in the census's two files where the "
       "repair prints 39" % tot_all)
R.gate(tot_dec == 17,
       "%d operands lie inside a deciding condition where the repair prints "
       "17" % tot_dec)
R.gate(tot_all - tot_dec == 22,
       "%d operands are in no column where the repair prints 22"
       % (tot_all - tot_dec))
R.selfgate(len(OUTSIDE) == tot_all - tot_dec,
           "the named residue has %d rows and the subtraction says %d"
           % (len(OUTSIDE), tot_all - tot_dec))

# AND THE PRINTED NUMBER, READ OUT OF THE REPAIR'S OWN TRANSCRIPT.
p1 = L.read_worktree("code/repair_69d1/out_p1_bound.txt")
row = [ln for ln in p1.splitlines() if ln.strip().startswith("ALL")
       and "39" in ln]
print("   READ (not counted) -- the row mg-69d1's repaired p1_bound.py "
      "prints:\n     %s" % (row[0].strip() if row else "*** NOT FOUND"))
R.gate(bool(row),
       "the repaired p1_bound.py transcript does not carry a row printing 39 "
       "beside 17 -- the wider population is not published where the repair "
       "says it is")

# ---------------------------------------------------------------------------
L.rule("(ii) AND THE 22, NAMED")
# ---------------------------------------------------------------------------

print("""   The 22 are outside every deciding condition, so they are outside
   the sweep's reach AND outside the census's table.  That is a
   statement about what the census covers.  Named, because a count of
   what is uncovered that cannot be pointed at is the same silence as
   no count at all.
""")
print("   %-18s %-26s %-4s %s" % ("file", "function", "op", "operand text"))
for o in sorted(OUTSIDE, key=lambda o: (o["file"], o["span"])):
    print("   %-18s %-26s %-4s %s"
          % (o["file"], o["func"], o["op"],
             (o["text"] or "").replace("\n", " ")[:44]))
print("   %-18s %d row(s)" % ("ALL", len(OUTSIDE)))

# ---------------------------------------------------------------------------
L.rule("(iii) THE QUALIFIER AT ALL 15 SITES")
# ---------------------------------------------------------------------------


def grep_sites(needle, rev=None):
    """[(path, line)] for every line stating `needle`.

    `git grep -F`, untracked included when reading the worktree, because
    this audit's own files are untracked at the moment it runs and a
    population that excludes them by accident is a population drawn to pass.
    """
    args = ["grep", "-n", "-F"]
    args += [needle, rev] if rev else ["--untracked", needle]
    out = L.git_quiet(*args)
    got = []
    for line in out.splitlines():
        if not line.strip():
            continue
        rest = line.split(":", 1)[1] if rev else line
        path, _, tail = rest.partition(":")
        got.append((path, tail.split(":", 1)[0]))
    return got


_CACHE = {}


def lines_of(path, rev=None):
    key = (rev, path)
    if key not in _CACHE:
        if rev:
            _CACHE[key] = L.show_or_empty(rev, path).splitlines()
        else:
            try:
                _CACHE[key] = L.read_worktree(path).splitlines()
            except (IOError, OSError):
                _CACHE[key] = []
    return _CACHE[key]


def disposition(path, lineno, rev=None):
    """mg-2c77's three labels, from mg-2c77's rule, character for character.

    QUALIFIED iff the UNHYPHENATED words `deciding condition` stand within 3
    lines.  A QUOTATION if `NO FURTHER` or `is read as` is in the same window
    -- the wide BOUND being quoted in order to correct it is a different
    sentence about a different thing.  Otherwise the site asserts the census
    unqualified.
    """
    lines = lines_of(path, rev=rev)
    i = int(lineno) - 1
    w = "\n".join(lines[max(0, i - 3):i + 4])
    if any(m in w for m in QUOTE_MARKERS):
        return "quotes the wide BOUND"
    if L.QUALIFIER in w:
        return "census, QUALIFIED"
    return "*** census, UNQUALIFIED"


d01_files = set(L.git("show", "--name-only", "--format=", L.D01FF32).split())
print("   files d01ff32 touched : %d" % len(d01_files))

then = [(p, n, disposition(p, n, rev=Q3_REV))
        for p, n in grep_sites(L.TERM, rev=Q3_REV)]
then_unq = [(p, n) for p, n, d in then
            if d.startswith("***") and p in d01_files]
print("   sites stating the term at %s        : %d" % (Q3_REV[:8], len(then)))
print("   of those, in files d01ff32 touched AND unqualified : %d"
      % len(then_unq))
labels_then = sorted({d for _p, _n, d in then})
print("   NON-VACUITY -- distinct labels the rule returned there: %d"
      % len(labels_then))
for lab in labels_then:
    print("      %s" % lab)

R.selfgate(len(then_unq) == 15,
           "the rule re-derives %d unqualified in-d01ff32 sites at %s where "
           "mg-2c77's finding names 15; the control fails and everything "
           "below rests on a rule that does not reproduce the table it "
           "audits" % (len(then_unq), Q3_REV[:8]))
R.selfgate(len(labels_then) >= 2,
           "the rule returned one label for every site at %s -- it is not "
           "distinguishing and every table below says nothing" % Q3_REV[:8])

now = [(p, n, disposition(p, n)) for p, n in grep_sites(L.TERM)]
now_by_file = {}
for p, n, d in now:
    now_by_file.setdefault(p, []).append(d)


def kind_of(path):
    base = os.path.basename(path)
    if base.startswith("out_") and base.endswith(".txt"):
        return "transcript"
    if base == "PREDICTIONS.md":
        return "record, pre-run"
    return "live claim"


print("\n   THE 15, EACH RE-SCORED AT HEAD.  Scored PER FILE, because a line\n"
      "   number is an anchor into a file's TEXT and editing the file moves\n"
      "   every site below the edit -- scoring the old line number in the new\n"
      "   file would be A-1 in miniature.\n")
print("   %-52s %-5s %-16s %s"
      % ("site (line as at %s)" % Q3_REV[:8], "line", "kind", "at HEAD"))
still = []
for path, lineno in sorted(then_unq):
    labels = now_by_file.get(path)
    worst = ("gone" if labels is None
             else ("*** census, UNQUALIFIED"
                   if any(x.startswith("***") for x in labels)
                   else sorted(set(labels))[0]))
    print("   %-52s %-5s %-16s %s" % (path, lineno, kind_of(path), worst))
    if worst.startswith("***"):
        still.append(path)

print("\n   of the 15 sites, files still carrying an unqualified site : %d"
      % len(set(still)))
R.gate(not still,
       "%d file(s) in mg-2c77's own 15-site population still state the "
       "census without the deciding-condition qualifier at HEAD: %s"
       % (len(set(still)), ", ".join(sorted(set(still)))))

# ---------------------------------------------------------------------------
L.rule("(iv) THE RULER WAS NOT MOVED")
# ---------------------------------------------------------------------------

print("""   mg-2c77's rule looks for the UNHYPHENATED words.  Its own
   q3_operands.py lines carrying `deciding-condition` were scored
   UNQUALIFIED by it.  If the repair had widened the rule to accept the
   hyphenated form, 15 sites would close without a word being written.
   Checked on a constructed site whose answer is known before the rule
   runs, and then on the real tree.
""")

HYPH = ["prose above", "the 17 explicit boolean operands",
        "inside a deciding-condition of the two files", "prose below"]
UNHY = ["prose above", "the 17 explicit boolean operands",
        "inside a deciding condition of the two files", "prose below"]


def score_lines(lines, idx):
    w = "\n".join(lines[max(0, idx - 3):idx + 4])
    if any(m in w for m in QUOTE_MARKERS):
        return "quotes the wide BOUND"
    if L.QUALIFIER in w:
        return "census, QUALIFIED"
    return "*** census, UNQUALIFIED"


print("   constructed site carrying `deciding-condition` : %s"
      % score_lines(HYPH, 1))
print("   constructed site carrying `deciding condition` : %s"
      % score_lines(UNHY, 1))
R.gate(score_lines(HYPH, 1).startswith("***"),
       "the scoring rule accepts the HYPHENATED `deciding-condition` as a "
       "qualifier -- the ruler has been widened and the 15 sites could close "
       "without a word being written")
R.selfgate(not score_lines(UNHY, 1).startswith("***"),
           "the scoring rule rejects the unhyphenated form too, so it cannot "
           "distinguish anything")

hyph_sites = [(p, n) for p, n in grep_sites("deciding-condition")]
print("\n   and on the REAL tree: %d line(s) carry the hyphenated form."
      % len(hyph_sites))
hyph_pass = [(p, n) for p, n in hyph_sites
             if L.TERM in "\n".join(lines_of(p)[max(0, int(n) - 1):int(n)])
             and not disposition(p, n).startswith("***")]
qualifying = []
for p, n in hyph_sites:
    lines = lines_of(p)
    i = int(n) - 1
    w = "\n".join(lines[max(0, i - 3):i + 4])
    if L.TERM in w and L.QUALIFIER not in w:
        qualifying.append((p, n))
print("   of those, in a window stating the term but NOT carrying the\n"
      "   unhyphenated form (i.e. sites the hyphen alone would have to\n"
      "   carry) : %d" % len(qualifying))
for p, n in qualifying:
    print("      %s:%s" % (p, n))

# ---------------------------------------------------------------------------
L.rule("(v) MY OWN CHOICE -- THE SAME RULE, RE-SCOPED TO HEAD")
# ---------------------------------------------------------------------------

print("""   NAMED IN ADVANCE IN PREDICTIONS.md, AND ON NO LIST IN THE BRIEF.

   The repair scores the term over `the files d01ff32 touched`.  That
   is the right population for a finding STATED at d01ff32 -- a
   population re-derived as `the files the newest repair touched` is
   A-1 -- but it is a population that stops growing while the tree does
   not.  Four commits landed after dfa263c:
""")
after = L.git("log", "--oneline", "--format=%h %s", "%s..HEAD" % L.REPAIR_8D5E)
for ln in after.splitlines():
    print("     %s" % ln[:96])
n_after = len([ln for ln in after.splitlines() if ln.strip()])
print("   commits since the repair : %d" % n_after)

print("""
   So the same rule, unchanged, over EVERY site in the tree at HEAD --
   untracked files included, which is where this audit's own files are.
""")
by_kind = {}
for p, n, d in now:
    by_kind.setdefault(kind_of(p), []).append((p, n, d))
print("   %-18s %-8s %-10s %s" % ("kind", "sites", "unqualified", "files"))
for k in ("live claim", "transcript", "record, pre-run"):
    rows = by_kind.get(k, [])
    unq = [r for r in rows if r[2].startswith("***")]
    print("   %-18s %-8d %-10d %d"
          % (k, len(rows), len(unq), len({r[0] for r in rows})))
print("   %-18s %-8d %-10d %d"
      % ("ALL", len(now), len([r for r in now if r[2].startswith("***")]),
         len({r[0] for r in now})))

live_unq = [r for r in by_kind.get("live claim", []) if r[2].startswith("***")]
mine = [r for r in live_unq if r[0].startswith("code/audit_330a/")]
theirs = [r for r in live_unq if not r[0].startswith("code/audit_330a/")]

print("""
   UNQUALIFIED LIVE CLAIMS AT HEAD, NAMED -- and this audit's OWN
   files are in the population and marked, not excluded by path:
""")
for p, n, d in sorted(theirs):
    print("      THEIRS  %s:%s" % (p, n))
for p, n, d in sorted(mine):
    print("      MINE    %s:%s" % (p, n))
print("   live claims unqualified, not mine : %d" % len(theirs))
print("   live claims unqualified, MINE     : %d" % len(mine))

theirs_unq_all = [r for r in now if r[2].startswith("***")
                  and not r[0].startswith("code/audit_330a/")]

print("""
   AND AGAINST THE REPAIR'S OWN PUBLISHED NUMBER -- which is the point
   of re-scoping, and the reason it is done by re-measuring rather
   than by reading.  dfa263c's commit message says:

     `20 sites remain unqualified in the tree, every one a record,
      named individually in r3 (iv).`

   Re-derived here, at HEAD, excluding this audit's own files:
     sites stating the term unqualified              : %d
   The two numbers %s.  The population is the same population
   and this audit found no site the repair did not name.

   BUT THE WORD `record` IS DOING TWO JOBS.  r3 (iii) derives a site's
   KIND FROM ITS PATH -- `out_*.txt` is a transcript, `PREDICTIONS.md`
   is a record, ANYTHING ELSE IS A LIVE CLAIM -- and that rule is what
   decides whether a site gets EDITED.  r3 (iv) then labels the same
   residue by SCOPE -- whose ticket owns the file -- and the summary
   sentence reports the scope label as though it were the kind label.
   Under the repair's OWN path-derived kind rule, of those %d sites:

     transcripts and prediction files (records by the path rule) : %d
     LIVE CLAIMS (source and prose by the path rule)             : %d

   Not one of them is a defect: they are other tickets' statements of
   what those tickets found, and rewriting another ticket's record to
   make this ticket's count come out is the failure this arc exists to
   avoid.  The declining is right.  What is not right is the SENTENCE:
   `every one a record` is true under the scope rule and false under
   the kind rule the same script uses three sections earlier, and a
   reader who applies r3 (iii)'s rule to r3 (iv)'s list gets %d live
   claims where the summary says 0.

   That is A-2's own shape -- ONE WORD OVER TWO POPULATIONS -- in the
   summary sentence of the repair that fixed a word over two
   populations.
""" % (len(theirs_unq_all),
       "AGREE" if len(theirs_unq_all) == 20 else "DISAGREE",
       len(theirs_unq_all),
       len(theirs_unq_all) - len(theirs), len(theirs), len(theirs)))

R.gate(not theirs,
       "dfa263c's summary says `20 sites remain unqualified in the tree, "
       "EVERY ONE A RECORD`.  Re-derived at HEAD the residue is %d sites -- "
       "the same 20, none missed -- but %d of them are LIVE CLAIMS under the "
       "path-derived kind rule r3 (iii) itself uses to decide treatment "
       "(source and prose, not transcripts or prediction files): %s.  The "
       "sites are correctly declined; the word `record` in the summary is "
       "the SCOPE label from r3 (iv) reported as the KIND label from "
       "r3 (iii), which is one word over two populations -- A-2's own shape, "
       "in the sentence summarising the repair of A-2"
       % (len(theirs_unq_all), len(theirs),
          ", ".join("%s:%s" % (p, n) for p, n, _d in theirs)))
R.gate(not mine,
       "%d LIVE claim(s) in THIS audit's own files state the census "
       "unqualified: %s.  Scored by the same rule as everybody else's, "
       "because a rule that exempts its author is not a rule"
       % (len(mine), ", ".join("%s:%s" % (p, n) for p, n, _d in mine)))

print("""
   AND THE RESIDUE, WHICH IS NOT A DEFECT.  The unqualified sites that
   remain are RECORDS -- transcripts of runs that happened, and
   prediction files committed before their runs.  A transcript is a
   measurement and editing one falsifies it; a prediction file
   committed before its run is not a later ticket's to rewrite.  They
   are counted above and named here so the number is not a bare one:
""")
resid = [r for r in now if r[2].startswith("***")
         and kind_of(r[0]) != "live claim"]
for p, n, _d in sorted(resid):
    print("      %-16s %s:%s" % (kind_of(p), p, n))
print("   records stating the term unqualified : %d" % len(resid))

R.done()
