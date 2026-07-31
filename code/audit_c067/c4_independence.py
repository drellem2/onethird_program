"""C4 -- REDUNDANCY SPECIFIED BY INDEPENDENCE OF FAILURE MODE, NOT BY COUNT.

The parent has three routes from a transcript to the tree it was measured at:

    DECLARED   the `POPULATION ANCHOR: commit=... count=... digest=...` line
    INFERRED   resolving the hex tokens in the transcript's own text
    RECOVERED  searching `--all` for a commit whose population has the digest

Three routes is a count.  The question the standing rule asks is different:
FOR EACH ROUTE, CONSTRUCT THE INPUT THAT BREAKS IT AND CONFIRM THE OTHERS
SURVIVE.  Where two routes die to one input they are not two.

⚠️ AND THE LAST SECTION TURNS THE SAME QUESTION ON THIS AUDIT'S OWN TOOLING.
"""
import sys

sys.path.insert(0, "../publication_anchor_132a")
import anchor_132a as P  # noqa: E402

import lib_c067 as L  # noqa: E402

OWN = "code/publication_anchor_132a/out_anchor_132a.txt"


def main(argv):
    as_of = L.as_of_from_argv(argv)
    L.banner(as_of)

    text = L.blob_at(as_of, OWN)
    pub = L.publishing_commit(OWN, as_of)
    d = L.declared_anchor(text)

    def strip_hex(t):
        """Remove every resolvable-looking hex token, killing INFERRED."""
        return L.HEX_RE.sub("XXXXXXX", t)

    # ----------------------------------------------------------------- C4a
    L.head("C4a -- EACH ROUTE BROKEN IN TURN, ON A REAL TRANSCRIPT")
    print(f"""
The subject is the parent's own committed transcript, published at {pub[:7]}.
Each row below is that file with ONE route disabled; the verdict is the
parent's own, and what is being read off is WHICH ROUTE PICKED UP THE SLACK.
""")
    cases = [
        ("intact -- all three available", text,
         "the control: nothing broken"),
        ("DECLARED broken (anchor line deleted)",
         L.DECLARED_RE.sub("POPULATION ANCHOR: (removed)", text, 1),
         "kills DECLARED and RECOVERED together -- one line carries both"),
        ("DECLARED sha mangled, digest intact",
         L.DECLARED_RE.sub(
             f"POPULATION ANCHOR: commit={'0' * 40} count={d['count']} "
             f"digest={d['digest']} scope={d['scope']}", text, 1),
         "kills DECLARED only; RECOVERED should carry it"),
        ("digest mangled, DECLARED sha intact",
         L.DECLARED_RE.sub(
             f"POPULATION ANCHOR: commit={d['commit']} count={d['count']} "
             f"digest={'f' * 16} scope={d['scope']}", text, 1),
         "kills RECOVERED only; DECLARED should carry it"),
        ("anchor line deleted AND body hex stripped",
         strip_hex(L.DECLARED_RE.sub("POPULATION ANCHOR: (removed)", text, 1)),
         "kills all three -- must fail closed, not fall through green"),
        ("anchor line deleted, body hex intact",
         L.DECLARED_RE.sub("POPULATION ANCHOR: (removed)", text, 1),
         "INFERRED is the only survivor"),
    ]
    print(f"    {'construction':<44} {'verdict':<22} route")
    results = {}
    for label, t, _ in cases:
        v = P.verdict_from_text(t, pub, as_of)
        results[label] = v
        print(f"    {label:<44} {v['verdict']:<22} {v['anchor_kind']}")

    closed = results["anchor line deleted AND body hex stripped"]
    L.record(closed["verdict"] in P.RED,
             f"C4a WITH ALL THREE ROUTES BROKEN THE LATTICE FAILS CLOSED: "
             f"`{closed['verdict']}`, which is red.  A redundancy scheme whose "
             f"exhausted state is green would be a blessing rather than a "
             f"check, and this one is not")

    mangled_sha = results["DECLARED sha mangled, digest intact"]
    mangled_dig = results["digest mangled, DECLARED sha intact"]
    L.record(mangled_sha["verdict"] not in P.RED
             and mangled_dig["verdict"] not in P.RED,
             f"C4a' AND THE TWO HALVES OF THE ANCHOR LINE ARE GENUINELY "
             f"INDEPENDENT OF EACH OTHER: mangling the sha leaves "
             f"`{mangled_sha['verdict']}` via {mangled_sha['anchor_kind']}, "
             f"mangling the digest leaves `{mangled_dig['verdict']}` via "
             f"{mangled_dig['anchor_kind']}.  Each survives the other's "
             f"corruption, which is the redundancy `A2d` claims and it holds "
             f"under construction rather than only in the synthetic case")

    # ----------------------------------------------------------------- C4b
    L.head("C4b -- BUT THE INPUT THAT BREAKS TWO ROUTES AT ONCE")
    dropped = results["DECLARED broken (anchor line deleted)"]
    print(f"""
The digest is the answer to a lost sha.  It is stored IN THE SAME LINE AS THE
SHA, written by ONE call to `anchor_line()`, in ONE `print`.  So the failure
that takes the sha takes the digest with it -- not a corrupted sha, which C4a
shows is survivable, but a MISSING LINE: a transcript truncated by a crash, a
transcript from a run whose publication step predates the field, an editor
touching the header, or the redirect in `run_all.sh` dying mid-write.

    anchor line deleted -> verdict {dropped['verdict']}, route {dropped['anchor_kind']}
""")
    L.record(dropped["anchor_kind"] == "INFERRED",
             f"C4b DECLARED AND RECOVERED ARE NOT TWO ROUTES, THEY ARE ONE "
             f"LINE.  Delete it and both die together; what catches the "
             f"transcript is {dropped['anchor_kind']}, giving "
             f"`{dropped['verdict']}`.  ⚠️ THE SURVIVOR IS THE ROUTE THE "
             f"PARENT ITSELF CALLS STRUCTURALLY WEAKER: `A1e` says inference "
             f"'SELECTS FOR AGREEMENT and therefore CANNOT WITNESS `WRONG WHEN "
             f"WRITTEN`'.  So under the common-mode failure of a dropped "
             f"anchor line, the remaining redundancy cannot witness the very "
             f"defect this arc exists to catch")
    L.finding(
        f"C4b' ⚠️ AND THAT DEGRADATION IS SILENT AT THE ONE PLACE IT MATTERS.  "
        f"The verdict for a transcript whose anchor line was dropped is "
        f"`{dropped['verdict']}` -- the same word, with `(anchor "
        f"{dropped['anchor_kind']})` beside it.  `A1e` COUNTS inferred anchors "
        f"and explains the weakness, so the information is on the page; what "
        f"is missing is any rung that treats `a transcript that HAD a declared "
        f"anchor and now does not` differently from `a legacy transcript that "
        f"never had one`.  The first is evidence of damage and the second is "
        f"just history, and the lattice gives them the same label")

    # ----------------------------------------------------------------- C4c
    L.head("C4c -- THE WORKING TREE IS IGNORED, CONSTRUCTED RATHER THAN "
           "TRUSTED")
    print("""
`verdict_for()` documents that it reads from git and never from disk.  A
post-merge audit that read the working tree would not be auditing the merge.
Asserted here by CORRUPTING THE FILE ON DISK and re-running -- and the on-disk
bytes are restored and re-verified afterwards.
""")
    import pathlib
    p = pathlib.Path(L.REPO) / OWN
    before = p.read_bytes()
    v_before = P.verdict_for(OWN, as_of)["verdict"]
    try:
        p.write_text("999 .py files under `code/` and nothing else\n")
        v_during = P.verdict_for(OWN, as_of)["verdict"]
    finally:
        p.write_bytes(before)
    restored = p.read_bytes() == before
    print(f"    verdict before corrupting the working tree : {v_before}")
    print(f"    verdict while the file on disk says 999    : {v_during}")
    print(f"    on-disk bytes restored byte-identically    : "
          f"{'YES' if restored else 'NO'}")
    L.record(v_before == v_during and restored,
             f"C4c THE WORKING TREE IS GENUINELY IGNORED: the verdict is "
             f"`{v_during}` whether the file on disk publishes 495 or 999, "
             f"because the bytes are read from git at the publishing commit.  "
             f"⚠️ THIS IS LOAD-BEARING FOR THE WHOLE `--at` REMEDY -- an audit "
             f"of a past commit that read present-day bytes would answer a "
             f"question nobody asked.  The probe restored the file "
             f"byte-identically ({'verified' if restored else 'NOT VERIFIED'})")

    # ----------------------------------------------------------------- C4d
    L.head("C4d -- THE SAME QUESTION TURNED ON THIS AUDIT'S OWN TOOLING")
    print("""
`Check your own tooling for the defect you are repairing.`  This instrument
derives populations by its own `git ls-tree` walk.  If that walk and the
parent's disagree, one of us is wrong and every count in both transcripts is
in doubt -- so they are compared across a spread of commits, which is a check
neither could perform alone.
""")
    revs = [r for r in (L.git("rev-list", as_of, "-n", "40") or "").split()]
    revs += ["4a06b4c", "89d6aa1", "3958b5a", "77306a7", "803bd50"]
    disagreements = []
    for r in revs:
        full = L.resolve(r)
        if not full:
            continue
        mine = L.population_count(full)
        theirs = len(P.py_files_at(full))
        if mine != theirs:
            disagreements.append((full[:7], mine, theirs))
    print(f"    commits compared : {len(revs)}")
    print(f"    disagreements    : {len(disagreements)}  "
          f"{disagreements[:5] if disagreements else ''}")
    L.record(not disagreements,
             f"C4d TWO INDEPENDENT DERIVATIONS OF THE POPULATION AGREE ON ALL "
             f"{len(revs)} COMMIT(S) COMPARED -- this module's own `ls-tree "
             f"-r` walk with a blob-type filter, against the parent's "
             f"`py_files_at()`.  ⚠️ THIS IS THE ROW THAT LICENSES EVERY OTHER "
             f"COUNT IN THIS AUDIT.  Had they disagreed, the finding would "
             f"have been about the two of us and not about the anchor, and "
             f"this instrument would have had no standing to report a figure "
             f"at all.  It is also the check the arc's own history says is "
             f"owed: `8c55168` records two copies of `figures()` disagreeing "
             f"on 3")

    return L.summary(as_of)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
