"""libnorm — THE NORMALISATION FIELD.  A representation, not a decision (mg-479c).

mg-06d1's agreement check compares VALUES across the names of one quantity and goes RED
when two names disagree beyond the group's recorded tolerance.  It has no representation
for the case where two names denote the SAME quantity IN DIFFERENT NORMALISATIONS, and so
it cannot tell one from a disagreement.  Both directions fail:

    FALSE RED    two conventions that agree modulo a factor report as a disagreement.  On
                 a gate that blocks merges, a red for a non-reason is how gates get
                 disabled.
    FALSE PASS   a genuine 2x error becomes dismissable as "just a normalisation
                 difference", because the check gives an operator no way to tell them
                 apart.

THIS FILE BUILDS THE MACHINERY TO *SAY* WHICH.  It decides nothing.  In particular it does
not settle whether STATE.md's `(L*)`/`(M#)` clause is in the halved or the doubled form —
mg-5e82 settled that for that row, and this module's live declarations are silent about it
by construction (arm N6 of `g3_normalisation.py` measures the silence).

THE FIELD IS PER NAME, NOT PER QUANTITY
---------------------------------------
Two names for one quantity may legitimately differ by a stated factor, so the factor is a
property of the NAME.  The semantics are one line and everything else follows from it:

    raw_value(name, at a poset of size n)  ==  factor(name, n) * canonical_value(quantity, n)

so `canonical = raw / factor(n)`, and the identity factor is a PASS-THROUGH rather than a
multiply by 1.0 (see IDENTITY below).  A `convention` id is a NAME for the frame; the
factor is the frame's content.  Requiring the two to agree — same convention ⇒ equal
factors, different conventions ⇒ different factors — is what makes the RED message
trustworthy, because it is what lets the message say "these two names share a convention"
and mean something.

THE FACTOR IS A RATIONAL FUNCTION OF n, NOT A CONSTANT
------------------------------------------------------
A constant per-name factor cannot represent one of the three examples the ticket itself
names.  `code/c3_audit_a94c3/a1_algebra.py:18` states

    eps_spec = 6 E[inv_e] / (n^2 - 1)     eps_c3ca = E[inv_e] / n^2
    eps_spec / eps_c3ca = 6 n^2 / (n^2 - 1)  ->  6

and `code/unitmap_audit_9f91/out_m1_map.txt:17` tabulates both as exact rationals at five
values of n under the heading "what a flat factor of 6 gets wrong at small n".  So the
representation is `{"num": [...], "den": [...]}`, integer coefficients ASCENDING in n,
evaluated in exact `Fraction` arithmetic, of which the constant is the degree-0 case.  Arm
N4 checks the declared factor against those tabulated rationals rather than against this
paragraph.

REFUSING IS NOT REDDENING
-------------------------
An undeclared normalisation is REFUSED (exit 2), not defaulted to "same" and not reported
as a disagreement (exit 1).  This is c9876's and cb417's lesson — a missing value must be
loud, never blank — applied to a field rather than to a cell.  The distinction matters on
a merge gate: exit 1 says "two of your numbers disagree, file a ticket"; exit 2 says "this
instrument could not answer", and conflating them is how an author is told the wrong thing.
"""

import copy
import hashlib
import json
import math
import os
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
NORM_PATH = os.path.join(HERE, "NORMALISATION.json")

IDENTITY = {"num": [1], "den": [1]}


# ------------------------------------------------------------------ the factor

def trim(cs):
    """Drop trailing zero coefficients so that [1] and [1, 0] are the same factor."""
    cs = list(cs)
    while len(cs) > 1 and cs[-1] == 0:
        cs.pop()
    return cs


def canonical_factor(f):
    return {"num": trim(f["num"]), "den": trim(f["den"])}


def is_identity(f):
    """EXACTLY the identity, by coefficients — never by evaluating at some n.

    A factor that happens to equal 1 at every n in the population but is not the constant
    polynomial 1 is a different statement about the world and is not treated as identity.
    """
    c = canonical_factor(f)
    return c["num"] == [1] and c["den"] == [1]


def poly_at(cs, n):
    v = 0
    for i, c in enumerate(cs):
        v += c * (n ** i)
    return v


def factor_at(f, n):
    """The factor as an exact Fraction at poset size n."""
    den = poly_at(f["den"], n)
    if den == 0:
        raise ValueError("factor denominator vanishes at n=%d" % n)
    return Fraction(poly_at(f["num"], n), den)


def poly_str(cs):
    cs = trim(cs)
    terms = []
    for i in range(len(cs) - 1, -1, -1):
        c = cs[i]
        if c == 0:
            continue
        a = abs(c)
        if i == 0:
            t = "%d" % a
        elif i == 1:
            t = "n" if a == 1 else "%dn" % a
        else:
            t = "n^%d" % i if a == 1 else "%dn^%d" % (a, i)
        if c < 0:
            t = "- " + t
        elif terms:
            t = "+ " + t
        terms.append(t)
    return " ".join(terms) if terms else "0"


def factor_str(f):
    if is_identity(f):
        return "1"
    c = canonical_factor(f)
    num, den = poly_str(c["num"]), poly_str(c["den"])
    if den == "1":
        return num
    return "(%s)/(%s)" % (num, den)


def wellformed(f):
    """None if the factor is a usable rational function, else why not."""
    if not isinstance(f, dict) or set(f) != {"num", "den"}:
        return "factor must be {\"num\": [...], \"den\": [...]}"
    for side in ("num", "den"):
        cs = f[side]
        if not isinstance(cs, list) or not cs:
            return "factor.%s must be a non-empty list of integer coefficients" % side
        for c in cs:
            if not isinstance(c, int) or isinstance(c, bool):
                return "factor.%s carries a non-integer coefficient %r" % (side, c)
    if trim(f["den"]) == [0]:
        return "factor denominator is identically zero"
    if trim(f["num"]) == [0]:
        return "factor is identically zero — a normalisation cannot annihilate its quantity"
    return None


# ------------------------------------------------------------------ the file

class Declarations(object):
    """The parsed NORMALISATION.json.  Parsing NEVER decides anything; `validate` does."""

    def __init__(self, raw):
        self.raw = raw
        self.conventions = raw.get("conventions", {})
        self.live = raw.get("declarations", {})
        self.illustrative = raw.get("illustrative", {})
        self.canonical_tolerances = raw.get("canonical_tolerances", {})
        self.pinned_digest = raw.get("pinned_digest")

    def entry(self, member):
        return self.live.get("%s:%s" % tuple(member))

    def factor_of(self, member):
        e = self.entry(member)
        return IDENTITY if e is None else e["factor"]

    def convention_of(self, member):
        e = self.entry(member)
        return None if e is None else e["convention"]


def load(path=NORM_PATH):
    with open(path) as fh:
        return Declarations(json.load(fh))


def planted(decl, live=None, remove=(), conventions=None, tolerances=None):
    """A COPY of the declarations with an edit, for the planted worlds.

    The falsification arms mutate declarations exactly the way mg-06d1's arms mutate
    captured columns: in memory, on a deep copy, never in the committed file.  A planted
    world that had to be written to `NORMALISATION.json` to be run would be a live
    declaration about a name nothing computes, which is the defect E6 of the
    pre-registration names.
    """
    raw = copy.deepcopy(decl.raw)
    for k in remove:
        raw.get("declarations", {}).pop(k, None)
    if live:
        raw.setdefault("declarations", {}).update(copy.deepcopy(live))
    if conventions:
        raw.setdefault("conventions", {}).update(copy.deepcopy(conventions))
    if tolerances:
        raw.setdefault("canonical_tolerances", {}).update(copy.deepcopy(tolerances))
    return Declarations(raw)


def digest_of(decl, baseline):
    """sha256 over the declarations RESTRICTED TO THE PINNED MEMBERS.

    Restricted, and this is mg-479c's own thesis applied to its own remedy: a digest that
    moved because somebody declared a normalisation for an UNPINNED name would put the gate
    RED for a non-reason, which is the failure this ticket is about.  Arm D4 plants exactly
    that and requires the digest not to move.
    """
    pinned = ["%s:%s" % tuple(m) for g in baseline["groups"] for m in g["members"]]
    body = {}
    for k in sorted(pinned):
        e = decl.live.get(k)
        if e is None:
            continue
        body[k] = {"convention": e["convention"],
                   "factor": canonical_factor(e["factor"])}
    blob = json.dumps(body, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]


# ------------------------------------------------------------------ the refusals

def validate(decl, baseline):
    """Everything that makes this instrument unable to answer.  Returns [(code, where, why)].

    A non-empty list is exit 2 — REFUSED — and never exit 1.  Nothing here is a finding
    about the corpus's mathematics; every item is a statement that a declaration is missing
    or self-contradictory, which is a fact about this file.
    """
    bad = []

    # --- the field itself
    for key, e in sorted(decl.live.items()) + sorted(decl.illustrative.items()):
        where = key
        if not isinstance(e, dict):
            bad.append(("MALFORMED", where, "declaration is not an object"))
            continue
        if "factor" not in e:
            bad.append(("UNDECLARED-FACTOR", where, "no factor field"))
            continue
        why = wellformed(e["factor"])
        if why:
            bad.append(("MALFORMED-FACTOR", where, why))
        if not e.get("convention"):
            bad.append(("UNDECLARED-CONVENTION", where, "no convention field"))
        elif e["convention"] not in decl.conventions:
            bad.append(("UNKNOWN-CONVENTION", where,
                        "convention %r is not defined in `conventions`" % e["convention"]))
        if not e.get("derivation"):
            bad.append(("UNDERIVED", where,
                        "no derivation — a factor with no stated derivation is an "
                        "assertion nobody can check"))

    # --- provenance.  An identity factor is seeded from mg-0d1b's MEASURED agreement and
    #     the quoted number is checked against the record; a non-identity factor has no
    #     such measurement behind it and must cite a source instead.
    obs = {}
    for g in baseline["groups"]:
        for m in g["members"]:
            obs["%s:%s" % tuple(m)] = (g["label"], g["observed_at_baseline"])
    for key, e in sorted(decl.live.items()):
        if not isinstance(e, dict) or "factor" not in e or wellformed(e["factor"]):
            continue
        ident = is_identity(e["factor"])
        quoted = e.get("seeded_from_measured_spread")
        if ident:
            if key not in obs:
                continue                      # an unpinned identity name — see D4
            if quoted is None:
                bad.append(("UNSEEDED", key,
                            "identity factor with no seeded_from_measured_spread — "
                            "declaring 71 identities by hand would be 71 assertions "
                            "nobody measured"))
            elif quoted != obs[key][1]:
                bad.append(("SEED-STALE", key,
                            "quotes a measured spread of %.17g; BASELINE.json records "
                            "%.17g for group `%s`"
                            % (quoted, obs[key][1], obs[key][0])))
        else:
            if quoted is not None:
                bad.append(("SEED-MISAPPLIED", key,
                            "a non-identity factor cannot be seeded from an agreement "
                            "measured in the raw frame"))
            if not e.get("source"):
                bad.append(("UNSOURCED", key,
                            "non-identity factor with no source — the factor is a claim "
                            "about the corpus and must cite where it comes from"))

    # --- completeness.  AN UNDECLARED NORMALISATION IS REFUSED, NOT DEFAULTED TO "SAME".
    for g in baseline["groups"]:
        for m in g["members"]:
            key = "%s:%s" % tuple(m)
            if key not in decl.live:
                bad.append(("UNDECLARED", key,
                            "pinned member of group `%s` has no normalisation "
                            "declaration.  A missing field is not evidence that this name "
                            "shares its group's convention." % g["label"]))

    # --- agreement between the label and the content, within each group
    for g in baseline["groups"]:
        ms = [tuple(m) for m in g["members"] if decl.entry(m) is not None]
        for i, a in enumerate(ms):
            for b in ms[i + 1:]:
                ca, cb = decl.convention_of(a), decl.convention_of(b)
                fa, fb = canonical_factor(decl.factor_of(a)), \
                    canonical_factor(decl.factor_of(b))
                if ca == cb and fa != fb:
                    bad.append(("CONVENTION-SPLIT", "%s:%s vs %s:%s" % (a + b),
                                "both declare convention %r but declare different factors "
                                "%s and %s — one convention cannot have two factors"
                                % (ca, factor_str(fa), factor_str(fb))))
                if ca != cb and fa == fb:
                    bad.append(("CONVENTION-PHANTOM", "%s:%s vs %s:%s" % (a + b),
                                "declare different conventions %r and %r but the same "
                                "factor %s — two names in the same normalisation are in "
                                "the same convention" % (ca, cb, factor_str(fa))))

    # --- the frame the TOLERANCE is stated in.  mg-0d1b measured max RAW spread.  The
    #     moment a group gains a non-identity member the comparison happens in a different
    #     frame and that number no longer governs it.  Rescaling it would be this ticket's
    #     own defect one level up, so the registrant supplies one with its own source or
    #     the instrument refuses.
    for g in baseline["groups"]:
        lab = g["label"]
        nonid = [tuple(m) for m in g["members"]
                 if decl.entry(m) is not None and not is_identity(decl.factor_of(m))]
        ct = decl.canonical_tolerances.get(lab)
        if nonid and ct is None:
            bad.append(("TOLERANCE-FRAME", lab,
                        "%d member(s) declare a non-identity factor, so the recorded "
                        "tolerance %.6e is a max spread in the RAW frame and does not "
                        "govern the canonical comparison.  Supply "
                        "canonical_tolerances[%r] = {tolerance, source}."
                        % (len(nonid), g["tolerance"], lab)))
        if ct is not None:
            if not nonid:
                bad.append(("TOLERANCE-UNUSED", lab,
                            "a canonical tolerance is declared but every member is in the "
                            "identity normalisation, so nothing consumes it.  A tolerance "
                            "that would take effect on the next declaration edit is a "
                            "number nobody checked."))
            if not isinstance(ct, dict) or "tolerance" not in ct or not ct.get("source"):
                bad.append(("TOLERANCE-UNSOURCED", lab,
                            "canonical tolerance must be {tolerance, source}"))

    return bad


def tolerance_for(decl, g):
    """The tolerance the comparison is actually made against, and the frame it is in."""
    nonid = any(decl.entry(m) is not None and not is_identity(decl.factor_of(m))
                for m in g["members"])
    if nonid and g["label"] in decl.canonical_tolerances:
        return decl.canonical_tolerances[g["label"]]["tolerance"], "canonical"
    return g["tolerance"], "raw"


# ------------------------------------------------------------------ canonicalisation

def canonicalise(cols, decl, pop):
    """{(tree,name): column} in each name's own frame -> the same in the canonical frame.

    THE IDENTITY CASE IS A PASS-THROUGH AND NOT A MULTIPLY BY 1.0.  `v * 1.0 == v` for
    every finite float, but routing the identity through a multiply makes the seven
    exact-equality rows depend on that also being true of None, of inf, and of whatever a
    tree returns next.  The same column object is returned, so the identity case cannot
    perturb anything even in principle — and `g1_values.py` MEASURES the resulting bit
    identity against the pre-479c path rather than arguing it from this comment.
    """
    out = {}
    for key, col in cols.items():
        f = decl.factor_of(key)
        if is_identity(f):
            out[key] = col
            continue
        vals = []
        for (n, _dn), v in zip(pop, col):
            if v is None or v != v or math.isinf(v):
                vals.append(v)
            else:
                vals.append(float(Fraction(v) / factor_at(f, n)))
        out[key] = vals
    return out


def describe(decl, member, n=None):
    """How this name is declared, for the RED message.  `1` reads as `1`, not as absent."""
    e = decl.entry(member)
    if e is None:
        return "UNDECLARED"
    s = "convention %r  factor %s" % (e["convention"], factor_str(e["factor"]))
    if n is not None and not is_identity(e["factor"]):
        s += "  = %s at n=%d" % (factor_at(e["factor"], n), n)
    return s
