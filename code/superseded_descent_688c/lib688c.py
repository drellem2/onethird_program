"""mg-688c -- shared machinery for THE DESCENT SWEEP.

The question this instrument answers is NOT "is the tree stale" (mg-cdd5 answered
that and repaired it).  It is: during the interval in which the checked-out
`main-mirror` resolved STATE.md's citations into WITHDRAWN text, did any artifact
in this programme cite, quote, or reason from that withdrawn reading?

Three design rules, each of which the ticket forces:

1.  NOTHING IS READ OFF A WORKING COPY.  Every revision-dependent fact comes from
    `git show <rev>:<path>` or `git log`.  A sweep about a stale checkout that
    reads a checkout is the defect it is about.

2.  THE WINDOW IS PER-CLAIM, NOT GLOBAL.  A document written on 2026-08-01 that
    quotes `0/132` bare did not read withdrawn text: the withdrawal landed
    2026-08-07.  Scoring it as a descendant would inflate the count with
    artifacts that were correct when written.  Each struck claim therefore
    carries its own hazard window, opening at the moment its withdrawal became
    fetchable from the remote.

3.  THE POPULATION IS NAMED BEFORE ANY COUNT, and a zero is only reported next to
    the population that produced it.
"""

import json
import os
import re
import subprocess
import datetime as dt

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

# The two repositories.  MIRROR is the repo whose checkout went stale; CITING is
# the repo that holds STATE.md and cites into it (and is where this file lives).
MIRROR_REPO = "/Users/daniel/research/one_third_width_three"
CITING_REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

MG_ROOT = os.path.expanduser("~/.macguffin")

# The two revisions.  Named constants because every figure in this instrument is
# measured against them; if either moves the transcript is stale, which is the
# defect this instrument is about.
MIRROR_REV = "912f1b1"          # what the checkout had for the whole window
TIP_REV = "949c439"             # origin/main at the repair, and at this writing

UTC = dt.timezone.utc


def ts(s):
    """Parse an ISO-8601 timestamp to an aware UTC datetime."""
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(UTC)


def fmt(t):
    return t.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def dur(a, b):
    d = b - a
    days = d.days
    h, rem = divmod(d.seconds, 3600)
    m, s = divmod(rem, 60)
    return "%dd %02dh %02dm %02ds" % (days, h, m, s)


def git(repo, *args, check=True):
    r = subprocess.run(["git", "-C", repo] + list(args),
                       capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError("git %s -> %s" % (" ".join(args), r.stderr.strip()))
    return r.stdout


def show(repo, rev, path):
    """File content at a revision.  Never touches the working copy."""
    return git(repo, "show", "%s:%s" % (rev, path), check=False)


# ---------------------------------------------------------------------------
# THE WINDOW
# ---------------------------------------------------------------------------
# Both ends come from the mirror repo's own reflogs; the START is sharpened by
# the remote's push history, because the reflog can only say when THIS clone
# learned something, not when the remote had it.

def mirror_reflog():
    """The two entries of refs/heads/main-mirror, oldest last."""
    out = git(MIRROR_REPO, "reflog", "show", "main-mirror", "--date=iso-strict")
    rows = []
    for line in out.strip().splitlines():
        m = re.match(r"^(\S+) \S+@\{([^}]+)\}: (.*)$", line)
        if m:
            rows.append({"sha": m.group(1), "at": ts(m.group(2)), "what": m.group(3)})
    return rows


def push_events():
    """Cached PushEvents for the mirror repo's origin, oldest first.

    Provenance: `gh api repos/drellem2/one_third_width_three/events --paginate`,
    captured 2026-08-12 into data/push_events.json.  GitHub's events feed is
    retained for roughly 90 days; the window this instrument bounds is inside
    that retention, which is the only reason the START of the window is
    knowable to the second rather than as a bracket.  Re-running this
    instrument after the retention lapses will find the cache and use it -- see
    the DURABILITY note in README.md.
    """
    with open(os.path.join(DATA, "push_events.json")) as fh:
        evs = json.load(fh)
    rows = [{"at": ts(e["created_at"]), "head": e["head"][:7], "ref": e["ref"]}
            for e in evs if e["ref"] == "refs/heads/main"]
    return sorted(rows, key=lambda r: r["at"])


def push_time(sha7):
    """When the push carrying <sha7> reached origin.

    A commit is not necessarily a push head, so this returns the FIRST push
    whose head has <sha7> as an ancestor.  That is the instant the withdrawal
    became fetchable, which is what a hazard window opens on.
    """
    for ev in push_events():
        r = subprocess.run(["git", "-C", MIRROR_REPO, "merge-base",
                            "--is-ancestor", sha7, ev["head"]],
                           capture_output=True, text=True)
        if r.returncode == 0:
            return ev["at"], ev["head"]
    return None, None


# ---------------------------------------------------------------------------
# THE FOUR AFFECTED CITED DOCUMENTS, and the claims withdrawn in each.
# ---------------------------------------------------------------------------
# Sourced from mg-cdd5's s2 sweep (which named the citations) and from
# `git diff 912f1b1 949c439` over each (which names what moved).  `landed` is
# the commit on the mirror repo's main that performed the withdrawal.

DOCS = {
    "RC": "docs/OneThird-L1b-Reverse-Cheeger-Proof-Attempt.md",
    "KS": "docs/OneThird-Spectral-NearOrdinalSum-KillShot-Probe.md",
    "CR": "docs/OneThird-StandardDominance-ComparisonRoute.md",
    "BK": "docs/OneThird-L1b-BK-Transport-Transfer-Probe.md",
}

CLAIMS = [
    dict(
        id="RC1", doc="RC", landed="bde9610", kind="STRUCK",
        title="`lambda_std <= lambda_2^BK` (the standard sector is a subspace)",
        stale=("The Reverse-Cheeger bullet at line 286 asserts, unstruck: "
               "**But `λ_std ≤ λ₂^{BK}`** (the standard sector is a subspace): "
               "Theorem E bounds the gap in the *wrong direction* for the "
               "transport quotient."),
        current=("The same bullet, struck, plus a STRUCK 2026-08-07 (mg-d1be) "
                 "note: the inequality is FALSE with exact counterexamples "
                 "(A2+A2: 1 > 2/3; A3+A3: 1 > 9/10), and the parenthetical is "
                 "not a proof of it.  The bullet's CONCLUSION survives on "
                 "stronger ground (no universal inequality in either direction)."),
        fps=[r"λ_std\s*≤\s*λ₂", r"lambda_std\s*<=\s*lambda_2",
             r"standard sector is a subspace"],
        loc=r"standard sector is a subspace",
    ),
    dict(
        id="RC2", doc="RC", landed="bde9610", kind="ABSENT-IN-MIRROR",
        title="section 5.0' -- the correction section itself",
        stale="Section 5.0' does not occur in the mirror's copy at all.",
        current=("2,700 words of correction: (a) exact witnesses, (b) why the "
                 "parenthetical is not a proof, (c) the two spectra are "
                 "INCOMPARABLE, (d) the conclusion survives and is strengthened, "
                 "(e) do NOT reach for the 'off the ordinal sums' rescue."),
        fps=[r"§\s*5\.0['′]", r"5\.0['′]"],
        loc=r"^#+ *5\.0['′]",
    ),
    dict(
        id="KS1", doc="KS", landed="a8688f2", kind="STRUCK",
        title="Kill-shot 2 verdict word GREEN",
        stale="## Kill-shot 2 -- Standard dominance -- **GREEN**",
        current=("~~**GREEN**~~ **GREEN-IN-FRAME ONLY**, under a scope-correction "
                 "banner: the measurements stand, the VERDICT WORD is withdrawn."),
        fps=[r"Kill-shot 2[^\n]{0,80}GREEN", r"[Ss]tandard [Dd]ominance[^\n]{0,40}GREEN"],
        loc=r"^#+ *Kill-shot 2",
    ),
    dict(
        id="KS2", doc="KS", landed="a8688f2", kind="WITHDRAWN",
        title='the word "universal" applied to standard dominance',
        stale=('"...standard dominance is universal, the eigenvector order tracks '
               'expected rank..." -- stated as a property of posets.'),
        current=('"UNIVERSAL" IS WITHDRAWN AND WAS THE WORST SENTENCE IN THIS '
                 'DOCUMENT: the unconditional form is REFUTED by 166 moderate-λ '
                 'n=7 refuters outside the frame; what stays open is the '
                 'all-pairs-frozen conditional, which IS L1b.'),
        fps=[r"dominance[^\n]{0,60}universal", r"universal[^\n]{0,60}dominance"],
        loc=r"universal, the eigenvector order|universal~~",
    ),
    dict(
        id="KS3", doc="KS", landed="a8688f2", kind="WITHDRAWN",
        title="`0 / 132` quoted bare",
        stale=("Data-appendix row: | standard-dominance failures "
               "(n<=6 exhaustive + n=7 top-λ spot) | 0 / 132 |  -- no consequence "
               "of the frame recorded anywhere in the document."),
        current=("SAMPLING ARTIFACT, NEVER QUOTABLE BARE.  The frame excludes the "
                 "known refuters; and 132 = 126 + 6, of which only the 126 ship in "
                 "the JSON, so a third-party check bottoms out at 0/126."),
        fps=[r"0\s*/\s*132"],
        loc=r"standard-dominance failures",
    ),
    dict(
        id="CR1", doc="CR", landed="949c439", kind="STRUCK",
        title='row C3: "fails exactly on the ordinal sums, holds elsewhere" [proven]',
        stale=("| C3 | `λ_std ≤ λ₂^BK` fails **exactly on the ordinal sums**, holds "
               "elsewhere | **[proven]** at n=4,5 (exact set equality) | -- and "
               "§2.4's prose: 'it is true generically and fails on a thin, "
               "exactly-identified set'."),
        current=('The "exactly" is FALSE for n >= 7 and breaks wholesale at n = 8 '
                 '(19 indecomposable violators, 16 of width exactly 3).  A small-n '
                 'coincidence, not a theorem with exceptions.'),
        fps=[r"exactly[^\n]{0,30}ordinal sums", r"holds elsewhere",
             r"exactly-identified set"],
        loc=r"^\| C3 \|",
    ),
    dict(
        id="CR2", doc="CR", landed="a8688f2", kind="WITHDRAWN",
        title="SD-Cayley row: `Empirically supported, 0/132`",
        stale="| **SD-Cayley** | ... | Empirically supported, **0/132** (`mgb0a6`). |",
        current="~~Empirically supported, 0/132~~ THE BARE FIGURE IS WITHDRAWN.",
        fps=[r"0\s*/\s*132"],
        loc=r"^\| \*\*SD-Cayley\*\*",
    ),
    dict(
        id="BK1", doc="BK", landed="af7fc2d", kind="CORRECTED-NO-STRIKE",
        title="946 both-connected n=7 isomorphism classes",
        stale=("Exhaustive both-connected posets n = 3..7 (3, 9, 12, 104, **946** "
               "posets) -- no correction present."),
        current=("A CORRECTED banner: there are **956**, not 946; `iso_signature` "
                 "is not a perfect canonical form and collapses 10 classes at n=7. "
                 "n = 3..6 unaffected.  No conclusion in the document turns on the 10."),
        fps=[r"\b946\b"],
        loc=r"Exhaustive both-connected posets",
        # The correction is a banner INSERTED ABOVE the line, not an edit of
        # it: the "946" sentence is byte-identical at both revisions.  So the
        # current side needs its own anchor, or this claim would print as
        # "no change" and be silently dropped from the delta.
        loc_cur=r"the `n = 7` count is wrong|\b956\b",
    ),
]


def claims_by_doc(doc):
    return [c for c in CLAIMS if c["doc"] == doc]


# ---------------------------------------------------------------------------
# THE POPULATIONS
# ---------------------------------------------------------------------------

def citing_commits(start, end):
    """Commits in onethird_program with COMMITTER date inside [start, end]."""
    out = git(CITING_REPO, "log", "--format=%H%x00%cI%x00%s",
              "--since=%s" % fmt(start), "--until=%s" % fmt(end), "HEAD")
    rows = []
    for line in out.strip().splitlines():
        if not line:
            continue
        sha, when, subj = line.split("\x00", 2)
        rows.append({"sha": sha, "at": ts(when), "subject": subj})
    return rows


def added_lines(sha):
    """The lines a commit ADDS.  A descendant is written, not merely present."""
    out = git(CITING_REPO, "show", "--format=", "--unified=0", sha, check=False)
    return [ln[1:] for ln in out.splitlines()
            if ln.startswith("+") and not ln.startswith("+++")]


def _walk(root):
    for dirpath, _dirs, files in os.walk(root):
        for f in files:
            yield os.path.join(dirpath, f)


def work_items():
    """Every macguffin work item, with the interval in which its text was written.

    `created` is the filed-at stamp in the body; mtime is the last write.  A
    work item is a candidate if [created, mtime] OVERLAPS a hazard window --
    using created alone would miss text appended by a later edit.
    """
    rows = []
    for path in _walk(os.path.join(MG_ROOT, "work")):
        try:
            with open(path, errors="replace") as fh:
                text = fh.read()
        except OSError:
            continue
        m = re.search(r"^created:\s*(\S+)", text, re.M)
        created = ts(m.group(1)) if m else None
        mtime = dt.datetime.fromtimestamp(os.path.getmtime(path), UTC)
        rows.append({"path": path, "created": created or mtime,
                     "mtime": mtime, "text": text})
    return rows


def mail_items():
    """Every macguffin mail message, with its Date: header (mtime as fallback)."""
    rows = []
    for path in _walk(os.path.join(MG_ROOT, "mail")):
        if os.path.basename(path).startswith("."):
            continue
        try:
            with open(path, errors="replace") as fh:
                text = fh.read()
        except OSError:
            continue
        m = re.search(r"^Date:\s*(\S+)", text, re.M)
        try:
            when = ts(m.group(1)) if m else None
        except ValueError:
            when = None
        if when is None:
            when = dt.datetime.fromtimestamp(os.path.getmtime(path), UTC)
        rows.append({"path": path, "at": when, "text": text})
    return rows


# ---------------------------------------------------------------------------
# CLASSIFICATION
# ---------------------------------------------------------------------------
# A fingerprint hit is NOT a descendant.  Most of this programme's traffic about
# these claims is the withdrawal itself propagating.  A hit is a DESCENDANT only
# if it asserts the withdrawn reading with no trace of the withdrawal nearby.

WITHDRAWAL_MARKERS = [
    r"STRUCK", r"struck", r"~~", r"<s>", r"REFUTED", r"refuted", r"WITHDRAWN",
    r"withdrawn", r"FALSE", r"is false", r"SAMPLING ARTIFACT", r"sampling artifact",
    r"NEVER QUOTABLE BARE", r"never quotable", r"not quotable", r"FP✗",
    r"scope correction", r"SCOPE CORRECTION", r"CORRECTED", r"corrected",
    r"frame", r"FRAME", r"mg-d1be", r"mg-e2a0", r"mg-55f2", r"mg-24eb",
    r"mg-65f5", r"mg-60d3", r"mg-8b64", r"956", r"small-n coincidence",
    r"coincidence", r"does not extend", r"incomparable", r"INCOMPARABLE",
]

_WMARK = re.compile("|".join(WITHDRAWAL_MARKERS))

CONTEXT = 400


def scan(text, claim):
    """Every occurrence of any of a claim's fingerprints, with a verdict.

    Verdict is CARRIES-WITHDRAWAL when a withdrawal marker occurs within
    CONTEXT characters either side, BARE otherwise.  The asymmetry is
    deliberate: the marker list is generous, so this over-reports
    CARRIES-WITHDRAWAL and under-reports BARE -- and BARE is the class that
    gets read by hand.  A generous marker list therefore SHRINKS the hand-read
    pile, which is the wrong direction, so s3 controls it by planting bare
    assertions and checking they survive as BARE.
    """
    out = []
    for fp in claim["fps"]:
        for m in re.finditer(fp, text):
            a = max(0, m.start() - CONTEXT)
            b = min(len(text), m.end() + CONTEXT)
            ctx = text[a:b]
            out.append({
                "claim": claim["id"],
                "fp": fp,
                "pos": m.start(),
                "excerpt": re.sub(r"\s+", " ", ctx)[:520],
                "verdict": "CARRIES-WITHDRAWAL" if _WMARK.search(ctx) else "BARE",
            })
    return out


def rule(ch="-", n=78):
    return ch * n


def wrap(text, indent=4, width=74):
    """Fixed-width prose block, so the transcripts read at 78 columns."""
    words = text.split()
    lines, cur = [], ""
    pad = " " * indent
    for w in words:
        if len(cur) + len(w) + 1 > width - indent:
            lines.append(pad + cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(pad + cur)
    return lines
