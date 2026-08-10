"""mg-d19f r1 — WHICH OF THE TWO LANDED CLAIMS IS TRUE.

The ticket's instruction: establish which claim is true at HEAD from the UNDERLYING
MEASUREMENT, correct the false site, and leave the true one alone. Do not harmonise.

The contradiction is not numeric. It is one document's claim ABOUT another document's
TEXT, so the underlying measurement has two parts and both are read here:

  (i)  THE TEXT.   Read mg-28ff at cb496e9 -- the only revision that existed when mg-51f4
       wrote its sentence -- and check mg-29fe's three joints against it directly.
  (ii) THE NUMBER. Read 168 of 86278 out of mg-51f4's OWN transcript, because that is the
       number that makes mg-28ff's repair row say 'false of the truth', and it is mg-51f4's
       measurement. The document being repaired supplies the evidence that repairs it.
"""

import os

import libd19f as L

orig = L.show(L.C_28FF_AS_READ, L.DOC_28FF).split("\n")
head28 = L.head_lines(L.DOC_28FF)
head51 = L.head_lines(L.DOC_51F4)


def q(lines, n):
    return lines[n - 1].strip()


L.banner("r1 — THE ADJUDICATION")

print("""
THE TWO CLAIMS, AT HEAD, TODAY
""")
for ln in L.find(head51, "correctly labelled as such at every appearance"):
    print(f"  {L.DOC_51F4}:{ln}")
    print(f"    {q(head51, ln - 1)}")
    print(f"    {q(head51, ln)}")
for ln in L.find(head51, "was correctly labelled a sample at each"):
    print(f"  {L.DOC_51F4}:{ln}  <- A SECOND SITE, NOT IN THE TICKET BODY")
    print(f"    {q(head51, ln)}")
    print(f"    {q(head51, ln + 1)}")
print()
for ln in L.find(head28, "read a **sample** as an enumeration"):
    print(f"  {L.DOC_28FF}:{ln}")
    print(f"    {q(head28, ln)[:200]}")

print("""

(i) THE TEXT OF mg-28ff AS mg-51f4 READ IT (cb496e9) -- mg-29fe's THREE JOINTS, CHECKED
""")

verdicts = []

# ---- joint 1: the summary sentence promotes the sample to an enumeration.
j1_line = L.find(orig, "100 % at every enumerated")
# The table row it sits under must be a SAMPLE row. Search upward for the nearest n=7 row.
row = None
for i in range(j1_line[0] - 2, j1_line[0] - 12, -1):
    if orig[i - 1].startswith("| 7 ") or orig[i - 1].startswith("> | 7 "):
        row = i
        break
j1 = bool(j1_line) and row is not None and "(sample)" in orig[row - 1]
verdicts.append(("joint 1  SS4.3 summary reads a SAMPLE as an ENUMERATION", j1))
print(f"  [{'CONFIRMED' if j1 else 'REFUTED'}] joint 1")
print(f"      {L.DOC_28FF}@{L.C_28FF_AS_READ}:{row}  {q(orig, row)}")
print(f"      {L.DOC_28FF}@{L.C_28FF_AS_READ}:{j1_line[0]}  {q(orig, j1_line[0])}")
print("      the row two lines above the sentence is a SAMPLE; the sentence says ENUMERATED.")
print("      That is an APPEARANCE of an n = 7 figure that is not correctly labelled.")

# ---- joint 2: SS8.1's self-audit claims all three rows carry 'NOT a maximum'.
j2_claim = L.find(orig, "every `n = 7` row is labelled *sample, not a")
n7_rows = [i + 1 for i, ln in enumerate(orig)
           if (ln.startswith("| 7 ") or ln.startswith("> | 7 ")) and "(sample" in ln]
carries = [(i, "NOT a maximum" in orig[i - 1]) for i in n7_rows]
n_carry = sum(1 for _, c in carries if c)
j2 = bool(j2_claim) and n_carry == 1 and len(carries) == 3
verdicts.append(("joint 2  SS8.1's own scope self-audit is FALSE at 2 of its 3 rows", j2))
print()
print(f"  [{'CONFIRMED' if j2 else 'REFUTED'}] joint 2")
print(f"      {L.DOC_28FF}@{L.C_28FF_AS_READ}:{j2_claim[0]}  {q(orig, j2_claim[0])}")
for i, c in carries:
    print(f"      :{i}  {'carries' if c else '   LACKS'} 'NOT a maximum'   {q(orig, i)}")
print(f"      {n_carry} of {len(carries)} rows carry it. The self-audit says all three.")

# ---- joint 3: SS4.2's population is a different sample.
import re as _re

# Report the draw PER CALL SITE, not per file. b1_footrule.py carries two different draws
# at two different lines, and a per-file summary would print '90, 200' for one script and
# read as a contradiction inside it rather than as two arms of it. The rows in question are
# named by mg-3bb9's repair-E table: b2_census.py:138, b1_footrule.py:73, b5_trend.py:48.
gens = []
for path in ("code/l2_conditionality_28ff/b2_census.py",
             "code/l2_conditionality_28ff/b1_footrule.py",
             "code/l2_conditionality_28ff/b5_trend.py"):
    try:
        txt = open(f"{L.REPO}/{path}", encoding="utf-8").read()
    except OSError:
        continue
    for i, ln in enumerate(txt.split("\n"), 1):
        for d in _re.findall(r"sample_posets\(7,\s*(\d+)\)", ln):
            gens.append((f"{os.path.basename(path)}:{i}", d))
CITED = {"b2_census.py:138": "§4.2 c♯(7)",
         "b1_footrule.py:73": "§4.3 f*(7)",
         "b5_trend.py:48": "§4.1 c_true(7)"}
draws = sorted({d for k, d in gens if k in CITED})
j3 = len(draws) >= 2
verdicts.append(("joint 3  SS4.2's n = 7 population is a DIFFERENT sample, unstated", j3))
print()
print(f"  [{'CONFIRMED' if j3 else 'REFUTED'}] joint 3")
for k, d in gens:
    tag = CITED.get(k, "(not a cited row -- listed so the census is complete)")
    print(f"      {k:22s} sample_posets(7, {d:3s})   {tag}")
print(f"      distinct draw sizes AT THE CITED ROWS: {draws}   -> the three rows labelled '(sample)' are")
print("      not the same sample. mg-3bb9's repair E re-measured the EVALUATED populations")
print("      as 98 and 208 (primitive 40 and 106), the draws supplying 35 and 101 of them.")

print("""

(ii) THE UNDERLYING NUMBER, FROM mg-51f4's OWN TRANSCRIPT
""")
t = open(f"{L.REPO}/code/sweep_loss_51f4/out_s3_n7.txt", encoding="utf-8").read()
for ln in t.split("\n"):
    if "86278" in ln and ("FAILS" in ln or "primitive posets on [7]" in ln):
        print(f"  code/sweep_loss_51f4/out_s3_n7.txt:  {ln.strip()}")
print("""
  So (F) is FALSE at n = 7 exhaustively. mg-28ff's SS4.3 summary said '100 % at every
  ENUMERATED n' over a table whose n = 7 row was a 106-poset sample -- and the exhaustive
  n = 7 that mg-51f4 itself produced is what makes that sentence false of the truth.
  mg-51f4 SUPPLIED THE MEASUREMENT THAT REFUTES THE SENTENCE IT CERTIFIED AS CORRECT.
""")

print("""
THE VERDICT
""")
ok = all(v for _, v in verdicts)
for name, v in verdicts:
    print(f"  [{'CONFIRMED' if v else 'REFUTED'}] {name}")
print(f"""
  mg-28ff:{L.find(head28, 'read a **sample** as an enumeration')[0]} (mg-29fe's repair row)  -> TRUE. LEFT ALONE.
  {L.DOC_51F4}:{L.find(head51, 'correctly labelled as such at every appearance')[0]}                        -> FALSE. STRUCK AND CORRECTED BESIDE.
  {L.DOC_51F4}:{L.find(head51, 'was correctly labelled a sample at each')[0]}                        -> FALSE. STRUCK AND CORRECTED BESIDE.

  AND THE SECOND SITE IS THE SHARPER ONE. mg-51f4's SS11 says 'None of these is a labelling
  failure' THREE LINES ABOVE its own site 1, which describes mg-28ff:247 in these words:
  'The word *enumerated* sat over a table whose n = 7 row was a sample, so the sentence
  reads as covering n = 7 and is false there.' That IS mg-29fe's joint 1, found
  independently by mg-51f4, tabulated by mg-51f4, and then denied by mg-51f4's own blanket
  sentence one paragraph above it. The two documents never disagreed about the FACT. They
  disagreed about a SUMMARY of the fact, and the summary was written last.
""")
print("ADJUDICATION COMPLETE" if ok else "ADJUDICATION INCOMPLETE -- a joint did not confirm")
raise SystemExit(0 if ok else 1)
