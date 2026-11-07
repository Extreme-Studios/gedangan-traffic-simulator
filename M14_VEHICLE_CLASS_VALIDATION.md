# M14 — Vehicle Class Validation

Tanggal laporan: 1 November 2026 (WIB). Semua jumlah demand adalah masukan eksperimen, bukan pengukuran Gedangan. Tidak ada klaim kalibrasi atau efektivitas rekayasa lapangan.

Staging: `http://127.0.0.1:5199/`. Build: `frontend/dist-m14/`. Jalankan ulang dengan `staging/m14/START_M14.ps1` dari proyek ini. SUMO lokal 1.28.0. Final M12 tidak ditimpa.

Jaringan eksisting: `simulation\network\m051\provisional\network.net.xml`. SHA-256: `0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c`. Tidak ada flyover, ruas baru, koneksi baru, vClass ignoring, atau override izin kendaraan TraCI. Pembatasan kelas/akses/geometri M04.5 tetap diterapkan; izin provisional dalam model bukan sertifikat legalitas atau swept-path lapangan.

## Parameter fisik nominal
| Tipe | SUMO class | L × W × H m | Max m/s | Accel/decel | Gap/tau |
| --- | --- | --- | --- | --- | --- |
| motorcycle | motorcycle | 2.1 × 0.8 × 1.4 | 16.67 | 2.0/4.0 | 1.0/1.2 |
| car | passenger | 4.5 × 1.8 × 1.5 | 22.22 | 2.0/4.5 | 2.5/1.2 |
| pickup_van | delivery | 5.2 × 1.9 × 2.1 | 19.44 | 1.8/4.0 | 2.5/1.2 |
| bus | bus | 12.0 × 2.5 × 3.5 | 16.67 | 1.2/4.0 | 3.0/1.2 |
| light_truck | truck | 6.5 × 2.1 × 2.6 | 16.67 | 1.3/4.0 | 3.0/1.2 |
| heavy_truck | truck | 11.5 × 2.5 × 3.8 | 13.89 | 0.9/4.0 | 3.0/1.2 |
| trailer | trailer | 16.5 × 2.55 × 4.0 | 13.89 | 0.8/4.0 | 3.5/1.2 |
| becak_nonmotor | bicycle | 2.6 × 1.2 × 1.6 | 3.5 | 0.45/1.5 | 1.2/1.5 |
| becak_motor | motorcycle | 2.7 × 1.25 × 1.7 | 8.3 | 0.8/2.5 | 1.2/1.5 |
| bicycle | bicycle | 1.8 × 0.65 × 1.5 | 5 | 0.7/2 | 1.2/1.5 |

M04 dipakai tanpa mengedit registry aslinya. Becak motor memiliki parameter nominal dan model 3D roda tiga sendiri, berbeda dari motor dan becak nonmotor. Izin becak motor mengikuti motorcycle, ditambah pemeriksaan ukuran modelnya sendiri. Semua dimensi/dinamika adalah asumsi teknis, bukan hasil ukur. Bicycle class tidak dibuka otomatis.

## Lifecycle aktual — manual 5 per tipe
Run `a668247fc301a9e4c8455827`, 900 detik; departure disebar pada 300 detik awal agar dapat mengamati arrival.

| Tipe | Diminta | Routed | Loaded | Departed | Moved | Arrived | Active |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Sepeda motor | 5 | 5 | 5 | 5 | 5 | 5 | 0 |
| Mobil pribadi | 5 | 5 | 5 | 5 | 5 | 5 | 0 |
| Pickup / van | 5 | 5 | 5 | 5 | 5 | 4 | 1 |
| Bus | 5 | 5 | 5 | 5 | 5 | 5 | 0 |
| Truk ringan | 5 | 5 | 5 | 5 | 5 | 4 | 1 |
| Truk berat | 5 | 5 | 5 | 5 | 5 | 5 | 0 |
| Trailer / gandeng | 5 | 5 | 5 | 5 | 5 | 5 | 0 |
| Becak nonmotor | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| Becak motor | 5 | 5 | 5 | 5 | 5 | 2 | 3 |
| Sepeda / kendaraan lambat | 5 | 0 | 0 | 0 | 0 | 0 | 0 |

Total 50 diminta, 40 memiliki rute; 10 sepeda/becak nonmotor tetap gagal. Unfinished trips dipertahankan. Trailer lulus pada rute utama yang memenuhi screen provisional M04.5; ini bukan izin untuk kendaraan oversize atau bukti swept path/legal permit. Tidak ada tipe oversize ditambahkan pada M14.

No recorded illegal lane permission, collision, teleport. Permission setiap kendaraan aktif diperiksa tiap langkah 0,5s, termasuk lane internal. Rute memakai koneksi yang diizinkan sumber. Bukti setiap ID: `simulation/runs/m14/a668247fc301a9e4c8455827/vehicle-results.json`, FCD dan tripinfo.
