/* nb.c (mg-cfba): exact pair laws over the ideal lattice, nested-balance statistics.
   Input: one poset per line, "n m_0 .. m_{n-1}" with m_i the strict DOWN-set bitmask (hex), transitively closed.
   Output per poset (one line):
     n e_approx delta deltaN nbal nbalN nnonnested flag soft
   deltaP = max over PRIMAL-nested pairs only (down-sets comparable); last column PNB / PNB_FAILS (exact)
   soft   = sum over nested pairs with min(p,1-p) > 1/3-0.02 of the excess (a smooth search objective only)
   delta  = max over incomparable pairs of min(p,1-p)           (1/3-2/3 holds iff delta >= 1/3)
   deltaN = max over NESTED incomparable pairs of min(p,1-p)    (Nested Balance holds iff deltaN >= 1/3)
   nested = down(a) subset down(b) or reverse, or up(a) subset up(b) or reverse.
   Balance tests are exact: 3B >= e and 3B <= 2e on __int128 counts.  With -v also prints every pair.
   Counts are __int128; the program aborts if e exceeds 2^125 (overflow guard via long double shadow). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef unsigned long long u64; typedef __int128 i128;
static int n; static u64 dn[64], up[64];
typedef struct { u64 *key; int *val; size_t cap, cnt; } HT;
static void ht_init(HT *h, size_t cap){ h->cap=cap; h->cnt=0; h->key=malloc(cap*8); h->val=malloc(cap*sizeof(int)); memset(h->val,-1,cap*sizeof(int)); }
static size_t hsh(u64 k,size_t cap){ k^=k>>33; k*=0xff51afd7ed558ccdULL; k^=k>>33; return k&(cap-1); }
static void ht_grow(HT *h);
static int ht_get(HT *h,u64 k){ size_t i=hsh(k,h->cap); while(h->val[i]>=0){ if(h->key[i]==k) return h->val[i]; i=(i+1)&(h->cap-1);} return -1; }
static void ht_put(HT *h,u64 k,int v){ if(2*(h->cnt+1)>h->cap) ht_grow(h); size_t i=hsh(k,h->cap); while(h->val[i]>=0){ if(h->key[i]==k){h->val[i]=v;return;} i=(i+1)&(h->cap-1);} h->key[i]=k; h->val[i]=v; h->cnt++; }
static void ht_grow(HT *h){ HT g; ht_init(&g,h->cap*2); for(size_t i=0;i<h->cap;i++) if(h->val[i]>=0) ht_put(&g,h->key[i],h->val[i]); free(h->key); free(h->val); *h=g; }
static u64 *ids; static size_t nid, capid; static i128 *N, *M; static long double *Nd;
int main(int argc,char**argv){
  int verbose = argc>1 && !strcmp(argv[1],"-v");
  char line[8192];
  static i128 B[64][64];
  while(fgets(line,sizeof line,stdin)){
    char *p=line; if(*p=='#'||*p=='\n') continue;
    n=strtol(p,&p,10); if(n<=0||n>63){ fprintf(stderr,"bad n\n"); return 2; }
    for(int i=0;i<n;i++) dn[i]=strtoull(p,&p,16);
    for(int i=0;i<n;i++){ up[i]=0; for(int j=0;j<n;j++) if(dn[j]>>i&1) up[i]|=1ULL<<j; }
    for(int i=0;i<n;i++) for(int j=0;j<n;j++) if(dn[i]>>j&1) if((dn[j]&~dn[i])) { fprintf(stderr,"not closed\n"); return 2; }
    u64 full = (n==64)?~0ULL:((1ULL<<n)-1);
    /* enumerate ideals by BFS (sizes increase) */
    HT h; ht_init(&h,1<<16); capid=1<<16; nid=0; ids=malloc(capid*8);
    ids[nid]=0; ht_put(&h,0,nid++);
    for(size_t q=0;q<nid;q++){ u64 I=ids[q];
      for(int x=0;x<n;x++) if(!(I>>x&1) && (dn[x]&~I)==0){ u64 J=I|1ULL<<x; if(ht_get(&h,J)<0){ if(nid==capid){capid*=2; ids=realloc(ids,capid*8);} ids[nid]=J; ht_put(&h,J,nid++);} } }
    N=calloc(nid,sizeof(i128)); M=calloc(nid,sizeof(i128)); Nd=calloc(nid,sizeof(long double));
    N[0]=1; Nd[0]=1;
    for(size_t q=0;q<nid;q++){ u64 I=ids[q];
      for(int x=0;x<n;x++) if(!(I>>x&1) && (dn[x]&~I)==0){ int t=ht_get(&h,I|1ULL<<x); N[t]+=N[q]; Nd[t]+=Nd[q]; } }
    int tf=ht_get(&h,full); if(Nd[tf]>4.0e37L){ fprintf(stderr,"overflow guard n=%d\n",n); return 3; }
    for(size_t q=nid;q-->0;){ u64 I=ids[q]; if(I==full){M[q]=1;continue;} i128 s=0;
      for(int x=0;x<n;x++) if(!(I>>x&1) && (dn[x]&~I)==0) s+=M[ht_get(&h,I|1ULL<<x)]; M[q]=s; }
    i128 e=N[tf];
    for(int a=0;a<n;a++) for(int b=0;b<n;b++) B[a][b]=0;
    for(size_t q=0;q<nid;q++){ u64 I=ids[q];
      for(int a=0;a<n;a++) if(!(I>>a&1) && (dn[a]&~I)==0){ i128 c=N[q]*M[ht_get(&h,I|1ULL<<a)]; u64 R=full&~I&~(1ULL<<a);
        while(R){ int b=__builtin_ctzll(R); R&=R-1; B[a][b]+=c; } } }
    double delta=0, deltaN=0, deltaP=0; int nbal=0,nbalN=0,nnon=0,nbalP=0; double soft=0;
    for(int a=0;a<n;a++) for(int b=a+1;b<n;b++){
      if((dn[a]>>b&1)||(dn[b]>>a&1)) continue;
      int nested = ((dn[a]&~dn[b])==0)||((dn[b]&~dn[a])==0)||((up[a]&~up[b])==0)||((up[b]&~up[a])==0);
      double pp=(double)((long double)B[a][b]/(long double)e); double m=pp<1-pp?pp:1-pp;
      int bal = 3*B[a][b]>=e && 3*B[a][b]<=2*e;
      if(!nested) nnon++;
      if(m>delta) delta=m; if(nested && m>deltaN) deltaN=m;
      int pnested = ((dn[a]&~dn[b])==0)||((dn[b]&~dn[a])==0); if(pnested && m>deltaP) deltaP=m;
      if(pnested && bal) nbalP++;
      nbal+=bal; if(bal&&nested) nbalN++;
      if(nested && m>1.0/3-0.02) soft+=m-(1.0/3-0.02);
      if(verbose) printf("  pair %d %d p=%.6f %s%s\n",a,b,pp,nested?"nested":"NONNESTED",bal?" BAL":"");
    }
    printf("%d %.6Le %.6f %.6f %d %d %d %s %.6f %.6f %s\n",n,(long double)Nd[tf],delta,deltaN,nbal,nbalN,nnon, nbalN? "NB":(nbal?"NB_FAILS":"CEX_1323"),soft,deltaP,nbalP?"PNB":"PNB_FAILS");
    fflush(stdout);
    free(N);free(M);free(Nd);free(ids);free(h.key);free(h.val);
  }
  return 0;
}
