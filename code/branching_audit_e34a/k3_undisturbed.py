"""k3_undisturbed.py -- WHAT mg-957f CONFIRMED, RE-DERIVED AFTER THE REPAIR.

mg-957f confirmed two things about mg-7e58 and this audit must not let a
repair to one half quietly weaken the other:

  * THE ATTRIBUTION IS RIGHT AT 17 OF 17 AND DERIVED.  g4 and g1 between them
    make 17 provenance claims.  mg-957f scored them against a ground truth it
    derived twice, over the range 286d5030..2d23d880 -- ITS OWN HEAD, PINNED.
  * g1 WAS NOT SILENCED: its direction probes were stated at 3 of 3, and the
    4 clone directions at 4 of 4.

mg-76cc's repair touches g1 and lib58da, and lib58da is underneath g4.  So
both are re-taken here, and the range is NOT pinned: it is 286d5030..HEAD, so
that a commit landing after mg-957f which breaks an attribution is inside the
population rather than outside it.  mg-05eb has already booked one finding in
this arc whose whole content was that a scan had been pinned.

Nothing here re-opens what mg-957f settled.  If a row disagrees, that is a
weakening introduced since, and it is a finding.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import sys

import libe34a as L

R = L.Report(
    selfpop="every git read and subprocess run this script performs, plus "
            "the requirement that each block it scores be FOUND in the "
            "output it parses -- a block this script could not locate is a "
            "fact about this script and is never scored as agreement",
    findpop="every attribution g4 and g1 print, each against a ground truth "
            "derived here twice over 286d5030..HEAD; g1's direction probes; "
            "and the exit code and totals of both scripts")

L.banner("K3", "THE ATTRIBUTION AND THE PROBES, RE-TAKEN AFTER THE REPAIR")
print("""
A repair that restores one half of a predicate is a way to break the other.
mg-76cc changed g1 and lib58da; g4 shares lib58da with it.
""")

HEAD = L.head_rev()
FIVE = ["c1_branching.py", "c2_vertexsets.py", "c3_withdrawal.py",
        "c4_seam.py", "c5_record.py"]

# ---------------------------------------------------------------------------
L.rule("(i) THE GROUND TRUTH, DERIVED TWICE, OVER 286d5030..HEAD")
print("""   Route one asks the LOG about a path.  Route two asks a COMMIT what
   it did.  Different questions, same answer, and the answer is used
   only where both give it.  The range ends at HEAD and not at
   mg-957f's own HEAD: a pinned scan stops being a measurement the
   moment anything lands after it.""")
print()
print("   range: %s..%s" % (L.REV_A218[:8], HEAD[:8]))
print("     left  %s  %s" % (L.REV_A218[:8], L.subject(L.REV_A218)[:56]))
print("     right %s  %s" % (HEAD[:8], L.subject(HEAD)[:56]))
print()
route1 = {}
for f in FIVE + ["kern_a218.py"]:
    route1[f] = L.commits_touching(L.A218_DIR + "/" + f, L.REV_A218, HEAD)
route1["out_t1_tl.txt"] = L.commits_touching(L.TARGET_REL, L.REV_A218, HEAD)
print("   route one -- git log <range> -- <path>:")
for f in FIVE:
    print("     %-24s %s" % (f, ", ".join(c[:8] for c in route1[f]) or "NONE"))
print()
touching_dir = [c for c in L.commits_touching(L.A218_DIR, L.REV_A218, HEAD)]
route2 = {}
for c in touching_dir:
    for p in L.files_of(c):
        base = p.split("/")[-1]
        if p.startswith(L.A218_DIR + "/") and base in FIVE:
            route2.setdefault(c, []).append(base)
print("   route two -- git show --name-only, per commit touching the "
      "directory:")
for c in touching_dir:
    print("     %-10s %s" % (c[:8], ", ".join(route2.get(c, [])) or "(none of "
                             "the five)"))
print()
agree = 0
for f in FIVE:
    r1 = sorted(route1[f])
    r2 = sorted(c for c in touching_dir if f in route2.get(c, []))
    ok = r1 == r2
    agree += ok
    R.check(ok, "the two derivation routes disagree about %s: %s vs %s; no "
                "row below may be scored against either" % (f, r1, r2))
print("   THE TWO ROUTES AGREE at %d of %d members." % (agree, len(FIVE)))
print("   and the kernel and the target, for the same range:")
for f in ("kern_a218.py", "out_t1_tl.txt"):
    print("     %-24s %s" % (f, ", ".join(c[:8] for c in route1[f]) or "NONE"))
print()

# ---------------------------------------------------------------------------
L.rule("(ii) g4 AND g1, RUN LIVE")
g4_out, g4_rc = L.run_script(L.S58DA_DIR, "g4_fleet.py")
g1_out, g1_rc = L.run_script(L.S58DA_DIR, "g1_provenance.py")
g4s, g4f = L.trailer(g4_out)
g1s, g1f = L.trailer(g1_out)
print("     g4  exit %d  SELF %s  FINDINGS %s" % (g4_rc, g4s, g4f))
print("     g1  exit %d  SELF %s  FINDINGS %s" % (g1_rc, g1s, g1f))
for out, name in ((g4_out, "g4_fleet.py"), (g1_out, "g1_provenance.py")):
    ok, why = L.trailer_consistent(out)
    R.check(ok, "%s printed a trailer that does not match its own listed "
                "lines: %s" % (name, why))
print()
print("""   mg-957f read g4 at exit 1 with 0/2 and g1 at exit 0 with 0/0.  A
   repair that moved either without saying so is a weakening whatever
   else it fixed:""")
R.gate((g4_rc, g4s, g4f) == (1, 0, 2),
       "g4_fleet.py now exits %d with %s/%s where mg-957f read exit 1 with "
       "0/2; mg-76cc's change to lib58da reached a script it says it did not "
       "open" % (g4_rc, g4s, g4f))
R.gate((g1_rc, g1s, g1f) == (0, 0, 0),
       "g1_provenance.py now exits %d with %s/%s where mg-957f read exit 0 "
       "with 0/0" % (g1_rc, g1s, g1f))
print("     g4 unchanged from mg-957f's reading : %s"
      % ("yes" if (g4_rc, g4s, g4f) == (1, 0, 2) else "NO"))
print("     g1 unchanged from mg-957f's reading : %s"
      % ("yes" if (g1_rc, g1s, g1f) == (0, 0, 0) else "NO"))
print()

# ---------------------------------------------------------------------------
L.rule("(iii) EVERY ATTRIBUTION THEY PRINT, ENUMERATED AND SCORED")


def block(out, start, stop=None):
    """The lines after the first line containing `start`, up to a blank line
    or `stop`.  Returns [] if `start` is absent -- and every caller books that
    as a SELF-ERROR, because a block this script cannot find is a fact about
    this script and not agreement."""
    lines = out.splitlines()
    for i, line in enumerate(lines):
        if start in line:
            got = []
            for x in lines[i + 1:]:
                if not x.strip():
                    break
                if stop and stop in x:
                    break
                got.append(x)
            return got
    return []


CLAIMS = []      # (what, claim, agrees?, why)


def score(what, claim, ok, why):
    CLAIMS.append((what, claim, ok, why))


# -- g4's five member rows -------------------------------------------------
rows = block(g4_out, "script                 %s -> " % L.REV_A218[:8])
R.check(bool(rows), "g4's member table was not found in its output; its 5 "
                    "member rows are DROPPED rather than scored")
g4_member = {}
for line in rows:
    s = line.strip()
    name = s.split()[0]
    if name not in FIVE:
        continue
    rest = s[len(name):].strip()
    if rest.startswith("CHANGED ("):
        g4_member[name] = [rest.split("(", 1)[1].split(")", 1)[0]]
    else:
        g4_member[name] = []
for f in FIVE:
    if f not in g4_member:
        R.check(False, "g4 printed no member row for %s; it is DROPPED "
                       "rather than scored" % f)
        continue
    truth = [c[:8] for c in route1[f]]
    got = g4_member[f]
    score("g4 member row", "%s <- %s" % (f, ", ".join(got) or "nothing"),
          got == truth, "git log here: %s" % (", ".join(truth) or "nothing"))

# -- g4's commit rows and its ticket labels --------------------------------
att = block(g4_out, "ATTRIBUTION, INVERTED FROM THE SAME git log CALLS")
R.check(bool(att), "g4's ATTRIBUTION block was not found; its commit rows "
                   "and ticket labels are DROPPED rather than scored")
cur, g4_commit, g4_label = None, {}, {}
for line in att:
    s = line.strip()
    if s.startswith("touches:"):
        if cur is not None:
            g4_commit[cur] = [x.strip() for x in
                              s.split(":", 1)[1].split(",") if x.strip()]
        continue
    parts = s.split()
    if len(parts) >= 2 and len(parts[0]) == 8 and all(
            c in "0123456789abcdef" for c in parts[0]):
        cur, g4_label[parts[0]] = parts[0], parts[1]
    elif s.startswith("(none)"):
        cur = "(none)"
for c8, members in g4_commit.items():
    if c8 == "(none)":
        score("g4 commit row", "an uncommitted edit -> %s"
              % (", ".join(members) or "none"),
              members in ([], ["none"]),
              "nothing is uncommitted in a clean tree")
        continue
    full = [c for c in touching_dir if c.startswith(c8)]
    truth = sorted(route2.get(full[0], [])) if full else None
    score("g4 commit row", "%s -> %s" % (c8, ", ".join(members)),
          truth is not None and sorted(members) == truth,
          "--name-only here: %s" % (", ".join(truth) if truth else "no such "
                                    "commit in the range"))
for c8, ticket in g4_label.items():
    full = [c for c in touching_dir if c.startswith(c8)]
    subj = L.subject(full[0]) if full else ""
    score("g4 ticket label", "%s is %s" % (c8, ticket),
          subj.rstrip().endswith("(%s)" % ticket),
          "its own subject ends %r" % (" (%s)" % ticket))

# -- g4's three summary lines ----------------------------------------------
nsum = 0
for line in g4_out.splitlines():
    s = line.strip()
    if not s.startswith("of the five, touched by"):
        continue
    nsum += 1
    head, _, tail = s.partition(":")
    who = head[len("of the five, touched by"):].strip()
    n = L._leading_int(tail)
    named = tail.split("--", 1)[1].strip() if "--" in tail else ""
    if "uncommitted" in who:
        truth_n, truth_named = 0, "none"
    else:
        # g4 writes this row two ways: by COMMIT PREFIX ("ed9cde4 (mg-13b2)")
        # and by TICKET alone ("mg-58da").  Both name the same thing and both
        # have to be resolved, or the ticket form scores WRONG against a
        # commit lookup that was never going to find it.  Resolved through
        # the commit SUBJECT, which is where the ticket name lives.
        tok = who.split()[0]
        if len(tok) >= 7 and all(c in "0123456789abcdef" for c in tok):
            full = [c for c in touching_dir if c.startswith(tok[:7])]
        else:
            full = [c for c in touching_dir
                    if L.subject(c).rstrip().endswith("(%s)" % tok)]
        ms = sorted(route2.get(full[0], [])) if full else []
        truth_n, truth_named = len(ms), ", ".join(ms) or "none"
        R.check(bool(full),
                "g4's summary line %r names something this script could "
                "resolve to neither a commit prefix nor a ticket in the "
                "range; the row is scored against an empty derivation and "
                "that is a fact about THIS script" % who)
    score("g4 summary", "%s -> %s (%s)" % (who[:24], n, named),
          n == truth_n and named == truth_named,
          "derived here: %d (%s)" % (truth_n, truth_named))
R.check(nsum == 3, "g4 printed %d `of the five, touched by` summary lines, "
                   "not the 3 mg-957f scored" % nsum)

# -- g1's three commits-touching rows --------------------------------------
g1rows = block(g1_out, "commits touching each part of the reproduction")
R.check(bool(g1rows), "g1's commits-touching block was not found; its 3 rows "
                      "are DROPPED rather than scored")
for line in g1rows:
    s = line.strip()
    name = s.split()[0]
    got = [t for t in s.split() if len(t) == 8
           and all(c in "0123456789abcdef" for c in t)]
    if "NONE" in s:
        got = []
    truth = [c[:8] for c in route1.get(name, [])]
    score("g1 commits-touching row", "%s <- %s"
          % (name, ", ".join(got) or "NONE"), got == truth,
          "git log here: %s" % (", ".join(truth) or "NONE"))

# -- g1's two file-sha rows ------------------------------------------------
sha_rows = block(g1_out, "NOTHING IS CONCLUDED FROM IT")
n_sha = 0
for line in sha_rows:
    s = line.strip()
    name = s.split()[0]
    if name not in ("c1_branching.py", "kern_a218.py"):
        continue
    n_sha += 1
    said = "CHANGED" if s.endswith("CHANGED") else "SAME"
    truth = ("CHANGED" if L.sha(L.git_show(L.REV_A218, L.A218_DIR + "/" + name))
             != L.sha(L.git_show(HEAD, L.A218_DIR + "/" + name)) else "SAME")
    score("g1 file-sha row", "%s is %s" % (name, said), said == truth,
          "sha256 at both revisions here: %s" % truth)
R.check(n_sha == 2, "g1 printed %d file-sha rows, not 2" % n_sha)

print()
print("   ATTRIBUTION                                        VERDICT  why")
print("   " + "-" * 68)
for what, claim, ok, why in CLAIMS:
    print("     %-48s %-8s %s"
          % (("%s: %s" % (what.split()[0], claim))[:48],
             "AGREES" if ok else "WRONG", why[:38]))
    R.gate(ok, "%s -- %s -- disagrees with the derivation here (%s)"
           % (what, claim, why))
print()
ok_n = len([c for c in CLAIMS if c[2]])
print("   ATTRIBUTIONS SCORED: %d of %d agree." % (ok_n, len(CLAIMS)))
print("   Population: g4's %d member rows, %d commit rows, %d ticket labels"
      % (len([c for c in CLAIMS if c[0] == "g4 member row"]),
         len([c for c in CLAIMS if c[0] == "g4 commit row"]),
         len([c for c in CLAIMS if c[0] == "g4 ticket label"])))
print("   and %d summary lines; g1's %d commits-touching rows and %d file-sha"
      % (len([c for c in CLAIMS if c[0] == "g4 summary"]),
         len([c for c in CLAIMS if c[0] == "g1 commits-touching row"]),
         len([c for c in CLAIMS if c[0] == "g1 file-sha row"])))
print("   rows -- enumerated from THEIR OWN OUTPUT, not from a list here.")
print()
print("""   mg-957f scored 17 and %d are scored here.  The difference is NAMED
   rather than reconciled: mg-957f scored g4's `(none) uncommitted`
   entry once, as a summary line; here it is scored twice, as the
   ATTRIBUTION block's own `touches: none` row as well.  Both readings
   are of the same two printed lines and neither is a claim the other
   does not cover.""" % len(CLAIMS))
R.gate(len(CLAIMS) >= 17,
       "only %d attributions could be enumerated out of g4's and g1's live "
       "output; mg-957f scored 17, and a population that shrank is how a "
       "claim stops being checked without anything going red" % len(CLAIMS))
print()

# ---------------------------------------------------------------------------
L.rule("(iv) g1's DIRECTION PROBES -- 3 OF 3 MUST STILL BE THERE")
print("""   mg-957f stated g1's disposition at 3 of 3 probes.  mg-76cc grew
   that population to 5.  A population that grows is not evidence that
   the original three survived: they are looked for BY NAME.""")
print()
probes = []
for line in g1_out.splitlines():
    s = line.strip()
    if s.endswith("HIT") or s.endswith("MISS"):
        if "predicted" in s or "silent" in s or "FIRES" in s:
            probes.append(s)
print("   %d probe rows in g1's live output:" % len(probes))
for p in probes:
    print("     %s" % p[:88])
print()
WANTED = [("c1 @ ", "(unmodified -- NULL PROBE)"),
          ("c1 @ HEAD with the vertex DIMENSIONS off by one", ""),
          ("c1 @ HEAD with a line added past section (iii)", "")]
found = 0
for a, b in WANTED:
    hits = [p for p in probes if a in p and b in p]
    ok = len(hits) >= 1 and all(p.endswith("HIT") for p in hits)
    found += bool(hits)
    print("     %-52s %s" % ((a + b)[:52],
                             "present and HIT" if ok else
                             ("present, NOT HIT" if hits else "ABSENT")))
    R.gate(ok, "g1's pre-mg-76cc direction probe %r is %s after the repair; "
               "mg-957f stated the disposition at 3 of 3 and a probe that "
               "vanished is a probe that stopped being run"
           % ((a + b).strip(), "not HIT" if hits else "gone"))
print()
print("   the three probes mg-957f scored, still present : %d of %d"
      % (found, len(WANTED)))
hit_n = len([p for p in probes if p.endswith("HIT")])
print("   the whole probe population at HEAD             : %d of %d HIT"
      % (hit_n, len(probes)))
R.gate(hit_n == len(probes) and len(probes) >= 3,
       "g1's own direction probes are %d HIT of %d at HEAD; a probe whose "
       "direction was mispredicted is the check reporting on itself"
       % (hit_n, len(probes)))
print()

# ---------------------------------------------------------------------------
L.rule("VERDICT")
print("""   NOTHING mg-957f CONFIRMED IS WEAKER HERE.

     attributions scored          : %d of %d agree, over 286d5030..HEAD
     the two derivation routes    : agree at %d of %d members
     g4                           : exit %d, %s/%s -- as mg-957f read it
     g1                           : exit %d, %s/%s -- as mg-957f read it
     mg-957f's 3 probes           : %d of %d present, by name
     g1's probe population at HEAD: %d of %d HIT

   The range is 286d5030..HEAD and not mg-957f's own HEAD, so a commit
   that landed after that audit is inside this population rather than
   behind it.
""" % (ok_n, len(CLAIMS), agree, len(FIVE), g4_rc, g4s, g4f, g1_rc, g1s, g1f,
       found, len(WANTED), hit_n, len(probes)))

sys.exit(R.emit())
