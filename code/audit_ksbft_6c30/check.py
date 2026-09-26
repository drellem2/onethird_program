"""check.py (audit mg-6c30): assertions over the transcripts; exit 1 on any failure."""
import re, sys, ast
fail = []
def need(cond, msg):
    print(('OK   ' if cond else 'FAIL ') + msg)
    if not cond: fail.append(msg)
r = lambda f: open(f).read()
g = r('out_gen.txt'); need(g.count('True') == 9, 'generator counts == OEIS A022493, n<=9, all distinct')
b = r('out_badl_4_9.txt')
for n in range(4, 9): need(f"n={n}: non-chain" in b and re.search(rf"n={n}:.*K-bad L: 0;", b), f'n={n}: no K-bad dominance L')
need("n=9: non-chain 31239; posets with a K-bad dominance L: 2; K-bad L: 2; first-match kill {'TS': 2}" in b, 'O9a/O9b: 2 bad L, both killed by Thm 3.1')
need("[3,4] [2,6] [4,5]" in b, 'O9a/O9b witness L contains the triple [3,4] [2,6] [4,5]')
b10 = r('out_badl_10.txt')
need("posets with a K-bad dominance L: 24; K-bad L: 29; first-match kill {'3.1*': 1, 'TS': 28}" in b10 and 'survivors 0' in b10, 'n=10: 24 posets / 29 L, 28 TS + 1 3.1*, 0 survivors')
p = r('out_props.txt'); d = {k: ast.literal_eval(v) for k, v in (l.split(' ', 1) for l in p.splitlines())}
io, ge = d['io'], d['gen']
need(io['t11_bad'] == 0 and ge['t11_bad'] == 0 and io['t11_ctrl'] > 0 and ge['t11_ctrl'] > 0, 'Thm 1.1 exact, control fires')
need(io['t31_bad'] == 0 and ge['t31_bad'] == 0 and io['t31_ctrl'] > 0 and ge['t31_ctrl'] > 0, 'Thm 3.1 inequality, control fires')
need(io['p22'] > 0 and io['p22_bad'] == 0 and io['p22_ctrl_bad'] > 0, 'Prop 2.2, control (Z != S) fires')
need(io['p24'] > 0 and io['p24_bad'] == 0 and io['p24_ctrl_bad'] > 0, 'Prop 2.4, control (non-unique maximal) fires')
w = r('out_witnesses.txt')
need("e = 11" in w and w.count("= 8/11") == 3 and "(3, 5, 3)" in w, 'P5: e=11, three laws 8/11, L1/L2/L3 = 3/5/3')
need("every law in X outside [1/3,2/3]: True" in w and "no X element between a and a' in the 2/3-order: True" in w, 'AA dominance LCC witness n=7')
need("P[a<a']=2/3 P[s<a']=1/3 P[t<a']=1/5 P[s<t]=43/60" in w and "equality P[a<a'] = 2P[s<a']: True" in w, 'T11 values and Prop 2.4 equality')
need("kills: []" in w and "K-bad: True" in w, 'sec 5 general n=9 survivor survives')
l = r('out_lcc.txt')
for row in ["('AB', 'DOM'): [12, 12, 1, 0, 0, 0]", "('AA', 'DOM'): [660, 524, 5, 2, 0, 0]", "('AB', 'DOM'): [44873, 40469, 12038, 186, 8, 0]",
            "('AA', 'CONT'): [20429, 2689, 0, 0, 0, 0]", "('AA', 'DOM'): [36436, 26581, 1002, 135, 0, 0]"]:
    need(row in l, 'LCC row ' + row)
need(not re.search(r"\[\d+, \d+, \d+, \d+, \d+, [1-9]", l), 'LCC on all of P is 0 everywhere (sanity control)')
lc = r('out_lemmac_census.txt')
need("n=9: K-bad posets 2, K-bad L 2, Lemma C fires on 2" in lc and "n=10: K-bad posets 24, K-bad L 29, Lemma C fires on 29" in lc, 'Lemma C rule kills all census obstructions')
rb = r('out_rand_badl.txt')
need("'SURVIVES'" in rb and "rand {'posets': 3000, 'with_bad': 0" in rb, 'own staircase family has Thm-3.1 survivors (positive control); uniform random has no bad L')
need("SURVIVOR n=11" not in rb, 'no survivor below n=12 in own staircase sample')
lm = r('out_lemmac.txt'); m = re.search(r"surviving \(P,L\): (\d+); Lemma C fires on (\d+)", lm)
need(m and m.group(1) == m.group(2) and int(m.group(1)) > 0, 'Lemma C fires on every own-family survivor')
lp = r('out_lpprobe.txt')
need("own-engine kills=[]" in lp and "eps* = 1/21  | +600 3-cycle rows: eps* = 1/21" in lp and "eps* = 1/48  | +600 3-cycle rows: eps* = 1/48" in lp, 'Q12: author LP 1/21, 1/48; 3-cycle rows do not move it')
need("((2, 5), 3)" in lp and "((5, 8), 3)" in lp, 'Q12 centre triples k = 3')
lp2 = r('out_lpprobe2.txt')
need("eps* = 1/21" in lp2 and "eps* = 1/48" in lp2, 'Q12: explicit Thm 3.1 rows do not move eps*')
print('ALL OK' if not fail else f'{len(fail)} FAILURES'); sys.exit(1 if fail else 0)
