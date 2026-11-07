# M13 — Historical Data Audit

Periode target: **1Agustus–31Oktober2026**, Asia/Jakarta. Audit menyelesaikan pemeriksaan isi **385 berkas lokal**: CSV/XLSX, read-only SQLite tables/JSON, source PDFs, OSM metadata, dan result SUMO. Duplicate build/export/backup tetap tercatat perfile dengan hash, bukan dianggap observasi independen. Pemeriksaan gagal sebelumnya karena parser belum tersedia diulang memakai bundled reader; final seluruh385lokal CONTENT_INSPECTED. Source register: [M13_DATA_SOURCE_REGISTER.csv](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/M13_DATA_SOURCE_REGISTER.csv>); rincian [source-file-audit.json](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/m13/source-file-audit.json>).

## Hasil aktual

- Tanggal punya observasi target: **0**. Tanpa observasi: **92 dari92**.
- Jam lengkap: **0**, parsial: **0**, kosong: **2208 dari2.208**.
- Ruas/arah/kelas teramati terverifikasi pada target: **tidak ditemukan dalam sumber yang diperiksa**. Seluruhparameter target tetap NULL/MISSING.
- 36 record asli publikasi2023 disalin ke DB M13 sebagai OBSERVED_SECONDARY dengan tanggal/lokasi sumber, arah UNSPECIFIED, review scope PENDING_REVIEW. Tidak dipetakan secara rekaan ke edge dan tidak masuk kalender2026.
- Distribusi file berdasarkan fungsi audit: {'OBSERVED_SECONDARY': 1, 'REFERENCE_STUDY': 15, 'SYNTHETIC_TEST': 157, 'SIMULATION_OUTPUT': 212}. Tag sumber pada file tidak otomatis menjadi bukti; tabel fixture dan synthetic-only workspaces tetap dikeluarkan.

## Pemeriksaan sumber publik

Unduhan XLS Dishub [identifikasi masalah lalu lintas](https://opendata.sidoarjokab.go.id/id/dataset/data-indentifikasi-masalah-lalu-lintas) berisi satu baris administratif dengan **satuan Dokumen**, nilai2023=1,2024=1,2025=0. Ini bukan jumlah kendaraan dan bukan data2026.

[Lampiran Dishub2023](https://opendata.sidoarjokab.go.id/dataset/2ed97d4c-cba0-4e5b-ba53-dc4e5d9ff48b/resource/ab78e87f-5332-4876-a6a3-7ef2d2816c79/download/outcome-visi-ratio-ruas-jalan-kab-sda-.pdf) menyatakan sumber survei2022, berunit SMP/jam; tanggal/jam arah count mentah target tidak tersedia. Bukan observasi2026.

[Kajian STTD](https://digilib.ptdisttd.ac.id/8279/1/Jurnal%20Kajian%20Rencana%20Pengendalian%20Simpang%20Gedangan%20M.Rizky%20Bima.P.pdf) kini berhasil diunduh dan diekstrak13halaman, memuat analisis2024 dan referensi2022. Tidak menyediakan tabel pencacahan bertanggal Agustus–Oktober2026. Tidak menyalin existing/model scenario numbers menjadi observations. Publication year tidak dianggap observation_date.

[Kusuma & Sholikhah](https://ejournal.undip.ac.id/index.php/ilmulingkungan/article/download/56951/pdf), Table1p927: sembilan jendela1jam Mei2023 ×4kelas; lokasi AhmadYani konteks Aloha. Diperiksa sebagai sumber historis terpisah, bukan pengganti count2026. OSM membuktikan atribut/geometri referensi, bukan volume kendaraan.

UMPR download masih502, directional2022 masih403; dicatat UNAVAILABLE, tidak menganggap halaman publikasi sebagai dataset yang sudah dimiliki. Pencarian publik bukan bukti bahwa data tidak ada di lembaga mana pun. Rincian URL/hash/akses: [web-source-audit.json](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/m13/web-source-audit.json>).

## Data yang perlu diminta / disurvei

Pencacahan asli1Agustus–31Oktober2026 per lokasi terpetakan/arah/kelas/interval15menit, dengan date-clock WIB, source permission, metode dan quality review. Prioritas06–10dan16–22WIB tetap MISSING. Minta Dishub data count mentah, turning counts, speed/travel-time samples, queue definition/timestamps, actual signal phases dan rail closure events; data geometri/OSM sendiri tidak memenuhi itu. Tidak ada pesan/permohonan yang dikirim atas nama pengguna pada pekerjaan ini.

