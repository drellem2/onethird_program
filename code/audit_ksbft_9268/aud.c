/* aud.c (mg-9268) -- INDEPENDENT re-implementation of the KSBFT-I finite
 * search (mg-e8b4, docs/KSBFT-I-finite-state.md Thm 5), written by the
 * auditor from the doc's lemmas, not from tree.c.  Differences of mechanism:
 *   - children enumerated by building the new element's DOWN-set in
 *     ascending position order (tree.c builds the up-set U descending);
 *   - incomparability counts recomputed from up/down masks at every node
 *     (tree.c keeps an incremental counter);
 *   - layers stepped by a PULL recurrence over the maximal elements of each
 *     new state, with a sorted array + binary search, which aborts if a
 *     predecessor state is missing (tree.c pushes into a hash table);
 *   - the complete-poset check computes P[a<b] for EVERY incomparable pair
 *     (not only the tracked ones) by a forward/backward down-set DP over the
 *     whole poset, from scratch (tree.c steps the tracked layer forward);
 *   - own simplex (Bland), rounding to NEAREST integer on a 2^28 grid, exact
 *     int128 verification; the LP pair set is recomputed here;
 *   - split by the DFS index of depth-S NODES (tree.c: of children created
 *     at depth S), so slice membership differs and only totals compare.
 * Output: per-depth nodes / cert / lp / cutpruned / frontier, and a RESULT.
 * usage: aud D MAXDEPTH [lo_num lo_den] [nolp] [nodcut] [split:I/M@S]      */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef unsigned __int128 U;
typedef __int128 S;
typedef uint64_t M;
#define MX 48
static int D, MAXD, NOLP = 0, NODCUT = 0, BADCUT = 0, SI = 0, SM = 1, SS = -1;
static M LN = 1, LD = 3;
static M dn[MX], up[MX];          /* strict down / up masks inside prefix */
static long long cnt_nodes[MX + 2], cnt_cert[MX + 2], cnt_lp[MX + 2], cnt_cut[MX + 2], cnt_front[MX + 2], cex = 0, lptry = 0;
static int FOLLOW = 0, FN = 0; static M FT[MX]; static int fdone; static char fmsg[4096];
static long long SAMPLE = 0, samp_ctr = 0;
static void emit(int n) { if (!SAMPLE || (samp_ctr++ % SAMPLE)) return; printf("SAMPLE n=%d [", n); for (int i = 0; i < n; i++) printf("%s%llu", i ? "," : "", (unsigned long long)dn[i]); printf("] %s\n", fmsg); }
static long long split_ctr = 0; static int maxst = 0, maxpairs = 0;

static int pc(M x) { return __builtin_popcountll(x); }
static void die(const char *s) { fprintf(stderr, "FATAL %s\n", s); printf("FATAL %s\n", s); exit(4); }

/* ratio c/e  in [lo, 1-lo] ? */
static int inr(U c, U e) { return c * LD >= e * LN && c * LD <= e * (LD - LN); }

typedef struct { int n, k, np; M *st; U *e; U *c; int (*pr)[2]; } Lay;
static void lalloc(Lay *L, int n, int np) {
  L->n = n; L->np = np; L->st = malloc(sizeof(M) * (n ? n : 1)); L->e = malloc(sizeof(U) * (n ? n : 1));
  L->c = calloc((size_t)(n ? n : 1) * (np ? np : 1), sizeof(U)); L->pr = malloc(sizeof(int[2]) * (np ? np : 1));
}
static void lfree(Lay *L) { free(L->st); free(L->e); free(L->c); free(L->pr); }
static int cmpM(const void *a, const void *b) { M x = *(const M *)a, y = *(const M *)b; return x < y ? -1 : x > y; }
static int find(const Lay *L, M J) { int lo = 0, hi = L->n - 1;
  while (lo <= hi) { int m = (lo + hi) / 2; if (L->st[m] == J) return m; if (L->st[m] < J) lo = m + 1; else hi = m - 1; } return -1; }

/* next layer (cut k+1) from L (cut k), prefix of n elements; pull recurrence */
static void stepup(const Lay *L, Lay *R, int n) {
  int cap = L->n * n + 1; M *cand = malloc(sizeof(M) * cap); int nc = 0;
  for (int s = 0; s < L->n; s++) for (int z = 0; z < n; z++)
    if (!((L->st[s] >> z) & 1) && (dn[z] & ~L->st[s]) == 0) cand[nc++] = L->st[s] | (1ULL << z);
  qsort(cand, nc, sizeof(M), cmpM);
  int u = 0; for (int i = 0; i < nc; i++) if (!u || cand[i] != cand[u - 1]) cand[u++] = cand[i];
  lalloc(R, u, L->np); R->k = L->k + 1; memcpy(R->pr, L->pr, sizeof(int[2]) * L->np);
  for (int t = 0; t < u; t++) {
    M J = cand[t]; R->st[t] = J; U e = 0;
    for (int z = 0; z < n; z++) if (((J >> z) & 1) && (up[z] & J) == 0) {   /* z maximal in J */
      int s = find(L, J & ~(1ULL << z)); if (s < 0) die("predecessor state missing");
      e += L->e[s];
      for (int p = 0; p < L->np; p++) { int a = L->pr[p][0], b = L->pr[p][1]; M I = J & ~(1ULL << z);
        if (((I >> a) & 1) && ((I >> b) & 1)) R->c[(size_t)t * L->np + p] += L->c[(size_t)s * L->np + p];
        else if (z == b && ((I >> a) & 1)) R->c[(size_t)t * L->np + p] += L->e[s]; }
    }
    if (e >> 110) die("count overflow");
    R->e[t] = e;
  }
  if (u > maxst) maxst = u;
  free(cand);
}

static int cutk(int n) {   /* complete cut for a prefix of n elements (Prop 1 + Lemma 2b) */
  int k = n - D; if (!NODCUT && n > 0 && pc(dn[n - 1]) > k) k = pc(dn[n - 1]);
  if (k > n) k = n; return k < 0 ? 0 : k;
}

/* pair status on layer: 2 certified, 0 hopeless, 1 live; also one-sidedness */
static int pstat(const Lay *L, int p, int *side) {
  int a = L->pr[p][0], b = L->pr[p][1], nin = 0, low = 0, high = 0, und = 0;
  for (int s = 0; s < L->n; s++) { M J = L->st[s]; int A = (J >> a) & 1, B = (J >> b) & 1;
    if (A && B) { U c = L->c[(size_t)s * L->np + p], e = L->e[s];
      if (c * LD < e * LN) low = 1; else if (c * LD > e * (LD - LN)) high = 1; else nin = 1; }
    else if (A) high = 1; else if (B) low = 1; else und = 1; }
  *side = und ? 0 : (low && !high) ? -1 : (high && !low) ? 1 : 0;
  if (!und && !low && !high) return 2;
  if (!und && !nin && (low != high)) return 0;
  return 1;
}

/* ---- own LP: max t st  sum_q lam_q a_Jq >= t (all J), sum lam = 1, lam >= 0.
 * variables x = (lam_1..lam_m, t+ ) with t shifted: t = tp - 1 so tp >= 0
 * rows:  tp - sum_q lam_q a_Jq <= 1     (J)       slack s_J
 *        sum lam <= 1                            slack s_0 ; we also add
 *        tp <= 2  (bounded)                       slack s_T
 * Bland's rule simplex on a dense tableau.                               */
static double *T = 0; static size_t Tcap = 0;
static double lpsolve(int R0, int m, const double *a, double *lam) {
  int R = R0 + 2, C = m + 1 + R + 1;
  size_t need = (size_t)(R + 1) * C; if (need > Tcap) { free(T); T = malloc(sizeof(double) * need); Tcap = need; }
  memset(T, 0, sizeof(double) * need); int *bas = malloc(sizeof(int) * R);
  for (int j = 0; j < R0; j++) { double *r = T + (size_t)j * C; for (int q = 0; q < m; q++) r[q] = -a[(size_t)j * m + q]; r[m] = 1; r[m + 1 + j] = 1; r[C - 1] = 1; bas[j] = m + 1 + j; }
  { double *r = T + (size_t)R0 * C; for (int q = 0; q < m; q++) r[q] = 1; r[m + 1 + R0] = 1; r[C - 1] = 1; bas[R0] = m + 1 + R0; }
  { double *r = T + (size_t)(R0 + 1) * C; r[m] = 1; r[m + 2 + R0] = 1; r[C - 1] = 2; bas[R0 + 1] = m + 2 + R0; }
  double *ob = T + (size_t)R * C; ob[m] = -1;
  for (int it = 0; it < 20000; it++) {
    int e = -1; for (int j = 0; j < C - 1; j++) if (ob[j] < -1e-11) { e = j; break; }
    if (e < 0) break;
    int l = -1; double bq = 0;
    for (int i = 0; i < R; i++) { double v = T[(size_t)i * C + e]; if (v > 1e-11) { double q = T[(size_t)i * C + C - 1] / v;
      if (l < 0 || q < bq - 1e-13 || (q <= bq + 1e-13 && bas[i] < bas[l])) { l = i; bq = q; } } }
    if (l < 0) break;
    double pv = T[(size_t)l * C + e]; for (int j = 0; j < C; j++) T[(size_t)l * C + j] /= pv;
    for (int i = 0; i <= R; i++) if (i != l) { double f = T[(size_t)i * C + e]; if (f != 0) for (int j = 0; j < C; j++) T[(size_t)i * C + j] -= f * T[(size_t)l * C + j]; }
    bas[l] = e;
  }
  double tp = 0; for (int q = 0; q < m; q++) lam[q] = 0;
  for (int i = 0; i < R; i++) { if (bas[i] < m) lam[bas[i]] = T[(size_t)i * C + C - 1]; else if (bas[i] == m) tp = T[(size_t)i * C + C - 1]; }
  free(bas); return tp - 1;
}

static int lpcert(const Lay *L, const int *st, const int *side) {
  int m = 0, *q2p = malloc(sizeof(int) * (L->np + 1));
  for (int p = 0; p < L->np; p++) if (st[p] == 1 && side[p]) q2p[m++] = p;
  if (m < 2) { free(q2p); return 0; }
  lptry++;
  S *A = malloc(sizeof(S) * (size_t)L->n * m); double *af = malloc(sizeof(double) * (size_t)L->n * m);
  for (int s = 0; s < L->n; s++) { M J = L->st[s]; S e = (S)L->e[s];
    for (int q = 0; q < m; q++) { int p = q2p[q], a = L->pr[p][0], b = L->pr[p][1]; S c;
      int A_ = (J >> a) & 1, B_ = (J >> b) & 1;
      if (A_ && B_) c = (S)L->c[(size_t)s * L->np + p]; else if (A_) c = e; else if (B_) c = 0; else die("undetermined state in one-sided pair");
      /* scaled by LD*e(J) > 0:  side -1: rho - lo ;  side +1: hi - rho */
      S v = side[p] < 0 ? (S)LD * c - (S)LN * e : (S)(LD - LN) * e - (S)LD * c;
      A[(size_t)s * m + q] = v; af[(size_t)s * m + q] = (double)v / ((double)LD * (double)e); } }
  double *lam = malloc(sizeof(double) * m); double t = lpsolve(L->n, m, af, lam); int ok = 0;
  if (t > 1e-10) {
    long long *li = malloc(sizeof(long long) * m); long long tot = 0;
    for (int q = 0; q < m; q++) { double x = lam[q] * 268435456.0 + 0.5; li[q] = x < 1 ? 0 : (long long)x; tot += li[q]; }
    if (tot > 0) { ok = 1;
      for (int s = 0; s < L->n && ok; s++) { S sum = 0; for (int q = 0; q < m; q++) sum += (S)li[q] * A[(size_t)s * m + q]; if (sum < 0) ok = 0; } }
    if (ok && (FOLLOW || SAMPLE)) { int w = sprintf(fmsg, "LP k=%d", L->k); for (int q = 0; q < m; q++) if (li[q]) w += sprintf(fmsg + w, " %d,%d,%d,%lld", L->pr[q2p[q]][0], L->pr[q2p[q]][1], side[q2p[q]], li[q]); }
    free(li);
  }
  free(A); free(af); free(lam); free(q2p); return ok;
}

/* ---- complete check from scratch: does the n-element prefix, as a whole
 * poset, have an incomparable pair with P[a<b] in [lo,hi]?  fwd f(I) =
 * #ways to build down-set I, bwd g(I) = #ways to finish from I. */
typedef struct { M k; U f, g; } Ent;
static Ent *H = 0; static int Hcap = 0, Hn = 0;
static int cmpE(const void *a, const void *b) { M x = ((const Ent *)a)->k, y = ((const Ent *)b)->k; return x < y ? -1 : x > y; }
static int hfind(M k) { int lo = 0, hi = Hn - 1; while (lo <= hi) { int m = (lo + hi) / 2; if (H[m].k == k) return m; if (H[m].k < k) lo = m + 1; else hi = m - 1; } return -1; }
static int complete_ok(int n) {
  /* enumerate all down-sets by layers */
  Hn = 0; M full = (n == 64) ? ~0ULL : ((1ULL << n) - 1);
  M *cur = malloc(sizeof(M)), *nx; int nc = 1; cur[0] = 0;
  #define PUSH(x) do { if (Hn == Hcap) { Hcap = Hcap ? 2 * Hcap : 4096; H = realloc(H, sizeof(Ent) * Hcap); } H[Hn].k = (x); H[Hn].f = 0; H[Hn].g = 0; Hn++; } while (0)
  PUSH(0);
  for (int k = 0; k < n; k++) {
    nx = malloc(sizeof(M) * (nc * n + 1)); int nn = 0;
    for (int i = 0; i < nc; i++) for (int z = 0; z < n; z++) if (!((cur[i] >> z) & 1) && (dn[z] & ~cur[i]) == 0) nx[nn++] = cur[i] | (1ULL << z);
    qsort(nx, nn, sizeof(M), cmpM); int u = 0; for (int i = 0; i < nn; i++) if (!u || nx[i] != nx[u - 1]) nx[u++] = nx[i];
    for (int i = 0; i < u; i++) PUSH(nx[i]);
    free(cur); cur = nx; nc = u;
  }
  free(cur);
  qsort(H, Hn, sizeof(Ent), cmpE);
  /* forward in increasing popcount: process by size */
  int *ord = malloc(sizeof(int) * Hn); { int w = 0; for (int s = 0; s <= n; s++) for (int i = 0; i < Hn; i++) if (pc(H[i].k) == s) ord[w++] = i; }
  H[hfind(0)].f = 1;
  for (int w = 0; w < Hn; w++) { int i = ord[w]; M I = H[i].k; if (!I) continue; U f = 0;
    for (int z = 0; z < n; z++) if (((I >> z) & 1) && (up[z] & I) == 0) { int j = hfind(I & ~(1ULL << z)); if (j < 0) die("complete: missing"); f += H[j].f; }
    H[i].f = f; }
  H[hfind(full)].g = 1;
  for (int w = Hn - 1; w >= 0; w--) { int i = ord[w]; M I = H[i].k; if (I == full) continue; U g = 0;
    for (int z = 0; z < n; z++) if (!((I >> z) & 1) && (dn[z] & ~I) == 0) { int j = hfind(I | (1ULL << z)); if (j < 0) die("complete: missing up"); g += H[j].g; }
    H[i].g = g; }
  U tot = H[hfind(full)].f; if (H[hfind(0)].g != tot) die("complete: f/g mismatch");
  if (tot >> 118) die("complete overflow");
  int ok = 0;
  for (int a = 0; a < n && !ok; a++) for (int b = a + 1; b < n && !ok; b++) {
    if (((dn[b] >> a) & 1)) continue;   /* a<b comparable (a earlier) */
    /* # extensions with a before b = sum over down-sets I, a in I, b not in I, b addable: f(I) g(I+b) */
    U c = 0;
    for (int i = 0; i < Hn; i++) { M I = H[i].k; if (!((I >> a) & 1) || ((I >> b) & 1) || (dn[b] & ~I)) continue;
      int j = hfind(I | (1ULL << b)); c += H[i].f * H[j].g; }
    if (inr(c, tot)) ok = 1;
  }
  free(ord);
  return ok;
}

static int decomposable(int n) {
  for (int c = 1; c < n; c++) { M low = (1ULL << c) - 1; int ok = 1; for (int i = c; i < n; i++) if ((dn[i] & low) != low) { ok = 0; break; } if (ok) return 1; }
  return 0;
}

static void visit(int n, Lay *L);

/* build down-set of new element at position n, ascending over window */
static void kids(int n, Lay *L, int pos, int wlo, M Dsel, int usz) {
  if (pos == n) {
    M Dn = ((wlo > 0) ? ((1ULL << wlo) - 1) : 0) | Dsel;
    if (n > 0) { int d = pc(Dn), dp = pc(dn[n - 1]); if (d < dp || (d == dp && Dn < dn[n - 1])) return; }
    if (FOLLOW && (n >= FN || Dn != FT[n])) return;
    /* install */
    dn[n] = Dn; up[n] = 0; for (int j = 0; j < n; j++) if ((Dn >> j) & 1) up[j] |= 1ULL << n;
    int N1 = n + 1, pruned = 0;
    if (usz == 0 && n >= 1) pruned = 1;                    /* Lemma 2c */
    int c = N1 - 2 * D + 1;
    if (!pruned && c >= 1) { M low = (1ULL << c) - 1; int ok = 1; for (int i = c; i < N1; i++) if ((dn[i] & low) != low) { ok = 0; break; } if (ok) pruned = 1; }
    if (pruned) { cnt_cut[N1]++; if (FOLLOW) { sprintf(fmsg, "CUT at %d", N1); fdone = N1; } }
    else {
      /* child pairs: parent's live pairs + (a, n) for a incomparable */
      int np = L->np; for (int a = 0; a < n; a++) if (!((Dn >> a) & 1)) np++;
      Lay C0; lalloc(&C0, L->n, np); C0.k = L->k;
      memcpy(C0.st, L->st, sizeof(M) * L->n); memcpy(C0.e, L->e, sizeof(U) * L->n);
      for (int p = 0; p < L->np; p++) { C0.pr[p][0] = L->pr[p][0]; C0.pr[p][1] = L->pr[p][1]; }
      { int p = L->np; for (int a = 0; a < n; a++) if (!((Dn >> a) & 1)) { C0.pr[p][0] = a; C0.pr[p][1] = n; p++; } }
      for (int s = 0; s < L->n; s++) { if ((L->st[s] >> n) & 1) die("new element in old state");
        for (int p = 0; p < L->np; p++) C0.c[(size_t)s * np + p] = L->c[(size_t)s * L->np + p]; }
      if (np > maxpairs) maxpairs = np;
      int kt = cutk(N1); if (kt < C0.k) die("cut decreased");
      while (C0.k < kt) { Lay R; stepup(&C0, &R, N1); lfree(&C0); C0 = R; }
      visit(N1, &C0);
      lfree(&C0);
    }
    for (int j = 0; j < n; j++) up[j] &= ~(1ULL << n);
    return;
  }
  /* incomparability count of pos within the current prefix of n elements */
  int inc = n - 1 - pc(dn[pos]) - pc(up[pos]);
  /* pos in down-set: needs its down-set (within window) selected */
  M need = dn[pos] & ~((wlo > 0) ? ((1ULL << wlo) - 1) : 0);
  if ((need & ~Dsel) == 0) kids(n, L, pos + 1, wlo, Dsel | (1ULL << pos), usz);
  /* pos incomparable to new element */
  if (usz < D && inc < D) {
    /* up-set property: nothing below-closed violation later: any later q in Dsel with pos in dn[q] is rejected by need-check */
    kids(n, L, pos + 1, wlo, Dsel, usz + 1);
  }
}

static void visit(int n, Lay *L) {
  if (n == SS && SM > 1) { long long t = split_ctr++; if (t % SM != SI) return; }
  cnt_nodes[n]++;
  /* FIRING CONTROL ONLY (badcut): decide on the layer ONE cut above the safe
   * cut, i.e. V_{k+1} of the prefix, which may miss down-sets of completions */
  Lay RB, *L0 = L; int usedRB = 0;
  if (BADCUT && L->k < n) { stepup(L, &RB, n); L = &RB; usedRB = 1; }
  int *st = malloc(sizeof(int) * (L->np + 1)), *sd = malloc(sizeof(int) * (L->np + 1)), cert = 0;
  for (int p = 0; p < L->np; p++) { st[p] = pstat(L, p, &sd[p]); if (st[p] == 2) cert = 1; }
  if (cert) { cnt_cert[n]++;
    if (FOLLOW || SAMPLE) { int w = sprintf(fmsg, "CERT k=%d", L->k); for (int p = 0; p < L->np; p++) if (st[p] == 2) w += sprintf(fmsg + w, " %d,%d", L->pr[p][0], L->pr[p][1]); fdone = n; emit(n); }
    if (usedRB) lfree(&RB);
    free(st); free(sd); return; }
  if (!NOLP && lpcert(L, st, sd)) { cnt_lp[n]++; if (FOLLOW) fdone = n; emit(n); free(st); free(sd); if (usedRB) lfree(&RB); return; }
  if (usedRB) lfree(&RB);
  L = L0;
  int nl = 0; for (int p = 0; p < L->np; p++) if (st[p] == 1) nl++;
  Lay V; lalloc(&V, L->n, nl); V.k = L->k; memcpy(V.st, L->st, sizeof(M) * L->n); memcpy(V.e, L->e, sizeof(U) * L->n);
  { int q = 0; for (int p = 0; p < L->np; p++) if (st[p] == 1) { V.pr[q][0] = L->pr[p][0]; V.pr[q][1] = L->pr[p][1];
      for (int s = 0; s < L->n; s++) V.c[(size_t)s * nl + q] = L->c[(size_t)s * L->np + p]; q++; } }
  free(st); free(sd);
  if (n >= 2 && !decomposable(n) && !complete_ok(n)) {
    cex++; printf("VIOLATION n=%d [", n); for (int i = 0; i < n; i++) printf("%s%llu", i ? "," : "", (unsigned long long)dn[i]); printf("]\n"); fflush(stdout);
  }
  if (FOLLOW && n == FN) { sprintf(fmsg, "ENDED complete-check %s", complete_ok(n) ? "ok" : "VIOLATION"); fdone = n; lfree(&V); return; }
  if (n >= MAXD) { cnt_front[n]++; lfree(&V); return; }
  int wlo = n - 2 * D + 1; if (wlo < 0) wlo = 0;
  kids(n, &V, wlo, wlo, 0, 0);
  lfree(&V);
}

int main(int argc, char **argv) {
  if (argc < 3) { fprintf(stderr, "usage\n"); return 1; }
  D = atoi(argv[1]); MAXD = atoi(argv[2]); if (MAXD > MX - 1) MAXD = MX - 1;
  int i = 3; if (argc >= 5 && argv[3][0] >= '0' && argv[3][0] <= '9') { LN = strtoull(argv[3], 0, 10); LD = strtoull(argv[4], 0, 10); i = 5; }
  for (; i < argc; i++) {
    if (!strcmp(argv[i], "nolp")) NOLP = 1; else if (!strcmp(argv[i], "nodcut")) NODCUT = 1;
    else if (!strcmp(argv[i], "follow")) FOLLOW = 1;
    else if (!strcmp(argv[i], "badcut")) BADCUT = 1;
    else if (!strncmp(argv[i], "sample:", 7)) SAMPLE = atoll(argv[i] + 7);
    else if (!strncmp(argv[i], "split:", 6)) sscanf(argv[i] + 6, "%d/%d@%d", &SI, &SM, &SS);
    else { fprintf(stderr, "bad arg %s\n", argv[i]); return 1; } }
  if (FOLLOW) {   /* stdin: one poset per line, down-masks in canonical order */
    char line[8192];
    while (fgets(line, sizeof line, stdin)) { FN = 0; char *p = line; while (*p) { while (*p == ' ' || *p == ',' || *p == '[') p++; if (*p < '0' || *p > '9') break; FT[FN++] = strtoull(p, &p, 10); }
      if (!FN) continue; fdone = -1; strcpy(fmsg, "MISSED");
      Lay R; lalloc(&R, 1, 0); R.k = 0; R.st[0] = 0; R.e[0] = 1; visit(0, &R); lfree(&R);
      printf("FOLLOW n=%d depth=%d %s\n", FN, fdone, fmsg); }
    return 0; }
  Lay R; lalloc(&R, 1, 0); R.k = 0; R.st[0] = 0; R.e[0] = 1;
  visit(0, &R); lfree(&R);
  printf("# aud D=%d MAXDEPTH=%d lo=%llu/%llu%s%s split=%d/%d@%d\n", D, MAXD, (unsigned long long)LN, (unsigned long long)LD, NOLP ? " nolp" : "", NODCUT ? " nodcut" : "", SI, SM, SS);
  long long tot = 0, fr = 0;
  for (int n = 0; n <= MAXD + 1; n++) { if (!cnt_nodes[n] && !cnt_cut[n]) continue;
    printf("depth %2d nodes %12lld cert %12lld lp %10lld cut %10lld front %lld\n", n, cnt_nodes[n], cnt_cert[n], cnt_lp[n], cnt_cut[n], cnt_front[n]); tot += cnt_nodes[n]; fr += cnt_front[n]; }
  printf("# total %lld lptry %lld maxstates %d maxpairs %d violations %lld\n", tot, lptry, maxst, maxpairs, cex);
  printf("RESULT %s D=%d\n", cex ? "VIOLATION" : fr ? "FRONTIER" : "CLEAN", D);
  return 0;
}
