# Deterministic attack catalog balance report

Catalog `2.0.0`: 10 startups, 4 choices per round, 640 reachable terminal paths.
Scores use the existing game scoring function. A bankrupt branch ends immediately; no later choices are counted.
These are local engine results, not a production-host CPU or memory benchmark.

| Startup | Paths | Score min | Score max | P25 | Mean | Median | P75 | Bankruptcy | Technical best | Technical worst |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| coffeebot | 64 | 220 | 913 | 360 | 454.56 | 430.5 | 512 | 1.56% | 913 (coffeebot_r1_b → coffeebot_r2_b → coffeebot_r3_b) | 220 (coffeebot_r1_d → coffeebot_r2_d → coffeebot_r3_d) |
| petmind | 64 | 259 | 800 | 391 | 466.03 | 451.5 | 519 | 0.00% | 800 (petmind_r1_b → petmind_r2_b → petmind_r3_b) | 259 (petmind_r1_a → petmind_r2_c → petmind_r3_c) |
| foodrover | 64 | 122 | 913 | 399 | 511.09 | 506.5 | 578 | 3.13% | 913 (foodrover_r1_b → foodrover_r2_b → foodrover_r3_b) | 122 (foodrover_r1_d → foodrover_r2_d → foodrover_r3_d) |
| studygenie | 64 | 155 | 913 | 328 | 414.86 | 362.5 | 433 | 1.56% | 913 (studygenie_r1_b → studygenie_r2_b → studygenie_r3_b) | 155 (studygenie_r1_d → studygenie_r2_d → studygenie_r3_d) |
| sleepwork | 64 | 195 | 900 | 296 | 349.17 | 323.0 | 357 | 1.56% | 900 (sleepwork_r1_2 → sleepwork_r2_2 → sleepwork_r3_2) | 195 (sleepwork_r1_2 → sleepwork_r2_3 → sleepwork_r3_3) |
| fitmirror | 64 | 108 | 712 | 238 | 317.78 | 315.0 | 363 | 0.00% | 712 (fitmirror_r1_2 → fitmirror_r2_2 → fitmirror_r3_2) | 108 (fitmirror_r1_4 → fitmirror_r2_2 → fitmirror_r3_2) |
| cloudkitchen | 64 | 90 | 900 | 244 | 360.95 | 318.0 | 419 | 1.56% | 900 (cloudkitchen_r1_2 → cloudkitchen_r2_2 → cloudkitchen_r3_2) | 90 (cloudkitchen_r1_4 → cloudkitchen_r2_4 → cloudkitchen_r3_4) |
| agrodrone | 64 | 143 | 900 | 343 | 437.2 | 429.0 | 492 | 1.56% | 900 (agrodrone_r1_2 → agrodrone_r2_2 → agrodrone_r3_2) | 143 (agrodrone_r1_4 → agrodrone_r2_4 → agrodrone_r3_4) |
| moodads | 64 | 126 | 913 | 232 | 326.92 | 271.0 | 356 | 1.56% | 913 (moodads_r1_2 → moodads_r2_2 → moodads_r3_2) | 126 (moodads_r1_4 → moodads_r2_4 → moodads_r3_4) |
| renteverything | 64 | 156 | 900 | 306 | 389.12 | 343.5 | 390 | 1.56% | 900 (renteverything_r1_1 → renteverything_r2_1 → renteverything_r3_1) | 156 (renteverything_r1_4 → renteverything_r2_4 → renteverything_r3_4) |

## All ten v2 startups: exhaustive outcome summary

Each startup has 64 choice sequences. Cash and damage are in RUB below; the raw path table retains kopeks. Player damage uses baseline at the same terminal month; score A uses baseline M9, including when bankruptcy ends a game early.
A bankrupt game stops immediately. The listed sequence is the actual played prefix.

| Startup | Min | Max | Mean | Median | Bankrupt | Near | Deep | Survived | Best coherent | DDD | Mixed mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---:|
| coffeebot | 220 | 913 | 454.56 | 430.5 | 1.56% | 15.63% | 81.25% | 1.56% | BBB: 913 | 220 | 441.82 |
| petmind | 259 | 800 | 466.03 | 451.5 | 0.00% | 43.75% | 56.25% | 0.00% | BBB: 800 | 525 | 450.97 |
| foodrover | 122 | 913 | 511.09 | 506.5 | 3.13% | 42.19% | 48.44% | 6.25% | BBB: 913 | 122 | 499.52 |
| studygenie | 155 | 913 | 414.86 | 362.5 | 1.56% | 10.94% | 71.88% | 15.63% | BBB: 913 | 155 | 398.18 |
| sleepwork | 195 | 900 | 349.17 | 323.0 | 1.56% | 3.13% | 90.63% | 4.69% | BBB: 900 | 243 | 334.23 |
| fitmirror | 108 | 712 | 317.78 | 315.0 | 0.00% | 4.69% | 59.38% | 35.94% | BBB: 712 | 216 | 302.52 |
| cloudkitchen | 90 | 900 | 360.95 | 318.0 | 1.56% | 4.69% | 50.00% | 43.75% | BBB: 900 | 90 | 344.12 |
| agrodrone | 143 | 900 | 437.20 | 429.0 | 1.56% | 12.50% | 79.69% | 6.25% | BBB: 900 | 143 | 425.42 |
| moodads | 126 | 913 | 326.92 | 271.0 | 1.56% | 4.69% | 39.06% | 54.69% | BBB: 913 | 126 | 308.42 |
| renteverything | 156 | 900 | 389.12 | 343.5 | 1.56% | 14.06% | 78.13% | 6.25% | AAA: 900 | 156 | 370.82 |

## Six-startup first-pass and final record

The first exhaustive pass is the final pass for SleepWork, FitMirror, CloudKitchen, AgroDrone, MoodAds and RentEverything. No permitted tuning field was changed, so both columns are the preserved first-pass and final result.

| Startup | First mean | Final mean | First bankruptcy | Final bankruptcy | First DDD | Final DDD |
|---|---:|---:|---:|---:|---:|---:|
| sleepwork | 349.17 | 349.17 | 1.56% | 1.56% | 243 | 243 |
| fitmirror | 317.78 | 317.78 | 0.00% | 0.00% | 216 | 216 |
| cloudkitchen | 360.95 | 360.95 | 1.56% | 1.56% | 90 | 90 |
| agrodrone | 437.2 | 437.2 | 1.56% | 1.56% | 143 | 143 |
| moodads | 326.92 | 326.92 | 1.56% | 1.56% | 126 | 126 |
| renteverything | 389.12 | 389.12 | 1.56% | 1.56% | 156 | 156 |

## First-four shared-engine regression

The four reference catalogs were byte-for-byte unchanged. Their before values are from the preceding v2 report; after values include only the shared defense max-use and inevitable-bankruptcy selection fixes.

| Startup | Before mean | After mean | Before bankruptcy | After bankruptcy |
|---|---:|---:|---:|---:|
| petmind | 463.28 | 466.03 | 0.00% | 0.00% |
| coffeebot | 454.56 | 454.56 | 1.56% | 1.56% |
| foodrover | 510.05 | 511.09 | 1.56% | 3.13% |
| studygenie | 412.77 | 414.86 | 1.56% | 1.56% |

## Explicit chains and prerequisite bypass controls

Controls ABB, CBB, DBB and AAC, ABC, ACB verify that a later same-letter card gets only base effects when the prerequisite chain was broken.

| Startup | Path | Score | Status | Cash RUB | Damage RUB | Flags | Defenses | Bankruptcy month |
|---|---|---:|---|---:|---:|---|---|---:|
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
| petmind | AAA | 648 | near_bankruptcy | 1,402,690 | 2,997,310 | accuracy_doubted, trust_crisis | independent_audit | — |
| petmind | BBB | 800 | near_bankruptcy | 566,968 | 3,833,032 | factory_pressure, stockout | NONE | — |
| petmind | CCC | 795 | near_bankruptcy | 615,162 | 3,784,838 | churn_wave, free_alternative | retention_offer | — |
| petmind | DDD | 525 | near_bankruptcy | 2,067,992 | 2,332,008 | — | NONE | — |
| petmind | ABB | 331 | deep_crisis | 3,004,485 | 1,395,515 | accuracy_doubted | NONE | — |
| petmind | CBB | 319 | deep_crisis | 3,070,341 | 1,329,659 | free_alternative | NONE | — |
| petmind | DBB | 352 | deep_crisis | 2,892,530 | 1,507,470 | — | NONE | — |
| petmind | AAC | 531 | near_bankruptcy | 1,983,298 | 2,416,702 | accuracy_doubted, trust_crisis | independent_audit | — |
| petmind | ABC | 368 | deep_crisis | 2,838,669 | 1,561,331 | accuracy_doubted | NONE | — |
| petmind | ACB | 338 | deep_crisis | 3,013,261 | 1,386,739 | accuracy_doubted | NONE | — |
| foodrover | AAA | 804 | near_bankruptcy | 658,097 | 4,716,639 | route_restricted, route_scrutiny | route_rebuild | — |
| foodrover | BBB | 913 | bankrupt | 0 | 5,639,342 | battery_backlog, battery_pressure | battery_reserve | 8 |
| foodrover | CCC | 900 | bankrupt | 0 | 5,374,736 | competitor_trial, restaurant_switch | restaurant_retention, cost_cut | 9 |
| foodrover | DDD | 122 | survived | 4,575,683 | 799,053 | — | NONE | — |
| foodrover | ABB | 542 | near_bankruptcy | 2,367,965 | 3,006,771 | route_scrutiny | NONE | — |
| foodrover | CBB | 561 | near_bankruptcy | 2,240,333 | 3,134,403 | competitor_trial | NONE | — |
| foodrover | DBB | 519 | deep_crisis | 2,518,166 | 2,856,570 | — | NONE | — |
| foodrover | AAC | 744 | near_bankruptcy | 1,056,143 | 4,318,593 | route_restricted, route_scrutiny | route_rebuild | — |
| foodrover | ABC | 595 | near_bankruptcy | 2,053,345 | 3,321,391 | route_scrutiny | NONE | — |
| foodrover | ACB | 578 | near_bankruptcy | 2,169,045 | 3,205,691 | route_scrutiny | NONE | — |
| studygenie | AAA | 696 | near_bankruptcy | 912,974 | 2,720,496 | quality_doubt, trust_crisis | quality_audit | — |
| studygenie | BBB | 913 | bankrupt | 0 | 3,672,030 | api_bottleneck, api_pressure | backup_provider | 8 |
| studygenie | CCC | 896 | near_bankruptcy | 17,855 | 3,615,616 | cohort_churn, exam_trial | student_retention, cost_cut | — |
| studygenie | DDD | 155 | survived | 2,828,566 | 804,904 | — | NONE | — |
| studygenie | ABB | 362 | deep_crisis | 2,164,217 | 1,469,254 | quality_doubt | NONE | — |
| studygenie | CBB | 363 | deep_crisis | 2,159,091 | 1,474,379 | exam_trial | NONE | — |
| studygenie | DBB | 330 | deep_crisis | 2,294,399 | 1,339,072 | — | NONE | — |
| studygenie | AAC | 603 | deep_crisis | 1,264,279 | 2,369,191 | quality_doubt, trust_crisis | quality_audit | — |
| studygenie | ABC | 433 | deep_crisis | 1,953,302 | 1,680,169 | quality_doubt | NONE | — |
| studygenie | ACB | 418 | deep_crisis | 2,020,334 | 1,613,137 | quality_doubt | NONE | — |
| sleepwork | AAA | 601 | near_bankruptcy | 1,436,319 | 2,428,207 | renewal_risk, utilization_exposed | flexible_lease | — |
| sleepwork | BBB | 900 | bankrupt | 0 | 3,864,526 | space_cost_exposed, space_reallocation | compact_redeploy, cost_cut | 9 |
| sleepwork | CCC | 549 | near_bankruptcy | 1,668,703 | 2,195,822 | no_hardware_trial, wellness_switch | digital_wellness | — |
| sleepwork | DDD | 243 | deep_crisis | 2,907,481 | 957,045 | — | price_retention | — |
| sleepwork | ABB | 292 | deep_crisis | 2,689,098 | 1,175,428 | utilization_exposed | NONE | — |
| sleepwork | CBB | 295 | deep_crisis | 2,680,004 | 1,184,521 | no_hardware_trial | NONE | — |
| sleepwork | DBB | 301 | deep_crisis | 2,652,724 | 1,211,802 | — | NONE | — |
| sleepwork | AAC | 472 | deep_crisis | 1,974,121 | 1,890,405 | renewal_risk, utilization_exposed | flexible_lease | — |
| sleepwork | ABC | 361 | deep_crisis | 2,470,722 | 1,393,804 | utilization_exposed | NONE | — |
| sleepwork | ACB | 320 | deep_crisis | 2,610,507 | 1,254,019 | utilization_exposed | digital_wellness | — |
| fitmirror | AAA | 614 | near_bankruptcy | 2,080,080 | 3,780,344 | affordability_crisis, price_pressure | financing_tradein | — |
| fitmirror | BBB | 712 | near_bankruptcy | 1,451,417 | 4,409,006 | retention_doubt, subscription_churn | bundled_subscription | — |
| fitmirror | CCC | 645 | near_bankruptcy | 1,866,087 | 3,994,336 | hardware_substitution, phone_substitute | mobile_mode | — |
| fitmirror | DDD | 216 | survived | 4,411,000 | 1,449,424 | — | NONE | — |
| fitmirror | ABB | 114 | survived | 4,904,146 | 956,277 | price_pressure | NONE | — |
| fitmirror | CBB | 112 | survived | 4,926,373 | 934,050 | phone_substitute | NONE | — |
| fitmirror | DBB | 108 | survived | 4,953,989 | 906,434 | — | NONE | — |
| fitmirror | AAC | 539 | deep_crisis | 2,546,187 | 3,314,236 | affordability_crisis, price_pressure | financing_tradein | — |
| fitmirror | ABC | 324 | deep_crisis | 3,961,191 | 1,899,232 | price_pressure | NONE | — |
| fitmirror | ACB | 246 | survived | 4,058,150 | 1,802,273 | price_pressure | mobile_mode | — |
| cloudkitchen | AAA | 779 | near_bankruptcy | 815,816 | 4,782,364 | discovery_crisis, ranking_pressure | direct_channel | — |
| cloudkitchen | BBB | 900 | bankrupt | 0 | 5,598,179 | menu_shortage, supply_pressure | second_supplier, cost_cut | 9 |
| cloudkitchen | CCC | 685 | near_bankruptcy | 1,444,914 | 4,153,265 | brand_substitution, menu_clone | unique_menu_loyalty | — |
| cloudkitchen | DDD | 90 | survived | 4,877,179 | 721,000 | — | NONE | — |
| cloudkitchen | ABB | 302 | deep_crisis | 3,332,989 | 2,265,191 | ranking_pressure | NONE | — |
| cloudkitchen | CBB | 308 | deep_crisis | 3,302,498 | 2,295,681 | menu_clone | NONE | — |
| cloudkitchen | DBB | 262 | survived | 3,557,182 | 2,040,997 | — | NONE | — |
| cloudkitchen | AAC | 652 | near_bankruptcy | 1,586,818 | 4,011,361 | discovery_crisis, ranking_pressure | direct_channel | — |
| cloudkitchen | ABC | 414 | deep_crisis | 2,984,094 | 2,614,085 | ranking_pressure | NONE | — |
| cloudkitchen | ACB | 406 | deep_crisis | 2,985,145 | 2,613,035 | ranking_pressure | NONE | — |
| agrodrone | AAA | 637 | near_bankruptcy | 1,584,079 | 3,228,613 | dealer_financing_loss, financing_pressure | seasonal_leasing | — |
| agrodrone | BBB | 900 | bankrupt | 0 | 4,812,692 | component_pressure, production_backlog | component_reserve | 9 |
| agrodrone | CCC | 776 | near_bankruptcy | 767,317 | 4,045,374 | satellite_trial, service_substitution | drone_as_a_service | — |
| agrodrone | DDD | 143 | survived | 4,000,564 | 812,128 | — | NONE | — |
| agrodrone | ABB | 451 | deep_crisis | 2,599,828 | 2,212,863 | financing_pressure | NONE | — |
| agrodrone | CBB | 442 | deep_crisis | 2,651,721 | 2,160,970 | satellite_trial | NONE | — |
| agrodrone | DBB | 425 | deep_crisis | 2,746,737 | 2,065,955 | — | NONE | — |
| agrodrone | AAC | 613 | near_bankruptcy | 1,715,630 | 3,097,061 | dealer_financing_loss, financing_pressure | seasonal_leasing | — |
| agrodrone | ABC | 504 | deep_crisis | 2,346,086 | 2,466,605 | financing_pressure | NONE | — |
| agrodrone | ACB | 518 | deep_crisis | 2,263,425 | 2,549,267 | financing_pressure | NONE | — |
| moodads | AAA | 759 | near_bankruptcy | 1,006,375 | 4,570,319 | privacy_doubt, privacy_review_wave | privacy_safe_mode | — |
| moodads | BBB | 913 | bankrupt | 0 | 5,498,811 | data_access_review, data_restricted | alternative_data | 8 |
| moodads | CCC | 620 | near_bankruptcy | 1,845,498 | 3,731,195 | contextual_migration, contextual_proof | contextual_mode | — |
| moodads | DDD | 126 | survived | 4,574,038 | 1,002,655 | — | analytics_bundle | — |
| moodads | ABB | 294 | deep_crisis | 3,341,264 | 2,235,429 | privacy_doubt | NONE | — |
| moodads | CBB | 299 | deep_crisis | 3,312,193 | 2,264,500 | contextual_proof | NONE | — |
| moodads | DBB | 273 | survived | 3,457,548 | 2,119,145 | — | NONE | — |
| moodads | AAC | 541 | deep_crisis | 2,267,690 | 3,309,003 | privacy_doubt, privacy_review_wave | privacy_safe_mode | — |
| moodads | ABC | 401 | deep_crisis | 3,022,906 | 2,553,787 | privacy_doubt | NONE | — |
| moodads | ACB | 375 | deep_crisis | 3,127,534 | 2,449,159 | privacy_doubt | NONE | — |
| renteverything | AAA | 900 | bankrupt | 0 | 4,585,500 | inventory_backlog, repair_pressure | repair_reserve, cost_cut | 9 |
| renteverything | BBB | 808 | near_bankruptcy | 534,532 | 4,050,968 | dispute_attention, dispute_wave | transparent_insurance | — |
| renteverything | CCC | 791 | near_bankruptcy | 657,483 | 3,928,017 | price_pressure, renter_churn | lower_deposit | — |
| renteverything | DDD | 156 | survived | 3,866,500 | 719,000 | — | NONE | — |
| renteverything | ABB | 350 | deep_crisis | 3,012,411 | 1,573,089 | repair_pressure | NONE | — |
| renteverything | CBB | 337 | deep_crisis | 3,087,925 | 1,497,575 | price_pressure | NONE | — |
| renteverything | DBB | 319 | deep_crisis | 3,183,797 | 1,401,703 | — | NONE | — |
| renteverything | AAC | 669 | near_bankruptcy | 1,295,023 | 3,290,477 | inventory_backlog, repair_pressure | repair_reserve | — |
| renteverything | ABC | 387 | deep_crisis | 2,847,079 | 1,738,421 | repair_pressure | NONE | — |
| renteverything | ACB | 403 | deep_crisis | 2,773,214 | 1,812,286 | repair_pressure | NONE | — |

## Matched BBB defense controls

The same BBB choices are simulated with normal deterministic defense selection and with defense forced to NONE; coefficients and incident costs are identical.

| Startup | Selected/no-defense cash RUB | Selected/no-defense bankruptcy month | Selected/no-defense total revenue RUB | Selected defense cost RUB | Selected/no-defense score |
|---|---:|---|---:|---:|---:|
| coffeebot | 0 / 0 | 8 / 8 | 15,145,166 / 14,512,771 | 600,000 | 913 / 913 |
| petmind | 566,968 / 566,968 | — / — | 16,824,240 / 16,824,240 | 0 | 800 / 800 |
| foodrover | 0 / 0 | 8 / 8 | 20,250,034 / 19,014,384 | 700,000 | 913 / 913 |
| studygenie | 0 / 0 | 8 / 8 | 9,382,648 / 8,875,963 | 500,000 | 913 / 913 |
| sleepwork | 0 / 0 | 9 / 9 | 11,140,950 / 10,736,536 | 812,500 | 900 / 900 |
| fitmirror | 1,451,417 / 786,536 | — / — | 19,097,487 / 17,756,406 | 180,000 | 712 / 798 |
| cloudkitchen | 0 / 0 | 9 / 9 | 20,944,631 / 20,159,626 | 1,012,500 | 900 / 900 |
| agrodrone | 0 / 0 | 9 / 9 | 16,351,394 / 15,778,517 | 650,000 | 900 / 900 |
| moodads | 0 / 0 | 8 / 8 | 10,720,894 / 9,971,126 | 450,000 | 913 / 913 |
| renteverything | 534,532 / 0 | — / 9 | 18,673,234 / 15,785,772 | 350,000 | 808 / 900 |

## All 64 paths per v2 startup

Monetary values in this table are integer kopeks; flags and defenses are server-side simulation observations.

| Startup | Choices | Combo flags | Active causes | Defenses | Final revenue | Final cash | Same-month baseline cash | Player damage | Unpaid obligations | Score | Status | Bankruptcy month |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| coffeebot | AAA | campus_locked, footfall_contested | coffeebot_a:coffeebot_a | campus_redeploy | 1846304177 | 115097715 | 472385682 | 357287967 | 0 | 709 | near_bankruptcy | — |
| coffeebot | AAB | campus_locked, footfall_contested | coffeebot_b:customer_churn | campus_redeploy | 1917538745 | 151400184 | 472385682 | 320985498 | 0 | 643 | near_bankruptcy | — |
| coffeebot | AAC | campus_locked, footfall_contested | coffeebot_c:coffeebot_c | campus_redeploy, loyalty_program | 1986176375 | 181014643 | 472385682 | 291371039 | 0 | 580 | deep_crisis | — |
| coffeebot | AAD | campus_locked, footfall_contested | coffeebot_d:coffeebot_d | campus_redeploy | 2005338204 | 218469833 | 472385682 | 253915849 | 0 | 513 | deep_crisis | — |
| coffeebot | ABA | footfall_contested | coffeebot_a:coffeebot_a | NONE | 2028986085 | 248840957 | 472385682 | 223544725 | 0 | 465 | deep_crisis | — |
| coffeebot | ABB | footfall_contested | coffeebot_b:customer_churn | NONE | 2014694759 | 229551594 | 472385682 | 242834088 | 0 | 503 | deep_crisis | — |
| coffeebot | ABC | footfall_contested | coffeebot_c:coffeebot_c | loyalty_program | 2035841267 | 228296824 | 472385682 | 244088858 | 0 | 495 | deep_crisis | — |
| coffeebot | ABD | footfall_contested | coffeebot_d:coffeebot_d | NONE | 2070178868 | 275616266 | 472385682 | 196769416 | 0 | 407 | deep_crisis | — |
| coffeebot | ACA | footfall_contested | coffeebot_a:coffeebot_a | loyalty_program | 2053820742 | 259983483 | 472385682 | 212402199 | 0 | 443 | deep_crisis | — |
| coffeebot | ACB | footfall_contested | coffeebot_b:customer_churn | loyalty_program | 1991902882 | 209736874 | 472385682 | 262648808 | 0 | 542 | near_bankruptcy | — |
| coffeebot | ACC | footfall_contested | coffeebot_c:coffeebot_c | loyalty_program | 2114835824 | 299643285 | 472385682 | 172742397 | 0 | 352 | deep_crisis | — |
| coffeebot | ACD | footfall_contested | coffeebot_d:coffeebot_d | loyalty_program | 2085529040 | 280593877 | 472385682 | 191791805 | 0 | 396 | deep_crisis | — |
| coffeebot | ADA | footfall_contested | coffeebot_a:coffeebot_a | NONE | 2093605356 | 310843482 | 472385682 | 161542200 | 0 | 352 | deep_crisis | — |
| coffeebot | ADB | footfall_contested | coffeebot_b:customer_churn | NONE | 2041460016 | 266949011 | 472385682 | 205436671 | 0 | 442 | deep_crisis | — |
| coffeebot | ADC | footfall_contested | coffeebot_c:coffeebot_c | loyalty_program | 2100683939 | 290444560 | 472385682 | 181941122 | 0 | 378 | deep_crisis | — |
| coffeebot | ADD | footfall_contested | coffeebot_d:coffeebot_d | NONE | 2162227542 | 355447903 | 472385682 | 116937779 | 0 | 243 | deep_crisis | — |
| coffeebot | BAA | uptime_exposed | coffeebot_a:coffeebot_a | NONE | 2097997584 | 313698429 | 472385682 | 158687253 | 0 | 339 | deep_crisis | — |
| coffeebot | BAB | uptime_exposed | coffeebot_b:customer_churn | NONE | 1997484373 | 238364841 | 472385682 | 234020841 | 0 | 494 | deep_crisis | — |
| coffeebot | BAC | uptime_exposed | coffeebot_c:coffeebot_c | loyalty_program | 2066212070 | 268037845 | 472385682 | 204347837 | 0 | 422 | deep_crisis | — |
| coffeebot | BAD | uptime_exposed | coffeebot_d:coffeebot_d | NONE | 2089189135 | 307972938 | 472385682 | 164412744 | 0 | 349 | deep_crisis | — |
| coffeebot | BBA | repair_backlog, uptime_exposed | coffeebot_a:coffeebot_a | service_reserve | 1944017278 | 97712649 | 472385682 | 374673033 | 0 | 732 | near_bankruptcy | — |
| coffeebot | BBB | repair_backlog, uptime_exposed | coffeebot_b:customer_churn | service_reserve | 1514516615 | 0 | 496421467 | 496421467 | 62872769 | 913 | bankrupt | 8 |
| coffeebot | BBC | repair_backlog, uptime_exposed | coffeebot_c:coffeebot_c | service_reserve, loyalty_program | 1950803093 | 76987712 | 472385682 | 395397970 | 0 | 766 | near_bankruptcy | — |
| coffeebot | BBD | repair_backlog, uptime_exposed | coffeebot_d:coffeebot_d | service_reserve | 1983747085 | 122742427 | 472385682 | 349643255 | 0 | 685 | near_bankruptcy | — |
| coffeebot | BCA | uptime_exposed | coffeebot_a:coffeebot_a | loyalty_program | 2064377555 | 266845411 | 472385682 | 205540271 | 0 | 431 | deep_crisis | — |
| coffeebot | BCB | uptime_exposed | coffeebot_b:customer_churn | loyalty_program | 2002459695 | 216598802 | 472385682 | 255786880 | 0 | 530 | near_bankruptcy | — |
| coffeebot | BCC | uptime_exposed | coffeebot_c:coffeebot_c | loyalty_program | 2125392637 | 306505213 | 472385682 | 165880469 | 0 | 339 | deep_crisis | — |
| coffeebot | BCD | uptime_exposed | coffeebot_d:coffeebot_d | loyalty_program | 2096085853 | 287455805 | 472385682 | 184929877 | 0 | 383 | deep_crisis | — |
| coffeebot | BDA | uptime_exposed | coffeebot_a:coffeebot_a | NONE | 2104162169 | 317705410 | 472385682 | 154680272 | 0 | 340 | deep_crisis | — |
| coffeebot | BDB | uptime_exposed | coffeebot_b:customer_churn | NONE | 2052016829 | 273810939 | 472385682 | 198574743 | 0 | 430 | deep_crisis | — |
| coffeebot | BDC | uptime_exposed | coffeebot_c:coffeebot_c | loyalty_program | 2111240752 | 297306488 | 472385682 | 175079194 | 0 | 366 | deep_crisis | — |
| coffeebot | BDD | uptime_exposed | coffeebot_d:coffeebot_d | NONE | 2172784355 | 362309831 | 472385682 | 110075851 | 0 | 230 | deep_crisis | — |
| coffeebot | CAA | price_pressure | coffeebot_a:coffeebot_a | NONE | 2079745151 | 301834348 | 472385682 | 170551334 | 0 | 360 | deep_crisis | — |
| coffeebot | CAB | price_pressure | coffeebot_b:customer_churn | NONE | 1979231940 | 226500760 | 472385682 | 245884922 | 0 | 514 | deep_crisis | — |
| coffeebot | CAC | price_pressure | coffeebot_c:coffeebot_c | loyalty_program | 2047959637 | 256173764 | 472385682 | 216211918 | 0 | 443 | deep_crisis | — |
| coffeebot | CAD | price_pressure | coffeebot_d:coffeebot_d | NONE | 2070936702 | 296108857 | 472385682 | 176276825 | 0 | 371 | deep_crisis | — |
| coffeebot | CBA | price_pressure | coffeebot_a:coffeebot_a | NONE | 2021290465 | 243838804 | 472385682 | 228546878 | 0 | 474 | deep_crisis | — |
| coffeebot | CBB | price_pressure | coffeebot_b:customer_churn | NONE | 2006999139 | 224549441 | 472385682 | 247836241 | 0 | 512 | deep_crisis | — |
| coffeebot | CBC | price_pressure | coffeebot_c:coffeebot_c | loyalty_program | 2028145647 | 223294671 | 472385682 | 249091011 | 0 | 504 | deep_crisis | — |
| coffeebot | CBD | price_pressure | coffeebot_d:coffeebot_d | NONE | 2062483248 | 270614113 | 472385682 | 201771569 | 0 | 416 | deep_crisis | — |
| coffeebot | CCA | margin_squeeze, price_pressure | coffeebot_a:coffeebot_a | loyalty_program | 1945448855 | 189541755 | 472385682 | 282843927 | 0 | 571 | near_bankruptcy | — |
| coffeebot | CCB | margin_squeeze, price_pressure | coffeebot_b:customer_churn | loyalty_program | 1883530995 | 139295146 | 472385682 | 333090536 | 0 | 664 | near_bankruptcy | — |
| coffeebot | CCC | margin_squeeze, price_pressure | coffeebot_c:coffeebot_c | loyalty_program | 1801854725 | 96205571 | 472385682 | 376180111 | 0 | 741 | near_bankruptcy | — |
| coffeebot | CCD | margin_squeeze, price_pressure | coffeebot_d:coffeebot_d | loyalty_program | 1969032938 | 204871409 | 472385682 | 267514273 | 0 | 539 | deep_crisis | — |
| coffeebot | CDA | price_pressure | coffeebot_a:coffeebot_a | NONE | 2085909736 | 305841329 | 472385682 | 166544353 | 0 | 361 | deep_crisis | — |
| coffeebot | CDB | price_pressure | coffeebot_b:customer_churn | NONE | 2033764396 | 261946858 | 472385682 | 210438824 | 0 | 450 | deep_crisis | — |
| coffeebot | CDC | price_pressure | coffeebot_c:coffeebot_c | loyalty_program | 2092988319 | 285442407 | 472385682 | 186943275 | 0 | 387 | deep_crisis | — |
| coffeebot | CDD | price_pressure | coffeebot_d:coffeebot_d | NONE | 2154531922 | 350445750 | 472385682 | 121939932 | 0 | 252 | deep_crisis | — |
| coffeebot | DAA | — | coffeebot_a:coffeebot_a | NONE | 2106383837 | 319149494 | 472385682 | 153236188 | 0 | 329 | deep_crisis | — |
| coffeebot | DAB | — | coffeebot_b:customer_churn | NONE | 2005870626 | 243815906 | 472385682 | 228569776 | 0 | 484 | deep_crisis | — |
| coffeebot | DAC | — | coffeebot_c:coffeebot_c | loyalty_program | 2074598323 | 273488910 | 472385682 | 198896772 | 0 | 412 | deep_crisis | — |
| coffeebot | DAD | — | coffeebot_d:coffeebot_d | NONE | 2097575388 | 313424003 | 472385682 | 158961679 | 0 | 340 | deep_crisis | — |
| coffeebot | DBA | — | coffeebot_a:coffeebot_a | NONE | 2047929151 | 261153950 | 472385682 | 211231732 | 0 | 444 | deep_crisis | — |
| coffeebot | DBB | — | coffeebot_b:customer_churn | NONE | 2033637825 | 241864587 | 472385682 | 230521095 | 0 | 482 | deep_crisis | — |
| coffeebot | DBC | — | coffeebot_c:coffeebot_c | loyalty_program | 2054784333 | 240609817 | 472385682 | 231775865 | 0 | 473 | deep_crisis | — |
| coffeebot | DBD | — | coffeebot_d:coffeebot_d | NONE | 2089121934 | 287929259 | 472385682 | 184456423 | 0 | 385 | deep_crisis | — |
| coffeebot | DCA | — | coffeebot_a:coffeebot_a | loyalty_program | 2072763808 | 272296476 | 472385682 | 200089206 | 0 | 421 | deep_crisis | — |
| coffeebot | DCB | — | coffeebot_b:customer_churn | loyalty_program | 2010845948 | 222049867 | 472385682 | 250335815 | 0 | 521 | deep_crisis | — |
| coffeebot | DCC | — | coffeebot_c:coffeebot_c | loyalty_program | 2133778890 | 311956278 | 472385682 | 160429404 | 0 | 329 | deep_crisis | — |
| coffeebot | DCD | — | coffeebot_d:coffeebot_d | loyalty_program | 2104472106 | 292906870 | 472385682 | 179478812 | 0 | 374 | deep_crisis | — |
| coffeebot | DDA | — | coffeebot_a:coffeebot_a | NONE | 2112548422 | 323156475 | 472385682 | 149229207 | 0 | 330 | deep_crisis | — |
| coffeebot | DDB | — | coffeebot_b:customer_churn | NONE | 2060403082 | 279262004 | 472385682 | 193123678 | 0 | 421 | deep_crisis | — |
| coffeebot | DDC | — | coffeebot_c:coffeebot_c | loyalty_program | 2119627005 | 302757553 | 472385682 | 169628129 | 0 | 356 | deep_crisis | — |
| coffeebot | DDD | — | coffeebot_d:coffeebot_d | NONE | 2181170608 | 367760896 | 472385682 | 104624786 | 0 | 220 | survived | — |
| petmind | AAA | accuracy_doubted, trust_crisis | petmind_a:petmind_a | independent_audit | 1781812800 | 140268960 | 440000000 | 299731040 | 0 | 648 | near_bankruptcy | — |
| petmind | AAB | accuracy_doubted, trust_crisis | petmind_b:customer_churn | independent_audit | 1847596800 | 186317760 | 440000000 | 253682240 | 0 | 556 | near_bankruptcy | — |
| petmind | AAC | accuracy_doubted, trust_crisis | petmind_c:petmind_c | independent_audit | 1864756800 | 198329760 | 440000000 | 241670240 | 0 | 531 | near_bankruptcy | — |
| petmind | AAD | accuracy_doubted, trust_crisis | petmind_d:petmind_d | independent_audit | 1761969600 | 126378720 | 440000000 | 313621280 | 0 | 674 | near_bankruptcy | — |
| petmind | ABA | accuracy_doubted | petmind_a:petmind_a | NONE | 1900190400 | 248133280 | 440000000 | 191866720 | 0 | 446 | deep_crisis | — |
| petmind | ABB | accuracy_doubted | petmind_b:customer_churn | NONE | 1974926400 | 300448480 | 440000000 | 139551520 | 0 | 331 | deep_crisis | — |
| petmind | ABC | accuracy_doubted | petmind_c:petmind_c | NONE | 1951238400 | 283866880 | 440000000 | 156133120 | 0 | 368 | deep_crisis | — |
| petmind | ABD | accuracy_doubted | petmind_d:petmind_d | NONE | 1849574400 | 212702080 | 440000000 | 227297920 | 0 | 518 | near_bankruptcy | — |
| petmind | ACA | accuracy_doubted | petmind_a:petmind_a | NONE | 1927641600 | 277349120 | 440000000 | 162650880 | 0 | 391 | deep_crisis | — |
| petmind | ACB | accuracy_doubted | petmind_b:customer_churn | NONE | 1961894400 | 301326080 | 440000000 | 138673920 | 0 | 338 | deep_crisis | — |
| petmind | ACC | accuracy_doubted | petmind_c:petmind_c | NONE | 2009500800 | 334650560 | 440000000 | 105349440 | 0 | 259 | deep_crisis | — |
| petmind | ACD | accuracy_doubted | petmind_d:petmind_d | NONE | 1874140800 | 239898560 | 440000000 | 200101440 | 0 | 468 | near_bankruptcy | — |
| petmind | ADA | accuracy_doubted | petmind_a:petmind_a | NONE | 1844044800 | 218831360 | 440000000 | 221168640 | 0 | 502 | near_bankruptcy | — |
| petmind | ADB | accuracy_doubted | petmind_b:customer_churn | NONE | 1886913600 | 248839520 | 440000000 | 191160480 | 0 | 440 | deep_crisis | — |
| petmind | ADC | accuracy_doubted | petmind_c:petmind_c | NONE | 1891449600 | 252014720 | 440000000 | 187985280 | 0 | 432 | deep_crisis | — |
| petmind | ADD | accuracy_doubted | petmind_d:petmind_d | NONE | 1842849600 | 217994720 | 440000000 | 222005280 | 0 | 505 | near_bankruptcy | — |
| petmind | BAA | factory_pressure | petmind_a:petmind_a | NONE | 1923556800 | 262489760 | 440000000 | 177510240 | 0 | 414 | deep_crisis | — |
| petmind | BAB | factory_pressure | petmind_b:customer_churn | NONE | 1919280000 | 259496000 | 440000000 | 180504000 | 0 | 419 | deep_crisis | — |
| petmind | BAC | factory_pressure | petmind_c:petmind_c | NONE | 1936579200 | 271605440 | 440000000 | 168394560 | 0 | 392 | deep_crisis | — |
| petmind | BAD | factory_pressure | petmind_d:petmind_d | NONE | 1831358400 | 197950880 | 440000000 | 242049120 | 0 | 545 | near_bankruptcy | — |
| petmind | BBA | factory_pressure, stockout | petmind_a:petmind_a | NONE | 1769184000 | 129428800 | 440000000 | 310571200 | 0 | 667 | near_bankruptcy | — |
| petmind | BBB | factory_pressure, stockout | petmind_b:customer_churn | NONE | 1682424000 | 56696800 | 440000000 | 383303200 | 0 | 800 | near_bankruptcy | — |
| petmind | BBC | factory_pressure, stockout | petmind_c:petmind_c | NONE | 1811491200 | 159043840 | 440000000 | 280956160 | 0 | 608 | near_bankruptcy | — |
| petmind | BBD | factory_pressure, stockout | petmind_d:petmind_d | NONE | 1724025600 | 97817920 | 440000000 | 342182080 | 0 | 726 | near_bankruptcy | — |
| petmind | BCA | factory_pressure | petmind_a:petmind_a | NONE | 1931404800 | 267983360 | 440000000 | 172016640 | 0 | 408 | deep_crisis | — |
| petmind | BCB | factory_pressure | petmind_b:customer_churn | NONE | 1965657600 | 291960320 | 440000000 | 148039680 | 0 | 355 | deep_crisis | — |
| petmind | BCC | factory_pressure | petmind_c:petmind_c | NONE | 2013264000 | 325284800 | 440000000 | 114715200 | 0 | 277 | deep_crisis | — |
| petmind | BCD | factory_pressure | petmind_d:petmind_d | NONE | 1877904000 | 230532800 | 440000000 | 209467200 | 0 | 485 | near_bankruptcy | — |
| petmind | BDA | factory_pressure | petmind_a:petmind_a | NONE | 1847808000 | 209465600 | 440000000 | 230534400 | 0 | 519 | near_bankruptcy | — |
| petmind | BDB | factory_pressure | petmind_b:customer_churn | NONE | 1890676800 | 239473760 | 440000000 | 200526240 | 0 | 457 | deep_crisis | — |
| petmind | BDC | factory_pressure | petmind_c:petmind_c | NONE | 1895212800 | 242648960 | 440000000 | 197351040 | 0 | 450 | deep_crisis | — |
| petmind | BDD | factory_pressure | petmind_d:petmind_d | NONE | 1846612800 | 208628960 | 440000000 | 231371040 | 0 | 522 | near_bankruptcy | — |
| petmind | CAA | free_alternative | petmind_a:petmind_a | NONE | 1929201600 | 278441120 | 440000000 | 161558880 | 0 | 384 | deep_crisis | — |
| petmind | CAB | free_alternative | petmind_b:customer_churn | NONE | 1924924800 | 275447360 | 440000000 | 164552640 | 0 | 389 | deep_crisis | — |
| petmind | CAC | free_alternative | petmind_c:petmind_c | NONE | 1942224000 | 287556800 | 440000000 | 152443200 | 0 | 362 | deep_crisis | — |
| petmind | CAD | free_alternative | petmind_d:petmind_d | NONE | 1837003200 | 213902240 | 440000000 | 226097760 | 0 | 516 | near_bankruptcy | — |
| petmind | CBA | free_alternative | petmind_a:petmind_a | NONE | 1909598400 | 254718880 | 440000000 | 185281120 | 0 | 434 | deep_crisis | — |
| petmind | CBB | free_alternative | petmind_b:customer_churn | NONE | 1984334400 | 307034080 | 440000000 | 132965920 | 0 | 319 | deep_crisis | — |
| petmind | CBC | free_alternative | petmind_c:petmind_c | NONE | 1960646400 | 290452480 | 440000000 | 149547520 | 0 | 356 | deep_crisis | — |
| petmind | CBD | free_alternative | petmind_d:petmind_d | NONE | 1858982400 | 219287680 | 440000000 | 220712320 | 0 | 506 | near_bankruptcy | — |
| petmind | CCA | churn_wave, free_alternative | petmind_a:petmind_a | retention_offer | 1886253600 | 233377520 | 440000000 | 206622480 | 0 | 475 | near_bankruptcy | — |
| petmind | CCB | churn_wave, free_alternative | petmind_b:customer_churn | retention_offer | 1915465440 | 253825808 | 440000000 | 186174192 | 0 | 433 | deep_crisis | — |
| petmind | CCC | churn_wave, free_alternative | petmind_c:petmind_c | retention_offer | 1640737440 | 61516208 | 440000000 | 378483792 | 0 | 795 | near_bankruptcy | — |
| petmind | CCD | churn_wave, free_alternative | petmind_d:petmind_d | retention_offer | 1833745440 | 196621808 | 440000000 | 243378192 | 0 | 548 | near_bankruptcy | — |
| petmind | CDA | free_alternative | petmind_a:petmind_a | NONE | 1853452800 | 225416960 | 440000000 | 214583040 | 0 | 490 | near_bankruptcy | — |
| petmind | CDB | free_alternative | petmind_b:customer_churn | NONE | 1896321600 | 255425120 | 440000000 | 184574880 | 0 | 427 | deep_crisis | — |
| petmind | CDC | free_alternative | petmind_c:petmind_c | NONE | 1900857600 | 258600320 | 440000000 | 181399680 | 0 | 420 | deep_crisis | — |
| petmind | CDD | free_alternative | petmind_d:petmind_d | NONE | 1852257600 | 224580320 | 440000000 | 215419680 | 0 | 493 | near_bankruptcy | — |
| petmind | DAA | — | petmind_a:petmind_a | NONE | 1903800000 | 260660000 | 440000000 | 179340000 | 0 | 417 | deep_crisis | — |
| petmind | DAB | — | petmind_b:customer_churn | NONE | 1899523200 | 257666240 | 440000000 | 182333760 | 0 | 422 | deep_crisis | — |
| petmind | DAC | — | petmind_c:petmind_c | NONE | 1916822400 | 269775680 | 440000000 | 170224320 | 0 | 395 | deep_crisis | — |
| petmind | DAD | — | petmind_d:petmind_d | NONE | 1811601600 | 196121120 | 440000000 | 243878880 | 0 | 548 | near_bankruptcy | — |
| petmind | DBA | — | petmind_a:petmind_a | NONE | 1884196800 | 236937760 | 440000000 | 203062240 | 0 | 467 | deep_crisis | — |
| petmind | DBB | — | petmind_b:customer_churn | NONE | 1958932800 | 289252960 | 440000000 | 150747040 | 0 | 352 | deep_crisis | — |
| petmind | DBC | — | petmind_c:petmind_c | NONE | 1935244800 | 272671360 | 440000000 | 167328640 | 0 | 389 | deep_crisis | — |
| petmind | DBD | — | petmind_d:petmind_d | NONE | 1833580800 | 201506560 | 440000000 | 238493440 | 0 | 538 | near_bankruptcy | — |
| petmind | DCA | — | petmind_a:petmind_a | NONE | 1911648000 | 266153600 | 440000000 | 173846400 | 0 | 411 | deep_crisis | — |
| petmind | DCB | — | petmind_b:customer_churn | NONE | 1945900800 | 290130560 | 440000000 | 149869440 | 0 | 359 | deep_crisis | — |
| petmind | DCC | — | petmind_c:petmind_c | NONE | 1993507200 | 323455040 | 440000000 | 116544960 | 0 | 281 | deep_crisis | — |
| petmind | DCD | — | petmind_d:petmind_d | NONE | 1858147200 | 228703040 | 440000000 | 211296960 | 0 | 488 | near_bankruptcy | — |
| petmind | DDA | — | petmind_a:petmind_a | NONE | 1828051200 | 207635840 | 440000000 | 232364160 | 0 | 523 | near_bankruptcy | — |
| petmind | DDB | — | petmind_b:customer_churn | NONE | 1870920000 | 237644000 | 440000000 | 202356000 | 0 | 460 | deep_crisis | — |
| petmind | DDC | — | petmind_c:petmind_c | NONE | 1875456000 | 240819200 | 440000000 | 199180800 | 0 | 453 | deep_crisis | — |
| petmind | DDD | — | petmind_d:petmind_d | NONE | 1826856000 | 206799200 | 440000000 | 233200800 | 0 | 525 | near_bankruptcy | — |
| foodrover | AAA | route_restricted, route_scrutiny | foodrover_a:foodrover_a | route_rebuild | 2571350562 | 65809662 | 537473577 | 471663915 | 0 | 804 | near_bankruptcy | — |
| foodrover | AAB | route_restricted, route_scrutiny | foodrover_b:customer_churn | route_rebuild | 2590856764 | 90356970 | 537473577 | 447116607 | 0 | 767 | near_bankruptcy | — |
| foodrover | AAC | route_restricted, route_scrutiny | foodrover_c:foodrover_c | route_rebuild | 2598268034 | 105614272 | 537473577 | 431859305 | 0 | 744 | near_bankruptcy | — |
| foodrover | AAD | route_restricted, route_scrutiny | foodrover_d:foodrover_d | route_rebuild | 2758995518 | 191652183 | 537473577 | 345821394 | 0 | 602 | near_bankruptcy | — |
| foodrover | ABA | route_scrutiny | foodrover_a:foodrover_a | NONE | 2687207592 | 233580405 | 537473577 | 303893172 | 0 | 548 | near_bankruptcy | — |
| foodrover | ABB | route_scrutiny | foodrover_b:customer_churn | NONE | 2709993931 | 236796481 | 537473577 | 300677096 | 0 | 542 | near_bankruptcy | — |
| foodrover | ABC | route_scrutiny | foodrover_c:foodrover_c | NONE | 2638507678 | 205334454 | 537473577 | 332139123 | 0 | 595 | near_bankruptcy | — |
| foodrover | ABD | route_scrutiny | foodrover_d:foodrover_d | NONE | 2809503286 | 304511908 | 537473577 | 232961669 | 0 | 415 | deep_crisis | — |
| foodrover | ACA | route_scrutiny | foodrover_a:foodrover_a | NONE | 2705289213 | 259067744 | 537473577 | 278405833 | 0 | 509 | deep_crisis | — |
| foodrover | ACB | route_scrutiny | foodrover_b:customer_churn | NONE | 2649835358 | 216904507 | 537473577 | 320569070 | 0 | 578 | near_bankruptcy | — |
| foodrover | ACC | route_scrutiny | foodrover_c:foodrover_c | restaurant_retention | 2784189939 | 269830165 | 537473577 | 267643412 | 0 | 475 | deep_crisis | — |
| foodrover | ACD | route_scrutiny | foodrover_d:foodrover_d | NONE | 2819108527 | 325082946 | 537473577 | 212390631 | 0 | 382 | deep_crisis | — |
| foodrover | ADA | route_scrutiny | foodrover_a:foodrover_a | NONE | 2859267486 | 348375142 | 537473577 | 189098435 | 0 | 366 | deep_crisis | — |
| foodrover | ADB | route_scrutiny | foodrover_b:customer_churn | NONE | 2807140286 | 308141367 | 537473577 | 229332210 | 0 | 437 | deep_crisis | — |
| foodrover | ADC | route_scrutiny | foodrover_c:foodrover_c | restaurant_retention | 2866504148 | 317572406 | 537473577 | 219901171 | 0 | 406 | deep_crisis | — |
| foodrover | ADD | route_scrutiny | foodrover_d:foodrover_d | NONE | 3021634816 | 442548194 | 537473577 | 94925383 | 0 | 147 | survived | — |
| foodrover | BAA | battery_pressure | foodrover_a:foodrover_a | NONE | 2785811692 | 290770782 | 537473577 | 246702795 | 0 | 451 | deep_crisis | — |
| foodrover | BAB | battery_pressure | foodrover_b:customer_churn | NONE | 2665650906 | 211077525 | 537473577 | 326396052 | 0 | 586 | near_bankruptcy | — |
| foodrover | BAC | battery_pressure | foodrover_c:foodrover_c | NONE | 2672554604 | 225081670 | 537473577 | 312391907 | 0 | 565 | near_bankruptcy | — |
| foodrover | BAD | battery_pressure | foodrover_d:foodrover_d | NONE | 2837342955 | 320658915 | 537473577 | 216814662 | 0 | 387 | deep_crisis | — |
| foodrover | BBA | battery_backlog, battery_pressure | foodrover_a:foodrover_a | battery_reserve | 2595377310 | 40176047 | 537473577 | 497297530 | 0 | 840 | near_bankruptcy | — |
| foodrover | BBB | battery_backlog, battery_pressure | foodrover_b:customer_churn | battery_reserve | 2025003369 | 0 | 563934235 | 563934235 | 86381491 | 913 | bankrupt | 8 |
| foodrover | BBC | battery_backlog, battery_pressure | foodrover_c:foodrover_c | battery_reserve | 2546916832 | 13280481 | 537473577 | 524193096 | 0 | 880 | near_bankruptcy | — |
| foodrover | BBD | battery_backlog, battery_pressure | foodrover_d:foodrover_d | battery_reserve | 2716422200 | 107355961 | 537473577 | 430117616 | 0 | 733 | near_bankruptcy | — |
| foodrover | BCA | battery_pressure | foodrover_a:foodrover_a | NONE | 2699251111 | 240565644 | 537473577 | 296907933 | 0 | 537 | near_bankruptcy | — |
| foodrover | BCB | battery_pressure | foodrover_b:customer_churn | NONE | 2643797256 | 198402407 | 537473577 | 339071170 | 0 | 605 | near_bankruptcy | — |
| foodrover | BCC | battery_pressure | foodrover_c:foodrover_c | restaurant_retention | 2778151837 | 251328065 | 537473577 | 286145512 | 0 | 504 | deep_crisis | — |
| foodrover | BCD | battery_pressure | foodrover_d:foodrover_d | NONE | 2813070425 | 306580846 | 537473577 | 230892731 | 0 | 412 | deep_crisis | — |
| foodrover | BDA | battery_pressure | foodrover_a:foodrover_a | NONE | 2853229384 | 329873042 | 537473577 | 207600535 | 0 | 395 | deep_crisis | — |
| foodrover | BDB | battery_pressure | foodrover_b:customer_churn | NONE | 2801102184 | 289639267 | 537473577 | 247834310 | 0 | 465 | deep_crisis | — |
| foodrover | BDC | battery_pressure | foodrover_c:foodrover_c | restaurant_retention | 2860466046 | 299070306 | 537473577 | 238403271 | 0 | 434 | deep_crisis | — |
| foodrover | BDD | battery_pressure | foodrover_d:foodrover_d | NONE | 3015596714 | 424046094 | 537473577 | 113427483 | 0 | 179 | survived | — |
| foodrover | CAA | competitor_trial | foodrover_a:foodrover_a | NONE | 2769844266 | 296509676 | 537473577 | 240963901 | 0 | 442 | deep_crisis | — |
| foodrover | CAB | competitor_trial | foodrover_b:customer_churn | NONE | 2649683480 | 216816419 | 537473577 | 320657158 | 0 | 577 | near_bankruptcy | — |
| foodrover | CAC | competitor_trial | foodrover_c:foodrover_c | NONE | 2656587178 | 230820564 | 537473577 | 306653013 | 0 | 556 | near_bankruptcy | — |
| foodrover | CAD | competitor_trial | foodrover_d:foodrover_d | NONE | 2821375529 | 326397809 | 537473577 | 211075768 | 0 | 377 | deep_crisis | — |
| foodrover | CBA | competitor_trial | foodrover_a:foodrover_a | NONE | 2665202064 | 220817199 | 537473577 | 316656378 | 0 | 567 | near_bankruptcy | — |
| foodrover | CBB | competitor_trial | foodrover_b:customer_churn | NONE | 2687988403 | 224033275 | 537473577 | 313440302 | 0 | 561 | near_bankruptcy | — |
| foodrover | CBC | competitor_trial | foodrover_c:foodrover_c | NONE | 2616502150 | 192571248 | 537473577 | 344902329 | 0 | 614 | near_bankruptcy | — |
| foodrover | CBD | competitor_trial | foodrover_d:foodrover_d | NONE | 2787497758 | 291748702 | 537473577 | 245724875 | 0 | 435 | deep_crisis | — |
| foodrover | CCA | competitor_trial, restaurant_switch | foodrover_a:foodrover_a | restaurant_retention | 2526207853 | 120200556 | 537473577 | 417273021 | 0 | 722 | near_bankruptcy | — |
| foodrover | CCB | competitor_trial, restaurant_switch | foodrover_b:customer_churn | restaurant_retention | 2472397182 | 78990366 | 537473577 | 458483211 | 0 | 784 | near_bankruptcy | — |
| foodrover | CCC | competitor_trial, restaurant_switch | foodrover_c:foodrover_c | restaurant_retention, cost_cut | 2243563386 | 0 | 537473577 | 537473577 | 31733235 | 900 | bankrupt | 9 |
| foodrover | CCD | competitor_trial, restaurant_switch | foodrover_d:foodrover_d | restaurant_retention | 2620943796 | 175147403 | 537473577 | 362326174 | 0 | 633 | near_bankruptcy | — |
| foodrover | CDA | competitor_trial | foodrover_a:foodrover_a | NONE | 2837261958 | 335611936 | 537473577 | 201861641 | 0 | 386 | deep_crisis | — |
| foodrover | CDB | competitor_trial | foodrover_b:customer_churn | NONE | 2785134758 | 295378161 | 537473577 | 242095416 | 0 | 456 | deep_crisis | — |
| foodrover | CDC | competitor_trial | foodrover_c:foodrover_c | restaurant_retention | 2844498620 | 304809200 | 537473577 | 232664377 | 0 | 425 | deep_crisis | — |
| foodrover | CDD | competitor_trial | foodrover_d:foodrover_d | NONE | 2999629288 | 429784988 | 537473577 | 107688589 | 0 | 169 | survived | — |
| foodrover | DAA | — | foodrover_a:foodrover_a | NONE | 2817746544 | 324292997 | 537473577 | 213180580 | 0 | 399 | deep_crisis | — |
| foodrover | DAB | — | foodrover_b:customer_churn | NONE | 2697585758 | 244599740 | 537473577 | 292873837 | 0 | 536 | near_bankruptcy | — |
| foodrover | DAC | — | foodrover_c:foodrover_c | NONE | 2704489456 | 258603885 | 537473577 | 278869692 | 0 | 515 | near_bankruptcy | — |
| foodrover | DAD | — | foodrover_d:foodrover_d | NONE | 2869277807 | 354181130 | 537473577 | 183292447 | 0 | 333 | deep_crisis | — |
| foodrover | DBA | — | foodrover_a:foodrover_a | NONE | 2713104342 | 248600520 | 537473577 | 288873057 | 0 | 525 | deep_crisis | — |
| foodrover | DBB | — | foodrover_b:customer_churn | NONE | 2735890681 | 251816596 | 537473577 | 285656981 | 0 | 519 | deep_crisis | — |
| foodrover | DBC | — | foodrover_c:foodrover_c | NONE | 2664404428 | 220354569 | 537473577 | 317119008 | 0 | 573 | near_bankruptcy | — |
| foodrover | DBD | — | foodrover_d:foodrover_d | NONE | 2835400036 | 319532023 | 537473577 | 217941554 | 0 | 391 | deep_crisis | — |
| foodrover | DCA | — | foodrover_a:foodrover_a | NONE | 2731185963 | 274087859 | 537473577 | 263385718 | 0 | 486 | deep_crisis | — |
| foodrover | DCB | — | foodrover_b:customer_churn | NONE | 2675732108 | 231924622 | 537473577 | 305548955 | 0 | 556 | near_bankruptcy | — |
| foodrover | DCC | — | foodrover_c:foodrover_c | restaurant_retention | 2810086689 | 284850280 | 537473577 | 252623297 | 0 | 451 | deep_crisis | — |
| foodrover | DCD | — | foodrover_d:foodrover_d | NONE | 2845005277 | 340103061 | 537473577 | 197370516 | 0 | 358 | deep_crisis | — |
| foodrover | DDA | — | foodrover_a:foodrover_a | NONE | 2885164236 | 363395257 | 537473577 | 174078320 | 0 | 343 | deep_crisis | — |
| foodrover | DDB | — | foodrover_b:customer_churn | NONE | 2833037036 | 323161482 | 537473577 | 214312095 | 0 | 414 | deep_crisis | — |
| foodrover | DDC | — | foodrover_c:foodrover_c | restaurant_retention | 2892400898 | 332592521 | 537473577 | 204881056 | 0 | 382 | deep_crisis | — |
| foodrover | DDD | — | foodrover_d:foodrover_d | NONE | 3047531566 | 457568309 | 537473577 | 79905268 | 0 | 122 | survived | — |
| studygenie | AAA | quality_doubt, trust_crisis | studygenie_a:studygenie_a | quality_audit | 1175927263 | 91297446 | 363347068 | 272049622 | 0 | 696 | near_bankruptcy | — |
| studygenie | AAB | quality_doubt, trust_crisis | studygenie_b:customer_churn | quality_audit | 1217200891 | 126792766 | 363347068 | 236554302 | 0 | 602 | deep_crisis | — |
| studygenie | AAC | quality_doubt, trust_crisis | studygenie_c:studygenie_c | quality_audit | 1216776657 | 126427925 | 363347068 | 236919143 | 0 | 603 | deep_crisis | — |
| studygenie | AAD | quality_doubt, trust_crisis | studygenie_d:studygenie_d | quality_audit | 1244865744 | 150584541 | 363347068 | 212762527 | 0 | 530 | deep_crisis | — |
| studygenie | ABA | quality_doubt | studygenie_a:studygenie_a | NONE | 1283816278 | 199081999 | 363347068 | 164265069 | 0 | 420 | deep_crisis | — |
| studygenie | ABB | quality_doubt | studygenie_b:customer_churn | NONE | 1303978665 | 216421651 | 363347068 | 146925417 | 0 | 362 | deep_crisis | — |
| studygenie | ABC | quality_doubt | studygenie_c:studygenie_c | NONE | 1279453712 | 195330191 | 363347068 | 168016877 | 0 | 433 | deep_crisis | — |
| studygenie | ABD | quality_doubt | studygenie_d:studygenie_d | NONE | 1307684038 | 219608272 | 363347068 | 143738796 | 0 | 344 | deep_crisis | — |
| studygenie | ACA | quality_doubt | studygenie_a:studygenie_a | NONE | 1279138351 | 205058982 | 363347068 | 158288086 | 0 | 407 | deep_crisis | — |
| studygenie | ACB | quality_doubt | studygenie_b:customer_churn | NONE | 1275620213 | 202033382 | 363347068 | 161313686 | 0 | 418 | deep_crisis | — |
| studygenie | ACC | quality_doubt | studygenie_c:studygenie_c | NONE | 1300690479 | 223593812 | 363347068 | 139753256 | 0 | 345 | deep_crisis | — |
| studygenie | ACD | quality_doubt | studygenie_d:studygenie_d | NONE | 1300798644 | 223686834 | 363347068 | 139660234 | 0 | 338 | deep_crisis | — |
| studygenie | ADA | quality_doubt | studygenie_a:studygenie_a | NONE | 1315345122 | 236196805 | 363347068 | 127150263 | 0 | 320 | deep_crisis | — |
| studygenie | ADB | quality_doubt | studygenie_b:customer_churn | NONE | 1309418925 | 231100276 | 363347068 | 132246792 | 0 | 339 | deep_crisis | — |
| studygenie | ADC | quality_doubt | studygenie_c:studygenie_c | NONE | 1306285194 | 228405267 | 363347068 | 134941801 | 0 | 348 | deep_crisis | — |
| studygenie | ADD | quality_doubt | studygenie_d:studygenie_d | NONE | 1354463256 | 269838401 | 363347068 | 93508667 | 0 | 180 | survived | — |
| studygenie | BAA | api_pressure | studygenie_a:studygenie_a | NONE | 1310212351 | 221782620 | 363347068 | 141564448 | 0 | 343 | deep_crisis | — |
| studygenie | BAB | api_pressure | studygenie_b:customer_churn | NONE | 1279747953 | 195583237 | 363347068 | 167763831 | 0 | 433 | deep_crisis | — |
| studygenie | BAC | api_pressure | studygenie_c:studygenie_c | NONE | 1279385511 | 195271538 | 363347068 | 168075530 | 0 | 434 | deep_crisis | — |
| studygenie | BAD | api_pressure | studygenie_d:studygenie_d | NONE | 1308232115 | 220079617 | 363347068 | 143267451 | 0 | 344 | deep_crisis | — |
| studygenie | BBA | api_bottleneck, api_pressure | studygenie_a:studygenie_a | backup_provider | 1222712713 | 46051029 | 363347068 | 317296039 | 0 | 793 | near_bankruptcy | — |
| studygenie | BBB | api_bottleneck, api_pressure | studygenie_b:customer_churn | backup_provider | 938264795 | 0 | 367203008 | 367203008 | 50040744 | 913 | bankrupt | 8 |
| studygenie | BBC | api_bottleneck, api_pressure | studygenie_c:studygenie_c | backup_provider | 1218420843 | 42488775 | 363347068 | 320858293 | 0 | 802 | near_bankruptcy | — |
| studygenie | BBD | api_bottleneck, api_pressure | studygenie_d:studygenie_d | backup_provider | 1245942028 | 65331359 | 363347068 | 298015709 | 0 | 743 | near_bankruptcy | — |
| studygenie | BCA | api_pressure | studygenie_a:studygenie_a | NONE | 1282952516 | 198339163 | 363347068 | 165007905 | 0 | 424 | deep_crisis | — |
| studygenie | BCB | api_pressure | studygenie_b:customer_churn | NONE | 1279434378 | 195313563 | 363347068 | 168033505 | 0 | 434 | deep_crisis | — |
| studygenie | BCC | api_pressure | studygenie_c:studygenie_c | NONE | 1304504644 | 216873993 | 363347068 | 146473075 | 0 | 362 | deep_crisis | — |
| studygenie | BCD | api_pressure | studygenie_d:studygenie_d | NONE | 1304612809 | 216967015 | 363347068 | 146380053 | 0 | 355 | deep_crisis | — |
| studygenie | BDA | api_pressure | studygenie_a:studygenie_a | NONE | 1319159287 | 229476986 | 363347068 | 133870082 | 0 | 337 | deep_crisis | — |
| studygenie | BDB | api_pressure | studygenie_b:customer_churn | NONE | 1313233090 | 224380457 | 363347068 | 138966611 | 0 | 355 | deep_crisis | — |
| studygenie | BDC | api_pressure | studygenie_c:studygenie_c | NONE | 1310099359 | 221685448 | 363347068 | 141661620 | 0 | 365 | deep_crisis | — |
| studygenie | BDD | api_pressure | studygenie_d:studygenie_d | NONE | 1358277421 | 263118582 | 363347068 | 100228486 | 0 | 193 | survived | — |
| studygenie | CAA | exam_trial | studygenie_a:studygenie_a | NONE | 1305802223 | 227989911 | 363347068 | 135357157 | 0 | 327 | survived | — |
| studygenie | CAB | exam_trial | studygenie_b:customer_churn | NONE | 1275337825 | 201790528 | 363347068 | 161556540 | 0 | 418 | deep_crisis | — |
| studygenie | CAC | exam_trial | studygenie_c:studygenie_c | NONE | 1274975383 | 201478829 | 363347068 | 161868239 | 0 | 419 | deep_crisis | — |
| studygenie | CAD | exam_trial | studygenie_d:studygenie_d | NONE | 1303821987 | 226286908 | 363347068 | 137060160 | 0 | 328 | survived | — |
| studygenie | CBA | exam_trial | studygenie_a:studygenie_a | NONE | 1283220315 | 198569471 | 363347068 | 164777597 | 0 | 422 | deep_crisis | — |
| studygenie | CBB | exam_trial | studygenie_b:customer_churn | NONE | 1303382702 | 215909123 | 363347068 | 147437945 | 0 | 363 | deep_crisis | — |
| studygenie | CBC | exam_trial | studygenie_c:studygenie_c | NONE | 1278857749 | 194817663 | 363347068 | 168529405 | 0 | 434 | deep_crisis | — |
| studygenie | CBD | exam_trial | studygenie_d:studygenie_d | NONE | 1307088075 | 219095744 | 363347068 | 144251324 | 0 | 345 | deep_crisis | — |
| studygenie | CCA | cohort_churn, exam_trial | studygenie_a:studygenie_a | student_retention | 1199659682 | 118707327 | 363347068 | 244639741 | 0 | 627 | near_bankruptcy | — |
| studygenie | CCB | cohort_churn, exam_trial | studygenie_b:customer_churn | student_retention | 1197669126 | 116995449 | 363347068 | 246351619 | 0 | 632 | near_bankruptcy | — |
| studygenie | CCC | cohort_churn, exam_trial | studygenie_c:studygenie_c | student_retention, cost_cut | 1054692445 | 1785503 | 363347068 | 361561565 | 0 | 896 | near_bankruptcy | — |
| studygenie | CCD | cohort_churn, exam_trial | studygenie_d:studygenie_d | student_retention | 1216066735 | 132817394 | 363347068 | 230529674 | 0 | 589 | deep_crisis | — |
| studygenie | CDA | exam_trial | studygenie_a:studygenie_a | NONE | 1314749159 | 235684277 | 363347068 | 127662791 | 0 | 322 | deep_crisis | — |
| studygenie | CDB | exam_trial | studygenie_b:customer_churn | NONE | 1308822962 | 230587748 | 363347068 | 132759320 | 0 | 340 | deep_crisis | — |
| studygenie | CDC | exam_trial | studygenie_c:studygenie_c | NONE | 1305689231 | 227892739 | 363347068 | 135454329 | 0 | 350 | deep_crisis | — |
| studygenie | CDD | exam_trial | studygenie_d:studygenie_d | NONE | 1353867293 | 269325873 | 363347068 | 94021195 | 0 | 181 | survived | — |
| studygenie | DAA | — | studygenie_a:studygenie_a | NONE | 1321535651 | 241520658 | 363347068 | 121826410 | 0 | 293 | survived | — |
| studygenie | DAB | — | studygenie_b:customer_churn | NONE | 1291071253 | 215321275 | 363347068 | 148025793 | 0 | 386 | deep_crisis | — |
| studygenie | DAC | — | studygenie_c:studygenie_c | NONE | 1290708811 | 215009576 | 363347068 | 148337492 | 0 | 387 | deep_crisis | — |
| studygenie | DAD | — | studygenie_d:studygenie_d | NONE | 1319555415 | 239817655 | 363347068 | 123529413 | 0 | 294 | survived | — |
| studygenie | DBA | — | studygenie_a:studygenie_a | NONE | 1298953743 | 212100218 | 363347068 | 151246850 | 0 | 389 | deep_crisis | — |
| studygenie | DBB | — | studygenie_b:customer_churn | NONE | 1319116130 | 229439870 | 363347068 | 133907198 | 0 | 330 | deep_crisis | — |
| studygenie | DBC | — | studygenie_c:studygenie_c | NONE | 1294591177 | 208348410 | 363347068 | 154998658 | 0 | 402 | deep_crisis | — |
| studygenie | DBD | — | studygenie_d:studygenie_d | NONE | 1322821503 | 232626491 | 363347068 | 130720577 | 0 | 311 | survived | — |
| studygenie | DCA | — | studygenie_a:studygenie_a | NONE | 1294275816 | 218077201 | 363347068 | 145269867 | 0 | 376 | deep_crisis | — |
| studygenie | DCB | — | studygenie_b:customer_churn | NONE | 1290757678 | 215051601 | 363347068 | 148295467 | 0 | 387 | deep_crisis | — |
| studygenie | DCC | — | studygenie_c:studygenie_c | NONE | 1315827944 | 236612031 | 363347068 | 126735037 | 0 | 313 | deep_crisis | — |
| studygenie | DCD | — | studygenie_d:studygenie_d | NONE | 1315936109 | 236705053 | 363347068 | 126642015 | 0 | 306 | survived | — |
| studygenie | DDA | — | studygenie_a:studygenie_a | NONE | 1330482587 | 249215024 | 363347068 | 114132044 | 0 | 289 | deep_crisis | — |
| studygenie | DDB | — | studygenie_b:customer_churn | NONE | 1324556390 | 244118495 | 363347068 | 119228573 | 0 | 308 | deep_crisis | — |
| studygenie | DDC | — | studygenie_c:studygenie_c | NONE | 1321422659 | 241423486 | 363347068 | 121923582 | 0 | 317 | deep_crisis | — |
| studygenie | DDD | — | studygenie_d:studygenie_d | NONE | 1369600721 | 282856620 | 363347068 | 80490448 | 0 | 155 | survived | — |
| sleepwork | AAA | renewal_risk, utilization_exposed | sleepwork_a:sleepwork_a | flexible_lease | 1240635109 | 143631876 | 386452590 | 242820714 | 0 | 601 | near_bankruptcy | — |
| sleepwork | AAB | renewal_risk, utilization_exposed | sleepwork_b:customer_churn | flexible_lease | 1324878080 | 195917095 | 386452590 | 190535495 | 0 | 474 | deep_crisis | — |
| sleepwork | AAC | renewal_risk, utilization_exposed | sleepwork_c:sleepwork_c | flexible_lease | 1319723682 | 197412104 | 386452590 | 189040486 | 0 | 472 | deep_crisis | — |
| sleepwork | AAD | renewal_risk, utilization_exposed | sleepwork_d:sleepwork_d | flexible_lease, price_retention | 1340914484 | 201821849 | 386452590 | 184630741 | 0 | 453 | deep_crisis | — |
| sleepwork | ABA | utilization_exposed | sleepwork_a:sleepwork_a | NONE | 1373895925 | 249249230 | 386452590 | 137203360 | 0 | 355 | deep_crisis | — |
| sleepwork | ABB | utilization_exposed | sleepwork_b:customer_churn | NONE | 1410161475 | 268909804 | 386452590 | 117542786 | 0 | 292 | deep_crisis | — |
| sleepwork | ABC | utilization_exposed | sleepwork_c:sleepwork_c | NONE | 1370694429 | 247072214 | 386452590 | 139380376 | 0 | 361 | deep_crisis | — |
| sleepwork | ABD | utilization_exposed | sleepwork_d:sleepwork_d | price_retention | 1392739572 | 252062910 | 386452590 | 134389680 | 0 | 336 | deep_crisis | — |
| sleepwork | ACA | utilization_exposed | sleepwork_a:sleepwork_a | digital_wellness | 1412049875 | 265193916 | 386452590 | 121258674 | 0 | 312 | deep_crisis | — |
| sleepwork | ACB | utilization_exposed | sleepwork_b:customer_churn | digital_wellness | 1413309893 | 261050727 | 386452590 | 125401863 | 0 | 320 | deep_crisis | — |
| sleepwork | ACC | utilization_exposed | sleepwork_c:sleepwork_c | digital_wellness | 1461850995 | 299058677 | 386452590 | 87393913 | 0 | 199 | survived | — |
| sleepwork | ACD | utilization_exposed | sleepwork_d:sleepwork_d | digital_wellness, price_retention | 1430791301 | 267938084 | 386452590 | 118514506 | 0 | 289 | deep_crisis | — |
| sleepwork | ADA | utilization_exposed | sleepwork_a:sleepwork_a | price_retention | 1396620294 | 264701801 | 386452590 | 121750789 | 0 | 321 | deep_crisis | — |
| sleepwork | ADB | utilization_exposed | sleepwork_b:customer_churn | price_retention | 1399013473 | 261329163 | 386452590 | 125123427 | 0 | 327 | deep_crisis | — |
| sleepwork | ADC | utilization_exposed | sleepwork_c:sleepwork_c | price_retention | 1393649734 | 262681821 | 386452590 | 123770769 | 0 | 327 | deep_crisis | — |
| sleepwork | ADD | utilization_exposed | sleepwork_d:sleepwork_d | price_retention | 1440272868 | 294385551 | 386452590 | 92067039 | 0 | 235 | deep_crisis | — |
| sleepwork | BAA | space_cost_exposed | sleepwork_a:sleepwork_a | NONE | 1418172266 | 289357142 | 386452590 | 97095448 | 0 | 247 | deep_crisis | — |
| sleepwork | BAB | space_cost_exposed | sleepwork_b:customer_churn | NONE | 1389965025 | 265176219 | 386452590 | 121276371 | 0 | 317 | deep_crisis | — |
| sleepwork | BAC | space_cost_exposed | sleepwork_c:sleepwork_c | NONE | 1384480002 | 266446404 | 386452590 | 120006186 | 0 | 317 | deep_crisis | — |
| sleepwork | BAD | space_cost_exposed | sleepwork_d:sleepwork_d | price_retention | 1406476522 | 271404037 | 386452590 | 115048553 | 0 | 290 | deep_crisis | — |
| sleepwork | BBA | space_cost_exposed, space_reallocation | sleepwork_a:sleepwork_a | compact_redeploy | 1346199465 | 159037429 | 386452590 | 227415161 | 0 | 555 | deep_crisis | — |
| sleepwork | BBB | space_cost_exposed, space_reallocation | sleepwork_b:customer_churn | compact_redeploy, cost_cut | 1114095020 | 0 | 386452590 | 386452590 | 26791013 | 900 | bankrupt | 9 |
| sleepwork | BBC | space_cost_exposed, space_reallocation | sleepwork_c:sleepwork_c | compact_redeploy | 1342997969 | 156598589 | 386452590 | 229854001 | 0 | 561 | deep_crisis | — |
| sleepwork | BBD | space_cost_exposed, space_reallocation | sleepwork_d:sleepwork_d | compact_redeploy, price_retention | 1365043112 | 161655321 | 386452590 | 224797269 | 0 | 542 | deep_crisis | — |
| sleepwork | BCA | space_cost_exposed | sleepwork_a:sleepwork_a | digital_wellness | 1414724463 | 267012636 | 386452590 | 119439954 | 0 | 308 | deep_crisis | — |
| sleepwork | BCB | space_cost_exposed | sleepwork_b:customer_churn | digital_wellness | 1415984481 | 262869447 | 386452590 | 123583143 | 0 | 316 | deep_crisis | — |
| sleepwork | BCC | space_cost_exposed | sleepwork_c:sleepwork_c | digital_wellness | 1464525583 | 300877397 | 386452590 | 85575193 | 0 | 195 | survived | — |
| sleepwork | BCD | space_cost_exposed | sleepwork_d:sleepwork_d | digital_wellness, price_retention | 1433465889 | 269756804 | 386452590 | 116695786 | 0 | 284 | deep_crisis | — |
| sleepwork | BDA | space_cost_exposed | sleepwork_a:sleepwork_a | price_retention | 1399294882 | 266520521 | 386452590 | 119932069 | 0 | 317 | deep_crisis | — |
| sleepwork | BDB | space_cost_exposed | sleepwork_b:customer_churn | price_retention | 1401688061 | 263147883 | 386452590 | 123304707 | 0 | 323 | deep_crisis | — |
| sleepwork | BDC | space_cost_exposed | sleepwork_c:sleepwork_c | price_retention | 1396324322 | 264500541 | 386452590 | 121952049 | 0 | 323 | deep_crisis | — |
| sleepwork | BDD | space_cost_exposed | sleepwork_d:sleepwork_d | price_retention | 1442947456 | 296204271 | 386452590 | 90248319 | 0 | 231 | deep_crisis | — |
| sleepwork | CAA | no_hardware_trial | sleepwork_a:sleepwork_a | NONE | 1414160384 | 286629062 | 386452590 | 99823528 | 0 | 254 | deep_crisis | — |
| sleepwork | CAB | no_hardware_trial | sleepwork_b:customer_churn | NONE | 1385953143 | 262448139 | 386452590 | 124004451 | 0 | 323 | deep_crisis | — |
| sleepwork | CAC | no_hardware_trial | sleepwork_c:sleepwork_c | NONE | 1380468120 | 263718324 | 386452590 | 122734266 | 0 | 323 | deep_crisis | — |
| sleepwork | CAD | no_hardware_trial | sleepwork_d:sleepwork_d | price_retention | 1402464640 | 268675957 | 386452590 | 117776633 | 0 | 296 | deep_crisis | — |
| sleepwork | CBA | no_hardware_trial | sleepwork_a:sleepwork_a | NONE | 1372558631 | 248339870 | 386452590 | 138112720 | 0 | 357 | deep_crisis | — |
| sleepwork | CBB | no_hardware_trial | sleepwork_b:customer_churn | NONE | 1408824181 | 268000444 | 386452590 | 118452146 | 0 | 295 | deep_crisis | — |
| sleepwork | CBC | no_hardware_trial | sleepwork_c:sleepwork_c | NONE | 1369357135 | 246162854 | 386452590 | 140289736 | 0 | 363 | deep_crisis | — |
| sleepwork | CBD | no_hardware_trial | sleepwork_d:sleepwork_d | price_retention | 1391402278 | 251153550 | 386452590 | 135299040 | 0 | 338 | deep_crisis | — |
| sleepwork | CCA | no_hardware_trial, wellness_switch | sleepwork_a:sleepwork_a | digital_wellness | 1327183773 | 207484966 | 386452590 | 178967624 | 0 | 448 | deep_crisis | — |
| sleepwork | CCB | no_hardware_trial, wellness_switch | sleepwork_b:customer_churn | digital_wellness | 1328204672 | 203179176 | 386452590 | 183273414 | 0 | 457 | deep_crisis | — |
| sleepwork | CCC | no_hardware_trial, wellness_switch | sleepwork_c:sleepwork_c | digital_wellness | 1267456390 | 166870346 | 386452590 | 219582244 | 0 | 549 | near_bankruptcy | — |
| sleepwork | CCD | no_hardware_trial, wellness_switch | sleepwork_d:sleepwork_d | digital_wellness, price_retention | 1344892311 | 209526771 | 386452590 | 176925819 | 0 | 434 | deep_crisis | — |
| sleepwork | CDA | no_hardware_trial | sleepwork_a:sleepwork_a | price_retention | 1395283000 | 263792441 | 386452590 | 122660149 | 0 | 323 | deep_crisis | — |
| sleepwork | CDB | no_hardware_trial | sleepwork_b:customer_churn | price_retention | 1397676179 | 260419803 | 386452590 | 126032787 | 0 | 329 | deep_crisis | — |
| sleepwork | CDC | no_hardware_trial | sleepwork_c:sleepwork_c | price_retention | 1392312440 | 261772461 | 386452590 | 124680129 | 0 | 329 | deep_crisis | — |
| sleepwork | CDD | no_hardware_trial | sleepwork_d:sleepwork_d | price_retention | 1438935574 | 293476191 | 386452590 | 92976399 | 0 | 237 | deep_crisis | — |
| sleepwork | DAA | — | sleepwork_a:sleepwork_a | NONE | 1410148502 | 283900982 | 386452590 | 102551608 | 0 | 260 | deep_crisis | — |
| sleepwork | DAB | — | sleepwork_b:customer_churn | NONE | 1381941261 | 259720059 | 386452590 | 126732531 | 0 | 329 | deep_crisis | — |
| sleepwork | DAC | — | sleepwork_c:sleepwork_c | NONE | 1376456238 | 260990244 | 386452590 | 125462346 | 0 | 329 | deep_crisis | — |
| sleepwork | DAD | — | sleepwork_d:sleepwork_d | price_retention | 1398452758 | 265947877 | 386452590 | 120504713 | 0 | 302 | deep_crisis | — |
| sleepwork | DBA | — | sleepwork_a:sleepwork_a | NONE | 1368546749 | 245611790 | 386452590 | 140840800 | 0 | 363 | deep_crisis | — |
| sleepwork | DBB | — | sleepwork_b:customer_churn | NONE | 1404812299 | 265272364 | 386452590 | 121180226 | 0 | 301 | deep_crisis | — |
| sleepwork | DBC | — | sleepwork_c:sleepwork_c | NONE | 1365345253 | 243434774 | 386452590 | 143017816 | 0 | 369 | deep_crisis | — |
| sleepwork | DBD | — | sleepwork_d:sleepwork_d | price_retention | 1387390396 | 248425470 | 386452590 | 138027120 | 0 | 344 | deep_crisis | — |
| sleepwork | DCA | — | sleepwork_a:sleepwork_a | digital_wellness | 1406700699 | 261556476 | 386452590 | 124896114 | 0 | 320 | deep_crisis | — |
| sleepwork | DCB | — | sleepwork_b:customer_churn | digital_wellness | 1407960717 | 257413287 | 386452590 | 129039303 | 0 | 328 | deep_crisis | — |
| sleepwork | DCC | — | sleepwork_c:sleepwork_c | digital_wellness | 1456501819 | 295421237 | 386452590 | 91031353 | 0 | 208 | survived | — |
| sleepwork | DCD | — | sleepwork_d:sleepwork_d | digital_wellness, price_retention | 1425442125 | 264300644 | 386452590 | 122151946 | 0 | 297 | deep_crisis | — |
| sleepwork | DDA | — | sleepwork_a:sleepwork_a | price_retention | 1391271118 | 261064361 | 386452590 | 125388229 | 0 | 329 | deep_crisis | — |
| sleepwork | DDB | — | sleepwork_b:customer_churn | price_retention | 1393664297 | 257691723 | 386452590 | 128760867 | 0 | 335 | deep_crisis | — |
| sleepwork | DDC | — | sleepwork_c:sleepwork_c | price_retention | 1388300558 | 259044381 | 386452590 | 127408209 | 0 | 335 | deep_crisis | — |
| sleepwork | DDD | — | sleepwork_d:sleepwork_d | price_retention | 1434923692 | 290748111 | 386452590 | 95704479 | 0 | 243 | deep_crisis | — |
| fitmirror | AAA | affordability_crisis, price_pressure | fitmirror_a:fitmirror_a | financing_tradein | 2050194105 | 208007952 | 586042321 | 378034369 | 0 | 614 | near_bankruptcy | — |
| fitmirror | AAB | affordability_crisis, price_pressure | fitmirror_b:fitmirror_b | financing_tradein | 2235624081 | 319717734 | 586042321 | 266324587 | 0 | 415 | deep_crisis | — |
| fitmirror | AAC | affordability_crisis, price_pressure | fitmirror_c:fitmirror_c | financing_tradein | 2127831354 | 254618672 | 586042321 | 331423649 | 0 | 539 | deep_crisis | — |
| fitmirror | AAD | affordability_crisis, price_pressure | fitmirror_d:fitmirror_d | financing_tradein | 2188632441 | 292455337 | 586042321 | 293586984 | 0 | 471 | deep_crisis | — |
| fitmirror | ABA | price_pressure | fitmirror_a:fitmirror_a | NONE | 2299323257 | 408573653 | 586042321 | 177468668 | 0 | 299 | deep_crisis | — |
| fitmirror | ABB | price_pressure | fitmirror_b:fitmirror_b | NONE | 2429229522 | 490414599 | 586042321 | 95627722 | 0 | 114 | survived | — |
| fitmirror | ABC | price_pressure | fitmirror_c:fitmirror_c | NONE | 2279554184 | 396119137 | 586042321 | 189923184 | 0 | 324 | deep_crisis | — |
| fitmirror | ABD | price_pressure | fitmirror_d:fitmirror_d | NONE | 2339240669 | 433721622 | 586042321 | 152320699 | 0 | 242 | survived | — |
| fitmirror | ACA | price_pressure | fitmirror_a:fitmirror_a | mobile_mode | 2258021599 | 344553607 | 586042321 | 241488714 | 0 | 394 | deep_crisis | — |
| fitmirror | ACB | price_pressure | fitmirror_b:fitmirror_b | mobile_mode | 2355261909 | 405815002 | 586042321 | 180227319 | 0 | 246 | survived | — |
| fitmirror | ACC | price_pressure | fitmirror_c:fitmirror_c | mobile_mode | 2353497452 | 404703394 | 586042321 | 181338927 | 0 | 254 | survived | — |
| fitmirror | ACD | price_pressure | fitmirror_d:fitmirror_d | mobile_mode | 2296056992 | 368515904 | 586042321 | 217526417 | 0 | 343 | deep_crisis | — |
| fitmirror | ADA | price_pressure | fitmirror_a:fitmirror_a | NONE | 2272081924 | 391411611 | 586042321 | 194630710 | 0 | 325 | deep_crisis | — |
| fitmirror | ADB | price_pressure | fitmirror_b:fitmirror_b | NONE | 2364017083 | 449330761 | 586042321 | 136711560 | 0 | 180 | survived | — |
| fitmirror | ADC | price_pressure | fitmirror_c:fitmirror_c | NONE | 2247146581 | 375702344 | 586042321 | 210339977 | 0 | 357 | deep_crisis | — |
| fitmirror | ADD | price_pressure | fitmirror_d:fitmirror_d | NONE | 2343040720 | 436115652 | 586042321 | 149926669 | 0 | 224 | survived | — |
| fitmirror | BAA | retention_doubt | fitmirror_a:fitmirror_a | NONE | 2290530912 | 403034475 | 586042321 | 183007846 | 0 | 297 | deep_crisis | — |
| fitmirror | BAB | retention_doubt | fitmirror_b:fitmirror_b | NONE | 2330390834 | 428146225 | 586042321 | 157896096 | 0 | 229 | survived | — |
| fitmirror | BAC | retention_doubt | fitmirror_c:fitmirror_c | NONE | 2218568614 | 357698226 | 586042321 | 228344095 | 0 | 386 | deep_crisis | — |
| fitmirror | BAD | retention_doubt | fitmirror_d:fitmirror_d | NONE | 2280056179 | 396435393 | 586042321 | 189606928 | 0 | 308 | deep_crisis | — |
| fitmirror | BBA | retention_doubt, subscription_churn | fitmirror_a:fitmirror_a | bundled_subscription | 2267991478 | 370834633 | 586042321 | 215207688 | 0 | 363 | deep_crisis | — |
| fitmirror | BBB | retention_doubt, subscription_churn | fitmirror_b:fitmirror_b | bundled_subscription | 1909748738 | 145141707 | 586042321 | 440900614 | 0 | 712 | near_bankruptcy | — |
| fitmirror | BBC | retention_doubt, subscription_churn | fitmirror_c:fitmirror_c | bundled_subscription | 2252053073 | 360793438 | 586042321 | 225248883 | 0 | 382 | deep_crisis | — |
| fitmirror | BBD | retention_doubt, subscription_churn | fitmirror_d:fitmirror_d | bundled_subscription | 2307908890 | 395982602 | 586042321 | 190059719 | 0 | 312 | deep_crisis | — |
| fitmirror | BCA | retention_doubt | fitmirror_a:fitmirror_a | mobile_mode | 2278121351 | 357216452 | 586042321 | 228825869 | 0 | 375 | deep_crisis | — |
| fitmirror | BCB | retention_doubt | fitmirror_b:fitmirror_b | mobile_mode | 2375361661 | 418477847 | 586042321 | 167564474 | 0 | 225 | survived | — |
| fitmirror | BCC | retention_doubt | fitmirror_c:fitmirror_c | mobile_mode | 2373597204 | 417366239 | 586042321 | 168676082 | 0 | 234 | survived | — |
| fitmirror | BCD | retention_doubt | fitmirror_d:fitmirror_d | mobile_mode | 2316156744 | 381178749 | 586042321 | 204863572 | 0 | 324 | deep_crisis | — |
| fitmirror | BDA | retention_doubt | fitmirror_a:fitmirror_a | NONE | 2292181676 | 404074456 | 586042321 | 181967865 | 0 | 307 | deep_crisis | — |
| fitmirror | BDB | retention_doubt | fitmirror_b:fitmirror_b | NONE | 2384116835 | 461993606 | 586042321 | 124048715 | 0 | 160 | survived | — |
| fitmirror | BDC | retention_doubt | fitmirror_c:fitmirror_c | NONE | 2267246333 | 388365189 | 586042321 | 197677132 | 0 | 338 | deep_crisis | — |
| fitmirror | BDD | retention_doubt | fitmirror_d:fitmirror_d | NONE | 2363140472 | 448778497 | 586042321 | 137263824 | 0 | 204 | survived | — |
| fitmirror | CAA | phone_substitute | fitmirror_a:fitmirror_a | NONE | 2273959307 | 392594363 | 586042321 | 193447958 | 0 | 313 | deep_crisis | — |
| fitmirror | CAB | phone_substitute | fitmirror_b:fitmirror_b | NONE | 2313819229 | 417706113 | 586042321 | 168336208 | 0 | 245 | survived | — |
| fitmirror | CAC | phone_substitute | fitmirror_c:fitmirror_c | NONE | 2201997009 | 347258114 | 586042321 | 238784207 | 0 | 401 | deep_crisis | — |
| fitmirror | CAD | phone_substitute | fitmirror_d:fitmirror_d | NONE | 2263484574 | 385995281 | 586042321 | 200047040 | 0 | 324 | deep_crisis | — |
| fitmirror | CBA | phone_substitute | fitmirror_a:fitmirror_a | NONE | 2302851404 | 410796386 | 586042321 | 175245935 | 0 | 295 | deep_crisis | — |
| fitmirror | CBB | phone_substitute | fitmirror_b:fitmirror_b | NONE | 2432757669 | 492637332 | 586042321 | 93404989 | 0 | 112 | survived | — |
| fitmirror | CBC | phone_substitute | fitmirror_c:fitmirror_c | NONE | 2283082331 | 398341870 | 586042321 | 187700451 | 0 | 321 | deep_crisis | — |
| fitmirror | CBD | phone_substitute | fitmirror_d:fitmirror_d | NONE | 2342768816 | 435944355 | 586042321 | 150097966 | 0 | 239 | survived | — |
| fitmirror | CCA | hardware_substitution, phone_substitute | fitmirror_a:fitmirror_a | mobile_mode | 2132124321 | 265238321 | 586042321 | 320804000 | 0 | 518 | deep_crisis | — |
| fitmirror | CCB | hardware_substitution, phone_substitute | fitmirror_b:fitmirror_b | mobile_mode | 2223648998 | 322898869 | 586042321 | 263143452 | 0 | 401 | deep_crisis | — |
| fitmirror | CCC | hardware_substitution, phone_substitute | fitmirror_c:fitmirror_c | mobile_mode | 2007315476 | 186608749 | 586042321 | 399433572 | 0 | 645 | near_bankruptcy | — |
| fitmirror | CCD | hardware_substitution, phone_substitute | fitmirror_d:fitmirror_d | mobile_mode | 2168122464 | 287917151 | 586042321 | 298125170 | 0 | 476 | deep_crisis | — |
| fitmirror | CDA | phone_substitute | fitmirror_a:fitmirror_a | NONE | 2275610071 | 393634344 | 586042321 | 192407977 | 0 | 322 | deep_crisis | — |
| fitmirror | CDB | phone_substitute | fitmirror_b:fitmirror_b | NONE | 2367545230 | 451553494 | 586042321 | 134488827 | 0 | 177 | survived | — |
| fitmirror | CDC | phone_substitute | fitmirror_c:fitmirror_c | NONE | 2250674728 | 377925077 | 586042321 | 208117244 | 0 | 353 | deep_crisis | — |
| fitmirror | CDD | phone_substitute | fitmirror_d:fitmirror_d | NONE | 2346568867 | 438338385 | 586042321 | 147703936 | 0 | 220 | survived | — |
| fitmirror | DAA | — | fitmirror_a:fitmirror_a | NONE | 2278342764 | 395355942 | 586042321 | 190686379 | 0 | 309 | deep_crisis | — |
| fitmirror | DAB | — | fitmirror_b:fitmirror_b | NONE | 2318202686 | 420467692 | 586042321 | 165574629 | 0 | 241 | survived | — |
| fitmirror | DAC | — | fitmirror_c:fitmirror_c | NONE | 2206380466 | 350019693 | 586042321 | 236022628 | 0 | 397 | deep_crisis | — |
| fitmirror | DAD | — | fitmirror_d:fitmirror_d | NONE | 2267868031 | 388756860 | 586042321 | 197285461 | 0 | 320 | deep_crisis | — |
| fitmirror | DBA | — | fitmirror_a:fitmirror_a | NONE | 2307234861 | 413557965 | 586042321 | 172484356 | 0 | 291 | deep_crisis | — |
| fitmirror | DBB | — | fitmirror_b:fitmirror_b | NONE | 2437141126 | 495398911 | 586042321 | 90643410 | 0 | 108 | survived | — |
| fitmirror | DBC | — | fitmirror_c:fitmirror_c | NONE | 2287465788 | 401103449 | 586042321 | 184938872 | 0 | 317 | deep_crisis | — |
| fitmirror | DBD | — | fitmirror_d:fitmirror_d | NONE | 2347152273 | 438705934 | 586042321 | 147336387 | 0 | 234 | survived | — |
| fitmirror | DCA | — | fitmirror_a:fitmirror_a | mobile_mode | 2265933203 | 349537919 | 586042321 | 236504402 | 0 | 387 | deep_crisis | — |
| fitmirror | DCB | — | fitmirror_b:fitmirror_b | mobile_mode | 2363173513 | 410799314 | 586042321 | 175243007 | 0 | 238 | survived | — |
| fitmirror | DCC | — | fitmirror_c:fitmirror_c | mobile_mode | 2361409056 | 409687706 | 586042321 | 176354615 | 0 | 246 | survived | — |
| fitmirror | DCD | — | fitmirror_d:fitmirror_d | mobile_mode | 2303968596 | 373500216 | 586042321 | 212542105 | 0 | 336 | deep_crisis | — |
| fitmirror | DDA | — | fitmirror_a:fitmirror_a | NONE | 2279993528 | 396395923 | 586042321 | 189646398 | 0 | 318 | deep_crisis | — |
| fitmirror | DDB | — | fitmirror_b:fitmirror_b | NONE | 2371928687 | 454315073 | 586042321 | 131727248 | 0 | 172 | survived | — |
| fitmirror | DDC | — | fitmirror_c:fitmirror_c | NONE | 2255058185 | 380686656 | 586042321 | 205355665 | 0 | 349 | deep_crisis | — |
| fitmirror | DDD | — | fitmirror_d:fitmirror_d | NONE | 2350952324 | 441099964 | 586042321 | 144942357 | 0 | 216 | survived | — |
| cloudkitchen | AAA | discovery_crisis, ranking_pressure | cloudkitchen_a:cloudkitchen_a | direct_channel | 2297021578 | 81581557 | 559817926 | 478236369 | 0 | 779 | near_bankruptcy | — |
| cloudkitchen | AAB | discovery_crisis, ranking_pressure | cloudkitchen_b:customer_churn | direct_channel | 2415925928 | 160789906 | 559817926 | 399028020 | 0 | 644 | deep_crisis | — |
| cloudkitchen | AAC | discovery_crisis, ranking_pressure | cloudkitchen_c:cloudkitchen_c | direct_channel | 2393503602 | 158681850 | 559817926 | 401136076 | 0 | 652 | near_bankruptcy | — |
| cloudkitchen | AAD | discovery_crisis, ranking_pressure | cloudkitchen_d:cloudkitchen_d | direct_channel | 2505731018 | 217047891 | 559817926 | 342770035 | 0 | 518 | deep_crisis | — |
| cloudkitchen | ABA | ranking_pressure | cloudkitchen_a:cloudkitchen_a | NONE | 2505981449 | 298409425 | 559817926 | 261408501 | 0 | 414 | deep_crisis | — |
| cloudkitchen | ABB | ranking_pressure | cloudkitchen_b:customer_churn | NONE | 2584734865 | 333298873 | 559817926 | 226519053 | 0 | 302 | deep_crisis | — |
| cloudkitchen | ABC | ranking_pressure | cloudkitchen_c:cloudkitchen_c | NONE | 2505981449 | 298409425 | 559817926 | 261408501 | 0 | 414 | deep_crisis | — |
| cloudkitchen | ABD | ranking_pressure | cloudkitchen_d:cloudkitchen_d | NONE | 2624852536 | 366165945 | 559817926 | 193651981 | 0 | 242 | survived | — |
| cloudkitchen | ACA | ranking_pressure | cloudkitchen_a:cloudkitchen_a | NONE | 2474605719 | 295525259 | 559817926 | 264292667 | 0 | 423 | deep_crisis | — |
| cloudkitchen | ACB | ranking_pressure | cloudkitchen_b:customer_churn | NONE | 2497393790 | 298514460 | 559817926 | 261303466 | 0 | 406 | deep_crisis | — |
| cloudkitchen | ACC | ranking_pressure | cloudkitchen_c:cloudkitchen_c | unique_menu_loyalty | 2582024108 | 331753741 | 559817926 | 228064185 | 0 | 285 | deep_crisis | — |
| cloudkitchen | ACD | ranking_pressure | cloudkitchen_d:cloudkitchen_d | NONE | 2590154971 | 361388332 | 559817926 | 198429594 | 0 | 248 | survived | — |
| cloudkitchen | ADA | ranking_pressure | cloudkitchen_a:cloudkitchen_a | NONE | 2612204817 | 373956746 | 559817926 | 185861180 | 0 | 274 | survived | — |
| cloudkitchen | ADB | ranking_pressure | cloudkitchen_b:customer_churn | NONE | 2637554787 | 378406229 | 559817926 | 181411697 | 0 | 244 | survived | — |
| cloudkitchen | ADC | ranking_pressure | cloudkitchen_c:cloudkitchen_c | unique_menu_loyalty | 2656254250 | 374064923 | 559817926 | 185753003 | 0 | 232 | survived | — |
| cloudkitchen | ADD | ranking_pressure | cloudkitchen_d:cloudkitchen_d | NONE | 2772453667 | 465298589 | 559817926 | 94519337 | 0 | 118 | survived | — |
| cloudkitchen | BAA | supply_pressure | cloudkitchen_a:cloudkitchen_a | NONE | 2555800472 | 326806268 | 559817926 | 233011658 | 0 | 338 | deep_crisis | — |
| cloudkitchen | BAB | supply_pressure | cloudkitchen_b:customer_churn | NONE | 2518682396 | 295648965 | 559817926 | 264168961 | 0 | 409 | deep_crisis | — |
| cloudkitchen | BAC | supply_pressure | cloudkitchen_c:cloudkitchen_c | NONE | 2495725326 | 292563435 | 559817926 | 267254491 | 0 | 426 | deep_crisis | — |
| cloudkitchen | BAD | supply_pressure | cloudkitchen_d:cloudkitchen_d | NONE | 2612400540 | 359068307 | 559817926 | 200749619 | 0 | 251 | survived | — |
| cloudkitchen | BBA | menu_shortage, supply_pressure | cloudkitchen_a:cloudkitchen_a | second_supplier | 2447438882 | 153584620 | 559817926 | 406233306 | 0 | 656 | deep_crisis | — |
| cloudkitchen | BBB | menu_shortage, supply_pressure | cloudkitchen_b:customer_churn | second_supplier, cost_cut | 2094463080 | 0 | 559817926 | 559817926 | 64661766 | 900 | bankrupt | 9 |
| cloudkitchen | BBC | menu_shortage, supply_pressure | cloudkitchen_c:cloudkitchen_c | second_supplier | 2447438882 | 153584620 | 559817926 | 406233306 | 0 | 656 | deep_crisis | — |
| cloudkitchen | BBD | menu_shortage, supply_pressure | cloudkitchen_d:cloudkitchen_d | second_supplier | 2565127533 | 215860966 | 559817926 | 343956960 | 0 | 503 | deep_crisis | — |
| cloudkitchen | BCA | supply_pressure | cloudkitchen_a:cloudkitchen_a | NONE | 2485304072 | 286623320 | 559817926 | 273194606 | 0 | 437 | deep_crisis | — |
| cloudkitchen | BCB | supply_pressure | cloudkitchen_b:customer_churn | NONE | 2508092143 | 289612521 | 559817926 | 270205405 | 0 | 421 | deep_crisis | — |
| cloudkitchen | BCC | supply_pressure | cloudkitchen_c:cloudkitchen_c | unique_menu_loyalty | 2592722461 | 322851802 | 559817926 | 236966124 | 0 | 296 | deep_crisis | — |
| cloudkitchen | BCD | supply_pressure | cloudkitchen_d:cloudkitchen_d | NONE | 2600853324 | 352486393 | 559817926 | 207331533 | 0 | 259 | survived | — |
| cloudkitchen | BDA | supply_pressure | cloudkitchen_a:cloudkitchen_a | NONE | 2622903170 | 365054807 | 559817926 | 194763119 | 0 | 289 | survived | — |
| cloudkitchen | BDB | supply_pressure | cloudkitchen_b:customer_churn | NONE | 2648253140 | 369504290 | 559817926 | 190313636 | 0 | 259 | survived | — |
| cloudkitchen | BDC | supply_pressure | cloudkitchen_c:cloudkitchen_c | unique_menu_loyalty | 2666952603 | 365162984 | 559817926 | 194654942 | 0 | 243 | survived | — |
| cloudkitchen | BDD | supply_pressure | cloudkitchen_d:cloudkitchen_d | NONE | 2783152020 | 456396650 | 559817926 | 103421276 | 0 | 129 | survived | — |
| cloudkitchen | CAA | menu_clone | cloudkitchen_a:cloudkitchen_a | NONE | 2539752943 | 332659177 | 559817926 | 227158749 | 0 | 328 | deep_crisis | — |
| cloudkitchen | CAB | menu_clone | cloudkitchen_b:customer_churn | NONE | 2502634867 | 301501874 | 559817926 | 258316052 | 0 | 400 | deep_crisis | — |
| cloudkitchen | CAC | menu_clone | cloudkitchen_c:cloudkitchen_c | NONE | 2479677797 | 298416344 | 559817926 | 261401582 | 0 | 417 | deep_crisis | — |
| cloudkitchen | CAD | menu_clone | cloudkitchen_d:cloudkitchen_d | NONE | 2596353011 | 364921216 | 559817926 | 194896710 | 0 | 244 | survived | — |
| cloudkitchen | CBA | menu_clone | cloudkitchen_a:cloudkitchen_a | NONE | 2500632273 | 295360395 | 559817926 | 264457531 | 0 | 419 | deep_crisis | — |
| cloudkitchen | CBB | menu_clone | cloudkitchen_b:customer_churn | NONE | 2579385689 | 330249843 | 559817926 | 229568083 | 0 | 308 | deep_crisis | — |
| cloudkitchen | CBC | menu_clone | cloudkitchen_c:cloudkitchen_c | NONE | 2500632273 | 295360395 | 559817926 | 264457531 | 0 | 419 | deep_crisis | — |
| cloudkitchen | CBD | menu_clone | cloudkitchen_d:cloudkitchen_d | NONE | 2619503360 | 363116915 | 559817926 | 196701011 | 0 | 246 | survived | — |
| cloudkitchen | CCA | brand_substitution, menu_clone | cloudkitchen_a:cloudkitchen_a | unique_menu_loyalty | 2333625835 | 190166726 | 559817926 | 369651200 | 0 | 602 | deep_crisis | — |
| cloudkitchen | CCB | brand_substitution, menu_clone | cloudkitchen_b:customer_churn | unique_menu_loyalty | 2354989027 | 192343746 | 559817926 | 367474180 | 0 | 593 | deep_crisis | — |
| cloudkitchen | CCC | brand_substitution, menu_clone | cloudkitchen_c:cloudkitchen_c | unique_menu_loyalty | 2253493668 | 144491390 | 559817926 | 415326536 | 0 | 685 | near_bankruptcy | — |
| cloudkitchen | CCD | brand_substitution, menu_clone | cloudkitchen_d:cloudkitchen_d | unique_menu_loyalty | 2437219759 | 249215262 | 559817926 | 310602664 | 0 | 458 | deep_crisis | — |
| cloudkitchen | CDA | menu_clone | cloudkitchen_a:cloudkitchen_a | NONE | 2606855641 | 370907716 | 559817926 | 188910210 | 0 | 279 | survived | — |
| cloudkitchen | CDB | menu_clone | cloudkitchen_b:customer_churn | NONE | 2632205611 | 375357199 | 559817926 | 184460727 | 0 | 249 | survived | — |
| cloudkitchen | CDC | menu_clone | cloudkitchen_c:cloudkitchen_c | unique_menu_loyalty | 2650905074 | 371015893 | 559817926 | 188802033 | 0 | 236 | survived | — |
| cloudkitchen | CDD | menu_clone | cloudkitchen_d:cloudkitchen_d | NONE | 2767104491 | 462249559 | 559817926 | 97568367 | 0 | 122 | survived | — |
| cloudkitchen | DAA | — | cloudkitchen_a:cloudkitchen_a | NONE | 2584434299 | 358127550 | 559817926 | 201690376 | 0 | 284 | survived | — |
| cloudkitchen | DAB | — | cloudkitchen_b:customer_churn | NONE | 2547316223 | 326970247 | 559817926 | 232847679 | 0 | 357 | deep_crisis | — |
| cloudkitchen | DAC | — | cloudkitchen_c:cloudkitchen_c | NONE | 2524359153 | 323884717 | 559817926 | 235933209 | 0 | 376 | deep_crisis | — |
| cloudkitchen | DAD | — | cloudkitchen_d:cloudkitchen_d | NONE | 2641034367 | 390389589 | 559817926 | 169428337 | 0 | 212 | survived | — |
| cloudkitchen | DBA | — | cloudkitchen_a:cloudkitchen_a | NONE | 2545313629 | 320828768 | 559817926 | 238989158 | 0 | 378 | deep_crisis | — |
| cloudkitchen | DBB | — | cloudkitchen_b:customer_churn | NONE | 2624067045 | 355718216 | 559817926 | 204099710 | 0 | 262 | survived | — |
| cloudkitchen | DBC | — | cloudkitchen_c:cloudkitchen_c | NONE | 2545313629 | 320828768 | 559817926 | 238989158 | 0 | 378 | deep_crisis | — |
| cloudkitchen | DBD | — | cloudkitchen_d:cloudkitchen_d | NONE | 2664184716 | 388585288 | 559817926 | 171232638 | 0 | 214 | survived | — |
| cloudkitchen | DCA | — | cloudkitchen_a:cloudkitchen_a | NONE | 2513937899 | 317944602 | 559817926 | 241873324 | 0 | 387 | deep_crisis | — |
| cloudkitchen | DCB | — | cloudkitchen_b:customer_churn | NONE | 2536725970 | 320933803 | 559817926 | 238884123 | 0 | 369 | deep_crisis | — |
| cloudkitchen | DCC | — | cloudkitchen_c:cloudkitchen_c | unique_menu_loyalty | 2621356288 | 354173084 | 559817926 | 205644842 | 0 | 257 | survived | — |
| cloudkitchen | DCD | — | cloudkitchen_d:cloudkitchen_d | NONE | 2629487151 | 383807675 | 559817926 | 176010251 | 0 | 220 | survived | — |
| cloudkitchen | DDA | — | cloudkitchen_a:cloudkitchen_a | NONE | 2651536997 | 396376089 | 559817926 | 163441837 | 0 | 236 | survived | — |
| cloudkitchen | DDB | — | cloudkitchen_b:customer_churn | NONE | 2676886967 | 400825572 | 559817926 | 158992354 | 0 | 205 | survived | — |
| cloudkitchen | DDC | — | cloudkitchen_c:cloudkitchen_c | unique_menu_loyalty | 2695586430 | 396484266 | 559817926 | 163333660 | 0 | 204 | survived | — |
| cloudkitchen | DDD | — | cloudkitchen_d:cloudkitchen_d | NONE | 2811785847 | 487717932 | 559817926 | 72099994 | 0 | 90 | survived | — |
| agrodrone | AAA | dealer_financing_loss, financing_pressure | agrodrone_a:agrodrone_a | seasonal_leasing | 1837378750 | 158407851 | 481269152 | 322861301 | 0 | 637 | near_bankruptcy | — |
| agrodrone | AAB | dealer_financing_loss, financing_pressure | agrodrone_b:customer_churn | seasonal_leasing | 1866388334 | 170455135 | 481269152 | 310814017 | 0 | 613 | near_bankruptcy | — |
| agrodrone | AAC | dealer_financing_loss, financing_pressure | agrodrone_c:agrodrone_c | seasonal_leasing | 1854688160 | 171563003 | 481269152 | 309706149 | 0 | 613 | near_bankruptcy | — |
| agrodrone | AAD | dealer_financing_loss, financing_pressure | agrodrone_d:agrodrone_d | seasonal_leasing | 1946821786 | 241584559 | 481269152 | 239684593 | 0 | 471 | deep_crisis | — |
| agrodrone | ABA | financing_pressure | agrodrone_a:agrodrone_a | NONE | 1958060280 | 265125814 | 481269152 | 216143338 | 0 | 442 | deep_crisis | — |
| agrodrone | ABB | financing_pressure | agrodrone_b:customer_churn | NONE | 1964451105 | 259982840 | 481269152 | 221286312 | 0 | 451 | deep_crisis | — |
| agrodrone | ABC | financing_pressure | agrodrone_c:agrodrone_c | NONE | 1917906081 | 234608622 | 481269152 | 246660530 | 0 | 504 | deep_crisis | — |
| agrodrone | ABD | financing_pressure | agrodrone_d:agrodrone_d | NONE | 2012311495 | 306356738 | 481269152 | 174912414 | 0 | 346 | deep_crisis | — |
| agrodrone | ACA | financing_pressure | agrodrone_a:agrodrone_a | NONE | 1926692992 | 256286674 | 481269152 | 224982478 | 0 | 461 | deep_crisis | — |
| agrodrone | ACB | financing_pressure | agrodrone_b:customer_churn | NONE | 1900450613 | 226342466 | 481269152 | 254926686 | 0 | 518 | deep_crisis | — |
| agrodrone | ACC | financing_pressure | agrodrone_c:agrodrone_c | drone_as_a_service | 1980497065 | 267177770 | 481269152 | 214091382 | 0 | 417 | deep_crisis | — |
| agrodrone | ACD | financing_pressure | agrodrone_d:agrodrone_d | NONE | 1983440606 | 299414860 | 481269152 | 181854292 | 0 | 364 | deep_crisis | — |
| agrodrone | ADA | financing_pressure | agrodrone_a:agrodrone_a | NONE | 2020646949 | 327691682 | 481269152 | 153577470 | 0 | 327 | deep_crisis | — |
| agrodrone | ADB | financing_pressure | agrodrone_b:customer_churn | NONE | 1991256127 | 295354657 | 481269152 | 185914495 | 0 | 394 | deep_crisis | — |
| agrodrone | ADC | financing_pressure | agrodrone_c:agrodrone_c | drone_as_a_service | 2021664122 | 298464733 | 481269152 | 182804419 | 0 | 369 | deep_crisis | — |
| agrodrone | ADD | financing_pressure | agrodrone_d:agrodrone_d | NONE | 2096533588 | 385365528 | 481269152 | 95903624 | 0 | 171 | survived | — |
| agrodrone | BAA | component_pressure | agrodrone_a:agrodrone_a | NONE | 2001531459 | 298163910 | 481269152 | 183105242 | 0 | 373 | deep_crisis | — |
| agrodrone | BAB | component_pressure | agrodrone_b:customer_churn | NONE | 1938422687 | 240201242 | 481269152 | 241067910 | 0 | 492 | deep_crisis | — |
| agrodrone | BAC | component_pressure | agrodrone_c:agrodrone_c | NONE | 1927476234 | 241881939 | 481269152 | 239387213 | 0 | 491 | deep_crisis | — |
| agrodrone | BAD | component_pressure | agrodrone_d:agrodrone_d | NONE | 2022114662 | 313807145 | 481269152 | 167462007 | 0 | 331 | deep_crisis | — |
| agrodrone | BBA | component_pressure, production_backlog | agrodrone_a:agrodrone_a | component_reserve | 1924951845 | 126125479 | 481269152 | 355143673 | 0 | 684 | near_bankruptcy | — |
| agrodrone | BBB | component_pressure, production_backlog | agrodrone_b:customer_churn | component_reserve | 1635139413 | 0 | 481269152 | 481269152 | 118020243 | 900 | bankrupt | 9 |
| agrodrone | BBC | component_pressure, production_backlog | agrodrone_c:agrodrone_c | component_reserve | 1884797646 | 95337115 | 481269152 | 385932037 | 0 | 740 | near_bankruptcy | — |
| agrodrone | BBD | component_pressure, production_backlog | agrodrone_d:agrodrone_d | component_reserve | 1979203060 | 165728867 | 481269152 | 315540285 | 0 | 605 | deep_crisis | — |
| agrodrone | BCA | component_pressure | agrodrone_a:agrodrone_a | NONE | 1929914668 | 243735148 | 481269152 | 237534004 | 0 | 482 | deep_crisis | — |
| agrodrone | BCB | component_pressure | agrodrone_b:customer_churn | NONE | 1903672289 | 213790940 | 481269152 | 267478212 | 0 | 539 | deep_crisis | — |
| agrodrone | BCC | component_pressure | agrodrone_c:agrodrone_c | drone_as_a_service | 1983718741 | 254626244 | 481269152 | 226642908 | 0 | 440 | deep_crisis | — |
| agrodrone | BCD | component_pressure | agrodrone_d:agrodrone_d | NONE | 1986662282 | 286863334 | 481269152 | 194405818 | 0 | 386 | deep_crisis | — |
| agrodrone | BDA | component_pressure | agrodrone_a:agrodrone_a | NONE | 2023868625 | 315140156 | 481269152 | 166128996 | 0 | 349 | deep_crisis | — |
| agrodrone | BDB | component_pressure | agrodrone_b:customer_churn | NONE | 1994477803 | 282803131 | 481269152 | 198466021 | 0 | 415 | deep_crisis | — |
| agrodrone | BDC | component_pressure | agrodrone_c:agrodrone_c | drone_as_a_service | 2024885798 | 285913207 | 481269152 | 195355945 | 0 | 391 | deep_crisis | — |
| agrodrone | BDD | component_pressure | agrodrone_d:agrodrone_d | NONE | 2099755264 | 372814002 | 481269152 | 108455150 | 0 | 194 | survived | — |
| agrodrone | CAA | satellite_trial | agrodrone_a:agrodrone_a | NONE | 2005137813 | 315904739 | 481269152 | 165364413 | 0 | 342 | deep_crisis | — |
| agrodrone | CAB | satellite_trial | agrodrone_b:customer_churn | NONE | 1942029041 | 257942071 | 481269152 | 223327081 | 0 | 462 | deep_crisis | — |
| agrodrone | CAC | satellite_trial | agrodrone_c:agrodrone_c | NONE | 1931082588 | 259622768 | 481269152 | 221646384 | 0 | 461 | deep_crisis | — |
| agrodrone | CAD | satellite_trial | agrodrone_d:agrodrone_d | NONE | 2025721016 | 331547974 | 481269152 | 149721178 | 0 | 299 | deep_crisis | — |
| agrodrone | CBA | satellite_trial | agrodrone_a:agrodrone_a | NONE | 1964888310 | 270315117 | 481269152 | 210954035 | 0 | 433 | deep_crisis | — |
| agrodrone | CBB | satellite_trial | agrodrone_b:customer_churn | NONE | 1971279135 | 265172143 | 481269152 | 216097009 | 0 | 442 | deep_crisis | — |
| agrodrone | CBC | satellite_trial | agrodrone_c:agrodrone_c | NONE | 1924734111 | 239797925 | 481269152 | 241471227 | 0 | 495 | deep_crisis | — |
| agrodrone | CBD | satellite_trial | agrodrone_d:agrodrone_d | NONE | 2019139525 | 311546041 | 481269152 | 169723111 | 0 | 336 | deep_crisis | — |
| agrodrone | CCA | satellite_trial, service_substitution | agrodrone_a:agrodrone_a | drone_as_a_service | 1839605174 | 160099933 | 481269152 | 321169219 | 0 | 629 | near_bankruptcy | — |
| agrodrone | CCB | satellite_trial, service_substitution | agrodrone_b:customer_churn | drone_as_a_service | 1814679441 | 131156376 | 481269152 | 350112776 | 0 | 680 | near_bankruptcy | — |
| agrodrone | CCC | satellite_trial, service_substitution | agrodrone_c:agrodrone_c | drone_as_a_service | 1729910147 | 76731712 | 481269152 | 404537440 | 0 | 776 | near_bankruptcy | — |
| agrodrone | CCD | satellite_trial, service_substitution | agrodrone_d:agrodrone_d | drone_as_a_service | 1894671887 | 201950634 | 481269152 | 279318518 | 0 | 545 | deep_crisis | — |
| agrodrone | CDA | satellite_trial | agrodrone_a:agrodrone_a | NONE | 2027474979 | 332880985 | 481269152 | 148388167 | 0 | 318 | deep_crisis | — |
| agrodrone | CDB | satellite_trial | agrodrone_b:customer_churn | NONE | 1998084157 | 300543960 | 481269152 | 180725192 | 0 | 385 | deep_crisis | — |
| agrodrone | CDC | satellite_trial | agrodrone_c:agrodrone_c | drone_as_a_service | 2028492152 | 303654036 | 481269152 | 177615116 | 0 | 359 | deep_crisis | — |
| agrodrone | CDD | satellite_trial | agrodrone_d:agrodrone_d | NONE | 2103361618 | 390554831 | 481269152 | 90714321 | 0 | 161 | survived | — |
| agrodrone | DAA | — | agrodrone_a:agrodrone_a | NONE | 2017639838 | 325406277 | 481269152 | 155862875 | 0 | 325 | deep_crisis | — |
| agrodrone | DAB | — | agrodrone_b:customer_churn | NONE | 1954531066 | 267443609 | 481269152 | 213825543 | 0 | 445 | deep_crisis | — |
| agrodrone | DAC | — | agrodrone_c:agrodrone_c | NONE | 1943584613 | 269124306 | 481269152 | 212144846 | 0 | 445 | deep_crisis | — |
| agrodrone | DAD | — | agrodrone_d:agrodrone_d | NONE | 2038223041 | 341049512 | 481269152 | 140219640 | 0 | 282 | deep_crisis | — |
| agrodrone | DBA | — | agrodrone_a:agrodrone_a | NONE | 1977390335 | 279816655 | 481269152 | 201452497 | 0 | 416 | deep_crisis | — |
| agrodrone | DBB | — | agrodrone_b:customer_churn | NONE | 1983781160 | 274673681 | 481269152 | 206595471 | 0 | 425 | deep_crisis | — |
| agrodrone | DBC | — | agrodrone_c:agrodrone_c | NONE | 1937236136 | 249299463 | 481269152 | 231969689 | 0 | 479 | deep_crisis | — |
| agrodrone | DBD | — | agrodrone_d:agrodrone_d | NONE | 2031641550 | 321047579 | 481269152 | 160221573 | 0 | 319 | deep_crisis | — |
| agrodrone | DCA | — | agrodrone_a:agrodrone_a | NONE | 1946023047 | 270977515 | 481269152 | 210291637 | 0 | 435 | deep_crisis | — |
| agrodrone | DCB | — | agrodrone_b:customer_churn | NONE | 1919780668 | 241033307 | 481269152 | 240235845 | 0 | 493 | deep_crisis | — |
| agrodrone | DCC | — | agrodrone_c:agrodrone_c | drone_as_a_service | 1999827120 | 281868611 | 481269152 | 199400541 | 0 | 391 | deep_crisis | — |
| agrodrone | DCD | — | agrodrone_d:agrodrone_d | NONE | 2002770661 | 314105701 | 481269152 | 167163451 | 0 | 338 | deep_crisis | — |
| agrodrone | DDA | — | agrodrone_a:agrodrone_a | NONE | 2039977004 | 342382523 | 481269152 | 138886629 | 0 | 301 | deep_crisis | — |
| agrodrone | DDB | — | agrodrone_b:customer_churn | NONE | 2010586182 | 310045498 | 481269152 | 171223654 | 0 | 368 | deep_crisis | — |
| agrodrone | DDC | — | agrodrone_c:agrodrone_c | drone_as_a_service | 2040994177 | 313155574 | 481269152 | 168113578 | 0 | 343 | deep_crisis | — |
| agrodrone | DDD | — | agrodrone_d:agrodrone_d | NONE | 2115863643 | 400056369 | 481269152 | 81212783 | 0 | 143 | survived | — |
| moodads | AAA | privacy_doubt, privacy_review_wave | moodads_a:moodads_a | privacy_safe_mode | 1307901771 | 100637486 | 557669338 | 457031852 | 0 | 759 | near_bankruptcy | — |
| moodads | AAB | privacy_doubt, privacy_review_wave | moodads_b:customer_churn | privacy_safe_mode | 1465316079 | 222865506 | 557669338 | 334803832 | 0 | 544 | deep_crisis | — |
| moodads | AAC | privacy_doubt, privacy_review_wave | moodads_c:moodads_c | privacy_safe_mode | 1458058328 | 226768996 | 557669338 | 330900342 | 0 | 541 | deep_crisis | — |
| moodads | AAD | privacy_doubt, privacy_review_wave | moodads_d:moodads_d | privacy_safe_mode, analytics_bundle | 1531225474 | 273229398 | 557669338 | 284439940 | 0 | 389 | deep_crisis | — |
| moodads | ABA | privacy_doubt | moodads_a:moodads_a | NONE | 1545433967 | 320164532 | 557669338 | 237504806 | 0 | 350 | deep_crisis | — |
| moodads | ABB | privacy_doubt | moodads_b:customer_churn | NONE | 1573959990 | 334126393 | 557669338 | 223542945 | 0 | 294 | deep_crisis | — |
| moodads | ABC | privacy_doubt | moodads_c:moodads_c | NONE | 1524155531 | 302290647 | 557669338 | 255378691 | 0 | 401 | deep_crisis | — |
| moodads | ABD | privacy_doubt | moodads_d:moodads_d | analytics_bundle | 1605256374 | 355415354 | 557669338 | 202253984 | 0 | 254 | survived | — |
| moodads | ACA | privacy_doubt | moodads_a:moodads_a | NONE | 1549886033 | 333904267 | 557669338 | 223765071 | 0 | 325 | deep_crisis | — |
| moodads | ACB | privacy_doubt | moodads_b:customer_churn | NONE | 1536611232 | 312753433 | 557669338 | 244915905 | 0 | 375 | deep_crisis | — |
| moodads | ACC | privacy_doubt | moodads_c:moodads_c | contextual_mode | 1599807915 | 350838647 | 557669338 | 206830691 | 0 | 260 | survived | — |
| moodads | ACD | privacy_doubt | moodads_d:moodads_d | analytics_bundle | 1606668596 | 366601620 | 557669338 | 191067718 | 0 | 240 | survived | — |
| moodads | ADA | privacy_doubt | moodads_a:moodads_a | NONE | 1618332713 | 391399477 | 557669338 | 166269861 | 0 | 209 | survived | — |
| moodads | ADB | privacy_doubt | moodads_b:customer_churn | NONE | 1604619458 | 369880345 | 557669338 | 187788993 | 0 | 255 | survived | — |
| moodads | ADC | privacy_doubt | moodads_c:moodads_c | contextual_mode | 1626278573 | 373073999 | 557669338 | 184595339 | 0 | 232 | survived | — |
| moodads | ADD | privacy_doubt | moodads_d:moodads_d | analytics_bundle | 1700923120 | 445775420 | 557669338 | 111893918 | 0 | 140 | survived | — |
| moodads | BAA | data_access_review | moodads_a:moodads_a | NONE | 1606747858 | 371668201 | 557669338 | 186001137 | 0 | 233 | survived | — |
| moodads | BAB | data_access_review | moodads_b:customer_churn | NONE | 1558494597 | 321135463 | 557669338 | 236533875 | 0 | 356 | deep_crisis | — |
| moodads | BAC | data_access_review | moodads_c:moodads_c | contextual_mode | 1580437530 | 324567528 | 557669338 | 233101810 | 0 | 296 | deep_crisis | — |
| moodads | BAD | data_access_review | moodads_d:moodads_d | analytics_bundle | 1630951391 | 376999169 | 557669338 | 180670169 | 0 | 227 | survived | — |
| moodads | BBA | data_access_review, data_restricted | moodads_a:moodads_a | alternative_data | 1475312632 | 162038244 | 557669338 | 395631094 | 0 | 634 | deep_crisis | — |
| moodads | BBB | data_access_review, data_restricted | moodads_b:customer_churn | alternative_data | 1072089375 | 0 | 549881121 | 549881121 | 62572593 | 913 | bankrupt | 8 |
| moodads | BBC | data_access_review, data_restricted | moodads_c:moodads_c | alternative_data | 1454403212 | 145101614 | 557669338 | 412567724 | 0 | 668 | near_bankruptcy | — |
| moodads | BBD | data_access_review, data_restricted | moodads_d:moodads_d | alternative_data, analytics_bundle | 1534387539 | 194888919 | 557669338 | 362780419 | 0 | 519 | deep_crisis | — |
| moodads | BCA | data_access_review | moodads_a:moodads_a | NONE | 1553346865 | 326811366 | 557669338 | 230857972 | 0 | 337 | deep_crisis | — |
| moodads | BCB | data_access_review | moodads_b:customer_churn | NONE | 1540072064 | 305660532 | 557669338 | 252008806 | 0 | 387 | deep_crisis | — |
| moodads | BCC | data_access_review | moodads_c:moodads_c | contextual_mode | 1603268747 | 343745746 | 557669338 | 213923592 | 0 | 269 | survived | — |
| moodads | BCD | data_access_review | moodads_d:moodads_d | analytics_bundle | 1610129428 | 359508719 | 557669338 | 198160619 | 0 | 249 | survived | — |
| moodads | BDA | data_access_review | moodads_a:moodads_a | NONE | 1621793545 | 384306576 | 557669338 | 173362762 | 0 | 218 | survived | — |
| moodads | BDB | data_access_review | moodads_b:customer_churn | NONE | 1608080290 | 362787444 | 557669338 | 194881894 | 0 | 267 | survived | — |
| moodads | BDC | data_access_review | moodads_c:moodads_c | contextual_mode | 1629739405 | 365981098 | 557669338 | 191688240 | 0 | 241 | survived | — |
| moodads | BDD | data_access_review | moodads_d:moodads_d | analytics_bundle | 1704383952 | 438682519 | 557669338 | 118986819 | 0 | 149 | survived | — |
| moodads | CAA | contextual_proof | moodads_a:moodads_a | NONE | 1599826195 | 375854005 | 557669338 | 181815333 | 0 | 228 | survived | — |
| moodads | CAB | contextual_proof | moodads_b:customer_churn | NONE | 1551572934 | 325321267 | 557669338 | 232348071 | 0 | 349 | deep_crisis | — |
| moodads | CAC | contextual_proof | moodads_c:moodads_c | contextual_mode | 1573515867 | 328753332 | 557669338 | 228916006 | 0 | 288 | deep_crisis | — |
| moodads | CAD | contextual_proof | moodads_d:moodads_d | analytics_bundle | 1624029728 | 381184973 | 557669338 | 176484365 | 0 | 222 | survived | — |
| moodads | CBA | contextual_proof | moodads_a:moodads_a | NONE | 1541973136 | 317257435 | 557669338 | 240411903 | 0 | 355 | deep_crisis | — |
| moodads | CBB | contextual_proof | moodads_b:customer_churn | NONE | 1570499159 | 331219296 | 557669338 | 226450042 | 0 | 299 | deep_crisis | — |
| moodads | CBC | contextual_proof | moodads_c:moodads_c | NONE | 1520694700 | 299383550 | 557669338 | 258285788 | 0 | 406 | deep_crisis | — |
| moodads | CBD | contextual_proof | moodads_d:moodads_d | analytics_bundle | 1601795543 | 352508257 | 557669338 | 205161081 | 0 | 258 | survived | — |
| moodads | CCA | contextual_migration, contextual_proof | moodads_a:moodads_a | contextual_mode | 1473492636 | 244733816 | 557669338 | 312935522 | 0 | 494 | deep_crisis | — |
| moodads | CCB | contextual_migration, contextual_proof | moodads_b:customer_churn | contextual_mode | 1460736347 | 224018533 | 557669338 | 333650805 | 0 | 535 | deep_crisis | — |
| moodads | CCC | contextual_migration, contextual_proof | moodads_c:moodads_c | contextual_mode | 1401845047 | 184549841 | 557669338 | 373119497 | 0 | 620 | near_bankruptcy | — |
| moodads | CCD | contextual_migration, contextual_proof | moodads_d:moodads_d | contextual_mode, analytics_bundle | 1525889069 | 273746818 | 557669338 | 283922520 | 0 | 356 | deep_crisis | — |
| moodads | CDA | contextual_proof | moodads_a:moodads_a | NONE | 1614871882 | 388492380 | 557669338 | 169176958 | 0 | 212 | survived | — |
| moodads | CDB | contextual_proof | moodads_b:customer_churn | NONE | 1601158627 | 366973248 | 557669338 | 190696090 | 0 | 260 | survived | — |
| moodads | CDC | contextual_proof | moodads_c:moodads_c | contextual_mode | 1622817742 | 370166902 | 557669338 | 187502436 | 0 | 235 | survived | — |
| moodads | CDD | contextual_proof | moodads_d:moodads_d | analytics_bundle | 1697462289 | 442868323 | 557669338 | 114801015 | 0 | 144 | survived | — |
| moodads | DAA | — | moodads_a:moodads_a | NONE | 1617130355 | 390389499 | 557669338 | 167279839 | 0 | 210 | survived | — |
| moodads | DAB | — | moodads_b:customer_churn | NONE | 1568877094 | 339856761 | 557669338 | 217812577 | 0 | 324 | survived | — |
| moodads | DAC | — | moodads_c:moodads_c | contextual_mode | 1590820027 | 343288826 | 557669338 | 214380512 | 0 | 269 | survived | — |
| moodads | DAD | — | moodads_d:moodads_d | analytics_bundle | 1641333888 | 395720467 | 557669338 | 161948871 | 0 | 203 | survived | — |
| moodads | DBA | — | moodads_a:moodads_a | NONE | 1559277296 | 331792929 | 557669338 | 225876409 | 0 | 330 | deep_crisis | — |
| moodads | DBB | — | moodads_b:customer_churn | NONE | 1587803319 | 345754790 | 557669338 | 211914548 | 0 | 273 | survived | — |
| moodads | DBC | — | moodads_c:moodads_c | NONE | 1537998860 | 313919044 | 557669338 | 243750294 | 0 | 382 | deep_crisis | — |
| moodads | DBD | — | moodads_d:moodads_d | analytics_bundle | 1619099703 | 367043751 | 557669338 | 190625587 | 0 | 239 | survived | — |
| moodads | DCA | — | moodads_a:moodads_a | NONE | 1563729362 | 345532664 | 557669338 | 212136674 | 0 | 304 | survived | — |
| moodads | DCB | — | moodads_b:customer_churn | NONE | 1550454561 | 324381830 | 557669338 | 233287508 | 0 | 356 | deep_crisis | — |
| moodads | DCC | — | moodads_c:moodads_c | contextual_mode | 1613651244 | 362467044 | 557669338 | 195202294 | 0 | 245 | survived | — |
| moodads | DCD | — | moodads_d:moodads_d | analytics_bundle | 1620511925 | 378230017 | 557669338 | 179439321 | 0 | 225 | survived | — |
| moodads | DDA | — | moodads_a:moodads_a | NONE | 1632176042 | 403027874 | 557669338 | 154641464 | 0 | 194 | survived | — |
| moodads | DDB | — | moodads_b:customer_churn | NONE | 1618462787 | 381508742 | 557669338 | 176160596 | 0 | 234 | survived | — |
| moodads | DDC | — | moodads_c:moodads_c | contextual_mode | 1640121902 | 384702396 | 557669338 | 172966942 | 0 | 217 | survived | — |
| moodads | DDD | — | moodads_d:moodads_d | analytics_bundle | 1714766449 | 457403817 | 557669338 | 100265521 | 0 | 126 | survived | — |
| renteverything | AAA | inventory_backlog, repair_pressure | renteverything_a:customer_churn | repair_reserve, cost_cut | 1804572525 | 0 | 458550000 | 458550000 | 3208561 | 900 | bankrupt | 9 |
| renteverything | AAB | inventory_backlog, repair_pressure | renteverything_b:renteverything_b | repair_reserve | 1977355680 | 121275850 | 458550000 | 337274150 | 0 | 685 | near_bankruptcy | — |
| renteverything | AAC | inventory_backlog, repair_pressure | renteverything_c:renteverything_c | repair_reserve | 1988391825 | 129502287 | 458550000 | 329047713 | 0 | 669 | near_bankruptcy | — |
| renteverything | AAD | inventory_backlog, repair_pressure | renteverything_d:renteverything_d | repair_reserve | 2030750640 | 156284337 | 458550000 | 302265663 | 0 | 615 | near_bankruptcy | — |
| renteverything | ABA | repair_pressure | renteverything_a:customer_churn | NONE | 2069141910 | 276707919 | 458550000 | 181842081 | 0 | 401 | deep_crisis | — |
| renteverything | ABB | repair_pressure | renteverything_b:renteverything_b | NONE | 2093102985 | 301241060 | 458550000 | 157308940 | 0 | 350 | deep_crisis | — |
| renteverything | ABC | repair_pressure | renteverything_c:renteverything_c | NONE | 2069141910 | 284707919 | 458550000 | 173842081 | 0 | 387 | deep_crisis | — |
| renteverything | ABD | repair_pressure | renteverything_d:renteverything_d | NONE | 2121244785 | 320658902 | 458550000 | 137891098 | 0 | 300 | deep_crisis | — |
| renteverything | ACA | repair_pressure | renteverything_a:customer_churn | NONE | 2057335665 | 276561608 | 458550000 | 181988392 | 0 | 402 | deep_crisis | — |
| renteverything | ACB | repair_pressure | renteverything_b:renteverything_b | NONE | 2046842670 | 277321442 | 458550000 | 181228558 | 0 | 403 | deep_crisis | — |
| renteverything | ACC | repair_pressure | renteverything_c:renteverything_c | NONE | 2091662745 | 308247294 | 458550000 | 150302706 | 0 | 334 | deep_crisis | — |
| renteverything | ACD | repair_pressure | renteverything_d:renteverything_d | NONE | 2101921395 | 315325763 | 458550000 | 143224237 | 0 | 314 | deep_crisis | — |
| renteverything | ADA | repair_pressure | renteverything_a:customer_churn | NONE | 2106244920 | 310308995 | 458550000 | 148241005 | 0 | 337 | deep_crisis | — |
| renteverything | ADB | repair_pressure | renteverything_b:renteverything_b | NONE | 2101271145 | 314877089 | 458550000 | 143672911 | 0 | 331 | deep_crisis | — |
| renteverything | ADC | repair_pressure | renteverything_c:renteverything_c | NONE | 2106244920 | 318308995 | 458550000 | 140241005 | 0 | 323 | deep_crisis | — |
| renteverything | ADD | repair_pressure | renteverything_d:renteverything_d | NONE | 2180451195 | 369511324 | 458550000 | 89038676 | 0 | 189 | survived | — |
| renteverything | BAA | dispute_attention | renteverything_a:customer_churn | NONE | 2099714370 | 305802915 | 458550000 | 152747085 | 0 | 339 | deep_crisis | — |
| renteverything | BAB | dispute_attention | renteverything_b:renteverything_b | NONE | 2057338470 | 284563544 | 458550000 | 173986456 | 0 | 390 | deep_crisis | — |
| renteverything | BAC | dispute_attention | renteverything_c:renteverything_c | NONE | 2067668520 | 291691278 | 458550000 | 166858722 | 0 | 374 | deep_crisis | — |
| renteverything | BAD | dispute_attention | renteverything_d:renteverything_d | NONE | 2112833610 | 322855191 | 458550000 | 135694809 | 0 | 299 | deep_crisis | — |
| renteverything | BBA | dispute_attention, dispute_wave | renteverything_a:customer_churn | transparent_insurance | 1948903511 | 146743423 | 458550000 | 311806577 | 0 | 640 | near_bankruptcy | — |
| renteverything | BBB | dispute_attention, dispute_wave | renteverything_b:renteverything_b | transparent_insurance | 1867323405 | 53453150 | 458550000 | 405096850 | 0 | 808 | near_bankruptcy | — |
| renteverything | BBC | dispute_attention, dispute_wave | renteverything_c:renteverything_c | transparent_insurance | 1948903511 | 154743423 | 458550000 | 303806577 | 0 | 625 | near_bankruptcy | — |
| renteverything | BBD | dispute_attention, dispute_wave | renteverything_d:renteverything_d | transparent_insurance | 1998607871 | 189039431 | 458550000 | 269510569 | 0 | 555 | deep_crisis | — |
| renteverything | BCA | dispute_attention | renteverything_a:customer_churn | NONE | 2060734305 | 288906669 | 458550000 | 169643331 | 0 | 380 | deep_crisis | — |
| renteverything | BCB | dispute_attention | renteverything_b:renteverything_b | NONE | 2050241310 | 289666503 | 458550000 | 168883497 | 0 | 381 | deep_crisis | — |
| renteverything | BCC | dispute_attention | renteverything_c:renteverything_c | NONE | 2095061385 | 320592355 | 458550000 | 137957645 | 0 | 312 | deep_crisis | — |
| renteverything | BCD | dispute_attention | renteverything_d:renteverything_d | NONE | 2105320035 | 327670824 | 458550000 | 130879176 | 0 | 291 | deep_crisis | — |
| renteverything | BDA | dispute_attention | renteverything_a:customer_churn | NONE | 2109643560 | 322654056 | 458550000 | 135895944 | 0 | 315 | deep_crisis | — |
| renteverything | BDB | dispute_attention | renteverything_b:renteverything_b | NONE | 2104669785 | 327222150 | 458550000 | 131327850 | 0 | 309 | deep_crisis | — |
| renteverything | BDC | dispute_attention | renteverything_c:renteverything_c | NONE | 2109643560 | 330654056 | 458550000 | 127895944 | 0 | 300 | deep_crisis | — |
| renteverything | BDD | dispute_attention | renteverything_d:renteverything_d | NONE | 2183849835 | 381856385 | 458550000 | 76693615 | 0 | 165 | survived | — |
| renteverything | CAA | price_pressure | renteverything_a:customer_churn | NONE | 2092767150 | 301009333 | 458550000 | 157540667 | 0 | 348 | deep_crisis | — |
| renteverything | CAB | price_pressure | renteverything_b:renteverything_b | NONE | 2050391250 | 279769962 | 458550000 | 178780038 | 0 | 398 | deep_crisis | — |
| renteverything | CAC | price_pressure | renteverything_c:renteverything_c | NONE | 2060721300 | 286897696 | 458550000 | 171652304 | 0 | 383 | deep_crisis | — |
| renteverything | CAD | price_pressure | renteverything_d:renteverything_d | NONE | 2105886390 | 318061609 | 458550000 | 140488391 | 0 | 308 | deep_crisis | — |
| renteverything | CBA | price_pressure | renteverything_a:customer_churn | NONE | 2065593330 | 284259398 | 458550000 | 174290602 | 0 | 387 | deep_crisis | — |
| renteverything | CBB | price_pressure | renteverything_b:renteverything_b | NONE | 2089554405 | 308792539 | 458550000 | 149757461 | 0 | 337 | deep_crisis | — |
| renteverything | CBC | price_pressure | renteverything_c:renteverything_c | NONE | 2065593330 | 292259398 | 458550000 | 166290602 | 0 | 373 | deep_crisis | — |
| renteverything | CBD | price_pressure | renteverything_d:renteverything_d | NONE | 2117696205 | 328210381 | 458550000 | 130339619 | 0 | 286 | deep_crisis | — |
| renteverything | CCA | price_pressure, renter_churn | renteverything_a:customer_churn | lower_deposit | 1940767708 | 181129717 | 458550000 | 277420283 | 0 | 581 | near_bankruptcy | — |
| renteverything | CCB | price_pressure, renter_churn | renteverything_b:renteverything_b | lower_deposit | 1927641522 | 180072648 | 458550000 | 278477352 | 0 | 584 | near_bankruptcy | — |
| renteverything | CCC | price_pressure, renter_churn | renteverything_c:renteverything_c | lower_deposit | 1761954038 | 65748285 | 458550000 | 392801715 | 0 | 791 | near_bankruptcy | — |
| renteverything | CCD | price_pressure, renter_churn | renteverything_d:renteverything_d | lower_deposit | 1974730873 | 212564301 | 458550000 | 245985699 | 0 | 519 | deep_crisis | — |
| renteverything | CDA | price_pressure | renteverything_a:customer_churn | NONE | 2102696340 | 317860474 | 458550000 | 140689526 | 0 | 324 | deep_crisis | — |
| renteverything | CDB | price_pressure | renteverything_b:renteverything_b | NONE | 2097722565 | 322428568 | 458550000 | 136121432 | 0 | 317 | deep_crisis | — |
| renteverything | CDC | price_pressure | renteverything_c:renteverything_c | NONE | 2102696340 | 325860474 | 458550000 | 132689526 | 0 | 309 | deep_crisis | — |
| renteverything | CDD | price_pressure | renteverything_d:renteverything_d | NONE | 2176902615 | 377062803 | 458550000 | 81487197 | 0 | 174 | survived | — |
| renteverything | DAA | — | renteverything_a:customer_churn | NONE | 2106661590 | 310596497 | 458550000 | 147953503 | 0 | 330 | deep_crisis | — |
| renteverything | DAB | — | renteverything_b:renteverything_b | NONE | 2064285690 | 289357126 | 458550000 | 169192874 | 0 | 381 | deep_crisis | — |
| renteverything | DAC | — | renteverything_c:renteverything_c | NONE | 2074615740 | 296484860 | 458550000 | 162065140 | 0 | 365 | deep_crisis | — |
| renteverything | DAD | — | renteverything_d:renteverything_d | NONE | 2119780830 | 327648773 | 458550000 | 130901227 | 0 | 290 | deep_crisis | — |
| renteverything | DBA | — | renteverything_a:customer_churn | NONE | 2079487770 | 293846562 | 458550000 | 164703438 | 0 | 370 | deep_crisis | — |
| renteverything | DBB | — | renteverything_b:renteverything_b | NONE | 2103448845 | 318379703 | 458550000 | 140170297 | 0 | 319 | deep_crisis | — |
| renteverything | DBC | — | renteverything_c:renteverything_c | NONE | 2079487770 | 301846562 | 458550000 | 156703438 | 0 | 356 | deep_crisis | — |
| renteverything | DBD | — | renteverything_d:renteverything_d | NONE | 2131590645 | 337797545 | 458550000 | 120752455 | 0 | 268 | deep_crisis | — |
| renteverything | DCA | — | renteverything_a:customer_churn | NONE | 2067681525 | 293700251 | 458550000 | 164849749 | 0 | 371 | deep_crisis | — |
| renteverything | DCB | — | renteverything_b:renteverything_b | NONE | 2057188530 | 294460085 | 458550000 | 164089915 | 0 | 373 | deep_crisis | — |
| renteverything | DCC | — | renteverything_c:renteverything_c | NONE | 2102008605 | 325385937 | 458550000 | 133164063 | 0 | 303 | deep_crisis | — |
| renteverything | DCD | — | renteverything_d:renteverything_d | NONE | 2112267255 | 332464406 | 458550000 | 126085594 | 0 | 282 | deep_crisis | — |
| renteverything | DDA | — | renteverything_a:customer_churn | NONE | 2116590780 | 327447638 | 458550000 | 131102362 | 0 | 306 | deep_crisis | — |
| renteverything | DDB | — | renteverything_b:renteverything_b | NONE | 2111617005 | 332015732 | 458550000 | 126534268 | 0 | 300 | deep_crisis | — |
| renteverything | DDC | — | renteverything_c:renteverything_c | NONE | 2116590780 | 335447638 | 458550000 | 123102362 | 0 | 292 | deep_crisis | — |
| renteverything | DDD | — | renteverything_d:renteverything_d | NONE | 2190797055 | 386649967 | 458550000 | 71900033 | 0 | 156 | survived | — |

## Balance observations

First pass is final: approved coefficients were not tuned after the exhaustive run. Review the reported DDD and mixed-path spreads before treating the shared leaderboard as fair.

## Defense usage distribution

Every named strategic defense has max_uses=1 per game; emergency cost cut is also single-use. Counts below are path-level usages across the 64 reachable sequences.

| Startup | Paths with a defense | Paths with 2+ defenses | Most-used defenses |
|---|---:|---:|---|
| coffeebot | 34 | 2 | loyalty_program (28), campus_redeploy (4), service_reserve (4) |
| petmind | 8 | 0 | independent_audit (4), retention_offer (4) |
| foodrover | 19 | 1 | restaurant_retention (11), battery_reserve (4), route_rebuild (4), cost_cut (1) |
| studygenie | 12 | 1 | backup_provider (4), quality_audit (4), student_retention (4), cost_cut (1) |
| sleepwork | 46 | 7 | price_retention (28), digital_wellness (16), compact_redeploy (4), flexible_lease (4) |
| fitmirror | 24 | 0 | mobile_mode (16), bundled_subscription (4), financing_tradein (4) |
| cloudkitchen | 19 | 1 | unique_menu_loyalty (11), direct_channel (4), second_supplier (4), cost_cut (1) |
| agrodrone | 19 | 0 | drone_as_a_service (11), component_reserve (4), seasonal_leasing (4) |
| moodads | 35 | 3 | analytics_bundle (16), contextual_mode (14), alternative_data (4), privacy_safe_mode (4) |
| renteverything | 12 | 1 | lower_deposit (4), repair_reserve (4), transparent_insurance (4), cost_cut (1) |

## Local deterministic round benchmark

1000 rounds with `coffeebot_r1_a` for `coffeebot`; per round: mean 0.3057 ms, median 0.2986 ms, p95 0.3287 ms, max 3.1778 ms. Peak process RSS observed: 31.44 MiB.

All ten catalogs use explicit v2 effects and ending thresholds. This local benchmark is not a target-host benchmark.
