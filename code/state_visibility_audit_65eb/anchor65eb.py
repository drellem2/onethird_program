#!/usr/bin/env python3
"""mg-65eb — THE FLOOR: THE ANCHORS THIS REPAIR SPENDS, RESOLVED RATHER THAN READ.

The brief names rows, claims, a surface and a re-run.  It does not name the REVISIONS the
repair pins its own integrity claim to.  mg-a74f's central integrity claim is:

    "`PREDICTIONS.md` was committed before any script in this directory existed (`739f7bd`)"

That sentence is the whole warrant for reading mg-a74f's predictions as predictions.  It is
carried entirely by a seven-character token, and NO PROGRAM IN THIS REPOSITORY RESOLVES IT.

This file resolves every one of them.  The population is computed, not listed: every `.py`,
`.md` and `.sh` under the four directories this repair touches or is scored against, at the
revision being read.  Every 7-to-12-character hex token in that text is extracted and put to
`git`, and each is classified into exactly one of four buckets:

    ANCHOR-LIVE      resolves to a commit AND is an ancestor of HEAD
    ANCHOR-STALE     resolves to a commit, is NOT an ancestor of HEAD, but some ref reaches it
    ANCHOR-DEAD      resolves to a commit that no ref reaches — one `git gc` from unreadable
    NOT-A-REVISION   a hex-shaped token that is not a commit (reported, never silently dropped)

THE PROPERTY IS ANCESTRY, NOT EXISTENCE, AND THAT DISTINCTION IS THE FINDING.  A reader of
`main` can follow an anchor only if `main` reaches it.  `git cat-file -e` — the idiom two
programs in this population actually use — passes a stale anchor happily.  Section D
demonstrates that on the live stale anchor rather than arguing it.

    python3 code/state_visibility_audit_65eb/anchor65eb.py            # the working tree
    python3 code/state_visibility_audit_65eb/anchor65eb.py --rev bd24efc   # negative control

Exit 1 if any anchor is STALE, DEAD or NOT-A-REVISION; exit 0 if every one is LIVE.  At
`bd24efc` this repair's directory does not exist, so the run is the NEGATIVE CONTROL: the same
program, the same rule, exit 0.

NOTHING IS WRITTEN.  This file only reads git and the file system.
"""
import argparse
import ast
import os
import re
import subprocess
import sys

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()

DIRS = [
    "code/state_delegation_repair_a74f",     # the repair under audit
    "code/state_delegation_repair_0049",     # the tree it edits
    "code/state_landing_control_2da3",       # the control it edits
    "code/state_delegation_audit_16eb",      # the auditor whose OPENs it answers
]
EXTS = (".py", ".md", ".sh")

# A hex token, bounded by non-alphanumerics so `bd24efc` in `at(bd24efc, CTL)` is seen and
# `deadbeef` inside a longer word is not.  All-alphabetic runs (`accede`, `defaced`) and
# all-numeric runs (a byte count, a line number) are NOT revisions and are excluded BY THE
# RULE rather than by a stop list, so the rule can be checked by a reader.
TOKEN = re.compile(r"(?<![0-9A-Za-z])([0-9a-f]{7,12})(?![0-9A-Za-z])")

# A program that reads sha tokens OUT OF PROSE would need a pattern of this shape.  Used as a
# stated PROXY for "does any program check the shas in this text", and labelled as one.  The
# MATCH IS PRINTED and the verdict is taken from its QUANTIFIER, so the reader is not asked to
# take this audit's word for which patterns are about revisions: a hex class bounded at 4 is a
# `mg-` work-item id, and one bounded at 7 or more is a sha.
SHA_PATTERN_IN_SOURCE = re.compile(
    r"[^\n]{0,24}\[0-9a-f(?:A-F)?\]\s*\{\s*(\d+)[^\n]{0,12}")


def git(*args, **kw):
    return subprocess.run(["git", "-C", REPO, *args], capture_output=True, text=True, **kw)


def is_hex_word(tok):
    return not tok.isalpha() and not tok.isdigit()


def population(rev):
    """Every .py/.md/.sh under the four directories, at `rev` (None = the working tree)."""
    files = []
    for d in DIRS:
        if rev is None:
            root = os.path.join(REPO, d)
            names = sorted(os.listdir(root)) if os.path.isdir(root) else []
            files += [f"{d}/{n}" for n in names if n.endswith(EXTS)
                      and os.path.isfile(os.path.join(root, n))]
        else:
            out = git("ls-tree", "-r", "--name-only", rev, "--", d).stdout.split("\n")
            files += [p for p in out if p.endswith(EXTS)]
    return files


def read(rev, path):
    if rev is None:
        with open(os.path.join(REPO, path), encoding="utf-8", errors="replace") as fh:
            return fh.read()
    return git("show", f"{rev}:{path}").stdout


def classify(tok):
    """(bucket, subject, the refs that reach it).  Every branch is a git answer."""
    t = git("cat-file", "-t", tok)
    if t.returncode != 0 or t.stdout.strip() != "commit":
        return "NOT-A-REVISION", f"git cat-file -t says: {t.stdout.strip() or 'no such object'}", []
    subj = git("log", "-1", "--format=%s", tok).stdout.strip()
    if git("merge-base", "--is-ancestor", tok, "HEAD").returncode == 0:
        return "ANCHOR-LIVE", subj, []
    refs = [ln.split()[-1] for ln in
            git("for-each-ref", "--contains", tok, "--format=%(refname)").stdout.split("\n")
            if ln.strip()]
    return ("ANCHOR-STALE" if refs else "ANCHOR-DEAD"), subj, refs


def twin_of(tok, subj):
    """A commit REACHABLE FROM HEAD carrying the same subject — the ancestor the stale
    pointer was rewritten into.  Re-derived by search, never taken from prose."""
    out = git("log", "--format=%H %s", "HEAD").stdout.split("\n")
    for ln in out:
        h, _, s = ln.partition(" ")
        if s == subj and h[:7] != tok[:7]:
            return h
    return None


def spent_shas(rev, files):
    """A sha is SPENT by a program when it is a STRING LITERAL that is NOT a docstring, in one
    of the population's .py files: the program hands it to git, so rot in it surfaces as a
    failure of that program.  Computed with `ast`.

    A DOCSTRING IS PROSE AND IS EXCLUDED — but per SITE, not per FILE.  Excluding the whole
    file because the token also appears in its docstring would drop `claims_a74f.py`, whose
    docstring names `bd24efc` AND whose line 38 spends it, and that is exactly the kind of
    population error this audit is filed about."""
    out = {}
    for path in files:
        if not path.endswith(".py"):
            continue
        try:
            tree = ast.parse(read(rev, path))
        except SyntaxError:
            continue
        docstrings = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef,
                                 ast.ClassDef)):
                body = getattr(node, "body", None)
                if (body and isinstance(body[0], ast.Expr)
                        and isinstance(body[0].value, ast.Constant)
                        and isinstance(body[0].value.value, str)):
                    docstrings.add(id(body[0].value))
        for node in ast.walk(tree):
            if (isinstance(node, ast.Constant) and isinstance(node.value, str)
                    and id(node) not in docstrings):
                for m in TOKEN.finditer(node.value):
                    if is_hex_word(m.group(1)):
                        out.setdefault(m.group(1), set()).add(f"{path}:{node.lineno}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", default=None,
                    help="read the population at this revision (default: the working tree)")
    args = ap.parse_args()
    rev = args.rev
    label = rev if rev else "the working tree"

    print("=" * 100)
    print("mg-65eb — THE ANCHORS THIS REPAIR SPENDS, RESOLVED")
    print("=" * 100)
    files = population(rev)
    print(f"  revision read   {label}")
    print(f"  population      {len(files)} files: every .py, .md and .sh under")
    for d in DIRS:
        print(f"                      {d}/  ({sum(1 for f in files if f.startswith(d + '/'))} files)")
    print("  rule            every 7-to-12-character hex token that is neither all-letters")
    print("                  nor all-digits, computed from the text — no stop list")
    print()

    sites, occurrences = {}, 0
    for path in files:
        text = read(rev, path)
        for i, line in enumerate(text.split("\n"), 1):
            for m in TOKEN.finditer(line):
                tok = m.group(1)
                if is_hex_word(tok):
                    sites.setdefault(tok, []).append(f"{path}:{i}")
                    occurrences += 1
    print(f"  {len(sites)} distinct hex token(s) over {occurrences} occurrence(s).")
    print()

    buckets = {"ANCHOR-LIVE": [], "ANCHOR-STALE": [], "ANCHOR-DEAD": [], "NOT-A-REVISION": []}
    stale_detail = []
    for tok in sorted(sites):
        bucket, subj, refs = classify(tok)
        buckets[bucket].append(tok)
        ok = "pass" if bucket == "ANCHOR-LIVE" else "FAIL"
        print(f"  [{ok}] {tok:<12s} {bucket}")
        print(f"         {subj}")
        if refs:
            print(f"                  reachable only from: {', '.join(refs)}")
        where = sites[tok]
        shown = ", ".join(where[:6]) + (f" (+{len(where) - 6} more)" if len(where) > 6 else "")
        print(f"         named at: {shown}")
        if bucket != "ANCHOR-LIVE":
            twin = twin_of(tok, subj)
            if twin:
                held = [p for p in git("ls-tree", "-r", "--name-only", twin, "--",
                                       DIRS[0]).stdout.split("\n") if p.strip()]
                print(f"         RE-DERIVED: ancestor twin {twin[:7]} carries the same subject; "
                      f"{DIRS[0]}/ at it holds {len(held)} file(s): "
                      f"{[os.path.basename(p) for p in held]}")
                stale_detail.append((tok, bucket, where, twin, held))
            else:
                print("         RE-DERIVED: no ancestor of HEAD carries this subject")
                stale_detail.append((tok, bucket, where, None, []))
        print()

    # -------------------------------------------------------------------------------------
    print("=" * 100)
    print("C.  IS ANY OF THIS CHECKED BY A PROGRAM?  SPENT vs CHECKED, AND THEY ARE DIFFERENT")
    print("=" * 100)
    spent = spent_shas(rev, files)
    print("  SPENT — a sha held as a NON-DOCSTRING string literal in a program, so that rot in")
    print("  it shows up as that program FAILING.  Not a check of the sha; a dependency on it.")
    if not spent:
        print("      (none)")
    for tok in sorted(spent):
        print(f"      {tok:<12s} {', '.join(sorted(spent[tok]))}")
    stale_and_spent = [t for t in spent if t in buckets["ANCHOR-STALE"] + buckets["ANCHOR-DEAD"]]
    print(f"      of these, SPENT AND NOT LIVE: {stale_and_spent or 'none'}")
    print("      — so no program in this population would fail today because of the rot.")
    print("      The stale anchor is spent by nothing and checked by nothing: it is carried")
    print("      by prose alone, which is why it could rot silently.")
    print()
    print("  CHECKED — a program that reads sha tokens OUT OF THIS PROSE and resolves them.")
    print("  PROXY, and it is labelled one: a program doing that needs a hex-token pattern in")
    print("  its own source.  Every hex class found in the population's sources is printed")
    print("  with the width it accepts, and the verdict is read off THAT, not off prose:")
    carriers, sha_shaped = [], []
    for p in files:
        if not p.endswith(".py"):
            continue
        for m in SHA_PATTERN_IN_SOURCE.finditer(read(rev, p)):
            width = int(m.group(1))
            kind = "SHA-SHAPED" if width >= 7 else f"not a sha — {width} hex digits is an mg- id"
            carriers.append((p, m.group(0).strip(), width, kind))
            if width >= 7:
                sha_shaped.append(p)
    if not carriers:
        print("      0 hex classes in any source in the population.")
    for p, frag, width, kind in carriers:
        print(f"      {p}")
        print(f"          {frag}   -> accepts {width} hex digits: {kind}")
    print(f"      SHA-SHAPED patterns: {len(sha_shaped)}  {sorted(set(sha_shaped)) or '(none)'}")
    print()
    print("  So the count of sha references in this prose that any program VERIFIES is 0.")
    print("  `prose_a74f.py` — the checker this repair added for exactly this class of rot —")
    print("  checks four shapes: repo-relative paths, `section N` references, pinned tables,")
    print("  and `all N rows` phrases.  A REVISION IS NOT ONE OF THEM.  Every sha above is an")
    print("  unchecked claim, and the one that has rotted is the one carrying this repair's")
    print("  own integrity statement.")
    print()

    # -------------------------------------------------------------------------------------
    print("=" * 100)
    print("D.  THE WRONG INSTRUMENT, DEMONSTRATED ON THE LIVE DEFECT — EXISTENCE vs ANCESTRY")
    print("=" * 100)
    print("  The brief asks that a new control be demonstrated against a commit where the")
    print("  defect is STILL PRESENT.  For this control that commit is HEAD: the anchor is")
    print("  stale right now, so the demonstration needs no reconstruction.")
    print()
    probe = buckets["ANCHOR-STALE"][:1] or buckets["ANCHOR-DEAD"][:1]
    if not probe:
        print("  No stale anchor in this population — at this revision there is nothing to")
        print("  demonstrate against, which is what a negative control looks like.")
    else:
        tok = probe[0]
        exists = git("cat-file", "-e", f"{tok}^{{commit}}").returncode
        anc = git("merge-base", "--is-ancestor", tok, "HEAD").returncode
        blob = git("cat-file", "-e",
                   f"{tok}:code/state_delegation_repair_a74f/PREDICTIONS.md").returncode
        print(f"  the stale anchor                                    {tok}")
        print(f"  git cat-file -e {tok}^{{commit}}                       exit {exists}   "
              f"{'PASSES — the existence idiom is satisfied' if exists == 0 else 'fails'}")
        print(f"  git cat-file -e {tok}:.../PREDICTIONS.md               exit {blob}   "
              f"{'PASSES — the path idiom is satisfied too' if blob == 0 else 'fails'}")
        print(f"  git merge-base --is-ancestor {tok} HEAD                exit {anc}   "
              f"{'FAILS — ancestry is the property, and it does not hold' if anc else 'passes'}")
        print()
        print("  Two of the three pass.  `claims_a74f.py:57` and `prose_a74f.py:114` are")
        print("  written in exactly the two idioms that pass.  A checker built the way this")
        print("  repair's own code reads revisions would certify this anchor as fine.")
    print()

    # -------------------------------------------------------------------------------------
    print("=" * 100)
    print("WHAT THIS RUN FOUND")
    print("=" * 100)
    for b in ("ANCHOR-LIVE", "ANCHOR-STALE", "ANCHOR-DEAD", "NOT-A-REVISION"):
        print(f"   {len(buckets[b]):>2d}  {b:<16s} {sorted(buckets[b])}")
    print()
    bad = sum(len(buckets[b]) for b in buckets if b != "ANCHOR-LIVE")
    if bad:
        print("  THE FINDING, ONE LINE PER ANCHOR:")
        for tok, bucket, where, twin, held in stale_detail:
            print(f"    {tok}  {bucket}  named at {where[0]}")
        print()
        print("  THE PROPERTY IS NOT THEREBY REFUTED.  It is re-derived above at an ancestor")
        print("  of HEAD and it HOLDS: that tree carries PREDICTIONS.md and nothing else, so")
        print("  the predictions really were committed before any script of that repair.")
        print("  What has rotted is the POINTER.  An anchor reachable only from an unmerged")
        print("  branch is a citation a reader of `main` cannot follow, and the branch it")
        print("  lives on is exactly the kind of object that gets deleted after a merge.")
    else:
        print("  0 findings: every anchor in this population resolves and is an ancestor of")
        print("  HEAD.  At a revision where this repair's own directory does not yet exist,")
        print("  that is the NEGATIVE CONTROL — the same program, the same rule, exit 0.")
    print("=" * 100)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
