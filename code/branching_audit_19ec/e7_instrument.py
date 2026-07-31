"""E7 -- THE THING NO LIST IN THE BRIEF NAMES, CHOSEN BY ME.

mg-19ec's brief names the four sentences, the population question, and the
things not to disturb, and then says: audit at least one thing no list here
names, and say what you chose.

I CHOSE THE INSTRUMENT'S OWN EXIT CONTRACT AND ITS OWN SELF-TEST, because F3 --
one of the four findings this repair landed -- is precisely "a control that
could not fire on the thing it appeared to certify", and the natural place for
that defect to recur is in the probes written to repair it.

E7a  MG-DFFA'S RUNNER IS GREEN IN AN ENVIRONMENT WITH NO NETWORK, WITH F4'S
     PREMISE UNREAD.  `w3_brown.py` carries the whole of F4: the premise the
     document's strongest sentence stands on is discharged by downloading
     Brown (2000) and locating section 4.3.  On download failure it prints a
     line and `return 0`.  `run_all.sh` uses `set -e` with `||` guards keyed on
     exit status, and its final `grep ... || true` cannot fail.  So on a
     machine with no network the runner exits 0, every status line reads
     green, and nothing verified premise (a).
     BUILT, not argued: the probe and the runner are both executed here with
     `urllib.request.urlopen` forced to raise.

E7b  THE 42-ASSERTION SELF-TEST, MUTATION-TESTED.  A self-test is worth what it
     refuses.  Four mutations are made to a COPY of `kerndffa.py` and
     `selftestdffa.py` is required to FAIL on each.  Nothing in the real tree
     is touched.

E7c  DISJOINTNESS AT THE GRAIN OF THE FIGURE, NOT THE DIRECTORY.  The README
     says the instrument imports nothing from the four earlier ones and reads
     their committed outputs where it cites them.  That is true.  The finer
     question is which probe reads which foreign file, so a reader can tell
     which figures are re-derived and which are located.  Enumerated.

E7d  AND THE SAME QUESTION TURNED ON MYSELF.  This audit's own exit contract,
     stated: my `e3_f4_brown.py` exits 2 -- not 0 -- when it cannot reach
     arXiv, and my `run_all.sh` is green only when every probe's exit code
     equals the one committed in PREDICTIONS.md before any of them ran.

EXIT 1 if E7a reproduces (it is a finding) or if any mutation survives.
PREDICTED 1.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

OUT = sys.stdout
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.join(HERE, "..")
DFFA = os.path.join(CODE, "branching_warrant_dffa")
BAD = [0]

SHIM = """import urllib.request


def _refuse(*a, **k):
    raise OSError("network disabled by mg-19ec's E7a shim")


urllib.request.urlopen = _refuse
"""


def ck(label, ok, detail=""):
    if not ok:
        BAD[0] += 1
    print("  %-58s %s%s" % (label, "ok" if ok else "BAD", detail), file=OUT)
    return ok


def note(label, value):
    print("  %-58s %s" % (label, value), file=OUT)


def head(t):
    print("=" * 78, file=OUT)
    for line in t.split("\n"):
        print(line, file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)


ROOT = os.path.join(CODE, "..")
SIBLINGS = ["branching_af28", "branching_audit_6ad0", "branching_audit_5800",
            "branching_repair_41aa"]


def copy_dffa():
    """A COMPLETE mini-tree: the instrument plus every sibling directory and
    document its probes read, placed INSIDE the repository so that w4's
    `git show` of the pre-repair check_doc.py still resolves.

    The first version of this probe copied only branching_warrant_dffa, and
    W1 then failed for want of out_a1_contact.txt rather than for want of the
    network -- a red runner that proved nothing.  Recorded rather than
    quietly corrected: an isolation bug in a probe about isolation."""
    tmp = tempfile.mkdtemp(prefix=".e7_19ec_", dir=ROOT)
    dst = os.path.join(tmp, "code", "branching_warrant_dffa")
    shutil.copytree(DFFA, dst)
    for d in SIBLINGS:
        shutil.copytree(os.path.join(CODE, d), os.path.join(tmp, "code", d))
    os.makedirs(os.path.join(tmp, "docs"))
    for f in os.listdir(os.path.join(ROOT, "docs")):
        if f.endswith(".md"):
            shutil.copy(os.path.join(ROOT, "docs", f),
                        os.path.join(tmp, "docs", f))
    shim = os.path.join(tmp, "shim")
    os.makedirs(shim)
    with open(os.path.join(shim, "sitecustomize.py"), "w") as f:
        f.write(SHIM)
    return tmp, dst, shim


def e7a():
    head("E7a  mg-dffa's runner with the network removed.  BUILT, not argued.")
    tmp, dst, shim = copy_dffa()
    try:
        env = dict(os.environ, PYTHONPATH=shim)
        p = subprocess.run([sys.executable, "w3_brown.py"], cwd=dst, env=env,
                           capture_output=True, text=True)
        ck("the shim really disabled the download",
           "DOWNLOAD FAILED" in p.stdout, " (%r)"
           % p.stdout.strip().split("\n")[-1][:60])
        note("w3_brown.py exit code with no network", p.returncode)
        fired = p.returncode != 0
        ck("w3_brown.py exits NON-ZERO when it verified nothing", fired,
           "  <-- it exits 0" if not fired else "")
        ck("  ... and it prints no SUMMARY line either",
           "SUMMARY w3_brown" not in p.stdout,
           " (so a downstream grep finds nothing to read)")
        r = subprocess.run(["/bin/sh", "run_all.sh"], cwd=dst, env=env,
                           capture_output=True, text=True)
        note("run_all.sh exit code with no network", r.returncode)
        green = r.returncode == 0
        ck("run_all.sh REFUSES to be green with F4's premise unread",
           not green, "  <-- it exits 0 and prints 'done.'" if green else "")
        print(file=OUT)
        print("  the runner's own headline block, with no network:", file=OUT)
        for line in r.stdout.strip().split("\n")[-9:]:
            print("      %s" % line[:100], file=OUT)
        print(file=OUT)
        print("  FINDING E7a.  F4 is the finding whose whole content is that a", file=OUT)
        print("  live claim was resting somewhere it could not rest.  Its", file=OUT)
        print("  repair rests on one probe, and that probe reports success", file=OUT)
        print("  when it has checked nothing.  This is DECLARED -- the", file=OUT)
        print("  docstring says it, run_all.sh says it, and the account", file=OUT)
        print("  document's section 7 says it -- so it is a warrant defect and", file=OUT)
        print("  not a hidden one, and it is the same shape as the F3 this", file=OUT)
        print("  same commit repaired: a control that cannot fire, with the", file=OUT)
        print("  status line staying green over it.", file=OUT)
        print(file=OUT)
        print("  WHAT FALLS INSIDE IT, ENUMERATED.  With no network the", file=OUT)
        print("  following are unverified while the runner is green:", file=OUT)
        for s in ["the section 4.3 heading is 'Distributive lattices'",
                  "the section 4.4 heading is 'The kids walk' and follows it",
                  "Brown's example sentence lies strictly between them",
                  "section 4.3 contains exactly one occurrence of 'example'",
                  "the maximal chains are the lattice paths",
                  "Brown counts the chains at (p+1)(q+1) - 2"]:
            print("      - %s" % s, file=OUT)
        print(file=OUT)
        print("  NOT A DEFECT IN THE DOCUMENT'S SENTENCE.  The committed", file=OUT)
        print("  out_w3_brown.txt records a run that DID reach arXiv, and E3", file=OUT)
        print("  of this audit re-reads the paper and pins it by digest.  The", file=OUT)
        print("  defect is in the exit contract, not in the reading.", file=OUT)
        print(file=OUT)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


MUTATIONS = [
    ("M1  canon not minimised over relabellings",
     "        t = tuple(new)\n        if best is None or t < best:\n"
     "            best = t\n    return best",
     "        t = tuple(new)\n        if best is None or t < best:\n"
     "            best = t\n    return tuple(up)"),
    ("M2  yf_up_covers inserts the 1 only at the FRONT of the 2-run",
     "    for i in range(a + 1):\n"
     "        out.add((2,) * i + (1,) + (2,) * (a - i) + t)",
     "    for i in range(1):\n"
     "        out.add((2,) * i + (1,) + (2,) * (a - i) + t)"),
    ("M3  contains() always true",
     "    return all(mu[i] <= lam[i] for i in range(len(mu)))",
     "    return True"),
    ("M4  Lattice.distributive() always true",
     "    def distributive(self):",
     "    def distributive(self):\n        return True\n"),
]


def e7b():
    head("E7b  mg-dffa's 42-assertion self-test, mutation-tested.\n"
         "     A self-test is worth what it REFUSES.")
    base = subprocess.run([sys.executable, "selftestdffa.py"], cwd=DFFA,
                          capture_output=True, text=True)
    ck("unmutated: selftestdffa.py exits 0", base.returncode == 0,
       " (exit %d)" % base.returncode)
    m = re.search(r"(\d+) assertions?, (\d+) failed", base.stdout)
    note("  it reports", m.group() if m else "(no summary line)")
    for label, old, new in MUTATIONS:
        tmp, dst, _ = copy_dffa()
        try:
            path = os.path.join(dst, "kerndffa.py")
            s = open(path, encoding="utf-8").read()
            if old not in s:
                ck("%s: mutation site located" % label, False)
                continue
            open(path, "w", encoding="utf-8").write(s.replace(old, new, 1))
            p = subprocess.run([sys.executable, "selftestdffa.py"], cwd=dst,
                               capture_output=True, text=True)
            mm = re.search(r"(\d+) assertions?, (\d+) failed", p.stdout)
            ck("%s: self-test FAILS" % label, p.returncode != 0,
               " (exit %d%s)" % (p.returncode,
                                 "; " + mm.group() if mm else ""))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    print(file=OUT)


def e7c():
    head("E7c  disjointness at the grain of the FIGURE, not the directory.")
    foreign = re.compile(r'"(branching_af28|branching_audit_6ad0|'
                         r'branching_audit_5800|branching_repair_41aa)",\s*'
                         r'"([a-z0-9_.]+)"')
    rows = []
    for fn in sorted(os.listdir(DFFA)):
        if not fn.endswith(".py"):
            continue
        s = open(os.path.join(DFFA, fn), encoding="utf-8").read()
        for d, f in foreign.findall(s):
            rows.append((fn, d, f))
    print("     probe            foreign directory          file read", file=OUT)
    for fn, d, f in rows:
        print("     %-16s %-26s %s" % (fn, d, f), file=OUT)
    if not rows:
        print("     (none)", file=OUT)
    print(file=OUT)
    readers = sorted({fn for fn, _, _ in rows})
    ck("only w1 (located results) and w4 (the control under test) read"
       " foreign files",
       readers == ["w1_ledger.py", "w4_control.py"], " (%s)" % readers)
    for fn in ["w2_family.py", "w3_brown.py"]:
        s = open(os.path.join(DFFA, fn), encoding="utf-8").read()
        ck("%s reads NO foreign file -- its figures are re-derived" % fn,
           not foreign.search(s))
    print(file=OUT)
    print("  READING E7c.  The two probes carrying F2's and F4's figures read", file=OUT)
    print("  nothing from the four earlier instruments, so those figures are", file=OUT)
    print("  reproductions.  The one probe that reads foreign files for", file=OUT)
    print("  EVIDENCE is w1, and its cell says LOCATED rather than MEASURED.", file=OUT)
    print("  The claim holds at a finer grain than the README states it at.", file=OUT)
    print(file=OUT)


def e7d():
    head("E7d  the same question turned on this audit.")
    mine = open(os.path.join(HERE, "e3_f4_brown.py"), encoding="utf-8").read()
    ck("mg-19ec's own network probe returns 2, not 0, when it cannot read",
       "return 2" in mine and "DOWNLOAD FAILED" in mine)
    runner = os.path.join(HERE, "run_all.sh")
    if os.path.exists(runner):
        r = open(runner, encoding="utf-8").read()
        ck("mg-19ec's runner compares each exit code with a COMMITTED"
           " prediction", "PREDICTIONS.md" in r or "PREDICTED" in r)
    else:
        ck("mg-19ec's runner exists", False)
    print(file=OUT)


def main():
    head("E7  mg-19ec: the thing no list in the brief names.")
    e7a()
    e7b()
    e7c()
    e7d()
    print("=" * 78, file=OUT)
    print("SUMMARY e7_instrument: findings %d" % BAD[0], file=OUT)
    print("=" * 78, file=OUT)
    return 1 if BAD[0] else 0


if __name__ == "__main__":
    sys.exit(main())
