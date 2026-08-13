# 1/3–2/3 Program — Executive Summary

*One page. Prose. Written to be read, not parsed — nothing machine-consumes this file, and
nothing should start. Depth is in [`STATE.md`](STATE.md), which is the internal working
record and is addressed by instruments; reference material is linked at the bottom.*

---

**What we are trying to prove.** The 1/3–2/3 conjecture: in any finite partial order that is
not a chain, some incomparable pair sits near the middle — over a uniformly random linear
extension, one of the pair comes first with probability between 1/3 and 2/3. The classical
line of attack has been stuck at 0.2764 for thirty years. This programme does not try to
push that constant. It goes at the conjecture directly.

**The shape of the attack.** Assume a smallest counterexample and derive a contradiction. It
has to be *frozen*: every incomparable pair decided more than 2/3 of the way, with all those
decisions lined up behind a single reference order. From there the argument runs in four
steps — frozen implies a random linear extension stays close to the reference order; staying
close implies a thin interface across some prefix cut; a thin interface implies a balanced
pair survives at that cut; and a balanced pair contradicts frozenness. No counterexample,
conjecture proved.

**Where it stands.** The chain is assembled and every link but two is proven for all finite
posets, at any width. The whole conjecture is now reduced to one implication.

**The wall.** That implication is step one: frozen implies few inversions, quantitatively.
The important thing about it is that it has already split in half, and only one half is
open. *That a uniform constant exists is proven* — for every finite poset, at every size.
What is open is purely **how small the constant is**. The downstream argument needs about
0.02; what is proven is under 1. The entire remaining gap in this programme is that factor
of roughly fifty.

**And the route that got us here provably cannot finish.** Everything proven so far is
derived from pairwise information alone — what each pair does, averaged. We now know
exactly how far that reaches: the best constant any pair-bias argument can produce tends to
1, with explicit witnesses attaining it. So there is no sharpening left to find on this
road. Closing the gap needs a genuinely different input: a *realizability* fact, something
that constrains which patterns of pairwise bias a **real poset** can actually exhibit, as
opposed to an arbitrary probability distribution.

**Why it is hard.** The step we need is *false* for abstract frozen distributions — one can
write down a distribution where every pair is frozen and the inversions are still as many as
possible. So no proof can treat the linear extensions as a generic random object; it must
use that they come from a genuine poset. That rules out the standard marginal-only toolkit,
and it is why the remaining work is hard rather than merely unfinished.

**What else is open.** One secondary link — thin interface implies the balanced pair
survives — is also unproven, though it is not the bottleneck. Beneath the wall sit three
concrete targets, any of which would move it: breaking a wrong-signed covariance, showing
frozen posets cannot be too dense, and bounding mean displacement.

**One caution about the record.** Several supporting facts are exhaustive checks over six or
seven elements. Those can *refute* a universal claim but never establish one, and a
counterexample's size is unknown and unbounded. Any summary sentence spanning several
results is only as strong as the weakest one in it — which is why the internal ledger marks
every result with the kind of warrant behind it.

**Bottom line.** The reduction is real, both endpoints are proven, and the programme is
down to a single implication about the size of a single constant. We can prove that
constant exists. We cannot yet prove it is small, and we have proved that our current
method never will.

---

### Reference

- [`STATE.md`](STATE.md) — internal working record: the full ledger, warrant kinds, open targets, attempt index.
- [`docs/CONCEPTS.md`](docs/CONCEPTS.md) — what the objects mean, in words before symbols.
- [`docs/FACTS.md`](docs/FACTS.md) — measured facts with no current consumer.
- [`docs/state-history/`](docs/state-history/) — per-attempt history, verbatim.
