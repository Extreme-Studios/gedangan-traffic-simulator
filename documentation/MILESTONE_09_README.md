# Gedangan Traffic Simulator — M09

## Membuka demonstrasi

Klik dua kali **START_GEDANGAN_PRESENTATION.bat** pada root proyek, atau launcher dengan nama sama di `presentation_demo/m09/`. Launcher memeriksa Python/build/cache lokal, memverifikasi cache, menggunakan kembali server M09 yang sudah aktif dan membuka dashboard otomatis:

**http://127.0.0.1:5185/presentation.html**

Port M09 terpisah dari M06/M08/M08.5. Tidak perlu membuka terminal atau JSON untuk presentasi. Sesudah build tersedia, demo memakai Python lokal dan cache rekaman; Node/SUMO live/internet/login tidak diperlukan. Launcher tidak mengubah firewall, tidak memasang dependency dan tidak menghentikan service lain bila port sudah dipakai. Jika port dipakai aplikasi lain, pesan error meminta penggunaan port alternatif oleh pengelola teknis.

Tunggu **START PRESENTATION** aktif. Rekaman utama dipreload sebelum alur dimulai. Model memakai demand ilustratif, bukan arus lalu lintas hasil survei Gedangan. Status acceptance aktual tercantum dalam `MILESTONE_09_REPORT.md` dan `presentation_demo/m09/qa/acceptance.json`.

## Kontrol presenter

- **Play / Pause / Reset**, timeline 0,5–2100 detik dan speed 0,5×–16× mengontrol rekaman SUMO. Reset kembali ke awal rekaman; kendaraan belum berangkat tidak dimunculkan lebih awal.
- Pilih delapan kamera: aerial master, main corridor, reverse corridor, Gedangan intersection, railway crossing, frontage, follow vehicle dan free orbit. Reset kamera mengembalikan komposisi preset. Aerial master mencakup seluruh jaringan sekitar 4 km, sehingga kendaraan terlihat kecil; gunakan koridor/follow untuk detail.
- **Analisis & filter** membuka kelas kendaraan dan pemilih kendaraan yang sedang aktif. Pilih kendaraan lalu **Ikuti pilihan**, atau klik kendaraan dalam scene. Kecepatan dan dimensinya berasal dari rekaman/registry model. Saat tidak aktif, kendaraan tidak diputar lagi atau dianggap berhenti palsu.
- **Konteks dekoratif** menyembunyikan bangunan dan vegetasi stylized. Retained OSM query tidak menyediakan footprint bangunan; massa bangunan tidak boleh digunakan sebagai peta bangunan, ROW atau elevasi terukur.
- **Fullscreen** memperbesar scene. Pada mode presentasi tombol ini memperbesar seluruh alur sehingga tombol next/previous dan talking points tetap terlihat.
- Dalam presentasi: **← / →** untuk bagian sebelumnya/berikutnya, **Space** untuk playback saat fokus bukan input/tombol, **Escape** untuk keluar presentasi/fullscreen, dan **Mulai ulang** untuk kembali ke intro. Tombol sentuh tetap tersedia.
- **Tutup layanan M09** menutup server M09 dengan token lokal. Ctrl+C di jendela launcher juga menutup bersih. Halaman yang sudah memuat cache dapat tetap terlihat; buka launcher kembali untuk mengaktifkan layanan.

## Tahun, demand dan skenario

Tahun 2026–2040 dan LOW/REFERENCE/HIGH mempunyai tabel demand M07. Main recordings meliputi baseline 2026/2030/2035/2040 REFERENCE dan intervensi operasional yang benar-benar dijalankan pada M08. Ada 23 rekaman seed42 provisional dan 17 pasangan perbandingan. Tidak semua kombinasi 15 tahun × 3 growth × 8 skenario pernah dijalankan.

**NOT RUN** berarti belum ada rekaman untuk pilihan tepat tersebut. **NOT SIMULATION READY** berarti skenario diblokir. **CONCEPT ONLY** berarti flyover/underpass belum mempunyai jaringan/desain yang layak disimulasikan. Aplikasi tidak memainkan rekaman tahun lain dengan label baru. Pilih baseline 2026 REFERENCE untuk kembali ke demonstrasi yang tersedia.

S00 baseline; S01 alternatif timing APILL sintetis; S02 pembatasan belok feeder existing; S03 pembatasan akses frontage existing; S04 penundaan jadwal kendaraan berat dengan biaya deferral eksplisit. S05 koordinasi diblokir karena hanya ada satu road controller yang valid. S06/S07 tetap konsep, tanpa kendaraan di struktur baru atau angka efektivitas.

## Membaca hasil

Kartu utama adalah **hasil horizon 35 menit**, bukan nilai sesaat: requested, arrived, running at end, unserved, mean waiting departed cohort dan episode spillback terverifikasi di model. Kendaraan terlihat/berhenti dan status APILL/perlintasan pada scene adalah kondisi playback saat ini.

Unserved menghitung failed route, belum berangkat dan belum selesai. Mean elapsed/waiting bersyarat pada departed cohort dan mencakup unfinished trips. Arrived-only travel-time benefit tidak ditampilkan sebagai manfaat seluruh demand. Arrivals/hour dihitung dari fixed horizon, bukan kapasitas jalan terukur. Nilai contoh 2026 baseline: 240 requested, 183 arrived, 23 running at end dan 57 unserved; bukan volume lalu lintas aktual Gedangan.

**COMPARISON** memakai dua trajectory terpisah, kamera/waktu yang sama, cohort/tahun/growth/seed/horizon yang lolos guard M08 dan network delta yang dijelaskan manifest. Delta bukan rekomendasi kebijakan. S01 bukan lampu APILL lapangan yang telah dioptimalkan atau disahkan.

## Keakuratan dan batas visual

- Lane/junction/rail mengikuti network M05.1 melalui turunan M08. Transformasi: `worldX=x−originX`, `worldZ=−(y−originY)`, `worldY=sourceZ atau 0 + surface offset`. Tidak ada perubahan routing, koneksi atau geometri simulasi.
- FCD beresolusi 0,5 detik. Label FCD digeser +0,5 detik agar cocok dengan clock TraCI; setiap ekspor memverifikasinya pada snapshot kendaraan yang sama. Interpolasi hanya antarsampel kendaraan yang sama; gap/discontinuity tidak diisi dengan rute baru.
- FCD adalah posisi depan kendaraan. Model 3D dipusatkan setengah panjang ke belakang menurut heading. Kereta delapan bagian mengikuti centerline rel dan panjang model 80 m. Ini siluet model, bukan spesifikasi armada yang telah disurvei.
- State sinyal/perlintasan direkam dengan sampling 1 detik. Warna dibaca per controlled link, bukan menebak izin seluruh simpang. Sudut boom adalah representasi schematic dari recorded control state; bukan sensor sudut/posisi palang fisik.
- Marka, poles, boom, material, ukuran furniture, pohon dan massa bangunan adalah render-only assumptions / stylized context. Tidak menyatakan stop line, clearance, izin, elevasi atau swept path terverifikasi. Tidak mengizinkan oversize; model oversize tidak dimunculkan tanpa actual record.
- Lajur sekitar 0,10 m dan deviasi M05.1 lama dipertahankan sebagai keterbatasan model. Render tidak menyamarkan atau memperbaiki jaringan secara diam-diam.

## Menyiapkan laptop rapat

1. Jalankan launcher sebelum rapat; pastikan Start Presentation sudah aktif dan seluruh rekaman utama selesai preload.
2. Gunakan 1920×1080. Fullscreen dan preset kamera lebih aman daripada orbit bebas saat demonstrasi.
3. Buka langkah Railway, Play dan perhatikan penutupan/pembukaan yang direkam. Scrub 105,5 s untuk kereta di crossing, lalu 160 s untuk pelepasan.
4. Pilih REFERENCE untuk empat tahun utama dan S01 2026 untuk perbandingan yang telah dipasangkan. HIGH 2040 tersedia untuk demonstrasi kepadatan dalam model.
5. Jelaskan kalibrasi belum ada sebelum membahas angka. Field Data memuat kebutuhan survei; status M08.5 lama tidak dipromosikan oleh M09.
6. Jangan mengubah source/cache mendadak sebelum rapat. Jika asset hilang, jalankan rebuild dan ulangi QA; jangan mengganti dengan animasi rekaan.

## Rebuild teknis

`REBUILD_PRESENTATION_M09.bat` memeriksa checkpoint, mengekspor ulang dari FCD M08 yang immutable, memeriksa TypeScript/build, menjalankan seluruh regression dan tes core, lalu memeriksa checkpoint kembali. Memerlukan dependency yang sudah tersedia; tidak memasang paket atau mengunduh model. Jangan menjalankan rebuild bersamaan dengan regression/browser acceptance yang membaca folder dist.

Browser automation memanfaatkan Playwright yang sudah dibundel runtime Codex. Set `M09_RUNTIME_PACKAGES` ke direktori Node packages yang diberikan `load_workspace_dependencies`, kemudian jalankan `node tests/m09/browser-qa.cjs`. Browser memakai Chrome terisolasi dan hanya mengizinkan request loopback M09. Tidak menggunakan profil login pengguna.

**EMPIRICAL BASELINE: BLOCKED — DATA REQUIRED. Tidak ada M10–M12 atau kalibrasi empiris yang dimulai.**
