#!/usr/bin/env python3
"""a3 — THE DIRECTORIES WITH `NO EVIDENCE OF ANY FALSIFICATION ATTEMPT`, ADJUDICATED.

WHAT THE INDEX ACTUALLY MEASURED.  mg-9876's §3 is explicit that the ticket's fourth smell —
"positive controls never demonstrated to fail" — is not decidable from source, and that what
it counted instead was two proxies:

    a source file whose BASENAME matches (negative|selftest|self_test|positive|control|falsif)
    a .txt/.md carrying one of (HOLE|CAUGHT|MISMATCH|REFUTED|FAILED TO|SETUP FAILED|NEGATIVE CONTROL)

A directory with neither is in the bucket.  c9876 said so in its own docstring and called the
bucket "weaker than saying it cannot [fail]".  ADJUDICATING IT MEANS ASKING WHAT THE PROXIES
MISS, and the first thing they miss is a directory that mutates its own subject inside a file
called `mutations16eb.py` and prints `MUTATIONS ... CAUGHT` in a transcript — a real, running,
two-way falsification, invisible to both proxies because the basename does not match the first
regex and the transcript vocabulary does not match the second.

SO THE ADJUDICATION IS TWO MEASURED QUESTIONS PER DIRECTORY, NOT ONE.

  Q1  IS THERE AN ATTEMPT, BY ANY ROUTE?  A widened detector, which is a REPLACEMENT for
      c9876's §3 proxies and says so: it looks for the CONSTRUCTION (source that perturbs its
      own subject) and for the OUTCOME (a transcript recording what the perturbation did),
      rather than for a filename.  Where it disagrees with c9876's proxy the disagreement is
      printed with the site that caused it, so the reader can check the call.

  Q2  IS THERE A CHECK TO FALSIFY AT ALL?  A directory that derives a number and prints it
      has no arm that can say NO, and "no falsification attempt" is not a hole in it — it is
      a description of what it is.  Confusing the two is how a bounded population turns into
      a defect count.  Mechanically: an assert, a non-zero exit, or a printed verdict token.

  VERDICTS.  ATTEMPT-FOUND (the index's proxy missed it) · NO-CONTROL-TO-FALSIFY (nothing to
  attempt) · HOLE (ships a check that can say NO, and nothing in the tree has ever tried to
  make it) — the last is the only one that is a finding, and each one is named.

§3 IS THE CONTROL, AND ITS FOURTH WORLD IS THE POINT.  Four planted directories, one per
answer, plus a directory whose entire falsification apparatus is an EMPTY FILE NAMED
`selftest.py`: c9876's proxy calls that covered, this arm calls it a hole.  That is the
weakness of a filename test DEMONSTRATED rather than asserted, which is the standard the whole
mg-9876 line is holding itself to.
"""

import os
import re
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import liba397 as L  # noqa: E402

# Q1 — the construction: source that makes a known-bad world out of a known-good one.
ATTEMPT_SOURCE = re.compile(
    r"(mutat\w*|planted?\s|plant\(|known[- _]?bad|counterfactual|perturb\w*|corrupt\w*|"
    r"negative[_ ]control|falsif\w*|sabotage|two ways|control world|seed_\w*bad)", re.I)
# Q1 — the outcome: a transcript that records what the perturbation did.  Both halves are
# required, because source that says `mutation` in a comment is not an attempt and a
# transcript saying `CAUGHT` with no construction behind it is a word.
ATTEMPT_OUTCOME = re.compile(
    r"(MUTATION|MUTANT|PLANTED|COUNTERFACTUAL|NEGATIVE CONTROL|KNOWN[- ]BAD|CAUGHT|"
    r"UNFALSIFIABLE|REFUSED|MUTATIONS)", re.I)

# Q2 — an arm that can say NO.
CAN_SAY_NO = [
    (re.compile(r"^\s*assert\b", re.M), "assert"),
    (re.compile(r"sys\.exit\(\s*[1-9]"), "non-zero exit"),
    (re.compile(r"sys\.exit\(\s*(1 if|2 if|int\(|rc\b|code\b|status\b)"), "computed exit"),
    (re.compile(r"""["'](\s*)(FAIL|RED|DEFECT|HOLE|MISMATCH|WRONG|BROKEN|DRIFT|DISAGREE)"""),
     "printed verdict token"),
    (re.compile(r"\braise\s+SystemExit"), "SystemExit"),
]


def scan(dirpath, a4):
    srcs = list(a4.files(dirpath, (".py", ".sh")))
    txts = list(a4.files(dirpath, (".txt", ".md")))
    src_body = "\n".join(L.read(f) for f in srcs)
    txt_body = "\n".join(L.read(f) for f in txts)

    # THE EVIDENCE IS PRINTED IN THE CASE IT WAS FOUND IN, and that is not cosmetic: this
    # arm's outcome regex is case-INSENSITIVE where c9876's RED_TOKENS is case-SENSITIVE, so
    # a transcript saying `caught` is invisible to the proxy and visible here.  My first
    # version upper-cased the matches before printing them, which made §2 read as though
    # c9876's token test had somehow missed the literal string `CAUGHT`.  It had not; the
    # tree had written it in lower case.  Destroying the evidence while reporting on
    # evidence is this ticket's own subject, so the case is kept.
    src_hits = sorted({m.group(0) for m in ATTEMPT_SOURCE.finditer(src_body)})
    out_hits = sorted({m.group(0) for m in ATTEMPT_OUTCOME.finditer(txt_body)})
    no_hits = [label for rx, label in CAN_SAY_NO if rx.search(src_body)]

    # c9876's own two proxies, recomputed here so the disagreement is exhibited and not
    # quoted from another transcript.
    proxy_name = [os.path.basename(f) for f in srcs
                  if a4.NEGATIVE_NAMES.search(os.path.basename(f))]
    proxy_red = [os.path.basename(f) for f in txts if a4.RED_TOKENS.search(L.read(f))]

    return {"srcs": len(srcs), "txts": len(txts),
            "attempt_src": src_hits, "attempt_out": out_hits, "can_say_no": no_hits,
            "proxy_name": proxy_name, "proxy_red": proxy_red}


def verdict(ev):
    # Q2 IS ASKED FIRST, and the order is the finding rather than a detail.  A directory
    # with nothing that can say NO has no control, so it cannot have an unfalsified one —
    # whatever falsification vocabulary its prose carries.  Answering Q1 first would file
    # `unitmap_audit_9f91`, which reports its findings in English at exit 0, as a directory
    # with a working falsification attempt.
    if not ev["can_say_no"]:
        return "NO-CONTROL-TO-FALSIFY"
    if ev["attempt_src"] and ev["attempt_out"]:
        return "ATTEMPT-FOUND"
    return "HOLE"


def planted_world(spec):
    """Build a directory on disk with exactly the requested evidence, and answer it."""
    tmp = tempfile.mkdtemp(prefix="a397_a3_")
    for name, body in spec.items():
        with open(os.path.join(tmp, name), "w", encoding="utf-8") as fh:
            fh.write(body)
    return tmp


def main():
    a4 = L.load_c9876()
    print("=" * 92)
    print("mg-a397 a3 — THE `NO FALSIFICATION ATTEMPT` DIRECTORIES, ADJUDICATED")
    print("=" * 92)
    print()

    bare = L.bare_dirs(a4)
    mine = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
    print(f"population: {len(bare)} directories in the bucket today "
          f"(the ticket was filed on 24)")
    if mine in bare:
        print(f"  … and one of them is MINE ({mine}), which is mg-724a's D1 arriving again:")
        print("    an instrument that gates this class of thing lands inside the population")
        print("    it measures, and is scored by it.  It is kept in the table below.")
    else:
        print(f"  MY OWN DIRECTORY ({mine}) IS NOT IN THE BUCKET, AND W4 BELOW IS WHY.")
        print("    It left by SHIPPING A FILE WHOSE NAME MATCHES c9876's first proxy —")
        print("    `a5_selftest.py`.  The file does contain real planted worlds, so the")
        print("    answer happens to be right; the point is that the PROXY never looked.  W4")
        print("    plants an EMPTY file of that name and shows the proxy calling it covered,")
        print("    and this directory is the same construction arriving for real, in the arm")
        print("    written to measure it.")
    print()

    print("§1  THE TWO QUESTIONS, PER DIRECTORY")
    print("-" * 92)
    print(f"    {'directory':36} {'verdict':22} {'attempt (src/out)':18} can say NO")
    rows = {}
    for d in bare:
        ev = scan(os.path.join(L.CODE, d), a4)
        v = verdict(ev)
        rows[d] = (v, ev)
        att = f"{len(ev['attempt_src'])}/{len(ev['attempt_out'])}"
        print(f"    {d:36} {v:22} {att:18} {', '.join(ev['can_say_no']) or '(nothing)'}")
    print()

    counts = {}
    for d, (v, _e) in rows.items():
        counts[v] = counts.get(v, 0) + 1
    print("    " + "   ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    print()

    print("§2  WHY THE INDEX PUT THEM HERE — THE DISAGREEMENT, WITH THE SITE")
    print("-" * 92)
    print("    Every directory below is in the bucket because BOTH of c9876's proxies said")
    print("    no.  For the ATTEMPT-FOUND ones this arm says yes, so exactly one of the two")
    print("    is wrong about it, and the evidence is printed rather than described.")
    print()
    for d, (v, ev) in sorted(rows.items()):
        if v != "ATTEMPT-FOUND":
            continue
        print(f"    {d}")
        print(f"        construction in source : {', '.join(ev['attempt_src'][:6])}")
        print(f"        outcome in transcript  : {', '.join(ev['attempt_out'][:6])}")
        print(f"        c9876 proxy 1 (a filename matching "
              f"{a4.NEGATIVE_NAMES.pattern}) : none")
        print(f"        c9876 proxy 2 (a transcript token) : none")
    print()

    print("§3  THE ONES THAT ARE NOT INSTRUMENTS")
    print("-" * 92)
    print("    No assert, no non-zero exit, no printed verdict token — nothing in them can")
    print("    say NO, so there is no control to have failed to falsify.  A directory that")
    print("    derives and prints is not a defect for not shipping a negative control.")
    for d, (v, ev) in sorted(rows.items()):
        if v == "NO-CONTROL-TO-FALSIFY":
            print(f"      {d:36}  {ev['srcs']} source file(s), {ev['txts']} transcript(s)")
    print()

    print("§4  THE RESIDUAL — SHIPS A CHECK THAT CAN SAY NO, NOTHING HAS TRIED TO MAKE IT")
    print("-" * 92)
    print("    THIS IS THE ONLY BUCKET THAT IS A FINDING, and it is a finding of ABSENCE:")
    print("    the check may well work.  What is established is that the tree contains no")
    print("    record of anyone having asked it to fail — which is the population where a")
    print("    laundered green would never have been noticed.")
    print()
    for d, (v, ev) in sorted(rows.items()):
        if v != "HOLE":
            continue
        print(f"      {d}")
        print(f"          can say NO via : {', '.join(ev['can_say_no'])}")
        print(f"          attempt evidence: source={ev['attempt_src'] or '(none)'} "
              f"transcript={ev['attempt_out'] or '(none)'}")
    print()

    print("§5  THIS ARM'S OWN CONTROL — FIVE PLANTED DIRECTORIES")
    print("-" * 92)
    print("    A classifier that has only ever been run on the tree it was written from has")
    print("    not been shown to discriminate.  Each world below has exactly one answer.")
    print()
    worlds = [
        ("W1 check + mutation harness + transcript outcome", "ATTEMPT-FOUND", {
            "probe.py": "import sys\nassert 1 == 1\nprint('PASS')\n",
            "d2_mutate.py": "# plant a known-bad world and re-run the probe\n"
                            "def mutate(x): return x + 1\n",
            "out_d2.txt": "MUTATION 1 -> CAUGHT\n"}),
        ("W2 check, no attempt anywhere", "HOLE", {
            "probe.py": "import sys\nassert 1 == 1\nprint('PASS')\n",
            "out_probe.txt": "PASS\n"}),
        ("W3 derivation only, nothing can say NO", "NO-CONTROL-TO-FALSIFY", {
            "derive.py": "print('the number is', 6 * 7)\n",
            "out_derive.txt": "the number is 42\n"}),
        ("W4 an EMPTY file named selftest.py — c9876's proxy 1 says COVERED",
         "HOLE", {
            "probe.py": "import sys\nassert 1 == 1\nprint('PASS')\n",
            "selftest.py": "",
            "out_probe.txt": "PASS\n"}),
        ("W5 the word `mutation` in a comment and nothing else", "HOLE", {
            "probe.py": "# a mutation would be nice one day\n"
                        "import sys\nassert 1 == 1\nprint('PASS')\n",
            "out_probe.txt": "PASS\n"}),
    ]
    ok = True
    for label, want, spec in worlds:
        tmp = planted_world(spec)
        try:
            ev = scan(tmp, a4)
            got = verdict(ev)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        mark = "ok " if got == want else "BROKEN"
        ok = ok and mark == "ok "
        print(f"      {mark}  {label:62} -> {got} (want {want})")
        if label.startswith("W4"):
            print(f"            c9876 proxy 1 on the same world: "
                  f"{ev['proxy_name'] or 'none'}  <- a filename is not an attempt")
    print()
    if not ok:
        print("    THE CONTROL DID NOT ANSWER.  Every verdict above is WITHDRAWN.")
        return 2
    print()

    print("§6  VERDICT")
    print("-" * 92)
    n_att = counts.get("ATTEMPT-FOUND", 0)
    n_noc = counts.get("NO-CONTROL-TO-FALSIFY", 0)
    n_hole = counts.get("HOLE", 0)
    print(f"    ATTEMPT-FOUND           {n_att:3}  the index's two proxies missed a real one")
    print(f"    NO-CONTROL-TO-FALSIFY   {n_noc:3}  nothing in them can say NO")
    print(f"    HOLE                    {n_hole:3}  a check nothing has ever tried to break")
    print(f"                            ---")
    print(f"                            {len(bare):3}")
    print()
    print("    THE BUCKET IS NOT A DEFECT COUNT AND WAS NEVER OFFERED AS ONE.  What this")
    print("    arm establishes is the split, and that the largest part of it is an artefact")
    print("    of two proxies c9876 named as proxies in its own docstring.")
    return 1 if n_hole else 0


if __name__ == "__main__":
    sys.exit(main())
