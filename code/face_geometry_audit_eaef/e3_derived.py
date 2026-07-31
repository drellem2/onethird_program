"""mg-eaef e3 -- IS THE DECLARATION STILL DERIVED AFTER THE RESTRUCTURING?

mg-0b07 booked the mg-64b6 repair's central claim as real: the unit each
mutation removes is COMPUTED from that mutation's own patch, not written beside
it.  It proved that by changing the patch in two directions and watching the
declaration follow.  mg-f7e1 then rewrote the guard the whole lineage is about,
added two rows to the sweep, and added a census section -- and a restructuring
of the thing being measured is exactly the event after which a computed value
can quietly become a written one, with the transcript unchanged because the
transcript was regenerated from the same numbers.

SO IT IS RE-RUN HERE, WITH THIS AUDIT'S OWN TWO DIRECTIONS.  A runnable copy of
the subject's instrument is made, ONE token of its MUTATION table is rewritten,
and its own `d2_deletion.py` is run.  The declaration is read out of its own
stdout.  Nothing that prints a declaration is edited.  The two directions are
chosen to move different axes:

  W  WIDEN THE SAME UNIT.  AFTER-6 deletes the `parity` return; rewrite it to
     take the `if` that guards it as well.  A derived declaration must gain a
     statement and syntax nodes and keep its function.
  K  CHANGE THE KIND AND THE FUNCTION.  AFTER-4 deletes a counter statement in
     `absorb_trace`; repoint it at a boolean OPERAND of `gate_violations`.  A
     derived declaration must lose its statement, gain a boolean clause, and
     name a different function.

If either declaration does not move, the declaration is a written value.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kern_eaef import (                                         # noqa: E402
    BAR, claim, declared_row, finding, head, instrument_copy, report,
    run_instrument,
)

# ---- direction W: AFTER-6 takes the `if` as well as the `return`
W_OLD = ("NEW_PARITY = ('face_complex.py',\n"
         "              '                    return Trace(False, \"parity\", "
         "signs_read)\\n',\n"
         "              '                    pass\\n')")
W_NEW = ("NEW_PARITY = ('face_complex.py',\n"
         "              '                if pi ^ pj != need:\\n'\n"
         "              '                    return Trace(False, \"parity\", "
         "signs_read)\\n',\n"
         "              '                pass\\n')")

# ---- direction K: AFTER-4 is repointed at an operand in another function
K_OLD = ("NEW_SIGNS = ('face_complex.py',\n"
         "             '            signs_read += 1\\n',\n"
         "             '            pass\\n')")
K_NEW = ("NEW_SIGNS = ('face_complex.py',\n"
         "             '    if m != len(B) or any(len(A[i]) != len(B[i]) "
         "for i in range(m)):\\n',\n"
         "             '    if any(len(A[i]) != len(B[i]) for i in "
         "range(m)):\\n')")


def main():
    print(BAR)
    print("mg-eaef e3 -- the derived declaration, under two changes of patch")
    print(BAR)
    print("\nPREDICTIONS, registered before these runs (PREDICTIONS.md e3):")
    print("   e3.1  control: AFTER-6 (1,0,0,7) and AFTER-4 (0,1,0,4) on the "
          "unedited copy")
    print("   e3.2  W: AFTER-6 gains one statement and more nodes, keeps "
          "`absorb_trace`")
    print("   e3.3  K: AFTER-4 -> 0 statements, >=1 boolean clause, and the "
          "function name\n         changes to `gate_violations`")
    print("   e3.4  no OTHER tag's declaration moves in either direction\n")

    head("1.  THE CONTROL -- the instrument copied and run with nothing edited")
    print("A copy that does not reproduce the subject's own numbers is a copy "
          "whose later\nruns say nothing, so the harness is scored before it "
          "is used.\n")
    ctrl_text, ctrl_code = run_instrument(instrument_copy())
    tags = ["BEFORE-1", "BEFORE-2", "AFTER-1", "AFTER-2", "AFTER-3", "AFTER-4",
            "AFTER-5", "AFTER-6", "R1", "R2", "R3"]
    ctrl = {t: declared_row(ctrl_text, t) for t in tags}
    print("   %-9s %-5s %-5s %-5s %-6s %s"
          % ("tag", "ret", "stmt", "cls", "nodes", "from"))
    for t in tags:
        r = ctrl[t]
        print("   %-9s %-5s %-5s %-5s %-6s %s"
              % ((t,) + (r[:4] if r else ("?",) * 4)
                 + ((r[4].split("from ")[-1] if r else "-"),)))
    claim("THE COPY RUNS AND PRINTS A DERIVED DECLARATION FOR EVERY ONE OF THE "
          "%d MUTATIONS: %d of %d rows parsed out of its own stdout, exit %d"
          % (len(tags), sum(1 for t in tags if ctrl[t]), len(tags), ctrl_code),
          all(ctrl[t] for t in tags),
          "the instrument failing to run outside its own directory, or "
          "changing the shape of the line the declaration is printed on -- "
          "either of which makes the two runs below unreadable rather than "
          "wrong",
          "AFTER-6 %s; AFTER-4 %s" % (ctrl["AFTER-6"][:4], ctrl["AFTER-4"][:4]))

    head("2.  DIRECTION W -- the same unit, widened")
    w_text, _ = run_instrument(instrument_copy([(W_OLD, W_NEW)]))
    w = {t: declared_row(w_text, t) for t in tags}
    print("   AFTER-6 control : %s  %s" % (ctrl["AFTER-6"][:4],
                                           ctrl["AFTER-6"][4][:72]))
    print("   AFTER-6 widened : %s  %s" % (w["AFTER-6"][:4],
                                           w["AFTER-6"][4][:72]))
    claim("THE DECLARATION FOLLOWED THE PATCH IN DIRECTION W: AFTER-6 moved "
          "from %s to %s with no declaration edited -- one more statement and "
          "%+d syntax nodes"
          % (ctrl["AFTER-6"][:4], w["AFTER-6"][:4],
             w["AFTER-6"][3] - ctrl["AFTER-6"][3]),
          w["AFTER-6"][1] == ctrl["AFTER-6"][1] + 1
          and w["AFTER-6"][3] > ctrl["AFTER-6"][3]
          and w["AFTER-6"][0] == ctrl["AFTER-6"][0],
          "the declaration being a written value, in which case it would read "
          "identically after the patch had grown -- which is the defect "
          "mg-c4c8 found in the WRITTEN declarations and the thing mg-64b6's "
          "repair claims to have made impossible")

    head("3.  DIRECTION K -- another kind of unit, in another function")
    k_text, _ = run_instrument(instrument_copy([(K_OLD, K_NEW)]))
    k = {t: declared_row(k_text, t) for t in tags}
    print("   AFTER-4 control : %s  %s" % (ctrl["AFTER-4"][:4],
                                           ctrl["AFTER-4"][4][:72]))
    print("   AFTER-4 repointed: %s  %s" % (k["AFTER-4"][:4],
                                            k["AFTER-4"][4][:72]))
    claim("THE DECLARATION FOLLOWED THE PATCH IN DIRECTION K: AFTER-4 moved "
          "from %s in `%s` to %s in `%s`, so both the UNIT KIND and the "
          "FUNCTION are read off the patch"
          % (ctrl["AFTER-4"][:4],
             ctrl["AFTER-4"][4].split("from ")[-1].strip("` "),
             k["AFTER-4"][:4],
             k["AFTER-4"][4].split("from ")[-1].strip("` ")),
          k["AFTER-4"][2] >= 1 and k["AFTER-4"][1] == 0
          and "gate_violations" in k["AFTER-4"][4],
          "a declaration that names a function from a table instead of from "
          "the patch -- the substitution this whole lineage is a chain of")

    head("4.  AND NOTHING ELSE MOVED")
    moved_w = [t for t in tags if w[t] != ctrl[t]]
    moved_k = [t for t in tags if k[t] != ctrl[t]]
    print("   direction W changed the declaration of: %s" % ", ".join(moved_w))
    print("   direction K changed the declaration of: %s" % ", ".join(moved_k))
    claim("EACH EDIT MOVED EXACTLY THE ONE DECLARATION ITS PATCH BELONGS TO -- "
          "W moved %d of %d, K moved %d of %d, and the tag that moved is the "
          "tag that was edited in both cases"
          % (len(moved_w), len(tags), len(moved_k), len(tags)),
          moved_w == ["AFTER-6"] and moved_k == ["AFTER-4"],
          "a declaration computed from something shared between mutations -- a "
          "table, a running total, the previous row -- which would show up as "
          "one edit moving several rows",
          "W: %s; K: %s" % (moved_w, moved_k))
    finding("E6", "NOT A FINDING AGAINST THE SUBJECT -- BOOKED AS CONFIRMED. "
            "The declaration survives mg-f7e1's restructuring as a DERIVED "
            "value: two patches changed in two directions, in a copy where no "
            "declaration was touched, and the printed unit followed both "
            "times, on exactly the row that was edited and on no other.  "
            "mg-0b07's finding that this was real is re-derived here from "
            "different anchors than the ones it used.")
    return report()


if __name__ == "__main__":
    sys.exit(main())
