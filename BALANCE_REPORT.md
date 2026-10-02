# Deterministic attack catalog balance report

Catalog `1.0.0`: 10 startups, 4 choices per round, 640 reachable terminal paths.
Scores use the existing game scoring function. A bankrupt branch ends immediately; no later choices are counted.
These are local engine results, not a production-host CPU or memory benchmark.

| Startup | Paths | Score min | Score max | Mean | Median | Bankruptcy | Technical best | Technical worst |
|---|---:|---:|---:|---:|---:|---:|---|---|
| coffeebot | 64 | 204 | 891 | 513.95 | 462.0 | 0.0% | 891 (coffeebot_r1_4 → coffeebot_r2_4 → coffeebot_r3_2) | 204 (coffeebot_r1_1 → coffeebot_r2_2 → coffeebot_r3_1) |
| petmind | 64 | 264 | 678 | 457.89 | 452.5 | 0.0% | 678 (petmind_r1_3 → petmind_r2_4 → petmind_r3_3) | 264 (petmind_r1_1 → petmind_r2_2 → petmind_r3_2) |
| foodrover | 64 | 191 | 900 | 605.02 | 611.0 | 4.69% | 900 (foodrover_r1_4 → foodrover_r2_4 → foodrover_r3_4) | 191 (foodrover_r1_1 → foodrover_r2_1 → foodrover_r3_2) |
| studygenie | 64 | 125 | 875 | 471.86 | 454.5 | 0.0% | 875 (studygenie_r1_3 → studygenie_r2_4 → studygenie_r3_3) | 125 (studygenie_r1_1 → studygenie_r2_2 → studygenie_r3_2) |
| sleepwork | 64 | 68 | 900 | 448.38 | 421.5 | 1.56% | 900 (sleepwork_r1_4 → sleepwork_r2_4 → sleepwork_r3_1) | 68 (sleepwork_r1_3 → sleepwork_r2_3 → sleepwork_r3_4) |
| fitmirror | 64 | 86 | 688 | 330.11 | 304.5 | 0.0% | 688 (fitmirror_r1_4 → fitmirror_r2_4 → fitmirror_r3_3) | 86 (fitmirror_r1_2 → fitmirror_r2_2 → fitmirror_r3_4) |
| cloudkitchen | 64 | 97 | 728 | 387.56 | 372.0 | 0.0% | 728 (cloudkitchen_r1_3 → cloudkitchen_r2_1 → cloudkitchen_r3_1) | 97 (cloudkitchen_r1_1 → cloudkitchen_r2_4 → cloudkitchen_r3_4) |
| agrodrone | 64 | 126 | 913 | 585.97 | 622.0 | 12.5% | 913 (agrodrone_r1_4 → agrodrone_r2_4 → agrodrone_r3_1) | 126 (agrodrone_r1_1 → agrodrone_r2_3 → agrodrone_r3_3) |
| moodads | 64 | 159 | 393 | 276.2 | 272.0 | 0.0% | 393 (moodads_r1_3 → moodads_r2_2 → moodads_r3_4) | 159 (moodads_r1_1 → moodads_r2_1 → moodads_r3_3) |
| renteverything | 64 | 313 | 913 | 644.42 | 623.5 | 12.5% | 913 (renteverything_r1_4 → renteverything_r2_4 → renteverything_r3_4) | 313 (renteverything_r1_3 → renteverything_r2_3 → renteverything_r3_1) |

## Local deterministic round benchmark

1000 rounds with `coffeebot_r1_1` for `coffeebot`; per round: mean 0.1336 ms, median 0.1195 ms, p95 0.1656 ms, max 2.3421 ms. Peak process RSS observed: 29.27 MiB.

No economy or scoring changes are proposed by this report.
