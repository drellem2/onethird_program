#!/usr/bin/env python3
"""mg-28b6 c1 — PLANTED WORLDS. A CONTROL THAT HAS NEVER BEEN SEEN TO FIRE IS A CLAIM, NOT A
CONTROL, AND THIS REPOSITORY HAS THE RECEIPTS: mg-9876 made 50 arms falsifiable across 59 sites
and nothing ran any of them until mg-724a.

Every world below is applied to a COPY of the four canonical files in a scratch tree. The live
tree is never written. `c0` is then asked what it says about the copy, and each row states BOTH
the exit it must produce AND a string that must appear in its report — with the string checked
for ABSENCE from the unmutated baseline report, which is mg-9876's guard against a row that
would 'pass' against any output at all.

ONE WORLD MUST STAY GREEN, AND IT IS THE MOST INFORMATIVE ROW HERE. W8 puts the DISCHARGED
existence phrasing back as row 8's lead while leaving the `mg-0e8c` rider on the line. `c0` sees
a site carrying its rider and says so. That is not a hole that was missed — it is `c0`'s stated
limit, measured rather than asserted: the gate is on STRUCTURE, not on truth, exactly as
code/facts_registry_03cf and code/concepts_gate_602d declare about themselves. What actually
defends against W8 is a reader, and nothing here pretends otherwise.

EXITS 0 if every world behaved as its row claims, 1 otherwise.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
C0 = os.path.join(HERE, "c0_application.py")

FILES = ["STATE.md",
         os.path.join("docs", "CONCEPTS.md"),
         os.path.join("docs", "OneThird-ProofShape-mg-3af8.md"),
         os.path.join("docs", "state-of-the-wall.html")]


def stage():
    d = tempfile.mkdtemp(prefix="l1b28b6_")
    for f in FILES:
        dst = os.path.join(d, f)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(os.path.join(ROOT, f), dst)
    return d


def run(tree):
    env = dict(os.environ, L1B_28B6_ROOT=tree)
    p = subprocess.run([sys.executable, C0], capture_output=True, text=True, env=env)
    return p.returncode, p.stdout + p.stderr


def edit(tree, f, fn):
    p = os.path.join(tree, f)
    t = open(p, encoding="utf-8").read()
    t2 = fn(t)
    if t2 == t:
        raise RuntimeError("mutation for %s changed nothing — the fixture has rotted" % f)
    open(p, "w", encoding="utf-8").write(t2)


def line_sub(text, contains, fn):
    """Apply fn to the single line containing `contains`; refuse if it is not unique."""
    lines = text.split("\n")
    hits = [i for i, l in enumerate(lines) if contains in l]
    if len(hits) != 1:
        raise RuntimeError("fixture anchor %r matched %d lines, expected 1" % (contains, len(hits)))
    lines[hits[0]] = fn(lines[hits[0]])
    return "\n".join(lines)


# ---- the worlds -----------------------------------------------------------------------------
# (label, mutation, expected exit, string that must appear in the report)

def w_row8_rider(tree):
    edit(tree, "STATE.md", lambda t: line_sub(
        t, "| 8 | **L1b — the wall**", lambda l: l.replace("mg-0e8c", "mg-XXXX")))


def w_chain_link_rider(tree):
    edit(tree, os.path.join("docs", "state-of-the-wall.html"), lambda t: line_sub(
        t, 'class="why"><b>L1b</b>', lambda l: l.replace("mg-28b6", "mg-XXXX")))


def w_chain_node_reverted(tree):
    edit(tree, os.path.join("docs", "state-of-the-wall.html"), lambda t: line_sub(
        t, '<div class="cnode">E[inv_e]',
        lambda l: '      <div class="cnode">&lambda;_std &rarr; 1<span class="n-sub">near-ordinal-sum</span></div>'))


def w_node_c_loses_eps_sup(tree):
    edit(tree, "STATE.md", lambda t: line_sub(
        t, 'C["E[inv_e]', lambda l: l.replace("a uniform constant is PROVEN (ε_sup &lt; 1)",
                                              "a constant, uniform in n")))


def w_new_bare_site(tree):
    # A NEW site, introduced the way a hurried edit would introduce one: the shorter, more
    # quotable, DISCHARGED phrasing, in a file that already carries the correction elsewhere.
    edit(tree, os.path.join("docs", "CONCEPTS.md"), lambda t: t.replace(
        "## 1. The objects, in words before symbols",
        "## 1. The objects, in words before symbols\n\nThe wall asks for `1 − λ_std ≤ ε_spec` "
        "for an explicit absolute constant, uniform in `n`.\n", 1))


def w_anchor_renamed(tree):
    edit(tree, "STATE.md", lambda t: line_sub(
        t, "| 8 | **L1b — the wall**",
        lambda l: l.replace("| 8 | **L1b — the wall**", "| 8 | **L1b — the barrier**", 1)))


def w_anchor_duplicated(tree):
    def dup(t):
        lines = t.split("\n")
        hits = [i for i, l in enumerate(lines) if '<div class="cnode">E[inv_e]' in l]
        lines.insert(hits[0], lines[hits[0]])
        return "\n".join(lines)
    edit(tree, os.path.join("docs", "state-of-the-wall.html"), dup)


def w_wrong_direction_stays_green(tree):
    # The rider stays; the SENTENCE goes back to the discharged form.
    edit(tree, "STATE.md", lambda t: line_sub(
        t, "| 8 | **L1b — the wall**",
        lambda l: l.replace(
            "frozen ⟹ **`E[inv_e] ≤ (ε/6)(n²−1)` for a constant `ε ≤ ε_dem ≈ 2×10⁻²`, uniform in `n`**",
            "frozen ⟹ **`1 − λ_std ≤ ε_spec` for an explicit absolute constant, uniform in `n`**", 1)))


WORLDS = [
    ("row 8 loses its mg-0e8c rider", w_row8_rider, 1, "FIRED   STATE.md row 8"),
    ("twin chain LINK loses its mg-28b6 rider", w_chain_link_rider, 1,
     "FIRED   twin chain link B->C"),
    ("twin chain NODE reverted to λ_std → 1", w_chain_node_reverted, 2,
     "site twin chain node C: anchor"),
    ("mermaid node C loses ε_sup, regains the old label", w_node_c_loses_eps_sup, 1,
     "FIRED   STATE.md mermaid node C"),
    ("a NEW bare existence sentence enters CONCEPTS.md", w_new_bare_site, 1,
     "with no rider or strike within reach"),
    ("row 8's label is renamed (anchor lost)", w_anchor_renamed, 2, "site STATE.md row 8: anchor"),
    ("the chain node is duplicated (anchor ambiguous)", w_anchor_duplicated, 2, "matched 2 lines"),
    ("WRONG DIRECTION — discharged phrasing restored, rider kept",
     w_wrong_direction_stays_green, 0, "c0 GREEN"),
]


def main():
    print("=" * 92)
    print("mg-28b6 c1 — PLANTED WORLDS FOR c0. Each is applied to a COPY; the live tree is never")
    print("written. Seven worlds must fire or refuse; the eighth must stay GREEN on purpose.")
    print("=" * 92)

    base_tree = stage()
    base_rc, base_out = run(base_tree)
    shutil.rmtree(base_tree)
    if base_rc != 0:
        print("\nc1 REFUSES to score anything: the UNMUTATED baseline is not green (exit %d)."
              % base_rc)
        print("A negative control against a red baseline scores its own noise.")
        print(base_out)
        return 1

    print("\n%-52s %-6s %-8s %s" % ("world", "exit", "wanted", "verdict"))
    print("-" * 92)
    bad = 0
    for label, mutate, want_rc, want_str in WORLDS:
        tree = stage()
        try:
            mutate(tree)
        except RuntimeError as e:
            print("%-52s %-6s %-8s *** FIXTURE ROTTED: %s" % (label, "-", want_rc, e))
            bad += 1
            shutil.rmtree(tree)
            continue
        rc, out = run(tree)
        shutil.rmtree(tree)
        ok_rc = (rc == want_rc)
        ok_str = want_str in out
        # mg-9876's guard: a row whose expect-string is already in the BASELINE report scores
        # nothing, because it would 'pass' against an arm that never noticed the mutation.
        falsifiable = want_str not in base_out or want_rc == 0
        verdict = "CAUGHT" if (ok_rc and ok_str and falsifiable) else "*** MISSED ***"
        detail = []
        if not ok_rc:
            detail.append("exit %d, wanted %d" % (rc, want_rc))
        if not ok_str:
            detail.append("report lacks %r" % want_str)
        if not falsifiable:
            detail.append("UNFALSIFIABLE: %r is in the baseline report too" % want_str)
        if verdict != "CAUGHT":
            bad += 1
        print("%-52s %-6d %-8d %s %s" % (label, rc, want_rc, verdict,
                                         ("— " + "; ".join(detail)) if detail else ""))

    print()
    print("%d of %d worlds behaved as claimed; %d did not." % (len(WORLDS) - bad, len(WORLDS), bad))
    print()
    print("READ W8 BEFORE CITING THIS SUITE. It is green because c0 checks that a rider is")
    print("THERE, not that the sentence beside it is true. That is the limit c0's docstring")
    print("states, and this row is the measurement of it rather than a promise about it.")
    print("=" * 92)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
