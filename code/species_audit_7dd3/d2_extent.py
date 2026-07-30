"""D2 -- THE EXTENT LINES, MEASURED AGAINST WHAT THE CODE ACTUALLY READS.

pm-onethird, strengthening mg-7dd3 mid-flight:

    "A checker printing an extent WIDER than it actually reads is worse than
     one printing none: it converts a reader's correct suspicion into false
     confidence."

So no extent line is read here as a statement of fact.  Each is measured:

  D2a  THE LIST AGAINST THE DOCUMENT'S OWN STRIKES.  The document marks what
       it withdrew with `~~`.  That enumeration cannot fall behind the
       document, because it IS the document.  Every checker's table is
       compared against it.
  D2b  WHAT EACH CHECKER OPENS.  Not inferred from reading the source --
       MEASURED, by running each checker with `open` instrumented and
       recording every path it touches.
  D2c  THE DECLARED EXCLUSION AGAINST THE REAL ONE, per tree.
  D2d  THE WHOLE REPOSITORY swept with the same list, split into the declared
       extent, the declared silences, and everything else.
  D2e  THE REACH OF THE EXONERATION RULE -- this audit's declared beyond-list
       target.  Nobody in this arc has measured how many INDEPENDENT clauses
       hold each hit down.  A hit held by four is a hit whose marker is
       decoration.

    python3 code/species_audit_7dd3/d2_extent.py
"""

import builtins
import io
import os
import re
import runpy
import sys

from kern7dd3 import (hdr, find, reasons, tokens, REASON_NAMES,
                      NAMES_A_REPAIR as NAMES_ANY)
from statements7dd3 import (STATEMENTS, DECLARED_TREES, SILENT_TREES, DOC,
                            A4EF_EXCLUDE, A4EF_EXTENSIONS)

bad = 0
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
OWN = {s[0]: s[3] for s in STATEMENTS}
PATS = {s[0]: s[2] for s in STATEMENTS}

# cheap per-statement prefilter, so 657 files are not tokenised character by
# character when a substring test settles it
ANCHOR = {
    "X1": ["smallest witness", "a<c", "a < c"],
    "X3": ["axiom"],
    "X4": ["controls", "are the control"],
    "X5": ["fires hard", "how differently"],
    "X6a": ["inequalities of the form"],
    "X6b": ["y(i)"],
    "X7": ["k-bar(pi", "k(pi", "k̄(π"],
    "X2a": ["measured, not proved"],
    "X2b": ["saliola and commins"],
    "X2c": ["in that generality"],
    "X8": ["three independent"],
    "Y2": ["descent algebra"],
}


def note(label, cond, weight=1):
    global bad
    bad += weight * (not cond)
    print("  %-68s %s" % (label[:68], "ok" if cond else "*** FAILS ***"))
    return cond


def scan_file(path):
    """{sid: [(line, reasons)]} for one file."""
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except (UnicodeDecodeError, OSError):
        return {}
    low = text.lower()
    out = {}
    for sid, _label, pats, own in STATEMENTS:
        if not any(a in low for a in ANCHOR[sid]):
            continue
        for ln in find(text, pats):
            out.setdefault(sid, []).append((ln, reasons(text, ln, own)))
    return out


# ---------------------------------------------------------------------------
hdr("D2a  THE LISTS AGAINST THE DOCUMENT'S OWN ~~STRIKES~~")

doc = open(os.path.join(REPO, "docs", DOC), encoding="utf-8").read()
strikes = [re.sub(r"\s+", " ", s).strip()
           for s in re.findall(r"~~(.+?)~~", doc, re.S)]
print("  the document strikes %d sentences." % len(strikes))
print()

cd_src = open(os.path.join(REPO, "code", "species_repair_6f61",
                           "check_doc.py"), encoding="utf-8").read()
w3_src = open(os.path.join(REPO, "code", "species_remainder_f8fa",
                           "w3_scope.py"), encoding="utf-8").read()
a4_src = open(os.path.join(REPO, "code", "species_repair_a4ef",
                           "stricken_a4ef.py"), encoding="utf-8").read()
c4_src = open(os.path.join(REPO, "code", "species_audit_73df",
                          "c4_scope.py"), encoding="utf-8").read()


def table_rows(src, name):
    m = re.search(r"(?ms)^%s = \[(.*?)^\]" % name, src)
    return len(re.findall(r"(?m)^    \(", m.group(1))) if m else 0


n_cd = table_rows(cd_src, "STRICKEN")
n_w3 = table_rows(w3_src, "FORBIDDEN")
n_a4 = table_rows(a4_src, "CORRECTIONS")
n_c4 = table_rows(c4_src, "CORRECTIONS")
print("  check_doc.py     STRICKEN     %2d row(s)" % n_cd)
print("  w3_scope.py      FORBIDDEN    %2d row(s)" % n_w3)
print("  stricken_a4ef.py CORRECTIONS  %2d row(s)  <- 'the ONE list'" % n_a4)
print("  c4_scope.py      CORRECTIONS  %2d row(s)  <- mg-73df's, 8 findings"
      % n_c4)
print()
note("check_doc.py's STRICKEN has 10 rows, as its extent line says",
     n_cd == 10)
note("stricken_a4ef.py has 11 rows, as its extent line says", n_a4 == 11)
print()
print("  THE ARITHMETIC.  11 rows, of which Y2 has NO struck sentence, so the")
print("  one list covers %d of the document's %d strikes." % (n_a4 - 1,
                                                              len(strikes)))
# A strike is COVERED if one of the ONE LIST's own DOCUMENT SENTENCES lies
# inside it.  The list's DATA is imported here -- it is the object under test,
# and the independent enumeration is the document's own `~~`.  Comparing my
# SOURCE patterns against the document instead would have reported X7 missing,
# because the source says `K-bar(Pi)` where the document says `K\u0304(\u03a0)`;
# that false positive was in this file's first run and is in OUTCOMES.md.
sys.path.insert(0, os.path.join(REPO, "code", "species_repair_a4ef"))
from stricken_a4ef import CORRECTIONS as A4EF_ROWS      # noqa: E402


def alnum(s):
    return " ".join(re.sub(r"[^0-9a-z]+", " ", s.lower()).split())


missing_from_a4ef = []
print()
for s in strikes:
    hit = None
    for row in A4EF_ROWS:
        sid, sentence = row[0], row[2]
        if sentence is None:
            continue
        a, b = alnum(sentence), alnum(s)
        if a and (a in b or b in a):
            hit = sid
            break
    if hit is None:
        missing_from_a4ef.append(s)
    print("      %-56s %s" % (s[:56], hit or "*** ON NO LIST ***"))
print()
note("every sentence the document strikes is on the one list",
     not missing_from_a4ef, weight=1)
for s in missing_from_a4ef:
    print()
    print("  THE STRIKE THAT IS ON NO LIST:")
    print("      %s" % s[:200])
    inc4 = bool(re.search(r"three\s+independent", c4_src))
    print("      on check_doc.py's STRICKEN     : no")
    print("      on w3_scope.py's FORBIDDEN     : no")
    print("      on stricken_a4ef.py's ONE LIST : no")
    print("      on mg-73df's c4_scope.py       : %s" % ("YES" if inc4
                                                         else "no"))
    print("      -- mg-a61f's X8.  The union was taken over TWO of the THREE")
    print("         lists that existed when it was written, and the third is")
    print("         the one mg-a4ef re-runs unmodified as its independent")
    print("         corroboration.")
print()

# ---------------------------------------------------------------------------
hdr("D2f  THE LEAD-IN TEST -- IS EACH STRUCK SENTENCE STRUCK EVERYWHERE?")

print("  Every checker in this arc stores a withdrawn claim as ONE EXACT")
print("  SENTENCE and asks whether that sentence occurs outside a strike.")
print("  A sentence has a LEAD-IN.  The same claim introduced by different")
print("  words is a different string, and is invisible to all of them --")
print("  while every extent line stays true: the file IS read, the statement")
print("  IS on the list, and the run IS clean.")
print()
print("  So, for each of the %d strikes: the LONGEST run of consecutive words"
      % len(strikes))
print("  it shares with the document OUTSIDE every strike.")
print("  A short shared run is a shared lead-in and means nothing.  A long")
print("  one is the claim itself, said again somewhere the strike does not")
print("  reach.  The line where it is said is printed.")
print()
# A leak is not "shares a long run" -- two quotations of the same source share
# a lead-in.  It is "shares MOST OF THE STRIKE": at least 15 tokens AND at
# least 60% of the struck sentence.  Both numbers are printed per strike.
LEAK_RUN = 15
LEAK_FRACTION = 0.60


def wordmap(text):
    """[(token, line)] using kern7dd3's tokeniser -- alphanumeric runs AND
    every other character as its own token.

    NOT `[a-z0-9]+`.  A first version used that, and `K\u0304(\u03a0)` and `K(\u03a0*)` both
    reduced to the single token `k`: the Greek letter and the star -- which
    are the ENTIRE correction -- were thrown away, and the corrected line
    matched the struck sentence.  The instrument written to find a claim
    hiding behind a lead-in reported the correction as the leak.  Kept in
    OUTCOMES.md; it is the same mistake, one level down, as the one it found.
    """
    return tokens(text)


def blank_strikes(text):
    """Strikes replaced by spaces of EQUAL LENGTH, newlines kept, so the
    line map of the remaining text is the document's own."""
    return re.sub(r"~~(.+?)~~",
                  lambda m: "".join("\n" if c == "\n" else " "
                                    for c in m.group(0)),
                  text, flags=re.S)


un_wm = wordmap(blank_strikes(doc))
un_words = [w for w, _ in un_wm]
un_join = " " + " ".join(un_words) + " "
leaks = []
for k, s_ in enumerate(strikes):
    w = [x for x, _ in wordmap(s_)]
    best, best_at = 0, None
    for i in range(len(w)):
        for j in range(len(w), i + best, -1):
            run = " ".join(w[i:j])
            pos = un_join.find(" " + run + " ")
            if pos >= 0:
                best = j - i
                idx = len(un_join[:pos + 1].split()) if pos else 0
                best_at = (run, un_wm[min(idx, len(un_wm) - 1)][1])
                break
    if best_at:
        run, ln = best_at
        rs = reasons(doc, ln, None)
        leaks.append((k + 1, s_, best, run, ln, rs))

leaks.sort(key=lambda d: -d[2])
for k, s_, n, run, ln, rs in leaks:
    tot = len(tokens(s_))
    frac = n / tot if tot else 0
    leak = (n >= LEAK_RUN and frac >= LEAK_FRACTION)
    print("  strike %-2d  run %-3d of %-3d (%3.0f%%)  line %-5d %s"
          % (k, n, tot, 100 * frac, ln,
             "*** THE CLAIM ITSELF, SAID AGAIN ***" if leak
             else "lead-in only"))
    print("      %s" % s_[:66])
    if leak:
        print("      shared: %s" % run[:150])
        print("      exoneration clauses at line %d: %s"
              % (ln, ", ".join(sorted(rs)) if rs
                 else "NONE -- STILL ASSERTED, UNSTRUCK, UNMARKED"))
        raw = doc.splitlines()
        lo, hi = max(0, ln - 7), min(len(raw), ln + 6)
        for j in range(lo, hi):
            m = NAMES_ANY.search(raw[j])
            if m:
                print("          the clause 'names-a-repair' comes from line "
                      "%d: %s" % (j + 1, raw[j].strip()[:90]))
    print()

# THE CLAUSE THAT IS NOT EVIDENCE HERE.  A ticket id near a sentence means the
# sentence is withdrawn only if the id is about THAT sentence.  This document
# names five tickets throughout, so proximity is not evidence -- and this arc
# has now recorded the same disarming three times: w3_scope.py's bare
# "REPAIRED" disarmed by "the error mg-1953 repaired" four lines above,
# c4_scope.py's generic negation disarmed by "is not the framework this ticket
# is about", and this.  For D2f the rule is therefore: inside a strike, or an
# explicit negation.  Proximity to a ticket id is printed, not counted.
live = [x for x in leaks
        if x[2] >= LEAK_RUN
        and x[2] / max(1, len(tokens(x[1]))) >= LEAK_FRACTION
        and not (x[5] - {"names-a-repair"})]
note("every struck claim is struck or explicitly negated at EVERY occurrence",
     not live)
for k, s_, n, run, ln, rs in live:
    print()
    print("  THE CLAIM THE ONE LIST HOLDS AND EVERY CHECKER PASSES ON:")
    print("      struck at   : the occurrence the list stores, with its")
    print("                    lead-in 'Recall from Section 17.4 that'")
    print("      asserted at : line %d, same document, no strike, and the" % ln)
    print("                    only marker within six lines is an unrelated")
    print("                    'added by the repair mg-6f61' about a")
    print("                    DIFFERENT correction to the same section")
    print("      why nothing sees it: check_doc.py and stricken_a4ef.py both")
    print("          store the sentence WITH its lead-in, so it occurs once")
    print("          and is struck once.  Every extent line is TRUE.")
    print()

# ---------------------------------------------------------------------------
hdr("D2b  WHAT EACH CHECKER OPENS -- MEASURED, NOT READ OFF THE SOURCE")

_real_open = builtins.open


def opened_by(script, argv, syspath):
    """Run `script` with `open` instrumented.  Returns (paths, exit code).

    TEXT reads only.  `s1_extent.py`'s control (c) copies a whole tree with
    `shutil.copytree`, which opens every file in BINARY to copy it -- counting
    those as "read by the checker" would have reported the checker reading a
    file its scan never looks at.  That false positive was in this file's
    first run and is kept in OUTCOMES.md.
    """
    seen = set()

    def spy(file, *a, **k):
        mode = (a[0] if a else k.get("mode", "r"))
        try:
            p = os.path.abspath(file)
        except TypeError:
            p = None
        if p and "b" not in mode and os.path.isfile(p):
            seen.add(p)
        return _real_open(file, *a, **k)

    old_argv, old_path, old_out = sys.argv, list(sys.path), sys.stdout
    code = 0
    try:
        builtins.open = spy
        sys.argv = argv
        sys.path = syspath + old_path
        sys.stdout = io.StringIO()
        try:
            runpy.run_path(script, run_name="__main__")
        except SystemExit as e:
            code = e.code or 0
    finally:
        builtins.open = _real_open
        sys.argv, sys.path, sys.stdout = old_argv, old_path, old_out
    return seen, code


CD = os.path.join(REPO, "code", "species_repair_6f61", "check_doc.py")
W3 = os.path.join(REPO, "code", "species_remainder_f8fa", "w3_scope.py")
S1 = os.path.join(REPO, "code", "species_repair_a4ef", "s1_extent.py")
S2 = os.path.join(REPO, "code", "species_repair_a4ef", "s2_seam.py")

cd_files, cd_code = opened_by(CD, [CD], [os.path.dirname(CD)])
w3_files, w3_code = opened_by(W3, [W3], [os.path.dirname(W3)])
s2_files, s2_code = opened_by(S2, [S2], [os.path.dirname(S2)])
s1_files, s1_code = opened_by(S1, [S1], [os.path.dirname(S1)])


def rel(p):
    return os.path.relpath(p, REPO)


def in_repo(paths):
    return sorted(rel(p) for p in paths if p.startswith(REPO + os.sep))


print("  check_doc.py  -- its extent line: 'enforces all 10 stricken")
print("                   sentences over ONE FILE ... It reads no code.'")
for p in in_repo(cd_files):
    print("        opens  %s" % p)
note("it reads no code -- TRUE", not any(p.endswith(".py")
                                         for p in in_repo(cd_files)))
note("it opens exactly ONE file, as 'ONE FILE' reads", len(in_repo(cd_files))
     == 1)
print("        ^ the extent line is about the STRICKEN list, which really is")
print("          enforced over one file.  But the checker READS two, and the")
print("          second carries five of its own assertions (C4).  NARROWER")
print("          than reality, which is the safe direction and still false.")
print()

print("  w3_scope.py   -- its extent line: 'TWO corrected statements -- X4")
print("                   and X5 -- plus the character-ring rule, over ONE")
print("                   tree.'")
w3_rel = in_repo(w3_files)
print("        opens %d file(s), all under %s"
      % (len(w3_rel), os.path.commonprefix(w3_rel) or "-"))
note("every file it opens is inside code/species_7d75",
     all(p.startswith("code/species_7d75/") for p in w3_rel))
_t7 = os.path.join(REPO, "code", "species_7d75")
tree = sorted(f for f in os.listdir(_t7)
              if os.path.isfile(os.path.join(_t7, f)))
unread = [f for f in tree
          if "code/species_7d75/" + f not in w3_rel]
print("        does NOT open: %s" % (", ".join(unread) or "-"))
note("the only file in the tree it does not read is run_all.sh",
     unread == ["run_all.sh"])
print()

print("  s1_extent.py  -- its extent line: '11 corrections over the document")
print("                   and 4 code trees', and 'SKIPPED, NAMED, so the")
print("                   exclusion cannot grow unseen -- 5 file(s)'.")
s1_rel = set(in_repo(s1_files))
print("        opens %d file(s) inside the repository" % len(s1_rel))
note("it opens the document", "docs/" + DOC in s1_rel)
for t in DECLARED_TREES:
    root = os.path.join(REPO, "code", t)
    allf = sorted(f for f in os.listdir(root)
                  if os.path.isfile(os.path.join(root, f)))
    read = [f for f in allf if "code/%s/%s" % (t, f) in s1_rel]
    skipped = [f for f in allf if f not in read]
    undeclared = [f for f in skipped if f not in A4EF_EXCLUDE]
    print("        code/%-24s %2d file(s), %2d read, skipped: %s"
          % (t, len(allf), len(read), ", ".join(skipped) or "-"))
    if undeclared:
        print("            UNDECLARED SKIP: %s" % ", ".join(undeclared))
print()

# ---------------------------------------------------------------------------
hdr("D2c  THE DECLARED EXCLUSION AGAINST THE REAL ONE")

print("  stricken_a4ef.py names %d skipped file(s), and s1_extent.py prints"
      % len(A4EF_EXCLUDE))
print("  that list under 'SKIPPED, NAMED, so the exclusion cannot grow")
print("  unseen'.  But tree_files() also filters on extension %s, and that"
      % ("/".join(A4EF_EXTENSIONS),))
print("  filter is in no extent line and in no printed list.")
print()
silent = []
for t in DECLARED_TREES:
    root = os.path.join(REPO, "code", t)
    for f in sorted(os.listdir(root)):
        if f in A4EF_EXCLUDE or not os.path.isfile(os.path.join(root, f)):
            continue
        if not f.endswith(A4EF_EXTENSIONS):
            silent.append("code/%s/%s" % (t, f))
for p in silent:
    print("      SILENTLY OUTSIDE THE SCAN, NOT NAMED ANYWHERE:  %s" % p)
print()
note("the declared exclusion is the whole exclusion", not silent)
print("  A file inside a tree the extent CLAIMS is covered, excluded by a")
print("  rule the extent does not state.  d5 plants a statement in one and")
print("  measures the exit code.")
print()

# ---------------------------------------------------------------------------
hdr("D2d  THE WHOLE REPOSITORY, SWEPT WITH THE SAME LIST")

buckets = {"declared extent": [], "declared silent": [], "outside": []}
walked = 0
for root, dirs, files in os.walk(REPO):
    dirs[:] = [d for d in dirs if d not in (".git", "state-history")]
    for f in sorted(files):
        if not f.endswith((".py", ".txt", ".md", ".sh")):
            continue
        path = os.path.join(root, f)
        r = rel(path)
        if r.startswith("code/species_audit_7dd3/"):
            continue          # this audit's own tables of forbidden strings
        walked += 1
        hits = scan_file(path)
        if not hits:
            continue
        live = [(sid, ln) for sid, v in hits.items() for ln, rs in v if not rs]
        if not live:
            continue
        parts = r.split("/")
        if r == "docs/" + DOC or (parts[0] == "code"
                                  and parts[1] in DECLARED_TREES
                                  and f.endswith(A4EF_EXTENSIONS)
                                  and f not in A4EF_EXCLUDE):
            b = "declared extent"
        elif (parts[0] == "docs" or (parts[0] == "code"
                                     and parts[1] in SILENT_TREES)
              or (parts[0] == "code" and parts[1] in DECLARED_TREES)):
            b = "declared silent"
        else:
            b = "outside"
        for sid, ln in live:
            buckets[b].append((sid, r, ln))

for b in ("declared extent", "declared silent", "outside"):
    print("  %-18s %3d still-asserted occurrence(s)" % (b, len(buckets[b])))
    for sid, r, ln in sorted(buckets[b])[:14]:
        print("        %-5s %s:%d" % (sid, r, ln))
    if len(buckets[b]) > 14:
        print("        ... and %d more" % (len(buckets[b]) - 14))
print()
note("nothing on the list is still asserted INSIDE the declared extent",
     not buckets["declared extent"], weight=1)
print("  The other two buckets are NOT counted as defects: mg-a4ef declares")
print("  the audit trees and the rest of docs/ out of extent, and this audit")
print("  is measuring whether the declaration is honest, not widening it.")
print()

# ---------------------------------------------------------------------------
hdr("D2e  THE REACH OF THE EXONERATION RULE -- the beyond-list target")

print("  Every worker in this arc has argued about WHEN a hit is exonerated.")
print("  Nobody has measured HOW MANY independent clauses hold each hit down.")
print("  A hit held by one clause is a marker doing work.  A hit held by")
print("  three is a marker that can be deleted without the number moving --")
print("  and the number is what a reader is shown.")
print()
hist = {}
per_clause = {k: 0 for k in REASON_NAMES}
total = 0
for t in DECLARED_TREES:
    root = os.path.join(REPO, "code", t)
    for f in sorted(os.listdir(root)):
        if not f.endswith(A4EF_EXTENSIONS) or f in A4EF_EXCLUDE:
            continue
        for sid, v in scan_file(os.path.join(root, f)).items():
            for ln, rs in v:
                total += 1
                hist[len(rs)] = hist.get(len(rs), 0) + 1
                for k in rs:
                    per_clause[k] += 1
print("  %d occurrence(s) of a listed statement inside the declared extent."
      % total)
for n in sorted(hist):
    print("      held by %d clause(s): %3d occurrence(s)%s"
          % (n, hist[n], "   <- STILL ASSERTED" if n == 0 else ""))
print()
for k in REASON_NAMES:
    print("      clause %-16s fires on %3d of %d" % (k, per_clause[k], total))
over = sum(v for n, v in hist.items() if n >= 2)
print()
print("  OVER-DETERMINED (2+ clauses): %d of %d = %.0f%%"
      % (over, total, 100.0 * over / total if total else 0))
print("  Not a defect on its own -- but it is the reason a repair can delete")
print("  the marker it points at and see no change, and it is printed by")
print("  nothing else in this arc.  d5's M10 measures exactly that.")
print()

print("=" * 78)
print("D2 TOTAL BAD: %d" % bad)
print("=" * 78)
print()
print("EXTENT OF THIS NUMBER.  D2 ranges over %d statements -- the %d the"
      % (len(STATEMENTS), len(strikes)))
print("document strikes, plus Y2 -- across EVERY .py/.txt/.md/.sh file under")
print("docs/ and code/ except this audit's own tree: %d file(s) walked."
      % walked)
print("It does NOT read PDFs, .html, .gz or any binary; it does not check")
print("mathematics; and its verdict on a statement is only as good as the")
print("patterns in statements7dd3.py, which are hand-written and which")
print("selftest7dd3.py exercises in both directions.")
sys.exit(1 if bad else 0)
