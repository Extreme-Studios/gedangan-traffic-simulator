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

# M12 QA REPORT
PASS teknis sesuai gate FINAL_ACCEPTANCE_REPORT.md. Bukan field validation.

- Regresi Python: 344 run / 343 pass / 1 service-dependent skip. Inti M10: 31 assertions pass.
- Application actual Chrome: 28 checks, 0 fatal page errors, 0 failed responses, 0 external request.
- Survey: 11 browser checks; state/provenance dan importer M06 dipertahankan.
- Distribusi: 3 cold starts; duplicate launch memakai PID sama; restart, missing-asset dan port conflict diuji.
- Empat waktu uji cocok dengan signal/rail source event; renderer/build M10 unchanged.
- Resolusi 1920x1080, 1366x768 dan field-workbench viewport 390x844 diuji. Tidak ada klaim ponsel fisik/proyektor.

## Hardware/performance aktual
Windows 11 Pro, AMD Radeon Graphics, RAM terlihat OS 11.70 GiB. WMI AdapterRAM dilaporkan terpisah dan bukan konfirmasi VRAM fisik 6 GB. Chrome melaporkan ANGLE AMD Direct3D11, bukan jaminan perangkat target lain. Sampel rolling render-loop sekitar 9 detik per preset, satu baseline 2026; proses authoring/QA lain dapat berlangsung bersamaan. Ini bukan benchmark lengkap semua rekaman.
- performance: measured mean 84.62 FPS, p5 59.17; 0 stalls >50 ms; draw calls 169.
- balanced: measured mean 92.85 FPS, p5 59.52; 0 stalls >50 ms; draw calls 169.
- presentation: measured mean 81.75 FPS, p5 40.65; 0 stalls >50 ms; draw calls 169.
Balanced dipilih sebagai default; preset hanya membatasi rasio drawing pixel.

## Temuan dan perbaikan
- Missing SUMO helper saat frozen import diperbaiki dengan hidden import helper; engine SUMO tidak dieksekusi atau dibundel.
- Mobile intrinsic grid overflow diperbaiki di M12 response stylesheet.
- Slide HTML inline script dieksternalisasi dalam salinan distribusi agar berjalan dengan CSP lokal; duplicate CSP directive dibersihkan.
- Windows sempat menahan port setelah listener fault injection. Handler startup kini tidak membuka dialog di child service; bind failure dilaporkan cepat. Uji foreign port memakai port tersendiri agar tidak menyamakan TIME_WAIT dengan aplikasi aktif.
- Re-run video yang sama ditolak replay guard secara benar; final survey memakai dataset QA kosong.
- Uji yang gagal atau terhenti bukan bukti PASS; hasil final eksplisit tersedia di QA_EVIDENCE.

# M12 SURVEY READINESS / penutupan QA browser M08.5
**BROWSER SOFTWARE ACCEPTANCE PASS dalam distribusi M12.** Status laporan M08.5/M11 historis tidak ditimpa.

Fixture SYNTHETIC_TEST terisolasi. Manual count, class/shortcut, WIB timestamps, pause/resume, IndexedDB saat command request diputus, browser restart/retry exactly once, SQLite checkpoint, backup/restore cabang baru, duplicate command prevention, CSV/JSON export dan 12 preview importer M06 lulus. File video MP4 lokal benar-benar di-hash, diregister, dimainkan, dijeda, di-step dan dianotasi; rewind tidak membuka kembali token yang sudah dicatat. Mobile 390x844 counter dan save diuji di Chrome viewport, bukan ponsel fisik.

Percobaan ulang pada video dengan SHA yang sudah pernah dihitung ditolak sebagai replay/rewind lintas sesi. Ini kontrol duplikasi yang benar; acceptance final memakai workspace kosong. QA tidak mematikan kontrol tersebut.

Lokasi/izin/bukti field belum disetujui. SYNTHETIC_TEST tetap DEMO_SYNTHETIC pada M06; tidak dipromosikan menjadi OBSERVED_FIELD. Reviewer manusia dan QC sebelum kalibrasi tetap wajib. Empirical baseline BLOCKED. Workbench software lulus, kesiapan operasi survei lapangan belum disahkan manusia.
