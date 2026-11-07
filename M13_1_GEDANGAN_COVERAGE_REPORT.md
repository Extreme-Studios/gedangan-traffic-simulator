# M13.1 — Cakupan Bukti Gedangan

Tanggal audit: 2026-11-01T13:29:43.783775+00:00

## Observasi per jam yang diterima

**Nol observasi baru lolos kalender per jam.** Target Agustus–Oktober 2026 tetap 92 tanggal merah dan 2.208 jam kosong. Kalender lintas tahun dapat diperiksa tanpa memindahkan bukti ke tanggal lain.

## Bukti B yang tersedia tetapi tertahan

[Paper Jenggolo](https://e-jurnal.pnl.ac.id/portal/article/download/5567/pdf) menyediakan 49 nilai pada tujuh kelompok kelas selama 27 November–3 Desember 2023, pukul 06.00–18.00 WIB per hari. Nilai asli, tanggal yang diselesaikan dari nama hari dalam rentang eksplisit, URL, SHA, nomor tabel dan halaman disimpan. Jumlah nilai kelas adalah 15,478 kendaraan; ini bukan seluruh traffic Gedangan atau count per jam.

Kandidat dikirim melalui workflow impor sebagai OBSERVED_SECONDARY dengan kualitas B. Seluruhnya masuk quarantine karena interval 12 jam tidak memenuhi gate per jam. Hambatan lain juga dipertahankan: dua arah digabung, kelas ringan mencampur mobil/pickup/truk box, dan posisi segmen belum cocok ke edge. Tidak ada pembagian kelas/arah atau distribusi per jam yang dibuat untuk meloloskannya.

## Referensi C dan metadata D

V/C Dishub berisi 43 ruas untuk survei 2022. Tanggal 11 Januari 2023 pada surat adalah tanggal dokumen; tanggal/jam hitung tetap NULL. Volume Raya Sukodono 713,2 SMP/jam tidak menjadi 713 kendaraan/jam. XLS, PDF dan datastore adalah representasi dataset yang sama, bukan tiga survei independen.

Bab V UPN memuat hasil analisis untuk 16 Mei 2025. Raw count berada pada bagian yang belum dapat diakses secara sah. Dj dan tundaan hasil analisis tidak diubah menjadi raw traffic count atau sampel perjalanan individual.

Metadata BPS 2024/2026 tetap D. Jadwal pengumpulan 15–16 Agustus 2024 dan 7–17 Agustus 2026 tidak mengaktifkan tanggal. Tidak ditemukan count baru A/B yang dapat langsung dipetakan untuk Sedati/Jenggala, frontage, Ketajen, akses stasiun atau perlintasan rel.

Arsip B/C: `documentation/m13_1/reference-aggregates.json` dan `INSPECTED_AGGREGATES_NOT_HOURLY_OBSERVATIONS.csv`. Keduanya menunjuk hitungan sumber yang sama dengan kandidat quarantine, bukan hitungan tambahan untuk dijumlahkan. Verifikasi tersedia pada `partial-import.json` dan source register.
