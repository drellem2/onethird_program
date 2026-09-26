/* indep_95d3.c (mg-95d3) -- INDEPENDENT re-check of mg-eedd (KSBFT-J) code/ksbft_one_pt/onept.c.
 * Written from the statement in docs/KSBFT-J-one-pt.md, not from onept.c.  Design differs on purpose:
 *   generator : add a new MINIMAL element whose up-set is any order FILTER of a class on n-1
 *               (onept.c adds a maximal element).  Exhaustive: delete a minimal element.
 *   dedup     : no canonical form.  Posets are bucketed by a 64-bit refinement-hash invariant and
 *               an exact backtracking isomorphism test is run inside each bucket (onept.c: least
 *               relation matrix over an individualisation-refinement tree).
 *   counter   : ideal DP, pair counts accumulated at the moment the LATER element y is placed
 *               (onept.c: when the earlier element x is placed).  Exact unsigned __int128.
 * MODES
 *   gen D NMAX PREFIX        classes on 1..NMAX elements of range <= D (D<0: all); writes
 *                            PREFIX<n>.txt, prints counts.  Range <= D is closed under deletion.
 *   scan FILE START STRIDE [indec] [lo_a lo_b]   ONE-PT census of classes START,START+STRIDE,...
 *   brute M TRIALS           counter vs brute-force permutations on random posets (and P-v)
 * Poset line format: n then strict down-sets as hex (element i = bit i), as in onept.c.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#define MAXN 18
typedef unsigned __int128 u128;
typedef __int128 i128;

static int pc(uint32_t x){ return __builtin_popcount(x); }
static uint64_t mix(uint64_t x){ x^=x>>33; x*=0xff51afd7ed558ccdULL; x^=x>>33; x*=0xc4ceb9fe1a85ec53ULL; x^=x>>33; return x; }

static void ups(int n,const uint32_t*dn,uint32_t*up){ for(int i=0;i<n;i++) up[i]=0; for(int i=0;i<n;i++) for(int j=0;j<n;j++) if(dn[i]>>j&1) up[j]|=1u<<i; }
static int piv(int n,const uint32_t*dn,const uint32_t*up,int v){ return n-1-pc(dn[v]|up[v]); }
static int rangeP(int n,const uint32_t*dn){ uint32_t up[MAXN]; ups(n,dn,up); int r=0; for(int v=0;v<n;v++){int p=piv(n,dn,up,v); if(p>r)r=p;} return r; }

/* ---------------- invariant + isomorphism ---------------- */
static void colours(int n,const uint32_t*dn,uint64_t*c){
  uint32_t up[MAXN]; ups(n,dn,up); uint64_t nc[MAXN];
  for(int v=0;v<n;v++) c[v]=mix(1000u*pc(dn[v])+pc(up[v])+17);
  for(int r=0;r<n+1;r++){
    for(int v=0;v<n;v++){ uint64_t s=c[v]*0x9E3779B97F4A7C15ULL;
      for(int u=0;u<n;u++){ if(dn[v]>>u&1) s+=mix(c[u]^0x1234567ULL); if(up[v]>>u&1) s+=mix(c[u]^0xabcdef9876ULL); }
      nc[v]=mix(s); }
    memcpy(c,nc,sizeof(uint64_t)*n); }
}
static int cmpu64(const void*a,const void*b){ uint64_t x=*(const uint64_t*)a,y=*(const uint64_t*)b; return x<y?-1:x>y; }
static uint64_t invariant(int n,const uint32_t*dn,uint64_t*c){
  colours(n,dn,c); uint64_t s[MAXN]; memcpy(s,c,sizeof(uint64_t)*n); qsort(s,n,sizeof(uint64_t),cmpu64);
  uint64_t h=mix(n+1); for(int i=0;i<n;i++) h=mix(h^s[i])+i; return h; }

static int in_,map_[MAXN],used_[MAXN]; static const uint32_t *A_,*B_; static const uint64_t *CA_,*CB_;
static int bt(int v){
  if(v==in_) return 1;
  for(int w=0;w<in_;w++){ if(used_[w]||CA_[v]!=CB_[w]) continue; int ok=1;
    for(int u=0;u<v&&ok;u++){ int m=map_[u]; if(((A_[v]>>u)&1)!=((B_[w]>>m)&1) || ((A_[u]>>v)&1)!=((B_[m]>>w)&1)) ok=0; }
    if(!ok) continue; map_[v]=w; used_[w]=1; if(bt(v+1)) return 1; used_[w]=0; }
  return 0; }
static int iso(int n,const uint32_t*a,const uint64_t*ca,const uint32_t*b,const uint64_t*cb){
  in_=n; A_=a; B_=b; CA_=ca; CB_=cb; memset(used_,0,sizeof used_); return bt(0); }

/* ---------------- class store ---------------- */
typedef struct { int n; long cnt, cap; uint16_t *dn; uint64_t *inv; long *next; long *head; long hsz; } store;
static void st_init(store*s,int n){ s->n=n; s->cnt=0; s->cap=1024; s->dn=malloc(sizeof(uint16_t)*n*s->cap); s->inv=malloc(8*s->cap); s->next=malloc(sizeof(long)*s->cap);
  s->hsz=1<<22; s->head=malloc(sizeof(long)*s->hsz); for(long i=0;i<s->hsz;i++) s->head[i]=-1; }
static long isochecks=0, candidates=0;
static void st_add(store*s,const uint32_t*dn){
  int n=s->n; uint64_t c[MAXN], c2[MAXN]; uint64_t h=invariant(n,dn,c); long b=h&(s->hsz-1);
  candidates++;
  for(long i=s->head[b];i>=0;i=s->next[i]){ if(s->inv[i]!=h) continue; uint32_t d2[MAXN]; for(int k=0;k<n;k++) d2[k]=s->dn[i*n+k];
    colours(n,d2,c2); isochecks++; if(iso(n,dn,c,d2,c2)) return; }
  if(s->cnt==s->cap){ s->cap*=2; s->dn=realloc(s->dn,sizeof(uint16_t)*n*s->cap); s->inv=realloc(s->inv,8*s->cap); s->next=realloc(s->next,sizeof(long)*s->cap); }
  for(int k=0;k<n;k++) s->dn[s->cnt*n+k]=(uint16_t)dn[k];
  s->inv[s->cnt]=h; s->next[s->cnt]=s->head[b]; s->head[b]=s->cnt; s->cnt++; }

/* enumerate order ideals of (n,dn): elements taken in a topological order, include only if down-set present */
static int ord_[MAXN], on_; static const uint32_t *odn_; static void (*ocb_)(uint32_t);
static void idrec(int k,uint32_t I){ if(k==on_){ ocb_(I); return; } int e=ord_[k]; idrec(k+1,I); if((odn_[e]&~I)==0) idrec(k+1,I|1u<<e); }
static void ideals(int n,const uint32_t*dn,void(*cb)(uint32_t)){ on_=n; odn_=dn; ocb_=cb; int k=0;
  for(int s=0;s<=n;s++) for(int e=0;e<n;e++) if(pc(dn[e])==s) ord_[k++]=e; idrec(0,0); }

static store *cur_; static uint32_t par_[MAXN]; static int parn_, D_;
static void addmin(uint32_t I){ /* filter F = complement of I; new element z=parn_ below all of F */
  int n=parn_+1; uint32_t F=((1u<<parn_)-1)&~I, dn[MAXN];
  for(int u=0;u<parn_;u++) dn[u]=par_[u] | ((F>>u&1)?1u<<parn_:0); dn[parn_]=0;
  if(D_>=0 && rangeP(n,dn)>D_) return; st_add(cur_,dn); }

static void writest(store*s,const char*fn){ FILE*f=fopen(fn,"w"); for(long i=0;i<s->cnt;i++){ fprintf(f,"%d",s->n); for(int k=0;k<s->n;k++) fprintf(f," %x",s->dn[i*s->n+k]); fprintf(f,"\n"); } fclose(f); }

/* ---------------- exact counter ---------------- */
static int *idxmap=NULL;
static uint32_t IL[1<<17]; static u128 FF[1<<17], BB[1<<17];
/* e = #L(P); N[x][y] = #L with x before y (x,y incomparable) */
static u128 count(int m,const uint32_t*dn,u128 N[MAXN][MAXN]){
  if(!idxmap){ idxmap=malloc(sizeof(int)<<17); for(int i=0;i<(1<<17);i++) idxmap[i]=-1; }
  uint32_t up[MAXN]; ups(m,dn,up);
  long ni=0, lo=0; IL[ni]=0; idxmap[0]=0; FF[0]=1; ni=1;
  while(lo<ni){ long hi=ni; /* BFS level */
    for(long a=lo;a<hi;a++){ uint32_t I=IL[a];
      for(int i=0;i<m;i++){ if(I>>i&1) continue; if(dn[i]&~I) continue; uint32_t J=I|1u<<i;
        if(idxmap[J]<0){ idxmap[J]=ni; IL[ni]=J; FF[ni]=0; ni++; } FF[idxmap[J]]+=FF[a]; } }
    lo=hi; }
  for(long a=ni-1;a>=0;a--){ uint32_t I=IL[a]; u128 s=0; int any=0;
    for(int i=0;i<m;i++){ if(I>>i&1) continue; if(dn[i]&~I) continue; any=1; s+=BB[idxmap[I|1u<<i]]; }
    BB[a]= any? s : 1; }
  for(int x=0;x<m;x++) for(int y=0;y<m;y++) N[x][y]=0;
  for(long a=0;a<ni;a++){ uint32_t I=IL[a];
    for(int y=0;y<m;y++){ if(I>>y&1) continue; if(dn[y]&~I) continue;
      u128 t=FF[a]*BB[idxmap[I|1u<<y]]; uint32_t X=I&~(dn[y]|up[y]); /* x already placed, incomparable to y */
      for(int x=0;x<m;x++) if(X>>x&1) N[x][y]+=t; } }
  u128 e=FF[idxmap[(m==32)?0xffffffffu:((1u<<m)-1)]];
  for(long a=0;a<ni;a++) idxmap[IL[a]]=-1;
  return e; }

static void delete_v(int n,const uint32_t*dn,int v,uint32_t*d2,int*o2n){
  int k=0; for(int i=0;i<n;i++){ if(i==v){o2n[i]=-1;continue;} o2n[i]=k++; }
  for(int i=0;i<n;i++){ if(i==v) continue; uint32_t d=0; for(int j=0;j<n;j++) if(j!=v && (dn[i]>>j&1)) d|=1u<<o2n[j]; d2[o2n[i]]=d; } }

static void pr128(char*b,u128 x){ char t[64]; int k=0; if(!x){strcpy(b,"0");return;} while(x){t[k++]='0'+(int)(x%10);x/=10;} for(int i=0;i<k;i++) b[i]=t[k-1-i]; b[k]=0; }
static u128 gcd128(u128 a,u128 b){ while(b){u128 t=a%b;a=b;b=t;} return a; }

/* ---------------- brute-force control ---------------- */
static u128 bN[MAXN][MAXN]; static u128 be;
static void brute(int m,const uint32_t*dn){ int perm[MAXN]; for(int i=0;i<m;i++) perm[i]=i; be=0; for(int x=0;x<m;x++) for(int y=0;y<m;y++) bN[x][y]=0;
  /* Heap-free: iterate all permutations via next_permutation */
  for(;;){ int ok=1; uint32_t seen=0; for(int k=0;k<m&&ok;k++){ if(dn[perm[k]]&~seen) ok=0; seen|=1u<<perm[k]; }
    if(ok){ be++; for(int a=0;a<m;a++) for(int b=a+1;b<m;b++) bN[perm[a]][perm[b]]++; }
    int i=m-2; while(i>=0 && perm[i]>perm[i+1]) i--; if(i<0) break; int j=m-1; while(perm[j]<perm[i]) j--;
    int t=perm[i];perm[i]=perm[j];perm[j]=t; for(int a=i+1,b=m-1;a<b;a++,b--){t=perm[a];perm[a]=perm[b];perm[b]=t;} } }
static int CTRL=0;
static int brute_cmp(int m,const uint32_t*dn){ static u128 N[MAXN][MAXN]; uint32_t up[MAXN]; ups(m,dn,up);
  u128 e=count(m,dn,N);
  if(CTRL){ /* firing control: brute force on P with every relation dropped from its highest element (a different poset) */
    uint32_t d2[MAXN]; memcpy(d2,dn,sizeof(uint32_t)*m); int t=-1; for(int i=0;i<m;i++) if(dn[i] && (t<0||pc(dn[i])>pc(dn[t]))) t=i; if(t>=0) d2[t]=0; /* still transitive: t becomes minimal */
    brute(m,d2); } else brute(m,dn); if(e!=be) return 1;
  for(int x=0;x<m;x++) for(int y=0;y<m;y++){ if(x==y) continue; int inc=!((dn[x]|up[x])>>y&1); if(inc && N[x][y]!=bN[x][y]) return 1; } return 0; }

/* ---------------- census ---------------- */
static long LA=1, LB=3;
static int bal(u128 N,u128 e){ return (u128)LB*N >= (u128)LA*e && (u128)LB*N <= (u128)(LB-LA)*e; }
static int connected(int n,const uint32_t*dn,const uint32_t*up){ uint32_t all=(1u<<n)-1, seen=1, fr=1;
  while(fr){ int v=__builtin_ctz(fr); fr&=fr-1; uint32_t nb=all&~(dn[v]|up[v]|1u<<v)&~seen; seen|=nb; fr|=nb; } return seen==all; }

int main(int argc,char**argv){
  if(argc>=2 && !strcmp(argv[1],"gen")){
    int D=atoi(argv[2]), NMAX=atoi(argv[3]); const char*pre=argv[4]; D_=D;
    store *prev=malloc(sizeof(store)); st_init(prev,1); uint32_t z[1]={0}; st_add(prev,z);
    printf("gen D=%d n=1 classes=1\n",D);
    for(int n=2;n<=NMAX;n++){ store*s=malloc(sizeof(store)); st_init(s,n); cur_=s; candidates=0; isochecks=0; parn_=n-1;
      for(long i=0;i<prev->cnt;i++){ for(int k=0;k<n-1;k++) par_[k]=prev->dn[i*(n-1)+k]; ideals(n-1,par_,addmin); }
      printf("gen D=%d n=%d from=%ld candidates=%ld isotests=%ld classes=%ld\n",D,n,prev->cnt,candidates,isochecks,s->cnt); fflush(stdout);
      char fn[512]; snprintf(fn,sizeof fn,"%s%d.txt",pre,n); writest(s,fn);
      free(prev->dn); free(prev->inv); free(prev->next); free(prev->head); free(prev); prev=s; }
    return 0; }
  if(argc>=2 && !strcmp(argv[1],"brute")){
    int m=atoi(argv[2]), T=atoi(argv[3]); CTRL=(argc>4); srand(12345+m); int bad=0, tests=0;
    for(int t=0;t<T;t++){ uint32_t dn[MAXN]; /* random poset: random DAG on 0..m-1 then transitive closure */
      for(int i=0;i<m;i++){ dn[i]=0; for(int j=0;j<i;j++) if(rand()%100 < 25) dn[i]|=1u<<j; }
      for(int i=0;i<m;i++) for(int j=0;j<i;j++) if(dn[i]>>j&1) dn[i]|=dn[j];
      /* random relabel */ int p[MAXN]; for(int i=0;i<m;i++) p[i]=i; for(int i=m-1;i>0;i--){int j=rand()%(i+1),q=p[i];p[i]=p[j];p[j]=q;}
      uint32_t d2[MAXN]; for(int i=0;i<m;i++){ uint32_t d=0; for(int j=0;j<m;j++) if(dn[i]>>j&1) d|=1u<<p[j]; d2[p[i]]=d; }
      tests++; bad+=brute_cmp(m,d2);
      for(int v=0;v<m;v++){ uint32_t d3[MAXN]; int o[MAXN]; delete_v(m,d2,v,d3,o); tests++; bad+=brute_cmp(m-1,d3); } }
    printf("brute%s m=%d: %d posets (P and every P-v) compared, mismatches=%d%s\n",CTRL?" CONTROL (brute runs on a modified poset)":"",m,tests,bad,CTRL?(bad?" FIRES":" DOES NOT FIRE"):""); return 0; }
  if(argc>=2 && !strcmp(argv[1],"scan")){
    FILE*f=fopen(argv[2],"r"); long start=atol(argv[3]), stride=atol(argv[4]); int indec=0;
    int ai=5; if(argc>ai && !strcmp(argv[ai],"indec")){indec=1;ai++;} if(argc>ai+1){ LA=atol(argv[ai]); LB=atol(argv[ai+1]); }
    long idx=-1, nP=0, fail_exists=0, fail_every=0, fail_minrange=0, fail_some_minrange=0, decomp=0, decomp_mismatch=0, indec_mismatch=0;
    long rchecks=0, rviol=0, rctrl=0; long double worst1=0; char w1[512]="";
    long double worstR[MAXN]={0};
    /* worst margin: min over P of max over (v,pair) of min(d_P,d_{P-v}); d as fraction num/den */
    int have_wm=0; u128 wmn=0, wmd=1; char wmP[256]=""; int have_wc=0; u128 wcn=0, wcd=1; long canon_neg=0; char wcP[256]="";
    int n; while(fscanf(f,"%d",&n)==1){ uint32_t dn[MAXN]; for(int k=0;k<n;k++){ unsigned x; if(fscanf(f,"%x",&x)!=1) return 2; dn[k]=x; }
      idx++; if(idx%stride!=start) continue;
      uint32_t up[MAXN]; ups(n,dn,up); int npairs=0; for(int v=0;v<n;v++) npairs+=piv(n,dn,up,v); if(npairs==0) continue; /* chain */
      int con=connected(n,dn,up); if(indec && !con) continue; if(n<3) continue;
      nP++;
      static u128 N[MAXN][MAXN], N2[MAXN][MAXN]; u128 e=count(n,dn,N);
      int balP=0; for(int x=0;x<n;x++) for(int y=x+1;y<n;y++) if(!((dn[x]|up[x])>>y&1) && bal(N[x][y],e)) balP=1;
      int minpi=n; for(int v=0;v<n;v++){int p=piv(n,dn,up,v); if(p<minpi) minpi=p;}
      int anyw=0, allw=1, allmin=1, somemin=0; int have_m=0; u128 mn=0, md=1; int have_c=0, cfail=0; u128 cn_=0, cd_=1;
      for(int v=0;v<n;v++){ uint32_t d2[MAXN]; int o[MAXN]; delete_v(n,dn,v,d2,o); u128 e2=count(n-1,d2,N2);
        int pv=piv(n,dn,up,v), r=pv+1, works=0; int have_v=0; u128 vn=0, vd=1;
        for(int x=0;x<n;x++) for(int y=x+1;y<n;y++){ if(x==v||y==v) continue; if((dn[x]|up[x])>>y&1) continue;
          u128 a=N[x][y], a2=N2[o[x]][o[y]];
          int b1=bal(a,e), b2=bal(a2,e2); if(b1&&b2) works=1;
          /* Lemma R window, integer: a/e <= r a2/(r a2 + e2 - a2)  and  a/e >= a2/(a2 + r (e2-a2)) */
          rchecks++;
          if(!( a*((u128)r*a2+e2-a2) <= (u128)r*a2*e && a*(a2+(u128)r*(e2-a2)) >= a2*e )) rviol++;
          { int rc=pv; if(!( a*((u128)rc*a2+e2-a2) <= (u128)rc*a2*e && a*(a2+(u128)rc*(e2-a2)) >= a2*e )) rctrl++; }
          long double dp=fabsl((long double)a/(long double)e-(long double)a2/(long double)e2);
          if(pv<MAXN && dp>worstR[pv]) worstR[pv]=dp;
          if(pv==1 && dp>worst1){ worst1=dp; i128 num=(i128)a*(i128)e2-(i128)a2*(i128)e; if(num<0) num=-num; u128 den=e*e2, g=gcd128((u128)num,den);
            char s1[64],s2[64]; pr128(s1,(u128)num/g); pr128(s2,den/g); int L=snprintf(w1,sizeof w1,"%s/%s v=%d x=%d y=%d P=%d",s1,s2,v,x,y,n); for(int k=0;k<n;k++) L+=snprintf(w1+L,sizeof w1-L," %x",dn[k]); }
          if(b1&&b2 && LA==1&&LB==3){ /* margin of this (v,pair) */
            u128 d1n = 3*a>=e ? 3*a-e : 0; if(2*e-3*a < d1n) d1n=2*e-3*a; u128 d1d=3*e;
            u128 d2n = 3*a2>=e2 ? 3*a2-e2 : 0; if(2*e2-3*a2 < d2n) d2n=2*e2-3*a2; u128 d2d=3*e2;
            u128 cn=d1n, cd=d1d; if(d2n*cd < cn*d2d){cn=d2n;cd=d2d;}
            if(!have_m || cn*md > mn*cd){ mn=cn; md=cd; have_m=1; }
            if(!have_v || cn*vd > vn*cd){ vn=cn; vd=cd; have_v=1; } } }
        if(pv==minpi){ if(!have_v) cfail=1; else if(!have_c || vn*cd_ < cn_*vd){ cn_=vn; cd_=vd; have_c=1; } }
        if(works) anyw=1; else allw=0;
        if(pv==minpi){ if(!works) allmin=0; else somemin=1; } }
      if(!anyw){ fail_exists++; printf("FAIL exists-v:"); for(int k=0;k<n;k++) printf(" %x",dn[k]); printf("\n"); }
      if(!allw) fail_every++; if(!allmin){ fail_minrange++; printf("FAIL every-min-range-v: %d",n); for(int k=0;k<n;k++) printf(" %x",dn[k]); printf("\n"); }
      if(!somemin) fail_some_minrange++;
      if(!con){ decomp++; if(anyw!=balP) decomp_mismatch++; } else if(anyw!=balP) indec_mismatch++;
      if(cfail) canon_neg++; else if(have_c && (!have_wc || cn_*wcd < wcn*cd_)){ wcn=cn_; wcd=cd_; have_wc=1; int L=snprintf(wcP,sizeof wcP,"%d",n); for(int k=0;k<n;k++) L+=snprintf(wcP+L,sizeof wcP-L," %x",dn[k]); }
      if(have_m && (!have_wm || mn*wmd < wmn*md)){ wmn=mn; wmd=md; have_wm=1; int L=snprintf(wmP,sizeof wmP,"%d",n); for(int k=0;k<n;k++) L+=snprintf(wmP+L,sizeof wmP-L," %x",dn[k]); }
    }
    char s1[64],s2[64]; u128 g=have_wm?gcd128(wmn,wmd):1; pr128(s1,wmn/g); pr128(s2,wmd/g);
    printf("AGG file=%s part=%ld/%ld indec=%d lo=%ld/%ld posets=%ld exists_v_fail=%ld every_v_fail=%ld every_minrange_fail=%ld some_minrange_fail=%ld decomposable=%ld decomp_equiv_mismatch=%ld indec_equiv_mismatch=%ld lemmaR_checks=%ld lemmaR_viol=%ld lemmaR_ctrl_viol=%ld worst_margin=%s/%s at %s\n",
      argv[2],start,stride,indec,LA,LB,nP,fail_exists,fail_every,fail_minrange,fail_some_minrange,decomp,decomp_mismatch,indec_mismatch,rchecks,rviol,rctrl,s1,s2,wmP);
    { u128 g2=have_wc?gcd128(wcn,wcd):1; char t1[64],t2[64]; pr128(t1,wcn/g2); pr128(t2,wcd/g2); printf("AGGC canonical_worst_margin=%s/%s (over P where every min-range v works) posets_where_some_min_range_v_fails=%ld at %s\n",t1,t2,canon_neg,wcP); }
    printf("AGGR maxdp_pi1=%.10Lf witness %s\n",worst1,w1);
    printf("AGGR maxdp_by_pi:"); for(int p=1;p<8;p++) printf(" pi%d=%.6Lf",p,worstR[p]); printf("\n");
    return 0; }
  fprintf(stderr,"usage\n"); return 1; }
