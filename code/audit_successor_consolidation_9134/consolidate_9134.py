#!/usr/bin/env python3
"""mg-9134 — the audit-successor detector after the clean-verdict tag was CONSOLIDATED.

WHAT HAPPENED AND WHY THIS EXISTS.  mg-a518 found that two names existed for one
concept: `audit-clean` (mg-7ff8's, armed, printed in `pogo doctor --check`'s own
remedy text, published in pogo's docs/CONFIGURATION.md) and `audit-verdict-pass`
(mg-a882's, introduced without knowing the first existed).  It configured BOTH
and left the choice to a decider, which was right.  pm-onethird decided in
mg-9134: `audit-clean` survives.

A RENAME IS THE ONE EDIT THIS PARTICULAR DETECTOR CANNOT SURVIVE QUIETLY.  Its
failure mode is SILENCE, and its clean-verdict half is a string match between a
tag on an item and a list in a config file.  Break the match in either direction
and the audit stops being answered — which surfaces as one number in a
population line moving by one, on a line most people read as "green".  So the
question this file exists to answer is not "is it still green" (it is) but:

    IS IT GREEN BECAUSE THE SURVIVING NAME IS DOING THE WORK,
    OR GREEN BECAUSE THE DETECTOR STOPPED LOOKING?

Every arm below answers that by MUTATING A COPY OF THE STORE, OR THE CONFIG, and
requiring the report to move.  Two of them (N1, N2) are the two halves of the
rename hazard itself, run as experiments rather than argued in prose.

ARM D IS THE ONE TO READ IF YOU READ ONE.  pa518 disclosed that its own first
control copied the store with `cp -R`, which does not preserve mtimes; the
detector ages an audit's silence from its `result.json` mtime, so on that copy
every unanswered audit was `0 seconds silent`, landed in WAITING instead of
SILENT, and ALL FOUR MUTATION ARMS CAME BACK PASS — a control that could not
fire, reporting green, inside the remedy for a detector that could not fire and
reported green.  My ticket said to assume the same class of error is available to
me.  It is: arm D REPRODUCES IT ON PURPOSE, so that the assertion in copy_store()
is a measured refusal and not a remembered one.

EXIT CODES, on this repository's standing rule that the exit code is not the
classifier: 0 every arm behaved, 1 an arm did not, 2 refused before reaching a
verdict (no binary, a store that would not copy, mtimes not preserved).  A
traceback and a finding must never share an exit code, so every path prints its
own VERDICT line and the runner reads that, not $?.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

# The four tags mg-a518 landed, in the names they carry AFTER mg-9134's
# consolidation.  FIX2's tag is the whole subject of this ticket: it was
# `audit-verdict-pass` when mg-a518 wrote it and is `audit-clean` now.
FIX1 = [
    ("mg-2f44", "mg-07fd-followup", "mg-07fd"),
    ("mg-8d63", "mg-5cba-followup", "mg-5cba"),
    ("mg-b417", "mg-5cba-followup", "mg-5cba"),
]
FIX2 = ("mg-a0d6", "audit-clean", "mg-a0d6")

SURVIVING = "audit-clean"
RETIRED = "audit-verdict-pass"

CHECK = "audit successors"
REPO = os.path.join(os.path.expanduser("~"), "research", "onethird_program")


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
    check fails, and none of that is this control's subject.  What IS an error is
    a run that produced no parseable row, because then nothing was measured and
    it must not be reported as clean.
    """
    env = dict(os.environ)
    env["MG_ROOT"] = mg_root
    if pogo_home:
        env["POGO_HOME"] = pogo_home
    else:
        env.pop("POGO_HOME", None)
    proc = subprocess.run(
        [pogo_bin(), "doctor", "--check", "--json"],
        capture_output=True, text=True, env=env, timeout=600,
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
    """The ids the row NAMES as silent, read out of the rendered detail."""
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


def advertised_tags(row):
    """The clean-verdict tag list the run ACTUALLY USED, read out of its own remedy.

    THIS ONLY WORKS ON A `warn`.  `cleanVerdictAdvice` is called from the warn
    branch of auditSuccessorLine and from nowhere else, so a GREEN run prints
    counts and no tag list at all — there is no way to read a passing run for
    which names were in force.  That asymmetry is a finding of this ticket and is
    stated in the README rather than worked around here: the arms that need to
    verify the tag list are the arms that go red.
    """
    m = re.search(r"by tagging the audit ([^.]*?)\. This is a DETECTOR", row.get("detail", ""))
    if not m:
        return None
    body = m.group(1).strip()
    if body.startswith("(no clean_verdict_tags"):
        return []
    return sorted(re.findall(r"`([^`]+)`", body))


def frontmatter(path):
    """The frontmatter block's lines, or [] if the file has none.

    Bounded to the block between the leading `---` and the next `---` because
    the store's bodies routinely quote `tags:` in prose — this item's own body
    does — and a whole-file scan for a key is how prose becomes metadata.
    """
    try:
        with open(path, encoding="utf-8") as fh:
            lines = fh.read().split("\n")
    except (OSError, UnicodeDecodeError):
        return []
    if not lines or lines[0].strip() != "---":
        return []
    out = []
    for line in lines[1:]:
        if line.strip() == "---":
            return out
        out.append(line)
    return []


def read_tags(path):
    """The item's tags, or None if it declares none.

    None means "this item has no `tags:` key", which is the ordinary state of
    hundreds of older archived items and is NOT a parse failure — conflating the
    two is a defect this file committed once and now separates by name (see
    tags_unreadable).
    """
    for line in frontmatter(path):
        if line.startswith("tags:"):
            inner = line[len("tags:"):].strip()
            if inner.startswith("[") and inner.endswith("]"):
                return [t.strip() for t in inner[1:-1].split(",") if t.strip()]
            return None
    return None


def tags_unreadable(path):
    """True only when a `tags:` KEY EXISTS in the frontmatter and could not be read.

    This is the condition that would undermine an absence claim.  A file with no
    `tags:` key carries no tags and cannot carry the retired name; a file with an
    unparseable one might.
    """
    for line in frontmatter(path):
        if line.startswith("tags:"):
            inner = line[len("tags:"):].strip()
            return not (inner.startswith("[") and inner.endswith("]"))
    return False


def write_tags(path, tags):
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    for i, line in enumerate(lines):
        if line.startswith("tags:"):
            lines[i] = "tags: [" + ", ".join(tags) + "]"
            with open(path, "w", encoding="utf-8") as fh:
                fh.write("\n".join(lines))
            return True
    return False


def strip_tag(path, tag):
    """Remove one tag from a work item's frontmatter, rewriting the LIST.

    Returns False if the tag was not there — an arm that mutated nothing must be
    reported broken, never passing.
    """
    tags = read_tags(path)
    if tags is None or tag not in tags:
        return False
    tags.remove(tag)
    return write_tags(path, tags)


def add_tag(path, tag):
    tags = read_tags(path)
    if tags is None or tag in tags:
        return False
    tags.append(tag)
    return write_tags(path, tags)


def copy_store(src, dst, preserve=True):
    """Copy the store, PRESERVING MTIMES unless a caller deliberately asks not to.

    preserve=False exists for ONE caller (arm D) whose entire purpose is to
    demonstrate what an unpreserved copy does to every arm above it.  Every other
    caller gets the assertion.
    """
    shutil.copytree(src, dst, copy_function=shutil.copy2 if preserve else shutil.copy)
    probe = os.path.join("done", "mg-a0d6.result.json")
    a, b = os.path.join(src, probe), os.path.join(dst, probe)
    if not os.path.exists(a):
        raise Refused(f"{a} is missing — the store does not have the shape this control assumes")
    drift = abs(os.path.getmtime(a) - os.path.getmtime(b))
    if preserve and drift > 1:
        raise Refused(
            "mtimes were NOT preserved by the copy, so silence cannot age on it and "
            "every arm below would report `pass` for the wrong reason"
        )
    return drift


def overlay(dirpath, audit_tags, clean_tags):
    """A pinned [audit_successor] section, so the arms test what they say they test."""
    os.makedirs(dirpath, exist_ok=True)
    with open(os.path.join(dirpath, "config.toml"), "w", encoding="utf-8") as fh:
        fh.write(
            "[audit_successor]\n"
            f'repos = ["{REPO}"]\n'
            f"audit_tags = {json.dumps(audit_tags)}\n"
            f"clean_verdict_tags = {json.dumps(clean_tags)}\n"
            'window = "4h"\n'
        )
    return dirpath


def main():
    failures = []
    print("mg-9134 — THE CLEAN-VERDICT TAG IS CONSOLIDATED ONTO `audit-clean`")
    print("=" * 78)

    src = os.path.join(store_root(), "work")
    if not os.path.isdir(src):
        raise Refused(f"{src} does not exist — no store to measure")

    live_item = os.path.join(src, "done", "mg-a0d6.md")
    live_tags = read_tags(live_item)
    print("\n[S] THE STORE, READ RATHER THAN ASSUMED — mg-9134 steps 1..3")
    print(f"    mg-a0d6 tags : {live_tags}")
    if live_tags is None or SURVIVING not in live_tags:
        failures.append(f"S: mg-a0d6 does not carry `{SURVIVING}` — step 1 of the ticket is "
                        "NOT satisfied and nothing below should be read as a consolidation")
    if live_tags and RETIRED in live_tags:
        failures.append(f"S: mg-a0d6 still carries `{RETIRED}` — step 2 did not land")

    # STEP 3, mechanically, over EVERY item file in EVERY status and EVERY repo.
    # `mg list` is not used: the point of this sweep is to find a carrier nobody
    # knew about, and a listing that filters is the wrong instrument for that.
    # TWO ROUTES, BECAUSE ONE OF THEM IS A PARSER AND THE CLAIM IS AN ABSENCE.
    # The frontmatter route is what the detector itself effectively does; the raw
    # route is a dumb substring sweep that cannot be defeated by a tags: line in a
    # shape read_tags() does not recognise.  If a file appears in `raw` and not in
    # `carriers`, that gap is either a body mention (harmless, the detector matches
    # tags) or a parser hole (not harmless), and it is PRINTED either way rather
    # than being absorbed by whichever route ran second.
    carriers = {SURVIVING: [], RETIRED: []}
    raw = {SURVIVING: [], RETIRED: []}
    scanned = 0
    unreadable = []
    untagged = 0
    for dirpath, _dirs, files in os.walk(src):
        for name in files:
            if ".md" not in name:
                continue
            scanned += 1
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, src)
            tags = read_tags(path)
            if tags is None:
                untagged += 1
                tags = []
            if tags_unreadable(path):
                unreadable.append(rel)
            for tag in (SURVIVING, RETIRED):
                if tag in tags:
                    carriers[tag].append(rel)
            try:
                with open(path, encoding="utf-8", errors="replace") as fh:
                    text = fh.read()
            except OSError:
                continue
            for tag in (SURVIVING, RETIRED):
                if tag in text:
                    raw[tag].append(rel)
    print(f"    item files scanned : {scanned} (every status, every repo, incl. archive/ and shelved/)")
    print(f"    carry `{SURVIVING}`      : {carriers[SURVIVING] or '(none)'}")
    print(f"    carry `{RETIRED}` : {carriers[RETIRED] or '(none)'}")
    print(f"    MENTION `{RETIRED}` anywhere in their text, tag or prose:")
    for rel in raw[RETIRED]:
        where = "TAG" if rel in carriers[RETIRED] else "prose only — the detector matches tags, not bodies"
        print(f"      {rel}  [{where}]")
    print(f"    declare no `tags:` key at all : {untagged} (older archived items and .bodybak/ "
          "body backups; an item with no tags cannot carry the retired one)")
    print(f"    have a `tags:` key that could NOT be read : {len(unreadable)}")
    if unreadable:
        failures.append(
            f"S: {len(unreadable)} file(s) have a `tags:` key this sweep could not parse, so the "
            f"absence claimed above rests on a parser that could not read them: {unreadable[:5]}")
    if carriers[RETIRED]:
        failures.append(
            f"S: {len(carriers[RETIRED])} item(s) still carry `{RETIRED}` while the config no "
            "longer names it — those audits are now SILENTLY unanswered, which is the exact "
            "failure the ticket's ordering exists to prevent")

    workdir = tempfile.mkdtemp(prefix="mg9134-")
    try:
        # ------------------------------------------------------------ the copy
        root = os.path.join(workdir, "store")
        os.makedirs(root)
        drift = copy_store(src, os.path.join(root, "work"))
        print(f"\n    store copied with mtimes intact (drift {drift:.3f}s) -> {root}")
        done = os.path.join(root, "work", "done")
        pristine = {}
        for item in sorted({f[0] for f in FIX1} | {FIX2[0]}):
            with open(os.path.join(done, f"{item}.md"), encoding="utf-8") as fh:
                pristine[item] = fh.read()

        def restore():
            for name, text in pristine.items():
                with open(os.path.join(done, f"{name}.md"), "w", encoding="utf-8") as fh:
                    fh.write(text)

        def arm(label, why, audit_tags, clean_tags, mutations=(), adds=(),
                expect_silent=(), expect_tags=None):
            """One measurement.  `mutations` strip tags, `adds` add them.

            Every arm restores the four items first, so an arm's result depends
            on its own mutation and not on the one before it.
            """
            restore()
            for item, tag in mutations:
                if not strip_tag(os.path.join(done, f"{item}.md"), tag):
                    failures.append(f"{label}: `{tag}` is not on {item} — the state this arm "
                                    "mutates is NOT IN THE STORE, so the arm measured nothing")
                    return None
            for item, tag in adds:
                if not add_tag(os.path.join(done, f"{item}.md"), tag):
                    failures.append(f"{label}: could not add `{tag}` to {item}")
                    return None
            cfg = overlay(os.path.join(workdir, f"cfg-{label}"), audit_tags, clean_tags)
            row = doctor(root, cfg)
            got = silent_ids(row)
            pop = population(row)
            tags_used = advertised_tags(row)
            print(f"\n[{label}] {why}")
            print(f"    audit_tags        : {audit_tags}")
            print(f"    clean_verdict_tags: {clean_tags}")
            if mutations or adds:
                bits = [f"{i} -{t}" for i, t in mutations] + [f"{i} +{t}" for i, t in adds]
                print("    mutated           : " + ", ".join(bits))
            else:
                print("    mutated           : nothing")
            print(f"    status            : {row['status']}")
            print(f"    silent            : {sorted(got) or '(none)'}")
            print(f"    expect            : {sorted(set(expect_silent)) or '(none)'}")
            if pop:
                print(f"    population        : examined={pop[0]} answered_by_successor={pop[1]} "
                      f"clean_verdict={pop[2]} waiting={pop[3]} undated={pop[4]}")
            print(f"    tags in the remedy: {tags_used if tags_used is not None else '(none printed — this run is GREEN)'}")
            ok = got == set(expect_silent)
            if expect_tags is not None:
                if tags_used != sorted(expect_tags):
                    ok = False
                    print(f"    TAG LIST MISMATCH : the run used {tags_used}, expected {sorted(expect_tags)}")
            print(f"    VERDICT           : {'as expected' if ok else 'NOT AS EXPECTED'}")
            if not ok and scored:
                failures.append(f"{label}: silent {sorted(got)} != {sorted(set(expect_silent))}"
                                + (f", tags {tags_used} != {sorted(expect_tags)}" if expect_tags is not None else ""))
            return row

        # ------------------------------------------------- mg-a518's TABLE, re-run
        print("\n" + "-" * 78)
        print("mg-a518's THREE-ROW TABLE, RE-RUN AFTER THE CONSOLIDATION (ticket step 5).")
        print("Only [audit_successor] varies; the store is the live one, copied with mtimes.")
        print("-" * 78)

        rowA = arm("R1", "ROW 1 — `[\"independent-audit\"]`, the arming mg-7ff8 shipped",
                   ["independent-audit"], [SURVIVING], expect_silent=[])

        rowB = arm("R2", "ROW 2 — `[\"audit\"]` BEFORE mg-a518's four tags: the pre-fix store",
                   ["audit"], [SURVIVING],
                   mutations=[(i, t) for i, t, _ in FIX1] + [(FIX2[0], FIX2[1])],
                   expect_silent=[FIX1[0][2], FIX1[1][2], FIX2[2]],
                   expect_tags=[SURVIVING])

        rowC = arm("R3", "ROW 3 — `[\"audit\"]` AS ARMED NOW, with the consolidated tag list",
                   ["audit"], [SURVIVING], expect_silent=[])

        # ------------------------------------------- the rename's two failure modes
        print("\n" + "-" * 78)
        print("THE RENAME HAZARD, RUN AS TWO EXPERIMENTS RATHER THAN ARGUED IN PROSE.")
        print("Both halves of a tag rename break the same string match, in opposite")
        print("directions, and BOTH surface as one number moving in a line people read")
        print("as green.  This is why the ticket fixed an ORDER and not just an outcome.")
        print("-" * 78)

        arm("N1", "THE TRAP THE ORDER AVOIDS — config consolidated onto `audit-clean` while "
                  "the item still carries only the RETIRED name.  This is the state that "
                  "would exist if step 4 had run before step 2, and `answered` would have "
                  "dropped from 9 to 8 exactly as the ticket predicts",
            ["audit"], [SURVIVING],
            mutations=[(FIX2[0], SURVIVING)], adds=[(FIX2[0], RETIRED)],
            expect_silent=[FIX2[2]], expect_tags=[SURVIVING])

        arm("N2", "THE SAME BREAK IN THE OTHER DIRECTION — item on the surviving name, config "
                  "still on the retired one.  Proves the two names are NOT interchangeable to "
                  "the detector: the collision mg-a518 found was a live hazard, not cosmetics",
            ["audit"], [RETIRED], expect_silent=[FIX2[2]], expect_tags=[RETIRED])

        arm("N3", "THE SURVIVING NAME IS LOAD-BEARING — strip `audit-clean` and mg-a0d6 must "
                  "become visible again.  Without this, R3's green is equally explained by a "
                  "detector that has stopped looking at mg-a0d6 altogether",
            ["audit"], [SURVIVING], mutations=[(FIX2[0], SURVIVING)],
            expect_silent=[FIX2[2]], expect_tags=[SURVIVING])

        arm("N4", "NO CLEAN TAGS CONFIGURED AT ALL — the remedy must offer no tag rather than "
                  "name one that would do nothing, and mg-a0d6 must be reported",
            ["audit"], [], expect_silent=[FIX2[2]], expect_tags=[])

        # --------------------------------------------------------------- arm D
        print("\n" + "-" * 78)
        print("ARM D — MY OWN CONTROL'S FAILURE MODE, REPRODUCED ON PURPOSE.")
        print("-" * 78)
        droot = os.path.join(workdir, "unpreserved")
        os.makedirs(droot)
        ddrift = copy_store(src, os.path.join(droot, "work"), preserve=False)
        ddone = os.path.join(droot, "work", "done")
        print(f"\n    store copied WITHOUT preserving mtimes — result.json drift {ddrift:.0f}s")
        strip_tag(os.path.join(ddone, f"{FIX2[0]}.md"), SURVIVING)
        cfg = overlay(os.path.join(workdir, "cfg-D"), ["audit"], [SURVIVING])
        rowD = doctor(droot, cfg)
        dsilent = silent_ids(rowD)
        dpop = population(rowD)
        print(f"\n[D] the N3 mutation, run on a store whose mtimes were destroyed by the copy")
        print(f"    status     : {rowD['status']}")
        print(f"    silent     : {sorted(dsilent) or '(none)'}")
        if dpop:
            print(f"    population : examined={dpop[0]} answered_by_successor={dpop[1]} "
                  f"clean_verdict={dpop[2]} waiting={dpop[3]} undated={dpop[4]}")
        if dsilent:
            print("    VERDICT    : the demonstration DID NOT REPRODUCE — this copy still")
            print("                 aged silence, so the mtime hazard is not what pa518 says")
            print("                 it is on this host, or shutil.copy preserved them anyway.")
            failures.append("D: the unpreserved-mtime copy still fired; the demonstration this "
                            "arm exists to give did not happen and copy_store()'s assertion is "
                            "therefore UNMEASURED here")
        else:
            print("    VERDICT    : REPRODUCED — the identical mutation that fires in N3 is")
            print("                 SILENT here.  Every audit reads as 0s silent and lands in")
            print("                 `waiting`, so a control built on this copy reports a clean")
            print("                 store while being unable to fire at all.  copy_store()'s")
            print("                 refusal is what stands between this file and that result,")
            print("                 and it is now MEASURED rather than remembered.")

        # ------------------------------------------------------------- the table
        print("\n" + "=" * 78)
        print("THE TABLE (ticket step 5).  Counts are RECORDED; what is ASSERTED is which")
        print("items are named, because the store grows and a control pinned to a population")
        print("goes red for a non-reason on the next audit that lands.")
        print()
        print("  audit_tags                          examined  answered  reported  false")
        for label, row, note in (("[\"independent-audit\"]  (mg-7ff8) ", rowA, "—"),
                                 ("[\"audit\"]  before mg-a518's fixes ", rowB, "2 of 3"),
                                 ("[\"audit\"]  AS ARMED NOW (mg-9134) ", rowC, "0")):
            pop = population(row) if row else None
            if not pop:
                print(f"  {label}   (no population parsed)")
                continue
            answered = pop[1] + pop[2]
            reported = len(silent_ids(row))
            print(f"  {label}  {pop[0]:>5}   {answered:>7}   {reported:>7}   {note:>6}"
                  f"     (successor {pop[1]} + clean verdict {pop[2]})")
        print()
        if rowC:
            popC = population(rowC)
            if popC and popC[2] < 1:
                failures.append(
                    "R3: `answered by a recorded clean verdict` is 0.  mg-a0d6 fell through the "
                    "rename — restore `audit-verdict-pass` to clean_verdict_tags and report")
            if popC and popC[1] + popC[2] != popC[0]:
                failures.append(
                    f"R3: {popC[0]} examined but only {popC[1] + popC[2]} answered — the "
                    "consolidation did not preserve mg-a518's 9/9/0 reading")
    finally:
        shutil.rmtree(workdir, ignore_errors=True)

    print("=" * 78)
    if failures:
        print(f"CONSOLIDATION VERDICT: FIRED — {len(failures)} check(s) did not behave")
        for f in failures:
            print(f"  * {f}")
        return 1
    print("CONSOLIDATION VERDICT: CLEAN — `audit-clean` is the only configured name, it is")
    print("the only name any item carries, it is load-bearing (N3), the retired name is")
    print("recognised by nothing (N2), and the ordering the ticket fixed is the difference")
    print("between this and N1.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Refused as exc:
        print(f"\nCONSOLIDATION VERDICT: REFUSED — {exc}")
        print("This is neither green nor red.  It reached no decision and must not be read")
        print("as either.")
        sys.exit(2)
