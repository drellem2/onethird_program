#!/usr/bin/env python3
"""Independent cell/line measurement for the mg-bd41 audit of b68db5d (mg-7735).

Imports nothing from code/state_restructure_34bf/ or code/state_audit_6a2f/.
Every figure is printed with its UNIT named, and every figure is computed over
UNBOUNDED input (no head/tail/limit anywhere).
"""
import subprocess, sys

REPO = subprocess.run(["git","rev-parse","--show-toplevel"],
                     capture_output=True, text=True, check=True).stdout.strip()

def blob(rev, path="STATE.md"):
    """Raw bytes of path at rev."""
    return subprocess.run(["git", "-C", REPO, "show", f"{rev}:{path}"],
                          capture_output=True, check=True).stdout

def lines_bytes(rev, path="STATE.md"):
    """List of lines as BYTES, newline stripped."""
    return blob(rev, path).split(b"\n")

def row(rev, n, path="STATE.md"):
    """1-indexed line n at rev, as bytes, newline stripped."""
    return lines_bytes(rev, path)[n-1]

def cells(line_bytes):
    """Split a markdown table row into its cells.

    A row is  | c1 | c2 | c3 |  -> split on '|' and drop the empty
    fragments produced by the leading and trailing pipe.  Returns the
    RAW inner fragments (leading/trailing spaces intact) and also the
    stripped variants, so the two candidate definitions can be compared.
    """
    s = line_bytes
    if not s.startswith(b"|"):
        return None
    parts = s.split(b"|")
    # leading '' from the opening pipe, trailing '' from the closing pipe
    assert parts[0] == b"", parts[0][:40]
    inner = parts[1:]
    if inner and inner[-1].strip() == b"":
        inner = inner[:-1]
    return inner

def measure(b):
    """Return (bytes, chars) for a bytes object decoded as UTF-8."""
    return len(b), len(b.decode("utf-8"))

def words(b):
    """Whitespace-separated token count, over the whole input."""
    return len(b.decode("utf-8").split())

def split_row(line_bytes):
    """Escape-aware markdown table row split.

    Literal pipes inside STATE.md cells are written `\\|`, so a cell
    boundary is a '|' NOT preceded by a backslash.  Returns the list of
    RAW inner fragments between the opening and closing boundary pipes.
    """
    s = line_bytes.decode("utf-8")
    bounds = [i for i, ch in enumerate(s)
              if ch == "|" and (i == 0 or s[i-1] != "\\")]
    if len(bounds) < 2 or bounds[0] != 0:
        return None
    return [s[bounds[i]+1:bounds[i+1]] for i in range(len(bounds)-1)]

def cell3(rev, n, path="STATE.md"):
    """The third (content) column of row n at rev.  Returns raw str."""
    parts = split_row(row(rev, n, path))
    if parts is None or len(parts) < 3:
        return None
    return parts[2]

def content_cell(rev, n, path="STATE.md"):
    """The row's CONTENT cell = its widest cell.

    STATE.md holds tables of different arities (the ledger rows at :131-:136 are
    3-column, row :89 sits in a 4-column table), so 'the third column' is not a
    portable definition of the cell the index table measures.  The widest cell is.
    """
    parts = split_row(row(rev, n, path))
    if not parts:
        return None
    return max(parts, key=len)
