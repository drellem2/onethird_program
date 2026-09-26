"""pinch.py (audit mg-6e7c): Pinch Lemma 1.2 of mg-ce69, tested as an event identity over the ideals of Inc(x).
Every ideal J of Z = Inc(x) (x minimal) occurs as the prefix before x with positive probability, so
{|J| <= t} = {x < w}  iff  for every ideal J of Z:  (|J| <= t)  <=>  (w not in J)."""
from aud import ups, incp


def ideals_of(dn, Z):
    Zm = sum(1 << z for z in Z)
    out = [0]
    seen = {0}
    i = 0
    while i < len(out):
        I = out[i]
        i += 1
        for z in Z:
            if not I >> z & 1 and (dn[z] & Zm) & ~I == 0:
                J = I | 1 << z
                if J not in seen:
                    seen.add(J)
                    out.append(J)
    return out


def pinch_levels_event(dn, x, sloppy=False):
    n = len(dn)
    up = ups(dn)
    Z = [z for z in range(n) if incp(dn, up, x, z)]
    ids = ideals_of(dn, Z)
    lv = []
    for t in range(len(Z) + 1):
        for w in Z:
            if all((bin(J).count("1") <= t) == (not J >> w & 1) for J in ids):
                lv.append(t)
                break
    return lv


def pinch_levels_struct(dn, x, sloppy=False):
    """Z = L (+) {w} (+) M (ordinal sum), |L| = t.  sloppy=True drops the 'M above w' clause (control)."""
    n = len(dn)
    up = ups(dn)
    Z = [z for z in range(n) if incp(dn, up, x, z)]
    lv = []
    for t in range(len(Z) + 1):
        for w in Z:
            L = [z for z in Z if dn[w] >> z & 1]
            M = [z for z in Z if z != w and z not in L]
            if len(L) == t and (sloppy or all(up[w] >> z & 1 for z in M)):
                lv.append(t)
                break
    return lv
