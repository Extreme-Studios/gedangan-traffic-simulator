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
