/* lemw.c (mg-f218) -- exhaustive check of Lemma W (docs/KSBFT-H-lemma-W.md).
 *
 * Mode "all N": every naturally labelled poset on N elements (count must
 * equal OEIS A006455: 1,2,7,40,357,4824,96428,2800472 for N=1..8 -- the
 * positive control on the generator).  Linear extensions are enumerated
 * one by one (exact integer counts).  For every ordered pair (y,x) with
 * x || y it records, over all extensions g:
 *   cyx = #{g(y) < g(x)},  c1 = #{g(x) = g(y)+1},  c2 = #{g(x) = g(y)+2},
 *   cge2 = #{g(x) - g(y) >= 2},
 * and Nxy = #{w != x,y : not w<y and not x<w}  (the set N of the doc).
 * Checks (each prints its violation count; the doc's proofs say 0):
 *   K0  cge2 > 0  iff  Nxy > 0              (the dichotomy, Lemma W part 1)
 *   K1  c1 <= piw*c2 when Nxy>0, piw = max range over N (Lemma W, injection)
 *   K2  cyx <= (pi+1)*cge2 when Nxy>0        (Lemma W, stated form)
 * Reports per range pi: max of c1/c2 (tightness of the 2D factor), min of
 * cge2/cyx over pairs with N nonempty, and the same min restricted to pairs
 * (x,y) that are the first two members of a Case-D BFT triple (x,y,z):
 *   x<z, x||y, y||z, h(x)<=h(y)<=h(z)<=h(x)+2  (heights compared exactly as
 *   integer position sums over e(P)).
 * NEGATIVE CONTROL: "K1m" tests the FALSE claim c1 <= (piw-1)*c2, printed
 * as a count that must be > 0, i.e. the checker can fire at the sharp
 * constant and the 0 of K1 is not an instrument that never fires. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXN 9
static int n; static unsigned down[MAXN], up[MAXN], inc[MAXN];
static long long cyx[MAXN][MAXN], c1[MAXN][MAXN], c2[MAXN][MAXN], cge2[MAXN][MAXN], spos[MAXN], e;
static int pos[MAXN];
static long long nposet=0, K0=0, K1=0, K2=0, K1m=0, npairs=0;
static double maxr1[MAXN+1], minr[MAXN+1], minrB[MAXN+1], minrB30[MAXN+1];
static long long nB[MAXN+1]; static unsigned wB[MAXN+1][MAXN]; static int wxyz[MAXN+1][3]; static double wpp[MAXN+1][2]; static unsigned wB30[MAXN+1][MAXN]; static int wxyz30[MAXN+1][3]; static double wpp30[MAXN+1][2];
static void ext(unsigned I,int k){
  if(k==n){ e++; for(int a=0;a<n;a++){ spos[a]+=pos[a];
      unsigned r=inc[a]; while(r){int b=__builtin_ctz(r); r&=r-1; /* y=a, x=b */
        int d=pos[b]-pos[a]; if(d>0){cyx[a][b]++; if(d==1)c1[a][b]++; else {cge2[a][b]++; if(d==2)c2[a][b]++;}}}}
    return; }
  for(int x=0;x<n;x++) if(!(I>>x&1) && (down[x]&~I)==0){ pos[x]=k; ext(I|1u<<x,k+1); }
}
static void analyse(void){
  nposet++;
  for(int i=0;i<n;i++) up[i]=0;
  for(int j=0;j<n;j++) for(int i=0;i<n;i++) if(down[j]>>i&1) up[i]|=1u<<j;
  unsigned full=(1u<<n)-1; int pi=0;
  for(int i=0;i<n;i++){ inc[i]=full&~(down[i]|up[i]|(1u<<i)); int c=__builtin_popcount(inc[i]); if(c>pi)pi=c; }
  if(pi==0) return;
  memset(cyx,0,sizeof cyx); memset(c1,0,sizeof c1); memset(c2,0,sizeof c2); memset(cge2,0,sizeof cge2); memset(spos,0,sizeof spos); e=0;
  ext(0,0);
  for(int y=0;y<n;y++) for(int x=0;x<n;x++) if(inc[y]>>x&1){
    npairs++;
    int Nxy=0, piw=0;
    for(int w=0;w<n;w++) if(w!=x&&w!=y && !(down[y]>>w&1) && !(up[x]>>w&1)){ Nxy++; int c=__builtin_popcount(inc[w]); if(c>piw)piw=c; }
    if((cge2[y][x]>0)!=(Nxy>0)) K0++;
    if(!Nxy) continue;
    if(c1[y][x] > (long long)piw*c2[y][x]) K1++;
    if(c1[y][x] > (long long)(piw-1)*c2[y][x]) K1m++;
    if(cyx[y][x] > ((long long)pi+1)*cge2[y][x]) K2++;
    if(c2[y][x]>0){ double r=(double)c1[y][x]/c2[y][x]; if(r>maxr1[pi]) maxr1[pi]=r; }
    double q=(double)cge2[y][x]/cyx[y][x]; if(q<minr[pi]) minr[pi]=q;
    /* first two of a Case-D BFT triple (x,y,z)? */
    for(int z=0;z<n;z++) if((up[x]>>z&1) && (inc[y]>>z&1)){
      if(spos[x]<=spos[y] && spos[y]<=spos[z] && spos[z]<=spos[x]+2*e){
        nB[pi]++; if(q<minrB[pi]-1e-12){ minrB[pi]=q; memcpy(wB[pi],down,sizeof down); wxyz[pi][0]=x;wxyz[pi][1]=y;wxyz[pi][2]=z; wpp[pi][0]=(double)cyx[y][x]/e; wpp[pi][1]=(double)cyx[z][y]/e; }
        /* local balances p=P[y<x], p'=P[z<y] */
        double p=(double)cyx[y][x]/e, pp=(double)cyx[z][y]/e; double mx=p>pp?p:pp;
        if(mx<=0.30 && q<minrB30[pi]-1e-12){ minrB30[pi]=q; memcpy(wB30[pi],down,sizeof down); wxyz30[pi][0]=x;wxyz30[pi][1]=y;wxyz30[pi][2]=z; wpp30[pi][0]=p; wpp30[pi][1]=pp; }
      } }
  }
}
static void gen(int j){
  if(j==n){ analyse(); return; }
  /* down[j] ranges over order ideals of the poset on {0..j-1} */
  unsigned lim=1u<<j;
  for(unsigned s=0;s<lim;s++){ int ok=1; unsigned r=s; while(r){int i=__builtin_ctz(r); r&=r-1; if((down[i]&~s)){ok=0;break;}}
    if(ok){ down[j]=s; gen(j+1); } }
}
int main(int argc,char**argv){
  n=atoi(argv[1]);
  for(int i=0;i<=MAXN;i++){maxr1[i]=0; minr[i]=minrB[i]=minrB30[i]=9;}
  gen(0);
  printf("N=%d posets=%lld (A006455 control) incomparable_ordered_pairs=%lld\n",n,nposet,npairs);
  printf("  K0 dichotomy violations=%lld  K1 (c1<=piN*c2) violations=%lld  K2 (p<=(pi+1)P[gap>=2]) violations=%lld\n",K0,K1,K2);
  printf("  negative control K1m (FALSE claim c1<=(piN-1)*c2) violations=%lld (must be >0)\n",K1m);
  for(int p=1;p<n;p++) if(minr[p]<9)
    printf("  pi=%d  max c1/c2=%.6f (pi=%d)  min P[gap>=2]/p=%.6f (1/(pi+1)=%.6f)  BFT-D: n=%lld min=%.6f  with max(p,p')<=0.30: %.6f\n",
      p,maxr1[p],p,minr[p],1.0/(p+1),nB[p],minrB[p]<9?minrB[p]:-1,minrB30[p]<9?minrB30[p]:-1);
  for(int p=1;p<n;p++) if(minrB[p]<9){ printf("  witness pi=%d down-sets [",p); for(int i=0;i<n;i++) printf("%s%u",i?",":"",wB[p][i]);
    printf("] (x,y,z)=(%d,%d,%d) p=%.6f p'=%.6f\n",wxyz[p][0],wxyz[p][1],wxyz[p][2],wpp[p][0],wpp[p][1]); }
  for(int p=1;p<n;p++) if(minrB30[p]<9){ printf("  witness(max(p,p')<=0.30) pi=%d down-sets [",p); for(int i=0;i<n;i++) printf("%s%u",i?",":"",wB30[p][i]);
    printf("] (x,y,z)=(%d,%d,%d) p=%.6f p'=%.6f\n",wxyz30[p][0],wxyz30[p][1],wxyz30[p][2],wpp30[p][0],wpp30[p][1]); }
  return 0;
}
