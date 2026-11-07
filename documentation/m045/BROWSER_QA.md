# M04.5 browser QA — PASS

Browser internal Codex, `http://127.0.0.1:5178/multiclass.html`, 31 Oktober 2026. Dev preview diperiksa langsung; production build diuji terpisah.

- Semua 16 family × variant × profile combinations berhasil dimuat dan menampilkan counts sesuai sumber original M04/corrected M04.5. Data original tidak ditulis ulang.
- Sepuluh kategori dipilih: motorcycle/car/pickup masing-masing 9/9 coverage provisional arrivals; minibus 6/9; bus, tiga ukuran truck dan trailer masing-masing 3/9; oversize 0/9.
- Frontage edge w160009748_s0_p0_0_f: light classes INFERRED ALLOW; bus/truck/trailer MISSING WITHHOLD. Request truck frontage NOT_ROUTABLE dan alasan terlihat.
- Arterial edge dipilih lewat route ledger: truck/trailer ASSUMPTION ALLOW pada provisional, status per class dan raw OSM source tags dapat diinspeksi.
- Search, permission/OD visibility, type/outcome filter dan route selection berfungsi.
- Playback 0s → 83s memperlihatkan motor, passenger, pickup, minibus, bus, truk dan trailer. Seluruh marker frame 83s cocok dengan FCD actual x/y (SVG y dibalik). Reset dan scrub End hingga 646s berhasil. Capture akhir memakai frame 65s.
- 1920×1080: clientWidth=scrollWidth=1905. 390×844: clientWidth=scrollWidth=375. Tidak ada overflow horizontal; viewport temporary telah direset.
- Console warn/error kosong. Detail hasil DOM/proof ada di browser-qa.json.

Screenshots actual: browser-initial.jpg, browser-frontage-permissions.jpg, browser-multiclass-playback.jpg, browser-mobile.jpg dan browser-final.jpg. Marker adalah ukuran display, bukan kendaraan 3D fisik. Playback tidak menjalankan live SUMO atau interpolasi acak. Tab preview dipertahankan untuk pengguna.

Final check: per-type lifecycle juga menampilkan loaded dari actual tripinfo, diurutkan sebelum departed/moved/arrived. Peringatan React createRoot yang muncul saat perubahan hot reload diperbaiki dengan menyimpan/reuse root pada host elemen M04.5. Setelah reload bersih dan interaksi ulang, console warn/error kosong; historical warning dipertahankan dalam browser-qa.json.
