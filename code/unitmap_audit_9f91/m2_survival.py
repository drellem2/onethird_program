#!/usr/bin/env python3
"""mg-9f91 / step 5 -- DID TODAY'S OTHER ROW-8 LANDINGS SURVIVE?

Three tickets edited ledger row 8 on 2026-08-07:
    a682e1d  mg-d1a2  the DO-NOT-CITE literature guard
    4ef64d7  mg-5ce3  the "NO N_0 WORKS FOR THE CLASS" text
    21ee93f  mg-9adf  the eps_spec/eps_c3ca unit map   <-- under audit

P13 (my own pre-registered most-likely error) is scoring a REFLOW as a LOSS.  Row 8
is one enormous single-line table cell; any edit to it renders as "the whole line
changed".  So this detector NEVER LOOKS AT THE DIFF.  It extracts each guarded span
by string search from the landed file and from the parent, and compares bytes.

  present + byte-identical  -> INTACT   (whatever the diff hunk looks like)
  present + differs         -> REFLOWED (report the delta, do not call it a loss)
  absent                    -> LOST

Run with no args: compares HEAD's STATE.md against 72a6e33's.
"""
import subprocess
import sys
import unicodedata

PARENT = "72a6e33"   # mg-ba78, the commit mg-9adf landed on top of
LANDED = "21ee93f"   # mg-9adf

# (owner, label, needle)   needle must be verbatim from the PARENT.
SPANS = [
    ("mg-d1a2", "guard: instruction",
     "DO NOT CITE THE LITERATURE BOUND AGAINST THIS `N₀`:"),
    ("mg-d1a2", "guard: reason",
     "that discharges nothing here"),
    ("mg-d1a2", "guard: refereed cite",
     "`n ≥ 12` (refereed, Peczarski 2006)"),
    ("mg-d1a2", "guard: preprint cite",
     "`n ≥ 15` (preprint, Gupta 2026)"),
    ("mg-d1a2", "guard: mg-d1a2's own reason kept and attributed",
     "an unspecified threshold is not a size any number can exceed"),

    ("mg-5ce3", "N_0: headline",
     "`N₀` IS NOT UNSPECIFIED: NO `N₀` WORKS FOR THE CLASS AT ALL"),
    ("mg-5ce3", "N_0: the counterexample family",
     "`g(n) = n²` below `N₀` and `n²/log₂ n` at and above"),
    ("mg-5ce3", "N_0: the 10^90 figure",
     "`n ≥ 2³⁰⁰ ≈ 10⁹⁰`"),
    ("mg-5ce3", "N_0: the superseded figure",
     "`10⁹⁰³¹` at the superseded"),
    ("mg-5ce3", "N_0: what that closes",
     "**What that closes:**"),
    ("mg-5ce3", "N_0: not a research direction",
     "is **not a research direction**"),
    ("mg-5ce3", "N_0: what it does not claim",
     "**What it does not claim:**"),
    ("mg-5ce3", "N_0: strictly stronger rider",
     "must first prove something strictly stronger than (LIB-weak)"),
]


def show(rev, path):
    return subprocess.run(["git", "show", f"{rev}:{path}"],
                          capture_output=True, text=True, check=True).stdout


def row8(text):
    """The ledger row-8 cell: the line starting '| 8 |'."""
    for line in text.split("\n"):
        if line.startswith("| 8 |"):
            return line
    return None


def report(name, parent_txt, landed_txt):
    p8, l8 = row8(parent_txt), row8(landed_txt)
    if p8 is None or l8 is None:
        print(f"  !! row 8 not found (parent={p8 is not None} landed={l8 is not None})")
        return 0, 0, 0
    intact = reflowed = lost = 0
    for owner, label, needle in SPANS:
        inp = needle in p8
        inl = needle in l8
        if not inp:
            print(f"  ?? {owner:8} {label:45} NEEDLE NOT IN PARENT -- detector bug, not a finding")
            continue
        if inl:
            print(f"  OK {owner:8} {label:45} INTACT (byte-identical substring)")
            intact += 1
        else:
            # present-but-reflowed vs outright gone: look for a normalised form
            norm = lambda s: unicodedata.normalize("NFKC", s).replace("*", "").replace("`", "")
            if norm(needle) in norm(l8):
                print(f"  ~~ {owner:8} {label:45} REFLOWED (survives modulo emphasis/backticks)")
                reflowed += 1
            else:
                print(f"  XX {owner:8} {label:45} LOST")
                lost += 1
    return intact, reflowed, lost


def main():
    path = "STATE.md"
    parent_txt = show(PARENT, path)
    landed_txt = show(LANDED, path)
    head_txt = open(path, encoding="utf-8").read()

    print(f"=== row-8 span survival: {PARENT} (parent) -> {LANDED} (mg-9adf) ===")
    a = report("landed", parent_txt, landed_txt)
    print()
    print(f"=== row-8 span survival: {PARENT} (parent) -> HEAD (working tree) ===")
    b = report("head", parent_txt, head_txt)

    print()
    print(f"at mg-9adf : {a[0]} intact, {a[1]} reflowed, {a[2]} LOST  (of {len(SPANS)})")
    print(f"at HEAD    : {b[0]} intact, {b[1]} reflowed, {b[2]} LOST  (of {len(SPANS)})")

    # size accounting -- a cell that SHRANK is the thing to look at
    p8, l8 = row8(parent_txt), row8(landed_txt)
    print()
    print(f"row-8 cell length: parent {len(p8)} chars -> landed {len(l8)} chars "
          f"({len(l8)-len(p8):+d})")

    return 1 if (a[2] or b[2]) else 0


if __name__ == "__main__":
    sys.exit(main())
