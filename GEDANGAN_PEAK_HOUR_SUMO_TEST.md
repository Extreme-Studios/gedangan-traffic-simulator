# Gedangan — Actual Peak-hour SUMO Tests

Dibuat dari actual outputs, 1 November 2026. Status penelitian: **belum dikalibrasi terhadap observasi Gedangan 2026**.

## Eksperimen

SUMO1.28.0 lokal, step0,5s, FCD1s. Main suite: PASS_WITH_DATA_AND_ENGINEERING_LIMITATIONS, 18 actual runs, 72 checks. Reference tests memakai tanggal4Agustus2026, horizon900s + warm-up300s, seed42, turnshare0,1; tanggal hanya memilih kalender/estimasi historis. Offpeak adalah input sintetis. Weekend memakai2Agustus. Tidak ada pengukuran volume2026 atau kalibrasi kapasitas.

Mass balance **seluruh horizon termasuk warm-up**:

| Run | Requested | Routed | Loaded | Departed | Arrived | Running | Failed | Not departed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| morning_base | 1938 | 1920 | 1920 | 1154 | 96 | 1058 | 18 | 766 |
| evening_base | 1912 | 1900 | 1900 | 1159 | 97 | 1062 | 12 | 741 |
| midday_reference | 1716 | 1696 | 1696 | 1132 | 100 | 1032 | 20 | 564 |
| signal_adjustment | 1938 | 1920 | 1920 | 1173 | 109 | 1064 | 18 | 747 |
| turn_management | 1938 | 1920 | 1920 | 1154 | 96 | 1058 | 18 | 766 |
| frontage_coordination | 1938 | 1920 | 1920 | 1154 | 96 | 1058 | 18 | 766 |
| heavy_schedule | 1938 | 1920 | 1851 | 1211 | 102 | 1109 | 18 | 709 |
| flyover_A | 1938 | 1920 | 1920 | 971 | 504 | 467 | 18 | 949 |
| flyover_B | 1938 | 1920 | 1920 | 1398 | 508 | 890 | 18 | 522 |
| construction_partial | 1938 | 1920 | 1920 | 877 | 95 | 782 | 18 | 1043 |
| construction_full | 1938 | 1844 | 1844 | 997 | 48 | 949 | 94 | 847 |
| morning_without_trains | 1938 | 1920 | 1920 | 1157 | 96 | 1061 | 18 | 763 |
| morning_signal_off | 1938 | 1920 | 1920 | 1399 | 471 | 928 | 18 | 521 |
| offpeak_explicit_synthetic | 252 | 252 | 252 | 252 | 97 | 155 | 0 | 0 |
| direction_split_low | 1936 | 1919 | 1919 | 1159 | 95 | 1064 | 17 | 760 |
| direction_split_high | 1936 | 1919 | 1919 | 1062 | 99 | 963 | 17 | 857 |
| volume_upper_sensitivity | 2710 | 2686 | 2686 | 1159 | 93 | 1066 | 24 | 1527 |
| weekend_reference | 1510 | 1496 | 1496 | 1140 | 95 | 1045 | 14 | 356 |

Requested=Routed+Failed; Routed=Departed+Not departed; Departed=Arrived+Running. Unserved tidak dibuang. Measurement-only cohort dan warm-up state disimpan terpisah di result.json.

## Metrik model

| Run | TT arrived-only s | Mean sample speed m/s | Wait departed s | Max queue extent m | Throughput veh/h |
| --- | --- | --- | --- | --- | --- |
| morning_base | 810.24 | 1.988 | 348.71 | 830.3 | 384.0 |
| evening_base | 820.93 | 1.976 | 334.35 | 832.3 | 388.0 |
| midday_reference | 826.05 | 2.067 | 328.35 | 832.9 | 400.0 |
| signal_adjustment | 825.44 | 2.091 | 341.14 | 830.2 | 436.0 |
| turn_management | 810.24 | 1.988 | 348.71 | 830.3 | 384.0 |
| frontage_coordination | 810.24 | 1.988 | 348.71 | 830.3 | 384.0 |
| heavy_schedule | 808.06 | 2.104 | 331.39 | 835.9 | 408.0 |
| flyover_A | 513.25 | 7.907 | 25.98 | 311.8 | 2016.0 |
| flyover_B | 563.82 | 5.572 | 47.62 | 412.7 | 2032.0 |
| construction_partial | 787.07 | 2.717 | 260.05 | 830.2 | 380.0 |
| construction_full | 809.74 | 2.659 | 235.22 | 829.7 | 192.0 |
| morning_without_trains | 809.61 | 1.988 | 344.91 | 830.1 | 384.0 |
| morning_signal_off | 598.46 | 5.52 | 50.79 | 610.8 | 1884.0 |
| offpeak_explicit_synthetic | 630.64 | 6.202 | 102.6 | 55.3 | 388.0 |
| direction_split_low | 817.16 | 1.988 | 340.2 | 832.3 | 380.0 |
| direction_split_high | 811.42 | 2.673 | 281.51 | 651.2 | 396.0 |
| volume_upper_sensitivity | 808.51 | 1.98 | 344.61 | 832.5 | 372.0 |
| weekend_reference | 817.16 | 2.218 | 312.0 | 830.6 | 380.0 |

Travel time hanya yang tiba; trips unfinished tersensor dan tidak diberi waktu0. Speed adalah vehicle-time sample mean. Queue extent adalah proxy lane, bukan panjang antrean lapangan. Throughput adalah arrivals pada measurement window diekstrapolasi ke perjam, bukan demand atau countobserved.

Spillback dievaluasi sebagai consecutive storage-blockage candidate samples; final continuous episodes ada di analysis.json. Tidak membuktikan penyebab lapangan dan dapat undercount. Jangan gunakan jumlah span samples engine sebagai durasi continuous.

Teleports dinonaktifkan (`time-to-teleport=-1`), illegal permissions/collision/teleport/occupancy ketika palang tutup tetap direkam. Status clean berarti tidak tercatat pada resolusi pengujian, bukan sertifikasi keselamatan.

Registry/kelas uji: [multiclass-compatibility.json](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/realism_recovery/multiclass-compatibility.json>). Heavy truck bergerak tetapi belum tiba dalam fixture; oversize seluruhnya ditolak. Trailer hanya pada rute existing yang lolos screen sementara, tidak melalui flyover konsep.

Output raw per run: FCD, tripinfo, summary, statistics, config, demand ledger, route ledger, vehicle results, signal/rail state, edge impact dan manifests. Run directory: [realism_recovery](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/simulation/runs/realism_recovery>).


Bukti lengkap: [acceptance-results.json](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/realism_recovery/acceptance-results.json>), [supplemental-acceptance.json](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/realism_recovery/supplemental-acceptance.json>), [api-acceptance.json](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/realism_recovery/api-acceptance.json>).
