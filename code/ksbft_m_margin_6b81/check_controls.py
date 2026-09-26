#!/usr/bin/env python3
"""check_controls.py (mg-6b81): assert the controls recorded in out_controls.txt / out_gen.txt.

Positive checks must hold (0 violations, counts agree).  Each NEGATIVE CONTROL must fire; when it
does it prints CAUGHT.  Any failed assertion exits 1, so a silent control cannot read as a pass."""
import re, sys
ok = True
def need(cond, msg):
    global ok
    print(('  ok      ' if cond else '  BROKEN  ') + msg)
    ok = ok and cond

ctl = open('out_controls.txt').read()
gen = open('out_gen.txt').read()

need(ctl.count('MATCH') >= 6 and 'MISMATCH' not in ctl, 'counter controls (fib, brute) all MATCH')

# pruned generator vs full census minus CUT
gc = {int(m.group(1)): int(m.group(2)) for m in re.finditer(r'gencut n=(\d+) D=3 .* nonCUT-classes=(\d+)', gen)}
for m in re.finditer(r'AGG CT (\d+) (\d+) (\d+) \d+ \d+', ctl.split('== e2e')[0]):
    t, tot, cut = map(int, m.groups())
    need(tot - cut == gc.get(t), f't={t}: full census {tot} - CUT {cut} = {tot-cut} equals gencut {gc.get(t)}')

E = [list(map(int, m.groups())) for m in re.finditer(r'AGG E ' + ' '.join([r'(\d+)'] * 7), ctl)]
need(len(E) == 6, 'six e2e lines present')
pos, neg = [E[0], E[1], E[4]], [E[2], E[3], E[5]]
for e in pos:
    need(e[3] == 0 and e[5] == 0, f'e2e (Lemma 2.2 s): {e[3]} bracket violations, {e[5]} certified-but-unbalanced (must be 0,0)')
for e in neg:
    fired = e[3] > 0
    need(fired, f'NEGATIVE CONTROL e2e with s = t-D+1: {e[3]} bracket violations, {e[5]} bad certificates'
         + (' -- CAUGHT' if fired else ' -- DID NOT FIRE'))
need(E[2][5] > 0 and E[3][5] > 0, 'NEGATIVE CONTROL e2e range<=3: a "certified" pair unbalanced in P appears -- CAUGHT'
     if E[2][5] > 0 and E[3][5] > 0 else 'NEGATIVE CONTROL e2e range<=3 bad certificates: DID NOT FIRE')

narrow = re.findall(r'AGG CT 13 (\d+) 0 (\d+) 0', ctl.split('cert FIRING control')[1])
need(len(narrow) == 2 and all(int(f) > 0 for _, f in narrow),
     'NEGATIVE CONTROL narrowed interval: uncertified %s -- %s' % ([int(f) for _, f in narrow],
     'CAUGHT' if narrow and all(int(f) > 0 for _, f in narrow) else 'DID NOT FIRE'))

# the headline numbers of the theorems
for fn, t, tot in (('out_cert_d3.txt', 11, 4224), ('out_cert_d4.txt', 15, 14298595)):
    m = re.search(r'AGG CT %d (\d+) (\d+) (\d+) (\d+)' % t, open(fn).read())
    need(m and int(m.group(1)) == tot and int(m.group(3)) == 0, f'{fn}: t={t} {tot} non-CUT classes, 0 uncertified')
base = open('out_base.txt').read()
need(base.count('LOW ') == 1 and 'LOW pi=2 margin=0/1 = 0.000000 P=3 0 0 2' in base,
     'out_base.txt: exactly one LOW line, 2+1 at delta = 1/3; no negative margin')

print('VERDICT:', 'GREEN' if ok else 'RED')
sys.exit(0 if ok else 1)
