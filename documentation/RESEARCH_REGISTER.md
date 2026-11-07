# Research Register

Ditinjau: 31 Oktober 2026. Referensi awal untuk menyusun pertanyaan penelitian. Tidak ada angka literatur yang diimpor menjadi parameter 2026.

## R01 · Kajian Rencana Pengendalian Simpang Gedangan Kabupaten Sidoarjo Jawa Timur

- Sumber primer: [repositori PTDI–STTD, record 8270](https://digilib.ptdisttd.ac.id/8270/).
- Metadata repositori menyebut Muhammad Rizky Bima Putra, Budiharso Hidayat, Luh Putu Widya Adnyani; 2024. Item bertanda Submitted; format peran penulis/pembimbing dan status publikasi perlu dicek pada naskah asli.
- Terbaca: metadata dan abstrak. Naskah penuh, rincian survei, metode, halaman dan validasi angka belum ditelaah.
- Relevansi: abstrak membahas hubungan dua simpang di kawasan Gedangan, pengaruh perlintasan kereta terhadap antrean, dan keberadaan frontage. Ini mendukung cakupan jaringan terhubung, tanpa membuktikan keadaan operasional 2026.
- Tindak lanjut: peroleh naskah lengkap, identifikasi tanggal survei dan perubahan jaringan, pisahkan nilai historis dari baseline, periksa asumsi palang dan sinyal.
- Status: ABSTRACT_CHECKED / NUMERIC_IMPORT_BLOCKED. Tidak ada volume, tundaan, kejenuhan atau kapasitas yang disalin.

## R02 · Studi Kelayakan Pembangunan Fly Over di Simpang Gedangan Sidoarjo Ditinjau dari Segi Lalu Lintas dan Ekonomi Jalan Raya

- Kandidat sumber primer: [Jurnal Teknik ITS, artikel 18895](https://ejurnal.its.ac.id/index.php/teknik/article/view/18895), DOI [10.12962/j23373539.v5i2.18895](https://doi.org/10.12962/j23373539.v5i2.18895).
- Penelusuran menemukan judul pada Jurnal Teknik ITS volume 5 nomor 2 (2016); metadata indeks mengarah ke Nanang Firmansyah dan Istiar. Tahun issue dan tanggal publikasi indeks dapat berbeda; cocokkan halaman penerbit/naskah.
- Akses halaman penerbit dan PDF penerbit gagal melalui alat baca saat M01. Metadata belum dikonfirmasi dengan naskah primer yang terbaca.
- Relevansi yang akan diperiksa: metode perbandingan sebelum/sesudah infrastruktur dan kelayakan. Tidak menjadi dasar memilih flyover atau menyatakan solusi efektif.
- Status: CANDIDATE / PRIMARY_FULLTEXT_PENDING / NUMERIC_IMPORT_BLOCKED.
- Tindak lanjut: peroleh salinan resmi, audit tahun survei, batas simpang, komposisi kendaraan, metode dan kondisi sebelum frontage sekarang.

## R03 · Eclipse SUMO / TraCI

- [Dokumentasi resmi TraCI Python](https://sumo.dlr.de/docs/TraCI/Interfacing_TraCI_from_Python.html), ditinjau untuk batas integrasi saja.
- Modul traci mengendalikan sesi SUMO; executable, konfigurasi jaringan dan handshake tetap dibutuhkan. Status paket terpasang tidak cukup untuk menyatakan mesin terhubung.
- Status: TECHNICAL_REFERENCE_CHECKED. Tidak ada sesi engine yang dijalankan M01.

## Kebutuhan sumber berikutnya

| ID | Data yang dibutuhkan | Sumber yang perlu ditelusuri | Status |
|---|---|---|---|
| D01 | Batas studi, node/edge/lane, frontage dan akses | survei lapangan, GIS berlisensi dan instansi pemilik jalan | belum tersedia |
| D02 | Volume per kelas/gerakan/periode dan OD | survei 2026 atau data resmi berkonteks | belum tersedia |
| D03 | Sinyal dan blocking antar simpang | pengamatan siklus aktual dan instansi terkait | belum tersedia |
| D04 | Event penutupan palang dan operasi stasiun | pengamatan bertimestamp, data operator berizin | belum tersedia |
| D05 | Penduduk, kendaraan, zona dan proyeksi | BPS/instansi relevan; seri tahun dan metode harus diperiksa | belum tersedia |
| D06 | Antrean, kecepatan, waktu tempuh untuk validasi | survei independen dari dataset kalibrasi | belum tersedia |

Jangan menganggap nama instansi di tabel sebagai data yang sudah diperoleh. Batas kawasan, CRS dan geometri belum ditetapkan pada M01.
