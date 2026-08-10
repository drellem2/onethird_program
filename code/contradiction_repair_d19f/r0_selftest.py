"""mg-d19f r0 — FORCED ARMS.

Every arm here is a way this ticket could produce the right verdict for the wrong reason,
or the wrong verdict outright. Four of the six are arms that must REFUSE something; an
instrument whose every arm says yes has measured nothing.

The arm this ticket most needs is A2, and it is not about mg-51f4 at all. It is about MY
OWN adjudication rule: the ticket forbids deciding the contradiction by recency, and A2
DEMONSTRATES why by showing the recency rule returning OPPOSITE answers depending on which
of two defensible clocks you read. A rule that can be made to say either thing is not a
rule, and A2 is what stops "the later document wins" from looking reasonable.
"""

import sys

import libd19f as L

fails = []


def arm(name, ok, detail):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    for line in detail.split("\n"):
        print(f"         {line}")
    if not ok:
        fails.append(name)


L.banner("r0 — SELFTEST, SIX FORCED ARMS")

# ---------------------------------------------------------------- A1
# item_of() must read AUTHORSHIP off the commit message trailer, not off a mention.
# 18a1347 is mg-29fe's audit commit and its text NAMES mg-51f4 repeatedly. mg-64cb's index
# attributes a commit to every id it mentions, which is correct for "which items does this
# commit concern" and wrong for "which item wrote it" -- and r2's whole finding is that the
# second question was being answered with the first.
a1_rev = "18a1347"
a1_got = L.item_of(a1_rev)
a1_mentions = "mg-51f4" in L.git("show", a1_rev)
arm("A1  authorship is read off the trailer, and REFUSES a mere mention",
    a1_got == "mg-29fe" and a1_mentions,
    f"item_of({a1_rev}) = {a1_got}   (expected mg-29fe)\n"
    f"the same commit mentions mg-51f4: {a1_mentions}  <- the trap")

# ---------------------------------------------------------------- A2
# THE FORBIDDEN RULE, RUN, so that its refusal is demonstrated and not asserted.
d_51f4 = L.author_date(L.C_51F4_LANDING)
d_28ff_read = L.author_date(L.C_28FF_AS_READ)
d_28ff_repair = L.author_date(L.C_28FF_REPAIR)
at_landing = "mg-51f4" if d_51f4 > d_28ff_read else "mg-28ff"
at_head = "mg-51f4" if d_51f4 > d_28ff_repair else "mg-28ff"
arm("A2  'the more recent document wins' answers BOTH ways -> refused",
    at_landing != at_head,
    f"mg-51f4  landing   {d_51f4}\n"
    f"mg-28ff  as read   {d_28ff_read}   -> recency picks {at_landing}\n"
    f"mg-28ff  repaired  {d_28ff_repair}   -> recency picks {at_head}\n"
    "one rule, two answers. The adjudication in r1 uses neither.")

# ---------------------------------------------------------------- A3
# The revision the adjudication reads must actually be the text mg-51f4 read. If the
# sentence under audit is absent from cb496e9, every joint below is about the wrong file.
orig = L.show(L.C_28FF_AS_READ, L.DOC_28FF).split("\n")
a3_hits = L.find(orig, "100 % at every enumerated")
arm("A3  cb496e9 IS the text mg-51f4 read (the audited sentence is present)",
    len(a3_hits) == 1 and len(orig) > 400,
    f"'100 % at every enumerated' at {L.C_28FF_AS_READ}: lines {a3_hits}\n"
    f"file length {len(orig)} lines")

# ---------------------------------------------------------------- A4
# NON-VACUITY. find() must return nothing for a needle that is not there. Without this,
# every 'the joint is present' check below could be a probe that matches anything.
a4 = L.find(orig, "this string is not in mg-28ff at any revision")
arm("A4  the locator REFUSES an absent needle (non-vacuity)",
    a4 == [],
    f"absent needle -> {a4}")

# ---------------------------------------------------------------- A5
# The repair I am about to make must not be checkable only against itself. HEAD's mg-51f4
# doc must still carry BOTH false sites when this suite is authored; if it does not, either
# somebody else repaired them or I am reading the wrong file, and in both cases the report
# below would be describing work that was already done.
head51 = L.head_lines(L.DOC_51F4)
s1 = L.find(head51, "correctly labelled as such at every appearance")
s2 = L.find(head51, "was correctly labelled a sample at each")
# D4 (kept): this arm asserted `len(...) == 1` and went RED the moment the repair landed --
# not because a site had vanished but because §0.0's repair table QUOTES both sentences, so
# each is now findable twice. An exact-count probe over a document that gains a section
# quoting itself is the same shape as mg-64cb's D1, whose survival classifier scored six
# superseded figures LIVE and every one was a quotation inside the document repairing it.
# The arm asks the question it meant: is each site still FINDABLE.
arm("A5  BOTH false sites are present in the file this ticket edits",
    len(s1) >= 1 and len(s2) >= 1,
    f"site A (SS4)  line {s1}\n"
    f"site B (SS11) line {s2}\n"
    "(two hits each after the repair: the struck original, and §0.0's table quoting it)\n"
    "NOTE: this arm still PASSES after the repair lands, and that is the point of the\n"
    "arc's strike-and-correct practice: the false sentence is struck, never deleted, so\n"
    "a reader who arrives with the old text in hand can still find it. A repair that made\n"
    "this arm go quiet would have removed the evidence along with the error.")

# A5' -- the post-repair form. Exactly one of A5 / A5' holds at any commit, and printing
# both is what makes this suite readable before AND after the edit.
a5p = (L.find(head51, "NOT correctly labelled at every appearance")
       or L.find(head51, "FALSIFIED BY SITE 1 OF THE VERY TABLE BELOW"))
arm("A5' the repair markers are present (post-repair form)",
    True,  # informational: reported, never used to pass or fail the suite
    f"repair markers at lines {a5p}  "
    f"({'REPAIRED' if a5p else 'NOT YET REPAIRED'})")

# ---------------------------------------------------------------- A6
# The measurement the adjudication rests on must come from a TRANSCRIPT, not from prose.
# mg-51f4's document and mg-28ff's repair row both print '168 of 86278'; if I read the
# number off either document I would be checking a claim against itself.
t = open(f"{L.REPO}/code/sweep_loss_51f4/out_s3_n7.txt", encoding="utf-8").read()
a6 = [ln.strip() for ln in t.split("\n") if "168 of 86278" in ln]
arm("A6  168 of 86278 is read from the TRANSCRIPT, not from either document",
    len(a6) >= 1,
    "code/sweep_loss_51f4/out_s3_n7.txt:\n  " + "\n  ".join(a6))

print()
if fails:
    print(f"SELFTEST FAILED: {len(fails)} arm(s): {', '.join(fails)}")
    sys.exit(1)
print("SELFTEST: 6 of 6 forced arms pass (A5' is informational).")
