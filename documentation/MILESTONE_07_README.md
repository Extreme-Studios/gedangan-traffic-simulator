# M07 Projection Lab — penggunaan lokal

M07 saja. Semua proyeksi kondisional, bukan prakiraan empiris tervalidasi. M08 belum dimulai.

## Membuka aplikasi

Dari root proyek, jalankan `START_PROJECTION_M07.bat`. UI: http://127.0.0.1:5182/projection.html. API hanya loopback, port 8772. Launcher memeriksa kedua layanan sebelum membuka halaman. Viewer M01–M06 dan launchernya tidak diubah.

Pilih tahun 2026–2040 dan LOW/REFERENCE/HIGH. Demand langsung dihitung, tetapi metrik lalu lintas hanya muncul setelah actual SUMO run. Kombinasi yang belum disimulasikan menampilkan NOT RUN. Growth editor mengubah laju tahunan konstan dan menyimpan CUSTOM dengan ID/hash baru; preset tidak ditimpa. Konfigurasi JSON juga mendukung piecewise dan year-specific schedules.

Primary precompute:2026/2030/2035/2040 REFERENCE seeds 42/43;2040 LOW/HIGH seed 42;2026 Strict dan M04.5 Provisional. UI dapat mengantrekan kombinasi lain melalui tombol Run. Satu worker SUMO, maksimum 2500 request/run dan batas wall time 180s. Jangan menjalankan rebuild offline bersamaan dengan interactive job. Resource-bound failure tetap dicatat, tanpa hasil trafik rekaan.

## Rebuild dan audit

Jalankan `REBUILD_PROJECTION_M07.bat`. Tahap berurutan:scenario initialization,45 demand projections,12 primary SUMO jobs, sensitivity, fresh reproduction, audit/export, regression, TypeScript dan production build, lalu laporan. Cache memverifikasi source/config/network/seed dan core-output hashes. File tambahan audit dapat dihitung ulang; network dan output milestone lama tidak diubah.

Folder utama:

- `configuration/growth-m07/`:LOW/REFERENCE/HIGH,versioned CUSTOM,baseline adapter dan launcher helper.
- `simulation/projections/m07/`:setiap cell OD/class/15 menit, fractional count,integer allocation,annual schedule dan provenance.
- `simulation/runs/m07/`:actual request/route/failure ledger,XML,tripinfo,FCD,priority trace,causal events,playback,process logs dan manifests.
- `documentation/m07/`:source audit,run summary,comparisons,sensitivity,reproduction,tests,browser QA dan hashes.
- `documentation/MILESTONE_07_REPORT.md`:hasil serta acceptance teknis dan empiris terpisah.

Rumus final rate:baseline(2026,OD,class,interval) × PRODUCT(1+r[2027..year]). Final OD/class rate menggantikan class-wide rate; tidak dikalikan dua kali. Missing/ambiguous rate adalah error, bukan fallback0. Integer total memakai global half-up dan largest remainder dengan stable lexical ties. Seed mengatur departure jitter, bukan menutupi selisih pembulatan.

## Batas ilmiah dan simulasi

Baseline 240request/two15min berasal dari software fixture M04, bukan volume Gedangan. Seluruh growth rate demo adalah SYNTHETIC ILLUSTRATIVE ASSUMPTION. Registered vehicle stock, populasi, ekonomi atau jumlah dokumen tidak menjadi local traffic growth secara otomatis.

Jaringan dan kontrol utama tetap M05.1 Provisional. Fixed demand window0–1800s, horizon2100s,step0.5s,warmup0,no optional drain. Teleport=-1 dinyatakan eksplisit. Requested=failed routes+arrived+running+notdeparted. Tripinfo unfinished/undeparted tetap diparse. Loaded direkonsiliasi dari actual SUMO summary minus train records; raw initial telemetry dipertahankan di lifecycle audit. Arrived-only travel time tidak mewakili seluruh demand.

Oversize tetap NOT_ROUTABLE; heavy access Provisional bukan legal clearance. Tidak ada perubahan geometry,oneway,turn restrictions atau permission demi meluluskan rute. Queue count dan meter extent terpisah. Crossing/stop-line/short-edge metrics masih memerlukan survei. Signal dan train schedule sintetis; verified-in-model spillback bukan field validation.

Burst stress ekstrem yang melampaui180s berstatus FAILED_RESOURCE_BUDGET, tanpa completed traffic metrics. HIGH2040 primary run tetap menunjukkan censoring pada horizon penuh. Interrupted runs setelah restart diarsipkan, bukan dipresentasikan selesai.

## Penggunaan lanjutan

Public-source refresh bersifat opsional (`python -m backend.gedangan.m07_sources`); runtime simulator tidak memerlukan internet. Future empirical bundle menggunakan `m07_baseline_adapter.resolve` hanya setelah M06 gate,approved observations,lineage hash,review evidence dan independent validation benar-benar lolos. Gate sekarang menolak empirical activation. Window baru memerlukan versi runner eksplisit, bukan penambahan horizon diam-diam.

Status browser terakhir dan item QA yang belum selesai ada di `documentation/m07/browser-qa.json`. Screenshot yang ada merupakan bukti saat capture, bukan jaminan QA versi akhir. M08 tetap menunggu persetujuan pengguna.
