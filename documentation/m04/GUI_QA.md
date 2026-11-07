# SUMO-GUI M04 — pemeriksaan aktual

SUMO-GUI 1.28.0 membuka provisional coverage smoke pada jaringan M03 yang tidak diubah. Output pemeriksaan diarahkan ke `documentation/m04/gui-*.xml`; output headless regresi tetap utuh. Run dijalankan dengan delay 150ms untuk inspeksi, lalu dijeda.

Vehicle Chooser menampilkan tujuh ID kendaraan aktif, termasuk fixture northbound, southbound, frontage, feeder dan junction. Salah satu kendaraan dipusatkan dan terlihat berwarna kuning di lane pada screenshot `sumo-gui-vehicle-paused.jpg`. Setelah run dilanjutkan, kendaraan meninggalkan area view yang sama, dan waktu simulasi meningkat; `sumo-gui-later-time.jpg` merekam view tersebut. Overview network direkam dalam `sumo-gui-network-context.jpg`.

Run GUI dihentikan untuk pemeriksaan pada waktu sekitar 169 detik, bukan sampai horizon 2.100 detik. GUI summary terakhir: loaded 9, inserted 9, arrived 2, running 7, waiting 0, collisions 0, teleports 0. Bukti kedatangan lengkap diperoleh dari delapan run headless yang selesai; tidak mengklaim GUI menuntaskan seluruh perjalanan.

`sumo-gui-vehicle-list.jpg` menunjukkan chooser dan ID aktual. Pemeriksaan ini membuktikan aplikasi memuat/menggerakkan passenger pada Gedangan; bukan bukti bus/truk/motor dapat melintasi lane passenger-only. Tidak ada network yang diedit atau izin yang diubah melalui GUI.
