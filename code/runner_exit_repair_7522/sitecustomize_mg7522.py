"""Injected via PYTHONPATH by s2_status.py.  Forces ONE named script to report
failure AFTER it has done all of its real work.

Why this and not an edit to the target.  Appending `raise SystemExit(1)` only
fires if the target falls off the end, and a target ending in `sys.exit(main())`
never reaches it -- so an appended forcer comes back 0, which looks exactly like
a runner that swallowed the status.  That is the instrument's own defect wearing
the finding's clothes; mg-05eb's first draft of j3 printed it as `NOT CAUGHT`
against two sound runners.  An `atexit` hook fires on every exit path, and
injecting it through `sitecustomize` leaves the target's bytes -- and its line
numbers -- untouched.

The marker is written to STDERR, not stdout, so it cannot land inside the
transcript the target is writing.  s2 checks the committed transcripts for
movement and a marker in the bytes would have made that check meaningless.
"""
import os
import sys

_want = os.environ.get("MG7522_FORCE_TARGET")
if _want:
    try:
        _me = os.path.abspath(sys.argv[0])
    except Exception:
        _me = ""
    if _me and os.path.abspath(_want) == _me:
        import atexit

        def _mg7522_force():
            try:
                sys.stdout.flush()
                sys.stderr.write("*** MG-7522 FORCED FAILURE ***\n")
                sys.stderr.flush()
            except Exception:
                pass
            os._exit(1)

        atexit.register(_mg7522_force)
