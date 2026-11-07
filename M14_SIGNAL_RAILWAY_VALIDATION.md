# M14 — Signal and Railway Validation

Tanggal laporan: 1 November 2026 (WIB). Semua jumlah demand adalah masukan eksperimen, bukan pengukuran Gedangan. Tidak ada klaim kalibrasi atau efektivitas rekayasa lapangan.

Staging: `http://127.0.0.1:5199/`. Build: `frontend/dist-m14/`. Jalankan ulang dengan `staging/m14/START_M14.ps1` dari proyek ini. SUMO lokal 1.28.0. Final M12 tidak ditimpa.

Jaringan eksisting: `simulation\network\m051\provisional\network.net.xml`. SHA-256: `0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c`. Tidak ada flyover, ruas baru, koneksi baru, vClass ignoring, atau override izin kendaraan TraCI. Pembatasan kelas/akses/geometri M04.5 tetap diterapkan; izin provisional dalam model bukan sertifikat legalitas atau swept-path lapangan.

## Profil sinyal
Inherited controller `m05_gedangan`, 27 fase protected dalam jaringan eksisting. Baseline nominal 12s green + 3s yellow + 2s all-red untuk masing-masing 9 grup; cycle 153s. Editable duration dimuat ke SUMO lewat additional tlLogic, state fase dan link tidak diubah. Ini ASSUMED SIGNAL PROFILE, bukan timing Dishub resmi. `signals.json` berasal dari state controller TraCI pada setiap perubahan.

## Uji perubahan hijau 12s → 30s
| Konfigurasi | Run ID | Arrived | Mean wait s | Mean speed m/s | Max lane queue | Transitions |
| --- | --- | --- | --- | --- | --- | --- |
| baseline | d1e082fcef90bbf4822b8a36 | 72 | 376.6426 | 0.8206 | 31 | 168 |
| edited | 0668d56c5fc9ed43786b611c | 72 | 401.322 | 0.8179 | 30 | 85 |

Demand, rute dan seed sama; perubahan sinyal mengubah waktu tunggu dan transisi. Angka arrival sama tidak berarti lampu tidak berpengaruh. Tidak ada klaim setting baru lebih baik secara lapangan.

## Kereta dan perlintasan
Satu arah N_TO_S memakai rute rel M05.1 yang sudah tersambung. Reverse tidak ditambahkan. Jadwal pengguna merupakan EDITABLE ASSUMED SCHEDULE, bukan jadwal resmi. Arrival input dikonversi ke nominal departure bebas; aktualnya dapat berbeda karena akselerasi/kondisi rel. Kecepatan nominal = panjang 80m / input passing seconds; train body tetap 80m. Headway closing, opening delay/time dan minimum open/recovery diterapkan pada rail-crossing controller. Yellow closing inherited 3s. Recovery di sini parameter minimum terbuka, bukan pengukuran waktu antrean pulih.

## Uji dengan/tanpa 3 KA
| Konfigurasi | Run ID | Arrived | Mean wait s | Mean speed m/s | Max lane queue | Transitions |
| --- | --- | --- | --- | --- | --- | --- |
| with_train | 65494368cfb2b902480c9116 | 147 | 2.1219 | 7.609 | 2 | 172 |
| without_train | 92d833744559340cb03b22c8 | 147 | 0.0 | 7.895 | 1 | 160 |

Demand 160 mobil pada pendekat perlintasan, seed dan departure identik. Dengan KA mean waiting menjadi 2.1219s, tanpa KA 0.0000s. Max queue berubah 1 → 2. Ini bukti in-model pengaruh perlintasan terhadap antrean, bukan angka observasi lapangan. Crossing lane samples KA aktual tersedia pada audit XML independen; phase transitions, FCD dan tripinfo disimpan.

Dokumentasi teknis: [SUMO Traffic Lights](https://sumo.dlr.de/docs/Simulation/Traffic_Lights.html), [SUMO Railways](https://sumo.dlr.de/docs/Simulation/Railways.html). Sumber geometri rel: `simulation/network/m051/provisional/rail-provenance.json`; baseline parameter `configuration/railway-m05/pilot.json`.
