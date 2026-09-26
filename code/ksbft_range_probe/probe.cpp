// probe.cpp -- KSBFT-A range probe (mg-2912).
//
// Enumerates finite posets up to isomorphism (optionally only those of range
// pi(P) <= DMAX), and for every poset whose incomparability graph G(P) is
// connected (and n >= 2) computes EXACTLY, in integer arithmetic:
//   e(P), pi(P), width, delta(P) and an attaining pair, the heights
//   h(x) = E[f(x)] (as integer numerators over e), the displacements
//   d_i = h(v_i) - i, M = max|d_i|, and the Lemma 4.1 triples of KSBFT_v7.
//
// Generation: every poset on n elements arises from one on n-1 elements by
// adding a new MAXIMAL element whose strict down-set is an order ideal.
// Removing a maximal element cannot raise the range, so restricting every
// level to pi <= DMAX is complete (README, "Completeness").  Duplicates are
// removed by a canonical form (individualisation-refinement, exhaustive,
// twin-pruned).  The level counts are checked against OEIS A000112.
//
// Modes:
//   probe enum NMAX DMAX OUTPREFIX   -- enumerate + analyse, write
//                                       OUTPREFIX_n<k>.jsonl extremes and a
//                                       summary on stdout
//   probe one                         -- read posets "n m_0 ... m_{n-1}" (m_i =
//                                       bitmask of elements strictly below i)
//                                       from stdin, print one JSON line each
//                                       (used by the independent Python check)
//
// Everything is exact except the ranking keys of the top-K lists (long
// double); every reported extremum is re-derived exactly by check.py.

#include <algorithm>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <functional>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

typedef uint32_t mask;
typedef __int128 i128;
static const int MAXN = 24;

struct Poset {
  int n;
  mask down[MAXN];  // strict down-sets (transitively closed)
  mask up[MAXN];
};

static void fill_up(Poset &P) {
  for (int i = 0; i < P.n; i++) P.up[i] = 0;
  for (int i = 0; i < P.n; i++)
    for (int j = 0; j < P.n; j++)
      if (P.down[i] >> j & 1) P.up[j] |= (mask)1 << i;
}

// ---------------------------------------------------------------- canonical
struct Canon {
  const Poset *P;
  int n;
  std::string best;
  bool have;

  // refine colouring c (values 0..k-1) to an equitable one; returns #colours
  int refine(std::vector<int> &c) {
    int k = 0;
    for (int v = 0; v < n; v++) k = std::max(k, c[v] + 1);
    while (true) {
      // signature: (c[v], counts of colours in down, counts in up)
      std::vector<std::vector<int>> sig(n);
      for (int v = 0; v < n; v++) {
        std::vector<int> s(2 * k + 1, 0);
        s[0] = c[v];
        for (int u = 0; u < n; u++) {
          if (P->down[v] >> u & 1) s[1 + c[u]]++;
          if (P->up[v] >> u & 1) s[1 + k + c[u]]++;
        }
        sig[v] = s;
      }
      std::vector<int> ord(n);
      for (int v = 0; v < n; v++) ord[v] = v;
      std::sort(ord.begin(), ord.end(),
                [&](int a, int b) { return sig[a] < sig[b]; });
      std::vector<int> nc(n);
      int id = 0;
      for (int i = 0; i < n; i++) {
        if (i > 0 && sig[ord[i]] != sig[ord[i - 1]]) id++;
        nc[ord[i]] = id;
      }
      int nk = id + 1;
      c = nc;
      if (nk == k) return k;
      k = nk;
    }
  }

  std::string code_of(const std::vector<int> &c) {
    // c is discrete: position of v is c[v]
    int bpr = (n + 7) / 8;
    std::string s(n * bpr, '\0');
    std::vector<int> at(n);
    for (int v = 0; v < n; v++) at[c[v]] = v;
    for (int i = 0; i < n; i++) {
      int v = at[i];
      mask row = 0;
      for (int u = 0; u < n; u++)
        if (P->down[v] >> u & 1) row |= (mask)1 << c[u];
      for (int b = 0; b < bpr; b++) s[i * bpr + b] = (char)(row >> (8 * b) & 255);
    }
    return s;
  }

  void search(std::vector<int> c) {
    int k = refine(c);
    if (k == n) {
      std::string s = code_of(c);
      if (!have || s < best) { best = s; have = true; }
      return;
    }
    // first non-singleton colour class
    std::vector<int> cnt(k, 0);
    for (int v = 0; v < n; v++) cnt[c[v]]++;
    int cc = 0;
    while (cnt[cc] == 1) cc++;
    std::vector<int> tried;
    for (int v = 0; v < n; v++) {
      if (c[v] != cc) continue;
      bool twin = false;  // twins give isomorphic subtrees (README)
      for (int u : tried)
        if (P->down[u] == P->down[v] && P->up[u] == P->up[v]) { twin = true; break; }
      if (twin) continue;
      tried.push_back(v);
      std::vector<int> d(n);
      for (int u = 0; u < n; u++) {
        if (c[u] < cc) d[u] = c[u];
        else if (u == v) d[u] = cc;
        else if (c[u] == cc) d[u] = cc + 1;
        else d[u] = c[u] + 1;
      }
      search(d);
    }
  }

  std::string run(const Poset &Q) {
    P = &Q;
    n = Q.n;
    have = false;
    std::vector<int> c(n);
    // initial colour: (|down|, |up|) -- labelling invariant
    std::vector<std::pair<int, int>> key(n);
    for (int v = 0; v < n; v++)
      key[v] = {__builtin_popcount(Q.down[v]), __builtin_popcount(Q.up[v])};
    std::vector<std::pair<int, int>> ks = key;
    std::sort(ks.begin(), ks.end());
    ks.erase(std::unique(ks.begin(), ks.end()), ks.end());
    for (int v = 0; v < n; v++)
      c[v] = std::lower_bound(ks.begin(), ks.end(), key[v]) - ks.begin();
    search(c);
    return best;
  }
};

static Poset decode(const std::string &s, int n) {
  Poset P;
  P.n = n;
  int bpr = (n + 7) / 8;
  for (int i = 0; i < n; i++) {
    mask row = 0;
    for (int b = 0; b < bpr; b++) row |= (mask)(unsigned char)s[i * bpr + b] << (8 * b);
    P.down[i] = row;
  }
  fill_up(P);
  return P;
}

static int range_of(const Poset &P) {
  int r = 0;
  mask all = (P.n == 32) ? ~0u : (((mask)1 << P.n) - 1);
  for (int v = 0; v < P.n; v++) {
    mask comp = P.down[v] | P.up[v] | ((mask)1 << v);
    r = std::max(r, __builtin_popcount(all & ~comp));
  }
  return r;
}

static bool connected_incomp(const Poset &P) {
  int n = P.n;
  mask all = ((mask)1 << n) - 1;
  mask seen = 1, frontier = 1;
  while (frontier) {
    int v = __builtin_ctz(frontier);
    frontier &= frontier - 1;
    mask nb = all & ~(P.down[v] | P.up[v] | ((mask)1 << v));
    mask nw = nb & ~seen;
    seen |= nw;
    frontier |= nw;
  }
  return seen == all;
}

static int width_of(const Poset &P) {
  // Dilworth: width = n - maximum matching in the comparability bipartite graph
  int n = P.n;
  std::vector<int> matchR(n, -1);
  int m = 0;
  // simple recursive Kuhn
  struct K {
    const Poset *P; int n; std::vector<int> *mr; std::vector<char> vis;
    bool aug(int u) {
      for (int v = 0; v < n; v++)
        if ((P->up[u] >> v & 1) && !vis[v]) {
          vis[v] = 1;
          if ((*mr)[v] < 0 || aug((*mr)[v])) { (*mr)[v] = u; return true; }
        }
      return false;
    }
  } k{&P, n, &matchR, {}};
  for (int u = 0; u < n; u++) {
    k.vis.assign(n, 0);
    if (k.aug(u)) m++;
  }
  return n - m;
}

// ---------------------------------------------------------------- analysis
struct Result {
  int n, pi, width;
  i128 e;
  i128 dnum;          // delta(P) = dnum / e
  int dx, dy;         // attaining pair (first found, lexicographic)
  int ndpairs;        // number of attaining pairs
  std::vector<i128> S;             // h(x) = S[x] / e
  std::vector<std::vector<i128>> B;  // B[x][y] = #ext with x before y
  std::vector<int> ord;            // v_1..v_n (0-based) sorted by (S, index)
  i128 Mnum;                       // M = Mnum / e
  int Marg;                        // 1-based index i attaining |d_i| = M (first)
  // Lemma 4.1 triples: candidates k with d_k = M (k <= n-2) or d_{k+2} = -M
  int ntrip;
  i128 trip_min_num, trip_max_num;  // min / max over candidates of max(bal(x,y),bal(y,z))
  bool trip_all_bft;                // every candidate is a BFT triple (non-chain, span <= 2)
  // structured (Lemma 3.2 (ii),(iii),(v)) consecutive triples, Case D
  int nstruct;
  long double struct_c_min;  // min over structured consecutive triples of (a-C)/Mloc^2
  i128 struct_a, struct_mloc; int struct_k;
};

static long double CBFT() { return (5.0L - sqrtl(5.0L)) / 10.0L; }

static void analyse(const Poset &P, Result &R) {
  int n = P.n;
  R.n = n;
  R.pi = range_of(P);
  R.width = width_of(P);
  // ideals by BFS over sizes
  std::vector<mask> ideals;
  std::unordered_map<mask, int> idx;
  ideals.push_back(0);
  idx[0] = 0;
  for (size_t q = 0; q < ideals.size(); q++) {
    mask I = ideals[q];
    for (int x = 0; x < n; x++)
      if (!(I >> x & 1) && (P.down[x] & ~I) == 0) {
        mask J = I | ((mask)1 << x);
        if (!idx.count(J)) { idx[J] = ideals.size(); ideals.push_back(J); }
      }
  }
  // BFS by adding one element => ideals are in nondecreasing size order
  int Ni = ideals.size();
  std::vector<i128> fwd(Ni, 0), bwd(Ni, 0);
  fwd[0] = 1;
  for (int q = 0; q < Ni; q++) {
    mask I = ideals[q];
    for (int x = 0; x < n; x++)
      if (!(I >> x & 1) && (P.down[x] & ~I) == 0) fwd[idx[I | ((mask)1 << x)]] += fwd[q];
  }
  mask all = ((mask)1 << n) - 1;
  bwd[idx[all]] = 1;
  for (int q = Ni - 1; q >= 0; q--) {
    mask I = ideals[q];
    if (I == all) continue;
    i128 s = 0;
    for (int x = 0; x < n; x++)
      if (!(I >> x & 1) && (P.down[x] & ~I) == 0) s += bwd[idx[I | ((mask)1 << x)]];
    bwd[q] = s;
  }
  R.e = fwd[idx[all]];
  R.S.assign(n, 0);
  R.B.assign(n, std::vector<i128>(n, 0));
  for (int q = 0; q < Ni; q++) {
    mask I = ideals[q];
    int sz = __builtin_popcount(I);
    for (int y = 0; y < n; y++)
      if (!(I >> y & 1) && (P.down[y] & ~I) == 0) {
        i128 c = fwd[q] * bwd[idx[I | ((mask)1 << y)]];
        R.S[y] += (i128)(sz + 1) * c;
        for (int x = 0; x < n; x++)
          if (I >> x & 1) R.B[x][y] += c;
      }
  }
  // delta
  R.dnum = -1; R.dx = R.dy = -1; R.ndpairs = 0;
  for (int x = 0; x < n; x++)
    for (int y = x + 1; y < n; y++) {
      if ((P.down[x] >> y & 1) || (P.up[x] >> y & 1)) continue;
      i128 b = std::min(R.B[x][y], R.B[y][x]);
      if (b > R.dnum) { R.dnum = b; R.dx = x; R.dy = y; R.ndpairs = 1; }
      else if (b == R.dnum) R.ndpairs++;
    }
  // heights, displacement
  R.ord.resize(n);
  for (int i = 0; i < n; i++) R.ord[i] = i;
  std::sort(R.ord.begin(), R.ord.end(), [&](int a, int b) {
    if (R.S[a] != R.S[b]) return R.S[a] < R.S[b];
    return a < b;
  });
  std::vector<i128> d(n);
  R.Mnum = -1; R.Marg = -1;
  for (int i = 0; i < n; i++) {
    d[i] = R.S[R.ord[i]] - (i128)(i + 1) * R.e;
    i128 a = d[i] < 0 ? -d[i] : d[i];
    if (a > R.Mnum) { R.Mnum = a; R.Marg = i + 1; }
  }
  auto bal = [&](int x, int y) -> i128 {
    if ((P.down[x] >> y & 1) || (P.up[x] >> y & 1)) return 0;
    return std::min(R.B[x][y], R.B[y][x]);
  };
  // Lemma 4.1 candidates
  R.ntrip = 0; R.trip_min_num = -1; R.trip_max_num = -1; R.trip_all_bft = true;
  for (int k = 0; k + 2 < n; k++) {
    bool cand = (d[k] == R.Mnum) || (d[k + 2] == -R.Mnum);
    if (!cand) continue;
    int x = R.ord[k], y = R.ord[k + 1], z = R.ord[k + 2];
    i128 a = std::max(bal(x, y), bal(y, z));
    R.ntrip++;
    if (R.trip_min_num < 0 || a < R.trip_min_num) R.trip_min_num = a;
    if (a > R.trip_max_num) R.trip_max_num = a;
    bool chain = (P.down[y] >> x & 1) && (P.down[z] >> y & 1);
    bool span = (R.S[z] - R.S[x] <= 2 * R.e);
    if (chain || !span) R.trip_all_bft = false;
  }
  // structured consecutive triples (Lemma 3.2 (i)-(iii),(v)) with span <= 2
  R.nstruct = 0; R.struct_c_min = 1e30L; R.struct_k = -1;
  long double C = CBFT();
  for (int k = 0; k + 2 < n; k++) {
    int x = R.ord[k], y = R.ord[k + 1], z = R.ord[k + 2];
    if (!(P.down[z] >> x & 1)) continue;                     // x < z
    if (P.down[z] & P.up[x]) continue;                       // z covers x
    mask incy = all & ~(P.down[y] | P.up[y] | ((mask)1 << y));
    if (incy != (((mask)1 << x) | ((mask)1 << z))) continue;  // (iii)
    if (R.S[z] - R.S[x] > 2 * R.e) continue;                 // BFT span
    mask L = P.down[y], U = P.up[y];
    bool ok = ((L & ~P.down[z]) == 0) && ((U & ~P.up[x]) == 0);
    for (int w = 0; w < n && ok; w++)
      if (L >> w & 1)
        if ((U & ~P.up[w]) != 0) ok = false;
    if (!ok) continue;
    R.nstruct++;
    i128 a = std::max(bal(x, y), bal(y, z));
    i128 ml = std::max(d[k] < 0 ? -d[k] : d[k], d[k + 2] < 0 ? -d[k + 2] : d[k + 2]);
    long double eps = (long double)a / (long double)R.e - C;
    long double m = (long double)ml / (long double)R.e;
    long double c = m > 0 ? eps / (m * m) : 1e30L;
    if (c < R.struct_c_min) { R.struct_c_min = c; R.struct_a = a; R.struct_mloc = ml; R.struct_k = k + 1; }
  }
}

static std::string i2s(i128 v) {
  if (v == 0) return "0";
  bool neg = v < 0;
  unsigned __int128 u = neg ? -(unsigned __int128)v : (unsigned __int128)v;
  std::string s;
  while (u) { s += char('0' + (int)(u % 10)); u /= 10; }
  if (neg) s += '-';
  std::reverse(s.begin(), s.end());
  return s;
}

static std::string json(const Poset &P, const Result &R) {
  std::string s = "{\"n\":" + std::to_string(R.n) + ",\"pi\":" + std::to_string(R.pi) +
                  ",\"width\":" + std::to_string(R.width) + ",\"down\":[";
  for (int i = 0; i < P.n; i++) s += (i ? "," : "") + std::to_string(P.down[i]);
  s += "],\"e\":\"" + i2s(R.e) + "\",\"delta_num\":\"" + i2s(R.dnum) + "\",\"pair\":[" +
       std::to_string(R.dx) + "," + std::to_string(R.dy) + "],\"npairs\":" + std::to_string(R.ndpairs) +
       ",\"S\":[";
  for (int i = 0; i < P.n; i++) s += std::string(i ? "," : "") + "\"" + i2s(R.S[i]) + "\"";
  s += "],\"ord\":[";
  for (int i = 0; i < P.n; i++) s += (i ? "," : "") + std::to_string(R.ord[i]);
  s += "],\"M_num\":\"" + i2s(R.Mnum) + "\",\"M_at\":" + std::to_string(R.Marg) +
       ",\"ntrip\":" + std::to_string(R.ntrip) + ",\"trip_min_num\":\"" + i2s(R.trip_min_num) +
       "\",\"trip_max_num\":\"" + i2s(R.trip_max_num) + "\",\"trip_all_bft\":" +
       (R.trip_all_bft ? "true" : "false") + ",\"nstruct\":" + std::to_string(R.nstruct);
  if (R.nstruct) {
    char buf[64];
    snprintf(buf, sizeof buf, "%.9Lf", R.struct_c_min);
    s += ",\"struct_c\":" + std::string(buf) + ",\"struct_k\":" + std::to_string(R.struct_k) +
         ",\"struct_a\":\"" + i2s(R.struct_a) + "\",\"struct_mloc\":\"" + i2s(R.struct_mloc) + "\"";
  }
  s += "}";
  return s;
}

// top-K by a key, keeping ties at the cutoff up to a cap
struct TopK {
  int K, cap;
  std::vector<std::pair<long double, std::string>> v;
  TopK(int k = 12, int c = 60) : K(k), cap(c) {}
  void add(long double key, const std::function<std::string()> &mk) {
    if ((int)v.size() >= K) {
      // current cutoff
      if (key > cut + 1e-15L) return;
    }
    v.push_back({key, mk()});
    if ((int)v.size() > 4 * cap) prune();
    else if ((int)v.size() >= K) recut();
  }
  long double cut = 1e30L;
  void recut() {
    if ((int)v.size() < K) { cut = 1e30L; return; }
    std::vector<long double> ks;
    for (auto &p : v) ks.push_back(p.first);
    std::nth_element(ks.begin(), ks.begin() + (K - 1), ks.end());
    cut = ks[K - 1];
  }
  void prune() {
    std::sort(v.begin(), v.end(), [](auto &a, auto &b) { return a.first < b.first; });
    recut();
    size_t keep = 0;
    while (keep < v.size() && (keep < (size_t)K || v[keep].first <= cut + 1e-15L) && keep < (size_t)cap) keep++;
    v.resize(keep);
  }
};

struct Bucket {
  long long count = 0;
  i128 min_dn = -1, min_de = 1;   // min delta
  i128 min_Mn = -1, min_Me = 1;   // min M
  long double min_c = 1e30L;      // min (delta - C)/M^2
  long double min_trip_c = 1e30L; // min over Lemma 4.1 candidates of (a - C)/M^2
  long long n_viol441 = 0;        // delta < C + M^2/441 (float, verified later)
  long long n_trip_viol441 = 0;
  long long n_not_bft = 0;
  long long n_with_struct = 0;
  long double min_struct_c = 1e30L;
  long long n_delta_third = 0;    // delta == 1/3 exactly
  TopK td{12, 80}, tM{12, 80}, tc{8, 40}, ts{8, 40};
};

static std::string fmt(long double x) {
  if (x > 1e29L) return "NA";
  char buf[64];
  snprintf(buf, sizeof buf, "%.6Lf", x);
  return buf;
}


// ---------------------------------------------------------------- search
// Simulated annealing over naturally labelled posets on n elements whose
// generating relations i<j satisfy j-i <= band.  Objective: M or delta of a
// poset with connected G(P) and pi <= DMAX.  HEURISTIC: a witness found here
// is an exact upper bound on the infimum; failure to find one proves nothing.
static unsigned long long rng_state = 88172645463325252ULL;
static unsigned long long xr() { rng_state ^= rng_state << 13; rng_state ^= rng_state >> 7; rng_state ^= rng_state << 17; return rng_state; }
static double ur() { return (xr() >> 11) * (1.0 / 9007199254740992.0); }

static bool build(int n, const std::vector<mask> &g, Poset &P) {
  P.n = n;
  for (int j = 0; j < n; j++) {
    mask d = 0;
    for (int i = 0; i < j; i++)
      if (g[j] >> i & 1) d |= P.down[i] | ((mask)1 << i);
    P.down[j] = d;
  }
  fill_up(P);
  return true;
}

static int search_main(int argc, char **argv) {
  int NMIN = atoi(argv[2]), NMAX = atoi(argv[3]), DMAX = atoi(argv[4]);
  std::string obj = argv[5];
  rng_state ^= (unsigned long long)atoll(argv[6]) * 0x9E3779B97F4A7C15ULL;
  long long iters = atoll(argv[7]);
  int restarts = argc > 8 ? atoi(argv[8]) : 4;
  auto value = [&](const Poset &P, Result &R) -> long double {
    analyse(P, R);
    return obj == "M" ? (long double)R.Mnum / (long double)R.e : (long double)R.dnum / (long double)R.e;
  };
  for (int n = NMIN; n <= NMAX; n++) {
    long double best = 1e30L; std::string bestjson;
    int band = DMAX + 2;
    for (int rs = 0; rs < restarts; rs++) {
      std::vector<mask> g(n, 0);
      // start: Fibonacci poset (pi = 2), always admissible
      for (int j = 2; j < n; j++) g[j] = ((mask)1 << (j - 2)) | (j >= 3 ? ((mask)1 << (j - 3)) : 0);
      Poset P; build(n, g, P);
      if (!connected_incomp(P) || range_of(P) > DMAX || range_of(P) != 2) { fprintf(stderr, "bad start\n"); return 3; }
      Result R; long double cur = value(P, R);
      if (cur < best - 1e-15L) { best = cur; bestjson = json(P, R); }
      for (long long it = 0; it < iters; it++) {
        double T = 0.03 * pow(0.0002 / 0.03, (double)it / iters);
        std::vector<mask> h = g;
        int j = 1 + xr() % (n - 1);
        int lo = std::max(0, j - band);
        int i = lo + xr() % (j - lo);
        h[j] ^= (mask)1 << i;
        if (xr() % 3 == 0) {  // occasional second toggle
          int j2 = 1 + xr() % (n - 1); int lo2 = std::max(0, j2 - band);
          h[j2] ^= (mask)1 << (lo2 + xr() % (j2 - lo2));
        }
        Poset Q; build(n, h, Q);
        if (!connected_incomp(Q) || range_of(Q) > DMAX) continue;
        Result S; long double v = value(Q, S);
        if (v <= cur || ur() < exp(-(double)(v - cur) / T)) {
          g = h; cur = v;
          if (v < best - 1e-15L) { best = v; bestjson = json(Q, S); }
        }
      }
    }
    printf("{\"tag\":\"search_%s\",\"D\":%d,\"rec\":%s}\n", obj.c_str(), DMAX, bestjson.c_str());
    fflush(stdout);
  }
  return 0;
}

static const char *OEIS_A000112[] = {"1", "1", "2", "5", "16", "63", "318", "2045", "16999", "183231",
                                     "2567284", "46749427"};

int main(int argc, char **argv) {
  if (argc >= 2 && std::string(argv[1]) == "one") {
    int n;
    while (scanf("%d", &n) == 1) {
      Poset P; P.n = n;
      for (int i = 0; i < n; i++) { unsigned m; scanf("%u", &m); P.down[i] = m; }
      fill_up(P);
      Result R; analyse(P, R);
      printf("%s\n", json(P, R).c_str());
    }
    return 0;
  }
  if (argc >= 8 && std::string(argv[1]) == "search") return search_main(argc, argv);
  if (argc < 5) { fprintf(stderr, "usage: probe enum NMAX DMAX OUTPREFIX | probe one\n"); return 2; }
  int NMAX = atoi(argv[2]), DMAX = atoi(argv[3]);
  std::string pre = argv[4];
  long double C = CBFT();
  std::vector<std::string> level = {std::string()};  // n = 0: empty poset
  Canon can;
  for (int n = 1; n <= NMAX; n++) {
    std::unordered_set<std::string> next;
    next.reserve(level.size() * 8);
    for (const std::string &code : level) {
      Poset Q = decode(code, n - 1);
      // enumerate ideals of Q
      std::vector<mask> ideals = {0};
      std::unordered_set<mask> seen = {0};
      for (size_t q = 0; q < ideals.size(); q++) {
        mask I = ideals[q];
        for (int x = 0; x < n - 1; x++)
          if (!(I >> x & 1) && (Q.down[x] & ~I) == 0) {
            mask J = I | ((mask)1 << x);
            if (seen.insert(J).second) ideals.push_back(J);
          }
      }
      for (mask I : ideals) {
        Poset P;
        P.n = n;
        for (int i = 0; i < n - 1; i++) P.down[i] = Q.down[i];
        P.down[n - 1] = I;
        fill_up(P);
        if (DMAX < 99) {
          // only the new element and elements it is incomparable to can change
          if (range_of(P) > DMAX) continue;
        }
        next.insert(can.run(P));
      }
    }
    level.assign(next.begin(), next.end());
    std::sort(level.begin(), level.end());
    std::unordered_set<std::string>().swap(next);
    // analyse
    std::vector<Bucket> B(n + 1);
    long long nconn = 0;
    FILE *out = fopen((pre + "_n" + std::to_string(n) + ".jsonl").c_str(), "w");
    for (const std::string &code : level) {
      Poset P = decode(code, n);
      if (n < 2 || !connected_incomp(P)) continue;
      nconn++;
      Result R;
      analyse(P, R);
      Bucket &b = B[R.pi];
      b.count++;
      if (b.min_dn < 0 || R.dnum * b.min_de < b.min_dn * R.e) { b.min_dn = R.dnum; b.min_de = R.e; }
      if (b.min_Mn < 0 || R.Mnum * b.min_Me < b.min_Mn * R.e) { b.min_Mn = R.Mnum; b.min_Me = R.e; }
      if (3 * R.dnum == R.e) b.n_delta_third++;
      long double del = (long double)R.dnum / (long double)R.e;
      long double M = (long double)R.Mnum / (long double)R.e;
      long double c = (del - C) / (M * M);
      if (c < b.min_c) b.min_c = c;
      if (del < C + M * M / 441.0L) b.n_viol441++;
      long double ta = (long double)R.trip_min_num / (long double)R.e;
      long double tc = (ta - C) / (M * M);
      if (R.ntrip > 0 && tc < b.min_trip_c) b.min_trip_c = tc;
      if (R.ntrip > 0 && ta < C + M * M / 441.0L) b.n_trip_viol441++;
      if (!R.trip_all_bft || R.ntrip == 0) b.n_not_bft++;
      if (R.nstruct) {
        b.n_with_struct++;
        if (R.struct_c_min < b.min_struct_c) b.min_struct_c = R.struct_c_min;
      }
      auto mk = [&]() { return json(P, R); };
      b.td.add(del, mk);
      b.tM.add(M, mk);
      b.tc.add(c, mk);
      if (R.nstruct) b.ts.add(R.struct_c_min, mk);
    }
    printf("n=%d posets(pi<=%d)=%zu%s connected-G=%lld\n", n, DMAX, level.size(),
           (DMAX >= 99 && n < 12) ? (std::string(" OEIS_A000112=") + OEIS_A000112[n]).c_str() : "",
           nconn);
    for (int pi = 0; pi <= n; pi++) {
      Bucket &b = B[pi];
      if (!b.count) continue;
      printf("  pi=%d count=%lld min_delta=%s/%s (%.6Lf) n_delta=1/3:%lld min_M=%s/%s (%.6Lf) "
             "min_c=%s min_trip_c=%s viol441=%lld trip_viol441=%lld not_bft=%lld "
             "with_struct=%lld min_struct_c=%s\n",
             pi, b.count, i2s(b.min_dn).c_str(), i2s(b.min_de).c_str(),
             (long double)b.min_dn / (long double)b.min_de, b.n_delta_third, i2s(b.min_Mn).c_str(),
             i2s(b.min_Me).c_str(), (long double)b.min_Mn / (long double)b.min_Me, fmt(b.min_c).c_str(),
             fmt(b.min_trip_c).c_str(), b.n_viol441, b.n_trip_viol441, b.n_not_bft, b.n_with_struct,
             fmt(b.min_struct_c).c_str());
      const char *tags[4] = {"min_delta", "min_M", "min_c", "min_struct_c"};
      TopK *ts[4] = {&b.td, &b.tM, &b.tc, &b.ts};
      for (int t = 0; t < 4; t++) {
        ts[t]->prune();
        for (auto &p : ts[t]->v)
          fprintf(out, "{\"tag\":\"%s\",\"rec\":%s}\n", tags[t], p.second.c_str());
      }
    }
    fclose(out);
    fflush(stdout);
  }
  return 0;
}
