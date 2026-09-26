/* indep_e60e.c (mg-e60e) -- INDEPENDENT audit census for docs/KSBFT-H-lemma-W.md.
 * Written without reading lemw.c's logic.  Differences from lemw.c by design:
 *  - posets generated as ALL transitive upper-triangular relation masks
 *    (i<j label order), not by appending down-sets; count must equal A006455;
 *  - all extension counts come from a down-set DP (fwd * bwd), never by
 *    listing extensions;
 *  - Lemma W is checked in its STATED form, with pi_N (not pi(P));
 *  - for every Case-D BFT triple the BFT quantities S, a1, a2, R are computed
 *    exactly and the inequalities the doc consumes are checked:
 *      (F-b)  9S+... chain result  S/2 >= C_BFT + R/(5+3sqrt5)
 *      (2.5)  R >= P[f(x)-f(y)>=2] + P[f(y)-f(z)>=2]
 *    plus the doc's sharpness claim (min ratio over Case-D pairs = 1/(pi+1)).
 * Usage: indep_e60e N [xy]   (N <= 7; a 2nd arg restricts Case-D ratios to the (x,y) side only)
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
typedef long long ll;
static int n; static unsigned pred[8], succ[8], inc[8];
static ll fwd[256], bwd[256];
static int lt(int a,int b){ return (pred[b]>>a)&1; }
/* count extensions in which the elements of seq[0..k-1] occupy consecutive
   positions in that order; seq[i] == -1 is a wildcard (any element). */
static ll pat(const int *seq,int k,unsigned S,int i){
  if(i==k) return bwd[S];
  ll t=0;
  for(int v=0;v<n;v++){ if((S>>v)&1) continue; if((pred[v]&~S)) continue;
    if(seq[i]==-1){ int used=0; for(int j=0;j<k;j++) if(seq[j]==v) used=1; if(used) continue; t+=pat(seq,k,S|1u<<v,i+1);} 
    else if(seq[i]==v) t+=pat(seq,k,S|1u<<v,i+1);
  }
  return t;
}
static ll patall(const int *seq,int k){ ll t=0; unsigned full=(1u<<n)-1;
  for(unsigned S=0;S<=full;S++){ if(!fwd[S]) continue; t+=fwd[S]*pat(seq,k,S,0);} return t; }
/* # extensions with a before b */
static ll before(int a,int b){ ll t=0; unsigned full=(1u<<n)-1;
  for(unsigned S=0;S<=full;S++){ if(!fwd[S]) continue; if((S>>a)&1||(S>>b)&1) continue; if(pred[a]&~S) continue; t+=fwd[S]*bwd[S|1u<<a]; }
  return t; }
/* stats */
static ll nposets,npairs,K0,K1,K2,K1m,nD,FB,F25;
static ll minN[9],minD[9],nDpi[9]; static ll minNd[9],minDd[9]; /* ratio as num/den */
static int wit[9][3]; static unsigned witP[9][8]; static ll mirrorhit[9];
static ll minW30n[9],minW30d[9];
static int better(ll a,ll b,ll c,ll d){ return a*d < c*b; } /* a/b < c/d */
static int onlyxy; int main(int argc,char**argv){ onlyxy = argc>2;
  n=atoi(argv[1]); int m=0; int I[64],J[64];
  for(int i=0;i<n;i++) for(int j=i+1;j<n;j++){ I[m]=i; J[m]=j; m++; }
  for(int p=0;p<9;p++){ minN[p]=2;minNd[p]=1;minD[p]=2;minDd[p]=1;minW30n[p]=2;minW30d[p]=1; }
  const double C=(5-sqrt(5))/10, K=5+3*sqrt(5);
  for(unsigned long mask=0; mask < (1ul<<m); mask++){
    int r[8][8]={{0}};
    for(int e=0;e<m;e++) if((mask>>e)&1) r[I[e]][J[e]]=1;
    int ok=1;
    for(int i=0;i<n&&ok;i++) for(int j=i+1;j<n&&ok;j++) if(r[i][j]) for(int k=j+1;k<n;k++) if(r[j][k]&&!r[i][k]){ok=0;break;}
    if(!ok) continue;
    nposets++;
    unsigned full=(1u<<n)-1;
    for(int v=0;v<n;v++){ pred[v]=succ[v]=0; }
    for(int i=0;i<n;i++) for(int j=0;j<n;j++) if(i<j&&r[i][j]){ pred[j]|=1u<<i; succ[i]|=1u<<j; }
    int piP=0; int pie[8];
    for(int v=0;v<n;v++){ inc[v]=full&~(pred[v]|succ[v]|1u<<v); pie[v]=__builtin_popcount(inc[v]); if(pie[v]>piP) piP=pie[v]; }
    if(piP==0) continue;
    for(unsigned S=0;S<=full;S++){ fwd[S]=0; bwd[S]=0; }
    fwd[0]=1;
    for(unsigned S=0;S<=full;S++){ if(!fwd[S]) continue; for(int v=0;v<n;v++) if(!((S>>v)&1) && !(pred[v]&~S)) fwd[S|1u<<v]+=fwd[S]; }
    bwd[full]=1;
    for(int S=(int)full-1;S>=0;S--){ ll t=0; for(int v=0;v<n;v++) if(!((S>>v)&1) && !(pred[v]&~(unsigned)S)) t+=bwd[S|1u<<v]; bwd[S]=t; }
    ll e=fwd[full]; if(e!=bwd[0]){ printf("DP MISMATCH\n"); return 1; }
    ll H[8]; for(int v=0;v<n;v++){ ll t=0; for(unsigned S=0;S<=full;S++){ if(!fwd[S]||((S>>v)&1)||(pred[v]&~S)) continue; t+=fwd[S]*bwd[S|1u<<v]*(ll)(__builtin_popcount(S)+1);} H[v]=t; }
    /* ordered incomparable pairs (X,Y), event Y before X */
    static ll cyx[8][8],gap2[8][8];
    for(int X=0;X<n;X++) for(int Y=0;Y<n;Y++){
      if(X==Y || !((inc[X]>>Y)&1)) continue;
      npairs++;
      ll cy=before(Y,X); int s1[2]={Y,X}; ll c1=patall(s1,2);
      int s2[3]={Y,-1,X}; ll c2=patall(s2,3);
      ll g2=cy-c1; cyx[X][Y]=cy; gap2[X][Y]=g2;
      int piN=-1; for(int w=0;w<n;w++){ if(w==X||w==Y) continue; if(lt(w,Y)||lt(X,w)) continue; if(pie[w]>piN) piN=pie[w]; }
      int Nne = piN>=0;
      if((g2>0)!=Nne) K0++;
      if(Nne){
        if(c1 > (ll)piN*c2) K1++;
        if(cy > (ll)(piN+1)*g2) K2++;
        if(c1 > (ll)(piN-1)*c2) K1m++;
        if(better(g2,cy,minN[piP],minNd[piP])){ minN[piP]=g2; minNd[piP]=cy; }
      }
    }
    /* Case-D BFT triples: x<z, x||y, y||z, H[x]<=H[y]<=H[z]<=H[x]+2e */
    for(int x=0;x<n;x++) for(int z=0;z<n;z++){ if(!lt(x,z)) continue;
      for(int y=0;y<n;y++){ if(!((inc[y]>>x)&1) || !((inc[y]>>z)&1)) continue;
        if(!(H[x]<=H[y] && H[y]<=H[z] && H[z]<=H[x]+2*e)) continue;
        nD++; nDpi[piP]++;
        ll p=cyx[x][y], pp=cyx[y][z];           /* p=P[y<x], p'=P[z<y] */
        int a11[3]={x,y,z}; ll a1=patall(a11,3);
        int a12[4]={x,y,-1,z}, a21[4]={x,-1,y,z}; ll a2=patall(a12,4)+patall(a21,4);
        ll S=p+pp, R=S-2*a1-a2;
        /* (F-b): S/2 >= C + R/K   (doubles of exact ints; tolerance 1e-12) */
        if((double)S/(2.0*e) < C + (double)R/(K*e) - 1e-12) FB++;
        /* (2.5) */
        if(R < gap2[x][y]+gap2[y][z]) F25++;
        /* ratios for pair (x,y) [gap f(x)-f(y)>=2 over p] and mirror (y,z) */
        for(int side=0;side<(onlyxy?1:2);side++){
          ll g= side? gap2[y][z]:gap2[x][y]; ll d= side? pp:p;
          if(g==0) continue; /* N empty: lemma's first alternative */
          if(better(g,d,minD[piP],minDd[piP])){ minD[piP]=g; minDd[piP]=d; wit[piP][0]=x;wit[piP][1]=y;wit[piP][2]=z; mirrorhit[piP]=side; for(int v=0;v<n;v++) witP[piP][v]=pred[v]; }
          if(10*p<=3*e && 10*pp<=3*e && better(g,d,minW30n[piP],minW30d[piP])){ minW30n[piP]=g; minW30d[piP]=d; }
        }
      }
    }
  }
  printf("N=%d posets=%lld (A006455: 3->7 4->40 5->357 6->4824 7->96428) ordered_incomparable_pairs=%lld caseD_BFT_triples=%lld\n",n,nposets,npairs,nD);
  printf("  K0 (gap>=2 possible <=> N nonempty) viol=%lld | K1 c1<=piN*c2 viol=%lld | K2 p<=(piN+1)P[gap>=2] viol=%lld | NEG CONTROL c1<=(piN-1)*c2 viol=%lld %s\n",K0,K1,K2,K1m,K1m>0?"FIRES":"SILENT!");
  printf("  BFT (F-b) S/2>=C_BFT+R/(5+3sqrt5) viol=%lld | (2.5) R>=gap(x,y)+gap(y,z) viol=%lld\n",FB,F25);
  for(int p=1;p<n;p++){
    if(minN[p]>minNd[p]) continue;
    printf("  pi(P)=%d  all pairs min P[gap>=2]/p = %lld/%lld = %.6f   1/(pi+1)=%.6f  %s\n",p,minN[p],minNd[p],(double)minN[p]/minNd[p],1.0/(p+1), minN[p]*(p+1)==minNd[p]?"EQUAL":"differs");
    if(minD[p]<=minDd[p]){ printf("           Case-D pairs (n=%lld) min = %lld/%lld = %.6f %s  witness (x,y,z)=(%d,%d,%d) side=%s pred-masks=[",nDpi[p],minD[p],minDd[p],(double)minD[p]/minDd[p],minD[p]*(p+1)==minDd[p]?"EQUAL 1/(pi+1)":"differs",wit[p][0],wit[p][1],wit[p][2],mirrorhit[p]?"(z,y)":"(x,y)"); for(int v=0;v<n;v++) printf("%s%u",v?",":"",witP[p][v]); printf("]\n"); }
    if(minW30n[p]<=minW30d[p]) printf("           Case-D with max(p,p')<=0.30: min = %lld/%lld = %.6f\n",minW30n[p],minW30d[p],(double)minW30n[p]/minW30d[p]);
  }
  return 0;
}
