"""mg-9160 -- the instrument for THE CLASSIFIER'S ARITY, and for the population
rule one layer down.

WHAT THIS FILE MAY AND MAY NOT CONTAIN, GIVEN WHAT IT IS ABOUT.  The subject is
a classifier that collapses distinctions because its value set is too small,
inside a population rule that never sees 626 of the integers it ranges over.
A library for that may not become a fourth copy of anything, and it may not
quietly re-implement the rules whose behaviour it is measuring -- a measurement
of `_classify` taken with a re-typed `_classify` measures the typing.  So:

  IMPORTED, NEVER RESTATED.
    `lib56dc`  -- `_classify`, `EXEC_WORDS`, `SITE_WORDS`, `count_rows`,
                  `grain_of`, `HEADER_LOOKBACK`.  THE SUBJECT.  Every number
                  this tree prints about the old classifier is taken by
                  CALLING it.
    `lib03d1`  -- `grain_nouns`, `singular` (the shape extractor A1d's 400
                  comes from), `embedded_counts` (the rule that finds the 626),
                  `all_transcripts` (the corpus the ticket's figures range
                  over), `read`, `git`, `head`.  Importing the parent's
                  population rather than re-deriving it is what makes a
                  disagreement between us a disagreement about the FINDING and
                  not about which files we globbed.

  WRITTEN HERE, AND WHY EACH IS NOT A COPY.

    `min_collapse`      the ARITY FLOOR: fewest pairs any k-valued function can
                        collapse over n words.  Nothing in the arc computes it,
                        and it is the whole of the correction -- the ticket
                        asserts a CAUSE and a cause is a decomposition.
    `collapse`          pair separation counted BY RUNNING a classifier over
                        every pair, not by the arithmetic `C(n,2) - |S|*|E|`
                        that A1c uses.  The arithmetic is right only if every
                        vocabulary word lands in its own list, which is a
                        property A1c prints but does not check.
    `two_test`          a classifier of EXACTLY `_classify`'s form -- two
                        membership sets, four symbols -- over word sets given
                        as an ARGUMENT.  This is what makes `four values leave
                        room for six distinctions` an exhibit rather than a
                        claim: the counterexample runs in the same shape as the
                        thing it refutes.
    `chromatic`         fewest colours for a must-separate graph, brute force
                        over a graph with eleven vertices.
    `count_items`       THE REPAIRED POPULATION.  One row per INTEGER, not one
                        per LINE.  Composes `lib56dc.count_rows` and
                        `lib03d1.embedded_counts`; re-implements neither.
    `attribute`         which noun an integer inside a label belongs to.  This
                        is the one place I disagree with the parent's rule
                        rather than composing it, and the disagreement is
                        printed row by row in `s3_population.py`.
    `grain_open`        the OPEN-SET classifier: the grain is the NOUN, and the
                        no-entry case names the word instead of returning a
                        symbol that means `no`.
    `verdict`           SAME / DIFFERENT / UNADJUDICATED.  The third verdict is
                        the actual repair; see the note on it below.

THE SELF-RULE THIS TREE DOES **NOT** ADOPT, AND WHY.  `lib03d1.row()` requires
every label of that tree to classify at stage `label` under `lib56dc.grain_of`,
and mg-03d1's own AS3 records what that cost: *my subject is grain distinctions
the classifier has no word for, and to pass my own check I must describe them
using only words it does.*  Adopting that rule here would oblige me to write
about the 370 words it has no entry for using only the 43 it does.  So `row()`
below checks the label against MY OWN extractor and PRINTS THE NOUN it found,
which is a weaker check in one respect -- it cannot fail on vocabulary, because
its vocabulary is open -- and that weakness is stated rather than hidden.
"""

import os
import re
import subprocess
import sys
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

for _p in ("code/runner_exit_audit_56dc", "code/runner_exit_repair_70c7",
           "code/runner_exit_repair_7522", "code/grain_axis_audit_03d1"):
    sys.path.insert(0, os.path.join(REPO, _p))

import lib56dc as A            # noqa: E402  THE SUBJECT
import lib03d1 as B            # noqa: E402  the parent audit's extractor

TREE = "code/grain_arity_9160"
PARENT = "code/grain_axis_audit_03d1"
PARENT_REV = "9f1ecaa"         # the commit mg-03d1's own transcripts print as
                               # HEAD.  Its corpus figures are AT THIS REF.

read = B.read
git = B.git
head = B.head


# ---------------------------------------------------------------------------
# OUTPUT.  Borrowed where it is already identical in four libraries of this
# arc; `row()` is this tree's own because its CHECK differs.
# ---------------------------------------------------------------------------

bar = A.bar
finding = A.finding


def hdr(t):
    print()
    print("=" * 74)
    print(t)
    print("=" * 74)
    print()


_NO_NOUN = []


def row(label, value, grain=None, indent=6):
    """One count row, with the grain noun MY extractor reads off its label.

    `grain` is what one unit of the value IS, stated by the caller.  The noun
    printed in brackets is what the label's own words say, read by
    `grain_open`.  When the two differ the reader can see it -- which is the
    defect this whole arc is about, made visible instead of asserted away.
    """
    kind, noun = grain_open(label)
    if kind != "WORD":
        _NO_NOUN.append(label)
    print("%s%-54s %8s" % (" " * indent, label, value))
    print("%s    ^ one unit is one %s;  label's own noun: %s"
          % (" " * indent, grain if grain else "?",
             ("`%s`" % noun) if kind == "WORD" else "NO NOUN EXTRACTED"))


def labels_without_noun():
    return list(_NO_NOUN)


def pop(text, indent=2):
    print("%spopulation: %s" % (" " * indent, text))


# ---------------------------------------------------------------------------
# THE CORPUS.  The parent's, by import, plus the same set AT A REF -- because
# the corpus grows and every figure in the ticket was measured at 9f1ecaa.
# ---------------------------------------------------------------------------

_OUT = re.compile(r"^code/[^/]+/out_[^/]*\.txt$")


def corpus(ref=None):
    """[path] -- every `code/*/out_*.txt`, sorted.

    GRAIN: one item per FILE.  `ref=None` is the parent's own on-disk glob, by
    import.  `ref` given goes through the index, which is the only way to ask
    what the corpus WAS -- and the ticket's 517 / 1191 / 400 / 626 are all
    figures about what it was.
    """
    if ref is None:
        return B.all_transcripts()
    return sorted(p for p in git("ls-tree", "-r", "--name-only",
                                 ref).splitlines() if _OUT.match(p.strip()))


PARENT_PUB = "eacc5e1"         # the commit that published mg-03d1's transcripts


def parent_corpus():
    """[(path, ref)] -- the corpus AS IT WAS ON DISK while mg-03d1 ran.

    NOT `corpus(PARENT_REV)`, and the difference is the whole of P7.  mg-03d1
    globbed the DISK, and on the run that writes them a tree's own transcripts
    are untracked -- `lib56dc.outs()` says so in its own docstring.  So the
    corpus its figures range over is

        everything tracked at 9f1ecaa   +   mg-03d1's own seven transcripts

    and neither ref alone reproduces it.  A figure whose population is `the
    disk at the moment of the run` is reproducible only by reconstruction, and
    saying which two refs the reconstruction takes is the difference between a
    reproduction and a coincidence.
    """
    return ([(p, PARENT_REV) for p in corpus(PARENT_REV)]
            + [(p, PARENT_PUB) for p in corpus(PARENT_PUB)
               if p.startswith(PARENT + "/")])


# ---------------------------------------------------------------------------
# PAIR SEPARATION, AND THE ARITY FLOOR.
# ---------------------------------------------------------------------------

def collapse(fn, words):
    """(pairs, separated, collapsed) for a classifier over a word list.

    GRAIN: one unit of each number is one UNORDERED PAIR of words.  Counted by
    CALLING `fn` on every word and comparing symbols over every pair, not by
    the closed form -- the closed form assumes each word lands in its own list,
    which is the thing being measured.
    """
    ws = list(words)
    v = [fn(w) for w in ws]
    n = len(ws)
    sep = sum(1 for i, j in combinations(range(n), 2) if v[i] != v[j])
    return n * (n - 1) // 2, sep, n * (n - 1) // 2 - sep


def blocks(fn, words):
    """{symbol: [word]} -- the partition a classifier induces."""
    out = {}
    for w in words:
        out.setdefault(fn(w), []).append(w)
    return out


def min_collapse(n, k):
    """Fewest pairs ANY k-valued function can collapse over n words.

    A k-valued function is a partition into at most k blocks; a pair is
    collapsed iff both words share a block.  Sum of C(n_i,2) is minimised by
    the most equal partition, because moving one word from a larger block to a
    smaller one changes the total by (n_small) - (n_large - 1) < 0 whenever
    n_large > n_small + 1.  So the minimum is at the balanced split.

    GRAIN: one unit of the return value is one UNORDERED PAIR of words.
    """
    if k <= 0 or n <= 1:
        return n * (n - 1) // 2 if k <= 0 else 0
    q, r = divmod(n, k)
    return r * ((q + 1) * q // 2) + (k - r) * (q * (q - 1) // 2)


def balanced_sets(words, k=4):
    """(exec_set, site_set) placing `words` in a balanced k<=4 partition.

    The four cells of `_classify` are (in EXEC only), (in SITE only), (in
    both), (in neither).  So a function OF EXACTLY `_classify`'S FORM can
    realise any partition into at most four blocks -- which is what makes
    `min_collapse(n, 4)` a FLOOR for this function shape and not merely a bound
    for some other one.  E1 of PREDICTIONS.md is this sentence, and
    `selftest9160.py` exhibits a string classifying `BOTH`.
    """
    ws = list(words)
    cells = [[] for _ in range(k)]
    for i, w in enumerate(ws):
        cells[i % k].append(w)
    ex = set(cells[0]) | (set(cells[2]) if k > 2 else set())
    si = set(cells[1]) | (set(cells[2]) if k > 2 else set())
    return ex, si


def two_test(exec_words, site_words):
    """A classifier of EXACTLY `_classify`'s form over the given word sets.

    Two boolean membership tests, four symbols, same order of cases.  Written
    once here so that every alternative vocabulary in this tree is run through
    the SAME shape as the subject -- an exhibit that changed the shape as well
    as the words would refute nothing.
    """
    ex, si = set(exec_words), set(site_words)

    def f(w):
        e, s = w in ex, w in si
        if e and s:
            return "BOTH"
        if e:
            return "EXECUTION"
        if s:
            return "SITE"
        return "NONE"
    return f


def chromatic(vertices, edges):
    """(k, colouring) -- fewest colours separating every edge, by brute force.

    Edges are MUST-SEPARATE constraints: an axis the classifier is required to
    express.  Eleven vertices, so exhaustive search over k = 1,2,3,... is
    affordable and needs no heuristic anybody has to trust.
    """
    vs = list(vertices)
    for k in range(1, len(vs) + 1):
        for code in range(k ** len(vs)):
            c, x = {}, code
            for v in vs:
                c[v] = x % k
                x //= k
            if all(c[a] != c[b] for a, b in edges):
                return k, c
    return len(vs), {v: i for i, v in enumerate(vs)}


# ---------------------------------------------------------------------------
# THE REPAIRED POPULATION.  ONE ROW PER INTEGER.
# ---------------------------------------------------------------------------

_WORD = re.compile(r"[A-Za-z][A-Za-z-]*")


def attribute(label, span):
    """(prev noun, next noun, verdict) for one integer inside a LABEL.

    THE DISAGREEMENT WITH THE PARENT, STATED WHERE IT HAPPENS.
    `lib03d1.embedded_counts` attaches the word immediately AFTER the integer.
    That is right for the shape

        ...ROWS outside it, across 10 distinct basenames         14      (VALUE NOUN)

    and wrong for the shape this arc's tables actually use as often

        973ca61 OUTSIDE rows   ROWS  10  SITES   9  GAP  1       (NOUN VALUE)

    where the word after `10` is `SITES` -- the noun of the NEXT column's
    value, not of this one.  Attaching it makes `10` a count of sites when the
    label says it is a count of rows: a value attributed to the wrong noun on
    the same line, which is the audited defect run backwards.  mg-03d1 caught
    this once in its own AS1, in the other direction, and repaired `label_grain`
    for it; `embedded_counts` was not repaired with it.

    So this returns BOTH neighbours and a verdict, and never silently picks:

      `NEXT`        only the following word is a word     -> VALUE NOUN shape
      `PREV`        only the preceding word is a word     -> NOUN VALUE shape
      `AMBIGUOUS`   both are                              -> UNRESOLVED, printed
      `NEITHER`     neither is
    """
    before = _WORD.findall(label[:span[0]])
    after = _WORD.findall(label[span[1]:])
    p = before[-1].lower() if before else ""
    n = after[0].lower() if after else ""
    if n and "distinct" == n:
        n = after[1].lower() if len(after) > 1 else ""
    if p and n:
        return p, n, "AMBIGUOUS"
    if n:
        return p, n, "NEXT"
    if p:
        return p, n, "PREV"
    return p, n, "NEITHER"


_TOK = re.compile(r"(?<![\w.:#-])(\d[\d,]*)(?![\w.])|([A-Za-z][A-Za-z-]*)")


def column_shape(label, nums=()):
    """'NOUN-VALUE' | 'VALUE-NOUN' | 'UNDETERMINED' for one count row.

    A SECOND PASS, DESIGNED AFTER LOOKING AT AF2's FIVE ROWS -- said here and
    not in a footnote.  `attribute` returns AMBIGUOUS whenever a word sits on
    both sides of an integer, which is the truthful primary verdict and
    resolves nothing.  This breaks the tie on the shape of the WHOLE row.

    THE DISCRIMINATOR IS STRICT ALTERNATION, not a threshold.  A column table
    in this arc's `NOUN VALUE` convention reads

        973ca61 ALL rows    ROWS  49  SITES  47  GAP  2

    -- from the first integer on, exactly ONE word between consecutive
    integers, and at least one word before the first.  Prose carrying an
    embedded count does not alternate:

        ...ROWS outside it, across 10 distinct basenames         14

    has TWO words between 10 and 14.  So the alternation test separates the two
    conventions without a hand list of table names and without a fitted
    constant -- but it was still WRITTEN after seeing the rows it separates,
    and `s3_population.py` prints how many AMBIGUOUS cases it moves and in
    which direction so a reader can discount it.  It is offered BESIDE the
    primary verdict and never in place of it.
    """
    toks = [("N" if m.group(1) else "W")
            for m in _TOK.finditer("%s  %s" % (label,
                                               "  ".join(str(n) for n in nums)))]
    idx = [i for i, t in enumerate(toks) if t == "N"]
    if len(idx) >= 2 and idx[0] > 0 and toks[idx[0] - 1] == "W" \
            and all(b - a == 2 for a, b in zip(idx, idx[1:])):
        return "NOUN-VALUE"
    if idx and toks[idx[0] + 1:idx[0] + 2] == ["W"]:
        return "VALUE-NOUN"
    return "UNDETERMINED"


_INT = B._INT_IN_LABEL


def count_items(text, lookback=A.HEADER_LOOKBACK):
    """[(line, where, value, noun, verdict, label)] -- ONE ROW PER INTEGER.

    GRAIN: one item per INTEGER printed in a count row -- which is the repair.
    `lib56dc.count_rows` returns one label and one grain per LINE, so an
    integer inside the label is in no population at all (626 of them across the
    corpus) and every trailing integer after the first shares one grain with
    its neighbours (nobody has counted those).  Both are visible here because
    the unit of the population is the integer.

      `where`   `trailing` -- the integer `count_rows` returned
                `label`    -- an integer inside the label, previously unseen
      `noun`    the grain noun this integer's own words give it, from
                `attribute` for label-internal ones and from
                `lib03d1.grain_nouns` for trailing ones
      `verdict` `NEXT`/`PREV`/`AMBIGUOUS`/`NEITHER` for label-internal ones;
                `SOLE` or `SHARED` for trailing ones -- `SHARED` meaning this
                integer is one of several on the line that the old rule gives
                a single grain to.

    WHAT THIS DOES NOT DO.  Being in the population is not being classified
    CORRECTLY.  Whether the noun attached here is the right grain for that
    integer is a fact about the code that printed it, and re-deriving it is
    possible only where a re-derivation sits beside the row.  E6.
    """
    lines = text.splitlines()
    out = []
    for i, label, nums in A.count_rows(text):
        for m in _INT.finditer(label):
            try:
                v = int(m.group(1).replace(",", ""))
            except ValueError:
                continue
            p, n, verdict = attribute(label, m.span(1))
            noun = {"NEXT": n, "PREV": p, "AMBIGUOUS": "%s|%s" % (p, n),
                    "NEITHER": ""}[verdict]
            out.append((i, "label", v, B.singular(noun) if verdict in
                        ("NEXT", "PREV") else noun, verdict, label))
        ns = B.grain_nouns(label)
        noun = B.singular(sorted(ns)[0]) if ns else ""
        for v in nums:
            out.append((i, "trailing", v, noun,
                        "SOLE" if len(nums) == 1 else "SHARED", label))
    del lines, lookback
    return out


# ---------------------------------------------------------------------------
# THE OPEN-SET CLASSIFIER, AND THE THIRD VERDICT.
# ---------------------------------------------------------------------------

def grain_open(label):
    """('WORD', noun) | ('NO-NOUN', label) -- the grain as a NOUN, open set.

    The value set is the set of nouns the corpus uses; it is not fixed by the
    function.  So there is no arity to run out of, and the failure mode is not
    `NONE` -- a symbol that reads as *this label has no grain* -- but
    `NO-NOUN`, which carries the label that defeated the extractor so a reader
    can see WHAT was not classified rather than how many were not.

    AND ITS PRICE, WHICH IS NOT SMALL.  An open value set separates every pair
    of distinct nouns, INCLUDING SYNONYMS.  `steps`/`iterations` are one grain
    and this function calls them two.  It has traded a classifier that
    collapses 623 pairs for one that splits every synonym pair there is.  That
    is not a defect of this implementation, it is D3 of PREDICTIONS.md and it
    is why `verdict` below exists.
    """
    ns = B.grain_nouns(label)
    if not ns:
        return "NO-NOUN", label
    return "WORD", B.singular(sorted(ns)[0])


# ADJUDICATIONS.  Hand judgements, printed rather than folded into a ratio,
# because A1f is right that there is no mechanical test for `same grain` and
# pretending there is would be this arc's own defect.  Every member is
# mg-03d1's A1f verdict, quoted, plus its reason.  NOTHING IS ADDED BY ME:
# extending this table is how the third verdict would become a hand list, and a
# hand list is what `count_rows`' docstring warns against.
SAME_GRAIN = [
    ("step", "iteration",
     "a loop's steps ARE its iterations (A1f)"),
    ("command", "invocation",
     "`3 commands issued` and `3 invocations` count the same events (A1f)"),
]
DIFF_GRAIN = [
    ("runner", "run", "a runner is a FILE and a run is an EVENT (A1f)"),
    ("script", "execution", "a script is a file; an execution is an event (A1f)"),
    ("check", "iteration", "a check is written once and may iterate (A1f)"),
    ("row", "site", "O1 itself: 14 (site,target) rows behind 12 source lines"),
    ("file", "line", "mg-d53d's arc: 806 deletion rows vs the files they fall in"),
    ("item", "specy", "mg-4adb's species vs its rungs"),
    ("pair", "poset", "mg-0ba7's 0 crossings over 10 ordered tree pairs"),
    ("mention", "name", "mg-bf79's P3c: a MENTION is still COUNTED"),
    ("site", "execution", "F1, the one axis the instrument was built for"),
]


def _key(a, b):
    return tuple(sorted((B.singular(a.lower()), B.singular(b.lower()))))


_ADJ = {}
for _a, _b, _why in SAME_GRAIN:
    _ADJ[_key(_a, _b)] = ("SAME", _why)
for _a, _b, _why in DIFF_GRAIN:
    _ADJ[_key(_a, _b)] = ("DIFFERENT", _why)


def verdict(a, b):
    """('SAME'|'DIFFERENT'|'UNADJUDICATED', reason) for two grain nouns.

    THE ACTUAL REPAIR, AND IT IS NOT MORE SYMBOLS.  `_classify` answers every
    one of the 79 800 corpus pairs with a definite verdict, and 68 596 of those
    answers are `same grain` -- including `rows`/`sites`.  An open-set
    classifier answers every one of them `different` -- including
    `steps`/`iterations`.  Both are total functions and both are wrong in bulk,
    because *are these the same grain* is a question about the world and
    neither function has been told the answer.

    So this returns a THIRD value for the pairs nobody has adjudicated.  It is
    a strictly weaker instrument by every count -- it answers fewer questions
    than either -- and that is the point: the number it makes reportable is HOW
    MANY PAIRS THE ARC HAS NEVER ADJUDICATED, which is the honest form of the
    ticket's `623` and its `370`.

    No arity carries this.  A function returning one symbol per WORD encodes a
    partition, a partition is an equivalence relation, and an equivalence
    relation cannot express *unknown* -- every pair is in or out of a block.
    That is why adding values to `_classify` is the wrong axis and why adding
    `ROW_WORDS` is the wrong axis a second time.
    """
    if B.singular(a.lower()) == B.singular(b.lower()):
        return "SAME", "identical noun"
    return _ADJ.get(_key(a, b), ("UNADJUDICATED", ""))


# ---------------------------------------------------------------------------
# Running things.
# ---------------------------------------------------------------------------

def run_argv(argv, cwd):
    return A.run_argv(argv, cwd)


def subject_rev_present(rev):
    p = subprocess.run(["git", "-C", REPO, "cat-file", "-e", "%s^{commit}"
                        % rev], capture_output=True, text=True)
    return p.returncode == 0
