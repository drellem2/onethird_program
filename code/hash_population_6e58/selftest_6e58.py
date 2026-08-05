"""selftest_6e58.py -- THE DELIVERABLE.

The brief:

    THE SELFTEST IS THE DELIVERABLE, not the tuple: mg-0ba7 asserted the
    equivalence on a constructed line so it holds of the RULES.  Whatever you
    ship must fail if someone later adds a fifth spelling and does not update
    it.

So every check here is on a line of Python CONSTRUCTED in this file and
parsed with `ast`.  Nothing below asks the repository anything: a check that
passes because of what happens to be in the tree today is a check that stops
holding when the tree moves, and this ticket exists because a population
moved underneath a constant.

Three groups:

  (a) THE POSITIVE CONTROL, which contains `%H` AND `%h` on separate
      constructed lines and must find BOTH.  The brief is explicit that a
      case-blind search would report success while reproducing the exact
      blindness under repair, so the control is built first and the
      case-blind comparison is run against it.

  (b) THE RULES, on constructed lines: the escape `%%`, the hex byte `%x68`,
      the `format:`/`tformat:` prefixes, `--oneline`, `--abbrev-commit`, and
      the equivalence that makes this ticket a defect rather than a count --
      `git log -1 --format=%h -- <path>` is `NEWEST`, which is A-1's defect.

  (c) THE CLOSURE, which is what makes this file fail on a FIFTH spelling.
      It is two-sided: what git documents must be handled, and what is
      handled must be documented or DECLARED.  A drill injects a fifth
      documented spelling into a constructed man page and requires the
      closure check to go red -- because a gate that has never been seen red
      is a gate whose red is unmeasured.

Exit 0 iff every assertion holds.
"""

import ast

import lib6e58 as L

PASS, FAIL = [], []


def ok(cond, msg):
    (PASS if cond else FAIL).append(msg)
    print("   %-4s %s" % ("ok" if cond else "FAIL", msg))


def rule(title):
    print()
    print("-- " + title)
    print()


def strs_of(line):
    """The direct string arguments of the FIRST call on a constructed line,
    through mg-330a's own `_strings_of` -- so that what is tested here is the
    format rule and not a second string extractor.
    """
    tree = ast.parse(line)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            return L.A330._strings_of(node)
    raise AssertionError("no call on the constructed line: %r" % line)


print("=" * 74)
print("selftest_6e58 -- THE RULES, ON CONSTRUCTED LINES")
print("=" * 74)

# ---------------------------------------------------------------------------
rule("(a) THE POSITIVE CONTROL -- BOTH CASES, SIDE BY SIDE")
# ---------------------------------------------------------------------------

CONTROL = {
    "upper": 'git("log", "-1", "--format=%H", "--", path)',
    "lower": 'git("log", "-1", "--format=%h", "--", path)',
}
print("   the two constructed lines:")
for k in ("upper", "lower"):
    print("      %-6s %s" % (k, CONTROL[k]))
print()

up = L.hash_emitters(strs_of(CONTROL["upper"]))
lo = L.hash_emitters(strs_of(CONTROL["lower"]))

ok(len(up) == 1 and up[0][1] == "FULL",
   "the `%H` line yields exactly one emitter, grain FULL")
ok(len(lo) == 1 and lo[0][1] == "ABBREV",
   "the `%h` line yields exactly one emitter, grain ABBREV")
ok(up[0][0] != lo[0][0],
   "the two lines are told apart -- the detector is not case-blind")

# The comparison the brief demands: a case-blind search on the SAME control.
def case_blind(strs):
    return any("%h" in s.lower() for s in strs)


ok(case_blind(strs_of(CONTROL["upper"])) and
   case_blind(strs_of(CONTROL["lower"])),
   "a CASE-BLIND search matches BOTH lines -- it would report `found them "
   "all` while being unable to say which is which")
ok(bool(up) and bool(lo),
   "this instrument matches both lines too, but by GRAIN and not by "
   "coincidence: FULL vs ABBREV above")

# And the direction that matters: mg-330a's tuple, on the same control.
a_up = L.is_revision_producing(strs_of(CONTROL["upper"]), L.POP_A)
a_lo = L.is_revision_producing(strs_of(CONTROL["lower"]), L.POP_A)
ok(a_up, "mg-330a's `_HASH_FORMATS` SEES the upper-case line")
ok(not a_lo, "mg-330a's `_HASH_FORMATS` DOES NOT SEE the lower-case line -- "
             "the defect, reproduced on a constructed line rather than "
             "recalled from a tree")

# ---------------------------------------------------------------------------
rule("(b) THE EQUIVALENCE THAT MAKES IT A DEFECT AND NOT A COUNT")
# ---------------------------------------------------------------------------

k_up = L.classify_call(strs_of(CONTROL["upper"]), L.POP_C)
k_lo = L.classify_call(strs_of(CONTROL["lower"]), L.POP_C)
ok(k_up == "NEWEST", "`git log -1 --format=%H -- <path>` is NEWEST")
ok(k_lo == "NEWEST", "`git log -1 --format=%h -- <path>` is NEWEST TOO -- "
                     "A-1's defect spelled with a lower-case letter")
ok(k_up == k_lo, "the two spellings classify IDENTICALLY, so the difference "
                 "between them is the DENOMINATOR and nothing else")
ok(L.classify_call(strs_of(CONTROL["lower"]), L.POP_A) is None,
   "and under mg-330a's population the same line classifies as nothing at "
   "all -- it is not counted as safe, it is not counted")

# ---------------------------------------------------------------------------
rule("(c) THE FORMAT-STRING RULES, EACH ON ITS OWN CONSTRUCTED LINE")
# ---------------------------------------------------------------------------

CASES = [
    ('git("log", "--format=%H %s")', "FULL", 1,
     "a COMPOSITE full-hash format -- `%H` with a subject stapled to it"),
    ('git("log", "--format=%H\\t%s")', "FULL", 1,
     "the same with a tab separator"),
    ('git("log", "--format=%H%x1f%s")', "FULL", 1,
     "the same with a hex byte separator"),
    ('git("log", "--format=%h %ad %s")', "ABBREV", 1,
     "a composite ABBREV format"),
    ('git("log", "--format=format:%H")', "FULL", 1,
     "the `format:` prefix, which IS in mg-330a's tuple"),
    ('git("log", "--pretty=tformat:%h")', "ABBREV", 1,
     "the `tformat:` prefix, which is in nobody's tuple"),
    ('git("log", "--pretty=%H")', "FULL", 1, "`--pretty=` as well as "
     "`--format=`"),
    ('git("log", "--oneline")', "ABBREV", 1,
     "`--oneline`, documented as `--pretty=oneline --abbrev-commit`"),
    ('git("log", "--pretty=oneline")', "FULL", 1,
     "`--pretty=oneline` WITHOUT `--abbrev-commit` prints the full hash"),
    ('git("log", "--pretty=oneline", "--abbrev-commit")', "ABBREV", 1,
     "and `--abbrev-commit` demotes it, in the SAME call"),
    ('git("log", "--pretty=reference")', "ABBREV", 1,
     "`--pretty=reference`, documented as `<abbrev-hash> (<title>, <date>)`"),
    ('git("log", "--format=%%h")', None, 0,
     "`%%h` is a LITERAL PERCENT followed by `h` -- git's own escape rule, "
     "and NOT an abbreviated hash"),
    ('git("log", "--format=%x68")', None, 0,
     "`%x68` is the hex byte for `h`, not a placeholder"),
    ('git("log", "--format=%T")', None, 0,
     "`%T` is the TREE hash -- a hash, and not a commit"),
    ('git("log", "--format=%p")', None, 0,
     "`%p` is the abbreviated PARENT hashes -- excluded for the same reason"),
    ('git("log", "--format=%s")', None, 0,
     "a subject-only format produces no revision at all"),
    ('git("show", "--format=%H")', None, 0,
     "`git show` is not `git log`; the subcommand half of the rule is "
     "mg-330a's and is unchanged here"),
]
for line, grain, n, what in CASES:
    ems = L.hash_emitters(strs_of(line)) if "\"log\"" in line else []
    if "\"log\"" not in line:
        got_n, got_grain = 0, None
        producing = L.is_revision_producing(strs_of(line), L.POP_C)
        ok(not producing, what)
        continue
    got_n = len(ems)
    got_grain = ems[0][1] if ems else None
    ok(got_n == n and got_grain == grain,
       "%s  [%s x%d]" % (what, got_grain, got_n))

# ---------------------------------------------------------------------------
rule("(d) THE POPULATIONS ARE NESTED, ON CONSTRUCTED LINES")
# ---------------------------------------------------------------------------

NEST = [
    ('git("log", "--format=%H", "--", p)', [1, 1, 1, 1], "%H: in all four"),
    ('git("log", "--format=%h", "--", p)', [0, 1, 1, 1],
     "%h: hidden from POP-A only"),
    ('git("log", "--format=%H %s", "--", p)', [0, 0, 1, 1],
     "a COMPOSITE %H: hidden from POP-A AND from the one-line `+%h` repair"),
    ('git("log", "--oneline", "--", p)', [0, 0, 1, 1],
     "--oneline: the same"),
    ('git("log", "--", p)', [0, 0, 0, 1],
     "no format at all: only POP-D, whose increment p2 adjudicates to zero"),
]
for line, want, what in NEST:
    got = [1 if L.is_revision_producing(strs_of(line), p) else 0
           for p in L.POPULATIONS]
    ok(got == want, "%s  %s" % (what, got))
    ok(got == sorted(got), "and the four populations are NESTED for it")

# ---------------------------------------------------------------------------
rule("(e) MY CLASSIFIER IS mg-330a's, ON CONSTRUCTED LINES")
# ---------------------------------------------------------------------------

SAME = [
    'git("log", "-1", "--format=%H", "--", p)',
    'git("log", "--format=%H", "--", p)',
    'git("log", "--format=%H", "--reverse", "--", p)',
    'git("log", "-S", "marker", "--format=%H", "--", p)',
    'git("log", "-G", "regex", "--format=%H", "--", p)',
    'git("log", "--format=%H", "a..b")',
    'git("log", "--format=%H")',
    'git("log", "-1", "--format=%H")',
]
for line in SAME:
    s = strs_of(line)
    ok(L.classify_call(s, L.POP_A) == L.A330.classify_call(s),
       "same kind as mg-330a for: %s" % line)

# ---------------------------------------------------------------------------
rule("(f) THE CLOSURE -- WHAT MAKES THIS FILE FAIL ON A FIFTH SPELLING")
# ---------------------------------------------------------------------------

text = L.man_text()
doc_ph = L.documented_commit_hash_placeholders(text)
doc_fmt = L.documented_builtin_formats(text)

ok(set(doc_ph) == set(L.HASH_PLACEHOLDERS),
   "every commit-hash placeholder git DOCUMENTS is handled, and no more: "
   "documented %s, handled %s"
   % (sorted(doc_ph), sorted(L.HASH_PLACEHOLDERS)))
ok(all(doc_ph[p] == L.HASH_PLACEHOLDERS[p] for p in doc_ph),
   "and each is handled at the GRAIN git documents for it")
ok(set(doc_fmt) <= set(L.BUILTIN_FORMATS),
   "every built-in format git documents as printing a commit identifier is "
   "handled")
ok(set(L.BUILTIN_FORMATS) - set(doc_fmt) == set(L.EXTRACTOR_BLIND),
   "and every handled format the extractor cannot find is DECLARED in "
   "EXTRACTOR_BLIND with the sentence that exempts it: %s"
   % sorted(L.EXTRACTOR_BLIND))

print()
print("   THE DRILL.  A fifth spelling, injected into a CONSTRUCTED man page")
print("   rather than into git, and the closure check required to go red:")
print()

FIFTH = """
           •   Placeholders that expand to information extracted from the
               commit:

               %H
                   commit hash

               %h
                   abbreviated commit hash

               %Q
                   commit hash in some future spelling

               %T
                   tree hash
"""
fifth_ph = L.documented_commit_hash_placeholders(FIFTH)
ok("%Q" in fifth_ph,
   "the constructed page's fifth spelling `%Q` IS read out of it -- the "
   "drill is a real input and not a stubbed answer")
ok(set(fifth_ph) != set(L.HASH_PLACEHOLDERS),
   "and the closure comparison GOES RED against it: documented %s vs "
   "handled %s.  If git ever documents a third commit-hash placeholder, "
   "this file fails until someone handles it."
   % (sorted(fifth_ph), sorted(L.HASH_PLACEHOLDERS)))

FIFTH_FMT = """
       •   futureline

           <hash> <title-line>

           A format that does not exist yet.
"""
fifth_fmt = L.documented_builtin_formats(FIFTH_FMT)
ok("futureline" in fifth_fmt,
   "a fifth built-in FORMAT is read out of a constructed page too")
ok(not (set(fifth_fmt) <= set(L.BUILTIN_FORMATS)),
   "and the format-side closure goes red against it as well")

print()
print("   THE OTHER SIDE OF THE CLOSURE.  The drill above catches a spelling")
print("   git documents.  This catches one that appears IN THE TREE: every")
print("   placeholder used in any `git log` format anywhere under `code/`")
print("   must be one `man git-log` documents.  A format nobody has")
print("   documented is a format nobody has classified.")
print()

calls, _unp = L.all_calls()
# `placeholders_in` tokenises at the grain of ONE character after `%`,
# because a commit hash is `%H` or `%h` and never longer.  git documents
# placeholders at a COARSER grain (`%ad`, `%an`), so the comparison is made
# at the finer of the two: the set of first characters.  Comparing the two
# grains directly is what turned this check red on `%a` and `%c` the first
# time it ran -- see out_selftest_6e58_FIRSTFORM_exit1.txt.  The check still
# catches a genuinely new spelling: a `%Q` nobody documents has no
# documented placeholder beginning with `Q`.
known = {p[:2] for p, _d in L.documented_placeholders(text)}
unknown = {}
for c in calls:
    if not any(s == "log" or s.endswith("log") for s in c["strs"]):
        continue
    for s in c["strs"]:
        for flag in L.FORMAT_FLAGS:
            if not s.startswith(flag):
                continue
            val = s[len(flag):]
            for pre in L.FORMAT_PREFIXES:
                if val.startswith(pre):
                    val = val[len(pre):]
            if val in L.BUILTIN_FORMATS:
                continue
            for ph in L.placeholders_in(val):
                if ph not in known:
                    unknown.setdefault(ph, []).append(L.site_key(c))
ok(not unknown,
   "every placeholder used in a `git log` format in this tree is documented "
   "on `man git-log`: %s" % (sorted(unknown) or "none undocumented"))

# ---------------------------------------------------------------------------
print()
print("=" * 74)
print("PASS: %d   FAIL: %d" % (len(PASS), len(FAIL)))
for f in FAIL:
    print("   FAIL: %s" % f)
print("TOTAL BAD: %d" % len(FAIL))
raise SystemExit(1 if FAIL else 0)
