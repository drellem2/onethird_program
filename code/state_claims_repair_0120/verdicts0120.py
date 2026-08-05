#!/usr/bin/env python3
"""mg-0120 — THE SIX VERDICTS `claims16eb.py` CARRIED AS LITERALS, COMPUTED.

`code/state_delegation_audit_16eb/claims16eb.py` is named "THE CLAIMS mg-0049 ADDED,
CHECKED".  Read with `ast` it has 16 `claim()` call sites and prints 17 rows, and SEVEN of
the sites pass a constant as the verdict.  Six of those seven are on the printed path:

    claims16eb.py:94    literal False    the two tables cannot drift apart in EITHER direction
    claims16eb.py:142   literal False    exit 1 means "NO LONGER PRESENTED TO A READER"
    claims16eb.py:156   literal True     presentation.py: nothing changed except one message
                                         and four self-test cases
    claims16eb.py:178   literal True     COVERAGE.md's R1/R2 table: exit 0 / exit 1
    claims16eb.py:194   literal False    both batteries "re-run in section 7 of run_all.sh"
    claims16eb.py:217   literal False    R5: `<details>` at the top SUPPRESSES NOTHING

The seventh (line 72) is the `if m is None:` guard branch: it runs only when the sentence the
row is about has been DELETED, so a constant there is a deliberate alarm and not a pinned
result.  It is left exactly as it is and this file does not touch it.

WHY A LITERAL IS NOT A CHECK.  A constant returns the same answer on every tree.  It reported
BROKEN before the repair and it reports BROKEN after it; it would report BROKEN on an empty
repository.  The row's NAME asserts a measurement and its BODY is a typed-in answer, which is
the exact defect this arc has spent eight tickets finding in other people's instruments.

WHY REPLACING THE LITERAL IS NOT ENOUGH EITHER, AND WHAT THIS FILE OWES.  An expression that
returns the right answer today is indistinguishable from a constant until somebody has seen
it return the other one.  So every function here is written to be run at MORE THAN ONE
REVISION, and `flip_0120.py` runs each of them on an input that produces the opposite
verdict.  A verdict this file computes and `flip_0120.py` cannot flip is reported as NOT
PROVEN CAPABLE OF BOTH ANSWERS.

THE THIRD STATE, and it is not a hedge.  Three of these six rows quote a SENTENCE, and
mg-a74f rewrote two of those sentences.  A row whose sentence is gone has not become true —
it has become moot, and reporting it `holds` would be the same defect one level up: a green
row standing for a measurement nobody took.  Every function here therefore LOCATES its
sentence first and returns `None` (RESPECIFIED) if it is not there, naming what replaced it.

NOTHING HERE WRITES TO THE WORKING TREE.  Constructions are applied inside throwaway
worktrees created with `git worktree add --detach`, which are removed on the way out; the
checkout this runs in is never opened for writing.  `claims16eb.py`'s header sentence
"Nothing here mutates anything" is updated by this repair to say that precisely, rather than
left to go quietly false.
"""
import ast
import html.parser
import os
import re
import shutil
import subprocess
import sys
import tempfile

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()

CTL = "code/state_landing_control_2da3/delta_control.py"
PRES = "code/state_landing_control_2da3/presentation.py"
COV = "code/state_landing_control_2da3/COVERAGE.md"
R49 = "code/state_delegation_repair_0049/render0049.py"
RDM = "code/state_delegation_repair_0049/README.md"
RUN = "code/state_delegation_repair_0049/run_all.sh"
RERUN = "code/state_delegation_audit_16eb/out_5644_rerun.txt"
TARGET = "docs/state-history/attempt-mg-276d.md"

# The two revisions mg-0049's diff is bounded by.  Claim 5 is about the DIFF, not the tree,
# so its population is a commit RANGE and it is written here rather than inside the function.
BASE_0049 = "db2b77d"
TIP_0049 = "5594c69"

ENGINES = ["marked", "markdown-it"]
CITED = ["H1", "H2", "H3", "H4", "H5"]
BRIDGE = "code/state_layer_audit_218d/render218d.js"


def git(*a, **kw):
    return subprocess.run(["git", "-C", REPO, *a], capture_output=True, text=True, **kw)


def at(rev, path):
    """The bytes of `path` at `rev`; `rev=None` means the working tree."""
    if rev is None:
        with open(os.path.join(REPO, path), encoding="utf-8") as fh:
            return fh.read()
    return git("show", f"{rev}:{path}").stdout


class Worktree:
    """A throwaway detached checkout.  Written to freely, removed whole on close, so there is
    no restore step and therefore no restore step that can fail."""

    def __init__(self, rev):
        self.rev = rev or "HEAD"
        self.dir = tempfile.mkdtemp(prefix="0120-wt-")
        shutil.rmtree(self.dir)
        git("worktree", "add", "--detach", self.dir, self.rev, check=True)

    def read(self, rel):
        with open(os.path.join(self.dir, rel), encoding="utf-8") as fh:
            return fh.read()

    def write(self, rel, text):
        with open(os.path.join(self.dir, rel), "w", encoding="utf-8") as fh:
            fh.write(text)

    def control(self):
        """(exit code, stdout, stderr) of delta_control.py AS IT STANDS IN THIS WORKTREE.

        STDERR IS RETURNED BECAUSE A CRASH IS NOT A CATCH.  The first draft of this class
        returned only (code, stdout), and `v3_two_tables` read a non-zero exit as "the
        control caught the drift" — so a mutation that made `delta_control.py` raise
        `NameError` before it reached any check was scored as the control working.  All
        three of that draft's constructions scored `caught` and none of them ran a check.
        mg-d075 recorded the same shape ("a crash the runner scored ok") in its own repair;
        this is its second instance and it was found by this repair's own no-op control."""
        p = subprocess.run([sys.executable, os.path.join(self.dir, CTL)], cwd=self.dir,
                           capture_output=True, text=True)
        return p.returncode, p.stdout, p.stderr

    def close(self):
        git("worktree", "remove", "--force", self.dir)
        shutil.rmtree(self.dir, ignore_errors=True)


# =========================================================================================
# PRESENTATION.  Two different questions, kept apart on purpose, because conflating them is
# the defect mg-4acd was landed to draw and mg-16eb's OPEN 1 is about.
#
#   in_html   are the section's BYTES in the serialised page?      a property of the artefact
#   shown     is a reader REACHED by them?                          a property of the reading
#
# `shown` is decided by handing the bytes to the standard library's HTML parser and reading
# attributes BY NAME off the parse — not by matching words in attribute text, which is the
# defect mg-65eb found in `visible_a74f.py` (`class="hidden"` scored suppressed there).
# =========================================================================================
class _Shown(html.parser.HTMLParser):
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
            "param", "source", "track", "wbr"}

    def __init__(self, marker):
        super().__init__(convert_charrefs=True)
        self.marker, self.stack, self.hits = marker, [], []

    def handle_starttag(self, tag, attrs):
        if tag not in self.VOID:
            self.stack.append((tag, dict(attrs)))

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                return

    def handle_comment(self, data):
        if self.marker in data:
            self.hits.append("an HTML comment — bytes in the file, nothing in the page")

    def handle_data(self, data):
        if self.marker in data:
            self.hits.append(self._suppressor())

    def _suppressor(self):
        for tag, attrs in self.stack:
            if tag == "details" and "open" not in attrs:
                return "a <details> carrying no `open` attribute"
            if "hidden" in attrs:
                return "the `hidden` ATTRIBUTE, read by name off the parse"
            if tag in ("script", "style", "template"):
                return f"a <{tag}> element"
            style = (attrs.get("style") or "").replace(" ", "").lower()
            if "display:none" in style or "visibility:hidden" in style:
                return "an inline style"
        return None


def render(engine, text, cwd=None):
    """mg-218d's renderer BRIDGE, unmodified, as mg-5644/mg-0049/mg-16eb/mg-a74f all use it.

    The bridge takes a PATH, not stdin — so the markdown goes to a temp file outside the
    repository.  (This function's first draft passed `-` and every render raised ENOENT,
    which `renderers_present()` reported as "renderers absent": a dependency check that
    answers the wrong question is exactly the shape this repair is about, and it fired on
    this repair first.  Kept described rather than deleted.)"""
    root = cwd or REPO
    fd, path = tempfile.mkstemp(suffix=".md", prefix="0120-render-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        p = subprocess.run(["node", os.path.join(root, BRIDGE), engine, path],
                           capture_output=True, text=True)
    finally:
        os.unlink(path)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip()[:300])
    return p.stdout


def renderers_present():
    try:
        render("marked", "# x")
        render("markdown-it", "# x")
        return True
    except Exception:
        return False


def _markers(doc_text):
    """The heading TEXT of each cited section — the string a reader would have to be shown."""
    out = []
    for name in CITED:
        m = re.search(rf"^#+\s+{name}\b[^\n]*$", doc_text, re.M)
        out.append(m.group(0).lstrip("# ").strip() if m else name)
    return out


def _shown_and_bytes(engine, markdown, markers, cwd=None):
    page = render(engine, markdown, cwd)
    shown, reasons = 0, {}
    for m in markers:
        p = _Shown(m)
        p.feed(page)
        p.close()
        if not p.hits:
            reasons[m] = "not in the rendered page at all"
        elif any(h is None for h in p.hits):
            shown += 1
        else:
            reasons[m] = p.hits[0]
    in_bytes = sum(1 for m in markers if m in page)
    return shown, in_bytes, len(markers), reasons


# =========================================================================================
# V3  claims16eb.py:94 — delta_control.py's DELEGATED_PRESENTATION comment:
#     "the two tables cannot drift apart quietly in EITHER direction"
#
# COMPUTED BY CONSTRUCTING THE DRIFT.  Three mutations, run through delta_control.py AS IT
# STANDS AT THE REVISION UNDER TEST.  The sentence says NEITHER direction can be quiet, so
# the verdict is "every one of the three is caught (non-zero exit)".
#
# The mutations are built from the PARSE, not from digest literals.  mg-65eb's version of
# this probe pasted a specific sha out of `bd24efc`'s table; at any revision where that sha
# moves, the mutation silently becomes a no-op and the probe passes on having done nothing.
# That failure mode is DETECTED here (a mutation that does not change the text is reported as
# a rotted anchor and the verdict is withheld), and avoided by locating the table with `ast`.
# =========================================================================================
def _dp_block(text):
    """(first line index, last line index, the source lines) of the whole
    `DELEGATED_PRESENTATION = {...}` STATEMENT — the target included.

    Located with `ast` so it cannot be missed when the table moves, but EDITED AS TEXT (see
    below), so the surrounding bytes are never reformatted."""
    tree = ast.parse(text)
    for node in tree.body:
        if (isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "")
                == "DELEGATED_PRESENTATION"):
            return node.lineno - 1, node.end_lineno - 1, text.split("\n")
    return None, None, None


_ROW_LINE = re.compile(r'^(\s+)"(\w+)":\s*"([0-9a-f]{64})",\s*$')


def v3_two_tables(rev=None, _wt=None, ctl_text=None):
    """(verdict, detail).  True iff every forbidden drift is caught.

    THE MUTATIONS ARE MINIMAL TEXT EDITS — one line inserted, one line deleted — inside the
    statement `ast` located.  An earlier draft re-emitted the whole table from
    `ast.literal_eval`, which is tidier and wrong twice over: it reformats bytes the sentence
    is not about, and its span started at the `{` rather than at the name, so every mutated
    copy dropped `DELEGATED_PRESENTATION = ` and the control died of `NameError` before
    reaching a single check.  All three constructions then scored `caught`.  That draft is
    described here rather than deleted because it is this repair's own instance of the defect
    the ticket is about: a verdict that reported the right answer for a reason unconnected to
    the property.  The no-op control below is what caught it and it now runs on every call.

    `ctl_text` overrides the base bytes of delta_control.py.  It exists because the first
    draft of `flip_0120.py`'s C3 patched the control INSIDE the worktree and then called this
    function, which read the base from the working tree and wrote it straight back over the
    patch — so the construction ran against an unpatched control and was scored as though the
    drift had been caught.  The construction reported MISSED, which is how it was found."""
    text = at(rev, CTL) if ctl_text is None else ctl_text
    i, j, lines_of = _dp_block(text)
    if i is None:
        return None, "    DELEGATED_PRESENTATION is not a module-level assignment here"
    block = lines_of[i:j + 1]
    rows = [k for k, ln in enumerate(block) if _ROW_LINE.match(ln)]
    if not rows:
        return None, "    the table has no `\"NAME\": \"<64 hex>\",` row to work from"
    last = rows[-1]
    indent = _ROW_LINE.match(block[last]).group(1)

    def rebuild(new_block):
        return "\n".join(lines_of[:i] + new_block + lines_of[j + 1:])

    d1 = list(block); d1.insert(last + 1, f'{indent}"H99": "{"0" * 64}",')
    d2 = list(block); d2.insert(1, f'    "docs/state-history/no-such-target.md": {{\n'
                                   f'        "H1": "{"1" * 64}",\n'
                                   f'    }},')
    d3 = [ln for k, ln in enumerate(block) if k != last]
    cases = [
        ("D0  NO-OP — the same bytes, rewritten by the same code path",
         "(this repair's own control)", rebuild(block)),
        ("D1  a PRESENTATION RECORD for a section nothing delegates or cites",
         "here and in nothing else", rebuild(d1)),
        ("D2  a whole TARGET FILE certified here and delegated by nobody",
         "here and in nothing else", rebuild(d2)),
        ("D3  a delegated section's record DELETED (the direction it gets right)",
         "in DELEGATED and absent here", rebuild(d3)),
    ]
    lines, verdicts = [], {}
    wt = _wt or Worktree(rev)
    try:
        for label, direction, mutated in cases:
            noop = label.startswith("D0")
            if (mutated == text) is not noop:
                why = ("CHANGED BYTES — the no-op is not one" if noop
                       else "MUTATION IS A NO-OP — anchor rotted")
                lines.append(f"    {label:<66s} {why}")
                verdicts[label] = None
                continue
            orig = wt.read(CTL)
            wt.write(CTL, mutated)
            code, _out, err = wt.control()
            wt.write(CTL, orig)
            crashed = "Traceback (most recent call last)" in err
            verdicts[label] = None if crashed else code
            note = ("CRASHED — not a catch" if crashed else
                    "QUIET — the control says nothing" if code == 0 else "caught")
            lines.append(f"    {label:<66s} exit {code}  {note}   ({direction})")
    finally:
        if _wt is None:
            wt.close()
    d0 = verdicts["D0  NO-OP — the same bytes, rewritten by the same code path"]
    if d0 != 0:
        return None, "\n".join(lines) + (
            "\n    THE NO-OP DID NOT EXIT 0.  The mutation machinery is disturbing something\n"
            "    other than the table, so nothing measured below is about the sentence.\n"
            "    VERDICT WITHHELD.")
    drifts = {k: v for k, v in verdicts.items() if not k.startswith("D0")}
    if any(v is None for v in drifts.values()):
        return None, "\n".join(lines) + ("\n    a construction was a no-op or crashed; the "
                                         "verdict is WITHHELD, not guessed")
    quiet = [k for k, v in drifts.items() if v == 0]
    lines.append(f"    population: 3 constructed drifts (plus the no-op control), 2 of them "
                 f"in the direction the sentence is doubted on.")
    lines.append(f"    {len(quiet)} of 3 are QUIET.  The sentence says none of them can be.")
    return not quiet, "\n".join(lines)


# =========================================================================================
# V4  claims16eb.py:142 — delta_control.py's EXIT CODES table:
#     exit 1 is "a region ... NO LONGER PRESENTED TO A READER"
#
# STAGE 1 LOCATES THE SENTENCE.  mg-a74f narrowed this bullet to the state-set predicate, so
# at any revision after that repair the sentence mg-16eb quoted IS NOT IN THE FILE, and the
# honest verdict is RESPECIFIED, not `holds`.  The locate rule is: does exit 1's bullet
# ASSERT the presentation property (rather than disclaim it)?
#
# STAGE 2, when it is asserted, refutes it in both directions by construction:
#     E1  exit 1 while a reader is shown every cited section  => exit 1 does not imply it
#     E2  a reader shown none of five, at an exit that is not 1 => it does not imply exit 1
# =========================================================================================
def _exit1_bullet(text):
    m = re.search(r"^    1   FAIL(.*?)^    2   MOVED", text, re.M | re.S)
    return m.group(1) if m else None


def v4_exit_semantics(rev=None, _wt=None, have_node=None,
                      e1_example=None, e2_prefix="<details>\n<summary>Superseded drafts"
                                                 "</summary>\n\n"):
    """`e1_example` and `e2_prefix` are the two CONSTRUCTIONS, exposed as parameters so
    `flip_0120.py` can hand this function an input on which the verdict is the opposite one.
    A verdict whose inputs are all hard-coded inside it can only ever be checked at the
    revisions history happens to provide, and that is not enough to show it computes."""
    text = at(rev, CTL)
    bullet = _exit1_bullet(text)
    if bullet is None:
        return None, "    the EXIT CODES table has no `1   FAIL` bullet at this revision"
    # Both patterns are whitespace-flexible because the bullet is HARD-WRAPPED prose: the
    # disclaimer really does read `IS NOT "WHAT A\n    READER IS SHOWN"`, and a first draft
    # of this line matched on a single space and reported `disclaims: False` about a file
    # that disclaims it in capitals.
    asserts = bool(re.search(r"NO\s+LONGER\s+PRESENTED\s+TO\s+A\s+READER", bullet))
    disclaims = bool(re.search(r'IS\s+NOT\s+"WHAT\s+A\s+READER\s+IS\s+SHOWN"', bullet))
    if not asserts:
        return None, (
            "    the sentence this row is about is NOT IN THE FILE at this revision.\n"
            f"    exit 1's bullet asserts the presentation property: {asserts}\n"
            f"    exit 1's bullet DISCLAIMS it in as many words:    {disclaims}\n"
            "    mg-a74f narrowed the bullet to the state-set predicate, so this row is\n"
            "    RESPECIFIED.  It has not become true; the claim it checked is gone, and\n"
            "    the successor sentence is a different claim needing a different check.")
    if have_node is False:
        return None, ("    the sentence IS asserted here, and refuting it needs two GFM\n"
                      "    renderers, which are absent.  UNPROBED — never guessed.")
    doc = at(rev, TARGET)
    markers = _markers(doc)
    wt = _wt or Worktree(rev)
    lines = []
    try:
        orig = wt.read(TARGET)
        head = orig.index("### H3 ")
        example = ("An example, so a reader can check the rescaling:\n\n"
                   "```python\nd_true = np.diag(row_signs) @ d_allplus\n```\n\n"
                   if e1_example is None else e1_example)
        e1 = orig[:head] + example + orig[head:]
        wt.write(TARGET, e1)
        code1, _o1, err1 = wt.control()
        e2 = e2_prefix + orig
        wt.write(TARGET, e2)
        code2, _o2, err2 = wt.control()
        wt.write(TARGET, orig)
        shown1 = shown2 = None
        for eng in ENGINES:
            s1, _b1, t1, _r = _shown_and_bytes(eng, e1, markers)
            s2, _b2, t2, r2 = _shown_and_bytes(eng, e2, markers)
            lines.append(f"    {eng:<12s} E1 exit {code1}  {s1}/{t1} cited sections SHOWN"
                         f"     E2 exit {code2}  {s2}/{t2} SHOWN")
            if r2:
                lines.append(f"    {'':<12s} E2's reason: {sorted(set(r2.values()))[0]}")
            shown1 = s1 if shown1 is None else min(shown1, s1)
            shown2 = s2 if shown2 is None else max(shown2, s2)
    finally:
        if _wt is None:
            wt.close()
    d1 = code1 == 1 and shown1 == len(markers)
    d2 = shown2 == 0 and code2 != 1
    lines.append(f"    direction 1 refuted (exit 1 and every section SHOWN):        {d1}")
    lines.append(f"    direction 2 refuted (nothing shown at an exit that is not 1): {d2}")
    return not (d1 or d2), "\n".join(lines)


# =========================================================================================
# V5  claims16eb.py:156 — presentation.py's header:
#     "NOTHING IN THIS FILE CHANGED EXCEPT ONE MESSAGE AND FOUR SELF-TEST CASES"
#
# THE POPULATION IS A COMMIT RANGE, NOT A TREE.  The sentence is about what mg-0049's diff
# did, so it is computed over `db2b77d..5594c69` and it does not move when the tree does.
#
# THE GRAIN IS AN EXECUTABLE STATEMENT.  Both revisions are parsed, EVERY DOCSTRING IS
# REMOVED, and the two are unparsed and compared line by line.  Prose is therefore out of the
# population by construction — a sentence about what CHANGED in a file cannot be answered by
# counting sentences.  The sentence is true iff the changed executable lines are exactly (a)
# one message string and (b) additions inside the self-test material.
#
# The row this replaces was pinned `True` and justified with a fact about a DIFFERENT
# property — that the eleven certified digests are byte-identical.  That justification is
# true and is not this sentence.
# =========================================================================================
_SELFTEST_NAMES = ("_self_test", "_SECTION_CASES", "_SECTION", "_POSITION_CASES", "_CASES")


class _StripDocstrings(ast.NodeTransformer):
    def _strip(self, node):
        self.generic_visit(node)
        if (node.body and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, ast.Constant)
                and isinstance(node.body[0].value.value, str)):
            node.body = node.body[1:] or [ast.Pass()]
        return node

    visit_Module = visit_FunctionDef = visit_ClassDef = _strip


def _code_lines(text):
    tree = _StripDocstrings().visit(ast.parse(text))
    ast.fix_missing_locations(tree)
    return ast.unparse(tree).split("\n")


def _owner_of(text, line_fragment):
    """The top-level name whose unparsed body contains `line_fragment` — used to say WHERE a
    changed statement is, so a reader can check the classification instead of trusting it."""
    tree = _StripDocstrings().visit(ast.parse(text))
    ast.fix_missing_locations(tree)
    for node in tree.body:
        name = (getattr(node, "name", None)
                or getattr(getattr(node, "targets", [None])[0], "id", None))
        if name and line_fragment in ast.unparse(node):
            return name
    return "(module level)"


def v5_presentation_diff(rev=None):
    """`rev` is accepted and IGNORED for the base: the claim is about a fixed commit range.
    It is used only to decide which TIP is compared, so `flip_0120.py` can point the same
    computation at a range where the answer differs."""
    import difflib
    tip = TIP_0049 if rev is None else rev
    old, new = at(BASE_0049, PRES), at(tip, PRES)
    try:
        a, b = _code_lines(old), _code_lines(new)
    except SyntaxError as exc:
        return None, f"    presentation.py does not parse at one end of the range: {exc}"
    changed = [ln for ln in difflib.unified_diff(a, b, n=0, lineterm="")
               if ln[:1] in "+-" and ln[:3] not in ("+++", "---")]
    messages, selftest, other = [], [], []
    for ln in changed:
        body = ln[1:].strip()
        owner = _owner_of(new if ln[0] == "+" else old, body[:60])
        if any(owner.startswith(n) or n in body for n in _SELFTEST_NAMES):
            selftest.append((ln[0], owner, body))
        elif re.match(r"^position\s*=", body) or body.startswith(("position =", "'no block")):
            messages.append((ln[0], owner, body))
        else:
            other.append((ln[0], owner, body))
    lines = [f"    population: EXECUTABLE lines of presentation.py changed between "
             f"{BASE_0049} and {tip}; every docstring removed from both sides first.",
             f"    grain: one unparsed statement line.",
             f"    changed lines: {len(changed)}   "
             f"message {len(messages)}   self-test {len(selftest)}   OTHER {len(other)}"]
    for sign, owner, body in other[:8]:
        lines.append(f"      {sign} {owner:<22s} {body[:78]}")
    if len(other) > 8:
        lines.append(f"      ... and {len(other) - 8} more")
    n_msg = len({b for s, _o, b in messages if s == "+"})
    if not other:
        lines.append(f"    nothing outside the two named categories changed; the sentence "
                     f"holds ({n_msg} message form(s), {len(selftest)} self-test lines).")
    else:
        lines.append(f"    {len(other)} changed executable line(s) are NEITHER a message NOR "
                     f"a self-test case.  The sentence says there are none.")
    return not other, "\n".join(lines)


# =========================================================================================
# V6  claims16eb.py:178 — COVERAGE.md's R1/R2 table: exit 0 against mg-bee1, exit 1 against
#     mg-0049.
#
# COMPUTED BY JOINING TWO DOCUMENTS.  The claimed pair is READ OUT OF THE TABLE (not typed
# here), the observed pair is READ OUT OF mg-5644's OWN re-run transcript, and the verdict is
# whether they agree row by row.  `expected exit N` in that transcript is mg-5644's
# prediction, made against mg-bee1's control — so it IS the "against mg-bee1" column, and
# `got exit N` is the "against mg-0049" column.  That identification is the one thing here a
# reader has to accept, and it is stated rather than buried.
# =========================================================================================
_ROW = re.compile(r"^\|\s*`(Q\d)`/`(R\d)`\s*\|(?P<mut>[^|]*)\|"
                  r"[^|]*?exit\s*(?P<bee1>\d)[^|]*\|[^|]*?exit\s*(?P<r0049>\d)[^|]*\|",
                  re.M)
_OBS = re.compile(r"^\s*!!\s+(Q\d)\s+.*?expected exit (\d).*?got exit (\d)", re.M)


def v6_r1r2_table(rev=None, rerun_text=None, cov_text=None):
    cov = at(rev, COV) if cov_text is None else cov_text
    rerun = at(rev, RERUN) if rerun_text is None else rerun_text
    claimed = {m.group(1): (int(m.group("bee1")), int(m.group("r0049")))
               for m in _ROW.finditer(cov)}
    observed = {m.group(1): (int(m.group(2)), int(m.group(3))) for m in _OBS.finditer(rerun)}
    if not claimed:
        return None, "    COVERAGE.md has no `Qn`/`Rn` exit-code table row at this revision"
    lines = [f"    population: the {len(claimed)} rows of COVERAGE.md's Q/R table; "
             f"grain: an (against-mg-bee1, against-mg-0049) exit-code pair.",
             f"    the observed pairs come from {RERUN} — mg-5644's OWN battery, re-run "
             f"unmodified."]
    agree = True
    for q in sorted(claimed):
        c = claimed[q]
        o = observed.get(q)
        ok = o == c
        agree &= ok
        lines.append(f"      {q}  COVERAGE.md says {c}   the transcript says "
                     f"{o if o else '(row absent)'}   {'agree' if ok else 'DISAGREE'}")
    missing = [q for q in claimed if q not in observed]
    if missing:
        lines.append(f"      {len(missing)} claimed row(s) have no observation: {missing}")
    return bool(agree and not missing), "\n".join(lines)


# =========================================================================================
# V7  claims16eb.py:194 — mg-0049's README: mg-218d's and mg-5644's batteries are "re-run in
#     section 7 of run_all.sh".
#
# RESOLVED, NOT READ.  The section that re-runs mg-5644's battery is found by its COMMAND,
# never by its title: a first draft of this shape (mg-65eb's, and it says so) asked whether
# section 7's TITLE mentioned `218d` and got the wrong answer, because section 7 is
# `coverage218d.py` — a different program of the same audit.  A population picked by a token
# that appears NEAR the thing is the defect this whole arc is about.
# =========================================================================================
def _sections(body):
    out, cur = {}, None
    for line in body.split("\n"):
        m = re.match(r'^echo "### (\d+)\.\s*(.+?)"\s*$', line)
        if m:
            cur = int(m.group(1))
            out[cur] = [m.group(2), []]
        elif cur is not None and line.strip() and not line.startswith(("echo", "#")):
            out[cur][1].append(line.strip())
    return {k: (v[0], v[1]) for k, v in out.items()}


def v7_section_pointer(rev=None, rdm_text=None):
    sections = _sections(at(rev, RUN))
    rdm = at(rev, RDM) if rdm_text is None else rdm_text
    runs_5644 = [n for n, (_t, c) in sections.items()
                 if any("state_delegation_audit_5644/run_all.sh" in x for x in c)]
    rows = [ln for ln in rdm.split("\n")
            if ln.startswith("| mg-218d's 16-mutation battery")
            or ln.startswith("| mg-5644's own battery")]
    said = sorted({int(x) for r in rows for x in re.findall(r"section (\d+)", r)})
    lines = [f"    population: the {len(rows)} README rows that assert a section number; "
             f"grain: a section ordinal of {RUN}.",
             f"    the rows assert section(s): {said}",
             f"    the section whose COMMAND re-runs mg-5644's battery: {runs_5644}",
             f"    section 7 is in fact {sections.get(7, ('(absent)', []))[0][:56]!r}"]
    if not rows:
        return None, "\n".join(lines) + "\n    no README row makes this claim at this revision"
    if not runs_5644:
        return None, "\n".join(lines) + "\n    no section re-runs mg-5644's battery — WITHHELD"
    ok = bool(set(said) <= set(runs_5644)) and bool(said)
    lines.append(f"    every asserted number is a section that really runs it: {ok}")
    return ok, "\n".join(lines)


# =========================================================================================
# V8  claims16eb.py:217 — render0049.py's R5: "`<details>` at the top SUPPRESSES NOTHING:
#     every cited section is still on the page as the document's own prose".
#
# TWO CONJUNCTS AND THEY ARE MEASURED SEPARATELY, because separating them is the whole
# finding: "still on the page" is about BYTES and "suppresses nothing" is about a READER.
# Stage 1 asks whether R5 still asserts the reader half; mg-a74f narrowed it, so on a
# repaired tree this row is RESPECIFIED rather than green.
# =========================================================================================
def v8_r5_details(rev=None, have_node=None, r49_text=None, prefix="<details>\n\n"):
    """`prefix` is the construction, exposed for the same reason as v4's: with
    `<details open>` a reader IS shown every cited section and this verdict must come out the
    other way.  If it does not, the row is not measuring what it says."""
    text = at(rev, R49) if r49_text is None else r49_text
    m = re.search(r"^    R5(.*?)^    R\d", text, re.M | re.S)
    if m is None:
        return None, "    render0049.py has no R5 row at this revision"
    body = m.group(1)
    asserts = "SUPPRESSES NOTHING" in body and "until mg-a74f" not in body
    if not asserts:
        return None, (
            "    the sentence this row is about is NOT ASSERTED at this revision.\n"
            f"    R5 still contains the phrase `SUPPRESSES NOTHING`: "
            f"{'SUPPRESSES NOTHING' in body}\n"
            f"    R5 disclaims it (`until mg-a74f`):                 "
            f"{'until mg-a74f' in body}\n"
            "    RESPECIFIED — the row was narrowed to the bytes-on-the-page property and\n"
            "    now says in as many words that a reader is shown none of them.")
    if have_node is False:
        return None, "    R5 asserts it here and the renderers are absent — UNPROBED."
    doc = prefix + at(rev, TARGET)
    markers = _markers(doc)
    lines, named_false, measured_true = [], [], []
    for eng in ENGINES:
        shown, in_bytes, total, reasons = _shown_and_bytes(eng, doc, markers)
        lines.append(f"    {eng:<12s} bytes on the page {in_bytes}/{total}    "
                     f"SHOWN to a reader {shown}/{total}")
        if reasons:
            lines.append(f"    {'':<12s} because: {sorted(set(reasons.values()))[0]}")
        named_false.append(shown == 0)
        measured_true.append(in_bytes == total)
    lines.append(f"    `SUPPRESSES NOTHING` (a reader): "
                 f"{'REFUTED on both renderers' if all(named_false) else 'not refuted'}")
    lines.append(f"    `still on the page` (the bytes): "
                 f"{'TRUE on both renderers' if all(measured_true) else 'not true'}")
    return not all(named_false), "\n".join(lines)


# The six, in the order `claims16eb.py` prints them.  `flip_0120.py` iterates THIS list, so a
# row added to the file and not to the list is a row the flip harness never sees — which is
# why the list is here and not there.
SIX = [
    ("claims16eb.py:94", "the two tables cannot drift apart quietly in EITHER direction",
     v3_two_tables),
    ("claims16eb.py:142", "exit 1 is \"a region ... NO LONGER PRESENTED TO A READER\"",
     v4_exit_semantics),
    ("claims16eb.py:156", "presentation.py: nothing changed except one message and four "
     "self-test cases", v5_presentation_diff),
    ("claims16eb.py:178", "COVERAGE.md's R1/R2 table: exit 0 against mg-bee1, exit 1 "
     "against mg-0049", v6_r1r2_table),
    ("claims16eb.py:194", "both batteries \"re-run in section 7 of run_all.sh\"",
     v7_section_pointer),
    ("claims16eb.py:217", "R5: `<details>` at the top SUPPRESSES NOTHING", v8_r5_details),
]
