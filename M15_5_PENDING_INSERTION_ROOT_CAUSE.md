# M15.5 — Pending Insertion Root Cause

2 November 2026, WIB. Staging M15.5 terpisah: http://127.0.0.1:5201/.

**MANUAL / RANDOM SCENARIO — NOT HISTORICAL OBSERVATION.**

**PROVISIONAL GEDANGAN NETWORK — NOT FIELD CALIBRATED.**

## Temuan utama

**Full causal attribution: UNRESOLVED.** Run `cc419452a995456df324fd05` mereproduksi tepat 3000 requested/routed/loaded, 1914 departed/moved, 1346 arrived, 568 active dan 1086 pending. Semua 1086 pending tetap di ledger; tidak dibuang atau diubah menjadi gagal rute. Northbound 600 (55.25%), southbound 486 (44.75%); cohort lain tidak memiliki pending akhir.

| Kondisi teramati akhir 3600s | Unique pending IDs | Persen /1086 |
| --- | --- | --- |
| OBSERVED_GEOMETRIC_ENTRY_SPACE_SHORTAGE | 254 | 23.39% |
| UNRESOLVED_OTHER_INSERTION_CHECK | 832 | 76.61% |

Persentase menggunakan **unique pending ID pada horizon**, bukan jumlah sampel 10s. Kategori pertama berarti tidak ada lane berizin dengan ruang geometris nominal length+minGap yang cukup pada snapshot akhir. Ini bukti kondisi yang menghalangi, bukan angka “23.39% disebabkan geometri”. Pada 832 lainnya, proxy celah cukup di setidaknya satu lane tetapi safe insertion/route lane/downstream/junction checks tidak terpisah. SUMO tidak mengembalikan reason lengkap per kendaraan; tidak diberi persentase sebab sinyal/kereta palsu. Snapshot akhir juga bukan riwayat lengkap penyebab sepanjang jam.

## Bukti origin, antrean dan penyimpanan

Northbound origin `w562358500_s11_p0_0_f` panjang lane 101.25m; southbound `w512351908_s1_p0_0_f` 169.30m. **0/1086** berasal dari origin di bawah 5m. Ini menolak penjelasan langsung “semua pending karena boundary edge terlalu pendek”; tidak membuktikan storage downstream telah realistis.

Maksimum sampel northbound: 51 aktif pada edge, 28 berhenti pada satu lane, stopped span 101.04m, 107763 vehicle-s berhenti. Southbound: 87 aktif, 47 berhenti pada satu lane, span 169.12m, 147930.5 vehicle-s berhenti. Edge count dan single-lane max adalah metrik berbeda. Queue mendekati panjang lane menunjukkan antrean nyata **dalam model**, bukan visual congestion buatan. Boundary samples berulang bukan persentase unique kendaraan atau sertifikasi spillback lapangan.

546 external dan 1911 internal lane di bawah 5m ada pada network sumber; segmentation tidak otomatis kesalahan. Kecepatan/occupancy/queue tiap edge, route concentration, origin/class, insertion delay dan censorship tersedia di `edge-diagnostics.json`, `insertion-samples.json`, `approach-analysis.json`, `demand-timeline.json`, FCD dan ledger.

## Pengujian penjelasan alternatif

Controller asumsi mengisolasi sembilan link protected (27 phase, cycle153s, green12/yellow3/allred2). Ini kandidat bottleneck konservatif; bukan timing APILL resmi. Green30 memberi 1483 arrived /970 pending. Menghilangkan train events memberi 1342 arrived /1084 pending. Efek ini terukur di model dan tidak mengisolasi kontribusi kausal aditif; interaction dan safe insertion tetap ada. Jangan mengartikan delta dua kendaraan sebagai persentase sebab seluruh backlog.

Menambah execution horizon menjadi7200 tanpa demand baru menghasilkan 2071 arrived, 475 active, 454 pending. Setelah tambahan60 menit jaringan belum kosong; discharge time **censored**, bukan “selesai dalam120 menit”. Route concentration (35% masing-masing cohort utama), assumed signals, insertion lane safety dan downstream storage masih perlu pengukuran/detector diagnostics lebih lanjut sebelum disimpulkan sebagai kapasitas Gedangan atau bug conversion.

Tidak ada mass-balance loss, illegal permission, collision atau unexplained teleport pada audit run ini. Itu tidak mengesahkan seluruh konektivitas fisik. Implementasi berhasil mempertahankan backlog; validitas bottleneck terhadap lapangan belum selesai.

Data per-ID: `documentation/m155/rootcause/cc419452a995456df324fd05.json`. Bukti counterfactual: `controlled-comparisons.json`. Tidak ada forced insertion, ignore permission, route rewrite atau queue removal.
