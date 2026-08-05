"""t3 -- CLASS 1: every recorded SHA in the arc, resolved, and the ones that
are not on `main` chased by PATCH-ID rather than by ancestry.

CLASS 1 is bookkeeping and the ticket says so.  It is measured here anyway,
separately and with its own denominator, because the addendum's central
warning is that merging it with CLASS 2 OVERSTATES the damage and makes the
remedy look bigger than it is.  You cannot report two numbers separately
without measuring them separately.

THE INSTRUMENT.  `git merge-base --is-ancestor <recorded> main` answers "is
this commit ON main".  `git patch-id --stable` answers "did this CONTENT
survive".  After a refinery rebase the first is FALSE and the second finds an
identical twin, which is why the mayor nearly reported mg-f3ff's
pre-registration commit as LOST.  Every verdict below that says a recording is
merely STALE is a patch-id verdict; ancestry is used only to decide which
recordings need chasing at all.

TWO POPULATIONS, kept apart because they support different claims.

  P_A  RESOLVABLE SHA SITES.  A (file, token) site where the token is 7-40 hex
       characters, is not part of a longer word, and RESOLVES to a commit in
       this repository's object store.  Resolution is the membership test, so
       P_A contains no false positives: every member is a real recorded commit.

  P_B  UNRESOLVABLE HEX TOKENS.  The same shape, not resolving.  This
       population is NOT claimed to be dead commits.  It contains hashes of
       other objects, digests, and ordinary hexadecimal numbers, and this
       script does not pretend to be able to tell them apart.  It is reported
       as a bound, named as a bound.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_1abe as L                                          # noqa: E402

# 7-40 hex chars not adjacent to another word character.  The lower bound is
# git's own default abbreviation length; below it, collisions make resolution
# meaningless rather than merely uncertain.
RE_SHA = re.compile(r"(?<![0-9A-Za-z])([0-9a-f]{7,40})(?![0-9A-Za-z])")

TEXT_SUFFIXES = (".md", ".py", ".sh", ".txt")


def scan_files(rev):
    out = L.git("ls-tree", "-r", "--name-only", rev)
    return [p for p in out.split("\n") if p.endswith(TEXT_SUFFIXES)]


def main():
    rev = L.main_rev()
    head = L.resolve(rev)
    led = L.Ledger("t3 -- CLASS 1: every recorded SHA, chased by PATCH-ID")
    print("""
POPULATION   P_A, defined in the module docstring: (file, token) sites whose
             token RESOLVES to a commit.  GRAIN one verdict per site; the
             commit-level counts are stated separately because one commit can
             be recorded at many sites and the two numbers are not the same
             number.
""")
    print("    as-of      %s  (%s)" % (head, rev))

    sites = []
    unresolvable = 0
    seen_tokens = {}
    for path in scan_files(rev):
        blob = L.blob_at(rev, path)
        if blob is None:
            continue
        try:
            text = blob.decode("utf-8")
        except UnicodeDecodeError:
            continue
        for m in RE_SHA.finditer(text):
            tok = m.group(1)
            if tok not in seen_tokens:
                seen_tokens[tok] = L.resolve(tok)
            full = seen_tokens[tok]
            if full is None:
                unresolvable += 1
            else:
                sites.append((path, tok, full))

    print("    P_A        %d resolvable SHA sites over %d distinct commits"
          % (len(sites), len({f for _, _, f in sites})))
    print("    P_B        %d unresolvable hex tokens (a BOUND, not a count of "
          "dead commits)" % unresolvable)

    # ------------------------------------------------------------------ on main
    led.head("T3a -- WHICH RECORDED COMMITS ARE ON `main` AT ALL "
             "(reachability, and reachability only)")
    commits = sorted({f for _, _, f in sites})
    on_main, off_main = [], []
    for c in commits:
        (on_main if L.is_ancestor(c, head) else off_main).append(c)
    print("    %d of %d distinct recorded commits are ancestors of %s"
          % (len(on_main), len(commits), head[:7]))
    print("    %d are NOT.  Ancestry stops here; it cannot tell a rebased "
          "commit from a deleted one." % len(off_main))
    led.record(None,
               "T3a %d of %d distinct recorded commits are not reachable from "
               "%s.  Reported as a REACHABILITY fact and nothing more -- read "
               "as a survival fact it would be a false negative on every one "
               "of them" % (len(off_main), len(commits), head[:7]))

    # -------------------------------------------------------------- patch-id
    led.head("T3b -- AND NOW THE RIGHT QUESTION: DID THE CONTENT SURVIVE?")
    print("""
For every recorded commit that is NOT an ancestor of `main`, its stable
patch-id is compared against the patch-id of every commit on `main`.  An
identical patch-id means the diff survived the rebase byte-for-byte and the
recording is STALE, not WRONG.  No identical patch-id means the content is not
on `main` in that form, and THAT is the verdict worth acting on.
""")
    main_pids = {}
    for c in L.git("rev-list", head).split():
        pid = L.patch_id(c)
        if pid:
            main_pids.setdefault(pid, c)
    print("    indexed %d patch-ids over %d commits reachable from %s"
          % (len(main_pids), len(L.git("rev-list", head).split()), head[:7]))
    print()
    print("    %-10s %-14s %-10s %s" % ("recorded", "verdict", "twin", "subject"))
    stale, orphan = [], []
    for c in off_main:
        pid = L.patch_id(c)
        twin = main_pids.get(pid) if pid else None
        subj = L.git("log", "-1", "--format=%s", c).strip()[:44]
        if twin:
            stale.append((c, twin))
            print("    %-10s %-14s %-10s %s" % (c[:8], "STALE", twin[:8], subj))
        else:
            orphan.append(c)
            print("    %-10s %-14s %-10s %s" % (c[:8], "NO-TWIN", "-", subj))
    if not off_main:
        print("    (no recorded commit is off main)")

    pct = 100.0 * len(stale) / len(off_main) if off_main else 100.0
    led.record(None,
               "T3b of the %d recorded commits that ancestry calls missing, "
               "%d (%.0f%%) have a patch-id-IDENTICAL twin on %s and are "
               "STALE rather than lost; %d have no twin"
               % (len(off_main), len(stale), pct, head[:7], len(orphan)))
    led.record(not orphan,
               "T3b' %d recorded commits have NO patch-id twin on %s.  These "
               "are the only CLASS 1 recordings whose content is not "
               "demonstrably on main, and they are named above"
               % (len(orphan), head[:7]))

    # ------------------------------------------------------------- site count
    led.head("T3c -- THE SITE COUNT, WHICH IS THE ONE THAT SIZES THE CLEANUP")
    off_set = set(off_main)
    stale_set = {c for c, _ in stale}
    site_stale = [(p, t, f) for p, t, f in sites if f in stale_set]
    site_orphan = [(p, t, f) for p, t, f in sites if f in off_set - stale_set]
    print("    %d of %d SITES record a commit that is not on main" %
          (len(site_stale) + len(site_orphan), len(sites)))
    print("      %d record a STALE identifier whose content IS on main" %
          len(site_stale))
    print("      %d record a commit with no twin" % len(site_orphan))
    print()
    print("    every site recording a commit with NO TWIN, named:")
    for p, t, f in site_orphan:
        print("      %-56s %s" % (p[:56], t))
    if not site_orphan:
        print("      (none)")

    led.record(None,
               "T3c CLASS 1 is %d sites of %d.  It is reported apart from "
               "CLASS 2 on purpose: a single number merging a stale identifier "
               "whose content is intact with a transcript that cannot be "
               "reproduced would overstate the damage and make the remedy look "
               "bigger than it is"
               % (len(site_stale) + len(site_orphan), len(sites)))
    return led.done()


if __name__ == "__main__":
    sys.exit(main())
