/* aud.c (audit mg-ebbe of mg-cfba / KSBFT-S): independent exact pair-law engine.
 * Shares no code with nb.c.  Input: lines "n m_0 .. m_{n-1}" (hex strict down-masks), n <= 20.
 * Method: forward count f(I) over down-closed sets by DP on subsets in popcount order via a hash-free
 * dense array (n <= 20 -> 2^n entries), backward count g(I) likewise; #ext(a before b) =
 * sum over ideals I with a,b not in I and I+a an ideal of f(I) * g(I+a).
 * Output per poset (one line):  n e dN_num dN_den ... in the form
 *   <poset> | e=<e> d=<num>/<e> dN=<num>/<e> dP=<num>/<e> dD=<num>/<e> nn=<#non-nested pairs>
 *   NB=<0/1> PNB=<0/1> DNB=<0/1> NBopen=<0/1> Bopen=<0/1> trap=<lemma1.1 mismatches> dbl=<doubling violations>
 * where d* are max over (all / nested / primal-nested / dual-nested) incomparable pairs of min(B, e-B),
 * NB* use the closed window [e/3, 2e/3] exactly (3B >= e && 3B <= 2e), *open uses strict inequalities.
 * trap: number of incomparable pairs where (non-nested) != (top pair of an induced 2+2 AND bottom pair of one).
 * dbl: pairs (x,b0) with down(x)=down(b0), up(x) sub up(b0), W = up(b0)\up(x) minus b0 nonempty with a unique
 *      minimum b1, violating B(x<b1) = 2 B(x<b0) or 2 B(x<b0) > e.  (Doubling Lemma, used by KSBFT-S Lemma 2.1.)
 *      dblcnt = number of such pairs tested.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef unsigned long long u64;
typedef unsigned __int128 u128;
static int n; static unsigned dn[32], upm[32];
static u128 *F, *G; static unsigned char *isI;

static void pr128(char *s, u128 v){ char b[64]; int k=0; if(!v){strcpy(s,"0");return;} while(v){b[k++]='0'+(int)(v%10); v/=10;} for(int i=0;i<k;i++) s[i]=b[k-1-i]; s[k]=0; }

int main(int argc, char **argv){
  char line[4096];
  int want_pairs = argc > 1 && !strcmp(argv[1], "-v");
  int ctrl = argc > 1 && !strcmp(argv[1], "-control"); /* planted defects: trap uses top-only, dbl expects 3x */
  while (fgets(line, sizeof line, stdin)) {
    char *p = line; char *e2; n = (int)strtol(p, &e2, 10); if (e2 == p) continue; p = e2;
    for (int i = 0; i < n; i++) { dn[i] = (unsigned)strtoul(p, &e2, 16); p = e2; }
    for (int i = 0; i < n; i++) { upm[i] = 0; for (int j = 0; j < n; j++) if (dn[j] >> i & 1) upm[i] |= 1u << j; }
    unsigned N = 1u << n;
    F = calloc(N, sizeof(u128)); G = calloc(N, sizeof(u128)); isI = calloc(N, 1);
    for (unsigned S = 0; S < N; S++) { int ok = 1; for (int i = 0; i < n && ok; i++) if ((S >> i & 1) && (dn[i] & ~S)) ok = 0; isI[S] = ok; }
    F[0] = 1;
    for (unsigned S = 0; S < N; S++) if (isI[S] && F[S]) for (int i = 0; i < n; i++) if (!(S >> i & 1) && isI[S | 1u << i]) F[S | 1u << i] += F[S];
    G[N - 1] = 1;
    for (unsigned S = N; S-- > 0;) if (isI[S] && S != N - 1) { u128 t = 0; for (int i = 0; i < n; i++) if (!(S >> i & 1) && isI[S | 1u << i]) t += G[S | 1u << i]; G[S] = t; }
    u128 e = F[N - 1];
    static u128 B[32][32];
    for (int a = 0; a < n; a++) for (int b = 0; b < n; b++) B[a][b] = 0;
    for (unsigned S = 0; S < N; S++) if (isI[S]) for (int a = 0; a < n; a++) if (!(S >> a & 1) && isI[S | 1u << a]) {
      u128 v = F[S] * G[S | 1u << a];
      for (int b = 0; b < n; b++) if (b != a && !(S >> b & 1)) B[a][b] += v;
    }
    u128 d = 0, dN = 0, dP = 0, dD = 0; int nn = 0, nbo = 0, bo = 0, trap = 0, dbl = 0, dblcnt = 0;
    int NB = 0, PNB = 0, DNB = 0, any = 0;
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) {
      if ((dn[a] >> b & 1) || (dn[b] >> a & 1)) continue;
      any = 1;
      u128 x = B[a][b]; u128 m = x < e - x ? x : e - x;
      int prim = !(dn[a] & ~dn[b]) || !(dn[b] & ~dn[a]);
      int dual = !(upm[a] & ~upm[b]) || !(upm[b] & ~upm[a]);
      int nest = prim || dual;
      int bal = 3 * x >= e && 3 * x <= 2 * e, balo = 3 * x > e && 3 * x < 2 * e;
      if (m > d) d = m;
      if (nest && m > dN) dN = m;
      if (prim && m > dP) dP = m;
      if (dual && m > dD) dD = m;
      if (!nest) nn++;
      if (nest && bal) NB = 1; if (prim && bal) PNB = 1; if (dual && bal) DNB = 1;
      if (nest && balo) nbo = 1; if (balo) bo = 1;
      /* Lemma 1.1: top pair of induced 2+2: exists u<a, v<b with u||b, v||a, u||v */
      int top = 0, bot = 0;
      for (int u = 0; u < n && !top; u++) if (dn[a] >> u & 1) for (int v = 0; v < n; v++) if (dn[b] >> v & 1) {
        int ub = !(dn[b] >> u & 1) && !(upm[b] >> u & 1) && u != b;
        int va = !(dn[a] >> v & 1) && !(upm[a] >> v & 1) && v != a;
        int uv = u != v && !(dn[u] >> v & 1) && !(dn[v] >> u & 1);
        if (ub && va && uv) { top = 1; break; }
      }
      for (int u = 0; u < n && !bot; u++) if (upm[a] >> u & 1) for (int v = 0; v < n; v++) if (upm[b] >> v & 1) {
        int ub = !(dn[b] >> u & 1) && !(upm[b] >> u & 1) && u != b;
        int va = !(dn[a] >> v & 1) && !(upm[a] >> v & 1) && v != a;
        int uv = u != v && !(dn[u] >> v & 1) && !(dn[v] >> u & 1);
        if (ub && va && uv) { bot = 1; break; }
      }
      if ((!nest) != (ctrl ? top : (top && bot))) trap++;
      if (want_pairs) { char s1[64]; pr128(s1, x); printf("  pair %d %d B=%s prim=%d dual=%d\n", a, b, s1, prim, dual); }
    }
    /* Doubling check over ordered pairs */
    for (int x = 0; x < n; x++) for (int b0 = 0; b0 < n; b0++) {
      if (x == b0 || (dn[x] >> b0 & 1) || (dn[b0] >> x & 1)) continue;
      if (dn[x] != dn[b0] || (upm[x] & ~upm[b0])) continue;
      unsigned W = upm[b0] & ~upm[x]; if (!W) continue;
      /* unique minimum of W: element w in W below all others of W */
      int b1 = -1;
      for (int w = 0; w < n; w++) if (W >> w & 1) { if (((W & ~(1u << w)) & ~upm[w]) == 0) { b1 = w; break; } }
      if (b1 < 0) continue;
      dblcnt++;
      if (B[x][b1] != (ctrl ? 3 : 2) * B[x][b0] || 2 * B[x][b0] > e) dbl++;
    }
    char se[64], s1[64], s2[64], s3[64], s4[64];
    pr128(se, e); pr128(s1, d); pr128(s2, dN); pr128(s3, dP); pr128(s4, dD);
    line[strcspn(line, "\n")] = 0;
    printf("%s | e=%s d=%s dN=%s dP=%s dD=%s nn=%d chain=%d NB=%d PNB=%d DNB=%d NBopen=%d Bopen=%d trap=%d dbl=%d dblcnt=%d\n",
           line, se, s1, s2, s3, s4, nn, !any, NB, PNB, DNB, nbo, bo, trap, dbl, dblcnt);
    free(F); free(G); free(isI);
  }
  return 0;
}
