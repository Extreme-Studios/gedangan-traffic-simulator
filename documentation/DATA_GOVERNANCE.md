# Data Governance

## Empat kategori wajib

| Kategori direktori | Makna | Aturan |
|---|---|---|
| observed_data | Survei/geometri terukur | cantumkan tanggal, periode, metode, cakupan, alat/petugas dan ketidakpastian |
| research_reference | Literatur atau dokumen resmi | catat tahun asli, metode, lokasi, halaman/tabel dan izin penggunaan |
| assumptions | Asumsi atau pengamatan awal belum terukur | nyatakan alasan, pembuat, keterbatasan; tidak dilabel sebagai pengukuran |
| simulated_results | Output model | cantumkan run/scenario/seed/hash/versi serta status kalibrasi |

Semua dataset M01 kosong. Register sumber awal berada dalam dokumentasi, belum menjadi record model. Keberadaan empat dataset kosong berarti struktur siap, bukan survei telah dilakukan.

## Provenance

data_provenance menyimpan source_title/URI/year, accessed_on, survey_period, method, spatial_scope, license_notes, verification_status, limitations. Record domain mereferensikan provenance_id. Satu dataset memuat satu kategori; validator menolak pencampuran kategori, ID ganda dan provenance yang hilang. Untuk penggunaan referensi lintas kategori kelak, registry versioned harus menelusuri sumber asal tanpa mengubah tipe sumber atau mengklaim validasi baru.

Pengamatan pengguna dari USER_BRIEF_M01.md (kapasitas alternatif belum memadai dan frontage relatif lancar) adalah kebutuhan penelitian/pengamatan awal belum diverifikasi; bukan nilai observed_data. Literatur yang membahas kondisi lain/tahun lama tetap research_reference. M01 tidak memindahkan angka literatur ke file demand, kapasitas atau pertumbuhan.

## Nilai tidak diketahui dan unit

Null berarti belum tersedia; [] berarti belum ada record. Tidak boleh mengganti keduanya dengan nol. Koordinat metrik memerlukan CRS; panjang m, kecepatan m/s di engine, durasi s, kepadatan kendaraan/km, kapasitas kendaraan/jam. UI masa depan boleh mengonversi km/jam atau menit hanya dengan konversi eksplisit. OD berisi jumlah perjalanan per kelas, zona asal/tujuan dan interval waktu. Definisi volume, arus dan kapasitas harus dibedakan.

Geometri jalan, lebar/jumlah lajur, kapasitas, pembagian belokan, dimensi kendaraan, perilaku, OD dan pola palang tidak mempunyai nilai default lapangan. Parameter display seperti camera/grid bukan data jalan.

## Pertumbuhan 2026 ke depan

baseline_year wajib 2026. growth_rates mempunyai year >= 2027, vehicle_class_id, zone_id, annual_rate dalam fraction_per_year dan provenance_id. Nilai tetap kosong pada M01. Rumus rencana: D(y,c,z) = D(2026,c,z) × ∏(1+r(t,c,z)), t=2027..y. Belum ada engine proyeksi pada M01.

Jika baseline OD, satu tahun pertumbuhan atau provenance tidak tersedia, proyeksi diblokir; jangan otomatis memakai nol atau satu persentase untuk semua kelas/zona. rate_for pada kerangka Python menolak missing/duplicate/undocumented/nonfinite rate. Korelasi penduduk, kepemilikan kendaraan, pergeseran moda dan kapasitas jaringan perlu metodologi tersendiri; pertumbuhan penduduk tidak otomatis sama dengan demand kendaraan.

## Kalibrasi dan review

Status: not_started → in_progress → calibrated, atau unverified → verified/rejected untuk record sumber/topologi. Verifikasi format tidak sama dengan verifikasi lapangan; calibrated tidak sama dengan validasi independen. Tabel calibration_status menyiapkan metode, sumber observasi/validasi, acceptance criteria dan reviewer. Semua baseline M01 NOT_STARTED.

M06 harus menetapkan ambang sebelum kalibrasi, memisahkan hari/periode kalibrasi dan validasi, serta mengevaluasi arus per gerakan/kelas, antrean, waktu tempuh dan penutupan palang. Jangan mengklaim keberhasilan berdasarkan kecocokan satu angka agregat. Simpan versi sumber mentah, transformasi dan audit trail; jangan menimpa data mentah.

## Batas validator M01

Schema memastikan bentuk dan unit melalui nama field, bukan kebenaran geografis atau ketersediaan sumber. Tidak memvalidasi isi URL, urutan periode, kualitas survei, timing SUMO atau semua referensi lintas dataset. Tidak ada proses persetujuan otomatis terhadap data ilmiah. Validator lanjutan harus ditambahkan bersama tipe data yang benar-benar diisi pada milestone berikutnya.
