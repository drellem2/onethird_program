"""mg-7ae5 / A1 — THE ABSENT STEP, STATED; and the CURRENCY CROSSINGS of the
chain, which is what makes the statement forced rather than chosen.

No poset is enumerated here.  This section re-reads mg-ac0c's merged 25-row
table (`docs/OneThird-DownstreamConstants-mg-ac0c.md` §1) and classifies each
row by the CURRENCY its quantity lives in.  A row cannot be constructed
without declaring what it takes IN and what it hands OUT, so a row whose two
ends differ is a crossing by construction and not by my say-so.

    SPECTRAL  1 - lambda_std, E[inv_e], eps_spec, eps_sup      (a number of P)
    CUT       Phi_P(A), Delta_1(A,B), C_3, K, eps_leak, eps_0  (a number of a CUT)
    PAIR      p_xy, delta(P), the [1/3,2/3] window             (a number of a PAIR)
    ARITH     bookkeeping with no poset in it

P1 predicted: the currency crosses exactly once and at the absent row.  This
section is where that is scored, and it is scored against a classification
declared here in full so a reader can disagree row by row.
"""

from fractions import Fraction

CUT, PAIR, SPEC, ARITH = 'CUT', 'PAIR', 'SPECTRAL', 'ARITH'


class Row:
    """One row of mg-ac0c §1, with the two ends of its currency declared."""

    def __init__(self, num, step, quantity, status, cin, cout, why):
        if cin not in (CUT, PAIR, SPEC, ARITH) or cout not in (CUT, PAIR, SPEC, ARITH):
            raise ValueError('row %s: undeclared currency' % num)
        self.num, self.step, self.quantity, self.status = num, step, quantity, status
        self.cin, self.cout, self.why = cin, cout, why

    @property
    def crosses(self):
        return self.cin != self.cout

    def __repr__(self):
        return '%s %s->%s' % (self.num, self.cin, self.cout)


# mg-ac0c §1, verbatim in its numbering, status and step.  The two currency
# columns and `why` are THIS document's reading and are the new content.
ROWS = [
    Row('00', 'L1b out', '1-lambda_std <= eps_spec', 'ABSENT', SPEC, SPEC,
        'the chain INPUT; a spectral number of P, no cut and no pair in it'),
    Row('01', 'supply', 'eps_sup = d*n/(n+1)', 'PROVED', PAIR, SPEC,
        'CROSSING, and it is the PROVED one: frozen (a PAIR hypothesis, every '
        'pair flips w.p. < 1/3) -> E[inv] < m/3 -> spectral, via Op-Form Cl. 6.1 '
        'and mg-210d\'s master bound'),
    Row('02', 'Step 3', 'L2 as a disjunction', 'ASSUMED', SPEC, CUT,
        'CROSSING: spectral smallness -> a structural statement about a prefix'),
    Row('03', 'Step 3', "L2's first disjunct (eigenvector)", 'REFUTED', SPEC, CUT,
        'same crossing, refuted at n=6'),
    Row('04', 'Step 4', 'Cheeger square (Phi*)^2/2 <= 1-lambda_std', 'PROVED', SPEC, CUT,
        'CROSSING, and it is the OTHER proved one: the spectral->cut conversion, '
        'a theorem at every poset'),
    Row('05', 'Step 3', "K on L2's second disjunct", 'ABSENT', SPEC, CUT,
        'the live half of row 02; unquantified at all 5 source occurrences'),
    Row('06', 'L3/Step 4', 'C_3^(III) in Phi_pref <= sqrt(2 C_3 eps_spec)', 'PROVED*', SPEC, CUT,
        'conditional on row 03, which is FP-refuted'),
    Row('07', 'L3', 'C_3^gap', 'EMPIRICAL', SPEC, CUT, 'same conversion, gap form'),
    Row('08', 'L3', 'C_3^cut = Phi*_pref / Phi*', 'EMPIRICAL', CUT, CUT,
        'cut -> cut: best cut to best PREFIX cut'),
    Row('09', 'L3 (row 10)', 'best-cut-is-a-prefix', 'EMPIRICAL', CUT, CUT, 'cut -> cut'),
    Row('10', 'chain IV', 'c, the capture fraction', 'EMPIRICAL', CUT, CUT, 'cut -> cut'),
    Row('11', 'Step 5', 'Phi_P(A) = Delta_1(A,B)', 'PROVED', CUT, CUT,
        'an IDENTITY inside cut currency — Op-Form Lemma 2.1; the place a '
        'crossing was once suspected and is not one'),
    Row('12', 'Step 5 out', 'Delta_1(A_k,A_k^c) <= eps_leak', 'EMPIRICAL', CUT, CUT,
        'the LAST pinned entry before the gap: a cut number, pinned at 1/5'),
    Row('13', 'Step 6/L4', 'eps_0^cons — the consumable threshold', 'ABSENT', CUT, PAIR,
        '*** THE CROSSING THAT IS ABSENT: hypothesis Delta_1 <= eps_0 is a CUT '
        'number, conclusion "P has a pair in [1/3,2/3]" is a PAIR number ***'),
    Row('14', 'Step 6/L4', 'eps_0^unif(U_either), restricted scope', 'PROVED', CUT, PAIR,
        'the same crossing, made refutable by dropping disjunct (i); CEILING only'),
    Row('15', 'Step 6/L4', 'the same, required scope', 'REFUTED', CUT, PAIR,
        'the same crossing, REFUTED at every positive eps by mg-d3c7'),
    Row('16', 'Step 6/L4', 'F, L4 modulus', 'ABSENT', CUT, PAIR,
        'would be the same crossing; UNCONSUMED, so it does not gate (mg-345e)'),
    Row('17', 'Step 6/L4', 'branch (i): P has a 1/3-balanced pair', 'PROVED', PAIR, PAIR,
        'NOT a crossing: no cut appears in it. True at eps=1 on every exhibitable '
        'poset and FALSE BY HYPOTHESIS at a counterexample'),
    Row('18', 'Step 6/L4', 'branch (ii): modify <= F(eps)n interface elements', 'REFUTED', CUT, PAIR,
        'the same crossing by a structural route; unconsumable at every F>0 (mg-3af9)'),
    Row('19', 'Step 6/L4', 'branch (iii) as literally stated', 'REFUTED', CUT, PAIR,
        'the same crossing with an endpoint gap; no contradiction at any F>0'),
    Row('20', 'minimality', 'delta(P[A]), delta(P[B]) >= 1/3', 'PROVED', PAIR, PAIR,
        'pair -> pair, inside a SIDE; supplies the object the crossing must move'),
    Row('21', 'minimality', 'both-sides-chain escape', 'PROVED', PAIR, PAIR,
        'closed by Linial, width <= 2'),
    Row('22', 'contradiction', 'a balanced pair contradicts delta(P) < 1/3', 'PROVED', PAIR, PAIR,
        'pair -> pair, dimensionless'),
    Row('23', 'demand', 'eps_dem on chain (I)=(III)', 'PROVED*', CUT, CUT, 'arithmetic on cut numbers'),
    Row('24', 'demand', 'eps_dem <= 2 eps_leak (the cap)', 'PROVED*', CUT, CUT, 'arithmetic on cut numbers'),
]

print("=" * 78)
print("mg-7ae5 / A1 — THE ABSENT STEP, AND THE CHAIN'S CURRENCY CROSSINGS")
print("=" * 78)

print("\nA. THE 25 ROWS, EACH WITH THE TWO ENDS OF ITS CURRENCY DECLARED")
print("   (rows are mg-ac0c §1 verbatim; the currency columns are new here)\n")
print("   %-4s %-11s %-38s %-9s %s" % ('#', 'step', 'quantity', 'status', 'currency'))
for r in ROWS:
    mark = ' <<<' if r.crosses else ''
    print("   %-4s %-11s %-38s %-9s %-8s -> %-8s%s"
          % (r.num, r.step, r.quantity[:38], r.status, r.cin, r.cout, mark))

assert len(ROWS) == 25, 'mg-ac0c publishes 25 rows'

print("\nB. THE CROSSINGS")
cross = [r for r in ROWS if r.crosses]
print("   %d of 25 rows change currency." % len(cross))
by_dir = {}
for r in cross:
    by_dir.setdefault((r.cin, r.cout), []).append(r)
for (a, b), rs in sorted(by_dir.items()):
    print("\n   %s -> %s : rows %s" % (a, b, ' '.join(r.num for r in rs)))
    for r in rs:
        print("      %s  %-9s  %s" % (r.num, r.status, r.why))

print("\nC. P1, SCORED")
cut_to_pair = by_dir.get((CUT, PAIR), [])
live = [r for r in cut_to_pair if r.status in ('ABSENT',) and r.num != '16']
print("   CUT -> PAIR crossings          : %s" % ' '.join(r.num for r in cut_to_pair))
print("   of which REFUTED               : %s"
      % ' '.join(r.num for r in cut_to_pair if r.status == 'REFUTED'))
print("   of which CEILING-ONLY (no value): %s"
      % ' '.join(r.num for r in cut_to_pair if r.status == 'PROVED'))
print("   of which UNCONSUMED            : %s"
      % ' '.join(r.num for r in cut_to_pair if r.num == '16'))
print("   LEFT LIVE                      : %s" % ' '.join(r.num for r in live))
print("""
   P1 said 'the currency crosses exactly once, at the absent row'.
   SCORED AS A PARTIAL LOSS, and the correction is sharper than the prediction:

     - the chain crosses currency in THREE places, not one:
         PAIR -> SPECTRAL   row 01           the SUPPLY, and it is PROVED
         SPECTRAL -> CUT    rows 02-07       Cheeger (row 04) is PROVED
         CUT -> PAIR        rows 13,14,15,16,18,19   *** the transfer ***
     - within the CUT -> PAIR family every member is REFUTED, ceiling-only,
       or unconsumed EXCEPT row 13.  So the sentence that survives is:

       THE CHAIN CONVERTS PAIR-CURRENCY INTO SPECTRAL-CURRENCY BY A THEOREM
       (row 01, one line, unconditional) AND MUST CONVERT IT BACK ACROSS
       ROW 13, WHERE THERE IS NO THEOREM, NO VALUE AND NO CANDIDATE LEFT
       STANDING.  The architecture is a loop (mg-3af8) and the loop has
       exactly one open joint.""")

print("\nD. THE ABSENT STEP, STATED")
print("""
   Between row 12 (Step 5's output, EMPIRICAL, pinned at eps_leak = 1/5) and
   rows 20/22 (minimality and the contradiction, both PROVED), the chain needs:

     (T)  There is eps_0 > 0 such that for EVERY finite poset P with
          delta(P) < 1/3 and EVERY prefix cut (A_k, A_k^c) with
          Delta_1(A_k, A_k^c) <= eps_0, P has an incomparable pair {x,y}
          with p^P_xy in [1/3, 2/3].

   IN  : Delta_1 — an expected displacement per element of a CUT      (row 12)
   OUT : p_xy in [1/3,2/3] — a probability of a PAIR                  (row 20/22)
   BETWEEN: row 12 and row 20.  Nothing else sits there.

   Three readings of (T) are already dead and mg-ac0c records each:
     via branch (ii)              REFUTED unconditionally      row 18
     via branch (iii) as stated   REFUTED, endpoint gap        row 19
     via a UNIVERSAL (i)-free surrogate  REFUTED at every eps>0 row 15
   and one is alive but vacuous:
     via branch (i)               true at eps=1 on every exhibitable poset,
                                  FALSE BY HYPOTHESIS at a counterexample  row 17

   So (T) must be proved FROZEN-CONDITIONALLY — it must consume
   delta(P) < 1/3 — which is mg-dcae's rule, and it is what mg-ac0c §4 reached
   from the demand side.  A2 prices what that hypothesis is worth; A3 asks
   whether mg-0e8c's density restatement changes the answer.""")
