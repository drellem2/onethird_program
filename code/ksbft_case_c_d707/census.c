/* census.c (mg-d707) -- exact linear-extension statistics for posets.
 *
 * Mode "all N":   every naturally labelled poset on N elements (N <= 8).
 *                 Positive control: the count must equal OEIS A006455
 *                 (2, 7, 40, 357, 4824, 96428, 2800472 for N = 2..8).
 * Mode "rand N W P SAMPLES SEED": random naturally labelled posets on N
 *                 elements (N <= 22) with i<j forced when j-i > W and each
 *                 other pair i<j related with probability P, then closed
 *                 transitively.  Range is then <= 2W.
 * Mode "fib M":   the Fibonacci poset F_M on 2M+1 elements (x_i < x_j iff
 *                 j-i >= 2); a second positive control against the paper's
 *                 closed form d = F_{2|i|}/F_{2m+2}.
 *
 * Only posets whose incomparability graph G(P) is connected are analysed
 * (the paper's WLOG, section 4; it implies n>=2 non-chain).  Per poset:
 *   h(x) = E f(x);  v_1..v_n sorted by h;  d_i = h(v_i) - i;  M = max|d_i|;
 *   delta = max over incomparable pairs of min(p, 1-p);  pi = range;
 *   d1*(pi+1)   -- PROVEN >= 1 in docs/KSBFT-B-case-c-attack.md (Prop B);
 *                  printed as a live check of that proof.
 *   minPair = min P[u<v] over incomparable u,v;  minGap2 = min over
 *         ordered incomparable (y,x) with P>0 of P[f(x)-f(y)>=2] (the event
 *         Lemma 3.2(iii) bounds below by q_3 via Lemma 3.1);
 *   B_j = best balance over incomparable pairs lying inside the first j or
 *         inside the last j elements of the h-order (boundary window j).
 * Linear extensions are counted by DP over order ideals (reachable set
 * only), all in double; e(P) <= 22!/... is not exact in double for the
 * random mode at large N, so the random mode is EMPIRICAL at ~1e-12 rel. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#define MAXN 22
#define NB 9   /* B_2..B_8 */
static int n;
static unsigned down[MAXN], upm[MAXN];
static double *Nw, *Sw; static char *vis; static unsigned *ideals; static long nid;

typedef struct { long count; double minGap2, minPair; unsigned wGap[MAXN]; double minM, minDelta, minD1ratio, minB[NB]; unsigned wM[MAXN]; unsigned wB[NB][MAXN]; double wMdelta, wBdelta[NB]; } Row;
static Row rows[2*MAXN+1];
static long total_all=0, total_conn=0;
static double lastM, lastDelta, lastB[NB], lastD1ratio; static int lastPi, lastConn;

static void closure(void){ /* down[] strict down-sets, natural labelling */
  for(int j=0;j<n;j++){ unsigned s=down[j]; for(int i=j-1;i>=0;i--) if(s>>i&1) s|=down[i]; down[j]=s; } }

static void pw(unsigned *w){ printf("["); for(int i=0;i<n;i++) printf("%s%u",i?",":"",w[i]); printf("]"); }

static void analyse(int verbose){
  unsigned full=(n==32)?0xffffffffu:((1u<<n)-1);
  for(int i=0;i<n;i++) upm[i]=0;
  for(int j=0;j<n;j++) for(int i=0;i<n;i++) if(down[j]>>i&1) upm[i]|=1u<<j;
  unsigned inc[MAXN];
  for(int i=0;i<n;i++) inc[i]=full & ~(down[i]|upm[i]|(1u<<i));
  unsigned seen=1, fr=1;
  while(fr){ unsigned nf=0; for(int i=0;i<n;i++) if(fr>>i&1) nf|=inc[i]; nf&=~seen; seen|=nf; fr=nf; }
  total_all++; lastConn=0;
  if(seen!=full || n<2) return;
  lastConn=1;
  total_conn++;
  int pi=0; for(int i=0;i<n;i++){int c=__builtin_popcount(inc[i]); if(c>pi)pi=c;}
  /* BFS over reachable ideals, in order of size (a BFS from the empty ideal
     visits ideals in nondecreasing size) */
  nid=0; ideals[nid++]=0; vis[0]=1; Nw[0]=1;
  for(long q=0;q<nid;q++){ unsigned I=ideals[q];
    for(int x=0;x<n;x++) if(!(I>>x&1) && (down[x]&~I)==0){ unsigned J=I|1u<<x;
      if(!vis[J]){ vis[J]=1; Nw[J]=0; ideals[nid++]=J; } Nw[J]+=Nw[I]; } }
  for(long q=nid-1;q>=0;q--){ unsigned I=ideals[q]; if(I==full){Sw[I]=1;continue;} double s=0;
    for(int x=0;x<n;x++) if(!(I>>x&1) && (down[x]&~I)==0) s+=Sw[I|1u<<x]; Sw[I]=s; }
  double e=Nw[full];
  double h[MAXN]; static double pb[MAXN][MAXN]; memset(h,0,sizeof h); memset(pb,0,sizeof pb);
  for(long q=0;q<nid;q++){ unsigned I=ideals[q]; if(I==full) continue; int k=__builtin_popcount(I)+1;
    for(int x=0;x<n;x++) if(!(I>>x&1) && (down[x]&~I)==0){ double w=Nw[I]*Sw[I|1u<<x]/e; h[x]+=w*k;
      unsigned rest=inc[x]&~I; for(int y=0;y<n;y++) if(rest>>y&1) pb[x][y]+=w; } }
  /* padj[y][x] = P[x immediately after y] */
  static double padj[MAXN][MAXN]; memset(padj,0,sizeof padj);
  for(long q=0;q<nid;q++){ unsigned I=ideals[q]; if(I==full) continue;
    for(int y=0;y<n;y++) if(!(I>>y&1) && (down[y]&~I)==0){ unsigned J=I|1u<<y; double w0=Nw[I];
      for(int x=0;x<n;x++) if(!(J>>x&1) && (down[x]&~J)==0 && (inc[y]>>x&1)) padj[y][x]+=w0*Sw[J|1u<<x]/e; } }
  double minGap2=1e9, minPair=1e9;
  for(int x=0;x<n;x++) for(int y=0;y<n;y++) if(x!=y && (inc[x]>>y&1)){
    double g2=pb[y][x]-padj[y][x]; if(g2>1e-13 && g2<minGap2) minGap2=g2;
    if(pb[y][x]<minPair) minPair=pb[y][x]; }
  for(long q=0;q<nid;q++) vis[ideals[q]]=0;
  double delta=0;
  for(int x=0;x<n;x++) for(int y=x+1;y<n;y++) if(inc[x]>>y&1){ double p=pb[x][y]; double b=p<1-p?p:1-p; if(b>delta)delta=b; }
  int ord[MAXN]; for(int i=0;i<n;i++) ord[i]=i;
  for(int i=0;i<n;i++) for(int j=i+1;j<n;j++) if(h[ord[j]]<h[ord[i]]-1e-12){int t=ord[i];ord[i]=ord[j];ord[j]=t;}
  double M=0; for(int i=0;i<n;i++){ double d=fabs(h[ord[i]]-(i+1)); if(d>M)M=d; }
  double d1=h[ord[0]]-1, d1ratio=d1*(pi+1);
  double B[NB];
  for(int j=2;j<NB;j++){ double b=0; int jj=j<n?j:n;
    for(int a=0;a<jj;a++) for(int c=a+1;c<jj;c++){
      int x=ord[a],y=ord[c]; if(inc[x]>>y&1){double p=pb[x][y]; double t=p<1-p?p:1-p; if(t>b)b=t;}
      x=ord[n-1-a]; y=ord[n-1-c]; if(inc[x]>>y&1){double p=pb[x][y]; double t=p<1-p?p:1-p; if(t>b)b=t;} }
    B[j]=b; }
  if(verbose){ printf("  h-order displacements d_i:"); for(int i=0;i<n;i++) printf(" %.6f",h[ord[i]]-(i+1));
    printf("\n  M=%.6f delta=%.6f pi=%d d1=%.6f B2=%.6f B3=%.6f\n",M,delta,pi,d1,B[2],B[3]); }
  lastM=M; lastDelta=delta; lastD1ratio=d1ratio; lastPi=pi; for(int j=2;j<NB;j++) lastB[j]=B[j];
  Row *r=&rows[pi]; r->count++;
  if(minGap2<r->minGap2){ r->minGap2=minGap2; memcpy(r->wGap,down,sizeof down); }
  if(minPair<r->minPair) r->minPair=minPair;
  if(M<r->minM-1e-12){ r->minM=M; memcpy(r->wM,down,sizeof down); r->wMdelta=delta; }
  if(delta<r->minDelta) r->minDelta=delta;
  if(d1ratio<r->minD1ratio) r->minD1ratio=d1ratio;
  for(int j=2;j<NB;j++) if(B[j]<r->minB[j]-1e-12){ r->minB[j]=B[j]; memcpy(r->wB[j],down,sizeof down); r->wBdelta[j]=delta; }
}
static void rec(int j){
  if(j==n){ analyse(0); return; }
  for(unsigned S=0;S<(1u<<j);S++){ unsigned cl=S; for(int i=0;i<j;i++) if(S>>i&1) cl|=down[i]; if(cl!=S) continue; down[j]=S; rec(j+1); }
}
static unsigned long long rs=88172645463325252ULL;
static double urand(void){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return (rs>>11)*(1.0/9007199254740992.0); }
static void report(const char*tag){
  printf("%s posets=%ld connected=%ld\n",tag,total_all,total_conn);
  for(int p=1;p<=2*MAXN;p++) if(rows[p].count){ Row*r=&rows[p];
    printf("pi=%d count=%ld minM=%.6f minDelta=%.6f min[d1*(pi+1)]=%.6f",p,r->count,r->minM,r->minDelta,r->minD1ratio);
    for(int j=2;j<NB;j++) printf(" minB%d=%.6f",j,r->minB[j]);
    printf("\n   minP[u<v] over incomparable pairs=%.6f  min positive P[f(x)-f(y)>=2]=%.6f argmin=",r->minPair,r->minGap2); pw(r->wGap);
    printf("\n   argminM(delta=%.6f)=",r->wMdelta); pw(r->wM);
    printf("\n   argminB4(delta=%.6f)=",r->wBdelta[4]); pw(r->wB[4]); printf("\n"); }
}

/* Mode "search N D ITERS SEED OBJ": simulated-annealing local search over
 * naturally labelled posets with range <= D, minimising OBJ in
 * {M, delta, B3, B4, B5, B6}.  Generators gen[j] (subset of {0..j-1}) are
 * flipped one bit at a time and closed transitively.  Starts from F_m-type
 * poset (i<j iff j-i>=2) truncated to N.  EMPIRICAL instrument: a search
 * finds upper bounds on infima, never lower bounds.                       */
static unsigned gen[MAXN];
static double objval(const char*obj){
  if(!strcmp(obj,"M")) return lastM; if(!strcmp(obj,"delta")) return lastDelta;
  if(obj[0]=='B') return lastB[obj[1]-'0']; return 1e9; }
static double eval(int D,const char*obj){ for(int j=0;j<n;j++) down[j]=gen[j]; closure(); analyse(0);
  if(!lastConn || lastPi>D) return 1e9; return objval(obj); }
static void do_search(int D,long iters,const char*obj){
  for(int j=0;j<n;j++){ gen[j]=0; for(int i=0;i+2<=j;i++) gen[j]|=1u<<i; }
  double cur=eval(D,obj), best=cur; unsigned bestg[MAXN]; memcpy(bestg,gen,sizeof gen);
  double T0=0.02;
  for(long it=0;it<iters;it++){ double T=T0*(1.0-(double)it/iters)+1e-6;
    int j=1+(int)(urand()*(n-1)); if(j>=n) j=n-1; int i=(int)(urand()*j); if(i>=j) i=j-1;
    gen[j]^=1u<<i; double v=eval(D,obj);
    if(v<=cur || urand()<exp((cur-v)/T)){ cur=v; if(v<best-1e-12){best=v; memcpy(bestg,gen,sizeof gen);} }
    else gen[j]^=1u<<i; }
  memcpy(gen,bestg,sizeof gen); for(int j=0;j<n;j++) down[j]=gen[j]; closure();
  printf("search n=%d D=%d obj=%s best=%.6f poset(down-sets)=",n,D,obj,best); pw(down); printf("\n"); analyse(1);
}
int main(int argc,char**argv){
  if(argc<3){ fprintf(stderr,"usage: census all N | rand N W P SAMPLES SEED | fib M | search N D ITERS SEED OBJ\n"); return 2; }
  for(int p=0;p<=2*MAXN;p++){ rows[p].count=0; rows[p].minM=rows[p].minDelta=rows[p].minD1ratio=rows[p].minGap2=rows[p].minPair=1e9; for(int j=0;j<NB;j++) rows[p].minB[j]=1e9; }
  const char*mode=argv[1];
  if(!strcmp(mode,"fib")) n=2*atoi(argv[2])+1; else n=atoi(argv[2]);
  if(n>MAXN){ fprintf(stderr,"n too large\n"); return 2; }
  size_t sz=(size_t)1<<n; Nw=malloc(sz*sizeof(double)); Sw=malloc(sz*sizeof(double)); vis=calloc(sz,1); ideals=malloc(sz*sizeof(unsigned));
  char tag[200];
  if(!strcmp(mode,"all")){ rec(0); snprintf(tag,sizeof tag,"all n=%d",n); report(tag); }
  else if(!strcmp(mode,"fib")){ for(int j=0;j<n;j++){ down[j]=0; for(int i=0;i+2<=j;i++) down[j]|=1u<<i; }
    printf("fib m=%d n=%d\n",atoi(argv[2]),n); analyse(1); report("fib"); }
  else if(!strcmp(mode,"search")){ rs^=(unsigned long long)atol(argv[5])*0x9E3779B97F4A7C15ULL; if(!rs) rs=1; do_search(atoi(argv[3]),atol(argv[4]),argv[6]); }
  else if(!strcmp(mode,"rand")){ int W=atoi(argv[3]); double P=atof(argv[4]); long S=atol(argv[5]); rs^=(unsigned long long)atol(argv[6])*0x9E3779B97F4A7C15ULL; if(!rs) rs=1;
    for(long s=0;s<S;s++){ for(int j=0;j<n;j++){ unsigned d=0; for(int i=0;i<j;i++){ if(j-i>W || urand()<P) d|=1u<<i; } down[j]=d; } closure(); analyse(0); }
    snprintf(tag,sizeof tag,"rand n=%d W=%d P=%.3f samples=%ld seed=%s",n,W,P,S,argv[6]); report(tag); }
  return 0;
}
