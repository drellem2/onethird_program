"""x2 — THE INDEX.  quantity -> every name and every tree that computes it.

The ticket's step 3: "BUILD THE INDEX, not a prose note.  The output that would have
prevented this is a lookup from quantity -> every name and every tree that computes it.
Prose describing the problem does not let the next thread check itself."

Two layers, and the difference between them is stated on every row rather than blurred:

  MEASURED  — the row exists because two or more trees COMPUTED THE SAME NUMBER for it.
              Rows come from `alias_groups.json`, written by `x3_values.py`.  I did not
              choose these; the values did.
  DECLARED  — the row exists because I looked the name up.  These are quantities the
              value probe cannot reach (families at large `n`, corpus-level scalars,
              quantities with no common poset argument).  A DECLARED row is a lead, not
              a finding, and is marked so on its face.

For every name in every row, x2 then sweeps the WHOLE corpus — not the 12 probed trees —
and reports each site as

  COMPUTES  a `.py` line that defines, assigns, or calls the symbol
  PRINTS    an `out_*.txt` transcript line carrying the token
  SAYS      a `.md` / `README` line carrying the token

because an audit QUOTING another tree's figure is not a second measurement of it (E3),
and an index that cannot tell those apart is worse than none.

Writes INDEX.md.  Exit 0 always: this arm is a census, not a verdict.
"""

import json
import os
import re
import sys
import time

import lib0d1b as L

t0 = time.time()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))       # .../code
REPO = os.path.dirname(ROOT)
SELF = os.path.basename(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- what a quantity is
#
# The MEASURED rows are keyed by the group's members, so the human-readable name of the
# quantity is the only thing here that is mine.  It is a LABEL, not a definition, and the
# definition is whichever tree's source you follow from the rows.

LABELS = [
    ("leak(A_1)", "leak(A_k) at the first prefix cut = E[#{i<k : pos(i)>=k}]"),
    ("gamma", "the spectral gap 1 - lambda_std of I - S_P on 1-perp"),
    ("Delta_P", "max_i d_i = max_i (1 - (S_P)_ii)"),
    ("Phi*_pref", "min over PREFIX cuts of leak(A_k)/min(k,n-k)"),
    ("mu_pref", "min of the Rayleigh quotient over the monotone cone"),
    ("rho*Delta_P", "(mu_pref/gamma) * Delta_P — the (L*) column"),
    ("Phi*_all", "min over ALL cuts of leak(A)/min(|A|,n-|A|)"),
    ("E_footrule", "E[ sum_i |i - pos(i)| ] over a uniform linear extension"),
    ("M", "sum_k leak(A_k) / (LE * floor(n^2/4)) — route (F)'s mean"),
    ("rho", "mu_pref / gamma"),
    ("1 - rho(A_1)", "Rayleigh quotient of the centred first-prefix indicator"),
    ("mu_pref (upper bound)", "an EXHIBITED monotone vector's quotient — an upper bound"),
]

# ---------------------------------------------------------------- DECLARED rows
#
# Named here because the ticket names them, or because they turned up beside a MEASURED
# row and could not be measured.  Each carries WHY the value probe cannot reach it.

DECLARED = [
    ("LSTAR(n)", "max_P min(v_F, v_L) over primitive posets on [n]",
     ["LSTAR", "Lstar", "lstar", "_alt_lstar"],
     "a MAXIMUM over a whole population, not a per-poset scalar — there is no common "
     "argument to hand two trees.  It is also where the corpus's one live numeric "
     "disagreement sat: 0.794253 (mg-789d landing) vs 0.794235 (mg-5cba a3), settled by "
     "mg-5cba on the exact bracket [0.794234562, 0.794234567]."),
    ("c_or(n)", "max_P min(c#, f*) — the disjunction's price",
     ["c_or"],
     "likewise a maximum over a population."),
    ("c#", "sweep(mu_pref)/(2 gamma) — route (M#)'s price",
     ["c_sharp", "c_sharp_float"],
     "MEASURED as a column in x3 (see V6), but its NAME `c#` is not a Python identifier "
     "and appears only in prose and transcripts, so its sites cannot be found the same "
     "way as the others."),
    ("u_M", "mu_pref / t*, t* = Delta - sqrt(Delta^2 - 2 gamma)",
     ["u_M"],
     "MEASURED in x3 V6.  Listed here as well because it is the one pair in this sweep "
     "where two names share a THRESHOLD and not a value."),
    ("f*", "M^2/(2 gamma) — route (F)'s price",
     ["f_star", "f_star_float"],
     "MEASURED as `anticorrelation_c50b:f_star_float`, but only one probed tree exposes "
     "it, so no cross-tree group forms and the row stays DECLARED."),
    ("eps_spec", "the spectral-freezing constant in (LIB-const)",
     ["eps_spec"],
     "not a poset scalar at all — a constant of the architecture.  Four trees compute a "
     "quantity under this name and this sweep does NOT establish that they are the same "
     "one."),
    ("delta(P)", "the 1/3-2/3 balance constant of the poset",
     ["delta_bruteforce", "delta_lazy", "delta_nosym", "delta_dp", "delta_1_dp",
      "hand_delta_1", "delta_le", "delta_of", "delta_R"],
     "reachable in principle; nine name-forms in eight trees with different argument "
     "conventions (pair vs element vs family), and this ticket did not have the budget "
     "to write eight adapters.  THE LARGEST UNSWEPT CANDIDATE IN THE CORPUS."),
    ("lambda_2", "second eigenvalue — TWO DIFFERENT OBJECTS UNDER ONE NAME",
     ["lambda2", "lambda_2", "lam2"],
     "in `chain_iv_*` this IS gamma (x3 V2 groups `chain_iv_c_81ff:lambda2_bracket` "
     "with the other eight gamma names); in `hodge_leverage_*` it is the second "
     "eigenvalue of a LINK GRAPH Laplacian, a different object entirely.  The one "
     "confirmed name COLLISION in this sweep, and it runs the opposite way to every "
     "other row here."),
]


def banner(s):
    print()
    print("=" * 78)
    print(s)
    print("=" * 78)


# ---------------------------------------------------------------- corpus sweep

PY_HITS, TXT_HITS, MD_HITS = {}, {}, {}
FILES = {"py": [], "txt": [], "md": []}
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if not d.startswith(".")]
    for fn in filenames:
        p = os.path.join(dirpath, fn)
        if fn.endswith(".py"):
            FILES["py"].append(p)
        elif fn.endswith(".txt"):
            FILES["txt"].append(p)
        elif fn.endswith(".md"):
            FILES["md"].append(p)
for fn in os.listdir(os.path.join(REPO, "docs")):
    if fn.endswith(".md"):
        FILES["md"].append(os.path.join(REPO, "docs", fn))
for fn in ("STATE.md", "README.md"):
    if os.path.exists(os.path.join(REPO, fn)):
        FILES["md"].append(os.path.join(REPO, fn))

CACHE = {}


def lines(p):
    if p not in CACHE:
        with open(p, encoding="utf8", errors="replace") as fh:
            CACHE[p] = fh.read().splitlines()
    return CACHE[p]


def treeof(p):
    r = os.path.relpath(p, REPO)
    parts = r.split(os.sep)
    return parts[1] if parts[0] == "code" and len(parts) > 1 else parts[0]


def sites(name, kinds=("py", "txt", "md"), within=None):
    """Every site of `name`, excluding this instrument's own directory.

    Excluding my own directory is not tidiness: `INDEX.md` lists all of these names, so
    counting myself would make every row's site count grow by one when I run, and the
    index would be measuring itself.

    `within` scopes the search to one tree.  MEASURED rows use it, and that is a
    correction of this script's own first version, which searched the whole corpus for
    every symbol and reported `M` at 1652 `.py` sites — a bare capital M matching every
    matrix variable in the arc.  A site count that large is not a site count, it is the
    regex telling you the token is ambiguous, and printing it beside a real one (`EDF`
    at 8) would have made the index's own numbers incomparable row to row.  Defect D3.
    """
    tok = re.compile(r"(?<![A-Za-z0-9_])" + re.escape(name) + r"(?![A-Za-z0-9_])")
    out = []
    for kind in kinds:
        for p in FILES[kind]:
            parts = p.split(os.sep)
            if SELF in parts:
                continue
            if within is not None and treeof(p) != within:
                continue
            for i, ln in enumerate(lines(p), 1):
                if tok.search(ln):
                    out.append((kind, os.path.relpath(p, REPO), i, ln.strip()[:90]))
    return out


DEFRE_CACHE = {}


def other_trees_defining(name):
    """Trees whose `.py` DEFINES or ASSIGNS this symbol — the name-collision column.

    This is the column that tells the next thread whether a name is safe to search for.
    `M` is defined in 40+ trees and means something different in most of them; `EDF` is
    defined in one.  A reader who greps for the first gets noise and concludes nothing.
    """
    if name in DEFRE_CACHE:
        return DEFRE_CACHE[name]
    pat = re.compile(r"^\s*(?:def\s+%s\s*\(|%s\s*=[^=])"
                     % (re.escape(name), re.escape(name)))
    trees = set()
    for p in FILES["py"]:
        if SELF in p.split(os.sep):
            continue
        for ln in lines(p):
            if pat.match(ln):
                trees.add(treeof(p))
                break
    DEFRE_CACHE[name] = trees
    return trees


def classify(kind, ln):
    return {"py": "COMPUTES", "txt": "PRINTS", "md": "SAYS"}[kind]


# ---------------------------------------------------------------- build

with open("alias_groups.json") as fh:
    G = json.load(fh)

print("x2  THE INDEX — quantity -> every name and every tree that computes it")
print()
print("  corpus swept: %d .py, %d transcripts, %d .md   (this instrument's own %d files"
      " excluded)" % (len([p for p in FILES["py"] if SELF not in p.split(os.sep)]),
                      len([p for p in FILES["txt"] if SELF not in p.split(os.sep)]),
                      len([p for p in FILES["md"] if SELF not in p.split(os.sep)]),
                      sum(1 for k in FILES for p in FILES[k] if SELF in p.split(os.sep))))
print("  MEASURED rows: %d (from x3's value clustering)   DECLARED rows: %d"
      % (len(G["groups"]), len(DECLARED)))

md = []
md.append("# INDEX — one scalar, every name, every tree\n")
md.append("*Generated by `x2_index.py`. Do not hand-edit; re-run the instrument.*\n")
md.append("""
**How to use this.** Before you publish a number about a quantity, find its row, and read
what the OTHER trees in that row already say about it. Every row below is a place where
the corpus computes one thing twice; where the numbers agree, the second tree is a free
check you are currently not using, and where they disagree, one of them is wrong.

**`MEASURED` vs `DECLARED`.** A `MEASURED` row exists because two or more trees computed
the *same number* for it over a stated population — the names were read afterwards, only
to print them. A `DECLARED` row exists because somebody (me) looked a name up: it is a
lead, not a finding. Do not cite a `DECLARED` row as evidence that two things are equal.

**This index does not rename anything.** Every symbol below is the name its own tree uses,
and that is the point: the names are load-bearing in their own threads.
""")
md.append("\n## Population this index was built over\n")
md.append("* value layer: **%d** posets (`POP-ALL`, every naturally-labelled poset at "
          "n = 3,4,5), of which **%d** primitive (`POP-PRIM`), across **%d** trees.\n"
          % (G["population"]["POP_ALL"], G["population"]["POP_PRIM"], len(G["trees"])))
md.append("* name layer: **%d** `.py` files, **%d** transcripts, **%d** `.md` files "
          "under `code/` + `docs/` + the repo root.\n"
          % (len([p for p in FILES["py"] if SELF not in p.split(os.sep)]),
             len([p for p in FILES["txt"] if SELF not in p.split(os.sep)]),
             len([p for p in FILES["md"] if SELF not in p.split(os.sep)])))

banner("MEASURED ROWS — established by value, named afterwards")
md.append("\n---\n\n## MEASURED rows\n")
for i, g in enumerate(G["groups"]):
    label, defn = LABELS[i] if i < len(LABELS) else ("(unlabelled)", "")
    trees = sorted({d["tree"] for d in g["names"]})
    print()
    print("  %-24s %d names in %d trees   spread %.3e%s"
          % (label, len(g["names"]), len(trees), g["max_spread"],
             "   DEGENERATE" if g["degenerate"] else ""))
    md.append("\n### `%s`\n" % label)
    md.append("*%s*\n\n" % defn)
    md.append("**%d names in %d trees**, agreeing to `%.3e` over the %d primitive posets "
              "of `POP-PRIM`.%s\n\n"
              % (len(g["names"]), len(trees), g["max_spread"],
                 G["population"]["POP_PRIM"],
                 "  **DEGENERATE — constant column, no evidence.**"
                 if g["degenerate"] else ""))
    md.append("| name | tree | kind | where it is computed | sites in its own tree "
              "(py/txt/md) | other trees defining this NAME |\n")
    md.append("|---|---|---|---|---|---|\n")
    for d in g["names"]:
        base = d["name"].split("(")[0].split("[")[0]
        s = sites(base, within=d["tree"])
        c = sum(1 for k, _p, _i, _l in s if k == "py")
        t = sum(1 for k, _p, _i, _l in s if k == "txt")
        m = sum(1 for k, _p, _i, _l in s if k == "md")
        # Prefer the tree's LIBRARY over its selftest: the pointer is meant to take a
        # reader to the definition, and a selftest line asserting the value is not it.
        own = sorted([x for x in s if x[0] == "py"],
                     key=lambda x: (0 if os.path.basename(x[1]).startswith(("lib", "kern"))
                                    else 1, x[1], x[2]))
        cite = L.COMPOSED_CITE.get("%s:%s" % (d["tree"], d["name"]))
        first = ("`%s:%d`" % (own[0][1], own[0][2])) if own else (
            "`%s`" % cite if cite else
            "**nowhere in its own tree** — see the DECLARED note")
        coll = other_trees_defining(base) - {d["tree"]}
        cn = ("**%d** — %s" % (len(coll), ", ".join("`%s`" % x
                                                    for x in sorted(coll)[:5])
                               + (" ..." if len(coll) > 5 else ""))) if coll else "0"
        md.append("| `%s` | `%s` | %s | %s | %d / %d / %d | %s |\n"
                  % (d["name"], d["tree"], d["kind"], first, c, t, m, cn))
        print("        %-26s %-22s  own-tree py %3d txt %3d md %3d   name also defined "
              "in %d other tree(s)" % (d["tree"], d["name"], c, t, m, len(coll)))

banner("DECLARED ROWS — leads, not findings")
md.append("\n---\n\n## DECLARED rows — leads, not findings\n")
md.append("\nEach of these is a quantity the value probe could NOT reach. The `why` "
          "column is the reason, and it is stated because a sweep that silently dropped "
          "what it could not measure would read as a clean result.\n")
for label, defn, names, why in DECLARED:
    allsites = []
    for nm in names:
        allsites.extend(sites(nm))
    trees = sorted({treeof(os.path.join(REPO, p)) for _k, p, _i, _l in allsites})
    print()
    print("  %-22s %d name-forms, %d sites, %d trees" %
          (label, len(names), len(allsites), len(trees)))
    md.append("\n### `%s`  *(DECLARED)*\n" % label)
    md.append("*%s*\n\n" % defn)
    md.append("**Why the value probe cannot reach it:** %s\n\n" % why)
    md.append("**Name-forms:** %s\n\n" % ", ".join("`%s`" % n for n in names))
    md.append("**%d sites in %d trees:** %s\n\n"
              % (len(allsites), len(trees), ", ".join("`%s`" % t for t in trees[:24])
                 + (" ..." if len(trees) > 24 else "")))
    for k, p, i, ln in allsites[:6]:
        md.append("* %s `%s:%d` — `%s`\n" % (classify(k, ln), p, i, ln))
    if len(allsites) > 6:
        md.append("* ... and %d more\n" % (len(allsites) - 6))

md.append("""
---

## What this index does NOT establish

* It does not establish that two names in a `DECLARED` row are the same quantity. They
  were matched by name; that is the failure mode this ticket exists to fix, not a method.
* It does not establish that a `MEASURED` agreement holds at `n > 5`. Every value here
  comes from `POP-ALL`/`POP-PRIM` at `n = 3,4,5`. Two scalars that agree there can differ
  at `n = 8`; what is established is that they agree where they were compared.
* It does not cover the 172 trees under `code/` that no adapter reaches. `x1_population.py`
  states which those are and why.
""")

with open("INDEX.md", "w") as fh:
    fh.write("".join(md))

banner("x2 RESULT")
print("  wrote INDEX.md — %d MEASURED rows, %d DECLARED rows   (%.1fs)"
      % (len(G["groups"]), len(DECLARED), time.time() - t0))
sys.exit(0)
