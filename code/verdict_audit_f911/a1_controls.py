#!/usr/bin/env python3
"""mg-f911 A1 -- MY OWN positive and negative controls for the mg-bf3f detector.

Brief items 1 and 2: make it fire, and make it NOT fire.

E4 of my PREDICTIONS.md binds me here: mg-bf3f already built a matched pair, and
re-running it would be a REPRODUCTION, not evidence I produced. So this file
builds its own store, its own arms, and -- the part that matters -- SHAPES THE
PARENT DID NOT TEST. A control that only repeats the parent's cases can only
confirm what the parent already knew.

Every arm here is FORCED by construction. That word appears on every count.

The two directions have very different stakes and the brief says so:

  * UNDER-reporting (a real drop read as DELIVERED) makes the detector useless.
  * OVER-reporting  (a delivered verdict read as DROPPED) "would retire the
    detector within a week" -- pm-onethird's words. It is the failure that gets
    an instrument switched off, so it gets the most arms here.

Exit 0 if every arm lands on its declared expectation, 1 otherwise. Expectations
are declared in the source BEFORE the run, and an arm whose expectation is
"the detector gets this WRONG" is declared that way rather than quietly omitted.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "verdict_delivery_bf3f"))
import lib_bf3f as L  # noqa: E402

MG_BIN = shutil.which("mg") or os.path.expanduser("~/go/bin/mg")
FAILS = []
NOTES = []


def mg(root, *args, actor=None, stdin=None):
    env = dict(os.environ)
    env["MG_ROOT"] = root
    env.pop("POGO_AGENT_NAME", None)
    if actor:
        env["MG_ACTOR"] = actor
    else:
        env.pop("MG_ACTOR", None)
    return subprocess.run([MG_BIN, "--root", root] + list(args), env=env,
                          capture_output=True, text=True, input=stdin, timeout=120)


def new_item(root, filer, title, body="body\n"):
    p = mg(root, "new", "--title", title, "--body-file", "-", "--no-repo",
           "--type", "task", "--no-declares-remainder", actor=filer, stdin=body)
    if p.returncode != 0:
        raise RuntimeError(f"mg new failed: {p.returncode} {p.stdout} {p.stderr}")
    for tok in (p.stdout + p.stderr).split():
        t = tok.strip(":,.()")
        if t.startswith("mg-") and len(t) >= 6:
            return t
    raise RuntimeError(f"could not read new item id from {p.stdout!r} {p.stderr!r}")


def land(root, iid, worker, archive=False):
    p = mg(root, "claim", iid, actor=worker)
    if p.returncode != 0:
        raise RuntimeError(f"claim failed: {p.stdout} {p.stderr}")
    p = mg(root, "done", iid, "--result",
           json.dumps({"branch": f"polecat-{worker}", "completed_by": "refinery",
                       "mr": "mr-f911-constructed", "target": "main"}), actor="daniel")
    if p.returncode != 0:
        raise RuntimeError(f"done failed: {p.stdout} {p.stderr}")
    if archive:
        p = mg(root, "archive", iid, actor="daniel")
        if p.returncode != 0:
            raise RuntimeError(f"archive failed: {p.stdout} {p.stderr}")


def mail(root, to, frm, subject, body):
    """Send, and VERIFY it landed. A control whose setup silently no-ops is the
    exact defect mg-bf3f's own DEFECT-4 was (its P6b asserted DELIVERED against a
    verdict that had never been archived, because the setup had quietly failed).
    So this raises on a bad send AND re-reads the box to prove the message is
    there before any assertion is made about it."""
    p = mg(root, "mail", "send", to, "--from", frm, "--subject", subject,
           "--body-file", "-", "--create", stdin=body)
    if p.returncode != 0:
        raise RuntimeError(f"mail send failed: {p.stdout} {p.stderr}")
    q = mg(root, "mail", "list", to, "--all", "--json")
    for line in q.stdout.splitlines():
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        if rec.get("subject") == subject and rec.get("from") == frm:
            return rec["id"]
    raise RuntimeError(f"SETUP DID NOT TAKE: no message to {to} from {frm} with that subject")


def status_of(root, filer, iid):
    res = L.scan(mg=root, filer=filer)
    row = next((r for r in res["rows"] if r["id"] == iid), None)
    return (row or {}).get("status"), row


def check(label, got, want, expected_wrong=False):
    ok = got == want
    tag = "PASS" if ok else "FAIL"
    mark = "  <-- DECLARED DEFECT OF THE DETECTOR" if (ok and expected_wrong) else ""
    print(f"  [{tag}] {label}: got {got!r}, expected {want!r}{mark}")
    if not ok:
        FAILS.append(label)
    return ok


def main():
    if not os.path.exists(MG_BIN):
        print(f"  !! mg not found at {MG_BIN}")
        return 1
    root = tempfile.mkdtemp(prefix="f911-controls-")
    print(f"  throwaway store : {root}")
    print(f"  mg binary       : {MG_BIN}")
    p = mg(root, "init")
    if p.returncode != 0:
        print(f"  !! mg init failed: {p.stdout} {p.stderr}")
        return 1
    try:
        print()
        print("=" * 78)
        print("A1.1  MY MATCHED PAIR -- brief items 1 and 2, both FORCED")
        print("=" * 78)
        print("  Not the parent's arms: mine use a filer with a REAL agent-shaped name")
        print("  and a worker whose name is the polecat convention <gen><4hex>, so the")
        print("  pair exercises the same name-matching path the live store uses.")

        a = new_item(root, "onethird-filer", "A: verdict deliberately NOT mailed")
        land(root, a, "z" + a[3:])
        print(f"  arm A {a}: landed, worker z{a[3:]}, NO VERDICT MAILED ON PURPOSE.")

        b = new_item(root, "onethird-filer", "B: verdict mailed before landing")
        wb = "z" + b[3:]
        mail(root, "onethird-filer", wb, f"VERDICT {b} — the finding",
             "the actual finding text\n")
        land(root, b, wb)
        print(f"  arm B {b}: verdict mailed by {wb}, then landed.")

        sa, _ = status_of(root, "onethird-filer", a)
        sb, _ = status_of(root, "onethird-filer", b)
        print()
        check("A1.1 IT FIRES on the dropped verdict", sa, "DROPPED")
        check("A1.1 IT DOES NOT FIRE on the delivered one", sb, "DELIVERED")

        res = L.scan(mg=root, filer="onethird-filer")
        n_drop = len([r for r in res["rows"] if r["status"] == "DROPPED"])
        check("A1.1 exactly one drop in the population (FORCED = 1)", n_drop, 1)

        print()
        print("=" * 78)
        print("A1.2  OVER-REPORTING -- the failure that retires the detector")
        print("=" * 78)
        print("  pm-onethird: over-reporting 'would retire the detector within a week'.")
        print("  So: can I find a verdict that DID arrive and is still called DROPPED?")

        # C2. The worker mails under its BRANCH name rather than its agent name.
        # This is not a contrived spelling: `polecat-<name>` is the string the
        # refinery writes, it is what `git rev-parse --abbrev-ref HEAD` prints in
        # the worktree, and the polecat protocol hands the worker BOTH strings.
        c = new_item(root, "onethird-filer", "C: verdict mailed under the BRANCH name")
        wc = "z" + c[3:]
        mail(root, "onethird-filer", f"polecat-{wc}", f"VERDICT {c} — arrived, wrong From:",
             "this verdict genuinely arrived in the filer's mailbox\n")
        land(root, c, wc)
        sc, rowc = status_of(root, "onethird-filer", c)
        check("A1.2 C: verdict present in the box but From: is the branch name",
              sc, "DROPPED", expected_wrong=True)
        NOTES.append(
            "OVER-REPORT (confirmed, forced): a verdict that IS in the filer's mailbox is "
            "reported DROPPED when the worker signs it with its branch name "
            f"`polecat-{wc}` instead of its agent name `{wc}`. worker_names() derives "
            "{name, mg-name} from the branch and never the `polecat-` spelling itself.")

        # C3. The filer reads the mail and archives it -- already covered by the
        # parent's P6b, so this is a REPRODUCTION and is labelled one.
        d = new_item(root, "onethird-filer", "D: delivered then archived (REPRODUCTION of parent P6b)")
        wd = "z" + d[3:]
        mid = mail(root, "onethird-filer", wd, f"VERDICT {d}", "body\n")
        land(root, d, wd)
        pa = mg(root, "mail", "archive", f"onethird-filer/{mid}")
        if pa.returncode != 0:
            raise RuntimeError(f"archive setup failed: {pa.stdout} {pa.stderr}")
        sd, _ = status_of(root, "onethird-filer", d)
        check("A1.2 D: archived verdict still DELIVERED (REPRODUCTION)", sd, "DELIVERED")

        # C4. The verdict arrives AFTER the landing. No time predicate exists, and
        # that is correct -- a late verdict is still a delivered one -- but it is
        # worth pinning, because a detector that quietly required "before" would
        # over-report every worker who mails from the merge notification.
        e = new_item(root, "onethird-filer", "E: verdict mailed AFTER the landing")
        we = "z" + e[3:]
        land(root, e, we)
        s_before, _ = status_of(root, "onethird-filer", e)
        check("A1.2 E: DROPPED before the late verdict is sent", s_before, "DROPPED")
        mail(root, "onethird-filer", we, f"VERDICT {e} — late", "late but delivered\n")
        s_after, _ = status_of(root, "onethird-filer", e)
        check("A1.2 E: DELIVERED once the late verdict arrives", s_after, "DELIVERED")
        print("        (the flip is produced by one mail and nothing else -- the same")
        print("         two-state evidence the parent produced live on its own row)")

        print()
        print("=" * 78)
        print("A1.3  UNDER-REPORTING -- a NON-verdict credited as a verdict")
        print("=" * 78)
        print("  The predicate is 'a message in the filer's mailbox whose From: is the")
        print("  worker'. There is NO test that the message is a verdict. So:")

        f = new_item(root, "onethird-filer", "F: worker mails the filer something that is NOT a verdict")
        wf = "z" + f[3:]
        mail(root, "onethird-filer", wf, "question about the ticket body",
             "I am stuck, can you clarify scope? (this is NOT a verdict)\n")
        land(root, f, wf)
        sf, _ = status_of(root, "onethird-filer", f)
        check("A1.3 F: a scope question is credited as a delivered verdict",
              sf, "DELIVERED", expected_wrong=True)
        NOTES.append(
            "UNDER-REPORT (confirmed, forced): ANY mail from the worker to the filer counts. "
            "A worker that asks a scope question and never files a verdict reads DELIVERED. "
            "So the reported DROPPED count is a LOWER bound on dropped verdicts, and the "
            "DELIVERED count is an UPPER bound on deliveries. The README sizes four other "
            "bounds explicitly and does not size this one.")

        print()
        print("=" * 78)
        print("A1.4  THE `archived` CASE -- brief item 5, BY CONSTRUCTION not by reading")
        print("=" * 78)
        print("  My PREDICTIONS.md E1 forbids me scoring this from the source alone.")

        # G. done -> archive. The file MOVES from work/done/ to work/archive/<month>/.
        g = new_item(root, "onethird-filer", "G: landed then archived, verdict dropped")
        wg = "z" + g[3:]
        land(root, g, wg, archive=True)
        moved = [p for p in _find(root, g)]
        print(f"  {g} now lives at: {[os.path.relpath(x, root) for x in moved]}")
        check("A1.4 G: the item file really left work/done/",
              any("/done/" in x for x in moved), False)
        sg, rowg = status_of(root, "onethird-filer", g)
        check("A1.4 G: an ARCHIVED item is still reported", sg, "DROPPED")
        check("A1.4 G: and its landing kind is `done` (it passed through done)",
              (rowg or {}).get("kind"), "done")

        # H. Can an item be archived WITHOUT ever being done? If mg refuses, then
        # load_landings' `work.archive` branch -- the half that makes the
        # predicate say "done OR archived" -- is unreachable in practice, and the
        # brief's premise that mg-c3ca "reached archived, not done" is impossible.
        h = new_item(root, "onethird-filer", "H: archive attempted without done")
        mg(root, "claim", h, actor="zh999")
        ph = mg(root, "archive", h, actor="daniel")
        print(f"  `mg archive` on a NOT-done item: rc={ph.returncode} "
              f"{(ph.stdout + ph.stderr).strip().splitlines()[0][:90] if (ph.stdout+ph.stderr).strip() else ''}")
        check("A1.4 H: mg REFUSES to archive an item that never went done",
              ph.returncode != 0, True)
        NOTES.append(
            "ITEM 5, CORRECTED: `mg archive` refuses an item that has not gone done "
            f"(rc={ph.returncode}), so every archived item passed through `done` first and "
            "the landing is recorded at `done`. The brief's premise that mg-c3ca 'reached "
            "archived, not done' is false -- the live store shows work.done at "
            "2026-08-06T00:48:36Z and work.archive 21h later. The real hazard in the "
            "archived case is the FILE MOVE out of work/done/, and the parent's recursive "
            "glob over work/** handles it: arm G above is found after the move.")

        print()
        print("=" * 78)
        print("A1.5  MY OWN MUTATION TEST -- is A1.1 capable of failing?")
        print("=" * 78)
        print("  A1.1's pair is evidence only if a detector that ignored its input")
        print("  would be CAUGHT by it. Built independently of the parent's S4.")

        real = L.scan
        for label, forced in (("always-DELIVERED", "DELIVERED"), ("always-DROPPED", "DROPPED")):
            def mutant(mg=None, filer=None, since=None, simulate=None, _f=forced):
                r = real(mg=mg, filer=filer, since=since, simulate=simulate)
                for row in r["rows"]:
                    row["status"] = _f
                    row["verdict"] = (_f == "DELIVERED")
                return r
            L.scan = mutant
            try:
                ma, _ = status_of(root, "onethird-filer", a)   # truly DROPPED
                mb, _ = status_of(root, "onethird-filer", b)   # truly DELIVERED
                caught = not (ma == "DROPPED" and mb == "DELIVERED")
                check(f"A1.5 mutant {label} is CAUGHT by my pair", caught, True)
            finally:
                L.scan = real

        print()
        print("=" * 78)
        print(f"A1 RESULT: {len(FAILS)} failing arm(s) {FAILS}")
        for n in NOTES:
            print()
            print("  FINDING: " + n.replace("\n", "\n  "))
        print("=" * 78)
        return 1 if FAILS else 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


def _find(root, iid):
    out = []
    for dirpath, _dirnames, filenames in os.walk(os.path.join(root, "work")):
        for fn in filenames:
            if fn.startswith(iid + ".md"):
                out.append(os.path.join(dirpath, fn))
    return out


if __name__ == "__main__":
    sys.exit(main())
