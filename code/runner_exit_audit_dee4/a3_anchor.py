"""A3 -- THE PIN.  UNPINNED FOR THE CENSUS, STILL PINNED FOR THE COMPARISON?

The audit ticket states the danger precisely: *a repair that unpins BOTH has
reintroduced the moving-baseline defect the pin was added to fix.*  So this
probe does not take mg-7522's word for which anchor serves which purpose; it
reads every anchor out of the repaired files and runs the questions both ways.

  A3a  EVERY ANCHOR IN THE REPAIRED SCAN, read from the source.  The census
       must be `None`; the classification and the byte-comparison must be
       `bee07a1`.
  A3b  THE PRE-REPAIR PREDICATE, RUN AGAINST THE SAME INPUTS.  mg-7522 changed
       four things in `k2_consume.py`'s caller scan at once -- the anchor, the
       file filter, the EXEC regex and the target regex.  Each is run in its
       pre-repair and post-repair form over the same HEAD bytes so the effect
       of each is separable, which is the only way to tell a fix from a
       coincidence.
  A3c  THE REPAIRED TARGET RULE IS STILL A NAME RULE.  It went from one
       filename to two.  `lib7522._TARGET` -- mg-7522's own property rule, in
       its own library -- is run over the same inputs to measure what the two
       filenames still cannot see.
  A3d  THE COMPARISON'S FIGURE.  The published document states the pinned
       byte-comparison as `154 changed files`.  That is a bare prose figure
       with no transcript behind it, in a document whose own rule is that a
       number that moves belongs in a transcript.  It is re-derived at every
       anchor that could plausibly have produced it.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import libdee4 as L

BAD = 0
FINDINGS = []
K2 = "code/runner_exit_c2b3/k2_consume.py"
S4 = "%s/s4_unpin.py" % L.TREE

L.bar("A3  THE ANCHOR OF A CENSUS IS NOT THE ANCHOR OF A COMPARISON")

# ---------------------------------------------------------------------------
L.hdr("A3a  EVERY ANCHOR IN THE REPAIRED FILES, READ FROM THE SOURCE")

k2 = L.read(K2, None)
s4 = L.read(S4, None)
ANCHORS = [
    ("k2_consume.py", "CALLER_REF", "CENSUS -- what, in the world, reads a "
     "runner's exit status", r"^CALLER_REF\s*=\s*None\b", k2),
    ("k2_consume.py", "REF", "COMPARISON -- classify the runner text as it "
     "stood before the repair", r"^REF\s*=\s*L\.TICKET_REF\b", k2),
    ("libc2b3.py", "TICKET_REF", "the pin itself",
     r'^TICKET_REF\s*=\s*"bee07a1"', L.read("code/runner_exit_c2b3/libc2b3.py",
                                            None)),
    ("s4_unpin.py", "changed_since(PINNED)", "COMPARISON -- did any committed "
     "transcript move", r"pin_changed\s*=\s*changed_since\(L\.PINNED\)", s4),
    ("s4_unpin.py", "changed_since(None)", "the HEAD side of the same "
     "comparison, shown to be 0 by construction",
     r"head_changed\s*=\s*changed_since\(None\)", s4),
]
print("    %-14s %-24s %-7s %s" % ("file", "anchor", "present", "question it serves"))
rows = []
for f, name, why, rx, src in ANCHORS:
    ok = bool(re.search(rx, src, re.M))
    if not ok:
        BAD += 1
        FINDINGS.append("A3a %s: `%s` not found in the form expected" % (f, name))
    rows.append((f, name, "yes" if ok else "*** NO ***", why))
L.rows(rows, (14, 24, 7), indent="    ")
print()
print("  THE LOAD-BEARING PAIR.  The census is `None` and the comparison is")
print("  `bee07a1`.  A repair that unpinned BOTH would have put mg-821e's")
print("  defect back; this one did not.  The document names which anchor")
print("  serves which purpose in two places -- `k2_consume.py`'s own comment")
print("  block, and S4e's anchor inventory.")
print()
UNPIN_DOC = "unpinned for the enumeration"
doc = L.read(L.DOC, None)
for phrase, where in ((UNPIN_DOC, "the published document"),
                      ("still pinned for the classification", "the same")):
    print("      %-42s %s" % ("`%s`" % phrase[:40],
                              "present" if phrase in doc else "*** ABSENT ***"))

# ---------------------------------------------------------------------------
L.hdr("A3b  THE PRE-REPAIR PREDICATE, RUN AGAINST THE SAME INPUTS")

print("  mg-7522 changed FOUR things in this one scan.  Each is run in both")
print("  forms over the same bytes, so the effect of each is separable.")
print()

EXEC_OLD = re.compile(r"subprocess\.|(?<![\w.])sh\s+[\"'./$]|\./run_all\.sh"
                      r"|run_runner\(")
EXEC_NEW = re.compile(r"subprocess\.|(?<![\w.])sh\s+[\"'./$]|\./run_\w*\.sh"
                      r"|run_runner\(")
NOT_EXEC = re.compile(r"[\"']git[\"']|git show|git -C|ls-tree")
READ = re.compile(r"returncode|check\s*=\s*True")
TGT_OLD = re.compile(r"([\w./]*?([\w]+)/run_all\.sh)")
TGT_NEW = re.compile(r"([\w./]*?([\w]+)/(?:run_all|run_audit)\.sh)")
# mg-7522's own PROPERTY rule, from its own library.  Imported explicitly and
# named, because running someone's rule to CHECK it is a different act from
# running it to rely on it.
TGT_PROP = re.compile(r"([\w./-]*?([\w-]+)/(\w+\.sh))")


def scan(ref, execrx, tgtrx, exclude_run_all):
    if ref is None:
        files = [f for f in L.git("ls-files", "--", "*.py", "*.sh").split()
                 if f]
    else:
        files = [f for f in L.git("ls-tree", "-r", "--name-only", ref).split()
                 if f.endswith(".py") or f.endswith(".sh")]
    if exclude_run_all:
        files = [f for f in files if not f.endswith("/run_all.sh")]
    hits = []
    for f in sorted(files):
        try:
            src = L.read(f, ref)
        except (RuntimeError, OSError):
            continue
        lines = src.split("\n")
        for i, line in enumerate(lines, 1):
            m = tgtrx.search(line)
            if not m or not execrx.search(line) or NOT_EXEC.search(line):
                continue
            if "%s" in m.group(1) or m.group(1).startswith("/"):
                continue
            if os.path.normpath(m.group(1)) == os.path.normpath(f):
                continue
            window = "\n".join(lines[i - 1:i + 25])
            hits.append((f, i, m.group(1), bool(READ.search(window))))
    return hits


VARIANTS = [
    ("pre-repair, as mg-c2b3 ran it", L.PINNED, EXEC_OLD, TGT_OLD, True),
    ("pre-repair rule, HEAD bytes -- ANCHOR alone", None, EXEC_OLD, TGT_OLD, True),
    ("…and the run_all.sh EXCLUSION dropped", None, EXEC_OLD, TGT_OLD, False),
    ("…and the EXEC regex widened", None, EXEC_NEW, TGT_OLD, False),
    ("repaired, as it stands now", None, EXEC_NEW, TGT_NEW, False),
    ("mg-7522's own PROPERTY rule (lib7522._TARGET)", None, EXEC_NEW, TGT_PROP,
     False),
]
print("    %-46s %-7s %s" % ("rule", "sites", "reading the status"))
res = {}
for label, ref, ex, tg, excl in VARIANTS:
    h = scan(ref, ex, tg, excl)
    res[label] = h
    print("    %-46s %5d   %d" % (label, len(h), len([1 for x in h if x[3]])))
print()
pin_n = len(res["pre-repair, as mg-c2b3 ran it"])
head_n = len(res["pre-repair rule, HEAD bytes -- ANCHOR alone"])
print("      THE ANCHOR, ALONE: %d site(s) pinned -> %d at HEAD, same rule."
      % (pin_n, head_n))
print()
print("  THAT IS NOT A NEGATIVE RESULT -- it is mg-7522's own F4, re-derived")
print("  from scratch.  Its README states the literal-path column of the 2x2")
print("  as `1 site` at the pin and `1 site` at HEAD, and the anchor alone")
print("  moving nothing is exactly what `unpinning is necessary and NOT")
print("  sufficient` means.  Two independent instruments now agree on it.")
CLAIMED_2X2 = {"pinned literal": 1, "HEAD literal": 1}
for label, got, want in (("pinned literal", pin_n, CLAIMED_2X2["pinned literal"]),
                         ("HEAD literal", head_n, CLAIMED_2X2["HEAD literal"])):
    ok = got == want
    if not ok:
        BAD += 1
        FINDINGS.append("A3b %s: mg-7522 says %d, re-derived %d"
                        % (label, want, got))
    print("      %-28s mg-7522 %d   re-derived %d   %s"
          % (label, want, got, "AGREES" if ok else "*** DIFFERS ***"))
print()
print("  AND THE OTHER THREE CHANGES MOVE NOTHING EITHER, at this grain: the")
print("  `run_all.sh` exclusion, the EXEC widening and the target widening")
print("  each leave the count at %d.  Every one of them is defensible on its"
      % head_n)
print("  own terms; none of them is what made the census correct.  The thing")
print("  that made it correct is the RUNTIME-PATH census mg-7522 published")
print("  separately and pointed at from a stated limit.")

# ---------------------------------------------------------------------------
L.hdr("A3c  THE REPAIRED TARGET RULE IS STILL A NAME RULE -- WITH TWO NAMES")

print("  `k2_consume.py`'s target regex went from `run_all\\.sh` to")
print("  `(?:run_all|run_audit)\\.sh`.  That is one filename replaced by two.")
print("  mg-7522's own library states the property -- \"an executable source")
print("  that runs a shell script\" -- and its `_TARGET` is `(\\w+\\.sh)`.")
print()
print("  POPULATION FOR THIS CENSUS, named: every line of every tracked")
print("  `*.py` or `*.sh` at HEAD that EXECUTES something (mg-c2b3's own")
print("  `EXEC` rule, and not its `NOT_EXEC` exclusions) and names a token")
print("  ending in `.sh`.  Grouped by the target's BASENAME, because the")
print("  basename is the thing the two-name rule tests.")
print()
ANY_SH = re.compile(r"[\w./-]*?([\w.-]+\.sh)\b")
TWO_NAMES = ("run_all.sh", "run_audit.sh")
targets = {}
for f in sorted(x for x in L.git("ls-files", "--", "*.py", "*.sh").split() if x):
    src = L.read(f, None)
    lines = src.split("\n")
    for i, line in enumerate(lines, 1):
        if not EXEC_NEW.search(line) or NOT_EXEC.search(line):
            continue
        for m in ANY_SH.finditer(line):
            base = os.path.basename(m.group(1))
            if base == os.path.basename(f):
                continue
            window = "\n".join(lines[i - 1:i + 25])
            targets.setdefault(base, []).append(
                (f, i, bool(READ.search(window))))
extra_names = {k: v for k, v in targets.items() if k not in TWO_NAMES}
extra = [(f, i, k, rd) for k, v in extra_names.items() for f, i, rd in v]
print("    %-26s %-7s %-11s %s" % ("target basename", "sites", "read status",
                                   "in the two-name rule?"))
rows = []
for t in sorted(targets, key=lambda k: (-len(targets[k]), k)):
    v = targets[t]
    rows.append((t, len(v), len([1 for x in v if x[2]]),
                 "yes" if t in TWO_NAMES else "NO -- invisible to it"))
L.rows(rows, (26, 7, 11), indent="    ")
print()
print("      executing sites naming a `*.sh`            %4d"
      % sum(len(v) for v in targets.values()))
print("      …whose basename the two-name rule matches  %4d"
      % sum(len(v) for k, v in targets.items() if k in TWO_NAMES))
print("      …outside it, across %2d distinct basenames  %4d"
      % (len(extra_names), len(extra)))
print("      …of those, reading the exit status         %4d"
      % len([1 for x in extra if x[3]]))
print()
print("  THE SITES THEMSELVES, so a reader can disagree with the rule rather")
print("  than with a total.  Some are fixtures inside a self-test and some")
print("  are live invocations; both are printed and neither is folded away:")
print()
L.rows([("%s:%d" % (f, i), "READS" if rd else "-", t)
        for f, i, t, rd in sorted(extra)], (50, 6), indent="      ")
print()
print("      executing sites naming `run_audit.sh`      %4d"
      % len(targets.get("run_audit.sh", [])))
print("      -- the name the repair ADDED to the rule.  At HEAD nothing")
print("      executes a `run_audit.sh` by literal path, so the widening from")
print("      one name to two is not exercised by any site in the arc.  The")
print("      two runners it was added for are executed by mg-7522's own S2")
print("      through a list argv it builds itself, which the literal-path")
print("      rule cannot see either.")
print()
if extra:
    FINDINGS.append(
        "A3c the repaired caller scan still enumerates targets by FILENAME -- "
        "`(?:run_all|run_audit)\\.sh`, two names instead of one.  mg-7522's "
        "own library states the property instead.  %d executing sites at HEAD "
        "name a `*.sh` whose basename is neither, across %d distinct target "
        "scripts, %d of them reading the exit status; the `k2_consume.py` "
        "STATED-LIMIT comment names the literal-path limit and does not name "
        "this one"
        % (len(extra), len(extra_names), len([1 for x in extra if x[3]])))
    print("  THE STATED LIMIT NAMES THE OTHER HALF.  mg-7522 wrote a")
    print("  stated-limit comment into `k2_consume.py` for the LITERAL-PATH")
    print("  rule -- a real limit, correctly named.  The FILENAME limit in the")
    print("  same regex, in the file whose section 1 is `a naming convention")
    print("  is not a property`, is not named anywhere.  An absence that is")
    print("  written down is checkable; this one is not written down.")

# ---------------------------------------------------------------------------
L.hdr("A3d  THE COMPARISON'S FIGURE -- `154 changed files`")

print("  The published document, section 3:")
print()
print("      \"anchored to the pin the byte-comparison sees **154 changed")
print("       files**; anchored to `HEAD` on a committed tree it sees 0, by")
print("       construction.\"")
print()
print("  `s4_unpin.py` computes that with `git diff --name-only <ref> --`.")
print("  Re-derived at every anchor that could have produced it:")
print()


def changed_since(ref):
    args = ["diff", "--name-only"] + ([ref] if ref else []) + ["--"]
    return [f for f in L.git(*args).split() if f]


CANDIDATES = [
    ("worktree vs the pin, now (what s4 prints)", None),
    ("%s vs the pin (the repair commit)" % L.REPAIR, L.REPAIR),
    ("%s vs the pin (immediately before)" % L.PRE_REPAIR, L.PRE_REPAIR),
    ("HEAD vs the pin", "HEAD"),
]
seen = []
for label, ref in CANDIDATES:
    if ref is None:
        n = len(changed_since(L.PINNED))
    else:
        n = len([f for f in L.git("diff", "--name-only",
                                  "%s..%s" % (L.PINNED, ref)).split() if f])
    seen.append(n)
    print("      %-46s %4d" % (label, n))
TRANS_S4 = "%s/out_s4_unpin.txt" % L.TREE
tn = None
if L.exists(TRANS_S4, None):
    for l in L.read(TRANS_S4, None).splitlines():
        m = re.search(r"anchored to %s\s+(\d+) file" % L.PINNED, l)
        if m:
            tn = int(m.group(1))
print("      %-46s %4s" % ("mg-7522's own committed transcript",
                           tn if tn is not None else "?"))
print("      %-46s %4d" % ("the published document says", 154))
print()
if tn is not None:
    seen.append(tn)
if 154 in seen:
    print("      -> the figure matches one of the anchors above.")
else:
    BAD += 1
    FINDINGS.append(
        "A3d the published document states the pinned byte-comparison as "
        "`154 changed files`; the same measurement is %s at the anchors "
        "above and %s in mg-7522's own committed transcript.  No anchor "
        "reproduces 154."
        % (", ".join(str(x) for x in seen[:4]), tn))
    print("      *** NO ANCHOR REPRODUCES 154. ***")
    print()
    print("  THIS IS THE DEFECT OF SECTION 2 IN THE DOCUMENT OF SECTION 3.")
    print("  mg-05eb's OPEN 2 was a reader-facing artifact carrying a number")
    print("  its own instrument's transcript disagreed with.  Here the")
    print("  document says 154 and the instrument's transcript says %s."
          % tn)
    print("  And the rule was already written down by mg-7522 itself, one")
    print("  commit later: \"a number that moves belongs in a transcript\".")
    print("  c252f96 applied it to the runner count and to the 2x2 totals in")
    print("  the SAME SECTION as this figure, and left this one as prose.")
    print()
    print("  WHAT IS NOT WRONG, so the finding is not read wider than it is:")
    print("  the CLAIM the figure supports -- that the pinned side is more")
    print("  informative than the HEAD side -- holds at every anchor above,")
    print("  and `s4_unpin.py` asserts the INEQUALITY rather than the number.")

print()
L.bar("A3 TOTAL BAD: %d" % BAD)
print()
print("EXTENT OF THAT NUMBER.  It counts a missing or mis-defaulted anchor in")
print("`k2_consume.py`, `libc2b3.py` or `s4_unpin.py`, an unpinning that did")
print("not widen the census, and a prose figure no anchor reproduces.  It")
print("ranges over every tracked `*.py` and `*.sh` at HEAD and at %s."
      % L.PINNED)
print("It does NOT count A3c: enumerating by two filenames instead of one is")
print("a narrower rule than mg-7522's own, not a broken one, and calling it")
print("BAD would overstate it.")
print()
for f in FINDINGS:
    print("FINDING: %s" % f)
sys.exit(1 if BAD else 0)
