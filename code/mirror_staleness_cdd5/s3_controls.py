"""mg-cdd5 s3 -- CONTROLS.  One arm per enumerated way THIS instrument could
exhibit the defect it is sent to find (PREDICTIONS.md E1-E7).

The arms are RUN, not argued.  Each states what it plants, what a defective
instrument would say, and what this one says.  An arm is SATISFACTORY when the
instrument answers the way a working one must -- which for two of them means
REFUSING to fire, not firing.

Exit 1 if any arm is unsatisfactory.  That IS a fact about this instrument, so
unlike s0-s2 it is allowed to set the status.
"""
import os
import sys

import lib_cdd5 as L

MIRROR_PIN = "912f1b1"
#: onethird_program commit immediately before this ticket repaired the two
#: line anchors at STATE.md:112.  Named so the erased finding stays replayable.
PRE_REPAIR_REV = "0a8415b"
CHEEGER = "docs/OneThird-L1b-Reverse-Cheeger-Proof-Attempt.md"

RESULTS = []


def arm(name, ok, detail):
    RESULTS.append((name, ok, detail))
    print("  [%s] %s" % ("OK  " if ok else "FAIL", name))
    for ln in detail.splitlines():
        print("        %s" % ln)
    print()


def main():
    L.banner("mg-cdd5 s3 -- CONTROLS: can this instrument exhibit its own subject?")
    mirror = L.find_mirror()
    if mirror is None:
        print("  UNREADABLE: mirror repo not found; no arm can run.")
        print("== s3 exit: 1 ==")
        return 1

    # ---- E1: reading the working copy instead of a revision ---------------
    # A defective sweep opens the file on disk.  Disk is always HEAD's blob,
    # so such a sweep answers `what does HEAD say`, never `what is true` --
    # and the two differ exactly while the checkout is behind.
    #
    # ⚠️ THE OBVIOUS PHRASING OF THIS ARM POINTS THE WRONG WAY, and this
    # instrument nearly shipped it.  Scoring `disk == blob@912f1b1` makes the
    # arm go RED the day the mirror is brought current -- i.e. red because
    # its own finding was ACTED ON, which is mg-d0e2's shape and is not a
    # control.  What is scored instead is direction-stable: disk tracks HEAD
    # (a property of this reader), and the two pinned revisions differ (a
    # property of history that no repair can undo).  The checkout's current
    # staleness is REPORTED, not scored.
    disk = None
    p = os.path.join(mirror, CHEEGER)
    if os.path.isfile(p):
        with open(p, encoding="utf-8", errors="replace") as fh:
            disk = fh.read()
    head = L.git(["rev-parse", "HEAD"], cwd=mirror).strip()
    at_head = L.blob_at(mirror, head, CHEEGER)
    at_pin = L.blob_at(mirror, MIRROR_PIN, CHEEGER)
    at_tip = L.blob_at(mirror, "origin/main", CHEEGER)
    disk_is_head = (disk == at_head)
    history_differs = L.classify(at_pin, at_tip) != L.UNCHANGED
    behind = int(L.git(["rev-list", "--count", "HEAD..origin/main"],
                       cwd=mirror).strip())
    correct = L.classify(at_pin, at_tip)
    arm("E1 the working-copy read answers HEAD, not the truth -- DEMONSTRATED",
        disk_is_head and history_differs,
        "disk content == blob@HEAD(%s): %s -- a disk-reading sweep can only\n"
        "ever report what the checkout has.\n"
        "blob@%s vs blob@origin/main: %s -- a fact about history, and no\n"
        "repair to the checkout can make it UNCHANGED.\n"
        "REPORTED, NOT SCORED: the checkout is %d commit(s) behind right now,\n"
        "so a disk-reading sweep %s miss the strike today."
        % (L.short(head), disk_is_head, MIRROR_PIN, correct, behind,
           "WOULD" if behind else "would not"))

    # ---- E3: absent at both revisions must not compare clean --------------
    ghost = "docs/THIS-FILE-HAS-NEVER-EXISTED-cdd5.md"
    g_old = L.blob_at(mirror, MIRROR_PIN, ghost)
    g_new = L.blob_at(mirror, "origin/main", ghost)
    naive_equal = (g_old is g_new)               # MISSING is MISSING -> True
    cls = L.classify(g_old, g_new)
    arm("E3 absent-at-both is NOT scored as unchanged",
        naive_equal and cls == L.ABSENT_BOTH,
        "a naive differ compares the two absences equal (`old is new` -> %s)\n"
        "and calls a citation to a file that has NEVER EXISTED clean.\n"
        "classify() returns %s." % (naive_equal, cls))

    # ---- E4: the relative link must not be resolved on the filesystem -----
    raw = "../one_third_width_three/docs/OneThird-L1b-Reverse-Cheeger-Proof-Attempt.md"
    naive = os.path.normpath(os.path.join(L.program_root(), raw))
    resolved, _ = L._normalise(raw)
    arm("E4 the `../` link is normalised, not filesystem-joined",
        (not os.path.exists(naive)) and resolved == CHEEGER,
        "joining the link onto this worktree's root gives\n"
        "  %s\n"
        "which exists: %s -- a sweep doing that finds nothing and reports a\n"
        "zero with the authority of having looked.\n"
        "_normalise() returns %r." % (naive, os.path.exists(naive), resolved))

    # ---- E5: file-level and section-level answers must differ -------------
    # §5 exists at both revisions; §5.0' exists only at the tip.  A sweep that
    # only diffs whole files cannot tell those two apart, and the second is
    # the sharper finding.
    s5_old = L.section_present(at_pin, "5")
    s5_new = L.section_present(at_tip, "5")
    s50_old = L.section_present(at_pin, "5.0'")
    s50_new = L.section_present(at_tip, "5.0'")
    arm("E5 the section-level answer is not the file-level answer",
        s5_old and s5_new and (not s50_old) and s50_new,
        "file-level: %s (one bit for the whole document).\n"
        "section-level: §5 mirror=%s tip=%s ; §5.0' mirror=%s tip=%s.\n"
        "the citation names both; only the second half fails to resolve, and\n"
        "a file-level differ cannot say that."
        % (correct, s5_old, s5_new, s50_old, s50_new))

    # ---- E6: the HTML extractor must be shown able to see -----------------
    # A markdown-only extractor returns 0 on the twin and that 0 reads as
    # "the twin cites nothing".  Planted href, plus the real twin's count.
    planted = ('<p>see <a href="../one_third_width_three/docs/'
               'OneThird-L1b-Reverse-Cheeger-Proof-Attempt.md">§5</a></p>')
    seen = L.extract_citations(planted, "planted.html")
    md_only = [c for c in seen if c.kind == "md"]
    arm("E6 the HTML href extractor is shown able to see BEFORE its zero is quoted",
        len(seen) == 1 and seen[0].path == CHEEGER and seen[0].kind == "href"
        and len(md_only) == 0,
        "planted one <a href=...> into synthetic HTML.\n"
        "extractor returns %d citation(s), kind=%s, path=%s.\n"
        "a markdown-only extractor returns %d and its zero would be a parser\n"
        "fact wearing the clothes of a corpus fact."
        % (len(seen), seen[0].kind if seen else "-",
           seen[0].path if seen else "-", len(md_only)))

    # ---- planted stale citation: the sweep MUST fire ----------------------
    planted_md = ("A claim supported by "
                  "[`x`](../one_third_width_three/%s) §5 and §5.0'." % CHEEGER)
    pc = L.dedupe(L.extract_citations(planted_md, "planted.md"))
    fired = False
    if pc:
        c = pc[0]
        k = L.classify(L.blob_at(mirror, MIRROR_PIN, c.path),
                       L.blob_at(mirror, "origin/main", c.path))
        fired = (k == L.STRUCK)
    arm("POSITIVE the planted stale citation FIRES, and fires as STRUCK",
        fired,
        "planted a citation with exactly the ticket's shape and ran the real\n"
        "classifier on it: %s.  sections picked up: %s"
        % (k if pc else "NO CITATION EXTRACTED",
           pc[0].sections if pc else "-"))

    # ---- negative: a citation to genuinely unchanged text must NOT fire ---
    # Choose a path present at both revisions and byte-identical.  Found, not
    # assumed: if no such path exists the arm REFUSES rather than passing.
    same = None
    names = L.git(["ls-tree", "-r", "--name-only", MIRROR_PIN],
                  cwd=mirror).splitlines()
    changed = set(L.git(["diff", "--name-only", MIRROR_PIN, "origin/main"],
                        cwd=mirror).splitlines())
    for n in names:
        if n not in changed and n.endswith((".md", ".tex")):
            same = n
            break
    if same is None:
        arm("NEGATIVE an unchanged citation does not fire", False,
            "no unchanged .md/.tex path exists between the two revisions --\n"
            "arm REFUSES rather than reporting a pass it did not earn.")
    else:
        k2 = L.classify(L.blob_at(mirror, MIRROR_PIN, same),
                        L.blob_at(mirror, "origin/main", same))
        arm("NEGATIVE an unchanged citation does not fire", k2 == L.UNCHANGED,
            "path %s is in neither the diff nor the added set.\n"
            "classifier says %s." % (same, k2))

    # ---- D1: an instrument that sweeps ITSELF measures itself -------------
    # Not hypothetical.  The first run of s2 swept its own directory and the
    # synthetic citations in this file and in the selftest (`docs/a.md`, a
    # planted href, a `%s` inside a format string) produced 10 rows -- so a
    # sweep whose subject is "does this repository point readers at withdrawn
    # text" reported ten broken references THAT IT HAD WRITTEN ITSELF.  The
    # arm runs both populations and requires them to differ.
    import s2_sweep as S2
    root = L.program_root()
    own = []
    for dirpath, _dn, fns in os.walk(os.path.join(root, "code",
                                                  "mirror_staleness_cdd5")):
        for fn in fns:
            if fn.lower().endswith((".md", ".py", ".sh", ".txt")):
                own.append(os.path.relpath(os.path.join(dirpath, fn), root))
    own_cits, _ = S2.gather(root, sorted(own))
    arm("D1 this instrument's own directory would contaminate the sweep",
        len(own_cits) > 0,
        "sweeping only this instrument's own %d files yields %d citations,\n"
        "every one of them synthetic.  s2 EXCLUDES this directory and prints\n"
        "the excluded count; the arm fails if that exclusion ever stops\n"
        "mattering, because then it has silently become decorative."
        % (len(own), len(own_cits)))

    # ---- D2: the en-dash range must parse ---------------------------------
    # Also not hypothetical: `step8.tex:389–394` is the corpus's own spelling
    # and a `:(\d+)$` reader left the range in the path, where it resolved at
    # neither revision -- three false BROKEN-CITATION rows on the first run.
    rng = "one_third_width_three/step8.tex:389–394"
    p_rng, l_rng = L._normalise(rng)
    old_style = (rng[rng.find("one_third_width_three/")
                     + len("one_third_width_three/"):])
    k_rng = L.classify(L.blob_at(mirror, MIRROR_PIN, p_rng),
                       L.blob_at(mirror, "origin/main", p_rng), p_rng)
    k_bad = L.classify(L.blob_at(mirror, MIRROR_PIN, old_style),
                       L.blob_at(mirror, "origin/main", old_style), old_style)
    arm("D2 an EN-DASH line range resolves, and the naive reader is shown wrong",
        p_rng == "step8.tex" and l_rng == 389 and k_rng != L.ABSENT_BOTH
        and k_bad == L.ABSENT_BOTH,
        "corpus spelling: %s\n"
        "naive `:(\\d+)$` reader keeps the path as %r -> %s, i.e. it reports a\n"
        "BROKEN CITATION where there is none -- a parser defect that sounds\n"
        "worse than the real finding.\n"
        "this parser gives path=%r line=%s -> %s."
        % (rng, old_style, k_bad, p_rng, l_rng, k_rng))

    # ---- PRE-REPAIR-ANCHORS: the finding the repair made invisible --------
    # s4 now reports STATE.md:112's two anchors as TIP-AUTHORED, because this
    # ticket repaired them.  The FINDING was that they were PIN-AUTHORED --
    # written against the stale tree, which is the evidence that authors here
    # read the mirror checkout.  A repair that erases its own evidence leaves
    # nothing for the next reader to check, so the pre-repair STATE.md is
    # replayed OUT OF GIT and the verdict re-derived on it.
    import s4_anchors as S4  # noqa: E402  (arm-local by design)

    class _Cit(object):
        def __init__(self, src, srcline, path, line):
            self.src, self.srcline, self.path, self.line = src, srcline, path, line

    pre = L.git(["show", "%s:STATE.md" % PRE_REPAIR_REV], cwd=L.program_root())
    pre_lines = pre.split("\n")
    rows, verdicts = [], []
    for path, anchor in ((CHEEGER, 310),
                         ("docs/OneThird-Spectral-NearOrdinalSum-KillShot-Probe.md",
                          286)):
        # find the citing line in the PRE-REPAIR file, by the anchor as written
        needle = "%s:%d" % (os.path.basename(path), anchor)
        srcline = next((n for n, ln in enumerate(pre_lines, 1)
                        if needle in ln), None)
        if srcline is None:
            verdicts.append(None)
            rows.append("%s:%d NOT FOUND in STATE.md@%s"
                        % (path, anchor, PRE_REPAIR_REV))
            continue
        lo = S4.line_at(L.blob_at(mirror, MIRROR_PIN, path), anchor)
        ln_ = S4.line_at(L.blob_at(mirror, "origin/main", path), anchor)
        v = S4.decide_by_quote_text(pre_lines[srcline - 1], lo, ln_)
        verdicts.append(v)
        rows.append("STATE.md@%s:%d -> %s:%d  verdict=%s"
                    % (PRE_REPAIR_REV, srcline, os.path.basename(path),
                       anchor, v))
    arm("PRE-REPAIR-ANCHORS the erased finding is replayed out of git",
        verdicts == ["pin", "pin"],
        "replayed STATE.md at %s (the commit before this ticket's anchor\n"
        "repair) and re-ran s4's quote decision on it:\n  %s\n"
        "both come back PIN-AUTHORED, which is the finding.  Today's STATE.md\n"
        "gives TIP-AUTHORED for the same two rows -- that is the repair, not a\n"
        "retraction, and this arm is what makes the difference checkable."
        % (PRE_REPAIR_REV, "\n  ".join(rows)))

    # ---- E2: the pin is printed, so this transcript is checkable ----------
    st = L.read_state(mirror, do_ls_remote=False)
    arm("E2 this instrument names the revision every figure is measured at",
        st.origin_main is not None,
        "one_third_width_three origin/main = %s at run time.\n"
        "if that ref moves, this transcript is stale -- which is the defect it\n"
        "is about.  The remedy is re-running, and the pin is what makes the\n"
        "staleness visible instead of invisible." % L.short(st.origin_main))

    # ---- E7: a zero must carry its population, and the two kinds of zero
    #      must be distinguishable.  "swept a document and it cites nothing"
    #      and "could not open the document" produce the SAME tally (empty),
    #      and only one of them is a measured zero.  Run both through the
    #      real gather() and require different answers.
    import s2_sweep as S2
    root = L.program_root()
    swept_empty, missing_empty = S2.gather(root, ["README.md"])
    swept_ghost, missing_ghost = S2.gather(root, ["NO-SUCH-DOCUMENT-cdd5.md"])
    same_tally = (len(swept_empty) == 0 and len(swept_ghost) == 0)
    distinguishable = (len(missing_empty) == 0 and len(missing_ghost) == 1)
    arm("E7 the two kinds of zero are distinguishable in the real gatherer",
        same_tally and distinguishable,
        "README.md is real and cites the mirror 0 times: swept=%d missing=%d.\n"
        "NO-SUCH-DOCUMENT-cdd5.md does not exist:        swept=%d missing=%d.\n"
        "both give an EMPTY TALLY (%s), and only the `missing` channel tells\n"
        "them apart -- s2 prints it as `!! source not found` and calls the\n"
        "tier INCOMPLETE rather than reporting a clean zero."
        % (len(swept_empty), len(missing_empty), len(swept_ghost),
           len(missing_ghost), same_tally))

    bad = [n for n, ok, _ in RESULTS if not ok]
    print("  %d arms, %d satisfactory, %d unsatisfactory"
          % (len(RESULTS), len(RESULTS) - len(bad), len(bad)))
    for n in bad:
        print("    UNSATISFACTORY: %s" % n)
    print("== s3 exit: %d ==" % (1 if bad else 0))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
