#!/usr/bin/env python3
"""
mg-6a2f — INDEPENDENT completeness check on mg-34bf / 57f962f.

Written from scratch. Does NOT import, read, or execute anything under
code/state_restructure_34bf/ (neither its spec nor its splitter nor its checker).
The only inputs are:
  * STATE.md as it stood at the parent commit  (baseline)
  * STATE.md as committed by mg-34bf           (after)
  * docs/state-history/*.md as committed        (after)

THE QUESTION: was anything LOST?

Method (deliberately different in construction from the author's, same in spirit
because there is only one honest way to ask it):

  A. WHOLE-FILE MULTISET CHECK.  Every whitespace-token occurrence in the baseline
     file must be matched by an occurrence somewhere in {after STATE.md} U
     {docs/state-history/*.md}.  This is coarse (it ignores order) but it is global:
     it catches material dropped from ANY line, not just the ten the author says it
     touched.

  B. PER-CELL MAXIMAL-RUN DECOMPOSITION, REACHABILITY-CONSTRAINED.  For each changed
     table cell, greedily decompose the baseline cell's token sequence into maximal
     contiguous runs that still occur, in order, in the union of
        (after version of THAT cell) U (history files THAT cell links to).
     A run of length 0 = a token that is not reachable from its own row = LOST.
     Short runs are reported because a decomposition into 1-2 word runs would mean
     the wording was shredded even though no word "went missing".

  C. MEANING-DRIFT SURFACE.  Baseline sentences that do NOT survive as a single
     verbatim sentence anywhere in the after-corpus are listed for hand reading.
     Token-level completeness cannot see a paraphrase that reuses all the words.
"""
import re, sys, subprocess, collections, os

BEFORE_REV = "97cb533"
AFTER_REV  = "57f962f"

def git_show(rev, path):
    return subprocess.run(["git","show",f"{rev}:{path}"],capture_output=True,text=True,check=True).stdout

def git_ls(rev, path):
    out = subprocess.run(["git","ls-tree","-r","--name-only",rev,path],capture_output=True,text=True,check=True).stdout
    return [l for l in out.split("\n") if l.strip()]

# ---------------------------------------------------------------- table parsing
CELL_SPLIT = re.compile(r'(?<!\\)\|')

def split_row(line):
    """Split a markdown table row into cells. Honours backslash-escaped pipes."""
    if not line.startswith("|"):
        return None
    parts = CELL_SPLIT.split(line)
    # leading '' before first pipe and trailing '' after last pipe
    if parts and parts[0].strip()=="" : parts = parts[1:]
    if parts and parts[-1].strip()=="": parts = parts[:-1]
    return [p.strip() for p in parts]

def tokens(s):
    return s.split()

# ---------------------------------------------------------------- run matching
class Corpus:
    """Token sequence with an index for fast contiguous-run lookup."""
    def __init__(self, toks):
        self.t = toks
        self.pos = collections.defaultdict(list)
        for i,tok in enumerate(toks):
            self.pos[tok].append(i)
    def longest_run_at(self, seq, i, cap=4000):
        """Longest L such that seq[i:i+L] occurs contiguously in self.t."""
        starts = self.pos.get(seq[i])
        if not starts:
            return 0
        best = 0
        for s in starts:
            L = 1
            while (i+L) < len(seq) and (s+L) < len(self.t) and self.t[s+L]==seq[i+L] and L < cap:
                L += 1
            if L > best:
                best = L
                if i+best >= len(seq):
                    break
        return best

def decompose(seq, corpus):
    """Greedy maximal-run decomposition. Returns (runs, lost_indices)."""
    runs=[]; lost=[]; i=0
    while i < len(seq):
        L = corpus.longest_run_at(seq, i)
        if L == 0:
            lost.append(i); i += 1
        else:
            runs.append((i, L)); i += L
    return runs, lost

# ---------------------------------------------------------------- load
before = git_show(BEFORE_REV,"STATE.md")
after  = git_show(AFTER_REV,"STATE.md")
hist_paths = [p for p in git_ls(AFTER_REV,"docs/state-history")]
hist = {p: git_show(AFTER_REV,p) for p in hist_paths}

bl = before.split("\n"); al = after.split("\n")
assert len(bl)==len(al), f"line count changed: {len(bl)} -> {len(al)}"
changed = [i for i in range(len(bl)) if bl[i]!=al[i]]

print("="*78)
print("mg-6a2f INDEPENDENT RELOCATION CHECK")
print("="*78)
print(f"baseline  {BEFORE_REV}:STATE.md   {len(before.encode()):,} bytes, {len(bl)-1} lines")
print(f"after     {AFTER_REV}:STATE.md   {len(after.encode()):,} bytes, {len(al)-1} lines")
print(f"history files: {len(hist_paths)}, {sum(len(v.encode()) for v in hist.values()):,} bytes")
print(f"lines differing: {len(changed)}  -> {[i+1 for i in changed]}")
print()

# ---------------------------------------------------------------- A. whole-file multiset
print("-"*78)
print("A. WHOLE-FILE TOKEN MULTISET CHECK (global; catches drops on ANY line)")
print("-"*78)
bcount = collections.Counter(tokens(before))
acount = collections.Counter(tokens(after))
for v in hist.values():
    acount.update(tokens(v))
missing = {}
for tok,n in bcount.items():
    have = acount.get(tok,0)
    if have < n:
        missing[tok] = (n, have)
print(f"baseline token occurrences : {sum(bcount.values()):,} ({len(bcount):,} distinct)")
print(f"after-corpus occurrences   : {sum(acount.values()):,} ({len(acount):,} distinct)")
if not missing:
    print("RESULT: 0 baseline token occurrences unaccounted for. PASS.")
else:
    print(f"RESULT: {len(missing)} distinct tokens short "
          f"({sum(n-h for n,h in missing.values())} occurrences). FAIL:")
    for tok,(n,h) in sorted(missing.items(), key=lambda kv:-(kv[1][0]-kv[1][1]))[:60]:
        print(f"   {n-h:3d} short  need {n} have {h}   {tok!r}")
print()

# ---------------------------------------------------------------- B. per-cell runs
print("-"*78)
print("B. PER-CELL MAXIMAL-RUN DECOMPOSITION, REACHABLE-FROM-ROW ONLY")
print("-"*78)
LINKRE = re.compile(r'docs/state-history/([A-Za-z0-9._-]+\.md)')
grand_words=0; grand_runs=0; grand_lost=0; shortest=None
percell=[]
for i in changed:
    bcells = split_row(bl[i]); acells = split_row(al[i])
    if bcells is None:
        print(f"line {i+1}: NOT a table row -- handled separately"); continue
    assert len(bcells)==len(acells), f"line {i+1}: column count {len(bcells)} -> {len(acells)}"
    # which columns changed
    diffcols=[c for c in range(len(bcells)) if bcells[c]!=acells[c]]
    key = bcells[0][:60]
    linked = sorted(set(LINKRE.findall(al[i])))
    reach = tokens(acells[-1] if len(diffcols)==0 else " ".join(acells[c] for c in diffcols))
    # be generous: reachable corpus = the WHOLE after row + every file it links to
    reach = tokens(al[i])
    for f in linked:
        p = "docs/state-history/"+f
        if p in hist: reach += tokens(hist[p])
        else: print(f"   !! line {i+1} links to MISSING file {p}")
    corp = Corpus(reach)
    seq = tokens(" ".join(bcells))   # whole baseline row
    runs, lost = decompose(seq, corp)
    smin = min((L for _,L in runs), default=0)
    grand_words += len(seq); grand_runs += len(runs); grand_lost += len(lost)
    shortest = smin if shortest is None else min(shortest,smin)
    percell.append((i+1,key,len(seq),len(runs),len(lost),smin,diffcols,linked))
    print(f"line {i+1:3d} | cols changed {diffcols} | {len(seq):5d} words -> "
          f"{len(runs):4d} runs, shortest {smin:3d}, LOST {len(lost)}")
    print(f"         links: {', '.join(linked) if linked else '(none)'}")
    if lost:
        print("         *** UNREACHABLE TOKENS ***")
        for j in lost[:40]:
            ctx = " ".join(seq[max(0,j-6):j+7])
            print(f"           {seq[j]!r}   ...{ctx}...")
    short = [(j,L) for j,L in runs if L < 5]
    if short:
        print(f"         {len(short)} run(s) shorter than 5 words:")
        for j,L in short[:20]:
            print(f"           len {L}: {' '.join(seq[j:j+L])!r}")
print()
print(f"TOTAL: {len(percell)} cells, {grand_words:,} baseline words, "
      f"{grand_runs} maximal runs, {grand_lost} words unreachable from their row, "
      f"shortest run {shortest}")
print()

# ------------------------------------------------- B'. strict variant: changed cell only
print("-"*78)
print("B'. STRICT VARIANT — decompose ONLY the changed cell against")
print("    (after version of that same cell) U (files that cell links to).")
print("    This is the comparable setup to the author's reported 11,625 / 125 / 8.")
print("-"*78)
tw=tr=tl=0; smin_all=None
for i in changed:
    bcells = split_row(bl[i]); acells = split_row(al[i])
    diffcols=[c for c in range(len(bcells)) if bcells[c]!=acells[c]]
    assert len(diffcols)==1, f"line {i+1}: {len(diffcols)} columns changed"
    c = diffcols[0]
    linked = sorted(set(LINKRE.findall(acells[c])))
    reach = tokens(acells[c])
    for f in linked:
        reach += tokens(hist["docs/state-history/"+f])
    corp = Corpus(reach)
    seq = tokens(bcells[c])
    runs, lost = decompose(seq, corp)
    smin = min((L for _,L in runs), default=0)
    tw+=len(seq); tr+=len(runs); tl+=len(lost)
    smin_all = smin if smin_all is None else min(smin_all,smin)
    print(f"line {i+1:3d} col {c} | {len(seq):5d} words -> {len(runs):4d} runs, "
          f"shortest {smin:3d}, LOST {len(lost)}")
    if lost:
        print("         *** UNREACHABLE ***")
        for j in lost[:40]:
            print(f"           {seq[j]!r}  ctx: ...{' '.join(seq[max(0,j-6):j+7])}...")
    for j,L in runs:
        if L < 8:
            print(f"         run len {L}: {' '.join(seq[j:j+L])!r}")
print(f"\nSTRICT TOTAL: {len(changed)} cells, {tw:,} words, {tr} maximal runs, "
      f"{tl} unaccounted, shortest run {smin_all}")
print(f"author reported: 10 cells, 11,625 words, 125 maximal runs, 0 unaccounted, shortest run 8")
