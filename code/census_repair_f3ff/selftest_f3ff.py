"""mg-f3ff selftest -- the harness checked against constructed inputs whose
answers are known without running git.

Every check here is one this instrument could plausibly get wrong in a way that
would look like a finding about the census.  In particular the UNKNOWN
propagation is checked at the LIBRARY level here and at the SCRIPT level in
s2/NC3, because a rule enforced in only one of the two is a rule that the next
edit removes silently.
"""
import sys
from datetime import timezone

import lib_f3ff as L

fails = 0


def C(label, ok, detail=""):
    global fails
    fails += L.check(label, ok, detail)


def mk(subject, body=None, adate="2026-07-30T00:00:00+00:00",
       cdate="2026-07-31T00:00:00+00:00"):
    return L.Commit("0" * 40, "a", adate, cdate, subject, body if body is not None else subject)


def main():
    L.banner("mg-f3ff selftest")

    # -- owner extraction -------------------------------------------------
    C("owner: trailing (mg-xxxx) is the owner",
      mk("docs: whatever (mg-1234)").owner == "mg-1234")
    C("owner: trailing id wins over ids earlier in the subject",
      mk("audit of mg-aaaa / abc123 (mg-bbbb)").owner == "mg-bbbb")
    C("owner: no trailing parens -> None",
      mk("pm-onethird: regenerate roadmap").owner is None,
      "unowned commits are still eligible successors; they are not dropped")
    C("owner: trailing text after the parens is not an owner",
      mk("docs (mg-1234) and more").owner is None)
    C("owner: uppercase id normalises",
      mk("docs (MG-1234)").owner == "mg-1234")

    # -- the subject/body distinction, which NC1 rests on ------------------
    c = mk("docs: a repair (mg-1234)", "docs: a repair (mg-1234)\n\nfixes mg-9999\n")
    C("names(): body hit counts", c.names("mg-9999"))
    C("names_subject_only(): body hit does NOT count",
      not c.names_subject_only("mg-9999"),
      "if this ever passed, NC1 would be comparing a reader with itself")
    C("names_subject_only(): subject hit counts", c.names_subject_only("mg-1234"))
    C("names(): case-insensitive", mk("x", "see MG-ABCD").names("mg-abcd"))

    # -- dates -------------------------------------------------------------
    t = L.utc("2026-07-31T04:13:24Z")
    C("utc(): Z suffix parses to UTC", t.tzinfo is not None and t.hour == 4)
    C("parse_iso(): +01:00 offset is converted, not truncated",
      L.parse_iso("2026-07-30T05:31:39+01:00").hour == 4,
      "a naive reader would call this 05:31 and put pre-filing commits after the cut")
    C("parse_iso(): junk -> None", L.parse_iso("not a date") is None)

    # -- UNKNOWN propagation, at the library level -------------------------
    class U:
        unknown, path, ref, label, sha = True, "/nonexistent", "origin/main", "u", None

    class K:
        unknown, path, ref, label = False, ".", "HEAD", "k"
        sha = "0" * 40

    C("successors(): UNKNOWN repo returns None, not []",
      L.successors(U, "mg-1234", t) is None,
      "None and [] must not be interchangeable -- this is the ticket's subject")
    v, per, unk = L.census_row({"u": U}, "mg-1234", t)
    C("census_row(): one UNKNOWN repo -> row UNKNOWN", v == "UNKNOWN" and unk == ["u"])
    v2, _p2, _u2 = L.census_row({"u": U, "k": K}, "mg-1234", t)
    C("census_row(): UNKNOWN is STICKY across a readable repo", v2 == "UNKNOWN",
      "a count over part of the population is not a count")
    C("generations(): UNKNOWN repo -> None",
      L.generations({"u": U}, "mg-1234", t) is None)

    # -- a Fetched whose fetch was forced to fail --------------------------
    f = L.Fetched(".", "forced", force_fail=True)
    C("Fetched(force_fail): unknown is True", f.unknown)
    C("Fetched(force_fail): sha is None, not a stale leftover", f.sha is None)
    C("Fetched(force_fail): line() says UNKNOWN", "UNKNOWN" in f.line())
    C("Fetched(force_fail): line() does NOT say 'no successor'",
      "no successor" not in f.line().lower())
    fmiss = L.Fetched("/no/such/path/at/all", "missing")
    C("Fetched(missing repo): unknown is True", fmiss.unknown)

    # -- the NUL record split, which the log parser rests on ---------------
    repo = L._run(["git", "rev-parse", "--show-toplevel"]).stdout.strip()
    cs = L.git_log(repo, "HEAD", extra=["-5"])
    C("git_log(): parses this repo's own last 5 commits", len(cs) == 5,
      f"got {len(cs)}")
    C("git_log(): no subject contains a newline",
      all("\n" not in x.subject for x in cs),
      "a body newline read as a record boundary is how mg-c067's figure grammar died")
    C("git_log(): every record has a parsed author date",
      all(x.adate is not None for x in cs))
    C("git_log(): bodies are non-empty for these commits",
      all(x.body.strip() for x in cs))

    # -- the population/blind-spot text is actually present ----------------
    C("POPULATION text names origin/main", "origin/main" in L.POPULATION)
    C("POPULATION text names the UNKNOWN case", "UNKNOWN" in L.POPULATION)
    C("BLIND_SPOTS lists 8 numbered spots",
      all(f"B{i}" in L.BLIND_SPOTS for i in range(1, 9)))

    # -- the row table matches the tickets on disk -------------------------
    files = L.ticket_files()
    for n, row, filed, parent in L.ROWS:
        p = files.get(row)
        C(f"row {n}: {row} exists in the work store", p is not None)
        if p:
            txt = L.ticket_text(p)
            C(f"row {n}: its ticket names its parent {parent}",
              parent in txt)
            C(f"row {n}: its `created:` matches the filing instant in ROWS",
              filed.replace("Z", "") in txt,
              "the filing instant is the cut; a wrong one silently moves every count")

    print()
    print(f"== selftest: {fails} FAIL ==")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
