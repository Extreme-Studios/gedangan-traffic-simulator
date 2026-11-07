# M04.5 SUMO-GUI — actual inspection

SUMO-GUI 1.28.0 menjalankan corrected provisional coverage dengan seed/config yang sama. Output GUI di-override ke gui-*.xml dalam folder dokumentasi agar output headless tetap utuh. Run dijeda sekitar waktu 104s lalu ditutup setelah inspeksi.

Vehicle Chooser memperlihatkan 26 kendaraan aktif dari berbagai kategori, termasuk motorcycle, pickup_van, minibus, bus, tiga ukuran truk dan trailer pada northbound/southbound. Screenshot `sumo-gui-multiclass-list.jpg` merekam ID aktual.

`m045_compat_provisional_northbound_heavy_truck` dipilih dan dipusatkan. Kendaraan terlihat pada lane arterial (`sumo-gui-heavy-truck.jpg`). Dialog parameter aktual (`sumo-gui-heavy-parameters.jpg`) menunjukkan lane `w35344052_s3_p0_0_f_0`, posisi 72,38m, speed 8,29m/s, odometer 553,57m dan depart delay 9s. Ini bukti kendaraan berat telah berangkat dan bergerak, bukan hanya route XML.

GUI summary terakhir: time 104s, loaded 41, inserted/running 26, arrived 0, waiting 0, collisions 0, teleports 0. Demand masa depan belum seluruhnya dimuat/berangkat ketika GUI dihentikan. Tidak mengklaim seluruh kendaraan tiba dalam run GUI pendek ini; arrival lengkap dibuktikan oleh delapan run headless yang berakhir di 2100s.

Tidak ada edit network, permission override, vClass ignoring, atau paksaan insertion melalui GUI. Proses GUI milik pemeriksaan ditutup; source M03/M04 dan run headless dipertahankan.
