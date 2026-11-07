# M04 internal browser QA — PASS

Tanggal: 31 Oktober 2026. URL: `http://127.0.0.1:5176/demand.html`. Pemeriksaan aktual melalui browser internal Codex, Vite dev server lokal. Build produksi diperiksa terpisah; tidak ada klaim deployment atau benchmark GPU.

Awalnya alat melaporkan browser disabled meskipun screenshot pengguna menunjukkan Browser aktif dan Browsing Always allow. Setelah pengguna menutup/membuka aplikasi, akses browser berhasil. Server preview ikut berhenti dan telah dijalankan kembali. Full CDP access dan izin sistem tidak diubah oleh agent. Kendala ini sudah resolved; penyebab teknis persisnya tidak dipastikan.

| Variant / profile | Requested | Routable | Failed | Departed / arrived | Teleports |
|---|---:|---:|---:|---:|---:|
| strict / low | 40 | 8 | 32 | 8 / 8 | 0 |
| strict / medium | 120 | 30 | 90 | 30 / 30 | 0 |
| strict / stress | 300 | 70 | 230 | 70 / 70 | 0 |
| strict / smoke | 90 | 5 | 85 | 5 / 5 | 0 |
| provisional / low | 40 | 16 | 24 | 16 / 16 | 0 |
| provisional / medium | 120 | 48 | 72 | 48 / 48 | 0 |
| provisional / stress | 300 | 120 | 180 | 120 / 120 | 0 |
| provisional / smoke | 90 | 9 | 81 | 9 / 9 | 0 |

Seluruh kombinasi dipilih melalui kontrol UI dan counts di atas teramati pada metrics panel, sesuai recorded run-summary. Label SYNTHETIC, NOT CALIBRATED, offline recorded, seed, network hash dan M05 NOT STARTED terlihat.

| Interaksi | Hasil |
|---|---|
| OD selection northbound provisional | PASS; car, 56 actual DUAROUTER edges, PROVISIONAL_ASSUMPTIONS dan source endpoints tampil |
| Zone anchor / OD schematic toggles | PASS; marker dapat dimatikan dan diagram OD diaktifkan/dipulihkan |
| NOT_ROUTABLE + heavy_truck filter | PASS; 9 baris coverage strict ditampilkan, izin gagal tetap terlihat |
| Car / strict station failure | PASS; destination Missing endpoint, 0 edges, ENDPOINT_EXCLUDED_BY_M03_POLICY |
| Vehicle registry | PASS; 10 kategori tampil, heavy truck detail sesuai registry, seluruhnya ASSUMPTION |
| QA & issues | PASS; empat issue M03, runtime/RAM/CPU dan lifecycle tampil |
| Play / pause | PASS; time 5s ke 290s dan actual marker coordinates berubah |
| Reset | PASS; kembali ke frame pertama 5s |
| Scrub | PASS; keyboard End mencapai frame terakhir 575s; Home/ArrowRight mencapai frame 105s |
| FCD position match | PASS; semua marker pada frame 290s cocok dengan x/y sumber SUMO (sumbu y SVG dibalik eksplisit) |
| 1920x1080 | PASS; clientWidth=scrollWidth=1905 pada capture akhir, tanpa overflow horizontal |
| 390x844 | PASS; layout menumpuk; clientWidth=scrollWidth=375, tanpa overflow horizontal |
| Console | Tidak ada warn/error pada tab viewer |

Screenshot aktual: browser-initial-1080.jpg, browser-provisional-route.jpg, browser-playback.jpg, browser-strict-failures.jpg, browser-strict-station-failure.jpg, browser-vehicle-registry.jpg, browser-mobile.jpg dan browser-final-m04.jpg. Hasil DOM/counters/posisi dan console tersimpan dalam browser-qa-results.json.

Screenshot full-page mencakup area di bawah viewport. Ukuran marker adalah ukuran display; tidak mengklaim render fisik kendaraan. Playback hanya rekaman FCD, bukan kendali live SUMO. Tidak ada perubahan source atau data simulasi untuk meluluskan QA browser. Viewport sementara dikembalikan ke default dan tab preview dipertahankan sebagai deliverable.
