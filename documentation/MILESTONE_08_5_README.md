# Gedangan Field Survey Workbench — M08.5

Status: **PARTIAL — browser acceptance pending**. Implementasi, build, dan pengujian backend tersedia. QA playback video, shortcut, pemulihan IndexedDB dan layout desktop/tablet/mobile belum dibuktikan karena alat kontrol browser berhenti. Jangan menganggap perangkat sudah disahkan untuk deployment lapangan.

**OBSERVED GEDANGAN DATA: NOT YET COLLECTED**  
**EMPIRICAL BASELINE 2026: BLOCKED — DATA REQUIRED**  
**M09: NOT STARTED**

## Menjalankan

1. Jalankan `START_SURVEY_M085.bat` dari root proyek.
2. Buka `http://127.0.0.1:5184/survey.html` pada internal browser atau browser lokal. API memakai port 8774. Tutup server lewat Ctrl+C pada jendela launcher bila perlu. Jangan menghentikan lab M06/M08 yang memakai port lain.
3. Setelah build tersedia, server hanya memerlukan Python lokal proyek dan berkas `frontend/dist-m085`. Tidak memerlukan Node, internet, login, cloud, GPU, atau model AI untuk menjalankan workbench.
4. `REBUILD_SURVEY_M085.bat` memeriksa baseline, semua tes, SHA256, TypeScript dan build lokal. Dependency harus sudah tersedia; script tidak menginstal atau mengunduh apa pun. Script ini tidak menjalankan generator atau optimizer milestone lama.

## Survei pertama di Perempatan Gedangan

1. Buka **Location Reconnaissance**. Pilih salah satu tujuh lokasi M06. Peta oranye adalah edge model, bukan titik kamera yang disahkan.
2. Buka **Observer Quality Control**, daftarkan alias pengamat dan reviewer, lengkapi lima latihan: klasifikasi, sinkronisasi clock, coverage, kontrol duplikasi dan privasi/keselamatan. Hindari identitas pengemudi.
3. Kembali ke reconnaissance. Ukur koordinat/CRS/akurasi, posisi aman, arah, lajur/gerakan terlihat, hambatan, pencahayaan, signal/railway visibility dan izin. Foto opsional hanya direferensikan dengan hash; tidak disalin ke database. Catat kebutuhan pengamat/kamera tambahan untuk area tak terlihat.
4. Reviewer memeriksa bukti aktual. Terapkan **FIELD_VERIFIED**, kemudian **APPROVED_FOR_SURVEY**. Bukti sintetis tidak dapat mengesahkan lokasi.
5. Buat sesi melalui **Survey Session Planner**. Tetapkan lokasi, pengamat, sumber, clock WIB, approach, arah, metode dan jenis survei. Untuk perbandingan independen, buat sesi kedua dengan window/sample group sama dan observer berbeda. Usulan 3 hari kerja + 1 akhir pekan, 07–09 / 12–14 / 16–18 bukan peak hour terukur dan bukan jaminan kecukupan penelitian.
6. Pilih sesi, ubah **READY**, lalu **IN_PROGRESS**. Sesi field belum bisa dimulai tanpa lokasi disetujui dan pengamat terlatih.
7. Untuk **Manual Traffic Counter** atau **Turning Movement Counter**, periksa approach/arah/lajur/gerakan terlebih dahulu. Ketuk kelas atau gunakan shortcut angka yang ditampilkan. Shift+←/↑/→ memilih gerakan, Ctrl+Z menambah void untuk count terakhir. Input dalam form tidak dihitung sebagai kendaraan.
8. Count disimpan di IndexedDB dahulu, lalu dikonfirmasi SQLite. Badge antrean harus nol sebelum undo, ekspor, backup atau restore. Bila gagal, periksa alasan, kirim ulang, atau arsipkan input FAILED beserta alasan. Jangan menganggap angka antrean sebagai event yang telah diterima.
9. Coverage **COMPLETE** harus dinyatakan untuk kelas, gerakan dan rentang yang benar-benar ditinjau. Nol hanya sah pada cakupan lengkap yang diamati. Gap, missing dan interval belum selesai tetap NULL. Coverage bertumpuk menghasilkan flag review dan NULL.
10. Catat queue count dan meter secara terpisah. Panjang meter membutuhkan referensi terukur, bukti dan konfirmasi; penanda piksel bukan meter. Tandai boundary censored bila ekor antrean keluar bidang pandang.
11. Travel time menggunakan endpoint, rute, token anonim dan timestamp aktual. Signal mencatat enam kejadian terpisah. Railway mencatat sepuluh kejadian terpisah; kereta tambahan dalam closure yang sama dapat dicatat sebagai structured JSON. Geometri memerlukan instrumen/metode/sumber/CRS/akurasi dan satuan meter untuk dimensi jalan.
12. Review hasil dua observer pada sampel sama. Baca perbedaan per kelas/gerakan/interval, bukan satu agreement universal. Reviewer memilih tally A/B atau recount dengan alasan; aplikasi tidak merata-ratakan otomatis.
13. Selesaikan sesi dan lakukan review dataset. Video/manual field memerlukan reviewer berbeda, bukti field dan persetujuan lokasi. **Data Validation & Export** menjalankan importer M06 yang sama dalam staging M08.5 dan menampilkan accepted/rejected.
14. Unduh CSV/JSON/ZIP dan baca `preimport-rejected.json`, `m06-rejected.json`, manifest, provenance dan quality flags. Enam format schema M06 tetap sama. Raw, koreksi, lineage dan versi pemetaan disertakan. Import berhasil belum berarti baseline telah dikalibrasi.
15. Buat backup ZIP, uji restore ke cabang baru dan simpan asli video sesuai izin/retention. Workbench memensiunkan referensi; penghapusan video asli dilakukan pemilik secara manual sesuai kewenangan.

Checklist cetak tersedia pada Dashboard dan `documentation/m085/FIRST_SURVEY_CHECKLIST.md`.

## Anotasi video lokal

- Gunakan sesi **VIDEO_OBSERVATION**; untuk latihan gunakan **Buat sesi latihan sintetis**. Semua latihan wajib tetap `SYNTHETIC_TEST` dan ber-watermark.
- Pilih video lokal MP4 H.264 yang kompatibel. Browser membaca melalui file/Blob; hashing worker membaca potongan 1 MiB. Tidak ada endpoint upload video, deteksi AI, pengenalan wajah atau pelat.
- Tunggu SHA256 dan durasi, isi metadata/izin, kemudian **Register & hubungkan video** sebelum anotasi pertama. Setelah browser ditutup, pilih ulang file dengan hash sama. Tidak ada video asli dalam backup database.
- Jangan menebak waktu dari nama file atau modification time. Clock tidak diketahui tetap **VIDEO_TIME_ONLY** dan tidak lolos ekspor M06 sebagai observasi bertanggal. Reviewer dapat menambah versi mapping clock dengan bukti; raw lama tetap utuh.
- Play/pause, timeline, .25/.5/1/2×, fullscreen, zoom dan stepping tersedia. Langkah 1/FPS bersifat nominal; tanpa FPS langkah sekitar 40 ms, bukan janji frame-exact untuk semua codec/VFR.
- Satu token untuk satu kendaraan anonim. Sesudah count, klik **Kendaraan baru** / Shift+N. Token sama pada video ber-hash sama ditolak. Rewind/overlap memerlukan konfirmasi kendaraan berbeda yang belum dihitung dan alasan diaudit. Ini bukan deteksi otomatis kendaraan fisik yang sama.
- Simpan coverage video yang benar-benar direview. Sekadar memutar video tidak membuat coverage lengkap.
- Fixture `tests/fixtures/m085/synthetic-annotation.mp4` hanya color test pattern 12 detik ber-watermark; bukan video Gedangan. Gunakan sesi latihan baru dan kosong sebelum memasangnya.

## Penyimpanan dan pemulihan

SQLite default: `data/surveys/m085/survey.sqlite`; pointer aktif: `active-db.json`. WAL + synchronous FULL, transaksi, idempotent command IDs, raw/version/correction/audit append-only dan pemeriksaan hash/projection digunakan. Jangan mengedit database secara langsung. Tutup server sebelum menyalin file database secara manual; gunakan fitur backup untuk snapshot yang konsisten.

Restore memerlukan teks `RESTORE_AS_NEW_BRANCH`. Cabang lama dipertahankan, checksum ZIP/database dan integritas diperiksa sebelum pointer berubah. Restore tidak menyertakan video asli, antrean/draft browser atau folder ekspor lama; paket ekspor harus disimpan terpisah. File hash membantu integritas, bukan tanda tangan kebal administrator.

IndexedDB terpisah per port menyimpan input yang belum dikonfirmasi dan arsip FAILED. Draft form yang belum dikirim dan penanda frame belum menjadi raw event; simpan pengamatan/checkpoint sebelum menutup browser. Status draft memperingatkan perubahan, tetapi tidak melakukan autosave draft form. Gunakan **Catat awal/akhir** dan **Simpan pengamatan** untuk menyimpan data sebenarnya.

## Batas saat ini

QA visual/playback/keyboard/touch, recovery antrean browser setelah restart dan layout 1920×1080 / 1024×768 / 390×844 masih **PENDING**. Lihat `documentation/m085/BROWSER_QA_PENDING.md`. Tidak ada screenshot palsu atau klaim lulus. Tidak ada data lapangan Gedangan yang dikumpulkan oleh pekerjaan ini, tidak ada optimizer M06 dijalankan, dan M09 belum dimulai.
