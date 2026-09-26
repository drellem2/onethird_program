#!/usr/bin/env python3
"""check_controls_f889.py (mg-f889): asserts every positive check and every firing control in the
out_*.txt transcripts of this directory.  Prints NEGATIVE CONTROL ... CAUGHT for each control that
fires; exits 1 (VERDICT: RED) if a positive check fails or a negative control stays silent."""
import re, sys, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
R=lambda f: open(f).read()
bad=[]
def pos(name, ok):
    print(f"{'OK  ' if ok else 'FAIL'} {name}");  ok or bad.append(name)
def neg(name, fired):
    print(f"NEGATIVE CONTROL {name}: {'CAUGHT' if fired else 'SILENT'}");  fired or bad.append(name)

a=R('out_a000112.txt'); pos('A000112 n=1..8', [int(x) for x in re.findall(r'classes=(\d+)',a)]==[1,2,5,16,63,318,2045,16999])
b=R('out_control_brokencanon.txt'); neg('broken canonical form overcounts A000112', [int(x) for x in re.findall(r'classes=(\d+)',b)][:5]!=[1,2,5,16,63])
f=R('out_full3.txt'); g=R('out_gen3.txt')
full=dict((int(t),int(c)) for t,c in re.findall(r't=(\d+) classes=\d+ nonCUT=(\d+)',f))
pr=dict((int(t),int(c)) for t,c in re.findall(r't=(\d+) nonCUT-classes=(\d+)',g))
pos('unpruned census minus CUT == pruned generator, D=3, t<=12', all(full[t]==pr[t] for t in full) and len(full)>=12)
pos('D=3 counts == pcert (938,2001,4224,9307,20459)', [pr[t] for t in (9,10,11,12,13)]==[938,2001,4224,9307,20459])
g4=dict((int(t),int(c)) for t,c in re.findall(r't=(\d+) nonCUT-classes=(\d+)',R('out_gen4.txt')))
pos('D=4 counts == pcert (29491,103198,357363,1224360)', [g4.get(t) for t in (10,11,12,13)]==[29491,103198,357363,1224360])
c3=R('out_cert3.txt')
pos('D=3 uncertified 13/4/0/0 at t=9..12', re.findall(r'cert D=3 t=\d+: classes=\d+ uncertified=(\d+)',c3)[:4]==['13','4','0','0'])
pos('D=3 t=11 worst rm 1/96, s=8 certifies all 4224', 'cert D=3 t=11 s=8: classes=4224 uncertified=0 worst(max_s rm)=1/96' in c3)
c4=R('out_cert4.txt')
pos('D=4 uncertified 990/943/496/192 at t=10..13', re.findall(r'cert D=4 t=\d+: classes=\d+ uncertified=(\d+)',c4)==['990','943','496','192'])
neg('interval [2/5,3/5] must leave classes uncertified at D=3 t=11', int(re.search(r'uncertified=(\d+)',R('out_control_narrow.txt')).group(1))>0)
b3=R('out_base3.txt')
pos('D=3 base: only zero is 2+1, no negative, min pi=3 5/318, 2583 indecomposable n=2..11',
    b3.count('ZERO margin')==1 and 'ZERO margin: n=3 P=0 0 1' in b3 and 'NEGATIVE' not in b3 and 'pi=3:642 min=5/318' in b3 and 'n=2..11: 2583' in b3)
b8=R('out_base_all8.txt'); pos('all posets n<=8: only zero is 2+1', b8.count('ZERO margin')==1 and 'NEGATIVE' not in b8)
w=R('out_witness.txt'); pos('mg-2912 witness: range 4, indecomposable, delta-1/3=721/46455 < 5/318',
    'range=4 indecomposable=True delta-1/3=721/46455' in w and 'below 5/318: True' in w)
e=R('out_e2e.txt').splitlines()
on=[l for l in e if 'OFF=0' in l]; off=[l for l in e if 'OFF=1' in l]
pos('e2e Theorem 2.4: 0 bracket violations, 0 bad certificates', len(on)==3 and all('bracket-violations=0 ' in l and 'dist(pP)<rm=0 ' in l for l in on))
neg('e2e s=t-D+1 (violates Lemma 2.2) must break the bracket', len(off)==2 and all(not re.search(r'bracket-violations=0 ',l) for l in off))
pc=R('out_pcert_rerun.txt')
pos('pcert re-run: AGG CT 15 14298595 0 0 0 and AGG CT 14 4177332 0 14 0', 'AGG CT 15 14298595 0 0 0' in pc and 'AGG CT 14 4177332 0 14 0' in pc)
sd=R('out_sample_d4.txt').splitlines()
pos('my certifier: the 14 t=14 failures fail', 'sampled=14 range>D=0 CUT=0 uncertified=14' in sd[0])
pos('my certifier: t=15 worst class rm = 1/150', 'worst(max_s rm)=1/150' in sd[2])
m=re.search(r'sampled=(\d+) range>D=0 CUT=0 uncertified=(\d+) .*distinct-canon=(\d+)',sd[3])
pos('my certifier: 1% sample of t=15 all certified, distinct, non-CUT, range<=4', m and m.group(2)=='0' and m.group(1)==m.group(3))
print('VERDICT:', 'RED '+str(bad) if bad else 'GREEN'); sys.exit(1 if bad else 0)
