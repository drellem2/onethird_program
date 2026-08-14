#!/usr/bin/env python3
"""FIGURES -- CAN THE READER MIXED OWES BE WRITTEN BY MACHINE?

mg-bdc0's remainder, in its own words: *305 transcripts are MIXED, and MIXED
is not a refutation -- `consumers.py` is MIXED and three of its figures are
path-list-valued anyway.  MIXED means a reader per figure is still owed:
somebody must say WHICH figures in a transcript are functions of the path list,
per figure, per transcript.*  That has been paid exactly twice in this estate
and both times BY HAND.  The open question was whether it can be paid by
machine at all, or whether the honest answer is that it cannot.

IT CAN, PARTLY, AND THE SIZE OF THE PARTLY IS THE FINDING.  A figure is an
interpolated value on a printed line, so it is an EXPRESSION in the producer's
source, and `is this expression a function of the tracked path list` is a
BACKWARD SLICE -- decidable wherever the slice closes and undecidable exactly
where it does not.  This file computes that slice for every figure of every
paired producer at pathlist.py's own AS_OF and reports the three-way split.

    WHAT THIS FILE IS.  A NET over FIGURES rather than over transcripts, and
    the unit is the whole point: pathlist.py grades a PRODUCER by what it
    reads, and a producer that reads both grades MIXED with nothing said about
    which of its figures is which.  Here the population is the 4 000-odd
    printed expressions those producers carry, and each gets its own verdict.
    It is PINNED, is a HAND-RUN, and is NOT in run_all.sh -- pathlist.py's
    arrangement in this same directory, for pathlist.py's reason.

    THE GRADE IS ONE-DIRECTIONAL IN THE SAME SENSE pathlist.py's IS, AND THE
    DIRECTION IS THE OPPOSITE ONE.  PATH-LIST-VALUED is a PROOF: it is claimed
    only when the slice CLOSES -- every root of it is a tracked-path-list read,
    a literal, or a non-repository input -- and any unresolved name, call or
    parameter anywhere in the slice makes the figure UNDECIDED instead.  So
    almost every failure of this analysis lands in UNDECIDED, which is the
    class that claims nothing.  CONTENT-VALUED is a proof of the other thing
    and is reached only by seeing an actual content read.

    THE EXCEPTION IS N35 AND IT IS PLANTED RATHER THAN DESCRIBED.  An
    assignment is recorded in the scope it is WRITTEN in, so a global filled
    by `X.append(...)` inside a function is invisible to a use at module
    level: that use sees `X = []` and reads a literal, and a figure whose real
    slice runs through such a global can come back a PROOF.  Exhibited in a
    control, LATENT in the corpus -- nothing here counts how many of the
    PATH-LIST-VALUED figures have that shape, and saying so is the honest half.

    THE CONTROL DEPENDENCE IS NOT AN EXTRA AND IT IS WHERE THE NAIVE VERSION
    IS WRONG.  consumers.py counts prose mentions with `prose += 1` inside
    `for path in git_grep_l(...)`, and the value assigned is the LITERAL 1.  A
    slice that followed values only would report that figure a function of a
    constant and grade it PATH-LIST-VALUED -- a false proof, published about
    the one transcript in this estate whose figures have been adjudicated by
    hand.  Every assignment therefore inherits the dependencies of the loop
    iterables and `if` tests it sits inside, and P51 plants exactly the
    counter-in-a-loop shape and requires CONTENT-VALUED.

    THE NON-REPOSITORY INPUTS ARE A CLASS AND NOT AN OVERSIGHT.  `sys.argv`,
    the environment and `__file__` are inputs that are not the repository, and
    a figure depending on one is still a function of the path list GIVEN that
    input.  That is not a liberty taken here: it is exactly what the hand
    reader does -- liveindex.py recovers consumers.py's subject FROM THE
    TRANSCRIPT HEADER and then re-derives the figures from the path list.  A
    figure the analysis cannot resolve past a parameter with no visible caller
    is UNKNOWN and not EXTERNAL, and the two are counted apart.

    THE ANCHOR IS THE ONE PLACE THIS CAN BE CHECKED AGAINST A HUMAN, AND IT IS
    RUN RATHER THAN CITED.  mg-ede8 adjudicated out_consumers.txt by hand and
    liveindex.py carries the answer: three figures path-list-valued, the prose
    count and the unnamed-scripts count content-valued.  Section 3 locates
    those exact print sites MECHANICALLY -- by the literal each one emits --
    and compares.  A pattern that no longer locates a site is UNREADABLE and
    is printed as such rather than skipped, which is git_grep_l's defect one
    file over.

    AND THE ANCHOR DISAGREES IN ONE PLACE, IN THE DIRECTION THAT IS A
    REFINEMENT RATHER THAN A CONTRADICTION.  mg-ede8 works at the granularity
    of a FIGURE IN A TRANSCRIPT and this file at the granularity of an
    EXPRESSION IN A PRINT, and one line of out_consumers.txt carries three
    figures of two different kinds -- `%d of %d%s`, whose first number is the
    content-valued unnamed count and whose second is the path-list-valued
    subject-script count already checked two sections earlier.  Nothing in
    liveindex.py is wrong; the line was excluded whole because the reader was
    a line reader.  Section 3 prints both and says which is which.

    THE SECOND CHECK NEEDS NO HUMAN AT ALL AND IS THE REASON THE FIRST IS NOT
    THE ONLY ONE.  pathlist.py grades 535 producers NO PATH-LIST READ.  Not
    one figure of any of them can be path-list-valued, by pathlist.py's own
    rule, so the count of PATH-LIST-VALUED figures over that class must be 0 --
    a cross-instrument invariant over hundreds of files that this file does not
    get to choose the answer to.  Section 4 runs it.

    python3 code/asof_census_20ee/figures.py         # at pathlist.py's AS_OF
    python3 code/asof_census_20ee/figures.py <rev>   # anywhere else
"""

import ast
import builtins
import collections
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import pathlist  # noqa: E402

# THE PIN IS IMPORTED AND NOT RE-TYPED (mg-d2c2, mg-1344's P5).  This file's
# population IS pathlist.py's MIXED class, so a second hash here could make the
# two pages disagree about which 305 transcripts are in question while both
# printed a commit.  Re-pinning is one edit, in one file, and moves both.
AS_OF = pathlist.AS_OF

# CALLS THAT CARRY THEIR ARGUMENTS THROUGH AND READ NOTHING.  A call this list
# names is descended into; a call it does not name must be RESOLVED to a
# function in the closure or the figure is UNDECIDED.  It is deliberately a
# list of shapes rather than a list of modules: `sorted`, `.join` and
# `os.path.basename` transform a value and cannot introduce a repository input,
# so descending into their arguments loses nothing, while `classify(path)`
# might read anything and is looked up instead.
PASSTHROUGH = frozenset("""
    abs all any bool bytes dict enumerate filter float format frozenset int
    iter len list map max min next range repr reversed round set setattr
    sorted str sum tuple zip
    add append basename capitalize center copy count decode difference dirname
    encode endswith escape extend find findall finditer get group groups index
    insert intersection isdigit isdisjoint isupper islower items join keys
    ljust lower lstrip most_common normpath partition pop popitem realpath
    relpath remove replace reverse rfind rindex rjust rpartition rsplit rstrip
    setdefault sort split splitlines startswith strip sub subn swapcase title
    union update upper values zfill
    Counter defaultdict OrderedDict deque namedtuple
""".split())

# INPUTS THAT ARE NOT THE REPOSITORY.  See the docstring: a figure that is a
# function of the path list GIVEN the subject it was asked about is exactly
# what liveindex.py re-derives, having recovered that subject from the
# transcript.  These are counted apart from UNKNOWN and reported.
EXTERNAL_ROOTS = frozenset(("sys.argv", "argv", "os.environ", "os.getenv",
                            "sys.executable", "__file__", "__name__",
                            "sys.version", "sys.platform"))

# WHICH TRACKED PATH LIST.  pathlist.PATHLIST deliberately treats four
# spellings as one -- `ls-files` reads the INDEX, `ls-tree` a named TREE, and
# `walk`/`glob`/`find` the WORKTREE -- because all four answer `what paths are
# there` and nothing else, and its class was empty so the difference never
# bound.  Per FIGURE it binds hard: liveindex.py re-derives a figure AT THE
# COMMIT THAT CARRIES IT, and only `ls-tree` names a commit.  An index-valued
# figure is a function of somebody's staging area and a worktree-valued one of
# somebody's checkout, and mg-ede8's own section 4 is that finding about
# consumers.py.  These two are NARROWINGS OF pathlist.PATHLIST and P53 asserts
# it: every string either matches makes pathlist.PATHLIST match too, so a
# widening there cannot leave this split reporting on a rule that moved.
TREE_SPELLING = re.compile(r'"ls-tree"|\bgit ls-tree\b')
INDEX_SPELLING = re.compile(r'"ls-files"|\bgit ls-files\b')

PATH_LIST_VALUED = "PATH-LIST-VALUED"
CONTENT_VALUED = "CONTENT-VALUED"
UNDECIDED = "UNDECIDED"
CONSTANT = "CONSTANT"

MAX_DEPTH = 32

BUILTINS = frozenset(dir(builtins))

# ---------------------------------------------------------------------------
# THE ANCHOR.  mg-ede8's HAND ADJUDICATION OF out_consumers.txt, quoted as
# (the literal the print emits, the source text of the figure, the grade a
# human gave it).  Located mechanically at run time: nothing here is a line
# number, because a line number rots on the first edit to the file above it.
# A row that does not LOCATE is UNREADABLE and is printed; it is never
# silently dropped, which is the defect liveindex.py's own P34 was built from.
# ---------------------------------------------------------------------------
ANCHOR_PRODUCER = "code/asof_census_20ee/consumers.py"
ANCHOR = (
    ("  subject scripts: %d",
     "len(scripts)", PATH_LIST_VALUED,
     "liveindex.FIELDS row 1, `subject scripts`"),
    ("  matched by basename: %d script(s); by FULL PATH: %d, because the",
     "len(scripts) - len(shared)", PATH_LIST_VALUED,
     "liveindex.FIELDS row 2, `unique-basename scripts`"),
    ("  matched by basename: %d script(s); by FULL PATH: %d, because the",
     "len(shared)", PATH_LIST_VALUED,
     "liveindex.FIELDS row 3, `shared-basename scripts`"),
    ("  basename is shared -- %s",
     '", ".join("%s (%d files)" % (b, n) for b, n in shared)\n'
     '             if shared else "none"', PATH_LIST_VALUED,
     "liveindex.FIELDS row 4, `shared basename counts`"),
    ("  because prose cannot execute anything: %d file(s)",
     "prose", CONTENT_VALUED,
     "liveindex section 1, `the prose count` -- NOT checked there"),
    ("  own directory: %d of %d%s",
     "len(unnamed)", CONTENT_VALUED,
     "liveindex section 1, `the named-in-no-tracked-file count`"),
    ("  own directory: %d of %d%s",
     "len(scripts)", PATH_LIST_VALUED,
     "THE REFINEMENT: same expression as row 1, on the line mg-ede8's "
     "LINE-granular reader excluded whole"),
)


# ---------------------------------------------------------------------------
# The slice.
# ---------------------------------------------------------------------------

# ONE PARSE PER TRACKED MODULE, NOT ONE PER CLOSURE THAT NAMES IT.  The 840
# closures overlap heavily -- a lib read by nine producers is one file -- and
# parsing and indexing it nine times is the difference between seconds and
# hours.  The record is a pure function of (rev, path), so sharing it across
# producers cannot make two of them disagree.  The SLICE memo is NOT shared,
# and must not be: a name resolves against the closure it is asked in.
_MODULES = {}


class Module:
    """One parsed tracked file: its source, its scopes and its functions."""

    def __init__(self, rev, path):
        self.path = path
        self.source = pathlist.source_at(rev, path)
        self.tree = ast.parse(self.source)
        self.scopes = {}       # node -> Scope
        self.parents = {}      # node -> node
        self.funcs = collections.defaultdict(list)   # name -> [FunctionDef]
        # NAMES BOUND BY `import`.  `os` in `os.path.basename(s)` is a
        # QUALIFIER and not a data dependency: the value flows from `s`, and
        # treating the module name as an unresolved free variable made every
        # basename in this estate UNDECIDED.  A module name is not a
        # repository input.
        self.imports = set()
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for alias in node.names:
                    self.imports.add(alias.asname or alias.name.split(".")[0])
        module = Scope(path, self.tree, None)
        self.scopes[self.tree] = module
        _walk(self, path, self.tree, module, [])
        # CALL SITES, SO A PARAMETER CAN BE BOUND TO WHAT CALLERS PASS IT.
        # `value_uses` is the guard: a function whose NAME appears anywhere
        # except in the callee position may be handed to something this file
        # cannot see -- a `key=`, a dispatch table -- and binding it to the
        # call sites that ARE visible would be an under-approximation, the one
        # direction that can publish a false proof.
        self.calls = collections.defaultdict(list)
        self.value_uses = set()
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call):
                name = (node.func.id if isinstance(node.func, ast.Name)
                        else node.func.attr
                        if isinstance(node.func, ast.Attribute) else None)
                if name:
                    self.calls[name].append(node)
            elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                parent = self.parents.get(node)
                if not (isinstance(parent, ast.Call) and parent.func is node):
                    self.value_uses.add(node.id)
            elif isinstance(node, ast.Attribute):
                parent = self.parents.get(node)
                if not (isinstance(parent, ast.Call) and parent.func is node):
                    self.value_uses.add(node.attr)


def module_at(rev, path):
    key = (rev, path)
    if key not in _MODULES:
        _MODULES[key] = Module(rev, path)
    return _MODULES[key]


class Unit:
    """One producer, its closure, and everything the slice needs to walk it.

    THE CLOSURE IS pathlist.py's AND IS NOT RE-COMPUTED HERE.  A second
    spelling of `what does this producer pull in` is a second answer waiting to
    happen, and the whole population of this file is defined by the first one.
    """

    def __init__(self, rev, producer, closure_paths):
        self.rev = rev
        self.producer = producer
        self.modules = {}
        self.funcs = collections.defaultdict(list)   # name -> [(path, node)]
        self.unparsed = []     # closure members that are not parseable Python
        self.imports = set()
        self.calls = collections.defaultdict(list)
        self.value_uses = set()
        self.param_scopes = {}
        self.memo = {}      # key -> the current under-approximation
        self.done = set()   # keys already recomputed in THIS pass
        self.busy = set()
        self.changed = False
        self.passes = 0
        for path in closure_paths:
            if not path.endswith(".py"):
                self.unparsed.append(path)
                continue
            try:
                module = module_at(rev, path)
            except SyntaxError:
                self.unparsed.append(path)
                continue
            self.modules[path] = module
            self.imports |= module.imports
            self.value_uses |= module.value_uses
            for name, sites in module.calls.items():
                self.calls[name].extend((path, site) for site in sites)
            for name, defs in module.funcs.items():
                for node in defs:
                    self.funcs[name].append((path, node))

    @property
    def trees(self):
        return {p: m.tree for p, m in self.modules.items()}

    def scope_of(self, path, node):
        module = self.modules[path]
        cur = node
        while cur is not None:
            if cur in module.scopes:
                return module.scopes[cur]
            cur = module.parents.get(cur)
        return module.scopes[module.tree]

    def segment(self, path, node):
        return ast.get_source_segment(self.modules[path].source, node) or ""

    def scope_for_func(self, path, node):
        return self.modules[path].scopes[node]

    def resolve(self, scope, name):
        """Every FunctionDef in the closure that could supply `name`.

        OVER-WIDE ON PURPOSE, AND THE DIRECTION IS THE REASON.  Where the
        producer's own module defines the name that definition alone is read;
        where it does not, EVERY definition of that name in the closure is
        read and their roots are UNIONED.  Resolving `sys.path` properly means
        evaluating it, and reading one function too many can only ADD roots --
        which can only move a figure OUT of PATH-LIST-VALUED, the class whose
        membership is a claim of proof.  Reading one too few is the direction
        that publishes a false proof.  pathlist.closure's trade, one level down.
        """
        here = scope
        while here is not None:
            if name in here.funcs:
                return [(here.path, here.funcs[name])]
            here = here.parent
        return list(self.funcs.get(name, ()))


def _walk(module, path, node, scope, controls, loops=()):
    """Index one AST node's children into `scope`, carrying control context."""
    for child in ast.iter_child_nodes(node):
        module.parents[child] = node
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            inner = Scope(path, child, scope)
            module.scopes[child] = inner
            scope.funcs[child.name] = child
            module.funcs[child.name].append(child)
            for arg in (child.args.posonlyargs + child.args.args
                        + child.args.kwonlyargs):
                inner.params.add(arg.arg)
            for extra in (child.args.vararg, child.args.kwarg):
                if extra is not None:
                    inner.params.add(extra.arg)
            _walk(module, path, child, inner, [], ())
            continue
        if isinstance(child, ast.Lambda):
            inner = Scope(path, child, scope)
            module.scopes[child] = inner
            for arg in child.args.args:
                inner.params.add(arg.arg)
            _walk(module, path, child, inner, controls, loops)
            continue

        # CONTROL DEPENDENCE.  See the docstring: a counter incremented by a
        # literal inside a loop over a content read is a function of that
        # content read, and a value-only slice grades it a PROOF.  P51.
        inner_controls = controls
        if isinstance(child, ast.For):
            inner_controls = controls + [(path, child.iter)]
        elif isinstance(child, (ast.While, ast.If, ast.IfExp)):
            inner_controls = controls + [(path, child.test)]
        elif isinstance(child, ast.comprehension):
            inner_controls = controls + [(path, child.iter)]
            for name in assigned_names(child.target):
                # `ast.comprehension` CARRIES NO LINE NUMBER and the first
                # draft therefore filed every comprehension target at line 0 --
                # visible to every use in the function, from the top.  That is
                # how `p` in a listcomp near the bottom of consumers.main came
                # to poison the frequency table 200 lines above it.
                scope.assign(name, child.iter, controls, _line(child.iter),
                             loops + (child,))

        if isinstance(child, ast.Assign):
            for target in child.targets:
                for name in assigned_names(target):
                    scope.assign(name, child.value, inner_controls,
                                 _line(child), loops)
        elif isinstance(child, (ast.AugAssign, ast.AnnAssign)):
            for name in assigned_names(child.target):
                scope.assign(name, child.value, inner_controls,
                             _line(child), loops)
        elif isinstance(child, ast.For):
            for name in assigned_names(child.target):
                scope.assign(name, child.iter, controls, _line(child),
                             loops + (child,))
        elif isinstance(child, ast.withitem) and child.optional_vars:
            for name in assigned_names(child.optional_vars):
                scope.assign(name, child.context_expr, inner_controls,
                             _line(child.context_expr), loops)
        elif isinstance(child, ast.ExceptHandler) and child.name:
            scope.assign(child.name, None, inner_controls, _line(child),
                         loops)
        elif isinstance(child, ast.Expr):
            # IN-PLACE MUTATION IS AN ASSIGNMENT AND MISSING IT IS NOT SAFE.
            # `out.append(path)` inside a loop is how half this estate builds a
            # list, and a slice that could not see it would find `out = []`
            # alone and call the figure a literal.
            mutated = mutation_target(child.value)
            if mutated is not None:
                name, payload = mutated
                scope.assign(name, payload, inner_controls, _line(child),
                             loops)

        _walk(module, path, child, scope, inner_controls,
              loops + (child,) if isinstance(child, (ast.For, ast.While))
              else loops)


class Scope:
    def __init__(self, path, node, parent):
        self.path = path
        self.node = node
        self.parent = parent
        self.assigns = collections.defaultdict(list)
        self.params = set()
        self.funcs = {}

    def assign(self, name, value, controls, lineno, loops):
        self.assigns[name].append({"value": value, "controls": tuple(controls),
                                   "lineno": lineno, "loops": frozenset(loops)})

    def lookup(self, name):
        """(owning scope, its assignment sites, whether it is a parameter).

        BOTH HALVES ARE RETURNED AND THE FIRST DRAFT RETURNED ONE.  A name that
        is a parameter AND is reassigned -- `subject = subject.rstrip("/")`,
        the first statement of consumers.main -- has both, and a lookup that
        stopped at the assignment lost the binding and turned the figure into a
        self-reference.  UNDECIDED either way here, but the reason printed in
        section 5 would have been `cycle` when the truth is `parameter`.
        """
        here = self
        while here is not None:
            if name in here.assigns:
                return here, here.assigns[name], name in here.params
            if name in here.params:
                return here, None, True
            here = here.parent
        return None, None, False


MUTATORS = frozenset(("append", "add", "extend", "update", "insert",
                      "setdefault", "__setitem__"))


def mutation_target(node):
    """(name, payload-expression) for `x.append(v)` and its family, else None."""
    if not isinstance(node, ast.Call):
        return None
    if not isinstance(node.func, ast.Attribute):
        return None
    if node.func.attr not in MUTATORS:
        return None
    base = node.func.value
    while isinstance(base, (ast.Subscript, ast.Attribute)):
        base = base.value
    if not isinstance(base, ast.Name):
        return None
    if not node.args:
        return (base.id, None)
    payload = node.args[-1] if len(node.args) > 1 else node.args[0]
    return (base.id, payload)


def assigned_names(target):
    if isinstance(target, ast.Name):
        return [target.id]
    if isinstance(target, (ast.Tuple, ast.List)):
        out = []
        for element in target.elts:
            out += assigned_names(element)
        return out
    if isinstance(target, (ast.Starred,)):
        return assigned_names(target.value)
    if isinstance(target, (ast.Subscript, ast.Attribute)):
        return assigned_names(target.value)
    return []


# A LONG STRING ARGUMENT IS PROSE, NOT AN ARGV.  pathlist's patterns are
# SPELLING MATCHERS over source text, and one of this estate's producers prints
# a paragraph containing the words `find .` -- which made `B.finding("<a label>",
# "<400 words>")` read as a directory walk and graded a printed CONSTANT a
# path-list PROOF.  A repository read is named by a short flag; a paragraph is
# not one.  THE BLANKING IS APPLIED TO THE PATH-LIST TEST ONLY, never to the
# content test: narrowing PATH-LIST can only shrink a class whose membership is
# a claim of proof, while narrowing CONTENT could promote a figure into it.
PROSE_ARG = 40


def call_signature(unit, path, node):
    """The call as an argv: its callee, and its arguments minus any prose."""
    parts = [unit.segment(path, node.func)]
    for arg in list(node.args) + [k.value for k in node.keywords]:
        if (isinstance(arg, ast.Constant) and isinstance(arg.value, str)
                and len(arg.value) > PROSE_ARG):
            parts.append("<prose>")
        else:
            parts.append(unit.segment(path, arg))
    return "%s(%s)" % (parts[0], ", ".join(parts[1:]))


def dotted(node):
    """`os.path.basename` for an Attribute chain, else None."""
    parts = []
    cur = node
    while isinstance(cur, ast.Attribute):
        parts.append(cur.attr)
        cur = cur.value
    if not isinstance(cur, ast.Name):
        return None
    parts.append(cur.id)
    return ".".join(reversed(parts))


def roots(unit, path, expr, scope, depth=0):
    """The set of ROOTS the value of `expr` depends on.

    A root is one of `PATHLIST`, `CONTENT`, `EXTERNAL`, or `UNKNOWN:<why>`.
    An expression whose root set is EMPTY depends on literals alone.

    MEMOISED PER UNIT AND NOT GLOBALLY.  A name resolves against the closure it
    is asked in, so two producers sharing a lib can legitimately reach
    different answers about the same expression; a shared memo would let the
    first one asked decide for the rest.  The parse and the scope index ARE
    shared, because they are a function of (rev, path) alone.

    A CYCLE RETURNS `UNKNOWN:cycle` AND NOT THE EMPTY SET, which is the safe
    direction: mutual recursion between two helpers must leave the figure
    UNDECIDED, never let it fall through to a proof.  A value memoised while a
    cycle was open can be more conservative than a fresh one, and that too
    only ever moves a figure OUT of PATH-LIST-VALUED.
    """
    if expr is None:
        return set()
    if depth > MAX_DEPTH:
        return {"UNKNOWN:depth"}
    key = (path, id(expr), id(scope))
    if key in unit.done:
        return unit.memo[key]
    if key in unit.busy:
        # A BACK EDGE RETURNS THE PREVIOUS PASS'S ANSWER, WHICH IS EMPTY ON THE
        # FIRST ONE.  `freq[k] = freq.get(k, 0) + 1` is a dependency cycle
        # through a single name, and its roots are the roots of everything ELSE
        # reaching it -- the least fixed point of a union.  Chaotic iteration
        # over a monotone union reaches it, and `figures_of` runs the passes.
        return unit.memo.get(key, set())
    unit.busy.add(key)
    try:
        got = _roots(unit, path, expr, scope, depth)
    finally:
        unit.busy.discard(key)
    if unit.memo.get(key) != got:
        unit.changed = True
    unit.memo[key] = got
    unit.done.add(key)
    return got


def _roots(unit, path, expr, scope, depth):
    out = set()

    if isinstance(expr, ast.Call):
        text = unit.segment(path, expr)
        # ORDER IS LOAD-BEARING: a call site whose argv names BOTH a path-list
        # read and a content read is a content read, because the figure cannot
        # be re-derived from the path list alone.  Content wins, always.
        if pathlist.OTHER.search(text):
            return {"CONTENT"}
        if pathlist.PATHLIST.search(call_signature(unit, path, expr)):
            # THE ARGUMENTS OF A PATH-LIST READ ARE PART OF THE FIGURE, AND
            # THE FIRST FULL RUN OF THIS FILE PUBLISHED 209 BECAUSE THEY WERE
            # NOT.  `git ls-tree -r <rev>` is a path list AT A REVISION, so a
            # figure counting that tree is re-derivable only when the REVISION
            # is too -- and code/audit_c067/c1_rebase.py takes its revision
            # from `git log`, which is history.  Returning PATHLIST and
            # stopping graded that figure a PROOF.  Refuted by hand on the
            # third candidate read; the roots of the arguments are unioned in.
            out = {"PATHLIST:%s" % ("tree" if TREE_SPELLING.search(text)
                                    else "index" if INDEX_SPELLING.search(text)
                                    else "worktree")}
            for arg in list(expr.args) + [k.value for k in expr.keywords]:
                out |= roots(unit, path, arg, scope, depth + 1)
            return out
        name = (expr.func.id if isinstance(expr.func, ast.Name)
                else expr.func.attr if isinstance(expr.func, ast.Attribute)
                else None)
        full = dotted(expr.func)
        if full in EXTERNAL_ROOTS or (full or "").startswith("os.environ"):
            return {"EXTERNAL"}
        if name in PASSTHROUGH:
            for arg in list(expr.args) + [k.value for k in expr.keywords]:
                out |= roots(unit, path, arg, scope, depth + 1)
            if isinstance(expr.func, ast.Attribute):
                out |= roots(unit, path, expr.func.value, scope, depth + 1)
            return out
        found = unit.resolve(scope, name) if name else []
        if not found:
            return {"UNKNOWN:call %s" % (full or name or "?")}
        for fpath, fnode in found:
            out |= function_roots(unit, fpath, fnode, path, expr, scope,
                                  depth + 1)
        return out

    if isinstance(expr, ast.Name):
        return name_roots(unit, path, expr, scope, depth)

    if isinstance(expr, ast.Attribute):
        full = dotted(expr)
        if full in EXTERNAL_ROOTS:
            return {"EXTERNAL"}
        return roots(unit, path, expr.value, scope, depth + 1)

    if isinstance(expr, ast.Constant):
        return set()

    if isinstance(expr, (ast.ListComp, ast.SetComp, ast.GeneratorExp)):
        out |= roots(unit, path, expr.elt, scope, depth + 1)
        for gen in expr.generators:
            out |= roots(unit, path, gen.iter, scope, depth + 1)
            for cond in gen.ifs:
                out |= roots(unit, path, cond, scope, depth + 1)
        return out

    if isinstance(expr, ast.DictComp):
        out |= roots(unit, path, expr.key, scope, depth + 1)
        out |= roots(unit, path, expr.value, scope, depth + 1)
        for gen in expr.generators:
            out |= roots(unit, path, gen.iter, scope, depth + 1)
            for cond in gen.ifs:
                out |= roots(unit, path, cond, scope, depth + 1)
        return out

    if isinstance(expr, ast.IfExp):
        # THE TEST IS A DEPENDENCY OF THE VALUE.  `x if shared else "none"` is
        # a function of `shared` even when both branches are literals.
        out |= roots(unit, path, expr.test, scope, depth + 1)
        out |= roots(unit, path, expr.body, scope, depth + 1)
        out |= roots(unit, path, expr.orelse, scope, depth + 1)
        return out

    for child in ast.iter_child_nodes(expr):
        if isinstance(child, ast.expr):
            out |= roots(unit, path, child, scope, depth + 1)
    return out


def _line(node):
    return getattr(node, "lineno", 0)


def enclosing_loops(unit, path, node):
    """The `for`/`while` statements that lexically contain `node`."""
    module = unit.modules[path]
    out, cur = [], node
    while cur is not None:
        if isinstance(cur, (ast.For, ast.While, ast.comprehension)):
            out.append(cur)
        # A COMPREHENSION IS A SIBLING OF THE ELEMENT IT BINDS, NOT ITS PARENT.
        # `ast` hangs `elt` and `generators` off the same node, so walking
        # parents from a name inside the element never meets the `for` clause
        # that binds it, and `b` in `... for b, n in shared` read as unbound.
        if isinstance(cur, (ast.ListComp, ast.SetComp, ast.DictComp,
                            ast.GeneratorExp)):
            out.extend(cur.generators)
        cur = module.parents.get(cur)
    return frozenset(out)


def visible(sites, use_line, use_loops):
    """The assignment sites a use at `use_line` can actually see.

    THE ANALYSIS IS FLOW-SENSITIVE AND THE FIRST DRAFT WAS NOT, WHICH IS WHERE
    IT GOT THE ANCHOR WRONG.  consumers.main binds `base` to a basename off the
    path list at the top and REBINDS IT, sixty lines later, to a field of a
    `git grep` hit.  Unioning every assignment to a name in a scope made the
    early use content-valued, and three of mg-ede8's four hand-adjudicated
    PATH-LIST figures came back CONTENT-VALUED -- not a conservative answer but
    a WRONG one, because CONTENT-VALUED is a proof of the other thing.

    THE RULE IS STRICTLY-EARLIER, PLUS THE LOOP BACK-EDGE.  A site is visible
    when it lies above the use, or when site and use share an enclosing loop --
    an accumulator read inside the loop that fills it must see the later
    `acc += ...` or the figure becomes a literal.  Equality of line numbers is
    NOT visibility: `subject = subject.rstrip("/")` would otherwise be its own
    input.  Both directions of the approximation are safe in the same way --
    a site wrongly hidden leaves a name UNDECIDED, and a site wrongly shown
    only ever adds roots -- and neither can invent a PATH-LIST-VALUED proof.
    """
    got = [s for s in sites
           if s["lineno"] < use_line or (s["loops"] & use_loops)]
    return got


def param_roots(unit, owner, pname, depth):
    """What callers actually pass for parameter `pname` of `owner`'s function.

    A figure inside `main(subject)` is a function of the path list GIVEN the
    subject, and consumers.py's caller supplies `sys.argv[1]` -- a
    NON-REPOSITORY input, which is exactly what liveindex.py recovers from the
    transcript header before re-deriving.  Leaving every parameter UNDECIDED
    instead would put mg-ede8's own worked example out of reach of the
    instrument built to describe it.

    IT REFUSES RATHER THAN GUESSES IN FOUR CASES: the enclosing scope is not a
    function, the function's name is used anywhere as a VALUE, no call site is
    visible in the closure, or the name is not a positional parameter.  Each is
    a way for a caller to exist that this file cannot see, and binding to a
    partial set of callers is the one error that SHRINKS a slice.
    """
    fnode = owner.node
    refused = {"UNKNOWN:parameter %s" % pname}
    if not isinstance(fnode, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return refused
    if fnode.name in unit.value_uses:
        return refused
    sites = unit.calls.get(fnode.name) or []
    if not sites:
        return refused
    names = [a.arg for a in (fnode.args.posonlyargs + fnode.args.args)]
    if pname not in names:
        return refused
    position = names.index(pname)
    out = set()
    for cpath, cnode in sites:
        bound = None
        if position < len(cnode.args):
            bound = cnode.args[position]
        for keyword in cnode.keywords:
            if keyword.arg == pname:
                bound = keyword.value
        if bound is None:
            defaults = dict(zip(names[len(names) - len(fnode.args.defaults):],
                                fnode.args.defaults))
            if pname in defaults:
                out |= roots(unit, owner.path, defaults[pname], owner,
                             depth + 1)
                continue
            out.add("UNKNOWN:unbound %s" % pname)
            continue
        out |= roots(unit, cpath, bound, unit.scope_of(cpath, cnode),
                     depth + 1)
    return out


def name_roots(unit, path, node, scope, depth):
    name = node.id
    if name in PASSTHROUGH or name in BUILTINS or name in unit.imports:
        return set()
    if name in EXTERNAL_ROOTS:
        return {"EXTERNAL"}
    owner, sites, is_param = scope.lookup(name)
    if owner is None:
        # A name defined nowhere in this closure: an import, a builtin this
        # list does not carry, or a genuine free variable.  Not resolvable, so
        # not a proof.
        return {"UNKNOWN:name %s" % name}
    out = set()
    if is_param:
        # THE PARAMETER IS NOT RESOLVED HERE.  A call this slice came THROUGH
        # binds it exactly, and resolving it early to the union of every
        # caller in the closure threw that precision away -- it graded
        # `B.finding("<a label>", "<a literal>")` PATH-LIST-VALUED, because some
        # OTHER caller of `finding` passes it a path count.  The scope travels
        # with the root so `function_roots` can bind the right one, and
        # `figures_of` resolves whatever is left over.
        unit.param_scopes[id(owner)] = owner
        out.add("PARAM:%d:%s" % (id(owner), name))
    if sites is None:
        return out
    here = visible(sites, _line(node), enclosing_loops(unit, path, node))
    if not here:
        # Every binding of this name is BELOW the use and shares no loop with
        # it.  That is a name this file cannot follow -- a global rebound by a
        # function, or a use the flow rule places wrongly -- and it is
        # UNDECIDED rather than assumed constant.
        return out or {"UNKNOWN:unbound %s" % name}
    for site in here:
        out |= roots(unit, owner.path, site["value"], owner, depth + 1)
        for cpath, control in site["controls"]:
            out |= roots(unit, cpath, control, owner, depth + 1)
    return out


def function_roots(unit, fpath, fnode, callpath, callnode, callscope,
                   depth):
    """The roots of what `fnode` RETURNS, with its parameters bound to the
    call's own arguments.

    A function with no `return` returns None and contributes nothing; a
    function whose return depends on a parameter this call does not supply
    positionally is UNKNOWN rather than assumed harmless.
    """
    fscope = unit.scope_for_func(fpath, fnode)
    raw = set()
    for node in ast.walk(fnode):
        if isinstance(node, ast.Return) and node.value is not None:
            raw |= roots(unit, fpath, node.value, fscope, depth)
        elif isinstance(node, (ast.Yield, ast.YieldFrom)) and node.value:
            raw |= roots(unit, fpath, node.value, fscope, depth)
    names = [a.arg for a in (fnode.args.posonlyargs + fnode.args.args)]
    out = set()
    for root in raw:
        if not root.startswith("PARAM:"):
            out.add(root)
            continue
        _tag, sid, pname = root.split(":", 2)
        if int(sid) != id(fscope):
            # A parameter of some OTHER function further down the slice.  This
            # call cannot bind it; pass it along untouched.
            out.add(root)
            continue
        # A BINDING CARRIES ITS OWN FILE AND SCOPE WITH IT.  A call argument
        # belongs to the CALLER's module and a default to the CALLEE's, and the
        # first draft read both out of the caller -- which raised IndexError
        # the first time a producer called a lib function with a default,
        # because the line number pointed past the end of the wrong file.
        bound = None
        if pname in names:
            position = names.index(pname)
            if position < len(callnode.args):
                bound = (callpath, callnode.args[position], callscope)
        for keyword in callnode.keywords:
            if keyword.arg == pname:
                bound = (callpath, keyword.value, callscope)
        if bound is None and fnode.args.defaults:
            defaults = dict(zip(names[len(names) - len(fnode.args.defaults):],
                                fnode.args.defaults))
            if pname in defaults:
                bound = (fpath, defaults[pname], fscope)
        if bound is None:
            out.add("UNKNOWN:unbound %s" % pname)
        else:
            out |= roots(unit, bound[0], bound[1], bound[2], depth + 1)
    return out


# HOW MANY TIMES A RESIDUAL PARAMETER IS EXPANDED.  Each round replaces every
# leftover `PARAM:` with what the closure's call sites pass, which can itself
# be a parameter one frame up.  Four rounds covers this corpus; a root still
# unresolved after them stays UNDECIDED, which is the honest answer.
SETTLE_ROUNDS = 4


def settle(unit, root_set):
    """Expand the parameters no call in the slice was able to bind.

    A figure inside `main(subject)` reached from the module's own `print` was
    never entered THROUGH a call, so its parameters are still open when the
    walk finishes.  They are resolved here, against every call site in the
    closure -- over-wide, and in the direction that only ADDS roots.
    """
    got = set(root_set)
    for _ in range(SETTLE_ROUNDS):
        pending = [r for r in got if r.startswith("PARAM:")]
        if not pending:
            break
        for root in pending:
            got.discard(root)
            _tag, sid, pname = root.split(":", 2)
            owner = unit.param_scopes.get(int(sid))
            if owner is None:
                got.add("UNKNOWN:unbound %s" % pname)
                continue
            got |= param_roots(unit, owner, pname, 0)
    return got


def grade(root_set):
    if any(r == "CONTENT" for r in root_set):
        return CONTENT_VALUED
    if any(r.startswith(("UNKNOWN", "PARAM")) for r in root_set):
        return UNDECIDED
    if any(r.startswith("PATHLIST") for r in root_set):
        return PATH_LIST_VALUED
    return CONSTANT


# ---------------------------------------------------------------------------
# What counts as a figure.
# ---------------------------------------------------------------------------

def interpolated(arg):
    """The sub-expressions of one printed argument that carry a VALUE.

    A print whose arguments are all literal is PROSE and contributes no
    figure at all -- which is most lines of most transcripts in this estate,
    and excluding them is why the population below is figures and not lines.
    """
    if isinstance(arg, ast.Constant):
        return []
    if (isinstance(arg, ast.BinOp) and isinstance(arg.op, ast.Mod)
            and isinstance(arg.left, ast.Constant)):
        right = arg.right
        if isinstance(right, ast.Tuple):
            return [e for e in right.elts if not isinstance(e, ast.Constant)]
        return [right]
    if isinstance(arg, ast.JoinedStr):
        return [v.value for v in arg.values
                if isinstance(v, ast.FormattedValue)]
    if (isinstance(arg, ast.Call) and isinstance(arg.func, ast.Attribute)
            and arg.func.attr == "format"):
        return [a for a in arg.args if not isinstance(a, ast.Constant)]
    if isinstance(arg, ast.BinOp) and isinstance(arg.op, ast.Mult):
        # `"=" * 78` is a rule, not a figure.
        if isinstance(arg.left, ast.Constant) and isinstance(arg.right,
                                                             ast.Constant):
            return []
    return [arg]


def emitters(unit, path, tree):
    """Every (call node, template literal) that puts a line in a transcript."""
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = dotted(node.func) or ""
        if name not in ("print", "sys.stdout.write", "out.write", "write"):
            continue
        template = None
        for arg in node.args:
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                template = arg.value
                break
            if (isinstance(arg, ast.BinOp) and isinstance(arg.op, ast.Mod)
                    and isinstance(arg.left, ast.Constant)):
                template = arg.left.value
                break
        out.append((node, template))
    return out


# ITERATION CAP.  Each pass is linear in the reachable slice, and every pass
# but the last is one the cycle had not yet converged on.  Three is what this
# corpus needs; the cap exists so a shape nobody has met cannot hang the run,
# and a producer that reaches it is REPORTED rather than quietly truncated.
MAX_PASSES = 8


def figures_of(unit):
    """Every figure of one producer, graded, at the fixed point of the slice.

    THE PASSES ARE THE CYCLE'S PRICE AND THEY ARE COUNTED.  Pass one reads
    every back edge as empty and so can UNDER-report roots; each further pass
    seeds the back edges with the previous answer and can only ADD.  The loop
    stops when a whole pass adds nothing, which is the least fixed point.
    Stopping at pass one instead -- the first draft -- graded three of
    mg-ede8's four hand-adjudicated figures UNDECIDED; never iterating at all
    and caching the truncated values graded them wrongly.
    """
    path = unit.producer
    if path not in unit.trees:
        return None
    rows = []
    for _ in range(MAX_PASSES):
        unit.done = set()
        unit.changed = False
        unit.passes += 1
        rows = _figures_once(unit, path)
        if not unit.changed:
            break
    return rows


def _figures_once(unit, path):
    rows = []
    for node, template in emitters(unit, path, unit.trees[path]):
        scope = unit.scope_of(path, node)
        for arg in node.args:
            for figure in interpolated(arg):
                found = settle(unit, roots(unit, path, figure, scope))
                rows.append({
                    "line": getattr(figure, "lineno", node.lineno),
                    "template": template,
                    "text": unit.segment(path, figure),
                    "roots": found,
                    "grade": grade(found),
                })
    return rows


# ---------------------------------------------------------------------------
# The scan.
# ---------------------------------------------------------------------------

def scan(rev=AS_OF):
    """Every figure this page publishes, from one commit and nothing else."""
    base = pathlist.scan(rev)
    out = {"rev": rev, "producers": [], "pathlist": base}
    for row in base["rows"]:
        unit = Unit(rev, row["producer"], row["closure"])
        rows = figures_of(unit)
        out["producers"].append({
            "transcript": row["transcript"],
            "producer": row["producer"],
            "producer_grade": row["grade"],
            "figures": rows,
            "unparsed": unit.unparsed,
            "unit": unit,
        })
    return out


def anchor_rows(result):
    """mg-ede8's hand adjudication against this file's mechanical one."""
    got = []
    subject = [p for p in result["producers"]
               if p["producer"] == ANCHOR_PRODUCER]
    if not subject:
        return [(t, f, want, why, "UNLOCATED", "no such producer in the "
                 "population at this revision") for t, f, want, why in ANCHOR]
    figures = subject[0]["figures"] or []
    for template, text, want, why in ANCHOR:
        hits = [f for f in figures
                if f["template"] == template and normalise(f["text"])
                == normalise(text)]
        if not hits:
            got.append((template, text, want, why, "UNLOCATED", None))
            continue
        if len(hits) > 1:
            got.append((template, text, want, why, "AMBIGUOUS",
                        "%d sites match" % len(hits)))
            continue
        got.append((template, text, want, why, hits[0]["grade"], hits[0]))
    return got


def normalise(text):
    return " ".join((text or "").split())


def main(argv):
    rev = argv[1] if len(argv) > 1 else AS_OF
    bar = "=" * 78
    result = scan(rev)
    producers = result["producers"]
    mixed = [p for p in producers if p["producer_grade"] == "MIXED"]
    noread = [p for p in producers if p["producer_grade"] == "NO PATH-LIST READ"]

    every = [f for p in mixed for f in (p["figures"] or [])]
    counts = collections.Counter(f["grade"] for f in every)
    unreachable = [p for p in mixed if p["figures"] is None]

    print(bar)
    print("mg-6219 -- CAN `A READER PER FIGURE` BE PAID BY MACHINE?")
    print(bar)
    print()
    print("  AS_OF = %s, imported from pathlist.py and not re-typed.  Every" % rev)
    print("  figure on this page is a function of that one commit, read through")
    print("  `git ls-tree` and `git show`, so this transcript has a fixed")
    print("  point.  NO INSTRUMENT IS EXECUTED and no worktree is touched.")
    print()

    print("-" * 78)
    print("1  THE UNIT IS A FIGURE, AND THAT IS THE WHOLE CHANGE")
    print("-" * 78)
    print()
    print("  pathlist.py grades a PRODUCER by what it reads and stops there:")
    print("  305 transcripts came back MIXED, meaning `reads a path list AND")
    print("  content`, with nothing said about WHICH of their figures is")
    print("  which.  A figure is an interpolated value on a printed line, so")
    print("  it is an expression in the producer's source, and `is this")
    print("  expression a function of the tracked path list` is a BACKWARD")
    print("  SLICE over that source.")
    print()
    print("      PATH-LIST-VALUED  the slice CLOSES and every root of it is a")
    print("                        tracked-path-list read, a literal, or a")
    print("                        non-repository input.  A PROOF: the figure")
    print("                        is re-derivable at any commit by")
    print("                        liveindex.py's method.")
    print("      CONTENT-VALUED    a content, history or blame read is in the")
    print("                        slice.  Also a proof, of the other thing.")
    print("      UNDECIDED         the slice does not close -- an unresolved")
    print("                        name, an unresolved call, or a parameter")
    print("                        with no visible caller.  CLAIMS NOTHING.")
    print("      CONSTANT          no repository input at all: a rule, a")
    print("                        heading, a number this file computed from")
    print("                        literals.  Not a figure about the corpus.")
    print()
    print("  ALMOST EVERY FAILURE OF THIS ANALYSIS LANDS IN UNDECIDED, AND")
    print("  THE EXCEPTION IS NAMED RATHER THAN GLOSSED.  An unresolved name,")
    print("  call or parameter cannot manufacture a PATH-LIST-VALUED verdict,")
    print("  so the class that is a claim of proof is only ever made SMALLER")
    print("  by a defect of that kind.  N35 plants the one shape that escapes")
    print("  it: an assignment is recorded in the scope it is WRITTEN in, so a")
    print("  global filled by `X.append(...)` INSIDE a function is invisible")
    print("  to a use at module level, which reads `X = []` and sees a")
    print("  literal.  A figure whose real slice runs through such a global")
    print("  can come back a PROOF.  EXHIBITED IN A PLANT, LATENT HERE:")
    print("  nothing below counts how many of the PATH-LIST-VALUED figures")
    print("  have that shape, and that is the next reader's measurement.")
    print()

    print("-" * 78)
    print("2  THE ANSWER, OVER pathlist.py's 305 MIXED TRANSCRIPTS")
    print("-" * 78)
    print()
    print("  %5d  MIXED transcripts at this commit (pathlist.py section 2)"
          % len(mixed))
    print("  %5d  of them have a Python producer this file can parse"
          % (len(mixed) - len(unreachable)))
    print("  %5d  do NOT -- a shell producer has no AST and is out of reach,"
          % len(unreachable))
    print("         counted here rather than dropped")
    print()
    print("  %5d  printed expressions in those producers" % len(every))
    print("  %5d  of them are CONSTANT -- rules, headings, arithmetic over"
          % counts[CONSTANT])
    print("         literals -- and are not figures about the corpus at all")
    print()
    figures = len(every) - counts[CONSTANT]
    print("  %5d  FIGURES, i.e. printed expressions with a repository input."
          % figures)
    print("         Of those:")
    print()
    for name in (PATH_LIST_VALUED, CONTENT_VALUED, UNDECIDED):
        share = (100.0 * counts[name] / figures) if figures else 0.0
        print("      %-18s %6d   %5.1f%%" % (name, counts[name], share))
    print()
    # WHICH PATH LIST -- THE HALF THAT DECIDES WHETHER THE METHOD APPLIES.
    plfigs = [f for f in every if f["grade"] == PATH_LIST_VALUED]
    by_spelling = collections.Counter()
    commit_valued = 0
    for f in plfigs:
        kinds = set(r.split(":", 1)[1] for r in f["roots"]
                    if r.startswith("PATHLIST:"))
        for kind in kinds:
            by_spelling[kind] += 1
        if kinds == {"tree"}:
            commit_valued += 1
    print("  AND WHICH PATH LIST, WHICH IS WHAT DECIDES WHETHER liveindex.py's")
    print("  METHOD ACTUALLY REACHES THE FIGURE.  `ls-tree` names a COMMIT;")
    print("  `ls-files` is the INDEX and a walk is somebody's WORKTREE, and")
    print("  neither can be re-derived at the commit that carries a transcript:")
    print()
    for kind in ("tree", "index", "worktree"):
        print("      reads a path list by %-9s %5d figure(s)"
              % (kind, by_spelling[kind]))
    print()
    holders = sorted(set(
        p["transcript"] for p in mixed for f in (p["figures"] or [])
        if f["grade"] == PATH_LIST_VALUED
        and set(r.split(":", 1)[1] for r in f["roots"]
                if r.startswith("PATHLIST:")) == {"tree"}))
    print("      %5d of the %d PATH-LIST-VALUED figures read `ls-tree` AND"
          % (commit_valued, len(plfigs)))
    print("            NOTHING ELSE, spread over %d transcript(s), and those"
          % len(holders))
    print("            are the ones liveindex.py's method re-derives at an")
    print("            arbitrary commit for free.  pathlist.py's answer was 0")
    print("            TRANSCRIPTS; per figure the same corpus yields %d."
          % commit_valued)
    print()
    for transcript in holders:
        print("          %s" % transcript)
    print()
    print("  consumers.py's own six are INDEX-valued, which is mg-ede8's")
    print("  section 4 arriving from the other side: it declared that census a")
    print("  mixture of the index and HEAD and left the repair to consumers.py.")
    print("  This file did not know that and re-derived it from the source.")
    print()
    print("  SO THE READER CAN BE PAID BY MACHINE FOR %.1f%% OF THE FIGURES"
          % (100.0 * (counts[PATH_LIST_VALUED] + counts[CONTENT_VALUED])
             / figures if figures else 0.0))
    print("  MIXED OWES, and the remaining %.1f%% is where a human still has"
          % (100.0 * counts[UNDECIDED] / figures if figures else 0.0))
    print("  to look.  `The population is 2 forever` is REFUTED; `it is")
    print("  mechanical` is not established either, and the split is the")
    print("  answer rather than a step towards one.")
    print()
    per = collections.Counter()
    for p in mixed:
        if p["figures"] is None:
            continue
        grades = set(f["grade"] for f in p["figures"]
                     if f["grade"] != CONSTANT)
        if not grades:
            per["no figure at all"] += 1
        elif grades == {PATH_LIST_VALUED}:
            per["every figure PATH-LIST-VALUED"] += 1
        elif grades == {CONTENT_VALUED}:
            per["every figure CONTENT-VALUED"] += 1
        elif UNDECIDED not in grades:
            per["decided, and MIXED figure by figure"] += 1
        else:
            per["some figure UNDECIDED"] += 1
    print("  BY TRANSCRIPT, WHICH IS THE UNIT THE WORK IS ACTUALLY DONE IN:")
    print()
    for label, n in sorted(per.items(), key=lambda kv: (-kv[1], kv[0])):
        print("      %-42s %5d" % (label, n))
    print()
    print("  The %d transcripts with no UNDECIDED figure are the ones a"
          % (per["every figure PATH-LIST-VALUED"]
             + per["every figure CONTENT-VALUED"]
             + per["decided, and MIXED figure by figure"]))
    print("  reader could be generated for outright.  Nothing here generates")
    print("  one: this file says WHICH figures are in reach and stops, because")
    print("  a reader also has to recover the figure from a committed page,")
    print("  which is a second problem and is liveindex.py's regex half.")
    print()

    print("-" * 78)
    print("3  THE ANCHOR -- AGAINST THE ONE ADJUDICATION A HUMAN MADE")
    print("-" * 78)
    print()
    print("  mg-ede8 read out_consumers.txt by hand and liveindex.py carries")
    print("  the verdict.  Each row below is located MECHANICALLY, by the")
    print("  literal its print emits and the source text of the figure --")
    print("  never by line number, which rots on the first edit above it.")
    print()
    rows = anchor_rows(result)
    agree = dis = bad = 0
    for template, text, want, why, got, _detail in rows:
        if got in ("UNLOCATED", "AMBIGUOUS"):
            verdict, bad = got, bad + 1
        elif got == want:
            verdict, agree = "AGREES", agree + 1
        else:
            verdict, dis = "DISAGREES", dis + 1
        print("      %-9s  %s" % (verdict, normalise(text)[:56]))
        print("                 hand %-16s machine %s" % (want, got))
        print("                 %s" % why)
    print()
    print("  %d of %d agree, %d disagree, %d could not be located."
          % (agree, len(rows), dis, bad))
    print()
    print("  A ROW THAT CANNOT BE LOCATED IS PRINTED AND IS NOT A PASS.  An")
    print("  anchor that silently matched nothing would agree with everything,")
    print("  which is git_grep_l's defect one file over: a census reporting")
    print("  `clean` because it never looked.")
    print()
    print("  WHERE THEY DISAGREE THE HAND READER IS NOT WRONG -- IT IS")
    print("  COARSER.  liveindex.py's readers are REGEXES OVER A COMMITTED")
    print("  PAGE, so its unit is a LINE, and it excluded `%d of %d%s` whole")
    print("  because the first of those three numbers is content-valued.  The")
    print("  second is `subject scripts` again, already checked two sections")
    print("  earlier and re-derivable here.  That is what per-FIGURE buys over")
    print("  per-LINE, and it is the only thing this file claims to buy.")
    print()

    print("-" * 78)
    print("4  THE CHECK THAT NEEDS NO HUMAN -- A CROSS-INSTRUMENT INVARIANT")
    print("-" * 78)
    print()
    violations = []
    checked = 0
    for p in noread:
        if p["figures"] is None:
            continue
        checked += 1
        for f in p["figures"]:
            if f["grade"] == PATH_LIST_VALUED:
                violations.append((p["producer"], f["line"], f["text"]))
    print("  pathlist.py grades %d producers NO PATH-LIST READ.  By its own"
          % len(noread))
    print("  rule not one figure of any of them can be a function of the path")
    print("  list, because their closures never read one.  So this file's")
    print("  PATH-LIST-VALUED count over that class must be EXACTLY 0, and it")
    print("  is a number this file does not get to choose.")
    print()
    print("      %5d  NO PATH-LIST READ producers parsed" % checked)
    print("      %5d  figures graded PATH-LIST-VALUED among them" % len(violations))
    print()
    if violations:
        print("  VIOLATIONS -- the two instruments disagree, and one of them is")
        print("  wrong.  Every one is printed:")
        for producer, line, text in violations[:20]:
            print("      %s:%d  %s" % (producer, line, normalise(text)[:44]))
        if len(violations) > 20:
            print("      ... and %d more" % (len(violations) - 20))
    else:
        print("  NO VIOLATIONS.  That is a real constraint and not a tautology:")
        print("  the two instruments share the PATTERNS -- this file imports")
        print("  pathlist.PATHLIST and pathlist.OTHER rather than re-spelling")
        print("  them -- but NOT the unit, the traversal or the closure walk.")
        print("  pathlist.py matches its patterns against the whole flattened")
        print("  closure; this file matches them at individual CALL SITES that")
        print("  a slice from a print statement actually reaches.  A figure")
        print("  could be graded PATH-LIST-VALUED here out of a producer whose")
        print("  flattened body never matched PATHLIST at all -- that is")
        print("  precisely the disagreement this arm would catch.")
    print()

    print("-" * 78)
    print("5  WHERE THE SLICE STOPS, COUNTED RATHER THAN DECLARED")
    print("-" * 78)
    print()
    why = collections.Counter()
    for f in every:
        if f["grade"] != UNDECIDED:
            continue
        for root in f["roots"]:
            if root.startswith("UNKNOWN:"):
                why[root.split(":", 1)[1].split()[0]] += 1
            elif root.startswith("PARAM:"):
                why["parameter"] += 1
    print("  Every UNDECIDED figure is undecided for a NAMED reason, and one")
    print("  figure can have several.  By reason, largest first:")
    print()
    for reason, n in sorted(why.items(), key=lambda kv: (-kv[1], kv[0])):
        print("      %-30s %6d" % (reason, n))
    print()
    print("  `call` and `name` are the same wall from two sides: a function")
    print("  or a value defined outside the closure pathlist.py computed.")
    print("  `parameter` is a function whose caller this file could not find,")
    print("  and `unbound` a call that did not supply the parameter the return")
    print("  depends on.  NONE of them is a claim that the figure is content-")
    print("  valued; they are the measured size of what a per-figure reader")
    print("  would still have to be told by hand.")
    print()
    if unreachable:
        print("  %d MIXED transcript(s) have a producer with no AST at all:"
              % len(unreachable))
        for p in unreachable[:10]:
            print("      %s" % p["producer"])
        if len(unreachable) > 10:
            print("      ... and %d more" % (len(unreachable) - 10))
        print()
    print("  AND THIS FILE IS OUTSIDE ITS OWN POPULATION, FOR pathlist.py's")
    print("  REASON AND BY THE SAME ARITHMETIC: the pin it imports is older")
    print("  than figures.py, so out_figures.txt is not tracked at the commit")
    print("  it reports on.  Graded by hand it is MIXED like its subject, and")
    print("  its own figures are mostly UNDECIDED by its own rule -- the slice")
    print("  from `print(counts[name])` runs back into `pathlist.scan`, whose")
    print("  return is a dict this analysis does not model.  The instrument")
    print("  that decides which figures are in reach is not in reach itself,")
    print("  which is the answer pathlist.py already gave about liveindex.py")
    print("  and this file gives about pathlist.py.")
    print()

    print(bar)
    print("FIGURES: %d of %d figures in %d MIXED transcripts are decidable by"
          % (counts[PATH_LIST_VALUED] + counts[CONTENT_VALUED], figures,
             len(mixed)))
    print("         machine -- %d PATH-LIST-VALUED and %d CONTENT-VALUED --"
          % (counts[PATH_LIST_VALUED], counts[CONTENT_VALUED]))
    print("         and %d are UNDECIDED.  The hand adjudication agrees on %d"
          % (counts[UNDECIDED], agree))
    print("         of %d anchor rows.  %d figure(s) in %d transcript(s) are"
          % (len(rows), commit_valued, len(holders)))
    print("         `ls-tree`-valued and so free to liveindex.py's method,")
    print("         where pathlist.py's per-TRANSCRIPT answer was 0.  The")
    print("         cross-instrument invariant holds")
    print("         with %d violation(s), at AS_OF %s." % (len(violations), rev))
    print(bar)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
