# Browser inspection M03 — 31 Oktober 2026

Pengujian manual dilakukan di browser internal Codex pada `http://127.0.0.1:5175/network.html`, memakai Vite lokal. TypeScript dan build produksi diverifikasi terpisah; tidak ada klaim browser produksi/deployment atau benchmark perangkat.

| Pemeriksaan | Hasil |
|---|---|
| Strict/provisional switch | PASS; 225/241/323 dan 1022/1961/2043 sesuai ekspor aktual |
| WebGL | READY, SUMO EXPORT LOADED |
| Edge inspector melalui pencarian | PASS; w266287935_s0_p0_0_f, OSM way 266287935, source/from/to/status tampil |
| Klik lane pada canvas | PASS; w512351908_s2_p0_0_f dipilih melalui raycast |
| Frontage visibility | PASS; layer frontage dapat dimatikan dan dipulihkan |
| Nodes / junctions dan lane connections | PASS; checkbox dan layer diaktifkan |
| Arah lane, rail, crossing | Terlihat pada canvas; berasal dari ekspor dan overlay statis |
| Orbit, wheel zoom, reset, Core, Fit network | PASS secara visual |
| Route tests strict | 4 FOUND, 4 NOT_FOUND; rute gagal tidak bisa dipilih sebagai keberhasilan |
| Route tests provisional | 8 FOUND; northbound 56 edge ditampilkan putih dengan label provisional |
| Evidence | Keempat status dan penjelasan geometri engine/provenance tampil |
| Desktop 1920 x 1080 | innerWidth=scrollWidth=1920; tanpa overflow horizontal |
| Viewport bawaan sempit | Layout menumpuk, canvas dapat diklik/orbit/zoom; viewport override dikembalikan |
| Console sesudah reload terakhir | Tidak ada warn/error tertangkap; lihat browser-final-state.json |

Screenshot: browser-strict-inspector.jpg dan browser-provisional-network.jpg disimpan ulang setelah perubahan terakhir. Screenshot frontage-hidden dan route tests merekam interaksi sebelumnya pada jaringan dengan semantic hash yang sama. Tidak ada kendaraan atau executable SUMO yang dijalankan dalam browser.
