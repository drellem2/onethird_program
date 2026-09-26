# ksbft_sec6_c929 — instrument for `docs/KSBFT-D-sec6-eps-spec.md` (mg-c929)

| script | what | status of what it shows |
|---|---|---|
| `s1_sec6_checks.py 6` | KSBFT (5.1)–(5.5), (6.4), (6.11), window-occupancy identity, Prop. B steps, over all 5230 naturally-labelled posets n ≤ 6; PC for the `d` formula; negative controls N1, N2 must print FIRES | EMPIRICAL; weak for §6 (only 86 posets have δ < 1/e, all with tiny gap) |
| `s2_parallel_chains.py 11` | window sum vs E[inv] on two parallel chains, exact, m ≤ 11 | EMPIRICAL (the window sum is also PROVEN in the doc) |
| `s3_constants.py` | explicit constants of Prop. B at ε₀ = 1/e − 1/3 and (illustrative) 1/6 | arithmetic |

`sh run_all.sh` regenerates all three transcripts (~50 s). Not wired into build.sh: nothing here
is a property the estate must hold.
