"""t4_preserve.py -- DO NOT DISTURB, plus the one thing sharper than the
repair stated it.

The brief lists what must survive this repair:

  * all four anchors resolve to the pairs their prose names, WITH THE SUBJECT
    of each commit printed beside the sha -- because `4755d029 agrees with
    4755d029` is true of any derivation that has drifted onto its own pin;
  * the confirmation as a DIFFERENCE, 3bc2cf76 -> 0/0/0 against HEAD -> 1/1/3,
    with the drifted pair both printing 1/1/3 -- one predicate asked twice;
  * g1 at d01ff32d BYTE-IDENTICAL to g1 at HEAD, which a distinctness check
    on shas cannot see;
  * the division: REFUSES on property-moving edits, REPORTS on cosmetic ones.

  (i)   THE FOUR ANCHORS, RE-DERIVED HERE, with subjects.
  (ii)  CONTENT IDENTITY WHERE SHA DISTINCTNESS SAYS NOTHING.
  (iii) THE KERNEL-HALF TRIPLES, READ and LABELLED READ.
  (iv)  REFUSES OR REPORTS, CONSTRUCTED.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.  This script asserts that this
repair disturbed nothing; if it is not 0 something was disturbed.
"""

import os
import subprocess
import sys

import lib_b2af as L

R = L.Report(
    selfpop="every git read, clone, parse and foreign-script run this "
            "script performs, plus the requirement that each constructed "
            "edit really change the file it names",
    findpop="the 4 anchors libe34a derives, each re-derived here and "
            "compared with the pin read from libe34a's source; the blob "
            "identity of g1_provenance.py at the two revisions the drifted "
            "anchor picks; the 4 kernel-half triples; and the 2 edits the "
            "refuse/report division is stated over")

L.banner("T4", "DO NOT DISTURB -- AND THE SHARPER FORM OF THE SAME LESSON")

# ---------------------------------------------------------------------------
L.rule("(i) THE FOUR ANCHORS, RE-DERIVED -- WITH SUBJECTS")
# ---------------------------------------------------------------------------
print("""   Re-derived HERE, with this file's own `first_introducing`, and
   compared against the pins READ OUT OF libe34a.py's source rather
   than by importing it.  An instrument that checks a derivation by
   calling that derivation has checked nothing.

   AND THE SUBJECT IS PRINTED BESIDE EACH SHA.  `4755d029 agrees with
   4755d029` is true of any derivation that has drifted onto its own
   pin; the subject is what makes the row readable as a claim about a
   particular commit.
""")

libsrc = os.path.join(L.REPO, L.E34A_LIB)
consts = L.module_constants(libsrc)
for name in ("REPAIR_REV_PIN", "PRE_REV_PIN", "REV_7E58_PIN", "PRE_7E58_PIN",
             "MARK_76CC", "MARK_7E58", "G1_REL"):
    R.check(name in consts,
            "%s could not be read out of %s's source" % (name, L.E34A_LIB))

G1 = consts.get("G1_REL", "code/branching_audit_58da/g1_provenance.py")

ANCHORS = [
    ("mg-76cc repair, derived from %r" % consts.get("MARK_76CC"),
     consts.get("MARK_76CC"), consts.get("REPAIR_REV_PIN"), False),
    ("  its first parent -- THE PRE-REPAIR PREDICATE",
     consts.get("MARK_76CC"), consts.get("PRE_REV_PIN"), True),
    ("mg-7e58 repair, derived from %r" % consts.get("MARK_7E58"),
     consts.get("MARK_7E58"), consts.get("REV_7E58_PIN"), False),
    ("  its first parent",
     consts.get("MARK_7E58"), consts.get("PRE_7E58_PIN"), True),
]

disagree = []
for label, marker, pin, parent in ANCHORS:
    got = L.first_introducing(G1, marker)
    if got and parent:
        got = L.resolve(got + "^")
    ok = got == pin
    if not ok:
        disagree.append((label, got, pin))
    print("   %-46s %s  %s" % (label, (got or "NONE")[:8],
                               "agrees" if ok else "*** DISAGREES"))
    print("   %-46s %-8s  %s" % ("", "", L.subject(got)[:60] if got else ""))

R.gate(not disagree,
       "%d of the 4 anchors no longer resolve to the pin libe34a carries: %s"
       % (len(disagree), "; ".join("%s got %s want %s"
                                   % (l, (g or "NONE")[:8], p[:8])
                                   for l, g, p in disagree)))

# ---------------------------------------------------------------------------
L.rule("(ii) CONTENT IDENTITY, WHERE SHA DISTINCTNESS SAYS NOTHING")
# ---------------------------------------------------------------------------
print("""   mg-330a's sharpest observation: the drifted column labelled `the
   repair` resolved to d01ff32d, and g1_provenance.py THERE is
   byte-identical to g1_provenance.py at HEAD.  The two drifted
   sources differ by sha, which is precisely why nothing complained.

   Both checks are run on the same pair, and both answers printed --
   because the point is that they disagree.
""")

D01 = "d01ff32dd4dce31b98cb8aca9f4ae6e3a8aaebc3"
HEAD = L.resolve("HEAD")
sha_a, sha_b = L.resolve(D01), HEAD
blob_a, blob_b = L.blob_sha(D01, G1), L.blob_sha(HEAD, G1)

print("   the pair : %s and %s (HEAD)" % (D01[:8], HEAD[:8]))
print()
print("   a distinctness check on the COMMIT SHAS")
print("      %s vs %s : %s" % (sha_a[:8], sha_b[:8],
                               "distinct -- PASSES" if sha_a != sha_b
                               else "identical -- fails"))
print("   a distinctness check on WHAT THEY RESOLVE TO (the blob of %s)" % G1)
print("      %s vs %s : %s"
      % ((blob_a or "NONE")[:8], (blob_b or "NONE")[:8],
         "IDENTICAL -- FAILS" if blob_a == blob_b else "distinct -- passes"))
print()
print("   The two checks disagree on the same pair.  Where two anchors")
print("   must differ, compare what they RESOLVE TO, not what they are")
print("   called.")

R.check(sha_a != sha_b,
        "the two revisions in this demonstration are the same commit, so "
        "there is no pair here and (ii) demonstrates nothing")
R.check(blob_a is not None and blob_b is not None,
        "%s does not exist at one of the two revisions, so the content "
        "comparison could not be made" % G1)
R.gate(blob_a == blob_b,
       "the sharpened lesson no longer reproduces: %s at %s and at HEAD are "
       "no longer byte-identical (%s vs %s).  The observation mg-330a made "
       "was true of the tree it measured; this repair records that it has "
       "since stopped being true rather than repeating it"
       % (G1, D01[:8], (blob_a or "NONE")[:8], (blob_b or "NONE")[:8]))

# ---------------------------------------------------------------------------
L.rule("(iii) THE KERNEL-HALF TRIPLES -- READ, AND LABELLED READ")
# ---------------------------------------------------------------------------
print("""   These four triples are READ out of mg-330a's committed transcript
   and are LABELLED READ.  They are not re-derived here.

   The reason is stated rather than left as an omission: re-deriving
   them costs about ten minutes of k1_prerepair.py, mg-330a already
   re-derived them from scratch with each pinned g1 travelling with its
   own lib58da, and a second re-derivation buys nothing this ticket
   needs.  SAYING `READ` is the point.  A number whose provenance is
   not stated is the defect this whole arc is about.
""")

S3 = "code/audit_330a/out_s3_kernel_half.txt"
with open(os.path.join(L.REPO, S3)) as fh:
    s3 = fh.read().splitlines()

WANT = [
    ("BEFORE THE REPAIR (property)", "3bc2cf76", "0      0      0"),
    ("THIS REPAIR (HEAD)", "HEAD", "1      1      3"),
    ("before the repair (DRIFTED)", "e5787e11", "1      1      3"),
    ("the repair (DRIFTED)", "d01ff32d", "1      1      3"),
]
print("   %-34s %-10s %-16s %s"
      % ("column", "revision", "exit/self/find", "provenance"))
missing = []
for label, rev, triple in WANT:
    hit = [ln for ln in s3 if ln.strip().startswith(label)]
    present = bool(hit) and rev in hit[0] and triple in hit[0]
    if not present:
        missing.append(label)
    print("   %-34s %-10s %-16s %s"
          % (label, rev, triple.replace("      ", "/"),
             "READ from %s" % S3 if present else "*** NOT FOUND THERE"))
R.check(not missing,
        "%d of the 4 triples are not in %s as this script quotes them: %s.  "
        "The figures above are attributed to a transcript that does not "
        "carry them" % (len(missing), S3, ", ".join(missing)))

print()
print("   THE CONFIRMATION IS A DIFFERENCE : 0/0/0 at 3bc2cf76 against")
print("   1/1/3 at HEAD.  THE DRIFTED PAIR BOTH PRINT 1/1/3 -- one")
print("   predicate asked twice, which is why its `0` was a plausible")
print("   number produced by asking one predicate the same question.")

# ---------------------------------------------------------------------------
L.rule("(iv) REFUSES, OR REPORTS?  CONSTRUCTED, NOT RESTATED")
# ---------------------------------------------------------------------------
print("""   The division mg-330a measured: a PROPERTY-MOVING edit makes the
   instrument REFUSE, a COSMETIC edit makes it REPORT.  That division
   is the reason the instrument can be run on a live tree at all -- one
   that refused on every comment could not be.

   Constructed here in two clones, with THIS repair's edits carried in,
   so the answer is about the tree as this ticket leaves it.
""")


def with_repair(root):
    for rel in (L.E34A_LIB, L.E34A_DIR + "/k4_cancel.py",
                L.E34A_DIR + "/k2_five.py"):
        with open(os.path.join(L.REPO, rel)) as fh:
            src = fh.read()
        with open(os.path.join(root, rel), "w") as fh:
            fh.write(src)


def selftest_in(root):
    p = subprocess.run([sys.executable, "selftest_e34a.py"],
                       cwd=os.path.join(root, L.E34A_DIR),
                       capture_output=True, text=True)
    tail = [ln for ln in p.stdout.splitlines() if "assertions" in ln]
    return p.returncode, (tail[-1].strip() if tail else "(no trailer)")


base = L.clone_at("HEAD")
with_repair(base)
rc_base, tr_base = selftest_in(base)
print("   %-34s exit %d   %s" % ("the tree, unperturbed", rc_base, tr_base))
R.check(rc_base == 0,
        "mg-e34a's selftest is already red on an unperturbed clone carrying "
        "this repair's edits (%s); every row below compares against a broken "
        "baseline" % tr_base)

cosmetic = L.clone_at("HEAD")
with_repair(cosmetic)
L.cosmetic_commit(cosmetic, G1)
rc_cos, tr_cos = selftest_in(cosmetic)
print("   %-34s exit %d   %s" % ("a COSMETIC edit to g1", rc_cos, tr_cos))

moving = L.clone_at("HEAD")
with_repair(moving)
gp = os.path.join(moving, G1)
with open(gp) as fh:
    src = fh.read()
mark = consts.get("MARK_76CC")
R.check(mark in src, "the marker %r is not in %s, so the property-moving "
                     "edit had nothing to remove" % (mark, G1))
with open(gp, "w") as fh:
    fh.write(src.replace(mark, "kernel_source_REMOVED_BY_T4="))
subprocess.run(["git", "-C", moving, "add", G1], check=True,
               capture_output=True, text=True)
subprocess.run(["git", "-C", moving, "-c", "user.email=b2af@probe",
                "-c", "user.name=mg-b2af probe", "commit", "--quiet",
                "-m", "probe: remove the property marker"],
               check=True, capture_output=True, text=True)
rc_mov, tr_mov = selftest_in(moving)
print("   %-34s exit %d   %s" % ("a PROPERTY-MOVING edit", rc_mov, tr_mov))

print()
print("   the cosmetic edit  => %s"
      % ("REPORTS -- the change is on the page and the anchor ignores it"
         if rc_cos == 0 else "*** REFUSES"))
print("   the property edit  => %s"
      % ("REFUSES" if rc_mov != 0 else "*** does not refuse"))
print()
print("   NON-VACUITY -- the two edits produced different answers : %s"
      % (rc_cos != rc_mov))

R.check(rc_cos != rc_mov,
        "the cosmetic edit and the property-moving edit produce the same "
        "answer, so this construction does not distinguish the two halves "
        "of the division it is testing")
R.gate(rc_cos == 0,
       "a COSMETIC edit to %s now makes mg-e34a's selftest red (%s).  The "
       "division has collapsed to `refuses on everything`, and an instrument "
       "that refuses on every comment cannot be run on a live tree"
       % (G1, tr_cos))
R.gate(rc_mov != 0,
       "a PROPERTY-MOVING edit to %s leaves mg-e34a's selftest green (%s).  "
       "The anchor is FOLLOWING the edit, which is A-1" % (G1, tr_mov))

# ---------------------------------------------------------------------------
L.rule("PREDICTIONS SCORED")
# ---------------------------------------------------------------------------
L.score(R, "P-7a", 0, len(disagree), note="4 of 4 agree, subjects printed")
L.score(R, "P-7b", True, blob_a == blob_b, note="byte-identical")
L.score(R, "P-7c", (True, True), (sha_a != sha_b, blob_a == blob_b),
        note="sha check passes, content check fails")
L.score(R, "P-7d", 0, len(missing), note="4 triples READ and labelled READ")
L.score(R, "P-7e", (0, True), (rc_cos, rc_mov != 0),
        note="cosmetic REPORTS, property REFUSES")

L.rule("VERDICT")
print("""   NOTHING WAS DISTURBED.  The four anchors resolve where they did,
   with subjects beside them; the byte identity mg-330a found still
   holds and is re-derived here by blob sha rather than quoted; the
   two kinds of edit still produce the two different answers that make
   the instrument usable.

   AND THE SHARPENED LESSON IS KEPT AS A RUNNING CHECK rather than a
   sentence: (ii) runs both a sha distinctness check and a content
   distinctness check on the same pair every time this script runs, and
   prints that they disagree.
""")

sys.exit(R.emit())
