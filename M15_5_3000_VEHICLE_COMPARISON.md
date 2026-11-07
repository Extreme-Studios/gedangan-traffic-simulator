# M15.5 — 3000 Vehicle Comparison

2 November 2026, WIB. Staging M15.5 terpisah: http://127.0.0.1:5201/.

**MANUAL / RANDOM SCENARIO — NOT HISTORICAL OBSERVATION.**

**PROVISIONAL GEDANGAN NETWORK — NOT FIELD CALIBRATED.**

## Fair comparison

Seluruh pasangan memakai **exact full request list yang sama**, tidak hanya seed yang sama: ID, vehicle category, approach, movement, edge route dan jadwal departure. Cohort SHA256 `8f8ea373a1e788a8a5435adeb09ff167df36f8b8e386102dbfcfb36a84216bf7`. Network SHA256 `0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c`. Semua road demand dibuat selama3600s. Semua perbandingan mempunyai 3000 routed/loaded, 0 route failure.

| Kasus | Execution menit | Departed akhir | Arrived akhir | Active akhir | Pending akhir | Mean wait departed (s) |
| --- | --- | --- | --- | --- | --- | --- |
| baseline-3000 | 60 | 1914 | 1346 | 568 | 1086 | 628.75 |
| discharge-3000 | 120 | 2546 | 2071 | 475 | 454 | 987.14 |
| green30-3000 | 60 | 2030 | 1483 | 547 | 970 | 612.92 |
| no-trains-3000 | 60 | 1916 | 1342 | 574 | 1084 | 628.22 |

Baseline3600 dan discharge7200 mempunyai checkpoint3600 yang persis sama: 1914 departed,1346 arrived,568 active,1086 pending. Kolom discharge adalah **akhir120 menit**, bukan hasil jam pertama yang membaik. Tambahan60 menit belum mengosongkan jaringan. Clearance time/additional discharge completion tetap null/censored; jangan mengisi estimasi buatan.

Green30 hanya mengganti green12→30, urutan sembilan protected links/yellow3/allred2 tetap. Cycle berubah153→315s sebagai konsekuensi parameter tersebut, bukan faktor tersembunyi. No-trains hanya menghapus daftar event KA, road request list tidak berubah. Discharge tidak menambah request atau event KA setelah jam pertama. Tidak ada perbandingan before/after geometry improvement karena tidak ada koreksi geometri terverifikasi.

Mean waiting menghitung departed termasuk trip aktif censored; berbeda dari travel time arrived-only dan belum mencakup semua delay pending. Tidak boleh membandingkannya sebagai indikator penelitian sebelum demand/network dikalibrasi.

## Regresi empat load level, actual SUMO

| Requested /60min | Routed | Loaded | Departed | Moved | Arrived | Active | Pending | SUMO loop wall s | Run ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 500 | 500 | 500 | 500 | 500 | 468 | 32 | 0 | 21.906 | 49da5fe5c9c3f965850389e1 |
| 1000 | 1000 | 1000 | 1000 | 1000 | 848 | 152 | 0 | 50.172 | ae6c842a279f3d42d1dc9fbc |
| 3000 | 3000 | 3000 | 1914 | 1914 | 1346 | 568 | 1086 | 226.781 | cc419452a995456df324fd05 |
| 5000 | 5000 | 5000 | 2385 | 2384 | 1644 | 741 | 2615 | 315.000 | 569df9741bf6f16d1cffa31e |

Waktu adalah wall-clock loop SUMO+TraCI dan pencatatan pada mesin ini, beberapa workload berjalan bersamaan. Bukan pure CPU benchmark terisolasi atau FPS browser. `generation_wall_s` dan `total_wall_s` tetap ada pada raw result; playback loading time, median/p5 FPS, stalls dan memory M15.5 belum tersedia karena browser ditolak.

## Pembacaan throughput yang benar

Raw inherited key `throughput_arrivals_per_hour` memakai jumlah tiba akhir-eksekusi dibagi durasi demand. Pada extended run definisi itu **bukan** laju dua jam atau hasil jam pertama. Raw output dipertahankan utuh; `controlled-comparisons.json` menghitung dua rate eksplisit dan UI memakai checkpoint. Pada discharge, first-hour arrivals/h =1346; execution-window arrivals/h =1035.5 (2071/2). Tidak memakai angka2071 sebagai throughput jam pertama.

![Perbandingan dan kondisi pending](documentation/m155/figures/actual-comparisons.png)

Run evidence lengkap: `simulation/runs/m155/<run_id>/` (request, demand, XML, FCD, tripinfo, ledger, playback, signal events, input/source/output manifests). Delapan audit independen lulus; jumlah request tidak disamakan dengan jumlah kendaraan yang terlihat pada suatu frame.
