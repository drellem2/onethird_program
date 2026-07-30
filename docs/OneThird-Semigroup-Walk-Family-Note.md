# The semigroup walk family — an expository note

*For Daniel. Written 2026-07-30 (mg-6016). Everything numerical here is produced by
`code/semigroup_note/note_check.py`; its committed output is `code/semigroup_note/note_check_output.txt`.
Regenerate with `code/semigroup_note/run_all.sh` — pure Python 3, no dependencies, about 13 seconds, and
the output file reproduces byte-identically. That script shares no code with `code/hodge_leverage/` or
`code/face_geometry/`: it rebuilds the objects from their definitions in exact rational arithmetic, so the
numbers below are independent of the pipeline they are about.*

---

## 0. Read this first: I described the moves wrongly in mail, and here is the correction

In an earlier mail I described a move as a **monotone refinement** — as though each step committed a few
more pairs of elements to a fixed relative order, and never un-committed anything. Your reply was:

> "Yes this walk alone seems somewhat trivial and is not really a walk."

Against the description I had given, that is correct, and it is worth being precise about *why* it is
correct, because it says what the real object has to avoid. If every step only added commitments and never
removed any, the number of committed pairs would be non-decreasing along every trajectory, so it would
converge; the process would grind to a halt at some maximally-committed configuration and stay there. That
is an **absorbing** process, not a mixing one, and its spectral theory would be uninteresting. My
description was of a process like that. It was wrong.

The actual action does something different. A move puts **its own elements at the front, in its own order,
and then fills in behind them from the current ordering**. It **overwrites the front and retains the tail**.
Nothing is monotone, nothing accumulates irreversibly, and a commitment made by one move is destroyed by
the next move that touches the same elements. The picture to hold is **move-named-cards-to-the-top**, not
progressive refinement. The walk **mixes**; it does not terminate. §1 states this precisely and §3 shows a
commitment being made and then destroyed, in four lines of arithmetic.

---

## 1. The terms

Six objects, and no others. Everything later is built from these.

I assume you know what a **poset** is and what a **linear extension** of one is. Fix a finite poset `P` on
a set of elements.

**1. Ordering.** A linear extension of `P` — a listing of all the elements, left to right, in which every
element appears before everything above it. These are the states of the walk. Write `L(P)` for the set of
them.

**2. Move.** An ordered list of disjoint blocks `(B_1, B_2, …, B_k)` whose union is all the elements,
subject to one condition: whenever `i < j` in `P`, the block containing `i` is not strictly after the
block containing `j`. (So `i` and `j` may share a block, or `i`'s block may come first — but `j`'s block
must not come first.) A move with `k = 1` is the one-block move, which is the do-nothing move. Call the
condition **`P`-compatibility**.

*Dictionary to the literature: a move is what is called a **face**, and `P`-compatibility is what makes it
a face of the order cone. Ordering = **chamber**.*

**3. The action of a move on an ordering.** Given a move `x = (B_1,…,B_k)` and an ordering `c`, the result
`x·c` is: **the elements of `B_1` first, then the elements of `B_2`, and so on — and inside each block, the
elements in the order they already appear in `c`.**

That is the whole definition. Note what it does and does not decide. The move decides **which block comes
first**; it does **not** decide the order inside a block — that is copied from the current state. So a move
is "move these named elements to the front (in this block order), and let everything else fall in behind in
the order it is already in."

**4. Weight.** A probability distribution `w` on the moves: `w(x) ≥ 0`, summing to 1.

**5. The walk.** From the current ordering `c`, draw a move `x` from `w`, go to `x·c`. Repeat. Every walk
in the family is specified by choosing `P` and choosing `w`.

**6. Commitment level of a move.** Forget the block *order* and keep only the blocks as an unordered
family. That partition of the elements is the move's commitment level. Two different moves can share a
level — `(ab|cd)` and `(cd|ab)` do. Intuitively the level records **which pairs of elements the move
decides the order of, regardless of where you started**: a pair in different blocks is decided by the move,
a pair in the same block is inherited from the current ordering. The level says which pairs get decided; the
block order says how.

That is all six. There is no seventh.

**Two facts about the action, checked exhaustively rather than asserted.** For the worked example of §3,
over all 26 moves × 6 orderings: the result is always again an ordering of `P` (0 failures of 156), and the
action agrees with what you get by treating the ordering itself as a move and multiplying (0 mismatches of
156). The second fact is the reason the walk is a *semigroup* walk at all, and it is what §2 is about.

---

## 2. The two properties that are the entire hypothesis

Moves compose. Given two moves `x` and `y`, define `x·y` by intersecting: take every block of `x` against
every block of `y`, keep the non-empty intersections, and order them by `(block of x, block of y)`
lexicographically — all the pieces of `x`'s first block first (subdivided in `y`'s order), then all the
pieces of `x`'s second block, and so on. This is again a move, and `x·(y·c) = (x·y)·c`, so **`x·y` is the
single move that does "`y` first, then `x`".**

The whole hypothesis of the theorem in §5 is two identities:

> **(i) `x·x = x`.** Applying a move twice in a row is the same as applying it once.
>
> **(ii) `x·y·x = x·y`.** Doing `x`, then `y`, then `x` again gives the same result as just doing `y` then
> `x`. The earlier `x` leaves no trace once `x` is done again.

**What these are properties of, and what they are not.** They are statements about **how moves compose** —
about the algebra of the moves among themselves. Property (ii) in particular is a statement that a move
*erases* the effect of an earlier copy of itself. That is the opposite of accumulation. Neither identity
says, or implies, that information only accumulates; neither is a monotonicity claim; neither makes the
walk absorbing. A structure satisfying (i) and (ii) is called a **left regular band**; both are classical
for ordered partitions, and the only thing that needs checking for us is that `P`-compatibility survives
the product (**closure**).

*Verified.* On the worked example: `x·x = x` on 26 of 26 moves; `x·y·x = x·y` on 676 of 676 pairs; closure
on 676 of 676; associativity on 17 576 of 17 576 triples. Exhaustively over **every labelled poset** on
`n` elements, 0 failures throughout:

| `n` | posets | `x·x = x` | `x·y·x = x·y` | closure | associativity |
|---|---|---|---|---|---|
| 2 | 3 | 0 bad of 7 | 0 bad of 17 | 0 bad of 17 | 0 bad of 43 |
| 3 | 19 | 0 bad of 121 | 0 bad of 865 | 0 bad of 865 | 0 bad of 6 949 |
| 4 | 219 | 0 bad of 4 399 | 0 bad of 109 121 | 0 bad of 109 121 | not run |
| 5 | 63 *(isomorphism classes)* | 0 bad of 5 757 | 0 bad of 922 073 | 0 bad of 922 073 | not run |

---

## 3. The worked example, part one: the walk

Take `P` on four elements `a, b, c, d` with exactly two relations: **`a < b` and `c < d`**, and nothing
else. This is the smallest poset on which the machinery is not degenerate — §4 says in what sense.

**The orderings.** The interleavings of `ab` with `cd`. There are six:

```
abcd    acbd    acdb    cabd    cadb    cdab
```

**The moves.** Of the 75 ordered partitions of four elements, **26** are `P`-compatible:

| blocks | count | the moves |
|---|---|---|
| 1 | 1 | `(abcd)` |
| 2 | 7 | `(abc\|d)` `(ab\|cd)` `(acd\|b)` `(ac\|bd)` `(a\|bcd)` `(cd\|ab)` `(c\|abd)` |
| 3 | 12 | `(ab\|c\|d)` `(ac\|b\|d)` `(a\|bc\|d)` `(a\|b\|cd)` `(ac\|d\|b)` `(a\|cd\|b)` `(a\|c\|bd)` `(c\|ab\|d)` `(cd\|a\|b)` `(c\|ad\|b)` `(c\|a\|bd)` `(c\|d\|ab)` |
| 4 | 6 | `(a\|b\|c\|d)` `(a\|c\|b\|d)` `(a\|c\|d\|b)` `(c\|a\|b\|d)` `(c\|a\|d\|b)` `(c\|d\|a\|b)` |

(For instance `(b|acd)` is not a move: it would put `b` before `a`. Neither is `(ad|b|c)`: it puts `d`
before `c`.)

**One step, spelled out.** Take the move `x = (ac|bd)` — "move `a` and `c` to the front, keeping their
current relative order; let `b` and `d` follow, keeping theirs." Applied to each of the six orderings:

| from | `a,c` in that order | `b,d` in that order | to |
|---|---|---|---|
| `abcd` | `a c` | `b d` | `acbd` |
| `acbd` | `a c` | `b d` | `acbd` |
| `acdb` | `a c` | `d b` | `acdb` |
| `cabd` | `c a` | `b d` | `cabd` |
| `cadb` | `c a` | `d b` | `cadb` |
| `cdab` | `c a` | `d b` | `cadb` |

Read the last row: from `cdab`, this move takes `a` and `c` to the front **in the order they already stood
in** (`c` before `a`), then `b` and `d` behind them in the order they already stood in (`d` before `b`).
The front is rewritten, the tail's internal order is kept. That is the whole mechanism.

**Nothing accumulates — a commitment made, then destroyed.** Start at `abcd`.

```
abcd                                      a stands before c
  apply (a|c|bd)   ->   acbd              a before c, and this move DECIDED it (a and c are in
                                          separate blocks, so the result did not depend on the input)
  apply (cd|ab)    ->   cdab              c before a -- the decision is gone
  apply (a|c|bd)   ->   acdb              a before c again
```

The move `(a|c|bd)` puts `a` strictly before `c` no matter what it is applied to. The very next move
`(cd|ab)` puts `c` strictly before `a`. There is no ratchet. Concretely: **every one of the six orderings
is reachable from every one of the six**, there is exactly one move that fixes all six (the do-nothing move
`(abcd)`), and there are **zero** absorbing orderings. The walk mixes.

---

## 4. The worked example, part two: the commitment levels

Collect the commitment levels of all 26 moves. There are **14** distinct ones, out of the 15 partitions of
`{a,b,c,d}`. The missing one is

```
    {a,d} | {b,c}
```

and it is missing for a reason worth seeing. Contract each block to a point. Since `a < b`, there is an
arrow `{a,d} → {b,c}`. Since `c < d`, there is an arrow `{b,c} → {a,d}`. That is a cycle, so no consistent
"which block first" is available, so no move has that shape. In general:

> **The commitment levels of `P` are exactly the partitions whose quotient is acyclic** — contract the
> blocks, keep the induced arrows between distinct blocks, and demand no directed cycle.

*Verified:* on this poset the two descriptions (supports of moves; acyclic quotients) give the same 14
partitions. Exhaustively, they agree on **every labelled poset up to 5 elements**: 1 of 1, 3 of 3, 19 of
19, 219 of 219, 4 231 of 4 231. Not proven in general — see §7.

This is the sense in which the example is not degenerate: for a poset like an antichain, *every* partition
is a level and the acyclic condition does nothing. Here it removes one, and you can see it removing it.

Here are the 14 levels with the moves sitting at each. Notice several levels carry more than one move —
that is the block-order information being forgotten.

```
abcd      <- (abcd)                          a|b|cd   <- (a|b|cd) (a|cd|b) (cd|a|b)
a|bcd     <- (a|bcd)                         a|bd|c   <- (a|c|bd) (c|a|bd)
acd|b     <- (acd|b)                         a|bc|d   <- (a|bc|d)
ab|cd     <- (ab|cd) (cd|ab)                 ad|b|c   <- (c|ad|b)
abd|c     <- (c|abd)                         ac|b|d   <- (ac|b|d) (ac|d|b)
ac|bd     <- (ac|bd)                         ab|c|d   <- (ab|c|d) (c|ab|d) (c|d|ab)
abc|d     <- (abc|d)                         a|b|c|d  <- the six orderings, read as moves
```

---

## 5. The worked example, part three: the spectrum

The theorem (stated in §7; it is not ours) says that for **any** weight `w` the transition matrix is
diagonalisable, and:

> **Eigenvalue at a level `X`:** `λ_X` = the total probability of the moves whose commitment level is
> **coarser than or equal to** `X`. (Coarser = `X` refines it. The do-nothing move is coarser than
> everything, so it contributes to every level.)
>
> **Multiplicity at a level `X`:** the integer `m_X` determined by `Σ_{Y refines X} m_Y = Π_{B ∈ X}
> |L(P restricted to B)|` — solved from the finest level downwards. **`m_X` involves no probabilities at
> all.**

### 5a. The multiplicities, from `P` alone

The right-hand side needs only counts of linear extensions of induced subposets. On our `P`:
`|L(P|{a,b})| = 1` (it is a chain), `|L(P|{a,c})| = 2` (an antichain), `|L(P|{a,b,c})| = 3`,
`|L(P)| = 6`, and so on. Solving from the top:

| level `X` | `Π_B \|L(P\|_B)\|` | levels refining it | `m_X` |
|---|---|---|---|
| `a\|b\|c\|d` | 1 | itself | **1** |
| `ac\|b\|d` | 2 | itself, `a\|b\|c\|d` | **1** |
| `ad\|b\|c` | 2 | itself, `a\|b\|c\|d` | **1** |
| `a\|bc\|d` | 2 | itself, `a\|b\|c\|d` | **1** |
| `a\|bd\|c` | 2 | itself, `a\|b\|c\|d` | **1** |
| `ab\|c\|d` | 1 | itself, `a\|b\|c\|d` | **0** |
| `a\|b\|cd` | 1 | itself, `a\|b\|c\|d` | **0** |
| `ac\|bd` | 4 | itself, `ac\|b\|d`, `a\|bd\|c`, `a\|b\|c\|d` | **1** |
| `ab\|cd` | 1 | itself, `ab\|c\|d`, `a\|b\|cd`, `a\|b\|c\|d` | **0** |
| `abc\|d` | 3 | itself, `ab\|c\|d`, `ac\|b\|d`, `a\|bc\|d`, `a\|b\|c\|d` | **0** |
| `abd\|c` | 3 | itself, `ab\|c\|d`, `ad\|b\|c`, `a\|bd\|c`, `a\|b\|c\|d` | **0** |
| `acd\|b` | 3 | itself, `ac\|b\|d`, `ad\|b\|c`, `a\|b\|cd`, `a\|b\|c\|d` | **0** |
| `a\|bcd` | 3 | itself, `a\|bc\|d`, `a\|bd\|c`, `a\|b\|cd`, `a\|b\|c\|d` | **0** |
| `abcd` | 6 | all 14 | **0** |

Sum of multiplicities: `1+1+1+1+1+0+0+1+0+0+0+0+0+0 = 6 = |L(P)|`. ✔

Work one row by hand to see there is no magic. Level `ac|bd`: the induced subposets are `{a,c}` and
`{b,d}`, both antichains, so the product is `2 × 2 = 4`. The levels refining `ac|bd` are `ac|bd` itself,
`ac|b|d`, `a|c|bd` (written `a|bd|c` above), and `a|b|c|d`. So `m + 1 + 1 + 1 = 4`, hence `m = 1`.

**Six of the fourteen levels carry a nonzero multiplicity:**
`ac|bd`, `a|bd|c`, `a|bc|d`, `ad|b|c`, `ac|b|d`, `a|b|c|d`. The other eight contribute nothing to the
spectrum. **That list was computed without ever mentioning a probability.**

### 5b. Three weightings

Now pick weights. Put all the probability on eight moves, in thirty-secondths:

| move | `w1` | `w2` | `w3` |
|---|---|---|---|
| `(abcd)` | 4/32 | 8/32 | 2/32 |
| `(a\|bcd)` | 6/32 | 4/32 | 3/32 |
| `(ac\|bd)` | 2/32 | 3/32 | 5/32 |
| `(ac\|b\|d)` | 3/32 | 2/32 | 1/32 |
| `(a\|bc\|d)` | 5/32 | 6/32 | 6/32 |
| `(c\|ad\|b)` | 7/32 | 3/32 | 7/32 |
| `(a\|c\|bd)` | 1/32 | 2/32 | 4/32 |
| `(a\|b\|c\|d)` | 4/32 | 4/32 | 4/32 |
| *total* | *1* | *1* | *1* |

**The eigenvalue at a level is a partial sum of that column**, over the moves whose level is coarser than
or equal to it. Take `w1` and the level `a|bd|c`. Which of the eight weighted moves have a level that
`a|bd|c` refines? `(abcd)` — level `abcd`, coarsest, always in. `(a|bcd)` — level `a|bcd`; is
`{a},{b,d},{c}` a refinement of `{a},{b,c,d}`? Yes. `(ac|bd)` — level `ac|bd`; is `{a},{b,d},{c}` a
refinement of `{a,c},{b,d}`? Yes (`{a}` and `{c}` sit inside `{a,c}`, `{b,d}` inside `{b,d}`).
`(a|c|bd)` — level `a|bd|c`, itself. Yes. And the other four: no. So

```
    lambda(a|bd|c)  =  4/32 + 6/32 + 2/32 + 1/32  =  13/32.
```

All six spectrum-carrying levels, under all three weightings:

| level (multiplicity) | `w1` | `w2` | `w3` |
|---|---|---|---|
| `ac\|bd` (1) | 6/32 = **3/16** | 11/32 | 7/32 |
| `ac\|b\|d` (1) | 9/32 | 13/32 | 8/32 = **1/4** |
| `ad\|b\|c` (1) | 11/32 | 11/32 | 9/32 |
| `a\|bd\|c` (1) | 13/32 | 17/32 | 14/32 = **7/16** |
| `a\|bc\|d` (1) | 15/32 | 18/32 = **9/16** | 11/32 |
| `a\|b\|c\|d` (1) | **1** | **1** | **1** |

**Checked against the actual 6 × 6 matrix, in exact rational arithmetic**, by computing
`dim ker(M − λI)` for each predicted `λ`. Under `w1`: dimensions `1,1,1,1,1,1`, summing to 6 of 6 — so the
spectrum is right and `M` is diagonalisable. Under `w2`: `1,1,1,2` summing to 6 of 6. Under `w3`:
`1,1,1,1,1,1` summing to 6 of 6.

### 5c. The point of the whole note

The three eigenvalue lists are three different sets of numbers. The **level → multiplicity** table did not
move, because it never saw a probability:

```
abcd:0   a|bcd:0   acd|b:0   ab|cd:0   abd|c:0   ac|bd:1   abc|d:0
a|b|cd:0   a|bd|c:1   a|bc|d:1   ad|b|c:1   ac|b|d:1   ab|c|d:0   a|b|c|d:1
```

Concretely: `w(abcd) = 4/32` under `w1` and `8/32` under `w2`. Both `1/8` and `1/4` are honest partial sums
— they are the number sitting at level `abcd`, and also at `acd|b`, at `ab|cd`, at `abd|c`, at `abc|d` and
at `ab|c|d`. **Neither is an eigenvalue**, under either weighting, because all six of those levels carry
multiplicity 0, and that 0 came out of counting linear extensions of `P`.

**One honest caveat, because it is the kind of thing that gets glossed.** What is `w`-independent is the
multiplicity attached to each **level**. The multiplicity of a **number** is the sum over the levels that
happen to land on it, and levels can collide. Under `w2` the levels `ac|bd` and `ad|b|c` both evaluate to
`11/32`, so the *number* `11/32` has multiplicity 2 — while each of the two levels still has multiplicity 1.
Under `w1` and `w3` all six are distinct and every eigenvalue has multiplicity 1. Both facts are in the
rank computations above. So the correct statement is *"the multiplicity function on levels is an invariant
of `P`"*, not *"the list of eigenvalue multiplicities never changes"*.

---

## 6. The antichain: this is the classical shuffle setting, and the family is exactly the classical family

Let `P` have **no relations at all**. Then:

- Every listing of the `n` elements is an ordering, so the states are all `n!` of them — **`L(P)` is the
  symmetric group `S_n`**, and this is the deck-of-cards setting, not a poset curiosity.
- `P`-compatibility is vacuous, so the moves are **all** ordered set partitions of the `n` elements.
  Verified: 1, 3, 13, 75, 541 moves for `n = 1..5` — the Fubini numbers, equal to the full count of ordered
  set partitions in every case.
- Every partition is a commitment level (the acyclic condition is vacuous): 2, 5, 15, 52 levels at
  `n = 2..5`.
- The multiplicities have a closed form: `m_X = Π_{B ∈ X} (|B| − 1)!`. Verified on every level for
  `n = 2..5`, and they sum to `n!` in each case. (So multiplicities above 1 are entirely normal — at
  `n = 3` the one-block level already has multiplicity `2! = 2`.)

**The question you should hold me to.** I told you I *believed* this is the classical shuffle setting and
flagged that I had not verified it. Here is the answer, and it is stronger than what I said.

> **The family does not merely resemble the classical shuffle walks — for the antichain it IS them,
> exactly.** The moves on an antichain are precisely the faces of the braid arrangement, with precisely the
> same product, and the states are precisely its chambers. So the family of walks obtained by choosing a
> weight `w` is, term for term, the family of **hyperplane walks on the braid arrangement** analysed by
> Bidigare–Hanlon–Rockmore and Brown–Diaconis. It is not a subfamily and not a generalisation: it is the
> same set of walks.

Two named members, both verified here against their classical descriptions:

**Move-to-front (the Tsetlin library / random-to-top).** Put weight `w_i` on the move `({i}, rest)` — "move
card `i` to the top." The classical spectrum is: eigenvalue `Σ_{i∈S} w_i` for each subset `S`, with
multiplicity `D(n − |S|)`, the derangement number. The commitment-level machinery reproduces this exactly
for `n = 2,3,4,5` (2, 5, 9, 14 distinct eigenvalues), and for `n ≤ 4` the predicted multiplicities are
confirmed against the actual `n! × n!` matrix by exact rank computation, diagonalisable in every case.
Derangements are nowhere in the code; they fall out of `Π_B (|B| − 1)!` summed over the levels with a given
singleton set.

**The inverse riffle shuffle (Gilbert–Shannon–Reeds `a`-shuffle).** Label each card independently and
uniformly with one of `a` labels, then stably sort by label. That procedure **is** the action of the move
whose blocks are the label classes — so the inverse `a`-shuffle is a member of this family with no
translation needed. Verified for `n = 2,3,4,5` and `a = 2,3`: (i) the weight induced by the labelling
matches the move-by-move law exactly; (ii) the eigenvalue at a level `X` comes out to `a^{|X| − n}`, i.e.
`a^{−j}` where `j = n − (number of blocks)`; (iii) the multiplicities reproduce the classical Stirling
counts (number of permutations of `n` with `n − j` cycles); and (iv) for `n ≤ 4` all of this is confirmed
against a transition matrix built **directly from the labelling description with no reference to the
semigroup at all**, diagonalisable in every case.

So: move-to-front, random-to-top, move-a-random-set-to-the-front, and the inverse riffle shuffles are all
one construction with different weights. (The third of those is a member by definition — a two-block move
`(S, rest)` *is* "move the set `S` to the front, keeping relative orders"; only the first and last were
checked against an independently-known spectrum.) That is the classical content, and the poset version is
that same construction with `P`-compatibility imposed on the moves and acyclicity imposed on the levels.

**Which classical shuffles are *not* in it, so the coincidence is not oversold.** The family consists of
walks driven by a probability on moves acting on the left, and that is a real restriction. Tested on the
antichain by an exact rank computation asking only whether the target matrix lies in the **linear span** of
the move matrices — a necessary condition, weaker than membership, so a "no" here is decisive:

| walk on `S_n` | in the linear span of the moves? `n = 3` | `n = 4` |
|---|---|---|
| random-to-top (**control** — it is in the family) | **yes** | **yes** |
| top-to-random (the time-reversal of random-to-top) | **no** | **no** |
| random transpositions | **no** | **no** |
| lazy adjacent transpositions | **no** | **no** |

So the coincidence is with the walks *driven by faces*, which is exactly the class Bidigare–Hanlon–Rockmore
and Brown–Diaconis study — not with "shuffles" in general. Note in particular that a walk being in the
family does not make its time-reversal a member.

---

## 7. The honest boundary, and the real status

**The tool points to the side of the original target.** The adjacent-transposition walk — the one the
1/3–2/3 work is actually about — is **not** in this family. There is a short argument: weights are
nonnegative, so a move can be used at all only if it moves *every* ordering to itself or to an
adjacent-transposition neighbour; if some needed adjacent-transposition edge is then unsupplied by any
usable move, no weighting reproduces the walk. Run over all isomorphism classes of poset, for the *lazy*
adjacent-transposition walk:

| `n` | classes | provably **not** in the family | single ordering (vacuous) | not decided by this test |
|---|---|---|---|---|
| 2 | 2 | 0 | 1 | 1 |
| 3 | 5 | **2** | 1 | 2 |
| 4 | 16 | **11** | 1 | 4 |
| 5 | 63 | **55** | 1 | 7 |

(These reproduce the counts already in `docs/OneThird-Hodge-Side-Leverage.md` §9.4, from independent code.)
On the antichain specifically, at `n = 3, 4, 5` exactly one move is usable (the do-nothing move) and it
supplies 0 of the 12 / 72 / 480 needed edges, so the answer there is a flat no.

The cases this test leaves undecided were decided elsewhere, by exact linear programming, and every one of
them came out the *other* way: there the walk **is** in the family. That is not a rescue. On those posets
either `|L(P)|` is tiny, or the adjacent-transposition graph is a hypercube — and on a hypercube the
adjacent-transposition Laplacian is a sum of commuting terms, already diagonal before any of this is
invoked. So the technique reaches that walk only where the walk needed no help. See
`docs/OneThird-Hodge-Side-Leverage.md` §9.4 and roadmap item **F1**; the exact characterisation of the
positive class ("iff the graph is a hypercube") is an open conjecture that nobody has claimed. This note
does not re-argue any of it — it is settled and priced in `docs/roadmap.md`.

**What is ours and what is not.** Being exact about this matters more than it usually does, because the
attractive part of §5 is the part we did not do.

- **Not ours.** The diagonalisation theorem — that (i) and (ii) plus a weight give a diagonalisable
  transition matrix with eigenvalue = total probability of the moves at or below a level, and
  multiplicities determined by the counting identity — is **standard**. It is Brown's theorem for random
  walks on left regular bands (Brown, *Semigroups, rings, and Markov chains*, 2000), with the braid-
  arrangement case due to Bidigare–Hanlon–Rockmore and Brown–Diaconis. We cite it; we did not prove it and
  do not claim to. The classical shuffle results in §6 (the Tsetlin spectrum, the `a`-shuffle spectrum) are
  likewise classical — here they are **controls**, showing the machinery reproduces known answers.
- **Ours.** Two things, both modest. First, the **identification**: that this construction — `P`-compatible
  ordered partitions of a poset, acting on its linear extensions — satisfies the hypothesis, so the theorem
  applies to it. Second, the **description of the commitment levels** as exactly the partitions with acyclic
  quotient, which is what makes the multiplicity formula computable from `P`.
- **The status of the second one.** It is **verified exhaustively only to five elements** — every labelled
  poset on `≤ 5` elements (1, 3, 19, 219 and 4 231 of them at `n = 1..5`), 0 disagreements. It is **not
  proven in general**. Nothing in this note should be read as saying otherwise.

---

## 8. Summary in five lines

1. A move lists **its own elements first, in its own order**, then everything else **in the order it is
   already in**. It overwrites the front and keeps the tail. It is move-to-the-top, not refinement, and
   the walk mixes rather than absorbing. My earlier "monotone refinement" description was wrong, and your
   objection to it was right.
2. The hypothesis is two composition identities — a move repeated does nothing new, and a move erases an
   earlier copy of itself. Neither says information accumulates.
3. Every eigenvalue is a **partial sum of the move probabilities**; every multiplicity is a **count of
   linear extensions of induced subposets**, with no probability in it. §5 does both arithmetically on a
   6-state example and confirms them against the matrix in exact arithmetic under three different weights.
4. On an antichain the states are `S_n` and the family **is** the classical braid-arrangement shuffle
   family — move-to-front / Tsetlin and the inverse riffle shuffles included, both verified against their
   classical spectra.
5. The adjacent-transposition walk is not in the family except where its spectrum was already obvious. The
   theorem is standard; ours is the identification plus the acyclic-cut description of the levels, verified
   to five elements and not proven in general.
