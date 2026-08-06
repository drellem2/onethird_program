#!/usr/bin/env python3
"""mg-40e4 — the shared parts of this audit.

Two things live here and nothing else: loading a module AS IT IS AT A REVISION (`git show`
plus `exec`, never a paraphrase and never a copy of the old source into this directory), and
the repository root.  Everything that decides anything is in the section script that decides
it, so no verdict of this audit is reached in a file a reader has to go looking for.
"""
import os
import subprocess
import types

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()

VISIBLE = "code/state_delegation_repair_a74f/visible_a74f.py"
SIX65EB = "code/state_visibility_audit_65eb/six65eb.py"
ANCHOR = "6fb424f"          # mg-5f7c's own pre-repair anchor, re-resolved rather than trusted


def module_at(rev, path, name):
    """The module as it is at `rev`, EXECUTED UNMODIFIED."""
    src = subprocess.run(["git", "-C", REPO, "show", f"{rev}:{path}"],
                         capture_output=True, text=True, check=True).stdout
    mod = types.ModuleType(name)
    mod.__file__ = os.path.join(REPO, path)
    exec(compile(src, f"{rev}:{path}", "exec"), mod.__dict__)   # noqa: S102
    return mod


def source_at(rev, path):
    return subprocess.run(["git", "-C", REPO, "show", f"{rev}:{path}"],
                          capture_output=True, text=True, check=True).stdout


def wrap(s, n, lead=""):
    out, line = [], ""
    for w in s.split():
        if len(line) + len(w) + 1 > n:
            out.append(lead + line)
            line = w
        else:
            line = f"{line} {w}".strip()
    if line:
        out.append(lead + line)
    return out
