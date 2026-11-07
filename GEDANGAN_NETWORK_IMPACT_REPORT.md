# Gedangan — Network-wide Impact

Dibuat dari actual outputs, 1 November 2026. Status penelitian: **belum dikalibrasi terhadap observasi Gedangan 2026**.

## Hasil dan cara membaca

18 actual runs dianalisis terhadap network connections dan FCD, status PASS. Main NB/SB, frontage, Sukodono, Ketajen/rail vicinity, local/feeder/service dan deck konsep diagregasi; OD lebih rinci ada pada masing-masing analysis.json. Sedati/Jenggolo tetap MISSING/possible alias; driveway stasiun belum terverifikasi.

Baseline regional model proxies:

| Region | Edges | Vehicle seconds | Queued lane seconds | Max queue extent m |
| --- | --- | --- | --- | --- |
| MAIN_NB_SB | 82 | 683475 | 24933 | 830.3 |
| LOCAL_FEEDER_SERVICE | 58 | 13967 | 239 | 4.5 |
| SUKODONO | 10 | 797 | 544 | 4.5 |
| KETAJEN_RAIL_VICINITY | 57 | 1322 | 0 | 0 |

Penjumlahan per-edge bisa menghitung kendaraan yang sama di beberapa ruas. Volume assigned dan actual entered disajikan terpisah. Export per-ruas berisi delta assigned, actual unique entered, queue, speed dan vehicle-seconds. New bottleneck candidates ditentukan berdasarkan model queue, bukan diumumkan sebagai temuan lapangan.

| Intervention | Comparable cohort | Per-road comparison |
| --- | --- | --- |
| construction_full | True | [construction_full.json](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/realism_recovery/comparisons/construction_full.json>) |
| construction_partial | True | [construction_partial.json](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/realism_recovery/comparisons/construction_partial.json>) |
| flyover_A | True | [flyover_A.json](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/realism_recovery/comparisons/flyover_A.json>) |
| flyover_B | True | [flyover_B.json](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/realism_recovery/comparisons/flyover_B.json>) |
| frontage_coordination | True | [frontage_coordination.json](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/realism_recovery/comparisons/frontage_coordination.json>) |
| heavy_schedule | True | [heavy_schedule.json](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/realism_recovery/comparisons/heavy_schedule.json>) |
| signal_adjustment | True | [signal_adjustment.json](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/realism_recovery/comparisons/signal_adjustment.json>) |
| turn_management | True | [turn_management.json](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/realism_recovery/comparisons/turn_management.json>) |

S01 meningkatkan arrivals dalam fixture; tidak membuktikan signal plan optimum. S02 default dan S03 pada reference cohort tidak berpengaruh karena gerakan yang dibatasi tidak dipakai. Targeted supplemental tests membuktikan24rerouted untuk masing-masing intervensi; frontage arrivals justru25→21. Hasil negatif dipertahankan.

S06A menaikkan arrivals tetapi menambah belum-departed di boundary. S07 full meningkatkan failed routes18→94. Ini alasan tidak memberi ranking berdasarkan satu indikator simpang pusat saja. S05 belum executable karena kekurangan controller kedua, tidak ada klaim dampak atau koordinasi palsu.

Spillback: final [network-impact-analysis.json](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/realism_recovery/network-impact-analysis.json>) mencantumkan sustained storage proxy episodes perrun; lane pairs/timestamps ada di analysis.json. Sampling/resolusi dan causal ambiguity membatasi interpretasi. Pengukuran network di luar boundary, demand calibration, field signal/rail timings dan perumahan/feeder observations masih diperlukan.

