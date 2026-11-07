# Browser acceptance — PENDING TOOL BLOCK

Tidak ada screenshot atau bukti interaksi browser aktual untuk M08.5 pada tahap ini. Build dan HTTP 200 bukan bukti playback/keyboard/layout lulus.

Internal preview diminta melalui `open_in_codex` untuk `http://127.0.0.1:5194/survey.html`; tool mengembalikan **queued**, bukan bukti tab telah dirender. Browser-use/CUA sebelumnya tidak tersedia dalam daftar alat runtime terbaru. Percobaan fallback Computer Use untuk window Chrome yang benar-benar dikembalikan inventory dihentikan alat sebelum kontrol halaman:

> Computer Use has been stopped for this turn because it could not determine the current browser URL on Windows with enough confidence to enforce policy.

Tidak ada tindakan input browser berikutnya atau bypass terhadap penghentian tersebut. Backend, tes, build, pemeriksaan hash dan dokumentasi tetap dikerjakan. Tidak meminta pengguna mengubah security/privacy settings.

## Skenario yang masih harus dijalankan melalui alat browser yang berfungsi

1. Jalankan server sintetis terpisah, `--data-dir data/surveys/m085/synthetic-ui-qa --ui-port 5194 --api-port 8784 --synthetic-environment`. Default produksi 5184 harus tetap kosong dari fixture.
2. Buka 13 panel. Periksa console, seluruh request hanya loopback/Blob, kegagalan server, pesan error dan pending input. Simpan screenshot nyata desktop 1920×1080, tablet 1024×768 dan mobile 390×844; ukur overflow.
3. Buat latihan sintetis. Uji touch dan shortcut 10 kelas, Shift-arrows, Ctrl+Z, pause/resume, catatan, interval, undo/edit/duplicate, event pagination. Pastikan mengetik angka di form tidak menghitung.
4. Pilih fixture MP4 ber-watermark 12 detik melalui file picker. Cocokkan SHA256 dengan `sha256-tests.json`. Uji play/pause, seek, speed, frame step nominal, fullscreen dan zoom; catat posisi playback aktual saat count.
5. Count token sama harus terkunci, replay tak menghapus ledger. Rewind + token baru tanpa konfirmasi harus ditolak. Berpindah dari video ke manual tidak boleh mengaktifkan dua listener count.
6. Unknown recording clock tetap VIDEO_TIME_ONLY. Ekspor menunjukkan penolakan. Review clock berbukti menambah versi, tidak mengubah raw lama; ekspor bertanggal memakai mapping baru.
7. Queue tanpa referensi meter ditolak untuk panjang. Censoring, travel endpoints/rute, missing signal dan railway stages, multiple movements, CRS/units/CSV geometry serta error validation berfungsi.
8. Dua observer sample group/window sama dibandingkan per kelas/gerakan/interval; missing bukan nol. Adjudikasi reviewer independen tercatat tanpa averaging.
9. Putuskan hanya layanan M08.5 pada lingkungan uji; input masuk IndexedDB dan belum berstatus committed. Restart browser/server, replay dengan idempotency, arsip FAILED dengan alasan. Jangan mematikan adapter internet/menurunkan keamanan global.
10. Ekspor seluruh 6 CSV/6 JSON/ZIP, periksa accepted/rejected aktual M06. Backup/download/upload/restore cabang baru, raw/audit/lineage tetap valid; sumber media asli tidak disalin.
11. Uji production static Python tanpa Vite/Node/cloud. Empirical status tetap BLOCKED; synthetic tetap ber-watermark. Setelah QA lulus, perbarui laporan/evidence/acceptance; jangan mengubah M01–M08 atau memulai M09.

QA ini bukan permintaan persetujuan atau pernyataan pekerjaan selesai. Ini daftar bukti penerimaan yang belum dapat dikumpulkan karena penghentian alat.
