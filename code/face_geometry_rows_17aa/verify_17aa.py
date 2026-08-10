"""mg-17aa -- the independent verifier for EXTENDING THE [CANNOT FAIL] TREATMENT
TO ALL FOUR I-ROWS of NEGATIVE CONTROL 4.

WHAT THIS FILE IS FOR.  The repair itself is in `code/face_geometry/controls.py`
and it prints its own counts.  A repair that scores its own arithmetic is the
defect this whole lineage exists to remove, so every number the repair rests on
is re-derived here by a route that does not go through the repair's routing
quantity:

  * absorbability is blocked by an EXHIBITED ENTRY (i, j) of the two matrices,
    checked against BOTH sign choices s_i s_j = +-1 -- a certificate, not a
    predicate's answer -- and cross-checked against `absorbable_bruteforce`,
    the definition enumerated over all 2^m sign vectors, wherever m is small
    enough to enumerate;
  * the forcing is re-asked at n = 6, a population the section does not sweep,
    so that "FORCED at every n" is not a property of 86 posets;
  * the conjunct decomposition is subjected to a DELETION test -- delete each
    conjunct and see whether any verdict anywhere moves -- because a clause
    whose deletion disturbs nothing is not carrying the row, and that is
    exactly the question this ticket is about.

THE ONE THING IT DOES NOT DO INDEPENDENTLY.  `claim1_pair` is imported from the
tree under test: re-implementing the face complex here would be a second
construction to keep in step, and the arc already has three instruments doing
that.  What is checked here is the SCORING -- which clauses can fail and which
cannot -- and for that the construction is input, not evidence.

Exit 0 iff every claim holds.  Run: python3 verify_17aa.py
"""

import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "face_geometry"))

from controls import (                                          # noqa: E402
    claim1_pair, claim1_test, absorbable_bruteforce, nc4_row_conjuncts,
    nc4_row_verdict, nc4_row_stats, MAGNITUDE_MOVES, DIAGONAL_MOVES,
)
from face_complex import (                                      # noqa: E402
    linear_extensions, mat_eq, absorbable_by_diagonal_twist,
)
from posets import all_posets                                   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

MODES = [("I1", "ridge_facets", True),
         ("I2", "split_free_as_interior", True),
         ("I3", "ridge_drop", True),
         ("I4", "facet_offbyone", False)]

BAR = "=" * 78
SCORE = []


def claim(text, ok, detail=""):
    SCORE.append(ok)
    print("  [%s] %s%s" % ("HOLDS" if ok else "BROKEN", text,
                           ("\n        " + detail) if detail else ""))
    return ok


def head(t):
    print("\n" + BAR + "\n" + t + "\n" + BAR)


def blocking_entry(A, B):
    """An entry of (A, B) that no diagonal +-1 twist can reconcile, or None.

    THE CERTIFICATE, not the predicate's answer.  S.A.S = B with s in {+1,-1}^m
    forces s_i^2 = 1 on the diagonal and |s_i s_j| = 1 off it, so:

      A[i][i] != B[i][i]           blocks: the diagonal entry is untouched by
                                   any S at all.
      |A[i][j]| != |B[i][j]|       blocks: S can only flip a sign.

    Returns (i, j, A[i][j], B[i][j], why).  The caller VERIFIES the certificate
    against both sign choices rather than trusting this function -- which is
    what makes it a certificate and not a second opinion.
    """
    m = len(A)
    if m != len(B) or any(len(A[i]) != len(B[i]) for i in range(m)):
        return (None, None, None, None, "shape")
    for i in range(m):
        if A[i][i] != B[i][i]:
            return (i, i, A[i][i], B[i][i], "diagonal")
    for i in range(m):
        for j in range(m):
            if abs(A[i][j]) != abs(B[i][j]):
                return (i, j, A[i][j], B[i][j], "magnitude")
    return None


def certificate_holds(cert):
    """Check the exhibited entry really is unreconcilable, for BOTH values of
    the product s_i s_j.  Two arithmetic comparisons; no eigensolver, no
    enumeration, no appeal to `absorbable_by_diagonal_twist`."""
    i, j, a, b, why = cert
    if why == "shape":
        return True
    return all(sgn * a != b for sgn in (1, -1))


def sweep(ps, mode):
    """Every biting pair of `mode` over `ps`, with its certificate."""
    out = []
    for P in ps:
        L_true, target = claim1_pair(P)
        L_mut, _ = claim1_pair(P, incidence_mode=mode)
        if mat_eq(L_mut, L_true):
            continue
        out.append((P, L_mut, target, blocking_entry(L_mut, target)))
    return out


def main():
    head("mg-17aa V0 -- THE POPULATIONS, STATED BEFORE ANYTHING IS CONCLUDED")
    ps5 = [P for n in range(2, 6) for P in all_posets(n)]
    ps6 = [P for P in all_posets(6)]
    claim("the section's own population is every poset up to isomorphism with "
          "2 <= n <= 5: %d of them, and claim (1) holds on all of them "
          "uncorrupted -- the row every 'rejects on N/N' below is forced GIVEN"
          % len(ps5),
          len(ps5) == 86 and all(claim1_test(P) for P in ps5),
          "86 posets, baseline green on 86")
    claim("and the wider population this file adds is n = 6: %d further posets, "
          "|L(P)| up to %d.  n = 7 is NOT swept and the reason is size, not "
          "principle: |L(P)| reaches 5040 there and L^rel is |L(P)| x |L(P)|"
          % (len(ps6), max(len(linear_extensions(P)) for P in ps6)),
          len(ps6) == 318)

    head("mg-17aa V1 -- absorb == 0 IS FORCED ON ALL FOUR ROWS, BY CERTIFICATE")
    print("Every biting pair gets an EXHIBITED ENTRY that no diagonal +-1 twist")
    print("can reconcile, and the exhibit is verified against both sign choices.")
    print("This is the claim the [CANNOT FAIL] row now makes for four rows where")
    print("it made it for three.\n")
    tot = tot_cert = tot_absorb = 0
    per_row = []
    for tag, mode, _ in MODES:
        pairs = sweep(ps5, mode)
        certs = [c for _, _, _, c in pairs]
        ok = sum(1 for c in certs if c is not None and certificate_holds(c))
        by = {}
        for c in certs:
            by[c[4] if c else "NONE"] = by.get(c[4] if c else "NONE", 0) + 1
        ab = sum(absorbable_by_diagonal_twist(m_, t) for _, m_, t, _ in pairs)
        per_row.append((tag, len(pairs), by, ab))
        tot += len(pairs)
        tot_cert += ok
        tot_absorb += ab
        claim("%s: %d biting pairs, %d carry a VERIFIED blocking certificate, "
              "predicate says absorbable on %d.  By kind: %s"
              % (tag, len(pairs), ok, ab,
                 ", ".join("%s %d" % kv for kv in sorted(by.items()))),
              ok == len(pairs) and ab == 0 and len(pairs) > 0)
    claim("SO THE ANSWER IS FORCED ON ALL FOUR: %d/%d biting pairs blocked by "
          "an exhibited entry, %d absorbable.  P1 of PREDICTIONS.md, at 0.90"
          % (tot_cert, tot, tot_absorb),
          tot_cert == tot and tot_absorb == 0 and tot == 297,
          "297 = 72 + 82 + 82 + 61, the section's own total")

    head("mg-17aa V1b -- AND THE CERTIFICATE AGREES WITH THE DEFINITION")
    agree = cases = 0
    for tag, mode, _ in MODES:
        for P, L_mut, target, cert in sweep(ps5, mode):
            if len(L_mut) > 10:
                continue
            cases += 1
            agree += (absorbable_bruteforce(L_mut, target)
                      is False) == (cert is not None)
    claim("on the %d biting pairs with |L(P)| <= 10, the certificate's verdict "
          "agrees with `absorbable_bruteforce` -- the definition enumerated "
          "over all 2^m sign vectors, which shares no line with either the "
          "certificate or the shipped predicate -- on %d of them"
          % (cases, agree), agree == cases and cases > 0,
          "an expected value DERIVED and not copied (mg-d0e2 OUTSTANDING 2)")

    # ... and BOTH DIRECTIONS, because no pair of the four rows is absorbable,
    # so V1b above only ever exercises one side of the agreement.  A detector
    # that returned a certificate for everything would pass it.  NEGATIVE
    # CONTROL 3's parity corruption is the one thing in this battery that IS
    # absorbable, and the certificate must decline to produce an exhibit there.
    nc3_pairs = []
    for P in ps5:
        L_true, target = claim1_pair(P)
        L_par, _ = claim1_pair(P, sign_mode="parity")
        if not mat_eq(L_par, L_true):
            nc3_pairs.append((L_par, target))
    nc3_none = sum(1 for A, B in nc3_pairs if blocking_entry(A, B) is None)
    nc3_bf = sum(1 for A, B in nc3_pairs
                 if len(A) <= 10 and absorbable_bruteforce(A, B))
    nc3_small = sum(1 for A, B in nc3_pairs if len(A) <= 10)
    claim("and the OTHER direction, which V1b cannot reach because nothing in "
          "the four rows is absorbable: on NEGATIVE CONTROL 3's parity "
          "corruption -- D.L.D by construction, so genuinely absorbable -- the "
          "certificate declines to exhibit an entry on %d/%d pairs, and brute "
          "force confirms absorbable on %d/%d of the small ones.  A detector "
          "that returned a certificate for everything would have passed V1b"
          % (nc3_none, len(nc3_pairs), nc3_bf, nc3_small),
          nc3_none == len(nc3_pairs) and nc3_bf == nc3_small and nc3_small > 0)

    head("mg-17aa V2 -- WHICH GATE, AND THE TIGHTNESS THAT KEPT ROW I4 SCORED")
    diag_only = [t for t, n, by, _ in per_row if by.get("magnitude", 0) == 0]
    needs_mag = [(t, by.get("magnitude", 0)) for t, n, by, _ in per_row
                 if by.get("magnitude", 0)]
    claim("the DIAGONAL gate alone -- mg-8a12's routing quantity, and the only "
          "one its [CANNOT FAIL] row argued -- covers %s and does NOT cover %s. "
          "That is why row I4 stayed scored for four repairs: the argument the "
          "other three rows were routed on is FALSE on it"
          % (", ".join(diag_only),
             ", ".join("%s (%d pairs)" % x for x in needs_mag)),
          diag_only == ["I1", "I2", "I3"] and needs_mag == [("I4", 3)],
          "P2 of PREDICTIONS.md, at 0.85: neither theorem alone covers the four")
    # D1 OF MY OWN, KEPT AND FIXED IN PLACE.  This arm first read `P.relations`
    # under a `hasattr` guard falling back to True.  `Poset` has `__slots__ =
    # ("n", "less", "name")`, so the attribute does not exist, the guard was
    # False on every element, and the `all(...)` was VACUOUSLY TRUE -- a probe
    # reporting HOLDS because it could not read the thing it was asked about,
    # inside a ticket about clauses that cannot fail.  It reads `P.less` now,
    # and the population is required to be non-empty so that "no pairs to check"
    # can never read as "checked".
    mag_pairs = [P for P, _, _, c in sweep(ps5, "facet_offbyone")
                 if c and c[4] == "magnitude"]
    claim("and the pairs it does not cover are exactly the ANTICHAINS, where "
          "the off-by-one is a bare relabelling of L(P) = S_n and the diagonal "
          "survives -- so the row that needed the second gate is the row whose "
          "corruption is a gauge on precisely those posets",
          len(mag_pairs) == 3 and all(len(P.less) == 0 for P in mag_pairs),
          "the %d pairs the magnitude gate settles have |less| = %s and "
          "|L(P)| = %s -- 3!, 4! and 5!"
          % (len(mag_pairs), [len(P.less) for P in mag_pairs],
             [len(linear_extensions(P)) for P in mag_pairs]))
    claim("the closed form for the second gate is recorded beside the first "
          "rather than left in a verdict mail: MAGNITUDE_MOVES carries an entry "
          "for facet_offbyone and DIAGONAL_MOVES carries none",
          "facet_offbyone" in MAGNITUDE_MOVES
          and "facet_offbyone" not in DIAGONAL_MOVES,
          "MAGNITUDE_MOVES keys: %s" % sorted(MAGNITUDE_MOVES))

    head("mg-17aa V3 -- AND IT IS NOT A PROPERTY OF 86 POSETS: n = 6")
    tot6 = cert6 = ab6 = 0
    rows6 = []
    for tag, mode, _ in MODES:
        pairs = sweep(ps6, mode)
        ok = sum(1 for _, _, _, c in pairs
                 if c is not None and certificate_holds(c))
        ab = sum(absorbable_by_diagonal_twist(m_, t) for _, m_, t, _ in pairs)
        mag = sum(1 for _, _, _, c in pairs if c and c[4] == "magnitude")
        rows6.append((tag, len(pairs), mag))
        tot6 += len(pairs)
        cert6 += ok
        ab6 += ab
    claim("at n = 6 -- a population NEGATIVE CONTROL 4 does not sweep -- the "
          "forcing holds on %d/%d biting pairs with %d absorbable, and the "
          "magnitude gate is needed on %s.  A count that reproduces at a size "
          "the repair never looked at is the difference between a theorem and "
          "an 86-poset measurement"
          % (cert6, tot6, ab6,
             ", ".join("%s %d" % (t, m) for t, _, m in rows6)),
          cert6 == tot6 and ab6 == 0 and tot6 > 0)

    head("mg-17aa V4 -- THE TICKET'S OWN INPUT PREMISE, CHECKED NOT RE-DERIVED")
    print("The ticket says to take as input that three of the four `>= 3 facets`")
    print("zeros are FORCED and that only I4's is a result.  It also says to")
    print("check it.  It is FALSE, and it was already false when the ticket was")
    print("written: mg-8af0 landed the correction on 2026-08-05, one day after.\n")
    readme = open(os.path.join(REPO, "code", "face_geometry_repair_e35b",
                               "README.md")).read()
    claim("mg-e35b's own README carries the struck correction -- 'ALL FOUR "
          "zeros are forced' -- so the premise is refuted IN THE TREE and this "
          "ticket does not have to re-run mg-8af0's 2424-build sweep to say so",
          "CORRECTED by mg-8af0" in readme and "All four zeros are forced" in readme,
          "the correction is at code/face_geometry_repair_e35b/README.md")
    log = subprocess.run(["git", "log", "--oneline", "--all", "--grep",
                          "ALL FOUR >=3-facet zeros are FORCED"],
                         cwd=REPO, capture_output=True, text=True)
    claim("and the commit that landed it is nameable rather than alleged",
          "mg-8af0" in log.stdout,
          (log.stdout.strip().split("\n")[0][:120]) if log.stdout.strip()
          else "no commit found")
    # ... and the two questions are INDEPENDENT, which is why mg-8af0's finding
    # corrects the ticket's premise without answering the ticket.
    nc3 = [(P,) + tuple(claim1_pair(P, sign_mode="parity")) for P in ps5]
    nc3_bites = [(P, L, t) for P, L, t in
                 ((P, L, claim1_pair(P)[1]) for P, L, _ in nc3)
                 if not mat_eq(L, claim1_pair(P)[0])]
    nc3_absorb = sum(absorbable_by_diagonal_twist(L, t) for _, L, t in nc3_bites)
    claim("AND THE TWO QUESTIONS ARE INDEPENDENT, which is why mg-8af0's "
          "finding corrects the ticket's premise without answering the ticket: "
          "NEGATIVE CONTROL 3's parity corruption raises NO ridge's facet count "
          "(it touches no incidence at all) and is absorbable on %d/%d of the "
          "posets where it bites.  'No ridge in >= 3 facets' therefore does not "
          "imply 'not absorbable', and the forcing this ticket establishes is "
          "not the forcing mg-8af0 established"
          % (nc3_absorb, len(nc3_bites)),
          len(nc3_bites) > 0 and nc3_absorb == len(nc3_bites),
          "P8 of PREDICTIONS.md, at 0.50")

    head("mg-17aa V5 -- THE CONJUNCT DECOMPOSITION, AND THE DELETION TEST")
    print("For each row, delete each conjunct from its scored condition and see")
    print("whether any verdict moves -- on the real population or on either")
    print("planted world.  A clause whose deletion disturbs nothing anywhere is")
    print("not carrying the row, and that is the whole question this ticket is")
    print("about.  A deletion that DOES move a verdict is load-bearing.\n")
    st_noop = nc4_row_stats(ps5, "true")
    load = {}
    for tag, mode, localised in MODES:
        st = nc4_row_stats(ps5, mode, mode if localised else None)
        conj = nc4_row_conjuncts(localised, forced=True)
        wrong = next(md for _, md, lc in MODES if lc and md != mode) \
            if localised else None
        worlds = [("real", st), ("no-op", st_noop)]
        if wrong:
            sw = dict(st)
            sw["caused"] = nc4_row_stats(ps5, mode, wrong)["caused"]
            worlds.append(("mis-predicted", sw))
        moved = []
        for k, (cname, _, _, _) in enumerate(conj):
            kept = conj[:k] + conj[k + 1:]
            if any(nc4_row_verdict(w, kept) != nc4_row_verdict(w, conj)
                   for _, w in worlds):
                moved.append(cname)
        load[tag] = moved
        claim("%s: %d conjuncts, load-bearing on some world: %s"
              % (tag, len(conj), ", ".join(moved) if moved else "NONE"),
              True,
              "conjuncts = " + " AND ".join(
                  "%s [%s]" % (c, k) for c, k, _, _ in conj))
    claim("`rej == app` and `shape_ok == app` are load-bearing on NO world in "
          "any row -- they are true, they are cheap, and they are not the "
          "section's evidence.  They are KEPT and NAMED rather than deleted: a "
          "conjunct that can only fail alongside a scored row is redundant, not "
          "unfalsifiable, and quietly deleting true checks to tidy a table is a "
          "worse change than the one this ticket makes",
          all("rej == app" not in v and "shape_ok == app" not in v
              for v in load.values()),
          "load-bearing per row: %s" % load)
    claim("and I4's contingent content is a SINGLE conjunct where I1/I2/I3 have "
          "two: the row that was kept scored BECAUSE its absorbability answer "
          "was supposedly a decision has the least measured content of the "
          "four.  P6 of PREDICTIONS.md, at 0.60",
          load["I4"] == ["app > 0"]
          and all(load[t] == ["app > 0", "caused == app"]
                  for t in ("I1", "I2", "I3")),
          "I4 %s vs I1 %s" % (load["I4"], load["I1"]))

    head("mg-17aa V6 -- THE NEW ROW'S OWN FALSIFIABILITY")
    print("The row that replaces the routing check scores 'every row has an")
    print("exhibited falsifying input'.  A row that cannot report its own")
    print("failure is the defect mg-e331 filed as its own D4, so the condition")
    print("is run against a row built to have no falsifying input.\n")
    all_forced = [c for c in nc4_row_conjuncts(False, forced=True)
                  if c[1] != "CONTINGENT"]
    claim("a row whose conjuncts are ALL forced is green on the real input AND "
          "green on every planted world, so no world is red and the "
          "falsifiability row's condition is FALSE on it -- the row can report "
          "its own failure",
          nc4_row_verdict(st_noop, all_forced)
          and nc4_row_verdict(nc4_row_stats(ps5, "facet_offbyone"), all_forced),
          "conjuncts kept: %s" % [c[0] for c in all_forced])
    claim("and the shipped section is GREEN on the real input, so this is a "
          "green-on-real + red-on-planted pair and not a probe satisfied by "
          "the good input alone",
          all(nc4_row_verdict(nc4_row_stats(ps5, m, m if lc else None),
                              nc4_row_conjuncts(lc, forced=True))
              for _, m, lc in MODES))

    head("mg-17aa V7 -- CONTAINMENT, BY ALLOWLIST AND NOT BY PREFIX")
    print("Every path this ticket may touch is named here WITH ITS REASON, so")
    print("that `it is under a directory I also edited` can never be the reason")
    print("a change is accepted.  A file appearing that is not on this list")
    print("turns the arm red whatever directory it is in.\n")
    ALLOWED = {
        "code/face_geometry_rows_17aa/":
            "this ticket's own tree",
        "code/face_geometry/controls.py":
            "the battery repaired: the routing, the [CANNOT FAIL] row, the "
            "conjunct decomposition and the replaced routing row",
        "code/face_geometry/controls_output.txt":
            "its artifact, regenerated by its own run_all.sh",
        "code/face_geometry/run_all.sh":
            "its runtime comment re-MEASURED on this tree (19.4 -> 20.8 s) "
            "rather than carried forward, and what moved attributed",
        "code/face_geometry_audit_e7bc/pc_all_pass.txt":
            "a DERIVED control -- the artifact with every marker promoted to "
            "[PASS] -- regenerated because g1 compares it live",
        "code/face_geometry_instr_5f9a/positive_control_all_fail.txt":
            "the same, demoted to [FAIL]",
        "code/face_geometry_audit_e7bc/out_g1_positive_control.txt":
            "that audit's transcript, regenerated by its own run_all.sh",
        "code/face_geometry_instr_5f9a/d3_reintroduction.py":
            "R1's anchor re-aimed onto the branch row I4 now prints from, and "
            "R2's scoped count re-aimed onto `signs_read`; both mutations kept",
        "code/face_geometry_instr_5f9a/d4_auditor_rerun.py":
            "one frozen EXPECTATION moved 4 -> 5 with the reason written in; "
            "the audit it scores is not edited",
        "code/face_geometry_instr_5f9a/out_d2_deletion.txt":
            "transcript, regenerated",
        "code/face_geometry_instr_5f9a/out_d3_reintroduction.txt":
            "transcript, regenerated",
        "code/face_geometry_instr_5f9a/out_d4_auditor_rerun.txt":
            "transcript, regenerated",
        "code/face_geometry_landing_da45/verify_landing.py":
            "TARGET 3 re-aimed off the deferral it froze and onto the guard it "
            "was protecting; TARGET 2's literal list now read from the row",
        "code/face_geometry_landing_da45/out_verify.txt":
            "transcript, regenerated",
        "code/face_geometry_landing_7d5a/out_verify.txt":
            "transcript, regenerated by its own run_all.sh (exit 0)",
        "code/face_geometry_audit_6653/out_attack_banner.txt":
            "transcript, regenerated by its own run_all.sh (exit 0)",
        "code/face_geometry_audit_6653/out_verify_claims.txt":
            "transcript, regenerated by its own run_all.sh (exit 0).  IT "
            "COUNTS COMMITS IN HISTORY, so it is a measurement AT the commit "
            "it ran at and not a live property: it is regenerated INSIDE this "
            "commit (554 = `git rev-list --count HEAD` here) and a refinery "
            "rebase will restale it by one, which no ordering of runs can fix",
    }
    # BOTH ROUTES, UNIONED.  A probe reading only the committed diff misses what
    # is still in the worktree -- mg-a0d6's own D7, whose fix fired on its first
    # run -- and a probe reading only the worktree reports NOTHING once the work
    # is committed, so the transcript would be honest for one hour and vacuous
    # afterwards.  The base is the branch point, pinned: `main` moves.
    BASE = "744cfd5"
    dif = subprocess.run(["git", "diff", "--name-only", BASE], cwd=REPO,
                         capture_output=True, text=True)
    st = subprocess.run(["git", "status", "--porcelain"], cwd=REPO,
                        capture_output=True, text=True)
    touched = sorted({l[3:].strip() for l in st.stdout.split("\n") if l.strip()}
                     | {l.strip() for l in dif.stdout.split("\n") if l.strip()})
    claim("the population is the union of two routes -- `git diff --name-only "
          "%s` (%d paths) and `git status --porcelain` (%d) -- because the "
          "committed diff misses the worktree and the worktree reports nothing "
          "once this lands"
          % (BASE, len([l for l in dif.stdout.split("\n") if l.strip()]),
             len([l for l in st.stdout.split("\n") if l.strip()])),
          dif.returncode == 0 and len(touched) > 0)
    unlisted = [f for f in touched
                if f not in ALLOWED
                and not any(f.startswith(k) for k in ALLOWED if k.endswith("/"))]
    claim("%d path(s) differ and every one of them is on the allowlist; %d are "
          "not: %s" % (len(touched), len(unlisted), unlisted or "none"),
          not unlisted,
          "\n        ".join("%-58s %s" % (f, ALLOWED.get(
              f, next((ALLOWED[k] for k in ALLOWED
                       if k.endswith("/") and f.startswith(k)), "?")))
              for f in touched))
    claim("and NO frozen audit document is edited -- what moved in another "
          "ticket's tree is an EXPECTATION, an anchor, or a transcript, never "
          "a recorded finding",
          not any(f.endswith(("e3_seams.py", "e2_parity.py", "audit_nc4.py",
                              "g1_positive_control.py", "g2_deletion.py",
                              "g3_differs_under.py", "g4_seams.py",
                              "README.md"))
                  for f in touched if "rows_17aa" not in f),
          "e3_seams.py gained a fifth BROKEN claim under this tree and is NOT "
          "edited: d4's expectation moved instead, saying which tree it recorded")

    print("\n" + BAR)
    print("%d claim(s) scored; %d BROKEN." % (len(SCORE), SCORE.count(False)))
    print(BAR)
    return 1 if not all(SCORE) else 0


if __name__ == "__main__":
    sys.exit(main())
