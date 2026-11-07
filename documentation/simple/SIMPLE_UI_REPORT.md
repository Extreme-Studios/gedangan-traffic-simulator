# Simulasi sederhana — 6 November 2026

UI hanya memiliki satu input jumlah kendaraan, 1–20.000. Komposisi otomatis diperbarui seketika; tombol Jalankan simulasi menghitung satu jam dengan SUMO 1.28.0 lalu memutar hasil aktual. Pengaturan detail dari UI lama tidak ditampilkan.

Komposisi asumsi: motor 65%, mobil 22%, angkot 6%, truk ringan 4%, truk berat 2%, trailer 1%. Pembulatan mempertahankan jumlah total tepat. Komposisi ini bukan pengukuran lalu lintas Gedangan. Angkot menggunakan parameter van sebagai proxy asumsi.

Pejalan kaki BELUM tersedia: network baseline tidak menyediakan jalur legal pedestrian. Tidak ada pedestrian dekoratif yang dihitung sebagai hasil simulasi. Trailer tetap terbatas pada rute yang lolos screening provisional terdahulu; tidak ada sertifikat swept path atau legalitas kendaraan oversize.

Uji SUMO nyata 20.000 permintaan selama satu jam: 19.574 mendapatkan rute, 426 ditolak, 3.569 berangkat dan bergerak, 2.891 tiba, 678 masih di jalan, 16.005 kendaraan yang memiliki rute masih menunggu masuk. Semua enam kategori bergerak. Tidak tercatat teleport, tabrakan, atau pelanggaran izin lane. Beban 20.000 tidak berarti seluruh kendaraan langsung tampil bersamaan: kapasitas dan antrean jaringan tetap berlaku. Waktu hitung pada mesin pengujian sekitar 440 detik.

SHA256 network baseline tetap 0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c. Tidak ada perubahan geometri, koneksi, atau bypass permission. Hasil belum terkalibrasi terhadap survei lapangan.

Validasi: TypeScript dan Vite berhasil. Input 20.001 ditolak. Pengujian UI browser dan EXE 100 kendaraan: 98 berangkat/bergerak, 92 tiba, 6 masih di jalan, 2 rute ditolak; keenam kategori bergerak. Pengujian paket ZIP terpisah dicatat pada dokumentasi proyek.

Implementasi baru berada di frontend/src/simple, backend/gedangan/simple_*.py, frontend/vite.simple.config.ts, frontend/tsconfig.simple.json dan staging/m1562/portable/{build_simple,host_simple,verify_simple}.py. Namespace dan runtime output dipisahkan dari M15.6.2 lama. Worker rekaman memeriksa panjang buffer dan mencoba ulang respons tidak lengkap.

Paket portable hasil ekstraksi ZIP lulus: EXE + Python/SUMO bawaan menjalankan 100 permintaan; enam kategori bergerak; input 20.001 ditolak; seluruh 60 chunk / 7.200 frame rekaman diunduh dan ukuran byte diverifikasi. Bukti ada di EVIDENCE/portable-qa.json dan EVIDENCE/simple-ui.png.
