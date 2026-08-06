#!/usr/bin/env python3
"""SELF-TEST -- the instrument checked against itself, and against a mutant.

Six of this instrument's defects were found while building it and are recorded
in the README. The three that could recur silently get a regression here.

The last section is the one that matters most: a MUTATION TEST. D3's matched
pair is only evidence if a detector that always answered the same thing would
FAIL it. So the pair is re-run against two mutants -- always-DELIVERED and
always-DROPPED -- and each must be caught. A control that cannot fail is the
defect this whole ticket is about.

Exit 0 if every check passes, 1 otherwise.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_bf3f as L  # noqa: E402
import d2_cause  # noqa: E402

FAILS = []


def check(label, got, want):
    ok = got == want
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}: got {got!r}, expected {want!r}")
    if not ok:
        FAILS.append(label)


def main():
    print("=" * 78)
    print("S1  parsing and resolution")
    print("=" * 78)
    check("parse_ts on a normal stamp",
          str(L.parse_ts("2026-08-06T21:54:58Z")), "2026-08-06 21:54:58")
    check("parse_ts on junk returns None", L.parse_ts("not-a-date"), None)
    check("parse_ts on empty returns None", L.parse_ts(""), None)

    check("shape resolver on a bare id", "9a19" in L.worker_names_by_shape("mg-9a19"), True)
    check("shape resolver on a generation prefix",
          "z9a19" in L.worker_names_by_shape("mg-9a19"), True)
    check("shape resolver refuses a two-character prefix",
          "zz9a19" in L.worker_names_by_shape("mg-9a19"), False)
    check("shape resolver refuses an unrelated agent",
          "mayor" in L.worker_names_by_shape("mg-9a19"), False)
    check("shape resolver refuses a name that merely CONTAINS the id",
          "9a19x" in L.worker_names_by_shape("mg-9a19"), False)
    check("shape resolver declines a non-hex id", L.worker_names_by_shape("mg-zzzz"), set())

    print()
    print("=" * 78)
    print("S2  Fisher exact, against values computable by hand")
    print("=" * 78)
    p = d2_cause.fisher_exact_2x2(1, 1, 1, 1)
    check("2x2 of all ones is p=1", round(p, 9), 1.0)
    p = d2_cause.fisher_exact_2x2(3, 0, 0, 3)
    check("perfect 3/3 separation", round(p, 4), 0.1)

    print()
    print("=" * 78)
    print("S3  regressions for defects found while building this")
    print("=" * 78)
    root = tempfile.mkdtemp(prefix="bf3f-self-")
    try:
        mgbin = shutil.which("mg") or os.path.expanduser("~/go/bin/mg")
        subprocess.run([mgbin, "--root", root, "init"], capture_output=True, timeout=120)
        work = os.path.join(root, "work", "claimed")
        os.makedirs(work, exist_ok=True)
        # DEFECT-5: a claimed item is `mg-xxxx.md.<pid>` on disk.
        open(os.path.join(work, "mg-aaaa.md.4242"), "w").write(
            "---\nid: mg-aaaa\ncreated: 2026-08-06T00:00:00Z\ncreator: f1\n---\n\n# claimed item\n")
        items = L.load_items(root)
        check("DEFECT-5: a pid-suffixed claimed item is loaded", "mg-aaaa" in items, True)
        check("DEFECT-5: its id has no pid in it",
              items.get("mg-aaaa", {}).get("id"), "mg-aaaa")
        # and a file that merely looks similar must NOT be loaded
        open(os.path.join(work, "mg-bbbb.md.bak"), "w").write("---\ncreator: f1\n---\n")
        items = L.load_items(root)
        check("DEFECT-5: a .md.bak sidecar file is NOT loaded as an item",
              "mg-bbbb" in items, False)

        # DEFECT-1: the worker shown must be the branch's own spelling.
        done = os.path.join(root, "work", "done")
        os.makedirs(done, exist_ok=True)
        open(os.path.join(done, "mg-cccc.md"), "w").write(
            "---\nid: mg-cccc\ncreated: 2026-08-06T00:00:00Z\ncreator: f1\n---\n\n# t\n")
        json.dump({"branch": "polecat-y0120"}, open(os.path.join(done, "mg-cccc.result.json"), "w"))
        it = L.load_items(root)["mg-cccc"]
        check("DEFECT-1: worker is displayed as the branch spells it",
              L.worker_declared(it), "y0120")
        check("DEFECT-1: matching still accepts the mg- spelling",
              "mg-y0120" in L.worker_names(it), True)
    finally:
        shutil.rmtree(root, ignore_errors=True)

    print()
    print("=" * 78)
    print("S4  THE MUTATION TEST -- can D3's matched pair actually fail?")
    print("=" * 78)
    print("  D3 asserts 1 dropped on arm A and 0 on arm B. That is only evidence if a")
    print("  detector that answered the same thing regardless would be CAUGHT. Two")
    print("  mutants are built and the pair must reject both.")

    real_scan = L.scan

    def mutant(answer):
        def _scan(*a, **kw):
            res = real_scan(*a, **kw)
            for r in res["rows"]:
                if r["status"] != "UNDECIDABLE":
                    r["status"] = answer
                    r["verdict"] = (answer == "DELIVERED")
            return res
        return _scan

    here = os.path.dirname(os.path.abspath(__file__))
    for answer in ("DELIVERED", "DROPPED"):
        L.scan = mutant(answer)
        import importlib
        d3 = importlib.import_module("d3_fire")
        importlib.reload(d3)
        d3.L.scan = mutant(answer)
        d3.FAILS = []
        buf = []
        real_print = print
        try:
            import builtins
            builtins.print = lambda *a, **k: buf.append(" ".join(str(x) for x in a))
            rc = d3.main()
        finally:
            builtins.print = real_print
        caught = rc != 0 and len(d3.FAILS) > 0
        check(f"mutant always-{answer} is CAUGHT by the matched pair", caught, True)
        real_print(f"        (mutant failed {len(d3.FAILS)} construction(s): {d3.FAILS[:4]})")
    L.scan = real_scan

    print()
    print("=" * 78)
    print(f"SELF-TEST RESULT: {len(FAILS)} failure(s) {FAILS}")
    print("=" * 78)
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
