# M14 — Actual SUMO Execution

Tanggal laporan: 1 November 2026 (WIB). Semua jumlah demand adalah masukan eksperimen, bukan pengukuran Gedangan. Tidak ada klaim kalibrasi atau efektivitas rekayasa lapangan.

Staging: `http://127.0.0.1:5199/`. Build: `frontend/dist-m14/`. Jalankan ulang dengan `staging/m14/START_M14.ps1` dari proyek ini. SUMO lokal 1.28.0. Final M12 tidak ditimpa.

Jaringan eksisting: `simulation\network\m051\provisional\network.net.xml`. SHA-256: `0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c`. Tidak ada flyover, ruas baru, koneksi baru, vClass ignoring, atau override izin kendaraan TraCI. Pembatasan kelas/akses/geometri M04.5 tetap diterapkan; izin provisional dalam model bukan sertifikat legalitas atau swept-path lapangan.

## Benchmark aktual 900 detik
| Demand | Routed | Loaded | Departed | Arrived | Active akhir | Belum berangkat | Gagal | Generation wall s | SUMO wall s | Total wall s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 500 | 481 | 481 | 481 | 237 | 244 | 0 | 19 | 3.125 | 24.157 | 27.297 |
| 1000 | 972 | 972 | 833 | 320 | 513 | 139 | 28 | 0.421 | 50.594 | 51.046 |
| 3000 | 2920 | 2920 | 1271 | 566 | 705 | 1649 | 80 | 0.453 | 74.891 | 75.687 |
| 5000 | 4876 | 4876 | 1475 | 737 | 738 | 3401 | 124 | 0.687 | 87.813 | 88.641 |

Semua run memakai SUMO 1.28.0, step 0,5s, teleport disabled (`-1`), collision warn dengan logging; tidak ada route ignore-errors atau izin bypass. Loaded adalah event actual loaded, berbeda dari departed. Pending insertion tidak dihapus. Arrived hanya aktual tripinfo arrival nonnegative. Waiting at end adalah active road speed <0,3m/s pada langkah terakhir. Queue extent adalah span kendaraan berhenti per lane, bukan panjang antrean lapangan terkalibrasi.

## Konservasi dan audit
Requested = Routed + Failed. Routed = Departed + Not departed. Departed = Arrived + Active akhir. Seluruh persamaan diverifikasi. Audit independen membandingkan departure/arrival dengan tripinfo XML, unique IDs, actual connections, network hash, playback frame count dan seluruh output hash.

Final source v2 run `67e1a759e0845754c09be215`: 3000 → routed 2920, loaded 2920, departed 1271, moved 1271, arrived 566, active 705, not departed 1649, failed 80. Waktu SUMO 84.531s. Semua angka sama dengan cohort benchmark 3.000 sebelumnya, sehingga penyempurnaan screen becak tidak mengganti tujuan/demand.

## Output dan reproducibility
`simulation/runs/m14/67e1a759e0845754c09be215/run.sumocfg` dapat dijalankan oleh SUMO toolchain lokal. Request lengkap di `demand.json`; snapshot dan hash dependency di `source-snapshot.json`/`input-manifest.json`. Re-run Python request akan membangun run dengan source version yang aktif; seed dan cohort dapat diperiksa secara eksplisit. UI frontend terpisah dari runner; hasil yang ditampilkan berasal dari FCD/chunks aktual.

Run 120 menit benar-benar dieksekusi, bukan hanya validasi form: `7e574d4fb954f9ed77f0d6b4`, 100 requested, 98 routed, 98 departed, 96 arrived, 2 active. Wall 28.344s.

## Kegagalan pengembangan yang diperbaiki
Percobaan awal gagal schema XML additional; kemudian schema SUMO lokal ditambahkan. Uji trailer awal gagal karena metadata eligibility belum dibawa dari registry; metadata dipertahankan lalu tes diulang. Satu tes sempat membaca benchmark ketika daftar masih ditulis bertahap; final suite dijalankan setelah benchmark lengkap. Renderer juga diperbaiki saat pergantian recording: callback animasi lama sekarang menunggu jika ID recording tidak cocok dengan mesh buckets yang sedang terpasang. Pergantian sparse/full cohort diperiksa ulang di browser pada build final. Jejak kegagalan tetap disimpan, tidak disembunyikan sebagai successful run.
