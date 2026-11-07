# Browser QA · 31 Oktober 2026

Manual UI verification melalui Computer Use pada Google Chrome terpasang. Server dinyalakan oleh `python configuration/start_dev.py --no-browser`; browser diarahkan ke `http://127.0.0.1:5173`. Pemeriksaan ini menggunakan aplikasi yang benar-benar berjalan, bukan mock/screenshot desain.

| Pemeriksaan | Hasil yang diamati |
|---|---|
| Halaman lokal | judul Gedangan Traffic Simulator muncul |
| Three.js | canvas menampilkan pedestal hexagon, rings, core dan grid abstrak; THREE.JS / SCENE READY |
| Status | Backend terhubung; SUMO/TraCI belum tersedia; ENGINE NOT CONNECTED |
| Kontrol simulasi | Mulai simulasi disabled |
| Data aktual | label geometri belum tersedia, placeholder bukan jaringan aktual; metrik pada accessibility tree berupa em dash dan Menunggu hasil simulasi |
| Toggle grid | Grid on → Grid off; grid visual hilang, mesh tetap tampil |
| Orbit | drag pada canvas mengubah sudut pandang nyata |
| Reset kamera | klik reset mengembalikan sudut awal |
| Data & validasi | empat kategori dan penjelasan null tampil |
| Riset | judul/referensi dan tautan PTDI–STTD/ITS tersedia; tidak membuka tautan eksternal pada uji UI |
| Roadmap | 12 judul terbaca melalui accessibility tree, M02–M12 Belum dimulai |
| Navigasi kembali | workspace dan scene dapat ditampilkan kembali |

Browser awal terbuka pada window kecil; kemudian dimaksimalkan (capture 1280×696). Halaman dapat discroll untuk melihat area canvas/panel. Tidak dilakukan pengukuran viewport DOM, audit console lengkap, Edge, 1080p fisik, FPS/VRAM/baterai, pemutusan internet fisik, atau pengujian beban SUMO. Bukti visual dilihat langsung dalam sesi; tidak menyimpan screenshot browser/history pribadi ke proyek.
