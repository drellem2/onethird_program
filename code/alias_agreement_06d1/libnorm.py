"""libnorm — THE NORMALISATION FIELD.  What mg-06d1's gate had no way to SAY.

mg-06d1 compares VALUES across the names of one quantity and goes RED when two names
disagree beyond the group's tolerance.  It has no representation for two names denoting the
same quantity IN DIFFERENT NORMALISATIONS, and mg-479c is the ticket for that hole:

    FALSE RED   two conventions that agree modulo a factor report as a disagreement.  On a
                gate that blocks merges, a red for a non-reason is how gates get disabled.
    FALSE PASS  a genuine 2x error becomes dismissable as "just a normalisation
                difference", because the check gives an operator no way to tell them apart.

Both are the SAME missing bit: the index cannot state whether two names share a convention.
This module supplies that bit, and nothing else.  It decides no ambiguity — see §4 of the
README and `no_verdict_on_5e82()` below.

WHY THE FACTOR IS A RATIONAL FUNCTION OF n AND NOT A CONSTANT
--------------------------------------------------------------
Because a constant cannot represent one of the three examples the ticket itself names.
`code/c3_audit_a94c3/a1_algebra.py:18` states

    eps_spec / eps_c3ca = 6 n^2 / (n^2 - 1)  ->  6

and `code/unitmap_audit_9f91/out_m1_map.txt` tabulates both quantities as exact rationals at
eleven values of n under the heading "DIRECTION OF APPROACH (what a flat factor of 6 gets
wrong at small n)": at n=3 a flat 6 is wrong by +0.0833.  A per-name constant factor field
would have been unable to say what this corpus already knows, so the factor is

    to_canonical(n) = num(n) / den(n),   num, den integer-coefficient polynomials in n

evaluated in exact `Fraction` arithmetic.  The constant factor is the degree-0 case and the
identity is `num = [1], den = [1]`.  `g3_normalisation.py` checks the eps pair against
mg-9f91's committed table rather than asserting it.

THE IDENTITY CASE IS A PASS-THROUGH AND NOT A MULTIPLY BY 1.0
--------------------------------------------------------------
`v * 1.0 == v` for every finite float, so a multiply would be harmless today.  It would also
make seven exact-equality rows in `BASELINE.json` depend on that staying true of whatever a
tree returns next — of `None`, of a `Fraction`, of an `inf`.  `canonicalise()` therefore
returns the SAME LIST OBJECT for an identity factor, and `g1_values.py` MEASURES the
bit-identity on all 71 pinned columns rather than arguing it.  (Filed in advance as E3.)

WHAT A DECLARATION IS WORTH, AND THE HOLE THIS DOES NOT CLOSE
--------------------------------------------------------------
A declared factor is an ESCAPE HATCH and this module cannot close it: an operator facing a
real 2x disagreement can silence it by declaring a factor of 2, and nothing here tells that
edit from a correct one.  Filed in advance as P6.  The two mitigations are both reporting,
not enforcement:

  * every non-identity factor is printed on EVERY run, green as well as red — a factor that
    only becomes visible when something breaks is invisible;
  * `describe_pair()` states whether the two names SHARE a convention, so an operator seeing
    "ratio exactly 2 and these two names are declared to be in the SAME convention" knows it
    is a real defect, which is the sentence the ticket asks for.

The declaration file is committed, so the edit is a diff with an author.  That is the whole
of the protection and the README says so.
"""

import json
import hashlib
import os
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
NORM_PATH = os.path.join(HERE, "NORMALISATION.json")


class NormError(Exception):
    """A declaration this module refuses to act on.

    RAISED, not defaulted.  Ticket item 3: "REFUSE AN UNDECLARED NORMALISATION rather than
    defaulting to 'same'."  Callers turn this into exit 2 (refused/broken), never exit 1 (a
    control fired) — an undeclared field means the comparison could not be made, which is a
    different fact from two numbers disagreeing, and the suite's exit convention already
    distinguishes them.
    """


# ------------------------------------------------------------------ the factor

class Factor(object):
    """num(n)/den(n), integer coefficients, low order first.  Exact `Fraction` arithmetic.

    `Factor([6,0,0], [-1,0,1])` is 6/(n^2-1); `Factor([0,0,6], [-1,0,1])` is 6n^2/(n^2-1).
    """

    __slots__ = ("num", "den")

    def __init__(self, num, den):
        for coeffs, which in ((num, "num"), (den, "den")):
            if not isinstance(coeffs, (list, tuple)) or not coeffs:
                raise NormError("factor %s must be a non-empty list of integers" % which)
            for c in coeffs:
                if not isinstance(c, int) or isinstance(c, bool):
                    raise NormError("factor %s coefficient %r is not an integer — a float "
                                    "coefficient would make the factor inexact, which is "
                                    "the one thing a normalisation must never be" % (which, c))
        self.num = tuple(num)
        self.den = tuple(den)
        if all(c == 0 for c in self.den):
            raise NormError("factor denominator is identically zero")

    # -- value

    def at(self, n):
        """The exact Fraction value of the factor at this n.  Raises on a zero denominator.

        A denominator that vanishes at an n in the population is not a rounding problem, it
        is a declaration that does not apply there, and it is refused rather than skipped.
        """
        num = sum(Fraction(c) * n ** i for i, c in enumerate(self.num))
        den = sum(Fraction(c) * n ** i for i, c in enumerate(self.den))
        if den == 0:
            raise NormError("factor denominator vanishes at n=%d" % n)
        return num / den

    def is_identity(self):
        """Exactly 1 as a RATIONAL FUNCTION, not merely 1 at the n we happen to sweep.

        `num == den` termwise after stripping trailing zeros.  A factor that is 1 at n=3,4,5
        and 2 at n=6 is NOT the identity, and treating it as one because the current
        population stops at 5 would hide it exactly when the population widens.
        """
        return _strip(self.num) == _strip(self.den)

    def as_text(self, n=None):
        s = "%s/%s" % (_poly_text(self.num), _poly_text(self.den))
        if n is not None:
            s += " = %s at n=%d" % (self.at(n), n)
        return s

    def key(self):
        """Canonical comparable form — two factors are EQUAL iff their keys are.

        Reduced by the gcd of all coefficients and by common trailing zeros, so `2/2` and
        `1/1` and `[0,2]/[0,2]` are one factor.  Used by the convention/factor consistency
        rule, which is the check that makes the RED message trustworthy.
        """
        num, den = _strip(self.num), _strip(self.den)
        g = 0
        for c in num + den:
            g = _gcd(g, abs(c))
        if g > 1:
            num = tuple(c // g for c in num)
            den = tuple(c // g for c in den)
        # a common factor of n on both sides is the same rational function away from n=0,
        # and n=0 is not a poset.
        while len(num) > 1 and len(den) > 1 and num[0] == 0 and den[0] == 0:
            num, den = num[1:], den[1:]
        if den and den[-1] < 0:
            num = tuple(-c for c in num)
            den = tuple(-c for c in den)
        return (num, den)

    def __eq__(self, other):
        return isinstance(other, Factor) and self.key() == other.key()

    def __hash__(self):
        return hash(self.key())

    def __repr__(self):
        return "Factor(%s)" % self.as_text()


def _gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def _strip(coeffs):
    out = list(coeffs)
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return tuple(out)


def _poly_text(coeffs):
    terms = []
    for i in range(len(coeffs) - 1, -1, -1):
        c = coeffs[i]
        if c == 0:
            continue
        if i == 0:
            terms.append("%d" % c)
        elif i == 1:
            terms.append("%dn" % c if abs(c) != 1 else ("n" if c == 1 else "-n"))
        else:
            terms.append(("%dn^%d" % (c, i)) if abs(c) != 1
                         else ("n^%d" % i if c == 1 else "-n^%d" % i))
    if not terms:
        return "0"
    s = terms[0]
    for t in terms[1:]:
        s += (" + " + t) if not t.startswith("-") else (" - " + t[1:])
    return s if len(terms) == 1 else "(%s)" % s


ONE = Factor([1], [1])


# ------------------------------------------------------------------ the declarations

def _parse_table(table, section):
    out = {}
    for key, d in sorted(table.items()):
        if ":" not in key:
            raise NormError("%s: key %r is not tree:name" % (section, key))
        for req in ("convention", "to_canonical", "source"):
            if req not in d:
                raise NormError("%s[%s] has no %r.  A declaration without a source is a "
                                "number somebody typed." % (section, key, req))
        tc = d["to_canonical"]
        out[key] = {"convention": d["convention"],
                    "factor": Factor(tc.get("num", [1]), tc.get("den", [1])),
                    "source": d["source"]}
    return out


def check_consistency(table, groups):
    """convention <-> factor must be TWO STATEMENTS OF THE SAME FACT, PER QUANTITY.

    Same convention  => equal factors.  Otherwise the label says two names share a frame
                        while the factors say they do not, and the RED message's sentence
                        "these two names share a convention" would be worth nothing.
    Different labels => different factors.  Otherwise one of the two labels is decorative,
                        and a decorative field an operator is invited to read as meaningful
                        is the defect mg-479c is about, shipped inside its own remedy.

    BOTH RULES ARE SCOPED TO ONE QUANTITY, and getting that wrong was a real error of mine
    (README §7, D1).  The factor a name declares is to ITS OWN GROUP'S canonical frame, so
    twelve groups whose members are all in the identity normalisation are twelve DIFFERENT
    conventions sharing one factor — which a global "different labels => different factors"
    rule refuses.  I wrote that rule globally first and it rejected the very file this
    ticket exists to write.

    `groups` is [(label, [member key, ...]), ...].  Names not in any group are not checked
    here: nothing is claimed about two names for two different quantities.
    """
    for label, keys in groups:
        by_conv = {}
        for key in sorted(keys):
            d = table.get(key)
            if d is None:
                continue
            by_conv.setdefault(d["convention"], []).append((key, d["factor"]))
        for conv, entries in sorted(by_conv.items()):
            fkeys = {f.key() for _k, f in entries}
            if len(fkeys) > 1:
                raise NormError(
                    "group %s: convention %r is declared by %d names with %d DIFFERENT "
                    "factors (%s).  The label says these names share a normalisation and "
                    "the factors say they do not; one of the two is wrong and this module "
                    "will not guess which."
                    % (label, conv, len(entries), len(fkeys),
                       ", ".join("%s -> %s" % (k, f.as_text()) for k, f in entries)))
        seen = {}
        for conv, entries in sorted(by_conv.items()):
            k = entries[0][1].key()
            if k in seen:
                raise NormError(
                    "group %s: conventions %r and %r declare the SAME factor %s.  Two "
                    "labels for one frame makes the label decorative, and this gate's RED "
                    "message invites an operator to read it as meaningful."
                    % (label, seen[k], conv, entries[0][1].as_text()))
            seen[k] = conv


class Declarations(object):
    """The parsed NORMALISATION.json, and every refusal it can raise.

    Keys are "tree:name" — PER NAME and not per quantity, which is ticket item 1 and is the
    whole point: two names for one quantity may legitimately differ by a stated factor, and
    the index must be able to SAY so.
    """

    def __init__(self, raw, path=NORM_PATH):
        self.path = path
        self.raw = raw
        self.decls = _parse_table(raw.get("declarations", {}), "declarations")
        self.examples = {}
        for qty, block in sorted(raw.get("worked_examples", {}).items()):
            self.examples[qty] = {
                "note": block.get("note", ""),
                "names": _parse_table(block.get("names", {}),
                                      "worked_examples[%s]" % qty),
            }
        self.tolerances = raw.get("canonical_tolerances", {})
        for qty, block in sorted(self.examples.items()):
            check_consistency(block["names"], [("worked_examples[%s]" % qty,
                                                sorted(block["names"]))])

    # ---- lookup, and the refusal

    def factor_for(self, member):
        """The declared factor, or REFUSE.  Never a default.

        Ticket item 3, and it is c9876's and cb417's lesson (a missing value must be loud,
        never blank) applied to a field rather than to a cell.  Defaulting an undeclared name
        to "same" is the FALSE PASS direction of this ticket with the volume turned all the
        way down: the gate would compare two frames it has never been told anything about and
        report agreement or disagreement as if it had.
        """
        key = "%s:%s" % tuple(member)
        if key not in self.decls:
            raise NormError(
                "NO NORMALISATION DECLARED for %s.  Refusing to default it to `same`: an "
                "undeclared normalisation is exactly the case where this gate cannot tell a "
                "convention from a defect.  Add an entry to %s naming the convention, the "
                "factor to the group's canonical frame, and the source it is carried from."
                % (key, os.path.basename(self.path)))
        return self.decls[key]["factor"]

    def convention_for(self, member):
        return self.decls["%s:%s" % tuple(member)]["convention"]

    def has(self, member):
        return "%s:%s" % tuple(member) in self.decls

    # ---- what the baseline freezes

    def digest_over(self, members):
        """sha256 over the declarations RESTRICTED TO these members.

        Restricted, deliberately.  A digest over the whole file would go RED the day somebody
        declares a normalisation for a name this gate does not pin — say while preparing
        mg-a397's widening — and a red for a non-reason is the ticket's own thesis about how
        gates get disabled.  Filed in advance as E9.
        """
        h = hashlib.sha256()
        for m in sorted(tuple(x) for x in members):
            key = "%s:%s" % m
            d = self.decls.get(key)
            if d is None:
                h.update(("%s\x00UNDECLARED\x00" % key).encode())
            else:
                h.update(("%s\x00%s\x00%s\x00%s\x00"
                          % (key, d["convention"], d["factor"].key()[0],
                             d["factor"].key()[1])).encode())
        return h.hexdigest()[:16]

    def canonical_tolerance(self, label):
        return self.tolerances.get(label)


def load(path=NORM_PATH):
    if not os.path.exists(path):
        raise NormError("no %s.  The gate has no way to tell a normalisation from a "
                        "disagreement without it and will not proceed as if it had."
                        % os.path.basename(path))
    with open(path) as fh:
        return Declarations(json.load(fh), path=path)


# ------------------------------------------------------------------ canonicalising

def canonicalise(cols, members, decls, ns):
    """{member: canonical column}, and the factor applied per member.

    `ns[i]` is the n of poset i.  The identity factor returns THE SAME LIST OBJECT — see the
    module docstring; `g1_values.py` measures that on all 71 pinned columns.

    A non-identity factor multiplies by the exact `Fraction` value and converts back with
    `float()`, which is correctly rounded.  That is a real, stated cost: a canonical column
    under a non-dyadic factor carries one rounding the raw column did not, so a group with a
    non-identity member CANNOT honestly be pinned at tolerance 0.  It is one more reason the
    carried tolerance does not survive into the canonical frame — see `tolerance_frame`.
    """
    out, applied = {}, {}
    for m in members:
        f = decls.factor_for(m)
        applied[tuple(m)] = f
        col = cols[tuple(m)]
        if f.is_identity():
            out[tuple(m)] = col                      # pass-through, not v * 1.0
            continue
        new = []
        for v, n in zip(col, ns):
            if v is None or v != v:
                new.append(v)
            else:
                try:
                    new.append(float(Fraction(v) * f.at(n)))
                except (OverflowError, ValueError):
                    new.append(v * float(f.at(n)))
        out[tuple(m)] = new
    return out, applied


def tolerance_frame(members, decls):
    """('IDENTITY'|'CANONICAL', why) — is the carried raw-frame tolerance still meaningful?

    mg-0d1b measured every tolerance as the max spread of RAW values.  If every member of a
    group is in the identity normalisation, the canonical frame IS the raw frame and the
    carried number governs exactly what it governed before; that is the case for all twelve
    pinned groups today and the reason this ticket is inert on them.

    The moment a group gains a member with a non-identity factor, the carried number is
    stated in a frame the comparison no longer happens in.  It is NOT rescalable: members
    with DIFFERENT factors have no single multiplier, so there is no honest arithmetic that
    turns mg-0d1b's measurement into a canonical-frame one.  The registrant must supply a
    canonical-frame tolerance with its own source, and until they do the gate REFUSES.
    Rescaling the frame while keeping the number that governs it would be this ticket's own
    defect one level up, and it is filed in advance as E4.
    """
    non_id = [tuple(m) for m in members if not decls.factor_for(m).is_identity()]
    if not non_id:
        return "IDENTITY", "all %d members in the identity normalisation" % len(members)
    return "CANONICAL", "%d member(s) carry a non-identity factor: %s" % (
        len(non_id), ", ".join("%s:%s" % m for m in non_id))


# ------------------------------------------------------------------ the RED message

SIMPLE = [(p, q) for q in range(1, 17) for p in range(1, 65)]


def nearest_simple_ratio(r, rel=1e-9):
    """(p, q, exact) for the simplest p/q within `rel` of r, or None.

    Ticket item 2: "An operator seeing `these differ by exactly 2, and the index says these
    two names share a convention` knows it is a real defect; seeing a bare inequality, they
    do not."  The ratio is the half of that sentence the numbers can supply.
    """
    if r is None or r != r or r == 0:
        return None
    r = abs(r)
    best = None
    for p, q in SIMPLE:
        if _gcd(p, q) != 1:
            continue
        val = p / q
        if abs(val - r) <= rel * max(1.0, r):
            score = (q, p)
            if best is None or score < best[0]:
                best = (score, p, q, val == r)
    return None if best is None else (best[1], best[2], best[3])


def describe_pair(a, b, va, vb, decls):
    """The sentence the ticket asks the RED message for.

    Reports the factor applied to each side, the two convention labels, the raw ratio, and —
    the part that turns a bare inequality into a verdict an operator can act on — whether the
    two names are DECLARED TO SHARE A CONVENTION.  If they do, a clean ratio is a defect and
    the message says so in those words.  If they do not, the residual after normalising is
    the finding and the declared factors are printed beside it so the reader can see what was
    applied and go and check it.
    """
    ka, kb = "%s:%s" % tuple(a), "%s:%s" % tuple(b)
    ca, cb = decls.decls[ka]["convention"], decls.decls[kb]["convention"]
    fa, fb = decls.decls[ka]["factor"], decls.decls[kb]["factor"]
    lines = ["normalisation: %s in convention %r (x %s);  %s in convention %r (x %s)"
             % (ka, ca, fa.as_text(), kb, cb, fb.as_text())]
    ratio = None
    if va not in (None, 0) and vb not in (None, 0):
        ratio = va / vb
        simple = nearest_simple_ratio(ratio)
        rtxt = "raw ratio %s:%s / %s:%s = %.12g" % (a[0], a[1], b[0], b[1], ratio)
        if simple and simple[:2] == (1, 1):
            # A ratio of 1 is the DEFAULT and saying "= 1/1" would read as a finding.  What
            # it actually tells an operator is the useful negative: whatever is wrong here,
            # it is not a scale.
            rtxt += "  — a ratio of 1 to within 1e-9, so this is NOT a scale difference"
        elif simple:
            rtxt += "  = %s%d/%d" % ("EXACTLY " if simple[2] else "", simple[0], simple[1])
        lines.append(rtxt)
    if ca == cb:
        lines.append("THESE TWO NAMES ARE DECLARED TO BE IN THE SAME CONVENTION (%r), so "
                     "this is a DEFECT and not a normalisation difference.  A ratio near a "
                     "simple rational here means one side is scaled wrong; it does not mean "
                     "the two are in different units." % ca)
    else:
        lines.append("The two names are declared in DIFFERENT conventions (%r vs %r) and the "
                     "spread above is the residual AFTER the declared factors were applied.  "
                     "Either a value is wrong or a declared factor is; the declarations are "
                     "in NORMALISATION.json with their sources." % (ca, cb))
    return lines
