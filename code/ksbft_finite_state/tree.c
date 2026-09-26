/* tree.c (mg-e8b4) -- the finite-state route for the 1/3-2/3 conjecture at
 * bounded range D.  See docs/KSBFT-I-finite-state.md for every lemma used.
 *
 * WHAT IT DECIDES.  It searches every ordinal-indecomposable poset of range
 * pi(P) <= D, built bottom-up along its canonical linear extension e
 * (non-decreasing down-degree, ties broken by down-set bitmask; Lemma 2 of
 * the doc).  A node is the bottom N elements of such a poset (a down-set of
 * every completion).  A node is CLOSED when
 *   (cert) some incomparable pair (a,b) is CERTIFIED: for every down-set J of
 *          size k = N-D, P_J[a<b] (read as 1 if only a is in J, 0 if only b
 *          is in J) lies in [lo,hi].  By Lemma 3 (convexity) P_P[a<b] is then
 *          in [lo,hi] for EVERY poset of range <= D whose bottom is this node.
 *   (cut)  a permanently closed ordinal cut appears (then no completion is
 *          ordinal-indecomposable; a minimal counterexample is).
 * Every node is also checked as a COMPLETE poset (the poset may end here):
 * its exact delta is computed; if no pair is in [lo,hi] it is printed as a
 * counterexample to the threshold (with lo=1/3 that would refute the
 * conjecture; with lo=0.39 it is the firing control).
 * If the search terminates below MAXDEPTH, the statement "every range-<=D
 * poset has a pair with P in [lo,hi]" is PROVEN by this computation.
 *
 * usage: tree D MAXDEPTH [lo_num lo_den] [mode]
 *   mode "run"   (default) the search, with per-depth statistics
 *   mode "dump"  print every node's complete poset (for the generation control)
 *   mode "check" additionally verify at every certified node that the node's
 *                own complete poset has the certified pair inside [lo,hi]
 *   mode "split:I/M" only explore root-level subtrees congruent I mod M at depth SPLITDEPTH
 * Exact integer arithmetic (unsigned __int128); aborts on overflow risk. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef unsigned __int128 u128;
typedef uint64_t u64;
#define MAXN 60
#define MAXP 512

static int D, MAXDEPTH, MODE_DUMP = 0, MODE_CHECK = 0, MODE_NOCERT = 0, MODE_BADCERT = 0, USE_DCUT = 1, USE_EARLYCUT = 1, NRAND = 4;
static u64 rng = 88172645463325252ULL;
static u64 xr(void){ rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17; return rng; }
static u64 LON = 1, LOD = 3;        /* lo = LON/LOD, hi = 1 - lo */
static u64 down_[MAXN], succ_[MAXN];
static int pic[MAXN];
static int splitI = 0, splitM = 1, splitDepth = 0;
static long long split_counter = 0;

typedef struct { int a, b; } Pair;
typedef struct {
  int n, np, cap, k;   /* k = the cut (size of every state) */
  u64 *mask; u128 *e; u128 *c;   /* c[s*np + p] */
  Pair *pairs;
} Layer;

/* stats */
static long long nodes[MAXN + 2], certd[MAXN + 2], cutp[MAXN + 2], frontier[MAXN + 2], cexs = 0, checked = 0;
static int maxlayer = 0, maxpairs = 0;
static u128 LIMIT;

/* The certifying cut for a node with N elements (Lemma 2/3 of the doc):
 * every down-set of size k of every completion lies inside the known N
 * elements when k <= N-D (window, F1) or k <= d(e_{N-1}) (canonical order:
 * every later element has down-degree >= d(e_{N-1}), so lies in no down-set
 * of size <= d(e_{N-1})). */
static int cut_of(int N) {
  if (N <= 0) return 0;
  int k = N - D, d = __builtin_popcountll(down_[N - 1]);
  if (USE_DCUT && d > k) k = d;
  return k < 0 ? 0 : k;
}

/* in [lo,hi]:  c/e >= lo  and c/e <= 1-lo  */
static int in_range(u128 c, u128 e) { return c * LOD >= e * LON && c * LOD <= e * (LOD - LON); }
static int below(u128 c, u128 e) { return c * LOD < e * LON; }

/* ---------- hash for building a layer ---------- */
static int hcap = 0; static int *htab = NULL;
static void hreset(int need) {
  int c = 16; while (c < 2 * need) c <<= 1;
  if (c > hcap) { free(htab); htab = malloc(sizeof(int) * c); hcap = c; }
  for (int i = 0; i < hcap; i++) htab[i] = -1;
}
static inline u64 hmix(u64 x) { x ^= x >> 33; x *= 0xff51afd7ed558ccdULL; x ^= x >> 33; return x; }

static void lay_init(Layer *L, int cap, int np) {
  L->cap = cap; L->n = 0; L->np = np;
  L->mask = malloc(sizeof(u64) * cap); L->e = malloc(sizeof(u128) * cap);
  L->c = calloc((size_t)cap * (np ? np : 1), sizeof(u128));
  L->pairs = malloc(sizeof(Pair) * (np ? np : 1));
}
static void lay_free(Layer *L) { free(L->mask); free(L->e); free(L->c); free(L->pairs); }

/* forward one cut: from layer P (cut k) to new layer Q (cut k+1), elements
 * 0..nel-1 available, tracking pair list pl[0..np) where pidx[p] is the index
 * of that pair in P (or -1: pair's later element absent from every P-state). */
static void step(const Layer *P, Layer *Q, int nel, const Pair *pl, int np, const int *pidx) {
  int cap = P->n * (D + 2) + 16;
  lay_init(Q, cap, np); Q->k = P->k + 1;
  memcpy(Q->pairs, pl, sizeof(Pair) * np);
  hreset(cap);
  for (int s = 0; s < P->n; s++) {
    u64 I = P->mask[s]; u128 eI = P->e[s];
    for (int z = 0; z < nel; z++) {
      if ((I >> z) & 1) continue;
      if ((down_[z] & ~I) != 0) continue;
      u64 J = I | (1ULL << z);
      u64 h = hmix(J) & (hcap - 1); int t;
      while ((t = htab[h]) >= 0 && Q->mask[t] != J) h = (h + 1) & (hcap - 1);
      if (t < 0) {
        if (Q->n == Q->cap) { fprintf(stderr, "layer overflow\n"); exit(2); }
        t = Q->n++; htab[h] = t; Q->mask[t] = J; Q->e[t] = 0;
      }
      Q->e[t] += eI;
      if (Q->e[t] > LIMIT) { fprintf(stderr, "count overflow risk at nel=%d\n", nel); exit(2); }
      u128 *cq = Q->c + (size_t)t * np; const u128 *cp = P->c + (size_t)s * P->np;
      for (int p = 0; p < np; p++) {
        int a = pl[p].a, b = pl[p].b;
        int ain = (I >> a) & 1, bin = (I >> b) & 1;
        if (ain && bin) cq[p] += cp[pidx[p]];
        else if (z == b && ain) cq[p] += eI;
      }
    }
  }
  if (Q->n > maxlayer) maxlayer = Q->n;
}

/* classify pair p on layer L: 2 = certified, 0 = hopeless, 1 = live */
static int classify(const Layer *L, int p) {
  int undet = 0, lt = 0, gt = 0, in = 0;
  int a = L->pairs[p].a, b = L->pairs[p].b;
  for (int s = 0; s < L->n; s++) {
    u64 J = L->mask[s]; int ain = (J >> a) & 1, bin = (J >> b) & 1;
    if (ain && bin) {
      u128 c = L->c[(size_t)s * L->np + p], e = L->e[s];
      if (in_range(c, e)) in = 1; else if (below(c, e)) lt = 1; else gt = 1;
    } else if (ain) gt = 1;       /* a surely before b: r = 1 */
    else if (bin) lt = 1;         /* b surely before a: r = 0 */
    else undet = 1;
    if (undet && (lt || gt)) break;
    if (MODE_BADCERT && (ain && bin)) { undet = 0; break; }   /* CONTROL ONLY: look at one state */
  }
  if (!undet && !lt && !gt) return 2;
  if (!undet && !in && !(lt && gt)) return 0;
  return 1;
}

static void print_poset(int N) {
  printf("[");
  for (int i = 0; i < N; i++) printf("%s%llu", i ? "," : "", (unsigned long long)down_[i]);
  printf("]");
}

/* complete check: poset of N elements ends here.  Returns 1 if a pair in
 * [lo,hi] exists among pl (all non-hopeless pairs), writes exact values. */
static int complete_balanced(const Layer *top, int N, int want_pair, int *which) {
  Layer cur = *top; int own = 0;
  int np = top->np; int *pidx = malloc(sizeof(int) * (np ? np : 1));
  for (int p = 0; p < np; p++) pidx[p] = p;
  for (int cut = top->k; cut < N; cut++) {
    Layer nx; step(&cur, &nx, N, top->pairs, np, pidx);
    if (own) lay_free(&cur);
    cur = nx; own = 1;
  }
  free(pidx);
  /* cur has single state = full */
  int ok = 0;
  if (cur.n != 1) { fprintf(stderr, "complete: %d states at full\n", cur.n); exit(2); }
  for (int p = 0; p < np; p++) {
    if (want_pair >= 0 && p != want_pair) continue;
    if (in_range(cur.c[p], cur.e[0])) { ok = 1; if (which) *which = p; break; }
  }
  if (own) lay_free(&cur);
  return ok;
}

static int decomposable_complete(int N) {
  for (int c = 1; c < N; c++) {
    u64 low = (1ULL << c) - 1; int closed = 1;
    for (int i = c; i < N && closed; i++) if ((down_[i] & low) != low) closed = 0;
    if (closed) return 1;
  }
  return 0;
}

static void visit(int N, Layer *top);

/* enumerate up-sets U inside window [lo, N) with |U| <= umax, recursing from
 * position N-1 downward.  inc = current U (bitmask). */
static Layer *curtop;
static void enum_U(int N, int pos, u64 U, int sz, int umax, int wlo) {
  if (pos < wlo) {
    u64 full = (N == 64) ? ~0ULL : ((1ULL << N) - 1);
    u64 Dn = full & ~U;
    int d = N - sz;
    if (N > 0) {
      int dprev = __builtin_popcountll(down_[N - 1]);
      if (d < dprev) return;
      if (d == dprev && Dn < down_[N - 1]) return;
    }
    /* Dn must be down-closed: guaranteed since U is up-closed */
    if (splitM > 1 && N == splitDepth) { long long t = split_counter++; if (t % splitM != splitI) return; }
    /* install element N */
    down_[N] = Dn; succ_[N] = 0;
    for (int j = 0; j < N; j++) if ((Dn >> j) & 1) succ_[j] |= 1ULL << N; else pic[j]++;
    pic[N] = sz;
    /* child's pair list: live pairs of the parent top + new (a, N) for a in U */
    Layer *P = curtop;
    int npar = P->np, nnew = sz;
    Pair *pl = malloc(sizeof(Pair) * (npar + nnew + 1)); int *pidx = malloc(sizeof(int) * (npar + nnew + 1));
    int np = 0;
    for (int p = 0; p < npar; p++) { pl[np] = P->pairs[p]; pidx[np] = p; np++; }
    for (int j = 0; j < N; j++) if ((U >> j) & 1) { pl[np].a = j; pl[np].b = N; pidx[np] = -1; np++; }
    if (np > maxpairs) maxpairs = np;
    int kc = P->k;          /* parent's cut */
    int kn = cut_of(N + 1); /* child's cut (element N installed) */
    Layer child;
    if (kn == kc) {
      lay_init(&child, P->n, np); child.n = P->n; child.k = kc;
      memcpy(child.pairs, pl, sizeof(Pair) * np);
      for (int s = 0; s < P->n; s++) { child.mask[s] = P->mask[s]; child.e[s] = P->e[s];
        for (int p = 0; p < np; p++) child.c[(size_t)s * np + p] = pidx[p] >= 0 ? P->c[(size_t)s * P->np + pidx[p]] : 0; }
    } else {
      step(P, &child, N + 1, pl, np, pidx);
      for (int p = 0; p < np; p++) pidx[p] = p;
      while (child.k < kn) { Layer nx; step(&child, &nx, N + 1, pl, np, pidx); lay_free(&child); child = nx; }
    }
    free(pl); free(pidx);
    /* permanently-final ordinal cut check: cut c final when N+1 >= c + 2D - 1 */
    int Nc = N + 1, c = Nc - 2 * D + 1, pruned = 0;
    /* Lemma 2(c): in canonical order, an element whose down-set is ALL earlier
     * elements (U empty) makes the cut before it ordinal for every completion. */
    if (sz == 0 && N >= 1 && USE_EARLYCUT) { pruned = 1; cutp[Nc]++; }
    if (!pruned && c >= 1) {
      u64 low = (1ULL << c) - 1; int closed = 1;
      for (int i = c; i < Nc && closed; i++) if ((down_[i] & low) != low) closed = 0;
      if (closed) { pruned = 1; cutp[Nc]++; if (getenv("SHOWCUT")) { printf("CUT c=%d ", c); print_poset(Nc); printf("\n"); } }
    }
    Layer *saved = curtop;
    if (!pruned) visit(Nc, &child);
    curtop = saved;
    lay_free(&child);
    /* uninstall */
    for (int j = 0; j < N; j++) if ((Dn >> j) & 1) succ_[j] &= ~(1ULL << N); else pic[j]--;
    return;
  }
  /* option: pos not in U */
  enum_U(N, pos - 1, U, sz, umax, wlo);
  /* option: pos in U -- needs all successors of pos in U, room, pic < D */
  if (sz < umax && pic[pos] < D && (succ_[pos] & ~U) == 0)
    enum_U(N, pos - 1, U | (1ULL << pos), sz + 1, umax, wlo);
}

/* check mode: random continuations of a certified node.  Appends L random
 * elements (random up-set U of the window, |U| <= D, respecting pic < D --
 * NOT the canonical order: Lemma 3 needs only range <= D), then completes and
 * tests the certified pair on that completion.  Returns 1 if all in range. */
static void layer_restrict(const Layer *top, const int *idx, int m, Layer *out) {
  lay_init(out, top->n ? top->n : 1, m); out->n = top->n; out->k = top->k;
  for (int q = 0; q < m; q++) out->pairs[q] = top->pairs[idx[q]];
  for (int s = 0; s < top->n; s++) { out->mask[s] = top->mask[s]; out->e[s] = top->e[s];
    for (int q = 0; q < m; q++) out->c[(size_t)s * m + q] = top->c[(size_t)s * top->np + idx[q]]; }
}

static int rand_check(int N, const Layer *sub) {
  int L = (int)(xr() % (2 * D + 2));
  if (N + L > MAXN - 1) L = MAXN - 1 - N;
  Layer cur;
  { int idx[MAXP]; for (int q = 0; q < sub->np; q++) idx[q] = q; layer_restrict(sub, idx, sub->np, &cur); }
  int n = N;
  for (int t = 0; t < L; t++) {
    /* random up-set U, retried until the continuation stays in canonical
     * (d-sorted, tie-broken) order -- certification is claimed only for
     * canonical representations, which every poset has (Lemma 2). */
    u64 U = 0; int sz = 0, ok = 0, lo = n - 2 * D + 1; if (lo < 0) lo = 0;
    for (int tries = 0; tries < 64 && !ok; tries++) {
      U = 0; sz = 0;
      for (int pos = n - 1; pos >= lo; pos--)
        if (sz < D && pic[pos] < D && (succ_[pos] & ~U) == 0 && (xr() & 1)) { U |= 1ULL << pos; sz++; }
      u64 Dn = ((1ULL << n) - 1) & ~U; int dp = __builtin_popcountll(down_[n - 1]);
      ok = (n - sz > dp) || (n - sz == dp && Dn >= down_[n - 1]);
    }
    if (!ok) { U = 0; sz = 0; }   /* the element above everything: always canonical */
    u64 Dn = ((1ULL << n) - 1) & ~U;
    down_[n] = Dn; succ_[n] = 0;
    for (int j = 0; j < n; j++) if ((Dn >> j) & 1) succ_[j] |= 1ULL << n; else pic[j]++;
    pic[n] = sz;
    n++;
  }
  int ok = complete_balanced(&cur, n, -1, NULL);
  lay_free(&cur);
  for (int t = L - 1; t >= 0; t--) { n--; u64 Dn = down_[n];
    for (int j = 0; j < n; j++) if ((Dn >> j) & 1) succ_[j] &= ~(1ULL << n); else pic[j]--; }
  return ok;
}

/* ---------- joint certificate (Lemma 4 of the doc) ----------
 * All pairs share ONE unknown weight vector w_J = P[I_k = J] > 0.  A pair p
 * whose hull can only leave [lo,hi] on one side ("<lo" or ">hi") must, in a
 * counterexample, satisfy sum_J w_J a_pJ < 0 with
 *   "<lo":  a_pJ = r_pJ - lo,   ">hi":  a_pJ = hi - r_pJ,
 * where an undetermined state (neither a nor b in J) takes the value most
 * favourable to the constraint (r = 0 resp. 1, so a_pJ = -lo).  If integers
 * lambda_p >= 0, not all 0, satisfy sum_p lambda_p a_pJ >= 0 for EVERY state
 * J, the constraints are jointly infeasible for every w >= 0 (Gordan), so
 * some pair with lambda_p > 0 is in [lo,hi] in every completion.  lambda is
 * found by a floating simplex and then VERIFIED in exact integers; only the
 * exact verification is trusted. */
typedef __int128 i128;
static long long lpcert[MAXN + 2], lptried = 0;
static int MODE_BADLP = 0, USE_LP = 1;
#define LPMAXR 4200
#define LPMAXM 96
static double *TB = NULL; static int TBcap = 0;

/* maximize t s.t. t - sum_p a[J][p] lam_p <= 0 (J<S), sum lam <= 1; vars lam(m), t >= 0.
 * returns t*, fills lam. dense tableau, Bland's rule. */
static double lp_solve(int S, int m, const double *a, double *lam) {
  int R = S + 1, C = m + 1 + R + 1;          /* vars: lam 0..m-1, t m, slacks m+1..m+R, rhs last */
  size_t need = (size_t)(R + 1) * C;
  if ((int)need > TBcap) { free(TB); TB = malloc(sizeof(double) * need); TBcap = (int)need; }
  double *T = TB; memset(T, 0, sizeof(double) * need);
  int *basis = malloc(sizeof(int) * R);
  for (int J = 0; J < S; J++) { double *row = T + (size_t)J * C;
    for (int p = 0; p < m; p++) row[p] = -a[(size_t)J * m + p];
    row[m] = 1; row[m + 1 + J] = 1; row[C - 1] = 0; basis[J] = m + 1 + J; }
  { double *row = T + (size_t)S * C; for (int p = 0; p < m; p++) row[p] = 1; row[m + 1 + S] = 1; row[C - 1] = 1; basis[S] = m + 1 + S; }
  double *obj = T + (size_t)R * C; obj[m] = -1;       /* z - t = 0 */
  for (int it = 0; it < 5000; it++) {
    int pc = -1; for (int j = 0; j < C - 1; j++) if (obj[j] < -1e-12) { pc = j; break; }   /* Bland */
    if (pc < 0) break;
    int pr = -1; double best = 0;
    for (int i = 0; i < R; i++) { double v = T[(size_t)i * C + pc]; if (v > 1e-12) { double q = T[(size_t)i * C + C - 1] / v;
      if (pr < 0 || q < best - 1e-15 || (q < best + 1e-15 && basis[i] < basis[pr])) { pr = i; best = q; } } }
    if (pr < 0) break;   /* unbounded: cannot happen (t <= max|a|) */
    double pv = T[(size_t)pr * C + pc]; for (int j = 0; j < C; j++) T[(size_t)pr * C + j] /= pv;
    for (int i = 0; i <= R; i++) if (i != pr) { double f = T[(size_t)i * C + pc]; if (f != 0) {
      double *ri = T + (size_t)i * C, *rp = T + (size_t)pr * C; for (int j = 0; j < C; j++) ri[j] -= f * rp[j]; } }
    basis[pr] = pc;
  }
  for (int p = 0; p < m; p++) lam[p] = 0;
  double t = 0;
  for (int i = 0; i < R; i++) { if (basis[i] < m) lam[basis[i]] = T[(size_t)i * C + C - 1]; else if (basis[i] == m) t = T[(size_t)i * C + C - 1]; }
  free(basis);
  return t;
}

/* returns number of pairs in the verified certificate (0 = none); idx gets them */
static int lp_certify(const Layer *L, const int *cls, int *idx) {
  int S = L->n, np = L->np, m = 0; int pid[LPMAXM], sgn[LPMAXM];
  if (S > LPMAXR) return 0;
  for (int s = 0; s < S; s++) if (L->e[s] >> 85) return 0;
  for (int p = 0; p < np && m < LPMAXM; p++) if (cls[p] == 1) {
    int a = L->pairs[p].a, b = L->pairs[p].b, canlt = 0, cangt = 0;
    for (int s = 0; s < S; s++) { u64 J = L->mask[s]; int ai = (J >> a) & 1, bi = (J >> b) & 1;
      if (ai && bi) { u128 c = L->c[(size_t)s * np + p], e = L->e[s]; if (below(c, e)) canlt = 1; else if (!in_range(c, e)) cangt = 1; }
      else if (ai) cangt = 1; else if (bi) canlt = 1; else { canlt = cangt = 1; } }
    if (canlt && !cangt) { pid[m] = p; sgn[m] = -1; m++; }
    else if (cangt && !canlt) { pid[m] = p; sgn[m] = +1; m++; }
  }
  if (m < 2) return 0;
  lptried++;
  /* exact integer coefficients A[J][q] = LOD*e_J * a_qJ */
  i128 *A = malloc(sizeof(i128) * (size_t)S * m); double *af = malloc(sizeof(double) * (size_t)S * m);
  for (int s = 0; s < S; s++) { u64 J = L->mask[s]; i128 e = (i128)L->e[s];
    for (int q = 0; q < m; q++) { int p = pid[q], a = L->pairs[p].a, b = L->pairs[p].b; int ai = (J >> a) & 1, bi = (J >> b) & 1;
      i128 c; int und = 0;
      if (ai && bi) c = (i128)L->c[(size_t)s * np + p]; else if (ai) c = e; else if (bi) c = 0; else { und = 1; c = 0; }
      i128 v;
      if (und) v = -(i128)LON * e;
      else if (sgn[q] < 0) v = (i128)LOD * c - (i128)LON * e;          /* r - lo */
      else v = (i128)(LOD - LON) * e - (i128)LOD * c;                   /* hi - r */
      A[(size_t)s * m + q] = v; af[(size_t)s * m + q] = (double)v / ((double)LOD * (double)e); } }
  double lam[LPMAXM]; double t = lp_solve(S, m, af, lam);
  int ok = 0, k = 0;
  if (MODE_BADLP) { ok = t > -0.02; for (int q = 0; q < m; q++) if (lam[q] > 1e-12 || ok) idx[k++] = pid[q]; if (!ok) k = 0; }
  else if (t > 1e-12) {
    long long li[LPMAXM]; long long tot = 0;
    for (int q = 0; q < m; q++) { li[q] = (long long)(lam[q] * 1073741824.0); if (li[q] < 0) li[q] = 0; tot += li[q]; }
    if (tot > 0) {
      ok = 1;
      for (int s = 0; s < S && ok; s++) { i128 sum = 0; for (int q = 0; q < m; q++) sum += (i128)li[q] * A[(size_t)s * m + q]; if (sum < 0) ok = 0; }
      if (ok) for (int q = 0; q < m; q++) if (li[q] > 0) idx[k++] = pid[q];
    }
  }
  free(A); free(af);
  return ok ? k : 0;
}

static long long visits = 0; static int deepest = 0;
static void visit(int N, Layer *top) {
  nodes[N]++;
  if (N > deepest) deepest = N;
  if ((++visits & ((1LL << 24) - 1)) == 0) { fprintf(stderr, "progress %lld nodes, deepest %d\n", visits, deepest); }
  /* classify pairs on the top layer (cut N-D) */
  int np = top->np; int *cls = malloc(sizeof(int) * (np ? np : 1)); int cert = -1;
  for (int p = 0; p < np; p++) { cls[p] = classify(top, p); if (MODE_NOCERT && cls[p] != 1) cls[p] = 1; if (cls[p] == 2 && cert < 0) cert = p; }
  if (cert >= 0) {
    certd[N]++;
    if (MODE_CHECK) {
      checked++;
      if (!complete_balanced(top, N, cert, NULL)) { printf("CHECK FAILED: certified pair not in range in own completion N=%d ", N); print_poset(N); printf("\n"); exit(3); }
      Layer one; layer_restrict(top, &cert, 1, &one);
      for (int r = 0; r < NRAND; r++) if (!rand_check(N, &one)) { printf("CHECK FAILED: random continuation of certified node N=%d ", N); print_poset(N); printf("\n"); exit(3); }
      lay_free(&one);
    }
    free(cls); return;
  }
  if (USE_LP && !MODE_NOCERT) {
    int idx[LPMAXM]; int k = lp_certify(top, cls, idx);
    if (k > 0) {
      lpcert[N]++;
      if (MODE_CHECK) {
        checked++;
        Layer sub; layer_restrict(top, idx, k, &sub);
        if (!complete_balanced(&sub, N, -1, NULL)) { printf("CHECK FAILED: LP-certified set not in range in own completion N=%d ", N); print_poset(N); printf("\n"); exit(3); }
        for (int r = 0; r < NRAND; r++) if (!rand_check(N, &sub)) { printf("CHECK FAILED: random continuation of LP-certified node N=%d ", N); print_poset(N); printf("\n"); exit(3); }
        lay_free(&sub);
      }
      free(cls); return;
    }
  }
  if (getenv("SHOWDEEP") && N >= atoi(getenv("SHOWDEEP"))) {
    printf("DEEP N=%d k=%d states=%d ", N, top->k, top->n); print_poset(N); printf("\n");
    for (int p = 0; p < np; p++) if (cls[p] == 1) {
      double mn = 9, mx = -9; int und = 0; int a = top->pairs[p].a, b = top->pairs[p].b;
      for (int s2 = 0; s2 < top->n; s2++) { u64 J = top->mask[s2]; int ai = (J >> a) & 1, bi = (J >> b) & 1; double r;
        if (ai && bi) r = (double)top->c[(size_t)s2 * np + p] / (double)top->e[s2]; else if (ai) r = 1; else if (bi) r = 0; else { und = 1; continue; }
        if (r < mn) mn = r; if (r > mx) mx = r; }
      printf("   live (%d,%d) hull [%.4f, %.4f]%s\n", a, b, mn, mx, und ? " +undet" : "");
    }
  }
  /* keep only live pairs */
  Layer live; int nl = 0;
  for (int p = 0; p < np; p++) if (cls[p] == 1) nl++;
  lay_init(&live, top->n ? top->n : 1, nl); live.n = top->n; live.k = top->k;
  { int q = 0; for (int p = 0; p < np; p++) if (cls[p] == 1) live.pairs[q++] = top->pairs[p]; }
  for (int s = 0; s < top->n; s++) {
    live.mask[s] = top->mask[s]; live.e[s] = top->e[s];
    int q = 0; for (int p = 0; p < np; p++) if (cls[p] == 1) live.c[(size_t)s * nl + q++] = top->c[(size_t)s * np + p];
  }
  free(cls);
  /* the poset may end here */
  if (N >= 2 && !decomposable_complete(N)) {
    if (MODE_DUMP) { printf("P "); print_poset(N); printf("\n"); }
    if (!complete_balanced(&live, N, -1, NULL)) {
      cexs++;
      printf("COUNTEREXAMPLE-TO-THRESHOLD N=%d ", N); print_poset(N); printf("\n");
      fflush(stdout);
    }
  }
  if (N >= MAXDEPTH) { frontier[N]++; lay_free(&live); return; }
  curtop = &live;
  int wlo = N - 2 * D + 1; if (wlo < 0) wlo = 0;
  enum_U(N, N - 1, 0, 0, D, wlo);
  lay_free(&live);
}

int main(int argc, char **argv) {
  if (argc < 3) { fprintf(stderr, "usage: tree D MAXDEPTH [lo_num lo_den] [run|dump|check|split:I/M@depth]\n"); return 1; }
  D = atoi(argv[1]); MAXDEPTH = atoi(argv[2]);
  if (argc >= 5) { LON = strtoull(argv[3], 0, 10); LOD = strtoull(argv[4], 0, 10); }
  for (int i = 5; i < argc; i++) {
    if (!strcmp(argv[i], "dump")) MODE_DUMP = 1;
    else if (!strcmp(argv[i], "check")) MODE_CHECK = 1;
    else if (!strcmp(argv[i], "nocert")) MODE_NOCERT = 1;
    else if (!strcmp(argv[i], "badcert")) MODE_BADCERT = 1;
    else if (!strcmp(argv[i], "nodcut")) USE_DCUT = 0;
    else if (!strcmp(argv[i], "nolp")) USE_LP = 0;
    else if (!strcmp(argv[i], "badlp")) MODE_BADLP = 1;
    else if (!strcmp(argv[i], "noearlycut")) USE_EARLYCUT = 0;
    else if (!strncmp(argv[i], "split:", 6)) sscanf(argv[i] + 6, "%d/%d@%d", &splitI, &splitM, &splitDepth);
  }
  if (MAXDEPTH > MAXN - 1) MAXDEPTH = MAXN - 1;
  LIMIT = ((u128)1) << 120; LIMIT /= (LOD + 1);
  Layer root; lay_init(&root, 1, 0); root.n = 1; root.k = 0; root.mask[0] = 0; root.e[0] = 1;
  visit(0, &root);
  long long tot = 0, tf = 0;
  printf("# D=%d MAXDEPTH=%d threshold=[%llu/%llu, 1-%llu/%llu] %s%s\n", D, MAXDEPTH,
         (unsigned long long)LON, (unsigned long long)LOD, (unsigned long long)LON, (unsigned long long)LOD,
         MODE_CHECK ? "check " : "", splitM > 1 ? "split" : "");
  if (splitM > 1) printf("# split %d/%d at depth %d\n", splitI, splitM, splitDepth);
  printf("# depth nodes certified cutpruned frontier\n");
  for (int n = 0; n <= MAXDEPTH + 1; n++) {
    if (!nodes[n] && !cutp[n]) continue;
    printf("depth %2d  nodes %12lld  certified %12lld  lpcert %10lld  cutpruned %10lld  frontier %lld\n", n, nodes[n], certd[n], lpcert[n], cutp[n], frontier[n]);
    tot += nodes[n]; tf += frontier[n];
  }
  printf("# LP attempts %lld%s\n", lptried, USE_LP ? "" : " (LP disabled)");
  printf("# total nodes %lld, max layer %d states, max tracked pairs %d\n", tot, maxlayer, maxpairs);
  if (MODE_CHECK) printf("# check mode: %lld certified nodes re-verified on their own completion\n", checked);
  printf("# counterexamples-to-threshold found: %lld\n", cexs);
  printf("RESULT %s D=%d\n", (tf == 0 && cexs == 0) ? "TERMINATED-CLEAN" : (cexs ? "FOUND-VIOLATION" : "FRONTIER-NONEMPTY"), D);
  return 0;
}
