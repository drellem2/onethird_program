"""lib5827 — the superseded-figure detector (mg-5827).

The defect class: a figure computed from an input that was later corrected, still quoted as
flat text at a site nobody thought to look at.

The rule, in one sentence: **an occurrence of a superseded value in a tracked file is a DEFECT
unless the site itself says it is superseded.**

Three deliberate choices, each of which is a place a predecessor went wrong:

1.  The file list comes from ``git ls-files``, NOT from a glob. ``docs/*.md`` is
    ``os.listdir``-shaped: non-recursive, and it reads the WORKING TREE rather than the index
    (mg-1d6c). A sweep that cannot see ``docs/state-history/`` cannot see where the correction
    was recorded.

2.  Classification is by PROXIMITY TO A REPAIR MARKER, not by presence of the value. The audit
    that performed the correction quotes the superseded value eleven times; so does the record
    that carries the standing instruction not to quote it. A detector that flags those is
    flagging the fix.

3.  Occurrences are partitioned TOTALLY into DEFECT / REPAIRED / AUTHORITY / FROZEN, with a
    count printed for each. A bucket that is silently dropped is a bucket nobody audits.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field

HERE = os.path.dirname(os.path.abspath(__file__))
REGISTRY_PATH = os.path.join(HERE, "registry.json")

# How many lines either side of an occurrence count as "the site itself".
PROXIMITY = 6

# Text files only; the corpus is markdown, python, shell, text and html.
TEXT_SUFFIXES = (".md", ".txt", ".py", ".sh", ".html", ".json", ".tex", ".csv")

DEFECT = "DEFECT"
REPAIRED = "REPAIRED"
AUTHORITY = "AUTHORITY"
FROZEN = "FROZEN"
BUCKETS = (DEFECT, REPAIRED, AUTHORITY, FROZEN)


@dataclass
class Occurrence:
    path: str
    lineno: int          # 1-indexed
    entry_id: str
    matched: str
    line: str
    bucket: str = ""
    why: str = ""


@dataclass
class Registry:
    entries: list
    repair_markers: list
    authorities: list
    frozen_prefixes: list
    raw: dict = field(default_factory=dict)

    @classmethod
    def load(cls, path: str = REGISTRY_PATH) -> "Registry":
        with open(path, "r", encoding="utf-8") as fh:
            raw = json.load(fh)
        return cls(
            entries=raw["entries"],
            repair_markers=raw["repair_markers"],
            authorities=raw["authorities"],
            frozen_prefixes=raw["frozen_prefixes"],
            raw=raw,
        )

    def compiled(self):
        """[(entry, [compiled patterns])]. Raises on a bad regex rather than skipping it."""
        out = []
        for entry in self.entries:
            pats = []
            for p in entry["patterns"]:
                try:
                    pats.append(re.compile(p))
                except re.error as exc:                     # pragma: no cover - config error
                    raise SystemExit(
                        "registry.json: entry %r has an uncompilable pattern %r: %s"
                        % (entry["id"], p, exc)
                    )
            out.append((entry, pats))
        return out

    def authority_paths(self):
        return [a["path"] for a in self.authorities]


def excluded_from_population(path: str) -> bool:
    """This instrument's own TRANSCRIPTS are not part of the population it measures.

    THIS IS A REPAIR OF A DEFECT THIS INSTRUMENT HAD. `out_gate.txt` records every occurrence
    the gate found, so the next run finds all of them again INSIDE the transcript — 691
    self-occurrences on the run that caught it, against 46 real ones. The census was not even a
    fixed point: its own output changed the number it printed on the next run, and the total
    grew monotonically with the number of times anyone had run it.

    Bucketing them as AUTHORITY was not enough. An exempt occurrence is still COUNTED, and the
    printed totals were therefore a fiction. They have to leave the population.

    Only the transcripts. `registry.json`, the scripts and the prose stay in the population and
    are exempted by the AUTHORITY rule, so this instrument is still visible to itself.
    """
    base = os.path.basename(path)
    return path.startswith("code/superseded_figures_5827/") and base.startswith("out_")


def tracked_files(rev: str | None = None, root: str | None = None) -> list[str]:
    """Every tracked text file, from git — not from a glob.

    ``rev=None`` reads the index (the working tree's tracked set). A revision reads that tree,
    which is what makes the retrospective at mg-2860's base commit possible.
    """
    root = root or os.getcwd()
    if rev is None:
        cmd = ["git", "ls-files", "-z"]
    else:
        cmd = ["git", "ls-tree", "-r", "-z", "--name-only", rev]
    out = subprocess.run(cmd, cwd=root, check=True, capture_output=True).stdout
    names = [n for n in out.decode("utf-8", "replace").split("\0") if n]
    return sorted(n for n in names
                  if n.endswith(TEXT_SUFFIXES) and not excluded_from_population(n))


def read_file(path: str, rev: str | None = None, root: str | None = None) -> list[str]:
    root = root or os.getcwd()
    if rev is None:
        full = os.path.join(root, path)
        if not os.path.exists(full):
            return []
        with open(full, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read().splitlines()
    blob = subprocess.run(
        ["git", "show", "%s:%s" % (rev, path)],
        cwd=root, capture_output=True,
    )
    if blob.returncode != 0:
        return []
    return blob.stdout.decode("utf-8", "replace").splitlines()


def _under(path: str, prefix: str) -> bool:
    """True if `path` is `prefix` or lives under it. Prefix-of-a-name is NOT a match:
    'code/foo' must not swallow 'code/foobar'."""
    if prefix.endswith("/"):
        return path.startswith(prefix)
    return path == prefix or path.startswith(prefix + "/")


def _struck(line: str, matched: str) -> bool:
    """True if `matched` falls inside a ``~~ ... ~~`` strikethrough span on this line.

    Spans are taken pairwise left to right. A lone unmatched ``~~`` opens nothing, so a line
    that merely contains a tilde pair elsewhere does not launder an unstruck value into
    REPAIRED — the match must sit inside a CLOSED span.
    """
    idx = line.find(matched)
    if idx < 0:
        return False
    marks = [m.start() for m in re.finditer(r"~~", line)]
    for a, b in zip(marks[0::2], marks[1::2]):
        if a < idx and idx + len(matched) <= b + 2:
            return True
    return False


def _blockquote_span(lines: list[str], lineno: int):
    """(lo, hi) 0-indexed half-open span of the maximal `>`-prefixed run containing `lineno`,
    or (None, None) if that line is not inside a blockquote."""
    i = lineno - 1
    if i < 0 or i >= len(lines) or not lines[i].lstrip().startswith(">"):
        return None, None
    lo = i
    while lo > 0 and lines[lo - 1].lstrip().startswith(">"):
        lo -= 1
    hi = i + 1
    while hi < len(lines) and lines[hi].lstrip().startswith(">"):
        hi += 1
    return lo, hi


def classify(occ: Occurrence, lines: list[str], reg: Registry) -> Occurrence:
    """Assign exactly one bucket. Order matters and is stated here rather than implied.

    AUTHORITY beats everything: a declared authority is where the correction lives.
    FROZEN beats DEFECT: a committed transcript is evidence at a commit, not a live claim —
      except a README/OUTCOMES/PREDICTIONS directly inside a code directory, which is prose in
      the present tense and IS a live claim.
    REPAIRED beats DEFECT: the site says it is superseded.
    Otherwise DEFECT.
    """
    for auth in reg.authorities:
        if _under(occ.path, auth["path"]):
            occ.bucket, occ.why = AUTHORITY, "declared authority: " + auth["why"]
            return occ

    base = os.path.basename(occ.path).upper()
    is_live_prose = base in ("README.MD", "OUTCOMES.MD", "PREDICTIONS.MD")
    for pref in reg.frozen_prefixes:
        if _under(occ.path, pref) and not is_live_prose:
            occ.bucket = FROZEN
            occ.why = "committed transcript/source under %r — evidence at a commit" % pref
            return occ

    # (a) The strongest signal, and the only one that is local to the match itself: the
    #     superseded value is STRUCK OUT on its own line. `~~...~~` around the match is an
    #     assertion by the author, at the exact site, that this value no longer stands.
    if _struck(occ.line, occ.matched):
        occ.bucket = REPAIRED
        occ.why = "the matched value is struck out (~~...~~) on its own line"
        return occ

    # (b) The repaired value stands on the same line as the superseded one. A site that prints
    #     both is showing the reader the correction, not asserting the stale number.
    entry = next(e for e in reg.entries if e["id"] == occ.entry_id)
    if entry["repaired"] and entry["repaired"] in occ.line:
        occ.bucket = REPAIRED
        occ.why = "the repaired value %r stands on the same line" % entry["repaired"]
        return occ

    # (c) A repair marker nearby. Weakest of the three, and the one that both over- and
    #     under-fires; it is last on purpose.
    # (c') A markdown BLOCKQUOTE is one annotation unit. This corpus writes a supersession as a
    #     `>` block whose first line shouts the marker and whose later lines carry the argument;
    #     a fixed +/-N window cuts such a block in half and reports its own tail as a live claim.
    #     Widening the window instead would buy the same coverage at the cost of false negatives
    #     in ordinary prose, which is the direction that costs something. This is structural.
    lo, hi = _blockquote_span(lines, occ.lineno)
    if lo is None:
        lo = max(0, occ.lineno - 1 - PROXIMITY)
        hi = min(len(lines), occ.lineno + PROXIMITY)
    window = "\n".join(lines[lo:hi])
    # CASE-SENSITIVE for the shouted markers. This corpus writes them in caps -- **SUPERSEDED**,
    # **STRUCK**, `[REPAIRED - ...]` -- and matching them case-insensitively means the ordinary
    # English word "struck" in a neighbouring sentence launders a live figure into REPAIRED.
    # Found by this instrument's own control C4, which is the direction that costs something:
    # a false NEGATIVE reports clean and looks exactly like a corpus that is clean.
    hits = [m for m in reg.repair_markers
            if (m in window if m.isupper() else m.lower() in window.lower())]
    if hits:
        occ.bucket = REPAIRED
        occ.why = "repair marker(s) within %d lines: %s" % (PROXIMITY, ", ".join(sorted(set(hits))))
        return occ

    occ.bucket = DEFECT
    occ.why = "no repair marker within %d lines — reads as a live claim" % PROXIMITY
    return occ


def scan(rev: str | None = None, root: str | None = None,
         reg: Registry | None = None, paths: list[str] | None = None) -> list[Occurrence]:
    reg = reg or Registry.load()
    compiled = reg.compiled()
    files = paths if paths is not None else tracked_files(rev=rev, root=root)
    out: list[Occurrence] = []
    for path in files:
        lines = read_file(path, rev=rev, root=root)
        if not lines:
            continue
        for i, line in enumerate(lines, start=1):
            for entry, pats in compiled:
                for pat in pats:
                    m = pat.search(line)
                    if m:
                        out.append(classify(
                            Occurrence(path=path, lineno=i, entry_id=entry["id"],
                                       matched=m.group(0), line=line.strip()),
                            lines, reg))
                        break          # one occurrence per (line, entry)
    return out


def tally(occs: list[Occurrence]) -> dict:
    t = {b: 0 for b in BUCKETS}
    for o in occs:
        t[o.bucket] += 1
    return t


def render(occs: list[Occurrence], bucket: str, limit: int | None = None) -> str:
    rows = [o for o in occs if o.bucket == bucket]
    if not rows:
        return "    (none)"
    shown = rows if limit is None else rows[:limit]
    out = []
    for o in shown:
        text = o.line if len(o.line) <= 108 else o.line[:105] + "..."
        out.append("    %s:%d  [%s]  %r" % (o.path, o.lineno, o.entry_id, o.matched))
        out.append("        %s" % text)
    if limit is not None and len(rows) > limit:
        out.append("    ... and %d more (NOT truncated silently: %d total)"
                   % (len(rows) - limit, len(rows)))
    return "\n".join(out)


def banner(title: str) -> str:
    return "\n" + "=" * 78 + "\n" + title + "\n" + "=" * 78


def emit(title: str, occs: list[Occurrence], limit: int | None = None) -> None:
    print(banner(title))
    t = tally(occs)
    print("  TOTAL OCCURRENCES: %d   %s" % (
        len(occs), "  ".join("%s=%d" % (b, t[b]) for b in BUCKETS)))
    assert sum(t.values()) == len(occs), "buckets do not partition the occurrences"
    for b in BUCKETS:
        print("\n  --- %s (%d) ---" % (b, t[b]))
        print(render(occs, b, limit=limit))


def defects(occs: list[Occurrence]) -> list[Occurrence]:
    return [o for o in occs if o.bucket == DEFECT]


def main_exit(occs: list[Occurrence]) -> int:
    d = defects(occs)
    if d:
        print("\n  GATE: FAIL — %d flat-text site(s) quoting a superseded input." % len(d))
        return 1
    print("\n  GATE: PASS — 0 flat-text sites.")
    return 0


if __name__ == "__main__":                                  # pragma: no cover
    rev = sys.argv[1] if len(sys.argv) > 1 else None
    occurrences = scan(rev=rev)
    emit("SUPERSEDED-FIGURE SCAN @ %s" % (rev or "working tree (index)"), occurrences)
    sys.exit(main_exit(occurrences))
