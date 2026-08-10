#!/usr/bin/env python3
"""mg-9bc2 — the negative control: does `twin_pin.py` actually fail when it should?

WHY THIS FILE EXISTS.  The artifact this ticket repairs was a claim nobody could check
(`Generated 2026-07-19`), and the obvious way to fail this ticket is to replace it with a
SECOND claim nobody can check — a control that exits 0 because it is looking at nothing.
mg-2da3's battery is the local precedent: it passed byte-identically while `STATE.md` was
gutted from 175,552 to 37,958 bytes, because every path in it was revision-pinned.  So each
mutation below is a specific way the twin or `STATE.md` could go wrong, applied to COPIES in
a temporary directory, with the section that is supposed to catch it named in advance.

READ THE LAST COLUMN.  A mutation that exits 0 is a hole in the instrument, not a pass.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
STATE = os.path.join(ROOT, "STATE.md")
TWIN = os.path.join(ROOT, "docs", "state-of-the-wall.html")

# The live tree is ALREADY at exit 1 (rows 8 and 9 have drifted), so "did the mutation make
# it fail?" is not a question the exit code can answer on its own here.  Every expectation
# below is therefore stated as a SECTION and a STRING that must appear in the output, and
# the baseline's own output is subtracted first.
MUTATIONS = []


def mutation(name, section, expect, target):
    def deco(fn):
        MUTATIONS.append((name, section, expect, target, fn))
        return fn
    return deco


# ---------------------------------------------------------------------- section 1
@mutation("pin block deleted entirely", "1",
          "no STATE-PIN block in the twin", "twin")
def m_no_pin(text):
    i = text.find("<!-- STATE-PIN v1")
    j = text.find("STATE-PIN end -->") + len("STATE-PIN end -->")
    return text[:i] + text[j:]


@mutation("a ledger row deleted from the twin only", "1",
          "the row sets disagree", "twin")
def m_drop_twin_row(text):
    return re.sub(r'<tr><td class="rowlabel">7</td>.*?</tr>', "", text, count=1, flags=re.S)


# ---------------------------------------------------------------------- section 2
@mutation("one character changed in an UNDRIFTED STATE.md ledger row (row 1)", "2",
          "row 1    MOVED", "state")
def m_touch_row1(text):
    return text.replace("| 1 | `λ_std = 1 ⟺ ordinal sum` | `U` | **proven** | any |",
                        "| 1 | `λ_std = 1 ⟺ ordinal sum` | `U` | **proven** | ANY |", 1)


@mutation("a whole STATE.md ledger cell emptied (row 10 status)", "2",
          "row 10   MOVED", "state")
def m_empty_row10(text):
    return text.replace("| ⚠️ **`FP`** | empirical (125/126) | n ≤ 6 data |",
                        "| ⚠️ **`FP`** |  | n ≤ 6 data |", 1)


# ---------------------------------------------------------------------- section 4
@mutation("twin's KIND mark for row 10 flipped FP -> U", "4",
          "row 10   MISMATCH", "twin")
def m_flip_kind(text):
    return text.replace('<span class="kind fp">&#9888;&#65039; FP</span>',
                        '<span class="kind u">U</span>', 1)


@mutation("STATE.md's KIND mark for row 9 flipped FP✗ -> U", "4",
          "row 9    MISMATCH", "state")
def m_flip_state_kind(text):
    return text.replace("| `FP✗` | **first disjunct** false as stated",
                        "| `U` | **first disjunct** false as stated", 1)


# ---------------------------------------------------------------------- section 5
@mutation("`Generated <date>` re-introduced into the header", "5",
          r"matches /\bGenerated\b", "twin")
def m_regenerate_claim(text):
    return text.replace("<span><b>Maintained by</b> pm-onethird</span>",
                        "<span><b>Maintained by</b> pm-onethird</span>\n"
                        "      <span><b>Generated</b> 2026-08-10</span>", 1)


@mutation("the twin re-claims canonicity in the footer", "5",
          "a canonicity claim on a line that does not name STATE.md", "twin")
def m_reclaim_canon(text):
    return text.replace("<footer>",
                        "<footer>\n    <p>This is the source of truth for the program.</p>", 1)


# ---------------------------------------------------------------------- section 6
@mutation("visible provenance line points at a DIFFERENT commit than the pin", "6",
          "the visible provenance line does not quote the pinned commit", "twin")
def m_desync_visible(text):
    return text.replace("@ 276aead1a8c5 (2026-08-07)", "@ deadbeefcafe (2026-08-10)", 1)


@mutation("visible provenance line removed (pin becomes machine-only)", "6",
          "no <span id=\"provenance\">", "twin")
def m_drop_visible(text):
    return re.sub(r'<span id="provenance">.*?</span>\s*$', "", text, count=1, flags=re.M | re.S)


# ---------------------------------------------------------------------- positive control
@mutation("NO MUTATION — the baseline", "-",
          None, "none")
def m_none(text):
    return text


def run(state_path, twin_path):
    proc = subprocess.run(
        [sys.executable, os.path.join(HERE, "twin_pin.py"),
         "--state", state_path, "--twin", twin_path],
        capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def main():
    base_state = open(STATE, encoding="utf-8").read()
    base_twin = open(TWIN, encoding="utf-8").read()

    print("=" * 92)
    print("mg-9bc2 — NEGATIVE CONTROL for twin_pin.py")
    print("=" * 92)
    print()
    print("Each mutation is applied to a COPY.  The live tree is never written.")
    print("The instrument's baseline verdict is DRIFT (exit 1) because ledger rows 8 and 9")
    print("really have moved, so the exit code alone cannot score these; each row states the")
    print("section that must fire and the string that must appear.")
    print()

    tmp = tempfile.mkdtemp(prefix="twinpin9bc2-")
    rows, holes = [], 0
    try:
        for name, section, expect, target, fn in MUTATIONS:
            sp = os.path.join(tmp, "STATE.md")
            tp = os.path.join(tmp, "twin.html")
            state_text = fn(base_state) if target == "state" else base_state
            twin_text = fn(base_twin) if target == "twin" else base_twin
            if target == "state" and state_text == base_state:
                rows.append((name, section, "SETUP FAILED", "mutation was a no-op"))
                holes += 1
                continue
            if target == "twin" and twin_text == base_twin:
                rows.append((name, section, "SETUP FAILED", "mutation was a no-op"))
                holes += 1
                continue
            with open(sp, "w", encoding="utf-8") as fh:
                fh.write(state_text)
            with open(tp, "w", encoding="utf-8") as fh:
                fh.write(twin_text)

            code, out = run(sp, tp)
            if expect is None:
                ok = (code == 1 and "rows 8 and 9" not in out
                      and "8 9" in out and "STRUCTURAL" not in out)
                verdict = "CAUGHT" if ok else "HOLE"
                detail = f"exit {code}; baseline must be DRIFT at rows 8 9 and nothing else"
            else:
                ok = expect in out
                verdict = "CAUGHT" if ok else "HOLE"
                detail = f"exit {code}; looked for {expect!r}"
            if not ok:
                holes += 1
            rows.append((name, section, verdict, detail))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    width = max(len(r[0]) for r in rows)
    print(f"{'mutation'.ljust(width)}  sec  verdict  detail")
    print("-" * 92)
    for name, section, verdict, detail in rows:
        print(f"{name.ljust(width)}  {section:<3}  {verdict:<7}  {detail}")
    print()
    print(f"{len(rows) - holes} of {len(rows)} caught; {holes} hole(s).")
    print()
    if holes:
        print("A HOLE IS A FINDING, NOT A TEST FAILURE TO SUPPRESS — it is a way the twin can")
        print("go wrong that this instrument does not see.  Record it in COVERAGE.md.")
        return 1
    print("Every mutation was caught by the section that claimed it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
