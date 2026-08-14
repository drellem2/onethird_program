#!/usr/bin/env python3
"""EMPTY IS NOT ZERO -- CAN THE ESTATE'S OWN RULE BE ENFORCED BY LOOKING?

`mg-9b6b` closed a route from the logic side and then measured why it keeps
reading as OPEN from the instrument side: `G(s) = max{d : delta <= s}` is EMPTY
in all 15 cells below 1/3, and *nothing at all* is what a ceiling looks like
from inside a tool that reports it as `0`.  Its carry-forward, which `mg-3c92`
inherits, proposes a rule for the WHOLE estate:

    any arm that can return "no answer" and "the answer is zero" must print
    them differently.

THIS FILE IS THE INSTRUMENT THAT ASKS WHETHER THAT RULE CAN BE A RULE.  A
proposal about every arm in an estate is worth what its enforcement is worth,
and enforcement has exactly two shapes: a MATCHER over source, or a DISCIPLINE
a human follows.  The difference is decidable and this file decides it.

    WHAT IT IS.  A NET, pinned at `AS_OF`, over every tracked `.py` file under
    `code/` -- parsed with `ast` and NOT grepped, because the shapes that matter
    are `IfExp` nodes and a regex cannot tell `1 if i == j else 0` (an indicator,
    and the single most common `else 0` in this corpus) from `max(xs) if xs
    else 0` (the defect).  Reading a producer means parsing the producer.

    THE CLASSES ARE THREE AND THE THIRD IS THE POINT.

    GUARDED_COLLAPSE -- `f(X) if X else <number>`, where the guard is a BARE
    truthiness test and at least one name in the guard is also named in the
    true branch.  This is the detectable family: the author saw the empty case,
    handled it, and chose a number for it.  Whether the choice LOSES anything
    is decided in `z1` -- computed from the operation where that is possible,
    and by a hand table with a reason per site where it is not.

    AGGREGATE_DEFAULT -- `max(xs, default=0)`, `min(...)`, `next(it, 0)`.  The
    one spelling a linter would reach for first.

    UNGUARDED_SUM -- `sum(<comprehension with an `if`>)`.  THE FAMILY NO
    MATCHER CAN JUDGE, and the reason the rule cannot be a lint.  `sum([]) == 0`
    is the LANGUAGE's collapse, not the author's: there is no fallback in the
    source, no guard to find, and the printed `0` is byte-identical whether the
    selection was empty or genuinely summed to nothing.  A site here is not a
    defect and is not evidence of one.  It is evidence about DETECTABILITY, and
    that is what it is counted for.

    THE GUARD-IS-NAMED-IN-THE-BODY REQUIREMENT IS LOAD-BEARING AND IS MEASURED
    RATHER THAN ASSERTED.  Without it every `sys.exit(1 if bad else 0)` in the
    estate (there are 177) and every matrix indicator joins the class.  `z1`
    runs the classifier BOTH WAYS over the whole corpus and prints both numbers,
    because a requirement whose removal changes nothing is decoration and a
    census resting on it would be measuring something coarser than it claims.

    ONE-DIRECTIONAL, LIKE EVERY RULE OF THIS SHAPE IN THIS ESTATE.  A site in
    GUARDED_COLLAPSE is a PROOF that the author chose a number for the empty
    case.  ABSENCE OF A SITE PROVES NOTHING: the collapse may be in a helper,
    in a `%d` format of a `None`-free default, in `dict.get(k, 0)`, or in
    `sum([])` where there is nothing to see at all.  The false-NEGATIVE
    direction is unbounded and is stated everywhere the figures are.

    EVERY FIGURE IS A FUNCTION OF ONE COMMIT.  Sources are read with `git show
    AS_OF:path`, never off the worktree, so this transcript has a fixed point
    (mg-ede8's arrangement, and pathlist.py's in this estate).  The ONE
    exception is `z1` section 8, the reflexive self-scan, which MUST read the
    worktree because this directory is younger than the pin -- an exemption by
    ARITHMETIC and not by rule, and it is declared at the section rather than
    left to be found.
"""

import ast
import os
import re
import subprocess
import warnings

# PARSING A CORPUS FILE CAN WARN, AND THE WARNING IS ABOUT THE SUBJECT RATHER
# THAN ABOUT THIS ARM.  At least one tracked producer contains a `"\|"` escape,
# and `ast.parse` emits `SyntaxWarning: invalid escape sequence` for it with the
# filename `<unknown>` -- which lands on stderr, which `run_all.sh` folds into
# the transcript.  Suppressed HERE, at the parse, rather than at the arm: a
# blanket filter at the top of an arm would also swallow a warning raised by
# this directory's own code, and the difference between "the corpus warned" and
# "I warned" is the whole reason the filter is narrow.
warnings.filterwarnings("ignore", category=SyntaxWarning)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))

# The commit every pinned figure on these pages is a function of.  Checked at
# run time to resolve AND to be an ancestor of origin/main, because a pin that
# has fallen out of history is a figure about nothing.  It was the tip of
# origin/main when this directory opened; it is not the tip when it lands, and
# that gap is the arrangement rather than a defect in it.
AS_OF = "179da0a"

# The estate's own demonstrated instance, named here so the controls in `z0`
# read it out of the tree rather than re-spelling it (mg-d2c2).
WITNESS_PATH = "code/lever_shape_9b6b/e2_frontier.py"
WITNESS_MARK = 'mx if mx is not None else "EMPTY"'

GUARDED = "GUARDED_COLLAPSE"
DEFAULTED = "AGGREGATE_DEFAULT"
UNGUARDED = "UNGUARDED_SUM"

# THE TWO SPELLINGS THAT ALREADY DO WHAT THE CARRY-FORWARD ASKS, counted for
# the same reason a wrong-direction control exists: a census that can only find
# the defect reports a number nobody can put in proportion, and `n sites are
# wrong` means something different when the compliant population is 0 than when
# it is comparable.  Both keep EMPTY reachable by the caller -- `None` and a
# string are not numbers and cannot be mistaken for an answer.
#
# PRESERVING IS DRAWN FROM EXACTLY THE SAME SYNTACTIC FAMILY AS GUARDED -- bare
# guard, guard named in the true branch -- and that is what makes the ratio
# between them a ratio.  A wider preserving class would put the two counts over
# different populations and the percentage would be arithmetic rather than a
# measurement.  It costs something and the cost is declared: a line whose guard
# is a COMPARISON is in NEITHER class, however carefully it keeps EMPTY apart,
# and mg-9b6b's own shipped `mx if mx is not None else "EMPTY"` is exactly such
# a line.  z0 D2 measures that and says so.
PRESERVING = "GUARDED_PRESERVING"      # `f(X) if X else None` / else "EMPTY"
DEFAULTED_NONE = "AGGREGATE_DEFAULT_NONE"   # `max(xs, default=None)`

# Aggregates that take a `default=` or a positional fallback.  `next` is here
# because `next(it, 0)` is the same statement in a different spelling.
DEFAULTING = {"max", "min", "next"}

_SRC = {}


def git(*args):
    got = subprocess.run(["git", "-C", ROOT, *args], capture_output=True)
    if got.returncode != 0:
        raise SystemExit("lib3c92: git %s failed: %s"
                         % (" ".join(args),
                            got.stderr.decode("utf-8", "replace").strip()))
    return got.stdout.decode("utf-8", "surrogateescape")


def check_pin(rev=AS_OF):
    """Resolve the pin and prove it is an ancestor of origin/main.

    A pin that does not resolve is a page about nothing; a pin that resolves
    but is unreachable is a page about a branch nobody else can see.  Both
    return figures that LOOK fine, which is why this is a refusal and not a
    warning.
    """
    full = git("rev-parse", rev).strip()
    got = subprocess.run(
        ["git", "-C", ROOT, "merge-base", "--is-ancestor", full, "origin/main"],
        capture_output=True)
    return full, got.returncode == 0


def source_at(rev, path):
    key = (rev, path)
    if key not in _SRC:
        _SRC[key] = git("show", "%s:%s" % (rev, path))
    return _SRC[key]


def tracked_py(rev=AS_OF):
    """Every tracked `.py` under `code/` at `rev`, sorted.

    Sorted rather than merely enumerated: every walk in this file is over this
    list, and a table whose row order came out of a set is a page published as
    a function of PYTHONHASHSEED (mg-bdc0's pathlist.py, on its own first run).
    """
    out = git("ls-tree", "-r", "--name-only", rev)
    return sorted(p for p in out.splitlines()
                  if p.startswith("code/") and p.endswith(".py"))


# --------------------------------------------------------------------------
# the classifier
# --------------------------------------------------------------------------

def _names(node):
    """Every bare identifier appearing anywhere under `node`."""
    return {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}


def _is_numeric_zero(node):
    """`0`, `0.0`, `Fraction(0)`, `Fraction(0, k)`.

    `Fraction` is in here because this corpus does exact rationals on every
    verdict path, so the literal zero an author writes is very often a call.
    A matcher that only knew `0` would report a small class for a reason that
    is about Python and not about the estate.
    """
    if isinstance(node, ast.Constant):
        return isinstance(node.value, (int, float)) \
            and not isinstance(node.value, bool) and node.value == 0
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
            and node.func.id == "Fraction" and node.args:
        return _is_numeric_zero(node.args[0])
    return False


def _is_preserving(node):
    """`None`, or a string.  Neither can be read as a computed answer."""
    return isinstance(node, ast.Constant) \
        and (node.value is None or isinstance(node.value, str))


def _is_numeric(node):
    if isinstance(node, ast.Constant):
        return isinstance(node.value, (int, float)) \
            and not isinstance(node.value, bool)
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
            and node.func.id == "Fraction":
        return True
    return False


def _bare_guard(test):
    """Is `test` a BARE truthiness test rather than a decision?

    `xs` / `t["mu"]` / `self.rows` / `len(xs)` are truthiness tests on a thing
    that can be empty.  `i == j`, `a and b`, `not xs`, `x in y` are decisions,
    and the fallback branch of a decision is an ANSWER rather than an absence.
    Excluding them is what separates this census from `git grep 'else 0'`,
    whose top two shapes in this corpus are both decisions.
    """
    return isinstance(test, (ast.Name, ast.Attribute, ast.Subscript, ast.Call))


class Site(object):
    def __init__(self, kind, path, line, col, text, loose_only=False,
                 op=None, printed=False, zero=False, fallback=None):
        self.kind = kind
        self.path = path
        self.line = line
        self.col = col
        self.text = text
        self.loose_only = loose_only
        self.op = op
        self.verdict = VERDICT_OF_OP.get(op) if op else None
        self.printed = printed
        self.zero = zero
        self.fallback = fallback   # "num" | "None" | "str" -- what was chosen

    @property
    def key(self):
        return "%s:%d" % (self.path, self.line)

    def __repr__(self):
        return "<%s %s>" % (self.kind, self.key)


def _line_of(src_lines, lineno):
    if 1 <= lineno <= len(src_lines):
        return src_lines[lineno - 1].strip()
    return "<line %d out of range>" % lineno



# --------------------------------------------------------------------------
# what happens to the collapsed value
# --------------------------------------------------------------------------

# The three ways a value reaches a page in this estate.  `print(...)`, a `%`
# against a format string, and an f-string.  `.format(` is in the call form.
def _printing_parents(tree):
    """Map id(node) -> True for every node that renders text.

    Syntactic containment ONLY, and that is a declared UNDER-count rather than
    a limitation nobody mentioned: a site assigned to a name on one line and
    printed forty lines later is invisible here.  The direction is safe for the
    claim being made -- PRINTED is a PROOF that the collapsed value reaches a
    page, and NOT-PRINTED proves nothing at all.
    """
    printing = set()
    for node in ast.walk(tree):
        rendering = False
        if isinstance(node, ast.Call):
            fn = node.func
            if isinstance(fn, ast.Name) and fn.id in ("print", "format"):
                rendering = True
            elif isinstance(fn, ast.Attribute) and fn.attr in ("format", "write"):
                rendering = True
        elif isinstance(node, ast.JoinedStr):
            rendering = True
        elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod):
            if isinstance(node.left, ast.Constant) \
                    and isinstance(node.left.value, str):
                rendering = True
            elif isinstance(node.left, ast.JoinedStr):
                rendering = True
        if rendering:
            for kid in ast.walk(node):
                printing.add(id(kid))
    return printing


# THE OPERATION THE TRUE BRANCH PERFORMS ON THE THING THE GUARD TESTS.  This is
# read off the AST and never assigned by hand, because the verdict below is a
# function of it and a hand-assigned input to a computed verdict is a hand
# verdict wearing a rule's clothes.
DIV = "DIV"        # a ratio whose divisor is the guard
MAXMIN = "MAXMIN"  # max / min / sorted over the thing being guarded
SUM = "SUM"        # a sum over it
LEN = "LEN"        # a count of it
OP_OTHER = "OTHER"  # anything else -- goes to the hand table and nowhere else

# THE VERDICT, AND THE QUESTION IT ANSWERS IS NARROW ON PURPOSE:
#
#   is the fallback the operation's OWN VALUE on the empty input, or is it a
#   CHOICE the author made because the operation has no value there?
#
# `sum(∅) = 0` and `len(∅) = 0` are DEFINITIONS: nothing is lost, the printed
# `0` inverts, and a reader can recover the empty case from it.  `max(∅)`,
# `min(∅)` and `x/0` HAVE NO VALUE: whatever is printed for them is a choice,
# the printed number does not invert, and EMPTY has become 0.
#
# ⚠️  COLLAPSE IS NOT AN ACCUSATION AND THIS FILE NEVER USES IT AS ONE.  It says
# the printed value cannot be inverted by a reader.  Whether that matters is a
# question about the reader, and `mg-9b6b` is the one case in this estate where
# the answer is known to be yes.
SOUND = "SOUND"
COLLAPSE = "COLLAPSE"
UNDECIDED = "UNDECIDED"

VERDICT_OF_OP = {DIV: COLLAPSE, MAXMIN: COLLAPSE, SUM: SOUND, LEN: SOUND,
                 OP_OTHER: UNDECIDED}


def _op(node):
    """Which operation the true branch applies to the guarded thing."""
    guard_names = _names(node.test)
    for sub in ast.walk(node.body):
        if isinstance(sub, ast.BinOp) and isinstance(sub.op, (ast.Div,
                                                              ast.FloorDiv)):
            if _names(sub.right) & guard_names:
                return DIV
    for sub in ast.walk(node.body):
        if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name):
            fn = sub.func.id
            if fn in ("max", "min", "sorted") and (_names(sub) & guard_names
                                                   or sub is node.body):
                return MAXMIN
            if fn == "sum" and (_names(sub) & guard_names or sub is node.body):
                return SUM
    outer = node.body
    if isinstance(outer, ast.Call) and isinstance(outer.func, ast.Name) \
            and outer.func.id == "len":
        return LEN
    return OP_OTHER


def classify(path, src, strict=True):
    """Every site in one file.

    `strict=False` drops the guard-is-named-in-the-body requirement and is the
    WRONG-DIRECTION control: it is what this census would be if that
    requirement were decoration.  It is not a second opinion and its number is
    never reported as a finding.
    """
    try:
        tree = ast.parse(src)
    except SyntaxError as exc:
        return [], "SYNTAX ERROR line %s" % exc.lineno
    lines = src.splitlines()
    printing = _printing_parents(tree)
    sites = []

    for node in ast.walk(tree):
        if isinstance(node, ast.IfExp):
            if not _bare_guard(node.test):
                continue
            referenced = bool(_names(node.test) & _names(node.body))
            if _is_preserving(node.orelse):
                if referenced:
                    sites.append(Site(
                        PRESERVING, path, node.lineno, node.col_offset,
                        _line_of(lines, node.lineno),
                        fallback=("None" if node.orelse.value is None
                                  else "str")))
                continue
            if not _is_numeric(node.orelse):
                continue
            if strict and not referenced:
                continue
            sites.append(Site(GUARDED, path, node.lineno, node.col_offset,
                              _line_of(lines, node.lineno),
                              loose_only=not referenced,
                              op=_op(node), fallback="num",
                              printed=id(node) in printing,
                              zero=_is_numeric_zero(node.orelse)))

        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            fn = node.func.id
            if fn in DEFAULTING:
                fallback = None
                for kw in node.keywords:
                    if kw.arg == "default":
                        fallback = kw.value
                if fn == "next" and len(node.args) == 2:
                    fallback = node.args[1]
                if fallback is not None and _is_preserving(fallback):
                    sites.append(Site(
                        DEFAULTED_NONE, path, node.lineno, node.col_offset,
                        _line_of(lines, node.lineno),
                        fallback=("None" if fallback.value is None
                                  else "str")))
                elif fallback is not None and _is_numeric(fallback):
                    sites.append(Site(DEFAULTED, path, node.lineno,
                                      node.col_offset,
                                      _line_of(lines, node.lineno),
                                      printed=id(node) in printing,
                                      zero=_is_numeric_zero(fallback)))
            elif fn == "sum" and len(node.args) == 1:
                arg = node.args[0]
                if isinstance(arg, (ast.GeneratorExp, ast.ListComp,
                                    ast.SetComp)) \
                        and any(g.ifs for g in arg.generators):
                    sites.append(Site(UNGUARDED, path, node.lineno,
                                      node.col_offset,
                                      _line_of(lines, node.lineno),
                                      printed=id(node) in printing))
    sites.sort(key=lambda s: (s.line, s.col, s.kind))
    return sites, None


def census(rev=AS_OF, strict=True, paths=None):
    """Every site in the pinned corpus, plus the files that would not parse.

    Unparseable files are COUNTED and named rather than dropped: a census that
    reports a number because it never looked is this estate's oldest defect
    (`git_grep_l`), and a scan that silently skipped a tenth of the corpus
    would report a small class for a reason that has nothing to do with the
    corpus.
    """
    paths = tracked_py(rev) if paths is None else paths
    sites, broken = [], []
    for path in paths:
        got, err = classify(path, source_at(rev, path), strict=strict)
        if err:
            broken.append((path, err))
        sites.extend(got)
    return sites, broken, paths


def by_kind(sites):
    out = {GUARDED: [], DEFAULTED: [], UNGUARDED: [], PRESERVING: [],
           DEFAULTED_NONE: []}
    for s in sites:
        out[s.kind].append(s)
    return out


def is_zero_fallback(site, rev=AS_OF, src=None):
    """Does this GUARDED site collapse to ZERO specifically?

    Reported separately from `is a number`, because the carry-forward's claim
    is about `0` in particular -- a fallback of `-1` or `900` is a sentinel a
    reader can SEE, and a fallback of `0` is one they cannot.
    """
    if site.kind != GUARDED:
        return False
    text = source_at(rev, site.path) if src is None else src
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.IfExp) and node.lineno == site.line \
                and node.col_offset == site.col:
            return _is_numeric_zero(node.orelse)
    return False


# --------------------------------------------------------------------------
# transcript helpers
# --------------------------------------------------------------------------

def rule(title):
    print()
    print(title)
    print("-" * len(title))


def head(name, subtitle):
    print("=" * 78)
    print(name)
    print(subtitle)
    print("=" * 78)


def count_or_empty(n, looked):
    """The rule this whole directory is about, applied to its own printing.

    `0` means I LOOKED AND THERE WERE NONE.  `EMPTY` means THERE WAS NOTHING TO
    LOOK AT -- no population, no question, no answer.  They are different
    answers and this function is the only place either is spelled, so no arm
    here can print one for the other by accident.
    """
    return "EMPTY" if not looked else "%d" % n


ELLIPSIS = re.compile(r"\s+")


def squeeze(text, width=96):
    text = ELLIPSIS.sub(" ", text).strip()
    return text if len(text) <= width else text[:width - 1] + "…"
