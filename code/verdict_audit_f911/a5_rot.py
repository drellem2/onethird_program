#!/usr/bin/env python3
"""mg-f911 A5 -- DEFECT-A demonstrated live, not transcribed.

mg-bf3f's two CONSTRUCTIVE probes -- the matched pair in d3_fire.py and the
mutation test in selftest_bf3f.py, which imports d3_fire's mail() -- stopped
working roughly 22 hours after mg-bf3f landed, because mg-d639 turned an unknown
mail recipient from a silent create into a refusal.

Quoting the crash in a markdown file would be a claim. This file makes it a
measurement: it drives BOTH spellings of the same send against a throwaway store
through the real `mg` binary and prints what each returns. It will keep passing
after the repair, because it asserts on the OLD form failing and the NEW form
working -- if mg ever reverts, this file says so.

Exit 0 if both arms land on their declared expectation.
"""
import os
import shutil
import subprocess
import sys
import tempfile

MG_BIN = shutil.which("mg") or os.path.expanduser("~/go/bin/mg")
FAILS = []


def mg(root, *args, stdin=None):
    env = dict(os.environ)
    env["MG_ROOT"] = root
    env.pop("POGO_AGENT_NAME", None)
    env.pop("MG_ACTOR", None)
    return subprocess.run([MG_BIN, "--root", root] + list(args), env=env,
                          capture_output=True, text=True, input=stdin, timeout=120)


def check(label, got, want):
    ok = got == want
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}: got {got!r}, expected {want!r}")
    if not ok:
        FAILS.append(label)


def main():
    root = tempfile.mkdtemp(prefix="f911-rot-")
    try:
        mg(root, "init")
        print(f"  throwaway store : {root}")
        print(f"  mg binary       : {MG_BIN}")
        print(f"  binary mtime    : {__import__('datetime').datetime.fromtimestamp(os.path.getmtime(MG_BIN)).isoformat()}")
        print()
        print("=" * 78)
        print("A5.1  THE FORM mg-bf3f SHIPPED -- d3_fire.py:80 as it landed")
        print("=" * 78)
        old = mg(root, "mail", "send", "filer-a", "--from", "wb1",
                 "--subject", "arm B verdict", "--body-file", "-",
                 stdin="the control arm's verdict\n")
        print(f"  rc={old.returncode}")
        for line in (old.stdout + old.stderr).strip().splitlines()[:3]:
            print(f"    {line}")
        check("A5.1 the shipped form is REFUSED by today's mg", old.returncode != 0, True)

        print()
        print("=" * 78)
        print("A5.2  THE REPAIRED FORM -- the same send with --create")
        print("=" * 78)
        new = mg(root, "mail", "send", "filer-a", "--from", "wb1",
                 "--subject", "arm B verdict", "--body-file", "-", "--create",
                 stdin="the control arm's verdict\n")
        print(f"  rc={new.returncode}")
        for line in (new.stdout + new.stderr).strip().splitlines()[:3]:
            print(f"    {line}")
        check("A5.2 the repaired form delivers", new.returncode, 0)

        print()
        print("=" * 78)
        print("A5.3  WHAT THIS COST -- which probes died and which did not")
        print("=" * 78)
        print("  d3_fire.py       (matched pair)  : DIED -- calls mail() for arm B")
        print("  selftest_bf3f.py (mutation test) : DIED -- imports d3_fire's mail()")
        print("  d1_population.py (the census)    : UNAFFECTED, read-only")
        print("  d2_cause.py      (the cause)     : UNAFFECTED, read-only")
        print("  verdictwatch.py  (the deliverable): UNAFFECTED, read-only")
        print()
        print("  The two that died are the two that constitute the evidence that the")
        print("  detector is not vacuous. The detector itself never stopped working.")
        print()
        print("=" * 78)
        print(f"A5 RESULT: {len(FAILS)} failing arm(s) {FAILS}")
        print("=" * 78)
        return 1 if FAILS else 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
