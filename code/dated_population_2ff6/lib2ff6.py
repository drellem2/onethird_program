"""mg-2ff6 -- the instrument for ADOPTING THE DATED-POPULATION CONVENTION.

WHAT THIS FILE MAY AND MAY NOT CONTAIN.  This ticket ADOPTS a convention that
another ticket decided and another ticket's checker enforces.  A library that
re-decides the convention, or re-implements the checker, has turned an adoption
into a second opinion -- and a second opinion that agrees today is worse than
the first (cfd9c's own words about `lib_f8e5` importing `lib_1abe`).  So:

  IMPORTED, NEVER RESTATED.
    `libfd9c`   -- `pop`, `render_figure`, `state_of`, `CLASSES`, `at`,
                   `file_stats`, `census_from`, `weight_of`, `census`.  THE
                   CONVENTION IS cfd9c's.  Every dated population line this
                   ticket adds anywhere in the arc is printed by `libfd9c.pop`,
                   which has no form that omits the ref, and every class comes
                   from `libfd9c.state_of`, which takes two booleans.
    `lib56dc`    -- `count_rows`.  The row rule is the population of the whole
                   accounting; a diff of count rows computed by a second rule
                   would be a measurement of my re-typing.
    `lib03d1`    -- `read`, `git`, `head`, `all_transcripts`.

  EXTRACTED, NOT RE-TYPED.
    `corpus_label_rx()` lifts the LITERAL SOURCE of cfd9c's `CORPUS_LABEL` out
    of `s4_convention.py` and compiles it.  The checker is inline in a probe
    and importing a probe runs it, so there is no import to make -- but there
    is also no excuse for a second copy.  If cfd9c's selector changes, mine
    changes with it, and if the extraction fails the probe goes RED rather than
    falling back on a stale copy (`d0` holds it against a known answer).

    `s4c()` runs `s4_convention.py` AS A SUBPROCESS and returns its stdout.
    That is the whole of my use of the checker: I do not import it, edit it,
    respecify it, or re-run cfd9c's suite.  The ticket's trap is that cfd9c
    already respecified this checker once after it failed on cfd9c's own tree;
    the second time would be mine, so there is no code here that could.

  WRITTEN HERE, AND WHY EACH IS NOT A COPY.

    `PUBLISHED_AT`  the ref the moved figures are moving FROM.  A hard-coded
                    ref, deliberately: a published figure's date is a constant
                    by definition, and the one thing it must not do is track a
                    moving branch tip.  `audit_c067`'s `git log main -n 40` is
                    what the other choice looks like three hundred commits
                    later (mg-f8e5 / d2).
    `sectioned`     count rows tagged with the SECTION they were printed in --
                    because cfd9c's rule makes the section the unit, and an
                    accounting that matched rows by label alone would pair two
                    different figures that happen to share a label.  Two rows
                    in `out_a6_self.txt` are both `...count ROWS in them`.
    `diff_rows`     the accounting itself: published value, new value, delta,
                    per figure.  Not a census -- a census is what moved; this
                    is WHICH figure moved and BY HOW MUCH, which is what the
                    ticket asks for and what no probe in the arc prints.

WHAT THIS TREE DOES OUTSIDE ITS OWN DIRECTORY.  It EDITS AND RE-RUNS EIGHT
TRANSCRIPTS IN TWO OTHER TREES and edits FOUR TRACKED `.md` FILES, and that is the
ticket.  Saying `nothing outside this directory was written` is not available
to me and I will not print a check that pretends otherwise; what replaces it is
`d1`, which names every figure that moved.  No probe HERE writes anything: the
edits are made by hand, committed, and then measured.
"""

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FD9C = os.path.join(REPO, "code", "corpus_fixedpoint_fd9c")

sys.path.insert(0, FD9C)

import libfd9c as F              # noqa: E402  THE CONVENTION
A = F.A                          # lib56dc -- the row rule
B = F.B                          # lib03d1 -- the disk glob

TREE = "code/dated_population_2ff6"

read = B.read
git = B.git
head = B.head
hdr = B.hdr
bar = A.bar
at = F.at


def pop(text, indent=2, ref=None):
    """`libfd9c.pop`, WITH THE ONE GUARD ITS CHECKER MAKES NECESSARY.

    S4c walks up from a count row to the first line containing `population:`
    and asks whether THAT LINE carries a ref.  So a population line whose text
    wraps puts `population:` on one line and `@ref` on the next, and the figure
    below it is UNDATED -- correctly, by a checker that is right.

    THIS IS NOT A HYPOTHETICAL.  My first form of `a1_axes.py`'s A1d subset
    line and of `a6_self.py`'s AS7 line both wrapped, and S4c scored
    `grain_axis_audit_03d1` at 15 of 18 for exactly that reason.  The remedy
    the ticket allows is to fix the PROBE, so the probes were fixed -- and
    then this guard was added, because `remember not to wrap` is not a fix,
    it is a thing to forget.  A wrapped population line is now an exception
    at the moment it is printed and not a silently undated figure three
    tickets later.
    """
    if "\n" in text:
        raise ValueError(
            "a population line must be ONE LINE -- S4c reads the ref off the "
            "line carrying `population:`, and a wrapped one leaves the figure "
            "below it undated.  Shorten the text or print the rest as prose. "
            "Offending text: %r" % text)
    F.pop(text, indent=indent, ref=ref)


note = F.note
plain = F.plain
render_figure = F.render_figure
state_of = F.state_of
file_stats = F.file_stats
census_from = F.census_from
weight_of = F.weight_of
census = F.census
CLASSES = F.CLASSES


# ---------------------------------------------------------------------------
# THE REF THE FIGURES MOVE FROM.  FROZEN, and hard-coded on purpose.
# ---------------------------------------------------------------------------

PUBLISHED_AT = "5c0849a"
"""The commit at which `mg-03d1`'s and `mg-9160`'s transcripts still carried
the values this ticket moves.

HARD-CODED, AND THAT IS THE CORRECT CHOICE HERE rather than the defect this
arc keeps finding.  The two are told apart by one question: does the thing the
ref names MOVE?  `audit_c067` pinned a WINDOW (`git log main -n 40`) onto a
growing branch and the window slid off it.  This pins the PUBLICATION DATE of a
figure, which is a fact about the past and cannot slide.  If a reader checks
this out at a later commit, `d1` still reads the same published bytes.
"""

# The probes this ticket edits and re-runs.  Named as TRANSCRIPTS because a
# transcript is the unit the accounting is over.
MOVED = [
    # mg-03d1: only the two probes that print an arc-wide corpus figure.  `a2`
    # to `a5` are NOT re-run -- they carry no figure this ticket dates, and
    # `a4` runs another tree's whole suite twice.  Re-running them would move
    # published numbers this ticket did not decide to move (E2).
    "code/grain_axis_audit_03d1/out_a1_axes.txt",
    "code/grain_axis_audit_03d1/out_a6_self.txt",
    # mg-9160: the WHOLE suite, because the convention was adopted at
    # `lib9160.pop` -- one edit, every population line in the tree dated -- and
    # a tree whose library moved and whose transcripts did not is a tree whose
    # transcripts declare a rule that did not produce them.
    "code/grain_arity_9160/out_selftest_9160.txt",
    "code/grain_arity_9160/out_s1_reproduce.txt",
    "code/grain_arity_9160/out_s2_arity.txt",
    "code/grain_arity_9160/out_s3_population.txt",
    "code/grain_arity_9160/out_s4_open.txt",
    "code/grain_arity_9160/out_s5_self.txt",
]

# The four tracked `.md` files carrying cfd9c's 10 ref-less prose sites.
PROSE = [
    "code/grain_arity_9160/PREDICTIONS.md",
    "code/grain_arity_9160/README.md",
    "code/grain_axis_audit_03d1/OUTCOMES.md",
    "code/grain_axis_audit_03d1/README.md",
]

# The refs the FROZEN figures in this arc are frozen AT.  Both are cfd9c's, by
# import where the library exposes them.
PARENT_REV = F.G.PARENT_REV
PARENT_PUB = F.G.PARENT_PUB
RECON = "%s+%s" % (PARENT_REV, PARENT_PUB)


# ---------------------------------------------------------------------------
# cfd9c's CHECKER, USED AND NEVER COPIED.
# ---------------------------------------------------------------------------

_RX_SRC = re.compile(r"^CORPUS_LABEL = re\.compile\((.*?)\)\s*$",
                     re.S | re.M)


def corpus_label_source():
    """The LITERAL TEXT of cfd9c's `CORPUS_LABEL`, out of its own file.

    Not an import (importing a probe runs it) and not a re-typing (a second
    copy is the thing the ticket forbids).  Returns the source text so a
    transcript can PRINT it -- a reader must be able to see that what I
    compiled is what cfd9c wrote, without opening two files.
    """
    src = read("code/corpus_fixedpoint_fd9c/s4_convention.py")
    m = _RX_SRC.search(src)
    if not m:
        raise RuntimeError(
            "cfd9c's CORPUS_LABEL could not be extracted from "
            "s4_convention.py.  I will not fall back on a copy of it -- see "
            "lib2ff6's docstring and PREDICTIONS.md/E7.")
    return m.group(1)


def corpus_label_rx():
    """cfd9c's `CORPUS_LABEL`, compiled from cfd9c's own characters."""
    return eval("re.compile(\n%s\n)" % corpus_label_source(),   # noqa: S307
                {"re": re})


def s4c(timeout=900):
    """(exit code, stdout) of cfd9c's `s4_convention.py`, RUN NOT IMPORTED.

    The probe writes nothing -- it prints to stdout and the runner redirects --
    so running it here does not regenerate cfd9c's committed transcript.  That
    matters: cfd9c's `out_s4_convention.txt` is the BEFORE reading of the score
    this ticket moves, and a probe of mine that overwrote it would have erased
    its own control.
    """
    p = subprocess.run([sys.executable, "-B", "s4_convention.py"],
                       cwd=FD9C, capture_output=True, text=True,
                       timeout=timeout)
    return p.returncode, p.stdout + p.stderr


_SCORE = re.compile(
    r"\.\.\.arc-wide corpus figures found\s+(\d+).*?"
    r"\.\.\.of them carrying a DATED population line\s+(\d+)", re.S)


def s4c_scores(text):
    """[(found, dated)] -- the two S4c blocks, in the order S4c prints them:
    the ARC first, then cfd9c's own tree.  Parsed off the transcript rather
    than recomputed, so this cannot disagree with the checker."""
    return [(int(a), int(b)) for a, b in _SCORE.findall(text)]


def s4c_per_tree(text):
    """{tree: (found, dated)} -- S4c's own per-tree table, parsed."""
    out = {}
    for ln in text.splitlines():
        m = re.match(r"\s+(\S+)\s+(\d+) found,\s+(\d+) dated\s*$", ln)
        if m:
            out[m.group(1)] = (int(m.group(2)), int(m.group(3)))
    return out


# ---------------------------------------------------------------------------
# THE CONVENTION, RENDERED.  Layout only -- every decision below is
# `libfd9c.state_of`'s or `libfd9c.render_figure`'s.
# ---------------------------------------------------------------------------

def class_block(figs, indent=2, intro=True):
    """One line per figure: its NAME, its CLASS, and the ref its population is
    dated at.

    `figs` is [(name, population_is_a_ref, observer_in_population, ref)] and
    the two booleans are the ONLY inputs to the class -- they go straight to
    `libfd9c.state_of`, which is cfd9c's function and is not re-decided here.
    A caller that wanted a different class would have to lie about one of the
    booleans, which is a thing a reader can check.
    """
    pad = " " * indent
    if intro:
        print("%sCLASS, from `libfd9c.state_of` -- two booleans and nothing" % pad)
        print("%selse: is the population a REF, and is the observer IN it." % pad)
        print()
    for name, is_ref, in_pop, ref in figs:
        cls = state_of(is_ref, in_pop)
        print("%s    %-50s %-9s @%s" % (pad, name, cls, ref or at()))


def observed_block(tree, fields=("files", "rows", "erows", "eints", "words"),
                   indent=2, note=None, paths=None):
    """The OBSERVED interval of the arc-wide census, field by field, for a
    probe whose own tree is `tree`.

    THE INTERVAL IS NOT AN ERROR BAR AND THE CODE SAYS SO WHERE THE NUMBER IS
    PRINTED, because the place a caution is needed is beside the figure and
    not in a paragraph three screens away.  Its width is one call to
    `libfd9c.weight_of`: the high end is the corpus as globbed, the low end is
    the same FILE LIST with this tree's own transcripts read as empty -- what
    a plain `>` leaves on disk while the probe that will fill it runs.

    `files` COMES OUT EMPTY (832-832) AND THAT IS THE PROPERTY TO PRESERVE.
    `>` truncates and does not unlink, so a file count cannot tell the two
    regimes apart.  A convention that printed a range on every field would be
    decorating the one field that is not at risk.
    """
    pad = " " * indent
    stats = file_stats(paths)
    now = census_from(stats)
    pre = tree.rstrip("/") + "/"
    w = weight_of(stats, lambda p: p.startswith(pre))
    print("%sOBSERVED, the two readings the apparatus admits -- width is one"
          % pad)
    print("%scall to `libfd9c.weight_of`, this tree's own transcripts read as"
          % pad)
    print("%sEMPTY as a plain `>` leaves them.  NOT AN ERROR BAR." % pad)
    if note:
        print("%s%s" % (pad, note))
    for f in fields:
        hi = now[f]
        lo = hi - w[f]
        print(("%s    %-8s %-32s%s"
               % (pad, f, render_figure(hi, "OBSERVED", low=lo, ref=at()),
                  "<- EMPTY INTERVAL" if lo == hi else "")).rstrip())
    return now, w


# ---------------------------------------------------------------------------
# THE ACCOUNTING.
# ---------------------------------------------------------------------------

_BAR = re.compile(r"^={10,}\s*$")


def sectioned(text):
    """[(section, lineno, label, nums)] -- every count row, tagged with the
    SECTION HEADING it was printed under.

    THE SECTION IS THE UNIT, because it is the unit in cfd9c's rule: its
    checker walks up from a count row and stops at a `====` bar, so a
    population declared in a previous section is not declared for this figure.
    An accounting that keyed on the label alone would pair `out_a6_self.txt`'s
    two `...count ROWS in them` rows with each other -- they are AF2's own
    transcripts and AF2's prose, two populations and two figures.
    """
    lines = text.splitlines()
    heads = {}
    cur = "(preamble)"
    for i, ln in enumerate(lines):
        # A HEADING IS A LINE BETWEEN TWO BARS, and not merely a line after
        # one -- `hdr` prints bar/title/bar, so the line after the SECOND bar
        # is the section's blank line and taking it would name every section
        # the empty string.  It did, on the first run of this function.
        if (_BAR.match(ln) and i + 2 < len(lines)
                and not _BAR.match(lines[i + 1]) and _BAR.match(lines[i + 2])):
            cur = lines[i + 1].strip()
        heads[i + 1] = cur
    return [(heads.get(i, "?"), i, label, nums)
            for i, label, nums in A.count_rows(text)]


def keyed(text):
    """{(section, label, ordinal): row} -- every count row, identified.

    THE ORDINAL IS NOT DECORATION.  `out_a6_self.txt`'s AS7 prints
    `...count ROWS in them` TWICE in one section -- once over this tree's own
    transcripts and once over its prose -- so (section, label) is not an
    identity and keying on it would silently merge two figures and report one
    of them as unmoved.  The ordinal is the only thing separating them that
    does not require me to read the labels and decide which is which.
    """
    out = {}
    seen = {}
    for row in sectioned(text):
        k = (row[0], row[2])
        seen[k] = seen.get(k, 0) + 1
        out[(row[0], row[2], seen[k])] = row
    return out


def diff_rows(path, old_ref=None, new_ref=None):
    """[(key, published nums, new nums, verdict)] for one transcript.

    `MOVED`, `SAME`, `ADDED` (a row the published transcript did not have) and
    `DROPPED` (one it had and this does not).  The last two are the ones that
    matter for honesty: a convention that silently deletes a published figure
    and reports `nothing moved` would be the worst outcome available here.
    """
    old = keyed(read(path, old_ref or PUBLISHED_AT))
    new = keyed(read(path, new_ref) if new_ref else read(path))

    def order(k):
        """A TOTAL ORDER THAT DOES NOT MOVE BETWEEN RUNS.

        The first form of this sorted by `the line number in whichever text
        has the row`, which interleaves two different numbering systems: a
        DROPPED row is placed by its line in the PUBLISHED text and its
        neighbours by their lines in the CURRENT one.  Add one line anywhere
        and two rows swap.  `d4`'s convergence arm caught it -- `out_d1_moved`
        differed between two rounds by one transposed row and nothing else --
        which is the arm doing the only job it has.

        Published order is FROZEN, so it is the primary key; rows the
        published text does not have are appended in current-text order and
        cannot interleave with it.
        """
        o = old.get(k)
        return (0, o[1], k[2]) if o else (1, new[k][1], k[2])

    out = []
    for k in sorted(set(old) | set(new), key=order):
        o, n = old.get(k), new.get(k)
        if o is None:
            out.append((k, None, n[3], "ADDED"))
        elif n is None:
            out.append((k, o[3], None, "DROPPED"))
        elif o[3] != n[3]:
            out.append((k, o[3], n[3], "MOVED"))
        else:
            out.append((k, o[3], n[3], "SAME"))
    return out


def fmt_nums(nums):
    return "-" if nums is None else " ".join(str(n) for n in nums)


def delta(old, new):
    """The signed change, when both readings are a single integer.  Blank when
    they are not -- a five-column row like `818 1984 458 1198 589` has five
    deltas and printing one of them would be picking a favourite."""
    if old is None or new is None:
        return ""
    if len(old) == 1 and len(new) == 1:
        return "%+d" % (new[0] - old[0])
    if len(old) == len(new):
        return " ".join("%+d" % (b - a) for a, b in zip(old, new))
    return ""


# ---------------------------------------------------------------------------
# THE PROSE SITES.
# ---------------------------------------------------------------------------

REF_IN_PROSE = re.compile(r"@[0-9a-f]{7,40}\b")


def prose_sites():
    """[(path, lineno, published line, current line)] for cfd9c's 10 sites.

    THE SITES ARE cfd9c's AND THE LINE NUMBERS ARE NOT.  `out_s2_drift.txt`
    names file and line at ITS commit; an edit above a site moves it.  So the
    sites are re-found HERE by the same needle-on-a-corpus-line shape, in the
    published text, and then followed into the current text BY CONTENT rather
    than by line number.
    """
    sites = []
    for p in PROSE:
        oldtxt = read(p, PUBLISHED_AT)
        newlines = read(p).splitlines()
        for i, ln in enumerate(oldtxt.splitlines(), 1):
            if not _NEEDLE.search(ln):
                continue
            if not re.search(r"corpus|transcript|grain word|count row|ARTIFACT",
                             ln):
                continue
            sites.append((p, i, ln, _follow(ln, newlines)))
    return sites


# The figures cfd9c's S2c looks for, as WHOLE numbers.  Same needles, same
# boundary rule -- including the `–—-` class members that S2c's D3 records
# getting wrong the first time, kept as members and not as a class.
_NB = u"–—-"
_NEEDLES = ("517", "1191", "400", "370", "86.0", "76.1", "79 800", "626",
            "818", "1984", "589", "2894")
_NEEDLE = re.compile("|".join(
    r"(?<![\d.%s])%s(?![\d.])" % (_NB, re.escape(n)) for n in _NEEDLES))


def _common(a, b):
    n = 0
    for x, y in zip(a, b):
        if x != y:
            break
        n += 1
    return n


MIN_PREFIX = 24


def _follow(oldline, newlines):
    """The current form of a published line, matched by its LONGEST COMMON
    PREFIX rather than by line number.  Returns None when it is gone -- which
    is a finding and not an absence: a prose site that vanished is a published
    claim that was deleted rather than dated.

    THE FIRST FORM OF THIS FUNCTION TOOK A FIXED 48-CHARACTER STEM and
    reported two dated sites as GONE, because this ticket's own marker is
    inserted at character 35 of both of them.  A false alarm in the exact
    direction that would read as `I deleted two published claims` -- and it
    was found by the check firing, not by reading the code.  The prefix is
    now as long as it is and must reach `MIN_PREFIX`, so a marker inserted
    anywhere after the opening clause is followed rather than mourned.
    """
    for ln in newlines:
        if ln == oldline:
            return ln
    best, bestn = None, 0
    for ln in newlines:
        n = _common(oldline, ln)
        if n > bestn:
            best, bestn = ln, n
    return best if bestn >= MIN_PREFIX else None


def figures_in(line):
    """The corpus figures a prose line carries, as printed.  Used to check
    that dating a site did not RECOMPUTE it: the digits must survive."""
    return sorted(m.group(0) for m in re.finditer(_NEEDLE, line))
