#!/usr/bin/env python3
"""mg-446b, targets 3 and 4: scope and beyond-brief additions.

mg-8fd1 was forbidden four things: surveying the literature, developing a
categorical formalism, touching the conjecture pricing, and extending to "other
set-represented categories".  All four are checked mechanically here, plus an
inventory of every claim the gate document makes that its ticket did not ask for.
"""
import re
import subprocess

GATE = "../../docs/OneThird-Unified-Framework-Gate.md"
PRE = ["../../docs/OneThird-Hodge-Side-Leverage.md",
       "../../docs/OneThird-Hodge-Side-Leverage-IndependentAudit.md",
       "../../STATE.md",
       "../../docs/OneThird-Semigroup-Walk-Family-Note.md"]
gate = open(GATE).read()
pre = "\n".join(open(p).read() for p in PRE)

print("=" * 78)
print("(3a) LITERATURE: every citation in the gate document, and whether the repo")
print("     already carried it (a new name would be evidence of a survey)")
print("=" * 78)
names = ["Brown", "Bidigare", "Hanlon", "Rockmore", "Diaconis", "Saliola",
         "Aldous", "Caputo", "Liggett", "Richthammer", "Young", "Coxeter",
         "Möbius", "Mobius", "Tsetlin", "Alev", "Lau", "Kaufman", "Oppenheim"]
for nm in names:
    ing = len(re.findall(nm, gate))
    inp = len(re.findall(nm, pre))
    if ing:
        print("  %-13s gate: %2d mentions   already in repo: %s"
              % (nm, ing, "YES (%d)" % inp if inp else "*** NO -- NEW NAME ***"))
newnames = [nm for nm in names if re.findall(nm, gate) and not re.findall(nm, pre)]
print("  citations introduced by the gate document that the repo did not already"
      " carry: %s" % (newnames if newnames else "NONE"))
print("  claims made ABOUT the literature (the forbidden activity would produce"
      " these):")
for i, l in enumerate(gate.split("\n"), 1):
    if re.search(r"literature|will return nothing|known in it|has been studied", l):
        print("     gate:%-4d %s" % (i, l.strip()[:110]))

print()
print("=" * 78)
print("(3b) CATEGORICAL FORMALISM: category-theory vocabulary in the gate document")
print("=" * 78)
vocab = ["functor", "natural transformation", "monoidal", "adjoint", "morphism",
         "category", "categories", "Yoneda", "colimit", "limit of", "2-category",
         "enriched", "presheaf"]
found = False
for v in vocab:
    for i, l in enumerate(gate.split("\n"), 1):
        if re.search(v, l, re.I):
            found = True
            print("  %-22s gate:%-4d %s" % (v, i, l.strip()[:100]))
if not found:
    print("  none")

print()
print("=" * 78)
print("(3c) CONJECTURE PRICING: files the commit touched, and pricing vocabulary")
print("=" * 78)
out = subprocess.run(["git", "show", "--stat", "--format=", "97cb533"],
                     capture_output=True, text=True, cwd="../..").stdout
print(out.strip())
for f in ("docs/roadmap.md", "STATE.md"):
    print("  %-18s touched by the commit: %s" % (f, "*** YES ***" if f in out else "no"))
for i, l in enumerate(gate.split("\n"), 1):
    if re.search(r"pricing|priced|2\^\{Θ|conjecture", l):
        print("     gate:%-4d %s" % (i, l.strip()[:110]))

print()
print("=" * 78)
print("(3d) OTHER SET-REPRESENTED CATEGORIES")
print("=" * 78)
for i, l in enumerate(gate.split("\n"), 1):
    if re.search(r"set-represented|other categories|generalis|generaliz", l):
        print("  gate:%-4d %s" % (i, l.strip()[:120]))

print()
print("=" * 78)
print("(4) WHAT THE GATE DOCUMENT ADDED BEYOND ITS BRIEF")
print("=" * 78)
added = [
 ("SS2.4 Theorem for all n (the ticket asked for n = 3,4,5 and 6 'if cheap', and "
  "for a characterisation IF a non-degenerate stable class existed)",
  "responsive but beyond; PROOF DEFECT -- see audit_proof.py"),
 ("SS2.3 two corrections to the ticket's own description of chains",
  "TRUE: |AC(C_n)| = 2^{n-1}, |G| = 2, unique minimiser -- reproduced"),
 ("SS2.5 |G(P)| histogram, D(P) comparison, non-injectivity of P -> AC(P)",
  "TRUE: 55/318 and 24/63 and 4231 -> 1316 with fibre 131 -- reproduced"),
 ("SS2.6 AC(P) is not a sublattice of Pi_n (join failure)",
  "mathematics TRUE (7/16, 49/63 reproduced); NOVELTY CLAIM FALSE -- the source "
  "says it"),
 ("SS1.3 the LRB mechanism as the live route, and the mg-66a6 identity of families",
  "responsive to L1's question; correctly attributed"),
 ("SS3 scope for the next ticket", "the ticket asked for the world statement; SS3.2 "
  "makes a claim about the literature"),
]
for what, verdict in added:
    print("  * %s\n      -> %s" % (what, verdict))
