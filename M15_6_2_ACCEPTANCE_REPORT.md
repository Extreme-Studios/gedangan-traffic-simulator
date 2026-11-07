# M15.6.2 — Acceptance Report

2 November 2026, WIB. Staging terpisah: http://127.0.0.1:5204/.

**REVIEW REQUIRED — menunggu pengguna memeriksa video aktual.**

MANUAL / RANDOM SCENARIO — NOT HISTORICAL OBSERVATION. PROVISIONAL NETWORK — NOT FIELD CALIBRATED.

## Keputusan

**Teknis/source: pemeriksaan yang dijalankan lulus. Visual: REVIEW REQUIRED.** Pengguna harus memeriksa actual video sebelum visual acceptance dapat berubah. Tidak membuat final EXE atau memulai milestone lanjutan.

| Pemeriksaan | Hasil |
| --- | --- |
| Footprint sumber | 953 source-mapped, nol footprint rekaan; 58 konflik ditahan |
| Tinggi/fasad | Seluruh tinggi asumsi; karakter stasiun photo-referenced; tidak ada klaim surveyed |
| Network | SHA256 `0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c` sama; alignment/signals/rail/turn/routes/counts/physics tidak diubah |
| Rekaman traffic | 7200 frame tiap run; 7,992,144 posisi kedua run diperiksa exact Float64 |
| Tes baru | 8 unittest integritas lulus; TypeScript dan isolated Vite build lulus; chunk warning>500KB masih ada |
| Preservasi | 682 file checkpoint M15.6/M15.6.1 dan 2984 file ancestor hash-equal; laporan lama tidak ditulis ulang |
| Memori/FPS | Before/after aktual pada dua demand; batas dan accounting ada pada laporan memori |
| Paket screenshot/video | ACTUAL_PACKAGE_READY_USER_REVIEW_REQUIRED — lihat review-package.json untuk berkas dan metadata aktual |
| Aksi dibatasi | Tidak menghapus file, upload GitHub, membuat EXE final, flyover, atau demand/route baru |

Regression scope: tes kontrak geometri/registry/recording/preservasi untuk perubahan renderer ini, bukan klaim menjalankan ulang seluruh suite M01–M15.6.1 atau SUMO eksperimen baru. Hasil actual SUMO lama dibaca sebagai playback; scenario random tidak diubah menjadi pengukuran historis Gedangan. Risiko tersisa: ketidakpastian source map, tinggi/fasad/roof asumsi, kualitas presentasi perlu penilaian manusia, GC/long-term memory belum tersertifikasi dan video screen-capture bisa lebih lunak daripada screenshot langsung.

## Reproduksi dari source yang diserahkan

Gunakan `.venv/Scripts/python.exe -m backend.gedangan.m1562_context` untuk scene dari XML cached; `-m backend.gedangan.m1562_recording` untuk dua buffer dari source asli. Source retrieval optional tersedia pada `m1562_sources.py` dan memakai cache. Build frontend dengan `tsc -p frontend/tsconfig.m1562.json`, lalu Vite memakai `vite.m1562.config.ts` dari folder frontend. Jalankan `staging/m1562/START_M1562.ps1`. Loader preprocessing membuat packed recording baru di namespace sendiri bila pengguna membuka run lain. Jangan menjalankan bootstrap/wire migrasi ulang pada source final; source final sudah memuat hasil migrasi. Source/build turunan terpisah; M12–M15.6.1 tidak ditimpa.
