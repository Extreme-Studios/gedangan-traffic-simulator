# M14 — Manual Traffic Scenario Builder

Tanggal laporan: 1 November 2026 (WIB). Semua jumlah demand adalah masukan eksperimen, bukan pengukuran Gedangan. Tidak ada klaim kalibrasi atau efektivitas rekayasa lapangan.

Staging: `http://127.0.0.1:5199/`. Build: `frontend/dist-m14/`. Jalankan ulang dengan `staging/m14/START_M14.ps1` dari proyek ini. SUMO lokal 1.28.0. Final M12 tidak ditimpa.

Jaringan eksisting: `simulation\network\m051\provisional\network.net.xml`. SHA-256: `0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c`. Tidak ada flyover, ruas baru, koneksi baru, vClass ignoring, atau override izin kendaraan TraCI. Pembatasan kelas/akses/geometri M04.5 tetap diterapkan; izin provisional dalam model bukan sertifikat legalitas atau swept-path lapangan.

## Alur yang tersedia
Tanggal native date picker (termasuk bulan/tahun), start WIB, 15/30/60/90/120 menit atau custom 60–14.400 detik; mode manual 10 kelas atau random sampai 10.000 permintaan; seed; komposisi; enam pendekat nyata; persentase belok; departure merata/puncak/custom 5/15/60 menit; parameter sinyal dan jadwal KA asumsi. Preview menampilkan komposisi, rute lolos/gagal, dan histogram departure sebelum Generate.

Generate menjalankan validasi, alokasi, routing, penulisan SUMO XML, SUMO nyata, pengumpulan output, lalu membuka rekaman 3D. Progress berasal dari langkah SUMO, bukan timer dekoratif. Error dipertahankan dengan penyebab. Save/Load/Duplicate membuat skenario JSON terpisah, bukan observasi historis.

## Implementasi
Modul baru `backend/gedangan/m14_*.py`, `frontend/src/m14/`, `frontend/manual.html`, `frontend/vite.manual.config.ts`, `tests/m14/`. Renderer M10 disalin ke namespace M14; sumber M10 tidak diedit. Render menggunakan geometri jaringan dan trajectory SUMO aktual, dengan interpolasi spasial antar sampel 0,5 detik. Kapasitas instancing dihitung dari maksimum kendaraan aktif per tipe, bukan seluruh permintaan.

## Hasil utama aktual
Final run `67e1a759e0845754c09be215`: diminta 3000; lolos rute 2920; berangkat 1271; tiba 566; aktif 705; belum berangkat 1649; gagal rute 80. Tidak ada peristiwa izin/tabrakan/teleport yang tercatat. Run 120 menit `7e574d4fb954f9ed77f0d6b4` benar-benar dieksekusi: 100 diminta, 98 routed, 98 berangkat, 96 tiba, 2 aktif.

## Bukti
- `documentation/m14/final-3000.json`, `duration-120min.json`, `final-xml-audit.json`.
- `simulation/runs/m14/<run_id>/`: input manifest, demand, route/config XML, FCD, tripinfo, statistik, vehicle ledger, phase transitions, playback chunks dan output hash.
- Screenshot dan video aktual: `documentation/m14/evidence/`. MP4 `GEDANGAN_M14_ACTUAL_SUMO.mp4` ditranscode dari capture canvas aktual sekitar 12s / 358 frame; provenance terpisah dalam `video-provenance.json`.
- Perlindungan data: PASS, 14 berkas/arsip dibandingkan SHA-256, tidak berubah.

## Batasan
Tidak semua permintaan masuk jaringan dalam horizon 15 menit. Sepeda dan becak nonmotor tidak diizinkan baseline. Gerakan belok dan arah KA dibatasi konektivitas yang benar-benar ada. Kedatangan KA nominal tidak dipaksa tepat pada waktu input. Performa browser bervariasi; lihat laporan benchmark, termasuk stall rendah, tanpa mengklaim FPS terjamin.
