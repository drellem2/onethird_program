"""mg-6bd1 — machinery for the INDEPENDENT AUDIT of mg-345e.

Written from the SOURCE DOCUMENTS, not from `lib345e.py`. It shares no line with it:
the ledger parser here is a two-pass split-on-pipes reader with an explicit
keyword scan, not a regex over the whole label cell, precisely so that mg-345e's
own Defect-1 failure mode (a quantifier that under-reads and drops edges) cannot
be inherited along with its result.

Exact rationals everywhere. No float on any path that decides anything.
"""

import os
import subprocess
from fractions import Fraction
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OPFORM = REPO / "docs" / "OneThird-lambda-std-Operative-Form.md"

#: THE COMMIT THIS AUDIT'S CORPUS IS READ AT (mg-20ee).
#:
#: b5 and the selftest print `NNN: <row>` -- line numbers into STATE.md, a file
#: mg-6bd1 does not own -- and they read it from the WORKING TREE.  ALREADY
#: FIRED: a re-run on 2026-08-13 moves the glossary row from :43 to :51 and the
#: mg-61bb row from :155 to :165, with EVERY ADJUDICATION IDENTICAL.  The same
#: read now serves the Op-Form ledger, which had not yet moved but is the same
#: construction and would have.
#:
#: CHOSEN ON A MEASUREMENT: at 52d290a -- the commit carrying these transcripts
#: -- STATE.md puts those rows at exactly :43 and :155, and all six committed
#: transcripts reproduce byte-identically.  Checked before one was edited.
AS_OF = "52d290a961872ca532973f7dbef9f0c1203a7c6e"

#: Override, for re-measuring against a different corpus: any commit-ish, or the
#: literal WORKTREE.  Unset is the pinned default and is the only value that
#: reproduces the committed transcripts.
AT = os.environ.get("PAIRBIAS_INDEP_AT", "").strip() or AS_OF


def read_at(rel):
    """REPO/rel as of AT.  Every `NNN:` this audit prints is an offset into
    THESE bytes, so pinning the bytes is what pins the addresses."""
    rel = str(rel)
    if rel.startswith(str(REPO)):
        rel = os.path.relpath(rel, str(REPO))
    if AT == "WORKTREE":
        return (REPO / rel).read_text()
    got = subprocess.run(["git", "-C", str(REPO), "show", "%s:%s" % (AT, rel)],
                         capture_output=True)
    if got.returncode != 0:
        raise SystemExit(
            "mg-6bd1: cannot read %s at %s: %s\n"
            "  (PAIRBIAS_INDEP_AT=%r; unset it for the pinned run.)"
            % (rel, AT, got.stderr.decode("utf-8", "replace").strip(), AT))
    return got.stdout.decode("utf-8", "replace")


# ----------------------------------------------------------------- ledger reader
#
# Deliberately NOT a regex over the label. Two passes:
#   pass 1 — cut the §9 table into rows by splitting on '|' and demanding the first
#            cell be an integer;
#   pass 2 — tokenise the label into words and walk it, so that a dependency clause
#            is recognised by POSITION after a keyword rather than by a pattern that
#            has to be told where to stop. An under-reading quantifier is the exact
#            defect mg-345e's selftest caught in its own parser; this reader cannot
#            have it, because it consumes numbers greedily by construction and then
#            has to be stopped explicitly.

KEYWORDS = ("on", "given")
STOPWORDS = {"claim", "claims", "the"}


def _ledger_rows(text):
    lines = text.split("\n")
    start = next(i for i, l in enumerate(lines) if l.startswith("## 9. Claim ledger"))
    rows = []
    for l in lines[start + 1:]:
        if l.startswith("---"):
            break
        if not l.startswith("|"):
            continue
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        # DEFECT OF THIS READER, KEPT IN THE SOURCE (mg-6bd1 §D1). The first form
        # demanded exactly 4 cells. Claim 1's statement contains `$|A|\le n/2$` —
        # LITERAL PIPES INSIDE MATH — so it splits into 6 and the row was dropped,
        # giving 35 rows and 10 edges against mg-345e's 36 and 11. The dropped row
        # was claim 1, which is a dependency of claim 17, so the 11th edge went with
        # it. mg-345e's greedy regex does NOT have this defect and ITS numbers are
        # right. Fix: id is the first cell, section and label are the LAST two, and
        # everything between is the statement.
        if len(cells) < 4:
            continue
        if not cells[0].isdigit():
            continue
        rows.append((int(cells[0]), " | ".join(cells[1:-2]), cells[-2], cells[-1]))
    return rows


def _strip_markup(s):
    for ch in "*`~$\\":
        s = s.replace(ch, " ")
    return s


def _deps_from_label(label, valid_ids):
    """Claim ids this label declares a dependency on.

    Walks tokens. After `on`/`given` (skipping `claim`/`claims`/`the`), consume every
    following token that is an integer or an integer with a trailing comma, and stop at
    the first token that is neither. Anything not in `valid_ids` is DROPPED and returned
    separately so it can be adjudicated rather than silently swallowed.
    """
    toks = _strip_markup(label).replace(",", " , ").split()
    deps, rejected = set(), []
    i = 0
    while i < len(toks):
        if toks[i].lower() in KEYWORDS:
            j = i + 1
            while j < len(toks) and toks[j].lower() in STOPWORDS:
                j += 1
            taken = False
            while j < len(toks):
                t = toks[j]
                if t == ",":
                    j += 1
                    continue
                if t.isdigit():
                    v = int(t)
                    if v in valid_ids:
                        deps.add(v)
                    else:
                        rejected.append(v)
                    taken = True
                    j += 1
                    continue
                break
            i = j if taken else i + 1
            continue
        i += 1
    return deps, rejected


def read_ledger(path=None):
    # mg-20ee: the CORPUS ledger is read at AT; an explicitly-passed path is a
    # SYNTHETIC FIXTURE (the selftest writes one) and must be read off disk --
    # pinning a fixture would look for it in a commit that never had it.
    text = read_at(OPFORM) if path is None else Path(path).read_text()
    rows = _ledger_rows(text)
    ids = {r[0] for r in rows}
    claims, edges, rejected = {}, {}, {}
    for cid, stmt, sec, label in rows:
        claims[cid] = (stmt, sec, label)
        d, rej = _deps_from_label(label, ids)
        edges[cid] = d
        if rej:
            rejected[cid] = rej
    return claims, edges, rejected


def ancestors(edges, cid):
    """Everything `cid` transitively depends on."""
    out, stack = set(), list(edges.get(cid, ()))
    while stack:
        c = stack.pop()
        if c in out:
            continue
        out.add(c)
        stack.extend(edges.get(c, ()))
    return out


def dependents(edges, target):
    return sorted(c for c in edges if target in ancestors(edges, c))


def edge_count(edges):
    return sum(len(v) for v in edges.values())


# ------------------------------------------------------------------ the algebra
#
# Every identity this audit needs, in exact rationals, derived here from the
# definitions rather than copied from mg-345e.

def C2(n):
    return Fraction(n * (n - 1), 2)


def eps_spec_from_Einv(E, n):
    """eps_spec such that E = (eps_spec/6)(n^2-1).  <=>  eps_spec = 6E/(n^2-1)."""
    return Fraction(6) * E / Fraction(n * n - 1)


def eps_c3ca_from_Einv(E, n):
    """mg-c3ca's normalisation (`OneThird-LIBweak-mg-c3ca.md` Prop 4.1): E <= eps*n^2."""
    return E / Fraction(n * n)


def frozen_sup_Einv(n, m):
    """The pair-bias ceiling: E[inv_e] < m/3 (Op-Form Claim 6.1)."""
    return Fraction(m, 3)


def E_unif_footrule(n):
    """E_unif[sum_i |sigma(i)-i|], by the closed form, for cross-checking brute force."""
    return Fraction(n * n - 1, 3)


def E_unif_footrule_bruteforce(n):
    from itertools import permutations
    tot, cnt = 0, 0
    for p in permutations(range(n)):
        tot += sum(abs(p[i] - i) for i in range(n))
        cnt += 1
    return Fraction(tot, cnt)


def E_unif_footrule_sum(n):
    """(1/n) * sum_{i,j} |j-i|, summed directly.  Independent of the closed form."""
    tot = sum(abs(j - i) for i in range(n) for j in range(n))
    return Fraction(tot, n)


def E_unif_inv(n):
    """E_unif[inv] = C(n,2)/2."""
    return C2(n) / 2


def asof_stamp():
    """The as-of block b5 and the selftest open the address screen with."""
    return """\
------------------------------------------------------------------------------
AS-OF STAMP -- WHICH LINES BELOW ARE ADDRESSES AND WHICH ARE FINDINGS (mg-20ee)
------------------------------------------------------------------------------
  corpus read at : %s
      %s

  EVERY `NNN:` PREFIXING A QUOTED ROW IS AN ADDRESS, NOT A FINDING.  It is an
  offset into STATE.md, a file this audit DOES NOT OWN, and it moves whenever
  pm-onethird amends it.  IT ALREADY HAD: read live on 2026-08-13 the glossary
  row is at :51 and the mg-61bb row at :165, against the :43 and :155 recorded
  here -- WITH EVERY ADJUDICATION IDENTICAL.  THE QUOTED ROW ITSELF IS THE
  PRIMARY ADDRESS: it survives STATE.md moving, the number does not.

  EVERYTHING ELSE IS STABLE: the rows-matched counts, the naive-grep confound
  count, the L4-token screens and every ADJUDICATION.  To re-ask against the
  current corpus:

      PAIRBIAS_INDEP_AT=HEAD sh run_all.sh    (or =WORKTREE, or any commit)
------------------------------------------------------------------------------
""" % (AT, "AS_OF, the pinned default" if AT == AS_OF
       else "OVERRIDE via PAIRBIAS_INDEP_AT -- NOT the as-of stamp " + AS_OF[:7])
