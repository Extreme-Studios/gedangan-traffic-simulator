# M09 — Walkthrough presentasi teknis

Pembuka: “Ini demonstrasi perangkat lunak berbasis jaringan Gedangan dan rekaman SUMO. Demand masih ilustratif. Kami belum mengklaim angka ini sebagai kondisi lalu lintas Gedangan yang terukur.”

| Bagian | Kamera / pilihan | Talking point dan tindakan |
|---|---|---|
| 01 Intro | Aerial master · 2026 S00 REFERENCE | Tunjukkan batas jaringan yang tersedia. Nama Gedangan adalah lokasi sumber geometri, bukan sertifikat semua input sudah tervalidasi. |
| 02 Area overview | Aerial master | Jalan, frontage dan rel dipisahkan pada model. Bangunan/vegetasi hanya konteks dekoratif; matikan layer bila membahas geometri sumber. |
| 03 Main road | Main corridor | Play lalu Pause. Kendaraan mengikuti FCD, memiliki siluet/dimensi kelas dan tidak bergerak acak. Gunakan Reverse dan Frontage untuk sisi lain. |
| 04 Railway | Railway crossing · sekitar 104,5–160 s | Play untuk melihat kereta melintas, state perlintasan menutup dan kendaraan jalan merespons. Barrier schematic mengikuti recorded state. Timing/clearance belum disurvei. |
| 05 Baseline | Gedangan intersection · 2026 S00 | Tunjukkan count aktif/berhenti versus kartu horizon. Failed route dan unfinished trips tetap dihitung; jangan menyebut 240 request sebagai volume lapangan. |
| 06 Future traffic | Main corridor · 2040 S00 REFERENCE | Pilih 2030, 2035 dan 2040 bila ingin menjelaskan transisi. Setiap tahun utama punya rekaman sendiri. Tabel demand bersyarat memakai asumsi growth M07. |
| 07 Congestion indicators | Intersection · 2040 | Bahas queue extent, waiting dan unserved; perhatikan batas cohort/censoring. HIGH 2040 dapat dipilih secara eksplisit, bukan sebagai kondisi masa depan yang pasti. |
| 08 Operational solution | Intersection · 2026 S01 REFERENCE | Jelaskan mekanisme alternatif timing APILL sintetis. Skenario operasional dipakai ulang dari M08; bukan rancangan pengaturan lampu aktual yang disahkan. |
| 09 Before / after | Split · 2026 S00 ↔ S01 | Kamera dan waktu sinkron, trajectory terpisah, cohort dan fixed horizon sama. Tunjukkan nilai/delta tanpa memilih pemenang kebijakan berdasarkan satu angka. |
| 10 Field requirements | Field Data | Tutup dengan kebutuhan count per kelas/arah, turning, OD, travel time, queue, signal/rail events, geometri dan validasi independen. M09 tidak mengubah status baseline empiris. |

Dalam mode presentasi gunakan tombol Next/Previous, ←/→, Space dan Escape. Fullscreen pada presentasi menyertakan talking points. Untuk pemilihan tahun/skenario bebas, keluar ke dashboard; seluruh kontrol ada di halaman.

Jika pilihan menampilkan NOT RUN / NOT SIMULATION READY / CONCEPT ONLY, jelaskan batas itu. Jangan mengatakan aplikasi telah mensimulasikan flyover atau underpass. Gunakan **Kembali ke baseline 2026** untuk kembali ke rekaman valid.

Penutup: “Visualisasi memudahkan kita membaca model dan membandingkan eksperimen yang sebanding. Efektivitas di lapangan baru dapat dinilai setelah survei, kalibrasi dan validasi independen.”
