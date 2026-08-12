#!/usr/bin/env python3
"""mg-a518 — the controls for the audit-successor detector's WIDE arming.

WHAT THIS EXISTS TO REFUSE.  mg-a882 recorded that the detector (mg-28b7), armed
narrow on `independent-audit`, examined 4 of this program's 9 merged audits and
reported GREEN.  A 56% blind spot behind a green line.  The remedy — widening to
`audit` — produces an artifact OF THE SAME KIND AS THE DEFECT: a detector that
reports green.  So the only interesting question about the remedy is the one that
was interesting about the defect: IS IT GREEN BECAUSE IT LOOKED, OR GREEN BECAUSE
IT CANNOT SEE?

Every arm below answers that by MUTATING THE STORE AND REQUIRING THE REPORT TO
MOVE.  An arm that only observed the live green state would be the defect wearing
the remedy's clothes.

WHAT IT DOES NOT DO, stated because a control's scope is the part people assume:

  * It does not check that any audit was READ.  Both artifacts it counts — a
    successor ticket and a clean-verdict tag — are cheap to produce, which is
    limit 1 of the detector itself and is not repaired by anything here.
  * It does not run on the merge gate.  See run_all.sh for why, at length.
  * It asserts WHICH ITEMS are named, never HOW MANY audits exist.  The store
    grows; a control pinned to `9 examined` would go red on the next audit that
    lands, for a non-reason, and a gate that goes red for a non-reason is how
    gates get turned off.  The 2026-08-12 counts are PRINTED for the record and
    are not asserted.

EXIT CODES, on this repository's standing rule that the exit code is not the
classifier: 0 every arm behaved, 1 an arm did not, 2 refused before reaching a
verdict (a missing binary, a store that would not copy, mtimes not preserved).
A traceback and a finding must never share an exit code, so every path here
prints its own VERDICT line and the runner reads that, not $?.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

# The three retro-links and the one verdict tag mg-a518 landed, as (item, the
# exact tag text added).  Each is removed from a COPY of the store and the audit
# it points at must then be reported.  If it is not, the tag was decorative.
FIX1 = [
    ("mg-2f44", "mg-07fd-followup", "mg-07fd"),
    ("mg-8d63", "mg-5cba-followup", "mg-5cba"),
    ("mg-b417", "mg-5cba-followup", "mg-5cba"),
]
FIX2 = ("mg-a0d6", "audit-verdict-pass", "mg-a0d6")

CHECK = "audit successors"


class Refused(Exception):
    """Raised when the control cannot reach a verdict at all."""


def store_root():
    return os.path.join(os.path.expanduser("~"), ".macguffin")


def pogo_bin():
    exe = shutil.which("pogo")
    if not exe:
        raise Refused("`pogo` is not on PATH — nothing to measure with")
    return exe


def doctor(mg_root, pogo_home=None):
    """Run `pogo doctor --check --json` and return the audit-successors row.

    A non-zero exit is NOT an error here: doctor exits 1 when any critical host
    check fails (pogod down, a plist adrift), and none of that is this control's
    subject.  What IS an error is a run that produced no parseable row, because
    then we have measured nothing and must not report it as clean.
    """
    env = dict(os.environ)
    env["MG_ROOT"] = mg_root
    if pogo_home:
        env["POGO_HOME"] = pogo_home
    else:
        env.pop("POGO_HOME", None)
    proc = subprocess.run(
        [pogo_bin(), "doctor", "--check", "--json"],
        capture_output=True, text=True, env=env, timeout=300,
    )
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise Refused(f"doctor --check --json emitted unparseable output: {exc}")
    for row in payload.get("checks", []):
        if row.get("name") == CHECK:
            return row
    raise Refused(
        f"doctor --check produced no {CHECK!r} row — the detector is not in this "
        "binary, so this control has measured nothing"
    )


def silent_ids(row):
    """The ids the row NAMES as silent, read out of the rendered detail.

    Read from the human detail rather than from a structured field because the
    detail is what a person acts on; a control that agreed with a JSON field
    while the printed sentence said something else would certify the wrong
    artifact.  `pass` renders no names at all, so an empty set is correct there.
    """
    if row.get("status") != "warn":
        return set()
    head = row.get("detail", "").split("Read each one")[0]
    return set(re.findall(r"\bmg-[0-9a-f]{4}\b", head))


def population(row):
    """(examined, answered_by_successor, clean_verdict, waiting, undated), or None."""
    m = re.search(
        r"(\d+) merged audit\(s\) examined: (\d+) answered by a successor, "
        r"(\d+) by a recorded clean verdict, (\d+) still inside the \S+ window, "
        r"(\d+) with no recorded completion time",
        row.get("detail", ""),
    )
    return tuple(int(g) for g in m.groups()) if m else None


def strip_tag(path, tag):
    """Remove one tag from a work item's frontmatter `tags:` list.

    Rewrites the list rather than string-replacing the tag text, so it cannot
    half-remove a tag that is a prefix of another one and cannot leave a stray
    comma behind.  Returns True only if the tag was actually there — an arm that
    mutated nothing must be reported as a broken arm, never as a passing one.
    """
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    for i, line in enumerate(lines):
        if not line.startswith("tags:"):
            continue
        inner = line[len("tags:"):].strip()
        if not (inner.startswith("[") and inner.endswith("]")):
            return False
        tags = [t.strip() for t in inner[1:-1].split(",") if t.strip()]
        if tag not in tags:
            return False
        tags.remove(tag)
        lines[i] = "tags: [" + ", ".join(tags) + "]"
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines))
        return True
    return False


def copy_store(src, dst):
    """Copy the store PRESERVING MTIMES, and refuse if they did not survive.

    THIS ASSERTION IS HERE BECAUSE THE CONTROL FAILED IT ON ITS FIRST RUN (D1 in
    the README).  The detector ages an audit's silence from its
    `<id>.result.json` MTIME.  A plain `cp -R` stamps every copied file with the
    time of the copy, so on the copied store every unanswered audit is `0
    seconds silent` and lands in WAITING instead of SILENT — and every mutation
    arm comes back `pass`.  That reads exactly like "the fixes are load-bearing
    and the store is healthy" and means "this control cannot fire".  A control
    whose failure mode is a green report is the defect this whole ticket is
    about, reproduced inside its own remedy, so the preservation is CHECKED here
    rather than remembered by whoever next edits this file.
    """
    shutil.copytree(src, dst, copy_function=shutil.copy2)
    probe = os.path.join("done", "mg-a0d6.result.json")
    a, b = os.path.join(src, probe), os.path.join(dst, probe)
    if not os.path.exists(a):
        raise Refused(f"{a} is missing — the store does not have the shape this control assumes")
    if abs(os.path.getmtime(a) - os.path.getmtime(b)) > 1:
        raise Refused(
            "mtimes were NOT preserved by the copy, so silence cannot age on it and "
            "every arm below would report `pass` for the wrong reason"
        )


def overlay(dirpath, audit_tags):
    """A pinned [audit_successor] section, so the arms test the STORE not the host config."""
    os.makedirs(dirpath, exist_ok=True)
    with open(os.path.join(dirpath, "config.toml"), "w", encoding="utf-8") as fh:
        fh.write(
            "[audit_successor]\n"
            f'repos = ["{os.path.expanduser("~")}/research/onethird_program"]\n'
            f"audit_tags = {json.dumps(audit_tags)}\n"
            'clean_verdict_tags = ["audit-clean", "audit-verdict-pass"]\n'
            'window = "4h"\n'
        )
    return dirpath


def main():
    failures = []
    print("mg-a518 — CONTROLS FOR THE WIDE ARMING OF THE AUDIT-SUCCESSOR DETECTOR")
    print("=" * 78)

    src = os.path.join(store_root(), "work")
    if not os.path.isdir(src):
        raise Refused(f"{src} does not exist — no store to measure")

    # ---------------------------------------------------------------- ARM A
    # Is the LIVE configuration actually widened?  Separate from every arm
    # below, which pins its own config: this one asks about the host, the rest
    # ask about the store.  Conflating them would let a green run mean either.
    print("\n[A] THE LIVE ARMING — does this host's config name the wide tag?")
    live = doctor(store_root())
    live_pop = population(live)
    print(f"    status : {live['status']}")
    print(f"    detail : {live['detail']}")
    if live_pop:
        print(f"    parsed : examined={live_pop[0]} answered={live_pop[1]} "
              f"clean={live_pop[2]} waiting={live_pop[3]} undated={live_pop[4]}")
    if not live_pop:
        failures.append("A: the live run reported no population at all — the detector is "
                        "unconfigured or unreadable, which is NOT a clean store")
    elif live_pop[0] <= 4:
        failures.append(
            f"A: the live config examined only {live_pop[0]} audits. mg-a882 measured that "
            "the narrow arming sees 4 of 9. This host looks NARROW again — the widening was "
            "reverted, or [audit_successor].audit_tags no longer names `audit`"
        )
    else:
        print(f"    VERDICT: live config is WIDE ({live_pop[0]} examined, > 4)")

    workdir = tempfile.mkdtemp(prefix="a518-controls-")
    try:
        root = os.path.join(workdir, "store")
        os.makedirs(root)
        copy_store(src, os.path.join(root, "work"))
        print(f"\n    store copied with mtimes intact -> {root}")
        ph = overlay(os.path.join(workdir, "cfg"), ["audit"])
        done = os.path.join(root, "work", "done")
        pristine = {}
        for item in [f[0] for f in FIX1] + [FIX2[0]]:
            with open(os.path.join(done, f"{item}.md"), encoding="utf-8") as fh:
                pristine[item] = fh.read()

        def restore():
            for name, text in pristine.items():
                with open(os.path.join(done, f"{name}.md"), "w", encoding="utf-8") as fh:
                    fh.write(text)

        def arm(label, mutations, expect_silent, why):
            restore()
            for item, tag in mutations:
                if not strip_tag(os.path.join(done, f"{item}.md"), tag):
                    failures.append(f"{label}: `{tag}` is not on {item} — the fix this arm "
                                    "mutates is NOT IN THE STORE")
                    return None
            row = doctor(root, ph)
            got = silent_ids(row)
            ok = got == set(expect_silent)
            print(f"\n[{label}] {why}")
            if mutations:
                print("    mutated: " + ", ".join(f"{i} -{t}" for i, t in mutations))
            else:
                print("    mutated: nothing")
            print(f"    status : {row['status']}")
            print(f"    silent : {sorted(got) or '(none)'}")
            print(f"    expect : {sorted(set(expect_silent)) or '(none)'}")
            pop = population(row)
            if pop:
                print(f"    parsed : examined={pop[0]} answered={pop[1]} clean={pop[2]} "
                      f"waiting={pop[3]} undated={pop[4]}")
            print(f"    VERDICT: {'as expected' if ok else 'NOT AS EXPECTED'}")
            if not ok:
                failures.append(f"{label}: silent set {sorted(got)} != {sorted(set(expect_silent))}")
            return row

        c0 = arm("C0", [], [],
                 "BASELINE — the store as mg-a518 leaves it must report nothing silent")

        arm("C1", [(FIX1[0][0], FIX1[0][1])], [FIX1[0][2]],
            "mg-2f44 loses its retro-link — mg-07fd must become visible again")

        arm("C2", [(FIX1[1][0], FIX1[1][1]), (FIX1[2][0], FIX1[2][1])], [FIX1[1][2]],
            "BOTH of mg-5cba's repairs lose theirs — mg-5cba must become visible")

        arm("C2b", [(FIX1[1][0], FIX1[1][1])], [],
            "only ONE of mg-5cba's two repairs loses its link — either alone must "
            "still answer, so this must stay GREEN.  Without this arm C2 would be "
            "satisfied by a detector that needs every successor rather than any")

        arm("C3", [(FIX2[0], FIX2[1])], [FIX2[2]],
            "mg-a0d6 loses its verdict tag — a PASSING audit with no successor must "
            "become visible, which is the false report FIX 2 exists to remove")

        c4 = arm("C4",
                 [(i, t) for i, t, _ in FIX1] + [(FIX2[0], FIX2[1])],
                 [FIX1[0][2], FIX1[1][2], FIX2[2]],
                 "EVERY fix reverted — this must reproduce mg-a882's pre-fix row: the "
                 "SAME THREE audits it measured as false reports on 2026-08-12")

        c5 = arm("C5", [], [],
                 "RESTORED — the mutations must leave nothing behind, so this must be "
                 "byte-identical to C0")

        if c0 and c5 and c0.get("detail") != c5.get("detail"):
            failures.append("C5: the restored store does not render identically to C0 — a "
                            "mutation leaked, so every arm between them is suspect")

        print("\n" + "=" * 78)
        print("WHAT C4 SHOWS, and it is the load-bearing arm.  mg-a882 measured 3 false")
        print("reports on 2026-08-12 and named them: mg-07fd, mg-5cba, mg-a0d6.  With")
        print("mg-a518's four tags removed the detector names exactly those three again,")
        print("so the green in C0 is the fixes doing work and NOT the detector going blind")
        print("a second time.  The counts printed above are the 2026-08-12 population and")
        print("are deliberately NOT asserted — the store grows, and a control pinned to a")
        print("population count goes red for a non-reason on the next audit that lands.")
        if c0 and population(c0):
            pop0 = population(c0)
            print(f"\n  RECORDED, not asserted — C0 population: examined={pop0[0]} "
                  f"answered={pop0[1]} clean_verdict={pop0[2]} silent=0")
        if c4 and population(c4):
            pop4 = population(c4)
            print(f"  RECORDED, not asserted — C4 population: examined={pop4[0]} "
                  f"answered={pop4[1]} clean_verdict={pop4[2]} silent=3")
    finally:
        shutil.rmtree(workdir, ignore_errors=True)

    print("\n" + "=" * 78)
    if failures:
        print(f"CONTROLS VERDICT: FIRED — {len(failures)} arm(s) did not behave")
        for f in failures:
            print(f"  * {f}")
        return 1
    print("CONTROLS VERDICT: CLEAN — every arm behaved, and every arm that was")
    print("supposed to make the detector speak did make it speak.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Refused as exc:
        print(f"\nCONTROLS VERDICT: REFUSED — {exc}")
        print("This is neither green nor red.  It reached no decision and must not be read")
        print("as either.")
        sys.exit(2)
