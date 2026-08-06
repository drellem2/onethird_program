"""mg-bf3f — the verdict-delivery detector.

ONE PREDICATE, pm-onethird's own words:

    AN ITEM REACHING `done` (OR `archived`) WITH NO VERDICT MAIL RECEIVED BY ITS
    FILER IS A DROPPED VERDICT.

Both halves are read from macguffin's own store and nothing else:

  * the landing         -- `work.done` / `work.archive` in events.jsonl
  * the filer           -- `creator:` in the item's own frontmatter
  * the worker          -- `polecat-<name>` in the item's result sidecar
  * the verdict mail    -- a message in the filer's mailbox whose `From:` is
                           that worker

WHAT THIS DETECTOR CANNOT SEE, stated here and not in a footnote:

  D-1  A verdict delivered by any channel other than macguffin mail -- a commit
       subject, a docs/ file, a Slack relay, a spoken handover -- is invisible
       to it and is reported as DROPPED. That is the intended polarity: the
       ticket's whole complaint is that commit subjects are not delivery.
  D-2  An item whose worker cannot be resolved is NOT reported as delivered and
       NOT reported as dropped. It goes in its own UNDECIDABLE bucket, sized and
       listed, because a gate that silently absorbs what it cannot reach is the
       defect this arc keeps finding.
  D-3  A verdict mailed to somebody OTHER than the filer (to mayor, say) is not
       delivery to the filer and is reported as DROPPED. `mails_elsewhere` on
       each row records it, because it discriminates a dead process from a live
       one that did not mail the filer.
"""

import datetime
import glob
import json
import os
import re

MG_DEFAULT = os.path.expanduser("~/.macguffin")

_HDR = re.compile(r"^([A-Za-z-]+):[ \t]*(.*)$", re.M)
_CREATOR = re.compile(r"^creator:\s*(\S+)\s*$", re.M)
_CREATED = re.compile(r"^created:\s*(\S+)\s*$", re.M)
_TITLE = re.compile(r"^#\s+(.*)$", re.M)


def root(explicit=None):
    return explicit or os.environ.get("MG_ROOT") or MG_DEFAULT


def parse_ts(s):
    """Parse an RFC3339-ish stamp to naive UTC. Returns None on junk."""
    if not s:
        return None
    try:
        return datetime.datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return None


# ---------------------------------------------------------------- items

def load_items(mg):
    """Every work item on disk, keyed by id, from every status directory.

    Reads the store, not `mg list`, so an archived item under work/archive/<month>/
    is seen exactly like an available one.
    """
    out = {}
    for path in glob.glob(os.path.join(mg, "work", "**", "mg-*.md*"), recursive=True):
        base = os.path.basename(path)
        # DEFECT-5 of this instrument. A CLAIMED item is not `mg-bf3f.md` on
        # disk: macguffin stamps the owning pid into the filename, so it is
        # `mg-bf3f.md.90246`. The first form globbed `*.md` and therefore could
        # not see a single in-flight item -- including the one this instrument
        # was written for. Harmless for the predicate (a landed item is back to a
        # plain `.md`), and NOT harmless for anything that asks about work in
        # flight, which is why it is fixed rather than scoped around.
        m = re.match(r"^(mg-[0-9a-z]+)\.md(?:\.\d+)?$", base)
        if not m:
            continue
        iid = m.group(1)
        try:
            text = open(path, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        m = _CREATOR.search(text)
        c = _CREATED.search(text)
        t = _TITLE.search(text)
        out[iid] = {
            "id": iid,
            "path": path,
            "creator": m.group(1) if m else None,
            "created": c.group(1) if c else None,
            "title": t.group(1).strip() if t else "",
            "text": text,
            "status_dir": os.path.relpath(os.path.dirname(path), os.path.join(mg, "work")),
        }
    return out


def load_sidecar(item):
    path = item["path"][:-3] + ".result.json"
    if not os.path.exists(path):
        return None
    try:
        return json.load(open(path, encoding="utf-8", errors="replace"))
    except (OSError, ValueError):
        return None


_BRANCH = re.compile(r"^polecat-(.+)$")


def worker_names(item):
    """Candidate agent names for the worker of `item`, from mg's own store.

    The branch is the only worker identity macguffin records. `polecat-c1d6c`
    means the agent was `c1d6c`; the older `polecat-mg-69be` means `mg-69be` and
    also, historically, `69be`. Both spellings are returned, because the `From:`
    an agent writes has varied.
    """
    side = load_sidecar(item)
    if not side:
        return set()
    branch = side.get("branch") or ""
    m = _BRANCH.match(branch)
    if not m:
        return set()
    name = m.group(1)
    names = {name}
    if name.startswith("mg-"):
        names.add(name[3:])
    else:
        names.add("mg-" + name)
    return names


_SUFFIX = re.compile(r"^mg-([0-9a-f]{4})$")


def worker_names_by_shape(iid):
    """Second resolver: the polecat naming convention.

    DEFECT-2 of this instrument. The sidecar is the only worker identity mg
    RECORDS, but it is not the only one mg CARRIES: a polecat working `mg-9a19`
    is named `9a19`, or `z9a19`, or `mg-9a19` -- the id's four hex characters
    with at most a one-character generation prefix. Resolving from the sidecar
    alone put mg-9a19 and mg-65eb -- two items I had hand-verified as DELIVERED
    -- into UNDECIDABLE, which is the same silence the ticket is about.

    Deliberately narrow: at most ONE alphanumeric character of prefix, or the
    literal `mg-`/`cat-` prefixes. A wider rule starts matching unrelated agents.
    """
    m = _SUFFIX.match(iid)
    if not m:
        return set()
    s = m.group(1)
    out = {s, "mg-" + s, "cat-" + s}
    for c in "abcdefghijklmnopqrstuvwxyz0123456789":
        out.add(c + s)
        out.add("cat-" + c + s)
        out.add("mg-" + c + s)
    return out


def worker_declared(item):
    """The worker name EXACTLY as the branch spells it, or None.

    DEFECT-1 of this instrument: the first form displayed `sorted(names)[0]`,
    which prefers `mg-y0120` over `y0120` alphabetically and so printed a name
    that agent never used. The alternate spellings are for MATCHING; only this
    one is for READING.
    """
    side = load_sidecar(item)
    if not side:
        return None
    m = _BRANCH.match(side.get("branch") or "")
    return m.group(1) if m else None


# ---------------------------------------------------------------- events

def load_landings(mg):
    """item id -> {'ts': <first landing>, 'kind': 'done'|'archived', 'actor': ...}

    An item that goes done and is later archived lands once, at `done`. An item
    archived without ever going done lands at `archive` -- the predicate says
    "done OR archived" and both are terminal for the filer's purposes.
    """
    land = {}
    path = os.path.join(mg, "events.jsonl")
    if not os.path.exists(path):
        return land
    for line in open(path, encoding="utf-8", errors="replace"):
        try:
            e = json.loads(line)
        except ValueError:
            continue
        t = e.get("type")
        if t not in ("work.done", "work.archive"):
            continue
        iid = e.get("item_id")
        if not iid:
            continue
        kind = "done" if t == "work.done" else "archived"
        prev = land.get(iid)
        if prev is None or (prev["kind"] == "archived" and kind == "done"):
            land[iid] = {"ts": e.get("ts"), "kind": kind, "actor": e.get("actor"), "pid": e.get("pid")}
    return land


def load_mail_sent(mg):
    """Every mail.sent event, as a list of {from,to,ts,msg_id}."""
    out = []
    path = os.path.join(mg, "events.jsonl")
    if not os.path.exists(path):
        return out
    for line in open(path, encoding="utf-8", errors="replace"):
        if '"mail.sent"' not in line:
            continue
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if e.get("type") == "mail.sent":
            out.append(e)
    return out


# ---------------------------------------------------------------- mail

def load_mailbox(mg, agent):
    """Every message in `agent`'s mailbox: unread, read AND archived.

    Returns (messages, exists). `exists` is False when the mailbox directory has
    never been created -- which is a different thing from an empty mailbox and is
    reported separately, because 'nobody ever wrote to them' and 'they got no
    verdicts' are different findings.
    """
    box = os.path.join(mg, "mail", agent)
    if not os.path.isdir(box):
        return [], False
    msgs = []
    for sub in ("new", "cur", "archive"):
        d = os.path.join(box, sub)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            p = os.path.join(d, fn)
            if not os.path.isfile(p):
                continue
            try:
                text = open(p, encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            head = text.split("\n\n", 1)[0]
            hdr = {k.lower(): v.strip() for k, v in _HDR.findall(head)}
            msgs.append({
                "id": fn,
                "state": sub,
                "from": hdr.get("from", ""),
                "subject": hdr.get("subject", ""),
                "date": hdr.get("date", ""),
                "text": text,
            })
    return msgs, True


# ---------------------------------------------------------------- detector

def scan(mg=None, filer=None, since=None, simulate=None):
    """Run the predicate.

    filer=None scans every filer that has at least one landed item.
    since is an RFC3339 prefix; items that landed before it are excluded.

    Returns {'rows': [...], 'boxes': {agent: exists}, 'mg': mg}
    Each row: id, filer, worker, landed, kind, verdict (bool|None),
              verdict_mail, mails_elsewhere, title, status.
    status is one of DELIVERED / DROPPED / UNDECIDABLE.

    DECLARED ASYMMETRY. The `shape` fallback resolver (DEFECT-2) is consulted
    only when the sidecar is silent, and it is accepted only when the name it
    proposes actually appears as a `From:` in that filer's mailbox. So it can
    move an item UNDECIDABLE -> DELIVERED and can NEVER move one to DROPPED. It
    can only shrink the reported drop count, never inflate it. That is stated
    here rather than left for a reader to derive, because a resolver that could
    manufacture drops would make this whole report unfalsifiable.
    """
    mg = root(mg)
    items = load_items(mg)
    land = load_landings(mg)
    sent = load_mail_sent(mg)

    # `simulate` injects a landing that has not happened yet: {item_id: ts}. It
    # touches nothing but the landing half of the predicate -- the mail half is
    # read from the live store exactly as it stands. It exists so a live drop can
    # be OBSERVED before it happens, on real mail, rather than argued for. Every
    # row it produces is marked `simulated: True`.
    sim_worker = {}
    for iid, spec in (simulate or {}).items():
        if isinstance(spec, dict):
            ts, w = spec.get("ts"), spec.get("worker")
        else:
            ts, w = spec, None
        if w:
            # DEFECT-6. A worker's identity enters macguffin's store ONLY when
            # the refinery writes `branch: polecat-<name>` into the result
            # sidecar -- which happens at merge. So an item that has not merged
            # has no recorded worker, and a simulated landing lands in
            # UNDECIDABLE rather than DROPPED however plainly its verdict is
            # missing. That is a genuine BOUND, not a bug: A POLECAT WHOSE WORK
            # NEVER MERGES AND WHICH NEVER MAILS LEAVES NO TRACE THIS DETECTOR
            # CAN READ. Callers may supply the worker for a simulated landing;
            # it is recorded as `worker_supplied` on the row so no reader can
            # mistake it for something the store said.
            sim_worker[iid] = w
        if iid in land:
            continue
        land[iid] = {"ts": ts, "kind": "done", "actor": "SIMULATED", "pid": None,
                     "simulated": True}

    sent_by = {}
    for e in sent:
        sent_by.setdefault(e.get("from"), []).append(e)

    boxes = {}
    mailindex = {}

    rows = []
    for iid, info in items.items():
        if iid not in land:
            continue
        L = land[iid]
        if since and (L["ts"] or "") < since:
            continue
        f = info["creator"]
        if not f:
            continue
        if filer and f != filer:
            continue
        if f not in mailindex:
            msgs, exists = load_mailbox(mg, f)
            boxes[f] = exists
            byfrom = {}
            for m in msgs:
                byfrom.setdefault(m["from"], []).append(m)
            mailindex[f] = byfrom
        byfrom = mailindex[f]

        names = worker_names(info)
        resolver = "sidecar" if names else None
        supplied = sim_worker.get(iid)
        if not names and supplied:
            names = {supplied, "mg-" + supplied}
            resolver = "supplied"
        if not names:
            # DEFECT-2 fallback. Only consult the shape rule when the sidecar is
            # silent, and only accept it when it actually matches a sender that
            # wrote to this filer -- a name that nobody used resolves nothing.
            shape = worker_names_by_shape(iid)
            hit = shape & set(byfrom)
            if hit:
                names = hit
                resolver = "shape"
        row = {
            "id": iid,
            "filer": f,
            "worker": worker_declared(info) or supplied or (sorted(names)[0] if names else None),
            "resolver": resolver,
            "worker_supplied": bool(supplied and resolver == "supplied"),
            "worker_names": sorted(names),
            "landed": L["ts"],
            "kind": L["kind"],
            "done_actor": L.get("actor"),
            "simulated": bool(L.get("simulated")),
            "title": info["title"],
            "verdict_mail": None,
            "mails_elsewhere": 0,
            "mailbox_exists": boxes.get(f, False),
        }
        if not names:
            row["status"] = "UNDECIDABLE"
            row["verdict"] = None
            rows.append(row)
            continue

        hits = []
        for n in names:
            hits.extend(byfrom.get(n, []))
        hits.sort(key=lambda m: m["date"])
        elsewhere = 0
        for n in names:
            for e in sent_by.get(n, []):
                if e.get("to") != f:
                    elsewhere += 1
        row["mails_elsewhere"] = elsewhere
        if hits:
            row["status"] = "DELIVERED"
            row["verdict"] = True
            row["verdict_mail"] = {
                "id": hits[0]["id"], "date": hits[0]["date"],
                "subject": hits[0]["subject"], "state": hits[0]["state"],
                "n": len(hits),
            }
        else:
            row["status"] = "DROPPED"
            row["verdict"] = False
        rows.append(row)

    rows.sort(key=lambda r: (r["landed"] or "", r["id"]))
    return {"rows": rows, "boxes": boxes, "mg": mg}


def summarise(res):
    c = {"DELIVERED": 0, "DROPPED": 0, "UNDECIDABLE": 0}
    for r in res["rows"]:
        c[r["status"]] += 1
    return c


# ------------------------------------------------- lead time (for the cause)

def verdict_lead_minutes(row):
    """Minutes by which the verdict mail PRECEDED the landing. Negative = after.

    This is the number that discriminates the reap from the instruction: a reap
    that fires at landing+0.5s cannot suppress a mail that a compliant worker
    sends minutes to hours BEFORE landing.
    """
    if not row.get("verdict_mail"):
        return None
    a = parse_ts(row["verdict_mail"]["date"])
    b = parse_ts(row["landed"])
    if a is None or b is None:
        return None
    return round((b - a).total_seconds() / 60.0, 1)
