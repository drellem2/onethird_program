/* pcert.c (mg-6b81) -- KSBFT-M instruments.  Reuses mg-eedd's audited generator, canonical form
 * and exact __int128 linear-extension counter verbatim, by #including onept.c (its main() is
 * renamed; every onept mode stays reachable through "onept ...").
 *
 * MODES
 *   onept ARGS...                 pass through to onept.c (gen / scan / fib / brute).
 *   cert FILE START STRIDE D      PREFIX CERTIFICATE (Theorem 2.2 of docs/KSBFT-M-margin-induction.md).
 *        For every class Q in FILE (size t, range <= D) and every s = 2..t-D:
 *          J ranges over the order ideals of Q of size s, K = intersection of those J;
 *          rm(Q,s) = max over incomparable {x,y} in K of  min over J of  dist(p_J(x<y), [1/3,2/3])
 *          (dist >= 0 iff balanced; exact fractions).  Q is CERTIFIED if rm(Q,s) >= 0 for some s.
 *        Q is flagged CUT if it has a strong cut (an ideal I, 1 <= |I| <= t-2D+1, with I < Q\I
 *        elementwise); such a Q is never an ideal of an indecomposable P in Pi_D (Lemma 2.4).
 *   decay FILE START STRIDE       transport error |p_P - p_{P-v}| against the distance, in the
 *        incomparability graph G(P), from v to the pair; indecomposable non-chains only.
 *   delta FILE START STRIDE THR   delta(P) - 1/3 on indecomposable non-chains; prints every P with
 *        delta(P) - 1/3 < THR (a fraction a/b), and the worst per range.
 *
 * Decisions are exact integers.  Doubles appear only in printed summaries.
 */
#define main onept_main
#include "../ksbft_one_pt/onept.c"
#undef main

static void setup_up(void){
  for(int i=0;i<n;i++) upm_[i]=0;
  for(int j=0;j<n;j++) for(int i=0;i<n;i++) if(dn[j]>>i&1) upm_[i]|=1u<<j;
}
static int read_poset(FILE *fi, uint32_t *d){
  int nn; if(fscanf(fi,"%d",&nn)!=1) return 0;
  for(int i=0;i<nn;i++){ unsigned x; if(fscanf(fi,"%x",&x)!=1) return -1; d[i]=x; } return nn;
}
static void print_frac(frac f){ printf("%lld/%lld", (long long)f.num, (long long)f.den); }
static frac freduce(frac f){ i128 a=f.num<0?-f.num:f.num, b=f.den; while(b){ i128 t=a%b; a=b; b=t; } if(a>1){ f.num/=a; f.den/=a; } return f; }

/* ------------------------------------------------------------------ cert */
#define MAXID 20000
static uint32_t idl[MAXID]; static int nidl;
static void all_ideals(uint32_t U){ /* every order ideal of the induced poset on U, BFS by size */
  curstamp++; nidl=0; idl[nidl++]=0; stamp[0]=curstamp;
  for(int q=0;q<nidl;q++){ uint32_t I=idl[q]; uint32_t av=U&~I;
    while(av){ int x=__builtin_ctz(av); av&=av-1;
      if((dn[x]&U&~I)==0){ uint32_t J=I|1u<<x; if(stamp[J]!=curstamp){ stamp[J]=curstamp;
          if(nidl>=MAXID){ fprintf(stderr,"MAXID\n"); exit(3);} idl[nidl++]=J; } } } }
}
static long c_tot[MAXN+1], c_cut[MAXN+1], c_fail[MAXN+1], c_failcut[MAXN+1];
static long c_spass[MAXN+1][MAXN+1]; /* [t][s]: #non-CUT Q certified at this s */
static long c_sbest[MAXN+1][MAXN+1]; /* [t][s]: #non-CUT Q whose largest certifying s is s */
static frac c_worst[MAXN+1]; static int c_hw[MAXN+1]; static uint32_t c_wp[MAXN+1][MAXN];
static frac c_worst_s[MAXN+1][MAXN+1]; static int c_hws[MAXN+1][MAXN+1];
static int c_printed;

static void cert_one(int D){
  int t=n; if(range_of(dn,n)>D) return; /* input files below n=9 hold every class */
  setup_up();
  uint32_t full=(1u<<t)-1;
  uint32_t inc[MAXN]; for(int i=0;i<t;i++) inc[i]=full&~dn[i]&~upm_[i]&~(1u<<i);
  all_ideals(full);
  int cut=0;
  for(int q=0;q<nidl&&!cut;q++){ uint32_t I=idl[q]; int k=__builtin_popcount(I);
    if(k<1 || k>t-2*D+1) continue;
    int ok=1; for(int j=0;j<t&&ok;j++) if(!(I>>j&1) && (dn[j]&I)!=I) ok=0;
    if(ok) cut=1; }
  c_tot[t]++; if(cut) c_cut[t]++;
  frac best={-1000000,1}; int hb=0, sbest=-1;
  static u128 cnt[MAXN][MAXN];
  for(int s=t-D;s>=2;s--){
    uint32_t K=full; int nj=0;
    for(int q=0;q<nidl;q++) if(__builtin_popcount(idl[q])==s){ K&=idl[q]; nj++; }
    if(!nj) continue;
    /* pairs in K */
    int px[MAXN*MAXN], py[MAXN*MAXN], np=0;
    for(int x=0;x<t;x++) if(K>>x&1) for(int y=x+1;y<t;y++) if((K>>y&1)&&(inc[x]>>y&1)){ px[np]=x; py[np]=y; np++; }
    if(!np){ continue; }
    frac mn[MAXN*MAXN]; int alive[MAXN*MAXN]; for(int p=0;p<np;p++){ mn[p].num=1000000; mn[p].den=1; alive[p]=1; }
    int nalive=np;
    for(int q=0;q<nidl && nalive;q++) if(__builtin_popcount(idl[q])==s){
      uint32_t J=idl[q]; u128 e=lecount(J,cnt);
      for(int p=0;p<np;p++) if(alive[p]){ frac d=dist(cnt[px[p]][py[p]],e); if(fcmp(d,mn[p])<0) mn[p]=d; }
    }
    frac rm={-1000000,1}; int h=0;
    for(int p=0;p<np;p++) if(!h||fcmp(mn[p],rm)>0){ rm=mn[p]; h=1; }
    if(!cut){ if(rm.num>=0) c_spass[t][s]++;
      if(!c_hws[t][s]||fcmp(rm,c_worst_s[t][s])<0){ c_worst_s[t][s]=rm; c_hws[t][s]=1; } }
    if(rm.num>=0 && sbest<0) sbest=s;
    if(!hb||fcmp(rm,best)>0){ best=rm; hb=1; }
  }
  int pass = hb && best.num>=0;
  if(!pass){ if(cut) c_failcut[t]++; else { c_fail[t]++;
      if(c_printed<20){ c_printed++; printf("FAIL (no certificate, not CUT) Q="); print_poset(); printf(" best rm=%.6f\n", hb?fd(best):-1.0); } } }
  if(!cut){ if(sbest>=0) c_sbest[t][sbest]++;
    if(!c_hw[t]||fcmp(best,c_worst[t])<0){ c_worst[t]=best; c_hw[t]=1; memcpy(c_wp[t],dn,sizeof(uint32_t)*t); } }
}

static int mode_cert(const char *file,long start,long stride,int D){
  FILE *fi=fopen(file,"r"); if(!fi){perror(file);return 1;}
  uint32_t d[MAXN]; int nn; long idx=0; int alloc=0;
  while((nn=read_poset(fi,d))>0){
    if(!alloc){ alloc_dp(nn); alloc=1; }
    if(idx%stride==start){ n=nn; memcpy(dn,d,sizeof(uint32_t)*n); cert_one(D); }
    idx++;
  }
  fclose(fi);
  for(int t=0;t<=MAXN;t++) if(c_tot[t]){
    printf("AGG CT %d %ld %ld %ld %ld\n",t,c_tot[t],c_cut[t],c_fail[t],c_failcut[t]);
    if(c_hw[t]){ printf("AGG CW %d %lld %lld %d",t,(long long)c_worst[t].num,(long long)c_worst[t].den,t); for(int i=0;i<t;i++) printf(" %x",c_wp[t][i]); printf("\n"); }
    for(int s=0;s<=MAXN;s++){ if(c_hws[t][s]) printf("AGG CS %d %d %ld %lld %lld\n",t,s,c_spass[t][s],(long long)c_worst_s[t][s].num,(long long)c_worst_s[t][s].den);
      if(c_sbest[t][s]) printf("AGG CB %d %d %ld\n",t,s,c_sbest[t][s]); }
  }
  return 0;
}

/* ------------------------------------------------------------------ decay */
#define MAXDIST 16
static frac dk_max[MAXN+1][MAXDIST+1]; static int dk_h[MAXN+1][MAXDIST+1]; static long dk_cnt[MAXN+1][MAXDIST+1];
/* the transport a margin-carrying induction would use: best margin (min of the two dists) among
   pairs at distance >= d from v, minimised over (P, v of minimal range) */
static frac dk_tm[MAXDIST+1]; static int dk_htm[MAXDIST+1]; static long dk_tmn[MAXDIST+1];
static long dk_P;
static void decay_one(void){
  setup_up(); uint32_t full=(1u<<n)-1; uint32_t inc[MAXN]; int pv[MAXN], pi=0;
  for(int i=0;i<n;i++){ inc[i]=full&~dn[i]&~upm_[i]&~(1u<<i); pv[i]=__builtin_popcount(inc[i]); if(pv[i]>pi) pi=pv[i]; }
  if(pi==0||n<3||!indecomposable(full)) return;
  dk_P++;
  int pmin=n; for(int i=0;i<n;i++) if(pv[i]<pmin) pmin=pv[i];
  static u128 cP[MAXN][MAXN], cV[MAXN][MAXN];
  u128 eP=lecount(full,cP);
  for(int v=0;v<n;v++){
    int dd[MAXN]; for(int i=0;i<n;i++) dd[i]=-1; dd[v]=0; int qq[MAXN],h=0,tl=0; qq[tl++]=v;
    while(h<tl){ int a=qq[h++]; for(int b=0;b<n;b++) if((inc[a]>>b&1)&&dd[b]<0){ dd[b]=dd[a]+1; qq[tl++]=b; } }
    u128 eV=lecount(full&~(1u<<v),cV);
    frac bestm[MAXDIST+1]; int hbm[MAXDIST+1]; for(int k=0;k<=MAXDIST;k++) hbm[k]=0;
    for(int x=0;x<n;x++) if(x!=v) for(int y=x+1;y<n;y++) if(y!=v&&(inc[x]>>y&1)){
      int dxy = dd[x]<dd[y]?dd[x]:dd[y]; if(dxy>MAXDIST) dxy=MAXDIST;
      i128 l=(i128)(cP[x][y]*eV), r2=(i128)(cV[x][y]*eP); frac df={l>r2?l-r2:r2-l,(i128)(eP*eV)};
      int pvv=pv[v];
      if(!dk_h[pvv][dxy]||fcmp(df,dk_max[pvv][dxy])>0){ dk_max[pvv][dxy]=df; dk_h[pvv][dxy]=1; }
      dk_cnt[pvv][dxy]++;
      frac m=fmin_(dist(cP[x][y],eP),dist(cV[x][y],eV));
      for(int k=1;k<=dxy;k++) if(!hbm[k]||fcmp(m,bestm[k])>0){ bestm[k]=m; hbm[k]=1; }
    }
    if(pv[v]==pmin) for(int k=1;k<=MAXDIST;k++) if(hbm[k]){ dk_tmn[k]++;
        if(!dk_htm[k]||fcmp(bestm[k],dk_tm[k])<0){ dk_tm[k]=bestm[k]; dk_htm[k]=1; } }
  }
}
static int mode_decay(const char *file,long start,long stride){
  FILE *fi=fopen(file,"r"); if(!fi){perror(file);return 1;}
  uint32_t d[MAXN]; int nn; long idx=0; int alloc=0;
  while((nn=read_poset(fi,d))>0){
    if(!alloc){ alloc_dp(nn); alloc=1; }
    if(idx%stride==start){ n=nn; memcpy(dn,d,sizeof(uint32_t)*n); decay_one(); }
    idx++;
  }
  fclose(fi);
  printf("AGG DP %ld\n",dk_P);
  for(int p=0;p<=MAXN;p++) for(int k=0;k<=MAXDIST;k++) if(dk_h[p][k]) printf("AGG DM %d %d %ld %lld %lld\n",p,k,dk_cnt[p][k],(long long)dk_max[p][k].num,(long long)dk_max[p][k].den);
  for(int k=1;k<=MAXDIST;k++) if(dk_htm[k]) printf("AGG DT %d %ld %lld %lld\n",k,dk_tmn[k],(long long)dk_tm[k].num,(long long)dk_tm[k].den);
  return 0;
}

/* ------------------------------------------------------------------ delta */
static long dl_tot[MAXN+1]; static frac dl_w[MAXN+1]; static int dl_h[MAXN+1]; static uint32_t dl_wp[MAXN+1][MAXN];
static long dl_below[MAXN+1];
static long THR_A=1, THR_B=50;
static void delta_one(void){
  setup_up(); uint32_t full=(1u<<n)-1; uint32_t inc[MAXN]; int pi=0;
  for(int i=0;i<n;i++){ inc[i]=full&~dn[i]&~upm_[i]&~(1u<<i); int c=__builtin_popcount(inc[i]); if(c>pi) pi=c; }
  if(pi==0||n<3||!indecomposable(full)) return;
  static u128 cP[MAXN][MAXN]; u128 e=lecount(full,cP);
  frac b={-1000000,1}; int h=0;
  for(int x=0;x<n;x++) for(int y=x+1;y<n;y++) if(inc[x]>>y&1){ frac d=dist(cP[x][y],e); if(!h||fcmp(d,b)>0){b=d;h=1;} }
  dl_tot[pi]++;
  if(!dl_h[pi]||fcmp(b,dl_w[pi])<0){ dl_w[pi]=b; dl_h[pi]=1; memcpy(dl_wp[pi],dn,sizeof(uint32_t)*n); }
  frac thr={(i128)THR_A,(i128)THR_B};
  if(fcmp(b,thr)<0){ dl_below[pi]++; frac r=freduce(b); printf("LOW pi=%d margin=",pi); print_frac(r); printf(" = %.6f P=",fd(b)); print_poset(); printf("\n"); }
}
static int mode_delta(const char *file,long start,long stride){
  FILE *fi=fopen(file,"r"); if(!fi){perror(file);return 1;}
  uint32_t d[MAXN]; int nn; long idx=0; int alloc=0;
  while((nn=read_poset(fi,d))>0){
    if(!alloc){ alloc_dp(nn); alloc=1; }
    if(idx%stride==start){ n=nn; memcpy(dn,d,sizeof(uint32_t)*n); delta_one(); }
    idx++;
  }
  fclose(fi);
  for(int p=0;p<=MAXN;p++) if(dl_tot[p]){ printf("AGG LT %d %ld %ld %lld %lld %d",p,dl_tot[p],dl_below[p],(long long)dl_w[p].num,(long long)dl_w[p].den,n); for(int i=0;i<n;i++) printf(" %x",dl_wp[p][i]); printf("\n"); }
  return 0;
}


/* ------------------------------------------------------------------ gencut: pruned generator */
/* is Q (global dn, size n) CUT for prefix length n and range D ? */
static int is_cut(int D){
  setup_up(); uint32_t full=(1u<<n)-1; all_ideals(full);
  for(int q=0;q<nidl;q++){ uint32_t I=idl[q]; int k=__builtin_popcount(I);
    if(k<1 || k>n-2*D+1) continue;
    int ok=1; for(int j=0;j<n&&ok;j++) if(!(I>>j&1) && (dn[j]&I)!=I) ok=0;
    if(ok) return 1; }
  return 0;
}
static int mode_gencut(const char *in,const char *out,int D){
  FILE *fi=NULL; int m; long cnt=0, cand=0, kept=0;
  uint32_t q[MAXN]; int nn=-1;
  if(strcmp(in,"-")){ fi=fopen(in,"r"); if(!fi){perror(in);return 1;} }
  int alloced=0;
  for(;;){
    if(fi){ if(fscanf(fi,"%d",&m)!=1) break; for(int i=0;i<m;i++){ unsigned x; if(fscanf(fi,"%x",&x)!=1) return 2; q[i]=x; } }
    else { if(cnt) break; m=0; }
    cnt++; nn=m+1; uint32_t full=(1u<<m)-1;
    if(!alloced){ alloc_dp(nn); alloced=1; }
    /* ideals of q: enumerate through the BFS helper on q */
    n=m; memcpy(dn,q,sizeof(uint32_t)*m); all_ideals(full);
    int nI=nidl; static uint32_t Is[MAXID]; memcpy(Is,idl,sizeof(uint32_t)*nI);
    for(int a=0;a<nI;a++){ uint32_t d[MAXN]; memcpy(d,q,sizeof(uint32_t)*m); d[m]=Is[a]; cand++;
      if(range_of(d,nn)>D) continue;
      n=nn; memcpy(dn,d,sizeof(uint32_t)*nn); if(is_cut(D)) continue;
      uint32_t k[MAXN]; canon(d,nn,k); if(insert(k,nn)) kept++; }
  }
  if(fi) fclose(fi);
  FILE *fo=fopen(out,"w"); if(!fo){perror(out);return 1;}
  for(long s=0;s<nstore;s++){ fprintf(fo,"%d",nn); for(int i=0;i<nn;i++) fprintf(fo," %x",store[s*nn+i]); fprintf(fo,"\n"); }
  fclose(fo);
  printf("gencut n=%d D=%d from %ld classes: candidates=%ld nonCUT-classes=%ld\n",nn,D,cnt,cand,nstore);
  return 0;
}

/* ------------------------------------------------------------------ e2e: the theorem, end to end */
/* For every indecomposable P in FILE (size > t, range <= D): take EVERY ideal Q of size t, find the
   certificate of Q at s = t - D + OFF (OFF = 0 is Lemma B's s; OFF = 1 is a firing control that
   violates Lemma B), and check (a) mixture bracket min_J p_J <= p_P <= max_J p_J for every pair in
   K, (b) the certifying pair is balanced in P.  Counts violations. */
static long e_P, e_Q, e_pairs, e_brk, e_cert, e_certbad, e_nocert, e_nocert_cut;
static void e2e_one(int t,int D,int off){
  setup_up(); uint32_t full=(1u<<n)-1; uint32_t inc[MAXN]; int pi=0;
  for(int i=0;i<n;i++){ inc[i]=full&~dn[i]&~upm_[i]&~(1u<<i); int c=__builtin_popcount(inc[i]); if(c>pi) pi=c; }
  if(pi==0 || pi>D || n<=t || !indecomposable(full)) return;
  e_P++;
  static u128 cP[MAXN][MAXN], cJ[MAXN][MAXN]; u128 eP=lecount(full,cP);
  all_ideals(full); int nI=nidl; static uint32_t Is[MAXID]; memcpy(Is,idl,sizeof(uint32_t)*nI);
  int s=t-D+off;
  for(int a=0;a<nI;a++) if(__builtin_popcount(Is[a])==t){
    uint32_t Q=Is[a]; e_Q++;
    /* size-s ideals of Q = ideals of P of size s contained in Q */
    uint32_t Js[MAXID]; int nj=0; uint32_t K=Q;
    for(int b=0;b<nI;b++) if(__builtin_popcount(Is[b])==s && (Is[b]&~Q)==0){ Js[nj++]=Is[b]; K&=Is[b]; }
    int px[MAXN*MAXN],py[MAXN*MAXN],np=0;
    for(int x=0;x<n;x++) if(K>>x&1) for(int y=x+1;y<n;y++) if((K>>y&1)&&(inc[x]>>y&1)){px[np]=x;py[np]=y;np++;}
    /* per pair: min and max of p_J as fractions N/e, and min dist */
    u128 loN[MAXN*MAXN],loE[MAXN*MAXN],hiN[MAXN*MAXN],hiE[MAXN*MAXN]; frac md[MAXN*MAXN];
    for(int j=0;j<nj;j++){ u128 e=lecount(Js[j],cJ);
      for(int p=0;p<np;p++){ u128 N=cJ[px[p]][py[p]]; frac d=dist(N,e);
        if(j==0){ loN[p]=hiN[p]=N; loE[p]=hiE[p]=e; md[p]=d; }
        else { if(N*loE[p]<loN[p]*e){loN[p]=N;loE[p]=e;} if(N*hiE[p]>hiN[p]*e){hiN[p]=N;hiE[p]=e;} if(fcmp(d,md[p])<0) md[p]=d; } } }
    int best=-1;
    for(int p=0;p<np;p++){ e_pairs++; u128 N=cP[px[p]][py[p]];
      if(N*loE[p]<loN[p]*eP || N*hiE[p]>hiN[p]*eP) e_brk++;
      if(md[p].num>=0 && (best<0 || fcmp(md[p],md[best])>0)) best=p; }
    if(best>=0){ e_cert++; frac dP=dist(cP[px[best]][py[best]],eP); if(dP.num<0) e_certbad++; }
    else e_nocert++;
  }
}
static int mode_e2e(const char *file,long start,long stride,int t,int D,int off){
  FILE *fi=fopen(file,"r"); if(!fi){perror(file);return 1;}
  uint32_t d[MAXN]; int nn; long idx=0; int alloc=0;
  while((nn=read_poset(fi,d))>0){
    if(!alloc){ alloc_dp(nn); alloc=1; }
    if(idx%stride==start){ n=nn; memcpy(dn,d,sizeof(uint32_t)*n); e2e_one(t,D,off); }
    idx++;
  }
  fclose(fi);
  printf("AGG E %ld %ld %ld %ld %ld %ld %ld\n",e_P,e_Q,e_pairs,e_brk,e_cert,e_certbad,e_nocert);
  return 0;
}

int main(int argc,char **argv){
  if(argc>=2 && !strcmp(argv[1],"onept")) return onept_main(argc-1,argv+1);
  { const char *lo=getenv("ONEPT_LO"); if(lo && sscanf(lo,"%ld/%ld",&LO_A,&LO_B)!=2){ fprintf(stderr,"bad ONEPT_LO\n"); return 2; } }
  if(argc>=5 && !strcmp(argv[1],"gencut")) return mode_gencut(argv[2],argv[3],atoi(argv[4]));
  if(argc>=8 && !strcmp(argv[1],"e2e")) return mode_e2e(argv[2],atol(argv[3]),atol(argv[4]),atoi(argv[5]),atoi(argv[6]),atoi(argv[7]));
  if(argc>=6 && !strcmp(argv[1],"cert")) return mode_cert(argv[2],atol(argv[3]),atol(argv[4]),atoi(argv[5]));
  if(argc>=5 && !strcmp(argv[1],"decay")) return mode_decay(argv[2],atol(argv[3]),atol(argv[4]));
  if(argc>=5 && !strcmp(argv[1],"delta")){ if(argc>=6 && sscanf(argv[5],"%ld/%ld",&THR_A,&THR_B)!=2) return 2; return mode_delta(argv[2],atol(argv[3]),atol(argv[4])); }
  fprintf(stderr,"usage: see header\n"); return 2;
}
