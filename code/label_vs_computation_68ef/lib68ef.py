"""Machinery for `mg-68ef` -- can a check compare what a table HEADER claims against what the
arm beneath it COMPUTES?

`mg-9d9e` corrected two of its own prose defects by re-reading rather than by a control, and named
the class: *a mislabelled column that prints the right number*.  The carry-forward asks whether a
label-vs-computation check is buildable at all.  This file is the attempt, and its shape is the
answer: it is buildable for ONE of the two exhibits and provably not for the other.

NOTHING HERE IS IMPORTED FROM `code/`.  Every predicate under study belongs to this directory; the
two exhibits are READ OUT OF THE TREE at their own commits and never re-typed (`mg-d2c2`).

⚠️ EVERY FIGURE IS A FUNCTION OF ONE COMMIT.  Arms read `AS_OF` through `git show`, never the
worktree, with one declared exemption: the reflexive scan of `SELF_DIR`, which must read the
worktree because this directory is younger than the pin.  That exemption is arithmetic and not a
rule, and the arm that takes it says so at the section.
"""

import ast
import os
import re
import subprocess

# --------------------------------------------------------------------------------- the pin

AS_OF = "5ffb22e558b185f20628873848c549eed78a9780"

#: `p9d9e`'s own commit -- the exhibit BEFORE its correction.  The correction landed at `e9432cd`.
PRE_CORRECTION = "3561300f3d87c34440730e9de27574a48b9da326"

#: The two exhibits, by path.  Both are read out of the tree at both revisions.
EXHIBIT_B = "code/lstar_code_9d9e/s1_run_the_test.py"   # the mislabelled COLUMN
EXHIBIT_A = "code/lstar_code_9d9e/lib9d9e.py"           # the mislabelled COMPLEXITY

SELF_DIR = "code/label_vs_computation_68ef"


class Refused(Exception):
    """Raised rather than answering.  An instrument that cannot resolve its own inputs must say
    so; a zero returned by a broken walk is indistinguishable from a zero that is true."""


#: The repository root, derived from THIS FILE's location rather than from the process's working
#: directory.
#:
#: ⚠️ THIS WAS A DEFECT IN THIS INSTRUMENT AND IT IS FIXED HERE RATHER THAN DESCRIBED.  `git
#: ls-tree -r --name-only <rev>` run from a SUBDIRECTORY lists only that subdirectory's subtree,
#: so the corpus population silently fell from 1 252 files to this directory's own three the
#: moment `run_all.sh` did its `cd` -- the exact shape m1.0 exists to catch, arriving inside the
#: instrument that prints m1.0.  Every git call is anchored to `ROOT` and the tree walk is
#: `--full-tree`, so no figure here is a function of where the arm was started.
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def git(*args):
    p = subprocess.run(["git", "-C", ROOT] + list(args), capture_output=True, text=True)
    if p.returncode != 0:
        raise Refused("git %s failed: %s" % (" ".join(args), p.stderr.strip()[:200]))
    return p.stdout


def resolve(rev):
    """Full sha of `rev`, refusing rather than guessing."""
    return git("rev-parse", "--verify", "%s^{commit}" % rev).strip()


def show(rev, path):
    return git("show", "%s:%s" % (rev, path))


def tracked_py(rev):
    return sorted(p for p in git("ls-tree", "-r", "--full-tree", "--name-only", rev).splitlines()
                  if p.endswith(".py"))


def show_many(rev, paths):
    """`{path: source}` for many paths in ONE `git cat-file --batch`.

    Identical content to calling `show` per path -- `m0` asserts that on a sample rather than
    trusting it -- and about fifty times faster, which is what makes a suite over 1 252 files
    cheap enough to run twice and compare byte for byte.
    """
    if not paths:
        return {}
    stdin = "".join("%s:%s\n" % (rev, p) for p in paths)
    p = subprocess.run(["git", "-C", ROOT, "cat-file", "--batch"],
                       input=stdin.encode(), capture_output=True)
    if p.returncode != 0:
        raise Refused("git cat-file --batch failed: %s" % p.stderr.decode()[:200])
    out, buf, i = {}, p.stdout, 0
    for path in paths:
        nl = buf.index(b"\n", i)
        header = buf[i:nl].decode()
        parts = header.split()
        if len(parts) != 3 or parts[1] != "blob":
            raise Refused("cat-file refused %s at %s: %r" % (path, rev, header))
        size = int(parts[2])
        out[path] = buf[nl + 1:nl + 1 + size].decode("utf-8", "replace")
        i = nl + 1 + size + 1
    return out


# ------------------------------------------------------------------------- what a formula is

#: A column label is FORMULA-SHAPED if it carries an operator BETWEEN SYMBOLS.  The `-` case is
#: deliberately narrow: `shape-A`, `MERGE-P` and `exact-index` are hyphenated WORDS, not
#: subtractions, and a matcher that read them as arithmetic would inflate every population below
#: with English.  So `-` counts only with a digit on its left (`1-c`) or with space on both sides.
FORMULA = re.compile(
    r"[\w)\]]\s*[*/^]\s*[\w(\[]"      # a*b, E/(n ...), n^2
    r"|\)\s*\("                        # )( -- juxtaposed product
    r"|\d\s*\("                        # 0.9399(a+b)
    r"|[\w)\]]\s*\+\s*[\w(\[]"         # a+b, a + b
    r"|\d\s*-\s*[\w(\[]"               # 1-c
    r"|[\w)\]]\s+-\s+[\w(\[]"          # a - b
)

#: THE SAME RULE WITH THE JUXTAPOSITION CLAUSE BOUNDED TO ONE SPACE.
#:
#: ⚠️ THIS WAS WRITTEN AFTER SEEING WHAT `FORMULA` FOUND, AND THAT IS SAID HERE RATHER THAN LEFT
#: TO BE NOTICED.  `FORMULA`'s only hit in the whole estate was `n=6   (non-chain posets ...)`, a
#: column label whose PADDING before a parenthesis reads as a juxtaposed product under `\d\s*\(`.
#: Both spellings ship and both are reported, so the reader can see what the repair costs instead
#: of being handed the number the tighter rule happens to give.
FORMULA_TIGHT = re.compile(
    r"[\w)\]]\s*[*/^]\s*[\w(\[]"
    r"|\)\s*\("
    r"|\d\s?\("                        # 0.9399(a+b) and `0.9399 (a+b)`, but not `6   (`
    r"|[\w)\]]\s*\+\s*[\w(\[]"
    r"|\d\s*-\s*[\w(\[]"
    r"|[\w)\]]\s+-\s+[\w(\[]"
)

#: A bare numeric literal: a digit run not glued to an identifier.  This is what keeps `log2 n!`
#: from contributing a `2` -- the digit there is part of a NAME, and a rule that counted it would
#: report a disagreement on every base-2 logarithm in the estate.
NUMLIT = re.compile(r"(?<![\w.])\d+(?:\.\d+)?(?![\w])")

#: A `%`-format placeholder.
PCT = re.compile(r"%[-# +0-9.*]*[diouxXeEfFgGcrsa]")

#: A rule line: the `---+---` shape this estate writes under a table header.
RULE = re.compile(r"^[\s|+-]*$")


def is_rule(s):
    return "+" in s and s.count("-") >= 3 and RULE.match(s) is not None


def formula_shaped(label, tight=False):
    rx = FORMULA_TIGHT if tight else FORMULA
    return bool(rx.search(label)) and bool(re.search(r"[A-Za-z]", label))


def label_literals(label):
    return sorted({float(m.group(0)) for m in NUMLIT.finditer(label)})


def expr_literals(node):
    """Every numeric literal reachable in `node`."""
    out = set()
    for sub in ast.walk(node):
        if isinstance(sub, ast.Constant) and isinstance(sub.value, (int, float)) \
                and not isinstance(sub.value, bool):
            out.add(float(sub.value))
    return sorted(out)


# ------------------------------------------------------------------------- table extraction

class Table(object):
    """A rule line, the header above it, and the `%`-format row template below it."""

    def __init__(self, path, lineno, header, rule, shift, cols, naive_cols):
        self.path = path
        self.lineno = lineno
        self.header = header
        self.rule = rule
        self.shift = shift
        self.cols = cols                # segmented by the rule line under `shift`
        self.naive_cols = naive_cols    # segmented by splitting the header on `|`
        self.row_template = None
        self.args = []                  # one expression per placeholder, or []
        self.scope = None

    @property
    def paired(self):
        return self.row_template is not None and len(self.args) == len(self.cols)

    @property
    def segmentation_disagrees(self):
        return len(self.cols) != len(self.naive_cols)


def _string_constants(tree):
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            out.append((node.lineno, node.value, node))
    out.sort(key=lambda t: (t[0], t[1]))
    return out


def _best_shift(rule, header, span=3):
    """The integer offset that best aligns the rule's `+` columns with the header's `|` columns.

    ⚠️ THIS SEARCH IS NOT COSMETIC AND WAS NOT IN THE FIRST DRAFT.  Two of the seven tables in
    `s1_run_the_test.py` carry their rule line ONE CHARACTER LEFT of their header, in the source
    and in the committed transcript both, so a segmenter that took the `+` columns literally would
    hand every one of those labels a stray leading `|` and mis-segment a real table silently.
    """
    plus = [i for i, ch in enumerate(rule) if ch == "+"]
    bars = {i for i, ch in enumerate(header) if ch == "|"}
    if not plus:
        return 0, 0
    best, best_hits = 0, -1
    for d in range(-span, span + 1):
        hits = sum(1 for i in plus if i + d in bars)
        # prefer the smaller |shift| on a tie, so a table that is already aligned stays at 0
        if hits > best_hits or (hits == best_hits and abs(d) < abs(best)):
            best, best_hits = d, hits
    return best, best_hits


def _segment(header, rule, shift):
    bounds = [i + shift for i in range(len(rule)) if rule[i] == "+"]
    segs, prev = [], 0
    for b in bounds:
        segs.append(header[prev:b])
        prev = b + 1
    segs.append(header[prev:])
    return [s.strip() for s in segs]


def find_tables(path, src, header_window=6, row_window=30):
    """Every table in `src`.  A table needs a rule line AND a header; anything else is not one."""
    try:
        tree = ast.parse(src)
    except SyntaxError:
        raise Refused("cannot parse %s" % path)

    strs = _string_constants(tree)
    tables = []
    for idx, (ln, s, node) in enumerate(strs):
        if not is_rule(s):
            continue
        header = None
        for ln2, s2, _ in reversed(strs[:idx]):
            if ln - ln2 > header_window:
                break
            if "|" in s2 and not PCT.search(s2) and not is_rule(s2):
                header = s2
                break
        if header is None:
            continue
        shift, _hits = _best_shift(s, header)
        cols = _segment(header, s, shift)
        naive = [x.strip() for x in header.split("|")]
        t = Table(path, ln, header, s, shift, cols, naive)
        _attach_row(t, tree, strs, idx, row_window)
        tables.append(t)
    return tables


def _attach_row(t, tree, strs, idx, row_window):
    """Find the `%`-format row template under the rule line and read its argument expressions.

    Pairing is by INDEX and requires the placeholder count to equal the column count.  A row that
    spends two placeholders on one column is left UNPAIRED rather than guessed at -- a guessed
    alignment is exactly the defect this directory is about, arriving inside the instrument.
    """
    mods = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod) \
                and isinstance(node.left, ast.Constant) and isinstance(node.left.value, str):
            mods.setdefault(id(node.left), node)

    for ln2, s2, node2 in strs:
        if ln2 <= t.lineno or ln2 - t.lineno > row_window:
            continue
        if not PCT.search(s2) or "|" not in s2:
            continue
        n_ph = len(PCT.findall(s2))
        if n_ph != len(t.cols):
            continue
        mod = mods.get(id(node2))
        if mod is None:
            continue
        right = mod.right
        args = list(right.elts) if isinstance(right, ast.Tuple) else [right]
        if len(args) != n_ph:
            continue
        t.row_template = s2
        t.args = args
        return


# ------------------------------------------------------------- resolving one step of local state

def local_assignments(tree):
    """`name -> value expression` for every single-target assignment, last one wins.

    ONE STEP ONLY, and that is declared rather than hidden: `ceil_ = 0.9399 * size * k` resolves,
    `ceil_ = f(x)` does not, and the second returns NOT ADJUDICABLE instead of a pass.
    """
    out = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name):
            out[node.targets[0].id] = node.value
    return out


AGREE, DISAGREE, NOT_ADJUDICABLE = "AGREE", "DISAGREE", "NOT ADJUDICABLE"


def adjudicate(label, expr, assigns):
    """The narrow rule: every numeric literal the LABEL names must appear in the COMPUTATION.

    ⚠️ THIS JUDGES LITERALS AND NOT ALGEBRA.  It cannot tell `(1-c)(a+b)` from `c(a+b)` by
    reasoning; it tells them apart because the corrected label spells `0.9399` and the wrong one
    spells `1`, and only one of those is in the expression.  Every other label in the estate comes
    back NOT ADJUDICABLE, which is a verdict and not a pass.
    """
    lits = label_literals(label)
    if not lits:
        return NOT_ADJUDICABLE, [], []
    node = expr
    if isinstance(expr, ast.Name) and expr.id in assigns:
        node = assigns[expr.id]
    elits = expr_literals(node)
    if not elits:
        return NOT_ADJUDICABLE, lits, elits
    missing = [x for x in lits if not any(abs(x - y) < 1e-12 for y in elits)]
    return (DISAGREE if missing else AGREE), lits, elits


# ------------------------------------------------------- the OTHER half: the complexity claim

BIGO = re.compile(r"\bO\(([^()]*(?:\([^()]*\)[^()]*)*)\)")


def bigo_claims(path, src):
    """`O(...)` claims in docstrings, with the enclosing definition."""
    try:
        tree = ast.parse(src)
    except SyntaxError:
        raise Refused("cannot parse %s" % path)
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        doc = ast.get_docstring(node)
        if not doc:
            continue
        name = getattr(node, "name", "<module>")
        for m in BIGO.finditer(doc):
            out.append((path, name, m.group(0), m.group(1), node))
    return out


def claimed_rank(inner):
    """How many nested dimensions an `O(...)` argument claims, or `None` where the question does
    not apply.

    `O(a*b)` is 2.  `O(a*b*(a+b))` is 3.  `O(n^3)` is 3.  `O(1)` is 0.  `O(2^n)`, `O(n!)`,
    `O(1/n)` and `O(n^-2)` are `None` -- they are not polynomial nesting claims at all and ranking
    them would manufacture a population.
    """
    s = inner.strip()
    if "!" in s or "/" in s or re.search(r"\^\s*-", s) or re.search(r"\d\s*\^", s):
        return None
    if s in ("1", ""):
        return 0
    total = 0
    for factor in re.split(r"\*(?!\*)", s.replace("**", "^")):
        f = factor.strip().strip("()")
        if not f:
            continue
        m = re.search(r"\^\s*(\d+)", f)
        if m:
            total += int(m.group(1))
        else:
            # `2^n n` style products written with a space, e.g. `2^n n`
            total += max(1, len([w for w in re.split(r"\s+", f) if w]))
    return total or None


def loop_depth(node):
    """The syntactic loop-nesting depth of a definition: the deepest chain of `for`/`while`/
    comprehension generators, counting nested definitions.

    THIS IS THE PROXY, AND IT IS OFFERED IN ORDER TO BE REFUTED.  It is the only thing a matcher
    can see about cost without executing anything, and `feasible_merges` is the demonstration that
    what it sees is not the cost: the recursion there is memoised, so its two dimensions are in the
    memo key rather than in any `for`, and the one comprehension the proxy CAN see is the rescan
    that the corrected claim's third factor is about.
    """
    def walk(n, depth):
        best = depth
        for child in ast.iter_child_nodes(n):
            if isinstance(child, (ast.For, ast.AsyncFor, ast.While)):
                best = max(best, walk(child, depth + 1))
            elif isinstance(child, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
                best = max(best, walk(child, depth + len(child.generators)))
            else:
                best = max(best, walk(child, depth))
        return best
    return walk(node, 0)


# ------------------------------------------------------------------------------- the reporter

class Report(object):
    """A deterministic transcript.  NO CLOCK AND NO RANDOMNESS ANYWHERE: every figure is a
    function of the pin, so two consecutive runs are byte-identical."""

    def __init__(self, title):
        self.rows = []
        self.bad = 0
        self.checks = 0
        self.line("=" * 96)
        self.line(title)
        self.line("=" * 96)

    def line(self, s=""):
        self.rows.append(s)

    def note(self, s):
        self.rows.append("       " + s)

    def banner(self, s):
        self.line()
        self.line("-" * 96)
        self.line(s)
        self.line("-" * 96)
        self.line()

    def verdict(self, ok, claim, why=""):
        self.checks += 1
        if not ok:
            self.bad += 1
        self.line("   %s  %s" % ("OK    " if ok else "FAILED", claim))
        if why:
            self.note(why)
        return ok

    def caught(self, ok, claim, why=""):
        """A PLANT world: `CAUGHT` means the planted defect WAS detected, which is the passing
        outcome.  Kept separate from `verdict` on purpose -- `mg-9876`'s a4 counts a directory as
        recording a demonstrated failure when a committed transcript carries one of seven
        \\b-anchored red tokens, and `CAUGHT` is one of them, so the word must be printed by a live
        plant rather than only appearing in a banner."""
        self.checks += 1
        if not ok:
            self.bad += 1
        self.line("   %s  %s" % ("CAUGHT" if ok else "MISSED", claim))
        if why:
            self.note(why)
        return ok

    def render(self):
        return "\n".join(self.rows) + "\n"

    def done(self, path=None):
        self.line()
        self.line("=" * 96)
        self.line("   %d check(s), %d failed" % (self.checks, self.bad))
        self.line("=" * 96)
        text = self.render()
        if path:
            with open(path, "w") as fh:
                fh.write(text)
        return text
