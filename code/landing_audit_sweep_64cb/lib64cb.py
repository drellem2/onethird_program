"""mg-64cb — shared reader for the landing/audit concurrency sweep.

WHAT THIS MEASURES, AND WHAT IT CANNOT

The ticket's question is: how many landings in this arc carried figures from a parent
document that was under audit? Three things have to be pinned down to answer it, and
each one is a choice this file makes explicitly rather than by accident:

  LANDING   Measured from GIT, not from the title: an item whose merge commit modifies a
            canonical document (STATE.md, docs/**, README.md). The title-based reading
            ("LAND" appears in the title) finds 45 items and MISSES every landing that
            did not announce itself, so it is computed too, as a cross-check, and the two
            are reported side by side. The git reading is deliberately WIDE: it counts a
            document-AUTHORING ticket as a landing, which is filed as E1 and is why the
            adjudication in s3 is per-case rather than a count.

  AUDIT     Strict: the `independent-audit` tag, or a title beginning "INDEPENDENT AUDIT".
            The bare `audit` tag does NOT qualify and the reason is exhibited in s0:
            mg-1319 and mg-a806 are tagged `audit` and are LANDINGS of an audit's
            consequences. A classifier keyed on `audit` reports a landing as its own
            auditor and scores the collision against itself.

  INTERVAL  TWO of them, because they answer different questions and disagree:
              wall  = [work.claim, work.done]  — spawn to merge. Includes merge-queue
                      time, so an overlap here may be a QUEUE overlap and not a READING
                      overlap (E3).
              write = [first commit author date, last commit author date] over the
                      commits naming the item. This is when the polecat actually wrote,
                      and it survives the refinery's rebase because rebase preserves
                      author dates.
            Every collision is bucketed under BOTH and both are printed. A case that is
            CONCURRENT on wall and not on write is a weaker finding and must not be
            reported as the same thing.

REFUSALS. Functions here return an explicit REFUSED sentinel rather than a default when
their input is missing. A sweep whose missing timestamps quietly become "no overlap" is a
sweep that reports the arc as safer than it is.
"""

import collections
import glob
import json
import os
import re
import subprocess

SELF_DIR = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(SELF_DIR, "..", ".."))
STORE = os.path.expanduser("~/.macguffin/work")
EVENTS = os.path.expanduser("~/.macguffin/events.jsonl")

REFUSED = "REFUSED"

CANONICAL_EXACT = ("STATE.md", "README.md")
CANONICAL_PREFIX = ("docs/",)


# ---------------------------------------------------------------- work items

def parse_item(path):
    """Parse one mg item file. Returns None if it has no frontmatter."""
    txt = open(path, encoding="utf-8", errors="replace").read()
    m = re.match(r"---\n(.*?)\n---\n(.*)", txt, re.S)
    if not m:
        return None
    fm, body = m.group(1), m.group(2)
    d = {}
    for line in fm.split("\n"):
        if ": " in line:
            k, v = line.split(": ", 1)
            d[k.strip()] = v.strip()
    iid = d.get("id") or os.path.basename(path)[:-3]
    title = next((l[2:].strip() for l in body.split("\n") if l.startswith("# ")), "")
    return dict(id=iid, created=d.get("created", ""), tags=d.get("tags", ""),
                depends=d.get("depends", "[]"), repo=d.get("repo", ""),
                assignee=d.get("assignee", ""), title=title, body=body,
                bucket=os.path.basename(os.path.dirname(path)), path=path)


def load_items():
    items = {}
    for f in glob.glob(STORE + "/**/mg-*.md", recursive=True):
        it = parse_item(f)
        if it:
            items[it["id"]] = it
    return items


def is_onethird(it):
    return "onethird" in it["tags"] or "onethird_program" in it["repo"]


def tags_of(it):
    return [t.strip() for t in it["tags"].strip("[]").split(",") if t.strip()]


def is_audit(it):
    """STRICT. The bare `audit` tag is NOT enough -- see the module docstring."""
    return "independent-audit" in tags_of(it) or it["title"].upper().startswith("INDEPENDENT AUDIT")


def is_landing_by_title(it):
    return bool(re.search(r"\bLAND(ING|S|ED)?\b", it["title"], re.I))


PARENT_PROSE = re.compile(
    r"(?:AUDIT of|audit of|from c[0-9a-f]{4}'s|SAME ACTION as|parent |successor to |Successor to )"
    r"\s*(mg-[0-9a-f]{4})")


def parents_depends_only(it):
    """Just the `depends:` field -- the only source that is a GATE rather than a label."""
    return set(re.findall(r"mg-[0-9a-f]{4}", it["depends"]))


def parents(it, prose_window=1500):
    """Ids this item names as the work it carries or audits.

    Three sources, deliberately: `depends:`, the `mg-XXXX-followup` tag, and a prose
    window at the head of the body. A parent named only further down is invisible (E2),
    so this is a LOWER BOUND and every count built on it is one too.
    """
    p = set(re.findall(r"mg-[0-9a-f]{4}", it["depends"]))
    p |= {"mg-" + m for m in re.findall(r"mg-([0-9a-f]{4})-followup", it["tags"])}
    p |= set(PARENT_PROSE.findall(it["body"][:prose_window]))
    return p - {it["id"]}


# ---------------------------------------------------------------- events

def load_events():
    """item -> {claim: first claim ts, done: last done ts}."""
    ev = collections.defaultdict(dict)
    with open(EVENTS, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                e = json.loads(line)
            except Exception:
                continue
            i, t = e.get("item_id"), e.get("type")
            if not i:
                continue
            if t == "work.claim":
                ev[i].setdefault("claim", e["ts"])
            elif t == "work.done":
                ev[i]["done"] = e["ts"]
    return ev


# ---------------------------------------------------------------- git

def load_commits(rev="main"):
    """Commits on `rev` with author date, subject and touched files."""
    out = subprocess.run(
        ["git", "-C", REPO, "log", rev, "--format=%x01%H\t%aI\t%s", "--name-only"],
        capture_output=True, text=True).stdout
    commits = []
    cur = None
    for line in out.split("\n"):
        if line.startswith("\x01"):
            h, ad, s = line[1:].split("\t", 2)
            cur = dict(h=h, adate=ad, subject=s, files=[])
            commits.append(cur)
        elif line.strip() and cur is not None:
            cur["files"].append(line.strip())
    return commits


def is_canonical(path):
    return path in CANONICAL_EXACT or path.startswith(CANONICAL_PREFIX)


def commit_index(commits):
    """mg-id -> dict(commits=[...], canonical=[...], state=[...], first/last author date).

    An item is attributed a commit when the commit SUBJECT names it. A commit that does
    not name its item is invisible here (E6).
    """
    idx = collections.defaultdict(lambda: dict(commits=[], canonical=[], state=[], adates=[]))
    for c in commits:
        for i in set(re.findall(r"mg-[0-9a-f]{4}", c["subject"])):
            e = idx[i]
            e["commits"].append(c["h"][:7])
            e["adates"].append(c["adate"])
            if any(is_canonical(f) for f in c["files"]):
                e["canonical"].append(c["h"][:7])
            if "STATE.md" in c["files"]:
                e["state"].append(c["h"][:7])
    for e in idx.values():
        e["adates"].sort()
        e["first_write"] = e["adates"][0] if e["adates"] else None
        e["last_write"] = e["adates"][-1] if e["adates"] else None
    return idx


# ---------------------------------------------------------------- intervals

def wall_interval(ev, i):
    e = ev.get(i, {})
    a, b = e.get("claim"), e.get("done")
    if not (a and b):
        return REFUSED
    if a == b:
        # A zero-length interval overlaps NOTHING under any half-open rule, so letting it
        # through would print "no collision" for an item we cannot time at all. That is
        # the exact shape of a laundered green and it is REFUSED instead. mg-845e is a
        # live instance: claim and done land in the same second.
        return REFUSED
    return (a, b)


def write_interval(idx, i):
    e = idx.get(i)
    if not e or not e.get("first_write"):
        return REFUSED
    if e["first_write"] == e["last_write"]:
        # A single commit gives an instant, not an interval. Same refusal, same reason --
        # except here it is COMMON (a one-commit landing), so the write reading refuses
        # far more often than the wall reading and s2 must say so rather than net it out.
        return REFUSED
    return (e["first_write"], e["last_write"])


def overlaps(x, y):
    """Half-open interval intersection. REFUSED propagates -- it never becomes False."""
    if x is REFUSED or y is REFUSED:
        return REFUSED
    return x[0] < y[1] and y[0] < x[1]


def relation(landing_iv, audit_iv):
    """CONCURRENT / AUDIT-AFTER / AUDIT-BEFORE / REFUSED, from two intervals."""
    if landing_iv is REFUSED or audit_iv is REFUSED:
        return REFUSED
    ov = overlaps(landing_iv, audit_iv)
    if ov:
        return "CONCURRENT"
    if audit_iv[0] >= landing_iv[1]:
        return "AUDIT-AFTER"
    return "AUDIT-BEFORE"


# ---------------------------------------------------------------- the join

def build(prose_window=1500):
    items = load_items()
    one = {k: v for k, v in items.items() if is_onethird(v)}
    ev = load_events()
    commits = load_commits()
    idx = commit_index(commits)

    audits = {k: v for k, v in one.items() if is_audit(v)}
    subject_of_audit = collections.defaultdict(set)   # parent id -> {audit ids}
    for a in audits.values():
        for p in parents(a, prose_window):
            subject_of_audit[p].add(a["id"])

    landings = {k: v for k, v in one.items()
                if idx.get(k, {}).get("canonical")}

    triples = []
    for lid, lv in landings.items():
        for p in parents(lv, prose_window):
            for aid in subject_of_audit.get(p, ()):
                if aid == lid:
                    continue
                triples.append(dict(
                    landing=lid, parent=p, audit=aid,
                    landing_is_audit=is_audit(lv),
                    state=bool(idx.get(lid, {}).get("state")),
                    wall=relation(wall_interval(ev, lid), wall_interval(ev, aid)),
                    write=relation(write_interval(idx, lid), write_interval(idx, aid)),
                    l_wall=wall_interval(ev, lid), a_wall=wall_interval(ev, aid),
                    l_write=write_interval(idx, lid), a_write=write_interval(idx, aid),
                ))
    triples.sort(key=lambda t: (t["landing"], t["audit"]))
    return dict(items=items, one=one, ev=ev, idx=idx, audits=audits,
                landings=landings, subject_of_audit=subject_of_audit, triples=triples)


# ---------------------------------------------------------------- the RULE

def unaudited_parent(item, one, subject_of_audit, ev, at=None):
    """THE RULE, as a function of data that exists at landing time.

    Answers, for a landing about to be dispatched: does an audit of my parent exist that
    is NOT yet done? Returns a list of (parent, audit, state) for every such audit --
    empty means the landing may proceed under rule (b) with nothing to re-read.

    `at` is an ISO timestamp: the moment the question is asked. Passing it is what makes
    this answerable HISTORICALLY -- ask it at a past landing's claim time and it reports
    what was true then, which is how s6 shows the rule refusing cases it should refuse.
    """
    out = []
    for p in parents(item):
        for aid in sorted(subject_of_audit.get(p, ())):
            if aid == item["id"]:
                continue
            e = ev.get(aid, {})
            done = e.get("done")
            claim = e.get("claim")
            if at is None:
                st = "OPEN" if not done else "DONE"
            elif done and done <= at:
                st = "DONE"
            elif claim and claim <= at:
                st = "RUNNING"
            else:
                st = "NOT-YET-DISPATCHED"
            out.append((p, aid, st))
    return out


def banner(name, text):
    print("=" * 78)
    print(name)
    print("=" * 78)
    if text:
        print(text)
    print()
