# MILESTONE 05.1 — Validation

**PARTIAL — NEEDS FIELD DATA. M06 belum dimulai.**

Proyek: `C:\Users\ROG ALLY\Documents\EXTREME STUDIOS\PROJECT\Simulasi Kemacetan Lalu Lintas`.

## Jalankan

Buka `START_VALIDATION_M051.bat`, kemudian [halaman validasi M05.1](http://127.0.0.1:5180/validation.html). Viewer M05 tetap tersedia pada port 5179. Toggle overlay original/adjusted/raw/rail/vector/stop line untuk membandingkan geometri. Pilih eksperimen dan event untuk memeriksa ruang hilir, link priority/open/foe, queue footprint serta actual discharge setelah recovery.

`SHOW_VALIDATION_SUMO_M051.bat` membuka SUMO-GUI dengan output sesi baru, terpisah dari bukti dan headless runs. GUI berhenti pada 105 dan 130 detik; tekan Play untuk melanjutkan.

## Rebuild

Jalankan `REBUILD_VALIDATION_M051.bat`. Skrip memakai .venv dan SUMO/NETCONVERT 1.28.0 lokal, tanpa instalasi tambahan. Baseline SHA diperiksa sebelum bekerja. Geometry audit tidak mengubah koordinat tanpa sumber: execution copies tetap identik dengan M05.

Proses menjalankan 20 replay independen, 2 evidence aliases yang telah divalidasi, dan 3 isolated controls. Reproducibility, safety, publication, seluruh tes, TypeScript dan Vite validation build dijalankan. Outputs M03–M05 tidak ditimpa.

## Hasil dan batas

- 37 verified model vehicle-event episodes, termasuk 2 alias dari hasil identik; 35 episode berasal dari replay independen.
- Positive control: 1 verified spillback. Negative free/signal controls: 0 false verified events.
- Seluruh 114 kandidat M05 diaudit; 99 memiliki matched head-priority trace, 15 diklasifikasikan dengan positional-following evidence.
- Ran 152 tests in 43.855s, OK. Seluruh 134 tes warisan tetap dipertahankan.
- Empat edge endpoint berubah sekitar 1.60 m dan tujuh lane shapes hingga 7.178 m pada turunan M05. Audit ini mengukur perubahan, tidak mengarang koreksi fisik.
- Model stop-to-rail distances: 6.898 m dan 2.936 m, EPSG:32749. Kedua road connectors mempunyai gap 0 pada koordinat XML. Ini bukan pengukuran stop marking atau clearance lapangan.
- Physical geometry tetap **NEEDS FIELD SURVEY**. Tidak digunakan toleransi arbitrer untuk memberi label aman. Oversize tetap diblokir; frontage dan access policy dipertahankan.
- Synthetic experiments dan isolated fixtures tidak disajikan sebagai observasi lalu lintas Gedangan.

Laporan: `MILESTONE_05_1_REPORT.md`. Bukti: `documentation/m051`; actual priority traces: `simulation/runs/m051`. `baseline-complete.zip` mencakup seluruh baseline yang terdaftar; hash arsip tersedia di `snapshot-manifest.json`.

M06 memerlukan persetujuan pengguna terhadap hasil M05.1. Belum ada pekerjaan M06 yang dimulai.
