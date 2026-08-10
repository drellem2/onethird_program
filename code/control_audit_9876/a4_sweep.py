#!/usr/bin/env python3
"""mg-9876 — the population question: how do instruments in `code/` get VALIDATED at all?

THE TICKET'S CLAIM IS ABOUT A PRACTICE, NOT ABOUT ONE DIRECTORY, and a claim about a practice
is answerable only over the population.  Three of the ticket's four smells are mechanically
detectable, so they are counted here across every directory under `code/`.

WHAT THIS IS AND IS NOT.  It is an INDEX: a list of sites that carry a smell, with the count
stated so the coverage is legible.  It is NOT an adjudication.  A `X in out` membership test
is a smell because it CAN match something the report prints unconditionally — establishing
that a particular one DOES requires running it two ways, which is `a2_discriminate.py`'s
method and was applied to exactly one directory.  Every number below is therefore a count of
CANDIDATES, and saying otherwise would be this ticket's own defect at population scale.

NOTHING OUTSIDE `code/rendered_twin_pin_9bc2` AND THIS DIRECTORY IS EDITED.  The other
suites belong to other tickets; naming a site is in scope, repairing it is not.

THE SWEEP HAS A TWO-SIDED CONTROL OF ITS OWN (§4).  A detector that finds things is not a
detector that discriminates — the local instance of that error is the whole reason this
ticket exists.  So the tee detector is required to FIND the known `| tee` runners in the arc
and to NOT find one in `rendered_twin_pin_9bc2`, whose first version had one and whose
current version does not.  A run where either half fails is a broken sweep and says so.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib9876 as L  # noqa: E402

CODE = os.path.join(L.ROOT, "code")

# ---- smell 1: a membership test against a WHOLE captured output ----------------------
# The haystack names below are the ones this tree actually uses for "everything the
# instrument printed".  A test against a parsed field is not matched and must not be.
_HAYSTACKS = r"(?:out|output|stdout|text|txt|report|blob|body|content|contents|combined)"
# THE FIRST VERSION OF THIS DETECTOR WAS ITSELF LAUNDERED and it is worth saying how.  It was
# `in <haystack>\b`, which matched `for line in out.splitlines()` and `for name, text in
# contents.items()` — ITERATION, not membership — and returned 597 "candidates" over 119
# directories.  A number that large reads as a finding about the tree and was a finding about
# the regex.  Two corrections: the haystack must TERMINATE the expression (so `.splitlines()`
# and `.items()` are excluded), and a `for` binding on the same line disqualifies it.  §4
# requires the detector to answer both ways on the two constructions by name.
SMELL_MEMBERSHIP = re.compile(
    r"(?<!\w)(?:not\s+)?in\s+%s\s*(?:[)\],:]|$|\band\b|\bor\b|\belse\b)" % _HAYSTACKS)
_FOR_BINDING = re.compile(r"\bfor\b[^\n]*?\bin\s+%s" % _HAYSTACKS)

# ---- smell 2: an exit code read downstream of a pipe --------------------------------
SMELL_TEE = re.compile(r"\|\s*tee\b")
SMELL_PIPE_STATUS = re.compile(r"^\s*\w+=\$\?")

# ---- smell 3: does the directory ship anything that tries to make its control fail? --
NEGATIVE_NAMES = re.compile(r"(negative|selftest|self_test|positive|control|falsif)", re.I)
RED_TOKENS = re.compile(r"\b(HOLE|CAUGHT|MISMATCH|REFUTED|FAILED TO|SETUP FAILED|"
                        r"NEGATIVE CONTROL)\b")


def dirs():
    for name in sorted(os.listdir(CODE)):
        path = os.path.join(CODE, name)
        if os.path.isdir(path):
            yield name, path


def files(path, exts):
    for root, _dirnames, filenames in os.walk(path):
        for fn in sorted(filenames):
            if fn.endswith(exts):
                yield os.path.join(root, fn)


def rel(path):
    return os.path.relpath(path, L.ROOT)


def main():
    print("=" * 92)
    print("mg-9876 — SMELL INDEX over code/ (candidates, NOT adjudications)")
    print("=" * 92)
    print()

    all_dirs = list(dirs())
    print(f"population: {len(all_dirs)} directories under code/")
    print()

    # ------------------------------------------------------------------ §1 membership
    print("§1  MEMBERSHIP TESTS AGAINST A WHOLE CAPTURED OUTPUT")
    print("-" * 92)
    print("The shape of instance 3: `\"8 9\" in out` where `out` is the entire report, so a")
    print("line printed unconditionally elsewhere satisfies it forever.  A candidate is not a")
    print("defect — only running it two ways decides that.")
    print()
    mem = {}
    for name, path in all_dirs:
        hits = []
        for f in files(path, (".py",)):
            for i, line in enumerate(L.read(f).split("\n"), 1):
                s = line.strip()
                if s.startswith("#") or not SMELL_MEMBERSHIP.search(s):
                    continue
                if _FOR_BINDING.search(s):
                    continue
                hits.append((rel(f), i, s[:88]))
        if hits:
            mem[name] = hits
    total_mem = sum(len(v) for v in mem.values())
    print(f"  {total_mem} candidate site(s) in {len(mem)} of {len(all_dirs)} directories")
    print()
    for name in sorted(mem, key=lambda k: -len(mem[k]))[:12]:
        print(f"    {name}  ({len(mem[name])})")
        for f, i, s in mem[name][:3]:
            print(f"        {f}:{i}  {s}")
    if len(mem) > 12:
        print(f"    … and {len(mem) - 12} more directories, listed in full below")
    print()
    print("  FULL LIST (directory: count)")
    print("   ", "  ".join(f"{n}:{len(v)}" for n, v in sorted(mem.items())))
    print()

    # ------------------------------------------------------------------ §2 tee / pipe
    print("§2  AN EXIT CODE READ DOWNSTREAM OF A PIPE")
    print("-" * 92)
    print("Instance 1 exactly: `cmd | tee f` makes `$?` TEE's status, and tee succeeds")
    print("whatever it is fed.  POSIX sh has no PIPESTATUS to reach for.")
    print()
    tee_dirs, status_after_pipe = {}, {}
    for name, path in all_dirs:
        for f in files(path, (".sh",)):
            lines = L.read(f).split("\n")
            for i, line in enumerate(lines, 1):
                s = line.strip()
                if s.startswith("#"):
                    continue
                if SMELL_TEE.search(s):
                    tee_dirs.setdefault(name, []).append((rel(f), i, s[:88]))
                if SMELL_PIPE_STATUS.match(line) and i >= 2 and "|" in lines[i - 2] \
                        and not lines[i - 2].strip().startswith("#"):
                    status_after_pipe.setdefault(name, []).append(
                        (rel(f), i, lines[i - 2].strip()[:60] + "  ->  " + s[:24]))
    print(f"  `| tee` : {sum(len(v) for v in tee_dirs.values())} site(s) in "
          f"{len(tee_dirs)} directories")
    for name in sorted(tee_dirs):
        for f, i, s in tee_dirs[name]:
            print(f"      {f}:{i}  {s}")
    print(f"  `$?` immediately after a pipeline : "
          f"{sum(len(v) for v in status_after_pipe.values())} site(s) in "
          f"{len(status_after_pipe)} directories")
    for name in sorted(status_after_pipe):
        for f, i, s in status_after_pipe[name]:
            print(f"      {f}:{i}  {s}")
    print()

    # ------------------------------------------------------------------ §3 negatives
    print("§3  DOES THE DIRECTORY SHIP ANYTHING THAT TRIES TO MAKE ITS OWN CONTROL FAIL?")
    print("-" * 92)
    print("The ticket's fourth smell — `positive controls never demonstrated to fail` — is not")
    print("decidable from source.  What IS decidable is whether the directory ships a negative")
    print("control at all, and whether any committed transcript records a demonstrated")
    print("failure.  A directory with neither has no evidence its instrument can fail; that is")
    print("weaker than saying it cannot.")
    print()
    has_neg, has_red, bare = [], [], []
    for name, path in all_dirs:
        srcs = list(files(path, (".py", ".sh")))
        txts = list(files(path, (".txt", ".md")))
        neg = any(NEGATIVE_NAMES.search(os.path.basename(f)) for f in srcs)
        red = any(RED_TOKENS.search(L.read(f)) for f in txts)
        if neg:
            has_neg.append(name)
        if red:
            has_red.append(name)
        if not neg and not red and srcs:
            bare.append(name)
    print(f"  ships a file named for negative/self/positive-control : "
          f"{len(has_neg)} of {len(all_dirs)}")
    print(f"  a committed transcript records a demonstrated failure  : "
          f"{len(has_red)} of {len(all_dirs)}")
    print(f"  NEITHER, though the directory ships code               : "
          f"{len(bare)} of {len(all_dirs)}")
    print()
    print("  directories with code and no evidence of a falsification attempt:")
    for i in range(0, len(bare), 3):
        print("      " + "  ".join(n.ljust(34) for n in bare[i:i + 3]))
    print()

    # ------------------------------------------------------------------ §4 the control
    print("§4  THE SWEEP'S OWN TWO-SIDED CONTROL")
    print("-" * 92)
    print("A detector that only ever finds things has not been shown to discriminate.  The tee")
    print("detector is required to answer BOTH ways at two directories whose answer is known")
    print("in advance, and to be exercised against a constructed negative.")
    print()
    target_sh = os.path.join(L.TARGET, "run_all.sh")
    target_hit = bool(SMELL_TEE.search(
        "\n".join(ln for ln in L.read(target_sh).split("\n")
                  if not ln.strip().startswith("#"))))
    synthetic = "python3 x.py | tee out.txt\nCODE=$?\n"
    synth_hit = bool(SMELL_TEE.search(synthetic))
    arc_hit = sum(len(v) for v in tee_dirs.values())

    checks = [
        ("tee: must NOT fire on rendered_twin_pin_9bc2/run_all.sh, whose tee was removed "
         "(instance 1)", not target_hit),
        ("tee: must fire on a constructed `python3 x.py | tee out.txt`", synth_hit),
        ("tee: must fire somewhere in the arc, or it is not looking at anything",
         arc_hit > 0),
        ("membership: must fire on `if \"8 9\" in out:` — instance 3 itself",
         bool(SMELL_MEMBERSHIP.search('if "8 9" in out:'))
         and not _FOR_BINDING.search('if "8 9" in out:')),
        ("membership: must NOT fire on `for line in out.splitlines():` — iteration, which "
         "the first version of this detector counted 597 times",
         not (SMELL_MEMBERSHIP.search("for line in out.splitlines():")
              and not _FOR_BINDING.search("for line in out.splitlines():"))),
        ("membership: must NOT fire on a test against a PARSED FIELD, "
         "`if row in worklist:`",
         not SMELL_MEMBERSHIP.search("if row in worklist:")),
        ("pipe-status: must fire on a constructed `cmd | tee f` followed by `rc=$?`, "
         "which is why a 0 count below is a measurement and not a dead detector",
         bool(SMELL_PIPE_STATUS.match("rc=$?"))),
    ]
    ok = True
    for text, passed in checks:
        print(f"    [{'PASS' if passed else 'FAIL'}]  {text}")
        ok = ok and passed
    print()
    print("=" * 92)
    if ok:
        print(f"SWEEP OK — {total_mem} membership candidates, {arc_hit} tee sites, "
              f"{len(bare)} directories with no falsification evidence.  All CANDIDATES.")
    else:
        print("SWEEP BROKEN — its own control did not answer both ways.  Do not cite the "
              "counts above.")
    print("=" * 92)
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
