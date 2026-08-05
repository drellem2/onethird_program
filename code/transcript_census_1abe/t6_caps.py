"""t6 -- THE SHAPE, NOT THE INSTANCE: a truncating slice printed under a
sentence whose own words claim completeness.

The ticket asks for `unreachable[:3]` in `code/audit_c067/c2_anchors.py` to be
fixed in passing.  IT IS ALREADY FIXED -- mg-c3a2 removed it in `5bd0d71` and
the only surviving occurrence of the string in that file is inside the comment
explaining the removal.  That is disclosed in PREDICTIONS.md as D3 and it is
not going to be re-fixed here.

What is worth doing instead is the thing the ticket itself says about it: it is
"the arc's most repeated shape -- A CAP THAT WAS A NO-OP WHEN WRITTEN AND
BECAME A SILENT TRUNCATION WHEN THE POPULATION GREW".  A shape survives in
places nobody has looked.  So this script looks.

POPULATION  every `.py` file tracked under `code/` at the named revision.
GRAIN       one row per (file, line) SLICE SITE.

A site is LIVE when all three hold, checked on the AST rather than by grep:
  1  a subscript slices with a CONSTANT upper bound and no lower bound --
     `xs[:3]`, the shape that silently drops the tail;
  2  the enclosing statement emits output -- a `print`, an f-string, or a
     `.join`;
  3  a string literal in that same statement claims completeness, using the
     vocabulary printed below.

THE DETECTOR IS CONTROLLED BEFORE IT IS BELIEVED.  T6a runs it against the
blob of `c2_anchors.py` FROM BEFORE mg-c3a2's fix, where the defect is known to
be present, and against the blob from after, where it is known to be gone.  A
detector that cannot go green and red on the one instance everybody agrees
about is not evidence about the instances nobody has checked.
"""

import ast
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_1abe as L                                          # noqa: E402

# The vocabulary is printed into the transcript so a reader can disagree with
# it precisely rather than in general.
COMPLETENESS = re.compile(
    r"\b(each|every|all \d|all of|in full|nothing truncated|"
    r"the full list|every one|no cap|complete list)\b", re.I)


def output_bearing(node):
    for n in ast.walk(node):
        if isinstance(n, ast.JoinedStr):
            return True
        if isinstance(n, ast.Call):
            f = n.func
            if isinstance(f, ast.Name) and f.id == "print":
                return True
            if isinstance(f, ast.Attribute) and f.attr == "join":
                return True
    return False


def strings_in(node):
    out = []
    for n in ast.walk(node):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            out.append(n.value)
    return out


def capped_slices(node):
    """Lines of `x[:N]` subscripts with a constant upper bound, no lower."""
    hits = []
    for n in ast.walk(node):
        if isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Slice):
            s = n.slice
            if s.lower is None and s.step is None and \
                    isinstance(s.upper, ast.Constant) and \
                    isinstance(s.upper.value, int):
                hits.append((n.lineno, s.upper.value))
    return hits


def truncating_slices(node):
    """Capped slices that are ITERATED OVER, which is the actual defect.

    `unreachable[:3]` in mg-c3a2's finding is the iterable of a generator
    inside a `join`.  `commit[:7]` is a SHA ABBREVIATION and is not a truncated
    list at all -- and this arc abbreviates shas inside sentences containing
    the word `each` constantly.  A detector that counts every capped slice
    reports the abbreviations, buries the three real sites among them, and is
    the same defect it is hunting: a number whose population is not what its
    name says.

    So a site counts only where the slice is consumed as a SEQUENCE: the
    iterable of a `for` or a comprehension, the argument of a `.join`, or an
    argument printed directly -- and only where the slice IS that expression,
    not merely somewhere inside it.  `"; ".join(f"{c[:7]}" for c in xs)` joins
    the whole list and abbreviates each sha; the cap is on the sha, not on the
    list, and a rule that looked anywhere inside the join argument would call
    that a truncated list.  It is the same over-collection in miniature.
    """
    consumed = []
    for n in ast.walk(node):
        if isinstance(n, ast.For):
            consumed.append(n.iter)
        elif isinstance(n, ast.comprehension):
            consumed.append(n.iter)
        elif isinstance(n, ast.Call):
            f = n.func
            if isinstance(f, ast.Attribute) and f.attr == "join":
                consumed.extend(n.args)
            elif isinstance(f, ast.Name) and f.id == "print":
                consumed.extend(n.args)
    hits = []
    for expr in consumed:
        hits.extend(_root_capped(expr))
    return hits


# Wrappers that pass a sequence straight through, so a cap under one of them is
# still a cap on the sequence being consumed.
PASSTHROUGH = ("sorted", "list", "reversed", "tuple", "set", "enumerate")


def _root_capped(expr):
    """The capped slice AT THE ROOT of a consumed expression, if there is one."""
    if isinstance(expr, ast.Call) and isinstance(expr.func, ast.Name) \
            and expr.func.id in PASSTHROUGH and expr.args:
        return _root_capped(expr.args[0])
    if isinstance(expr, ast.Subscript) and isinstance(expr.slice, ast.Slice):
        s = expr.slice
        if s.lower is None and s.step is None and \
                isinstance(s.upper, ast.Constant) and \
                isinstance(s.upper.value, int):
            return [(expr.lineno, s.upper.value)]
    return []


def scan(source):
    """[(line, bound, claim)] -- the LIVE sites of one module's source."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None
    live = []
    for stmt in ast.walk(tree):
        if not isinstance(stmt, ast.stmt):
            continue
        caps = capped_slices_shallow(stmt)
        if not caps or not output_bearing(stmt):
            continue
        claims = [s for s in strings_in(stmt) if COMPLETENESS.search(s)]
        if not claims:
            continue
        for line, bound in caps:
            live.append((line, bound, COMPLETENESS.search(claims[0]).group(0)))
    return live


def _nested_node_ids(stmt):
    """Ids of every node inside a compound statement's own sub-statements.

    Without this a `for` loop would claim every slice nested inside it and the
    row count would measure nesting depth rather than sites.
    """
    inner = set()
    for field in ("body", "orelse", "finalbody", "handlers"):
        for sub in getattr(stmt, field, None) or []:
            for n in ast.walk(sub):
                inner.add(id(n))
    return inner


def capped_slices_shallow(stmt):
    """Truncating slices belonging to THIS statement, not to nested bodies."""
    inner = _nested_node_ids(stmt)
    hits = []
    for ln, b in truncating_slices(stmt):
        node = _slice_node(stmt, ln, b)
        if id(node) not in inner:
            hits.append((ln, b))
    return hits


def _slice_node(stmt, line, bound):
    for n in ast.walk(stmt):
        if isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Slice) \
                and n.lineno == line and isinstance(n.slice.upper, ast.Constant) \
                and n.slice.upper.value == bound:
            return n
    return stmt


def main():
    rev = L.main_rev()
    head = L.resolve(rev)
    led = L.Ledger("t6 -- A CAP UNDER A SENTENCE THAT CLAIMS COMPLETENESS")
    print("    as-of      %s  (%s)" % (head, rev))
    print("    completeness vocabulary: %s" % COMPLETENESS.pattern)

    # ------------------------------------------------- control the detector
    led.head("T6a -- THE DETECTOR CONTROLLED ON THE ONE INSTANCE EVERYBODY "
             "AGREES ABOUT")
    print("""
`git log -S` cannot find mg-c3a2's fix: the commit REMOVED the code
`unreachable[:3]` and ADDED a comment quoting it, so the occurrence count is
unchanged and the pickaxe is silent.  The two blobs are therefore located by
asking every historical version of the file whether it contains the CODE form
`in unreachable[:3]`, which the explanatory comment does not.
""")
    path = "code/audit_c067/c2_anchors.py"
    before = after = None
    for c in L.git("log", "--format=%H", rev, "--", path).split():
        blob = L.blob_at(c, path)
        if blob is None:
            continue
        if b"in unreachable[:3]" in blob:
            before = before or c
        elif before is None:
            after = c
    if before is None:
        led.self_error("T6a no historical blob of %s contains the code form "
                       "`in unreachable[:3]`; the control did not run" % path)
    else:
        after = after or rev
        b_before = L.blob_at(before, path)
        b_after = L.blob_at(after, path)
        s_before = scan(b_before.decode()) or []
        s_after = scan(b_after.decode()) or []
        print("    newest blob WITH the defect : %s" % before[:7])
        print("    the blob that replaced it   : %s" % after[:7])
        print("    LIVE sites with the defect  : %s" % s_before)
        print("    LIVE sites after the fix    : %s" % s_after)
        led.record(bool(s_before),
                   "T6a RED ANSWER: the detector finds %d LIVE site(s) in %s "
                   "at %s, where mg-c3a2 says the defect was"
                   % (len(s_before), os.path.basename(path), before[:7]))
        led.record(not s_after,
                   "T6a' GREEN ANSWER: and finds %d at %s, after the fix.  "
                   "Both answers on the same file, so the sweep below is "
                   "evidence rather than an assertion"
                   % (len(s_after), after[:7]))

    # ----------------------------------------------------------- the sweep
    led.head("T6b -- THE SWEEP: EVERY `.py` UNDER `code/`")
    files = [p for p in L.git("ls-tree", "-r", "--name-only", rev,
                              "code/").split("\n")
             if p.endswith(".py")]
    total_caps, unparsed, live = 0, [], []
    for p in files:
        blob = L.blob_at(rev, p)
        if blob is None:
            continue
        try:
            src = blob.decode("utf-8")
        except UnicodeDecodeError:
            unparsed.append(p)
            continue
        try:
            total_caps += len(truncating_slices(ast.parse(src)))
        except SyntaxError:
            unparsed.append(p)
            continue
        for line, bound, claim in scan(src) or []:
            live.append((p, line, bound, claim))

    print("    %d `.py` files, %d capped-slice sites in all, %d files this "
          "instrument could not parse" % (len(files), total_caps, len(unparsed)))
    for p in unparsed:
        print("      UNPARSED %s" % p)
    print()
    print("    LIVE SITES -- a capped slice, printed, under a completeness "
          "claim.  Every one, no cap of my own:")
    print("    %-56s %-6s %-6s %s" % ("file", "line", "bound", "the claim"))
    for p, line, bound, claim in sorted(live):
        print("    %-56s %-6d [:%-4d %s" % (p[len("code/"):][:56], line, bound,
                                            claim))
    if not live:
        print("      (none)")

    led.record(not live,
               "T6b %d LIVE sites over %d `.py` files: a constant-capped slice "
               "reaching output in a statement whose own words claim "
               "completeness.  The ticket asked for ONE instance in ONE file "
               "and that instance was already fixed; this is the shape it "
               "belongs to, measured" % (len(live), len(files)))
    led.record(None,
               "T6b' the denominator matters: %d capped-slice sites exist in "
               "all, so %d LIVE is a claim about %.1f%% of them.  Most caps in "
               "this arc are legitimate -- a preview, a column width, a "
               "first-N-of-a-sorted-list under a sentence that says so"
               % (total_caps, len(live),
                  100.0 * len(live) / total_caps if total_caps else 0))
    # ------------------------------------------------------- adjudication
    led.head("T6c -- EACH LIVE SITE WITH ITS SOURCE, SO THE READER CAN "
             "DISAGREE WITH ME")
    print("""
A detector's hit is a candidate.  The surrounding source is printed for every
one, because the question `does the completeness word refer to the sliced list
or to something else in the same sentence?` is a judgement, and a judgement
made behind a count cannot be checked.
""")
    for p, line, bound, claim in sorted(live):
        blob = L.blob_at(rev, p)
        lines = blob.decode("utf-8", "replace").splitlines()
        lo, hi = max(0, line - 7), min(len(lines), line + 3)
        print("    --- %s:%d   cap [:%d   claim %r" % (p, line, bound, claim))
        for i in range(lo, hi):
            print("      %5d %s%s" % (i + 1, ">>" if i + 1 == line else "  ",
                                      lines[i][:100]))
        print()
    if not live:
        print("    (no live sites to adjudicate)")

    led.record(None,
               "T6b'' WHAT THIS DOES NOT SEE: a cap whose completeness claim "
               "lives in a DIFFERENT statement -- a heading printed three "
               "lines earlier, or prose in a README.  The detector is "
               "statement-scoped, so its %d is a LOWER BOUND and reading it as "
               "the population would repeat the ticket's own defect"
               % len(live))
    return led.done()


if __name__ == "__main__":
    sys.exit(main())
