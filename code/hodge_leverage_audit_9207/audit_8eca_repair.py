#!/usr/bin/env python3
"""mg-9207 -- INDEPENDENT AUDIT OF THE mg-8eca REPAIR OF mg-8aae.

Target: `d59ecd9` + `bee07a1`, and the two items mg-8aae left open on the
mg-8916 repair.

  H-1  the figure census was a MULTISET, and a multiset is invariant under a
       transposition, so two DECLARED figures of equal length exchanged in
       ordinary prose were invisible at 2 of 2 sites at exit 0.  mg-8eca
       replaced the roster with `ORDER`, an ordered list of slots, and added a
       `FIGURE ORDER` row per site.

  H-2  `SUMMARY vs ROWS` scored `printed == derived` where
       `printed = FORCE_SUMMARY or derived` -- `x == x` off the forcing hook.
       mg-8eca parses the printed verdict AND its count back out of the lines
       the run will print.

THE STANDARD THIS INSTRUMENT HOLDS THE DEMONSTRATIONS TO, and it is mg-8aae's
own: the defect was a check that fired ONLY THROUGH A PURPOSE-BUILT HOOK while
being `x == x` against the artifact.  So a demonstration is evidence here only
if it runs THE SAME PATH A REAL DEFECT WOULD -- the real file on disk, the real
runner as a SUBPROCESS, no environment variable, no in-memory call of the gate
function, no fixture.

  ⚠️ mg-8eca's own negative control N15-N18 calls `figure_gate` on IN-MEMORY
  copies of the site texts.  That is a FIXTURE.  It is a good fixture and it is
  not rejected as worthless -- but it is not accepted here as evidence that the
  gate fires, because "the gate function returns False when called with a
  mutated string" and "the runner goes red when the document is wrong" are
  different sentences and the whole of H-1 and H-2 is the difference.  Every
  exchange below is written TO DISK and scored by
  `python3 code/hodge_leverage_landing_e1d0/verify_landing.py` run as a
  subprocess.

  C  THE CENSUS, ON DISK.  Exchanges selected BY A PROCEDURE, not by hand, at
     all THREE sites -- including §14, which mg-8eca never exchanged on disk.
     Each must (i) make the runner red, (ii) at the `FIGURE ORDER` row FOR THAT
     SITE, (iii) as the ONLY row that failed, and (iv) with that site's
     licensing (multiset) row still green -- which is the ARTIFACT'S OWN
     evidence that the mutation was a permutation and nothing else.  Then 3-
     cycles in BOTH cyclic senses, and the involution control.

  E  DID THE FIX MOVE THE INVARIANCE?  The exchange has two halves -- the
     figures and the statements they are attached to -- and mg-8eca closed one.
     E2/E3 exchange the LABELS instead of the figures and reproduce mg-8aae's
     own reader-visible defect from the other side.  NOTHING IN THE ASSIGNMENT
     NAMES THESE; they are this audit's own item.

  D  `SUMMARY vs ROWS` ON THE REAL ARTIFACT, in the direction the assignment
     names -- move a ROW, not the sentence -- across every achievable state of
     the rows.  Then mg-8eca's own text direction, re-taken on disk.  Then THE
     DELETION TEST AT THE FINEST UNIT THAT HAS A RETURN: the repaired condition
     is a conjunction of two terms and each is deleted ON ITS OWN.

  S  DO NOT DISTURB WHAT IS CONFIRMED.  mg-8aae's own instrument and mg-8916's
     own instrument, both UNMODIFIED, re-run here rather than quoted.

IT MUTATES THE TREE AND RESTORES IT.  `STATE.md`, the deliverable, the row
history and `code/hodge_leverage_audit_8a5c/audit_repair_8e30.py` are written to
and restored inside a `finally`, every restoration CHECKED BY sha256 against the
bytes read before the run rather than asserted.  It REFUSES TO RUN if any of
them is already dirty.  Every site mutation is LENGTH-PRESERVING, because four
of the five live figures are lengths of the very text being mutated.

PREDICTED EXIT CODE, WRITTEN BEFORE THE FIRST RUN: 1.  Not because the repair
fails -- C and D are predicted to hold -- but because E2/E3 and the deletion
test are predicted to land as findings.
"""
import hashlib
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))

STATE = "STATE.md"
DELIV = "docs/OneThird-Hodge-Side-Leverage.md"
HIST = "docs/state-history/attempt-mg-a3d4.md"
AUDIT_8A5C = "code/hodge_leverage_audit_8a5c/audit_repair_8e30.py"
VERIFY = "code/hodge_leverage_landing_e1d0/verify_landing.py"

MUTABLE = [STATE, DELIV, HIST, AUDIT_8A5C]

# Committed transcripts this run reads or whose instruments it re-runs.  Every
# one is sha256-checked UNCHANGED afterwards: an audit that regenerates the
# record it is auditing has destroyed its own evidence.
FROZEN = ["code/hodge_leverage_audit_8aae/out_audit_8916.txt",
          "code/hodge_leverage_audit_8a5c/out_audit_8e30.txt",
          "code/hodge_leverage_repair_8916/out_repair_8916.txt",
          "code/hodge_leverage_repair_8eca/out_repair_8eca.txt",
          "code/hodge_leverage_landing_e1d0/out_verify.txt"]

RESULTS = []
FINDINGS = []


# --------------------------------------------------------------------------
# plumbing
# --------------------------------------------------------------------------
def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args),
                          capture_output=True, text=True, check=True).stdout


def read(path):
    with open(os.path.join(REPO, path), encoding="utf-8") as fh:
        return fh.read()


def write(path, text):
    with open(os.path.join(REPO, path), "w", encoding="utf-8") as fh:
        fh.write(text)


def sha(path):
    return hashlib.sha256(read(path).encode("utf-8")).hexdigest()


def record(ok, detail):
    RESULTS.append((detail, ok))
    mark = {True: "[CONFIRMED]", False: "[REFUTED  ]", None: "[MEASURED ]"}[ok]
    print(f"  {mark} {detail}")


def finding(tag, detail):
    FINDINGS.append((tag, detail))
    print(f"  [FINDING  ] {tag} -- {detail}")


def head(title):
    print()
    print(title)
    print("-" * len(title))


def run_verify():
    """THE REAL RUNNER, as a subprocess, against whatever is on disk.

    Not `run_all.sh`: that redirects into `out_verify.txt`, which is a
    committed transcript, and an audit that overwrites the record it checks has
    destroyed its own evidence.  Same interpreter, same file, same exit code."""
    r = subprocess.run([sys.executable, os.path.join(REPO, VERIFY)],
                       capture_output=True, text=True, cwd=REPO)
    return r.returncode, r.stdout + r.stderr


def run_8a5c(env=None):
    """The mg-8a5c audit instrument, as a subprocess, against what is on disk."""
    e = dict(os.environ)
    e.pop("MG8916_FORCE_SUMMARY", None)
    if env:
        e.update(env)
    r = subprocess.run([sys.executable, os.path.join(REPO, AUDIT_8A5C)],
                       capture_output=True, text=True, cwd=REPO, env=e)
    return r.returncode, r.stdout + r.stderr


def refuted_rows(out):
    return [l.strip()[len("[REFUTED  ]"):].strip()
            for l in out.split("\n") if l.strip().startswith("[REFUTED  ]")]


def confirmed_rows(out):
    return [l.strip()[len("[CONFIRMED]"):].strip()
            for l in out.split("\n") if l.strip().startswith("[CONFIRMED]")]


def summary_row(out):
    """The `SUMMARY vs ROWS` line and its mark, out of a run's own output."""
    for l in out.split("\n"):
        s = l.strip()
        if "SUMMARY vs ROWS" in s and s.startswith("["):
            return s[:11], s
    return None, None


# --------------------------------------------------------------------------
# MY OWN READER OF THE SITES.  It shares no code with `verify_landing.py`:
# quotations are MASKED IN PLACE rather than deleted, so every token keeps its
# offset in the raw file and a mutation can be written back at that offset.
# The gate is never imported and never called.
# --------------------------------------------------------------------------
QUOTED = [re.compile(r'\*"(.+?)"\*', re.DOTALL),
          re.compile(r"\*'(.+?)'\*", re.DOTALL)]


def mask_quotations(raw):
    """Marked quotations blanked to spaces, LENGTH AND OFFSETS PRESERVED.  The
    convention is the sites' own and is stated in `assertions()`: a quotation
    of a withdrawn figure is not an assertion of it."""
    out = raw
    for pat in QUOTED:
        while True:
            m = pat.search(out)
            if not m:
                break
            out = out[:m.start()] + " " * (m.end() - m.start()) + out[m.end():]
    return out


def scan_figures(raw):
    """[(offset, token)] for every figure-shaped token the site ASSERTS, in the
    order a reader meets them.  Found by SCANNING, character by character, with
    no regex -- so a shared pattern cannot make this agree with the gate for
    the wrong reason.  A figure of this class is a space-grouped number
    (`48 846`, `+23 771`) or a signed run of three or more digits (`−875`)."""
    t = mask_quotations(raw)
    out = []
    i, n = 0, len(t)
    while i < n:
        c = t[i]
        start = i
        sign = ""
        if c in "−+":
            sign, i = c, i + 1
        if i >= n or not t[i].isdigit():
            i = start + 1
            continue
        if start > 0 and (t[start - 1].isalnum() or t[start - 1] in "_−+"):
            i = start + 1
            continue
        groups, j = [], i
        while True:
            k = j
            while k < n and t[k].isdigit():
                k += 1
            groups.append(t[j:k])
            if (k + 1 < n and t[k] == " " and t[k + 1].isdigit()
                    and len(groups[-1]) <= 3 and k + 4 <= n
                    and t[k + 1:k + 4].isdigit()
                    and (k + 4 >= n or not t[k + 4].isdigit())):
                j = k + 1
                continue
            break
        end = j + len(groups[-1])
        if end < n and t[end].isdigit():
            i = start + 1
            continue
        tok = t[start:end]
        if len(groups) >= 2 and all(len(g) == 3 for g in groups[1:]) \
                and 1 <= len(groups[0]) <= 3:
            out.append((start, tok))
            i = end
            continue
        if sign and len(groups) == 1 and len(groups[0]) >= 3:
            out.append((start, tok))
            i = end
            continue
        i = start + 1
    return out


def only_line(text, prefix):
    hits = [(i, l) for i, l in enumerate(text.split("\n")) if l.startswith(prefix)]
    if len(hits) != 1:
        raise SystemExit(f"expected 1 line starting {prefix!r}, got {len(hits)}")
    lines = text.split("\n")
    off = sum(len(l) + 1 for l in lines[:hits[0][0]])
    return off, hits[0][1]


def only_section(text, prefix):
    lines = text.split("\n")
    starts = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    if len(starts) != 1:
        raise SystemExit(f"expected 1 heading {prefix!r}, got {len(starts)}")
    i = starts[0]
    lvl = len(lines[i]) - len(lines[i].lstrip("#"))
    end = len(lines)
    for j in range(i + 1, len(lines)):
        s = lines[j]
        if s.startswith("#"):
            l2 = len(s) - len(s.lstrip("#"))
            if l2 <= lvl:
                end = j
                break
    off = sum(len(l) + 1 for l in lines[:i])
    return off, "\n".join(lines[i:end])


SITE_SPECS = [
    ("the STATE.md row", STATE, "line", "| **AMBER-POSITIVE"),
    ("§14", DELIV, "section", "## §14 — `STATE.md` row, as landed"),
    ("H8", HIST, "section", "### H8 — "),
]

# The roster's declared slot count per site, transcribed from `ORDER` in
# `verify_landing.py` BY HAND so that this instrument's reader is checked
# against the roster rather than derived from it.
DECLARED_SLOTS = {"the STATE.md row": 17, "§14": 16, "H8": 36}


def sites():
    """{name: (path, file offset of the site, site text)}."""
    out = {}
    for name, path, kind, anchor in SITE_SPECS:
        t = read(path)
        off, txt = (only_line(t, anchor) if kind == "line"
                    else only_section(t, anchor))
        out[name] = (path, off, txt)
    return out


def live_values():
    """The five figures the run measures, formatted as the documents write
    them.  Computed here, in this file, so that a pair touching a live value
    can be excluded without asking the gate."""
    st, dl, hs = read(STATE), read(DELIV), read(HIST)
    a = len(only_line(st, "| **AMBER-POSITIVE")[1])
    b = len(only_line(dl, "> **AMBER-POSITIVE")[1])
    h = len(hs)

    def num(v, signed=False):
        s = f"{v:+,}" if signed else f"{v:,}"
        return s.replace(",", " ").replace("-", "−")
    return {num(a), num(h), num(b), num(a - b, True), num(a + h - b, True)}, (a, b, h)


def splice(path, off, old_site, new_site):
    t = read(path)
    assert t[off:off + len(old_site)] == old_site, ("site moved", path)
    write(path, t[:off] + new_site + t[off + len(old_site):])


def swap_tokens(site_text, i, j, figs):
    """Exchange the tokens at figure-sequence positions i and j.  Equal length
    is required, so the site text is LENGTH-PRESERVED and a gate that fires
    because the file grew has read nothing."""
    (oi, ti), (oj, tj) = figs[i], figs[j]
    assert len(ti) == len(tj) and ti != tj
    assert oi < oj
    return (site_text[:oi] + tj + site_text[oi + len(ti):oj]
            + ti + site_text[oj + len(tj):])


def rotate_tokens(site_text, idxs, figs, back=False):
    """Rotate three tokens through their three slots, in one cyclic sense or
    the other.  A transposition is its own inverse and so has only ONE
    exchanged text; a 3-cycle is the smallest permutation that genuinely has
    two distinct orderings, which is what makes 'both orderings' a question
    that can be asked at all."""
    toks = [figs[k][1] for k in idxs]
    new = toks[-1:] + toks[:-1] if not back else toks[1:] + toks[:1]
    out, prev = "", 0
    for k, val in zip(idxs, new):
        off, tok = figs[k]
        out += site_text[prev:off] + val
        prev = off + len(tok)
    return out + site_text[prev:]


def pick_pairs(name, figs, live, limit=4):
    """THE SELECTION PROCEDURE, stated so the probes are not hand-picked: every
    pair of ADJACENT, DISTINCT, EQUAL-LENGTH tokens in the site's own asserted
    sequence, NEITHER of which is a value measured live this run, taken
    greedily disjoint from the front.  Live values are excluded because
    exchanging one moves a DESIGNATED statement as well, and a probe that fires
    two rows cannot show which row saw it."""
    out, used = [], set()
    for k in range(len(figs) - 1):
        a, b = figs[k][1], figs[k + 1][1]
        if k in used or k + 1 in used:
            continue
        if a == b or len(a) != len(b) or a in live or b in live:
            continue
        out.append((k, k + 1))
        used.update({k, k + 1})
        if len(out) == limit:
            break
    return out


def pick_triple(figs, live):
    """The first three DISTINCT, EQUAL-LENGTH, non-live tokens at distinct
    slots -- the material for a 3-cycle.  Returns None where a site has none,
    which is reported as an ABSENCE rather than passed over."""
    by_len = {}
    for k, (_o, t) in enumerate(figs):
        if t in live:
            continue
        by_len.setdefault(len(t), [])
        if t not in [figs[m][1] for m in by_len[len(t)]]:
            by_len[len(t)].append(k)
        if len(by_len[len(t)]) == 3:
            return sorted(by_len[len(t)])
    return None


# --------------------------------------------------------------------------
# C -- THE CENSUS, ON DISK, AGAINST THE REAL RUNNER
# --------------------------------------------------------------------------
def order_row(out, site):
    for l in out.split("\n"):
        s = l.strip()
        if f"GATE @ {site}: FIGURE ORDER" in s and s.startswith("["):
            return s[:11]
    return None


def census_row(out, site):
    for l in out.split("\n"):
        s = l.strip()
        if f"GATE @ {site}: FIGURE CENSUS --" in s and s.startswith("["):
            return s[:11]
    return None


def crashed(out):
    """⚠️ THE RUNNER CAN EXIT 1 WITHOUT THE GATE HAVING SEEN ANYTHING.  Its
    negative control lifts three literal strings out of the live documents
    (`CHAIN`, `H8_TABLE`, `H8_HIST_ROW`) and `assert`s each occurs exactly
    once, so an edit AT THOSE SITES raises AssertionError instead of reporting.
    An exit code is not a verdict unless you know which produced it."""
    return "Traceback (most recent call last)" in out


def gate_rows(rows):
    return [r for r in rows if r.startswith("GATE @")]


def c_census(pristine):
    head("C -- THE CENSUS, ON DISK, AGAINST THE REAL RUNNER (mg-8aae H-1)")
    print("""Every mutation below is WRITTEN TO DISK and scored by running
`verify_landing.py` as a SUBPROCESS.  mg-8eca's N15-N18 call `figure_gate` on
in-memory strings; that is a fixture and is not evidence here.  The pairs are
chosen by the procedure in `pick_pairs`, not by hand, and §14 -- a site
mg-8eca's own battery never exchanged -- is included on the same footing.
""")
    rc, out = run_verify()
    record(rc == 0, f"C0 the real runner on the clean tree exits {rc} "
                    f"({len(refuted_rows(out))} refuted rows)")

    live, (a, b, h) = live_values()
    print(f"\n    live figures this run: {sorted(live)}")
    print(f"    a(cell)={a:,}  b(§14 copy)={b:,}  h(row history)={h:,}\n")

    S = sites()
    figs = {}
    for name, (_p, _o, txt) in S.items():
        figs[name] = scan_figures(txt)
    ok = True
    for name in DECLARED_SLOTS:
        n, want = len(figs[name]), DECLARED_SLOTS[name]
        print(f"    {name:<20} my reader finds {n:>3} asserted figure tokens, "
              f"the roster declares {want:>3} slots  "
              f"{'ok' if n == want else '<-- DISAGREE'}")
        ok = ok and n == want
    record(ok, "C1 my own reader -- which shares no regex with the gate, scans "
               "character by character and MASKS quotations in place rather "
               "than deleting them -- finds the same number of asserted figure "
               "tokens at each site as the roster declares slots, 3 of 3.  A "
               "probe built on a reader that disagreed with the roster would "
               "be exchanging tokens the gate never looks at")

    print(f"\n    {'probe':<50}{'exit':>6}{'FIG ORDER':>12}{'CENSUS':>12}"
          f"{'gate rows':>11}{'crash':>7}")
    fired = only = licensed = involution = 0
    crashes, selftest = 0, 0
    total = 0
    for name, (path, off, txt) in S.items():
        pairs = pick_pairs(name, figs[name], live)
        for (i, j) in pairs:
            total += 1
            ti, tj = figs[name][i][1], figs[name][j][1]
            mutated = swap_tokens(txt, i, j, figs[name])
            assert len(mutated) == len(txt), "not length-preserving"
            assert mutated != txt
            try:
                splice(path, off, txt, mutated)
                rc, out = run_verify()
                omark = order_row(out, name)
                cmark = census_row(out, name)
                bad = refuted_rows(out)
                g = gate_rows(bad)
                is_only = (len(g) == 1
                           and g[0].startswith(f"GATE @ {name}: FIGURE ORDER"))
                fired += rc != 0
                only += is_only
                licensed += cmark == "[CONFIRMED]"
                crashes += crashed(out)
                selftest += len(bad) - len(g) > 0
                # the involution control: apply the same exchange again
                figs2 = scan_figures(mutated)
                back = swap_tokens(mutated, i, j, figs2)
                involution += back == txt
            finally:
                write(path, pristine[path])
            print(f"    {name + ': ' + ti + ' <-> ' + tj:<50}{rc:>6}"
                  f"{str(omark).strip('[] '):>12}{str(cmark).strip('[] '):>12}"
                  f"{len(g):>11}{str(crashed(out)):>7}")

    record(fired == total,
           f"C2 EVERY EXCHANGE WRITTEN TO DISK MAKES THE REAL RUNNER RED: "
           f"{fired} of {total}, at 3 of 3 sites, with no environment variable "
           f"set and the gate never called in memory.  This is the mutation "
           f"mg-8aae observed at exit 0")
    record(only == total,
           f"C3 and the `FIGURE ORDER` row FOR THAT SITE is the ONLY GATE row "
           f"that failed: {only} of {total}.  A run that went red for some "
           f"other reason would keep the headline and lose the result")
    record(licensed == total,
           f"C4 and that site's licensing (multiset) row stayed [CONFIRMED]: "
           f"{licensed} of {total}.  That is THE ARTIFACT'S OWN evidence that "
           f"each mutation was a permutation and nothing else -- asserted by "
           f"the thing being audited, not by the prober")
    record(involution == total,
           f"C5 each exchange applied TWICE returns the site byte-identical: "
           f"{involution} of {total}.  A transposition is its own inverse, so "
           f"'both orderings' of ONE pair is one text -- which is why C6 asks "
           f"the question with a 3-cycle instead")

    # ⚠️ C7 -- THE EXIT CODE IS NOT ALWAYS THE GATE'S.
    record(crashes == 0,
           f"C7 the runner REPORTED rather than CRASHED on {total - crashes} of "
           f"{total} exchanges -- it raised AssertionError out of its own "
           f"negative control on {crashes}.  An exit code produced by a "
           f"traceback is not a gate verdict, and here the two are the same "
           f"integer")
    if crashes:
        finding("J-3",
                f"THE RUNNER'S OWN NEGATIVE CONTROL CRASHES ON EDITS AT ITS "
                f"OWN PROBE SITES, AND THE CRASH IS INDISTINGUISHABLE FROM A "
                f"FIRE.  mg-8eca's `transpose` lifts three literals out of the "
                f"live documents -- `CHAIN`, `H8_TABLE`, `H8_HIST_ROW` -- and "
                f"`assert`s each occurs exactly once in the site.  An edit at "
                f"those exact lines, INCLUDING THE VERY EXCHANGE THE CONTROL "
                f"EXISTS TO MODEL, raises AssertionError: {crashes} of {total} "
                f"exchanges here, and E2 below where the gate saw NOTHING and "
                f"the run still exited 1.  A reader who reads the exit code "
                f"concludes the gate caught it.  It did not.  The fix is the "
                f"one the census itself already uses: locate the probe text BY "
                f"CONTENT and fail with a message, not by a frozen literal and "
                f"an assert.")
    record(selftest == 0,
           f"C7b and the runner's negative-control SELF-TEST row went red on "
           f"{selftest} of {total} exchanges, because the battery evaluates its "
           f"own 18 mutations against the MUTATED site texts.  It is a true "
           f"report of a tree nobody should ship, not a gate row -- but it is "
           f"why C3 is scored over GATE rows and not over every refuted line")

    # C6 -- 3-cycles, both cyclic senses.
    print()
    rot_fired, rot_total, absent = 0, 0, []
    for name, (path, off, txt) in S.items():
        tri = pick_triple(figs[name], live)
        if tri is None:
            absent.append(name)
            print(f"    {name:<20} NO triple of distinct equal-length non-live "
                  f"tokens exists at this site -- reported as an ABSENCE")
            continue
        for back in (False, True):
            rot_total += 1
            mutated = rotate_tokens(txt, tri, figs[name], back=back)
            assert len(mutated) == len(txt)
            try:
                splice(path, off, txt, mutated)
                rc, out = run_verify()
                mark = order_row(out, name)
                rot_fired += rc != 0 and mark == "[REFUTED  ]"
            finally:
                write(path, pristine[path])
            toks = [figs[name][k][1] for k in tri]
            print(f"    {name}: 3-cycle {'backward' if back else 'forward'} "
                  f"{toks} -> exit {rc}, FIGURE ORDER {mark}")
    record(rot_fired == rot_total and rot_total > 0,
           f"C6 3-CYCLES IN BOTH CYCLIC SENSES fire: {rot_fired} of "
           f"{rot_total}.  A 3-cycle is the smallest permutation with two "
           f"distinct orderings, so this is where 'both orderings' can actually "
           f"be asked.  Sites with no such triple: {absent or 'none'}")


# --------------------------------------------------------------------------
# E -- DID THE FIX MOVE THE INVARIANCE?
# --------------------------------------------------------------------------
def swap_row_labels(text, line1, line2):
    """Exchange the LABEL field of two table rows, keeping each line's length
    and leaving every numeric column exactly where it was.  The colon is at the
    same offset in both rows, so the swap is length-preserving by
    construction."""
    out = []
    for src, other in ((line1, line2), (line2, line1)):
        i, j = src.index(":"), other.index(":")
        lab = other[:j].rstrip()
        pad = i - len(lab)
        assert pad >= 1, (lab, i)
        out.append(lab + " " * pad + src[i:])
    assert len(out[0]) == len(line1) and len(out[1]) == len(line2)
    return text.replace(line1 + "\n" + line2,
                        out[0] + "\n" + out[1], 1)


BB_L1 = "    STATE.md row cell                          :   9 748 chars"
BB_L2 = "    this file (the relocated history)          :  10 483 chars"

E_PROBES = [
    ("E2 H8: the two LABELS exchanged, the figures left alone",
     HIST,
     "STATE.md row  before mg-a2bd :  13 551 chars\n"
     "    STATE.md row  after  mg-a2bd :  16 692 chars",
     "STATE.md row  after  mg-a2bd :  13 551 chars\n"
     "    STATE.md row  before mg-a2bd :  16 692 chars",
     "SILENT",
     "the table now says the `STATE.md` row SHRANK across mg-a2bd -- "
     "mg-8aae's own H-1 defect, reached by moving the OTHER half of the pair"),
    ("E2b H8: two LABELS exchanged AWAY from the control's own literals",
     HIST, BB_L1 + "\n" + BB_L2, None,
     "SILENT",
     "the `bbe83b5` table now says the `STATE.md` row cell was 10 483 and the "
     "relocated history 9 748 -- the two figures swapped, without either "
     "figure moving, at a site mg-8eca's negative control does not hard-code"),
    ("E3 H8: the two historical COLUMN HEADERS exchanged",
     HIST,
     "at bbe83b5^    at bbe83b5  AFTER mg-8e30",
     "at bbe83b5     at bbe83b5^ AFTER mg-8e30",
     "SILENT",
     "every historical column of the three-column table is now attributed to "
     "the wrong commit, and the figures never moved"),
    ("E4 H8: two ROW LABELS exchanged INSIDE the designated table",
     HIST,
     "    gap, cell only                                        −875"
     "          +755        +2 744\n"
     "    gap, cell + relocated history                       +9 608"
     "       +17 023       +23 771",
     "    gap, cell + relocated history                         −875"
     "          +755        +2 744\n"
     "    gap, cell only                                      +9 608"
     "       +17 023       +23 771",
     "FIRES",
     "the label is what the designated reader keys on, so THIS label swap is "
     "caught -- which is exactly what marks the boundary E2/E3 sit outside"),
]


def e_invariance(pristine):
    head("E -- DID THE FIX MOVE THE INVARIANCE, OR REMOVE IT?")
    print("""An exchange has two halves: the FIGURES, and the STATEMENTS they are
attached to.  mg-8eca closed the first.  E2 and E3 exchange the second and
reproduce mg-8aae's own reader-visible defect from the other side.  NOTHING IN
THE ASSIGNMENT NAMES THESE -- they are this audit's own item.

E1 first, because it is the one mg-8eca DECLARES uncovered.
""")
    # E1 -- the declared non-coverage, checked rather than repeated.
    t = read(HIST)
    n875 = t.count("−875")
    record(True,
           f"E1 two occurrences of the SAME token exchanged: the exchange is "
           f"the IDENTITY ON THE BYTES.  `−875` occurs {n875}x in the row "
           f"history; exchanging any two of them changes 0 characters, so "
           f"there is no artifact to detect and mg-8eca's declaration -- "
           f"'the identity map on values' -- is true BY CONSTRUCTION, not by "
           f"luck.  A reader who moved the two STATEMENTS instead would be "
           f"doing E2")

    print(f"\n    ⚠️ SCORED AT GATE GRANULARITY.  `exit` is the runner's; "
          f"`gate rows` is how many\n       GATE rows it refuted.  They are "
          f"not the same measurement, and E2 is why.\n")
    print(f"    {'probe':<58}{'pred':>8}{'exit':>6}{'gate':>6}{'crash':>7}"
          f"{'observed':>10}")
    silent_at_gate = 0
    for label, path, old, new, predicted, why in E_PROBES:
        t = read(path)
        if new is None:                       # the label swap, built in code
            a, b = old.split("\n")
            assert t.count(old) == 1, (label, t.count(old))
            mutated = swap_row_labels(t, a, b)
            assert len(mutated) == len(t), label
        else:
            assert t.count(old) == 1, (label, t.count(old))
            assert len(new) == len(old), (label, len(old), len(new))
            mutated = t.replace(old, new, 1)
        try:
            write(path, mutated)
            rc, out = run_verify()
            bad = refuted_rows(out)
            g = gate_rows(bad)
        finally:
            write(path, pristine[path])
        observed = "SILENT" if len(g) == 0 else "FIRES"
        print(f"    {label:<58}{predicted:>8}{rc:>6}{len(g):>6}"
              f"{str(crashed(out)):>7}{observed:>10}")
        agree = observed == predicted
        if label.startswith("E4"):
            record(agree and rc != 0,
                   f"E4 the row-label exchange INSIDE the designated table "
                   f"FIRES ({len(g)} gate rows refuted), and the rows that "
                   f"failed are READ AT THE SITE rows rather than FIGURE "
                   f"ORDER.  That is the boundary: a label is checked exactly "
                   f"where a designated reader keys on it, and nowhere else")
            for r in g[:4]:
                print(f"        refuted: {r[:120]}")
        else:
            silent_at_gate += observed == "SILENT"
            record(agree,
                   f"{label} -> {len(g)} gate rows refuted ({observed}), "
                   f"predicted {predicted}"
                   + (f"; the runner still exited {rc}, BY CRASH, not by the "
                      f"gate" if crashed(out) else f"; runner exit {rc}"))
            if observed == "SILENT":
                finding(label.split()[0],
                        f"THE CENSUS IS POSITION-AWARE OVER FIGURES, NOT OVER "
                        f"THE CLAIMS THEY ARE ATTACHED TO.  {why}.  The "
                        f"mutation is length-preserving, leaves every figure "
                        f"token in its declared slot, and the gate refutes "
                        f"NOTHING"
                        + (" -- the run's exit 1 is an AssertionError out of "
                           "its own negative control (see J-3), which is a "
                           "different sentence and the same integer"
                           if crashed(out) else ", at exit 0"))
    record(silent_at_gate == 3,
           f"E2/E2b/E3 THE INVARIANCE MOVED, IT DID NOT GO AWAY: "
           f"{silent_at_gate} of 3 label-side exchanges leave the gate silent. "
           f"An exchange has two halves -- the figures, and the statements they "
           f"are attached to -- and mg-8eca closed the first.  The reader-"
           f"visible defect mg-8aae raised (H8's table saying the row SHRANK "
           f"across mg-a2bd) is reproducible today from the other half")

    # E5 -- a figure moved to a different SITE with the same value.  `48 846`
    # is declared at H8 and `44 055` at §14; they are exchanged ACROSS the two
    # sites.  Both are 6 characters, both sit in ordinary prose, and neither is
    # a live measurement -- so `a`, `b` and `h` are untouched and the only
    # thing that moved is which site asserts which declared figure.
    print()
    S = sites()
    p14, o14, t14 = S["§14"]
    ph8, oh8, th8 = S["H8"]
    assert t14.count("44 055") == 1 and th8.count("48 846") == 1
    try:
        splice(p14, o14, t14, t14.replace("44 055", "48 846", 1))
        splice(ph8, oh8, th8, th8.replace("48 846", "44 055", 1))
        rc, out = run_verify()
        bad = refuted_rows(out)
    finally:
        write(HIST, pristine[HIST])
        write(DELIV, pristine[DELIV])
    record(rc != 0,
           f"E5 a figure MOVED TO A DIFFERENT SITE at the same value -- H8's "
           f"declared `48 846` and §14's declared `44 055` exchanged ACROSS the "
           f"two sites, length-preserving, no live figure touched -- makes the "
           f"runner red (exit {rc}, {len(bad)} refuted rows).  A cross-site "
           f"move changes both sequences AND both multisets, so this one the "
           f"roster sees twice over")
    for r in bad[:5]:
        print(f"        refuted: {r[:120]}")


# --------------------------------------------------------------------------
# D -- `SUMMARY vs ROWS` ON THE REAL ARTIFACT
# --------------------------------------------------------------------------
ROW1_OLD = "record(a == 12692 and h == 18593 and b == 10623,"
ROW2_OLD = "record(a - b == 2069 and a + h - b == 20662,"
COND_OLD = "    agree = printed == derived and said == owed"
HEAD_OLD = ('    out = [f"  THE PRIMARY TARGET IS {verdict} IN THIS TREE: "\n'
            '           f"{len(bad)} of {len(rows)} rows tagged",')
DEFECT_NEW = ("    printed = FORCE_SUMMARY or derived\n"
              "    said = owed")


def d_summary(pristine, live_abh):
    head("D -- `SUMMARY vs ROWS` ON THE REAL ARTIFACT (mg-8aae H-2)")
    a, b, h = live_abh
    print(f"""Run as a subprocess with MG8916_FORCE_SUMMARY UNSET except where the row
says otherwise.  There are exactly TWO rows tagged PRIMARY, and their
expectations are constants frozen in the audited instrument's own source; the
source says a later commit that legitimately moves them makes these rows
refuted on a re-run, which is the state this tree is in (a={a:,} h={h:,}
b={b:,} against 12,692 / 18,593 / 10,623).

So the ROW direction is taken by EDITING THE ROW -- on disk, in the real file,
with no environment variable -- and not by editing `STATE.md`, the deliverable
and the row history, which the audited instrument's own dirty-tree guard
`SystemExit(2)`s over before the bottom line is ever reached.
""")
    src = pristine[AUDIT_8A5C]
    assert src.count(ROW1_OLD) == 1 and src.count(ROW2_OLD) == 1
    assert src.count(COND_OLD) == 1 and src.count(HEAD_OLD) == 1

    row1_live = f"record(a == {a} and h == {h} and b == {b},"
    row2_live = f"record(a - b == {a - b} and a + h - b == {a + h - b},"

    def probe(label, mutate, env=None):
        try:
            write(AUDIT_8A5C, mutate(src))
            rc, out = run_8a5c(env)
        finally:
            write(AUDIT_8A5C, pristine[AUDIT_8A5C])
        mark, line = summary_row(out)
        return rc, mark, line, out

    # ---- D-row: move a ROW, across every achievable state of the rows.
    states = [
        ("D1 2 of 2 PRIMARY rows refuted (the tree as it stands)",
         lambda s: s),
        ("D2 1 of 2 refuted (row 1's expectation brought up to live)",
         lambda s: s.replace(ROW1_OLD, row1_live, 1)),
        ("D3 0 of 2 refuted (both expectations brought up to live)",
         lambda s: s.replace(ROW1_OLD, row1_live, 1)
                    .replace(ROW2_OLD, row2_live, 1)),
    ]
    print(f"    {'state of the rows':<58}{'exit':>6}{'SUMMARY vs ROWS':>18}")
    green = 0
    for label, mut in states:
        rc, mark, line, out = probe(label, mut)
        prim = [l for l in out.split("\n") if "THE PRIMARY TARGET IS" in l
                and "record" not in l]
        green += mark == "[CONFIRMED]"
        print(f"    {label:<58}{rc:>6}{str(mark):>18}")
        for p in prim[:1]:
            print(f"        the bottom line a reader gets: {p.strip()[:120]}")
        if line:
            print(f"        {line[11:][:150]}")
    record(green == 3,
           "D4 NO ACHIEVABLE STATE OF THE ROWS MAKES `SUMMARY vs ROWS` FIRE: "
           "0, 1 and 2 of 2 PRIMARY rows refuted, all three green, all three "
           "on disk with no environment variable.  The assignment's direction "
           "-- edit a row so it disagrees with the summary -- CANNOT BE DONE, "
           "and that is the measurement, not a failure of the probe")

    # ---- D-text: mg-8eca's own direction, re-taken on disk.
    print()
    head_confirmed = HEAD_OLD.replace("{verdict}", "CONFIRMED")
    head_count = HEAD_OLD.replace("{len(bad)}", "{len(rows) - len(bad)}")
    head_both = (HEAD_OLD.replace("{verdict}", "CONFIRMED")
                 .replace("{len(bad)}", "{len(rows) - len(bad)}"))
    texts = [
        ("D5 the REFUTED headline edited to a literal CONFIRMED "
         "(mg-8aae's direction 2)",
         lambda s: s.replace(HEAD_OLD, head_confirmed, 1), None),
        ("D6 the COUNT edited, the verdict word left correct",
         lambda s: s.replace(HEAD_OLD, head_count, 1), None),
        ("D7 a COHERENT false summary -- headline AND count both moved",
         lambda s: s.replace(HEAD_OLD, head_both, 1), None),
        ("D8 mg-8916's hook, kept: MG8916_FORCE_SUMMARY=CONFIRMED",
         lambda s: s, {"MG8916_FORCE_SUMMARY": "CONFIRMED"}),
    ]
    print(f"    {'direction':<66}{'exit':>6}{'SUMMARY vs ROWS':>18}")
    red = 0
    for label, mut, env in texts:
        rc, mark, line, out = probe(label, mut, env)
        red += mark == "[REFUTED  ]"
        print(f"    {label:<66}{rc:>6}{str(mark):>18}")
    record(red == 4,
           f"D5-D8 all four directions make the check fire: {red} of 4.  D5-D7 "
           f"set NO environment variable and edit the REAL FILE ON DISK the way "
           f"G-2 was actually made -- so mg-8eca's headline claim, that the "
           f"check no longer fires only through the hook, HOLDS")

    # ---- D-del: the deletion test, at the finest unit that has a return.
    print()
    print("""    THE DELETION TEST, AT THE FINEST UNIT THAT HAS A RETURN.  The repaired
    condition is `agree = printed == derived and said == owed`.  Two clauses of
    one condition are not one unit: deleting them together tests neither.  So
    each is deleted ON ITS OWN and every direction above is re-scored.
""")
    dels = [
        ("D9  `printed == derived` REMOVED",
         lambda s: s.replace(COND_OLD, "    agree = said == owed", 1)),
        ("D10 `said == owed` REMOVED",
         lambda s: s.replace(COND_OLD, "    agree = printed == derived", 1)),
        ("D11 the defect REINSTATED (printed = FORCE_SUMMARY or derived)",
         lambda s: s.replace(COND_OLD, DEFECT_NEW + "\n" + COND_OLD, 1)),
    ]
    grid = {}
    short = [t[0].split()[0] for t in texts]
    print(f"    {'deletion':<52}" + "".join(f"{n:>7}" for n in short))
    for dlabel, dmut in dels:
        row = []
        for tlabel, tmut, env in texts:
            rc, mark, line, out = probe(dlabel, lambda s: tmut(dmut(s)), env)
            row.append(mark)
        grid[dlabel] = row
        print(f"    {dlabel:<52}"
              + "".join(f"{('RED' if m == '[REFUTED  ]' else 'green'):>7}"
                        for m in row))

    d9 = grid["D9  `printed == derived` REMOVED"]
    d10 = grid["D10 `said == owed` REMOVED"]
    d11 = grid["D11 the defect REINSTATED (printed = FORCE_SUMMARY or derived)"]
    RED = "[REFUTED  ]"
    record(all(m != RED for m in d11[:3]),
           f"D11 THE CONTROL: with the defect reinstated, all three ON-DISK "
           f"directions go green again ({[m for m in d11[:3]]}).  Without this "
           f"row, 'the check fires' and 'the instrument fires' are the same "
           f"sentence")

    isolates9 = [texts[i][0].split()[0] for i in range(4) if d9[i] != RED]
    isolates10 = [texts[i][0].split()[0] for i in range(4) if d10[i] != RED]
    record(len(isolates10) > 0,
           f"D10 deleting `said == owed` alone MOVES SOMETHING: the directions "
           f"that go green are {isolates10}.  The clause has a return of its "
           f"own")
    record(len(isolates9) > 0,
           f"D9 deleting `printed == derived` alone MOVES SOMETHING: the "
           f"directions that go green are {isolates9}.  The clause has a return "
           f"of its own")

    off_hook = [x for x in isolates9 if x != "D8"]
    mg8eca = [x for x in isolates9 if x in ("D5", "D6", "D8")]
    record(mg8eca == ["D8"] or mg8eca == [],
           f"D12 OF THE DIRECTIONS mg-8eca DECLARES (D5, D6 and the hook D8), "
           f"the ones that isolate `printed == derived` are {mg8eca or 'none'}")
    if mg8eca == ["D8"]:
        finding("J-2",
                "HALF THE REPAIRED CONDITION IS STILL DEMONSTRATED ONLY "
                "THROUGH THE HOOK.  `agree = printed == derived and said == "
                "owed`.  Deleting `printed == derived` alone leaves mg-8eca's "
                "own on-disk directions D5 (headline) and D6 (count) STILL "
                "RED, because `said == owed` fires on both -- with 2 PRIMARY "
                "rows and 2 refuted, an edited headline moves the count's "
                "expectation from (2,2) to (0,2) as a side effect.  The only "
                "declared probe that isolates the clause is "
                "MG8916_FORCE_SUMMARY, the environment variable.  D7 -- a "
                "COHERENT false summary, headline and count moved together, "
                "which is what a hand-writer producing G-2 would actually "
                "write -- does isolate it on disk with no env var, and is this "
                "audit's construction, not mg-8eca's.  The clause is NOT "
                "inert; mg-8eca's battery just does not show it.")
    if off_hook:
        record(True,
               f"D12b and it IS isolable off the hook: {off_hook} does it on "
               f"disk with no environment variable.  The clause is load-bearing; "
               f"what is missing is the probe, not the code")


def d_independence(pristine):
    """The second question the assignment asks: two independent derivations, or
    one value read twice?  Answered from the SOURCE, at the two branches."""
    head("D-ind -- ARE THE TWO SIDES INDEPENDENT DERIVATIONS?")
    src = pristine[AUDIT_8A5C]
    refuted_branch = ('f"  THE PRIMARY TARGET IS {verdict} IN THIS TREE: "'
                      in src and 'f"{len(bad)} of {len(rows)} rows tagged"'
                      in src)
    confirmed_branch = ('"  THE PRIMARY TARGET IS CONFIRMED: the repair'
                        in src)
    print("""    On the CONFIRMED branch the verdict word is a LITERAL, so parsing it
    back is a genuinely second read of a hand-written string.  On the REFUTED
    branch it is `{verdict}` -- the same expression `derived` recomputes -- and
    the count is `{len(bad)}`, the same expression `owed` recomputes.  With
    exactly two PRIMARY rows, every achievable state agrees by construction,
    which is what D1-D4 measured on disk.
""")
    record(refuted_branch and confirmed_branch,
           "D-ind the REFUTED branch interpolates `{verdict}` and `{len(bad)}` "
           "into the sentence that the check then parses back out; the "
           "CONFIRMED branch writes the verdict as a literal.  Both read from "
           "the source, not from a re-run")
    finding("J-1",
            "THE TWO SIDES ARE INDEPENDENT WITH RESPECT TO THE PRINTED TEXT, "
            "NOT WITH RESPECT TO THE ROWS -- and the row's own wording claims "
            "the wider one.  It says the sentence is 'READ BACK OUT OF THE "
            "LINES THIS RUN WILL PRINT' and that its PRIMARY rows are "
            "'counted again here', which reads as two derivations of the same "
            "quantity meeting.  On the REFUTED path they are one: the printed "
            "verdict is `{verdict}` and the printed count is `{len(bad)}`, "
            "which are the two expressions the other side recomputes, so the "
            "round trip is a regex through an f-string.  D1-D4 show it on "
            "disk: 0, 1 and 2 of 2 PRIMARY rows refuted, all three green.  "
            "WHAT THE CHECK ACTUALLY DISCRIMINATES is an edit to "
            "`primary_summary`'s OWN SOURCE TEXT -- which is real, is not a "
            "hook, and is exactly how G-2 was made, so H-2 is CLOSED.  The "
            "EXTENT is narrower than the sentence printed beside it, which is "
            "the same shape as both of mg-8aae's findings.")


# --------------------------------------------------------------------------
# S -- DO NOT DISTURB WHAT IS CONFIRMED
# --------------------------------------------------------------------------
def own_rows(out):
    """The instrument's OWN check rows, which are printed at exactly two spaces
    of indent.  Deeper indents are ECHOED OUTPUT of the sub-runs it drives, and
    counting those is how a re-run of a healthy instrument comes to look red:
    mg-8aae echoes six `[REFUTED  ]` GATE lines that are its probes WORKING."""
    marks = {"[CONFIRMED]": [], "[REFUTED  ]": [], "[MEASURED ]": []}
    for l in out.split("\n"):
        if l.startswith("  ") and not l.startswith("   "):
            for m in marks:
                if l[2:].startswith(m):
                    marks[m].append(l[2 + len(m):].strip())
    return marks


def s_undisturbed():
    head("S -- DO NOT DISTURB WHAT IS CONFIRMED")
    print("""mg-8aae's 12 of 12 at ROW granularity and its G-1 closure are re-taken by
RE-RUNNING mg-8aae's own instrument, unmodified, rather than by quoting its
verdict or mg-8eca's.  Likewise mg-8916's.  Both are slow; both are run once.

⚠️ THE POPULATION IS NAMED, because a bare total here is wrong twice over.  A
row is counted only if the instrument printed it AS ITS OWN, at two spaces of
indent; the deeper-indented `[REFUTED  ]` lines are ECHOES of the sub-runs it
drives and are its probes WORKING.  And "checks" means confirmed + measured +
refuted, which is how mg-8916's 16 confirmed and 2 measurements come to 18.
""")
    runs = {}
    for tag, path in [
            ("S1", "code/hodge_leverage_audit_8aae/audit_8916_repair.py"),
            ("S2", "code/hodge_leverage_repair_8916/repair_835f.py")]:
        r = subprocess.run([sys.executable, os.path.join(REPO, path)],
                           capture_output=True, text=True, cwd=REPO)
        out = r.stdout + r.stderr
        runs[tag] = (r.returncode, out, own_rows(out))

    rc, out, rows = runs["S1"]
    nf = len([l for l in out.split("\n") if "[FINDING" in l])
    ref = rows["[REFUTED  ]"]
    n = sum(len(v) for v in rows.values())
    record(nf == 0,
           f"S1 mg-8aae's own `audit_8916_repair.py`, UNMODIFIED, on this tree: "
           f"{n} of its own rows ({len(rows['[CONFIRMED]'])} confirmed, "
           f"{len(rows['[MEASURED ]'])} measured, {len(ref)} refuted), "
           f"{nf} FINDINGS, exit {rc}")
    for l in ref:
        print(f"        its one refuted row: {l[:150]}")
    record(len(ref) == 1 and "permutation probes" in ref[0],
           "S1b and the single refuted row is A4's OWN permutation row -- the "
           "row that RAISED H-1, now false because the gate fires.  Its "
           "predictions are left as written and read `PREDICTION MISSED` at 2 "
           "of 2 sites.  That is what a landed finding looks like from the "
           "raising instrument's side, and it is why exit 1 here is not a "
           "regression")

    a2 = [l for l in rows["[CONFIRMED]"] if "12 of 12" in l]
    for l in a2:
        print(f"        {l[:160]}")
    record(len(a2) >= 3,
           f"S2 THE 12 OF 12 SURVIVES THE WIDENING AT ROW GRANULARITY: "
           f"{len(a2)} of mg-8aae's own A2 rows read 12 of 12 -- the runner "
           f"goes red, the row that failed is the `READ AT THE SITE` row FOR "
           f"THAT FIGURE, and all 12 restorations return it to exit 0.  "
           f"Nothing here is quoted from mg-8eca")

    g1 = [l for l in rows["[CONFIRMED]"]
          if "U1" in l and ("GATE FIRES" in l or "3 of 3" in l)]
    for l in g1:
        print(f"        {l[:160]}")
    record(len(g1) >= 1,
           f"S3 and G-1 stays closed against the AUDITOR'S OWN wording: "
           f"{len(g1)} of mg-8aae's rows report its own prose probes at 3 of 3, "
           f"in slots it chose by procedure and controlled green before use")

    rc, out, rows = runs["S2"]
    n = sum(len(v) for v in rows.values())
    record(rc == 0 and len(rows["[REFUTED  ]"]) == 0 and n == 18,
           f"S4 mg-8916's own `repair_835f.py`, UNMODIFIED: {n} checks "
           f"({len(rows['[CONFIRMED]'])} confirmed, "
           f"{len(rows['[MEASURED ]'])} measured, "
           f"{len(rows['[REFUTED  ]'])} refuted), exit {rc}.  mg-8eca's own "
           f"claim is '18 checks / 0 refuted at exit 0'; counted here from its "
           f"own rows, with the population named, it holds -- 18 is 16 + 2 + 0, "
           f"not 18 confirmations")


# --------------------------------------------------------------------------
def main():
    print("=" * 78)
    print("mg-9207 -- INDEPENDENT AUDIT OF THE mg-8eca REPAIR (d59ecd9 + bee07a1)")
    print("=" * 78)
    print(__doc__.split("PREDICTED EXIT CODE")[0].rstrip())

    head("GUARD -- THE TREE THIS RUN WILL RESTORE")
    dirty = "\n".join(l for l in git("status", "--porcelain", "--", *MUTABLE)
                      .strip().split("\n") if l.strip())
    if dirty:
        print("  REFUSING TO RUN: a file this run will restore is already dirty.")
        for l in dirty.split("\n"):
            print("    " + l)
        raise SystemExit(2)
    pristine = {p: read(p) for p in MUTABLE}
    before = {p: sha(p) for p in MUTABLE}
    frozen_before = {p: sha(p) for p in FROZEN}
    print(f"  {len(MUTABLE)} mutable files read and sha256-pinned; "
          f"{len(FROZEN)} committed transcripts pinned frozen")

    _live, abh = live_values()
    try:
        c_census(pristine)
        e_invariance(pristine)
        d_summary(pristine, abh)
        d_independence(pristine)
        s_undisturbed()
    finally:
        for p in MUTABLE:
            write(p, pristine[p])

    head("RESTORATION AND THE FROZEN RECORD")
    after = {p: sha(p) for p in MUTABLE}
    record(after == before,
           f"restoration CHECKED by sha256, not asserted: all {len(MUTABLE)} "
           f"mutated files are byte-identical to what this run read")
    fafter = {p: sha(p) for p in FROZEN}
    record(fafter == frozen_before,
           f"all {len(FROZEN)} committed transcripts this run's instruments "
           f"could have regenerated are byte-identical afterwards -- including "
           f"`out_verify.txt`, which is why this instrument runs "
           f"`verify_landing.py` directly and never `run_all.sh`")
    left = git("status", "--porcelain", "--", *MUTABLE).strip()
    record(left == "", f"git status over the mutated files is clean: {left!r}")

    head("BOTTOM LINE")
    conf = sum(1 for _d, ok in RESULTS if ok is True)
    ref = sum(1 for _d, ok in RESULTS if ok is False)
    print(f"  {len(RESULTS)} checks: {conf} confirmed, {ref} refuted.")
    print(f"  {len(FINDINGS)} findings.")
    for tag, d in FINDINGS:
        print(f"    {tag}: {d[:110]}...")
    print()
    print("  VERDICT: PARTIAL." if FINDINGS else "  VERDICT: CLEAN.")
    raise SystemExit(1 if (FINDINGS or ref) else 0)


if __name__ == "__main__":
    main()
