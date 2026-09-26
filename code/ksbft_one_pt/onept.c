/* onept.c (mg-eedd) -- exact census of (ONE-PT): does a non-chain poset P have a vertex v and a pair
 * {x,y} (v not in it) that is balanced, p in [1/3,2/3], in BOTH P and P - v ?
 *
 * All linear-extension counts are exact integers (unsigned __int128); every comparison with 1/3,
 * 2/3 and every margin comparison is done by integer cross-multiplication.  No floating point
 * enters any decision; doubles appear only in printed summaries.
 *
 * MODES
 *   gen IN OUT [D]     read the isomorphism classes on n-1 elements from IN ("-" = the 1-point
 *                      poset), add a new maximal element in every way (new down-set = any order
 *                      ideal), canonicalise, deduplicate, write the classes on n to OUT.  With D,
 *                      keep only posets of range <= D (Pi_D is closed under induced subposets, so
 *                      this still reaches every class of Pi_D).  Prints the class count: the
 *                      positive control is OEIS A000112 (1,2,5,16,63,318,2045,16999,183231,
 *                      2567284 for n=1..10).
 *   scan FILE START STRIDE [indec]   analyse classes START, START+STRIDE, ... of FILE.  With
 *                      "indec", only posets whose incomparability graph is connected.
 *   fib M              exact P[x2 < x1] in the Fibonacci poset F_M against f(M-1)/f(M+1).
 *   brute N SEEDS      cross-check the ideal DP against brute-force permutation counting on
 *                      random posets (positive control for the counter itself).
 *
 * The interval can be narrowed (for the firing control) by env ONEPT_LO/ONEPT_HI as a fraction
 * "a/b": balanced means lo <= p <= 1-lo; default lo = 1/3.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 24
typedef unsigned __int128 u128;
typedef __int128 i128;

static int n;
static uint32_t dn[MAXN]; /* strict down-sets */
static uint32_t upm_[MAXN];
static long LO_A = 1, LO_B = 3; /* balanced: LO_A/LO_B <= p <= 1 - LO_A/LO_B */

/* ------------------------------------------------------------------ canonical form */
static int cn; static uint32_t cdn[MAXN], cup[MAXN];
static uint32_t best[MAXN]; static int have_best;
static long leaves;

static void rerank(int *col, long *key){ /* col[v] := rank of key[v] among distinct keys */
  int idx[MAXN]; for(int i=0;i<cn;i++) idx[i]=i;
  for(int i=1;i<cn;i++){int t=idx[i],j=i; while(j>0 && key[idx[j-1]]>key[t]){idx[j]=idx[j-1];j--;} idx[j]=t;}
  int r=0; for(int i=0;i<cn;i++){ if(i>0 && key[idx[i]]!=key[idx[i-1]]) r++; col[idx[i]]=r; }
}
static int ncolors(const int *col){ int m=-1; for(int i=0;i<cn;i++) if(col[i]>m)m=col[i]; return m+1; }

/* 1-WL refinement on the order: signature = (colour, #down-neighbours of each colour, #up of each).
   Keys are compared as sequences; we build a comparable sequence and rank by sorting. */
static void refine(int *col){
  for(;;){
    int k=ncolors(col);
    static int sig[MAXN][2*MAXN+1];
    for(int v=0;v<cn;v++){ memset(sig[v],0,sizeof(int)*(2*k+1)); sig[v][0]=col[v];
      for(int u=0;u<cn;u++){ if(cdn[v]>>u&1) sig[v][1+col[u]]++; if(cup[v]>>u&1) sig[v][1+k+col[u]]++; } }
    int idx[MAXN]; for(int i=0;i<cn;i++) idx[i]=i;
    int L=2*k+1;
    for(int i=1;i<cn;i++){int t=idx[i],j=i; while(j>0 && memcmp(sig[idx[j-1]],sig[t],0)==0 && 0){}
      while(j>0){ int c=0; for(int q=0;q<L;q++){ if(sig[idx[j-1]][q]!=sig[t][q]){ c = sig[idx[j-1]][q]>sig[t][q]?1:-1; break;} }
        if(c<=0) break; idx[j]=idx[j-1]; j--; }
      idx[j]=t; }
    int nc[MAXN], r=0;
    for(int i=0;i<cn;i++){ if(i>0){ int d=0; for(int q=0;q<L;q++) if(sig[idx[i]][q]!=sig[idx[i-1]][q]){d=1;break;} if(d) r++; } nc[idx[i]]=r; }
    int k2=r+1; memcpy(col,nc,sizeof(int)*cn);
    if(k2==k) return;
  }
}
static void leaf(const int *col){
  leaves++;
  int pos[MAXN]; for(int v=0;v<cn;v++) pos[v]=col[v];
  uint32_t rows[MAXN]; for(int p=0;p<cn;p++) rows[p]=0;
  for(int v=0;v<cn;v++){ uint32_t r=0; for(int u=0;u<cn;u++) if(cdn[v]>>u&1) r|=1u<<pos[u]; rows[pos[v]]=r; }
  if(!have_best || memcmp(rows,best,sizeof(uint32_t)*cn)<0){ /* memcmp on little-endian words: a
      fixed total order on keys, which is all a canonical form needs (it is the same order for
      every labelling of the same poset). */
    memcpy(best,rows,sizeof(uint32_t)*cn); have_best=1; }
}
static void search(int *col){
  refine(col);
  int k=ncolors(col);
  if(k==cn){ leaf(col); return; }
  /* first non-singleton cell (smallest colour with >1 member) */
  int cnt[MAXN]={0}; for(int v=0;v<cn;v++) cnt[col[v]]++;
  int c=0; while(cnt[c]<2) c++;
  for(int v=0;v<cn;v++) if(col[v]==c){
    int nc[MAXN]; long key[MAXN];
    for(int u=0;u<cn;u++) key[u]=2L*col[u]+((col[u]==c && u!=v)?1:0);
    rerank(nc,key); search(nc);
  }
}
/* canonicalise dn[0..n-1] into out[] */
static void canon(const uint32_t *d, int nn, uint32_t *out){
  cn=nn; for(int i=0;i<cn;i++){cdn[i]=d[i]; cup[i]=0;}
  for(int j=0;j<cn;j++) for(int i=0;i<cn;i++) if(cdn[j]>>i&1) cup[i]|=1u<<j;
  int col[MAXN]; for(int i=0;i<cn;i++) col[i]=0;
  have_best=0; search(col);
  memcpy(out,best,sizeof(uint32_t)*cn);
}

/* ------------------------------------------------------------------ hash set of keys */
static uint32_t *store; static long nstore, capstore; static long *htab; static long hcap;
static uint64_t hkey(const uint32_t *k,int nn){ uint64_t h=1469598103934665603ull; for(int i=0;i<nn;i++){ h^=k[i]; h*=1099511628211ull; h^=h>>29; } return h; }
static int insert(const uint32_t *k,int nn){
  if(nstore*2>=hcap){ long nc=hcap?hcap*2:1<<20; long *nt=malloc(sizeof(long)*nc); for(long i=0;i<nc;i++) nt[i]=-1;
    for(long s=0;s<nstore;s++){ uint64_t h=hkey(store+s*nn,nn)&(nc-1); while(nt[h]>=0) h=(h+1)&(nc-1); nt[h]=s; }
    free(htab); htab=nt; hcap=nc; }
  uint64_t h=hkey(k,nn)&(hcap-1);
  while(htab[h]>=0){ if(memcmp(store+htab[h]*nn,k,sizeof(uint32_t)*nn)==0) return 0; h=(h+1)&(hcap-1); }
  if(nstore>=capstore){ capstore=capstore?capstore*2:1<<16; store=realloc(store,sizeof(uint32_t)*nn*capstore); }
  memcpy(store+nstore*nn,k,sizeof(uint32_t)*nn); htab[h]=nstore; nstore++; return 1;
}

static int range_of(const uint32_t *d,int nn){
  uint32_t up[MAXN]={0}; for(int j=0;j<nn;j++) for(int i=0;i<nn;i++) if(d[j]>>i&1) up[i]|=1u<<j;
  int r=0; for(int i=0;i<nn;i++){ int c=nn-1-__builtin_popcount(d[i]|up[i]); if(c>r) r=c; } return r;
}

static int mode_gen(const char *in,const char *out,int D){
  FILE *fi=NULL; int m; long cnt=0;
  uint32_t q[MAXN];
  if(strcmp(in,"-")){ fi=fopen(in,"r"); if(!fi){perror(in);return 1;} }
  long cand=0; leaves=0;
  int nn=-1;
  for(;;){
    if(fi){ if(fscanf(fi,"%d",&m)!=1) break; for(int i=0;i<m;i++){ unsigned x; if(fscanf(fi,"%x",&x)!=1) return 2; q[i]=x; } }
    else { if(cnt) break; m=0; }
    cnt++;
    nn=m+1;
    uint32_t full=(1u<<m)-1;
    for(uint32_t I=0;;I++){ /* order ideals of q */
      int ok=1; for(int i=0;i<m&&ok;i++) if((I>>i&1) && (q[i]&~I)) ok=0;
      if(ok){ uint32_t d[MAXN]; memcpy(d,q,sizeof(uint32_t)*m); d[m]=I; cand++;
        if(D<0 || range_of(d,nn)<=D){ uint32_t k[MAXN]; canon(d,nn,k); insert(k,nn); } }
      if(I==full) break;
    }
  }
  if(fi) fclose(fi);
  FILE *fo=fopen(out,"w"); if(!fo){perror(out);return 1;}
  for(long s=0;s<nstore;s++){ fprintf(fo,"%d",nn); for(int i=0;i<nn;i++) fprintf(fo," %x",store[s*nn+i]); fprintf(fo,"\n"); }
  fclose(fo);
  printf("gen n=%d D=%d from %ld classes: candidates=%ld leaves=%ld classes=%ld\n",nn,D,cnt,cand,leaves,nstore);
  return 0;
}

/* ------------------------------------------------------------------ exact LE statistics */
static u128 *Nw,*Sw; static uint32_t *stamp; static uint32_t curstamp; static uint32_t *ideals;
static void alloc_dp(int nn){ size_t sz=(size_t)1<<nn; Nw=malloc(sizeof(u128)*sz); Sw=malloc(sizeof(u128)*sz); stamp=calloc(sz,sizeof(uint32_t)); ideals=malloc(sizeof(uint32_t)*sz); }

/* counts over the induced subposet on U: cnt[x][y] = #LE with x before y (x,y in U incomparable);
   returns e. */
static u128 lecount(uint32_t U, u128 cnt[MAXN][MAXN]){
  curstamp++; long nid=0; ideals[nid++]=0; stamp[0]=curstamp; Nw[0]=1;
  for(long q=0;q<nid;q++){ uint32_t I=ideals[q];
    uint32_t av=U&~I; while(av){ int x=__builtin_ctz(av); av&=av-1;
      if((dn[x]&U&~I)==0){ uint32_t J=I|1u<<x; if(stamp[J]!=curstamp){stamp[J]=curstamp;Nw[J]=0;ideals[nid++]=J;} Nw[J]+=Nw[I]; } } }
  for(long q=nid-1;q>=0;q--){ uint32_t I=ideals[q]; if(I==U){Sw[I]=1;continue;} u128 s=0;
    uint32_t av=U&~I; while(av){ int x=__builtin_ctz(av); av&=av-1; if((dn[x]&U&~I)==0) s+=Sw[I|1u<<x]; } Sw[I]=s; }
  for(int x=0;x<n;x++) for(int y=0;y<n;y++) cnt[x][y]=0;
  for(long q=0;q<nid;q++){ uint32_t I=ideals[q]; if(I==U) continue;
    uint32_t av=U&~I; while(av){ int x=__builtin_ctz(av); av&=av-1; if((dn[x]&U&~I)==0){
      u128 w=Nw[I]*Sw[I|1u<<x]; uint32_t rest=U&~I&~dn[x]&~upm_[x]&~(1u<<x);
      while(rest){ int y=__builtin_ctz(rest); rest&=rest-1; cnt[x][y]+=w; } } } }
  return Nw[U];
}

/* signed distance of N/e from the boundary of [lo,1-lo], as a fraction num/den with den>0:
   min(N/e - a/b, 1 - a/b - N/e) = min(bN - a e, (b-a)e - bN) / (b e) */
typedef struct { i128 num, den; } frac;
static frac dist(u128 N,u128 e){ i128 A=(i128)(LO_B*N)-(i128)(LO_A*e), B=(i128)((LO_B-LO_A)*e)-(i128)(LO_B*N); frac f={A<B?A:B,(i128)(LO_B*e)}; return f; }
static int fcmp(frac a,frac b){ i128 l=a.num*b.den, r=b.num*a.den; return l<r?-1:l>r?1:0; }
static double fd(frac a){ return (double)a.num/(double)a.den; }
static frac fmin_(frac a,frac b){ return fcmp(a,b)<=0?a:b; }

static void print_poset(void){ printf("%d",n); for(int i=0;i<n;i++) printf(" %x",dn[i]); }

/* aggregates, indexed by range pi */
#define NCLS 18
static const char *clsname[NCLS]={
 "exists v (ONE-PT)", "every v (CONTROL, expected to fail)",
 "some minimal v", "some maximal v", "some extremal (min or max) v", "every extremal v",
 "some v of min h (h-first, any tie)", "some v of max h (h-last, any tie)", "some h-endpoint v",
 "some v of minimal range pi(v)", "some v of maximal range pi(v)",
 "some v comparable to both x,y (with its pair)", "some v and a delta-attaining pair of P",
 "exists v: EVERY balanced pair of P-v balanced in P (and >=1)",
 "some v with P-v indecomposable", "every minimal v",
 "every v with P-v indecomposable", "every v of minimal range pi(v)"};
static long fails[MAXN+1][NCLS], tot[MAXN+1];
static frac worst_margin[MAXN+1]; static int have_wm[MAXN+1]; static uint32_t wm_poset[MAXN+1][MAXN]; static int wm_n[MAXN+1];
static frac worst_mcan[MAXN+1]; static int have_mc[MAXN+1]; static frac worst_eps; static int have_eps;
static long minW_hist[MAXN+2]; /* number of working v */
static int verbose_fail=3; static int printed[NCLS]; static int print_every=0;
/* reweighting lemma R: p_P in [p'/(p'+r(1-p')), r p'/(r p'+1-p')] with r = pi(v)+1, p' = p_{P-v};
   rviol counts violations (expected 0), rctl counts violations with r replaced by pi(v) (a
   firing control: the bound with r-1 must fail somewhere if the lemma is anywhere near tight). */
static long rviol=0, rctl=0, rchecks=0; static frac maxdiff[MAXN+1]; static int have_md[MAXN+1];
static int Rcheck(u128 a,u128 e,u128 a2,u128 e2,long r){ /* 1 if a/e inside the window */
  u128 up_l=a*((u128)r*a2+e2-a2), up_r=(u128)r*a2*e;
  u128 lo_l=a*(a2+(u128)r*(e2-a2)), lo_r=a2*e;
  return up_l<=up_r && lo_l>=lo_r; }

static int indecomposable(uint32_t U){ /* incomparability graph on U connected (|U|>=1) */
  if(!U) return 0; uint32_t seen=1u<<__builtin_ctz(U), fr=seen;
  while(fr){ uint32_t nf=0; uint32_t t=fr; while(t){int i=__builtin_ctz(t); t&=t-1; nf|=U&~dn[i]&~upm_[i]&~(1u<<i);} nf&=~seen; seen|=nf; fr=nf; }
  return seen==U;
}

static void analyse(int only_indec){
  uint32_t full=(n==32)?0xffffffffu:((1u<<n)-1);
  for(int i=0;i<n;i++) upm_[i]=0;
  for(int j=0;j<n;j++) for(int i=0;i<n;i++) if(dn[j]>>i&1) upm_[i]|=1u<<j;
  uint32_t inc[MAXN]; int pi=0, pv[MAXN];
  for(int i=0;i<n;i++){ inc[i]=full&~dn[i]&~upm_[i]&~(1u<<i); pv[i]=__builtin_popcount(inc[i]); if(pv[i]>pi) pi=pv[i]; }
  if(pi==0 || n<3) return; /* chains and n<3 excluded */
  if(only_indec && !indecomposable(full)) return;
  static u128 cP[MAXN][MAXN], cV[MAXN][MAXN];
  u128 eP=lecount(full,cP);
  /* delta-attaining pairs, h */
  frac bestd={-1000000,1}; int any=0;
  for(int x=0;x<n;x++) for(int y=x+1;y<n;y++) if(inc[x]>>y&1){ frac d=dist(cP[x][y],eP); if(!any||fcmp(d,bestd)>0){bestd=d;any=1;} }
  u128 H[MAXN]; /* e * h(x) */
  for(int x=0;x<n;x++){ H[x]=eP*(u128)(1+__builtin_popcount(dn[x])); for(int y=0;y<n;y++) if(inc[x]>>y&1) H[x]+=cP[y][x]; }
  u128 Hmin=H[0],Hmax=H[0]; for(int x=1;x<n;x++){ if(H[x]<Hmin)Hmin=H[x]; if(H[x]>Hmax)Hmax=H[x]; }
  int pmin=n,pmax=-1; for(int x=0;x<n;x++){ if(pv[x]<pmin)pmin=pv[x]; if(pv[x]>pmax)pmax=pv[x]; }
  uint32_t Min=0,Max=0; for(int x=0;x<n;x++){ if(!dn[x]) Min|=1u<<x; if(!upm_[x]) Max|=1u<<x; }
  uint32_t W=0, Wbest=0, Wcomp=0, Wstrong=0, Windec=0, Iset=0;
  frac margin={-1000000,1}; int havem=0; frac mcan={1000000,1};
  frac eps={1000000,1}; int havee=0; /* min over v, pairs balanced in P-v, of distance of p_P outside */
  for(int v=0;v<n;v++){
    uint32_t U=full&~(1u<<v);
    u128 eV=lecount(U,cV);
    int ok=0, okb=0, okc=0, allbal=1, nbal=0; frac mv={-1000000,1}; int havemv=0;
    for(int x=0;x<n;x++) if(x!=v) for(int y=x+1;y<n;y++) if(y!=v && (inc[x]>>y&1)){
      frac dP=dist(cP[x][y],eP), dV=dist(cV[x][y],eV);
      rchecks++; if(!Rcheck(cP[x][y],eP,cV[x][y],eV,pv[v]+1)) rviol++; if(!Rcheck(cP[x][y],eP,cV[x][y],eV,pv[v])) rctl++;
      { i128 l=(i128)(cP[x][y]*eV), r2=(i128)(cV[x][y]*eP); frac df={l>r2?l-r2:r2-l,(i128)(eP*eV)};
        if(!have_md[pv[v]]||fcmp(df,maxdiff[pv[v]])>0){maxdiff[pv[v]]=df;have_md[pv[v]]=1;} }
      frac m=fmin_(dP,dV);
      if(!havem||fcmp(m,margin)>0){margin=m;havem=1;}
      if(!havemv||fcmp(m,mv)>0){mv=m;havemv=1;}
      int bP=dP.num>=0, bV=dV.num>=0;
      if(bV){ nbal++; if(!bP) allbal=0; frac o={dP.num<0?-dP.num:0,dP.den}; if(!havee||fcmp(o,eps)<0){eps=o;havee=1;} }
      if(bP&&bV){ ok=1; if(fcmp(dP,bestd)==0) okb=1; if(!(inc[v]>>x&1) && !(inc[v]>>y&1)) okc=1; }
    }
    if(ok) W|=1u<<v; if(okb) Wbest|=1u<<v; if(okc) Wcomp|=1u<<v; if(allbal&&nbal) Wstrong|=1u<<v;
    if(pv[v]==pmin && fcmp(mv,mcan)<0) mcan=mv;
    if(indecomposable(U)){ Iset|=1u<<v; if(ok) Windec|=1u<<v; }
  }
  uint32_t Hlo=0,Hhi=0,Plo=0,Phi=0; for(int x=0;x<n;x++){ if(H[x]==Hmin)Hlo|=1u<<x; if(H[x]==Hmax)Hhi|=1u<<x; if(pv[x]==pmin)Plo|=1u<<x; if(pv[x]==pmax)Phi|=1u<<x; }
  int f[NCLS];
  f[0]=!W; f[1]=(W!=full); f[2]=!(W&Min); f[3]=!(W&Max); f[4]=!(W&(Min|Max)); f[5]=((W&(Min|Max))!=(Min|Max));
  f[6]=!(W&Hlo); f[7]=!(W&Hhi); f[8]=!(W&(Hlo|Hhi)); f[9]=!(W&Plo); f[10]=!(W&Phi); f[11]=!Wcomp; f[12]=!Wbest; f[13]=!Wstrong; f[14]=!Windec; f[15]=((W&Min)!=Min); f[16]=((W&Iset)!=Iset); f[17]=((W&Plo)!=Plo);
  tot[pi]++;
  minW_hist[__builtin_popcount(W)]++;
  for(int c=0;c<NCLS;c++) if(f[c]){ fails[pi][c]++;
    if((c==1 && print_every) || (printed[c]<verbose_fail && c!=1 && c!=5 && c!=15 && c!=16 && c!=17)){ printed[c]++; printf("FAIL[%s] pi=%d P=",clsname[c],pi); print_poset(); printf(" W=%x Min=%x Max=%x Hlo=%x Hhi=%x\n",W,Min,Max,Hlo,Hhi); } }
  if(!have_wm[pi] || fcmp(margin,worst_margin[pi])<0){ worst_margin[pi]=margin; have_wm[pi]=1; memcpy(wm_poset[pi],dn,sizeof(uint32_t)*n); wm_n[pi]=n; }
  if(!have_mc[pi] || fcmp(mcan,worst_mcan[pi])<0){ worst_mcan[pi]=mcan; have_mc[pi]=1; }
  if(havee && (!have_eps || fcmp(eps,worst_eps)>0)){ worst_eps=eps; have_eps=1; }
}

static int mode_scan(const char *file,long start,long stride,int only_indec){
  FILE *fi=fopen(file,"r"); if(!fi){perror(file);return 1;}
  long idx=0, done=0; int nn;
  int alloc=0;
  while(fscanf(fi,"%d",&nn)==1){
    uint32_t d[MAXN]; for(int i=0;i<nn;i++){ unsigned x; if(fscanf(fi,"%x",&x)!=1) return 2; d[i]=x; }
    if(!alloc){ alloc_dp(nn); alloc=1; }
    if(idx%stride==start){ n=nn; memcpy(dn,d,sizeof(uint32_t)*n); analyse(only_indec); done++; }
    idx++;
  }
  fclose(fi);
  printf("== scan %s start=%ld stride=%ld %s: classes read=%ld analysed=%ld  interval [%ld/%ld, 1-%ld/%ld]\n",strrchr(file,'/')?strrchr(file,'/')+1:file,start,stride,only_indec?"indecomposable-only":"all",idx,done,LO_A,LO_B,LO_A,LO_B);
  for(int p=0;p<=MAXN;p++) if(tot[p]){
    printf("pi=%d non-chains=%ld\n",p,tot[p]);
    for(int c=0;c<NCLS;c++) printf("  fails %-62s %ld\n",clsname[c],fails[p][c]);
    printf("  worst margin (min over P of max over v,pair of min dist in P,P-v) = %.6f = %lld/%lld  at P=",fd(worst_margin[p]),(long long)worst_margin[p].num,(long long)worst_margin[p].den);
    printf("%d",wm_n[p]); for(int i=0;i<wm_n[p];i++) printf(" %x",wm_poset[p][i]); printf("\n");
  }
  printf("working-v count histogram (#v that work, over analysed non-chains):");
  for(int k=0;k<=MAXN;k++) if(minW_hist[k]) printf(" %d:%ld",k,minW_hist[k]); printf("\n");
  /* machine-readable lines, merged across processes by merge.py */
  for(int p=0;p<=MAXN;p++) if(tot[p]){ printf("AGG TOT %d %ld\n",p,tot[p]); for(int c=0;c<NCLS;c++) printf("AGG FAIL %d %d %ld\n",p,c,fails[p][c]);
    printf("AGG WM %d %lld %lld",p,(long long)worst_margin[p].num,(long long)worst_margin[p].den); printf(" %d",wm_n[p]); for(int i=0;i<wm_n[p];i++) printf(" %x",wm_poset[p][i]); printf("\n"); }
  for(int p=0;p<=MAXN;p++) if(have_mc[p]) printf("AGG MC %d %lld %lld\n",p,(long long)worst_mcan[p].num,(long long)worst_mcan[p].den);
  printf("AGG R %ld %ld %ld\n",rchecks,rviol,rctl);
  for(int p=0;p<=MAXN;p++) if(have_md[p]) printf("AGG MD %d %lld %lld\n",p,(long long)maxdiff[p].num,(long long)maxdiff[p].den);
  for(int c=0;c<NCLS;c++) printf("AGG NAME %d %s\n",c,clsname[c]);
  for(int k=0;k<=MAXN;k++) if(minW_hist[k]) printf("AGG HIST %d %ld\n",k,minW_hist[k]);
  if(have_eps) printf("AGG EPS %lld %lld\n",(long long)worst_eps.num,(long long)worst_eps.den);
  if(have_eps) printf("eps-transport: max over P of min over (v, pair balanced in P-v) of dist(p_P,[lo,1-lo]) = %.6f\n",fd(worst_eps));
  return 0;
}

/* ------------------------------------------------------------------ controls */
static int mode_fib(int M){
  n=M; for(int j=0;j<n;j++){ dn[j]=0; for(int i=0;i+2<=j;i++) dn[j]|=1u<<i; }
  for(int i=0;i<n;i++) upm_[i]=0; for(int j=0;j<n;j++) for(int i=0;i<n;i++) if(dn[j]>>i&1) upm_[i]|=1u<<j;
  alloc_dp(n); static u128 c[MAXN][MAXN]; u128 e=lecount((1u<<n)-1,c);
  long f[MAXN+3]; f[1]=1; f[2]=1; for(int k=3;k<MAXN+3;k++) f[k]=f[k-1]+f[k-2];
  int ok = (e==(u128)f[M+1]) && (M<2 || c[1][0]==(u128)f[M-1]);
  printf("fib M=%d e=%llu (f(M+1)=%ld)  #(x2 before x1)=%llu (f(M-1)=%ld)  p=%.6f  %s\n",M,(unsigned long long)e,f[M+1],
         M>=2?(unsigned long long)c[1][0]:0ull,M>=2?f[M-1]:0,M>=2?(double)c[1][0]/(double)e:0.0,ok?"MATCH":"MISMATCH");
  return !ok;
}
static uint64_t rs=88172645463325252ull; static uint64_t rnd(void){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return rs; }
static int mode_brute(int N,int S){
  n=N; alloc_dp(n); int bad=0;
  for(int s=0;s<S;s++){
    for(int j=0;j<n;j++){ dn[j]=0; for(int i=0;i<j;i++) if(rnd()%3==0) dn[j]|=1u<<i; }
    for(int j=0;j<n;j++) for(int i=j-1;i>=0;i--) if(dn[j]>>i&1) dn[j]|=dn[i];
    for(int i=0;i<n;i++) upm_[i]=0; for(int j=0;j<n;j++) for(int i=0;i<n;i++) if(dn[j]>>i&1) upm_[i]|=1u<<j;
    uint32_t full=(1u<<n)-1;
    for(int v=-1;v<n;v++){ uint32_t U=v<0?full:(full&~(1u<<v));
      static u128 c[MAXN][MAXN]; u128 e=lecount(U,c);
      /* brute force over permutations of U */
      int el[MAXN],m=0; for(int i=0;i<n;i++) if(U>>i&1) el[m++]=i;
      long be=0; static long bc[MAXN][MAXN]; memset(bc,0,sizeof bc);
      int perm[MAXN]; for(int i=0;i<m;i++) perm[i]=el[i];
      /* Heap-free: iterate lexicographic permutations */
      for(;;){ int ok=1; uint32_t seen=0; for(int i=0;i<m&&ok;i++){ if(dn[perm[i]]&U&~seen) ok=0; seen|=1u<<perm[i]; }
        if(ok){ be++; for(int i=0;i<m;i++) for(int j=i+1;j<m;j++) bc[perm[i]][perm[j]]++; }
        int i=m-2; while(i>=0 && perm[i]>perm[i+1]) i--; if(i<0) break; int j=m-1; while(perm[j]<perm[i]) j--;
        int t=perm[i];perm[i]=perm[j];perm[j]=t; for(int a=i+1,b=m-1;a<b;a++,b--){t=perm[a];perm[a]=perm[b];perm[b]=t;} }
      if((u128)be!=e) bad++;
      for(int x=0;x<n;x++) for(int y=0;y<n;y++) if(x!=y && (U>>x&1)&&(U>>y&1) && !(dn[x]>>y&1) && !(dn[y]>>x&1)) if((u128)bc[x][y]!=c[x][y]) bad++;
    }
  }
  printf("brute N=%d samples=%d (each with all %d deletions): mismatches=%d %s\n",N,S,N,bad,bad?"MISMATCH":"MATCH");
  return bad!=0;
}

int main(int argc,char **argv){
  if(getenv("ONEPT_PRINT_EVERY")) print_every=1;
  const char *lo=getenv("ONEPT_LO"); if(lo){ if(sscanf(lo,"%ld/%ld",&LO_A,&LO_B)!=2){fprintf(stderr,"bad ONEPT_LO\n");return 2;} }
  if(argc>=4 && !strcmp(argv[1],"gen")) return mode_gen(argv[2],argv[3],argc>4?atoi(argv[4]):-1);
  if(argc>=5 && !strcmp(argv[1],"scan")) return mode_scan(argv[2],atol(argv[3]),atol(argv[4]),argc>5 && !strcmp(argv[5],"indec"));
  if(argc>=3 && !strcmp(argv[1],"fib")) return mode_fib(atoi(argv[2]));
  if(argc>=4 && !strcmp(argv[1],"brute")) return mode_brute(atoi(argv[2]),atoi(argv[3]));
  fprintf(stderr,"usage: see header\n"); return 2;
}
