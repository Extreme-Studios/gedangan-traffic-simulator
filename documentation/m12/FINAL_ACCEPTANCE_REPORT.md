# FINAL ACCEPTANCE REPORT
Gedangan Traffic Simulator v1.0.0 | EXTREME STUDIOS | 2026-11-01

**PRESENTATION-READY ILLUSTRATIVE RELEASE**. SOFTWARE RELEASE READY dan PRESENTATION READY untuk penggunaan ilustratif yang diuji. Bukan field-validated production model.

| Gate | Status |
|---|---|
| SOFTWARE FUNCTIONALITY | PASS |
| 3D DIGITAL TWIN | PASS |
| SUMO SIMULATION INTEGRITY | PASS |
| PRESENTATION READINESS | PASS |
| OFFLINE DEPLOYMENT | PASS |
| WINDOWS PORTABILITY | PASS |
| FIELD SURVEY WORKBENCH | PASS |
| REPORT EXPORT | PASS |
| EMPIRICAL BASELINE | BLOCKED |
| INFRASTRUCTURE FEASIBILITY | CONCEPT ONLY |
| HUMAN ACCEPTANCE | PENDING |

## Bukti teknis
- Frozen Windows x64 EXE berjalan tanpa Python/Node/SUMO eksternal; browser Edge/Chrome dengan WebGL2 tetap prerequisite.
- Ekstraksi ke folder baru dengan spasi dan PATH hanya Windows/System32. Tiga cold start, duplicate same PID, clean shutdown, restart persistence, missing-asset rejection dan foreign-port rejection diuji.
- Chrome aktual: tahun 2026/2030/2035/2040, HIGH, pasangan APILL, split sinkron, kamera, fullscreen, preset kualitas, sepuluh bagian presentasi, video Full HD dan ekspor aktual PDF/CSV/JSON.
- Semua non-loopback network request diblokir pada level browser selama QA. Tidak ada request keluar tercatat. Tidak ada firewall/security setting diubah.
- Audit source memverifikasi 23 recording indexes/chunks/scenes dan hash SUMO output asli, bukan membaca laporan saja. Accounting seluruh run tetap benar.
- Regresi: 344 tests dijalankan; 343 lulus, satu skip service M09 terpisah. 31 assertion inti M10 lulus. 9.236 berkas baseline M01-M11 tidak berubah.
- Survey: manual count, shortcut, timestamp, pause/resume, IndexedDB setelah koneksi gagal, browser recovery, duplicate idempotency, SQLite checkpoint/backup/restore, video hash/play/pause/step/annotation/rewind, enam CSV dan JSON lewat importer M06, dan mobile counter diuji.
- PPTX asli 15 slide dan 15 notes, PDF M11, MP4 dan semua 15 gambar dipertahankan. HTML salinan distribusi mengeluarkan inline script ke berkas lokal agar sesuai CSP.

## Batas acceptance
- PASS survei adalah acceptance browser/software pada fixture SYNTHETIC_TEST. Lokasi, izin, clock, coverage dan data lapangan tetap memerlukan review manusia.
- Baseline empiris BLOCKED; tidak ada observasi Gedangan yang dipromosikan menjadi verified pada pekerjaan ini.
- Flyover/underpass CONCEPT ONLY. Tidak ada bypass clearance, legalitas, swept path, lane permission atau oversize.
- Runtime distribusi memutar hasil SUMO yang direkam, bukan menjalankan simulasi/kalibrasi SUMO baru. M06 preview dan dataset versioning tersedia. Eksekusi kalibrasi baru memakai toolchain riset terpisah sesudah QC; baseline lama tidak ditimpa.
- Uji Windows dilakukan di mesin ini, bukan clean VM, PC kedua, ponsel fisik atau proyektor fisik. Binary belum ditandatangani sertifikat penerbit.
- HUMAN ACCEPTANCE tetap PENDING. Tidak ada klaim FULLY VALIDATED.

## Mulai
Ekstrak seluruh paket lalu buka APPLICATION/GEDANGAN_TRAFFIC_SIMULATOR.exe. Alternatif: START_GEDANGAN_TRAFFIC_SIMULATOR.bat. Tutup melalui tombol aplikasi atau STOP_GEDANGAN_TRAFFIC_SIMULATOR.bat. Baca DOCUMENTATION/QUICK_START_ID.pdf.
