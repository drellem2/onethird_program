"""Injected via PYTHONPATH by j3_control.py.  Forces ONE named script to report
failure AFTER it has done all of its real work.

Why this and not an edit to the script.  Appending `raise SystemExit(1)` to the
target only fires if the target falls off the end; `code/face_geometry_audit_6653/
verify_claims.py` ends in `sys.exit(main())`, so an appended forcer never runs and
the runner comes back 0 -- which looks exactly like a runner that swallowed the
status.  That is the audit's own defect wearing the finding's clothes, and the
first draft of j3 printed it as `*** NOT CAUGHT ***` at two sites.  An `atexit`
hook fires on every exit path, and injecting it through `sitecustomize` leaves the
target's bytes -- and its line numbers -- untouched.
"""
import os
import sys

_want = os.environ.get("MG05EB_FORCE_TARGET")
if _want:
    try:
        _me = os.path.abspath(sys.argv[0])
    except Exception:
        _me = ""
    if _me and os.path.abspath(_want) == _me:
        import atexit

        def _mg05eb_force():
            try:
                sys.stdout.write("*** MG-05EB FORCED FAILURE ***\n")
                sys.stdout.flush()
                sys.stderr.flush()
            except Exception:
                pass
            os._exit(1)

        atexit.register(_mg05eb_force)
