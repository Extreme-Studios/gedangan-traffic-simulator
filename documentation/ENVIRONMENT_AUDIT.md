# Environment Audit

Audit: 31 Oktober 2026. Semua pemeriksaan sebelum implementasi bersifat read-only. Direktori proyek sudah ada dan kosong saat diperiksa, termasuk file tersembunyi. Tidak ada pekerjaan lama yang dihapus/ditimpa. Tidak ditemukan AGENTS.md tambahan pada direktori induk yang diperiksa; instruksi langsung pengguna berlaku.

## Sistem dan tool

| Komponen | Hasil aktual | Keterangan |
|---|---|---|
| Windows | Windows 11 Pro 10.0.26300, build 26300 | CIM Win32_OperatingSystem |
| Python | 3.12.10 | tersedia pada PATH |
| pip global | 25.0.1 | tidak memasang paket global |
| Node.js | 24.22.1 | tersedia; kompatibel dengan Vite yang dipasang |
| npm | 12.0.1 | tersedia |
| Git | 2.56.0.windows.1 | tersedia; tidak init/commit/push pada M01 |
| Eclipse SUMO | tidak ditemukan pada PATH atau registry uninstall yang diperiksa | SUMO_HOME tidak terisi; tidak mengklaim pencarian seluruh disk |
| TraCI / sumolib | import spec tidak ditemukan pada Python audit | tidak dipasang |
| Chrome | 156.0.8078.76 | executable ada, UI lokal diuji |
| Edge | registry uninstall mencatat 151.0.4129.78 | tidak diuji pada M01 |
| Blender | registry mencatat 5.2.2, lokasi Blender 5.2 | terpasang, bukan pada PATH; tidak diluncurkan |
| GPU | AMD Radeon Graphics, driver 32.0.31007.6002 | juga ada SuperDisplay Virtual Adapter; VRAM terdedikasi/alokasi 6 GB belum diverifikasi |
| RAM terpasang | 16 GiB, 4 modul × 4 GiB dari CIM | sesuai target kapasitas fisik |
| RAM terlihat OS | 12,568,088,576 byte, sekitar 11.70 GiB | alasan selisih/alokasi UMA tidak diverifikasi |
| Browser QA | window kecil lalu dimaksimalkan, capture 1280 × 696 | bukan benchmark/pengujian 1920 × 1080 |

## Dependensi awal dan akhir

Awal: folder proyek kosong, belum ada package manifest, node_modules, virtualenv. Python global tidak mempunyai traci, sumolib, fastapi, uvicorn atau jsonschema. FastAPI/uvicorn tidak dibutuhkan karena API foundation memakai standard library.

Akhir: dependency frontend terpasang lokal pada frontend/node_modules dengan package-lock.json. Versi aktual: React/React DOM 19.3.1, Three.js 0.180.0, Vite 7.3.7, TypeScript 5.9.3, @vitejs/plugin-react 5.2.0, @types/react dan @types/react-dom 19.3.0, @types/three 0.180.0. Paket sengaja memakai seri kompatibel, bukan memaksakan versi mayor terbaru untuk M01.

Virtualenv `.venv` khusus proyek memuat jsonschema 4.25.1 dan dependency pengujiannya. Daftar terpasang dikunci pada tests/requirements-lock.txt. API dapat berjalan dengan Python audit tanpa virtualenv atau pip runtime tambahan.

## Error, warning dan resolusi

1. npm awal berulang kali gagal `UNABLE_TO_VERIFY_LEAF_SIGNATURE`; metadata sempat memakai cache stale. Proses instalasi milik tugas dihentikan, lalu npm dijalankan dengan `node --use-system-ca` memakai trust store Windows. Registry ping/install/audit kemudian berhasil. Tidak mematikan strict-ssl/TLS dan tidak mengubah konfigurasi sistem/npm global.
2. npm 12 memberi warning bahwa postinstall esbuild tidak termasuk allowScripts. Tidak mengizinkan script global. Platform dependency yang terpasang cukup untuk build Vite, terbukti build berhasil.
3. Build memberi warning chunk >500 kB; bundle JS sekitar 741.68 kB (gzip 201.25 kB). Warning dicatat, tidak disembunyikan lewat menaikkan batas. Profiling/code splitting adalah pekerjaan optimasi mendatang bila diperlukan.
4. Satu pengulangan tes POST sempat gagal WinError 10054 meskipun handler mencatat 409. Request body belum dikonsumsi sebelum koneksi ditutup. Handler diperbaiki untuk membaca body terbatas sebelum menolak; pengujian ulang 18/18 PASS. Log sebelum perbaikan disimpan.
5. Akses sumber primer ITS melalui alat web gagal. Referensi tetap kandidat dan tidak menyumbang angka model.

## Instalasi dan perubahan yang dilakukan

Hanya dependency npm pada proyek dan dependency tes dalam `.venv`. Tidak memasang SUMO, TraCI, Blender, browser, Git, Node atau Python sistem; tidak memakai administrator; tidak mengubah registry/PATH/firewall; tidak membuat EXE atau melakukan deployment.

Untuk pemasangan ulang di lingkungan sertifikat yang sama, gunakan sesi PowerShell dengan `$env:NODE_OPTIONS = "$env:NODE_OPTIONS --use-system-ca"` sebelum `npm ci`, atau jalankan npm-cli melalui Node dengan flag tersebut. Ini memakai CA sistem, bukan menonaktifkan verifikasi.

Bukti lokal: evidence/environment.json, frontend-dependencies.txt, npm-audit.json, frontend-build.txt, schema-validation.txt, backend-tests.txt dan backend-tests-before-fix.txt. npm audit pada saat pemeriksaan melaporkan 0 advisory; bukan jaminan keamanan menyeluruh.
