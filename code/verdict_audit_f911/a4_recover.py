#!/usr/bin/env python3
"""mg-f911 A4 -- brief item 3: RECOVER the eleven, do not count them.

    "Check each has an actual recovered verdict -- the finding, not the fact of
     its absence. A list of eleven ids with no content is the same failure
     re-expressed as a report."

The parent produced a 122-row backlog of ids and TICKET TITLES, and recovered the
CONTENT of exactly one verdict (mg-ec63, in D4.5). A ticket title is what the
filer wrote when filing; it is not what the worker found. So on the brief's own
standard the backlog is a count, not a recovery, 1 case excepted.

This file does the recovery. For each target item it goes to the repository --
where mg-bf3f correctly observed the verdicts were never lost, "only lost from
their reader" -- and extracts the worker's own account.

WHAT COUNTS AS A RECOVERED VERDICT, declared before running:

  * The full subject AND body of a commit this arc calls `evidence*` or
    `audit*`, which is where it puts a finished account, authored on the item's
    own branch. That is the worker's own words about what it found.
  * FAILING that, the fullest `instrument*`/`docs*` subject on the item.
  * A row that yields only a ticket title is NOT recovered and is reported as
    NOT RECOVERED. Reporting an absence as a recovery is the failure being
    audited, and this instrument must not commit it.

Writes RECOVERED_VERDICTS.md. Read-only with respect to git and mg.
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "verdict_delivery_bf3f"))
import lib_bf3f as L  # noqa: E402

# TWO REPOSITORIES, and the second one is a CORRECTION TO MY OWN FIRST RUN.
# E3 of my PREDICTIONS.md said I would get a different answer than the parent by
# using a different rule and score my own rule's error as a defect. It fired
# here, twice, and both are recorded rather than quietly fixed:
#
#   (i)  My first run searched only onethird_program. 14 of the 64 items I was
#        about to publish as "nothing to read" are filed against
#        one_third_width_three, a repo my search never entered. Their accounts
#        may be perfectly intact and I would have called them lost.
#   (ii) My first RANK table was a hand-written whitelist of commit types, and
#        this arc writes COMPOUND types -- `docs+repair`, `docs+audit`,
#        `control+repair`, `evidence+control`, `census+repair`, `STATE+docs`.
#        98 `docs+repair` and 98 `docs+audit` commits scored as "not a verdict"
#        because the exact string was not in my table. A hand list where the
#        population is open is the same defect this arc keeps filing against
#        others; mine lasted one run.
#
# The rule is COMPONENT-BASED now: split the type on `+` and ask whether any
# component is verdict-bearing. `predictions` alone is excluded BY DEFINITION --
# it is pre-registered before the work and cannot be the finding.
REPOS = [
    "/Users/daniel/.pogo/polecats/pf911",          # onethird_program (this worktree)
    "/Users/daniel/research/one_third_width_three",
]
MG = L.root(None)
FILER = "pm-onethird"

VERDICT_BEARING = {
    "evidence", "audit", "instrument", "docs", "repair", "control", "census",
    "probe", "harden", "fix", "state", "refute", "land", "measure",
}
PREFERENCE = ["evidence", "audit", "instrument", "control", "census", "repair",
              "docs", "probe", "state", "harden", "fix"]

# The items mg-bf3f's own body names. THE TICKET SAYS ELEVEN AND NAMES SEVEN:
# four that landed in one evening, then three "earlier", then "and others".
# That gap is a finding in itself and is reported rather than papered over by
# picking four more to round the list out.
NAMED_IN_TICKET = [
    ("mg-ec63", "named FIRST and by name: the unknown-unknowns runner-truncation finding"),
    ("mg-6e58", "one of the four that landed in a single evening"),
    ("mg-0120", "one of the four that landed in a single evening"),
    ("mg-5f7c", "one of the four that landed in a single evening"),
    ("mg-d53d", "named under 'earlier'"),
    ("mg-ba2a", "named under 'earlier'"),
    ("mg-1abe", "named under 'earlier'"),
]

TYPE = re.compile(r"^([a-z+]+):")


def commits_for(iid):
    """Every commit on either repo's main whose message names this item."""
    recs = []
    for repo in REPOS:
        p = subprocess.run(
            ["git", "-C", repo, "log", "main",
             "--format=%H%x00%cI%x00%s%x00%b%x01", f"--grep={iid}"],
            capture_output=True, text=True, timeout=180)
        for chunk in p.stdout.split("\x01"):
            chunk = chunk.strip("\n")
            if not chunk:
                continue
            parts = chunk.split("\x00")
            if len(parts) < 4:
                continue
            h, ts, subj, body = parts[0], parts[1], parts[2], parts[3]
            m = TYPE.match(subj)
            recs.append({"h": h, "ts": ts, "subj": subj, "body": body,
                         "type": m.group(1) if m else "?",
                         "repo": os.path.basename(repo)})
    return recs


def components(rec):
    return [c.lower() for c in rec["type"].split("+")]


def is_verdict_bearing(rec):
    """Component-based, not a whitelist of whole strings. A commit counts if any
    component of its type is verdict-bearing. `predictions` alone never counts:
    it is committed BEFORE the work by construction and cannot be the finding."""
    cs = components(rec)
    if cs == ["predictions"] or cs == ["?"]:
        return False
    return any(c in VERDICT_BEARING for c in cs)


def rank(rec):
    cs = components(rec)
    for i, pref in enumerate(PREFERENCE):
        if pref in cs:
            return i
    return len(PREFERENCE)


def best(recs, iid):
    """The commit most likely to BE the verdict, by the declared rule.

    DEFECT-3 OF THIS INSTRUMENT, found by reading my own first output. My
    docstring said "authored on the item's own branch" and the code only grepped
    for a MENTION, so for mg-ec63 it recovered commit e11b63e -- which is
    mg-18dc's INDEPENDENT AUDIT *of* mg-ec63, not mg-ec63's own account. An
    auditor's verdict about an item is not that item's verdict; recovering the
    wrong one and calling it recovered is precisely the substitution this brief
    is about ("the finding, not the fact of its absence").

    This arc stamps authorship in a trailing `(mg-xxxx)`. So OWN commits are
    preferred absolutely, and a fallback to a mention-only commit is marked
    `own=False` on the row and labelled in the output rather than passed off.
    """
    own = [r for r in recs if is_verdict_bearing(r) and r["subj"].rstrip().endswith(f"({iid})")]
    if own:
        r = sorted(own, key=lambda r: (rank(r), -len(r["subj"])))[0]
        r["own"] = True
        return r
    cand = [r for r in recs if is_verdict_bearing(r)]
    if not cand:
        return None
    r = sorted(cand, key=lambda r: (rank(r), -len(r["subj"])))[0]
    r["own"] = False
    return r


def successor_tickets(iid):
    """pm-onethird's own follow-up items, which sometimes carry a recovered
    verdict in their TITLE -- e.g. mg-d075 'mg-19ec verdict (RECOVERED from
    commit messages)'. Credit where it exists; it is recovery, done by hand."""
    items = L.load_items(MG)
    hits = []
    for i, info in items.items():
        t = info["title"]
        if iid in t and i != iid:
            hits.append((i, t))
    return hits


def main():
    res = L.scan(mg=MG, filer=FILER)
    byid = {r["id"]: r for r in res["rows"]}

    lines = []
    W = lines.append
    W("# RECOVERED VERDICTS — mg-f911")
    W("")
    W("Brief item 3: *the eleven must be RECOVERED, not counted.*")
    W("")
    W("mg-bf3f delivered a 122-row backlog of item ids and **ticket titles**, plus")
    W("the recovered content of exactly one verdict (mg-ec63). A ticket title is")
    W("what the filer wrote when filing. It is not what the worker found. This file")
    W("recovers the workers' own accounts for the items mg-bf3f's ticket names.")
    W("")
    W("**Recovery rule, declared before running:** the finished account lives in the")
    W("`evidence*` / `audit*` commit on the item's branch. Its subject and body are")
    W("reproduced verbatim below. Where no such commit exists the row says **NOT")
    W("RECOVERED** — reporting an absence as a recovery is the defect under audit.")
    W("")

    print("=" * 78)
    print("A4.1  THE ELEVEN -- how many does the ticket actually name?")
    print("=" * 78)
    print(f"  mg-bf3f says ELEVEN and names {len(NAMED_IN_TICKET)}:")
    for iid, why in NAMED_IN_TICKET:
        print(f"    {iid}  {why}")
    print(f"  The remaining {11 - len(NAMED_IN_TICKET)} are 'and others' and are NOT")
    print("  enumerated anywhere in the ticket. THE ELEVEN CANNOT BE LISTED FROM THE")
    print("  TICKET. Any instrument that prints eleven ids has chosen four of them,")
    print("  and this one says so instead of choosing.")

    W("## The set itself is under-specified")
    W("")
    W(f"mg-bf3f says **eleven** and names **{len(NAMED_IN_TICKET)}**: "
      + ", ".join(f"`{i}`" for i, _ in NAMED_IN_TICKET) + ".")
    W("The remaining four are *\"and others\"* and are enumerated nowhere. So \"the")
    W("eleven\" is not a recoverable set — it is seven items plus a number. Any list")
    W("of exactly eleven ids has silently chosen four. This one does not choose;")
    W("it recovers the seven that are named, and then the rest of the live backlog")
    W("by the same rule.")
    W("")

    print()
    print("=" * 78)
    print("A4.2  RECOVERY, item by item")
    print("=" * 78)
    recovered = 0
    for iid, why in NAMED_IN_TICKET:
        recs = commits_for(iid)
        b = best(recs, iid)
        row = byid.get(iid)
        status = (row or {}).get("status", "NOT IN THE DETECTOR'S POPULATION")
        succ = successor_tickets(iid)
        ok = b is not None
        recovered += 1 if ok else 0
        own = bool(b and b.get("own"))
        print(f"  {iid}  detector={status:12} commits={len(recs):3} "
              f"best={b['type'] if b else '-':16} "
              f"{'OWN ' if own else ('MENTION-ONLY ' if ok else '')}"
              f"{'RECOVERED' if ok else 'NOT RECOVERED'}")

        W(f"## `{iid}` — {'RECOVERED' if ok else 'NOT RECOVERED'}")
        W("")
        W(f"- ticket's reason for naming it: {why}")
        W(f"- detector status today: **{status}**")
        W(f"- commits on `main` naming it: {len(recs)}"
          + (f" (types: {', '.join(sorted({r['type'] for r in recs}))})" if recs else ""))
        if succ:
            W("- pm-onethird follow-up items carrying it:")
            for i, t in succ:
                W(f"  - `{i}` — {t}")
        W("")
        if ok:
            if own:
                W(f"### The worker's own account — commit `{b['h'][:7]}` "
                  f"({b['ts']}, type `{b['type']}`, repo `{b['repo']}`)")
            else:
                W(f"### ⚠ MENTION-ONLY — commit `{b['h'][:7]}` "
                  f"({b['ts']}, type `{b['type']}`, repo `{b['repo']}`)")
                W("")
                W("This commit **names** the item but is not stamped `(" + iid + ")`, so it")
                W("was authored on somebody else's branch. It is somebody's account *of*")
                W("this item, not this item's own verdict. Recorded as the best available")
                W("and explicitly NOT presented as the worker's own words.")
            W("")
            W("> " + b["subj"].replace("\n", "\n> "))
            W("")
            if b["body"].strip():
                W("Body of that commit:")
                W("")
                W("```")
                W(b["body"].strip()[:6000])
                W("```")
                W("")
        else:
            W("**NOT RECOVERED.** No `evidence*`/`audit*`/`instrument*`/`docs*` commit on")
            W("`main` names this item. Its verdict is not in the repository either, so it")
            W("is not merely unread — on this evidence it was never written down anywhere")
            W("this audit can reach.")
            W("")
        W("")

    print(f"  -> RECOVERED {recovered} of {len(NAMED_IN_TICKET)} named items")

    print()
    print("=" * 78)
    print("A4.3  THE REST OF THE BACKLOG, BY THE SAME RULE")
    print("=" * 78)
    drops = [r for r in res["rows"] if r["status"] == "DROPPED"]
    print(f"  dropped rows for {FILER} today: {len(drops)}")
    stats = {"recoverable": 0, "not": 0}
    table = []
    for r in drops:
        b = best(commits_for(r["id"]), r["id"])
        ok = b is not None
        stats["recoverable" if ok else "not"] += 1
        table.append((r["landed"], r["id"], b["type"] if b else "-",
                      b["h"][:7] if b else "-", ok, r["title"][:60]))
    print(f"  with a recoverable account in the repo : {stats['recoverable']}")
    print(f"  with NONE                              : {stats['not']}")
    print()
    print("  THE SECOND NUMBER IS THE ONE THAT MATTERS. Those verdicts are not")
    print("  'unread' -- there is nothing to read. mg-bf3f's consoling sentence,")
    print("  'it was never lost from the repository, only from its reader', is TRUE")
    print(f"  OF {stats['recoverable']} OF THE {len(drops)} AND FALSE OF THE OTHER {stats['not']}.")

    W("## The rest of the backlog, by the same rule")
    W("")
    W(f"Of the **{len(drops)}** dropped rows for `{FILER}` on this store today,")
    W(f"**{stats['recoverable']}** have a recoverable account in the repository and")
    W(f"**{stats['not']}** have none at all.")
    W("")
    W("mg-bf3f's closing consolation — *\"it was never lost from the repository, only")
    W(f"from its reader\"* — is true of {stats['recoverable']} of them and **false of the other")
    W(f"{stats['not']}**. For those there is nothing to read.")
    W("")
    W("| landed | item | best commit | type | recovered | ticket title |")
    W("|---|---|---|---|---|---|")
    for landed, iid, typ, h, ok, title in table:
        W(f"| {landed} | `{iid}` | `{h}` | {typ} | {'yes' if ok else '**NO**'} | {title} |")
    W("")

    out = os.path.join(HERE, "RECOVERED_VERDICTS.md")
    open(out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print()
    print(f"  wrote {out} ({len(lines)} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
