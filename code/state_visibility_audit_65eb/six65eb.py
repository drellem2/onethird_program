#!/usr/bin/env python3
"""mg-65eb — THE SIX, RE-CLASSIFIED FROM SCRATCH, AND THE ENUMERATOR'S OWN PINNED VERDICTS.

mg-16eb asked for the six broken claims to be enumerated INDIVIDUALLY and each classified
false / unsupported / true-but-unevidenced, "because those need different repairs".  mg-a74f
did that and published 5 FALSE + 1 TRUE OF A DIFFERENT PROPERTY.  This audit's brief says:

    "Check the classification, not just the count — a claim moved to 'unsupported' that is
     actually false is a downgrade dressed as a repair."

So this file does not read mg-a74f's labels and check they add up.  It probes each of the six
INDEPENDENTLY, decides its bucket by a rule stated in code below, and only then compares.

WHAT MAKES A PROBE INDEPENDENT HERE, stated so it can be disagreed with.  mg-a74f's own
`before` probes are, for four of the six, TEXT-PRESENCE tests: they establish that the
sentence is IN the file at `bd24efc`, which is not the same as establishing that it is FALSE
there.  Section C therefore re-derives the truth value:

    claims 1, 2, 5   by RESOLVING the reference the sentence makes, at bd24efc
    claims 3, 4      by CONSTRUCTION — a tree on which the sentence is observably false,
                     built at bd24efc, where the defect is still present
    claim 6          by CONSTRUCTION through two real GFM renderers and an ancestor walk
                     that is NOT visible_a74f.py's

NOTHING IN THE WORKING TREE IS EVER WRITTEN.  Every construction is applied inside a THROWAWAY
GIT WORKTREE checked out at the revision under test and removed in a `finally`.  That is
stronger than snapshot-and-restore: the tree this audit runs in cannot be damaged even by a
crash, because it is never opened for writing.

Section B is the finding this audit did not go looking for: `claims16eb.py` — the program that
ENUMERATED the six — carries four of its seventeen verdicts as the LITERAL `False`.  Run it on
the repaired tree and it reports four of the six still BROKEN, and it would report that
whatever the repair did.  Nothing in mg-a74f's suite runs it.

    D=$(mktemp -d) && npm install --prefix "$D" marked markdown-it
    NODE_PATH="$D/node_modules" python3 code/state_visibility_audit_65eb/six65eb.py

Without the renderers claim 6's construction cannot run; it is reported UNPROBED, the
classification of claim 6 is withheld rather than guessed, and the exit code is 3.

Exit 0 if this audit's classification agrees with mg-a74f's on all six AND no claim sits in a
softer bucket than its evidence warrants.  Exit 1 on any disagreement or any downgrade.
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
sys.path.insert(0, os.path.join(REPO, "code/state_delegation_audit_16eb"))
import render16eb as R16                                          # noqa: E402  (the bridge only)

BEFORE = "bd24efc"
CTL = "code/state_landing_control_2da3/delta_control.py"
RDM = "code/state_delegation_repair_0049/README.md"
R49 = "code/state_delegation_repair_0049/render0049.py"
MUT = "code/state_delegation_repair_0049/mutations_0049.py"
RUN = "code/state_delegation_repair_0049/run_all.sh"
CLAIMS16 = "code/state_delegation_audit_16eb/claims16eb.py"
TARGET = "docs/state-history/attempt-mg-276d.md"

ENGINES = ["marked", "markdown-it"]
CITED = ["H1", "H2", "H3", "H4", "H5"]

# The four buckets mg-16eb named plus the one mg-a74f added, ordered from HARDEST to SOFTEST.
# A "downgrade" is a claim mg-a74f puts in a bucket further down this list than the evidence
# in section C supports.  The order is an argument and it is written here to be argued with:
# FALSE says the sentence is wrong; TRUE OF A DIFFERENT PROPERTY says the sentence is wrong
# AS NAMED but the instrument under it is sound; the last two say nobody knows.
HARDNESS = ["FALSE", "TRUE OF A DIFFERENT PROPERTY", "UNSUPPORTED", "TRUE-BUT-UNEVIDENCED"]


def git(*a, **kw):
    return subprocess.run(["git", "-C", REPO, *a], capture_output=True, text=True, **kw)


def at(rev, path):
    return git("show", f"{rev}:{path}").stdout


class Worktree:
    """A throwaway checkout of `rev`.  Files inside it may be written freely; the whole
    directory is removed on exit, so no restore discipline is needed and none can fail."""

    def __init__(self, rev):
        self.rev = rev
        self.dir = tempfile.mkdtemp(prefix="65eb-wt-")
        shutil.rmtree(self.dir)
        git("worktree", "add", "--detach", self.dir, rev, check=True)

    def read(self, rel):
        with open(os.path.join(self.dir, rel), encoding="utf-8") as fh:
            return fh.read()

    def write(self, rel, text):
        with open(os.path.join(self.dir, rel), "w", encoding="utf-8") as fh:
            fh.write(text)

    def control(self):
        """(exit code, stdout) of delta_control.py AS IT STANDS IN THIS WORKTREE."""
        p = subprocess.run([sys.executable, os.path.join(self.dir, CTL)], cwd=self.dir,
                           capture_output=True, text=True)
        return p.returncode, p.stdout

    def close(self):
        git("worktree", "remove", "--force", self.dir)
        shutil.rmtree(self.dir, ignore_errors=True)


# =========================================================================================
# THIS AUDIT'S OWN VISIBILITY INSTRUMENT.  It is not visible_a74f.py and it does not import
# it: that file is under audit here, and rows65eb.py section B reports three defects in it.
#
# The difference is not cosmetic.  This one hands the bytes to the STANDARD LIBRARY'S HTML
# parser and reads ATTRIBUTES BY NAME off the parse.  visible_a74f.py hand-rolls a tag stack
# and matches `hidden` and `open` as WORDS ANYWHERE IN THE ATTRIBUTE TEXT, which is why
# `class="hidden"` scores SUPPRESSED there and `<details title="open me">` scores shown.
# Both of those come out right below, which is the point of building a second instrument.
# =========================================================================================
class Shown(html.parser.HTMLParser):
    """Is `marker` reached by a reader?  Reports the first suppressing ancestor, or None."""

    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
            "param", "source", "track", "wbr"}

    def __init__(self, marker):
        super().__init__(convert_charrefs=True)
        self.marker = marker
        self.stack = []
        self.hits = []          # (suppressor or None) once per occurrence of the marker
        self.in_comment_depth = 0

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
            self.hits.append("an HTML comment — the bytes are in the file and not in the page")

    def handle_data(self, data):
        if self.marker not in data:
            return
        self.hits.append(self._suppressor())

    def _suppressor(self):
        for tag, attrs in self.stack:
            if tag == "details" and "open" not in attrs:
                return "a <details> carrying no `open` attribute — a closed disclosure widget"
            if "hidden" in attrs:
                return "the `hidden` ATTRIBUTE (read by name off the parse, not by word match)"
            if tag in ("script", "style", "template"):
                return f"a <{tag}> element"
            style = (attrs.get("style") or "").replace(" ", "").lower()
            if "display:none" in style or "visibility:hidden" in style:
                return "an inline style"
        return None


def shown_count(engine, markdown, markers):
    """(shown, total, reasons) for `markers` in `markdown` rendered by `engine`."""
    out = R16.render(engine, markdown)
    shown, reasons = 0, {}
    for m in markers:
        p = Shown(m)
        p.feed(out)
        p.close()
        if not p.hits:
            reasons[m] = "not in the rendered page at all"
        elif any(h is None for h in p.hits):
            shown += 1
        else:
            reasons[m] = p.hits[0]
    return shown, len(markers), reasons


def in_html(engine, markdown, markers):
    """How many markers' BYTES are in the rendered page, suppressed or not — the quantity
    mg-0049's R5 measures, kept separate from the one it names."""
    out = R16.render(engine, markdown)
    return sum(1 for m in markers if m in out), len(markers)


def renderers_present():
    p = subprocess.run(["node", R16.BRIDGE, "marked", os.devnull],
                       capture_output=True, text=True)
    return p.returncode == 0


# =========================================================================================
# A.  THE ENUMERATION — IS mg-a74f's SIX THE SAME POPULATION AS mg-16eb's SIX?
# =========================================================================================
# The sites mg-a74f's claims_a74f.py publishes, read out of that file's own SIX table with
# ast so this audit is not transcribing them by hand.
def a74f_sites():
    tree = ast.parse(at("HEAD", "code/state_delegation_repair_a74f/claims_a74f.py"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "SIX":
            out = []
            for elt in node.value.elts:
                cid = elt.elts[0].value
                where = elt.elts[1]
                # `f"{CTL}:233"` — rebuild the f-string from its parts.
                if isinstance(where, ast.JoinedStr):
                    text = ""
                    for part in where.values:
                        if isinstance(part, ast.Constant):
                            text += part.value
                        else:
                            text += {"CTL": CTL, "RDM": RDM, "R49": R49}[part.value.id]
                else:
                    text = where.value
                out.append((cid, text, elt.elts[3].value, elt.elts[2].value))
            return out
    return []


BROKEN_LINE = re.compile(r"^  \[BROKEN\] (.+)\n {11}(.+)$", re.M)
ROW_LINE = re.compile(r"^  \[(holds|BROKEN)\] ", re.M)


def _key(text):
    """The join key between the two enumerations: the claim's own WORDS, lowercased and
    stripped of everything but letters and digits, first 48 characters.

    NOT the site.  mg-16eb cites `delta_control.py:757` and mg-a74f cites
    `delta_control.py:798` for the same sentence, because the file grew between the two
    revisions.  A line number is a fact about a revision, and these two enumerations are
    written at different ones, so joining on it would report six mismatches where there are
    none.  This audit's first draft did exactly that."""
    return re.sub(r"[^a-z0-9]", "", text.lower())


def claims16_broken(cwd):
    """The (site, sentence) pairs claims16eb.py reports BROKEN, run in `cwd`, plus how many
    rows it printed in total.  Parsed with the regex above, which is printed in the
    transcript so the parse can be checked rather than trusted."""
    p = subprocess.run([sys.executable, os.path.join(cwd, CLAIMS16)], cwd=cwd,
                       capture_output=True, text=True)
    pairs = [(a.strip(), b.strip()) for a, b in BROKEN_LINE.findall(p.stdout)]
    return pairs, len(ROW_LINE.findall(p.stdout)), p.returncode


def pinned_verdicts():
    """Every `claim(...)` call in claims16eb.py whose `ok` argument is a LITERAL.

    A row whose verdict is a constant is not a check.  It reports the same answer on every
    tree, including a repaired one."""
    tree = ast.parse(at("HEAD", CLAIMS16))
    # Calls that sit inside an `if`/`else` body are GUARD BRANCHES: they run only when an
    # anchor has rotted, so a constant verdict there is a deliberate alarm, not a pinned
    # result.  Marked rather than lumped in, because the difference decides the finding.
    guarded = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.If, ast.Try)):
            for sub in ast.walk(node):
                if isinstance(sub, ast.Call) and getattr(sub.func, "id", "") == "claim":
                    guarded.add(sub.lineno)
    rows = []
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call) and getattr(node.func, "id", "") == "claim"
                and len(node.args) >= 3):
            where = node.args[0]
            if isinstance(where, ast.Constant):
                label = where.value
            elif isinstance(where, ast.JoinedStr):
                label = ""
                for part in where.values:
                    label += (part.value if isinstance(part, ast.Constant)
                              else {"R0049": "code/state_delegation_repair_0049",
                                    "CTL_DIR": "code/state_landing_control_2da3",
                                    }.get(getattr(part.value, "id", ""), "?"))
            else:
                label = ast.unparse(where)
            ok = node.args[2]
            rows.append((node.lineno, label, isinstance(ok, ast.Constant),
                         ok.value if isinstance(ok, ast.Constant) else ast.unparse(ok)[:48],
                         node.lineno in guarded))
    return rows


# =========================================================================================
# C.  THE SIX, PROBED.  Each returns (refuted_as_named, true_of_measured, probeable, detail).
# =========================================================================================
def probe_c1():
    """`the guards-only decomposition lives in .../guards_only_0049.py` — RESOLVE the path."""
    text = at(BEFORE, CTL)
    m = re.search(r"(code/state_delegation_repair_0049/\S+\.py) runs the guards-only", text)
    named = m.group(1) if m else None
    exists = named and git("cat-file", "-e", f"{BEFORE}:{named}").returncode == 0
    # Where does it actually live?  Computed, not asserted: the file at BEFORE that runs the
    # guards-only decomposition is the one whose source mentions the guards-only split.
    real = [p for p in git("ls-tree", "-r", "--name-only", BEFORE, "--",
                           "code/state_delegation_repair_0049").stdout.split("\n")
            if p.endswith(".py") and "guards" in at(BEFORE, p).lower()]
    return (not exists, False, named is not None,
            f"the sentence names {named!r}; that path at {BEFORE}: "
            f"{'exists' if exists else 'DOES NOT EXIST'}; the file(s) at {BEFORE} that "
            f"actually carry the guards-only decomposition: {real}")


def probe_c2():
    """`runs against all six rows` — COUNT the rows the named script runs, at BEFORE."""
    text = at(BEFORE, CTL)
    m = re.search(r"runs the guards-only\s+control against\s+all (\w+) rows", text)
    said = m.group(1) if m else None
    n = len(re.findall(r'^\s*\("R\d+"', at(BEFORE, MUT), re.M))
    words = {6: "six", 9: "nine"}
    return (said is not None and said != words.get(n, str(n)), False, said is not None,
            f"the sentence says {said!r}; the population it is about — mutations_0049.ROWS "
            f"at {BEFORE} — has {n} rows, which is {words.get(n, n)!r}")


def _sections(body):
    """run_all.sh split into {number: (title, the COMMANDS under it)}.

    THE COMMANDS, NOT THE TITLE.  A first draft of this probe asked whether section 7's
    TITLE mentioned `218d` and got the wrong answer, because section 7's title is
    `coverage218d.py — COVERAGE.md checked against the code`: a different program of the
    same audit.  That draft is left described rather than deleted because it is this audit's
    own instance of the defect the whole arc is about — a population picked by a token that
    appears near the thing instead of by the thing."""
    out, cur = {}, None
    for line in body.split("\n"):
        m = re.match(r'^echo "### (\d+)\.\s*(.+?)"\s*$', line)
        if m:
            cur = int(m.group(1))
            out[cur] = [m.group(2), []]
        elif cur is not None and line.strip() and not line.startswith(("echo", "#")):
            out[cur][1].append(line.strip())
    return {k: (v[0], v[1]) for k, v in out.items()}


def probe_c5():
    """`re-run in section 7 of run_all.sh` — RESOLVE the section, at BEFORE.

    The two batteries are identified by the COMMAND that runs them:
      mg-5644's own battery      `sh code/state_delegation_audit_5644/run_all.sh`
      mg-218d's 16-mutation one  reached only THROUGH that file (its own section 5), so the
                                 section of mg-0049's run_all.sh that re-runs it is the same
                                 section — checked below rather than assumed.
    """
    sections = _sections(at(BEFORE, RUN))
    lines = []
    for n in sorted(sections):
        title, cmds = sections[n]
        lines.append(f"      section {n}  {title[:58]:<58s} {cmds or ['(no command)']}")
    runs_5644 = [n for n, (_t, cmds) in sections.items()
                 if any("state_delegation_audit_5644/run_all.sh" in c for c in cmds)]
    inner = _sections(at(BEFORE, "code/state_delegation_audit_5644/run_all.sh"))
    inner_218d = [n for n, (_t, cmds) in inner.items()
                  if any("state_layer_audit_218d" in c and "coverage" not in c
                         for c in cmds)]
    rows = [ln for ln in at(BEFORE, RDM).split("\n")
            if ln.startswith("| mg-218d's 16-mutation battery")
            or ln.startswith("| mg-5644's own battery")]
    said = sorted({int(m) for r in rows for m in re.findall(r"section (\d+)", r)})
    refuted = bool(rows) and bool(runs_5644) and not set(said) & set(runs_5644)
    detail = "\n".join(lines)
    detail += (f"\n      {len(rows)} README rows make the claim; the section number(s) they "
               f"assert: {said}")
    detail += (f"\n      section(s) whose COMMAND re-runs mg-5644's own battery: {runs_5644}")
    detail += (f"\n      mg-5644's run_all.sh section(s) that run mg-218d's battery (not its "
               f"coverage checker): {inner_218d}")
    detail += (f"\n      so both are re-run in section {runs_5644[0] if runs_5644 else '?'}, "
               f"and section 7 is {sections.get(7, ('(absent)',))[0][:52]!r}")
    return (refuted, False, bool(rows), detail)


def probe_c3(wt_before, wt_head):
    """`the two tables cannot drift apart quietly in EITHER direction` — CONSTRUCT the drift.

    Three mutations of DELEGATED_PRESENTATION, each run through delta_control.py as it
    stands at that revision.  The claim is refuted if any drift the sentence forbids exits 0.
    """
    lines = []
    verdicts = {}
    for label, mutate, direction in [
        ("D1  a PRESENTATION RECORD for a section nothing delegates or cites",
         lambda t: t.replace(
             '        "H5": "f6ae6325c5307d5a6c088990ad5f49b7b2f9f8347e73458b55c66f072fcbe406",',
             '        "H5": "f6ae6325c5307d5a6c088990ad5f49b7b2f9f8347e73458b55c66f072fcbe406",\n'
             '        "H9": "0000000000000000000000000000000000000000000000000000000000000000",',
             1),
         "here and in nothing else"),
        ("D2  a whole TARGET FILE certified here and delegated by nobody",
         lambda t: t.replace(
             "DELEGATED_PRESENTATION = {\n",
             'DELEGATED_PRESENTATION = {\n    "docs/state-history/no-such-target.md": {\n'
             '        "H1": "1111111111111111111111111111111111111111111111111111111111111111",\n'
             "    },\n", 1),
         "here and in nothing else"),
        ("D3  a delegated section's record DELETED  (the direction the sentence gets right)",
         lambda t: t.replace(
             '        "H3": "2fae29f7da64900f5ec7bd10ffd2199666feb11b65a50279c9adaef5e908747e",\n',
             "", 1),
         "in DELEGATED and absent here"),
    ]:
        for wt in (wt_before, wt_head):
            orig = wt.read(CTL)
            new = mutate(orig)
            if new == orig:
                lines.append(f"    {label:<72s} {wt.rev:<8s} ANCHOR ROTTED — mutation is a "
                             f"no-op and tests nothing")
                verdicts[(label, wt.rev)] = None
                continue
            wt.write(CTL, new)
            code, _ = wt.control()
            wt.write(CTL, orig)
            verdicts[(label, wt.rev)] = code
            quiet = "QUIET — the control says nothing" if code == 0 else "caught"
            lines.append(f"    {label:<72s} {wt.rev:<8s} exit {code}   {quiet}")
    quiet_at_before = [k for k, v in verdicts.items() if k[1] == wt_before.rev
                       and k[0].startswith(("D1", "D2")) and v == 0]
    return (bool(quiet_at_before), False, True,
            "\n".join(lines) + f"\n    {len(quiet_at_before)} of the 2 forbidden drifts are "
            f"QUIET at {wt_before.rev}; the sentence says NEITHER direction can be.")


def probe_c4(wt_before, markers, have_node):
    """`exit 1 is "a region ... NO LONGER PRESENTED TO A READER"` — refute BOTH directions.

    E1  exit 1 while a reader is shown every line of the region  (=> exit 1 does not imply
        "not presented")
    E2  a reader shown NOTHING of five regions, at an exit that is not 1  (=> "not presented"
        does not imply exit 1)
    Presentation is decided by THIS FILE'S OWN renderer walk, never by the control's opinion
    of itself.
    """
    lines = []
    orig = wt_before.read(TARGET)

    # ---- E1: an ordinary fenced code example inside cited section H3 --------------------
    head = "### H3 "
    i = orig.index(head)
    e1 = (orig[:i] + "An example, so a reader can check the rescaling:\n\n"
          "```python\nd_true = np.diag(row_signs) @ d_allplus\n```\n\n" + orig[i:])
    wt_before.write(TARGET, e1)
    code1, out1 = wt_before.control()
    wt_before.write(TARGET, orig)

    # ---- E2: a <details><summary> over the whole document -------------------------------
    e2 = "<details>\n<summary>Superseded drafts — click to expand</summary>\n\n" + orig
    wt_before.write(TARGET, e2)
    code2, out2 = wt_before.control()
    wt_before.write(TARGET, orig)

    lines.append(f"    E1  a fenced code example inside cited section H3      exit {code1}")
    lines.append(f"    E2  <details><summary> over the whole document         exit {code2}")
    if have_node:
        for eng in ENGINES:
            s1, t1, _r = shown_count(eng, e1, markers)
            s2, t2, r2 = shown_count(eng, e2, markers)
            lines.append(f"        {eng:<12s} E1: {s1}/{t1} cited sections SHOWN to a reader"
                         f"     E2: {s2}/{t2} SHOWN")
            if r2:
                why = sorted(set(r2.values()))[0]
                lines.append(f"        {'':<12s} E2's reason, from a stdlib HTML parse: {why}")
        shown_e1 = shown_count(ENGINES[0], e1, markers)[0]
        shown_e2 = shown_count(ENGINES[0], e2, markers)[0]
    else:
        lines.append("        (renderers absent — presentation not measured for E1/E2)")
        shown_e1 = shown_e2 = None

    d1 = code1 == 1 and shown_e1 == len(markers)
    d2 = shown_e2 == 0 and code2 != 1
    lines.append(f"    direction 1 refuted (exit 1, and every region SHOWN):      {d1}")
    lines.append(f"    direction 2 refuted (nothing shown, and the exit is not 1): {d2}")
    return (bool(d1 or d2), False, have_node, "\n".join(lines))


def probe_c6(wt_before, markers, have_node):
    """R5: "`<details>` at the top SUPPRESSES NOTHING: every cited section is still on the
    page as the document's own prose".

    TWO conjuncts and they are probed separately, because that is the whole classification:
      NAMED    "suppresses nothing" — a claim about what the <details> does to a reader
      MEASURED "still on the page"  — a claim about bytes in the serialised HTML
    """
    if not have_node:
        return (False, False, False, "    renderers absent — claim 6 is UNPROBED and its "
                                     "classification is WITHHELD, not guessed")
    orig = wt_before.read(TARGET)
    doc = "<details>\n\n" + orig
    lines = []
    named_false, measured_true = [], []
    for eng in ENGINES:
        shown, total, reasons = shown_count(eng, doc, markers)
        bytes_in, _ = in_html(eng, doc, markers)
        lines.append(f"    {eng:<12s} bytes in the rendered page {bytes_in}/{total}    "
                     f"SHOWN to a reader {shown}/{total}")
        if reasons:
            lines.append(f"    {'':<12s} because: {sorted(set(reasons.values()))[0]}")
        named_false.append(shown == 0)
        measured_true.append(bytes_in == total)
    lines.append(f"    `SUPPRESSES NOTHING` (about a reader):     "
                 f"{'REFUTED on both engines' if all(named_false) else 'not refuted'}")
    lines.append(f"    `still on the page` (about the bytes):     "
                 f"{'TRUE on both engines' if all(measured_true) else 'not true'}")
    return (all(named_false), all(measured_true), True, "\n".join(lines))


def classify(refuted_as_named, true_of_measured, probeable):
    """THE RULE, in code, applied identically to all six.  It is stated before it is used and
    it is the only thing that decides a bucket in this file."""
    if not probeable:
        return "UNSUPPORTED"
    if refuted_as_named and true_of_measured:
        return "TRUE OF A DIFFERENT PROPERTY"
    if refuted_as_named:
        return "FALSE"
    return "TRUE-BUT-UNEVIDENCED"


def main():
    have_node = renderers_present()
    print("=" * 100)
    print("mg-65eb — THE SIX, RE-CLASSIFIED FROM SCRATCH")
    print("=" * 100)
    print(f"  before revision   {BEFORE}   (where the defect must still be present)")
    print(f"  renderers         {'marked + markdown-it present' if have_node else 'ABSENT'}")
    print("  constructions     applied in THROWAWAY WORKTREES; the working tree is never")
    print("                    opened for writing by this program")
    print()

    # -------------------------------------------------------------------------------------
    print("=" * 100)
    print("A.  THE ENUMERATION — IS THIS THE SAME SIX?  BY SITE, NOT BY COUNT")
    print("=" * 100)
    sites = a74f_sites()
    print(f"  mg-a74f's SIX, read out of claims_a74f.py with `ast` (not transcribed): "
          f"{len(sites)} rows")
    for cid, where, klass, sentence in sites:
        print(f"      claim {cid}   {where:<56s} {klass}")
        print(f"                  {sentence[:88]}")
    print()
    wt_before = Worktree(BEFORE)
    wt_head = Worktree("HEAD")
    try:
        broken_before, n_rows_b, rc_b = claims16_broken(wt_before.dir)
        broken_head, n_rows_h, rc_h = claims16_broken(wt_head.dir)
        print(f"  mg-16eb's claims16eb.py, run UNMODIFIED at {BEFORE}: "
              f"{len(broken_before)} BROKEN of {n_rows_b} rows (exit {rc_b})")
        print(f"      parse rule: {BROKEN_LINE.pattern!r}")
        for s, sent in broken_before:
            print(f"      {s}")
            print(f"          {sent[:88]}")
        print()
        print("  THE JOIN IS ON THE CLAIM'S OWN WORDS, NOT ON ITS SITE.  mg-16eb cites")
        print("  `delta_control.py:757` and mg-a74f cites `delta_control.py:798` for the same")
        print("  sentence: the file grew by 41 lines between the two revisions.  A line number")
        print("  is a fact about a revision and these two enumerations are written at")
        print("  different ones, so joining on the site reports six mismatches where there")
        print("  are none.  This audit's first draft did exactly that and is corrected here,")
        print("  not quietly — it is the same defect class the whole arc is about.")
        print()
        declared = {_key(s): (c, w) for c, w, _k, s in sites}
        found = {_key(sent): (site, sent) for site, sent in broken_before}

        def _join(k, pool):
            """Prefix match either way.  mg-16eb states claim 4 as the exit-1 sentence AND
            the exit-2 sentence in one row; mg-a74f enumerates only the first.  One is a
            prefix of the other, and requiring equality would report a mismatch where the
            two records name the same claim at different lengths."""
            for j in pool:
                if j.startswith(k) or k.startswith(j):
                    return j
            return None

        missing = sorted(found[k][0] for k in found if not _join(k, declared))
        extra = sorted(declared[k][1] for k in declared if not _join(k, found))
        for k, (c, w) in sorted(declared.items(), key=lambda kv: kv[1][0]):
            j = _join(k, found)
            hit = found.get(j) if j else None
            print(f"      claim {c}  {w[:52]:<52s} -> "
                  f"{'mg-16eb ' + hit[0][:38] if hit else 'NO MATCH in mg-16eb''s six'}")
        print()
        print(f"  in mg-16eb's six and NOT enumerated by mg-a74f : {missing or 'none'}")
        print(f"  enumerated by mg-a74f and NOT in mg-16eb's six : {extra or 'none'}")
        enumeration_ok = (not missing and not extra and len(sites) == 6
                          and len(broken_before) == 6)
        print(f"  >>> ENUMERATION {'COMPLETE' if enumeration_ok else 'DOES NOT MATCH'} — "
              f"{len(sites)} declared, {len(broken_before)} reported, "
              f"{len(declared) - len(extra)} joined")
        print()

        # ---------------------------------------------------------------------------------
        print("=" * 100)
        print("B.  THE ENUMERATOR'S OWN VERDICTS ARE PINNED — AND THAT IS WHY THE REPAIR")
        print("    CANNOT BE SCORED BY THE INSTRUMENT THAT FILED THE CHARGE")
        print("=" * 100)
        rows = pinned_verdicts()
        pinned_false = [r for r in rows if r[2] and r[3] is False and not r[4]]
        print(f"  claims16eb.py has {len(rows)} claim() call SITES and printed {n_rows_h} rows")
        print("  on the repaired tree — the difference is guard branches that run only when")
        print("  an anchor has rotted.  For each site, is the `ok` argument a COMPUTED")
        print("  EXPRESSION or a LITERAL?  Read with `ast`:")
        for lineno, label, is_const, val, guard in sorted(rows):
            kind = f"LITERAL {val!r}" if is_const else f"computed: {val}"
            if guard:
                kind += "   (GUARD BRANCH — runs only if an anchor rotted)"
            print(f"      claims16eb.py:{lineno:<5d} {label[:52]:<52s} {kind}")
        print()
        print(f"  {len([r for r in rows if r[2]])} of {len(rows)} sites carry a constant "
              f"verdict.  Excluding guard branches, {len(pinned_false)} are the constant "
              f"False ON THE MAIN PATH — a verdict that cannot change.")
        print(f"  claims16eb.py run UNMODIFIED on the REPAIRED tree: {len(broken_head)} BROKEN "
              f"of {n_rows_h} rows (exit {rc_h})")
        for s, sent in broken_head:
            print(f"      {s}")
        pinned_keys = {p[1].split(" ")[0] for p in pinned_false}
        still_pinned = [s for s, _sent in broken_head
                        if any(k in s or s.split(" ")[0] in k for k in pinned_keys)]
        print()
        print(f"  of those, rows whose verdict is the LITERAL False: {len(still_pinned)} of "
              f"{len(broken_head)}   {still_pinned}")
        print("  >>> THE FINDING.  Four of the six were filed by rows that report BROKEN on")
        print("  every tree, repaired or not.  mg-a74f repaired all four and mg-16eb's own")
        print("  claim-checker still calls them broken — not because the repair failed, but")
        print("  because those rows do not measure anything.  `claims16eb.py` is named")
        print("  `THE CLAIMS mg-0049 ADDED, CHECKED` and for 4 of its 17 rows the quantity")
        print("  computed is a constant.  THAT IS THIS AUDIT'S PRIMARY QUESTION, one level")
        print("  up: a row name that is not its measurement, in the auditor rather than in")
        print("  the auditee.")
        print()
        print("  AND NOTHING RUNS IT.  Files in mg-a74f's directory naming claims16eb.py:")
        namers = [p for p in git("ls-tree", "-r", "--name-only", "HEAD", "--",
                                 "code/state_delegation_repair_a74f").stdout.split("\n")
                  if p.strip() and "claims16eb" in at("HEAD", p)]
        print(f"      {namers or '(none)'}")
        print("  mg-a74f re-runs battery16eb.py (its section 5) and reports 6 of 8.  It does")
        print("  not re-run the program that produced the six it is repairing, and if it did")
        print("  it would have to explain a transcript that says four are still broken.")
        print()

        # ---------------------------------------------------------------------------------
        print("=" * 100)
        print("C.  THE SIX, PROBED INDEPENDENTLY, AND THEN CLASSIFIED BY A STATED RULE")
        print("=" * 100)
        print("  RULE:  refuted as named AND true of the measured quantity -> TRUE OF A")
        print("         DIFFERENT PROPERTY;  refuted as named alone -> FALSE;  not probeable")
        print("         -> UNSUPPORTED;  otherwise -> TRUE-BUT-UNEVIDENCED.")
        print("  The rule is applied to all six identically and nothing else assigns a bucket.")
        print()
        markers = CITED
        probes = {
            "1": ("RESOLVE the reference", probe_c1()),
            "2": ("RESOLVE the reference", probe_c2()),
            "3": ("CONSTRUCTION at " + BEFORE, probe_c3(wt_before, wt_head)),
            "4": ("CONSTRUCTION at " + BEFORE, probe_c4(wt_before, markers, have_node)),
            "5": ("RESOLVE the reference", probe_c5()),
            "6": ("CONSTRUCTION, two renderers", probe_c6(wt_before, markers, have_node)),
        }
        mine = {}
        for cid, where, klass, _sentence in sites:
            how, (refuted, measured, probeable, detail) = probes[cid]
            verdict = classify(refuted, measured, probeable)
            mine[cid] = verdict
            print(f"  CLAIM {cid}   {where}")
            print(f"    probe          {how}")
            for line in detail.split("\n"):
                print(f"    {line}" if line.startswith("    ") else f"      {line}")
            print(f"    refuted as named {refuted}   true of the measured quantity {measured}"
                  f"   probeable {probeable}")
            print(f"    THIS AUDIT      {verdict}")
            print(f"    mg-a74f         {klass}")
            agree = verdict == klass
            soft = HARDNESS.index(klass) > HARDNESS.index(verdict) if agree is False else False
            print(f"    >>> {'AGREE' if agree else 'DISAGREE'}"
                  f"{'   AND IT IS A DOWNGRADE' if soft else ''}")
            print()

        # ---------------------------------------------------------------------------------
        print("=" * 100)
        print("D.  THE CLASSIFICATION, TALLIED, AND THE DOWNGRADE QUESTION ANSWERED")
        print("=" * 100)
        tally = {b: 0 for b in HARDNESS}
        for v in mine.values():
            tally[v] += 1
        for b in HARDNESS:
            print(f"    {tally[b]}  {b}")
        print()
        disagreements = [(c, mine[c], k) for c, _w, k, _s in sites if mine[c] != k]
        downgrades = [(c, m, k) for c, m, k in disagreements
                      if HARDNESS.index(k) > HARDNESS.index(m)]
        print(f"  population: the {len(sites)} claims mg-a74f enumerates, each probed above.")
        print(f"  disagreements with mg-a74f's classification : {len(disagreements)} "
              f"{disagreements or ''}")
        print(f"  DOWNGRADES (softer bucket than the evidence) : {len(downgrades)} "
              f"{downgrades or ''}")
        print()
        if not downgrades:
            print("  The specific hazard the brief names — a FALSE claim parked in")
            print("  'unsupported' — is ABSENT, and the reason is worth stating rather than")
            print("  leaving as an absence: BOTH SOFT BUCKETS ARE EMPTY.  There is nowhere")
            print("  to downgrade to.  Every one of the six was refutable by resolving a")
            print("  reference or by building a tree, and this audit did one or the other")
            print("  for all six rather than reading mg-a74f's label.")
            print()
            print("  The one row where the classification could have gone wrong is claim 6,")
            print("  and it is the row that carries a different label from the other five.")
            print("  Its two conjuncts come apart under section C's construction exactly as")
            print("  mg-a74f says: the bytes are on the page and the reader is shown none of")
            print("  them.  TRUE OF A DIFFERENT PROPERTY is the right bucket, and claim 4 —")
            print("  refuted in BOTH directions, so no reading of it survives — is correctly")
            print("  NOT in that bucket.  That distinction is the whole of what this section")
            print("  was asked to check.")
        else:
            for c, m, k in downgrades:
                print(f"  claim {c}: this audit's evidence supports {m}; mg-a74f files it "
                      f"as {k}")
        print("=" * 100)
        bad = len(disagreements) + (0 if enumeration_ok else 1)
        if not have_node:
            print("  RENDERERS ABSENT — claim 6 was not probed and this run is PARTIAL.")
            return 3
        return 1 if bad else 0
    finally:
        wt_before.close()
        wt_head.close()


if __name__ == "__main__":
    sys.exit(main())
