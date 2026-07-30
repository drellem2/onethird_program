"""Run a script with `open` instrumented, and record every path it READS.

    D633_TRACE=/path/to/record python3 trace_open.py <script> [args...]

Why a wrapper process and not an in-process patch: the five checkers are
module-level scripts that call `sys.exit`, import siblings by bare name, and
two of them import the same module under the same name.  One process each
keeps them from measuring one another.

WHAT IS RECORDED, AND WHAT IS NOT.  Only opens in TEXT mode.  mg-7dd3 recorded
its own near-miss here: an `open`-tracer that counted `shutil.copytree`'s
binary reads, which would have hidden the `run_all.sh` hole under a pile of
byte-for-byte copies.  Binary opens are counted separately and reported, so
the exclusion is visible rather than silent -- the failure this whole ticket
is about, applied to the instrument measuring it.
"""

import builtins
import io
import json
import os
import runpy
import sys

RECORD = os.environ.get("D633_TRACE")
_real_open = builtins.open
text_reads, binary_reads = [], []

# NOTHING IS SUBTRACTED HERE, AND TWO EARLIER VERSIONS SUBTRACTED SOMETHING.
# The target's own path must NOT be dropped: `s1_extent.py` reads its own
# source AS A TARGET, its file sitting inside one of the four trees it scans,
# and dropping it made E1 report that checker's printed file count as false.
# A skip-once was then added for "runpy's own read" -- and runpy does not read
# through `builtins.open` at all (it goes through `io.open_code`), so the skip
# was never consumed by runpy and swallowed the checker's genuine self-read
# instead.  Both are in OUTCOMES.md.  The tracer now records every text read
# and lets the caller decide, which is the only version of this that cannot
# hide a read by accident.
def _open(file, mode="r", *a, **kw):
    try:
        path = os.path.abspath(os.fspath(file))
    except TypeError:                      # a file descriptor
        path = None
    if path is not None and "w" not in mode and "a" not in mode \
            and "x" not in mode and "+" not in mode:
        (binary_reads if "b" in mode else text_reads).append(path)
    return _real_open(file, mode, *a, **kw)


builtins.open = _open
io.open = _open

target = sys.argv[1]
sys.argv = sys.argv[1:]
sys.path.insert(0, os.path.dirname(os.path.abspath(target)))
code = 0
try:
    runpy.run_path(target, run_name="__main__")
except SystemExit as e:
    code = e.code if isinstance(e.code, int) else 0
finally:
    builtins.open = _real_open
    io.open = _real_open
    if RECORD:
        with _real_open(RECORD, "w", encoding="utf-8") as fh:
            json.dump({"exit": code,
                       "text": sorted(set(text_reads)),
                       "binary": sorted(set(binary_reads))}, fh)
sys.exit(code)
