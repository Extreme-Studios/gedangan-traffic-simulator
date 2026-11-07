# MILESTONE 05 — Cara menjalankan

Status: **PARTIAL**. Actual SUMO pilot rail/signals/mixed traffic lulus mekanisme. QA browser desktop/mobile sudah selesai. Review adaptasi geometri crossing dan kausalitas kandidat spillback Gedangan masih terbuka. Baca MILESTONE_05_REPORT.md. **M06 belum dimulai.**

Project: `C:\Users\ROG ALLY\Documents\EXTREME STUDIOS\PROJECT\Simulasi Kemacetan Lalu Lintas`

## Viewer

Jalankan `START_BEHAVIOR_M05.bat` lalu buka [Behavior M05](http://127.0.0.1:5179/behavior.html). Port5179khususM05. Launcher lama tidak diganti. URL menampilkan recorded outputs; tidak mengendalikan SUMO secara real-time. Jika ingin hanya menyalakan server tanpa membuka browser eksternal, gunakan `START_BEHAVIOR_M05.bat --no-browser`.

Pilih skenario dan seed; Putar/Jeda, Reset, speed1/5/10/25×, timeline, Perlintasan/Atas/Jaringan. Drag orbit, scroll zoom, klik kendaraan atau pilih inspector. Toggle Jalan/Rel/Antrean. Event timeline melompat ke fase aktual. Angka unserved/running tetap ditampilkan. Source road geometry dan frontage terpisah.

Label wajib: **SYNTHETIC TRAFFIC EXPERIMENT — NOT CALIBRATED TO GEDANGAN 2026.** Jangan menggunakan angka ini sebagai hasil penelitian lalu lintas aktual.

## SUMO-GUI

Jalankan `SHOW_BEHAVIOR_SUMO_M05.bat`. Native GUI memakai actual seed42/runG, pause pada105dan130s. Tombol Play melanjutkan ke breakpoint berikutnya. Output GUI terpisah pada documentation/m05/gui-session. Pada105s kereta berada di crossing; pada130s road crossing sudah open. Synthetic block signals hanya di varianH, bukan klaim equipment railway nyata.

## Rebuild

Jalankan `REBUILD_BEHAVIOR_M05.bat` dari Windows. Memakai `.venv`, SUMO portable1.28.0dan npm dependencies yang sudah ada. Tidak menginstal tool tambahan. Proses melakukan22instrumented runs (dua seeds utama), controlled lateral/spillback fixtures, deterministic rebuild/repeat, analysis, full-sample safety, export, tests dan production build. Hasil lamaM01–M04.5tidak ditulis ulang.

Konfigurasi: configuration/behavior-m05/profiles.json, signals-m05/program.json, railway-m05/pilot.json. Parameter behavior pada profiles.json mencatat profil yang diuji; parameter longitudinal tetap registryM04. Schedules synthetic didefinisikan eksplisit pada m05_behavior.py. Mengubah input memerlukan rebuild dan review hasil, bukan menganggap hash lama masih berlaku.

## Bukti dan batas

- documentation/m05/scenario-results.json:22runs lengkap dan failure accounting.
- Setiap simulation/runs/m05/*:run.sumocfg, demand/provenance, FCD, tripinfo, summary, playback, events, crossing-events, queue-timeline, vehicle-lifecycle, safety-audit.
- documentation/m05/safety-audits.json:2,814,465samples0.5s, illegal lane/red crossing samples0.
- final-regression.txt:Ran 134 tests in 26.822s; Vite/TypeScript lulus.
- reproducibility.json:network hash dan repeat XML element-identical.
- Isolated fixtures dinyatakan terpisah, tidak disajikan sebagai observedGedangan.
- OriginalM04.5immutable. M05rail derivative mempunyai4edge-endpoint/7lane-shapeadaptations lokal yang belum diterima sebagai exact geometry preservation.
- Mean waiting/travel yang berasal dari tripinfo hanya arrived trips; lihat running/not_departed/lifecycle untuk censoring.
- Pending insertion tidak sama dengan seluruh demand yang belum selesai. Tidak ada unexplained teleport/collision pada run valid.
- Kandidat spillback Gedangan belum konfirmasi kausal. Oversize tetap diblokir; akses heavy tetap asumsiProvisionalM04.5.

## QA browser akhir

Akses pulih setelah restart pengguna. Versi akhir diverifikasi pada desktop1920×1080/mobile390×844 tanpa overflow horizontal. Playback, pause/reset/scrub/rate, camera presets/orbit/zoom, layers, vehicle inspector dan event jumps berfungsi. Loading tidak lagi menyajikan nol atau crossing open tanpa data. Final clean browser session tanpa warning/error. Screenshot: documentation/m05/browser-final-desktop.jpg dan browser-final-mobile.jpg. Direct vehicle raycast click belum diuji terpisah; dropdown inspector teruji. M06 tidak dimulai.
