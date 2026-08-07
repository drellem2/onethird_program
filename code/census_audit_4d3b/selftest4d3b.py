"""mg-4d3b selftest -- THIS AUDIT'S OWN HARNESS, on constructed inputs whose
answers are known without running git, plus the three claims of fact this audit
makes about the subject that are cheap enough to check directly.

Every check here is one this audit could plausibly get wrong in a way that
would look like a finding about mg-f3ff.  Two in particular:

  * THE FILING INSTANTS.  `lib4d3b.ROWS` transcribes four timestamps.  A wrong
    one silently moves every count in a1, a2 and a4, and would look exactly
    like a disagreement with mg-f3ff.  They are re-derived from the work store
    here rather than trusted.
  * THE FIXTURE ALPHABET.  ⚠️ DEFECT OF THIS SELFTEST, KEPT AND FIXED IN
    PLACE: the first version of the fixtures used ids like `mg-pppp`, which is
    outside the `[0-9a-f]{4}` alphabet BOTH readers use for the owner match.
    Two checks failed against code that was correct -- an assertion refuted by
    its own fixture.  Found by the selftest failing, which is the only reason
    it is not in a1's numbers.  The fixtures are hex now.

  * THE PREMISE STRINGS.  a2's whole finding rests on which rows' TITLES say
    `no landing commit`.  If that transcription is wrong, a2 is wrong.  The
    titles are re-read from the work store.
"""
import os
import re
import sys
from datetime import timezone

import lib4d3b as L

fails = 0


def C(label, ok, detail=""):
    global fails
    fails += L.check(label, ok, detail)


def mk(subject, message=None, adate="2026-07-30T00:00:00+00:00",
       cdate="2026-07-31T00:00:00+00:00"):
    return L.Commit("r", "0" * 40, "a", adate, cdate, subject,
                    message if message is not None else subject)


class FakeRepo:
    """A repo object with a hand-written commit list and a settable
    `unknown` -- so the UNKNOWN rule is checked without a filesystem."""

    def __init__(self, label, commits, unknown=False):
        self.label, self._c, self._u = label, commits, unknown

    @property
    def unknown(self):
        return self._u

    def commits(self, include_merges=True):
        if self._u:
            raise RuntimeError("commits() on UNKNOWN")
        return self._c


def ticket_path(tid):
    for root, _d, files in os.walk(L.WORK_STORE):
        for fn in files:
            if fn == f"{tid}.md" or fn.startswith(f"{tid}.md."):
                return os.path.join(root, fn)
    return None


def main():
    L.banner("mg-4d3b selftest")

    # -- owner extraction ---------------------------------------------------
    C("owner: the TRAILING (mg-xxxx) is the owner",
      mk("docs: whatever (mg-1234)").owner == "mg-1234")
    C("owner: a trailing id wins over ids earlier in the subject",
      mk("audit of mg-aaaa (mg-bbbb)").owner == "mg-bbbb")
    C("owner: no trailing parens -> None",
      mk("pm-onethird: regenerate roadmap").owner is None,
      "an unowned commit is still an eligible successor and is not dropped")
    C("owner: text after the parens means no owner",
      mk("docs (mg-1234) and more").owner is None)

    # -- naming -------------------------------------------------------------
    C("names(): matches in the BODY, not only the subject",
      mk("docs: x (mg-1111)", "docs: x (mg-1111)\n\ncloses mg-2222").names("mg-2222"))
    C("names(): case-insensitive",
      mk("docs (mg-1111)", "docs (mg-1111)\nMG-2222").names("mg-2222"))
    C("names(): a non-occurrence is False",
      not mk("docs (mg-1111)").names("mg-9999"))

    # -- the UNKNOWN rule, at the library level -----------------------------
    good = FakeRepo("good", [mk("x (mg-aaaa)", "x (mg-aaaa)\nmg-0abc")])
    bad = FakeRepo("bad", [], unknown=True)
    T = L.utc("2026-07-31T00:00:00Z")
    C("successors(): UNKNOWN repo -> None, never []",
      L.successors(bad, "mg-0abc", T) is None)
    C("successors(): readable repo -> a list",
      isinstance(L.successors(good, "mg-0abc", T), list))
    v, per, unk = L.row_verdict([good, bad], "mg-0abc", T)
    C("row_verdict(): UNKNOWN is STICKY across a readable repo",
      v == "UNKNOWN" and unk == ["bad"],
      "one unreadable repo makes the row UNKNOWN; a count over part of a "
      "population is not a count")
    C("row_verdict(): the unreadable repo's entry is None, not []",
      per["bad"] is None)
    v2, _p, _u = L.row_verdict([good], "mg-0abc", T)
    C("row_verdict(): the SAME harness returns REFUTED when it can read",
      v2 == "REFUTED",
      "without this the UNKNOWN checks above pass vacuously for a "
      "constant-UNKNOWN harness")
    v3, _p, _u = L.row_verdict([good], "mg-0fff", T)
    C("row_verdict(): and UPHELD when it reads and finds nothing",
      v3 == "UPHELD",
      "UPHELD and UNKNOWN are produced by different inputs -- the "
      "distinction this audit is about")

    # -- the date bound and the owner exclusion -----------------------------
    late = FakeRepo("late", [mk("x (mg-aaaa)", "x (mg-aaaa)\nmg-0abc",
                                adate="2026-08-30T00:00:00+00:00")])
    C("successors(): a commit AFTER the instant is excluded",
      L.successors(late, "mg-0abc", T) == [])
    own = FakeRepo("own", [mk("x (mg-0abc)", "x (mg-0abc)\nmg-0abc")])
    C("successors(): the parent's OWN commit is not its successor",
      L.successors(own, "mg-0abc", T) == [])
    C("successors(exclude_own=False): the same commit IS returned",
      len(L.successors(own, "mg-0abc", T, exclude_own=False)) == 1,
      "this switch is the whole of a2 -- if it did nothing, a2 measures nothing")

    # -- landings -----------------------------------------------------------
    C("landings(): finds the parent's OWN commits",
      len(L.landings([own], "mg-0abc", T)) == 1)
    C("landings(): UNKNOWN repo -> None, never []",
      L.landings([own, bad], "mg-0abc", T) is None)
    C("landings(): a commit merely NAMING the parent is not a landing",
      L.landings([good], "mg-0abc", T) == [])

    # -- clocks -------------------------------------------------------------
    skew = FakeRepo("skew", [mk("x (mg-aaaa)", "x (mg-aaaa)\nmg-0abc",
                                adate="2026-07-30T00:00:00+00:00",
                                cdate="2026-08-30T00:00:00+00:00")])
    C("clocks: a rebase-skewed commit is IN on author and OUT on committer",
      len(L.successors(skew, "mg-0abc", T, clock="author")) == 1
      and len(L.successors(skew, "mg-0abc", T, clock="committer")) == 0,
      "B5; both are reported and neither is called the truth")

    # -- the record parser --------------------------------------------------
    repos = L.open_repos()
    if any(r.unknown for r in repos):
        C("live repos readable", False,
          "the selftest's live half is UNKNOWN, and is reported UNKNOWN "
          "rather than skipped")
    else:
        cs = repos[0].commits()
        C("git_log: every record parsed to 6 fields", bool(cs))
        C("git_log: no subject contains a newline",
          all("\n" not in c.subject for c in cs),
          "a body newline read as a record boundary is how mg-c067's "
          "figure grammar died")
        C("git_log: every record has a parsed author date",
          all(c.adate is not None for c in cs))
        C("git_log: the message contains the subject (%B, not %b)",
          all(c.subject.strip()[:40] in c.message for c in cs[:50]))

        # -- THE TRANSCRIBED CONSTANTS, re-derived --------------------------
        for n, row, filed, parent, premise in L.ROWS:
            p = ticket_path(row)
            C(f"row {n}: {row} exists in the work store", p is not None)
            if not p:
                continue
            txt = open(p, encoding="utf-8", errors="replace").read()
            m = re.search(r"^created:\s*(\S+)", txt, re.M | re.I)
            got = m.group(1).strip('"\'') if m else None
            ok = bool(got) and L.utc(got.replace("Z", "+00:00")) == L.utc(filed)
            C(f"row {n}: transcribed filing instant == the store's `created`",
              ok, f"{filed} vs {got} -- a wrong instant silently moves every count")
            tm = re.search(r"^title:\s*(.*)$", txt, re.M)
            title = tm.group(1) if tm else txt
            claims = "no landing commit" in title.lower()
            C(f"row {n}: the `no landing commit` clause is transcribed correctly",
              claims == ("no landing commit" in premise),
              f"a2's entire finding rests on this: title says "
              f"{'YES' if claims else 'NO'}, ROWS says "
              f"{'YES' if 'no landing commit' in premise else 'NO'}")
            C(f"row {n}: the ticket names its parent {parent}",
              parent in txt.lower())

    print(f"\n== selftest: {fails} FAIL ==")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
