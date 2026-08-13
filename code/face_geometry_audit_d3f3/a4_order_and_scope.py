#!/usr/bin/env python3
"""mg-d3f3 a4 -- THE ORDER, AND WHAT WAS LEFT OUT.  (PREDICTIONS.md P7, P8, P9)

The brief's first sentence is a question about ORDER: "verify F2 was fixed
BEFORE F1".  The addendum then lists eight things mg-8af0 says it deliberately
did not do and asks whether each was genuinely out of scope "rather than quietly
dropped".  Both are answered here against `git`, not against prose.

ONE THING THE ADDENDUM GETS WRONG, and it is worth saying before the checks: the
four commit hashes it names (`41bdbfa`, `903a2e9`, `a8d1723`, `12a1553`) are NOT
on main.  The refinery rebased the branch, so the landed commits are `c420303`,
`0c3a2ba`, `534c06b`, `66130f8` and `2657490`.  The pre-rebase hashes are still
reachable in this repository, which is why this file can check BOTH and say the
files this ticket touched carry the same BLOBS (the TREES necessarily differ --
the rebase replayed onto a moved main, and my first version of a4.2 called that
difference a failure while measuring the rest of the repository).

Exit 0 iff every check below holds.
"""

import ast
import os
import re
import subprocess
import sys

import lib_d3f3 as L

REPO = os.path.normpath(os.path.join(L.CODE, ".."))
LANDED = ["c420303", "0c3a2ba", "534c06b", "66130f8", "2657490"]
NAMED = ["41bdbfa", "903a2e9", "a8d1723", "12a1553"]
FCB2 = os.path.join(L.CODE, "face_geometry_audit_fcb2")


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args),
                          capture_output=True, text=True).stdout


def files(rev):
    return sorted(x for x in git("show", "--stat=200", "--format=",
                                 "--name-only", rev).split("\n") if x)


def main():
    R = L.Report("mg-d3f3 a4 -- order on main, and the eight declared omissions")

    # -- a4.1: are the addendum's hashes on main? -----------------------
    on_main = [c for c in NAMED
               if git("merge-base", "--is-ancestor", c, "main") is not None
               and subprocess.run(["git", "-C", REPO, "merge-base",
                                   "--is-ancestor", c, "main"]).returncode == 0]
    landed_ok = all(subprocess.run(["git", "-C", REPO, "merge-base",
                                    "--is-ancestor", c, "main"]).returncode == 0
                    for c in LANDED)
    R.check("a4.1 THE ADDENDUM'S HASHES ARE PRE-REBASE.  %d of the 4 commits it "
            "names are ancestors of main; the 5 rebased commits all are.  This "
            "is a refinery rebase and not work loss -- the trees agree, checked "
            "in a4.2" % len(on_main),
            not on_main and landed_ok,
            "named-and-on-main: %s; landed-and-on-main: %s"
            % (on_main or "none", landed_ok))
    # COMPARED AT THE BLOB, NOT THE TREE.  A rebase replays onto a MOVED main,
    # so the whole-tree hashes must differ -- they carry other tickets' files.
    # What the rebase must preserve is the CONTENT OF THE FILES THIS TICKET
    # TOUCHED, and that is what is compared.  (My first version of this row
    # compared trees, called the difference a failure, and was measuring the
    # rest of the repository.)
    pairs = list(zip(NAMED[1:], LANDED[1:4]))
    detail = []
    same_blobs = True
    for a, b in pairs:
        touched = sorted(set(files(a)) | set(files(b)))
        agree = all(git("rev-parse", "%s:%s" % (a, f)).strip()
                    == git("rev-parse", "%s:%s" % (b, f)).strip()
                    for f in touched)
        same_blobs &= agree
        detail.append("%s/%s %d files %s" % (a, b, len(touched),
                                             "agree" if agree else "DIFFER"))
    R.check("a4.2 and the rebase preserved the WORK: at each of the three repair "
            "commits, every file the commit touches has the SAME BLOB pre- and "
            "post-rebase (trees necessarily differ -- the rebase replayed onto a "
            "moved main)", same_blobs, "; ".join(detail))

    # -- a4.3: the order, and what the F2 commit touched ----------------
    order = [git("log", "-1", "--format=%s", c).split(":")[0].strip()
             for c in LANDED]
    dates = [git("log", "-1", "--format=%ci", c).strip() for c in LANDED]
    f2_files = files("0c3a2ba")
    f2_touches_probe = [f for f in f2_files if f.startswith("code/face_geometry/")]
    R.check("a4.3 ORDER HOLDS AND IT IS LOAD-BEARING.  On main the sequence is "
            "%s, and the F2 commit touches NO file under code/face_geometry/ -- "
            "so the count was still the tautology `%% (N, N, ...)` at the moment "
            "the verifier was repaired, which is what the mandate was for (P7a)"
            % " -> ".join(order),
            order[:4] == ["predictions", "repair", "repair", "repair"]
            and not f2_touches_probe,
            "F2 (0c3a2ba) touched %s; timestamps %s"
            % (f2_files, [d[11:19] for d in dates]))

    # -- a4.4: the verifier was WATCHED FAILING on the unrepaired F1 ----
    tx = git("show", "0c3a2ba:code/face_geometry_repair_e35b/out_verify_e35b.txt")
    m = re.search(r"(\d+) checks, (\d+) REFUTED", tx)
    refuted = [l.strip()[4:] for l in tx.splitlines() if l.strip().startswith("- ")]
    tails = {}
    for c in LANDED[1:4]:
        t = git("show", "%s:code/face_geometry_repair_e35b/out_verify_e35b.txt" % c)
        mm = re.search(r"(\d+) checks, (\d+|0) (?:REFUTED|refuted)", t)
        tails[c] = mm.group(0) if mm else "??"
    green = all("0 refuted" in v for v in tails.values())
    R.check("a4.4 P7b IS REFUTED, AND THIS IS THE AUDIT'S SECOND FINDING.  The "
            "committed transcript at EVERY one of mg-8af0's three repair "
            "commits reports 0 refuted: %s.  THE REPAIRED VERIFIER WAS NEVER "
            "WATCHED FAILING ON THE REAL TREE.  I predicted one refuted row at "
            "the F2 commit and there are none -- so on the branch that landed, "
            "F2-before-F1 is a COMMIT ORDERING and not a demonstration.  It is "
            "the right ordering and it was correctly obeyed; what it is not is "
            "EVIDENCE, and a1 says why it could not have been: F1 leaves no "
            "trace any of these rows can read"
            % "; ".join("%s %r" % (c[:7], v) for c, v in tails.items()),
            green,
            "and note the SIBLING branch of the same ticket (0c39f34, never "
            "merged) DID exit 1 at its F2 commit -- its message says so -- "
            "because it added V7 at F2 time rather than at F1 time")
    R.count("refuted rows across mg-8af0's three landed repair commits", 0,
            "COULD MOVE",
            "a repair that had landed V7's twelfth anchor before repairing the "
            "count would print a non-zero here; the sibling branch did")

    # -- a4.5: E9's second clause ---------------------------------------
    f1_files = files("534c06b")
    touched_verifier = any("verify_e35b.py" in f for f in f1_files)
    R.check("a4.5 E9's SECOND CLAUSE IS FALSE AS RECORDED -- the F1 commit DOES "
            "change verify_e35b.py, and mg-8af0 scores E9 a HALF-MISS rather "
            "than rounding it to a hit (P7c)",
            touched_verifier, "534c06b touched %s" % f1_files)

    # -- a4.6: STATE.md, across every mg-8af0 commit --------------------
    touched = set()
    for c in LANDED + NAMED:
        touched |= set(files(c))
    R.check("a4.6 STATE.md IS UNTOUCHED by every one of mg-8af0's %d commits, "
            "pre- and post-rebase -- the omission is real and matches the choice "
            "mg-2789 and mg-e35b made at the same site (P8b)"
            % len(LANDED + NAMED),
            not any(f.endswith("STATE.md") for f in touched),
            "files touched across all of them: %d, none named STATE.md"
            % len(touched))

    # -- a4.7: F4 is not in the brief -----------------------------------
    pred = open(os.path.join(L.EIGHT, "PREDICTIONS.md")).read()
    head = pred[:pred.index("---")]
    assigned = sorted(set(re.findall(r"\*\*(F\d)\*\*", head)))
    R.check("a4.7 mg-8af0's BRIEF ASSIGNS %s AND NOTHING ELSE, stated in its own "
            "PREDICTIONS.md before any code existed -- so mg-fcb2's F4 was out "
            "of scope and not dropped (P8a)" % "/".join(assigned),
            assigned == ["F1", "F2", "F3"],
            "findings named in the brief section: %s" % assigned)

    # -- a4.8: A1.4a scores the mathematics ------------------------------
    a1 = open(os.path.join(FCB2, "a1_counts.py")).read()
    i = a1.index("A1.4a")
    scored = a1[i:i + 900]
    maths = "worst >= 3" in scored
    R.check("a4.8 mg-fcb2's A1.4a SCORES `worst >= 3` -- a claim about the "
            "MATHEMATICS and not about the artifact's wording -- so it stays "
            "[REFUTED] after a repair that changed the wording, correctly (P8d)",
            maths, "the scored condition contains %r"
            % ("worst >= 3" if maths else "NOT worst >= 3"))
    frozen = "[REFUTED] A1.4a" in open(os.path.join(FCB2,
                                                    "out_a1_counts.txt")).read()
    R.check("a4.9 and its transcript still records [REFUTED], unedited -- an "
            "audit's transcript is a record of what it found, not a status "
            "board", frozen,
            "out_a1_counts.txt carries the REFUTED line: %s" % frozen)

    # -- a4.10: n > 6 ----------------------------------------------------
    probe = open(os.path.join(L.EIGHT, "probe_f3_ridge_multiplicity.py")).read()
    ns = sorted(set(int(x) for x in re.findall(r"^NMAX\s*=\s*(\d+)", probe, re.M)))
    R.check("a4.10 THE n > 6 OMISSION IS REAL: the multiplicity probe's sweep "
            "stops at the bound in its own source (%s), and the README says so "
            "under 'Not shown' (P8c)" % ns,
            ns == [6],
            "NMAX in probe_f3_ridge_multiplicity.py: %s" % ns)

    # -- a4.11: P9, the material beyond the brief ------------------------
    print()
    added = ["demo_f2_row_can_go_red.py", "probe_f1_count_moves.py",
             "probe_f3_ridge_multiplicity.py"]
    spec = re.compile(r"%[-#0 +]*[0-9*]*(?:\.[0-9*]+)?([diouxXeEfFgGcrsa%])")
    own = 0
    per = {}
    for f in added:
        s = open(os.path.join(L.EIGHT, f)).read()
        n = 0
        for node in ast.walk(ast.parse(s)):
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod) \
               and isinstance(node.left, ast.Constant) \
               and isinstance(node.left.value, str):
                n += len([c for c in spec.findall(node.left.value) if c != "%"])
        per[f] = n
        own += n
    sys.path.insert(0, L.REPAIR)
    from verify_e35b import TABLE, census                        # noqa: E402
    R.count("formatted values printed by the three scripts mg-8af0 ADDS",
            own, "COULD MOVE",
            "a print added to any of them moves it: %s"
            % ", ".join("%s %d" % (k, v) for k, v in per.items()))
    R.count("of those covered by any census or table in the repair", 0, "FORCED",
            "FORCED BY THE POPULATIONS AS DECLARED: census() takes "
            "`negative_control_incidence` and TABLE takes the counts the repair "
            "OFFERS AS EVIDENCE, and neither population can contain a value "
            "printed by an 8af0 script.  This 0 is not a discovery")
    R.check("a4.11 mg-8af0's OWN E11 CALLED THIS BEFORE THE CODE EXISTED -- "
            "'the pre-filed audit mg-d3f3 will find at least one printed count "
            "in code this repair adds that this repair does not classify'.  "
            "There are %d, and E11 is a HIT.  I record it as CALLED, not "
            "DISCOVERED, and it is not this audit's headline (P9a)" % own,
            own > 0 and "will find **at least one printed count in code this"
            in " ".join(pred.split()),
            "E11 present in PREDICTIONS.md: %s"
            % ("will find **at least one printed count in code this"
               in " ".join(pred.split())))
    R.note("WHERE THE WORST FINDING ACTUALLY IS (P9b, and I bet on this at "
           "0.50): not in the probes but in the README's 'Predictions, scored' "
           "table -- prose the brief did not ask for -- which is where a3.6's "
           "false causal claim lives and where a3.2's false remedy is stated "
           "most plainly.  The material beyond the brief was right again; it "
           "was the PROSE beyond the brief and not the CODE beyond it.")

    return R.finish()


if __name__ == "__main__":
    sys.exit(main())
