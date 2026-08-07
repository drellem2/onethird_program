"""mg-4d3b a5 -- DOES THE DELIVERABLE REPRODUCE, IN ITS OWN NEW CODE, THE
DEFECT IT WAS SENT TO REPAIR?

The defect mg-f3ff was filed about has one sentence: *a check that cannot
distinguish "I looked and there was nothing" from "I could not look"*.
`lib_f3ff.successors`' own docstring states the rule in the strongest terms
available: *"Returns None when the repo is UNKNOWN -- callers must NOT treat
None as an empty list.  That confusion is the whole subject of this ticket."*

Three probes, each EXECUTED rather than read:

  E1  A SOURCE CENSUS of the sites where the deliverable's own scripts turn
      that None into a list, and of the sites that call len() on it.  The
      idiom is `or []`, which is exactly the merger, spelled in two
      characters.  Each site is then CLASSIFIED by whether it can be reached
      under a fetch failure, because a site that cannot be reached is a
      latent defect and saying otherwise would be this audit inflating its
      own finding.

  E2  THE WORK STORE, a THIRD channel.  `ticket_files()` walks a directory;
      an absent or unreadable store yields `{}` and `s3_graph.py` prints
      `0 ticket file(s) readable` and `(none)` for every row.  mg-f3ff names
      this as blind spot B8 in prose.  A caveat is checked against its
      hypothesis by running it, not by reading it -- so this runs s3 against
      an empty store and reads what it prints.

  E3  `allow_fetch=False`.  Wired to no caller and no CLI flag as merged, so
      it is LATENT and is reported as latent.  Executed anyway, because a
      dead branch that says `ok` for a repo nobody fetched is the ticket's
      own defect sitting in the library built to remove it, and the next
      edit that wires it up ships it.

⚠️ AND THE AUDITOR IS NOT EXEMPT.  E1 runs the same source census over
`lib4d3b.py` and this audit's own scripts.  Whatever it finds is printed in
the same table.

EXIT: 1 if a control of THIS instrument fails.  Findings do not set it.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

import lib4d3b as L

F3FF = os.path.abspath(os.path.join(L.HERE, "..", "census_repair_f3ff"))
SELF = L.HERE

MERGE_RE = re.compile(r"successors\([^()]*(?:\([^()]*\)[^()]*)*\)\s*or\s*\[\]")
LEN_RE = re.compile(r"len\(\s*(?:L\.)?successors\(")


def _prose_lines(src):
    """Line numbers that are inside a string literal or a comment.

    ⚠️ THIS EXISTS BECAUSE THE FIRST VERSION OF THIS CENSUS DID NOT HAVE IT,
    and it reported a hit in `a3_fetchfail.py` that is a SENTENCE OF MY OWN
    PROSE describing the defect -- a rule that reads text as code, in the
    section whose subject is a rule that reads one thing as another.  Kept as
    a defect of this instrument; the fix is to CLASSIFY rather than to drop,
    so a prose hit is still shown and is labelled PROSE."""
    import io
    import tokenize
    out = set()
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(src).readline))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return out
    for t in toks:
        if t.type in (tokenize.STRING, tokenize.COMMENT):
            for ln in range(t.start[0], t.end[0] + 1):
                out.add(ln)
    return out


def census(root, label):
    print(f"  --- {label}  ({root}) ---")
    rows = []
    for fn in sorted(os.listdir(root)):
        if not fn.endswith(".py"):
            continue
        src = open(os.path.join(root, fn), encoding="utf-8").read()
        prose = _prose_lines(src)
        for i, line in enumerate(src.splitlines(), 1):
            kind = ("or []" if MERGE_RE.search(line)
                    else "len(None)" if LEN_RE.search(line) else None)
            if kind:
                rows.append((fn, i, kind, "PROSE" if i in prose else "CODE ",
                             line.strip()))
    if not rows:
        print("      0 sites.")
    for fn, i, kind, where, line in rows:
        print(f"      {fn}:{i:<4} {where} {kind:<10} {line[:90]}")
    code = [r for r in rows if r[3] == "CODE "]
    print(f"      TOTAL: {len(rows)} site(s), {len(code)} in CODE, "
          f"{len(rows) - len(code)} in PROSE (a string or comment describing one)")
    print()
    return code


def main():
    L.banner("mg-4d3b a5 -- does the repair reproduce its own defect class?")
    red = 0

    print("=" * 78)
    print("E1 -- SOURCE CENSUS: where None is turned into a list, or len()'d")
    print("=" * 78)
    print("  THE RULE, quoted from the subject's own library:")
    print("    \"Returns None when the repo is UNKNOWN -- callers must NOT treat")
    print("     None as an empty list.  That confusion is the whole subject of")
    print("     this ticket.\"                      lib_f3ff.py, successors()")
    print()
    subj = census(F3FF, "SUBJECT: code/census_repair_f3ff")
    mine = census(SELF, "AUDITOR: code/census_audit_4d3b -- the same rule, applied to me")

    print("  REACHABILITY, so a latent site is not billed as a live one:")
    print("    A site is LIVE if a fetch failure can reach it.  a3 ran the real")
    print("    thing: s1_rows.py died at :131 under arm G, which is the len()")
    print("    site, so the len() sites are LIVE.  The `or []` sites in s1 and s3")
    print("    sit in code that a fetch failure also reaches, and each silently")
    print("    contributes 0 to a sum instead of refusing to sum.")
    print("    s2_controls.py:130-131 is inside NC1, which runs with a HEALTHY")
    print("    fetch by construction -- LATENT there.")
    print()
    print("  ⚠️ WHAT THIS IS AND IS NOT.  It is NOT a claim that mg-f3ff's four row")
    print("     verdicts are wrong -- a1 re-derived all four from a disjoint reader")
    print("     and they reproduce exactly.  It IS the claim that the rule the")
    print("     deliverable states in its library is broken by the deliverable's own")
    print("     scripts, at the sites listed above, and that a3 shows what that")
    print("     prints when a fetch fails.")
    print()

    tmp = L.scratch_dir("self-")

    print("=" * 78)
    print("E2 -- THE WORK STORE: is B8 a caveat, or a caveat that was checked?")
    print("=" * 78)
    stage = os.path.join(tmp, "stage_ws")
    shutil.copytree(F3FF, stage)
    empty = os.path.join(tmp, "empty_work_store")
    os.makedirs(empty)
    lib = os.path.join(stage, "lib_f3ff.py")
    src = open(lib, encoding="utf-8").read()
    patched, n = re.subn(r'WORK_STORE = .*', f'WORK_STORE = {empty!r}', src, count=1)
    red += L.check("E2 setup: WORK_STORE was actually redirected", n == 1,
                   "an unpatched setup would pass VACUOUSLY, which is this arc's "
                   "signature failure and is checked rather than assumed")
    open(lib, "w", encoding="utf-8").write(patched)
    r = subprocess.run([sys.executable, "s3_graph.py"], cwd=stage,
                       capture_output=True, text=True, timeout=600)
    out = r.stdout + r.stderr
    print(f"  s3_graph.py exit under an EMPTY work store: {r.returncode}")
    for line in out.splitlines():
        if ("work store" in line or "tickets whose body names" in line
                or "(none)" in line or "UNKNOWN" in line
                or "successor TICKET" in line or "P9" in line or "P10" in line):
            print("    | " + line.rstrip()[:150])
    print()
    findings = []
    if re.search(r"work store: .*, 0 ticket file\(s\) readable", out):
        findings.append(
            "F6  s3 prints `0 ticket file(s) readable` and `(none)` for all four\n"
            "      rows, with NO UNKNOWN anywhere, when the store it depends on is\n"
            "      empty.  Its own next line names B8 -- `a deleted ticket is absent\n"
            "      here` -- so the hazard is DECLARED and NOT ENFORCED.  The rule\n"
            "      lib_f3ff enforces twice for repos (library + NC3) has no\n"
            "      counterpart for the third channel s3 actually reads.")
    if "UNKNOWN" not in out.split("work store:")[-1][:4000]:
        findings.append(
            "F7  and nothing downstream degrades: P8/P9/P10 are still SCORED off an\n"
            "      empty graph, so the section reports prediction outcomes computed\n"
            "      from a channel that returned nothing.")
    for f in findings:
        print("    " + f)
    if not findings:
        print("    (none -- s3 refused to answer from an empty store)")
    print()
    print("  P12 SCORING (pre-registered at 70%): "
          + ("HIT" if findings else "MISS"))
    print()

    print("=" * 78)
    print("E3 -- `allow_fetch=False`: 'I could not look' rendered as 'ok'")
    print("=" * 78)
    sys.path.insert(0, F3FF)
    import lib_f3ff as F                                    # noqa: E402
    fm = F.fetch_all(allow_fetch=False)
    for f in fm.values():
        print("    " + f.line().replace("\n", "\n    "))
    any_ok = [f for f in fm.values() if not f.unknown]
    print()
    if any_ok:
        f0 = any_ok[0]
        print(f"    {f0.label}: unknown={f0.unknown}  fetch_rc={f0.fetch_rc}  "
              f"reason={f0.reason!r}")
        print("    >>> F8  The repo reports `ok`, prints a resolved sha and a full")
        print("            staleness figure, and the string `fetch skipped by flag`")
        print("            is stored in `.reason` -- which `line()` prints ONLY on")
        print("            the UNKNOWN branch.  So the one fact that would tell the")
        print("            reader no fetch happened is computed and then not shown.")
        print("            The four rows would then be derived, and printed, against")
        print("            whatever the last fetch left.")
        print("    >>> AND ITS SIZE, STATED: `allow_fetch` is wired to no caller and")
        print("            no CLI flag in the merged tree (verified by grep, D6 of")
        print("            PREDICTIONS.md, before this file existed).  It is LATENT.")
        print("            Calling a dead branch a live defect would be this audit")
        print("            committing the class of error it came to look for.")
        v, _p, unk = F.census_row(fm, "mg-16eb", F.utc("2026-07-31T04:22:15Z"))
        print(f"    >>> and the row it would print: {v} (unreadable: {unk or 'none'})"
              " -- an answer, not an UNKNOWN.")
    else:
        print("    Every repo came back UNKNOWN under allow_fetch=False.")
        print("    P9 is a MISS and is kept as written.")
    print("    P9 SCORING: " + ("HIT" if any_ok else "MISS"))
    print()
    print("  ⚠️ THIS AUDIT'S OWN lib4d3b.Repo TAKES THE OTHER BRANCH ON PURPOSE:")
    r_self = L.Repo("self-check", L.WORKTREE, fetch=False)
    red += L.check("lib4d3b: fetch=False yields UNKNOWN, not `ok`",
                   r_self.unknown,
                   "the auditor is held to the rule it is enforcing")
    print()
    print(f"== a5 exit: {1 if red else 0} ==")
    return 1 if red else 0


if __name__ == "__main__":
    sys.exit(main())
