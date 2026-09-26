"""check_95d3.py (mg-95d3): exit non-zero on any failed expectation or silent control in the out_*_95d3.txt files."""
import re, sys
bad=[]
def need(c,msg):
    print(("ok    " if c else "FAIL  ")+msg); c or bad.append(msg)
g=open('out_gen_95d3.txt').read()
cnt=lambda D,n: int(re.search(rf'gen D={D} n={n} .*classes=(\d+)',g).group(1))
need([cnt(-1,n) for n in range(2,11)]==[2,5,16,63,318,2045,16999,183231,2567284], "all classes n=2..10 = OEIS A000112")
need([cnt(3,n) for n in range(9,17)]==[2942,8362,23701,67116,190035,538329,1525168,4320980], "range<=3 counts n=9..16 = mg-eedd out_gen_range.txt")
need([cnt(4,n) for n in range(11,14)]==[178811,666778,2490595], "range<=4 counts n=11..13 = mg-eedd out_gen_range.txt")
c=open('out_controls_95d3.txt').read()
need(all(int(x)==0 for x in re.findall(r'^brute m=\d+:.*mismatches=(\d+)',c,re.M)), "counter = brute force (P and every P-v)")
need('FIRES' in c, "brute-force comparison control FIRES")
k=open('out_classify_pi2_95d3.txt').read()
need('none of A3, 2+2, F_n: 0 ' in k and 'FIRES' in k, "Pi_2 classification: 0 others to n=14; control FIRES")
s=open('out_sharp_95d3.txt').read(); need('formula mismatches: 0' in s, "Lemma R sharpness family: closed form exact")
def blocks(fn):
    return re.findall(r'#### (.*?)\n(.*?)(?=####|\Z)',open(fn).read(),re.S)
for name,b in blocks('out_census_95d3.txt'):
    v=lambda key: int(re.search(key+r'=(\d+)',b).group(1))
    need(v('exists_v_fail')==0 and v('lemmaR_viol')==0 and v('lemmaR_ctrl_viol')>0 and v('decomp_equiv_mismatch')==0,
         f"{name}: exists-v 0 failures, Lemma R 0 violations (control fires), Prop 1.2 equivalence 0 mismatches")
nb=blocks('out_control_narrow_95d3.txt')
need(sum(int(re.search(r'exists_v_fail=(\d+)',b).group(1)) for _,b in nb)>0, "narrow [2/5,3/5] control: exists-v FIRES")
need(sum(int(re.search(r'indec_equiv_mismatch=(\d+)',b).group(1)) for _,b in nb)>0, "narrow control: equivalence test FIRES on indecomposable P")
need(all(int(re.search(r'decomp_equiv_mismatch=(\d+)',b).group(1))==0 for _,b in nb), "narrow control: Prop 1.2 still exact on decomposable P (interval-free)")
print("RESULT:", "GREEN" if not bad else f"RED ({len(bad)} failures)"); sys.exit(1 if bad else 0)
