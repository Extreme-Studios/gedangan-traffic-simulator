# M14 — Performance Benchmark

Tanggal laporan: 1 November 2026 (WIB). Semua jumlah demand adalah masukan eksperimen, bukan pengukuran Gedangan. Tidak ada klaim kalibrasi atau efektivitas rekayasa lapangan.

Staging: `http://127.0.0.1:5199/`. Build: `frontend/dist-m14/`. Jalankan ulang dengan `staging/m14/START_M14.ps1` dari proyek ini. SUMO lokal 1.28.0. Final M12 tidak ditimpa.

Jaringan eksisting: `simulation\network\m051\provisional\network.net.xml`. SHA-256: `0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c`. Tidak ada flyover, ruas baru, koneksi baru, vClass ignoring, atau override izin kendaraan TraCI. Pembatasan kelas/akses/geometri M04.5 tetap diterapkan; izin provisional dalam model bukan sertifikat legalitas atau swept-path lapangan.

## Lingkungan terukur
Microsoft Windows 11 Pro 10.0.26300. Adapter terdeteksi: SuperDisplay Virtual Adapter, AMD Radeon Graphics. RAM yang dilaporkan OS 11.70 GiB; bukan klaim seluruh 16GB tersedia untuk aplikasi. Browser melaporkan WebKit WebGL; deteksi adapter AMD oleh OS tidak membuktikan browser memakai adapter fisik tersebut. Target window 1920×1080; canvas lebih kecil karena toolbar. DPR dan viewport tersimpan per sampel.

## Eksekusi SUMO
| Demand | Routed | Loaded | Departed | Arrived | Active akhir | Belum berangkat | Gagal | Generation wall s | SUMO wall s | Total wall s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 500 | 481 | 481 | 481 | 237 | 244 | 0 | 19 | 3.125 | 24.157 | 27.297 |
| 1000 | 972 | 972 | 833 | 320 | 513 | 139 | 28 | 0.421 | 50.594 | 51.046 |
| 3000 | 2920 | 2920 | 1271 | 566 | 705 | 1649 | 80 | 0.453 | 74.891 | 75.687 |
| 5000 | 4876 | 4876 | 1475 | 737 | 738 | 3401 | 124 | 0.687 | 87.813 | 88.641 |

Wall times terukur pada satu mesin dengan pekerjaan lain berjalan; bukan benchmark mesin bersih, tidak menjanjikan durasi konstan. Generation time dan total_wall_s per run juga disimpan pada result JSON. Durasi 15 menit adalah waktu model, bukan waktu komputasi.

## Browser actual playback
| Demand | Sampel aktif | FPS min | FPS median | FPS max | Playback load s | Canvas px |
| --- | --- | --- | --- | --- | --- | --- |
| 500 | 3 | 106.46 | 110.56 | 110.58 | 0.362 | [1905, 953] |
| 1000 | 7 | 8.51 | 100.53 | 105.68 | 0.507 | [1905, 953] |
| 3000 | 21 | 1.05 | 1.47 | 97.11 | 0.797 | [1905, 953] |
| 5000 | 28 | 74.08 | 89.26 | 99.81 | 0.833 | [1905, 953] |
| 3000 (final v2) | 8 | 83.56 | 89.27 | 97.77 | 0.72 | [1905, 953] |

Sampel hanya saat Play aktif pada window 1920×1080; paused/warm-up tidak digabung. Min rendah dan stall tetap dimasukkan. File mentah menyimpan FPS mean, p5, draw calls, triangle count, visible/active sampled vehicles, visibility/focus dan waktu playback. Metrik merupakan render-loop timing browser, bukan FPS dari perekam video atau pengukuran AMD GPU hardware. Ada callback mendekati interval satu detik dalam sesi; pembatasan/occlusion browser mungkin berperan tetapi penyebabnya belum dibuktikan sepenuhnya.

## Optimasi dan batas klaim
Mesh kendaraan di-instance per tipe, kapasitas dihitung dari maksimum active per tipe pada rekaman. Gambar hanya instance aktif pada waktu terpilih. Playback dipaket gzip chunk 60 detik, concurrency fetch empat; data 0,5s disimpan tanpa animasi kendaraan dekoratif. Geometri static digabung, context massing opsional tidak dihitung saat dimatikan. Playback timing memakai elapsed wall clock agar stall tidak diam-diam mengubah multiplier waktu.

Aplikasi terbukti memproses 3.000/5.000 permintaan serta membuka hasil 3D aktual, tetapi jumlah kendaraan aktif mengikuti kapasitas jaringan, bukan total requested. FPS stabil sepanjang sesi dan performa khusus AMD 16GB/1080p belum disertifikasi. STATUS PERFORMANCE: CONDITIONAL, karena variasi dan stall browser masih tercatat. Data 3.000 tidak boleh dipresentasikan sebagai 3.000 kendaraan semuanya berhasil masuk.
