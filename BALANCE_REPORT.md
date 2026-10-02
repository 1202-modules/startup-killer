# Deterministic attack catalog balance report

Catalog `2.0.0-partial`: 10 startups, 4 choices per round, 640 reachable terminal paths.
Scores use the existing game scoring function. A bankrupt branch ends immediately; no later choices are counted.
These are local engine results, not a production-host CPU or memory benchmark.

| Startup | Paths | Score min | Score max | Mean | Median | Bankruptcy | Technical best | Technical worst |
|---|---:|---:|---:|---:|---:|---:|---|---|
| coffeebot | 64 | 220 | 913 | 454.56 | 430.5 | 1.56% | 913 (coffeebot_r1_b → coffeebot_r2_b → coffeebot_r3_b) | 220 (coffeebot_r1_d → coffeebot_r2_d → coffeebot_r3_d) |
| petmind | 64 | 259 | 800 | 463.28 | 451.5 | 0.00% | 800 (petmind_r1_b → petmind_r2_b → petmind_r3_b) | 259 (petmind_r1_a → petmind_r2_c → petmind_r3_c) |
| foodrover | 64 | 122 | 913 | 510.05 | 506.5 | 1.56% | 913 (foodrover_r1_b → foodrover_r2_b → foodrover_r3_b) | 122 (foodrover_r1_d → foodrover_r2_d → foodrover_r3_d) |
| studygenie | 64 | 155 | 913 | 412.77 | 362.5 | 1.56% | 913 (studygenie_r1_b → studygenie_r2_b → studygenie_r3_b) | 155 (studygenie_r1_d → studygenie_r2_d → studygenie_r3_d) |
| sleepwork | 64 | 32 | 900 | 372.52 | 303.5 | 1.56% | 900 (sleepwork_r1_4 → sleepwork_r2_4 → sleepwork_r3_1) | 32 (sleepwork_r1_3 → sleepwork_r2_3 → sleepwork_r3_4) |
| fitmirror | 64 | 48 | 629 | 251.72 | 200.5 | 0.00% | 629 (fitmirror_r1_4 → fitmirror_r2_4 → fitmirror_r3_3) | 48 (fitmirror_r1_2 → fitmirror_r2_2 → fitmirror_r3_4) |
| cloudkitchen | 64 | 19 | 560 | 257.0 | 251.5 | 0.00% | 560 (cloudkitchen_r1_3 → cloudkitchen_r2_1 → cloudkitchen_r3_1) | 19 (cloudkitchen_r1_1 → cloudkitchen_r2_4 → cloudkitchen_r3_4) |
| agrodrone | 64 | 54 | 900 | 464.56 | 432.5 | 10.94% | 900 (agrodrone_r1_4 → agrodrone_r2_4 → agrodrone_r3_4) | 54 (agrodrone_r1_1 → agrodrone_r2_3 → agrodrone_r3_3) |
| moodads | 64 | 99 | 333 | 211.06 | 209.5 | 0.00% | 333 (moodads_r1_3 → moodads_r2_2 → moodads_r3_4) | 99 (moodads_r1_1 → moodads_r2_1 → moodads_r3_3) |
| renteverything | 64 | 171 | 913 | 529.72 | 498.0 | 9.38% | 913 (renteverything_r1_4 → renteverything_r2_4 → renteverything_r3_4) | 171 (renteverything_r1_3 → renteverything_r2_3 → renteverything_r3_1) |

## Four v2 startups: exhaustive outcome summary

Each startup has 64 choice sequences. Cash and damage are in RUB below; the raw path table retains kopeks. Player damage uses baseline at the same terminal month; score A uses baseline M9, including when bankruptcy ends a game early.
A bankrupt game stops immediately. The listed sequence is the actual played prefix.

| Startup | Min | Max | Mean | Median | Bankrupt | Near | Deep | Survived | Best coherent | DDD | Mixed mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---:|
| petmind | 259 | 800 | 463.28 | 451.5 | 0.00% | 43.75% | 56.25% | 0.00% | BBB: 800 | 525 | 450.97 |
| coffeebot | 220 | 913 | 454.56 | 430.5 | 1.56% | 15.63% | 81.25% | 1.56% | BBB: 913 | 220 | 441.82 |
| foodrover | 122 | 913 | 510.05 | 506.5 | 1.56% | 43.75% | 48.44% | 6.25% | BBB: 913 | 122 | 499.52 |
| studygenie | 155 | 913 | 412.77 | 362.5 | 1.56% | 10.94% | 71.88% | 15.63% | BBB: 913 | 155 | 398.18 |

## Explicit chains and prerequisite bypass controls

Controls ABB, CBB, DBB and AAC, ABC, ACB verify that a later same-letter card gets only base effects when the prerequisite chain was broken.

| Startup | Path | Score | Status | Cash RUB | Damage RUB | Flags | Defenses | Bankruptcy month |
|---|---|---:|---|---:|---:|---|---|---:|
| petmind | AAA | 648 | near_bankruptcy | 1,402,690 | 2,997,310 | accuracy_doubted, trust_crisis | independent_audit | — |
| petmind | BBB | 800 | near_bankruptcy | 566,968 | 3,833,032 | factory_pressure, stockout | NONE | — |
| petmind | CCC | 619 | near_bankruptcy | 1,587,402 | 2,812,598 | churn_wave, free_alternative | retention_offer, retention_offer | — |
| petmind | DDD | 525 | near_bankruptcy | 2,067,992 | 2,332,008 | — | NONE | — |
| petmind | ABB | 331 | deep_crisis | 3,004,485 | 1,395,515 | accuracy_doubted | NONE | — |
| petmind | CBB | 319 | deep_crisis | 3,070,341 | 1,329,659 | free_alternative | NONE | — |
| petmind | DBB | 352 | deep_crisis | 2,892,530 | 1,507,470 | — | NONE | — |
| petmind | AAC | 531 | near_bankruptcy | 1,983,298 | 2,416,702 | accuracy_doubted, trust_crisis | independent_audit | — |
| petmind | ABC | 368 | deep_crisis | 2,838,669 | 1,561,331 | accuracy_doubted | NONE | — |
| petmind | ACB | 338 | deep_crisis | 3,013,261 | 1,386,739 | accuracy_doubted | NONE | — |
| coffeebot | AAA | 709 | near_bankruptcy | 1,150,977 | 3,572,880 | campus_locked, footfall_contested | campus_redeploy | — |
| coffeebot | BBB | 913 | bankrupt | 0 | 4,964,215 | repair_backlog, uptime_exposed | service_reserve | 8 |
| coffeebot | CCC | 741 | near_bankruptcy | 962,056 | 3,761,801 | margin_squeeze, price_pressure | loyalty_program | — |
| coffeebot | DDD | 220 | survived | 3,677,609 | 1,046,248 | — | NONE | — |
| coffeebot | ABB | 503 | deep_crisis | 2,295,516 | 2,428,341 | footfall_contested | NONE | — |
| coffeebot | CBB | 512 | deep_crisis | 2,245,494 | 2,478,362 | price_pressure | NONE | — |
| coffeebot | DBB | 482 | deep_crisis | 2,418,646 | 2,305,211 | — | NONE | — |
| coffeebot | AAC | 580 | deep_crisis | 1,810,146 | 2,913,710 | campus_locked, footfall_contested | campus_redeploy, loyalty_program | — |
| coffeebot | ABC | 495 | deep_crisis | 2,282,968 | 2,440,889 | footfall_contested | loyalty_program | — |
| coffeebot | ACB | 542 | near_bankruptcy | 2,097,369 | 2,626,488 | footfall_contested | loyalty_program | — |
| foodrover | AAA | 804 | near_bankruptcy | 658,097 | 4,716,639 | route_restricted, route_scrutiny | route_rebuild | — |
| foodrover | BBB | 913 | bankrupt | 0 | 5,639,342 | battery_backlog, battery_pressure | battery_reserve | 8 |
| foodrover | CCC | 833 | near_bankruptcy | 462,199 | 4,912,537 | competitor_trial, restaurant_switch | restaurant_retention, restaurant_retention | — |
| foodrover | DDD | 122 | survived | 4,575,683 | 799,053 | — | NONE | — |
| foodrover | ABB | 542 | near_bankruptcy | 2,367,965 | 3,006,771 | route_scrutiny | NONE | — |
| foodrover | CBB | 561 | near_bankruptcy | 2,240,333 | 3,134,403 | competitor_trial | NONE | — |
| foodrover | DBB | 519 | deep_crisis | 2,518,166 | 2,856,570 | — | NONE | — |
| foodrover | AAC | 744 | near_bankruptcy | 1,056,143 | 4,318,593 | route_restricted, route_scrutiny | route_rebuild | — |
| foodrover | ABC | 595 | near_bankruptcy | 2,053,345 | 3,321,391 | route_scrutiny | NONE | — |
| foodrover | ACB | 578 | near_bankruptcy | 2,169,045 | 3,205,691 | route_scrutiny | NONE | — |
| studygenie | AAA | 696 | near_bankruptcy | 912,974 | 2,720,496 | quality_doubt, trust_crisis | quality_audit | — |
| studygenie | BBB | 913 | bankrupt | 0 | 3,672,030 | api_bottleneck, api_pressure | backup_provider | 8 |
| studygenie | CCC | 762 | near_bankruptcy | 624,143 | 3,009,327 | cohort_churn, exam_trial | student_retention, student_retention | — |
| studygenie | DDD | 155 | survived | 2,828,566 | 804,904 | — | NONE | — |
| studygenie | ABB | 362 | deep_crisis | 2,164,217 | 1,469,254 | quality_doubt | NONE | — |
| studygenie | CBB | 363 | deep_crisis | 2,159,091 | 1,474,379 | exam_trial | NONE | — |
| studygenie | DBB | 330 | deep_crisis | 2,294,399 | 1,339,072 | — | NONE | — |
| studygenie | AAC | 603 | deep_crisis | 1,264,279 | 2,369,191 | quality_doubt, trust_crisis | quality_audit | — |
| studygenie | ABC | 433 | deep_crisis | 1,953,302 | 1,680,169 | quality_doubt | NONE | — |
| studygenie | ACB | 418 | deep_crisis | 2,020,334 | 1,613,137 | quality_doubt | NONE | — |

## Matched BBB defense controls

The same BBB choices are simulated with normal deterministic defense selection and with defense forced to NONE; coefficients and incident costs are identical.

| Startup | Selected/no-defense cash RUB | Selected/no-defense bankruptcy month | Selected/no-defense total revenue RUB | Selected defense cost RUB | Selected/no-defense score |
|---|---:|---|---:|---:|---:|
| petmind | 566,968 / 566,968 | — / — | 16,824,240 / 16,824,240 | 0 | 800 / 800 |
| coffeebot | 0 / 0 | 8 / 8 | 15,145,166 / 14,512,771 | 600,000 | 913 / 913 |
| foodrover | 0 / 0 | 8 / 8 | 20,250,034 / 19,014,384 | 700,000 | 913 / 913 |
| studygenie | 0 / 0 | 8 / 8 | 9,382,648 / 8,875,963 | 500,000 | 913 / 913 |

## All 64 paths per v2 startup

Monetary values in this table are integer kopeks; flags and defenses are server-side simulation observations.

| Startup | Choices | Combo flags | Active causes | Defenses | Final cash | Same-month baseline cash | Player damage | Score | Status | Bankruptcy month |
|---|---|---|---|---|---:|---:|---:|---:|---|---:|
| petmind | AAA | accuracy_doubted, trust_crisis | petmind_a:petmind_a | independent_audit | 140268960 | 440000000 | 299731040 | 648 | near_bankruptcy | — |
| petmind | AAB | accuracy_doubted, trust_crisis | petmind_b:customer_churn | independent_audit | 186317760 | 440000000 | 253682240 | 556 | near_bankruptcy | — |
| petmind | AAC | accuracy_doubted, trust_crisis | petmind_c:petmind_c | independent_audit | 198329760 | 440000000 | 241670240 | 531 | near_bankruptcy | — |
| petmind | AAD | accuracy_doubted, trust_crisis | petmind_d:petmind_d | independent_audit | 126378720 | 440000000 | 313621280 | 674 | near_bankruptcy | — |
| petmind | ABA | accuracy_doubted | petmind_a:petmind_a | NONE | 248133280 | 440000000 | 191866720 | 446 | deep_crisis | — |
| petmind | ABB | accuracy_doubted | petmind_b:customer_churn | NONE | 300448480 | 440000000 | 139551520 | 331 | deep_crisis | — |
| petmind | ABC | accuracy_doubted | petmind_c:petmind_c | NONE | 283866880 | 440000000 | 156133120 | 368 | deep_crisis | — |
| petmind | ABD | accuracy_doubted | petmind_d:petmind_d | NONE | 212702080 | 440000000 | 227297920 | 518 | near_bankruptcy | — |
| petmind | ACA | accuracy_doubted | petmind_a:petmind_a | NONE | 277349120 | 440000000 | 162650880 | 391 | deep_crisis | — |
| petmind | ACB | accuracy_doubted | petmind_b:customer_churn | NONE | 301326080 | 440000000 | 138673920 | 338 | deep_crisis | — |
| petmind | ACC | accuracy_doubted | petmind_c:petmind_c | NONE | 334650560 | 440000000 | 105349440 | 259 | deep_crisis | — |
| petmind | ACD | accuracy_doubted | petmind_d:petmind_d | NONE | 239898560 | 440000000 | 200101440 | 468 | near_bankruptcy | — |
| petmind | ADA | accuracy_doubted | petmind_a:petmind_a | NONE | 218831360 | 440000000 | 221168640 | 502 | near_bankruptcy | — |
| petmind | ADB | accuracy_doubted | petmind_b:customer_churn | NONE | 248839520 | 440000000 | 191160480 | 440 | deep_crisis | — |
| petmind | ADC | accuracy_doubted | petmind_c:petmind_c | NONE | 252014720 | 440000000 | 187985280 | 432 | deep_crisis | — |
| petmind | ADD | accuracy_doubted | petmind_d:petmind_d | NONE | 217994720 | 440000000 | 222005280 | 505 | near_bankruptcy | — |
| petmind | BAA | factory_pressure | petmind_a:petmind_a | NONE | 262489760 | 440000000 | 177510240 | 414 | deep_crisis | — |
| petmind | BAB | factory_pressure | petmind_b:customer_churn | NONE | 259496000 | 440000000 | 180504000 | 419 | deep_crisis | — |
| petmind | BAC | factory_pressure | petmind_c:petmind_c | NONE | 271605440 | 440000000 | 168394560 | 392 | deep_crisis | — |
| petmind | BAD | factory_pressure | petmind_d:petmind_d | NONE | 197950880 | 440000000 | 242049120 | 545 | near_bankruptcy | — |
| petmind | BBA | factory_pressure, stockout | petmind_a:petmind_a | NONE | 129428800 | 440000000 | 310571200 | 667 | near_bankruptcy | — |
| petmind | BBB | factory_pressure, stockout | petmind_b:customer_churn | NONE | 56696800 | 440000000 | 383303200 | 800 | near_bankruptcy | — |
| petmind | BBC | factory_pressure, stockout | petmind_c:petmind_c | NONE | 159043840 | 440000000 | 280956160 | 608 | near_bankruptcy | — |
| petmind | BBD | factory_pressure, stockout | petmind_d:petmind_d | NONE | 97817920 | 440000000 | 342182080 | 726 | near_bankruptcy | — |
| petmind | BCA | factory_pressure | petmind_a:petmind_a | NONE | 267983360 | 440000000 | 172016640 | 408 | deep_crisis | — |
| petmind | BCB | factory_pressure | petmind_b:customer_churn | NONE | 291960320 | 440000000 | 148039680 | 355 | deep_crisis | — |
| petmind | BCC | factory_pressure | petmind_c:petmind_c | NONE | 325284800 | 440000000 | 114715200 | 277 | deep_crisis | — |
| petmind | BCD | factory_pressure | petmind_d:petmind_d | NONE | 230532800 | 440000000 | 209467200 | 485 | near_bankruptcy | — |
| petmind | BDA | factory_pressure | petmind_a:petmind_a | NONE | 209465600 | 440000000 | 230534400 | 519 | near_bankruptcy | — |
| petmind | BDB | factory_pressure | petmind_b:customer_churn | NONE | 239473760 | 440000000 | 200526240 | 457 | deep_crisis | — |
| petmind | BDC | factory_pressure | petmind_c:petmind_c | NONE | 242648960 | 440000000 | 197351040 | 450 | deep_crisis | — |
| petmind | BDD | factory_pressure | petmind_d:petmind_d | NONE | 208628960 | 440000000 | 231371040 | 522 | near_bankruptcy | — |
| petmind | CAA | free_alternative | petmind_a:petmind_a | NONE | 278441120 | 440000000 | 161558880 | 384 | deep_crisis | — |
| petmind | CAB | free_alternative | petmind_b:customer_churn | NONE | 275447360 | 440000000 | 164552640 | 389 | deep_crisis | — |
| petmind | CAC | free_alternative | petmind_c:petmind_c | NONE | 287556800 | 440000000 | 152443200 | 362 | deep_crisis | — |
| petmind | CAD | free_alternative | petmind_d:petmind_d | NONE | 213902240 | 440000000 | 226097760 | 516 | near_bankruptcy | — |
| petmind | CBA | free_alternative | petmind_a:petmind_a | NONE | 254718880 | 440000000 | 185281120 | 434 | deep_crisis | — |
| petmind | CBB | free_alternative | petmind_b:customer_churn | NONE | 307034080 | 440000000 | 132965920 | 319 | deep_crisis | — |
| petmind | CBC | free_alternative | petmind_c:petmind_c | NONE | 290452480 | 440000000 | 149547520 | 356 | deep_crisis | — |
| petmind | CBD | free_alternative | petmind_d:petmind_d | NONE | 219287680 | 440000000 | 220712320 | 506 | near_bankruptcy | — |
| petmind | CCA | churn_wave, free_alternative | petmind_a:petmind_a | retention_offer | 233377520 | 440000000 | 206622480 | 475 | near_bankruptcy | — |
| petmind | CCB | churn_wave, free_alternative | petmind_b:customer_churn | retention_offer | 253825808 | 440000000 | 186174192 | 433 | deep_crisis | — |
| petmind | CCC | churn_wave, free_alternative | petmind_c:petmind_c | retention_offer, retention_offer | 158740208 | 440000000 | 281259792 | 619 | near_bankruptcy | — |
| petmind | CCD | churn_wave, free_alternative | petmind_d:petmind_d | retention_offer | 196621808 | 440000000 | 243378192 | 548 | near_bankruptcy | — |
| petmind | CDA | free_alternative | petmind_a:petmind_a | NONE | 225416960 | 440000000 | 214583040 | 490 | near_bankruptcy | — |
| petmind | CDB | free_alternative | petmind_b:customer_churn | NONE | 255425120 | 440000000 | 184574880 | 427 | deep_crisis | — |
| petmind | CDC | free_alternative | petmind_c:petmind_c | NONE | 258600320 | 440000000 | 181399680 | 420 | deep_crisis | — |
| petmind | CDD | free_alternative | petmind_d:petmind_d | NONE | 224580320 | 440000000 | 215419680 | 493 | near_bankruptcy | — |
| petmind | DAA | — | petmind_a:petmind_a | NONE | 260660000 | 440000000 | 179340000 | 417 | deep_crisis | — |
| petmind | DAB | — | petmind_b:customer_churn | NONE | 257666240 | 440000000 | 182333760 | 422 | deep_crisis | — |
| petmind | DAC | — | petmind_c:petmind_c | NONE | 269775680 | 440000000 | 170224320 | 395 | deep_crisis | — |
| petmind | DAD | — | petmind_d:petmind_d | NONE | 196121120 | 440000000 | 243878880 | 548 | near_bankruptcy | — |
| petmind | DBA | — | petmind_a:petmind_a | NONE | 236937760 | 440000000 | 203062240 | 467 | deep_crisis | — |
| petmind | DBB | — | petmind_b:customer_churn | NONE | 289252960 | 440000000 | 150747040 | 352 | deep_crisis | — |
| petmind | DBC | — | petmind_c:petmind_c | NONE | 272671360 | 440000000 | 167328640 | 389 | deep_crisis | — |
| petmind | DBD | — | petmind_d:petmind_d | NONE | 201506560 | 440000000 | 238493440 | 538 | near_bankruptcy | — |
| petmind | DCA | — | petmind_a:petmind_a | NONE | 266153600 | 440000000 | 173846400 | 411 | deep_crisis | — |
| petmind | DCB | — | petmind_b:customer_churn | NONE | 290130560 | 440000000 | 149869440 | 359 | deep_crisis | — |
| petmind | DCC | — | petmind_c:petmind_c | NONE | 323455040 | 440000000 | 116544960 | 281 | deep_crisis | — |
| petmind | DCD | — | petmind_d:petmind_d | NONE | 228703040 | 440000000 | 211296960 | 488 | near_bankruptcy | — |
| petmind | DDA | — | petmind_a:petmind_a | NONE | 207635840 | 440000000 | 232364160 | 523 | near_bankruptcy | — |
| petmind | DDB | — | petmind_b:customer_churn | NONE | 237644000 | 440000000 | 202356000 | 460 | deep_crisis | — |
| petmind | DDC | — | petmind_c:petmind_c | NONE | 240819200 | 440000000 | 199180800 | 453 | deep_crisis | — |
| petmind | DDD | — | petmind_d:petmind_d | NONE | 206799200 | 440000000 | 233200800 | 525 | near_bankruptcy | — |
| coffeebot | AAA | campus_locked, footfall_contested | coffeebot_a:coffeebot_a | campus_redeploy | 115097715 | 472385682 | 357287967 | 709 | near_bankruptcy | — |
| coffeebot | AAB | campus_locked, footfall_contested | coffeebot_b:customer_churn | campus_redeploy | 151400184 | 472385682 | 320985498 | 643 | near_bankruptcy | — |
| coffeebot | AAC | campus_locked, footfall_contested | coffeebot_c:coffeebot_c | campus_redeploy, loyalty_program | 181014643 | 472385682 | 291371039 | 580 | deep_crisis | — |
| coffeebot | AAD | campus_locked, footfall_contested | coffeebot_d:coffeebot_d | campus_redeploy | 218469833 | 472385682 | 253915849 | 513 | deep_crisis | — |
| coffeebot | ABA | footfall_contested | coffeebot_a:coffeebot_a | NONE | 248840957 | 472385682 | 223544725 | 465 | deep_crisis | — |
| coffeebot | ABB | footfall_contested | coffeebot_b:customer_churn | NONE | 229551594 | 472385682 | 242834088 | 503 | deep_crisis | — |
| coffeebot | ABC | footfall_contested | coffeebot_c:coffeebot_c | loyalty_program | 228296824 | 472385682 | 244088858 | 495 | deep_crisis | — |
| coffeebot | ABD | footfall_contested | coffeebot_d:coffeebot_d | NONE | 275616266 | 472385682 | 196769416 | 407 | deep_crisis | — |
| coffeebot | ACA | footfall_contested | coffeebot_a:coffeebot_a | loyalty_program | 259983483 | 472385682 | 212402199 | 443 | deep_crisis | — |
| coffeebot | ACB | footfall_contested | coffeebot_b:customer_churn | loyalty_program | 209736874 | 472385682 | 262648808 | 542 | near_bankruptcy | — |
| coffeebot | ACC | footfall_contested | coffeebot_c:coffeebot_c | loyalty_program | 299643285 | 472385682 | 172742397 | 352 | deep_crisis | — |
| coffeebot | ACD | footfall_contested | coffeebot_d:coffeebot_d | loyalty_program | 280593877 | 472385682 | 191791805 | 396 | deep_crisis | — |
| coffeebot | ADA | footfall_contested | coffeebot_a:coffeebot_a | NONE | 310843482 | 472385682 | 161542200 | 352 | deep_crisis | — |
| coffeebot | ADB | footfall_contested | coffeebot_b:customer_churn | NONE | 266949011 | 472385682 | 205436671 | 442 | deep_crisis | — |
| coffeebot | ADC | footfall_contested | coffeebot_c:coffeebot_c | loyalty_program | 290444560 | 472385682 | 181941122 | 378 | deep_crisis | — |
| coffeebot | ADD | footfall_contested | coffeebot_d:coffeebot_d | NONE | 355447903 | 472385682 | 116937779 | 243 | deep_crisis | — |
| coffeebot | BAA | uptime_exposed | coffeebot_a:coffeebot_a | NONE | 313698429 | 472385682 | 158687253 | 339 | deep_crisis | — |
| coffeebot | BAB | uptime_exposed | coffeebot_b:customer_churn | NONE | 238364841 | 472385682 | 234020841 | 494 | deep_crisis | — |
| coffeebot | BAC | uptime_exposed | coffeebot_c:coffeebot_c | loyalty_program | 268037845 | 472385682 | 204347837 | 422 | deep_crisis | — |
| coffeebot | BAD | uptime_exposed | coffeebot_d:coffeebot_d | NONE | 307972938 | 472385682 | 164412744 | 349 | deep_crisis | — |
| coffeebot | BBA | repair_backlog, uptime_exposed | coffeebot_a:coffeebot_a | service_reserve | 97712649 | 472385682 | 374673033 | 732 | near_bankruptcy | — |
| coffeebot | BBB | repair_backlog, uptime_exposed | coffeebot_b:customer_churn | service_reserve | 0 | 496421467 | 496421467 | 913 | bankrupt | 8 |
| coffeebot | BBC | repair_backlog, uptime_exposed | coffeebot_c:coffeebot_c | service_reserve, loyalty_program | 76987712 | 472385682 | 395397970 | 766 | near_bankruptcy | — |
| coffeebot | BBD | repair_backlog, uptime_exposed | coffeebot_d:coffeebot_d | service_reserve | 122742427 | 472385682 | 349643255 | 685 | near_bankruptcy | — |
| coffeebot | BCA | uptime_exposed | coffeebot_a:coffeebot_a | loyalty_program | 266845411 | 472385682 | 205540271 | 431 | deep_crisis | — |
| coffeebot | BCB | uptime_exposed | coffeebot_b:customer_churn | loyalty_program | 216598802 | 472385682 | 255786880 | 530 | near_bankruptcy | — |
| coffeebot | BCC | uptime_exposed | coffeebot_c:coffeebot_c | loyalty_program | 306505213 | 472385682 | 165880469 | 339 | deep_crisis | — |
| coffeebot | BCD | uptime_exposed | coffeebot_d:coffeebot_d | loyalty_program | 287455805 | 472385682 | 184929877 | 383 | deep_crisis | — |
| coffeebot | BDA | uptime_exposed | coffeebot_a:coffeebot_a | NONE | 317705410 | 472385682 | 154680272 | 340 | deep_crisis | — |
| coffeebot | BDB | uptime_exposed | coffeebot_b:customer_churn | NONE | 273810939 | 472385682 | 198574743 | 430 | deep_crisis | — |
| coffeebot | BDC | uptime_exposed | coffeebot_c:coffeebot_c | loyalty_program | 297306488 | 472385682 | 175079194 | 366 | deep_crisis | — |
| coffeebot | BDD | uptime_exposed | coffeebot_d:coffeebot_d | NONE | 362309831 | 472385682 | 110075851 | 230 | deep_crisis | — |
| coffeebot | CAA | price_pressure | coffeebot_a:coffeebot_a | NONE | 301834348 | 472385682 | 170551334 | 360 | deep_crisis | — |
| coffeebot | CAB | price_pressure | coffeebot_b:customer_churn | NONE | 226500760 | 472385682 | 245884922 | 514 | deep_crisis | — |
| coffeebot | CAC | price_pressure | coffeebot_c:coffeebot_c | loyalty_program | 256173764 | 472385682 | 216211918 | 443 | deep_crisis | — |
| coffeebot | CAD | price_pressure | coffeebot_d:coffeebot_d | NONE | 296108857 | 472385682 | 176276825 | 371 | deep_crisis | — |
| coffeebot | CBA | price_pressure | coffeebot_a:coffeebot_a | NONE | 243838804 | 472385682 | 228546878 | 474 | deep_crisis | — |
| coffeebot | CBB | price_pressure | coffeebot_b:customer_churn | NONE | 224549441 | 472385682 | 247836241 | 512 | deep_crisis | — |
| coffeebot | CBC | price_pressure | coffeebot_c:coffeebot_c | loyalty_program | 223294671 | 472385682 | 249091011 | 504 | deep_crisis | — |
| coffeebot | CBD | price_pressure | coffeebot_d:coffeebot_d | NONE | 270614113 | 472385682 | 201771569 | 416 | deep_crisis | — |
| coffeebot | CCA | margin_squeeze, price_pressure | coffeebot_a:coffeebot_a | loyalty_program | 189541755 | 472385682 | 282843927 | 571 | near_bankruptcy | — |
| coffeebot | CCB | margin_squeeze, price_pressure | coffeebot_b:customer_churn | loyalty_program | 139295146 | 472385682 | 333090536 | 664 | near_bankruptcy | — |
| coffeebot | CCC | margin_squeeze, price_pressure | coffeebot_c:coffeebot_c | loyalty_program | 96205571 | 472385682 | 376180111 | 741 | near_bankruptcy | — |
| coffeebot | CCD | margin_squeeze, price_pressure | coffeebot_d:coffeebot_d | loyalty_program | 204871409 | 472385682 | 267514273 | 539 | deep_crisis | — |
| coffeebot | CDA | price_pressure | coffeebot_a:coffeebot_a | NONE | 305841329 | 472385682 | 166544353 | 361 | deep_crisis | — |
| coffeebot | CDB | price_pressure | coffeebot_b:customer_churn | NONE | 261946858 | 472385682 | 210438824 | 450 | deep_crisis | — |
| coffeebot | CDC | price_pressure | coffeebot_c:coffeebot_c | loyalty_program | 285442407 | 472385682 | 186943275 | 387 | deep_crisis | — |
| coffeebot | CDD | price_pressure | coffeebot_d:coffeebot_d | NONE | 350445750 | 472385682 | 121939932 | 252 | deep_crisis | — |
| coffeebot | DAA | — | coffeebot_a:coffeebot_a | NONE | 319149494 | 472385682 | 153236188 | 329 | deep_crisis | — |
| coffeebot | DAB | — | coffeebot_b:customer_churn | NONE | 243815906 | 472385682 | 228569776 | 484 | deep_crisis | — |
| coffeebot | DAC | — | coffeebot_c:coffeebot_c | loyalty_program | 273488910 | 472385682 | 198896772 | 412 | deep_crisis | — |
| coffeebot | DAD | — | coffeebot_d:coffeebot_d | NONE | 313424003 | 472385682 | 158961679 | 340 | deep_crisis | — |
| coffeebot | DBA | — | coffeebot_a:coffeebot_a | NONE | 261153950 | 472385682 | 211231732 | 444 | deep_crisis | — |
| coffeebot | DBB | — | coffeebot_b:customer_churn | NONE | 241864587 | 472385682 | 230521095 | 482 | deep_crisis | — |
| coffeebot | DBC | — | coffeebot_c:coffeebot_c | loyalty_program | 240609817 | 472385682 | 231775865 | 473 | deep_crisis | — |
| coffeebot | DBD | — | coffeebot_d:coffeebot_d | NONE | 287929259 | 472385682 | 184456423 | 385 | deep_crisis | — |
| coffeebot | DCA | — | coffeebot_a:coffeebot_a | loyalty_program | 272296476 | 472385682 | 200089206 | 421 | deep_crisis | — |
| coffeebot | DCB | — | coffeebot_b:customer_churn | loyalty_program | 222049867 | 472385682 | 250335815 | 521 | deep_crisis | — |
| coffeebot | DCC | — | coffeebot_c:coffeebot_c | loyalty_program | 311956278 | 472385682 | 160429404 | 329 | deep_crisis | — |
| coffeebot | DCD | — | coffeebot_d:coffeebot_d | loyalty_program | 292906870 | 472385682 | 179478812 | 374 | deep_crisis | — |
| coffeebot | DDA | — | coffeebot_a:coffeebot_a | NONE | 323156475 | 472385682 | 149229207 | 330 | deep_crisis | — |
| coffeebot | DDB | — | coffeebot_b:customer_churn | NONE | 279262004 | 472385682 | 193123678 | 421 | deep_crisis | — |
| coffeebot | DDC | — | coffeebot_c:coffeebot_c | loyalty_program | 302757553 | 472385682 | 169628129 | 356 | deep_crisis | — |
| coffeebot | DDD | — | coffeebot_d:coffeebot_d | NONE | 367760896 | 472385682 | 104624786 | 220 | survived | — |
| foodrover | AAA | route_restricted, route_scrutiny | foodrover_a:foodrover_a | route_rebuild | 65809662 | 537473577 | 471663915 | 804 | near_bankruptcy | — |
| foodrover | AAB | route_restricted, route_scrutiny | foodrover_b:customer_churn | route_rebuild | 90356970 | 537473577 | 447116607 | 767 | near_bankruptcy | — |
| foodrover | AAC | route_restricted, route_scrutiny | foodrover_c:foodrover_c | route_rebuild | 105614272 | 537473577 | 431859305 | 744 | near_bankruptcy | — |
| foodrover | AAD | route_restricted, route_scrutiny | foodrover_d:foodrover_d | route_rebuild | 191652183 | 537473577 | 345821394 | 602 | near_bankruptcy | — |
| foodrover | ABA | route_scrutiny | foodrover_a:foodrover_a | NONE | 233580405 | 537473577 | 303893172 | 548 | near_bankruptcy | — |
| foodrover | ABB | route_scrutiny | foodrover_b:customer_churn | NONE | 236796481 | 537473577 | 300677096 | 542 | near_bankruptcy | — |
| foodrover | ABC | route_scrutiny | foodrover_c:foodrover_c | NONE | 205334454 | 537473577 | 332139123 | 595 | near_bankruptcy | — |
| foodrover | ABD | route_scrutiny | foodrover_d:foodrover_d | NONE | 304511908 | 537473577 | 232961669 | 415 | deep_crisis | — |
| foodrover | ACA | route_scrutiny | foodrover_a:foodrover_a | NONE | 259067744 | 537473577 | 278405833 | 509 | deep_crisis | — |
| foodrover | ACB | route_scrutiny | foodrover_b:customer_churn | NONE | 216904507 | 537473577 | 320569070 | 578 | near_bankruptcy | — |
| foodrover | ACC | route_scrutiny | foodrover_c:foodrover_c | restaurant_retention | 269830165 | 537473577 | 267643412 | 475 | deep_crisis | — |
| foodrover | ACD | route_scrutiny | foodrover_d:foodrover_d | NONE | 325082946 | 537473577 | 212390631 | 382 | deep_crisis | — |
| foodrover | ADA | route_scrutiny | foodrover_a:foodrover_a | NONE | 348375142 | 537473577 | 189098435 | 366 | deep_crisis | — |
| foodrover | ADB | route_scrutiny | foodrover_b:customer_churn | NONE | 308141367 | 537473577 | 229332210 | 437 | deep_crisis | — |
| foodrover | ADC | route_scrutiny | foodrover_c:foodrover_c | restaurant_retention | 317572406 | 537473577 | 219901171 | 406 | deep_crisis | — |
| foodrover | ADD | route_scrutiny | foodrover_d:foodrover_d | NONE | 442548194 | 537473577 | 94925383 | 147 | survived | — |
| foodrover | BAA | battery_pressure | foodrover_a:foodrover_a | NONE | 290770782 | 537473577 | 246702795 | 451 | deep_crisis | — |
| foodrover | BAB | battery_pressure | foodrover_b:customer_churn | NONE | 211077525 | 537473577 | 326396052 | 586 | near_bankruptcy | — |
| foodrover | BAC | battery_pressure | foodrover_c:foodrover_c | NONE | 225081670 | 537473577 | 312391907 | 565 | near_bankruptcy | — |
| foodrover | BAD | battery_pressure | foodrover_d:foodrover_d | NONE | 320658915 | 537473577 | 216814662 | 387 | deep_crisis | — |
| foodrover | BBA | battery_backlog, battery_pressure | foodrover_a:foodrover_a | battery_reserve | 40176047 | 537473577 | 497297530 | 840 | near_bankruptcy | — |
| foodrover | BBB | battery_backlog, battery_pressure | foodrover_b:customer_churn | battery_reserve | 0 | 563934235 | 563934235 | 913 | bankrupt | 8 |
| foodrover | BBC | battery_backlog, battery_pressure | foodrover_c:foodrover_c | battery_reserve | 13280481 | 537473577 | 524193096 | 880 | near_bankruptcy | — |
| foodrover | BBD | battery_backlog, battery_pressure | foodrover_d:foodrover_d | battery_reserve | 107355961 | 537473577 | 430117616 | 733 | near_bankruptcy | — |
| foodrover | BCA | battery_pressure | foodrover_a:foodrover_a | NONE | 240565644 | 537473577 | 296907933 | 537 | near_bankruptcy | — |
| foodrover | BCB | battery_pressure | foodrover_b:customer_churn | NONE | 198402407 | 537473577 | 339071170 | 605 | near_bankruptcy | — |
| foodrover | BCC | battery_pressure | foodrover_c:foodrover_c | restaurant_retention | 251328065 | 537473577 | 286145512 | 504 | deep_crisis | — |
| foodrover | BCD | battery_pressure | foodrover_d:foodrover_d | NONE | 306580846 | 537473577 | 230892731 | 412 | deep_crisis | — |
| foodrover | BDA | battery_pressure | foodrover_a:foodrover_a | NONE | 329873042 | 537473577 | 207600535 | 395 | deep_crisis | — |
| foodrover | BDB | battery_pressure | foodrover_b:customer_churn | NONE | 289639267 | 537473577 | 247834310 | 465 | deep_crisis | — |
| foodrover | BDC | battery_pressure | foodrover_c:foodrover_c | restaurant_retention | 299070306 | 537473577 | 238403271 | 434 | deep_crisis | — |
| foodrover | BDD | battery_pressure | foodrover_d:foodrover_d | NONE | 424046094 | 537473577 | 113427483 | 179 | survived | — |
| foodrover | CAA | competitor_trial | foodrover_a:foodrover_a | NONE | 296509676 | 537473577 | 240963901 | 442 | deep_crisis | — |
| foodrover | CAB | competitor_trial | foodrover_b:customer_churn | NONE | 216816419 | 537473577 | 320657158 | 577 | near_bankruptcy | — |
| foodrover | CAC | competitor_trial | foodrover_c:foodrover_c | NONE | 230820564 | 537473577 | 306653013 | 556 | near_bankruptcy | — |
| foodrover | CAD | competitor_trial | foodrover_d:foodrover_d | NONE | 326397809 | 537473577 | 211075768 | 377 | deep_crisis | — |
| foodrover | CBA | competitor_trial | foodrover_a:foodrover_a | NONE | 220817199 | 537473577 | 316656378 | 567 | near_bankruptcy | — |
| foodrover | CBB | competitor_trial | foodrover_b:customer_churn | NONE | 224033275 | 537473577 | 313440302 | 561 | near_bankruptcy | — |
| foodrover | CBC | competitor_trial | foodrover_c:foodrover_c | NONE | 192571248 | 537473577 | 344902329 | 614 | near_bankruptcy | — |
| foodrover | CBD | competitor_trial | foodrover_d:foodrover_d | NONE | 291748702 | 537473577 | 245724875 | 435 | deep_crisis | — |
| foodrover | CCA | competitor_trial, restaurant_switch | foodrover_a:foodrover_a | restaurant_retention | 120200556 | 537473577 | 417273021 | 722 | near_bankruptcy | — |
| foodrover | CCB | competitor_trial, restaurant_switch | foodrover_b:customer_churn | restaurant_retention | 78990366 | 537473577 | 458483211 | 784 | near_bankruptcy | — |
| foodrover | CCC | competitor_trial, restaurant_switch | foodrover_c:foodrover_c | restaurant_retention, restaurant_retention | 46219907 | 537473577 | 491253670 | 833 | near_bankruptcy | — |
| foodrover | CCD | competitor_trial, restaurant_switch | foodrover_d:foodrover_d | restaurant_retention | 175147403 | 537473577 | 362326174 | 633 | near_bankruptcy | — |
| foodrover | CDA | competitor_trial | foodrover_a:foodrover_a | NONE | 335611936 | 537473577 | 201861641 | 386 | deep_crisis | — |
| foodrover | CDB | competitor_trial | foodrover_b:customer_churn | NONE | 295378161 | 537473577 | 242095416 | 456 | deep_crisis | — |
| foodrover | CDC | competitor_trial | foodrover_c:foodrover_c | restaurant_retention | 304809200 | 537473577 | 232664377 | 425 | deep_crisis | — |
| foodrover | CDD | competitor_trial | foodrover_d:foodrover_d | NONE | 429784988 | 537473577 | 107688589 | 169 | survived | — |
| foodrover | DAA | — | foodrover_a:foodrover_a | NONE | 324292997 | 537473577 | 213180580 | 399 | deep_crisis | — |
| foodrover | DAB | — | foodrover_b:customer_churn | NONE | 244599740 | 537473577 | 292873837 | 536 | near_bankruptcy | — |
| foodrover | DAC | — | foodrover_c:foodrover_c | NONE | 258603885 | 537473577 | 278869692 | 515 | near_bankruptcy | — |
| foodrover | DAD | — | foodrover_d:foodrover_d | NONE | 354181130 | 537473577 | 183292447 | 333 | deep_crisis | — |
| foodrover | DBA | — | foodrover_a:foodrover_a | NONE | 248600520 | 537473577 | 288873057 | 525 | deep_crisis | — |
| foodrover | DBB | — | foodrover_b:customer_churn | NONE | 251816596 | 537473577 | 285656981 | 519 | deep_crisis | — |
| foodrover | DBC | — | foodrover_c:foodrover_c | NONE | 220354569 | 537473577 | 317119008 | 573 | near_bankruptcy | — |
| foodrover | DBD | — | foodrover_d:foodrover_d | NONE | 319532023 | 537473577 | 217941554 | 391 | deep_crisis | — |
| foodrover | DCA | — | foodrover_a:foodrover_a | NONE | 274087859 | 537473577 | 263385718 | 486 | deep_crisis | — |
| foodrover | DCB | — | foodrover_b:customer_churn | NONE | 231924622 | 537473577 | 305548955 | 556 | near_bankruptcy | — |
| foodrover | DCC | — | foodrover_c:foodrover_c | restaurant_retention | 284850280 | 537473577 | 252623297 | 451 | deep_crisis | — |
| foodrover | DCD | — | foodrover_d:foodrover_d | NONE | 340103061 | 537473577 | 197370516 | 358 | deep_crisis | — |
| foodrover | DDA | — | foodrover_a:foodrover_a | NONE | 363395257 | 537473577 | 174078320 | 343 | deep_crisis | — |
| foodrover | DDB | — | foodrover_b:customer_churn | NONE | 323161482 | 537473577 | 214312095 | 414 | deep_crisis | — |
| foodrover | DDC | — | foodrover_c:foodrover_c | restaurant_retention | 332592521 | 537473577 | 204881056 | 382 | deep_crisis | — |
| foodrover | DDD | — | foodrover_d:foodrover_d | NONE | 457568309 | 537473577 | 79905268 | 122 | survived | — |
| studygenie | AAA | quality_doubt, trust_crisis | studygenie_a:studygenie_a | quality_audit | 91297446 | 363347068 | 272049622 | 696 | near_bankruptcy | — |
| studygenie | AAB | quality_doubt, trust_crisis | studygenie_b:customer_churn | quality_audit | 126792766 | 363347068 | 236554302 | 602 | deep_crisis | — |
| studygenie | AAC | quality_doubt, trust_crisis | studygenie_c:studygenie_c | quality_audit | 126427925 | 363347068 | 236919143 | 603 | deep_crisis | — |
| studygenie | AAD | quality_doubt, trust_crisis | studygenie_d:studygenie_d | quality_audit | 150584541 | 363347068 | 212762527 | 530 | deep_crisis | — |
| studygenie | ABA | quality_doubt | studygenie_a:studygenie_a | NONE | 199081999 | 363347068 | 164265069 | 420 | deep_crisis | — |
| studygenie | ABB | quality_doubt | studygenie_b:customer_churn | NONE | 216421651 | 363347068 | 146925417 | 362 | deep_crisis | — |
| studygenie | ABC | quality_doubt | studygenie_c:studygenie_c | NONE | 195330191 | 363347068 | 168016877 | 433 | deep_crisis | — |
| studygenie | ABD | quality_doubt | studygenie_d:studygenie_d | NONE | 219608272 | 363347068 | 143738796 | 344 | deep_crisis | — |
| studygenie | ACA | quality_doubt | studygenie_a:studygenie_a | NONE | 205058982 | 363347068 | 158288086 | 407 | deep_crisis | — |
| studygenie | ACB | quality_doubt | studygenie_b:customer_churn | NONE | 202033382 | 363347068 | 161313686 | 418 | deep_crisis | — |
| studygenie | ACC | quality_doubt | studygenie_c:studygenie_c | NONE | 223593812 | 363347068 | 139753256 | 345 | deep_crisis | — |
| studygenie | ACD | quality_doubt | studygenie_d:studygenie_d | NONE | 223686834 | 363347068 | 139660234 | 338 | deep_crisis | — |
| studygenie | ADA | quality_doubt | studygenie_a:studygenie_a | NONE | 236196805 | 363347068 | 127150263 | 320 | deep_crisis | — |
| studygenie | ADB | quality_doubt | studygenie_b:customer_churn | NONE | 231100276 | 363347068 | 132246792 | 339 | deep_crisis | — |
| studygenie | ADC | quality_doubt | studygenie_c:studygenie_c | NONE | 228405267 | 363347068 | 134941801 | 348 | deep_crisis | — |
| studygenie | ADD | quality_doubt | studygenie_d:studygenie_d | NONE | 269838401 | 363347068 | 93508667 | 180 | survived | — |
| studygenie | BAA | api_pressure | studygenie_a:studygenie_a | NONE | 221782620 | 363347068 | 141564448 | 343 | deep_crisis | — |
| studygenie | BAB | api_pressure | studygenie_b:customer_churn | NONE | 195583237 | 363347068 | 167763831 | 433 | deep_crisis | — |
| studygenie | BAC | api_pressure | studygenie_c:studygenie_c | NONE | 195271538 | 363347068 | 168075530 | 434 | deep_crisis | — |
| studygenie | BAD | api_pressure | studygenie_d:studygenie_d | NONE | 220079617 | 363347068 | 143267451 | 344 | deep_crisis | — |
| studygenie | BBA | api_bottleneck, api_pressure | studygenie_a:studygenie_a | backup_provider | 46051029 | 363347068 | 317296039 | 793 | near_bankruptcy | — |
| studygenie | BBB | api_bottleneck, api_pressure | studygenie_b:customer_churn | backup_provider | 0 | 367203008 | 367203008 | 913 | bankrupt | 8 |
| studygenie | BBC | api_bottleneck, api_pressure | studygenie_c:studygenie_c | backup_provider | 42488775 | 363347068 | 320858293 | 802 | near_bankruptcy | — |
| studygenie | BBD | api_bottleneck, api_pressure | studygenie_d:studygenie_d | backup_provider | 65331359 | 363347068 | 298015709 | 743 | near_bankruptcy | — |
| studygenie | BCA | api_pressure | studygenie_a:studygenie_a | NONE | 198339163 | 363347068 | 165007905 | 424 | deep_crisis | — |
| studygenie | BCB | api_pressure | studygenie_b:customer_churn | NONE | 195313563 | 363347068 | 168033505 | 434 | deep_crisis | — |
| studygenie | BCC | api_pressure | studygenie_c:studygenie_c | NONE | 216873993 | 363347068 | 146473075 | 362 | deep_crisis | — |
| studygenie | BCD | api_pressure | studygenie_d:studygenie_d | NONE | 216967015 | 363347068 | 146380053 | 355 | deep_crisis | — |
| studygenie | BDA | api_pressure | studygenie_a:studygenie_a | NONE | 229476986 | 363347068 | 133870082 | 337 | deep_crisis | — |
| studygenie | BDB | api_pressure | studygenie_b:customer_churn | NONE | 224380457 | 363347068 | 138966611 | 355 | deep_crisis | — |
| studygenie | BDC | api_pressure | studygenie_c:studygenie_c | NONE | 221685448 | 363347068 | 141661620 | 365 | deep_crisis | — |
| studygenie | BDD | api_pressure | studygenie_d:studygenie_d | NONE | 263118582 | 363347068 | 100228486 | 193 | survived | — |
| studygenie | CAA | exam_trial | studygenie_a:studygenie_a | NONE | 227989911 | 363347068 | 135357157 | 327 | survived | — |
| studygenie | CAB | exam_trial | studygenie_b:customer_churn | NONE | 201790528 | 363347068 | 161556540 | 418 | deep_crisis | — |
| studygenie | CAC | exam_trial | studygenie_c:studygenie_c | NONE | 201478829 | 363347068 | 161868239 | 419 | deep_crisis | — |
| studygenie | CAD | exam_trial | studygenie_d:studygenie_d | NONE | 226286908 | 363347068 | 137060160 | 328 | survived | — |
| studygenie | CBA | exam_trial | studygenie_a:studygenie_a | NONE | 198569471 | 363347068 | 164777597 | 422 | deep_crisis | — |
| studygenie | CBB | exam_trial | studygenie_b:customer_churn | NONE | 215909123 | 363347068 | 147437945 | 363 | deep_crisis | — |
| studygenie | CBC | exam_trial | studygenie_c:studygenie_c | NONE | 194817663 | 363347068 | 168529405 | 434 | deep_crisis | — |
| studygenie | CBD | exam_trial | studygenie_d:studygenie_d | NONE | 219095744 | 363347068 | 144251324 | 345 | deep_crisis | — |
| studygenie | CCA | cohort_churn, exam_trial | studygenie_a:studygenie_a | student_retention | 118707327 | 363347068 | 244639741 | 627 | near_bankruptcy | — |
| studygenie | CCB | cohort_churn, exam_trial | studygenie_b:customer_churn | student_retention | 116995449 | 363347068 | 246351619 | 632 | near_bankruptcy | — |
| studygenie | CCC | cohort_churn, exam_trial | studygenie_c:studygenie_c | student_retention, student_retention | 62414332 | 363347068 | 300932736 | 762 | near_bankruptcy | — |
| studygenie | CCD | cohort_churn, exam_trial | studygenie_d:studygenie_d | student_retention | 132817394 | 363347068 | 230529674 | 589 | deep_crisis | — |
| studygenie | CDA | exam_trial | studygenie_a:studygenie_a | NONE | 235684277 | 363347068 | 127662791 | 322 | deep_crisis | — |
| studygenie | CDB | exam_trial | studygenie_b:customer_churn | NONE | 230587748 | 363347068 | 132759320 | 340 | deep_crisis | — |
| studygenie | CDC | exam_trial | studygenie_c:studygenie_c | NONE | 227892739 | 363347068 | 135454329 | 350 | deep_crisis | — |
| studygenie | CDD | exam_trial | studygenie_d:studygenie_d | NONE | 269325873 | 363347068 | 94021195 | 181 | survived | — |
| studygenie | DAA | — | studygenie_a:studygenie_a | NONE | 241520658 | 363347068 | 121826410 | 293 | survived | — |
| studygenie | DAB | — | studygenie_b:customer_churn | NONE | 215321275 | 363347068 | 148025793 | 386 | deep_crisis | — |
| studygenie | DAC | — | studygenie_c:studygenie_c | NONE | 215009576 | 363347068 | 148337492 | 387 | deep_crisis | — |
| studygenie | DAD | — | studygenie_d:studygenie_d | NONE | 239817655 | 363347068 | 123529413 | 294 | survived | — |
| studygenie | DBA | — | studygenie_a:studygenie_a | NONE | 212100218 | 363347068 | 151246850 | 389 | deep_crisis | — |
| studygenie | DBB | — | studygenie_b:customer_churn | NONE | 229439870 | 363347068 | 133907198 | 330 | deep_crisis | — |
| studygenie | DBC | — | studygenie_c:studygenie_c | NONE | 208348410 | 363347068 | 154998658 | 402 | deep_crisis | — |
| studygenie | DBD | — | studygenie_d:studygenie_d | NONE | 232626491 | 363347068 | 130720577 | 311 | survived | — |
| studygenie | DCA | — | studygenie_a:studygenie_a | NONE | 218077201 | 363347068 | 145269867 | 376 | deep_crisis | — |
| studygenie | DCB | — | studygenie_b:customer_churn | NONE | 215051601 | 363347068 | 148295467 | 387 | deep_crisis | — |
| studygenie | DCC | — | studygenie_c:studygenie_c | NONE | 236612031 | 363347068 | 126735037 | 313 | deep_crisis | — |
| studygenie | DCD | — | studygenie_d:studygenie_d | NONE | 236705053 | 363347068 | 126642015 | 306 | survived | — |
| studygenie | DDA | — | studygenie_a:studygenie_a | NONE | 249215024 | 363347068 | 114132044 | 289 | deep_crisis | — |
| studygenie | DDB | — | studygenie_b:customer_churn | NONE | 244118495 | 363347068 | 119228573 | 308 | deep_crisis | — |
| studygenie | DDC | — | studygenie_c:studygenie_c | NONE | 241423486 | 363347068 | 121923582 | 317 | deep_crisis | — |
| studygenie | DDD | — | studygenie_d:studygenie_d | NONE | 282856620 | 363347068 | 80490448 | 155 | survived | — |

## Balance observations

Approved coefficients were not tuned. CoffeeBot, FoodRover and StudyGenie B chains reach 913; PetMind has no bankrupt path. DDD is markedly weaker than BBB on all four. Review product coefficients before treating the shared leaderboard as fair.

## Local deterministic round benchmark

1000 rounds with `coffeebot_r1_a` for `coffeebot`; per round: mean 0.3035 ms, median 0.3022 ms, p95 0.3287 ms, max 0.4116 ms. Peak process RSS observed: 30.66 MiB.

The four v2 catalogs use explicit effects and new ending thresholds; six legacy catalogs retain v1 behavior. This local benchmark is not a target-host benchmark.
