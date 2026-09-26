"""describe.py -- human-readable structure of probe records (mg-2912)."""
import json, sys
from fractions import Fraction

def covers(down):
    n = len(down); out = []
    for b in range(n):
        for a in range(n):
            if down[b] >> a & 1 and not any(down[b] >> c & 1 and down[c] >> a & 1 for c in range(n)):
                out.append((a, b))
    return out

def levels_str(rec):
    """elements listed in height order v_1..v_n with their incomparables"""
    down = rec["down"]; n = len(down); ordr = rec["ord"]; pos = {v: i + 1 for i, v in enumerate(ordr)}
    inc = []
    for v in ordr:
        I = sorted(pos[u] for u in range(n) if u != v and not (down[v] >> u & 1) and not (down[u] >> v & 1))
        inc.append(f"{pos[v]}:{{{','.join(map(str, I))}}}")
    return " ".join(inc)

def describe(rec):
    e = int(rec["e"]); down = rec["down"]; n = len(down); ordr = rec["ord"]
    pos = {v: i + 1 for i, v in enumerate(ordr)}
    d = [Fraction(int(rec["S"][v]), e) - (i + 1) for i, v in enumerate(ordr)]
    cov = sorted((pos[a], pos[b]) for a, b in covers(down))
    x, y = rec["pair"]
    return (f"n={n} pi={rec['pi']} w={rec['width']} e={e} delta={Fraction(int(rec['delta_num']), e)}"
            f"={int(rec['delta_num'])/e:.6f} pair=(v{pos[x]},v{pos[y]}) npairs={rec['npairs']} "
            f"M={Fraction(int(rec['M_num']), e)}={int(rec['M_num'])/e:.6f} at v{rec['M_at']}\n"
            f"   covers(height-index)={cov}\n   incomparables={levels_str(rec)}\n"
            f"   d=[{', '.join(f'{float(t):+.3f}' for t in d)}]")

if __name__ == "__main__":
    tag = sys.argv[1]; lim = int(sys.argv[2])
    for f in sys.argv[3:]:
        k = 0
        for line in open(f):
            o = json.loads(line)
            if o["tag"] == tag and k < lim:
                print(describe(o["rec"])); k += 1
