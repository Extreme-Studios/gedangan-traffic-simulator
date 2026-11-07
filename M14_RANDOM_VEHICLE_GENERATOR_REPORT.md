# M14 — Random Vehicle Generator

Tanggal laporan: 1 November 2026 (WIB). Semua jumlah demand adalah masukan eksperimen, bukan pengukuran Gedangan. Tidak ada klaim kalibrasi atau efektivitas rekayasa lapangan.

Staging: `http://127.0.0.1:5199/`. Build: `frontend/dist-m14/`. Jalankan ulang dengan `staging/m14/START_M14.ps1` dari proyek ini. SUMO lokal 1.28.0. Final M12 tidak ditimpa.

Jaringan eksisting: `simulation\network\m051\provisional\network.net.xml`. SHA-256: `0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c`. Tidak ada flyover, ruas baru, koneksi baru, vClass ignoring, atau override izin kendaraan TraCI. Pembatasan kelas/akses/geometri M04.5 tetap diterapkan; izin provisional dalam model bukan sertifikat legalitas atau swept-path lapangan.

## Ketepatan dan reproduksi
Random composition memakai PRNG lokal dengan seed tersimpan, weighted physical draws (bukan PCU/SMP). Semua permintaan memiliki ID `m14_000000` dan seterusnya. Tidak ada kehilangan akibat pembulatan. Pendekat berbobot diacak secara reproducible. Pembagian belok exact dan histogram departure memakai largest remainder, tie-break stabil, lalu penempatan cohort diacak dengan seed yang sama.

Lima profil bobot editable diberi label ILLUSTRATIVE RANDOM PROFILE. Tidak ada klaim profil default mewakili komposisi Gedangan. Manual/random terpisah dari VERIFIED HISTORICAL OBSERVATION; M14 tidak memanggil penulisan database observasi.

## Contoh 3.000, seed 42
| Tipe | Jumlah |
| --- | --- |
| motorcycle | 2090 |
| car | 601 |
| pickup_van | 80 |
| bus | 29 |
| light_truck | 59 |
| heavy_truck | 41 |
| trailer | 0 |
| becak_nonmotor | 0 |
| becak_motor | 61 |
| bicycle | 39 |

Total tepat 3000. Departure 0–5/5–10/10–15 menit masing-masing 1.000 permintaan. Cohort SHA: `c4c61031a2941d04c367e488c6c419da1e1460460620f8fd859e79087714a019`. Seed identik menghasilkan cohort, kelas, pendekat, belok dan departure yang sama; seed 43 berbeda. ID unik dan konservasi diuji pada total 1, 7, 499, 500, 1.000, 2.998, 3.000 dan 5.000.

Setiap run menyimpan request, komposisi hasil, alokasi pendekat/belok, histogram, seed, registry dan network hash. Run final versi m14-2 juga menyimpan teks source snapshot, hash SUMO exe, source dependencies dan policy inspection. Output SUMO/config ditandai hash. Saved scenario baru menyimpan request beserta ringkasan hasil generator. Scenario lama yang disimpan sebelum penyempurnaan ini tetap reproducible dari seed dan request.

## Pengujian
`documentation/m14/m14-tests-final.txt`: 13 tes M14 lulus. Source request disimpan di `simulation/runs/m14/67e1a759e0845754c09be215/demand.json`. Profil adalah asumsi eksperimen; bukan hasil survei.
