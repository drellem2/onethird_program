# KSBFT-O: novelty of "every poset of range ≤ 7 has a 1/3-balanced pair" (mg-00c0)

Subject: the claim in mg-e8b4 (`docs/KSBFT-I-finite-state.md` §0 item 2). It is a computer proof that every finite non-chain poset of range π(P) ≤ 7 has an incomparable pair x ∥ y with 1/3 ≤ P[x<y] ≤ 2/3. Its audit, mg-9268, is in flight. **This file checks novelty only. It does not check correctness.**

Terminology: "k-thin" (BW92, Pec08) means every element is incomparable to at most k others, i.e. range π(P) ≤ k. KSBFT_v7 footnote 1 states this equivalence. Chan–Pak define k-thin as α(x)+β(x) > n−k with closed ideals, which gives the same condition.

## 0. Verdict

**NOT FOUND — as of 2026-09-26, no source states the 1/3–2/3 conjecture (or the Gold Partition Conjecture) for 7-thin posets or for any range bound above 6.**

- **Evidence that the frontier is 6.** Every source that lists known cases stops at Peczarski 2008 (6-thin). That includes three written in 2025–26:
  - the Chan–Pak survey (arXiv:2311.02743v2, Feb 2025);
  - Gupta (arXiv:2607.23926v2, Jul 2026);
  - KSBFT_v7 itself (Aires–Chan–Pak–Panova, 2026-09-25).

  KSBFT_v7 p.3 goes further: after citing BW92 (D ≤ 5) and Pec08 (D ≤ 6) it says "Unfortunately, their methods break down for larger D." Those authors are active specialists and wrote the leading survey, and their paper is dated the day before this search. So the gap was open, in their view, as of that date.
- **What could still exist.** It is not possible to prove a negative. The residual risk is:
  - an unpublished or non-indexed result;
  - something inside a paywalled text we could not read (Pec08 full text, BW92 full text, Brightwell 1999 survey, Peczarski's 2006 PhD thesis, the 2024 Springer chapter "On Partially Ordered Sets and the 1/3–2/3 Conjecture");
  - a paper posted in the last few days.

  None of these seems likely. Pec08 itself proves only the 6-thin case, which follows from its title and abstract.
- **What mg-e8b4 may say.** If the audit holds, it may say: "new: the first range not covered by BW92/Pec08". Two scope notes it should carry:
  1. Pec08 proves the **Gold Partition Conjecture** (GPC) for 6-thin posets, and GPC is **stronger** than 1/3–2/3. mg-e8b4 proves only 1/3–2/3 at D = 7. So its D ≤ 6 positive control reproduces the 1/3–2/3 *consequence* of Pec08, not Pec08 itself. GPC for 7-thin posets stays open.
  2. Gupta 2026 already covers range-7 posets with **n ≤ 14** (all posets up to 14 elements satisfy GPC). mg-e8b4 is new for range ≤ 7 posets with **n ≥ 15**, i.e. for every n. Its n-uniformity is exactly the part that no exhaustive-by-size census can give.

## 1. What is known (cited, each read at the source named)

| result | source | how I read it |
|---|---|---|
| 1/3–2/3 for 5-thin | Brightwell–Wright, SIAM J. Discrete Math. 5 (1992) 467–474 | abstract only (OpenAlex): "…the conjecture is established in the case where every element of the poset is incomparable with at most five others. **The proof involves the use of a computer to eliminate a large number of cases.**" |
| GPC (⇒ 1/3–2/3) for 6-thin | Peczarski, Order 25 (2008) 91–103 | abstract via Semantic Scholar/Springer snippet: "The GPC is proved in the case where every element of the poset is incomparable with at most six others and **the proof involves the extensive use of computers.**" Reference list via Crossref (§3). Full text paywalled (Springer 303 to login; OpenAlex `oa_status: closed`). |
| GPC for n ≤ 11 | Peczarski, Order 23 (2006) 89–95 | cited this way by Gupta, Olson–Sagan and Dolores-Cuenca–Guzmán-Sáenz–Kim |
| GPC for n ≤ 14 | Gupta, arXiv:2607.23926v2 (2026) | full text (arXiv PDF/HTML). The only mention of thin posets is "Peczarski proved the conjecture … for 6-thin posets [24, 23]". Nothing about range beyond 6. |
| survey list, Thm 13.2(8): "6-thin posets [Pec08] (a weaker 5-thin version was given in [BW92])" | Chan–Pak, arXiv:2311.02743v2 §13 (= "CP25 §11" in the EMS published numbering that KSBFT cites) | full text, §13.1 read in full |
| p.3: "for D ≤ 5, Brightwell and Wright … In [Pec08], Peczarski extended this result to D ≤ 6. Unfortunately, their methods break down for larger D." | KSBFT_v7 (`/Users/daniel/files/KSBFT_v7.pdf`) | full text (pdftotext); reference list checked (§2) |

## 2. Every search run

The instruments are arXiv's API over https, OpenAlex, Semantic Scholar, Crossref, web search, and direct reads of full text. The search terms are those the ticket asked for.

**arXiv API** (`export.arxiv.org/api/query`, all fields unless marked). Totals are as returned. Nothing relevant beyond the listed hits:
- `"gold partition"` → 2: 2607.23926 (Gupta), 2410.12494 (Dolores-Cuenca et al.). Both read (below).
- `"7-thin"` → 12. All are physics (La₃Ni₂O₇ thin films etc.). **0 relevant.**
- `"6-thin"` → 8 and `"5-thin"` → 7. **0 relevant.** This null is itself informative: BW92 and Pec08 are not on arXiv, so the phrase is not indexed there even for the known cases.
- `"thin posets"` / `"thin poset"` → 3. All are about the categorification sense of "thin". **0 relevant.**
- `"k-thin"` → 12. All are about thin trees or graph thinness. **0 relevant.**
- abs `"1/3-2/3"` → 87. The relevant hits (1107.5626, 1610.00809, 1706.04985, 1709.05753, 2005.09719, 2607.23926) all predate this work or are Gupta. None mentions range > 6.
- ti `"balanced pair"` → 18. Poset-relevant: 2002.11604 (greedy balanced pairs, N-free) and 1302.5967 (antimatroids). No thin result.
- abs `"balanced pairs" AND poset` → 1 (1706.04985).
- abs `"balance constant"` → 14. Poset-relevant: 2607.23926, 1811.01500, 1709.05753, 2005.09719.
- abs `Peczarski` → 3 (2607.23926, 2206.05597 on sorting lower bounds, 1811.01500). `au:Peczarski` → 4, all on sorting, Mastermind or Ulam's game. **Peczarski has posted nothing on thin posets on arXiv.**
- abs `"sorting probability"` → 8. Relevant: 2510.26134 (AK25b), 2005.13686 and 2005.08390 (CPP). No thin result.
- abs `"bounded range" AND poset` → 1 (unrelated).
- abs `"1/3" AND "linear extension"` → 10. Same set as the `"1/3-2/3"` query.
- abs `"linear extensions" AND cat:math.CO`, sorted newest first. I read the titles of every 2025–26 entry (23). Relevant: 2607.23926, 2510.26134, 2509.11549. Also 2607.10084 ("Relative Linear Extension Ratios"), 2607.06275 (equality in correlation inequalities) and 2511.11785, whose titles are unrelated to balance/thinness. None claims a thin/range result.
- ti `"infinite barrier"` → 2 (physics). **KSBFT itself is not on arXiv**, consistent with mg-3c5b's finding.
- **Instrument note.** A first run over plain `http://` returned 301 with an empty body, so every query printed nothing. I caught it with a positive control: `"gold partition"` must return Gupta, and did so only after switching to https with `-L`. All counts above are from the https run.

**Citation graph of Pec08** (DOI 10.1007/s11083-008-9081-9). Crossref gives `is-referenced-by-count` = 7.
- OpenAlex `cites:W2019922946` → 11 works:
  - Zaguia 2012 (N-free) and 2018/19 (forest);
  - Chan–Pak–Panova 2024 (cross-product);
  - Chen 2018 (×2, journal and arXiv);
  - Sah 2020;
  - Olson–Sagan 2018;
  - Zaguia 2020 (×2, greedy N-free);
  - "On Partially Ordered Sets and the 1/3–2/3 Conjecture" (Springer chapter 2024, no abstract available);
  - "A Similarity Space Approach to the 1/3–2/3 Conjecture" (IEEE Informatics 2024). Its abstract claims a general "proof" that it concedes needs "a more rigorous and detailed proof". Nothing about thin posets.
- Semantic Scholar citations → 10. It adds Gupta 2026 and Dolores-Cuenca et al. 2024.
- Of these I read, in full text or the relevant passage: Gupta, Dolores-Cuenca et al. (lines 26–29 and 61–62: "5-thin posets [5] … 6-thin posets [16]"), Zaguia 2012 (l.43–44: "for 5-thin posets [4], and for 6-thin posets [8]"), and Olson–Sagan (p.2: "posets with each element incomparable to at most 6 others [Pec08]"). **Each one stops at 6.**

**Peczarski's later papers:**
- Order 23 (2006), GPC for n ≤ 11: title and citations only.
- "Comments on the Golden Partition Conjecture", Contrib. Discrete Math. 12 (2017) 106–109: abstract read. It covers N-free generalisation and automorphisms, with no thin result.
- "The Worst Balanced Partially Ordered Sets — Ladders with Broken Rungs", Exp. Math. 28 (2019) 181–184: abstract read. It is a computer search for small balance constants, with no thin result.
- dblp's page and search API returned Access Denied and a non-JSON response, so I used the arXiv author query and the OpenAlex/Semantic Scholar/Crossref records instead.

**Web search (7 queries):**
- `"7-thin" posets 1/3-2/3 conjecture`
- `Peczarski "gold partition conjecture" 6-thin posets computer`
- `"thin posets" balanced pair 1/3-2/3 conjecture arXiv 2025 2026`
- `"balanced pair" poset "incomparable to at most" elements 1/3-2/3`
- `Brightwell Wright "5-thin" … proof method computer minimal counterexample`
- `"incomparable with at most seven" OR "incomparable to at most seven" poset linear extensions`
- `Peczarski "6-thin" gold partition conjecture pdf mimuw`

Every hit restates 5-thin and 6-thin as the known cases. **No hit mentions 7-thin or "at most seven".** Wikipedia's 1/3–2/3 page (raw source, read) says "partial orders in which each element is incomparable to at most six others [Peczarski 2008]" and lists Gupta 2026 through 14 elements.

**KSBFT_v7 reference list** (pp. 26–28, read in full). No entry beyond BW92 and Pec08 bears on thin posets. Its [Gup26] and [Haq26] were covered above and in mg-3c5b.

**Could not access** (paywall or bot wall; abstracts only where noted):
- Pec08 full text (Springer);
- BW92 full text (SIAM 403; abstract via OpenAlex);
- Brightwell 1999 survey (Elsevier open-archive PDF, but ScienceDirect served a bot-check page to both curl and fetch);
- Peczarski's 2006 PhD thesis (Polish, Univ. Warsaw);
- the 2024 Springer chapter.

I did not use Google Scholar directly. OpenAlex and Semantic Scholar stand in for "anything citing Pec08".

**Positive controls.** The same instruments did find every *known* item: Pec08 through its citers, Gupta through the arXiv `"gold partition"` query, and BW92 through web and OpenAlex. So a 7-thin paper phrased in the standard vocabulary would have surfaced. The one thing that cannot be controlled for is a result stated in non-standard terms, e.g. "bandwidth" or "incomparability degree", in a venue we could not search.

## 3. Peczarski's method, and how mg-e8b4 differs

**What is established:**
- Pec08 is a computer proof: its abstract says "the proof involves the extensive use of computers". BW92 is one too: "the use of a computer to eliminate a large number of cases".
- Pec08's reference list (Crossref) shows the toolchain:
  - Ullman 1976 (subgraph isomorphism);
  - Varol–Rotem 1981 ("an algorithm to generate all topological sorting arrangements", i.e. listing linear extensions);
  - Wells 1971 and Lipski 2004 (combinatorial computing texts);
  - Peczarski 2004 (min-comparison sorting) and Peczarski 2006 (GPC ≤ 11 elements, and the PhD thesis "Computer Assisted Research of Posets");
  - C. D. Wright's 1990 Cambridge PhD thesis "Combinatorial Algorithms" (Wright is BW92's co-author);
  - BW92 and Brightwell 1988 (linear extensions of infinite posets).
- So Pec08 extends the BW92 computation. It enumerates finitely many small configurations up to isomorphism (subgraph isomorphism for rejection) and evaluates them **exactly by listing linear extensions** (Varol–Rotem). It checks the stronger GPC property, which needs counts after two comparisons, not only single-pair probabilities.

**What is NOT established (I did not read the full texts):** the reduction BW92/Pec08 use to turn "all k-thin posets, all n" into finitely many cases. In particular, whether it is a bottom-configuration/minimal-counterexample argument like mg-e8b4's is unknown. The citation of Brightwell 1988 (infinite posets) hints that the infinite limits are handled explicitly, but that is inference. **Any sentence in mg-e8b4 claiming "our reduction differs from Pec08's" must stay CONDITIONAL until someone reads Pec08 §2–3.**

**What can be said now about the difference:**

| | BW92 / Pec08 | mg-e8b4 (KSBFT-I) |
|---|---|---|
| property checked | 1/3–2/3 (BW92); GPC, which is stronger (Pec08) | 1/3–2/3 only |
| exact evaluation | enumerate linear extensions (Varol–Rotem) | transfer-matrix / down-set Markov chain over ≤ C(2D,D) states; exact rational P over prefix down-sets |
| isomorphism handling | subgraph isomorphism (Ullman) | canonical down-degree order (Lemma 2b) |
| n-uniformity | yes (a theorem for all n); the mechanism is unread | Lemma 3 convexity (prefix certificate) plus a joint Gordan/LP certificate (Lemma 4). Every continuation is covered at once. |
| reach | D ≤ 6, and KSBFT_v7 says the methods "break down for larger D" | D ≤ 7 (2.18·10⁹ nodes, 1 h 49 min on 3 cores, per mg-e8b4; **not re-run here**, audit mg-9268 in flight) |

**Suggested wording for mg-e8b4 / KSBFT-I §0 item 2**, pending mg-9268: "To our knowledge (search mg-00c0, 2026-09-26) the 1/3–2/3 conjecture was known only for 6-thin posets [Pec08]; ours is the first result for 7-thin posets. Pec08 proves the stronger Gold Partition Conjecture at D ≤ 6, which we do not address at D = 7. Posets of range ≤ 7 on ≤ 14 elements were already covered by [Gup26]."

## 4. Not measured / not verified here

- The correctness of mg-e8b4 (that is mg-9268's job). The 2.18·10⁹ nodes and the timing are mg-e8b4's figures, not re-derived here.
- The finite-reduction mechanism in BW92/Pec08 (full texts unread).
- Whether Peczarski's 2006 thesis or the 2024 Springer chapter mention range 7 (both unread; the chapter has no abstract indexed).
- Whether anything appeared on arXiv after the queries ran (2026-09-26 ~07:30 UTC).
