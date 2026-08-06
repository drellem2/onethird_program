#!/usr/bin/env python3
"""D3 -- MAKE THE DETECTOR FIRE. A verdict dropped ON PURPOSE.

mayor's dispatch note, and it governs this file:

    "Do not ship a detector you have only ever seen stay quiet. A detector for a
     silent failure that has never fired is this arc's signature."

So this section CONSTRUCTS the failure. It builds a throwaway macguffin store,
drives the REAL `mg` binary through new / claim / done -- no mock, no fixture
hand-written to be detected -- and then, on one arm, deliberately does not mail
the verdict.

The matched pair is the whole point. One arm drops the verdict and the detector
must report exactly one. The other arm sends it and the detector must report
exactly zero. A detector that fires on both is an alarm, not a detector.

Then six edge cases, three of which PREDICTIONS.md P6 named in advance as the
ones most likely to break the first form of this code.

Exit 0 if every constructed case lands on its declared expectation, 1 otherwise.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_bf3f as L  # noqa: E402

MG_BIN = shutil.which("mg") or os.path.expanduser("~/go/bin/mg")
FAILS = []


def mg(root, *args, actor=None, stdin=None):
    env = dict(os.environ)
    env["MG_ROOT"] = root
    env.pop("POGO_AGENT_NAME", None)
    if actor:
        env["MG_ACTOR"] = actor
    else:
        env.pop("MG_ACTOR", None)
    p = subprocess.run([MG_BIN, "--root", root] + list(args), env=env,
                       capture_output=True, text=True, input=stdin, timeout=120)
    return p


def new_item(root, filer, title, body):
    p = mg(root, "new", "--title", title, "--body-file", "-", "--no-repo",
           "--type", "task", "--no-declares-remainder", actor=filer, stdin=body)
    if p.returncode != 0:
        raise RuntimeError(f"mg new failed: {p.returncode} {p.stdout} {p.stderr}")
    for tok in (p.stdout + p.stderr).split():
        t = tok.strip(":,.()")
        if t.startswith("mg-") and len(t) >= 6:
            return t
    raise RuntimeError(f"could not read the new item id from: {p.stdout!r} {p.stderr!r}")


def land(root, iid, worker, kind="done"):
    """Take an item to done exactly as the arc does it: claim, then close it,
    then write the refinery-shaped result sidecar naming the worker's branch."""
    p = mg(root, "claim", iid, actor=worker)
    if p.returncode != 0:
        raise RuntimeError(f"mg claim failed: {p.stdout} {p.stderr}")
    p = mg(root, "done", iid, "--result",
           json.dumps({"branch": f"polecat-{worker}", "completed_by": "refinery",
                       "mr": "mr-constructed", "target": "main"}), actor="daniel")
    if p.returncode != 0:
        raise RuntimeError(f"mg done failed: {p.stdout} {p.stderr}")
    if kind == "archived":
        p = mg(root, "archive", iid, actor="daniel")
        if p.returncode != 0:
            raise RuntimeError(f"mg archive failed: {p.stdout} {p.stderr}")


def mail(root, to, frm, subject, body):
    p = mg(root, "mail", "send", to, "--from", frm, "--subject", subject,
           "--body-file", "-", stdin=body)
    if p.returncode != 0:
        raise RuntimeError(f"mg mail send failed: {p.stdout} {p.stderr}")
    # DEFECT-4 of this instrument. The first form read the MSG-ID by scanning
    # `mg mail send`'s output for a dotted token -- but what it prints is
    # `filer-a/new/1786058827378511000.27053.1000`, a PATH, so the scan matched
    # nothing and returned None. The P6b construction below then silently skipped
    # its own setup and asserted DELIVERED against a verdict that had never been
    # archived: a vacuous pass, of exactly the shape this arc keeps finding, in
    # the file whose entire job is to prove the detector is not vacuous.
    # It is read from the documented `--json` contract now, and it RAISES.
    q = mg(root, "mail", "list", to, "--all", "--json")
    if q.returncode != 0:
        raise RuntimeError(f"mg mail list failed: {q.stdout} {q.stderr}")
    for line in q.stdout.splitlines():
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        if rec.get("subject") == subject and rec.get("from") == frm:
            return rec["id"]
    raise RuntimeError(f"could not recover the MSG-ID of the message just sent to {to}")


def check(label, got, want):
    ok = got == want
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}: got {got}, expected {want}")
    if not ok:
        FAILS.append(label)
    return ok


def main():
    if not os.path.exists(MG_BIN):
        print(f"  !! mg binary not found at {MG_BIN} -- cannot construct the failure")
        return 1
    root = tempfile.mkdtemp(prefix="bf3f-fire-")
    print(f"  throwaway store: {root}")
    print(f"  mg binary      : {MG_BIN}")
    try:
        p = mg(root, "init")
        if p.returncode != 0:
            print(f"  !! mg init failed: {p.stdout} {p.stderr}")
            return 1

        print()
        print("=" * 78)
        print("D3.1  THE MATCHED PAIR -- one verdict dropped on purpose, one delivered")
        print("=" * 78)

        a = new_item(root, "filer-a", "arm A: the verdict is dropped on purpose",
                     "This worker will finish the work and never mail the filer.\n")
        land(root, a, "wa1")
        print(f"  arm A  {a}: landed, and I am DELIBERATELY NOT MAILING THE VERDICT.")

        b = new_item(root, "filer-a", "arm B: the verdict is delivered",
                     "This worker mails its verdict before the item lands.\n")
        mail(root, "filer-a", "wb1", f"{b} VERDICT: the control arm",
             f"{b} verdict body -- this is what delivery looks like.\n")
        land(root, b, "wb1")
        print(f"  arm B  {b}: verdict mailed by wb1, then landed.")

        res = L.scan(mg=root, filer="filer-a")
        dropped = [r for r in res["rows"] if r["status"] == "DROPPED"]
        deliv = [r for r in res["rows"] if r["status"] == "DELIVERED"]
        print()
        check("dropped verdicts reported", len(dropped), 1)
        check("the reported drop is arm A", [r["id"] for r in dropped], [a])
        check("delivered verdicts reported", len(deliv), 1)
        check("the delivery is arm B", [r["id"] for r in deliv], [b])
        print()
        print("  THE DETECTOR HAS NOW BEEN SEEN TO FIRE ON A FAILURE CONSTRUCTED ON")
        print("  PURPOSE, AND TO STAY QUIET ON ITS MATCHED CONTROL. It is not a")
        print("  detector that has only ever been observed silent.")

        print()
        print("=" * 78)
        print("D3.2  EDGE CASES -- three of these were named in P6 before this file existed")
        print("=" * 78)

        # (a) P6a -- archived rather than done
        c = new_item(root, "filer-a", "arm C: archived, verdict dropped", "no verdict\n")
        land(root, c, "wc1", kind="archived")
        res = L.scan(mg=root, filer="filer-a")
        row = next((r for r in res["rows"] if r["id"] == c), None)
        check("P6a archived item is reported at all", row is not None, True)
        check("P6a archived item is DROPPED", row and row["status"], "DROPPED")

        # (b) P6b -- verdict archived out of the active mailbox
        d = new_item(root, "filer-a", "arm D: verdict delivered THEN archived", "\n")
        mid = mail(root, "filer-a", "wd1", f"{d} VERDICT: then archived",
                   f"{d} verdict, which the filer then archived.\n")
        land(root, d, "wd1")
        pa = mg(root, "mail", "archive", f"filer-a/{mid}")
        if pa.returncode != 0:
            raise RuntimeError(f"P6b SETUP FAILED, refusing to assert on it: {pa.stdout} {pa.stderr}")
        # The setup is VERIFIED, not reported: the message must be gone from the
        # active mailbox, or the assertion below is vacuous.
        chk = mg(root, "mail", "list", "filer-a", "--all", "--json")
        still_active = any(json.loads(x).get("id") == mid
                           for x in chk.stdout.splitlines() if x.strip())
        check("P6b setup: the verdict really left the active mailbox", still_active, False)
        res = L.scan(mg=root, filer="filer-a")
        row = next((r for r in res["rows"] if r["id"] == d), None)
        check("P6b archived verdict still counts as DELIVERED", row and row["status"], "DELIVERED")

        # (c) P6c -- a filer with no mailbox at all. I predicted this breaks first.
        e = new_item(root, "filer-nobox", "arm E: filer has never received any mail", "\n")
        land(root, e, "we1")
        res = L.scan(mg=root, filer="filer-nobox")
        row = next((r for r in res["rows"] if r["id"] == e), None)
        check("P6c mailbox-less filer's item is reported", row is not None, True)
        check("P6c mailbox-less filer's item is DROPPED", row and row["status"], "DROPPED")
        check("P6c mailbox absence is flagged, not silently treated as empty",
              res["boxes"].get("filer-nobox"), False)

        # (d) a verdict mailed to SOMEBODY ELSE is not delivery to the filer
        f = new_item(root, "filer-a", "arm F: verdict mailed to mayor, not the filer", "\n")
        mail(root, "mayor", "wf1", f"{f} VERDICT sent to the wrong addressee",
             "the filer never sees this\n")
        land(root, f, "wf1")
        res = L.scan(mg=root, filer="filer-a")
        row = next((r for r in res["rows"] if r["id"] == f), None)
        check("arm F (verdict to mayor only) is DROPPED", row and row["status"], "DROPPED")
        check("arm F records that the worker mailed elsewhere",
              (row or {}).get("mails_elsewhere", 0) >= 1, True)

        # (e) an item that has not landed must not be reported at all
        g = new_item(root, "filer-a", "arm G: claimed, still in flight", "\n")
        mg(root, "claim", g, actor="wg1")
        res = L.scan(mg=root, filer="filer-a")
        check("arm G (not landed) is absent from the report",
              any(r["id"] == g for r in res["rows"]), False)

        # (f) a mail from somebody whose name merely CONTAINS the worker's
        h = new_item(root, "filer-a", "arm H: near-miss sender name", "\n")
        mail(root, "filer-a", "wh1x", f"{h} not from the worker", "near miss\n")
        land(root, h, "wh1")
        res = L.scan(mg=root, filer="filer-a")
        row = next((r for r in res["rows"] if r["id"] == h), None)
        check("arm H (sender name is a near miss) is DROPPED", row and row["status"], "DROPPED")

        print()
        print("=" * 78)
        print("D3.3  THE EXIT CODE OF THE DELIVERABLE ITSELF")
        print("=" * 78)
        here = os.path.dirname(os.path.abspath(__file__))
        env = dict(os.environ)
        env["MG_ROOT"] = root
        r1 = subprocess.run([sys.executable, os.path.join(here, "verdictwatch.py"),
                             "--root", root, "--filer", "filer-a", "--quiet"],
                            capture_output=True, text=True, env=env, timeout=120)
        check("verdictwatch exits 1 while drops exist", r1.returncode, 1)
        r2 = subprocess.run([sys.executable, os.path.join(here, "verdictwatch.py"),
                             "--root", root, "--filer", "filer-b-never-filed", "--quiet"],
                            capture_output=True, text=True, env=env, timeout=120)
        check("verdictwatch exits 0 on an empty population", r2.returncode, 0)

        print()
        print("=" * 78)
        print(f"D3 RESULT: {len(FAILS)} failing construction(s) {FAILS}")
        print("=" * 78)
        return 1 if FAILS else 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
