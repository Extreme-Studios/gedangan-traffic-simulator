# M14 — Acceptance Report

Tanggal laporan: 1 November 2026 (WIB). Semua jumlah demand adalah masukan eksperimen, bukan pengukuran Gedangan. Tidak ada klaim kalibrasi atau efektivitas rekayasa lapangan.

Staging: `http://127.0.0.1:5199/`. Build: `frontend/dist-m14/`. Jalankan ulang dengan `staging/m14/START_M14.ps1` dari proyek ini. SUMO lokal 1.28.0. Final M12 tidak ditimpa.

Jaringan eksisting: `simulation\network\m051\provisional\network.net.xml`. SHA-256: `0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c`. Tidak ada flyover, ruas baru, koneksi baru, vClass ignoring, atau override izin kendaraan TraCI. Pembatasan kelas/akses/geometri M04.5 tetap diterapkan; izin provisional dalam model bukan sertifikat legalitas atau swept-path lapangan.

## Keputusan
FUNCTIONAL FLOW: PASS. PRESENTATION/PERFORMANCE: CONDITIONAL. M14 menghasilkan SUMO nyata dan playback jaringan eksisting; performa browser dicatat beserta stall, tanpa klaim FPS terjamin atau validasi lalu lintas lapangan.

| Kriteria | Status | Bukti |
| --- | --- | --- |
| Manual exact composition | PASS | 13 tes M14; actual all-ten-class run |
| Random exact total / rounding | PASS | 1,7,499,500,1000,2998,3000,5000 |
| Seed identik reproducible | PASS | Cohort SHA dan demand identik |
| Seed baru berbeda | PASS | Seed42 vs43 |
| Unique ID | PASS | Seluruh requests dan XML audit |
| Legal model routes | PASS with explicit denials | Actual connections/type/access screens; 80 failed pada 3000 |
| Departure tersebar | PASS | Uniform/peak/custom + duration tests; histogram |
| Signal controller berpengaruh | PASS | Actual timing sensitivity |
| Kereta memengaruhi antrean | PASS | Paired160-car experiment; waiting0→2.121875s |
| Statistik sama output SUMO | PASS | Tripinfo independent audit + mass balance |
| Tidak ada flyover / baseline immutable | PASS | Network SHA unchanged; route/no-flyover audit |
| Tidak masuk historical calendar | PASS | Database hashes unchanged; M14 store terpisah |
| Saved scenario reopen | PASS | HTTP save/load + browser save |
| 3000 handled actual | PASS with pending/failed retained | 2920routed/1271departed/566arrived/705active/1649pending/80failed |
| Windows1080p FPS assurance | CONDITIONAL | Measured varying FPS and stalls; raw samples retained |
| Actual screenshot/video | PASS, capture limits recorded | documentation/m14/evidence; video probe JSON |

## Pengujian dan perlindungan
`regression-tests-final.txt`: 357 tests, 356 lulus, 1 skipped (duplicate presentation-service CLI test, karena layanan M09 tidak berjalan). Tidak ada failures/errors. Setelah screen ukuran becak motor diperketat, 13 tes M14 diulang dan lulus; TypeScript build/type check lulus. Generate dari browser pada build final juga menghasilkan 50 requested, 49 routed/departed/moved, 41 arrived, 8 active, 1 failed; diperiksa dalam `browser-final-audit.json`. Duplicate/Save/Load diuji lewat UI dan memulihkan total50 serta nama salinan, lihat `browser-qa.json`. `xml-independent-audit.json` dan `final-xml-audit.json`: 11 run, semua checks pass: True. Perlindungan 14 berkas/arsip: PASS.

## Cara mencoba
1. Buka staging localhost5199; pilih tanggal/jam WIB dan durasi.
2. Pilih manual/random, jumlah, profil/seed, pendekat dan belok yang tersedia.
3. Preview; periksa total, distribusi dan failed routes.
4. Edit timing/jadwal asumsi bila diperlukan; klik Generate Simulation.
5. Tunggu progress actual; hasil dan rekaman 3D terbuka otomatis. Pilih Play, kamera, timeline dan kecepatan.
6. Save Scenario menyimpan request/seed. Load memulihkan request; Duplicate memberi salinan yang dapat disimpan terpisah.

## Batas yang belum selesai
- Izin sepeda/becak nonmotor tidak tersedia pada baseline; ditolak eksplisit.
- Belok/arah KA di luar koneksi existing tidak dibuat. Jadwal KA hanya nominal assumption, bukan jadwal resmi.
- Data geometri, signal timing, dimensi/dinamika belum divalidasi survei. Tidak ada legal swept-path certificate untuk trailer.
- Queue extent dan boundary sample adalah model proxy. Tidak ada klaim causal field spillback.
- FPS dan capture video bervariasi karena sesi browser; tidak dinyatakan sebagai presentasi 1080p mulus terjamin.
- M14 adalah staging web dengan runner SUMO lokal, bukan penggantian atau EXE rilis baru M12.

## Deliverables
Delapan laporan root M14, staging frontend/backend, skenario JSON, SUMO XML/output, manifest/hash/source snapshot final, screenshot, video aktual dan performance logs telah disimpan. Tidak ada upload GitHub, penghapusan data penelitian, perubahan final M12, atau implementasi flyover/milestone berikutnya.
