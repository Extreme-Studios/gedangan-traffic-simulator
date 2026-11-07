# M14 — Route and Turning Validation

Tanggal laporan: 1 November 2026 (WIB). Semua jumlah demand adalah masukan eksperimen, bukan pengukuran Gedangan. Tidak ada klaim kalibrasi atau efektivitas rekayasa lapangan.

Staging: `http://127.0.0.1:5199/`. Build: `frontend/dist-m14/`. Jalankan ulang dengan `staging/m14/START_M14.ps1` dari proyek ini. SUMO lokal 1.28.0. Final M12 tidak ditimpa.

Jaringan eksisting: `simulation\network\m051\provisional\network.net.xml`. SHA-256: `0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c`. Tidak ada flyover, ruas baru, koneksi baru, vClass ignoring, atau override izin kendaraan TraCI. Pembatasan kelas/akses/geometri M04.5 tetap diterapkan; izin provisional dalam model bukan sertifikat legalitas atau swept-path lapangan.

## Koneksi tersedia
| Pendekat | Anchor SUMO | Gerakan tersedia |
| --- | --- | --- |
| ketajen | w266287927_s0_p0_0_f | straight |
| sukodono | w266287930_s0_p0_0_f | straight |
| southbound | w512351908_s4_p0_0_f | straight, left |
| northbound | w562358500_s16_p0_0_f | straight |
| frontage | w1181141358_s0_p0_0_f | straight |
| rail_crossing | w1240685448_s1_p1_0_f | straight |

Pendekat adalah anchor actual SUMO connection. Ujung rute diperpanjang sepanjang koneksi lurus berfungsi/nama sama, target sekitar 420m upstream/downstream; panjang aktual dapat berbeda. Origin, mandatory turn dan destination diperlihatkan di ledger. Ini katalog model terbatas, bukan survei seluruh belokan Gedangan.

Gerakan kosong/tidak legal tidak dibuat. Right/U-turn tidak ditambahkan untuk memuaskan demand. Tes permintaan northbound→right mempertahankan 10 ID sebagai gagal, tanpa penggantian tujuan. Exact approach harus berjumlah sama dengan demand; vehicle/approach/turn percentages harus 100. Turn nontersedia dinonaktifkan UI, dan backend tetap mencatat gagal jika request semacam itu dikirim.

Screen memeriksa permissions external/internal lane, explicit lane-to-lane connection, private/conditional access dan dimensi; heavy road-function serta trailer deflection screen inherited tetap dipakai. Frontage tetap route tersendiri. Akses slow tidak diperlebar.

## Bukti
`documentation/m14/route-compatibility.json`: 10 tipe × 6 pendekat × 4 gerakan. `network-catalog.json`, `vehicle-registry.json`, route-ledger di setiap run (`vehicle-results.json`). 11 run diperiksa terhadap XML actual dan output hashes; hasil `xml-independent-audit.json` serta `final-xml-audit.json`. Tidak ada perubahan geometri/koneksi/izin pada berkas baseline.
