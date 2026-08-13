"""PINNABLE -- THE PRE-CONDITION ON mg-20ee's CONDITIONS 1-3.

mg-20ee's method for pinning a transcript has three conditions, in this order:

    1.  git merge-base --is-ancestor <declared-commit> origin/main   -- YES
    2.  the transcript reproduces byte-identically AT that commit
    3.  every instrument that RUNS this one is re-measured (consumers.py)

All three assume the question has already been settled.  This file asks it:

    0.  IS A PIN THE REMEDY FOR THIS INSTRUMENT'S DRIFT AT ALL?

WHY THIS EXISTS, AND IT IS NOT A HYPOTHETICAL.  mg-20ee's 44 candidates were
nominated by census.py, which is a classifier FOR FOREIGN ADDRESSES -- so an
address-only difference is exactly what it went looking for.  Working the
remaining work-list IN ITS OWN DRIFT ORDER, mg-4020 took the two cheapest
instruments on it and NEITHER IS PINNABLE, for two different reasons:

    code/species_repair_a4ef        2+/5-.  Its whole drift is three lines
                                    naming `__pycache__` directories in
                                    SIBLING trees.  Those are in .gitignore,
                                    so they are in NO COMMIT, and no AS_OF
                                    can restore them.  MEASURED BOTH WAYS at
                                    HEAD with no pin whatever: create the
                                    three empty directories and the committed
                                    transcript reproduces BYTE-IDENTICALLY;
                                    remove them and the 2+/5- returns.  The
                                    transcript is a function of WHICH SUITES
                                    THE OPERATOR HAS RUN, not of repo state.

    code/state_relocation_audit_b0ae  7+/7-.  ALREADY PINNED -- libb0ae.py
                                    declares OLD_REV=78ae4d9 and
                                    NEW_REV=cc4c663 and reads every input
                                    through `git show <rev>:<path>`.  Its
                                    drift is entirely in B8.2, a section its
                                    own runner header declares to be "about
                                    the repo as it stands".  A pin there
                                    would not repair the section; it would
                                    DELETE THE QUESTION THE SECTION ASKS.

A third, for contrast, IS reachable by a pin: code/landscape_repair_1953,
whose drift is a walk of docs/ that has gone `23` -> `44` occurrences as the
corpus grew from 267 to 530 files.  Those addresses are tracked files.  That
is the shape mg-20ee's remedy was built for.

    SO THE POPULATION IS NOT 26 PINNINGS.  Whether it is mostly pinnings is
    NOT KNOWN AND IS NOT CLAIMED HERE -- three instruments is three
    instruments.  What is established is that the work-list is a list of
    instruments whose transcripts DRIFT, and that "drifts" and "wants an
    AS_OF" are different properties, so the second must be measured per
    instrument rather than inherited from membership of the list.
    mg-54b1's sweep reached the same conclusion from the other direction on
    an UNSELECTED sample, which is why this is written down as a rule and
    not as an anecdote.

    THE METHOD, STATED SO THAT IT CAN BE ARGUED WITH:

      * INPUT IS A DIFF, NOT A GUESS.  This reads `git diff -- <subject>` in
        the worktree as it stands, so you must have RUN the suite and NOT yet
        restored it.  An empty diff is REFUSED rather than reported clean:
        nothing to classify is not the same as nothing to fix, and this
        instrument has no way to tell a reproducing suite from one you forgot
        to run.  ground_truth.sh already makes exactly this run.

      * R1  IGNORED ADDRESS.  A changed line names a path that `git
        check-ignore` matches.  Git is configured never to track it, so it is
        in no commit, so NO AS_OF PIN REACHES IT.  Both `<path>` and
        `<path>/` are tested, because `__pycache__/` in .gitignore carries a
        trailing slash and matches DIRECTORIES ONLY -- `check-ignore` returns
        1 for the same path written without it, and a rule that tested one
        form would have missed the instance this was built from.

      * R2  ALREADY PINNED.  A tracked script in the subject carries a 7-to-40
        character hex token that `git cat-file -e` RESOLVES IN THIS
        REPOSITORY.  Resolution is what makes this a rule rather than a
        regex: `deadbeef` and an eight-letter word are both hex-shaped, and
        only a real object means somebody declared a revision.

      * R2 OVER-COUNTS, DECLARED AND MEASURED ON THE FIRST SUBJECT IT MET.
        It fires on a declared revision ANYWHERE in the subject's scripts,
        and a revision may be a CONTROL's rather than the corpus read's:
        species_repair_a4ef declares ebecd89 and 83ac472 in s1_extent.py,
        which are its controls (a) and (b) reading the PRE-REPAIR trees, and
        its corpus read is not pinned at all.  So R2 firing means "a revision
        is declared here, go and read why", and a rule that could tell a
        control's revision from a corpus pin would be a rule about the
        difference between an instrument's subject and its evidence -- which
        is not decidable from the token.  The bias is stated rather than
        tuned away, in the form census.py states its two.

      * NEITHER RULE IS A VERDICT.  R1 says a pin cannot remove THAT LINE.
        R2 says a pin already EXISTS.  Both are reasons to stop and look
        before spending the forty-five minutes conditions 1-3 cost; neither
        says the instrument is healthy, and R2 in particular is compatible
        with the instrument being badly wrong.

    AND THE BLIND SPOT, WHICH IS THE POINT OF WRITING THE METHOD DOWN:

      * R1 READS ADDRESSES, SO A BARE COUNT IS INVISIBLE TO IT.  This is not
        a supposition: species_repair_a4ef's own drift has TWO hunks, and the
        second is `9 stated, 0 not stated` -> `6 stated, 0 not stated` --
        the same defect, carrying no path at all.  R1 catches that instrument
        only because its FIRST hunk lists the directories.  An instrument
        that printed the count and not the list would be in this blind spot
        entirely, and would look like clean residue.
      * R2 CONFIRMS A PIN, NOT ITS COVERAGE.  b0ae is pinned and drifts
        anyway, which is the instance R2 was built from -- so R2 firing tells
        you where to read, not what to conclude.
      * RESIDUE IS NOT A PROMISE.  A drift this file cannot attribute to
        either rule may still be a moved verdict, a dead runner, or an
        operator-specific absolute path -- mg-20ee's own tranche 1 hit all
        three.  Residue means "conditions 1-3 are worth starting", nothing
        more.
      * THE DIFF IS THE ONLY EVIDENCE.  An instrument that writes outside its
        own directory, or that writes nothing at all because its runner is
        dead, produces a diff this file will read at face value.  mg-54b1
        measured that exact failure -- `NOTHING CHANGED` is not `IT
        REPRODUCED` -- and no rule here detects it.

    THE BLIND-SPOT LIST ABOVE IS LOAD-BEARING AND IS NOT TO BE TIDIED AWAY,
    for the reason consumers.py states one file over: a triage rule with no
    stated blind spot is indistinguishable, to its reader, from a verdict.
    THIS IS A PREFILTER.  THE BACKSTOP IS CONDITIONS 1-3 THEMSELVES -- search
    for the AS_OF and measure both directions -- and if you skip them because
    this file printed RESIDUE, you have used it as the opposite of what it is.

    sh code/asof_census_20ee/run_all.sh          # NOT run there: needs a
                                                # suite to have been run
    sh code/species_repair_a4ef/run_all.sh
    python3 code/asof_census_20ee/pinnable.py code/species_repair_a4ef
    git checkout -- code/species_repair_a4ef
"""

import io
import os
import re
import subprocess
import sys
import tokenize

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "..", ".."))

# A repository-shaped path token: at least one `/`, no whitespace.  Deliberately
# looser than census.py's ADDR, which requires BOTH a known extension and a
# `:line` -- the instance this file was built from addresses a DIRECTORY with
# neither.  A trailing `:123` is stripped; trailing punctuation is not part of
# a path.
PATHTOK = re.compile(r"(?:[A-Za-z0-9_.\-]+/)+[A-Za-z0-9_.\-]+")
HEXTOK = re.compile(r"\b[0-9a-f]{7,40}\b")

# R3.  An enumeration of the filesystem whose ORDER the repository does not
# determine.  `grep` is matched with a following short-flag cluster containing
# r or R, and tolerantly, because a Python subject spells it as a LIST --
# ["grep", "-rn", "-E", pat] -- with quotes and a comma between the two tokens.
WALK = re.compile(
    r"""\bgrep\b[^\n]{0,24}?-[A-Za-z]*[rR]        # grep -r / -rn / "grep", "-rn"
      | \bos\.(?:walk|listdir|scandir)\s*\(
      | \.iterdir\s*\(
      | \bglob\.(?:glob|iglob)\s*\(
      | \bfind\s+[^\n|]*-(?:type|name)\b          # shelled-out find(1)
    """, re.X)
# The negative half.  git sorts its own output, so `git grep` and `git ls-files`
# are ORDERED READS OF A COMMIT and must never fire; nor may a walk the subject
# has already ordered itself.  Without this half R3 fires on every correct
# instrument in the estate, including the repaired form it exists to recommend.
ORDERED = re.compile(r"git\s+(?:grep|ls-files)|sorted\s*\(|\|\s*sort\b")


def _blank(s):
    """`s` with every non-space character replaced by a space.

    COLUMNS ARE PRESERVED ON PURPOSE.  R3's window is computed from the walk's
    own INDENTATION, so a blanking that shortened lines would move the boundary
    it scans to and silence hits for a reason that has nothing to do with prose.
    """
    return re.sub(r"\S", " ", s)


def _blank_comments(src, shell):
    """Blank every comment, tracking quote state so a `#` in a string survives.

    Per line and deliberately so: this is the FALLBACK for a fragment or a file
    Python cannot parse, and a scanner that carried quote state across lines
    would turn one unbalanced quote into a file-long blanking.  A shell `#`
    starts a comment only at a word boundary -- `grep '#'` and `a#b` are not
    comments, and `sed -e s/#//` is an argument.
    """
    out = []
    for ln in src.split("\n"):
        quote, cut = None, None
        for i, ch in enumerate(ln):
            if quote:
                if ch == quote:
                    quote = None
                continue
            if ch in "'\"":
                quote = ch
            elif ch == "#" and (not shell or i == 0 or ln[i - 1] in " \t;&|()"):
                cut = i
                break
        out.append(ln if cut is None else ln[:cut] + _blank(ln[cut:]))
    return "\n".join(out)


def _blank_prose_py(src):
    """Blank Python's comments and DOCSTRINGS, or report that it could not.

    ASKING THE LANGUAGE RATHER THAN GUESSING AT IT, which is R2's shape one
    rule over: `tokenize` is Python's own answer to "is this a comment", the
    way `git cat-file -e` is git's own answer to "is this a revision".  A
    regex for `#` cannot tell a comment from a `#` inside a regex, and this
    file's own WALK pattern contains one.

    A DOCSTRING IS A STRING STANDING ALONE AS A STATEMENT, and no other string
    is touched -- which is the boundary that keeps P5 alive.  The only subject
    R3 has ever had spells its invocation as string literals in a list,
    `["grep", "-rn", ...]`, so a rule that blanked STRINGS would go blind to
    the one form it was built to see: an under-count, and the silent direction.

    Returns (text, True), or (src, False) when the source does not tokenize --
    a fragment, or a file this Python cannot parse.  THE FAILURE IS RETURNED
    RATHER THAN SWALLOWED because falling back to comments alone restores the
    docstring half of the over-count, and a repair that quietly stops applying
    is worse than one that never did.
    """
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(src).readline))
    except Exception:
        return src, False
    lines = src.split("\n")
    kill, sig = [], []
    for t in toks:
        if t.type == tokenize.COMMENT:
            kill.append((t.start, t.end))
        elif t.type not in (tokenize.NL, tokenize.INDENT, tokenize.DEDENT):
            sig.append(t)
    starts_line = True
    for i, t in enumerate(sig):
        if t.type == tokenize.STRING and starts_line:
            nxt = sig[i + 1] if i + 1 < len(sig) else None
            if nxt is None or nxt.type == tokenize.NEWLINE:
                kill.append((t.start, t.end))
        starts_line = t.type == tokenize.NEWLINE
    for (sr, sc), (er, ec) in kill:
        sr, er = sr - 1, er - 1
        if sr == er:
            lines[sr] = lines[sr][:sc] + _blank(lines[sr][sc:ec]) + lines[sr][ec:]
        else:
            lines[sr] = lines[sr][:sc] + _blank(lines[sr][sc:])
            for r in range(sr + 1, er):
                lines[r] = _blank(lines[r])
            lines[er] = _blank(lines[er][:ec]) + lines[er][ec:]
    return "\n".join(lines), True


def code_only(src, path=None):
    """`src` with its PROSE blanked out -- R3's corpus, and not its text.

    THE BOUNDARY IS `TEXT THE INTERPRETER NEVER EXECUTES`, which is a fact
    about the language rather than a judgement about intent.  Comments and
    docstrings are that text.  A string passed to a call is NOT, because
    nothing here can tell `print("grep -rn ...")` from
    `run(["grep", "-rn", ...])` without knowing which callee executes -- and
    a rule that special-cased `print` would be silently incomplete the moment
    a subject narrates through `banner()` or `sys.stdout.write`.  That residue
    is MEASURED rather than assumed away: 2 of the 83 surviving hits at
    12aa5f8 are prose inside a `print(...)`, and permuted.py's section 4
    prints them.

    Returns (text, separated) -- `separated` is False when the docstring half
    could not run.
    """
    if path is not None and path.endswith(".sh"):
        return _blank_comments(src, shell=True), True
    out, ok = _blank_prose_py(src)
    if ok:
        return out, True
    return _blank_comments(src, shell=False), False


def git(*args):
    got = subprocess.run(["git", "-C", ROOT, *args], capture_output=True)
    if got.returncode != 0:
        raise SystemExit("pinnable: git %s failed: %s"
                         % (" ".join(args),
                            got.stderr.decode("utf-8", "replace").strip()))
    return got.stdout.decode("utf-8", "surrogateescape")


def is_ignored(path):
    """True when git is CONFIGURED never to track `path`.

    Both `path` and `path + "/"` are tested.  `.gitignore`'s `__pycache__/`
    carries a trailing slash and so matches directories only; `check-ignore`
    answers 1 for the same path written without one, and the instance this
    rule exists for -- `code/species_7d75/__pycache__`, as a4ef prints it --
    is written without one.  Testing a single form silently halves the rule.
    """
    for form in (path, path.rstrip("/") + "/"):
        got = subprocess.run(["git", "-C", ROOT, "check-ignore", "-q", form],
                             capture_output=True)
        if got.returncode == 0:
            return True
    return False


def changed_lines(diff_text):
    """The added and removed lines of a unified diff, without its headers.

    `+++`/`---` are excluded: a diff header names the file under change, and
    counting it would make every diff address its own instrument.
    """
    out = []
    for ln in diff_text.splitlines():
        if ln[:3] in ("+++", "---") or not ln:
            continue
        if ln[0] in "+-":
            out.append(ln)
    return out


def addresses_of(diff_text):
    """Every distinct repository-shaped path token in a diff's changed lines."""
    seen = []
    for ln in changed_lines(diff_text):
        for tok in PATHTOK.findall(ln):
            tok = tok.rstrip(".,;:)")
            if tok and tok not in seen:
                seen.append(tok)
    return seen


def declared_revs(text, resolves):
    """Hex tokens in `text` that `resolves` accepts as real objects.

    `resolves` is injected so the control can plant a source without needing
    the planted revision to exist here.  RESOLUTION IS THE RULE: a regex over
    hex alone fires on `deadbeef`, on `accede`, and on the first eight
    characters of a hash printed in prose, and this rule is asserting that
    somebody DECLARED A REVISION.
    """
    return [t for t in dict.fromkeys(HEXTOK.findall(text)) if resolves(t)]


def unordered_walks(text, path=None, prose="none"):
    """Lines that enumerate the filesystem in an order no commit determines.

    `prose` selects WHICH OF THREE RULES is being asked, so that all three can
    be counted SIDE BY SIDE the way permuted.py prints `set` beside `bag` -- a
    repair whose before is not printed beside its after is an assertion, and a
    rejected design quoted rather than re-taken is the `18 of 129` shape:

        "read"      mg-0e77's rule, character for character.  Prose included.
        "comments"  THE HALF-REPAIR, KEPT SO IT CAN BE RE-MEASURED AND NOT
                    MERELY REPORTED AS REJECTED.  It is wrong, it is wrong in
                    a direction nobody would look at, and permuted.py's
                    section 4 prints the hit it ADDS.
        "none"      the rule.  Comments and docstrings both.

    MEASURED, NOT REASONED ABOUT (mg-0e77).  `grep -rn` emits hits in
    directory-enumeration order.  On the filesystem this repository lives on
    that order is a deterministic function of the SET OF NAMES -- two trees
    built from the same 191 paths in OPPOSITE creation order enumerate
    identically, and four consecutive runs agree -- so it is stable, and it is
    also not sorted, not `git ls-files` order, and not derivable from the
    commit by any portable rule.  It is the filesystem's, and the filesystem is
    in no commit.

    THE CONSEQUENCE IS ABOUT CONDITION 2, NOT ABOUT WHETHER TO PIN.  The only
    form that reads a corpus AT a commit is `git grep <rev>`, and git SORTS.
    So pinning a `grep -r` corpus necessarily permutes the transcript, and
    mg-20ee's condition 2 -- "reproduces byte-identically" -- CANNOT be met by
    a correct pin.  Read byte-identity as BAG-IDENTITY PLUS A DECLARED
    PERMUTATION for a subject R3 fires on, or a correct pin reads as a failed
    one -- and `bag` rather than `set`, because a set forgets MULTIPLICITY and
    the transcripts this rule fires on repeat addresses (mg-885d).  The hand
    figures this docstring used to quote -- `18 of 129` and `30 of 149` -- are
    not reproduced by anything and are not repeated; permuted.py takes that
    measurement, and takes it three ways because `permuted` does not pick one.

    AND IT READS CODE, NOT PROSE (mg-e5f3).  The rule matched the invocation
    wherever it appeared, so A SENTENCE NAMING THE INVOCATION FIRED IT, and in
    an estate where every docstring explains its own method that is not a rare
    shape: 9 of 92 hits at 12aa5f8, in 8 files.  It landed hardest on
    audit_scope_text.py -- THE INSTRUMENT TRANCHE 4 REPAIRED AND PINNED, whose
    only two hits were comments explaining the defect it no longer has -- so
    condition 0 told a repaired instrument to expect a permuted transcript,
    which is N9's own rationale failing by PROSE instead of by the git form.

    THE TWO PROSE SURFACES MOVE TOGETHER, AND THAT WAS MEASURED RATHER THAN
    ARGUED.  Blanking COMMENTS ALONE ADDS A HIT -- to this very file: the walk
    line at the top of this docstring was suppressed by a `sorted(` that lives
    in the block comment below, so removing comments removes the SUPPRESSOR
    and un-silences a line no operator could act on.  A repair introducing the
    defect it repairs, in the half nobody would have looked at.  Blanking
    comments AND docstrings: 92 -> 83 hits, 9 removed, ZERO ADDED.
    """
    raw = text.splitlines()
    if prose == "read":
        lines = raw
    elif prose == "comments":
        lines = _blank_comments(text, shell=bool(path and path.endswith(".sh"))
                                ).splitlines()
    else:
        lines = code_only(text, path)[0].splitlines()
    hits = []
    for i, ln in enumerate(lines):
        if not WALK.search(ln) or ORDERED.search(ln):
            continue
        # THE SORT IS ROUTINELY NOT ON THE WALK'S OWN LINE, and this was
        # MEASURED rather than allowed for: pointed at the two instruments
        # mg-20ee's tranche 1 pinned to byte-identity, this rule fired on both
        # -- absent_step_7ae5 and anchor_drift_96df each `os.walk` into a list
        # and `return sorted(out)` seven or eight lines below.  A per-line test
        # would have called two clean pins defective, which is tranche 3's 94%
        # over-count arriving inside the rule written from it.
        #
        # THE WINDOW IS A SYNTACTIC BOUNDARY AND DELIBERATELY NOT A LINE COUNT:
        # scan to the end of the enclosing block -- the next line at or left of
        # the walk's own indentation that opens something new.  A number tuned
        # to fit 7 and 8 would be a threshold guessed from the two cases it was
        # built from, which is the shape this arc keeps landing commits about.
        indent = len(ln) - len(ln.lstrip())
        span = [ln]
        for nxt in lines[i + 1:]:
            if nxt.strip():
                nid = len(nxt) - len(nxt.lstrip())
                if nid < indent or (nid == indent
                                    and re.match(r"\s*(def|class)\b", nxt)):
                    break
            span.append(nxt)
        if not any(ORDERED.search(s) for s in span):
            # THE ORIGINAL LINE, NOT THE BLANKED ONE.  An operator asked to go
            # and read why must be shown the text that is in the file; a hit
            # printed with its trailing comment shaved off would be a second
            # thing to reconcile against the source.
            hits.append(raw[i].strip())
    return hits


def resolver():
    def resolves(tok):
        got = subprocess.run(["git", "-C", ROOT, "cat-file", "-e",
                              tok + "^{commit}"], capture_output=True)
        return got.returncode == 0
    return resolves


def main(subject):
    subject = subject.rstrip("/")
    diff_text = git("diff", "--", subject)
    if not diff_text.strip():
        raise SystemExit(
            "pinnable: `git diff -- %s` is EMPTY, and this instrument\n"
            "  classifies a drift it is given rather than one it produces.\n"
            "  RUN THE SUITE FIRST and do not restore it:\n"
            "      sh %s/run_all.sh\n"
            "  An empty diff is refused rather than reported clean, because a\n"
            "  suite that reproduces and a suite you forgot to run look the\n"
            "  same from here -- which is mg-54b1's `NOTHING CHANGED is not IT\n"
            "  REPRODUCED`, and this file has no way to tell them apart."
            % (subject, subject))

    scripts = [p for p in git("ls-files", "--", subject).splitlines()
               if p.endswith(".py") or p.endswith(".sh")]

    print("=" * 78)
    print("mg-4020 -- IS A PIN THE REMEDY?  %s" % subject)
    print("=" * 78)
    print()
    print("  mg-20ee condition 0, asked BEFORE conditions 1-3 are paid for.")
    print("  METHOD AND BLIND SPOT are in this file's docstring and are not")
    print("  repeated here; what is repeated is the sentence that matters --")
    print("  THIS IS A PREFILTER AND NOT A VERDICT.  See the residue section.")
    print()
    print("  THIS INSTRUMENT ANSWERS ITS OWN THREE RULES AND THE ANSWERS ARE")
    print("  PRINTED RATHER THAN LEFT TO BE FOUND.  R2 fires on its own")
    print("  directory: census.py declares AS_OF = 5a62e8c.  And its OUTPUT")
    print("  carries ignored addresses whenever R1 does, so a committed")
    print("  transcript of this file is itself a document R1 would flag.")
    print("  Neither is a defect; both are the reason the rules are stated as")
    print("  `go and read why` rather than as verdicts.")
    print()
    own = sum(len(unordered_walks(git("show", "HEAD:%s" % p), p))
              for p in git("ls-files", "--", os.path.dirname(
                  os.path.relpath(os.path.abspath(__file__), ROOT))).splitlines()
              if p.endswith(".py") or p.endswith(".sh"))
    # COUNTED, NOT ASSERTED.  This sentence read `SIX TIMES` as a literal until
    # mg-e5f3 added controls to selftest_20ee.py, each of which plants a needle
    # and moves the number.  A self-hit count written as prose is a figure that
    # goes stale the next time somebody adds a control -- which is the class
    # mg-30bd's census exists to count, in the file arguing that rules must be
    # measured rather than stated.
    print("  R3 FIRES ON THIS DIRECTORY %d TIME(S) AND EVERY ONE IS FALSE, and"
          % own)
    print("  that is checked here rather than left for a reader: 1 hit is R3's")
    print("  OWN REGEX SOURCE and the rest are its controls' planted needles.")
    print("  This is the README's section 4 -- a control that plants its own probe")
    print("  into the corpus it searches -- for the FOURTH time in this arc,")
    print("  and section 4's remedy DOES NOT APPLY: it says assemble the")
    print("  needle at runtime, and a DETECTOR FOR A TOKEN CANNOT AVOID")
    print("  CONTAINING THAT TOKEN.  R1 and R2's self-hits above are TRUE and")
    print("  R3's are FALSE, which is the sharper statement of why none of the")
    print("  three is a verdict: they read TEXT, not behaviour.")
    print()
    print("  IT IS ALSO NOT PINNED AND NOT ON A BUILD PATH, DELIBERATELY.  It")
    print("  reads HEAD and the LIVE worktree diff because it must answer")
    print("  about the tree you are ABOUT TO CHANGE -- consumers.py's")
    print("  declaration, for the same reason.  It cannot go in run_all.sh")
    print("  because it REQUIRES a suite to have been run and not restored,")
    print("  which is a state no build path should be in.")
    print()

    lines = changed_lines(diff_text)
    addrs = addresses_of(diff_text)
    print("  changed lines: %d      distinct path tokens in them: %d"
          % (len(lines), len(addrs)))
    print("  subject scripts read for a declared revision: %d" % len(scripts))
    print()

    ignored = [a for a in addrs if is_ignored(a)]

    print("-" * 78)
    print("R1  IGNORED ADDRESSES -- git is configured never to track these,")
    print("    so they are in NO COMMIT and NO AS_OF PIN REACHES THEM")
    print("-" * 78)
    print()
    for a in ignored:
        print("      %s" % a)
    if not ignored:
        print("      none.  Which is NOT evidence that the drift is repo state:")
        print("      R1 reads ADDRESSES, and a drift that moved only a COUNT")
        print("      carries none.  species_repair_a4ef's own second hunk is")
        print("      exactly that shape.")
    print()

    resolves = resolver()
    pinned = []
    for s in scripts:
        for rev in declared_revs(git("show", "HEAD:%s" % s), resolves):
            pinned.append((s, rev))

    print("-" * 78)
    print("R2  DECLARED REVISIONS IN THE SUBJECT'S OWN SCRIPTS -- if these")
    print("    exist, SOMETHING HERE IS ALREADY PINNED")
    print("-" * 78)
    print()
    for s, rev in pinned:
        print("      %-52s %s" % (s, rev))
    if not pinned:
        print("      none")
    print()
    if pinned:
        print("  A REVISION IS DECLARED HERE AND THE TRANSCRIPT DRIFTS ANYWAY.")
        print("  READ THE INSTRUMENT BEFORE PINNING FURTHER:")
        print("  state_relocation_audit_b0ae is pinned twice over and its")
        print("  runner header DECLARES the exception -- B8.2 is 'about the")
        print("  repo as it stands', and pinning it would not repair the")
        print("  section, it would delete the question it asks.")
        print()
        print("  BUT THIS RULE OVER-COUNTS, DECLARED: a revision may be a")
        print("  CONTROL's rather than the corpus read's.  MEASURED on the")
        print("  first subject it met -- species_repair_a4ef's ebecd89 and")
        print("  83ac472 are its controls (a) and (b) reading the PRE-REPAIR")
        print("  trees, and its corpus read is not pinned at all.  R2 says GO")
        print("  AND READ WHY, and it does not say the corpus is pinned.")
        print()

    walks, prose_only, unseparated = [], [], []
    for s in scripts:
        src = git("show", "HEAD:%s" % s)
        if not code_only(src, s)[1]:
            unseparated.append(s)
        code_hits = unordered_walks(src, s)
        for ln in code_hits:
            walks.append((s, ln))
        for ln in unordered_walks(src, s, prose="read"):
            if ln not in code_hits:
                prose_only.append((s, ln))

    print("-" * 78)
    print("R3  UNORDERED WALKS -- the subject enumerates the filesystem, so")
    print("    its transcript's LINE ORDER is in no commit")
    print("-" * 78)
    print()
    for s, ln in walks:
        print("      %-52s %s" % (s, ln[:60]))
    if not walks:
        print("      none.  Every corpus read this rule can see is either an")
        print("      ordered read of a commit (`git grep`, `git ls-files`) or")
        print("      sorted by the subject itself.")
    print()
    if prose_only:
        print("  AND %d LINE(S) THAT THE RULE FIRED ON BEFORE mg-e5f3 AND DOES"
              % len(prose_only))
        print("  NOT NOW -- PROSE NAMING THE INVOCATION, printed rather than")
        print("  silently dropped, because a repair that removes hits without")
        print("  showing which ones is indistinguishable from one that broke:")
        print()
        for s, ln in prose_only:
            print("      %-52s %s" % (s, ln[:60]))
        print()
        if not walks:
            print("  THIS SUBJECT'S ONLY R3 HITS WERE PROSE.  Before mg-e5f3 the")
            print("  verdict below carried `+R3: expect a permuted transcript`")
            print("  for sentences DESCRIBING an enumeration this subject does")
            print("  not do -- N9's rationale (`every repaired instrument in the")
            print("  estate is told it is still defective`) arriving by prose.")
            print()
    if unseparated:
        print("  %d SCRIPT(S) COULD NOT BE SEPARATED FROM THEIR PROSE -- Python"
              % len(unseparated))
        print("  could not tokenize them, so only their comments were removed")
        print("  and the DOCSTRING half of the over-count is still live here.")
        print("  Printed because a repair that quietly stops applying is worse")
        print("  than one that never did:")
        for s in unseparated:
            print("      %s" % s)
        print()
    if walks:
        print("  THIS IS A RULE ABOUT CONDITION 2, NOT ABOUT WHETHER TO PIN.")
        print("  The only form that reads a corpus AT a commit is")
        print("  `git grep <rev>`, and git SORTS its output; `grep -r` emits")
        print("  DIRECTORY-ENUMERATION order, which is a function of the")
        print("  filesystem and of no commit.  So a CORRECT pin here will")
        print("  permute the transcript, and mg-20ee's `reproduces")
        print("  byte-identically` cannot be met by it.")
        print()
        print("  READ CONDITION 2 AS BAG-IDENTITY PLUS A DECLARED PERMUTATION,")
        print("  AND `BAG` IS NOT A SYNONYM FOR THE `SET` THIS FILE USED TO")
        print("  PRINT: a set forgets MULTIPLICITY, and mg-3b51's own pinned")
        print("  transcript prints one address twice while mg-1953's prints one")
        print("  three times, so a pin dropping one occurrence would move an")
        print("  address and the count it belongs to and score IDENTICAL.")
        print("  DO NOT EYEBALL IT -- permuted.py scores it:")
        print("      python3 code/asof_census_20ee/permuted.py <transcript> <rev>")
        print()
        print("  The `18 of 129` and `30 of 149` this file used to quote were")
        print("  hand counts and NEITHER REPRODUCES.  Re-taken mechanically the")
        print("  two pins are 21 of 129 and 26 of 148 core positions, 9 and 11")
        print("  lines that MUST move; `18` is neither, and nobody could tell")
        print("  WHICH QUANTITY it had been.  Both pins still hold -- the")
        print("  verdict did not move, only the figure nothing stood behind.")
        print()
        print("  AND R3 IS NOT A REASON NOT TO PIN.  The order was never a")
        print("  function of repo state, so the permutation is the transcript")
        print("  BECOMING repo-valued -- it is the repair, priced.")
        print()

    print("-" * 78)
    print("RESIDUE -- what a pin is CAPABLE of reaching.  NOT A PROMISE")
    print("-" * 78)
    print()
    residue = [a for a in addrs if a not in ignored]
    print("  %d of %d path token(s) are not ignored." % (len(residue), len(addrs)))
    print()
    print("  This is where conditions 1-3 BEGIN, not where they are answered.")
    print("  A residual drift may still be a moved verdict, a dead runner, or")
    print("  an absolute path that reproduced for exactly one operator --")
    print("  mg-20ee's tranche 1 hit all three, and none of them is a pin.")
    print("  IF YOU SKIP CONDITIONS 1-3 BECAUSE THIS SECTION IS NON-EMPTY,")
    print("  YOU HAVE USED THIS FILE AS THE OPPOSITE OF WHAT IT IS.")
    print()

    if ignored:
        verdict = "NOT WHOLLY PINNABLE -- %d ignored address(es)" % len(ignored)
    elif pinned:
        verdict = "ALREADY PINNED -- %d declared revision(s)" % len(pinned)
    else:
        verdict = "NO PRE-CONDITION FIRED -- proceed to conditions 1-3"
    # R3 never DECIDES the verdict.  It says the acceptance test needs
    # rewording, not that a pin is the wrong remedy, and folding it into the
    # headline would make it the third thing here that reads as one.
    if walks:
        verdict += "  (+R3: expect a permuted transcript)"
    print("=" * 78)
    print("PINNABLE: %s" % verdict)
    print("=" * 78)
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: pinnable.py <instrument-dir>   "
                         "(run its suite first, and do not restore it)")
    sys.exit(main(sys.argv[1]))
