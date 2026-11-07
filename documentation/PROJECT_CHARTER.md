# Project Charter

Tanggal: 31 Oktober 2026 · Gedangan Traffic Simulator · M01 saja.

## Tujuan

Membangun platform penelitian transportasi berbasis mikrosimulasi untuk kawasan Perempatan Gedangan, Sidoarjo. Hasil akhir berupa digital twin 3D interaktif untuk menilai kemacetan dan membandingkan alternatif, setelah geometri, demand, perilaku, dan baseline dikalibrasi. Versi M01 adalah fondasi perangkat lunak dan tata kelola riset, bukan digital twin tervalidasi.

## Lingkup penelitian yang harus dipertahankan

- Kapasitas koridor utama Sidoarjo–Surabaya adalah fokus pengguna. Pengamatan kurangnya kapasitas alternatif menuju Surabaya belum merupakan hasil survei.
- Frontage merupakan jalur tersendiri dengan koneksi masuk/keluar, bukan tambahan lajur otomatis pada koridor utama. Klaim relatif lancar berasal dari pengguna dan perlu verifikasi lapangan.
- Motor, mobil, bus, truk, trailer dan oversize/special mempunyai kelas, dimensi, dan perilaku tersendiri; dimensinya belum ditetapkan.
- Simpang Gedangan, simpang kawasan Stasiun Gedangan, rel dan perlintasan harus berada dalam sistem jaringan terhubung agar spillback tidak terpotong di batas model.
- OD antarzona, periode waktu, komposisi kendaraan, waktu penutupan palang, pertumbuhan penduduk dan kendaraan perlu sumber serta ketidakpastian.
- Baseline adalah 2026. Data tahun sebelumnya tetap berlabel tahun asal; tidak otomatis menjadi kondisi 2026.

## Hasil M01

Audit lingkungan; struktur modular; React/TypeScript/Vite/Three.js lokal; API Python status; tujuh batas modul domain; schema data dan konfigurasi; register riset; dokumentasi roadmap dan pengujian; launcher START_DEV. Tidak ada EXE, geometri aktual, volume, kapasitas, jadwal kereta, angka pertumbuhan, simulasi nyata, atau klaim efektivitas solusi.

## Target dan keberhasilan

Windows 11, AMD GPU, alokasi VRAM 6 GB, RAM 16 GB, 1080p. Gunakan perangkat lunak gratis/open-source. UI dapat dibuka di Chrome/Edge lokal, scene abstrak tampil, status tidak menyesatkan, schema memisahkan kategori, backend hidup tanpa SUMO. Acceptance detail ada pada laporan M01.

## Batas kewenangan

Tidak menghapus pekerjaan, tidak memasang software dengan administrator, tidak mengubah konfigurasi sistem, dan tidak memulai M02 tanpa persetujuan pengguna. Folder proyek diperiksa sebelum dibuat; awalnya kosong. User brief disimpan pada USER_BRIEF_M01.md.

## Risiko utama

Data survei/batas jaringan belum tersedia; literatur historis dapat tidak cocok dengan frontage atau pola operasi sekarang. Motor dan kendaraan oversize memerlukan kalibrasi yang tidak cukup dengan parameter bawaan SUMO. Spillback dapat bias bila batas OD terlalu dekat. Jadwal kereta belum tentu mewakili waktu penutupan palang. Target kinerja dan ketelitian harus ditetapkan sebelum validasi final.
