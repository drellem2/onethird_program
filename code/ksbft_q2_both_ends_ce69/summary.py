"""summary.py (mg-ce69): collate the transcripts and assert (exit 1 otherwise):
  - PROVEN checks clean: gadget A1-A4, B (release time), C (cyclic sums), X (XYZ); swap ladder STEP/SL violations 0;
    SL conclusion violations 0 on the records; witness cross-checks agree.
  - firing controls fired: gadget ctrl1-4; swapladder CTRL_H1, CTRL_WIN; bothends CONTROL FIRES.
Prints the coverage table of doc sec. 4 (per file, NOT cumulative: slstruct/goodpair reset per file)."""
import re
import sys

bad = []


def last(path, key):
    t = open(path).read()
    m = re.findall(key, t)
    return m


g = open("out_gadget.txt").read()
if "RESULT violations=0 controls_fire" not in g:
    bad.append("gadget")
for f in ("out_swapladder_1.txt", "out_swapladder_2.txt"):
    if "RESULT violations=0 controls_fire" not in open(f).read():
        bad.append(f)
if "SL conclusion violations 0" not in open("out_slrecords.txt").read():
    bad.append("slrecords")
if "RESULT cross-checks agree" not in open("out_witness.txt").read():
    bad.append("witness")
if "CONTROL FIRES" not in open("out_bothends.txt").read():
    bad.append("bothends control")
bt = open("out_bothends.txt").read()
if len(re.findall(r"WIN_bot=FAILS WIN_top=FAILS", bt)) != 6:
    bad.append("bothends: Q_m family no longer fails WIN at both ends")

print("| population | indecomposable | SL fires (Thm 1.4) | Zaguia good pair | structural (Cor 1.6) | nested balanced pair |")
print("|---|---|---|---|---|---|")
gp = {m[0]: m[1:] for m in re.findall(r"file (\S+) posets=(\d+) good=(\d+) sl=(\d+)", open("out_goodpair.txt").read())}
st = {m[0]: m[1:] for m in re.findall(r"file (\S+) posets=(\d+) struct=(\d+) nested_bal=(\d+)", open("out_slstruct.txt").read() + open("out_slstruct_range.txt").read())}
for name in st:
    tot, s, nb = map(int, st[name])
    good, sl = (int(gp[name][1]), int(gp[name][2])) if name in gp else (None, None)
    fmt = lambda v: "—" if v is None else f"{v} ({100.0 * v / tot:.2f}%)"
    print(f"| {name} | {tot} | {fmt(sl)} | {fmt(good)} | {fmt(s)} | {fmt(nb)} |")
r = open("out_goodpair_records.txt").read()
print("records:", re.findall(r"file records .*", r)[0])
print("RESULT", "ALL CHECKS CLEAN, CONTROLS FIRE" if not bad else "FAILED: " + ", ".join(bad))
sys.exit(1 if bad else 0)
